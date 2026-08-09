# Live Review — F105 Cache-optimal prompt ordering

> Reviewer: the main session of a one-session self-drive build
> (docs/agents/self_drive_protocol.md). Worker: one delegated subagent per
> round. Findings are authored here by the reviewer only. A worker marks a
> landed fix `Landed: R-XXXX`; only reviewer-authored `Done:` text sets
> Resolved (docs/agents/planner_reviewer_prompt.md §4.4).
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0229.

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
  Landed: R-0229 — literal-per-role mapping assertions added; the swap now
  turns 2 tests RED.
- R-0230 (Low, F105 R4): `packages/orchestration/role_conventions.py`
  `role_conventions_text` promises `RoleConventionsError` for a document that is
  "missing or unreadable", and the round's spec said the same, but only `OSError`
  is caught. A document that is not valid UTF-8 raises `UnicodeDecodeError`,
  which escapes the conventions layer — so `except PromptSegmentError`, the
  single catch this module's error hierarchy exists to enable, does not cover it.
  Fix: catch `(OSError, UnicodeDecodeError)` and pin it with a test. OPEN.

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
