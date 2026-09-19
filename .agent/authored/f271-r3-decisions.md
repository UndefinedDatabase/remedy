
## DECISION F271 D3 (2026-09-19, reviewer, round 3) — T002: closure precondition 7 and the planted dead command; R-0982: patch_revert is deleted
CONTEXT: T2_F271.md T002 asks for precondition 7 in `docs/roadmap/STATUS_closure_protocol.md` and
for a `remedy doctor core` fixture that plants a dead command and sees it listed; Design (d) asks
that the closure protocol cite the AGENTS.md rule "Replacing is deleting" beside precondition 7.
Read at `8bacb0fc`: the dead-command section already exists — F281 landed it in `_cmd_doctor_core`
of `apps/cli/commands/worker_facade_cmd.py` over `packages/orchestration/dead_command_check.py`,
with tests that see it empty — and a comment there leaves the planted-command red proof to F271.
The rule "Replacing is deleting" sits under AGENTS.md's `## 🎯 Scope Control`, not under Core
Workflow as the feature file's DECISIONs section says. No test pins the closure protocol's
precondition count. Finding R-0982: `patch_revert.py` has no importer outside `tests/`, the
`patch.revert` command routes through `revert_repository_apply()`, and the module is the only
writer of `patch_intent_reverted`, which `change_set.py`, `project_brain.py`,
`autonomy_readiness.py` and `ui_server.py` read.
CHOSEN: (1) PRECONDITION 7, appended after precondition 6: no new module outside the reachable
set unless its feature file names it; the reachability test and the orphan-module test are green
in the transcript precondition 2 reads, so the reviewer re-runs nothing there; a line a feature
adds to either list is named in its feature file; and the rule is cited as AGENTS.md's Scope
Control rule "Replacing is deleting", not restated. The feature file's Core Workflow wording is
corrected in its Built State at closure. (2) THE PLANTED DEAD COMMAND. No production change: a
test helper monkeypatches the catalog module's `CATALOG` with one extra entry and
`collect_all_handlers` with a handler that references no name. Its group and command ids are
minted from a uuid at run time, because the scan reads `tests/` and a literal id in the test file
would count as a reference. The JSON test asserts `dead_commands` equals exactly that command,
and the text test asserts it is the section's only line. The comment in `_cmd_doctor_core` that
leaves this to F271 is rewritten to name the test. (3) THE DELETION. `patch_revert.py` goes, with
the five `TestPatchRevert` tests that exercised only it. `test_brain_has_patch_revert_node` keeps
the brain's revert-node coverage by planting the event after a real apply, and gains an assertion
on the `ET_REVERTED_BY` edge. The `ALLOWED_UNWIRED` entry goes. Section 12q of
`scripts/remedy_smoke.sh` loses the check for `patch_snapshots/<intent>`, a directory only the
deleted module wrote, which printed OK on both of its branches. The four readers of
`patch_intent_reverted` stay: they read run logs already on disk. The brain's `patch_revert` node
type and its labels are a data shape, not the module, and stay.
ALTERNATIVES: a production seam to inject a catalog into `doctor core`, rejected because
monkeypatching the two module attributes reaches the real scan unchanged; deleting the event's
readers with the writer, rejected because run logs written before the deletion still carry the
event and the brain and change-set views read them.
REVERSE: remove precondition 7, the two planted-command tests and their helper, and restore the
comment, `patch_revert.py`, the five tests, the fixture, the allowance and the smoke lines from
`8bacb0fc`; then delete this paragraph.
