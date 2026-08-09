# Live Review — F105 Cache-optimal prompt ordering

> Reviewer: the main session of a one-session self-drive build
> (docs/agents/self_drive_protocol.md). Worker: one delegated subagent per
> round. Findings are authored here by the reviewer only. A worker marks a
> landed fix `Landed: R-XXXX`; only reviewer-authored `Done:` text sets
> Resolved (docs/agents/planner_reviewer_prompt.md §4.4).
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0245.

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
  Done: R-0231 (2026-08-09) — RESOLVED. The R5 gate record and the R6 step line
  now sit at the end of `## Steps`, and `## Findings` holds only findings again.
  Verified as a MOVE, not a retype: the 21-line region was cut and re-inserted
  with identical bytes, occurring exactly once before and once after.
- R-0232 (Medium, F105 R6, reviewer-authored defect): this file's header still
  reads `Next free ID: R-0229` while R-0229 and R-0230 are both issued and
  resolved, and `.agent/plan.md` correctly says R-0231. A later reviewer that
  trusts the header — the documented place to look — reissues a live ID onto a
  different finding, and two findings then share one number in the permanent
  record. That is the F056 candidate-loss class: a state file that lies quietly
  costs more than one that is missing. Fix: correct the header to the true next
  free ID. OPEN.
  Done: R-0232 (2026-08-09) — RESOLVED. The header declares the true next free
  ID; verified on disk, exactly ONE declaration, FROM 0x and TO 1x. The second
  `Next free ID` match is the R-0232 text quoting the old value — the F104 R11
  "gate quotes its own marker" class, which made the R7 count gate J
  unsatisfiable and put its substance gate J' in J's place.
- R-0233 (Medium, F105 R7, reviewer-authored defect): the R7 step line invokes
  docs/agents/planner_reviewer_prompt.md §4.13 to declare that R7 "has NO
  on-disk gate entry of its own". §4.13 exempts the last round of a BRANCH, and
  this branch continues through T003, T004, the integration gate and closure —
  R7 ended a SESSION, which §4.13 does not cover. Left standing, the line tells
  a later reviewer no gate is owed and "no repair round is opened to close it",
  stranding R-0231 and R-0232 on `Landed:` lines forever, because §4.4 reserves
  `Done:` for reviewer text. Fix: state why §4.13 does not apply here. OPEN.
  Done: R-0233 (2026-08-09) — RESOLVED. The R7 step line now states that §4.13
  exempts the last round of a BRANCH and that R7 ended a SESSION, so its gate
  was owed; the R7 gate record sits directly below it under `## Steps`. Verified
  on disk by the reviewer: the four-line terminator claim the finding quoted
  occurs 0x and the corrected text 1x.
- R-0234 (Low, F105 R5 and R6, reviewer-authored defect): both the R5 and the R6
  gate records cite `test_test_runner.py` by bare basename, but TWO files carry
  that name — `tests/test_test_runner.py` (43 tests) and
  `tests/orchestration/test_test_runner.py` (51 tests). Re-run as written, the
  record selects the 43-test file, where the R7 gate's `-k` filter reports `43
  deselected` and no tests run; this reviewer lost a run to exactly that. The
  number 51 is real and belongs to the orchestration file, so only the citation
  is wrong — but a gate record that cannot reproduce its own result reads as a
  regression. Fix: cite the full path in both records. OPEN.
  Done: R-0234 (2026-08-09) — RESOLVED. The R5 and R6 gate records now cite
  `tests/orchestration/test_role_conventions.py`'s sibling by full path, so
  re-running either record's own command selects the 51-test file it reports
  instead of the 43-test one that deselects everything.
- R-0235 (Low, F105 R8 completion round, worker record defect): the R8 handoff's
  path counts disagree with the real diff. Its gate K row reports the range as
  "5 paths" where `git diff --stat c95db6e7..337ba21f` lists SIX, and its
  Deviations section reports "Three paths total" where that round's own three
  commits touch FOUR. The worker's completion report carried both numbers
  correctly, so only `.agent/handoff.md` — the sole return channel
  (docs/agents/planner_reviewer_prompt.md §4.8) — states them wrong. Nothing
  escaped scope: every path is under `.agent/` and the reviewer re-derived both
  counts before passing the round. The cost is a later reviewer's: spot-checking
  "did this round touch only what it declared" compares a declared count against
  the real one, and a mismatch reads as an undeclared path until a round is
  spent disproving it. Fix: the next handoff derives every path count from
  `git diff --stat` at write time and names that command as its source. OPEN.
  Done: R-0235 (2026-08-09) — RESOLVED. The R9 handoff derives its path counts
  from `git diff --stat 337ba21f..HEAD` and names that command as the source,
  once in the commit tables and again in the deviations. The reviewer re-derived
  the same range independently and got six paths, all under `.agent/`, matching.
  No count in that handoff disagrees with the diff.
- R-0236 (Medium, F105 R9, reviewer-authored defect): the R9 step block is 254
  lines against the 240-line cap DECISION F105 D2 sets, and the reviewer emitted
  it without counting. C1 saves a block to TWO paths, so the 14-line overage
  cost 28 insertions and left C1 at 488 of the 500-insertion commit cap — six
  more lines of authored text and the round would have needed an unplanned
  split, which is what R5 already spent a finding on. The worker declared the
  overage and refused to trim reviewer text; that behaviour is correct and is no
  part of this finding. Fix: the reviewer counts every block BEFORE emitting it,
  and C1 reports the real count against the cap so the claim is falsifiable by
  the worker instead of discovered at the gate. OPEN.
  Done: R-0236 (2026-08-09) — RESOLVED. The R10 block was counted before it was
  emitted and C1 reported the real number: 240 lines / 15250 bytes, exactly AT
  the DECISION F105 D2 cap and not over it. The reviewer re-ran `wc -l -c` on the
  committed `.agent/authored/f105-r10-1.md` and got the same two numbers, so the
  claim was falsifiable and was checked rather than taken. C1's commit came in at
  404 insertions against the 500 cap, where R9 sat at 488.
- R-0237 (Low, F105 R9, inventory omission): `.agent/t003_inventory.md` closes
  site 4 by arguing that reordering the rules ahead of the mission changes bytes
  and is therefore a content change by the feature file's own definition, and
  concludes that the site's golden cannot be a pure equality golden. The feature
  file answers that in the same sentence the inventory paraphrases:
  docs/roadmap/features/T2_F105.md requires "golden before/after
  content-equality tests per builder, modulo ordering". Modulo ordering IS the
  answer — the golden pins the segment SET and each segment's bytes, not the
  concatenated string, which is exactly why a reorder counts as composition and
  not as content. Left uncited, T003's first builder round either re-derives the
  clause or concludes no golden is possible and invents a weaker one. Fix: cite
  the clause where the inventory raises the tension. OPEN.
  Done: R-0237 (2026-08-09) — RESOLVED. Site 4 of `.agent/t003_inventory.md` now
  cites the modulo-ordering clause where it raises the tension, so T003's first
  builder round reads the answer instead of re-deriving it. Spot-checked against
  the source rather than accepted: `docs/roadmap/features/T2_F105.md:18` does
  carry the words "modulo ordering", and the inventory quotes them correctly.
- R-0238 (Medium, F105 R11, reviewer-authored defect): the R11 step block is 257
  lines against the 240-line cap DECISION F105 D2 sets — 17 over, where R-0236
  was 14 over. R-0236 was resolved on R10's evidence and re-broken by the very
  next block, so the control it installed does not work: it asked the reviewer
  to count, and this reviewer's sandbox rejects the shell pipelines a count
  needs, so "counted" degraded to "estimated by hand" and the estimate was off
  by 22 lines. Not hypothetical — C1 saves the block to TWO paths, so R11's C1
  landed at 453 insertions of the 500-insertion cap. Fix: a count is MECHANICAL
  or it is not a count. The reviewer splits the drafted block into pieces small
  enough for its tool layer to parse, counts each with a `python3 - <<PY`
  heredoc — no pipeline, so it runs — and emits only once the sum is at most
  240. A hand estimate is never again reported as a count. OPEN.
  Fix amended at the R12 gate (2026-08-09), because R-0238 RECURRED: the R12
  block came in at 243, three over. The mechanical count DID run — three pieces
  measured 103, 62 and 78, summing to 245 — and then the reviewer trimmed six
  lines by hand and claimed 239 without recounting, so a mechanical measurement
  was turned back into an estimate at the last step. Amended fix: the pieces are
  counted from the FINAL text, and any edit after a count voids it and forces a
  recount. R-0238 stays OPEN until a block lands at or under 240.
  Done: R-0238 (resolved at the R14 gate, 2026-08-09). The R13 block landed at
  231 lines / 13795 bytes, measured by the reviewer with `wc -lc` on BOTH
  `.agent/authored/f105-r13-1.md` and `.agent/last_block.md` — 9 under the cap,
  counted mechanically with no edit after the count. That is the resolution
  condition this finding set itself, met on the first block after the
  amendment. RESOLVED.
- R-0239 (Low, F105 R12, reviewer-authored defect): the R12 step block's gate E
  cited `tests/test_do_run.py`, which does not exist — the real file is
  `tests/orchestration/test_do_run.py`, and the reviewer read that name out of
  an `ls tests/orchestration/` listing and then wrote the wrong prefix. The
  worker caught it, ran the real path, and declared the correction, so nothing
  was skipped and no number is wrong. This is the R-0234 class exactly: a gate
  citation that cannot be re-run as written costs the next reader a run to
  discover it is a typo and not a regression, and R-0234's own fix — cite the
  full path — was already on disk when this was authored. Fix: full paths are
  copied from a listing, never reconstructed from memory of one. OPEN.
- R-0240 (Low, F105 R13, reviewer-authored defect): `.agent/live_review.md`
  line 8 reads "Next free ID: R-0238" while R-0238 and R-0239 are both
  registered below it, so the header contradicts its own findings list and
  disagrees with `.agent/plan.md`, which correctly carries R-0240. It was one
  behind at 927bfdad and R13 made it two. The R13 worker declared this as an
  observation and correctly refused to widen its authorised change set, so the
  defect is the reviewer's: the R13 block registered a finding without also
  authoring the header pair its own numbering required. Two disagreeing sources
  of the next free ID is how an ID gets reused, and a reused ID silently
  overwrites a finding's history. Fix: any block that registers or resolves a
  finding carries, in the same pair set, the rewrite of the header's
  next-free-ID line. Applied at C3 of this block. OPEN until it lands.
- R-0241 (Low, F105 R13, reviewer-authored defect): `.agent/plan.md` and the
  R13 handoff both label the next builder "T003 SITE 2" while naming
  `packages/orchestration/mission_compiler.py::build_mission_prompt`. Those
  halves disagree with `.agent/t003_inventory.md`, which numbers its CATALOGUE
  `## Site 1` to `## Site 6` and keeps a SEPARATE `## Migration order` list.
  `build_mission_prompt` is catalogue Site 6 and migration-order step 2; the
  inventory's `## Site 2` is `_build_reviewer_prompt`, which that list puts LAST
  as the hardest of the six. A reader following the label lands on the worst
  possible target and finds out only after reading the wrong function. Nothing
  was built wrongly — the function name carried the truth — but the label is a
  trap. Fix: plan and handoff say "migration-order step N" and always name the
  function; "Site N" is reserved for the inventory's catalogue headings.
  Applied in this block's authored plan text. OPEN until it lands.
  Done: R-0240 and R-0241 (resolved at the R14 gate, 2026-08-09). Both fixes
  landed in R14 and the reviewer confirmed each on disk rather than from the
  handback: line 8 now reads "Next free ID: R-0242" and the stale R-0238
  spelling occurs 0x, closing R-0240; `.agent/plan.md` now counts in the
  MIGRATION ORDER and names `mission_compiler.py::build_mission_prompt` without
  the "Site N" label, closing R-0241. RESOLVED.
- R-0242 (Low, F105 R14, reviewer-authored defect): every block on this branch
  puts the `.agent/plan.md` rewrite in its LAST commit, so intermediate commits
  carry the previous round's plan — at R14, C2 and C3 committed while the plan
  still read "Next finding ID: R-0240" after both findings were registered. The
  worker declared it rather than taking it silently. AGENTS.md's Commit Gate
  item 1 verifies plan.md against current work before EVERY commit and documents
  no exception, so the branch runs on an unpersisted convention — the class the
  planner/reviewer prompt calls a practice invoked without a doc pointer. Fix:
  settle it as a DECISION that either exempts intra-round commits or moves the
  plan rewrite earlier, then cite it from every later block. Not settled here:
  inventing a rule in a terminator round is how unreviewed conventions start.
  OPEN.
- R-0243 (Medium, F105 R14 and R15, process defect in the reviewer's own
  authoring): DECISION F105 D2 caps a step block at 240 lines and its remedy for
  an over-cap round is a split, but the content a reviewed round MUST carry —
  the gate verdict, the finding registrations and resolutions, the header pair,
  and the verbatim `.agent/plan.md` — costs roughly 150 lines before any feature
  work is described. The reviewer measured the combined gate-plus-migration
  block three times at R14 (293) and four times at R15 (329, 283, 276, 275) and
  could not fit it without degrading the record. The consequence is structural,
  not stylistic: R14 and R15 both became record-only rounds, so this session
  spent two rounds and merged no feature change, and the same split will recur
  every round that follows a gate. This is the ⚠️ momentum condition in
  docs/agents/planner_reviewer_prompt.md §2, named here rather than left for a
  reader to infer from the round log. Candidate fixes, for the next session to
  weigh and settle as a DECISION: raise the cap now that C1's cost is understood
  (2N insertions against the 500 commit cap allows about 245); or exempt the
  authored `.agent/plan.md` slice from the block count, since it is state text
  rather than instruction; or move the gate verdict out of the step block into a
  reviewer-written record the worker copies from scratch, the way this block's
  own bytes already travel. OPEN.
  Fix chosen at the R15 gate (2026-08-09) as DECISION F105 D5, written at C4 of
  this block: the block stops being counted twice. C1 splits into C1a, which
  commits `.agent/authored/<round>.md` alone and counts its N insertions against
  the AGENTS.md 500 cap, and C1b, which rewrites `.agent/last_block.md` alone —
  the verbatim rewrite of a SINGLE `.agent/**` state file named in the AGENTS.md
  Commit Discipline exemption, and therefore exempt exactly as written, with no
  rule reinterpreted. D2's rejected alternative is not revived: the block still
  meets a 500-line ceiling at C1a, so the pressure keeping blocks short survives
  and only the doubling artifact goes. The cap moves 240 -> 400. R-0243 stays
  OPEN until a round lands a gate record AND a feature change out of one block —
  the condition R16 is built to meet, held to the same discipline as R-0238,
  which was resolved on a landing and not on a promise.
- R-0244 (Low, F105 R15, reviewer-authored defect): the authored `.agent/plan.md`
  text is 54 lines against the AGENTS.md plan.md rule "keep it short (<50
  lines)". The R14 plan was 49 and inside it; R15 regressed past it while
  compressing its block four times, so the lines the block saved were spent in
  the state file instead. The worker declared the overage and correctly refused
  to trim reviewer-authored text, so the defect is the reviewer's alone.
  AGENTS.md is the highest authority and no rule of it may be weakened by an
  authoring convenience; a plan outgrowing its own cap is also the first symptom
  of a plan turning into a log, which is what the cap exists to prevent. Fix:
  the authored plan slice is counted before it is emitted and lands at 49 lines
  or fewer. Applied at C6 of this block. OPEN until it lands.

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
  22 passed, `tests/docs/` 294 passed,
  `tests/orchestration/test_test_runner.py` 51 passed, the
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
  `tests/docs/` 294 passed, `tests/orchestration/test_test_runner.py` 51
  passed, the canary 42
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
  docs/agents/planner_reviewer_prompt.md §4.13 this round would have NO on-disk
  gate entry of its own. CORRECTED at the R7 gate (R-0233): §4.13 exempts the
  last round of a BRANCH, and this branch continues through T003, T004, the
  integration gate and closure. R7 ended a SESSION, not the branch, so its gate
  IS owed and is recorded directly below.
- Reviewer gate on R7 (2026-08-09): PASS. Range `c0ce100a..c95db6e7` read as a
  real diff — five paths, ALL under `.agent/`, exactly the change set the R7
  block named; no `packages/`, `apps/`, `tests/`, `docs/`, `AGENTS.md` or
  `.agent/context.md` byte changed. Per-commit insertions 359, 18, 45, 2 and
  111, every one under the 500 cap. Gates re-run by the NEXT session's reviewer
  from the repo root with real exit codes: `cmp` of the authored block against
  `.agent/last_block.md` exit 0 and no output;
  `tests/orchestration/test_test_runner.py -k "live_review or context_md or
  plan_md"` 4 passed 47 deselected; `tests/docs/` 294 passed; in
  `tests/orchestration/`, `test_role_conventions.py` plus
  `test_prompt_segments.py` 48 passed; the canary 42 passed; integrity
  `passed=True`, `fail_count=0` over 5 checks; tree clean; the primary checkout
  the only worktree; HEAD equal to origin.
  Authored-text application re-proved on disk, not by retype: both finding
  paragraphs, the R6 gate record, the R7 step line and the pair-C TO header each
  occur exactly 1x as sliced from `.agent/authored/f105-r7-1.md`, the pair-C
  FROM 0x, `.agent/plan.md` equals its authored 48-line slice exactly, and each
  `Landed:` line occurs 1x with no worker-authored `Done:` anywhere. The block
  is 206 lines / 12802 bytes, no CR, no trailing whitespace, final newline. Both
  declared deviations are ACCEPTED: gate J was unsatisfiable by construction and
  was reported rather than fitted, and the overage is what D15 permits. The two
  defects found are the REVIEWER's own authoring, which is why this round passes;
  registered as R-0233 and R-0234. `LAST_REVIEWED_SHA` advances -> c95db6e7.
- R8: the record-integrity round — the R7 gate recorded, R-0231 and R-0232
  resolved with reviewer-authored text, R-0233 and R-0234 registered and fixed.
  `.agent/` state only; T003 starts in R9.
- Reviewer gate on R8 (2026-08-09): PASS. R8 ran across TWO worker sessions —
  C1-C4, then a completion round after that worker died before C5. Range
  `c95db6e7..337ba21f` read as a real diff: seven commits, six paths, ALL under
  `.agent/`; no `packages/`, `apps/`, `tests/`, `docs/`, `AGENTS.md`,
  `.agent/context.md` or `.agent/decisions.md` byte changed. Per-commit
  insertions 432, 18, 35, 11, 143, 24 and 80, every one under the 500 cap.
  Gates re-run by the reviewer from the repo root with real exit codes: `cmp` of
  the completion block against `.agent/last_block.md` exit 0 and no output;
  `tests/orchestration/test_test_runner.py -k "live_review or context_md or
  plan_md"` 4 passed 47 deselected; `tests/docs/` 294 passed;
  `tests/orchestration/test_role_conventions.py` plus `test_prompt_segments.py`
  48 passed; the canary `tests/cli/test_golden_path.py` 42 passed; integrity
  `passed=True`, `fail_count=0` over 5 checks; tree clean; the primary checkout
  the only worktree; HEAD equal to origin. The interrupted C5 is proved harmless
  ON DISK, not by report: `.agent/plan.md` as committed equals lines 177-220 of
  `.agent/authored/f105-r8-1.md` byte for byte, sha256 5a85ee84 on both sides,
  so the dead worker's uncommitted write was the authored text and nothing else.
  All ten pair counts were re-derived by the reviewer with every needle sliced
  out of the authored block: both new finding paragraphs, both `Landed:` lines,
  the R-0231 and R-0232 `Done:` paragraphs and the R7 gate record 1x each, the
  pair C, D and F FROM strings 0x each. The declared handoff overage is what D15
  permits. One record defect found, registered as R-0235.
  `LAST_REVIEWED_SHA` advances -> 337ba21f.
- R9: the T003 inventory round — the R8 gate recorded, R-0233 and R-0234
  resolved, R-0235 registered and fixed, and `.agent/t003_inventory.md` written.
  READ-ONLY on the code: no builder migrated, no golden written, no test added.
- Reviewer gate on R9 (2026-08-09): PASS. Range `337ba21f..9b50fafe` read as a
  real diff: five commits, SIX paths, ALL under `.agent/`; no `packages/`,
  `apps/`, `tests/`, `docs/`, `docs/roadmap/`, `AGENTS.md`, `.agent/context.md`,
  `.agent/decisions.md` or `.agent/candidates.md` byte changed, so the round was
  read-only on the code exactly as it declared. Per-commit insertions 488, 14,
  35, 262 and 98, every one under the 500 cap. Gates re-run by the reviewer from
  the repo root with real exit codes: `cmp` exit 0 and no output;
  `tests/orchestration/test_test_runner.py -k "live_review or context_md or
  plan_md"` 4 passed 47 deselected; `tests/docs/` 294 passed;
  `tests/orchestration/test_role_conventions.py` plus `test_prompt_segments.py`
  48 passed; the canary `tests/cli/test_golden_path.py` 42 passed; integrity
  `passed=True`, `fail_count=0` over 5 checks; tree clean; the primary checkout
  the only worktree; HEAD equal to origin. All TWELVE pair counts were
  re-derived by the reviewer with every needle sliced out of
  `.agent/authored/f105-r9-1.md`: the three rewrite FROMs 0x with their TOs 1x,
  the three append FROMs 1x with each TO-only addition 1x. `.agent/plan.md`
  equals its authored 42-line slice exactly, sha256 9702bc68 on both sides. The
  inventory was SPOT-CHECKED against the source rather than accepted: intake's
  `Rules:` block does sit after `{mission}` in `_INTAKE_PROMPT_TEMPLATE`, and
  both `plan_job_llm` call sites in `apps/cli/commands/do_cmd.py` do pass a call
  function and no `on_call`, as it claims. Two defects registered, R-0236 and
  R-0237; neither is in the inventory's findings, which stand.
  `LAST_REVIEWED_SHA` advances -> 9b50fafe.
- R10: the session-terminator round — the R9 gate recorded, R-0235 resolved,
  R-0236 and R-0237 registered and fixed, the session-end handoff written. The
  session ends at its DECLARED THREE-ROUND CAP; T003 starts next session. R10
  ends a SESSION, not the branch, so its own gate is OWED and the next session's
  reviewer records it (R-0233's correction to §4.13).
- Reviewer gate on R10 (2026-08-09): PASS. Range `9b50fafe..9d773b14` read as a
  real diff by the NEXT session's reviewer: five commits, SIX paths, ALL under
  `.agent/`. `git diff --name-only 9b50fafe..HEAD -- packages apps tests docs
  AGENTS.md README.md` returns NOTHING, so the round was read-only on the code
  exactly as it declared. Per-commit insertions 404, 23, 33, 2 and 95, every one
  under the 500 cap. Gates re-run from the repo root with real exit codes: `cmp`
  of the authored block against `.agent/last_block.md` exit 0 and no output; the
  block 240 lines / 15250 bytes, AT the D2 cap and not over, so R-0236's fix held
  on its first use; `tests/orchestration/test_test_runner.py -k "live_review or
  context_md or plan_md"` 4 passed 47 deselected; `tests/docs/` 294 passed;
  `tests/orchestration/test_role_conventions.py` plus
  `tests/orchestration/test_prompt_segments.py` 48 passed; the canary
  `tests/cli/test_golden_path.py` 42 passed; integrity `passed=True`,
  `fail_count=0` over 5 checks; `git status --porcelain` empty; the primary
  checkout the only worktree; HEAD equal to origin. Every pair count was
  re-derived with the needle SLICED out of `.agent/authored/f105-r10-1.md`:
  rewrites B and C end FROM 0x TO 1x, appends A, D, E and F end FROM 1x with each
  TO-only addition 1x. One nuance, recorded so no later reader re-finds it as a
  defect: pair A's TO-only region matches 1x per paragraph but NOT as one
  contiguous slice, because C5's `Landed: R-0236` line sits between the two
  paragraphs, exactly where C5 was told to put it. `.agent/plan.md` equals its
  authored 46-line slice, sha256 241a03e3 on both sides. The R-0237 fix was
  spot-checked at the source: `docs/roadmap/features/T2_F105.md:18` really does
  carry "modulo ordering". The declared handoff overage is what D15 permits, and
  the declared gate-M collision is the F104 R11 "gate quotes its own marker"
  class, reported rather than fitted. No new finding. `LAST_REVIEWED_SHA`
  advances 9b50fafe -> 9d773b14.
- R11: T003 SITE 1 — `packages/orchestration/intake.py::_build_intake_prompt`
  composes through the prompt-segment registry, under the content-equality
  golden `tests/orchestration/test_intake_prompt_golden.py`. Composition only:
  the segment manifest reaches call evidence in R12, split off so each diff is
  one reviewable idea rather than a migration and an evidence rewiring at once.
  Sites 2-6 stay untouched.
- Reviewer gate on R11 (2026-08-09): PASS. Range `9d773b14..0f17725a`, four
  commits, SEVEN paths — five under `.agent/` plus
  `packages/orchestration/intake.py` and the new
  `tests/orchestration/test_intake_prompt_golden.py`; `git diff --name-only`
  over `apps docs AGENTS.md README.md .agent/context.md .agent/decisions.md
  .agent/candidates.md` returns NOTHING. Per-commit insertions 453, 44, 153, 103
  — each under the 500 cap. Gates re-run by the reviewer with real exit codes:
  `cmp` exit 0; the golden plus `tests/orchestration/test_intake.py` 42 passed,
  the pre-existing file unchanged at 37; `test_prompt_segments.py`,
  `test_role_conventions.py`, `test_test_runner.py` 99; `tests/docs/` 294; the
  canary 42; `grep -rn "_INTAKE_PROMPT_TEMPLATE" packages/ apps/` 0 hits;
  integrity `passed=True`, `fail_count=0` over 5; tree clean, no untracked
  files; HEAD equal to origin. All six pair counts re-derived with each needle
  SLICED out of `.agent/authored/f105-r11-1.md`; `.agent/plan.md` equals its
  authored 43-line slice, sha256 cde2364d both sides. THREE mutation red-proofs
  ran in a disposable worktree at 0f17725a, removed and pruned before this
  verdict: demoting `intake_rules` to STEERING turns 3 golden tests RED,
  rewording ONE word of the rules block turns 2 RED, dropping the rules
  registration turns 4 RED — the golden is load bearing on order, on content AND
  on segment loss. Both declared worker deviations ACCEPTED; the unimplementable
  wording in golden test 1 was the reviewer's and the replacement is stronger.
  One new finding, R-0238, the reviewer's own. `LAST_REVIEWED_SHA` advances
  9d773b14 -> 0f17725a.
- R12: T003 SITE 1 part 2 — the intake segment manifest reaches call evidence.
  `PromptTraceEntry` gains the manifest rows and the character count they cover,
  `packages/orchestration/intake.py` gains the named recorder factory that fills
  them, and `apps/cli/commands/do_cmd.py` uses it. No prompt byte and no
  composition change. DECISION F105 D3 — the schema tail stays unregistered, its
  coverage gap made visible through `segment_manifest_chars` — is documented in
  the code this round and lands in `.agent/decisions.md` at R13.
- Reviewer gate on R12 (2026-08-09): PASS. Range `0f17725a..927bfdad`, five
  commits, NINE paths — five under `.agent/` plus
  `packages/orchestration/prompt_trace.py`,
  `packages/orchestration/intake.py`, `apps/cli/commands/do_cmd.py` and
  `tests/orchestration/test_prompt_trace.py`. `git diff --name-only` over
  `docs AGENTS.md README.md .agent/context.md .agent/decisions.md
  .agent/candidates.md .agent/t003_inventory.md` and the R11 golden returns
  NOTHING, so the golden really did pass unedited. Per-commit insertions 434,
  12, 30, 153 and 88 — each under the 500 cap. Gates re-run by the reviewer
  with real exit codes: `cmp` exit 0 and no output;
  `tests/orchestration/test_prompt_trace.py` plus the R11 golden plus
  `tests/orchestration/test_intake.py` 79 passed, which is 37 + 42 with the
  golden's 5 and intake's 37 both unchanged;
  `tests/orchestration/test_structured_outputs.py`,
  `test_provider_mode.py`, `test_agent_run_trace.py` and
  `tests/orchestration/test_do_run.py` 159 passed; the canary
  `tests/cli/test_golden_path.py` plus `tests/docs/` 336 passed; integrity
  `passed=True`, `fail_count=0`; tree clean with no untracked files; the
  primary checkout the only worktree; HEAD equal to origin. Both pairs are
  appends and both proved FROM 1x with the TO-only addition 1x, every needle
  SLICED out of `.agent/authored/f105-r12-1.md`; `.agent/plan.md` equals its
  authored 37-line slice, sha256 1a2da455 both sides. TWO mutation red-proofs
  ran in a disposable worktree at 927bfdad, removed and pruned before this
  verdict, and they test the two halves of the wiring separately: dropping
  `composed_prompt=composed` from the recorder turns
  `test_the_cli_recorder_passes_the_composed_prompt` RED, and deleting the
  `on_call=make_intake_call_recorder(...)` argument from
  `apps/cli/commands/do_cmd.py` turns the same test RED. A field wired into the
  model but never filled by the CLI therefore cannot pass — which is the
  failure this round was most exposed to. All five declared deviations
  ACCEPTED. Two defects found, BOTH the reviewer's own: R-0238 recurred at 3
  over cap and its fix is amended above rather than resolved, and the wrong
  test path is registered as R-0239. `LAST_REVIEWED_SHA` advances
  0f17725a -> 927bfdad.
- R13: the session-terminator round — R-0238's fix amended, R-0239 registered,
  the R12 gate recorded, DECISION F105 D3 written to the ledger, the
  session-end handoff written. The session ends at its DECLARED THREE-ROUND CAP
  (R11, R12, R13) under docs/agents/self_drive_protocol.md G7. R13 ends a
  SESSION, not the branch, so its own gate is OWED and the next session's
  reviewer records it (R-0233's correction to §4.13).
- Reviewer gate on R13 (2026-08-09): PASS. Range `927bfdad..HEAD` at 2d993ed9,
  five commits, SIX paths, all under `.agent/`. Per-commit insertions, read by
  the reviewer from `git log --numstat`: 394, 17, 40, 21, 101 — each under the
  500 cap and each equal to the handoff's own table. Gates re-run by the
  reviewer with real results: `cmp` of the authored block against
  `.agent/last_block.md` exit 0, no output; `wc -lc` 231 lines / 13795 bytes on
  BOTH, the first block at or under D2's cap of 240;
  `tests/orchestration/test_test_runner.py -k "live_review or context_md or
  plan_md"` 4 passed, 47 deselected; `tests/docs/` 294 passed;
  `tests/orchestration/test_prompt_trace.py`,
  `tests/orchestration/test_intake_prompt_golden.py` and
  `tests/orchestration/test_intake.py` 79 passed, 79 before and after; canary
  `tests/cli/test_golden_path.py` 42 passed; integrity `passed=True`,
  `fail_count=0`, 5 checks; `git worktree list` the primary alone at 2d993ed9;
  `git status --porcelain` empty. Transport proved disk to disk, not by retype:
  all 78 lines the range adds to `.agent/live_review.md` and
  `.agent/decisions.md` occur verbatim in `.agent/authored/f105-r13-1.md`, zero
  missing, and `.agent/plan.md` equals block lines 172-212, sha256 2ed24940 both
  sides. Both declared deviations ACCEPTED: the D15 handoff overage at 124 lines
  is mandated content only, and the `subprocess.run` exit-code transport was
  re-run directly by the reviewer with the same results. R-0238 RESOLVES here.
  Two defects registered, BOTH the reviewer's own: R-0240 and R-0241.
  `LAST_REVIEWED_SHA` advances 927bfdad -> 2d993ed9.
- R14: the record half of the R13 gate — R-0238 resolved, R-0240 and R-0241
  registered and fixed, the gate recorded. No builder migrated: the combined
  block measured 293 lines, over DECISION F105 D2's cap, so the migration moves
  to R15 under D2's own split remedy. R14's gate is owed at R15.
- Reviewer gate on R14 (2026-08-09): PASS. Range `2d993ed9..HEAD` at 73e159b7,
  four commits, FIVE paths, all under `.agent/`. Per-commit insertions from
  `git log --numstat`: 407, 31, 28, 100 — each under the 500 cap and each equal
  to the handback's table. Transport is the strongest this branch has recorded:
  the reviewer's scratch original, the committed
  `.agent/authored/f105-r14-1.md` and `.agent/last_block.md` share one sha256,
  de2bfec6, so both `cmp` runs are exit 0 against a SURVIVING original rather
  than a reconstruction; 231 lines / 14237 bytes, 9 under the cap. All 59 lines
  the range adds to `.agent/live_review.md` occur verbatim in the authored file,
  zero missing, and the ONE removed line is exactly pair C's FROM. `.agent/plan.md`
  is a contiguous 49-line slice, block lines 164-212, sha256 9607d792. Pair
  placement was checked structurally, not only by count: the R13 gate landed
  after R13's own step line and the R10 record at line 421 is untouched, which
  is where the ambiguous one-line anchor the reviewer widened would have
  spliced it. Gates re-run by the reviewer: state contracts 4 passed / 47
  deselected; `tests/docs/` 294 passed; canary 42 passed; integrity
  `passed=True`, `fail_count=0`; tree clean; primary the only worktree; HEAD
  equal to origin. Deviations 1 and 2 ACCEPTED on R13's grounds. Deviation 3,
  the plan stale between C1 and C3, is NOT waved through: registered as R-0242.
  `LAST_REVIEWED_SHA` advances 2d993ed9 -> 73e159b7.
- R15: the record half of the R14 gate — R-0240 and R-0241 resolved, R-0242 and
  R-0243 registered, the gate recorded. No builder migrated: the combined block
  measured 275 lines after four compression passes, over D2's cap, so the
  migration and DECISION F105 D4 move to R16. The session revised its declared
  cap from two rounds to three, stated in this block rather than taken
  silently, and R15's own gate is owed at R16.
- Reviewer gate on R15 (2026-08-09): PASS. Range `73e159b7..HEAD` at ed5b2421,
  four commits, FIVE paths, all under `.agent/`. Per-commit insertions read by
  the reviewer from `git log --numstat`: 388 (227 + 161), 38, 26 and 96
  (66 + 30) — each under the 500 cap. The R15 handoff left C4's number to the
  completion report; it is 96, derived here rather than accepted. Transport is
  proved against a SURVIVING original: `.remedy-wt/f105-r15-1.block.md`,
  `.agent/authored/f105-r15-1.md` and `.agent/last_block.md` all hash to
  b0bbc7d6, both `cmp` runs exit 0, at 227 lines / 14333 bytes, 13 under D2's
  cap. Application is proved disk to disk, not by retype: of the 64 lines the
  range adds to `.agent/live_review.md`, 64 occur verbatim in the authored file
  and 0 are missing, and the single removed line is exactly pair B's FROM, so
  the rewrite landed where it was aimed and nowhere else. `.agent/plan.md`
  equals its authored slice at block lines 155-208, sha256 4fb762f5 both sides.
  Gates re-run by the reviewer with real exit codes: state contracts 4 passed /
  47 deselected; `tests/docs/` 294 passed; canary `tests/cli/test_golden_path.py`
  42 passed; integrity `passed=True`, `fail_count=0` over 5 checks;
  `git status --porcelain` empty; `git worktree list` the primary alone; HEAD
  equal to origin. Deviations 1, 2 and 5 ACCEPTED — the D15 handoff overage is
  mandated content only, the `bash -c` exit-code transport was re-run directly
  by the reviewer with identical results, and `.remedy-wt/` is ignored at
  `.gitignore:235` with nothing tracked. Deviation 3 is R-0242's own declared
  condition and stays with it. Deviation 4 is NOT waved through: a 54-line
  `.agent/plan.md` breaks an AGENTS.md rule, and it is registered as R-0244. One
  defect found, the reviewer's own. `LAST_REVIEWED_SHA` advances
  73e159b7 -> ed5b2421.
- R16: the round that ends the record-only stall — the R15 gate recorded, R-0244
  registered, R-0243 amended with its chosen fix, DECISIONS F105 D4 and D5
  written, and migration-order step 2,
  `mission_compiler.py::build_mission_prompt`, moved onto the registry under a
  new `tests/orchestration/test_mission_prompt_golden.py`. The mission manifest
  does NOT reach call evidence this round: no production caller passes `on_call`
  to `plan_mission` (`apps/cli/commands/mission_cmd.py:187`,
  `packages/orchestration/gauntlet_runner.py:505`), so that seam is its own
  later round, exactly as intake split across R11 and R12. R16's own gate is
  owed at R17.
