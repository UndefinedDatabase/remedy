"""F009 T002 — the per-job command nonce store.

DECISION F009 D8 fixes the store's path, its create-only publication and the replay window;
DECISION F009 D15 rules that only an accepted command publishes, that the door's lookup runs
before the rate limit, and that a nonce is validated as the FILENAME it becomes. These tests
hold the store to the two properties a replay guarantee is worthless without: the first
answer wins even under a race, and nothing a client can spell escapes the job's directory.
"""
from __future__ import annotations

import json
import stat as _stat
import threading
from pathlib import Path

import pytest

from packages.common import secure_fs as _fs
from packages.orchestration.command_nonce import (
    NONCE_DIRNAME,
    NONCE_FIELD_ORDER,
    lookup_nonce_result,
    nonce_is_valid,
    publish_nonce_result,
)
from packages.orchestration.safe_points import job_control_dir

JOB = "a1b2c3d4e5f60718"
NONCE = "nonce-0001"
BODY = {"status": "queued", "command": "job.stop", "job_id": JOB}

# Everything a client can spell that must never become a path component. The 65-character
# case is one past `_ID_RE`'s ceiling, which is where an off-by-one would hide.
UNUSABLE_NONCES = (
    "../escape",
    "",
    "a" * 65,
    "with/slash",
    "..",
    ".",
    "-leading-dash",
    "has space",
    "nul\0byte",
    None,
    17,
)


@pytest.fixture
def control(tmp_path: Path) -> Path:
    """A control root of our own. Nothing here touches the developer's real data dir."""
    return tmp_path / "control"


def nonce_dir(control_root: Path, job_id: str = JOB) -> Path:
    return job_control_dir(job_id, control_root) / NONCE_DIRNAME


def record_path(control_root: Path, nonce: str = NONCE, job_id: str = JOB) -> Path:
    return nonce_dir(control_root, job_id) / f"{nonce}.json"


# -- publication and lookup ------------------------------------------------------------


def test_a_published_body_reads_back_byte_equal(control: Path) -> None:
    """Byte equality, not just object equality: the record is what a later reader parses."""
    published = publish_nonce_result(JOB, NONCE, BODY, status=501, control_root_path=control)
    assert published == {"status": 501, "body": BODY}

    found = lookup_nonce_result(JOB, NONCE, control_root_path=control)
    assert found == published
    assert _fs.json_bytes(found["body"]) == _fs.json_bytes(BODY)
    assert found["status"] == 501


def test_the_record_is_private_and_under_the_jobs_control_directory(control: Path) -> None:
    publish_nonce_result(JOB, NONCE, BODY, status=200, control_root_path=control)

    path = record_path(control)
    assert path.exists()
    assert path.parent == control / "jobs" / JOB / NONCE_DIRNAME
    assert _stat.S_IMODE(path.stat().st_mode) == 0o600


def test_the_record_carries_the_status_first_in_the_ruled_order(control: Path) -> None:
    """Not the parsed keys — the ORDER the bytes carry, which is what a reader sees."""
    publish_nonce_result(JOB, NONCE, BODY, status=429, control_root_path=control)

    line = record_path(control).read_bytes().decode()
    assert tuple(json.loads(line).keys()) == NONCE_FIELD_ORDER
    positions = [line.index(f'"{field}"') for field in NONCE_FIELD_ORDER]
    assert positions == sorted(positions), f"fields are out of order: {line}"


def test_a_second_publish_of_one_nonce_returns_the_first_body(control: Path) -> None:
    """D8's whole contract: a seen nonce answers with the ORIGINAL result, forever."""
    first = publish_nonce_result(JOB, NONCE, BODY, status=501, control_root_path=control)
    before = record_path(control).read_bytes()

    second = publish_nonce_result(JOB, NONCE, {"status": "different"}, status=200,
                                  control_root_path=control)

    assert second == first
    assert record_path(control).read_bytes() == before
    assert lookup_nonce_result(JOB, NONCE, control_root_path=control) == first


def test_two_different_nonces_coexist(control: Path) -> None:
    one = publish_nonce_result(JOB, "nonce-one", {"n": 1}, status=200,
                               control_root_path=control)
    two = publish_nonce_result(JOB, "nonce-two", {"n": 2}, status=501,
                               control_root_path=control)

    assert one != two
    assert lookup_nonce_result(JOB, "nonce-one", control_root_path=control) == one
    assert lookup_nonce_result(JOB, "nonce-two", control_root_path=control) == two
    assert sorted(p.name for p in nonce_dir(control).iterdir()) == [
        "nonce-one.json", "nonce-two.json"]


def test_a_nonce_is_scoped_to_its_own_job(control: Path) -> None:
    other = "b9c8d7e6f5a40312"
    publish_nonce_result(JOB, NONCE, BODY, status=501, control_root_path=control)

    assert lookup_nonce_result(other, NONCE, control_root_path=control) is None


def test_an_unpublished_nonce_is_a_miss(control: Path) -> None:
    publish_nonce_result(JOB, "nonce-published", BODY, status=501,
                         control_root_path=control)

    assert lookup_nonce_result(JOB, "nonce-never-seen", control_root_path=control) is None


def test_a_job_with_no_control_directory_is_a_miss(control: Path) -> None:
    """The read path must not CREATE anything, so a lookup can never litter this host."""
    assert lookup_nonce_result(JOB, NONCE, control_root_path=control) is None
    assert not control.exists()


def test_a_job_with_no_nonce_store_is_a_miss(control: Path) -> None:
    """The control directory exists but nothing was ever published into it."""
    publish_nonce_result(JOB, NONCE, BODY, status=501, control_root_path=control)
    for path in sorted(nonce_dir(control).iterdir()):
        path.unlink()
    nonce_dir(control).rmdir()

    assert lookup_nonce_result(JOB, NONCE, control_root_path=control) is None


def test_an_unreadable_record_is_a_miss_and_never_raises(control: Path) -> None:
    """A record that cannot answer a replay is treated exactly as an absent one."""
    publish_nonce_result(JOB, NONCE, BODY, status=501, control_root_path=control)
    record_path(control).write_bytes(b"{not json at all")

    assert lookup_nonce_result(JOB, NONCE, control_root_path=control) is None


def test_a_record_without_a_usable_status_is_a_miss(control: Path) -> None:
    publish_nonce_result(JOB, NONCE, BODY, status=501, control_root_path=control)
    record_path(control).write_bytes(json.dumps({"body": BODY}).encode())

    assert lookup_nonce_result(JOB, NONCE, control_root_path=control) is None


# -- the character class ---------------------------------------------------------------


def test_a_plain_nonce_is_valid() -> None:
    assert nonce_is_valid(NONCE) is True
    assert nonce_is_valid("a") is True
    assert nonce_is_valid("a" * 64) is True


@pytest.mark.parametrize("nonce", UNUSABLE_NONCES)
def test_an_unusable_nonce_is_refused_by_every_entry_point(nonce, control: Path) -> None:
    """Refused by BOTH functions: a validator only one caller consults guards nothing."""
    assert nonce_is_valid(nonce) is False
    assert publish_nonce_result(JOB, nonce, BODY, status=501,
                                control_root_path=control) is None
    assert lookup_nonce_result(JOB, nonce, control_root_path=control) is None
    assert not control.exists(), "a refused nonce must leave nothing behind"


def test_an_invalid_job_id_is_refused_without_raising(control: Path) -> None:
    assert publish_nonce_result("../escape", NONCE, BODY, status=501,
                                control_root_path=control) is None
    assert lookup_nonce_result("../escape", NONCE, control_root_path=control) is None
    assert not control.exists()


# -- the race --------------------------------------------------------------------------


def test_concurrent_publishers_of_one_nonce_all_receive_the_same_body(
        control: Path) -> None:
    """The loser of the `os.link` returns the WINNER's record, so no client sees its own.

    Every thread publishes a DIFFERENT body under the same nonce, so a store that let the
    last writer win would hand back several distinct answers. The barrier makes the threads
    contend rather than run in sequence, and the assertion is on the set of results, never
    on which thread won — that is the server's choice to make.
    """
    publishers = 8
    ready = threading.Barrier(publishers)
    results: list[dict | None] = [None] * publishers

    def publish(index: int) -> None:
        ready.wait(timeout=10)
        results[index] = publish_nonce_result(
            JOB, NONCE, {"publisher": index}, status=500 + index,
            control_root_path=control)

    threads = [threading.Thread(target=publish, args=(index,))
               for index in range(publishers)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=30)
        assert not thread.is_alive(), "a publisher never finished"

    assert all(result is not None for result in results)
    unique = {json.dumps(result, sort_keys=True) for result in results}
    assert len(unique) == 1, f"publishers disagreed on the answer in force: {unique}"
    assert results[0] == lookup_nonce_result(JOB, NONCE, control_root_path=control)
    assert len(list(nonce_dir(control).iterdir())) == 1
