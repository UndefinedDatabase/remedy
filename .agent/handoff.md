# Handback — F286, round 3: the closure sequence's evidence round

## Session

SESSION 1 of feature F286 · round 3 · rounds so far 3. This session ran round 3 only: verified the
block and every payload byte-exact, copied the block and payloads (C1), booked round 2's PASS verdict
and the round-3 plan (C2, the ACCEPTED HEAD), pushed, then ran the closure protocol's algorithm steps
1 and 2 — the evidence job (A1) and the review package build (A2) — both from the clean, pushed C2
tree, and rewrote this handoff (C3). Context self-assessment: a comfortable margin remained through
the whole round; every payload, hash and numstat matched its expected reading on the first try, both
A1 and A2 exited 0 on the first attempt, and the work was not near its limit.

For the operator, in plain words: this round closed the loop on F286's round 2 — booking its PASS
verdict into the permanent record — then built the two artifacts the closing round's STATUS line will
quote: the evidence bundle (job `f286r3e1001`, PASS_WITH_RISKS, 557 of 557 collected tests passed) and
the review package (`READY_FOR_REVIEW`, archived outside the repo). Nothing was merged and nothing was
closed. The booking of round 3, the ledger rotation, the next findings paydown, the STATUS line and
the pull request are the closure's remaining round.

## Range

Review of 6a8773eba..HEAD

## Commits

### 0d1da2742 F286 R3 C1: copy round 3 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f286-r3-block.md | +147/-0 | verbatim copy of this round's block |
| .agent/authored/f286-r3-booking.diff | +10/-0 | verbatim copy of the booking.diff payload |
| .agent/authored/f286-r3-create_f286_evidence.py | +146/-0 | verbatim copy of the create_f286_evidence.py payload (the A1 tool) |
| .agent/authored/f286-r3-plan.md | +24/-0 | verbatim copy of the plan payload |

Measured insertions: 327 (147 + 10 + 146 + 24), matching the block's expectation "this block's line
count plus 180" (147 + 180 = 327) exactly. Under the 500-line cap.

### b7c09100b F286 R3 C2: book round 2's PASS with the closure suite — ACCEPTED HEAD
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | round 2's gate entry (VERDICT PASS) appended, via `booking.diff` |
| .agent/plan.md | +4/-8 | rewritten to round 3's plan (`plan.md` payload) |

Measured: 2/0, 4/8 — matching the block's expected table exactly, per file. `git apply --check` on
`booking.diff` exited 0 before the real `git apply`, which also exited 0. This commit's full SHA,
`b7c09100bbb53ad92eec714a06181ab1e9b76ebe`, is this closure's ACCEPTED HEAD, per the block. Pushed
immediately after this commit, before A1.

### (no commit — A1, the evidence job, run at C2)
`bash -c 'python3 .remedy-wt/f286-r3-payloads/create_f286_evidence.py > .remedy-wt/f286-r3-worker/evidence.log 2>&1; echo "REAL_EXIT=$?"'`
— REAL_EXIT=0. Writes only to the gitignored `.remedy-wt/f286-r3-evidence/`; no tracked file changed,
so no commit and no changed-files table entry apply. Full readings under Verification/G3 below.

### (no commit — A2, the review package, run at C2)
`bash -c 'bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f286-r3-evidence > .remedy-wt/f286-r3-worker/zip.log 2>&1; echo "REAL_EXIT=$?"'`
— REAL_EXIT=0. Writes only to `/home/decodeux/Repos/remedy-history/zips/` (outside the repo); no
tracked file changed, so no commit and no changed-files table entry apply. Full readings under
Verification/G4 below.

### (this commit) F286 R3 C3: rewrite handoff for round 3 with the evidence and package readings
| Path | Reason |
|---|---|
| .agent/handoff.md | rewritten per the template (self-reference exception, R-0149 pattern) |

## External actions

- `git push -u origin feature/f286-findings-paydown-v5` — run immediately after C2 (before A1); real
  outcome: `6a8773eba..b7c09100b  feature/f286-findings-paydown-v5 -> feature/f286-findings-paydown-v5`,
  tracking set up.
- `git push` after C3 — its real outcome is reported in the reply (this file cannot contain it, per
  the block).
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push, no
  `git stash`, no worktree added or removed this round.

## Verification

**G1 TRANSPORT**

Payload readings against the PAYLOADS table (all matched before use):

| file | lines | bytes | sha256 match |
|---|---|---|---|
| booking.diff | 10 | 5278 | match |
| create_f286_evidence.py | 146 | 6957 | match |
| plan.md | 24 | 686 | match |

Block self-verification (BEFORE ANYTHING ELSE step 3): lines 147 (expected 147), bytes 11422
(expected 11422), sha256 matched exactly. No difference found.

Committed-copy-vs-source, read back with `git show <C1>:<path>`, byte for byte:
```
0d1da2742 .agent/authored/f286-r3-block.md                == .remedy-wt/f286-r3/block.md                              -> True
0d1da2742 .agent/authored/f286-r3-booking.diff             == .remedy-wt/f286-r3-payloads/booking.diff                 -> True
0d1da2742 .agent/authored/f286-r3-create_f286_evidence.py  == .remedy-wt/f286-r3-payloads/create_f286_evidence.py      -> True
0d1da2742 .agent/authored/f286-r3-plan.md                  == .remedy-wt/f286-r3-payloads/plan.md                      -> True
```

**G2 THE BOOKING**

Records hashes, read with `git show <C2>:<path>`, against the block's table:

| path | bytes | sha256 match |
|---|---|---|
| .agent/live_review.md | 324089 | match |
| .agent/plan.md | 686 | match |

`open_finding_ids` and `latest_gate_verdict` (from `scripts/rotate_live_review.py`) over
`.agent/live_review.md`'s text at C2 (`b7c09100b`): `[]` and `PASS` — matching the block exactly.

Serially at C2: `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py`,
tail:
```
........................................................................ [ 97%]
.........                                                                [100%]
369 passed in 58.30s
```
REAL_EXIT=0 — matching the block's stated reviewer reading of `369 passed, exit 0` exactly.

**G3 THE BUNDLE, at A1**

Tool real exit code: 0. Log (`.remedy-wt/f286-r3-worker/evidence.log`), lines up to the summary:
```
head b7c09100bbb53ad92eec714a06181ab1e9b76ebe
ancestry-path count 12
plain count 12
collected node ids 557, deselected 2
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 557, 'failed': 0, 'skipped': 0}, output_hash 0c9882f0b998f2d0a3ece44c0b5c8acead3f6f8ce176404e25adedcbafbdf051
validate_verification_tests problems [] passed 557
is_valid_current_run True
validation_errors []
gates written: ['artifact_contract_gate.json', 'change_provenance_gate.json', 'commit_execution_gate.json', 'fresh_evidence_gate.json', 'runtime_integration_gate.json', 'final_verifier_report.json']
```
Ancestry-path count and plain count: both 12, equal — one more than the reviewer's dry-run reading of
11, exactly as the block predicts "for C1" (this round's C1 commit is the one extra commit on top of
the reviewer's dry tree, which carried C2 but no C1). Collected 557 node ids, 2 deselected — matches
the reviewer's dry run. Red control: 0 unsafe among the real ids, planted id answered "a local
absolute path" — matches. pytest exit 0, 557 passed / 0 failed / 0 skipped — matches the reviewer's
"557 passed and 0 skipped". `output_hash`: `0c9882f0b998f2d0a3ece44c0b5c8acead3f6f8ce176404e25adedcbafbdf051`.
`validate_verification_tests` problem list: `[]` (EMPTY, matching). `is_valid_current_run`: `True`,
`validation_errors`: `[]` — matching "no validation error". Gate files the evidence directory holds
(as the tool itself reports writing): `artifact_contract_gate.json`, `change_provenance_gate.json`,
`commit_execution_gate.json`, `fresh_evidence_gate.json`, `runtime_integration_gate.json`,
`final_verifier_report.json`.

**G4 THE PACKAGE, at A2**

Script real exit code: 0. Log (`.remedy-wt/f286-r3-worker/zip.log`) tail:
```
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
PACKAGING_CWD=/home/decodeux/Repos/remedy
EVIDENCE_DIR=.remedy-wt/f286-r3-evidence
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260929-044850-READY_FOR_REVIEW.zip
```
`PACKAGE_STATUS`: `READY_FOR_REVIEW` (the reading, not the exit code). `EVIDENCE_AUTHORITATIVE`:
`true`. Package filename: `remedy-review-20260929-044850-READY_FOR_REVIEW.zip`. Re-hashed independently
(`hashlib.sha256` over the file's bytes): `13311e03d7335e6ad49adc91a0d961e3bc832026dce35fa57fb173c5eddd3d9a`
— matches the script's own reported `final_sha256`. Archived directory:
`/home/decodeux/Repos/remedy-history/zips`.

`committed_review_subject`, read from `.review_zip_manifest.json` INSIDE the package (via
`zipfile.ZipFile`): `base_commit` = `6ba1f4be8600c2f9ad451dab6816c2839b6401bc` (equal to the fork
point the block names), `head_commit` = `b7c09100bbb53ad92eec714a06181ab1e9b76ebe` (equal to C2's full
SHA, the accepted head). `base_is_ancestor`: `true`. `commit_count`: 12. `file_count`: 24.

`zipfile.is_zipfile(path)`: `True`. `zf.testzip()`: `None`.

**G5 THE TREE, after A2**

`python3 -m apps.cli.main integrity check --json`, REAL_EXIT=0:
```
check_count: 6, fail_count: 0, ok: true, passed: true
handler_import          -> pass  (handlers=169)
live_review_verdict     -> pass  (last Gate verdict PASS)
plan_consistency        -> pass  (unchecked=0, context_complete=False)
relevant_untracked      -> pass  (untracked=0, relevant=0)
repo_root_hygiene       -> pass  (no reviewer scratch, evidence dir or archive at the root)
high_blockers_open      -> pass  (no open blocker/high findings)
```
`git status --porcelain`: empty. `git worktree list | wc -l`: 64.

## Authored-text proofs

Every reviewer-authored text applied this round, disk-to-disk against the committed
`.agent/authored/` file:
- `.agent/authored/f286-r3-block.md` (C1) == `.remedy-wt/f286-r3/block.md`: byte-identical.
- `.agent/authored/f286-r3-booking.diff` (C1) == `.remedy-wt/f286-r3-payloads/booking.diff`:
  byte-identical.
- `.agent/authored/f286-r3-create_f286_evidence.py` (C1) == `.remedy-wt/f286-r3-payloads/create_f286_evidence.py`:
  byte-identical.
- `.agent/authored/f286-r3-plan.md` (C1) == `.remedy-wt/f286-r3-payloads/plan.md`: byte-identical.

`.agent/plan.md` was rewritten from the same verified `plan.md` payload via `shutil.copyfile` (C2);
`booking.diff` was applied via `git apply` only (C2), never retyped or edited.
`create_f286_evidence.py` was run only via `python3 <path>` from the payload directory (A1), never
edited or retyped.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | ACCEPTED HEAD `b7c09100bbb53ad92eec714a06181ab1e9b76ebe`; pushed |
| A1 | done | evidence job `f286r3e1001`, exit 0, PASS_WITH_RISKS, 557/557 passed |
| A2 | done | review package exit 0, `READY_FOR_REVIEW`, archived outside the repo |
| C3 | done | this commit |
| G1 | done | all payload, block and transport reads matched exactly |
| G2 | done | booking hashes matched; open set `[]`/PASS; targeted suite 369 passed at exit 0 |
| G3 | done | evidence job exit 0; ancestry/plain 12=12 (one more than dry run, for C1); 557/2 collected; red controls clean; pytest 557 passed at exit 0; validators clean |
| G4 | done | package `READY_FOR_REVIEW`, `EVIDENCE_AUTHORITATIVE=true`, manifest base/head match fork point and accepted head, zip integrity clean |
| G5 | done | integrity check all-pass at fail_count 0; tree clean; 64 worktrees |
| G6 | done | reported in the final reply per the block (post-push, post-C3 readings) |

## Deviations & assumptions

1. **No deviation from the bundle order**: C1, C2, A1, A2, C3 ran in the block's exact order; A1 and
   A2 are actions committing nothing, exactly as the block frames them, so neither carries a commit or
   a changed-files table entry — matching the pattern the block's own predecessor round (S, in round
   2) established.
2. **Environment note, not a deviation**: an early inline heredoc (`python3 - <<'PY' ... PY`)
   containing a dict literal with quotes next to braces was rejected by the sandbox as "Contains brace
   with quote character (expansion obfuscation)" before any file was touched. Every script after that
   point was written to a file under `.remedy-wt/f286-r3-worker/` and run with `python3 <path>`,
   exactly as the block's own THIS SANDBOX REFUSES SHAPES section anticipates; no payload, gate or
   commit was affected.
3. **Transcription note, not a block error**: while manually copying the PAYLOADS and G2 hash tables
   into a verification command, one hash was mistyped with an extra trailing character; re-reading the
   block file directly with `grep` confirmed the block's own text matches the measured hashes exactly
   in all cases. No block content was wrong; the error was in an intermediate typed copy that was
   never used to gate a decision.
4. No forbidden path was touched; the reviewer's directories (`.remedy-wt/f286-r3-payloads/`,
   `.remedy-wt/f286-r3/`, `.remedy-wt/f286-r3-sim/`, `.remedy-wt/f286-r3-dryev/`,
   `.remedy-wt/f286-r3-dryzip/`) were read-only throughout; no full suite was run (amend0917 rule 1 /
   constraint 8 honored — round 2's `57b3c5af` run stands); no `gh pr create` or `gh pr merge`; no
   STATUS or README edit; no ledger rotation; no queue edit; no self-use run; no worktree, branch or
   stash was added, removed or altered this round.

## Next

Per the block's `## Next` order: Phase 1 rule 1. Then the review of round 3. Then the closing round —
the booking of round 3, the ledger rotation, the next findings paydown registered, the STATUS line
with the README counters in the same commit, and the pull request. Open-findings count (as
`open_finding_ids` reads it at C2): 0. Operator questions open: 1.
