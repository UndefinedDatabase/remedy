# Handback — F040 · SESSION 1 · round 2 — THE THREE SPEC DECISIONS AND THE ONE-SOURCE URGENCY

> Written by the WORKER in C9, the last commit of the bundle. Every exit code
> below is REAL, taken from `subprocess.run(...).returncode` inside a script
> under the gitignored `.remedy-wt/`; not one was read through a pipe.

## Session

SESSION 1 of feature F040 · round 2 · rounds so far 2.

The soft limit (25 rounds / 7 sessions, amend0827 rule 6) is not approached, so
no scope report is owed.

## Range

Review of `6664bf5e5e88b11708e5f350f2da90222072a558`..`HEAD` on branch
`feature/f040-completion-digest`. The base is round 1's handback commit and was
the tip of the branch when this round opened.

## Commits

### fa008282 docs(f040): save the round 2 step block as authored

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f040-r2.md` | +349 −0 | C0a — the block, copied with `shutil.copyfile` from `.remedy-wt/f040-r2-block.md`, never retyped |

### b681213c docs(f040): mirror the round 2 block into last_block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +299 −289 | C0b — the same bytes, the same `shutil.copyfile` call |

### 3ecf5b16 docs(f040): retarget the plan at the round 2 decisions

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +19 −18 | C1 — rewritten from slice PLAN2; first substantive commit, ahead of the ledger append, per constraint 3 |

### 72cffd6c docs(f040): book the round 1 verdict, R-0751 and decisions D2 to D4

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +10 −0 | C2 — slice RECORD2 appended: the R1 PASS, finding R-0751, and DECISIONS F040 D2, D3 and D4 |

### bbf4ded2 docs(f040): record the round 1 plan-table slip

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/prose_slips.md` | +1 −0 | C3 — slice SLIP2, the one-line append-only slip |

### bcd96133 docs(f040): amend the feature file with A1, A2 and the plural test dir

| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/features/T5_F040.md` | +16 −1 | C4 — PAIR-OWNERSHIP (append-shaped, amendments A1 and A2) and PAIR-TESTPATH (rewrite, the plural `tests/ui_contracts/`) |

### c832c898 fix(f040): correct the next-action rule table comment arity (R-0751)

| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/run_report.py` | +1 −1 | C5 — PAIR-COMMENT; the comment now names the arity the value has |

### f49d42b7 feat(f040): add decision_urgency as the single home of the formula

| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/decision_inbox.py` | +51 −0 | C6 — the SPEC'd public `decision_urgency`, written by the worker, placed after `_answerable_by_decision_resolve` |

### db29cfa4 test(f040): pin every property of the urgency formula

| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_decision_inbox.py` | +72 −0 | C7 — section (h), class `TestDecisionUrgency`, one test per property the SPEC lists |

### c9fbdc6e test(f040): pin the python and typescript urgency homes equal

| Path | +/- | Reason |
|------|-----|--------|
| `tests/ui_contracts/test_decision_urgency_parity.py` | +185 −0 | C8 — the parity pin, reading `decisionOrder.ts` as comment-stripped TEXT |

### C9 — this file (self-reference)

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | C9 — the handback; a handoff cannot table the commit that writes it (R-0149 pattern). The push that follows it is likewise unrecordable by it. |

Every `+/-` cell above is taken from `git diff --numstat <sha>^ <sha>`, not from a
file line count. Every commit touches exactly one path. The largest insertion count
is 349 (C0a); none reaches the 500 cap.

## External actions

| Action | Outcome |
|--------|---------|
| `git worktree add .remedy-wt/f040r2-wt-g3 --detach HEAD` | created at `bbf4ded2` — G3's negative control |
| `git worktree remove --force .remedy-wt/f040r2-wt-g3` | removed; `git worktree list` then held the primary checkout alone |
| `git worktree add .remedy-wt/f040r2-wt-g7 --detach HEAD` | created at `c9fbdc6e` — G7's mutation red proof |
| `git worktree remove --force .remedy-wt/f040r2-wt-g7` | removed; `git worktree list` then held the primary checkout alone |
| `git push -u origin feature/f040-completion-digest` | run once, after C9, per constraint 11 |

No pull request was created, edited or merged. No `gh` command was run. No branch
was cut. Nothing was force-pushed. The `remedy` console script is denied in this
sandbox and was not needed: no gate ordered it.

## Verification

One line per gate, with the REAL exit code.

| Gate | Command / reading | Exit |
|------|-------------------|------|
| G1 | sha256 over the scratch original, `.agent/authored/f040-r2.md` and `.agent/last_block.md` | 0 |
| G2 | `.agent/plan.md` byte-equal to PLAN2, 38 lines, `## Goal` and `## Next Steps` present | 0 |
| G3a | whole reconstruction + paragraph order, accepted in the primary checkout | 0 |
| G3b | the same two readings, accepted in the disposable worktree BEFORE the flip | 0 |
| G3c | the same two readings, both REJECTING the one-byte flip in the worktree | 0 |
| G4 | the ledger and `.agent/prose_slips.md` set readings | 0 |
| G5a | PAIR-OWNERSHIP, PAIR-TESTPATH and the `tests/ui_contract/` sweep | 0 |
| G5b | `python3 -m pytest tests/docs/ -q` — 295 passed | 0 |
| G5c | `python3 -m pytest tests/orchestration/test_roadmap_index.py -q` — 30 passed | 0 |
| G6a | PAIR-COMMENT counts, `DECISION_INBOX_VERSION`, `build_decision_inbox`'s key set by CALLING it | 0 |
| G6b | `python3 -c "…NEXT_ACTION_RULES…"` — printed `5 {2}` | 0 |
| G6c | `ruff check packages/orchestration/run_report.py packages/orchestration/decision_inbox.py` | 0 |
| G6d | `python3 -m compileall -q packages/orchestration/decision_inbox.py` | 0 |
| G7a | `pytest tests/orchestration/test_decision_inbox.py tests/ui_contracts/test_decision_urgency_parity.py -q` — 58 passed | 0 |
| G7b | the UNMUTATED CONTROL, same two files, inside the worktree — 58 passed | 0 |
| G7c | the MUTANT, `(blocked + 1) * age` → `blocked * age` — 9 failed, 49 passed | 1 |
| G8a | `python3 -m pytest tests/ui_server/ -q` — 508 passed | 0 |
| G8b | `python3 -m pytest tests/orchestration/test_test_runner.py -q` — 52 passed | 0 |
| G8c | `python3 -m pytest tests/regression/test_resource_safety.py -q` — 21 passed | 0 |
| G8d | `python3 -m pytest tests/orchestration/test_integrity_gate.py -q` — 16 passed | 0 |
| G8e | `python3 -m pytest tests/orchestration/test_run_report.py -q` — 81 passed | 0 |
| G8f | `python3 -m pytest tests/cli/test_golden_path.py -q` — 42 passed (canary) | 0 |
| G8g | clean tree, no untracked files, per-commit insertion counts | 0 |

The decisive readings, in the order the block ordered them.

**G1 TRANSPORT.** All three files 29954 bytes at sha256
`d05f9c085aa6227ae2de7a8dc666901900e2404b3aa657a480711ccf4ad39e1c` — the scratch
original `.remedy-wt/f040-r2-block.md`, the committed `.agent/authored/f040-r2.md`
and the committed `.agent/last_block.md`. ALL THREE EQUAL.

**G2 THE PLAN.** `.agent/plan.md` and slice PLAN2 are both 1783 bytes at sha256
`0411c9f63ddacd0bcbc6dc358f16c0feae7519823d2a9487c50ab32e5a35c4dd`; BYTE-EQUAL
is True. 38 lines, under 50. `## Goal` and `## Next Steps` both present.

**G3 THE RECORD APPEND.** The pre-commit length was re-measured here, not taken
from the block: 1643633 bytes, which agrees with the reviewer's reading at
`6664bf5e`. RECORD2 is 12099 bytes; 1643633 + 1 separator newline + 12099 =
1655733, and the committed file is 1655733. Reading (a), WHOLE RECONSTRUCTION
against the ENTIRE committed file rather than a prefix test: True. N, counted by
the script and not assumed, is 5. Reading (b), the last 5 blank-line units equal
RECORD2's 5 paragraphs IN ORDER: True. NEGATIVE CONTROL, in the disposable
worktree `.remedy-wt/f040r2-wt-g3` and never in the primary checkout: byte offset
1643674, inside the FIRST appended paragraph, flipped `b'C'` → `b'c'`
(`VERDICT PASS` → `VERDIcT PASS`). Both readings ACCEPT the unflipped bytes there
(exit 0) and both REJECT the flipped ones (exit 0 for the expected rejection).
The worktree was removed and `git worktree list` then named the primary checkout
alone.

**G4 THE LEDGER.** Distinct `^- R-\d+ — ` ids 311 → 312; ADDED registered
`['R-0751']`. Distinct `^Done: R-\d+` 53 → 53; ADDED resolved `[]`. Distinct
`^DECISION F040 D\d+ — ` `['D1']` → `['D1', 'D2', 'D3', 'D4']`; ADDED exactly
`['D2', 'D3', 'D4']`. `^Gate: F040 R1 — ` occurs exactly 1 time.
`^Done: R-0570` still counts 0. `.agent/prose_slips.md` 283 → 284 lines,
difference 1, and the old bytes are a byte-exact PREFIX of the new file.

**G5 THE FEATURE FILE.** PAIR-OWNERSHIP is APPEND-shaped — `TO contains FROM` is
True — so it is measured that way: PAIROWNERSHIP-FROM occurs exactly 1x in the
committed file (NOT counted to zero), and each of the 13 TO-ONLY lines occurs
exactly 1x among the 16 lines C4's diff ADDS. PAIR-TESTPATH is a REWRITE —
`TO contains FROM` is False — so FROM 0x and TO 1x after C4.
`git grep -n "tests/ui_contract/"` over the whole repository returns 35 hits,
every one of them printed in the round's transcript: 22 in the append-only
records and inventories under `.agent/` (including this round's own block, which
quotes the retired spelling on purpose) and 13 in OTHER feature files under
`docs/roadmap/features/` — T4_F119, T4_F126, T5_F008, T5_F009, T5_F019, T5_F022,
T5_F023, T5_F024, T5_F031, T5_F038, T5_F041, T5_F042 and T7_F142. Hits in
`docs/roadmap/features/T5_F040.md`: 0. The count was REPORTED, not driven to
zero, which is the item-2 trap the block names.

**G6 THE PRODUCTION EDITS.** PAIRCOMMENT-FROM 0x and PAIRCOMMENT-TO 1x in
`packages/orchestration/run_report.py`.
`python3 -c "from packages.orchestration.run_report import NEXT_ACTION_RULES as R; print(len(R), {len(r) for r in R})"`
printed `5 {2}` — the value the repaired comment now describes.
`ruff check` on both edited modules: `All checks passed!`.
`python3 -m compileall -q packages/orchestration/decision_inbox.py`: silent, exit 0.
`DECISION_INBOX_VERSION` is still 1. `build_decision_inbox` was CALLED on a real
two-task job with an enqueued task decision: its top-level keys are still
`['decisions', 'job_id', 'version']` and its cards still carry `age_seconds`,
`blocked_count` and `answerable_by_decision_resolve` beside the queue's export
keys. The round added a function and changed nothing else in that module's
behaviour.

**G7 THE NEW BEHAVIOUR AND ITS RED PROOF.** In the primary checkout,
`python3 -m pytest tests/orchestration/test_decision_inbox.py tests/ui_contracts/test_decision_urgency_parity.py -q`
is exit 0 at 58 passed (43 in the inbox file, 15 in the pin). The red proof ran
ONLY inside the disposable worktree `.remedy-wt/f040r2-wt-g7`, created at
`c9fbdc6e`, with `__pycache__` purged before each run and `python3 -B` used
throughout. THE UNMUTATED CONTROL RAN AND IS REPORTED FIRST: exit 0, 58 passed.
Then ONE mutation, in
`.remedy-wt/f040r2-wt-g7/packages/orchestration/decision_inbox.py`, the single
occurrence of `(blocked + 1) * age` replaced by `blocked * age`: exit 1, 9 failed
and 49 passed. Failures reached BOTH files, the inbox tests and the parity pin —
for example
`test_the_python_home_scores_the_shared_table[0-42-42-product]`, the row that
exists because a card blocking nothing must still score its age. The worktree was
removed and `git worktree list` then named the primary checkout alone.

An EXTRA red proof, not ordered by the block but taken because the pin claims to
fail loudly: in the same worktree, with the Python mutation restored, renaming
`function decisionUrgency(` to `function scoreCard(` in `decisionOrder.ts` made
the pin exit 1 at 6 failed / 9 passed, and
`test_the_typescript_function_is_found_at_all` was among the failures. An empty
extraction therefore cannot pass silently.

**G8 THE SUITES AND THE TREE.** `tests/ui_server/` 508 passed (base 508),
`tests/orchestration/test_test_runner.py` 52 (base 52),
`tests/regression/test_resource_safety.py` 21 (base 21),
`tests/orchestration/test_integrity_gate.py` 16 (base 16),
`tests/orchestration/test_run_report.py` 81 — no base comparison, the reviewer did
not run it — and the canary `tests/cli/test_golden_path.py` 42 (base 42). Every
one a REAL exit 0. `git status --porcelain` is EMPTY,
`git ls-files --others --exclude-standard` counts 0, and the per-commit insertion
counts for C0a through C8 are 349, 299, 19, 10, 1, 16, 1, 51, 72 and 185 — every
one under 500.

## Authored-text proofs

Nine reviewer-authored units were applied this round. Each was extracted
MECHANICALLY from the committed `.agent/authored/f040-r2.md`'s own delimiters by a
script under `.remedy-wt/`, never retyped, and each was applied byte for byte.

| Unit | Bytes | sha256 (full) | Applied to | Proof |
|------|-------|---------------|------------|-------|
| PLAN2 | 1783 | `0411c9f63ddacd0bcbc6dc358f16c0feae7519823d2a9487c50ab32e5a35c4dd` | `.agent/plan.md` | file byte-equal to the unit (G2) |
| RECORD2 | 12099 | `5dc02e45314a6d17d1cb3fa65bad9e61efdc9d65666e1655b72a32cd6d567c9f` | `.agent/live_review.md` | whole-file reconstruction + paragraph order (G3) |
| SLIP2 | 377 | `c1c6a444050295a5c48b72577931ac7924cc1d50c80d56cb5a5c69fbcee1df3c` | `.agent/prose_slips.md` | old file a byte-exact prefix, +1 line (G4) |
| PAIROWNERSHIP-FROM | 221 | `c2a3056d8dd677cabcafbe51a0072a6818236b15b68bb9ab6d6d7ce962718bed` | `docs/roadmap/features/T5_F040.md` | 1x in the committed file (append shape) |
| PAIROWNERSHIP-TO | 1040 | `6f737c6fae4558c4bd640d97dfe9ec4c2fabdeeb25fe420f5e2d7e174be9779a` | same | each of 13 TO-ONLY lines 1x among C4's added lines |
| PAIRTESTPATH-FROM | 77 | `05b186ad6ae1083f27ac5c1b8a458e7fe66bf35133ea7226acb4d754c5a6be55` | same | 0x after C4 |
| PAIRTESTPATH-TO | 237 | `35f22d2b143fb05fc716ce96ee0484cffcf4a25cbba0fc2cb32693ec16c19c8c` | same | 1x after C4 |
| PAIRCOMMENT-FROM | 43 | `b9c6e48ba7a51e6711bfd850e22ac44c716724a796eca4b87cec2aa10e2b0533` | `packages/orchestration/run_report.py` | 0x after C5 |
| PAIRCOMMENT-TO | 26 | `b4c583d23244a35a869f3375933e04d727514782dcb2639f4af748bdb0ab7cef` | same | 1x after C5 |

The block itself is 29954 bytes at
`d05f9c085aa6227ae2de7a8dc666901900e2404b3aa657a480711ccf4ad39e1c`, equal on disk
in all three places (G1), so the units above were extracted from the same bytes the
reviewer holds.

## Deviations & assumptions

The block's ordered commit sequence was followed EXACTLY: C0a, C0b, C1 through C9,
ten commits, no extra commit, none dropped, none reordered, one path each. The
change set is exactly the eleven declared paths and nothing under `apps/` was
touched — `apps/ui/src/api/decisionOrder.ts` is READ by C8's pin and is not edited.
No commit was amended, reset or rebased.

1. **C6 edited one line the block arguably froze, and it is declared here rather
   than left to be found.** Constraint 8 reads "This round ADDS a function and
   nothing else in that file." I added `decision_urgency(card) -> int` to the
   module docstring's `Public API::` list — one line, +1 insertion inside the 51.
   Reason: the same constraint calls `decision_urgency` "NEW PUBLIC API", the
   module maintains an explicit public-API list, and a stale one is a live defect
   class in this repository (open finding R-0746 is exactly that reading of
   `proof_chain.py`). Leaving it out would have shipped a known defect to satisfy
   a sentence whose subject is the module's BEHAVIOUR — `build_decision_inbox`'s
   return shape, its three card keys and `DECISION_INBOX_VERSION`, all three of
   which are unchanged and were re-measured by calling the function (G6). If the
   reviewer reads constraint 8 literally, this line is the one to revert.
2. **C7 introduces the file's first test CLASS.** The SPEC says "APPEND a new test
   class"; `tests/orchestration/test_decision_inbox.py` holds twenty module-level
   test functions and no class at all, and the same SPEC says to follow the file's
   conventions. The two cannot both be satisfied. I followed the explicit
   instruction and added `class TestDecisionUrgency`, keeping every other
   convention of the file — the section banner comment, the property-named tests,
   the WHY docstrings. Declared because it makes section (h) shaped unlike
   sections (a) through (g) above it.
3. **SLIP2 was appended with NO blank-line separator, unlike every other entry in
   `.agent/prose_slips.md`.** Every existing entry in that file is separated from
   its neighbour by a blank line. G4 requires the line-count difference to be
   exactly 1, which a separator would make 2. I applied the slice as given, so the
   new entry abuts the F033 R24 line directly. Applied as ordered, declared here.
4. **A factual overstatement inside slice RECORD2, applied byte for byte.**
   DECISION F040 D3 states "THIS IS THE THIRD FEATURE FILE CARRYING THAT TYPO". The
   round's own G5 sweep measures 13 OTHER feature files under
   `docs/roadmap/features/` still carrying `tests/ui_contract/` after C4, listed in
   the Verification section above; F040 was the fourteenth, not the third. The
   slice was applied unchanged per constraint 1 and the correction is recorded
   here. Nothing rests on the numeral: the amendment's authority is AGENTS.md's
   "one spelling per concept repo-wide" and the F009 precedent, both of which hold
   at any count, and the gate the block wrote reports the hits rather than
   requiring them to fall.
5. **The three DECISIONS were recorded in `.agent/live_review.md`, not in
   `.agent/decisions.md`.** The block's change set names the former and not the
   latter, and RECORD2 carries D2, D3 and D4 in full. Noted because AGENTS.md's
   Commit Gate item 7 asks whether `.agent/decisions.md` needs an update; it does
   by the general rule, and the block's change set overrides it for this round.
6. **`.agent/context.md` was not updated.** It is not in the change set. Its round
   1 content — the digest feature, this branch, the scope boundaries — is still
   accurate; nothing this round changed the scope it describes.
7. **Assumption in C8, stated so the reviewer can reject it.** The parity pin
   cannot EXECUTE the TypeScript (no vitest reachable from pytest, and the pin
   deliberately imports nothing from `apps/`). It therefore asserts the shared
   table's numbers against the shipped Python, and asserts against the shipped,
   comment-stripped TypeScript that all four rules those numbers depend on are
   still present — the finiteness test and the clamp on `blockedCount`, the null /
   non-finite / non-positive guard on the age, and the product with its `+ 1` —
   plus that the rejected form `blockedCount * ageSeconds` is absent from the
   comment-stripped body. `test_the_table_exercises_every_typescript_rule` stops a
   rule being asserted present without a row that depends on it. This is a
   structural pin over one implementation and a behavioural pin over the other,
   not an execution of both.
8. **The `remedy` console script was not run.** It is denied in this sandbox and no
   gate ordered it; `python3 -m apps.cli.grouped` was therefore not needed either.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block to `.agent/authored/f040-r2.md` | done | `shutil.copyfile`, byte-equal |
| C0b mirror it into `.agent/last_block.md` | done | `shutil.copyfile`, byte-equal |
| C1 rewrite `.agent/plan.md` from PLAN2 | done | byte-equal, 38 lines |
| C2 append RECORD2 to `.agent/live_review.md` | done | reconstruction and paragraph order both hold |
| C3 append SLIP2 to `.agent/prose_slips.md` | deviated | applied byte for byte; no blank separator — deviation 3 |
| C4 apply PAIR-OWNERSHIP and PAIR-TESTPATH | done | append shape and rewrite shape measured separately |
| C5 apply PAIR-COMMENT | done | FROM 0x, TO 1x |
| C6 add `decision_urgency` per the SPEC | deviated | one extra line in the module's Public API list — deviation 1 |
| C7 add the unit tests | deviated | the file's first test class — deviation 2 |
| C8 add the parity pin | done | 15 tests, all green; loud-failure test proved to fail loudly |
| C9 rewrite `.agent/handoff.md` | done | this file |
| G1 TRANSPORT | done | exit 0 |
| G2 THE PLAN | done | exit 0 |
| G3 THE RECORD APPEND | done | exit 0 accepted, exit 0 on the rejection control |
| G4 THE LEDGER | done | exit 0 |
| G5 THE FEATURE FILE | done | exit 0, 0, 0 |
| G6 THE PRODUCTION EDITS | done | exit 0, 0, 0, 0 |
| G7 THE RED PROOF | done | control 0, mutant 1 at 9 failed |
| G8 THE SUITES AND THE TREE | done | six suites exit 0, clean tree |
| R-0751 the stale rule-table comment | fixed | C5; the comment now names the arity `NEXT_ACTION_RULES` has |
| R-0570 the docs-consistency finding | open | routed OFF this branch: its fix edits `README.md` and `tests/docs/test_docs_consistency.py`, which F040 does not own |

## Next

The reviewer re-runs G1 through G8 against its own copy of the block and reads the
committed diff, then orders T001: the digest composition module over
`build_report_sources` and the inbox read path, with the four state fixtures
(green, blocked-with-decisions, budget-stopped, mid-run), `ownership` fixed as an
empty list per D3 and `cost.basis` re-derived as exactness per D4.
