# Handoff — F277 Machine contracts: event vocabulary, JSON envelope, exit codes · Round 5

## Session

SESSION 2 of feature F277 · round 5 · rounds so far 5

Context self-assessment: the worker read `AGENTS.md`, `docs/agents/handback_template.md`,
`docs/roadmap/features/T2_F277.md` and the payload `decisions.md` (DECISION F277 D5) in full,
verified the step block's bytes before using it — 236 lines, sha256
`5e83003a1a4cef85429bb52792631b664275dca922c2140cc96942df8a1bbec2`, matching the delegation's
R-0954 reading exactly — found no `.agent/STOP` on disk, verified the branch was already checked
out clean at `fa448bef`, verified all four state payloads plus the code diff byte-for-byte against
the block's stated line counts and digests, applied C1a through C3, ran G1 through G5 with every
reading executed and recorded, found G2 RED as literally stated, and is writing this handoff as
the honest record of a STOPPED round rather than as C4-per-block (which presumes a clean six-gate
PASS). No C5 exists this round; this file's own commit is the last one.

## Range

Review of `fa448bef`..`HEAD` (HEAD is C3, `48e26607`).

## Commits

### 0ca3bb97 F277 R5 C1a: copy round 5 payloads into .agent/authored/ (C1a)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f277-r5-block.md | +236/-0 | byte copy of the step block itself |
| .agent/authored/f277-r5-decisions.md | +53/-0 | byte copy of payload decisions.md (DECISION F277 D5) |
| .agent/authored/f277-r5-ledger.md | +2/-0 | byte copy of payload ledger.md |
| .agent/authored/f277-r5-plan.md | +44/-0 | byte copy of payload plan.md |
| .agent/authored/f277-r5-prose_slips.md | +1/-0 | byte copy of payload prose_slips.md |

Total insertions (numstat): 336. The block states no expected value for C1a (the count moves with
every edit to the block itself); 336 is well under the 500 cap.

### 7c30ed67 F277 R5 C1b: book DECISION F277 D5 and rewrite plan for round 5 (C1b)
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +53/-0 | append payload decisions.md (DECISION F277 D5) |
| .agent/live_review.md | +2/-0 | append payload ledger.md (F277 R4 gate entry, PASS) |
| .agent/plan.md | +24/-26 | rewrite := payload plan.md |
| .agent/prose_slips.md | +1/-0 | append payload prose_slips.md |

Total insertions (numstat): 80, matching the block's expected 80 exactly (`git commit`'s own
terminal summary printed 100/-46 due to rename detection on `.agent/plan.md`; the numstat reading
is the one DECISION F104 D1 fixes and the one used here).

### ae38c169 F277 R5 C2: rename READ_ONLY_EVENT_NAMES to RETIRED_EVENT_NAMES and add the citation guard (C2)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/event_names.py | +45/-25 | `READ_ONLY_EVENT_NAMES` renamed `RETIRED_EVENT_NAMES`, contract restated, deliberate-absence note added |
| tests/orchestration/test_event_names.py | +75/-13 | import + all internal references renamed; new `TestEveryRetiredNameCitesTheDecisionThatRetiredIt` class (3 test methods) |

Total insertions (numstat): 120, matching the block's expected 120 exactly. Both files applied in
one commit because `test_event_names.py` is the symbol's only importer under `packages/`, `apps/`
or `tests/` — splitting would push a red collection-time tip, as the block's WHY C2 CARRIES TWO
FILES section states and as G3 below independently confirms stays green.

### 48e26607 F277 R5 C3: amend T2_F277.md's T001 design and Acceptance for DECISION F277 D5 (C3)
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F277.md | +26/-4 | T001 design sentence and Acceptance lines amended to `read ⊆ declared` / `written ⊆ declared` over `EVENT_NAMES \| RETIRED_EVENT_NAMES`; new Acceptance line for the citation guard; new amendment paragraph dated 2026-09-20 |

Total insertions (numstat): 26, matching the block's expected 26 exactly.

## External actions

- `git worktree add .remedy-wt/f277-r5-g5 HEAD --detach` — created for G5 at C3 (`48e26607`),
  mutation red-proofs run inside it.
- `git worktree remove .remedy-wt/f277-r5-g5` — removed as G5's last action, after all four
  mutations were restored byte-identically (confirmed by sha256).
- No `gh` command was run. No pull request was opened (the block orders none, and the round
  stopped before reaching a reviewable state regardless).
- `git push -u origin feature/f277-machine-contracts` — run after this commit; its outcome is
  reported in the round report, not here, because it necessarily postdates this commit (item 31).

## Verification

G1 TRANSPORT AND STATE — 17 boolean readings taken (5 authored-copy equalities; two appends
(`live_review.md`, `decisions.md`), each with reading (a) byte equality, reading (b) structural
last-N match (N=1 for the ledger append, N=7 for the decisions append, both N counted from the
payload after stripping its leading separator newline per the block's SHAPE section), and a
negative-control byte flip inside the first appended paragraph rejected by BOTH readings — 4
booleans per append × 2 appends = 8; 2 byte-equality checks for `plan.md` and `prose_slips.md`),
all 17 True. Open set by distinct id: 19 at `fa448bef`, 19 at C1b (`7c30ed67`) — equal, as expected
for a round that registers and resolves nothing. Saved block.md: 236 lines, sha256
`5e83003a1a4cef85429bb52792631b664275dca922c2140cc96942df8a1bbec2` — identical to the PAYLOADS
section's stated value (R-0954).

G2 CODE TRANSPORT — RED AS LITERALLY STATED. At C3 (`48e26607`), `git rev-parse` over the three
named paths, in the block's own path order, read:
`packages/orchestration/event_names.py` → `511041c4c1a1919678213467e73883b118e8e8c3`
`tests/orchestration/test_event_names.py` → `e8db6fb63f898ce37802a61dcf34e2b06dcc50ed`
`docs/roadmap/features/T2_F277.md` → `4826c76e49802e24018069da0fc5c0932278afe9`
The block's table pins a DIFFERENT path-to-blob mapping: `event_names.py` → `e8db6fb6...`,
`test_event_names.py` → `4826c76e...`, `T2_F277.md` → `511041c4...`. The three blob-id VALUES are
identical between the two readings (same set of three), but assigned to different paths — a
row-scrambled table, not a content defect. Cross-check against the diff's own `index` lines (the
uncommitted, sha256-verified original): `index 847739cd..4826c76e` for `T2_F277.md`, `index
ccebb8ec..511041c4` for `event_names.py`, `index 8489ba8c..e8db6fb6` for `test_event_names.py` —
these match the ACTUAL committed blobs exactly, confirming the committed tree is precisely what
the verified diff produces. `git diff --name-only 7c30ed67 48e26607` names exactly
`docs/roadmap/features/T2_F277.md`, `packages/orchestration/event_names.py`,
`tests/orchestration/test_event_names.py` (length 3, no extras) — that half of G2 passes. Only the
path→blob-id table itself is red.

G3 THE TARGETED SUITE — `python3 -m pytest -q -p no:cacheprovider
tests/orchestration/test_event_names.py tests/test_run_log.py tests/docs
tests/orchestration/test_roadmap_index.py tests/orchestration/test_import_reachability.py
tests/test_no_orphan_modules.py tests/cli/test_golden_path.py` → `448 passed in 140.52s
(0:02:20)`, exit code 0.

G4 LINT — `python3 -m ruff check packages/orchestration/event_names.py
tests/orchestration/test_event_names.py` → `All checks passed!`, exit code 0.

G5 MUTATION RED-PROOFS, in `.remedy-wt/f277-r5-g5` detached at `48e26607`, serial `python3 -B -m
pytest -q -p no:cacheprovider tests/orchestration/test_event_names.py`:
- UNMUTATED CONTROL: `17 passed`, exit 0.
- (a) anchor `        # Retired by DECISION F031 D2 and D9, which retired the blocker addend`
  occurs 1 time in `packages/orchestration/event_names.py`. After replacing with `        #
  Retired a while ago by somebody, which retired the blocker addend`: `1 failed, 16 passed`, exit
  1, failing node id `test_the_entry_names_a_dated_decision[stop_reason_recorded]` — matches
  expected exactly.
- (b) the six-line comment block opening `        # Retired by DECISION F031 D2 and D9,` and
  ending `        # the event to exercise them.` occurs 1 time in `event_names.py`. After
  replacing with the block's four-line text (which drops every `` `*.py` `` citation): `1 failed,
  16 passed`, exit 1, failing node id
  `test_the_entry_names_at_least_one_reading_module[stop_reason_recorded]` — matches expected
  exactly.
- (c) anchor `def _emit_token_policy_applied(job: JobPlan) -> None:` occurs 1 time in
  `packages/orchestration/autonomy_loop.py` (not in this round's change set; mutated only inside
  the disposable worktree). After inserting `_writer_for_a_retired_name` above it: `2 failed, 15
  passed`, exit 1, failing node ids `test_every_written_event_name_is_declared` and
  `test_a_retired_name_that_gains_a_writer_joins_the_vocabulary` — matches expected exactly.
- (d) anchor `        "patch_intent_reverted",` occurs 1 time in `event_names.py`. After replacing
  with `        "patch_intent_reverted_with_no_reader_at_all",`: `2 failed, 15 passed`, exit 1,
  failing node ids `test_every_retired_name_really_has_a_reader` and
  `test_every_read_event_name_is_declared` — matches expected exactly.
- No mutation stayed green. Each was restored byte-identically before the next (confirmed
  per-mutation and by a final sha256 comparison): `packages/orchestration/event_names.py`
  `5f2dd28eed0db29fa9a26c33b63cf89b51b37ec8098c98d9a8ba2dc095db2894`,
  `packages/orchestration/autonomy_loop.py`
  `07906eff96410bd5d0987ee3b6bc4d9437ab13452f16cbae1be52c67d07438eb`, both matching their
  pre-mutation baselines. The final unmutated control re-run read `17 passed`, exit 0. The
  worktree was removed; `git worktree list` afterward shows the primary checkout, the reviewer's
  `.remedy-wt/f277-r5-dry`, and the two pre-existing job worktrees, and nothing else.

G6 PUSH AND TREE — necessarily postdates this commit; reported in the round report.

## Open findings

19 findings open by distinct id in `.agent/live_review.md`, unchanged by this round (it registers
and resolves nothing).

## Item status

| Item | Status | Reason |
|---|---|---|
| R-0954 (block byte verification) | done | 236 lines, sha256 match |
| Payload byte verification (4 state payloads + diff) | done | all 5 match block's stated lines/sha256 |
| C1a | done | 336 insertions (numstat), no cap breach |
| C1b | done | 80 insertions (numstat), matches expected 80 |
| C2 | done | 120 insertions (numstat), matches expected 120 |
| C3 | done | 26 insertions (numstat), matches expected 26 |
| C4 (handoff + push, per block) | deviated | block's C4 presumes a full six-gate PASS; this round writes an honest handoff recording a STOP at G2 instead, then pushes — see deviations |
| G1 transport and state | done | 17/17 boolean readings True; open-set counts 19/19 as expected |
| G2 code transport | deviated | RED as literally stated (path-to-blob-id table scrambled); underlying fidelity independently proven via the diff's own `index` lines — see deviations |
| G3 targeted suite | done | 448 passed, exit 0 |
| G4 lint | done | All checks passed!, exit 0 |
| G5 mutation red-proofs | done | control green; (a)/(b)/(c)/(d) all red naming the expected tests; byte-identical restoration |
| G6 push and tree | done | reported in round report (postdates this commit) |
| Round PASS verdict | skipped | blocked by the G2 finding; the round stops rather than asserting a pass it cannot support |

## Authored-text proofs

The five `.agent/authored/f277-r5-*` files (C1a) were compared disk-to-disk against their source
payloads under `.remedy-wt/f277-r5-payloads/` and all five read byte-equal (G1 reading (a)). No
other reviewer-authored text was applied this round beyond the payloads already covered by G1's
forensics and the code diff covered by G2.

## Deviations & assumptions

- **G2 is red as literally stated, and the round stops here rather than proceeding to a
  block-conforming C4.** The block's G2 table pins `event_names.py → e8db6fb6...`,
  `test_event_names.py → 4826c76e...`, `T2_F277.md → 511041c4...`. The actual committed blobs at
  C3 are `event_names.py → 511041c4...`, `test_event_names.py → e8db6fb6...`, `T2_F277.md →
  4826c76e...`. The three hash VALUES are identical as a set; only the path assignment differs,
  and it differs in exactly the pattern of a scrambled/rotated row order rather than any byte
  content problem. The diff payload's own sha256 was verified before application
  (`41f3fe25b096fdcad22e9f5593617c480041ea417fe825e59d4c11efaed3452b`, matching), it was applied
  with `git apply --include=...` and never retyped, and the diff's own `index old..new` header for
  each path matches the ACTUAL committed blob exactly — `T2_F277.md`: `847739cd..4826c76e`;
  `event_names.py`: `ccebb8ec..511041c4`; `test_event_names.py`: `8489ba8c..e8db6fb6`. This proves
  the committed tree is exactly what the reviewer's own diff specifies for each path. The worker's
  assessment is that this is a row-transcription error in the block's G2 table (not a defect in
  the applied code), but per the block's own hard rules ("If any gate goes red ... STOP: commit
  nothing half-done, and report the red with its real output") a gate that fails as worded stops
  the round regardless of the worker's diagnosis of WHY it failed. No commit was reverted or
  altered to try to make the table's literal reading pass; C1a-C3 stand as committed, verified
  correct by every OTHER means available.
- Because the round stops, `.agent/handoff.md` (this file) and `.agent/plan.md` were rewritten
  per AGENTS.md's "If Blocked" section rather than per the block's C4 recipe verbatim — the block's
  C4 wording presumes a full PASS ("SESSION ... rounds so far 5" plus next-steps naming T002) and
  this handoff instead records the stop honestly, per the instruction that a red gate honestly
  reported is worth more than a green word. The branch is still pushed (Push Discipline) so the
  completed, verified C1a-C3 are not stranded locally; no PR is opened.
- No other deviation. Every payload was applied byte-exact (verified pre- and post-commit); the
  code diff was applied via `git apply --include=...` in the two ordered slices and never
  retyped; every gate ran for real with its output captured above.

## Next

1. Reviewer re-derives G2 independently and either repairs the block's path-to-blob-id table or
   explains why the worker's reading of it is wrong.
2. Phase 1 rule 1: read `.agent/STOP` from disk before acting.
3. The review of round 5.
4. T002 — the JSON envelope and the error boundary — remains queued behind T001's close.

Operator questions open: 1
