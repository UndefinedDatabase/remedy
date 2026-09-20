# Handoff — F277 Machine contracts: event vocabulary, JSON envelope, exit codes · Round 2

## Session

SESSION 2 of feature F277 · round 2 · rounds so far 2

Context self-assessment: the worker read `AGENTS.md`, `docs/agents/handback_template.md`,
`docs/roadmap/features/T2_F277.md` and the payload `decisions.md` in full, verified the step
block's bytes before using it — 227 lines, sha256
`5a260b134de247d65a19d206bdeeee10da3f5d6ad3d62af4de98630d1d3e42ba`, matching the delegation
message's R-0954 reading exactly — found no `.agent/STOP` on disk, verified the branch was
already checked out clean at `9114721f`, verified all five state payloads plus the code diff
byte-for-byte against the block's stated line counts and digests, applied C1a and C1b, applied
the code diff in two `--include` slices as C2 and C3, applied C4's resolution append, ran G1
through G5 with every reading executed and recorded, and is now writing this handoff as C5.

## Range

Review of `9114721f`..`HEAD` (HEAD before this commit is C4, `9c29ca6d`).

## Commits

### 213c2879 F277 R2 C1a: copy round 2 payloads into .agent/authored (C1a)
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f277-r2-block.md | +227/-0 | byte copy of the step block itself |
| .agent/authored/f277-r2-decisions.md | +65/-0 | byte copy of payload decisions.md (DECISION F277 D4) |
| .agent/authored/f277-r2-ledger.md | +4/-0 | byte copy of payload ledger.md |
| .agent/authored/f277-r2-plan.md | +47/-0 | byte copy of payload plan.md |
| .agent/authored/f277-r2-prose_slips.md | +1/-0 | byte copy of payload prose_slips.md |
| .agent/authored/f277-r2-resolution.md | +2/-0 | byte copy of payload resolution.md |

Total insertions (numstat): 346. The block states no expected value for C1a (the count moves
with every edit to the block itself); 346 is well under the 500 cap.

### 2de3bb3f F277 R2 C1b: book round 1 PASS and register R-1012, plan for round 2 (C1b)
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +65/-0 | append payload decisions.md (DECISION F277 D4) |
| .agent/live_review.md | +4/-0 | append payload ledger.md (F277 R1 gate + R-1012 registration) |
| .agent/plan.md | +27/-24 | rewrite := payload plan.md |
| .agent/prose_slips.md | +1/-0 | append payload prose_slips.md |

Total insertions (numstat): 97. The block's stated expectation was 117; `git show --numstat`
(re-checked with and without rename detection, both identical) reads 97 — see Deviations. Well
under the 500 cap either way.

### dc789ab0 F277 R2 C2: dispose of worker_adapters_listed, approval_decision and the dead revert_snapshot signal (C2)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/autonomy_readiness.py | +0/-9 | delete `_has_worker_adapters` and `_has_revert_snapshot`, drop the `revert_snapshot` signal |
| packages/orchestration/event_names.py | +6/-9 | remove `approval_decision` and `worker_adapters_listed` from the quarantine, update the `patch_intent_reverted` comment |
| packages/orchestration/project_brain.py | +1/-1 | `revert_capable` reads `verified_snapshot` instead of the dead `revert_snapshot` |
| packages/orchestration/stop_reasons.py | +8/-2 | `derive_stop_reasons` repoints at `patch_intent_approved`/`patch_intent_rejected` via `_DECIDED` |

Total insertions (numstat): 15, matching the block's expected 15 exactly.

### a19777a0 F277 R2 C3: add tests for the three dispositions and repair R-1012 (C3)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_event_names.py | +2/-2 | R-1012 repair: docstring numeral sentence replaced |
| tests/orchestration/test_stop_reasons.py | +64/-0 | `TestADecidedIntentIsNotAwaitingApproval`, four tests |
| tests/test_autonomy_readiness.py | +59/-0 | `TestTheBrainReadsTheAuthoritativeRevertSignal`, two tests |

Total insertions (numstat): 125, matching the block's expected 125 exactly.

### 9c29ca6d F277 R2 C4: resolve R-1012 (C4)
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | append payload resolution.md (`Done: R-1012 —`) |

Total insertions (numstat): 2, matching the block's expected 2 exactly.

## External actions

- `git worktree add --detach .remedy-wt/f277-r2-g5 a19777a0` — created for G5, mutation
  red-proofs run inside it.
- `git worktree remove .remedy-wt/f277-r2-g5` — removed as G5's last action, after all three
  mutations were restored byte-identically (confirmed by sha256).
- `git push -u origin feature/f277-machine-contracts` — run after this commit (C5); its outcome
  is reported in the round report, not here, because it necessarily postdates this commit
  (item 31).
- No `gh` command was run. No pull request was opened.

## Verification

G1 TRANSPORT AND STATE — 20 boolean readings taken, all True (6 authored-copy equalities;
live_review.md@C1b reading (a), N=2, reading (b), two negative-control rejections; decisions.md@C1b
reading (a), N=9, reading (b), two negative-control rejections; live_review.md@C4 reading (a),
N=1, reading (b), two negative-control rejections; 2 byte-equality checks for plan.md and
prose_slips.md). Open set by distinct id: 19 at `9114721f` (R-1012 not present), 20 at C1b
(R-1012 present), 19 at C4 (R-1012 not present). Saved block.md: 227 lines, sha256
`5a260b134de247d65a19d206bdeeee10da3f5d6ad3d62af4de98630d1d3e42ba` — identical to the PAYLOADS
section's stated value.

G2 CODE TRANSPORT — at C3, `git rev-parse` over the seven named paths read
`6bf0866a32ab7afc53b0c62de671abe3ad11533d`, `c7ea49597a894652e9bbb16d4e806c70776a81da`,
`e1fc35c8a4de6f34042f5994f6d2ebc2ab905f78`, `1b56d322a8f8f515965473b64ab26503416522f4`,
`f812ba15e101dbfb8e6333e172e3c8e11ca79f64`, `62219863ce4aacf0f052985d549609ec51fef935`,
`33926504985c02943e2bb021744d75f2f8045900` — all seven exact matches in the order pinned.
`git diff --name-only 2de3bb3f a19777a0` names exactly those seven paths, length 7, no extras.

G3 THE TARGETED SUITE — `python3 -m pytest -q -p no:cacheprovider
tests/orchestration/test_event_names.py tests/orchestration/test_stop_reasons.py
tests/test_autonomy_readiness.py tests/test_project_brain.py
tests/orchestration/test_source_apply.py tests/test_memory_learn.py
tests/orchestration/test_autonomy.py tests/test_run_log.py
tests/orchestration/test_change_set.py tests/cli/test_golden_path.py` → `332 passed in 140.14s`,
exit code 0.

G4 LINT — `python3 -m ruff check packages/orchestration/autonomy_readiness.py
packages/orchestration/project_brain.py packages/orchestration/stop_reasons.py
packages/orchestration/event_names.py tests/orchestration/test_event_names.py
tests/orchestration/test_stop_reasons.py tests/test_autonomy_readiness.py` →
`All checks passed!`, exit code 0.

G5 MUTATION RED-PROOFS, in `.remedy-wt/f277-r2-g5` detached at `a19777a0`, serial `python3 -B -m
pytest -q -p no:cacheprovider tests/orchestration/test_event_names.py
tests/orchestration/test_stop_reasons.py tests/test_autonomy_readiness.py`:
- UNMUTATED CONTROL: `56 passed`, exit 0.
- (a) anchor `a.get("event") in _DECIDED` occurs 1 time in `stop_reasons.py`. After replacing
  with `a.get("event") == "approval_decision"`: `4 failed, 52 passed`, exit 1, failing node ids
  `test_every_read_event_name_is_declared`, `test_an_approved_intent_no_longer_blocks`,
  `test_a_rejected_intent_no_longer_blocks`, `test_only_the_matching_intent_is_decided` — both
  block-named tests present; the other two are cascading effects of the same reverted guard.
- (b) anchor `"verified_snapshot": _has_verified_snapshot(job, data_dir),` occurs 1 time in
  `autonomy_readiness.py`; anchor `"revert_capable": sigs.get("verified_snapshot", False),`
  occurs 1 time in `project_brain.py`. After the paired insertion/replacement: `2 failed, 54
  passed`, exit 1, failing node ids `test_a_revert_event_alone_does_not_make_the_brain_revert_capable`,
  `test_the_signal_dict_no_longer_carries_the_phantom` — matches expected exactly, no cascade.
- (c) anchor `def _has_agent_loop(events: list[dict[str, Any]]) -> bool:` occurs 1 time in
  `autonomy_readiness.py`. After inserting `_has_worker_adapters` above it: `1 failed, 55
  passed`, exit 1, failing node id `test_every_read_event_name_is_declared` — matches expected
  exactly.
- No mutation stayed green. Each was restored byte-identically before the next (confirmed
  per-mutation and by a final sha256 comparison): `stop_reasons.py`
  `473f06d4d5b3023145c7e4f43f0cc6212d596ef97818f5302aaade3776af9965`, `autonomy_readiness.py`
  `f9e08929ec925a48146baa8cb1603a9d3847da4ef79cc4b9d6116f04ec0d6b79`, `project_brain.py`
  `d691a3e5d3ec89bcf8687a4f2c5dbc9a5eeb99faf8ab32b6a68079508e998d1b`, all matching their
  pre-mutation originals. The final unmutated control re-run read `56 passed`, exit 0. The
  worktree was removed; `git worktree list` afterward shows the primary checkout, the reviewer's
  `.remedy-wt/f277-r2-dry`, and the two pre-existing job worktrees, and nothing else.

G6 PUSH AND TREE — necessarily postdates this commit; reported in the round report.

## Open findings

19 findings open by distinct id in `.agent/live_review.md` after C4: `^- R-\d+ — ` minus
`^Done: R-\d+ — `, same count as before the round (round registered R-1012 at C1b, taking the
open count to 20, then resolved it at C4, returning to 19). `R-1012` is not among the open ids
at C4; it is among them at C1b only.

## Item status

| Item | Status | Reason |
|---|---|---|
| R-0954 (block byte verification) | done | 227 lines, sha256 match |
| Payload byte verification (5 state payloads + diff) | done | all 6 match block's stated lines/sha256 |
| C1a | done | 346 insertions (numstat), no cap breach |
| C1b | done | 97 insertions (numstat) read; block's stated 117 differs — reported per constraint 4, not a stop condition |
| C2 | done | 15 insertions (numstat), matches expected 15 |
| C3 | done | 125 insertions (numstat), matches expected 125 |
| C4 | done | 2 insertions (numstat), matches expected 2 |
| G1 transport and state | done | 20/20 boolean readings True; open-set counts 19/20/19 with R-1012 tracked correctly |
| G2 code transport | done | all seven blob ids and the name-only list match exactly |
| G3 targeted suite | done | 332 passed, exit 0 |
| G4 lint | done | All checks passed!, exit 0 |
| G5 mutation red-proofs | done | control green; (a)/(b)/(c) all red naming the expected tests; byte-identical restoration |
| C5 handoff | done | this file |
| G6 push and tree | done | reported in round report (postdates this commit) |

## Authored-text proofs

The six `.agent/authored/f277-r2-*` files (C1a) were compared disk-to-disk against their source
payloads under `.remedy-wt/f277-r2-payloads/` and all six read byte-equal (G1 reading (a)). No
other reviewer-authored text was applied this round beyond the payloads already covered by G1's
forensics and the code diff covered by G2.

## Deviations & assumptions

- C1b's insertion count: the block's PAYLOADS/Bundle text states "Expected insertions 117 by
  `git show --numstat`". The worker's own `git show --numstat` reading of commit `2de3bb3f`
  (re-checked both with default rename detection and with `--no-renames`, identical both times)
  sums to 97 (65 + 4 + 27 + 1). Constraint 4 states the four expected values are "the reviewer's
  arithmetic; where yours differs, report YOURS and say so, and stop only if yours reaches 500."
  97 is reported here as the worker's own reading; the round was not stopped because 97 is well
  under the 500 cap. No commit content was altered to chase the expected number — `.agent/plan.md`
  was replaced with the exact payload bytes as ordered, and the resulting diff is what `git diff`
  and `git show --numstat` both report.
- No other deviation. Every payload was applied byte-exact (verified pre- and post-commit); the
  code diff was applied via `git apply --include=...` in the two ordered slices and never
  retyped; every gate ran for real with its output captured above.

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk before acting.
2. The review of round 2.
3. Round 3: give `command_discovery_completed` a writer in the discovery path, using the
   metadata keys `memory_learn` already reads (`source_types`, `candidate_count`), per DECISION
   F277 D4's "what the remaining rounds take."

Operator questions open: 1
