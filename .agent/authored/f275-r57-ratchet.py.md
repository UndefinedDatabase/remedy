# F275 R57 — `tests/orchestration/test_uuid_record_ratchet.py`, the ratchet D33 wants

> Committed verbatim as the authored source of a TEST FILE, so the file that lands
> under `tests/` is a copy of reviewer-authored bytes and not a retype. DECISION F275
> D33 makes this the last commit of the seven, in the shape DECISION F274 D1 set for
> the reachability test: a RATCHET over the LIVE class objects, with its own
> discriminator so that a green reading cannot come from a broken matcher.

```python
"""The one-world id shape is a `str`, and no record outside the classic pair may say UUID.

DECISION F275 D33 (finding `R-0878`): DECISION F275 D26's premise P2 selected records with
`issubclass(obj, BaseModel)`, so seven production DATACLASSES declaring a UUID-typed job or
task id were invisible to it and survived two migration rounds. This is the RATCHET that
stops the eighth arriving the same way, in the shape DECISION F274 D1 set for the
reachability test: it reads the LIVE class objects rather than source text, because an
annotation can be spelled `UUID`, `uuid.UUID` or `"UUID"` and only the object settles it.
"""
import dataclasses
import importlib
import inspect
import pkgutil

import pytest
from pydantic import BaseModel

#: The classic record defines the id shape the one world replaces; it keeps its UUIDs
#: until the flip deletes it, and `pingpong_job` holds the unified record it becomes.
CLASSIC_MODULES = {"packages.core.models", "packages.orchestration.pingpong_job"}

#: Records carrying a UUID id the flip does NOT feed, ruled out of scope by DECISION
#: F275 D33. Each entry is (module, class, field) and each is there for a stated reason.
ALLOWED = {
    # A memory entry's id is minted by the memory store and never by a job or a task.
    ("packages.memory.models", "MemoryEntry", "id"),
    # A project id is the registry's own; DECISION F275 D33 leaves it until a feature
    # gives a reason to move it.
    ("packages.orchestration.project_registry", "RemyProject", "id"),
}

#: The field names the one world spells as a 16-hex `str` (DECISION F260 D2).
ID_FIELDS = ("job_id", "task_id", "id")


def _uuid_fields(obj):
    """Every field of one class whose ANNOTATION names UUID, read from the live object."""
    if inspect.isclass(obj) and issubclass(obj, BaseModel) and obj is not BaseModel:
        return [n for n, i in obj.model_fields.items() if "UUID" in str(i.annotation)]
    if dataclasses.is_dataclass(obj):
        hints = getattr(obj, "__annotations__", {})
        return [f.name for f in dataclasses.fields(obj)
                if "UUID" in str(hints.get(f.name, f.type))]
    ann = getattr(obj, "__annotations__", None)
    if inspect.isclass(obj) and ann:
        return [n for n, a in ann.items() if "UUID" in str(a)]
    return []


def _walk():
    """Yield (module_name, class, uuid_field) for every class under packages/ and apps/."""
    for pkg_name in ("packages", "apps"):
        pkg = importlib.import_module(pkg_name)
        for m in pkgutil.walk_packages(pkg.__path__, pkg_name + "."):
            try:
                mod = importlib.import_module(m.name)
            except Exception:
                continue
            for obj in vars(mod).values():
                if not inspect.isclass(obj):
                    continue
                if getattr(obj, "__module__", "") != m.name:
                    continue
                for field in _uuid_fields(obj):
                    yield m.name, obj, field


class TestNoRecordOutsideTheClassicPairDeclaresAUuidId:
    def test_no_uuid_typed_job_or_task_id_survives(self):
        offenders = sorted(
            f"{module}.{obj.__name__}.{field}"
            for module, obj, field in _walk()
            if field in ID_FIELDS
            and module not in CLASSIC_MODULES
            and (module, obj.__name__, field) not in ALLOWED
        )
        assert offenders == [], (
            "these records declare a UUID-typed id the one world spells as a str; "
            "retype the field and its readers, or add it to ALLOWED with a reason: "
            + ", ".join(offenders)
        )

    def test_the_matcher_can_see_a_uuid_field_at_all(self):
        """The discriminator. Without it the test above passes on a broken matcher."""
        from packages.core.models import Job

        assert "id" in _uuid_fields(Job), (
            "the matcher cannot see `Job.id`, which IS a uuid.UUID, so a green "
            "no-offenders reading proves nothing"
        )

    def test_the_classic_modules_are_exempt_and_would_otherwise_offend(self):
        """The exemption is load-bearing, not decorative: prove it is carrying something."""
        classic = [
            f"{module}.{obj.__name__}.{field}"
            for module, obj, field in _walk()
            if field in ID_FIELDS and module in CLASSIC_MODULES
        ]
        assert classic, "no classic record declares a UUID id, so CLASSIC_MODULES is dead"


class TestNoModuleReadsAUuidMethodOffAnIdField:
    """The other half of the retype, and the half a type annotation cannot hold.

    Retyping `RunTaskResult.task_id` to `str` does not stop a reader calling `.hex` on
    it: annotations are not enforced, so the only thing that fails is the run. The one
    such reader, `task_runner.materialize_task_output`, became `str(...)[:8]`, which is
    the identity for a `str` and equals `.hex[:8]` for a `UUID` — the canonical string
    of a UUID begins with its first eight hex digits. This keeps the unsafe form out.
    """

    def _reads(self):
        import ast
        import subprocess

        out = subprocess.run(["git", "ls-files", "packages/*.py", "apps/*.py"],
                             capture_output=True, text=True).stdout
        for rel in (p for p in out.split() if p):
            try:
                tree = ast.parse(open(rel, "rb").read(), filename=rel)
            except (SyntaxError, OSError):
                continue
            for node in ast.walk(tree):
                if (isinstance(node, ast.Attribute)
                        and node.attr in ("hex", "int", "urn")
                        and isinstance(node.value, ast.Attribute)
                        and node.value.attr in ("job_id", "task_id")):
                    yield f"{rel}:{node.lineno}  .{node.value.attr}.{node.attr}"

    def test_no_uuid_only_method_is_read_off_a_job_or_task_id(self):
        offenders = sorted(self._reads())
        assert offenders == [], (
            "these read a UUID-only method off an id the one world spells as a str; "
            "use `str(x)[:n]`, which is correct for both shapes: " + ", ".join(offenders)
        )

    def test_the_matcher_can_see_such_a_read_at_all(self):
        """The discriminator, on a source this repository really contains."""
        import ast

        tree = ast.parse("x = result.task_id.hex[:8]")
        found = [n for n in ast.walk(tree)
                 if isinstance(n, ast.Attribute) and n.attr == "hex"
                 and isinstance(n.value, ast.Attribute)
                 and n.value.attr == "task_id"]
        assert found, "the matcher cannot see `result.task_id.hex`, so a green reading "                       "of the test above proves nothing"


@pytest.mark.parametrize("module,name,field", sorted(ALLOWED))
class TestEveryAllowlistEntryStillExists:
    def test_the_entry_names_a_real_uuid_field(self, module, name, field):
        """An allowlist entry that no longer matches anything is a silent hole."""
        live = {(m, o.__name__, f) for m, o, f in _walk()}
        assert (module, name, field) in live, (
            f"ALLOWED names {module}.{name}.{field}, which is not a UUID-typed field "
            "any more — remove the entry rather than leaving it to cover a future one"
        )
```
