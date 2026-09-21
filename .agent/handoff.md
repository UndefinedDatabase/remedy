# Handoff — F277 Machine contracts: event vocabulary, JSON envelope, exit codes · Round 16

## Session

SESSION 7 of feature F277 · round 16 · rounds so far 16

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE.

**SCOPE REPORT (required by amend0827 rule 6 at the 7-session soft limit).** Unchanged in
substance since round 12. *Finished:* T001, the event vocabulary, and T002, the JSON envelope
with its dispatch error boundary. *Missing:* T003 is partly applied — `fail()` exists and nine
of the twenty-eight CLI modules call it. T004 is not started. *The proposal, already carried
out:* DECISION F277 D10 closes F277 on T001 and T002 complete and T003 in part; the remainder
is registered as F283, directly after F277. The operator question it owes is
`.agent/operator_questions.md` Q2. **New this round: THE CLOSURE IS BLOCKED.** The evidence
bundle built clean and the package did NOT: it is **`BLOCKED_EVIDENCE`**, on one validator
error, reported below verbatim and NOT retried, exactly as the block ordered.

Context self-assessment: before any edit I read `AGENTS.md`, `docs/agents/handback_template.md`,
`.remedy-wt/f277-r16-block.md` and `docs/roadmap/STATUS_closure_protocol.md` in full, then all
three payloads. Because this round calls a producer rather than patching a file, I also read
`packages/orchestration/job_evidence.py` `create_manual_completion_bundle`, the run-record
normaliser `packages/orchestration/manual_attestation.py` `_vt_run_v11`, the feature-binding
selector in `packages/orchestration/runtime_integration_gate.py`, and the VerificationTests
validator in `scripts/build_review_manifest.py`, so that every field of the one verification
record was chosen against the contract that reads it rather than guessed.

## Range

Review of `b10e9bf1`..`HEAD`.

## Commits

### 3d269bdb F277 R16 C1a: copy round 16 payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f277-r16-block.md | +231/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f277-r16-ledger.md | +2/-0 | byte-for-byte copy of the ledger.md payload |
| .agent/authored/f277-r16-plan.md | +45/-0 | byte-for-byte copy of the plan.md payload |
| .agent/authored/f277-r16-slips.md | +1/-0 | byte-for-byte copy of the slips.md payload |

Measured insertions (`git show --numstat`): **279**. Expected: 48 payload lines plus the
measured block line count of 231, which is 279. They **MATCH**. I ran the ordered cap
arithmetic BEFORE committing: `500 − 48 − 231 =` **221**, non-negative, so the commit was legal
and needed no oversize declaration. This feature's one permitted declaration stays spent where
round 12 spent it.

### 9dbd8e6d F277 R16 C1b: book round 15's PASS and the reviewer's worktree slip
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | append the ledger.md payload: the round 15 `Gate:` entry, VERDICT PASS |
| .agent/plan.md | +22/-22 | rewrite to the plan.md payload, byte-identical, 45 lines |
| .agent/prose_slips.md | +1/-0 | append the slips.md payload's single line |

Measured insertions (`git show --numstat`): **25**. The block expected **25**, and each
per-file number also matches the block's own breakdown, including the plan rewrite's diff
insertions of 22.

A NOTE ON A SECOND, LOUDER NUMBER, so nobody has to re-derive it: `git commit` printed
`3 files changed, 48 insertions(+), 45 deletions(-)` for this commit, because its own summary
applied rewrite detection to `.agent/plan.md` (`rewrite .agent/plan.md (66%)`) and counted the
file as 45 deleted plus 45 added. `git show --numstat`, which is the reading the block names
and the reading every size rule in this repository uses, reads 22/22 for that file and **25**
insertions for the commit. Both numbers are real; only the second one is the contract's.

### C2 — THE EVIDENCE JOB AND THE REVIEW ZIP (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot table the
commit that writes it. **C2's tracked change set is the handback and nothing else**, which is
what the block ordered: neither the evidence dir nor the zip is committed. Every artifact this
round produced — the driver script, the four logs, the evidence dir itself — lives under the
gitignored `.remedy-wt/f277-r16-scratch/`, so no evidence file entered the `base..HEAD` review
subject.

## External actions

- `git push -u origin feature/f277-machine-contracts` after C1b — outcome
  `b10e9bf1..9dbd8e6d  feature/f277-machine-contracts -> feature/f277-machine-contracts`,
  real exit code **0**.
- `bash scripts/make_review_zip.sh --evidence-dir
  /home/decodeux/Repos/remedy/.remedy-wt/f277-r16-scratch/remedy-job-evidence-f277-r16` —
  real exit code **0**, package **BLOCKED_EVIDENCE**. Full output in G5. **One attempt only**;
  the block forbids a second.
- `git push -u origin feature/f277-machine-contracts` after C2 runs as the round's last act;
  see deviation 2 for why its own transcript cannot live inside the file it pushes.
- No `gh` command was run. No PR was created, edited or merged. **No worktree was added or
  removed this round** — the evidence job and the package both run in the primary checkout, and
  the three `remedy/job-*` worktrees were left alone.

## Verification

### Pre-flight

- `ls .agent/STOP`: `No such file or directory`. There is no STOP on disk.
- `git status --porcelain`: empty (0 lines).
- `git branch --show-current`: `feature/f277-machine-contracts`.
- `git rev-parse HEAD`: `b10e9bf1ab732594e8ff92aac090ef45e8df4744`, matching `b10e9bf1`.
- Block self-verification (R-0954), `.remedy-wt/f277-r16-block.md`:

| reading | measured | given in the delegation message | equal |
|---|---|---|---|
| line count | 231 | 231 | True |
| sha256 | `b3348ad1615ef344d94abbd4ef7e9718362fa1281a20fa17f4b0a2e23b382d95` | `b3348ad1615ef344d94abbd4ef7e9718362fa1281a20fa17f4b0a2e23b382d95` | True |

Neither reading differs, so the round went ahead. The block file is 15016 bytes and ends in a
newline (231 newline bytes for 231 `splitlines()` lines).

### G1(a) — PAYLOADS transport, nine readings

| file | lines measured / given | bytes measured / given | sha256 measured (given identical) | equal |
|---|---|---|---|---|
| ledger.md | 2 / 2 | 5658 / 5658 | `4666506d04d5788e3edcfef7a793adb8ca2148498226145c6b47fc01bbc5e0ea` | True |
| plan.md | 45 / 45 | 2253 / 2253 | `c3a28ba36cd4d552d55f0958b21046e7eb0438c7f846267b3310f91b933c413d` | True |
| slips.md | 1 / 1 | 1296 / 1296 | `e2546b3de13ec43f705ffc2ae3945d0e1b99f30e59acc10fb5107e1ca0b7fc8f` | True |

**All nine readings equal: True.** Total payload lines **48**. I also confirmed the two append
payloads carry the separator shape the block declares: `ledger.md` begins with a newline
(`True`) and `slips.md` does not (`False`). Nothing was written into
`.remedy-wt/f277-r16-payloads/`.

### G1(b) — the four `.agent/authored/f277-r16-*` copies against their sources

Copied with `shutil.copyfile`, then compared byte-for-byte against the originals:

| copy | source | bytes | sha256 | identical |
|---|---|---|---|---|
| f277-r16-block.md | `.remedy-wt/f277-r16-block.md` | 15016 | `b3348ad1615ef344…` | True |
| f277-r16-ledger.md | `.remedy-wt/f277-r16-payloads/ledger.md` | 5658 | `4666506d04d5788e…` | True |
| f277-r16-plan.md | `.remedy-wt/f277-r16-payloads/plan.md` | 2253 | `c3a28ba36cd4d552…` | True |
| f277-r16-slips.md | `.remedy-wt/f277-r16-payloads/slips.md` | 1296 | `e2546b3de13ec43f…` | True |

**Copies compared: 4. All True.** The chain makes no claim about the bytes emitted into the
worker's prompt, which this workflow cannot measure.

### G1(c) — the two appends at C1b

Byte arithmetic by strict CONCATENATION, not by length. The pre bytes were read back out of
`b10e9bf1` with `git show`, not from the working tree, so the baseline is the commit's:

| file | pre measured | pre, reviewer's | payload | post measured | post, reviewer's | pre+payload == post |
|---|---|---|---|---|---|---|
| .agent/live_review.md | 473511 | 473511 | 5658 | 479169 | 479169 | True |
| .agent/prose_slips.md | 353613 | 353613 | 1296 | 354909 | 354909 | True |

All four of my numbers equal the reviewer's four.

**Negative control**, on `.agent/live_review.md` only. I flipped one bit at byte offset 2829
INSIDE the appended paragraph, on an in-memory copy; the committed file was never mutated:

```
negative control: byte index 2829 flipped, concat_equal=False
```

The strict reader returns **False** on a payload that differs by a single bit at unchanged
length, so the gate is carried in its strict form and not as a length comparison.

### G1(d) — the plan rewrite at C1b

| reading | value |
|---|---|
| payload sha256 | `c3a28ba36cd4d552d55f0958b21046e7eb0438c7f846267b3310f91b933c413d` |
| committed `.agent/plan.md` sha256 | `c3a28ba36cd4d552d55f0958b21046e7eb0438c7f846267b3310f91b933c413d` |
| byte equal | True |
| line count | 45 (under the AGENTS.md 50-line rule: True) |

### G1(e) — open set by distinct id in `.agent/live_review.md`

Computed with the repository's OWN canonical reader rather than a hand-rolled regex: I loaded
`scripts/rotate_live_review.py` and called its `open_finding_ids`, which is the same function
`packages/orchestration/integrity_gate.py` loads by path (R-0648 is the finding that says a
re-implemented parser drifts). Its definition is the set difference
`{^- R-\d{4} — }` minus `{^Done: R-\d{4} — }`, by DISTINCT id.

| rev | OPEN by distinct id |
|---|---|
| b10e9bf1 | **22** |
| C1b `9dbd8e6d` | **22** |

Ids added by round 16: **none**. Ids resolved by round 16: **none**. The two sets are not merely
equal in size, they are the same 22 ids: R-0499, R-0622, R-0662, R-0819, R-0820, R-0829,
R-0866, R-0880, R-0892, R-0950, R-0984, R-0998, R-0999, R-1000, R-1004, R-1005, R-1007, R-1008,
R-1009, R-1014, R-1015, R-1016.

### G2 — THE BASE IS THE FORK POINT

Both counts re-run by me at my own tip `9dbd8e6d`, and again a second time from inside the
driver script immediately before it called the producer:

| command | count |
|---|---|
| `git rev-list --ancestry-path f2494c0216b33d5f261195789ec9f7a300de5fca..HEAD` | **89** |
| `git rev-list f2494c0216b33d5f261195789ec9f7a300de5fca..HEAD` | **89** |

**They are EQUAL**, so the base is the fork point and no commit is silently dropped from the
packaged chain. The reviewer measured 87 and 87 at `b10e9bf1`; my tip carries C1a and C1b on
top of that, so 89 is 87 plus exactly this round's two commits. The driver script raises
`SystemExit` on a disagreement rather than packaging, and it did not raise. Independent
confirmation from the package itself: the manifest's `review_subject_alignment` is **PASS** and
the bundle summary's `commit_count` is **89**, the same number — pitfall (e) is clean, and it is
NOT the cause of the blocked package.

### G3 — THE VERIFICATION RECORD IS SELF-CONSISTENT

One driver script, `.remedy-wt/f277-r16-scratch/run_evidence.py`, real exit code **0**. It
DERIVES every number: node ids from `--collect-only`, passed/failed/skipped from the real run,
and it asserts the consistency itself and exits non-zero rather than packaging an inconsistent
record. No number below was transcribed from the block.

Collect: `python3 -m pytest -q -p no:cacheprovider --collect-only <5 files>`, real exit code
**0**, summary line `105 tests collected`.

Run: `python3 -m pytest -q -p no:cacheprovider <5 files>`, real exit code **0**, summary line
`105 passed in 138.29s (0:02:18)`.

| reading | mine | the reviewer's dry run |
|---|---|---|
| collect count | **105** | 105 |
| `len(node_ids)` | **105** | — |
| `passed` | **105** | 105 |
| `failed` | **0** | 0 |
| `skipped` | **0** | — |
| `exit_code` | **0** | 0 |
| `len(test_files)` | **5** | — |
| run summary line | `105 passed in 138.29s (0:02:18)` | `105 passed in 143.90s` |

The assertion the script evaluated, printed by the script itself:

```
ASSERT len(node_ids) == passed+failed+skipped -> True
```

Every `test_files` entry is a FILE by `os.path.isfile`, all five **true**:

```
{"tests/cli/test_golden_path.py": true,
 "tests/cli/test_json_envelope.py": true,
 "tests/cli/test_memory_cmd.py": true,
 "tests/orchestration/test_event_names.py": true,
 "tests/ui_contracts/test_humanize_catalog.py": true}
```

No directory entry (pitfall b), `run_id` is `vr-0001` and matches `^vr-\d{4,}$` (pitfall c), the
node-id list is the SCOPED selection and never the full suite (pitfall d), and `base_commit` was
passed at full length (the producer pitfall the protocol names).

### G4 — THE EVIDENCE BUNDLE

`packages.orchestration.job_evidence.create_manual_completion_bundle` returned, in full:

```json
{
 "authority_count": 42,
 "commit_count": 89,
 "head_commit": "9dbd8e6dfe2a30ae5805896028166659d80fa7f8",
 "job_id": "f2771600aabbccdd",
 "manual_completion": true,
 "operator_attested_tasks": ["T001", "T002", "T003"],
 "partition": {"T001": 14, "T002": 14, "T003": 14},
 "total_passed": 105,
 "verdict": "PASS_WITH_RISKS"
}
```

- Evidence dir, absolute:
  `/home/decodeux/Repos/remedy/.remedy-wt/f277-r16-scratch/remedy-job-evidence-f277-r16`
- `token_truth.json` is a file in it: **True**
- The final verdict the summary carries: **`PASS_WITH_RISKS`**
- `review_feature_id="f277"` was passed, so the runtime gate ran the generic pipeline checks
  only. There are no `f277_`-prefixed entries in `TEST_EXECUTION_BINDINGS`, so the feature
  selection bound zero test-execution checks — and the gate came back **PASS**.

**The evidence job itself is a success.** It ran to completion, it is internally consistent, its
final verifier is reproducible over its own bytes, and the producer's own determinism check
(`build_final_verifier_report` twice, compared) did not raise. The block's step 1 is done.

### G5 — THE PACKAGE: BLOCKED_EVIDENCE, A CLOSURE BLOCKER

`git status --porcelain` **immediately before the build: empty (0 lines)**, at the pushed head
`9dbd8e6d`. The package was NOT built from a dirty tree.

Command and full output, real exit code **0** (the script exits 0 even when the package is not
commit-ready — the exit code is not the verdict here, the status is):

```
$ bash scripts/make_review_zip.sh --evidence-dir /home/decodeux/Repos/remedy/.remedy-wt/f277-r16-scratch/remedy-job-evidence-f277-r16
UNCHANGED: runtime_integration_gate.json — rebuilt from source; identical to existing
Evidence refresh completed for staged copy.
Observability index generated from staged bytes: evidence/current/self_run_observability_index.json
WARNING: Evidence validation failed (is_valid_current_run=false).
Zip will be built anyway — reviewer will see validation status in manifest.
{"member_count": 4964, "authoritative_count": 42, "symlink_count": 0, "tombstone_count": 0,
 "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20260921-025659-BLOCKED_EVIDENCE.zip",
 "final_sha256": "8245d4a790ecd9a5342e0511bc5d5253c3a5f0ffd38c266a60df0a1030b5b8fb",
 "publication_capability": "SUPPORTED", "package_status": "BLOCKED_EVIDENCE",
 "evidence_authoritative": false, "review_subject_alignment": "PASS",
 "manifest_sha256": "a8f38da5ed18f55437e2e58993d11103784b979e955e8c669e164205336610e0"}

============================================
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=BLOCKED_EVIDENCE
PACKAGING_CWD=/home/decodeux/Repos/remedy
EVIDENCE_DIR=/home/decodeux/Repos/remedy/.remedy-wt/f277-r16-scratch/remedy-job-evidence-f277-r16
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=false
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260921-025659-BLOCKED_EVIDENCE.zip
DO_NOT_COMMIT=true
============================================

*** ZIP CREATED, BUT THIS PACKAGE IS NOT COMMIT-READY ***

27M     /home/decodeux/Repos/remedy-history/zips/remedy-review-20260921-025659-BLOCKED_EVIDENCE.zip
Included files: 4964
Branch: feature/f277-machine-contracts
Commit: 9dbd8e6dfe2a30ae5805896028166659d80fa7f8
```

**The three things DECISION amend0827 D1 and the closure protocol require in the record:**

| field | value |
|---|---|
| package FILENAME | `remedy-review-20260921-025659-BLOCKED_EVIDENCE.zip` |
| SHA-256 | `8245d4a790ecd9a5342e0511bc5d5253c3a5f0ffd38c266a60df0a1030b5b8fb` |
| archived path (absolute directory) | `/home/decodeux/Repos/remedy-history/zips` |

The sandbox did NOT refuse the write, so the record carries the real directory and not
`NOT ARCHIVED`. **Package STATUS as the filename carries it: `BLOCKED_EVIDENCE`.**

**THE RAW ERROR.** I did not retry and I do not offer a repair — the block routes the diagnosis
to the reviewer's next round. I read the blocking reasons out of the package's own
`.review_zip_manifest.json` (a read of the artifact just built, not a second build). Verbatim:

```json
"ready_gate_matrix": {
  "ok": false,
  "blocking_reasons": [
    "final_verifier_report.json test_status.passed cannot be confirmed: the VerificationTests total is missing or invalid",
    "verification_tests.json runs[0] test_files is not sorted"
  ],
  "gate_verdicts": {
    "artifact_contract_gate.json": "PASS",
    "change_provenance_gate.json": "PASS",
    "commit_execution_gate.json": "NEEDS_HUMAN_APPROVAL",
    "final_verifier_report.json": "PASS_WITH_RISKS",
    "fresh_evidence_gate.json": "PASS",
    "manifest_integrity.json": "ok=true",
    "postmortem_integrity.json": "ok=true",
    "runtime_integration_gate.json": "PASS"
  }
}
```

and, from the same manifest's `current_evidence.validation`:

```json
"validation_errors": ["verification_tests.json runs[0] test_files is not sorted"]
```

**There is exactly ONE root error and the second blocking reason is its consequence**: a
rejected VerificationTests document yields no usable total, which is the `vt_passed = None`
cascade the closure protocol's pitfall (c) paragraph already describes for a different cause.
Everything else in the package is green — eight gate verdicts with no BLOCKED among them,
`review_subject_alignment` **PASS**, `snapshot_inventory_status.ok` **true**,
`git_status_snapshot.status` **OK** with an empty diagnostic, zero hash mismatches, zero dirty
files, 42 authoritative files matching the bundle's `authority_count`, and zero symlinks.

WHAT I OBSERVED ABOUT THE CAUSE, stated as an observation and not as a verdict, because naming
it is what lets the next round be short: the five `test_files` I passed are the block's own
selection IN THE BLOCK'S ORDER, which is not alphabetical. The producer path that normalises a
run record, `packages/orchestration/manual_attestation.py` `_vt_run_v11` line 173, writes
`"test_files": list(run.get("test_files") or [])` — it preserves caller order. The sibling
producer for the same field, `packages/orchestration/job_evidence.py` `_build_verification_tests`
line 1834, writes `sorted({_vt_norm(f) for f in test_files})`. One sorts and one does not, and
the validator requires sorted. Whether that asymmetry is the defect, or whether a caller is
simply obliged to pre-sort, is the reviewer's ruling and not mine; I am recording that the two
producers of one field disagree, and that my input reached the validator unmodified.

### G6 — PUSH AND TREE

- **Push after C1b**: `git push -u origin feature/f277-machine-contracts`, real exit code **0**:

```
To github.com:UndefinedDatabase/remedy.git
   b10e9bf1..9dbd8e6d  feature/f277-machine-contracts -> feature/f277-machine-contracts
Branch 'feature/f277-machine-contracts' set up to track remote branch 'feature/f277-machine-contracts' from 'origin'.
```

- **POST-PUSH readings, taken after that push and after the package build**, which is the state
  C2 is committed on top of and the state the push of C2 carries forward unchanged:

`git status --porcelain`: **empty (0 lines)**. The evidence dir, the driver script and all four
logs are under the gitignored `.remedy-wt/f277-r16-scratch/`, and the packaging script's own
staging directory left no tracked file dirty.

`git worktree list`:

```
/home/decodeux/Repos/remedy                                  9dbd8e6d [feature/f277-machine-contracts]
/home/decodeux/Repos/remedy/.remedy-wt/job-468c8e62a2cc4fac  1b9ae606 [remedy/job-468c8e62a2cc4fac]
/home/decodeux/Repos/remedy/.remedy-wt/job-86f628f5e4fb4e0c  aca27d4a [remedy/job-86f628f5e4fb4e0c]
/home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968  fd23710f [remedy/job-c1dba9c3d7874968]
```

Four entries: the primary checkout and the three `remedy/job-*` worktrees, all three untouched.
Round 15's `.remedy-wt/f277-r14-dry` is gone, so I added nothing and removed nothing.

- **Push after C2** runs as the round's last act. Its transcript is in the worker's session
  reply: a file cannot record the outcome of the push that ships it without a second write,
  which the template's write-once rule and the block's own "not into a trailing commit" both
  refuse. See deviation 2.

### The round's whole tracked path set

`git diff --name-only b10e9bf1 9dbd8e6d` returns **7** paths, plus `.agent/handoff.md` at C2 for
**8** — set-equal to constraint 3's enumeration:

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f277-r16-block.md | C1a `3d269bdb` |
| 2 | .agent/authored/f277-r16-ledger.md | C1a `3d269bdb` |
| 3 | .agent/authored/f277-r16-plan.md | C1a `3d269bdb` |
| 4 | .agent/authored/f277-r16-slips.md | C1a `3d269bdb` |
| 5 | .agent/live_review.md | C1b `9dbd8e6d` |
| 6 | .agent/plan.md | C1b `9dbd8e6d` |
| 7 | .agent/prose_slips.md | C1b `9dbd8e6d` |
| 8 | .agent/handoff.md | C2, this commit |

Nothing missing, nothing extra. `scripts/self_use_queue.json` appears **0** times. Nothing under
`packages/`, `apps/`, `tests/`, `docs/` or `scripts/` was touched. `.agent/decisions.md` and
`.agent/operator_questions.md` were not touched.

Commit trailers over `b10e9bf1..9dbd8e6d`, read per commit with
`git log --format='%(trailers:key=Co-Authored-By,valueonly)'`: both read
`Claude Opus 5 <noreply@anthropic.com>`, and this commit carries the same line.

## Authored-text proofs

- The four copies at C1a, compared with the reviewer's originals under
  `.remedy-wt/f277-r16-payloads/` and `.remedy-wt/f277-r16-block.md`: **four readings, all
  True** (G1(b)).
- The REWRITE payload against the committed file: `.agent/plan.md` is sha256-equal to `plan.md`
  at 45 lines (G1(d)).
- The two APPEND payloads against the committed files: strict byte concatenation True for both,
  with all four byte numbers equal to the reviewer's, and a one-bit negative control inside the
  appended paragraph driving the strict reader to False (G1(c)).
- No payload was edited or retyped. All four copies were made with `shutil.copyfile`; the two
  appends were made by reading the payload's bytes and concatenating them, never by typing.

## Deviations & assumptions

1. **The bundle ran C1a, C1b, C2 — three commits, exactly as ordered. Nothing was added,
   dropped or reordered.** Recorded here because the template asks the question directly.
2. **No trailing commit for the C2 push; its transcript goes in the session reply.** The block
   says to write the post-push readings "into the handback itself after pushing, not into a
   trailing commit". I satisfied both halves as far as a single write allows: the C1b push
   outcome is in G6 verbatim, and the post-push `git status --porcelain` and `git worktree list`
   are in G6 as measured readings taken AFTER that push. Only the C2 push's own transcript is
   unobtainable from inside the file it pushes, and adding a second commit to carry it is the
   thing the block forbids.
3. **`skipped`, `selected`, `deselected`, `duration_seconds`, `head_sha` and `output_hash` were
   supplied on the verification record although the block listed only the fields it cared
   about.** I read the contract that consumes the record first: the v1.1.0 VerificationTests
   validator in `scripts/build_review_manifest.py` requires `selected == passed + failed +
   skipped` and `len(node_ids) == selected`, and the runtime gate's `bound_run` path reads
   `head_sha` and `output_hash` straight off the caller's dict. Every one of those values is
   DERIVED — `skipped` and the counts from the run's own output, `selected` as `len(node_ids)`,
   `head_sha` from `git rev-parse HEAD`, `output_hash` as the sha256 of the scrubbed, truncated
   `stdout_summary` I stored. None was transcribed. **None of them is the blocked package's
   cause**, which is the unsorted `test_files` list.
4. **`test_files` was passed in the block's stated order, not sorted.** The block fixes the
   selection and says `test_files` is "the five paths of the selection, as FILES"; I passed
   exactly those five paths, unreordered, because reordering a list the block states is the kind
   of silent deviation this workflow punishes. That is the field the validator rejected. I am
   flagging it as the deviation candidate it may turn out to be: had I sorted them the package
   might have read READY, and I did not, because the block told me what to pass and the block's
   own third directive told me to report a non-READY package rather than to start adjusting
   inputs until one appeared. The next round can settle it in one line.
5. **I read the built package's manifest to obtain the raw error.** That is a read of the
   artifact the one permitted build produced, not a second build, and the block asks for "the
   raw error" — which is only recoverable there, since the script's console output names the
   failure but not its reason.
6. **Scratch and payload hygiene.** The driver script, the collect log, the run log, the
   verification record and the bundle summary are all under `.remedy-wt/f277-r16-scratch/`,
   together with the evidence dir itself. I wrote nothing into `.remedy-wt/f277-r16-payloads/`
   and nothing under `.agent/` that the block did not name — the F281 round 28 mistake
   constraint 5 exists for did not recur. Both directories are gitignored and
   `git status --porcelain` is empty at every commit boundary.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a copy block + 3 payloads | done | 279 insertions, matching 48 + 231; cap headroom 221, computed before committing |
| C1b book round 15 PASS + 1 slip, rewrite plan | done | 25 insertions by `git show --numstat`, matching the block's 25 (2 + 22 + 1) |
| C2 evidence job + review zip + handback | done | the evidence job succeeded; the package built and is BLOCKED_EVIDENCE, reported not retried; tracked change set is this file only |
| G1(a) payload transport, nine readings | done | 9/9 equal to the table |
| G1(b) four authored copies | done | 4/4 byte-identical to their sources |
| G1(c) two appends by strict concatenation | done | both True; all four byte numbers equal the reviewer's; one-bit negative control returns False |
| G1(d) plan rewrite | done | sha256-equal, 45 lines, under the 50-line rule |
| G1(e) open set | done | 22 at `b10e9bf1`, 22 at C1b, same 22 ids, by the canonical `rotate_live_review.py` reader |
| G2 base is the fork point | done | 89 and 89, EQUAL, at my own tip; manifest `review_subject_alignment` PASS confirms independently |
| G3 verification record self-consistent | done | 105 node ids, 105 passed, 0 failed, exit 0, 5 test_files all `isfile` true; assertion evaluated True in the script |
| G4 evidence bundle | done | summary dict reported in full; `token_truth.json` present; verdict PASS_WITH_RISKS |
| G5 the package | **done — and the result is a BLOCKER** | `BLOCKED_EVIDENCE`; filename, SHA-256 and archived directory all recorded; raw error quoted verbatim; tree was clean immediately before the build; ONE attempt, no retry |
| G6 push and tree | done | C1b push exit 0; post-push status empty; four worktrees, the three `job-*` untouched; C2 push transcript in the session reply (deviation 2) |
| Constraint 1 no payload edited or retyped | done | `shutil.copyfile` and byte concatenation only |
| Constraint 2 every commit under 500 | done | 279 and 25; this handoff is a single `.agent/**` state file and exempt |
| Constraint 3 no unnamed file touched | done | 8 paths, set-equal to the enumeration; `scripts/self_use_queue.json` 0 times |
| Constraint 4 stop on red | done | no gate went red; the zip's status is reported, not repaired, as the block requires |
| Constraint 5 nothing lands in the tracked tree | done | evidence dir, driver and all logs under the gitignored `.remedy-wt/f277-r16-scratch/`; `git status --porcelain` empty after the build |
| Constraint 6 leave the three `remedy/job-*` worktrees alone | done | untouched and still listed; no worktree added or removed this round |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 16: C1a, C1b and C2, with all six gates — and in particular G5, whose
   result is a **closure BLOCKER**, not a pass.
3. **The closure round the block names cannot start yet.** It was conditioned on the package
   being `READY_FOR_REVIEW`, and the package is `BLOCKED_EVIDENCE` on one validator error:
   `verification_tests.json runs[0] test_files is not sorted`. What the next round owes, before
   the §3 checklist consolidation carrying R-1014, the ledger rotation, the open-finding owner
   re-assignment and the STATUS `[x]` flip with the README sync and the `SU-025` `consumed_by`
   edit, is a ruling on that one error and a re-run of the evidence job and the package. The
   diagnosis is the reviewer's: `manual_attestation._vt_run_v11` preserves the caller's
   `test_files` order while its sibling `job_evidence._build_verification_tests` sorts, and the
   validator requires sorted (G5 records the observation and takes no position on the fix).
   Everything else the closure needs is already in hand: the evidence job itself succeeded at
   `PASS_WITH_RISKS` with a self-consistent 105-node record, the fork-point base is proven by two
   equal counts of 89 and by the manifest's own `review_subject_alignment: PASS`, eight gate
   verdicts carry no BLOCKED, and the tree is clean and pushed.

Open findings count: **22**. Operator-questions count: **2**.
