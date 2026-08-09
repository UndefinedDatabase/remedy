# Live Review — F105 Cache-optimal prompt ordering

> Reviewer: the main session of a one-session self-drive build
> (docs/agents/self_drive_protocol.md). Worker: one delegated subagent per
> round. Findings are authored here by the reviewer only. A worker marks a
> landed fix `Landed: R-XXXX`; only reviewer-authored `Done:` text sets
> Resolved (docs/agents/planner_reviewer_prompt.md §4.4).
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0235.

## Findings

- R-0221 (Low, carried from F103 R5 through the whole of F104):
  `TestAutoBuildBehavior::test_auto_build_runs_by_default` in
  `tests/ui_server/test_dashboard_contract.py` pops `REMEDY_UI_NO_AUTO_BUILD`
  and runs a real `npm install` + `npm run build` in whatever checkout it runs
  in, refreshing `apps/ui/dist` mtimes mid-suite. That costs every integration
  gate six or seven phantom base-only failures through the mtime comparison in
  `_frontend_is_stale()`. Carried into F105 unchanged: it is not this feature's
  code either, AGENTS.md Scope Control bars the "while I'm here" edit, and it
  stays routed to the F252 flake-debt class, to be attributed by controlled
  evidence at the integration gate rather than chased. OPEN.

- R-0229 (Medium, F105 R4): the segment-name mapping is unpinned, because the
  test that looks like its guard reads the mapping it is meant to prove.
  `tests/orchestration/test_role_conventions.py::TestRoleConventionsRegistration::test_registered_segment_carries_the_documented_name_and_rank`
  asserts `segment.name == CONVENTIONS_SEGMENT_NAMES[role]`, which holds for any
  mapping, correct or swapped. Proven in a disposable worktree at 65d3c7b9:
  exchanging the two values of `CONVENTIONS_SEGMENT_NAMES` between WORKER and
  REVIEWER leaves all 21 tests GREEN. This is not cosmetic — the segment name is
  what the T001 manifest records, so a swapped mapping would label the worker's
  conventions `reviewer_conventions` in every audit row, and the T003 per-builder
  goldens would inherit the mislabel. The module docstring itself says the names
  "appear in the segment manifest, so renaming one rewrites audit history": that
  is precisely the property no test guarded. The sibling mapping is fine —
  exchanging the two values of `CONVENTIONS_DOC_RELATIVE_PATHS` turns 3 tests RED
  through the role-specific rule anchors. Fix: assert the expected literal per
  role, for both mappings, and red-proof the swap. OPEN.
  Done: R-0229 (2026-08-09) — RESOLVED. `TestRoleConventionsMappings` now asserts
  the expected literal per role for BOTH mappings, so the assertion no longer
  reads the mapping it pins. Re-proved by the reviewer in a disposable worktree
  at a8e9ab1f: exchanging the two values of `CONVENTIONS_SEGMENT_NAMES` turns
  exactly 2 tests RED, the two `test_segment_name_mapping_holds_the_expected_literal`
  parameters, where before the fix it turned none. The worktree was removed and
  pruned before this verdict.
- R-0230 (Low, F105 R4): `packages/orchestration/role_conventions.py`
  `role_conventions_text` promises `RoleConventionsError` for a document that is
  "missing or unreadable", and the round's spec said the same, but only `OSError`
  is caught. A document that is not valid UTF-8 raises `UnicodeDecodeError`,
  which escapes the conventions layer — so `except PromptSegmentError`, the
  single catch this module's error hierarchy exists to enable, does not cover it.
  Fix: catch `(OSError, UnicodeDecodeError)` and pin it with a test. OPEN.
  Done: R-0230 (2026-08-09) — RESOLVED. `role_conventions_text` now catches
  `(OSError, UnicodeDecodeError)`, so an undecodable document fails as a
  `RoleConventionsError` exactly like a missing one and stays inside the
  `PromptSegmentError` hierarchy. Re-proved by the reviewer in the same
  disposable worktree: reverting the except clause turns
  `test_non_utf8_document_raises_role_conventions_error` RED with
  `UnicodeDecodeError` at `role_conventions.py:107`.
- R-0231 (Medium, F105 R6, reviewer-authored defect): the R5 gate record and the
  R6 step line sit at the END of `## Findings` instead of under `## Steps`. The
  cause is the reviewer's authoring, not the application — the R6 block appended
  both bullets to PAIR B's TO text, whose target is a finding paragraph, and the
  worker applied the bytes exactly as instructed and flagged the placement rather
  than silently re-indenting. Every other gate record in this file lives under
  `## Steps`, so the record that `LAST_REVIEWED_SHA` advanced to a8e9ab1f is
  filed where no reader looks for it, and `## Findings` now reads as though it
  holds two entries that are not findings. Fix: MOVE those bytes to the end of
  `## Steps`, unchanged. OPEN.
  Landed: R-0231 — the R5 gate and R6 step bytes moved into ## Steps unchanged.
- R-0232 (Medium, F105 R6, reviewer-authored defect): this file's header still
  reads `Next free ID: R-0229` while R-0229 and R-0230 are both issued and
  resolved, and `.agent/plan.md` correctly says R-0231. A later reviewer that
  trusts the header — the documented place to look — reissues a live ID onto a
  different finding, and two findings then share one number in the permanent
  record. That is the F056 candidate-loss class: a state file that lies quietly
  costs more than one that is missing. Fix: correct the header to the true next
  free ID. OPEN.
  Landed: R-0232 — header corrected to the true next free ID.
- R-0233 (Medium, F105 R7, reviewer-authored defect): the R7 step line invokes
  docs/agents/planner_reviewer_prompt.md §4.13 to declare that R7 "has NO
  on-disk gate entry of its own". §4.13 exempts the last round of a BRANCH, and
  this branch continues through T003, T004, the integration gate and closure —
  R7 ended a SESSION, which §4.13 does not cover. Left standing, the line tells
  a later reviewer no gate is owed and "no repair round is opened to close it",
  stranding R-0231 and R-0232 on `Landed:` lines forever, because §4.4 reserves
  `Done:` for reviewer text. Fix: state why §4.13 does not apply here. OPEN.
- R-0234 (Low, F105 R5 and R6, reviewer-authored defect): both the R5 and the R6
  gate records cite `test_test_runner.py` by bare basename, but TWO files carry
  that name — `tests/test_test_runner.py` (43 tests) and
  `tests/orchestration/test_test_runner.py` (51 tests). Re-run as written, the
  record selects the 43-test file, where the R7 gate's `-k` filter reports `43
  deselected` and no tests run; this reviewer lost a run to exactly that. The
  number 51 is real and belongs to the orchestration file, so only the citation
  is wrong — but a gate record that cannot reproduce its own result reads as a
  regression. Fix: cite the full path in both records. OPEN.

## Steps

- R1: claim F105 `[~]` under Rule A5, sweep both F104 closure candidates into
  docs/agents/planner_reviewer_prompt.md (§4.4 `Landed:` versus `Done:`, §4.13
  the terminating convention), empty `.agent/candidates.md`, and reset the
  `.agent/` state to F105. No `packages/`, `apps/`, `tests/` or `README.md`
  byte changed.
- Reviewer gate on R1 (2026-08-09): PASS. Range `cfda4245..6b74d7c4` read as a real
  diff — nine paths, all of them the ones the block named; nothing under
  `packages/`, `apps/`, `tests/`, no `README.md`, no `ROADMAP.md`. Pairs A, B and C
  applied byte for byte; the four full-file rewrites match their authored text.
  `docs/roadmap/STATUS.md` differs from main by exactly one line, the F105 claim.
  Gates re-run by the reviewer from the repo root with real exit codes:
  `tests/docs/` 294 passed, the `.agent` contract tests 4 passed, resource safety
  21 passed, the canary 42 passed, `remedy integrity check --json` `"passed": true`
  over 5 checks, `.agent/candidates.md` holding `**No open candidates.**` exactly
  once, working tree clean, HEAD equal to origin.
- R2: T001 — `packages/orchestration/prompt_segments.py` with the rank scale,
  the registry, `compose_prompt_segments`, the segment manifest and the
  conventions token cap, pinned by 22 tests. No builder migrated, no prompt
  content changed.
- Reviewer gate on R2 (2026-08-09): PASS. Range `6b74d7c4..4d01a40a` read as a real
  diff — six files, exactly the change set the block named. Gates re-run by the
  reviewer: the new suite 22 passed, `test_token_economy.py` 37 passed,
  `tests/docs/` 294 passed, the canary 42 passed, integrity 5 of 5, tree clean,
  HEAD equal to origin. THREE independent mutation red-proofs, run in a disposable
  worktree at 4d01a40a that was removed and pruned before this verdict: dropping
  the rank from the sort key turns 3 tests RED, giving the delimiter an injected
  marker turns 5 RED, and disabling the token-cap check turns 1 RED. The guards
  are load bearing. `LAST_REVIEWED_SHA` advances 6b74d7c4 -> 4d01a40a.
- R3: the session-terminator round of the previous session — `.agent/` state
  only (the R3 block saved verbatim, the R1 and R2 gates recorded, the
  session-end handoff and plan). No `packages/`, `apps/`, `tests/` or `docs/`
  byte changed.
- Reviewer gate on R3 (2026-08-09): PASS. Range `4d01a40a..1a054862` read as a
  real diff — five paths, all under `.agent/`, exactly the change set the R3
  block named; nothing under `packages/`, `apps/`, `tests/` or `docs/`. Gates
  re-run by the reviewer of THIS session from the repo root with real exit
  codes: `cmp .agent/authored/f105-r3-1.md .agent/last_block.md` exit 0 and no
  output, `tests/docs/` 294 passed, `tests/orchestration/test_prompt_segments.py`
  22 passed, the `.agent` contract tests 4 passed, the canary
  `tests/cli/test_golden_path.py` 42 passed, `git status --porcelain` empty, and
  `git worktree list` showing the primary checkout alone.
  `LAST_REVIEWED_SHA` advances 4d01a40a -> 1a054862.
- Round numbering, corrected (2026-08-09): the previous session's terminator
  round WAS R3 — its own handoff header names it so and its three commits sit on
  the branch — yet that handoff's "Next" line and `.agent/plan.md` both called
  the UPCOMING round R3 as well. The upcoming round is R4. No work is affected;
  the record is made unambiguous instead of left to a reader's guess.
- R4: T002 part 1 — `packages/orchestration/role_conventions.py`, the loaders
  that read the two existing conventions documents verbatim as the conventions
  segment under `CONVENTIONS_TOKEN_CAP`, with the content-equality goldens in
  `tests/orchestration/test_role_conventions.py`. No conventions RULE is
  re-authored, not one byte of either document changes, and no builder is
  migrated.
- Reviewer gate on R4 (2026-08-09): FINDINGS. Range `1a054862..65d3c7b9` read as
  a real diff — the eight declared paths and nothing else; no `docs/`, no
  `apps/`, no `AGENTS.md`, so neither conventions document changed a byte. Gates
  re-run by the reviewer from the repo root: `cmp` of the authored block against
  `.agent/last_block.md` exit 0, `test_role_conventions.py` 21 passed,
  `test_prompt_segments.py` 22 passed, `test_token_economy.py` 37 passed, the
  `.agent` contract tests 4 passed, `tests/docs/` 294 passed, the canary 42
  passed, integrity 5 of 5, tree clean, HEAD equal to origin. FOUR mutation
  red-proofs ran in a disposable worktree at 65d3c7b9, removed and pruned before
  the verdict: stripping the verbatim read turns 2 tests RED, dropping the token
  cap turns 1 RED, exchanging the document paths turns 3 RED — and exchanging the
  segment NAMES turns none, which is R-0229. `LAST_REVIEWED_SHA` does NOT advance
  and stays 1a054862.
- R5: the repair round for R-0229 and R-0230, plus DECISION F105 D2 on step-block
  size. No feature work; the discoverability block moves to R6.
- Reviewer gate on R5 (2026-08-09): PASS. Range `65d3c7b9..a8e9ab1f` read as a
  real diff — nine paths, none under `docs/`, `apps/` or `AGENTS.md`, so neither
  conventions document changed a byte in the repair round either. Every commit
  is under the 500-insertion cap, the largest 295. Gates re-run by the reviewer:
  `cmp` exit 0, `test_role_conventions.py` 26 passed, `test_prompt_segments.py`
  22 passed, `tests/docs/` 294 passed, `test_test_runner.py` 51 passed, the
  canary 42 passed, integrity 5 of 5, tree clean, HEAD equal to origin, the
  primary checkout the only worktree. Two mutation red-proofs of my own confirm
  both fixes. The worker's C1 split is RATIFIED: my R5 block was 295 lines, 55
  over the cap DECISION F105 D2 sets in that same block, and the mandated single
  commit would have been 529 insertions with F105's once-per-feature exception
  already spent — AGENTS.md "stop and split before committing" is the governing
  rule, the bytes and the `cmp` proof are unchanged, and the second commit is a
  single `.agent/**` verbatim rewrite, exempt under DECISION F104 D1. The
  authoring defect is the reviewer's: from R6 on the block is COUNTED before it
  is emitted, not estimated. `LAST_REVIEWED_SHA` advances 1a054862 -> a8e9ab1f.
- R6: T002 part 2 — the operator addition of 2026-07-30, a distilled
  write-discoverable-code block appended to BOTH conventions documents as a
  reviewed diff. Measured by the reviewer before authoring: the worker document
  goes from 505 to 740 estimated tokens and the reviewer document from 515 to
  703, both under the cap of 800 the R4 loader enforces.
- Reviewer gate on R6 (2026-08-09): PASS. T002 is COMPLETE. Range
  `a8e9ab1f..c0ce100a` read as a real diff — seven paths, and the only two
  outside `.agent/` are the two conventions documents. Both document diffs are
  PURE APPENDS after the previous final line: no existing rule was reworded,
  reordered or removed, which is what the feature file's "must not re-author
  policy" requires. Every commit is under the 500-insertion cap, the largest 370.
  Gates re-run by the reviewer from the repo root: `cmp` exit 0,
  `test_role_conventions.py` 26 passed, `test_prompt_segments.py` 22 passed,
  `tests/docs/` 294 passed, `test_test_runner.py` 51 passed, the canary 42
  passed, integrity 5 of 5, tree clean, HEAD equal to origin, the primary
  checkout the only worktree. Token estimates measured on disk after the append:
  the worker document 740 and the reviewer document 703 against the cap of 800,
  matching the pre-authoring measurement exactly. One mutation red-proof ran in a
  disposable worktree at c0ce100a, removed and pruned before this verdict:
  padding the worker document past the cap turns 5 tests RED, so the cap is
  genuinely enforced now that the headroom is only 60 tokens.
  `LAST_REVIEWED_SHA` advances a8e9ab1f -> c0ce100a.
- R7: the session-terminator round — R-0231 and R-0232 registered and fixed, the
  R6 gate recorded, the session-end handoff written. Per
  docs/agents/planner_reviewer_prompt.md §4.13 this round has NO on-disk gate
  entry of its own; its verdict lives in `.agent/handoff.md`, the reviewer's
  completion report and, later, the closure PR. That absence is the TERMINATOR,
  not a missing gate, and no repair round is opened to close it.
