# F275 R60 — `f275_r60_probe.py`, the DECISION F272 D7 descriptor probe narrowed to `Task.status`

> Committed verbatim because DECISION F275 D35 rests on what it recorded, and because the
> figures on `.agent/f275_t003_flip_residue_r60.md` are reproducible only by re-running it.
> It is round 53's instrument — committed at `.agent/authored/f275-r53-probe.py.md` — with
> ONE line changed, its `DESCRIPTORS` tuple, so the three defects that instrument's own
> docstring records are not re-introduced. Run it as a pytest plugin from OUTSIDE the
> worktree, reached through `PYTHONPATH`: copied INTO a worktree it is scanned by
> `ruff check .` and turns `tests/orchestration/test_ci_budgets.py` red, which this round
> reproduced once before moving it out.
> It is a `.md` and not a `.py` for that same reason.

```python
"""F275 R53 — the DECISION F272 D7 descriptor probe, RECORDING disposition, WIDENED.

Loaded as a pytest plugin with `-p f275_r60_probe`. It installs a class-level
`property` over the FOUR classic-record fields the flip's attribute rename moves:
`Job.id`, `Job.name`, `Task.id` and `Task.description` (DECISION F275 D25 maps
`description` onto `TaskEntry.title`). Round 31's probe carried the `Job` pair only.

Three defects it must not have, each found at round 31 by RUNNING it. (1) BOTH HALVES:
a getter-only descriptor raises at every write site, so the suite dies before reaching
its remaining sites. (2) WALK OUTWARD: pydantic dispatches assignment through its own
`__setattr__`, so a fixed frame depth attributes every write to pydantic. (3) A FILENAME
IS NOT A PATH: `os.path.abspath("<string>")` resolves UNDER the current directory, so an
abspath-based containment test accepts a dataclass's synthetic `__init__` frame; this
probe qualifies a frame only when its RAW `co_filename` is already absolute.
"""
import json
import os
import sys

# The worktree root is passed IN and never derived from `__file__`: this plugin is
# imported from a gitignored scratch directory, because a `.py` file anywhere `ruff
# check .` scans is counted by `tests/orchestration/test_ci_budgets.py` and turns the
# lint-ceiling test red — measured, as a leftover probe at the worktree root.
ROOT = os.path.realpath(os.environ["R60_ROOT"])
OUT = os.environ["R60_PROBE_OUT"]
DESCRIPTORS = (("Task", "status"),)

RECORDS: dict = {}
_FILE_CACHE: dict = {}
_PREFIX = ROOT + os.sep


def _classify(filename):
    """True only for a REAL absolute path under the worktree root (defect 3)."""
    hit = _FILE_CACHE.get(filename)
    if hit is None:
        if isinstance(filename, str) and os.path.isabs(filename) \
                and filename.startswith(_PREFIX):
            hit = (True, filename[len(_PREFIX):])
        else:
            hit = (False, filename)
        _FILE_CACHE[filename] = hit
    return hit


def _record(owner, field, mode):
    frame = sys._getframe(2)          # 0 = _record, 1 = getter/setter, 2 = caller
    if frame is None:                 # pragma: no cover - defensive
        return
    innermost, direct, chosen, f = frame, None, None, frame
    while f is not None:
        qual, rel = _classify(f.f_code.co_filename)
        if direct is None:
            direct = qual
        if qual:
            chosen = (rel, f.f_lineno, f.f_code.co_name)
            break
        f = f.f_back
    if chosen is None:
        _, rel = _classify(innermost.f_code.co_filename)
        chosen = (rel, innermost.f_lineno, innermost.f_code.co_name)
    key = (owner, field, mode, bool(direct)) + chosen
    RECORDS[key] = RECORDS.get(key, 0) + 1


def _make(owner, field):
    def getter(self, _o=owner, _f=field):
        _record(_o, _f, "read")
        return self.__dict__[_f]

    def setter(self, value, _o=owner, _f=field):
        _record(_o, _f, "write")
        self.__dict__[_f] = value
        # what pydantic's own no-`validate_assignment` path does
        self.__pydantic_fields_set__.add(_f)

    return property(getter, setter)


def install():
    from packages.core import models
    if not _classify(models.__file__)[0]:
        raise RuntimeError("f275_r60_probe: packages.core.models resolves OUTSIDE "
                           "the worktree root %s -> %s" % (ROOT, models.__file__))
    for owner, field in DESCRIPTORS:
        cls = getattr(models, owner)
        if field not in cls.model_fields:
            raise RuntimeError("f275_r60_probe: %s has no field %r" % (owner, field))
        setattr(cls, field, _make(owner, field))


install()


def pytest_report_header(config):
    import packages.core.models as m
    return ["f275_r60_probe: root=%s" % ROOT,
            "f275_r60_probe: models=%s" % m.__file__,
            "f275_r60_probe: inside_root=%s" % _classify(m.__file__)[0],
            "f275_r60_probe: out=%s" % OUT]


def pytest_sessionfinish(session, exitstatus):
    rows = [{"owner": k[0], "field": k[1], "mode": k[2], "direct": k[3],
             "path": k[4], "line": k[5], "func": k[6], "count": v}
            for k, v in RECORDS.items()]
    rows.sort(key=lambda r: (r["owner"], r["field"], r["mode"], r["path"],
                             r["line"], r["func"], r["direct"]))
    with open(OUT, "w") as fh:
        json.dump({"root": ROOT, "exitstatus": int(exitstatus), "rows": rows},
                  fh, indent=1)
```
