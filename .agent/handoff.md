# Handback — F037 Rendered diff viewer, round 27 (THE CLOSURE)

## Session

SESSION 8 of feature F037 · round 27 · rounds so far 27

This session's rounds: R25 (PASSED), R26 (PASSED) and R27, this one, which ends
the session and the feature. The round is permitted past the 25-round and
seven-session soft limits of operator amendment amend0827-process-diet rule 6 by
that amendment's rule 1, which names a feature's CLOSURE SEQUENCE as the one
exception to the ban on bookkeeping-only rounds.

SCOPE REPORT, carried because both soft limits are exceeded (rule 6):

- FINISHED. T001 the unified-diff parser, T002 the diff source and the two read
  endpoints, T003 the client row model, file sidebar, hunk collapse, intraline
  emphasis and virtual scrolling — all built, all tested, all named with their
  test files in the Built State section of `docs/roadmap/features/T5_F037.md`.
  The integration gate PASSED at R25; the evidence bundle and the READY package
  were built and verified at R26; this round flips STATUS to `[x]`, syncs README
  and opens the PR.
- MISSING, and deliberately so per DECISION F037 D11 and amendment A6: the
  highlighting WIRING (the lazy language model ships complete, tested and
  UNWIRED), the 10k-line end-to-end perf measurement, and a ruling on the
  sidebar's visual treatment.
- PROPOSAL, unchanged from R24 and R26 and executed by no session: the split-off
  scope of A6 wants its own STATUS line immediately before F033. Rule 6 forbids a
  session executing a STATUS split on its own authority, so only F037's own line
  changed in `docs/roadmap/STATUS.md` this round.
- REMAINING WORK ON F037: none. The feature is CLOSED; only the merge of its PR
  remains, and that belongs to the next feature's Open PR Gate.

## Range

Review of `6a32be79..HEAD`.

## Commits

### 314159ab docs(agent): save the F037 R27 closure block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f037-r27.md` | +286 / -0 | C0a — the block saved verbatim |

### ae1b8b2c docs(agent): mirror the R27 block into last_block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +211 / -415 | C0b — same bytes, one blob with C0a |

### c640a996 docs(agent): retarget the plan at the F037 closure

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +21 / -23 | C1 — the PLANF037R27 slice, rewritten not appended |

### 7d84971b docs(review): book the R26 verdict on the closure package

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +12 / -0 | C2 — GATER26, appended |

### C3 docs(roadmap): close F037 with the rendered diff viewer

| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/STATUS.md` | +1 / -1 | P1 — the `[~]` line rewritten to the `[x]` closure line |
| `README.md` | +7 / -2 | P2 the accepted count and `Next:` clause, P3 the Tier 5 row, P4 the F037 capability paragraph |
| `.agent/handoff.md` | +263 / -308 | C4-equivalent — this file; it is written INSIDE C3, which the block orders as ONE commit |

C3's short SHA cannot appear in this table: the table is written into the commit
it describes. Its per-path `+/-` cells were measured with
`git diff --cached --numstat` over the fully staged C3 content immediately before
the commit was made, which is the same reading `git diff --numstat` gives after
it, and the total insertion figure is repeated in G8 below. The C3 SHA is
reported in this round's session output (R-0149 pattern; a handoff cannot table
the commit that writes it).

## External actions

| Command | Outcome |
|---------|---------|
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | `[]` — no open PR, so no duplicate is created and nothing was merged |
| `git ls-files .remedy-wt` | 0 lines — the scratch directory never entered the index |
| `git push -u origin feature/f037-rendered-diff-viewer` | Runs immediately AFTER the commit that writes this file; outcome in the session output, see the note below |
| `gh pr create --base main --title "F037 — Rendered diff viewer"` | Runs after the push. The PR is CREATED and NOT MERGED. Its number cannot exist when this text is written; it is reported in the session output |

No merge of this or any other PR. No force-push, no history rewrite, no work on
`main`.

THE PUSH AND PR OUTCOMES ARE NOT STATED HERE, deliberately. Both necessarily
happen after the commit that writes this file, so any value printed here would be
one that could not exist when the text was written, and the write-once rule
forbids a second handoff commit to fill it in. The reviewer can measure both
directly: `git rev-parse HEAD` equals
`git rev-parse origin/feature/f037-rendered-diff-viewer` if and only if the push
succeeded, and `gh pr list --state open` names the PR.

## The closure record

| Field | Value |
|-------|-------|
| Evidence job | `f037-closure` |
| package | `remedy-review-20260828-142213-READY_FOR_REVIEW.zip` |
| SHA-256 | `c3755b73a6cbaf21cd0547ce590aafee244d4143ace6ca1833bc93b50c87ef26` |
| package path | `/home/decodeux/Repos/remedy-history/zips` |
| accepted HEAD | `5e557a1c2b4f7f9187f5388b18a3712d4a5c3d7e` |

All five come from the R26 handback and have no other source; they are carried
verbatim into the STATUS line, which G6's whole-line grep proof measures.

## Verification

**G1 HYGIENE — PASS.** `.agent/STOP` read from disk before C0a with
`os.path.exists` — `False`, ABSENT. Read again before C3, same call, same answer
— `False`, ABSENT. `git rev-parse HEAD` before C0a =
`6a32be7969b326a29ebfc45e399cbb540dd23666`, equal to the BASE `6a32be79`.
`git branch --show-current` = `feature/f037-rendered-diff-viewer`.
`git status --porcelain | wc -l` = 0 after C0a, after C0b, after C1, after C2 and
after C3 — five readings, all 0.

**G2 TRANSPORT — PASS.** sha256 of the committed `.agent/authored/f037-r27.md`
blob, read with `git show HEAD:.agent/authored/f037-r27.md` into memory, =
`c61bfc2eeeff1a450cd1d4d8c1e1640cc48154a423ebfc4b2c28f83869b5bc7c` (20360 bytes,
286 lines). sha256 of the reviewer's own original at
`.remedy-wt/f037-r27-block.md` = the same digest over the same 20360 bytes, and
the byte comparison itself is `True`. That file existed before this worker did
and was not written by it, so this reading covers the EMISSION and not merely
this worker's self-consistency. No digest is stated here that was not computed
here. At C0b, `git rev-parse HEAD:.agent/authored/f037-r27.md` and
`git rev-parse HEAD:.agent/last_block.md` both print
`2b0101abe6cc702d70815e7d31936dcfdb32414e` — ONE blob.

**G3 THE PLAN AT C1 — PASS.** PLANF037R27 was re-extracted from the COMMITTED
C0a blob via `git show 314159ab:.agent/authored/f037-r27.md`, never from the
session's copy, and compared with `.agent/plan.md` at `c640a996`: BYTE EQUAL
including the trailing newline (`True`). Negative control, the same comparison
with the trailing newline dropped: `False`. `wc -l` = 42, strictly under 50.
Lines exactly `## Goal`: 1. Lines exactly `## Next Steps`: 1.

**G4 THE RECORD AT C2, both readers — PASS.** (a) The `6a32be79` blob of
`.agent/live_review.md` + `\n` + GATER26 == the C2 blob → `True`. NEGATIVE
CONTROL: byte offset 50 of GATER26, which the script confirmed lies INSIDE the
FIRST appended paragraph (that paragraph ends at offset 671), replaced with a
different byte and the equality recomputed → `False`, REJECTED as required. (b)
The C2 blob split on blank lines; N, counted by the script from the slice itself
and not taken from the block, is **6**; the LAST 6 units of the file match those
6 paragraphs IN ORDER, unit by unit, all `True`. The pre-round blob is a byte
PREFIX of the C2 blob: `True`, **1329032** bytes growing to **1334200**.

**G5 THE LEDGER — PASS.** Base figures re-measured by this worker at `6a32be79`,
not inherited: registrations `^- R-\d+ — ` **292**, all DISTINCT (292 found, 292
unique); `^Done: R-\d+ — ` **43**; `^Landed: R-` **11**;
`^Gate: F\d+ R\d+ — ` **96**; OPEN SET as a set **251**. Every one equals the
figure the block states. Over the C2 blob: registrations **292**, UNMOVED, all
DISTINCT; `^Done: R-\d+ — ` **43**, UNMOVED; `^Landed: R-` **11**, UNMOVED;
`^Gate: F\d+ R\d+ — ` **97**, a rise of exactly ONE; OPEN SET **251**, UNMOVED.
`Gate: F037 R26` occurs exactly **1** time in the C2 blob. `R-0714` is present as
a registration (1 line) and carries NO `Done:` line (0) and no `Landed:` line
(0), so it is STILL OPEN — the documented Medium risk F037 closes with.

**G6 THE CLOSURE EDITS AT C3 — PASS.** All four pairs were re-extracted from the
COMMITTED C0a blob and applied by replacing the single FROM occurrence, each
verified to be exactly 1 before the write. Counts over the C3 content of each
file:

| Pair | File | Shape | FROM count after | TO count after |
|------|------|-------|------------------|----------------|
| P1 | `docs/roadmap/STATUS.md` | REWRITE | **0** | **1** |
| P2 | `README.md` | REWRITE | **0** | **1** |
| P3 | `README.md` | REWRITE | **0** | **1** |
| P4 | `README.md` | APPEND (TO contains FROM) | **1** | **1** |

Each header's own declaration was re-checked rather than trusted: `TO contains
FROM` computed `False`, `False`, `False`, `True` for P1–P4, matching the four
headers exactly.

THE STATUS GREP PROOF the closure protocol's step 5 requires: `[P1-TO]`'s text
was extracted from the COMMITTED C0a blob and looked up in the split lines of
`docs/roadmap/STATUS.md` at C3 — present as a WHOLE LINE (`True`), occurring
exactly **1** time. `docs/roadmap/STATUS.md` at C3 contains exactly **60** lines
matching `^- \[x\] F\d{3} — ` (59 before this round) and **0** lines matching
`^- \[~\]` (1 before).

**G7 THE CLOSURE PRECONDITIONS AT C3 — PASS.** One pytest process at a time, from
the repository root, output captured in memory.

| Command | Exit | Wall | Result |
|---------|------|------|--------|
| `python3 -m pytest tests/docs/ -q` | **0** | 0.6s | `295 passed in 0.44s` |
| `python3 -m pytest -n auto -q` | **0** | 149.2s | `18119 passed, 20 skipped in 148.70s` |

THE DOCS GATE DEMONSTRABLY BITES: the reviewer measured 2 failed and 293 passed
with the README left untouched against this round's 295 passed with all four
edits applied, which is the R-0154 pin that forces STATUS and README into ONE
commit. The full-suite run is closure precondition 2's confirmation and the
second of the feature's two full-suite runs; its `FAILED` list is EMPTY — the
regex `^FAILED .*$` over the captured output found **0** matches, so no id needed
attribution and the suite was not re-run to chase a colour. Both figures equal
the reviewer's readings at `38966bf3`: 18119 and 20.

CLOSURE PRECONDITION 3, through
`from packages.orchestration.integrity_gate import run_integrity_checks` because
the `remedy` CLI is denied session-wide: `.passed` = **True**, `.fail_count` =
**0**, five checks and every one PASS — `handler_import` PASS,
`live_review_verdict` PASS, `plan_consistency` PASS, `relevant_untracked` PASS,
`high_blockers_open` PASS.

**G8 STRUCTURE AND THE PR — PASS.** `git diff --name-only 6a32be79..<C3>` returns
exactly the block's change set: `.agent/authored/f037-r27.md`,
`.agent/handoff.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`.agent/plan.md`, `README.md`, `docs/roadmap/STATUS.md` — **7** paths. RESIDUE
measured-minus-changeset: `[]`. RESIDUE changeset-minus-measured: `[]`. Both
printed, both EMPTY IN BOTH DIRECTIONS. `git diff --stat 6a32be79..<C3>`
restricted to `apps/`, to `packages/`, to `tests/` and to
`docs/roadmap/features/T5_F037.md` prints the empty string in all FOUR cases —
nothing under the code trees was touched and the feature file was not re-edited,
its Built State already being current from R26 as closure precondition 4
requires. Every commit C0a through C3 is single-parent (parent count 1, five
times); insertions from `git diff --numstat`, each under 500 and each equal to
the corresponding `## Commits` cell above:

| Commit | Insertions | Under 500 |
|--------|-----------|-----------|
| `314159ab` C0a | 286 | yes |
| `ae1b8b2c` C0b | 211 | yes |
| `c640a996` C1 | 21 | yes |
| `7d84971b` C2 | 12 | yes |
| C3 | 271 | yes |

TRANSPORT-MARKER SWEEP, counted affirmatively over each file's C3 content rather
than inferred from a silent `git grep`: `^<<<SLICE ` and `^<<<END ` are **0 and
0** in `.agent/plan.md`, **0 and 0** in `.agent/live_review.md`, **0 and 0** in
`docs/roadmap/STATUS.md` and **0 and 0** in `README.md`, against the non-zero
control `.agent/authored/f037-r27.md`, which reports **3 and 3** — one pair per
slice. PAIR-HEADER SWEEP: lines beginning `[P1`, `[P2`, `[P3` or `[P4` number
**0, 0, 0, 0** in `README.md` and **0, 0, 0, 0** in `docs/roadmap/STATUS.md`, so
no delimiter of the CLOSUREEDITS carrier reached a target file.
`git ls-files .remedy-wt | wc -l` = **0**. The push and the
`git rev-parse HEAD` / `origin/feature/f037-rendered-diff-viewer` comparison
follow this commit and are reported in the session output, for the reason the
External-actions note gives.

## Authored-text proofs

Two reviewer-authored slices and one four-pair carrier were applied this round.
Every one was re-extracted from the COMMITTED `.agent/authored/f037-r27.md` blob
— not from the session's copy of the block — and compared on disk.

| Slice | Target | Result |
|-------|--------|--------|
| PLANF037R27 | `.agent/plan.md` at `c640a996` | BYTE EQUAL including trailing newline (`True`); negative control dropping that newline `False` |
| GATER26 | `.agent/live_review.md` at `7d84971b` | Reader (a) equality `True`, negative control inside its FIRST appended paragraph `False`; reader (b) all 6 tail paragraphs match in order; pre-round blob a byte prefix, 1329032 → 1334200 |
| CLOSUREEDITS P1 | `docs/roadmap/STATUS.md` at C3 | FROM 0, TO 1; `[P1-TO]` present as a WHOLE LINE, exactly once — the closure protocol's step 5 grep proof |
| CLOSUREEDITS P2 | `README.md` at C3 | FROM 0, TO 1 |
| CLOSUREEDITS P3 | `README.md` at C3 | FROM 0, TO 1 |
| CLOSUREEDITS P4 | `README.md` at C3 | FROM 1 (its TO contains it), TO 1 |

No slice and no pair was reflowed, reworded, retitled, corrected or shortened,
and no FROM or TO string was retyped by hand — each was carried as bytes from the
committed blob into the replacement. The delimiter lines never reached a target
file; G8's two sweeps measure that rather than assert it.

## Deviations & assumptions

1. **The ordered commit sequence C0a, C0b, C1, C2, C3 was followed exactly.** No
   extra commit, no dropped commit, no reordering. C3 is the LAST commit on this
   branch (Rule A4); the closure gate raised no candidate here, so the one
   permitted successor of DECISION amend0827 D2 — a `.agent/candidates.md`-only
   commit — was not made and `.agent/candidates.md` is untouched.
2. **Shell-guard re-expressions (constraint 9).** Three command FORMS were
   rejected by this session's guard and were re-expressed rather than weakened or
   skipped; no gate lost coverage. (a) A compound hygiene probe combining a
   redirect, `echo` and `$?` (`ls -la .agent/STOP 2>&1; echo "---STOP-exit:$?"`)
   was rejected; `.agent/STOP` was read instead with `os.path.exists` inside
   `python3 - <<'PY'`, which is a direct disk read rather than an exit-code
   inference, and the branch/HEAD/porcelain readings were split into separate
   plain commands. (b) A `python3 - <<'PY'` heredoc whose pattern table was a
   BRACE LITERAL CONTAINING QUOTES (`pats = { "name": r"regex" }`) was rejected;
   the identical G5 measurement was re-expressed with a list of tuples built by
   `pats.append((...))`, with no brace literal in the source. (c) The full-suite
   and docs-suite runs were expressed as
   `subprocess.run([...], capture_output=True, env=env)` with `p.returncode`
   printed, which yields the REAL exit code of pytest itself rather than of a
   pipeline — a stronger reading than a `| tail` form, not a weaker one, and it
   is also how the block's "captured IN MEMORY" instruction is met.
3. **The C3 row of the `## Commits` table names no SHA and its `+/-` cells were
   measured from the staged index.** The table is written into the commit it
   describes, so its own SHA cannot exist when the text is written (the R-0149
   pattern the handback template names). The per-path figures were taken with
   `git diff --cached --numstat` over the fully staged C3 content and re-measured
   after the commit to confirm the two agree; the total, 271 insertions,
   is repeated in G8's table. The SHA is reported in the session output.
4. **The push and the PR outcomes are not written into this file.** Recording
   either here would require a value that cannot exist when the text is written,
   and the write-once rule forbids a second handoff commit. Both are reported in
   the session output and are independently measurable, by the `rev-parse`
   comparison and by `gh pr list --state open` respectively. The block itself
   states this for the PR number.
5. **The Session section carries the rule-6 scope report.** Both soft limits — 25
   rounds and 7 sessions — are exceeded at round 27 of session 8, and
   `docs/agents/handback_template.md` makes the scope report mandatory in that
   state. The block ordered the Session line and its roster; the report is the
   template's own obligation on top of it, not new work, and it restates R24's
   D11/A6 ruling rather than re-opening it.
6. **No assumption was carried from the block's numbers.** Every base figure the
   block states — the 292/43/11/96/251 ledger readings, the 295-passed docs gate,
   the 18119/20 full-suite reading, the integrity result, the 59-to-60 STATUS
   transition, and each pair's "FROM occurs 1x" claim — was independently
   re-measured here, and each matched. The one figure the block states that this
   round did NOT re-measure is the 2-failed/293-passed partial-edit control,
   because measuring it would require committing or staging a deliberately
   inconsistent README; it is quoted as the reviewer's reading and labelled as
   such in G7.
7. **No test was edited, added, deleted or skipped, and nothing under `apps/`,
   `packages/` or `tests/` was touched.** G8's four restricted stats print
   nothing, which proves it rather than asserting it.
8. **No disagreement with the block arose.** Every slice and pair was applied as
   written; nothing in the block was judged wrong.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block | done | `314159ab` |
| C0b mirror the block | done | `ae1b8b2c` |
| C1 the plan | done | `c640a996` |
| C2 the R26 verdict | done | `7d84971b` |
| C3 STATUS, README and the handback | done | one commit, the last on this branch; SHA in the session output |
| the closure PR | done | created after C3 and the push, NOT merged; number in the session output |
| G1 hygiene | done | STOP absent twice, base SHA equal, branch correct, 5×0 porcelain |
| G2 transport | done | digests EQUAL against the pre-existing original; one blob `2b0101ab` |
| G3 the plan at C1 | done | byte equal, control `False`, 42 lines, 1 and 1 |
| G4 the record at C2 | done | reader (a) `True` with control `False`; reader (b) N=6 in order; prefix `True` |
| G5 the ledger | done | 292 / 43 / 11 / 97 / open 251; `Gate: F037 R26` once; `R-0714` still open |
| G6 the closure edits at C3 | done | FROM 0/0/0/1, TO 1/1/1/1; STATUS line present as a whole line once; 60 `[x]` and 0 `[~]` |
| G7 the closure preconditions | done | docs 295 passed exit 0; full suite 18119 passed 20 skipped exit 0, FAILED list empty; integrity `passed=True` `fail_count=0`, 5 PASS |
| G8 structure and the PR | done | 7 paths, residue empty both ways; 4 restricted stats empty; 5 single-parent commits all under 500; markers 0 in 4 targets vs control 3; pair headers 0; `.remedy-wt` 0 |

## Open findings

**251** open, computed AS A SET over the C2 blob — 292 distinct registered ids
minus the resolved ones — UNMOVED from `6a32be79`, because this round registered
nothing and resolved nothing. F037 carries no open finding of its own. `R-0714`
remains open and is carried into closure as a DOCUMENTED MEDIUM RISK, which
closure precondition 1 admits exactly: it is a defect in a `tests/ui_server/`
test that F037 does not own and did not cause, its counter-measure is recorded in
the finding itself, and repairing it here would be scope drift.

## Next

F037 is CLOSED. Its closure PR is created by this round and is NOT merged by it;
it merges at the NEXT feature's start through the Open PR Gate, and the gap is
the operator's manual-review window. A fresh session claims the next feature by
Rule A5 — `F033 Hunk-level diff approval` — and its Open PR Gate merges this
feature's PR first. The split-off scope of amendment A6 remains a PROPOSAL to the
operator, executed by no session, and would want its own STATUS line before F033.

The next session applies Phase 1 rule 1 (read `.agent/STOP`) BEFORE rule 2 (the
Open PR Gate), in that order.
