# Live Review — F105 Cache-optimal prompt ordering

> Reviewer: the main session of a one-session self-drive build
> (docs/agents/self_drive_protocol.md). Worker: one delegated subagent per
> round. Findings are authored here by the reviewer only. A worker marks a
> landed fix `Landed: R-XXXX`; only reviewer-authored `Done:` text sets
> Resolved (docs/agents/planner_reviewer_prompt.md §4.4).
> Branch: feature/f105-cache-optimal-prompt-ordering. Next free ID: R-0261.

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
  Done: R-0242 (2026-08-09) — RESOLVED as DECISION F105 D6, recorded in
  `.agent/decisions.md` at this round's C4. The convention is on disk with its
  reason and scope: within one round the plan rewrite closes the round, and the
  Commit Gate's plan check is met for the intermediate commits by
  `.agent/last_block.md`, which lands at C1b before any of them. D6 takes the
  exempting branch and says why the earlier-rewrite branch was refused.
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
  Done: R-0243 (resolved at the R16 gate, 2026-08-09). The condition this
  finding set for itself — one block landing a gate record AND a feature change
  — was met by R16 at 399 authored lines under DECISION F105 D5's cap of 400:
  the R15 gate record, two registrations, two DECISIONS, and migration-order
  step 2 with its golden, out of a single block, in seven commits whose largest
  is 399 insertions and none of which exceeds 500. The reviewer confirmed the
  counts from `git log --numstat` rather than from the handback. The forced
  split is gone because the block is no longer counted twice. RESOLVED.
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
  Done: R-0244 (resolved at the R16 gate, 2026-08-09). `.agent/plan.md` is 47
  lines and equals its authored slice byte for byte, sha256 8029c8ca on both
  sides, confirmed by the reviewer on disk. Inside the AGENTS.md cap with two
  lines to spare. RESOLVED.
- R-0245 (Low, F105 R16, worker record defect): `.agent/handoff.md` is 101 lines
  against the AGENTS.md cap of 60 — 100 where per-commit tables of more than
  five commits require it — and declares neither the overage nor its line count.
  DECISION D15 permits a stated-cause overage precisely so that a long handoff
  stays honest, and it requires the file to name its actual length and the
  mandated content that caused it; the R15 handoff did exactly that at 135
  lines. The same file also omits the item-status table AGENTS.md requires of
  every completion report covering an ordered bundle. The worker DID put one in
  its completion report to the reviewer, but that report dies with the session
  and the file is the only channel that survives it. Nothing is padded and
  nothing is fabricated; what is missing is the declaration and the table. Fix:
  a handoff over cap states its line count and its cause, and every handoff
  covering an ordered bundle carries the item-status table. OPEN.
  Done: R-0245 (resolved at the R17 gate, 2026-08-09). `.agent/handoff.md` is
  92 lines; `wc -l` returns 92, and the file's opening section declares that
  same number, names the AGENTS.md cap it exceeds and names the mandated content
  that caused the overage. The item-status table is present with all five bundle
  items, and both halves of the fix landed in the file that survives the
  session. RESOLVED.
- R-0246 (Low, F105 R16, reviewer-authored defect): `build_mission_prompt`'s
  docstring still ends "``None`` reproduces today's prompt byte for byte".
  Before R16 that sentence was about the `max_milestones` parameter alone and
  was unambiguous. After a migration whose entire point is that segment ORDER
  changed while segment BYTES did not, a reader landing on that line — and it is
  exactly where a search for "did the migration change the prompt?" lands — can
  read it as a claim that the byte SEQUENCE was preserved, which is false. The
  R16 block mandated that the docstring be kept unchanged, so the defect is the
  reviewer's and not the worker's. Fix: the sentence says what it means — a
  `None` cap reproduces the pre-R-0197 milestone ceiling, while the composed
  ORDER differs from the pre-migration template and the segment bytes do not.
  OPEN.
  Done: R-0246 (2026-08-10) — RESOLVED at F105 R30, commit 39da9b61. The
  docstring now says "reproduces the pre-R-0197 milestone CEILING — not the
  pre-migration byte SEQUENCE", and states that the composed order differs at
  every value of `max_milestones`, `None` included. Verified by the reviewer
  against the real diff, not the handback: the sentence a reader searching for
  "did the migration change the prompt?" lands on can no longer be read as a
  claim about byte order.
- R-0247 (Low, F105 R17, reviewer-authored defect in a finding's own citation):
  R-0245 opens "`.agent/handoff.md` is 101 lines". The file is 100:
  `git show efd66b68:.agent/handoff.md | wc -l` returns 100 and the blob ends in
  a newline, so no counting convention closes the gap — the number came from a
  draft, not from the command that produced it. The SUBSTANCE is untouched: 100
  exceeds the cap of 60 exactly as 101 would, and the missing declaration and
  item-status table are what the finding was about, both of which R17 fixed.
  Wrong is a cited number the reader cannot reproduce — the R-0234 and R-0239
  class, third instance on this branch, and each time it costs a run deciding
  between a typo and a file that changed underneath. Fix: any count entering a
  finding is pasted from that command's own output in the same sitting. OPEN.
- R-0248 (Low, F105 R18, defect in a DECISION's account of its own mechanism):
  DECISION F105 D6, landed this round, says the Commit Gate's plan check is met
  for a round's intermediate commits by `.agent/last_block.md`, "which carries
  the round's plan verbatim and is committed BEFORE any of them at C1b". C1a
  commits `.agent/authored/<round>.md` and C1a runs BEFORE C1b — D5 split them
  in that order precisely so the block is counted once. So exactly one commit
  per round, the first, is not covered by the mechanism D6 names, and D6's
  "before any of them" is false for it. The worker declared the gap rather than
  reordering, which was right: reordering C1a after C1b would defeat D5. The
  SUBSTANCE of D6 is unaffected — C1a adds a file that is a verbatim copy of
  the block, so the plan of record and the commit agree by construction, which
  is the very thing D6 argues makes the mechanism sound. What is wrong is the
  word "any", which overclaims coverage a reader can falsify in one `git log`.
  Fix: D6's sentence names C1b onward, and states that C1a is covered by being
  the block's own verbatim copy rather than by `.agent/last_block.md`. Amend the
  entry in place, in the round that next touches `.agent/decisions.md`.
  Done: R-0248 — fixed at F105 R20, in the round that next touched
  `.agent/decisions.md`, exactly as the finding directed. DECISION D6's
  mechanism sentence now reads "from C1b onward" and states that C1a is covered
  by committing the block's own verbatim copy, so the coverage claim matches
  what `git log` shows. The amendment is marked as an amendment inside the
  entry, naming R-0248 and quoting the phrase that overclaimed, so a later
  reader can see what changed without diffing. RESOLVED.
- R-0249 (Low, F105 R19, the plan names a narrower function than the migration
  order does): `.agent/plan.md` sends R20 to "migration-order step 4,
  `orchestrator_loop.py::build_orchestrator_system_prompt`". The migration order
  in `.agent/t003_inventory.md` — which that same plan names as the authority
  over how T003 is counted — lists step 4 as `build_orchestrator_prompt`, the
  OUTER composition at line 797, and describes it as "two segments, already
  rank-ordered". `build_orchestrator_system_prompt` at line 89 is only its
  rank-0/rank-1 half. A worker reading the plan alone migrates the inner
  function and leaves the outer one an f-string that concatenates a composed
  prompt with a raw section header; the round's own acceptance — this prompt
  composes from registered segments — is then false for the prompt actually
  sent, and the manifest describes a strict prefix of it. This is not a wrong
  spec: the inventory is right and the plan abbreviated it. Fix: the plan names
  `build_orchestrator_prompt` and says its system half migrates with it. The
  fix lands in this round's plan rewrite; the next gate verifies it and
  resolves this entry.
  Done: R-0249 — fixed at F105 R20 and verified at R21. `.agent/plan.md` now
  reads "step 4 covers `build_orchestrator_prompt` AND its system half
  `build_orchestrator_system_prompt`", so the plan and the migration order name
  the same work. The reviewer confirmed the wider reading was the correct one
  by reconstructing the pre-migration builders from
  `git show 04a3396d:packages/orchestration/orchestrator_loop.py` and diffing
  both renders: had only the inner function migrated, the outer f-string would
  still have concatenated a composed prompt with a raw `# Mission state`
  header, and the manifest would have described 3852 of 3861 characters instead
  of all of them. RESOLVED.
- R-0250 (Medium, F105 R20, reviewer-authored gates that cannot be satisfied):
  R20's block carried FOUR defects, all in reviewer-authored text and all
  correctly caught, declared and worked around by the worker rather than
  silently absorbed. (1) The block was 471 lines against DECISION D5's cap of
  400, and because a worker must save the block verbatim it could not be fixed
  downstream. (2) The authored `.agent/plan.md` replacement was 56 lines
  against AGENTS.md's <50, and a slice required to apply byte for byte cannot
  be trimmed by the applier — so a reviewer defect landed a live rule violation
  on disk. (3) Done-when C required
  `grep -c 'committed BEFORE any of them at C1b' .agent/decisions.md` to be 0,
  while the same block's PAIR_D_TO deliberately wrote that phrase into that
  same file as a quotation of the retired text: unsatisfiable by construction.
  (4) PAIR_F was declared APPEND when its TO edits the FROM line, making it a
  REWRITE. Defect (3) is the FIFTH instance of its class across F104 R11 and
  F105, and each instance costs a round a deviation that proves a reviewer
  mistake rather than a worker one. The common cause is that all four checks
  are mechanical, are known, and lived only in reviewer session memory — the A1
  trap named in docs/agents/planner_reviewer_prompt.md §0. Fix: a pre-emission
  checklist in that file's §3, installed as DECISION F105 D8 in the same round
  as this entry, so the next reviewer runs the checks off disk instead of
  remembering them. Fixed and resolved in this same round; the NEXT session's
  gate verifies the rule is on disk and reads as intended.
- R-0251 (Low, F105 R22): the fallback branch of
  `_drop_one_newline_per_segment_boundary` in
  `packages/orchestration/pingpong_loop.py` ships unproven. The helper has three
  branches; composition reaches two of them. The third — drop the NEXT segment's
  leading newline when the earlier one has no trailing newline to give — is
  unreachable for today's ten segments, because every non-last segment's raw
  text already ends with a newline. Proven by the reviewer at b35d9d56 in a
  disposable worktree: replacing that branch's body with a `raise` leaves 433
  tests green across the golden, the three pingpong suites, `test_scope_plan.py`
  and `test_task_input.py`. The worker declared exactly this as R22 deviation 1
  rather than reporting the ordered mutation as red, which is the behaviour the
  gate exists to reward. Fix: pin the helper directly with synthetic lists — not
  delete the branch, which handles a legal case a future segment may produce.
  Done: R-0251 — RESOLVED at R23. The helper now carries its own test class,
  called directly with lists the composed prompts cannot produce: the trailing
  branch, the fallback branch, the illegal boundary's `PromptSegmentError`, a
  mixed three-segment list, and the untouched last element. Re-proved by the
  reviewer's own red-proof at gate F, where deleting the `elif` turns the
  fallback and mixed-boundary tests RED where before the pin it turned nothing.
- R-0252 (Medium, F105 R22, reviewer-authored defect): DECISION F105 D8's
  pre-emission checklist does not cover the red-proofs a block ORDERS. R22's
  gate F ordered a mutation — delete the fallback branch, expect red — against
  a branch no test can reach, so the gate was unsatisfiable exactly as R-0250's
  four were. That is the SIXTH instance of the class across F104 and F105, and
  the first the freshly installed checklist did not catch: its four items read
  the block's own bytes, and reachability is a property of the CODE the block
  points at. The cost is the same as every earlier instance — a round spends a
  declared deviation proving a reviewer mistake. Fix: a fifth checklist item in
  docs/agents/planner_reviewer_prompt.md §3, installed as DECISION F105 D10 in
  the same round as this entry. Fixed and resolved in this same round; the NEXT
  session's gate verifies the rule is on disk and reads as intended.
- R-0253 (Low, F105 R24, reviewer-authored defect): §4.9's append-shaped pair
  obligation is written whole-file where it can only hold over the DIFF. The
  rule says "FROM exactly 1x plus each TO-ONLY addition exactly 1x". R24's
  PAIR_A had 34 TO-only lines, of which 33 occur once in the file and one —
  "`git worktree list` the primary alone at this verdict." — occurs twice,
  because the identical sentence already stood in the R22 gate paragraph. The
  gate was therefore unsatisfiable by construction, and the worker correctly
  MEASURED it and declared it rather than editing the text to dodge it. The
  reviewer re-measured and confirms: `git show --numstat` on the C2 commit
  reads exactly `34 0 .agent/live_review.md`, so the diff-scoped reading is
  both exact and achievable. This is the seventh unsatisfiable-gate instance
  across F104 and F105 and the second one DECISION F105 D8's checklist did not
  catch, because like item 5 it is not a property of the block's own bytes —
  it is a property of the TARGET FILE's existing content. Fix: amend §4.9 so
  the TO-only count is over lines ADDED BY THE DIFF, and add the whole-file
  collision to D8 as the check that catches it before emission. Note for
  whoever fixes it: prose that repeats an earlier gate's sentence is normal and
  desirable in this file, so the rule must bend, not the text. OPEN.
  Done: R-0253 (2026-08-10) — RESOLVED. §4.9 now scopes the TO-only count to the
  lines that commit's diff ADDS, names `git show --numstat` as the measurement,
  and D8 carries a sixth item for the whole-file collision. The reviewer
  re-measured the new rule against its own first use: the C2 commit adds 47
  lines, all 47 are PAIR_A TO-only lines at exactly 1x, strays 0 — achievable
  where the whole-file reading was not.
- R-0254 (Low, F105 R24): `_drop_one_newline_per_segment_boundary` in
  `packages/orchestration/pingpong_loop.py` raises `PromptSegmentError` with
  the text "builder prompt segment boundary carries no newline to drop between
  segments N and N+1", but since R24 the helper composes the REVIEWER prompt
  too. A reviewer-side boundary fault would report itself as a builder fault
  and send the next reader to the wrong function. The worker spotted this and
  correctly did NOT act: it is outside R24's declared change set and AGENTS.md
  Scope Control bars the "while I'm here" edit. Cost today is zero — the
  message is unreachable in production, which is exactly what R-0251 pinned —
  so this is a message-quality finding, not a correctness one. Fix: drop the
  word "builder", and update the two message assertions in
  `tests/orchestration/test_builder_prompt_golden.py::TestDropOneNewlinePerSegmentBoundary`
  in the same commit. Production code, so it needs a SPLIT round. OPEN.
  Done: R-0254 (2026-08-10) — RESOLVED. The message now reads "prompt segment
  boundary carries no newline to drop between segments N and N+1", so a
  reviewer-side boundary fault no longer reports itself as a builder fault, and
  the one assertion that pins it anchors with `^` and `$`. Re-proved by the
  reviewer in a disposable worktree at d0ebba63: putting "builder " back turns
  exactly that test RED, where before R26 the same mutation stayed green.
- R-0255 (Low, F105 R26): DECISION F105 D8's checklist now holds six items, but
  its preamble still reads "Run all four checks" and its closing note still
  reads "item 2 has recurred five times ... R20 hit all four items". Item 5
  landed at R24 and item 6 at R26; neither round updated the two counts. A
  reviewer following the preamble literally runs four of six checks — and the
  two the preamble drops are exactly the two most recently learned. The R26
  worker spotted this and correctly did NOT act: no pair was given for it and
  AGENTS.md Scope Control bars the "while I'm here" edit. Fix: the preamble
  says six, and the closing note says six recurrences and "four of them in one
  block". OPEN.
  Done: R-0255 (2026-08-10) — RESOLVED. The preamble reads "Run all six checks"
  and the closing note reads "recurred six times ... R20 hit four of them in one
  block", so the count a reviewer follows now matches the list they must run.
  Verified by the reviewer against the applied file, not the diff alone.
- R-0256 (Low, F105 R27): the segment manifest a flight-plan trace carries is
  composed a SECOND time at the call site. `apps/cli/commands/do_cmd.py` calls
  `compose_flight_plan_prompt(plan_intake_dict)` for the manifest while
  `plan_job_llm` composes the bytes it actually sends, and both reach
  `repo_facts_block()` independently. The trace's `prompt_text` is the effective
  prompt but its `segment_manifest` describes the reviewer-composed twin, so an
  audit row can describe bytes that were never sent if the two compositions
  differ. `make_intake_call_recorder` has the same shape, so the finding covers
  both sites. Cost today is bounded and visible: `prompt_chars` and
  `segment_manifest_chars` are both recorded, so a divergence shows up as a
  mismatch rather than a silent lie. Fix: compose ONCE — have the builder return
  or accept its `ComposedPrompt` so exactly one composition feeds both the
  provider and the trace. Needs a signature change on `plan_job_llm` and
  `run_intake`, so it is its own round. OPEN.

- R-0258 (Medium, F105 R33, reviewer-authored defect): the R33 block ordered
  `provider="ollama", provider_kind="ollama"` onto the `run_mission` call in
  `apps/cli/commands/mission_cmd.py` while
  `tests/orchestration/test_mission_compiler.py:1210` already asserted
  `source.count('provider_kind="ollama"') == 1` over the WHOLE of that file. The
  second label is CORRECT and makes the count 2, so the ordered change and the
  existing suite could not both hold. The R33 worker applied the edit, measured
  `assert 2 == 1`, reverted it and declared the deviation rather than landing a
  red test or editing a file outside its change set — which was right on both
  counts. Reproduced by the reviewer in a disposable worktree at af35adbc: the
  edit applied verbatim yields exactly that failure and
  `grep -c 'provider_kind="ollama"'` prints 2. Cost: C4 item 3 and C5 test 4 of
  R33 unlanded, and both `run_mission` callers still writing unlabelled rows.
  This is the SEVENTH instance of the unsatisfiable-gate class across F104 and
  F105 and the first whose counting gate lives in a test file the block never
  names: DECISION F105 D8's items 1-4 read the block, item 5 the code it points
  at, item 6 the file it writes into, and none of them reads the TESTS that
  already guard that file. Fix: a seventh checklist item, and repair the guard
  into a per-call-site assertion so a second labelled call site is allowed.
  OPEN.
  Done: R-0258 (2026-08-10) — RESOLVED at F105 R34, commits 3c651516 and
  083a42d3. §3 of docs/agents/planner_reviewer_prompt.md now carries a SEVENTH
  pre-emission item: grep the suite for tests that COUNT a string over a whole
  file before ordering a change that adds that string. The guard that caused
  this is repaired in the same feature — `test_the_cli_names_the_provider_it_
  planned_with` asserts the label inside a window anchored at its own call site
  instead of `source.count(...) == 1` over all of `mission_cmd.py`. Verified by
  the reviewer against the real diff and by measurement, not from the handback:
  the file-wide count of `provider_kind="ollama"` is now 2 and the suite is
  green, which is precisely the state the old guard made impossible. The two
  call sites are 7335 characters apart, so neither window can see the other's
  label, and both R34 mutations went red as ordered — M1 taking only the run
  guard down while the plan guard stayed green, which is the property "scoped to
  its own call site" means. The remaining imprecision is registered separately
  as R-0260 and does not reopen this one.
- R-0259 (Medium, F105 R31, reviewer-authored defect): the R-0257 finding block
  sits at lines 1528-1554 of `.agent/live_review.md`, under `## Steps` instead
  of under `## Findings` — the R-0231 class in the mirror direction, and the
  second instance of it on this branch. It is worse than misplacement: the block
  was inserted INSIDE the R30 gate record, so that record's concluding
  ``LAST_REVIEWED_SHA` advances 0c8932e3 -> 0ba30611.` line is orphaned at 1555,
  27 lines below the record it belongs to and directly beneath R-0257's
  resolution text. A reader parsing the round history attributes R30's advance
  to R-0257's `Done:` paragraph. R-0231's own resolution claimed "`## Findings`
  holds only findings again", and that invariant is broken again in the other
  direction. Fix: MOVE lines 1528-1554 to the end of `## Findings`, bytes
  unchanged, so the R30 record closes with its own advance line — proved as a
  MOVE and not a retype, the block occurring exactly 1x before and 1x after.
  Registered here, fixed in its own round: doing it inside this commit would
  bury this round's real diff under a 27-line relocation. OPEN.
  Landed: R-0259 — the R-0257 block moved to the end of Findings, C2 of R36.
- R-0260 (Low, F105 R34, reviewer-authored defect): the two per-call-site guard
  comments claim more precision than the code has. The authored comment says
  "The window is the call expression itself", and the run-site test repeats the
  shape, but a 200-character window from `outcome = plan_mission(` overshoots
  that call by 71 characters — measured, not estimated — spilling into
  `except MissionPlanInProgressError as exc:` and the first characters of the
  next `print(`; the run site overshoots its 173-character call by 27. The
  guarded PROPERTY holds and was proved to hold: the call sites are 7335
  characters apart, so no window reaches the other's label, and both mutations
  went red. So this is an inaccurate claim on disk, not a broken test — but it
  is a comment written to teach the next reader what the guard pins, landed by
  the very round whose subject was guards that promise more than they check.
  The R34 worker measured the overshoot and declared it rather than silently
  tightening the constant, which was right: the wording is the reviewer's.
  Fix: bound each window at its call's closing parenthesis instead of a magic
  200, or correct both comments to say "200 characters from the call's start,
  which covers the call and a little after". OPEN.
  Landed: R-0260 — both guard comments now describe the real window, C4 of R36.
- R-0257 (Medium, F105 R30, reviewer-authored defect): the R30 block lifted
  composition OUT of the try/except that turns any failure into the
  deterministic fallback. `compile_mission_plan` used to build its prompt as an
  ARGUMENT to `run_structured_call` inside `try:`, so a raising composer became
  `_fallback(goal, hint=f"provider error: {exc}")`; PAIR_F put
  `composed = compose_mission_prompt(...)` above the `try:`, so it now escapes
  the function. Proved by the reviewer in a disposable worktree with the
  composer monkeypatched to raise: at 39da9b61^ the call returns
  `source="deterministic"` and `error_hint="provider error: composition blew
  up"`; at 39da9b61 the `RuntimeError` propagates out. No test covers it, which
  is exactly why every gate was green — the module docstring's promise that
  "any provider failure, or an unparseable answer" yields the fallback "rather
  than an exception" is what regressed, and `remedy mission plan` would
  traceback where it used to degrade. The realistic trigger is a filesystem
  failure inside `repo_facts_block()`. The R30 worker DECLARED this rather than
  repairing it, which was right: the defect is the reviewer's, and a worker that
  silently fixes authored text hides the mistake instead of pricing it. Fix:
  compose inside the try, pinned by a test that makes the composer raise. OPEN.
  Landed: R-0257 — composition moved back inside the try at C3 of R31.
  Done: R-0257 (2026-08-10) — RESOLVED at F105 R31, commit 3d37567f.
  `compose_mission_prompt` and the recorder wiring both sit inside the `try`
  again, so a composition failure returns to being `_fallback(goal,
  hint=f"provider error: {exc}")`. Re-proved by the reviewer at 9bd3a3e7 with
  the composer monkeypatched to raise: `source="deterministic"`,
  `error_hint="provider error: composition blew up"` — the pre-R30 behaviour
  exactly. `test_a_failing_composer_still_yields_the_fallback` now pins it, so
  the regression cannot return silently the way it arrived.

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
- Reviewer gate on R16 (2026-08-09): PASS, and it is the first PASS on this
  branch over a round that carried production code. Range `ed5b2421..HEAD` at
  efd66b68, SEVEN commits, EIGHT paths, exactly the block's declared change set
  with nothing beside it. Per-commit insertions from `git log --numstat`: 399,
  366, 24, 35, 55, 255 (73 + 182) and 88 (63 + 25) — each under 500, so D5's
  exemption for C1b was not even load bearing this round. Transport: the
  reviewer's surviving original `.remedy-wt/f105-r16-1.block.md`,
  `.agent/authored/f105-r16-1.md` and `.agent/last_block.md` all hash to
  744fe981, both `cmp` runs exit 0, 399 lines against D5's cap of 400.
  Application proved disk to disk: of the 59 lines added to
  `.agent/live_review.md` and the 55 added to `.agent/decisions.md`, all 114
  occur verbatim in the authored file and 0 are missing; the single removed line
  is exactly pair B's FROM; no `===BEGIN` or `===END` marker reached any target
  file. `.agent/plan.md` equals its authored slice, sha256 8029c8ca both sides.
  The golden's frozen `_PRE_MIGRATION_MISSION_TEMPLATE` was diffed by the
  reviewer against `git show ed5b2421:packages/orchestration/mission_compiler.py`
  lines 78-108 and is byte-identical — 31 lines, exit 0 — so the golden pins the
  real pre-migration prompt and not a retyping of it. `grep` for
  `_MISSION_PROMPT_TEMPLATE` across `packages/ apps/ tests/` returns only the
  golden's own docstring, so the migration left no straggler, and
  `build_mission_prompt`'s one production caller at `mission_compiler.py:338` is
  untouched. Gates re-run by the reviewer with real exit codes: the golden 5
  passed; `test_mission_compiler.py` + `test_prompt_segments.py` 135 passed,
  the same 135 the reviewer measured at ed5b2421 BEFORE the round; state
  contracts 4 passed / 47 deselected; `tests/docs/` 294 passed; canary 42
  passed; integrity `passed=True`, `fail_count=0` over 5 checks;
  `git status --porcelain` empty; `git worktree list` the primary alone; HEAD
  equal to origin. The reviewer re-ran mutation M3 independently in a disposable
  worktree at efd66b68 and reproduced the worker's result exactly — dropping the
  schema directive's trailing newline turns the same THREE named tests RED — and
  added a fourth axis the round did not claim: deleting the `mission_repo_facts`
  registration turns SIX tests RED, including one pre-existing
  `test_mission_compiler.py` test, so the golden is load bearing on segment loss
  as well as on order, wording and that one byte. The worktree was removed and
  pruned before this verdict. All five declared deviations ACCEPTED. Deviations
  3 and 4 are better than what was asked for: literal whole-string equality is
  impossible once composition reorders, and the reordered-join assertion is the
  strongest true reading; and reporting the no-op statement swap as control M0
  instead of dressing it up as a red proof is the honesty this loop runs on.
  Two defects found, R-0245 and R-0246, one the worker's record and one the
  reviewer's own text. R-0243 and R-0244 RESOLVE here.
  `LAST_REVIEWED_SHA` advances ed5b2421 -> efd66b68.
- R17: the session-terminator round — R-0243 and R-0244 resolved, R-0245 and
  R-0246 registered, the R16 gate recorded, the session-end handoff written. The
  session ends at its DECLARED TWO-ROUND CAP (R16 building, R17 recording) under
  docs/agents/self_drive_protocol.md G7. R17 ends a SESSION, not the branch, so
  its own gate is OWED and the next session's reviewer records it first
  (§4.13 as corrected by R-0233). No production code changed this round.
- Reviewer gate on R17 (2026-08-09, opening a NEW session under
  docs/agents/self_drive_protocol.md): PASS. The owed gate is paid first, before
  any new work was planned. Range `efd66b68..HEAD` at 70156f31: FIVE commits,
  FIVE paths, all under `.agent/`, the block's declared change set exactly, no
  production code. Insertions from `git log --numstat`: 257, 160, 38, 48, 65
  (51 + 14), each under 500; C1b's 160 needed no D5 exemption. Transport:
  `.remedy-wt/f105-r17-1.block.md`, `.agent/authored/f105-r17-1.md` and
  `.agent/last_block.md` all hash to 8db0b6d7, both `cmp` exit 0, 257 lines
  under D5's 400. Application proved disk to disk by the reviewer's own script:
  each of the four TO slices occurs in `.agent/live_review.md` exactly ONCE;
  A, B, D are appends whose FROM survives 1x, C is the header rewrite whose FROM
  is gone; no marker LINE reached a target — the one `===BEGIN` present is a
  finding quoting the token in prose. `.agent/plan.md` at 70156f31 equals its
  slice byte for byte, sha256 49527b18, 48 lines; R-0244's claim re-checked, the
  file at efd66b68 is 47 lines and hashes to 8029c8ca as stated. Gates re-run,
  real exit codes: state contracts 4 passed / 47 deselected; `tests/docs/` 294
  passed; canary 42 passed; integrity `passed=True`, `fail_count=0` over 5
  checks; `git worktree list` primary alone; HEAD equal to origin. All five
  declared deviations ACCEPTED; no mutation red-proof owed, nothing executable
  changed. R-0245 RESOLVES here; one defect found, R-0247, the reviewer's own.
  `git status --porcelain` was NOT empty: a first R18 attempt halted on an
  operator `.agent/STOP`, applied nothing, and died before its halt commit
  landed, leaving `.agent/handoff.md` and `.agent/plan.md` uncommitted; 70156f31
  and the R17 range are untouched by it. Disposition for a dirty Phase 0 tree:
  COPY the pair to `.remedy-wt/`, then restore to HEAD, never commit it — its
  plan.md reads BLOCKED, which the Commit Gate's item 1 would make false the
  moment the round resumed. `LAST_REVIEWED_SHA` advances efd66b68 -> 70156f31.
- Reviewer gate on R18 (2026-08-09, same session, paid in-session and NOT
  deferred because R18 is the first round on this branch to land production
  code): PASS. Range `70156f31..HEAD` at c65d663e, SEVEN commits, EIGHT paths,
  exactly the block's declared change set. Insertions from `git log --numstat`:
  400, 296, 18, 27, 38, 246 and 91, each under 500; C1b's 296 is the verbatim
  rewrite of one state file. Transport: `.remedy-wt/f105-r18-2.block.md`,
  `.agent/authored/f105-r18-2.md` and `.agent/last_block.md` all hash to
  a89262c0, both `cmp` exit 0, 400 lines — exactly D5's cap, measured before
  delegation. Application proved disk to disk by the reviewer's own script: all
  SIX pairs land in their declared shape, A, B, D, E, F appending with FROM
  surviving 1x and TO fresh 1x, C rewriting the header with its FROM gone; zero
  marker LINES in `.agent/live_review.md`, `.agent/decisions.md` or
  `.agent/plan.md`; `.agent/plan.md` equals its slice byte for byte, 46 lines,
  sha256 2b80abaf. Nothing else entered the state files: of 51, 32 and 13 added
  lines across the three, every one traces to an authored TO slice and the stray
  count is 0.
  The production claim was checked without using the worker's test as evidence.
  `_PRE_MIGRATION_PLAN_TEMPLATE` is byte-identical to `_PLAN_PROMPT_TEMPLATE` as
  it stood at 70156f31 — same sha256 ca5f325d after normalising only the
  constant's NAME, and the two exec to equal values — so the golden is pinned to
  the real prior text and not to a retyped copy of it. Reconstructing the OLD
  builder from 70156f31 and rendering both: on two different intakes, the new
  composition reordered back into template order equals the old render exactly,
  the lengths match, and the sorted part SETS are equal. Content equality modulo
  ordering therefore holds against the pre-migration code itself, not merely
  against a constant in a test file. The cacheable-prefix payoff was measured,
  not asserted: two calls differing only in intake now share a 1437-character
  prefix of a 1505-character prompt, and only `plan_intake` changes hash.
  Gates re-run by the reviewer, real exit codes: golden 5 passed; bundled
  clarification + prompt segments 60 passed, identical to the pre-round baseline
  of 60 so the migration added no test to that pair and removed none; state
  contracts 4 passed / 47 deselected; `tests/docs/` 294 passed; canary 42
  passed; integrity `passed=True`, `fail_count=0` over 5 checks. Beyond the
  block's gates the reviewer ran the FULL `tests/orchestration/` suite — 10452
  passed, 7 skipped, exit 0 in 661s — plus every test file that names
  `flight_plan`, 309 and 487 passed, so the new keyword-only seam broke no
  caller. Mutation red-proofs were re-run by the reviewer in a fresh disposable
  worktree, not taken from the handback: M1 rank swap, M2 dropped trailing
  newline, M3 deleted `plan_repo_facts` — each RED, each with the block's
  expected named test among the failures, and the suite green again after every
  revert. Worktree removed and pruned; `git status --porcelain` empty,
  `git worktree list` the primary alone, HEAD equal to origin.
  All six declared deviations ACCEPTED. Deviation 4's `passed:false` on
  `relevant_untracked` before the C5 commit is the check working as designed on
  a not-yet-committed new file, not a failure. Deviation 3's added docstring
  exceeds what the block mandated but documents the seam the block introduced
  and touches no caller; kept. The 115-line handoff is inside DECISION D15: it
  declares its own count, names the cap and names the mandated content, and
  `wc -l` returns the number it declares. One defect found, R-0248, in DECISION
  D6's account of its own mechanism. `LAST_REVIEWED_SHA` advances
  70156f31 -> c65d663e.
- Reviewer gate on R19 (2026-08-09, the next session's reviewer, paying the
  gate R19 was owed as the session terminator): PASS. Range `c65d663e..HEAD`
  at 04a3396d, FIVE commits, FIVE paths, every one `.agent/` state — exactly
  the block's declared change set, no production file and no test file, so no
  mutation red-proof was owed and none is claimed. Insertions from
  `git log --numstat`: 230, 137, 17, 51 and 53, each under 500; C1b's 137/-307
  and C4's handoff rewrite are each the verbatim rewrite of one state file.
  Transport was re-proved disk to disk by the reviewer rather than read out of
  the handback: `.agent/authored/f105-r19-1.md` and `.agent/last_block.md` both
  hash to 7f8cd1eb1a388d07c74381658934d473c1afdd4447e546784e3b88bc4a3638c3,
  `cmp` exits 0, and both are 230 lines, so the handback's `7f8cd1eb…` is the
  real digest and D5's 400-line cap holds with room. Application checked per
  target: `grep -c '^- R-0248 '` is 1 and `grep -c '^- Reviewer gate on R18 '`
  is 1, so neither the finding nor the owed gate was applied twice; line 8 read
  `Next free ID: R-0249.`; marker LINES `^===BEGIN|^===END` count 0 in both
  `.agent/live_review.md` and `.agent/plan.md`.
  Gates re-run by the reviewer with real exit codes, none accepted as a word:
  canary `tests/cli/test_golden_path.py` 42 passed in 19.35s; `tests/docs/`
  294 passed; `tests/ui_server/test_dashboard_contract.py` 70 passed;
  `tests/orchestration/test_integrity_gate.py` 15 passed; the `.agent` state
  contracts 2 passed / 16360 deselected under the reviewer's own `-k` selector.
  `git status --porcelain` was empty and `git worktree list` showed the primary
  alone, so G5 holds and no destructive check leaked into the checkout.
  Honest gap, stated rather than papered over: the handback's fourth D-gate
  item, `remedy integrity check --json`, could NOT be executed — this session's
  shell layer refused the invocation — so the reviewer ran the integrity gate's
  own test file instead and does NOT restate the handback's `passed=True,
  fail_count=0` over 5 checks. That number stays the worker's claim, unverified
  here. It gates nothing this round, because R19 shipped no code for the
  integrity checker to have an opinion about; a round that ships code does not
  get the same pass.
  The declared counts check out against the commands that produced them:
  `wc -l` returns 46 for `.agent/plan.md`, under the <50 rule, and 85 for
  `.agent/handoff.md`, exactly the number the D15 overage line declares — the
  overage is stated truthfully rather than rounded, which is the whole test of
  a stated-cause deviation. All four declared deviations ACCEPTED; deviation
  2's benign 2x sentence collision was re-counted and the PAIR_C block itself
  occurs exactly 1x, which is the claim that matters. Deviation 3 is the R-0248
  gap, already registered and fixed this round. One finding is registered
  against the handback's planning record rather than against R19's work,
  R-0249. `LAST_REVIEWED_SHA` advances c65d663e -> 04a3396d.
- Reviewer gate on R20 (2026-08-09, same session): PASS. Range
  `04a3396d..HEAD` at 9cb128d7, SIX commits, EIGHT paths, exactly the block's
  declared change set. Insertions from `git log --numstat`: 471, 422, 58, 89,
  232, 59 and 98, each under 500.
  The production claim was checked WITHOUT using the worker's golden as
  evidence. The reviewer reconstructed the pre-migration builders directly from
  `git show 04a3396d:packages/orchestration/orchestrator_loop.py`, confirmed the
  frozen f-string anchor is present in that source, rendered both the system
  prompt and the full prompt against two different contexts, and compared byte
  for byte: equal in every case, lengths 3861 and 3865. This site is therefore
  the first of the six whose migration is byte-EXACT rather than equal modulo
  ordering, which is what its pre-existing rank order made possible. The
  manifest reads `[('orchestrator_system', 0), ('orchestrator_protocol', 1),
  ('orchestrator_mission_state', 3)]`, ranks non-decreasing; across two
  contexts the two stable hashes are equal and only the mission-state hash
  differs; the shared prefix measures 3852 of 3861 characters, 99.77%, and runs
  past the end of the protocol segment; and the two-entry system manifest is
  the exact prefix of the three-entry one. The cache payoff is measured, not
  asserted.
  Gates re-run by the reviewer with real exit codes: the golden, the loop suite
  and the segment suite together 220 passed — 6 + 192 + 22, and 192 is
  unchanged from the pre-round baseline, so the migration added no test to the
  loop file and removed none; canary plus `tests/docs/` together 336 passed —
  42 + 294. A mutation red-proof of the REVIEWER's own choosing, distinct from
  the worker's three, ran in a disposable worktree at HEAD: M4 changed
  `orchestrator_mission_state`'s rank from JOB_CONTEXT to CONVENTIONS, which
  leaves the composed TEXT byte-identical because equal ranks tie-break on
  registration order. A text-only golden would have passed it.
  `test_manifest_carries_the_three_declared_segments_in_rank_order` went RED
  with `At index 2 diff: 1 != 3`, the suite returned to 6 passed on revert, and
  the worktree was removed and pruned — so the golden pins the declared rank
  and not merely the bytes. `git status --porcelain` empty and
  `git worktree list` the primary alone at the verdict.
  All seven declared deviations ACCEPTED. Deviation 7's `_register_orchestrator_prefix`
  helper exceeds what the block asked for and is kept as an improvement on it:
  it makes the manifest-prefix property hold by construction rather than by two
  registration lists agreeing, and the block's actual constraint — that
  `compose_orchestrator_prompt` build its own registry and list all three
  entries — holds. Deviation 5's adaptation of golden test 5 is correct and the
  block was wrong: a shared prefix cannot end exactly at the protocol segment,
  because the next segment opens with a constant header. Deviations 1-4 are the
  reviewer's own authoring defects, not the worker's, and are registered
  together as R-0250 rather than charged to this round. The handback declared
  every one of them, including two gates it could not satisfy, instead of
  reporting green — which is the behaviour the gate exists to reward.
  `LAST_REVIEWED_SHA` advances 04a3396d -> 9cb128d7.
- Reviewer gate on R21 (2026-08-09, next session): PASS. Range
  `9cb128d7..HEAD` at 54049e6b, SIX commits, SEVEN paths, exactly the block's
  declared change set plus the declared correction commit. Insertions per
  `git log --numstat`: 328, 242, 80, 62, 60, 9 — each under 500.
  All seven gates were re-run by the reviewer, not read from the handback.
  A: both files sha256 `a97328127a09dfaf…`, `cmp` silent. B: 328 lines, under
  the 400 cap. C: the four greps returned 1/1/1/1, line 8 ends
  `Next free ID: R-0251.`, the two doc greps returned 1/1, and the BEGIN/END
  marker count is 0 in all four target files. D: `tests/docs/` 294 passed,
  `test_dashboard_contract.py` 70 passed. E: canary 42 passed. F: no red-proof
  owed and none faked — the change set contains no executable file. G:
  `git status --porcelain` empty, `git worktree list` the primary alone.
  The pair shapes were re-measured rather than accepted: A and B REWRITE with
  FROM 0x and TO 1x, C, D and E APPEND with FROM 1x and TO 1x — five for five
  against the declared table. Stray added lines were recomputed from the
  authored TO slices against the real diffs of both content commits: 80 added
  and 0 stray at C2, 62 added and 0 stray at C3. PAIR_F's slice and
  `.agent/plan.md` are byte-identical at sha256 `d263bfd059ab0798…`.
  All three declared deviations ACCEPTED. Deviation 1 — `.agent/plan.md` at 50
  lines against AGENTS.md's <50 — is confirmed as the reviewer's defect and not
  the worker's: the PAIR_F slice is itself 50 lines, so an applier required to
  match it byte for byte could not have complied with both. It is the second
  live instance of the R-0250 class, and it is repaired by this round's plan
  rewrite rather than registered again. Deviation 3's fifth commit is the right
  call: the alternative to correcting a false `+50/-57` row was a force-push,
  which G2 forbids outright.
  R-0250's own resolution asked the next gate to verify the rule reached disk
  and reads as intended. It did: docs/agents/planner_reviewer_prompt.md §3 now
  carries the four-item pre-emission checklist, and this round's block was
  written against it — item 1 caught the size before emission and item 2 was run
  against every zero-gate in Done-when C.
  `LAST_REVIEWED_SHA` advances 9cb128d7 -> 54049e6b.
- Reviewer gate on R22 (2026-08-10, same session): PASS. Range
  `54049e6b..HEAD` at b35d9d56, SIX commits, NINE path rows over eight paths,
  exactly the block's declared change set. Insertions per `git log --numstat`:
  376, 306, 32, 102, 392, 71 — each under 500.
  Transport was proved disk to disk, not by retype: the reviewer's authored
  original and the committed `.agent/authored/f105-r22-1.md` are byte-identical
  under `cmp`, and all three of original, authored copy and `.agent/last_block.md`
  hash to `8f5fc0c8bf8bdb67…`.
  The production claim was checked WITHOUT using the worker's numbers. Before
  the block was authored the reviewer had already proved the decomposition
  reproduces the pre-migration render BYTE FOR BYTE in pre-migration order over
  all 64 combinations of the six optional arguments, so the round was ordered
  against a spec known to be satisfiable — the R-0250 discipline applied
  forward for the first time. After the round the golden was re-read and re-run:
  16 tests, four fixture shapes, and the four frozen renders are `repr()` of the
  real 54049e6b output rather than retyped prompt text. `compose_prompt_segments`
  sorts by `(rank, registration index)`, and the worker registers in rank order,
  so the manifest's ten names and the ranks `(0,2,3,3,3,3,4,4,5,5)` are pinned
  exactly, not merely as a monotonic sequence.
  Gates re-run by the reviewer with real exit codes: golden plus segments
  41 passed — 16 + 25, where 25 is the pre-round 22 plus D9's three pins; the
  five caller suites 417 passed, unchanged from the pre-round baseline, so the
  migration added no test to them and removed none; canary 42 passed.
  TWO mutation red-proofs of the REVIEWER's own choosing, distinct from the
  worker's, ran in a disposable worktree at HEAD. M3 dropped the bare `"\n"`
  from `builder_context`'s parts: all 16 golden tests went RED, so the golden
  really does pin bytes and not only shape. M4b changed `builder_staged_diff`'s
  rank from JOB_CONTEXT to DOSSIER, which leaves every segment's TEXT identical
  and the ranks still non-decreasing: exactly one test failed,
  `test_the_full_shape_registers_the_ten_segments_in_rank_order`, so the golden
  pins the rank ASSIGNMENT and not just its monotonicity. Both reverted, the
  worktree removed and pruned, `git status --porcelain` empty and
  `git worktree list` the primary alone at this verdict.
  Application was re-measured rather than accepted: pairs A and B APPEND with
  FROM 1x and TO 1x, PAIR_C's slice and `.agent/plan.md` byte-identical at
  sha256 `45b21911…`, `.agent/plan.md` 45 lines against the cap of 50, zero
  BEGIN/END markers in all three targets, and stray added lines recomputed from
  the authored TO slices against the real diffs: 32 added and 0 stray at C2, 42
  added and 0 stray at C3.
  Both declared deviations ACCEPTED, and deviation 1 is charged to the
  reviewer, not the worker: gate F's M2 ordered a mutation against an
  unreachable branch. It is registered as R-0251 and R-0252 rather than held
  against R22. Deviation 2 is the round working as intended — gate H asked for a
  measured number, the number contradicted the block's guess, and the worker
  reported the measurement instead of the guess.
  `LAST_REVIEWED_SHA` advances 54049e6b -> b35d9d56.
- Reviewer gate on R23 (2026-08-10, next session): PASS. Range
  `b35d9d56..HEAD` at 554d9521, FIVE commits, eight path rows. Insertions per
  `git log --numstat`: 368, 292, 78, 45, 36 — each under 500, and the 368-line
  authored save is under DECISION F105 D5's 400.
  Transport proved disk to disk under the §4.9 DIGEST FALLBACK, stated as
  required: the previous session's scratchpad originals no longer exist, so the
  proof is `sha256sum` over the two COMMITTED files plus `cmp`.
  `.agent/authored/f105-r23-1.md` and `.agent/last_block.md` are byte-identical
  at `fd3271aedac2f81f…`, 368 lines each.
  Gates re-run by THIS reviewer, not accepted from the handback: the golden
  21 passed, `tests/docs/` 294 passed, the canary 42 passed,
  `test_dashboard_contract.py` 70 passed — every number equal to the worker's.
  `.agent/plan.md` measured 47 lines against the cap of 50. Zero BEGIN/END
  transport markers in all four target files; the six `PAIR_` hits in
  `.agent/live_review.md` were read and are prose inside finding text, not
  stray marker lines.
  TWO mutation red-proofs of the REVIEWER's own choosing ran in a disposable
  worktree at HEAD and BOTH went red, so R-0251's pin is real and not merely
  present. M1 deleted the `elif` fallback branch of
  `_drop_one_newline_per_segment_boundary`: exactly two tests failed,
  `test_the_leading_newline_of_the_later_segment_is_the_fallback` and
  `test_each_boundary_chooses_its_own_branch`, reproducing the worker's gate F
  to the test name. M2 replaced the `else: raise` with `pass`: exactly one test
  failed, `test_a_boundary_with_no_newline_at_all_is_illegal`. Both reverted,
  the worktree removed and pruned, `git status --porcelain` empty and
  `git worktree list` the primary alone at this verdict.
  R-0251 and R-0252 are confirmed RESOLVED against the disk, not the summary:
  the test class exists with five tests and the red-proof above, and checklist
  item 5 plus DECISION F105 D10 are on disk and read as intended.
  Declared deviation 1 ACCEPTED and it is the round working as intended: the
  worker MEASURED PAIR_D's shape, found the block's word "prefix" wrong where
  the FROM is the TO's SUFFIX, and reported the measurement instead of the
  claim. Containment holds either way, so application was unaffected.
  `LAST_REVIEWED_SHA` advances b35d9d56 -> 554d9521.
- Reviewer gate on R24 (2026-08-10, same session): PASS. Migration-order step 6
  is landed, so ALL SIX T003 migration sites are done. Range
  `554d9521..HEAD` at df32f595, SIX commits, seven path rows. Insertions per
  `git log --numstat`: 258, 226, 34, 279, 142, 70 — each under 500, and the
  258-line authored save is under DECISION F105 D5's 400.
  Transport: `.agent/authored/f105-r24-1.md` and `.agent/last_block.md` are
  byte-identical under `cmp` at sha256 `eb6e071e399cd967…`, 258 lines.
  THE SPEC WAS PROVED SATISFIABLE BEFORE THE BLOCK WAS AUTHORED, the R-0250
  discipline applied forward for the second time. In a disposable worktree at
  554d9521 the reviewer proved the decomposition byte-exact over 3584 argument
  combinations in two passes: 2048 for the decomposition itself (80 distinct
  segment sets, 0 mismatches) and 1536 for the property the golden actually
  rests on — that registering in RANK order instead of source order leaves
  every segment's BYTES unchanged. It does: 0 per-segment differences, 0
  changes of last-segment identity, 0 boundaries needing the fallback newline.
  Without that second pass the golden's "reassemble in pre-migration order"
  assertion would have been an assumption, since
  `_drop_one_newline_per_segment_boundary` runs over the registration order.
  AFTER the round the reviewer re-proved content equality against the REAL
  pre-migration bytes, not against the worker's numbers:
  `git show 554d9521:packages/orchestration/pingpong_loop.py` was imported as a
  second live module and run side by side with HEAD's composer over 2048
  combinations and 160 distinct segment sets. 0 reassembly failures, 0 wrapper
  mismatches, 0 unknown segment names, 0 non-monotonic manifests. 224 renders
  are byte-identical to the old one and 1824 are genuinely reordered, so the
  reorder this feature exists to make is real and measured, not asserted.
  Gates re-run by THIS reviewer: the new golden 16 passed, the four caller
  suites 234 passed — equal to the worker's pre-round baseline, so the
  migration added no test to them and removed none — and the canary 42 passed.
  TWO mutation red-proofs of the REVIEWER's own choosing, distinct from the
  worker's M1 and M2, ran in a disposable worktree at HEAD. M3 changed
  `reviewer_task_input`'s rank from TASK to STEERING, which leaves every
  segment's TEXT identical and the ranks still non-decreasing: exactly one test
  failed, `test_the_fallback_full_shape_registers_its_segments_in_rank_order`.
  M4 changed `reviewer_scope_contract`'s rank from JOB_CONTEXT to DOSSIER:
  exactly the two shape tests failed. So the golden pins the rank ASSIGNMENT
  and not merely its monotonicity — the property R22's M4b established for the
  builder, now established for the reviewer. Both reverted, the worktree
  removed and pruned, `git status --porcelain` empty and `git worktree list`
  the primary alone at this verdict.
  Application re-measured disk to disk against the COMMITTED authored file,
  never a retype: PAIR_A APPEND with FROM 1x and TO 1x, PAIR_B's slice and
  `.agent/plan.md` byte-equal, plan 39 lines against the cap of 50, and not one
  transport marker of any shape left behind in either target.
  BOTH declared deviations ACCEPTED, and BOTH are charged to the reviewer.
  Deviation 1: gate D asked for failing test NAMES from a red that a
  module-level import makes a COLLECTION error, which yields none; the worker
  re-measured at test-name granularity in a worktree and got all 16. Deviation
  2 is registered as R-0253. Neither is held against R24. A round that measures
  a reviewer's gate and reports the number instead of the claim is the round
  working exactly as designed, for the third feature running.
  `LAST_REVIEWED_SHA` advances 554d9521 -> df32f595.
- Reviewer gate on R25 (2026-08-10, next session): PASS. A state-file-only
  round, exactly as declared: `git diff --stat df32f595..HEAD` touches five
  paths, all under `.agent/`, and no production file, no test file and nothing
  under `docs/` appears. Range df32f595..0341928d, FOUR commits, five path
  rows. Insertions per `git log --numstat`: 214, 167, 84, 69 — each under 500,
  and the 214-line authored save is under DECISION F105 D5's 400. C1b is the
  verbatim rewrite of ONE state file and is exempt from the churn reading by
  the AGENTS.md counting rule regardless.
  Transport: `.agent/authored/f105-r25-1.md` and `.agent/last_block.md` are
  byte-identical under `cmp` (exit 0) at sha256
  `a89edbcf2a2e9b5af1bd5befc90b4044f23d4861f32b83ab9ba34543abba0e9c`, 214 lines
  each — the digest the handback declared, recomputed by the reviewer.
  Application re-measured disk to disk against the COMMITTED authored file,
  never a retype: the reviewer re-sliced all four pairs from
  `.agent/authored/f105-r25-1.md` with its own reader, which rejects a marker
  line inside any body. PAIR_A is a REWRITE and measures FROM 0x after, TO 1x.
  PAIR_B and PAIR_C are APPEND-shaped and the prefix property holds literally —
  each TO begins with its own FROM — at FROM 1x each. PAIR_D and the applied
  `.agent/plan.md` are byte-equal, 40 lines against the cap of 50. Marker
  leakage: `PAIR_A_FROM`, `PAIR_D_PLAN`, `END_PAIR` and `<<<` all count 0 in
  both targets.
  The R-0253 reading was MEASURED, not accepted on the worker's word. The C2
  commit adds exactly 84 lines and removes exactly 1. The 84 decompose as 1
  (PAIR_A TO) + 31 (PAIR_B TO-only) + 52 (PAIR_C TO-only) = 84 with nothing
  left over: each of those 84 lines occurs exactly once among the diff's ADDED
  lines, and no ADDED line comes from outside a TO slice. Strays 0, extras 0.
  The one removed line is PAIR_A's FROM. So the diff-scoped reading is exact
  and achievable, which is the finding's own claim, now independently checked.
  Gates re-run by THIS reviewer: `tests/docs/` 294 passed, the dashboard
  contract 70 passed, the canary 42 passed. NO mutation red-proof was ordered
  or run, and that is correct: nothing executable changed, so there was no
  branch to mutate (DECISION F105 D10, checklist item 5). `git status
  --porcelain` empty and `git worktree list` the primary alone at this verdict.
  Two corrections to the record, BOTH charged to the reviewer, NEITHER held
  against R25. First: R25 called itself the §4.13 TERMINATOR. §4.13 covers the
  last round of a BRANCH; R25 is the last round of a SESSION and the branch
  continues, so its gate was never owed to construction — it is recorded here.
  R25 was right to open no repair round for it under either reading. Second:
  R-0254's fix note says to update "the two message assertions" in
  `TestDropOneNewlinePerSegmentBoundary`. There is exactly ONE, at
  `tests/orchestration/test_builder_prompt_golden.py:280`, and it matches on
  `segment boundary carries no newline to drop between segments 0 and 1` — a
  substring that SURVIVES dropping the word "builder". The fix as written would
  therefore change production bytes that no test pins. R26 anchors that
  assertion to the whole message instead, which turns the wording into
  something a mutation can prove red.
  `LAST_REVIEWED_SHA` advances df32f595 -> 0341928d.
- R26: SPLIT repair round — record the R25 gate, fix R-0253 (§4.9 scoped to the
  diff's ADDED lines plus a sixth D8 checklist item) and R-0254 (the shared
  boundary helper's builder-only message plus the one assertion that pins it).
- Reviewer gate on R26 (2026-08-10): PASS. Range `0341928d..d0ebba63`, nine
  commits, read as a real diff. Every path the block named and no other:
  `.agent/authored/f105-r26-1.md`, `.agent/last_block.md`,
  `.agent/live_review.md`, `docs/agents/planner_reviewer_prompt.md`,
  `packages/orchestration/pingpong_loop.py`,
  `tests/orchestration/test_builder_prompt_golden.py`, `.agent/plan.md`,
  `.agent/handoff.md`. Insertions per commit 264, 196, 47, 17, 1, 3, 1, 80, 8 —
  each under 500, and the authored save is 264 lines against DECISION F105 D5's
  cap of 400.
  Transport verified under the §4.9 DIGEST FALLBACK: this reviewer session holds
  no scratchpad original, so sha256 was recomputed over the COMMITTED files.
  `.agent/authored/f105-r26-1.md` and `.agent/last_block.md` are both
  `c249919e7e8d111f9cac38d8593b9f0c67d409ae85530256a0367eac4b1b4a0d`, `cmp`
  silent, 264 lines each — the digest the handback declared.
  Application re-measured disk to disk against the COMMITTED authored file with
  the reviewer's own slicer, never a retype: PAIR_A append-shaped with the
  prefix property holding literally, FROM 1x; PAIR_B rewrite, FROM 0x after,
  TO 1x; PAIR_C append-shaped, FROM 1x; PAIR_D rewrite, FROM 0x, TO 1x; PAIR_E
  rewrite, FROM 0x, TO 1x; PAIR_F byte-equal to `.agent/plan.md` at 41 lines
  against the cap of 50. Declared shape equals measured shape for all six.
  R-0253's own new rule was applied for the first time and it holds. `git show
  --numstat 4c53c746` reads `47 0`, and all 47 ADDED lines are PAIR_A's TO-only
  lines at exactly 1x, strays 0. `git show --numstat c6ec5d3e` reads `17 2`;
  PAIR_B's first TO line is diff CONTEXT, so the 17 decompose as 9 (PAIR_B) + 8
  (PAIR_C TO-only), strays 0, extras 0.
  Gates re-run by THIS reviewer with real exit codes: the golden suite `21
  passed`, `tests/docs/` `294 passed`, the dashboard contract `70 passed`, the
  canary `42 passed`, and `tests/orchestration/` `10498 passed, 7 skipped in
  672.30s` — the module regression re-run in full, not accepted on the word.
  Mutation red-proof M1 run by the reviewer in a disposable worktree at
  d0ebba63: restoring the word "builder" turns exactly one test RED,
  `TestDropOneNewlinePerSegmentBoundary::test_a_boundary_with_no_newline_at_all_is_illegal`,
  at `1 failed, 20 passed`. The worktree was removed and pruned; `git status
  --porcelain` empty and `git worktree list` the primary alone at this verdict.
  Gate D's redness is charged to the REVIEWER, not to R26. The R26 block's own
  PAIR_A TO wrote the marker NAMES and a bare `<<<` into `.agent/live_review.md`
  as prose, and then ordered those strings to count 0 in that same file —
  DECISION F105 D8 item 2's sixth recurrence, and precisely the class R26's own
  new item 6 installs. The worker MEASURED it and declared it instead of editing
  prose to force the count down, which is the correct behaviour and costs R26
  nothing. The property the gate exists to protect does hold, independently
  checked: a line-anchored count of marker LINES is 0 in all five targets.
  `LAST_REVIEWED_SHA` advances 0341928d -> d0ebba63.
- R27: SPLIT round — record the R26 gate, resolve R-0253 and R-0254, register
  and fix R-0255, and wire `on_call` for the flight-plan prompt at the one
  `do_cmd` site whose evidence sink already exists.
- Reviewer gate on R27 (2026-08-10): PASS. Range `d0ebba63..73259d7a`, eight
  commits, read as a real diff: only the nine paths the block named, and the
  replan site the block forbade is untouched. Insertions per commit 457, 371,
  69, 3, 1, 95, 77, 1 — each under 500.
  Transport under the §4.9 digest fallback: `.agent/authored/f105-r28-1.md`'s
  predecessor `.agent/authored/f105-r27-1.md` and `.agent/last_block.md` both
  recompute to `efef62a6c61e08b33682175f034b9ba1441cac7245b6dceca5e05093199fb71a`,
  `cmp` silent, 457 lines each — the digest the handback declared.
  All 13 pairs re-sliced from the COMMITTED authored file by the reviewer's own
  marker-LINE reader and measured disk to disk: declared shape equals measured
  shape for every one, appends at FROM 1x, rewrites at FROM 0x after and TO 1x,
  and PAIR_N byte-equal to `.agent/plan.md` at 42 lines against the cap of 50.
  Diff-scoped accounting per §4.9: `.agent/live_review.md` ADDED 69, fully
  decomposed, strays 0; `docs/agents/planner_reviewer_prompt.md` ADDED 3,
  strays 0; `packages/orchestration/flight_plan.py` ADDED 44, strays 0;
  `tests/orchestration/test_prompt_trace.py` ADDED 25, strays 0;
  `apps/cli/commands/do_cmd.py` ADDED 26, strays 0. No ADDED line in any file
  came from outside a TO slice.
  Gates re-run by THIS reviewer with real exit codes: `tests/orchestration/`
  `10499 passed, 7 skipped in 627.56s` — one more test than R26's 10499-minus-one
  baseline, the new guard; `tests/cli/` `1329 passed in 260.89s`;
  `test_prompt_trace.py` `38 passed`; `tests/docs/` `294 passed`; the dashboard
  contract `70 passed`; the canary `42 passed`. Mutation red-proof M1 run by the
  reviewer in a disposable worktree at 73259d7a: removing BOTH the `on_call=`
  argument and the `make_flight_plan_call_recorder,` import turns exactly one
  test RED, `TestSegmentManifest::test_the_cli_flight_plan_recorder_passes_the_composed_prompt`,
  at `1 failed, 37 passed`. Worktree removed and pruned; `git status
  --porcelain` empty and `git worktree list` the primary alone at this verdict.
  The 457-line block is charged to the REVIEWER, not to R27. DECISION F105 D5
  caps a block at 400 and D8 item 1 says to COUNT it on the final bytes; the
  reviewer estimated instead of counting, and a block must be saved verbatim, so
  the worker was right to declare the overage rather than trim it. First
  recurrence of item 1 in this feature. The remedy is mechanical counting before
  emission, which is what item 1 already prescribes.
  `LAST_REVIEWED_SHA` advances d0ebba63 -> 73259d7a.
- R28: SPLIT round — record the R27 gate, resolve R-0255, register R-0256, add
  `append_trace_jsonl` beside the per-job trace writer and wire the replan site
  with it so a replan records its flight-plan manifest without truncating the
  traces the job's first run wrote.
- Reviewer gate on R28 (2026-08-10): PASS. Range `73259d7a..55550615`, seven
  commits, read as a real diff: only the eight paths the block named.
  `write_trace_jsonl` is untouched, as the block required — the new function is
  a sibling, not a parameter on the old one. Insertions per commit 368, 263, 57,
  51, 25, 63, 1 — each under 500, and the authored block is 368 lines against
  DECISION F105 D5's cap of 400, counted this time rather than estimated.
  Transport under the §4.9 digest fallback: `.agent/authored/f105-r28-1.md` and
  `.agent/last_block.md` both recompute to
  `c323410875ab8da7313a988a79d6f74e0976ba3320721b0d8f0ad35808df7fe2`, `cmp`
  silent, 368 lines each — the digest the handback declared.
  All seven pairs re-sliced from the COMMITTED authored file by the reviewer's
  own marker-LINE reader and measured disk to disk: declared shape equals
  measured shape for every one, appends at FROM 1x, rewrites at FROM 0x after
  and TO 1x, and PAIR_H byte-equal to `.agent/plan.md` at 41 lines against the
  cap of 50. Diff-scoped accounting per §4.9: `.agent/live_review.md` ADDED 57,
  `packages/orchestration/prompt_trace.py` ADDED 13,
  `tests/orchestration/test_prompt_trace.py` ADDED 38,
  `apps/cli/commands/do_cmd.py` ADDED 25 — strays 0 in all four. No ADDED line
  came from outside a TO slice.
  Gates re-run by THIS reviewer with real exit codes: `tests/orchestration/`
  `10502 passed, 7 skipped in 703.66s` — three more than R27's 10499, the three
  tests this round adds; `tests/cli/` `1329 passed in 261.91s`;
  `test_prompt_trace.py` `41 passed`; `tests/docs/` `294 passed`; the dashboard
  contract `70 passed`; the canary `42 passed`.
  BOTH red-proofs reproduced by the reviewer in a disposable worktree at
  55550615, with `PYTHONDONTWRITEBYTECODE=1` because the worker's own first
  attempt showed CPython's `(mtime, size)` `.pyc` validation accepting a stale
  cache when a same-length revert lands in the same clock second — a real
  diagnosis, honestly declared, and worth remembering for every future
  same-length mutation. M1: `append_trace_jsonl`'s `path.open("a")` changed to
  `path.open("w")` turns exactly one test RED,
  `test_appending_traces_keeps_the_earlier_ones`, at `1 failed, 40 passed`. M2:
  after reverting M1, deleting the `on_call=` argument from the REPLAN call only
  turns exactly one test RED, `test_the_replan_path_records_and_appends_its_traces`,
  at `1 failed, 40 passed`, with `git diff --stat` showing
  `apps/cli/commands/do_cmd.py` alone — so M1 was genuinely reverted and the two
  mutants are independent. Worktree removed and pruned; `git status
  --porcelain` empty and `git worktree list` the primary alone at this verdict.
  Noted, not held against the round: the replan guard asserts
  `source.count("on_call=make_flight_plan_call_recorder(") == 2`, so it pins BOTH
  wiring sites and any future round that intentionally rewires either must update
  that count. The worker flagged this itself rather than letting the next round
  discover it.
  `LAST_REVIEWED_SHA` advances 73259d7a -> 55550615.
- R29: session-close round — record the R28 gate, sync the plan, write the
  session-ending handoff. State files only.
- Reviewer gate on R29 (2026-08-10): PASS. Range `55550615..HEAD` = five commits
  (9e497810, aa056f36, 0b431989, 9d7511e5, 0c8932e3) read as a real diff: five
  paths, every one under `.agent/`; insertions 165, 109, 48, 49, 9 — each under
  500. C4 (0c8932e3) is a declared deviation, not in the block: gate rows G and H
  can only carry real post-C3 numbers once C3 exists (the R28 C5 precedent), and
  the handoff declares it. Transport re-proved disk to disk —
  `.agent/authored/f105-r29-1.md` and `.agent/last_block.md` both recompute to
  `fdf4d7f6f05273c26b055f436675144954f241330b26a7d6f2414c2a5d04c179`, `cmp`
  silent, 165 lines each against DECISION F105 D5's cap of 400. Both pairs
  re-sliced from the COMMITTED authored file by the reviewer's own whole-line
  marker reader: PAIR_A is APPEND-shaped as declared — the TO's first line IS
  the FROM — at FROM 1x, and 0b431989 ADDS exactly 48 lines against 48 TO-only
  lines, in order, 0 removals and 0 strays; PAIR_B is byte-equal to
  `.agent/plan.md` at 43 lines against the cap of 50.
  Gates re-run by THIS reviewer, real exit codes: `grep -c -E '^<<<'` = 0 in
  `.agent/live_review.md` and `.agent/plan.md`; `tests/docs/` `294 passed in
  0.27s`; dashboard contract `70 passed in 4.16s`; canary `42 passed in 19.52s`;
  `git status --porcelain` empty; `git worktree list` the primary alone. Open
  findings recounted from the file rather than from the handoff: R-0221, R-0239,
  R-0246, R-0247, R-0256 — five, as declared. No mutation red-proof: the diff
  names nothing executable, so there is no branch to mutate (D10, D8 item 5).
  `remedy plan status` and `remedy plan next` were NOT run — the command sits
  outside this session's command allowlist and every attempt was denied;
  `docs/roadmap/STATUS.md` was read directly and carries exactly one `[~]`, F105.
  `LAST_REVIEWED_SHA` advances 55550615 -> 0c8932e3.
- R30: SPLIT round — `compile_mission_plan` composes ONCE and hands that one
  ComposedPrompt to a `mission_plan` recorder, plus the R-0246 docstring fix.
  No sink, no CLI: those are R31.
- Reviewer gate on R30 (2026-08-10): PASS, with R-0257 registered against the
  reviewer's own authored text. Range `0c8932e3..0ba30611` = six commits, read
  as a real diff: seven paths, exactly the ones the block named; insertions per
  commit 399, 349, 27, 64, 64, 57 — each under 500.
  Transport re-proved disk to disk against the reviewer's surviving original:
  `.remedy-wt/f105-r30-1.block.md`, `.agent/authored/f105-r30-1.md` and
  `.agent/last_block.md` all three
  `691c21a6b9717c160379291f63e6f45318e412f0e2714e590afb8ec7f8e14afa`, both
  `cmp` runs silent, 399 lines against DECISION F105 D5's cap of 400. This is
  the primary proof shape, not the §4.9 digest fallback: in-session the
  reviewer's original never left the disk.
  All seven pairs re-sliced from the COMMITTED authored file by the reviewer's
  own whole-line marker reader; declared shape equals measured shape for every
  one. PAIR_A FROM 1x with 27 TO-only lines against 27 ADDED and 0 removed;
  PAIR_G FROM 1x with 63 TO-only against 64 ADDED — the one extra is the
  `    compose_mission_prompt,` import line C4 explicitly ordered, so strays 0;
  PAIR_D FROM 1x with 42 TO-only. PAIR_B, C, E and F all FROM 0x after and
  TO 1x. Across the whole C3 commit (64 added, 3 removed) no ADDED line comes
  from outside a TO and no REMOVED line from outside a FROM. PAIR_H is
  byte-equal to `.agent/plan.md` at 45 lines against the cap of 50.
  Gates re-run by THIS reviewer with real exit codes: `grep -c -E '^<<<'` = 0 in
  all four targets; `test_mission_compiler.py` + `test_mission_prompt_golden.py`
  `121 passed in 0.49s`; the three caller suites `78 passed in 1.42s`;
  `tests/docs/` `294 passed in 0.30s`; the dashboard contract `70 passed in
  4.09s`; the canary `42 passed in 19.47s`; `git status --porcelain` empty and
  `git worktree list` the primary alone at this verdict.
  Red-proof M1 reproduced by the reviewer in a disposable worktree at ccb128f0
  with `PYTHONDONTWRITEBYTECODE=1`: deleting `composed_prompt=composed,` from
  `make_mission_plan_call_recorder` turns exactly the two named tests RED at
  `2 failed, 114 passed in 0.61s`. Reverted, worktree removed and pruned.
  `LAST_REVIEWED_SHA` advances 0c8932e3 -> 0ba30611.
- R31: SPLIT round — fix R-0257, name the mission-plan evidence sink in
  `plan_mission`, label the provider from `remedy mission plan`, and pin all of
  it with `TestMissionPlanEvidenceSink`.
- Reviewer gate on R31 (2026-08-10): PASS. Range `0ba30611..9bd3a3e7` = seven
  commits, read as a real diff: eight paths, exactly the ones the block named;
  insertions per commit 384, 257, 53, 13, 17, 67, 58 — each under 500.
  Transport disk to disk against the reviewer's surviving original:
  `.remedy-wt/f105-r31-1.block.md`, `.agent/authored/f105-r31-1.md` and
  `.agent/last_block.md` all three
  `8833261bcf731bec965fbcd52ff7aa8339141a5ae076397cfeee41232f307003`, both
  `cmp` runs silent, 384 lines against DECISION F105 D5's cap of 400.
  All eight pairs re-sliced from the COMMITTED authored file by the reviewer's
  own whole-line marker reader; declared shape equals measured shape for every
  one. PAIR_A FROM 1x with 52 TO-only lines; C2 ADDS 53 and REMOVES 1, the
  extra add and the single removal both PAIR_B's, so strays 0 in both
  directions. PAIR_C, D, E and F all FROM 0x after and TO 1x, with C3's 12
  added / 7 removed and C4's 12 added / 2 removed on the compiler and 5 added
  on the CLI all accounted for by their TOs. PAIR_G FROM 1x with 66 TO-only
  against 67 ADDED. PAIR_H byte-equal to `.agent/plan.md` at 42 lines against
  the cap of 50. Exactly two additions sit outside a TO in the whole round and
  the block named both in advance: the `Landed: R-0257` line and the
  `from packages.orchestration import mission_compiler` test import.
  Gates re-run by THIS reviewer with real exit codes: `grep -c -E '^<<<'` = 0
  in all five targets; `test_mission_compiler.py` + `test_mission_prompt_golden.py`
  `126 passed in 0.65s`; the three caller suites `78 passed in 1.23s`;
  `tests/cli/` `1329 passed in 261.30s`; `tests/docs/` `294 passed in 0.30s`;
  the dashboard contract `70 passed in 4.31s`; the canary `42 passed in 19.46s`;
  `git status --porcelain` empty and `git worktree list` the primary alone.
  BOTH red-proofs reproduced by the reviewer in a disposable worktree at
  db3bdef3 with `PYTHONDONTWRITEBYTECODE=1`. M1: `append_trace_jsonl` swapped
  for `write_trace_jsonl` in `plan_mission`'s import AND call turns exactly one
  test RED, `test_a_recompile_appends_rather_than_truncating`, at
  `1 failed, 120 passed in 0.60s`. M2: after reverting M1 — `git diff --stat`
  empty, so the revert is proved — deleting `traces=prompt_traces,` turns
  exactly two RED, `test_planning_writes_the_trace_into_the_evidence_dir` and
  the recompile test, at `2 failed, 119 passed in 0.74s`. Worktree removed and
  pruned. The handback's 71-line handoff carries its DECISION D15 stated-cause
  line and drops no mandated section, which is the rule, not an exception.
  `LAST_REVIEWED_SHA` advances 0ba30611 -> 9bd3a3e7.
- R32: session-close round — record the R31 gate, resolve R-0246 and R-0257,
  write the session-ending handoff. State files only.
- Reviewer gate on R32 (2026-08-10): PASS. Range `9bd3a3e7..cab89962` = four
  commits, read as a real diff: five paths, every one under `.agent/`, exactly
  the ones the block named; insertions per commit 196, 129, 54, 47 — each under
  500. Transport disk to disk against the reviewer's surviving original:
  `.remedy-wt/f105-r32-1.block.md`, `.agent/authored/f105-r32-1.md` and
  `.agent/last_block.md` all three
  `56173ae6acaf147af639b03200b9398df3158598b086dc686df68e34131cb78f`, all three
  `cmp` runs silent, 196 lines against DECISION F105 D5's cap of 400.
  All three C2 pairs re-sliced from the COMMITTED authored file by the
  reviewer's own whole-line marker reader: declared shape equals measured shape
  for every one — each TO opens with its FROM verbatim, so all three are APPEND
  as declared. FROM exactly 1x in the target both before and after the write,
  TO exactly 1x after. TO-only lines 39 + 7 + 8 = 54; the commit ADDS 54 and
  REMOVES 0 over `.agent/live_review.md`, so strays are 0 in both directions
  and no added line sits outside a TO. PAIR_D byte-equal to the applied
  `.agent/plan.md` at 43 lines against the cap of 50; the handoff is 59 lines
  against the cap of 60.
  Gates re-run by THIS reviewer with real exit codes: `grep -c -E '^<<<'`
  prints `0` in `.agent/live_review.md` and `0` in `.agent/plan.md` (rc 1, the
  honest no-match); `tests/docs/` `294 passed in 0.30s`; the dashboard contract
  `70 passed in 4.11s`; the canary `42 passed in 19.44s`; `git status
  --porcelain` empty and `git worktree list` the primary alone. Gate H is
  re-measured here AFTER the C3 commit the handback could not measure itself,
  and it is clean — the declared D15 deviation was a timing statement, not a
  gap. No mutation red-proof: nothing executable changed, so there is no branch
  to mutate (DECISION F105 D10).
  The record's own claims were spot-checked against git rather than read: the
  R31 gate line's "seven commits, eight paths" and its per-commit insertions
  384, 257, 53, 13, 17, 67, 58 are exact, and both resolution commits it names
  exist and touch the file it says they do — 39da9b61 for R-0246, 3d37567f for
  R-0257.
  The open-findings count of 4 was re-derived, not accepted: R-0221, R-0239,
  R-0247 and R-0256 carry no resolution. Four further entries also carry no
  `Done: R-XXXX` line of their own and are nevertheless closed — R-0240 and
  R-0241 share one `Done:` paragraph filed under R-0241, and R-0250 and R-0252
  were resolved inline as DECISIONs D8 and D10. Both of those deferred their
  proof to "the NEXT session's gate", which is this one: §3 of
  docs/agents/planner_reviewer_prompt.md carries the checklist as items 1-6,
  including item 5's reachability rule (D10) and item 6's target-content rule,
  and it reads as intended. Both are therefore closed on evidence, not on
  assertion. A mechanical `Done:`-grep undercounts resolutions by four; that is
  a property of this file's format, not a defect of R32, and it is recorded
  here so no later reader re-derives it as a finding.
  `LAST_REVIEWED_SHA` advances 9bd3a3e7 -> cab89962.
- R33: SPLIT round — the orchestrator prompt's call evidence: a per-iteration
  recorder carrying the segment manifest, and the sink appending to the
  mission's `prompt_trace.jsonl` from inside `run_mission` (DECISION D11).
- Reviewer gate on R33 (2026-08-10): PASS, with one declared deviation accepted
  and its cause registered as R-0258 against the REVIEWER, not the worker.
  Range `cab89962..af35adbc` = eight commits, read as a real diff: eight paths,
  every one on the block's Change line, `mission_cmd.py` absent by the declared
  deviation; insertions per commit 293, 232, 79, 27, 55, 105, 2 — each under
  500. Transport disk to disk against the reviewer's surviving original: all
  three of `.remedy-wt/f105-r33-1.block.md`, `.agent/authored/f105-r33-1.md`
  and `.agent/last_block.md` carry
  `d6d9d2a8e0d03d646021ed101d7c5b83dacce65b66dc75c74e5ea92306f40d80`, every
  `cmp` silent, 293 lines against D5's cap of 400.
  The code was read bottom-up rather than taken from the report. The append sits
  in a `finally`, so a call that RAISES still leaves its evidence before the
  boundary turns the fault into a terminal — the ledger's durability, which a
  single flush after the loop would not have given. The recorder is rebuilt per
  iteration from that iteration's `ComposedPrompt`, and `_observe_call` is
  defined and consumed inside the same iteration, so no manifest can describe
  earlier bytes and the closure has no late-binding hazard. `on_call` is CHAINED
  rather than replaced. The two new module-level imports introduce no cycle:
  `prompt_trace` imports only `prompt_segments`.
  Gates re-run by THIS reviewer with real exit codes: the scoped gate
  `201 passed in 1.15s` including the frozen prompt golden, so the composed
  BYTES did not move; the three caller suites `152 passed in 38.12s`;
  `tests/docs/` `294 passed in 0.30s`; the dashboard contract
  `70 passed in 3.96s`; the canary `42 passed in 19.46s`; `git status
  --porcelain` empty and `git worktree list` the primary alone.
  All three red-proofs reproduced by the reviewer in a disposable worktree at
  af35adbc with `PYTHONDONTWRITEBYTECODE=1`, each reverted and the revert proved
  by an empty `git diff --stat`, worktree removed and pruned. Baseline
  `3 passed in 0.33s`. M1, deleting the `append_trace_jsonl` call:
  `2 failed, 1 passed`, the two named tests RED. M2,
  `append_trace_jsonl` -> `write_trace_jsonl`: `1 failed, 2 passed`, only
  `test_a_second_run_appends_rather_than_truncating` RED — so the append is
  pinned as the writer, not merely used. M3 as ORDERED was unrunnable and the
  worker said so; the reviewer applied the ordered edit anyway to test the
  worker's account of WHY, and it failed exactly as reported.
  The handback's own corrections hold: the R-0149 self-reference exception it
  cites for the trailing bookkeeping commit is really in
  docs/agents/handback_template.md, and its note that D11 and PAIR_C's Next
  Steps understate the gap by one caller is correct — both reviewer-authored,
  applied verbatim, and this round repairs the substance, not the wording.
  `LAST_REVIEWED_SHA` advances cab89962 -> af35adbc.
- R34: SPLIT round — repair the file-wide source guard into a per-call-site
  assertion, install §3 checklist item 7, label the provider on
  `remedy mission run`, and document the gauntlet's absent label as deliberate.
- Reviewer gate on R34 (2026-08-10): PASS. Range `af35adbc..28fe51c3` = eight
  commits, read as a real diff: eleven paths, exactly the ones the block named;
  insertions per commit 398, 334, 123, 12, 7, 14, 17, 85 — each under 500.
  Transport disk to disk against the reviewer's surviving original: all three of
  `.remedy-wt/f105-r34-1.block.md`, `.agent/authored/f105-r34-1.md` and
  `.agent/last_block.md` carry
  `6d816a6434c6d98cdaafca3df7654580d2c5985abdef65398c9eccb8fb97c14e`, every
  `cmp` silent, 398 lines against D5's cap of 400.
  All eight FROM/TO pairs re-sliced from the COMMITTED authored file by the
  reviewer's own whole-line marker reader: declared shape equals measured shape
  for every one, four REWRITEs at FROM 0x / TO 1x and four CONTAINS-FROM at
  FROM 1x / TO 1x. PAIR_I byte-equal to the applied `.agent/plan.md` at 43 lines
  against the cap of 50. Strays 0 in both directions on all five written paths
  once the accounting is right: PAIR_H is a PREPEND, so its TO-only lines are
  the LEADING seven, and a line carried unchanged through a REWRITE is diff
  CONTEXT rather than an add plus a remove. The reviewer's first pass modelled
  both wrongly and reported three phantom strays against a round that had none;
  the corrected pass reconciles `+81/-1` on live_review.md, `+42/-0` on
  decisions.md, `+12/-0` on the prompt doc, `+7/-1` on the compiler test,
  `+7/-1` on the CLI and `+7/-0` on the gauntlet exactly.
  Gates re-run by THIS reviewer with real exit codes: the scoped gate
  `323 passed in 1.69s`, the frozen prompt golden inside it, so the composed
  BYTES still have not moved; the three caller suites `152 passed in 38.17s`;
  `tests/docs/` `294 passed in 0.25s`; the dashboard contract
  `70 passed in 3.92s`; the canary `42 passed in 19.55s`; `grep -c -E '^<<<'`
  prints 0 in all four written targets; `git status --porcelain` empty and
  `git worktree list` the primary alone.
  Both red-proofs reproduced by the reviewer in a disposable worktree at
  28fe51c3 with `PYTHONDONTWRITEBYTECODE=1`, each reverted and the revert proved
  by an empty `git diff --stat`, worktree removed and pruned. Baseline
  `2 passed in 0.39s`. M1, deleting the label from the `run_mission` call: the
  run guard RED and the plan guard GREEN — the two guards watch different call
  sites, which is the whole point of the repair. M2, moving the label onto the
  `plan_mission` call: the run guard RED, so the repaired guard is per-call-site
  and not a disguised count.
  The block's own C4-before-C5 ordering was honoured and matters: the repaired
  guard was green at 083a42d3, BEFORE the second label landed at f3968dfd, so
  the suite was never red between two commits of this round.
  The worker's declared deviation is ACCEPTED and is not a defect of the round:
  the 200-character window overshoots its call, the worker measured that instead
  of quietly shrinking the constant, and the wording is the reviewer's. It is
  registered as R-0260 rather than absorbed. The 120-line handoff carries its
  DECISION D15 stated-cause line and drops no mandated section, which is the
  rule and not an exception.
  `LAST_REVIEWED_SHA` advances af35adbc -> 28fe51c3.
- R35: session-close round — record the R34 gate, resolve R-0258 with
  reviewer-authored text, register R-0260, and write the session-ending
  handoff. State-file-only; no mutation red-proof ordered or run.
- Reviewer gate on R35 (2026-08-10): PASS, by the reviewer of the FOLLOWING
  session. R35 was the last round of a SESSION, not of the branch, so it does
  get an on-disk entry: §4.13's terminator clause covers the last round of a
  BRANCH, and R35's own handoff correctly named this gate as the next action
  rather than claiming a verdict on itself.
  Range `28fe51c3..bcfb12e3` = four commits, five paths, every one under
  `.agent/` — `git diff --name-only` lists exactly the five the block named,
  nothing under `packages/`, `apps/`, `tests/` or `docs/`. Insertions per
  commit 242, 168, 81 and 61, each under 500; the 168/324 one is the
  single-state-file verbatim rewrite AGENTS.md exempts from the churn reading
  anyway.
  Transport disk to disk against the reviewer's surviving original — the
  PRIMARY proof shape, not the §4.9 digest fallback:
  `.remedy-wt/f105-r35-1.block.md`, `.agent/authored/f105-r35-1.md` and
  `.agent/last_block.md` all three carry
  `b14899d9c8b57331e26b27546ece4352a4b33ebac6831aa4d2f2ed98195ddc96`, both
  `cmp` runs silent, 242 lines against DECISION F105 D5's cap of 400.
  All five pairs re-sliced from the COMMITTED authored file by this reviewer's
  own whole-line marker reader: declared shape equals measured shape for every
  one. PAIR_A and PAIR_C are REWRITEs at FROM 0x / TO 1x; PAIR_B and PAIR_D are
  CONTAINS-FROM at FROM 1x; PAIR_E is byte-equal to the applied
  `.agent/plan.md` at 44 lines against the cap of 50. The four live_review
  pairs share ONE path in ONE commit and so reconcile TOGETHER against
  `+81/-1`: of the 81 added lines not one comes from outside a TO, and the
  single removed line is PAIR_A's FROM. Strays 0 in both directions, line
  multisets taken against `git show -U0`.
  Gates re-run by THIS reviewer with real exit codes: `grep -c -E '^<<<'`
  prints 0 in both written targets; `tests/docs/` `294 passed in 0.25s`; the
  dashboard contract `70 passed in 4.14s`; the canary `42 passed in 19.64s`;
  `git status --porcelain` empty and `git worktree list` the primary alone at
  this verdict.
  No red-proof was ordered or run, and that is the correct call rather than an
  omission: the round changed nothing executable, so there is no branch to
  mutate (D8 checklist item 5, DECISION F105 D10).
  `LAST_REVIEWED_SHA` advances 28fe51c3 -> bcfb12e3.
