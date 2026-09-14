# F275 R65 — the receiver-keyed descriptor probe, saved verbatim as an authored blob

Its extension is `.md` and that is load-bearing: a `.py` file anywhere `ruff check .` scans
is counted by `tests/orchestration/test_ci_budgets.py`, whose ceiling this round gates on.

```python
"""F275 R65 — the DECISION F272 D7 descriptor probe, RE-KEYED BY RECEIVER.

Identical to `f275_r53_probe.py` in every respect except what it RECORDS. That probe's key
was `(owner, field, mode, direct, path, LINE, function)`, and
`.agent/f275_t003_descriptor_sites.md` records the consequence in its own words: "This
python is 3.10, so a frame carries no column and the probe's key is `(path, line)`. Where
one line holds two same-named attributes on different receivers the probe cannot separate
them." That is finding `R-0880`, and DECISION F275 D38 rules the route taken here.

THE KEY GAINS TWO FIELDS, `lasti` AND `recv`. `f_lasti` is the byte-code offset of the
instruction the chosen frame is executing, which differs between two attribute loads on one
line where `f_lineno` does not. `recv` is that offset resolved back to a receiver NAME by
disassembling the chosen frame's own code object, and it is None wherever the resolution
refuses — which it does, deliberately, in three cases:

  (1) the instruction at the offset is not a `LOAD_ATTR` of this field at all, which is what
      an outward walk through pydantic's dispatch leaves behind;
  (2) it is, but no name-load precedes it in the same code object, so there is no name;
  (3) the receiver is a subscript, a call or another attribute, so the instruction before
      the load is not a name load — `.agent/f275_t003_flip_residue_r64.md` section 5
      enumerates the nine sites of that shape among the at-risk lines.

A None `recv` is a REFUSAL and never a guess. The three defects `f275_r53_probe.py`'s own
docstring names — both halves of the descriptor, the outward walk, and an absolute
`co_filename` test — are unchanged and are not re-described here.

Loaded as a pytest plugin with `-p f275_r65_probe`.
"""
import dis
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("R65_PROBE_OUT", os.path.join(ROOT, "r65_probe_sites.json"))
DESCRIPTORS = (("Job", "id"), ("Job", "name"), ("Task", "id"), ("Task", "description"))
NAME_LOADS = ("LOAD_FAST", "LOAD_GLOBAL", "LOAD_DEREF", "LOAD_NAME")

RECORDS: dict = {}
_FILE_CACHE: dict = {}
_RECV_CACHE: dict = {}
_PREFIX = ROOT + os.sep


def _classify(filename):
    """True only for a REAL absolute path under the worktree root."""
    hit = _FILE_CACHE.get(filename)
    if hit is None:
        if isinstance(filename, str) and os.path.isabs(filename) \
                and filename.startswith(_PREFIX):
            hit = (True, filename[len(_PREFIX):])
        else:
            hit = (False, filename)
        _FILE_CACHE[filename] = hit
    return hit


def _receiver(code, lasti, field):
    """The NAME loaded as the receiver of the attribute load at ``lasti``, or None.

    Cached per code object: the disassembly is the expensive half and a code object's
    instructions do not change. None is a refusal, never a guess.
    """
    table = _RECV_CACHE.get(code)
    if table is None:
        table = {}
        prev_name = None
        for ins in dis.get_instructions(code):
            if ins.opname == "LOAD_ATTR":
                table[ins.offset] = (ins.argval, prev_name)
                # the value on the stack is now an ATTRIBUTE, not a name, so a second
                # `LOAD_ATTR` in a chain like `outcome.job.id` has no name receiver
                prev_name = None
            elif ins.opname in NAME_LOADS:
                prev_name = ins.argval
            else:
                prev_name = None
        _RECV_CACHE[code] = table
    hit = table.get(lasti)
    if hit is None:
        return None
    attr, name = hit
    if attr != field:
        return None
    return name


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
            chosen = (rel, f.f_lineno, f.f_code.co_name, f.f_lasti,
                      _receiver(f.f_code, f.f_lasti, field))
            break
        f = f.f_back
    if chosen is None:
        _, rel = _classify(innermost.f_code.co_filename)
        chosen = (rel, innermost.f_lineno, innermost.f_code.co_name,
                  innermost.f_lasti,
                  _receiver(innermost.f_code, innermost.f_lasti, field))
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
        raise RuntimeError("f275_r65_probe: packages.core.models resolves OUTSIDE "
                           "the worktree root %s -> %s" % (ROOT, models.__file__))
    for owner, field in DESCRIPTORS:
        cls = getattr(models, owner)
        if field not in cls.model_fields:
            raise RuntimeError("f275_r65_probe: %s has no field %r" % (owner, field))
        setattr(cls, field, _make(owner, field))


install()


def pytest_report_header(config):
    import packages.core.models as m
    return ["f275_r65_probe: root=%s" % ROOT,
            "f275_r65_probe: models=%s" % m.__file__,
            "f275_r65_probe: inside_root=%s" % _classify(m.__file__)[0],
            "f275_r65_probe: out=%s" % OUT]


def pytest_sessionfinish(session, exitstatus):
    rows = [{"owner": k[0], "field": k[1], "mode": k[2], "direct": k[3],
             "path": k[4], "line": k[5], "func": k[6], "lasti": k[7], "recv": k[8],
             "count": v}
            for k, v in RECORDS.items()]
    rows.sort(key=lambda r: (r["owner"], r["field"], r["mode"], r["path"],
                             r["line"], r["lasti"], r["func"], r["direct"]))
    with open(OUT, "w") as fh:
        json.dump({"root": ROOT, "exitstatus": int(exitstatus), "rows": rows},
                  fh, indent=1)
```
