# Handback — F033 · SESSION 3 CLOSE · rounds 9 through 12

> Written by the REVIEWER at the close of session 3 and applied by a worker,
> because the reviewer writes no work-tree file itself. It carries the round 12
> verdict and two reviewer prose slips. Operator amendment amend0827 rule 1: a
> verdict committed and pushed HERE is persisted, and is booked into
> `.agent/live_review.md` in the FIRST COMMIT of the next round that is happening
> anyway — never in a round of its own.

## Session

SESSION 3 of feature F033 · rounds 9, 10, 11 and 12 delegated · rounds so far 12.
The NEXT session is SESSION 4 of 7 against the amend0827 rule 6 soft limit.
The soft limit is NOT reached: 12 rounds of 25, 3 sessions of 7.

## Fortschritt

~72 % (T002's core complete: decision · subset · apply · failed-rollback truth ·
ledger · recorder · envelope seam. Open: the CLI command, the write door, T003) —
Schätzung.

## Range

`0ce3b71a52f229551be7a8bbafb0f405f80d6b8f`..`c4ad00c486beed780301b874d083860589c5bf44`
on branch `feature/f033-hunk-approval-v2`, pushed. Every round was gated by the
reviewer, which re-ran each round's own eight gates from scripts of its own,
reproduced every ordered reading, and re-ran every mutation with its own anchors
in its own disposable worktree before writing a verdict.

## Verdicts

| Round | Subject | Verdict | Ledger entry |
|-------|---------|---------|--------------|
| 9 | the failed-rollback truth · R-0740 | PASS | `Gate: F033 R9` at `c50b5ccf` |
| 10 | the hunk-decision ledger · R-0741 | PASS | `Gate: F033 R10` at `d48b4850` |
| 11 | the door's effect · DECISION F033 D4 | PASS | `Gate: F033 R11` at `62760bac` |
| 12 | the viewer-envelope seam | PASS | NOT YET BOOKED — see below |

## Round 12 verdict — PASS, and it is not yet in the ledger

The next round books it. All eight gates were re-executed by the reviewer at
`c4ad00c4` and every ordered reading reproduced. TRANSPORT: the C0a blob is 30167
bytes at sha256 `e15f5523…5fecf`, BYTE-IDENTICAL to the reviewer's own
pre-emission original, with ONE blob id `3bcfa06b` at C0b. THE RECORD APPEND at
`62760bac` reconstructs 1506343 plus one newline plus 6482 to 1512826, the
committed blob exactly, base a byte PREFIX, N COUNTED at 2, the last two
blank-line units equal to the slice's paragraphs IN ORDER, and THREE negative
controls placed inside the FIRST appended paragraph — whose BYTE span the
reviewer computed as 1506344 to 1511396, agreeing with the worker's — at its
start, its middle and two bytes from its end, all three rejected by BOTH readers.
THE LEDGER: registered 303 UNMOVED, `Done:` 47 lines over 45 distinct to 48 over
46 with the ADDED resolved id exactly `R-0742`, `Landed:` 15 UNMOVED with the
`Landed: R-0742` line still standing beside its new `Done:` paragraph, `Gate:`
128 to 129 with `^Gate: F033 R11 — ` exactly 1, `DECISION F033 D` 4 UNMOVED, and
the open set 258 to 257. THE PROSE FILES: `.agent/plan.md` byte-EQUAL at 2713
bytes over 49 lines, under the 50-line cap; `.agent/prose_slips.md` reconstructs
22079 plus one newline plus 927 to 23007. THE CODE AGAINST THE SPEC: `ruff` exits
0; the AST import set is twelve names, every one standard library or from
`diff_parser`, `hunk_approval` or `hunk_ledger`, with `hunk_apply`,
`source_apply`, `storage`, `subprocess` and `shutil` ALL ABSENT and `open(` and
`save_job` both 0, so DECISION F033 D4 survives this round MEASURED rather than
assumed; the two pre-existing constants are unchanged and `HUNK_RECORD_REFUSAL_NO_DIFF`
reads `no_diff_available`; `record_hunk_decision`'s signature is BYTE-IDENTICAL
to its signature at the base; and its extracted body is its docstring plus one
`return record_hunk_decision_from_view(...)` call, holding none of
`build_hunk_ledger`, `decide_hunk_approval`, `export_hunk_ledger` or `setdefault`
— so "one implementation, two doors" is a measurement and not a claim. THE
MUTATIONS were reproduced in the reviewer's own disposable worktree at `c4ad00c4`,
the import first proved to resolve inside it, each anchor asserted UNIQUE and the
module restored byte-identically after each: the UNMUTATED CONTROL is a real exit
0 at 15 passed against 9 at the base; skipping the availability refusal is exit 1
at 2 failed; defaulting `available` to False is exit 1 at 11 failed; checking
truncation before availability is exit 1 at 1 failed; and writing the record even
when the availability refusal fires is exit 1 at 2 failed. THE REVIEWER ALSO RAN A
MUTATION THE BLOCK NEVER ORDERED — making the text door hand the view door an
envelope marked unavailable — and it went RED at 10 failed, so the delegation
itself is pinned and not merely written. THE SUITES were re-run SERIALLY in the
primary checkout, every REAL exit 0: the recorder 15, the ledger 29, approval and
apply 41 together, `test_diff_view_source.py` 15, `tests/ui_server/test_command_channel.py`
106 and the canary 42. THE STRUCTURE: seven single-parent commits over the range
ending at C5 of 407, 256, 29, 4, 4, 94 and 153 insertions, every one under 500,
with the handback a further 340; the path set EQUALS the declared change set in
BOTH directions; residue 0 in all four targets against a 5 and 6 control;
`git ls-files .remedy-wt` 0; and ALL TWELVE do-not-touch paths byte-identical by
blob id, so the claim that the write door and the catalog are untouched is a
measurement.

## The worker's flag about the push transcript — examined and NOT a finding

The round 12 handback noted that its External-actions entry says "see the
transcript below" for a push that necessarily happens after the handback commit
is written. The reviewer read `docs/agents/handback_template.md` at `c4ad00c4`:
its `## External actions` section requires "command + outcome" and never a
transcript, and its `## Verification` section is scoped to "every gate the
round's paste block ordered", which a push is not. The template also already
carries the R-0149 carve-out for the commit that writes the handoff. So nothing
under `docs/` is wrong and no id is spent; the wording was the handback's own
choice, and the next handback should write the push as command plus outcome.

## Reviewer prose slips — for `.agent/prose_slips.md`, no id, no round of their own

2026-08-29 · F033 R12 · The block's Bundle line for C3 read "one dated line into
`.agent/prose_slips.md`" while its own SLIPSF033R12 slice carried TWO dated
paragraphs and G5 ordered the count without fixing it; the worker applied both
byte for byte under convention 1 and declared the disagreement, which is the
required behaviour, and the R12 append reconstructs exactly.

2026-08-29 · F033 R12 · The round 11 verdict recorded the recorder's AST import
set as eleven names and this round's is twelve, which reads as drift and is not:
`Mapping` was added for the `attempt_view: Mapping[str, Any]` annotation, it is
standard library, and the property the gate exists for — every entry stdlib or
one of the three allowed modules, all five forbidden names absent — is unchanged.

## What this session built

Four modules' worth of T002, every one mutation-proved by the reviewer in its own
worktree, and the architectural ruling the plan had carried unresolved for three
rounds.

| Path | What it decides | Tests |
|------|-----------------|-------|
| `packages/orchestration/hunk_apply.py` | landing, and the TRUTH when a rollback does not finish | 11 |
| `packages/orchestration/hunk_ledger.py` | the two axes: decision and landing | 29 |
| `packages/orchestration/hunk_decision_record.py` | recording a decision on the job, from text OR from the viewer's envelope | 15 |

DECISION F033 D4 rules that the write door RECORDS a hunk decision and never
applies one. It is not a preference: `hunk_apply` imports `source_apply`, and
`TestCommandDoorImportGuard`'s `_door_imports` collects DIRECT imports only, so a
door importing the seam would PASS the forbidden-module test while running the
applier inside an HTTP handler — defeating the guard by name rather than by
substance, with the suite staying green.

Findings R-0740 (Medium), R-0741 (Low) and R-0742 (Low) were raised, repaired and
resolved within this session. The open set is 257, down one from the 258 this
session opened with.

## Next expected action — SESSION 4, in this order

1. Read `.agent/STOP` from disk. If it exists, hand off and end (Phase 1 rule 1
   before rule 2 — finding R-0347).
2. Run the Open PR Gate. There was no open PR at the close of session 3.
3. The next round's FIRST commits book, into `.agent/live_review.md`, the round 12
   verdict above, and append the two prose slips. Neither buys a round of its own.
4. Then the round's real work, which is the plan's step 2: THE CLI COMMAND AND ITS
   HANDLER, TOGETHER. Measured by the reviewer at `624818e6`: `CATALOG` holds 340
   entries and `collect_all_handlers()` holds 340 handlers, so catalog entries
   without a handler number ZERO — no test asserts that invariant and nothing has
   ever broken it. `apps/cli/grouped.py` builds its argparse parsers FROM the
   catalog and dispatches by `command_id`, so an entry without a handler is
   reachable in help and answers `Error: no handler for <id>`. The entry belongs
   in the `patch` group beside `patch.approve` and `patch.apply`, its handler in
   `apps/cli/commands/patch.py`'s `COMMAND_HANDLERS`, and the handler calls
   `record_hunk_decision_from_view` on what `diff_view_source.build_diff_view`
   returns, then `storage.save_job`.
5. Only AFTER that, the write door. `UI_EXPOSED_COMMANDS` is a SUBSET of the
   catalog and is pinned at exactly two ids by `TestUiExposedCommands`, so
   exposure is impossible before step 4. `DOOR_METHODS` and `ALLOWED_IMPORTS` in
   `tests/ui_server/test_command_channel.py` are EQUALITY guards that must be
   widened in the SAME commit that adds the import, and
   `packages.orchestration.hunk_apply` joins `FORBIDDEN_MODULES` in that commit
   too, so the mistake DECISION F033 D4 forbids cannot be made silently later.

## Verification of THIS commit

None ordered beyond the reviewer's own: this commit rewrites `.agent/handoff.md`
and nothing else. The worker applying it runs the canary
`pytest tests/cli/test_golden_path.py -q` and reports its REAL exit code, checks
`.agent/STOP` before and after, and leaves `git status --porcelain` empty.
