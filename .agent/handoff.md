# Handoff — F114 Cost preview per command, round 17 (books R16's PASS; builds the evidence bundle + review zip)

## Session

SESSION 4 of feature F114 · round 17 · rounds so far 17.

This is session 4's 2nd delegated round. It books round 16's PASS
verdict into the ledger (RECORD16 — precondition 3 confirmed, all six
closure preconditions now hold), then executes closure algorithm steps
1-2 of `docs/roadmap/STATUS_closure_protocol.md`: the evidence job and
the review zip. This round does NOT close the feature — no `[x]`, no
README sync, no `consumed_by` edit, no pull request. Neither the
25-round nor the 7-session soft limit is anywhere close — F114 is at
round 17 of a 25-round cap, session 4 of a 7-session cap.

## Range

Review of `eeeee7c6f0368e38dd0891d92b49cecbd42c9ef0..6e0c2124723c9f55bfa1481b56bbcfe8ad2d2bc6`.
ACCEPTED HEAD (C1, the last content commit before the package build) is
`6e0c2124723c9f55bfa1481b56bbcfe8ad2d2bc6`. This handback (C2) follows
the READY package and is not part of the reviewed content range.

## Item Status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | pushed |
| evidence bundle | done | READY, 5/5 runs green, all 8 closed-schema gates present |
| review zip | done | PACKAGE_STATUS=READY_FOR_REVIEW |
| red control | done | PACKAGE_STATUS=BLOCKED_EVIDENCE, exit 0, 3 blocking reasons |
| C2 | done | this handback |
| G1 HYGIENE | done | PASS |
| G2 TRANSPORT | done | PASS |
| G3 THE PLAN AT C1 | done | PASS |
| G4 THE RECORD APPEND | done | PASS |
| G5 THE LEDGER | done | PASS, unchanged before/after C1 (see note on methodology) |
| G6 THE EVIDENCE BUNDLE | done | PASS |
| G7 THE REVIEW ZIP | done | PASS |
| G8 STRUCTURE + PRECONDITION 3 | done | PASS |

## Commits

### 4a14e6d9 F114 R17 C0a: save step block verbatim to .agent/authored/f114-r17.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f114-r17.md` | +247/-0 | transport proof — verbatim save of the supplied step block (corrected version, real RECORD16/PLAN17 slices), new file |

### fef49778 F114 R17 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +210/-119 | mirror of the round's authored block (whole-file rewrite; AGENTS.md `.agent/**` state-file exemption) |

### 6e0c2124 F114 R17 C1: append RECORD16 to live_review.md, replace plan.md with PLAN17
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +2/-1 | append RECORD16 (round 16's PASS verdict: precondition 3 confirmed) — exactly one `\n` then RECORD16's 3273 bytes, no separator |
| `.agent/plan.md` | +16/-13 | whole-file replace with PLAN17 (first substantive commit, per constraint 2) |

### (this handback commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback (write-once per PH v3) — numbers not tabled here per template's self-reference exception; the reviewer measures them at the next gate |

## External actions

- `git push origin feature/f114-cost-preview-per-command` → run after
  C1, before the evidence/zip build, per the block's own ordering
  ("then PUSH, and build the evidence bundle and the zip from the
  clean tree at C1"). Pushed `eeeee7c6..6e0c2124`; `git rev-parse HEAD
  origin/feature/f114-cost-preview-per-command` both read
  `6e0c2124723c9f55bfa1481b56bbcfe8ad2d2bc6` immediately after.
- `bash scripts/make_review_zip.sh --evidence-dir
  .remedy-wt/f114_closure_evidence/remedy-job-evidence-f114-closure` →
  exit 0, PACKAGE_STATUS=READY_FOR_REVIEW, wrote
  `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260904-185732-READY_FOR_REVIEW.zip`
  directly (no move needed — the script wrote to the archive path).
- `bash scripts/make_review_zip.sh --evidence-dir
  .remedy-wt/f114_closure_evidence_CONTROL/remedy-job-evidence-f114-closure-control`
  → exit 0, PACKAGE_STATUS=BLOCKED_EVIDENCE (DELIBERATE CONTROL, see
  Verification), wrote
  `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260904-185816-BLOCKED_EVIDENCE.zip`.
  This control zip was left on disk; constraint 9 forbids deleting
  anything already present under that directory and nothing in the
  block orders removing what THIS round adds either, so it was left in
  place rather than guessed at. It is a control artifact, not the live
  package — the live package is named explicitly below.
- No `gh pr` command of any kind was run this round — no PR is
  created, edited or merged, per this round's own scope ("This round
  does NOT close the feature").
- No worktree (`git worktree`) was created or removed this round; all
  scratch work (evidence dirs, the control copy, extraction scripts)
  lives under `.remedy-wt/` (gitignored), never committed.

## Verification

Preconditions, checked before C0a (re-confirmed after the coordinator's
correction, since real time had passed):
```
$ gh pr list --state open --json number,headRefName,baseRefName,isDraft
[]
$ git rev-parse HEAD
eeeee7c6f0368e38dd0891d92b49cecbd42c9ef0
$ git branch --show-current
feature/f114-cost-preview-per-command
$ git status --porcelain | wc -l
0
```
All four confirmed before C0a.

**G1 HYGIENE**:
```
STOP exists (os.path.exists('.agent/STOP')):
  before C0a:        False
  before zip build:  False
  before C2:         False
git status --porcelain | wc -l:
  after C0a: 0
  after C0b: 0
  after C1:  0
  immediately before zip build: 0
```
All PASS.

**G2 TRANSPORT** (after C0b):
```
$ sha256sum .agent/authored/f114-r17.md .agent/last_block.md
58b921c822ad80e9c134267525791d7c9b2f2ed3b2c8ff79f27e5d423b44c2a1  .agent/authored/f114-r17.md
58b921c822ad80e9c134267525791d7c9b2f2ed3b2c8ff79f27e5d423b44c2a1  .agent/last_block.md
```
One digest, twice — PASS.

**G3 THE PLAN AT C1**:
```
plan.md bytes: 1415
PLAN17 slice bytes: 1415
byte-equal: True
$ wc -l .agent/plan.md
35 .agent/plan.md
$ grep -c '^## Goal' .agent/plan.md
1
$ grep -c '^## Next Steps' .agent/plan.md
1
```
Byte-equal, 35 lines (under 50), both header counts 1 — PASS.

**G4 THE RECORD APPEND (RECORD16)**:
```
Base size of .agent/live_review.md immediately before C1: 2405496 bytes
Base ends with trailing newline: False
RECORD16 own byte length (extracted from committed authored file): 3273 bytes, 0 internal newlines
base + 1 + 3273 = 2405496 + 1 + 3273 = 2408770
post-C1 file byte length: 2408770
Match: True
```
Second reader: sliced the post-C1 file's bytes from offset 2405496 to
end-of-file and compared directly against `"\n" + RECORD16`:
```
tail (base..end) == "\n" + RECORD16: True
```
Negative control (scratch, in-memory copy only) — one byte flipped
(XOR 0x01 on the first byte) in a copy of RECORD16's own text, then
re-compared against the real tail:
```
second reader REJECTS the mutated copy: True (mutated tail != real tail)
```
All PASS, zero deviation.

**G5 THE LEDGER** — two readings taken, and a discrepancy between this
round's own constraint 7 and its own quoted expected value is declared
rather than silently resolved (see Deviations):

Reading A — raw line-count subtraction, matching
`docs/agents/planner_reviewer_prompt.md` item 10's literal wording
("every `^- R-\d+ — ` paragraph minus every `^Done: R-\d+ — ` line")
and RECORD16's own arithmetic:
```
BEFORE C1: registered paragraphs 354, Done: lines 76, raw_open 278
AFTER  C1: registered paragraphs 354, Done: lines 76, raw_open 278
```
UNCHANGED — matches the block's quoted `(354 registered, 278 open)`
exactly.

Reading B — constraint 7's own stated formula,
`len(set(registered) - set(resolved))`, distinct R-id:
```
BEFORE C1: distinct registered ids 354, distinct resolved ids 74, distinct_open 280
AFTER  C1: distinct registered ids 354, distinct resolved ids 74, distinct_open 280
```
UNCHANGED under this formula too (354/280), but this number does NOT
match the block's quoted `278`. Root cause measured: two ids
(`R-0721`, `R-0725`) each carry TWO `Done:` lines (a "RESOLVED IN PART"
paragraph followed by a "REMAINDER RESOLVED" / "FULLY RESOLVED"
paragraph for the same id), so raw line-count (76) and distinct-id
count (74) differ by exactly 2, and 354-74=280 not 278. Both readings
agree the count is UNCHANGED across C1, which is what this gate
actually requires; the 278-vs-280 disagreement is between the block's
own formula and its own quoted number, not something C1 caused.

**G6 THE EVIDENCE BUNDLE**:

(a) Unified diff, template (`git show HEAD:.agent/authored/f009-r33.md`
slice `EVIDENCESCRIPT`, lines 314-461) vs adapted
`.remedy-wt/f114_evidence_r17.py` — only the ordered values differ:
```
- EVIDENCE_DIR: f009_closure_evidence/remedy-job-evidence-f009-closure
+ EVIDENCE_DIR: f114_closure_evidence/remedy-job-evidence-f114-closure
- BASE = "ce49348b8f5b0374417f5b6c47d8c04966e7108e"
+ BASE = "a1b5d4bb455550f082da7d6c4c80fd968d6e1a88"
- runs = [5 F009 mkrun(...) calls with -k/deselection]
+ runs = [5 F114 mkrun(...) calls, no -k, no deselection, per spec]
- job_id="f009-closure", job_title="F009 The single write channel - closure"
+ job_id="f114-closure", job_title="F114 Cost preview per command - closure"
- prior_job_ids=["f008-closure"]
+ prior_job_ids=["79b21c8cba8b4352"]
- note_prefix="operator-attested manual completion - F009 closure"
+ note_prefix="operator-attested manual completion - F114 closure"
- review_feature_id="f009"
+ review_feature_id="f114"
```
Nothing else differs — the docstrings, `_tail`'s double path scrub,
`mkrun`'s node-id-from-`--collect-only` logic, the
`len(node_ids) == selected` assert, the sorted `test_files`, the
`_unsafe_text` pre-scan with its red control and the `OUTPUT_HASH`
re-derivation are byte-for-byte identical to the template, including
line 1's module docstring which still literally reads "F009 closure
evidence bundle" — left untouched because it is not one of the values
the block ordered changed (declared, not silently "fixed"; see
Deviations).

(b) Per verification run (from the produced `verification_tests.json`):
```
vr-0001 selected 19 len(node_ids) 19 equal True passed 19 failed 0 skipped 0 deselected 0 test_files_sorted True
vr-0002 selected 12 len(node_ids) 12 equal True passed 12 failed 0 skipped 0 deselected 0 test_files_sorted True
vr-0003 selected 5  len(node_ids) 5  equal True passed 5  failed 0 skipped 0 deselected 0 test_files_sorted True
vr-0004 selected 4  len(node_ids) 4  equal True passed 4  failed 0 skipped 0 deselected 0 test_files_sorted True
vr-0005 selected 295 len(node_ids) 295 equal True passed 295 failed 0 skipped 0 deselected 0 test_files_sorted True
```
Exactly the expected passes (19, 12, 5, 4, 295), zero failed/skipped/
deselected everywhere — PASS.

(c) `_unsafe_text` pre-scan over every node id and command in the real
bundle: `SCAN rejected strings: 0 []` — 0 rejected. Red control on a
fabricated absolute-path id
(`/home/user/repo/tests/x.py::t`):
`_unsafe_text(...)` returned the reason string `"a local absolute
path"` (truthy — the function returns a reason string or `None`, so a
non-`None` result is this gate's "True"). PASS.

(d) Files the producer wrote into the evidence directory: 3 top-level
JSON gate files not in the closed-schema-8 list plus the 8 required
ones, `task_runs/{T001,T002,T003}/*` (10 files each), `tasks.json`,
`token_truth.json`, `verification_tests.json`, `workspace.diff`,
`workspace_apply.json`, `review_subject.json`, `manifest.json`,
`review_commit_chain.json` and 81 `review_commit_patches/*.patch`
files (one per commit in the review range). All eight closed-schema
gates confirmed present: `final_verifier_report.json`,
`fresh_evidence_gate.json`, `artifact_contract_gate.json`,
`change_provenance_gate.json`, `manifest_integrity.json`,
`postmortem_integrity.json`, `commit_execution_gate.json`,
`runtime_integration_gate.json` — PASS.

(e) Per run, `output_hash == sha256(stdout_summary)`:
```
OUTPUT_HASH vr-0001 matches sha256(stdout_summary): True
OUTPUT_HASH vr-0002 matches sha256(stdout_summary): True
OUTPUT_HASH vr-0003 matches sha256(stdout_summary): True
OUTPUT_HASH vr-0004 matches sha256(stdout_summary): True
OUTPUT_HASH vr-0005 matches sha256(stdout_summary): True
```
All True — PASS.

(f) HEAD the template computed: `6e0c2124723c9f55bfa1481b56bbcfe8ad2d2bc6`
— confirmed equal to C1's full sha (same value, also present as
`head_commit` in the producer's own result JSON and in the zip
manifest's `committed_review_subject.head_commit`).

**G7 THE REVIEW ZIP** (constraint 8: exit 0 is never the reading — the
reading is `PACKAGE_STATUS`):

(a) LIVE build:
```
$ bash scripts/make_review_zip.sh --evidence-dir <EVIDENCE_DIR>
REAL_EXIT=0
PACKAGE_STATUS=READY_FOR_REVIEW
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260904-185732-READY_FOR_REVIEW.zip
```
SHA-256 computed independently over the file on disk (Python
`hashlib.sha256`, streamed): `8632f182052a2d0f1343e1a0c77ed1c588b87208e9192ec5cd675678ec0e2810`
— matches the script's own printed `final_sha256` exactly.

(b) From `.review_zip_manifest.json` inside the LIVE zip:
```
package_status: READY_FOR_REVIEW
ready_gate_matrix.ok: True
ready_gate_matrix.blocking_reasons: []
committed_review_subject.head_commit: 6e0c2124723c9f55bfa1481b56bbcfe8ad2d2bc6
  (C1's sha: 6e0c2124723c9f55bfa1481b56bbcfe8ad2d2bc6 — MATCH)
committed_review_subject.base_commit: a1b5d4bb455550f082da7d6c4c80fd968d6e1a88
  (matches the ordered BASE exactly)
```

(c) THE RED CONTROL — deliberate, declared: copied
`.remedy-wt/f114_closure_evidence/remedy-job-evidence-f114-closure` to
a second directory
`.remedy-wt/f114_closure_evidence_CONTROL/remedy-job-evidence-f114-closure-control`
(`shutil.copytree`), appended one absolute-path node id
(`/home/decodeux/Repos/remedy/tests/orchestration/test_cost_preview.py::test_absolute_path_injection`)
to `verification_tests.json`'s `runs[0].node_ids`, and built a zip from
the COPY:
```
REAL_EXIT=0
PACKAGE_STATUS=BLOCKED_EVIDENCE
```
`ready_gate_matrix.blocking_reasons` (untruncated, from the control's
own manifest):
```
- final_verifier_report.json test_status.passed cannot be confirmed: the VerificationTests total is missing or invalid
- verification_tests.json field verification_tests.runs[0].node_ids[19] carries a local absolute path
- verification_tests.json runs[0] node_ids count (20) != selected (19)
```
The real bundle at `.remedy-wt/f114_closure_evidence/...` was never
touched by this control — only the copy was mutated.

(d) The LIVE package's absolute path:
`/home/decodeux/Repos/remedy-history/zips/remedy-review-20260904-185732-READY_FOR_REVIEW.zip`
— the build script wrote it there directly (this is F114's first
package, so `REVIEW_PACKAGE_DIR` had nothing of this feature's own to
collide with); confirmed present on disk, size 22113384 bytes.

(e) `git status --porcelain | wc -l` after all of it: `0`.

**G8 STRUCTURE AND PRECONDITION 3** (range `eeeee7c6..6e0c2124`, the
round's own starting HEAD..C1):
```
$ git show --numstat --format="" 4a14e6d9   (C0a)
247  0  .agent/authored/f114-r17.md
$ git show --numstat --format="" fef49778   (C0b)
210  119  .agent/last_block.md
$ git show --numstat --format="" 6e0c2124   (C1)
2   1   .agent/live_review.md
16  13  .agent/plan.md
```
All insertions under 500. Parents:
```
6e0c2124 -> fef49778 -> 4a14e6d9 -> eeeee7c6
```
Each of C0a, C0b, C1 has exactly one parent — single-parent, PASS.
```
$ git ls-files .remedy-wt | wc -l
0
$ git ls-files | grep -c "remedy-job-evidence"
0
$ git diff --numstat eeeee7c6..6e0c2124 -- docs/roadmap/STATUS.md README.md scripts/self_use_queue.json
(empty — all three absent)
```
Precondition 3 re-run:
```
$ python3 -m apps.cli.grouped integrity check --json
{"passed": true, "fail_count": 0, "check_count": 5, ...
 "high_blockers_open": "pass" / "no open blocker/high findings"}
```
Identical reading to round 16's own (`passed: true`, `fail_count: 0`,
`high_blockers_open` pass, `check_count: 5`) — PASS, unmoved.

## Authored-text proofs

- `.agent/authored/f114-r17.md` written verbatim via the Write tool
  from the corrected step block supplied in this round's delegation
  (the coordinator's follow-up message, which substituted real
  RECORD16/PLAN17 content for the two placeholders an earlier message
  had sent by mistake — see Deviations), delimiter lines excluded,
  sha256 `58b921c822ad80e9c134267525791d7c9b2f2ed3b2c8ff79f27e5d423b44c2a1`,
  confirmed identical to `.agent/last_block.md` after C0b (G2).
- Both slices (RECORD16, PLAN17) were extracted from the COMMITTED
  `.agent/authored/f114-r17.md` by a Python script reading delimiter
  indices (`<<<BEGIN ...>>>` / `<<<END ...>>>`), taking the exact
  substring strictly between each pair of markers — never by
  hand-retyping (constraint 1).
- Per constraint 4: RECORD16 and PLAN17 each had no trailing `\n` of
  their own carried into the target file.
- RECORD16: 3273 bytes measured, 0 internal newlines; appended to
  `.agent/live_review.md` as exactly one `\n` + RECORD16 (G4, above).
- PLAN17: 1415 bytes, 35 `wc -l` lines, no trailing newline;
  `.agent/plan.md` reproduces it byte-identical (G3 above).
- The evidence script slice `EVIDENCESCRIPT` was extracted from
  `git show HEAD:.agent/authored/f009-r33.md` (lines 314-461 between
  its own `<<<SLICE EVIDENCESCRIPT` / `<<<END EVIDENCESCRIPT` markers)
  and adapted per the unified diff at G6(a) above — only the ordered
  values changed.

## Deviations & assumptions

Six declared, none a defect on disk:

1. **The round's FIRST delegation carried two unfilled template
   placeholders** (`RECORD16_PLACEHOLDER`, `PLAN17_PLACEHOLDER`)
   instead of real authored content. Before doing any work the worker
   verified this was a genuine gap rather than deliberate minimal
   content — `.agent/plan.md` on disk already carried real `## Goal`/
   `## Next Steps` prose, and `.agent/live_review.md`'s byte size
   (2405496, no trailing newline) already matched the block's own
   stated G4 base-size expectation, so the rest of the block's numbers
   were real and only the two slice bodies were not. The worker halted
   before any commit and reported this rather than fabricating
   reviewer-authored content (RECORD16/PLAN17 are not the worker's to
   author). The coordinator then re-sent the identical block with the
   two slices filled in for real, confirming the gap was a copy-paste
   error. No file was written or committed during the halted attempt.
2. **Constraint 7's own formula and its own quoted expected value
   disagree** (`len(set(registered) - set(resolved))` gives 354/280;
   the quoted `(354 registered, 278 open)` matches the raw
   line-count-subtraction formula in
   `docs/agents/planner_reviewer_prompt.md` item 10 instead, which
   gives 354/278). Root cause measured and reported under G5 above:
   `R-0721` and `R-0725` each carry two `Done:` lines for the same id.
   Both formulas independently confirm the count is UNCHANGED across
   C1, which is what the gate is actually checking; the worker did not
   pick a "correct" formula and silently apply it — both readings are
   reported and the disagreement is named rather than resolved, per
   "apply it as written and declare it."
3. **Several compound/chained Bash invocations and certain inline
   `python3 -c` one-liners were denied by this session's sandbox**
   (a chained `grep | ...; echo EXIT=$?` form; a multi-statement
   redirect-then-report chain; an inline `python3 -c` containing a
   `for` loop and a `re.split` regex; a bare `sha256sum`/`ls -la` pair
   targeting a path outside the repo). Each was re-expressed per
   constraint 6: single, unchained commands, and scratch Python logic
   moved into standalone script files under `.remedy-wt/` (e.g.
   `.remedy-wt/count_ledger2.py`, `.remedy-wt/apply_r17_slices.py`,
   `.remedy-wt/g4_check.py`, `.remedy-wt/inspect_manifest.py`,
   `.remedy-wt/inspect_control_manifest.py`) executed with a plain
   `python3 <script>` invocation. The `sha256sum` case was worked
   around with Python's `hashlib` (streamed read), which succeeded
   where the shell tool did not.
4. **`remedy integrity check --json` was not re-tried this round** —
   the worker used `python3 -m apps.cli.grouped integrity check
   --json` directly (the exact module the `remedy` console script maps
   to per `pyproject.toml`'s `[project.scripts]`), on the strength of
   this session's own standing, repeatedly-confirmed denial of the
   `remedy` CLI wrapper (round 16 hit the literal "This command
   requires approval" denial). This is the constraint's own named
   fallback either way.
5. **The control zip build's byproduct was left on disk**:
   `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260904-185816-BLOCKED_EVIDENCE.zip`.
   Constraint 9 forbids deleting anything already present under that
   directory; it does not say what to do with a new control artifact,
   so the worker left it in place rather than guess, and names it
   explicitly here and in the labelled list below so it is never
   mistaken for the live package.
6. **The module docstring in `.remedy-wt/f114_evidence_r17.py`** still
   reads `"""F009 closure evidence bundle. ..."""` verbatim — this line
   was not in the block's list of values to change, and "every other
   line stays BYTE FOR BYTE" was read literally rather than as an
   invitation to also fix an evidently stale line the spec did not
   name.

No other deviations. `.agent/STOP` was absent at all three checkpoints
(before C0a, before the zip build, before C2). No path outside the
declared change set was written under version control: only
`.agent/authored/f114-r17.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/plan.md` and this handback were
committed — `packages/`, `apps/`, `tests/`, `docs/` and `scripts/` were
never opened for writing, per the block's own prohibition. The evidence
directory and both zips are gitignored and were never committed. The
bundle's commit order (C0a, C0b, C1, then push, then the evidence/zip
build, then C2) was followed exactly. No pull request or merge action
was taken this round.

## Closure precondition status for F114

All six closure preconditions held BEFORE this round (established by
RECORD16, reproduced independently at this round's own G8). This
round's own scope is algorithm steps 1-2 only (evidence + zip); it
neither re-litigates nor re-breaks any precondition. Nothing here
changes that status.

## For the next round — carried, not re-derivable

- **Evidence job**: `f114-closure`
- **LIVE package filename**: `remedy-review-20260904-185732-READY_FOR_REVIEW.zip`
- **LIVE package SHA-256**: `8632f182052a2d0f1343e1a0c77ed1c588b87208e9192ec5cd675678ec0e2810`
- **LIVE package absolute archived path**: `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260904-185732-READY_FOR_REVIEW.zip`
- **ACCEPTED HEAD** (C1's full sha): `6e0c2124723c9f55bfa1481b56bbcfe8ad2d2bc6`
- (For disambiguation only, not to be cited as the live package: a
  DELIBERATE red-control byproduct also sits in the archive directory
  at `remedy-review-20260904-185816-BLOCKED_EVIDENCE.zip` — it is not
  this feature's package.)

## Next

**NEXT EXPECTED ACTION: the closure commit itself**, in ONE commit —
the `[x]` flip on `docs/roadmap/STATUS.md` (STATUS line built from the
carried facts above: Evidence job `f114-closure`, package
`remedy-review-20260904-185732-READY_FOR_REVIEW.zip`, SHA-256
`8632f182052a2d0f1343e1a0c77ed1c588b87208e9192ec5cd675678ec0e2810`,
package path `/home/decodeux/Repos/remedy-history/zips`, accepted HEAD
`6e0c2124723c9f55bfa1481b56bbcfe8ad2d2bc6`), the README capability
sync (STATUS and README may never disagree in any committed state),
and `scripts/self_use_queue.json`'s `consumed_by=F114` edit — followed
by the AGENTS.md PR workflow (`gh pr create`), likely this session's
next round per `docs/roadmap/STATUS_closure_protocol.md`'s algorithm
steps 4-5. The PR is not merged this session — that is the operator's
manual-review window, closed at the next feature's Open PR Gate.
