Round f052-r4 — CLOSURE per docs/roadmap/STATUS_closure_protocol.md
(v4). Read that file COMPLETELY before starting; it wins over this
summary on any detail. Save this block to .agent/last_block.md first
(OUTCOME: pending → executed at handback). Verify each authored
text's sha256 BEFORE use. f052-r4-3 is ONE 208-char line and WILL
arrive hard-wrapped: rejoin the fragments with a single space,
re-hash, use only after the hash matches (known recoverable class,
3rd instance). Never merge anything this round.

STEP 1 — COMMIT A (persist R3 verdict)
Save the four authored texts below to .agent/authored/<name>.md.
In .agent/live_review.md:
- replace the R3 Steps bullet ("- R3: ... In progress.") with the
  BODY of f052-r4-1.md;
- append the BODY of f052-r4-2.md to "## Verdicts" after the R2
  entry.
cmp proofs. Commit .agent/live_review.md, .agent/authored/
f052-r4-*.md, .agent/last_block.md as:
chore(f052): persist R3 verdict (PASS)
Push. Record this commit's FULL sha — it is the expected accepted
HEAD (the zip manifest must confirm it).

STEP 2 — PRECONDITIONS (abort closure on any failure)
python3 -m apps.cli.grouped integrity check --json → must PASS with
fail_count 0 (record the raw JSON summary). git status --porcelain
empty. git push; git rev-list --left-right --count @{u}...HEAD →
"0 0". R-0159 is Low → not a blocker (documented risk).

STEP 3 — EVIDENCE JOB
packages.orchestration.job_evidence.create_manual_completion_bundle(
review_feature_id="f052", ...), fresh job id, base commit FULL sha
c0a3b34ad3951cf1d195c39a7a3aff32ba4068d8, head = commit A. Four REAL
verification runs, executed now, exit codes recorded:
  pytest tests/orchestration/test_self_healing_cycles.py -q  (50)
  pytest tests/cli/test_golden_path.py -q                    (42)
  pytest tests/docs/ -q                                     (293)
  (plus any run the producer requires)
Producer pitfalls — ALL cumulative lessons apply: node_ids from
--collect-only with len(node_ids) == selected per run; test_files
are FILES, never directories (expand tests/docs/); output_hash =
sha256 of the EXACT stored stdout_summary bytes (pre-truncate to the
producer window and let the producer derive the hash — F050/F051
lesson); full-length base_commit; gate set = the full closed schema
(final_verifier, fresh_evidence, artifact_contract,
change_provenance, manifest_integrity, postmortem_integrity,
commit_execution, runtime_integration). Record job id + total
passed.

STEP 4 — READY ZIP (from the clean tree, BEFORE any evidence commit)
bash scripts/make_review_zip.sh --evidence-dir <path>  (or --job-id)
Requirements: PACKAGE_STATUS=READY_FOR_REVIEW,
EVIDENCE_AUTHORITATIVE=true, validation_errors empty,
committed_review_subject spans
c0a3b34ad3951cf1d195c39a7a3aff32ba4068d8..<commit A>, base_is_
ancestor true, ZipFile.testzip() → None. Record filename + SHA-256
(script JSON + independent sha256sum). accepted HEAD := the
manifest's committed_review_subject.head_commit — must equal commit
A. A failing zip build is a closure BLOCKER: record the raw error in
the handback and STOP (no [x], no further commits except handback).

STEP 5 — EVIDENCE COMMIT (only after the READY zip exists)
git add -f the evidence export dir; commit:
chore(f052): commit closure evidence (after READY zip)

STEP 6 — FINAL COMMIT (exactly STATUS.md + README.md + .agent/)
Substitute in a COPY of f052-r4-3.md (each placeholder exactly once;
grep -c 1→0 each; original file untouched): <JOB_ID> from step 3,
<ZIP_FILENAME> + <ZIP_SHA256> from the script JSON (independent
sha256sum must agree), <HEAD_SHA> = the manifest head_commit.
Replace the unique STATUS.md line "- [~] F052 — Self-healing test
rounds" with the substituted line (old 1→0, new 1 after; cmp of the
grepped line against the substituted copy → 0). Apply the three
README edits from f052-r4-4.md exactly as written (each FROM 1
before/0 after, each TO present after; the R-0151 count pin makes
STATUS+README land in this SAME commit by construction).
Provenance table per substituted value in the handback. Rewrite
.agent/handoff.md per the template + flip OUTCOME to executed.
Post-edit gates, raw tails: pytest tests/docs/ -q (must be 293,
exit 0 — the count pin now checks 28==28) and pytest
tests/cli/test_golden_path.py -q (42). grep -c '^- \[x\]'
docs/roadmap/STATUS.md → 28. Commit:
chore(f052): close F052 — STATUS [x] + README sync
Push.

STEP 7 — PR (NOT merged)
gh pr create --base main --title "F052 — Self-healing test rounds
(T001–T002)" — body per AGENTS.md: what/why, DECISION D1, changed-
files table, verdicts R1–R3, open findings: 1 (R-0159, Low,
documented), runtime actuals (observed; tokens/cost not-measured
unless the ledger has them), evidence job + package + SHA-256.
The PR merges at the NEXT feature's start via the Open PR Gate.
Report the PR number in the handback. Done — await the reviewer.

--- BEGIN f052-r4-1 sha256=e5909491774e623f16538547b204434d668da66bdf28254298de79ad2f9b9d1e ---
- R3: persist R2 verdict; register R-0158 + R-0159; fix R-0158
  (integration_gate.md path correction); closure stays its own
  round. Done.
- R4: closure per docs/roadmap/STATUS_closure_protocol.md v4:
  preconditions, evidence job, READY zip, evidence commit, then ONE
  final commit = STATUS [x] + README sync + final .agent state.
  In progress.
--- END f052-r4-1 ---

--- BEGIN f052-r4-2 sha256=11ae30109473b2241ca0d923c2402e5f0418ed4d8050c58dee24aa81475e2142 ---
- R3: PASS (reviewer, 2026-07-31). Range d410ce5..7262f5b. All 5
  authored texts verified against the recorded BEGIN digests by the
  reviewer's own sha256sum recompute (the reviewer scratchpad died
  between rounds — the digest fallback per project practice, not a
  worker fault); registrations and the R-0158 resolution applied
  byte-exact, Done sha f9dadc0 confirmed against the real doc diff.
  integration_gate.md paragraph replacement verified: parity
  targets corrected to apps/ui/node_modules + apps/ui/dist, ROOT
  node_modules named a .vite cache, non-restorable .git-directory
  class folded into the attribution rule. R-0159 deliberately Open
  (documented Low). Reviewer's own gates: tests/docs 293, canary
  42. Closure preconditions met: latest verdict PASS, all findings
  Resolved or documented risk, Built State current, tree clean.
  LAST_REVIEWED_SHA = 7262f5b.
--- END f052-r4-2 ---

--- BEGIN f052-r4-3 sha256=41ccf661801fe161526987590dd0130a1b7a9b9af235eb2e1858314e5f3671e6 ---
- [x] F052 — Self-healing test rounds (T001–T002 complete; accepted 2026-07-31 · live review PASS — ACCEPTED · Evidence job <JOB_ID> · package <ZIP_FILENAME> · SHA-256 <ZIP_SHA256> · accepted HEAD <HEAD_SHA>)
--- END f052-r4-3 ---

--- BEGIN f052-r4-4 sha256=21d715683e3943f00b6a04beceffac0fd7e06c7a49a79f728dcfba46456b2e42 ---
EDIT 1 — replace this exact line:
27 of 252 registered items accepted. Next: F052 (Self-healing test rounds).
with:
28 of 252 registered items accepted. Next: F053 (Final & interim report).
EDIT 2 — replace this exact line:
| 1 | Self-Build Bootstrap | 11 | 22 |
with:
| 1 | Self-Build Bootstrap | 12 | 22 |
EDIT 3 — replace this exact line:
F050 DAG scheduling, F051 escalate instead of block.
with these two lines:
F050 DAG scheduling, F051 escalate instead of block,
F052 self-healing test rounds.
--- END f052-r4-4 ---

OUTCOME: pending
