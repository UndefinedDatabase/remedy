# Handoff — F262 List commands v2 (dates, sort, filter), round 27 (books R26's PASS; builds the evidence bundle + review zip)

## Session

SESSION 9 of feature F262 · round 27 · rounds so far 27.

Session 9's delegated round 27 books round 26's PASS (RECORD26 — closure
preconditions 3 and 6 confirmed, all six now hold) and executes closure
algorithm steps 1-2 of `docs/roadmap/STATUS_closure_protocol.md`: the
evidence job `f262-closure` and the fresh review zip with its red
control. This round does NOT close the feature — no `[x]`, no README
sync, no `consumed_by` edit, no pull request. Context self-assessment:
this session started cold at `0609f113` with the round-27 block as its
only brief, read AGENTS.md, the closure protocol's Algorithm 1-2 and zip
sequence and the F114 round-17 handback (`af075516`) first, and executed
the block mechanically — every slice extracted from the COMMITTED
authored file by Python, every gate run with real exit codes, no state
carried from memory. Both soft limits are exceeded (round 27 of 25,
session 9 of 7); the scope report they oblige was carried by rounds
23-24 under DECISION F262 D4/D5 (remainder scoped to F267), and the plan
now holds exactly two steps to the merge.

## Range

Review of `0609f1138171a6e38dbfcd8d15d8a9fb06fade2b..a5896aa6c7e8ebc7616fdef62f5964f6bb9772a0`.
ACCEPTED HEAD (C1, the last content commit before the package build) is
`a5896aa6c7e8ebc7616fdef62f5964f6bb9772a0`. This handback (C2) follows
the READY package and is not part of the reviewed content range.

## For the next round — the carried facts

- **Evidence job**: `f262-closure`
- **LIVE package filename**: `remedy-review-20260905-112903-READY_FOR_REVIEW.zip`
- **LIVE package SHA-256**: `83953f280dd856277529add08212b767e5588370da937ccfad5608923a73295e`
- **LIVE package archived path**: `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260905-112903-READY_FOR_REVIEW.zip` (22992203 bytes)
- **ACCEPTED HEAD** (C1's full sha): `a5896aa6c7e8ebc7616fdef62f5964f6bb9772a0`
- **BASE**: `7c65d9ccfb512aef1c3eea0245030647332c26ea`
- Disambiguation only, NOT the live package: the DELIBERATE red-control
  byproduct `remedy-review-20260905-112938-BLOCKED_EVIDENCE.zip` also
  sits in that directory (see Deviations 4).

## Item Status

| Item | Status | Reason |
|---|---|---|
| C0a | done | primary `shutil.copyfile` transport, digest matched |
| C0b | done | |
| C1 | done | pushed before the build |
| push | done | `0609f113..a5896aa6`, HEAD == origin |
| evidence bundle | done | 7/7 runs green, all 8 closed-schema gates present, HEAD == C1 |
| review zip | done | PACKAGE_STATUS=READY_FOR_REVIEW, exit 0 |
| red control | done | PACKAGE_STATUS=BLOCKED_EVIDENCE, exit 0, 3 blocking reasons — DELIBERATE CONTROL |
| C2 | done | this handback |
| G1 HYGIENE | done | PASS |
| G2 TRANSPORT | done | PASS |
| G3 THE PLAN AT C1 | done | PASS (1681 bytes, 38 lines) |
| G4 THE RECORD APPEND | done | PASS (2503246 + 2 + 4992 = 2508240) |
| G5 THE LEDGER | done | PASS, 356 / 77 / 279 before and after C1 |
| G6 THE EVIDENCE BUNDLE | done | PASS |
| G7 THE REVIEW ZIP | done | PASS |
| G8 STRUCTURE | done | PASS |

## Commits

### fca83123 F262 R27 C0a: save step block verbatim to .agent/authored/f262-r27.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f262-r27.md` | +232/-0 | transport proof — verbatim save of the supplied step block, new file |

### 694a11e1 F262 R27 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +186/-155 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption) |

### a5896aa6 F262 R27 C1: append RECORD26 to live_review.md, replace plan.md with PLAN28
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +3/-1 | append RECORD26 (round 26's PASS: preconditions 3 and 6) — exactly two `\n` then RECORD26's 4992 bytes, no trailing newline |
| `.agent/plan.md` | +18/-21 | whole-file replace with PLAN28 (first substantive commit, per constraint 2) |

### (this handback commit, C2)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once per PH v3) — numbers not tabled here per the template's self-reference exception; the reviewer measures them at the next gate |

## External actions

- `git push -u origin feature/f262-list-commands-v2` after C1, before the
  evidence/zip build (the block's own ordering) → exit 0, pushed
  `0609f113..a5896aa6`; `git rev-parse HEAD origin/feature/f262-list-commands-v2`
  both read `a5896aa6c7e8ebc7616fdef62f5964f6bb9772a0` immediately after.
- `bash scripts/make_review_zip.sh --evidence-dir
  /home/decodeux/Repos/remedy/.remedy-wt/f262_closure_evidence/remedy-job-evidence-f262-closure`
  (run via `subprocess.run(cwd=REPO)`) → REAL_EXIT=0,
  PACKAGE_STATUS=READY_FOR_REVIEW, wrote
  `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260905-112903-READY_FOR_REVIEW.zip`
  directly — the READY zip was ALREADY in the archive directory when the
  build finished; no `shutil.move` was needed or performed.
- `bash scripts/make_review_zip.sh --evidence-dir
  /home/decodeux/Repos/remedy/.remedy-wt/f262_closure_evidence_CONTROL/remedy-job-evidence-f262-closure-control`
  → REAL_EXIT=0, PACKAGE_STATUS=BLOCKED_EVIDENCE (DELIBERATE CONTROL, see
  Verification G7(c)), wrote
  `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260905-112938-BLOCKED_EVIDENCE.zip`,
  left in place (constraint 8 deletes nothing there).
- A second push after C2 (this handback) — recorded in the round report,
  since this file cannot table it.
- No `gh pr` command of any kind, no merge, no worktree add/remove.
  `main` untouched.

## Verification

Preconditions before C0a:
```
$ git rev-parse HEAD
0609f1138171a6e38dbfcd8d15d8a9fb06fade2b
$ git status --porcelain | wc -l
0
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
$ git merge-base main HEAD
7c65d9ccfb512aef1c3eea0245030647332c26ea
```

**G1 HYGIENE**:
```
.agent/STOP:
  before C0a:        absent (ls: No such file or directory)
  before zip build:  absent (os.path.exists -> False)
  before C2:         absent (ls: No such file or directory)
git status --porcelain | wc -l:
  after C0a: 0
  after C0b: 0
  after C1:  0
  immediately before zip build: 0
```
PASS.

**G2 TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f262-r27.md .agent/last_block.md
68536a44a4274bd438ee53e58d2adb26201577e6df2fb62ede978fc4f2b2938f  .agent/authored/f262-r27.md
68536a44a4274bd438ee53e58d2adb26201577e6df2fb62ede978fc4f2b2938f  .agent/last_block.md
$ wc -c .agent/authored/f262-r27.md
18010
```
One digest, twice; equals the reviewer's stated original digest and
byte count. PASS.

**G3 THE PLAN AT C1** (from `.remedy-wt/apply_r27_slices.py` and shell):
```
PLAN28 bytes 1681 trailing newline False
plan.md bytes 1681 equals PLAN28: True sha256 01718eb8e98a76999fecdc6ac08c7eff79ae94c2f3206e50f796bb9668de867b
$ wc -l .agent/plan.md
38
$ grep -c '^## Goal' .agent/plan.md
1
$ grep -c '^## Next Steps' .agent/plan.md
1
```
PASS.

**G4 THE RECORD APPEND (RECORD26)**:
```
RECORD26 bytes 4992 internal newlines 0 trailing newline False
live_review base bytes 2503246 base trailing newline False
expected 2508240 post-C1 bytes 2508240 match True
tail == \n\n + RECORD26: True
negative control (flipped byte) REJECTED: True
$ wc -c .agent/live_review.md
2508240
```
The negative control flipped bit 0 of RECORD26's first byte in an
in-memory copy and re-compared against the real tail — rejected. PASS.

**G5 THE LEDGER** (canonical line-count formula, §3 item 10):
```
BEFORE C1: grep -c '^- R-[0-9]* — '    356 ; grep -c '^Done: R-[0-9]* — '  77 ; open 279
AFTER  C1: grep -c '^- R-[0-9]* — '    356 ; grep -c '^Done: R-[0-9]* — '  77 ; open 279
```
UNCHANGED at 356 / 77 / 279. PASS.

**G6 THE EVIDENCE BUNDLE**:

(a) Unified diff (difflib, n=0), template slice EVIDENCESCRIPT from
`git show HEAD:.agent/authored/f009-r33.md` (lines 314-461) vs
`.remedy-wt/f262_evidence_r27.py` — every changed line:
```
@@ -11 +11 @@
-    REPO, ".remedy-wt", "f009_closure_evidence", "remedy-job-evidence-f009-closure"
+    REPO, ".remedy-wt", "f262_closure_evidence", "remedy-job-evidence-f262-closure"
@@ -13 +13 @@
-BASE = "ce49348b8f5b0374417f5b6c47d8c04966e7108e"
+BASE = "7c65d9ccfb512aef1c3eea0245030647332c26ea"
@@ -93,5 +93,7 @@
-    mkrun("vr-0001", "tests/ui_server/test_command_channel.py", 99, "not escape", 1),
-    mkrun("vr-0002", "tests/ui_server/test_command_dispatch.py", 4),
-    mkrun("vr-0003", "tests/orchestration/test_command_nonce.py", 27, "not escape", 1),
-    mkrun("vr-0004", "tests/orchestration/test_command_audit.py", 16, "not escape", 1),
-    mkrun("vr-0005", "tests/orchestration/test_secure_fs.py", 11),
+    mkrun("vr-0001", "tests/orchestration/test_list_options.py", 11),
+    mkrun("vr-0002", "tests/test_command_catalog.py::TestListCommandOptions", 3),
+    mkrun("vr-0003", "tests/cli/test_config_cmd.py", 16),
+    mkrun("vr-0004", "tests/cli/test_worker_facade_cmd.py", 70),
+    mkrun("vr-0005", "tests/cli/test_managed_builder_execution_cli.py", 12),
+    mkrun("vr-0006", "tests/cli/test_queue_cmd.py", 28),
+    mkrun("vr-0007", "tests/docs/test_docs_consistency.py", 295),
@@ -124,2 +126,2 @@
-    job_id="f009-closure",
-    job_title="F009 The single write channel - closure",
+    job_id="f262-closure",
+    job_title="F262 List commands v2 (dates, sort, filter) - closure",
@@ -127 +129 @@
-    prior_job_ids=["f008-closure"],
+    prior_job_ids=["f114-closure"],
@@ -132,2 +134,2 @@
-    note_prefix="operator-attested manual completion - F009 closure",
-    review_feature_id="f009",
+    note_prefix="operator-attested manual completion - F262 closure",
+    review_feature_id="f262",
```
`step_range="T001-T003"` and `num_tasks=3` already matched the template
and are unchanged. Nothing else differs (see Deviations 2 for the
untouched line-1 docstring).

(b)+(e) Per verification run (from the produced `verification_tests.json`):
```
vr-0001 selected 11  len(node_ids) 11  equal True passed 11  failed 0 skipped 0 deselected 0 test_files_sorted True output_hash==sha256(stdout_summary) True
vr-0002 selected 3   len(node_ids) 3   equal True passed 3   failed 0 skipped 0 deselected 0 test_files_sorted True output_hash==sha256(stdout_summary) True
vr-0003 selected 16  len(node_ids) 16  equal True passed 16  failed 0 skipped 0 deselected 0 test_files_sorted True output_hash==sha256(stdout_summary) True
vr-0004 selected 70  len(node_ids) 70  equal True passed 70  failed 0 skipped 0 deselected 0 test_files_sorted True output_hash==sha256(stdout_summary) True
vr-0005 selected 12  len(node_ids) 12  equal True passed 12  failed 0 skipped 0 deselected 0 test_files_sorted True output_hash==sha256(stdout_summary) True
vr-0006 selected 28  len(node_ids) 28  equal True passed 28  failed 0 skipped 0 deselected 0 test_files_sorted True output_hash==sha256(stdout_summary) True
vr-0007 selected 295 len(node_ids) 295 equal True passed 295 failed 0 skipped 0 deselected 0 test_files_sorted True output_hash==sha256(stdout_summary) True
```
Exactly the expected passes 11, 3, 16, 70, 12, 28, 295; zero failed/
skipped/deselected everywhere. Evidence script REAL_EXIT=0. PASS.

(c) `_unsafe_text` pre-scan (script output):
```
SCAN rejected strings: 0 []
SCAN red control: a local absolute path
```
0 rejected; the fabricated `/home/user/repo/tests/x.py::t` returned the
non-empty reason `a local absolute path`. PASS.

(d) Files the producer wrote under
`.remedy-wt/f262_closure_evidence/remedy-job-evidence-f262-closure`: 225
files — 25 top-level (`artifact_contract_gate.json`,
`change_provenance_gate.json`, `commit_execution_gate.json`,
`context_strategy.json`, `current_change_content_proof.json`,
`execution_config.json`, `final_job_review.json`,
`final_verifier_report.json`, `fresh_evidence_gate.json`,
`job_report.json`, `job_timeline.json`, `manifest.json`,
`manifest_integrity.json`, `postmortem_integrity.json`,
`prompt_trace_summary.json`, `review_commit_chain.json`,
`review_subject.json`, `runtime_integration_gate.json`,
`scratch_file_guard.json`, `target_guard.json`, `tasks.json`,
`token_truth.json`, `verification_tests.json`, `workspace.diff`,
`workspace_apply.json`), 167 `review_commit_patches/*.patch` (one per
commit in BASE..HEAD, `commit_count` 167) and 33 files under
`task_runs/{T001,T002,T003}/`. All eight closed-schema gates present:
```
gate final_verifier_report.json present: True
gate fresh_evidence_gate.json present: True
gate artifact_contract_gate.json present: True
gate change_provenance_gate.json present: True
gate manifest_integrity.json present: True
gate postmortem_integrity.json present: True
gate commit_execution_gate.json present: True
gate runtime_integration_gate.json present: True
all eight present: True
```
PASS.

(f) HEAD the template computed: `a5896aa6c7e8ebc7616fdef62f5964f6bb9772a0`
(the producer's result JSON `head_commit`, and every run's `head_sha`)
— equals C1's full sha. Producer verdict `PASS_WITH_RISKS`,
`total_passed` 435, `authority_count` 48. PASS.

**G7 THE REVIEW ZIP** (constraint 7: the reading is PACKAGE_STATUS, never
the exit code):

(a) LIVE build:
```
REAL_EXIT=0
PACKAGE_STATUS=READY_FOR_REVIEW
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260905-112903-READY_FOR_REVIEW.zip
sha256 (hashlib, streamed, over the file on disk): 83953f280dd856277529add08212b767e5588370da937ccfad5608923a73295e
```
Matches the script's printed `final_sha256` exactly.

(b) From `.review_zip_manifest.json` inside the LIVE zip:
```
package_status: READY_FOR_REVIEW
ready_gate_matrix.ok: True
ready_gate_matrix.blocking_reasons: []
committed_review_subject.head_commit: a5896aa6c7e8ebc7616fdef62f5964f6bb9772a0
  (C1's sha: a5896aa6c7e8ebc7616fdef62f5964f6bb9772a0 — MATCH)
committed_review_subject.base_commit: 7c65d9ccfb512aef1c3eea0245030647332c26ea
  (equals the ordered BASE)
```

(c) THE RED CONTROL — a DELIBERATE CONTROL, in plain words: the real
evidence directory was copied (`shutil.copytree`) to
`.remedy-wt/f262_closure_evidence_CONTROL/remedy-job-evidence-f262-closure-control`;
in the COPY ONLY, one node id carrying an absolute path
(`/home/decodeux/Repos/remedy/tests/orchestration/test_list_options.py::test_absolute_path_injection`)
was appended to `verification_tests.json` `runs[0].node_ids` (11 -> 12,
selected still 11), and a zip was built from that copy:
```
CONTROL REAL_EXIT=0
PACKAGE_STATUS=BLOCKED_EVIDENCE
CONTROL ZIP: /home/decodeux/Repos/remedy-history/zips/remedy-review-20260905-112938-BLOCKED_EVIDENCE.zip (22992497 bytes)
ready_gate_matrix.ok: False
ready_gate_matrix.blocking_reasons (untruncated, 3):
  - final_verifier_report.json test_status.passed cannot be confirmed: the VerificationTests total is missing or invalid
  - verification_tests.json field verification_tests.runs[0].node_ids[11] carries a local absolute path
  - verification_tests.json runs[0] node_ids count (12) != selected (11)
```
The control package is NOT evidence about the real bundle; the two zips
were built from DIFFERENT inputs (the real directory and a deliberately
mutated copy), so their differing statuses are not non-determinism —
the misreading DECISION F262 D6 names from the F114 closure. The real
bundle was never touched: after the mutation, the real
`verification_tests.json` still holds 11 ids in `runs[0]` and does not
contain the fabricated id (`fake id in real bundle: False`).

(d) The LIVE package's absolute path:
`/home/decodeux/Repos/remedy-history/zips/remedy-review-20260905-112903-READY_FOR_REVIEW.zip`
— written there directly by the build script (`REVIEW_PACKAGE_DIR`);
exists: True; size 22992203 bytes.

(e) `git status --porcelain | wc -l` after all of it: `0`.

**G8 STRUCTURE**:
```
$ git show --numstat --format="" fca83123   (C0a)
232  0    .agent/authored/f262-r27.md
$ git show --numstat --format="" 694a11e1   (C0b)
186  155  .agent/last_block.md
$ git show --numstat --format="" a5896aa6   (C1)
3    1    .agent/live_review.md
18   21   .agent/plan.md
$ git log --format='%h parents=%p' 0609f113..a5896aa6
a5896aa6 parents=694a11e1
694a11e1 parents=fca83123
fca83123 parents=0609f113
$ git ls-files .remedy-wt | wc -l
0
$ git ls-files | grep -c remedy-job-evidence
0
$ git diff --numstat 0609f113..a5896aa6 -- docs/roadmap/STATUS.md README.md scripts/self_use_queue.json
(empty)
$ git diff --stat 0609f113..a5896aa6 -- packages/ apps/ tests/ docs/ scripts/
(empty)
```
Every cell matches the Commits tables above; each commit single-parent,
all insertions under 500.
```
$ python3 -m apps.cli.grouped integrity check --json   (cwd=REPO)
REAL_EXIT=0
passed: True fail_count: 0 check_count: 5
high_blockers_open: {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
```
The round-26 reading, unchanged. PASS.

## Authored-text proofs

- `.agent/authored/f262-r27.md` was written by the PRIMARY transport
  route — `shutil.copyfile` from the reviewer's scratch original
  `/tmp/claude-1000/-home-decodeux-Repos-remedy/62969f5d-578f-413a-8775-0dee473d35ff/scratchpad/f262-r27.block.md`
  — and measured sha256
  `68536a44a4274bd438ee53e58d2adb26201577e6df2fb62ede978fc4f2b2938f`
  over 18010 bytes, equal to the reviewer's stated digest and count; the
  Write-tool fallback was not needed. `.agent/last_block.md` was
  produced from the committed authored file by `shutil.copyfile` and
  measures the same digest (G2).
- RECORD26 (4992 bytes, 0 internal newlines, no trailing newline) and
  PLAN28 (1681 bytes, no trailing newline) were extracted from the
  COMMITTED blob `git show HEAD:.agent/authored/f262-r27.md` by
  `.remedy-wt/apply_r27_slices.py`, as the bytes strictly between each
  slice's one-line `<<<BEGIN ...>>>` / `<<<END ...>>>` markers (each
  marker asserted unique), never retyped (constraint 1).
- RECORD26 was appended as exactly `\n\n` + slice (constraint 3); PLAN28
  replaced `.agent/plan.md` whole; disk-to-slice equality and the
  flipped-byte control are at G3/G4.
- EVIDENCESCRIPT was extracted from the committed blob
  `git show HEAD:.agent/authored/f009-r33.md` between its `<<<SLICE
  EVIDENCESCRIPT` / `<<<END EVIDENCESCRIPT` marker lines by
  `.remedy-wt/adapt_r27_evidence.py` (the unmodified extraction is kept
  at `.remedy-wt/evidencescript_template.py`), then only the ordered
  values were substituted, each by a uniqueness-asserted replacement;
  the complete unified diff is at G6(a).

## Deviations & assumptions

Five declared, none a defect on disk, none a departure from the ordered
commit sequence (C0a, C0b, C1, push, evidence, zip, control, C2 — followed
exactly):

1. **One `cd` prefix.** The G8 structure command was issued as
   `cd /home/decodeux/Repos/remedy 2>/dev/null; git -C ... ` — every
   sub-command also carried its own absolute `-C` path, the `cd` was
   not refused, and it read only; nothing on disk changed. The block's
   "never `cd`" instruction was nonetheless not honoured on that one
   compound, so it is declared (the same class round 26 declared).
2. **The module docstring of `.remedy-wt/f262_evidence_r27.py`** still
   reads `"""F009 closure evidence bundle. ..."""` verbatim — not one of
   the values the block ordered changed, and "every other line stays
   BYTE FOR BYTE" was read literally (as the F114 R17 round also did).
3. **Sandbox re-expressions — pre-emptive, no refusal occurred.** No
   bash form was refused this round; the forms the block names as
   refusable were expressed in Python from the start: the evidence
   script, both zip builds and the integrity check were driven from
   `python3 - <<'PY'` heredocs / `.remedy-wt/*.py` scripts via
   `subprocess.run([...], cwd=REPO)` (so no `cd`, no env assignment);
   the evidence copy for the control was `shutil.copytree`; the zip
   SHA-256 values were `hashlib.sha256` streamed over the files on
   disk (also cross-checked against the script's printed
   `final_sha256`); exit codes were read from `CompletedProcess.returncode`
   and printed as `REAL_EXIT=`. `git commit` messages were passed via
   `-F <scratch file>` (printf-built) to carry the two trailer lines.
4. **The control zip's byproduct was left on disk**:
   `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260905-112938-BLOCKED_EVIDENCE.zip`.
   Constraint 8 forbids deleting anything under that directory and the
   block does not order removing what this round adds, so it stays, and
   is named here so it is never mistaken for the live package.
5. **`job_title` wrapping.** The block prints the title across two
   lines (`"F262 List commands v2 (dates,` / `sort, filter) - closure"`)
   for line-width; it was applied as the single string
   `"F262 List commands v2 (dates, sort, filter) - closure"` (one space
   at the wrap), as the visible line break is prose formatting and a
   string literal cannot span lines in the template.

`.agent/STOP` was absent at all three reads. No path outside the change
set was written under version control: only `.agent/authored/f262-r27.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` and
this handback. `packages/`, `apps/`, `tests/`, `scripts/` and `docs/`
were never opened for writing. The evidence directories and both zips
are gitignored and were never committed (`git ls-files .remedy-wt` 0,
tracked `remedy-job-evidence` 0). No pull request, no merge, `main`
untouched.

## Next

**NEXT EXPECTED ACTION: the closure commit (STATUS line, README sync,
consumed_by=F262) and the pull request** — in ONE commit the
reviewer-authored `[x]` STATUS line carrying Evidence job
`f262-closure`, package `remedy-review-20260905-112903-READY_FOR_REVIEW.zip`,
SHA-256 `83953f280dd856277529add08212b767e5588370da937ccfad5608923a73295e`,
archived path `/home/decodeux/Repos/remedy-history/zips`, accepted HEAD
`a5896aa6c7e8ebc7616fdef62f5964f6bb9772a0`; the README numerals and
F262 capability paragraph; `consumed_by=F262` on SU-009 — then
`gh pr create`, and the merge under the operator's 2026-09-05
authorization once hosted CI reads green.
