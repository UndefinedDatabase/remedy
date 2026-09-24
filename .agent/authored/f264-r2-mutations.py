"""F264 R2 G5 — mutation red-proofs of the cockpit's `chat.send` route, in a DISPOSABLE worktree.

Usage: python3 -B mutations.py <worktree-path>. The worktree must be at the round's test commit.
Each mutation's FROM text is asserted to occur EXACTLY ONCE in its file before it is applied,
the file is restored byte-for-byte after each, and an unmutated control runs first and last.
pytest runs under `python3 -B`, so no bytecode cache can serve a stale module (checklist item 18).
"""
import pathlib
import subprocess
import sys

WT = pathlib.Path(sys.argv[1]).resolve()
TESTS = ["tests/ui_server/test_command_dispatch.py::TestChatSendDispatchEffects",
         "tests/ui_server/test_command_channel.py"]
UI = "packages/orchestration/ui_server.py"
MUTATIONS = {
    "m1_route_never_dispatched": (
        UI,
        'CHAT_SEND_COMMAND_ID = "chat.send"\n',
        'CHAT_SEND_COMMAND_ID = "chat.sent"\n',
    ),
    "m2_door_records_the_wrong_channel": (
        UI,
        'job_state=state, channel="cockpit")\n',
        'job_state=state, channel="cli")\n',
    ),
    "m3_message_shape_unchecked": (
        UI,
        "        if command == CHAT_SEND_COMMAND_ID:\n",
        "        if False:\n",
    ),
    "m4_write_failure_read_as_ended_job": (
        UI,
        "        except SteeringWriteError:\n            raise\n",
        "",
    ),
    "m5_ended_job_read_as_write_failure": (
        UI,
        "        except SteeringError:\n            return None\n",
        "        except SteeringError:\n            raise\n",
    ),
    "m6_route_not_exposed": (
        "apps/cli/command_catalog.py",
        '    "chat.send",\n})\n',
        "})\n",
    ),
}


def run(label: str) -> None:
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TESTS],
                       cwd=WT, capture_output=True, text=True)
    keep = [ln for ln in r.stdout.splitlines()
            if ln.startswith("FAILED") or " passed" in ln or " failed" in ln]
    print(f"{label} REAL_EXIT={r.returncode}")
    print("\n".join(keep))


run("control_before")
for name, (rel, frm, to) in MUTATIONS.items():
    path = WT / rel
    good = path.read_bytes()
    text = good.decode("utf-8")
    print(f"{name} FROM count in {rel}: {text.count(frm)}")
    if text.count(frm) != 1:
        sys.exit(f"{name}: FROM must occur exactly once; stopping")
    path.write_text(text.replace(frm, to, 1), encoding="utf-8")
    run(name)
    path.write_bytes(good)
    print(f"{name} restored byte-identical: {path.read_bytes() == good}")
run("control_after")
