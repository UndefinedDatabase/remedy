# Handback — F278 Durable writes & loud failures · Round 11 · Book round 10's PASS, resolve R-1039, build the evidence bundle and the review package

## Session

SESSION 2 of feature F278 · round 11 · rounds so far 11

This round is the closure sequence's evidence half. It copied the round's
block and two payloads into `.agent/authored/` (C1); booked round 10's PASS
and resolved R-1039 into `.agent/live_review.md` (byte concatenation) and
rewrote `.agent/plan.md` (C2); built the evidence job against the fork
point `9817a927` through C2's accepted head `77773f76` (A1, action, no
commit) — job id `f278r11e1001`, 168 node ids over six test files, 168
passed / 0 failed, all eight closed-schema gates present and problem-free,
both `validate_verification_tests` and `validate_evidence_candidate`
returning empty problem lists, and the RED CONTROL reading both ways; built
the fresh review package (A2, action, no commit) with `make_review_zip.sh`,
which read `PACKAGE_STATUS=READY_FOR_REVIEW` on the first build, no
work-around needed; and now writes this handback (C3). All of G1-G5 ran
and matched the block's stated expectations exactly. Context
self-assessment: a comfortable majority of the working budget remains at
handback.

## Range

Review of `4d9ae208`..`HEAD`.

## Commits

### d69c3b2c F278 R11 C1: copy round 11 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f278-r11-block.md | +186/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f278-r11-ledger.md | +4/-0 | Payload copy: round 10's `Gate:` entry + R-1039's `Done:` paragraph |
| .agent/authored/f278-r11-plan.md | +27/-0 | Payload copy: the plan.md rewrite |

Measured insertions: 217 (186+4+27), under the 500 cap.

### 77773f76 F278 R11 C2: book round 10's PASS and resolve R-1039
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | `ledger.md` appended by strict byte concatenation onto the `4d9ae208` bytes |
| .agent/plan.md | +9/-13 | Rewritten to the round-11 plan.md payload |

Measured insertions: 13 (4+9), deletions: 13, all from the plan.md rewrite.
C2 is this closure's ACCEPTED HEAD: `77773f76ac1a640e4345574a2918468743e94730`.

### C3 (this commit) F278 R11 C3: rewrite handoff for round 11 with the evidence and package readings
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per docs/agents/handback_template.md |

## External actions

- `git push origin feature/f278-durable-writes-loud-failures` — after C2: `4d9ae208..77773f76 feature/f278-durable-writes-loud-failures -> feature/f278-durable-writes-loud-failures`, real exit 0, branch tracking set up.
- `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f278-r11-evidence` — real exit 0. `PACKAGE_STATUS=READY_FOR_REVIEW`.
- `git push origin feature/f278-durable-writes-loud-failures` (after C3) — see the session's final reply for the real outcome; it runs after this commit.
- No `gh pr create`, no `gh pr merge`, no force-push, no `git stash`, no checkout of another branch or commit in the primary checkout: none run, per the block's constraints.
- The two pre-existing job worktrees/branches (`.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831`) were left untouched throughout, per constraint 6.
- The evidence directory `.remedy-wt/f278-r11-evidence/` was built and left on disk (gitignored, never committed).

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `No such file or directory`, absent (proceed).
- `git status --porcelain` → empty. `git branch --show-current` → `feature/f278-durable-writes-loud-failures`. `git log --oneline -1` → `4d9ae208 F278 R10 C4: record the repaired suite transcript and rewrite handoff for round 10`.
- Block bytes (R-0954): measured line count (newline count)=186, sha256=`39e75524581db8dfaec40d7dad0b897202d8c86fc1a6c5803492cbb3f0b4d3e8`; matches both given readings exactly (bytes=12791).
- `git stash list` first line (before C1) → `stash@{0}: WIP on (no branch): 365051fa F277 R17 C3: rewrite handoff for round 17 with the rebuilt package readings`. `git worktree list` (before C1) → primary checkout + `.remedy-wt/job-129b3ad7206d4f8d` + `.remedy-wt/job-e7268925db3a4831`.

PAYLOADS — both measured and matched the block's table exactly: ledger.md (lines=4, bytes=3665, sha256=`7eb163090aaa06d2fbe5e8dd6d7d1c85ff33b14911546d3c505d656268290531`), plan.md (lines=27, bytes=1028, sha256=`a8830135c0725acb70cff0fac8dc9cea5090530ee951a411f51f0f0b52049ca4`).

G1 TRANSPORT — every `.agent/authored/f278-r11-*` copy (plus the block copy) read back with `git show d69c3b2c:<path>` and compared byte-for-byte against its source: all 3 copies matched exactly (block.md, ledger.md, plan.md), sha256 identical on both sides in every case.

G2 THE BOOKING — at C2 (`77773f76`):
- `.agent/live_review.md`: bytes=463142, sha256=`b8740a871c74b59fe9b4ce9b1c20a0b2826ef86a54614d815f8495a253ffb5cb` — MATCH to the block's stated reading exactly.
- `.agent/plan.md`: sha256 `a8830135c0725acb70cff0fac8dc9cea5090530ee951a411f51f0f0b52049ca4` — sha256-equal to plan.md payload; line count 27, under 50.
- Line-anchored counts on the C2 text: `^Gate: F278 R10 — ` 1, `^Done: R-1039 — ` 1 — both match.
- Open-finding-id set via `open_finding_ids` (`scripts/rotate_live_review.py`): at `4d9ae208` count=27; at C2 (`77773f76`) count=26; REMOVED=`['R-1039']`; ADDED=`[]` — matching the block's 27/26, REMOVED exactly `R-1039`, ADDED none.

G3 THE BUNDLE — at A1: ancestry-path count `git rev-list --count --ancestry-path 9817a927..77773f76` = 74; plain count `git rev-list --count 9817a927..77773f76` = 74; EQUAL (consistent with the reviewer's 72 read two commits before C2, plus C1 and C2). Evidence job id `f278r11e1001`, head_commit `77773f76ac1a640e4345574a2918468743e94730` (== C2's accepted head). Gate set: all 8 closed-schema gates present and problem-free under `_gate_closed_schema_problems` — `final_verifier_report.json`, `fresh_evidence_gate.json`, `artifact_contract_gate.json`, `change_provenance_gate.json`, `runtime_integration_gate.json`, `manifest_integrity.json`, `postmortem_integrity.json`, `commit_execution_gate.json`, each `[]`. `validate_verification_tests(verification_tests.json)` → problems=`[]`, passed_total=168. `validate_evidence_candidate(evidence_dir)` → `is_valid_current_run: True`, `validation_errors: []`. Verification run: `run_id=vr-1039` (matches `^vr-\d{4,}$`), `exit_code=0`, `passed=168`, `selected=168`, `len(node_ids)=168`, sorted `test_files` = the six named files exactly, `output_hash=4035c028413561b6ab3dc9dd34a22b65bfccd73c65682bd2ead5444372af3e9e`. RED CONTROL: `_unsafe_text` over all 168 real node ids → every answer `None` (ALL_NONE=True); over the planted id `tests/x.py::test_a[/home/someone/secret]` → `'a local absolute path'`. Both readings as required.

G4 THE PACKAGE — at A2: `PACKAGE_STATUS=READY_FOR_REVIEW`, `EVIDENCE_AUTHORITATIVE=true`. Package filename `remedy-review-20260923-030723-READY_FOR_REVIEW.zip`, SHA-256 `6dd87e83b40530115ebc046825f71dddaf99cb85a25c0f529278d14196d6c65c` (28846582 bytes). `committed_review_subject`: base=`9817a927b5fd41d7867195a51e8a7113ce26ae98`, head=`77773f76ac1a640e4345574a2918468743e94730` (== C2's sha), commit_count=74, file_count=187, tombstones=[]. Zip import check: `zipfile.is_zipfile()` → True, `testzip()` → None (no bad member). Archived directory: `/home/decodeux/Repos/remedy-history/zips` (absolute; the script writes directly there, not left elsewhere).

G5 THE TREE — `python3 -m apps.cli.main integrity check --json` → `passed: true`, `fail_count: 0`, all 5 checks `pass` (`handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `high_blockers_open`). `git status --porcelain` → empty. `git worktree list` → primary checkout + `.remedy-wt/job-129b3ad7206d4f8d` + `.remedy-wt/job-e7268925db3a4831`, unchanged.

G6 TREE AND PUSH — reported in the session's final reply, not this file, since it runs after this commit (C3). The handback cannot contain readings that postdate its own write.

## Authored-text proofs

Fidelity protocol (docs/agents/split_workflow.md, R-0147/R-0144/R-0148): byte-identity proof = mechanical disk-to-disk comparison of the applied location against the `.agent/authored/` copy.

- This block (`f278-r11-block.md`): `.agent/authored/f278-r11-block.md` at C1 verified byte-identical to `.remedy-wt/f278-r11-block.md` (G1) and to the two readings given in the delegation message.
- `ledger.md` (append): `.agent/live_review.md` at C2 sha256 `b8740a871c74b59fe9b4ce9b1c20a0b2826ef86a54614d815f8495a253ffb5cb` == payload sha256 concatenated onto the `4d9ae208` bytes (G2). MATCH.
- `plan.md` (rewrite): `.agent/plan.md` at C2 sha256 `a8830135c0725acb70cff0fac8dc9cea5090530ee951a411f51f0f0b52049ca4` == payload sha256 exactly (G2). MATCH.
- A1's evidence job and A2's review package are worker-generated (from the F283 template, adapted per the block), not reviewer-authored payloads; no authored-text fidelity claim applies to either.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| A1 | done | job id f278r11e1001, 168 passed, all 8 gates problem-free, both validators empty, red control both ways |
| A2 | done | PACKAGE_STATUS=READY_FOR_REVIEW on first build, no work-around |
| C3 | done | |
| G1 TRANSPORT | done | |
| G2 THE BOOKING | done | |
| G3 THE BUNDLE | done | ancestry counts equal (74/74), gate set complete, both validations empty, red control both ways |
| G4 THE PACKAGE | done | READY_FOR_REVIEW, zip valid, committed_review_subject head == C2 |
| G5 THE TREE | done | integrity passed, tree clean, worktrees unchanged |
| G6 TREE AND PUSH | done | reported in the session's final chat reply, not this file |

## Deviations & assumptions

The round followed the block's ordered commit/action sequence (C1, C2, A1,
A2, C3) exactly and touched exactly the tracked path set constraint 3
names (verified via `git diff --name-only 4d9ae208 HEAD` before C3: 5
paths, all within the allowed set; C3 adds exactly the one more path the
block orders — `.agent/handoff.md`). No procedural deviations from the
block's ordered steps.

One environment note, not a scope deviation: multi-step Python logic
(hashing, byte concatenation, the adapted evidence script, the gate/
validator/red-control checks) was written to files under
`.remedy-wt/f278-r11-scratch/` and run with `python3 <file>` or here-doc
`python3 -` invocations, per the block's own guidance that the sandbox
refuses chained shell one-liners.

The evidence directory `.remedy-wt/f278-r11-evidence/` and the review
package under `/home/decodeux/Repos/remedy-history/zips/` are outside the
review subject and were never committed, per constraint 3. Nothing was
merged and nothing was closed this round, per constraint 5.

`.remedy-wt/job-129b3ad7206d4f8d` and `.remedy-wt/job-e7268925db3a4831`
(both pre-existing before this round) are left in place untouched, per
constraint 6. No other deviation.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round
11, then the closure sequence's last round as `.agent/plan.md` lists it —
the ledger rotation, the STATUS line with the README counters and the
self-use item's `consumed_by` in one commit, and the pull request, which is
never merged in the session that opens it. Open findings: 26. Operator
questions: 0.
