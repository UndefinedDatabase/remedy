
## DECISION F271 D1 (2026-09-19, reviewer, round 1) — every command group names its owning feature and its reach; builder_eval is deleted
CONTEXT: DECISION amend0905-vocab D11 (a) asks that every command group in the catalog name its
owning feature and its reach, and that a catalog test refuse a group without both. Measured at
`a4f79a94`: `GroupDef` in `apps/cli/command_catalog.py` has `id`, `label`, `description`,
`user_facing`, `hidden` and `aliases`; `GROUPS` holds 30 groups; no test checks ownership; and
`tests/cli/test_cli_ux.py` builds `GroupDef` positionally with three and five arguments, so a
field without a default placed before `user_facing` breaks those tests, and one placed after the
defaulted fields cannot exist in a dataclass. DECISION amend0911-feedback D6 orders
`builder_eval.py` deleted with `tests/orchestration/test_builder_eval.py` and
`scripts/remedy_builder_eval.sh`; the only other references at `a4f79a94` outside `.agent/` and
`docs/roadmap/` are one line of `REAL_OLLAMA_FILES` in `tests/conftest.py` and a paragraph of
`docs/system/project-brain.md` telling the reader to run that script.
CHOSEN: (1) SHAPE. `apps/cli/command_catalog.py` gains `Reach`, a `Literal` of the seven reaches
D11 (a) names — golden-path, job-path, mission-path, self-use, teacher, cockpit, self-build — and
`GroupDef` gains, after `aliases`, `feature: str = ""` and `reach: Reach | None = None`. The
defaults exist so that a group missing either is refused by the test, as D11 (a) requires, and not
by a `TypeError` at import that would red every test importing the catalog. (2) THE TEST.
`tests/test_command_catalog.py`, beside `TestCatalogIntegrity`, refuses a group whose `feature` is
not `F` and three digits, whose `feature` has no line `- [<mark>] <id> — ` in
`docs/roadmap/STATUS.md`, or whose `reach` is not one of `Reach`'s values; a second test plants
bad groups and asserts the exact refusals. (3) OWNERS. A group's owner is the feature that
introduced it or most of its commands, read from the commit that added the group and from the
feature files that name its commands; where neither names one, the owner is F261, whose DECISION
amend0905-vocab D4 kept the group. The annotation at round 1: do F268, status F147, decision F051,
init F081, job F260, run F261, project F146, ui F261, doctor F254, config F081, worker F280,
memory F266, teacher F255, runtime F007, stats F010, patch F033, test F261, brain F261, mission
F056, change F261, file F261, event F261, blocker F051, self F257, dev F261, ci F083, integrity
F261, snapshot F261, study F266, roadmap F080. Reaches: golden-path for do, status, decision,
init, project, doctor, config and worker; job-path for job, run, runtime, stats, patch, test,
change, file, event, blocker and snapshot; mission-path for mission; teacher for memory, teacher
and study; cockpit for ui and brain; self-use for self; self-build for dev, ci, integrity and
roadmap. (4) THE DELETION. One commit removes the three files D6 names, the
`REAL_OLLAMA_FILES` line and the project-brain paragraph with its command block, which becomes one
sentence saying confidence rises only as the project's jobs run their builder on a real model;
the proof is a repository grep at zero outside `.agent/` and `docs/roadmap/`. No stub, no copy.
ALTERNATIVES: required fields without defaults, rejected by the dataclass ordering and the
positional test calls measured above; owners guessed from group names, rejected because the
owner is a claim a later closure relies on; keeping `builder_eval.py` until the orphan-module
test lands, rejected because D6 already rules its deletion and waiting buys nothing.
REVERSE: remove `Reach`, the two fields, their 30 annotations and `TestGroupOwnership`, restore
the three deleted files, the conftest line and the project-brain paragraph from `a4f79a94`, and
delete this paragraph.
