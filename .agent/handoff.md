# Handoff — F277 Machine contracts: event vocabulary, JSON envelope, exit codes · Round 17

## Session

SESSION 7 of feature F277 · round 17 · rounds so far 17

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE.

**SCOPE REPORT (required by amend0827 rule 6 at the 7-session soft limit).** Unchanged in
substance since round 12. *Finished:* T001, the event vocabulary, and T002, the JSON envelope
with its dispatch error boundary. *Missing:* T003 is partly applied — `fail()` exists and nine
of the twenty-eight CLI modules call it. T004 is not started. *The proposal, already carried
out:* DECISION F277 D10 closes F277 on T001 and T002 complete and T003 in part; the remainder
is registered as F283, directly after F277. The operator question it owes is
`.agent/operator_questions.md` Q2. **NEW THIS ROUND: THE CLOSURE IS UNBLOCKED.** The package
round 16 built `BLOCKED_EVIDENCE` on one validator error is rebuilt and reads
**`READY_FOR_REVIEW`**, with an empty `blocking_reasons` list and empty `validation_errors`.
The pre-check the block added caught nothing because there was nothing to catch — it ran green
BEFORE the build, which is the whole point of it.

Context self-assessment: before any edit I read `AGENTS.md`,
`docs/agents/handback_template.md`, `.remedy-wt/f277-r17-block.md`,
`docs/roadmap/STATUS_closure_protocol.md` (Algorithm steps 1 and 2 and the canonical zip build
sequence, including the five pitfalls it already carried) and round 16's `.agent/handoff.md` in
full, then all four payloads. I also read round 16's driver
`.remedy-wt/f277-r16-scratch/run_evidence.py` in full, so that the field shape the block calls
"round 16's shape, change none of them" was carried forward from the artefact that produced it
rather than from my memory of the handback describing it, and
`scripts/build_review_manifest.py::validate_verification_tests` for its return contract
(`(problems, passed)`) before calling it.

## Range

Review of `f44b8846`..`HEAD`.

## Commits

### 279059af F277 R17 C1a: copy round 17 payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f277-r17-block.md | +245/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f277-r17-ledger.md | +4/-0 | byte-for-byte copy of the ledger.md payload |
| .agent/authored/f277-r17-plan.md | +44/-0 | byte-for-byte copy of the plan.md payload |
| .agent/authored/f277-r17-protocol.diff | +31/-0 | byte-for-byte copy of the protocol.diff payload |
| .agent/authored/f277-r17-slips.md | +2/-0 | byte-for-byte copy of the slips.md payload |

Measured insertions (`git show --numstat`): **326**. Expected: 81 payload lines plus the
measured block line count of 245, which is 326. They **MATCH**. I ran the ordered cap
arithmetic BEFORE committing: `500 − 81 − 245 =` **174**, non-negative, so the commit was legal
and needed no oversize declaration. This feature's one permitted declaration stays spent where
round 12 spent it.

### 5bfa7420 F277 R17 C1b: register R-1017, book round 16's PASS and two reviewer slips
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | append the ledger.md payload: the R-1017 registration and the round 16 `Gate:` entry |
| .agent/plan.md | +15/-16 | rewrite to the plan.md payload, byte-identical, 44 lines |
| .agent/prose_slips.md | +2/-0 | append the slips.md payload's two lines |

Measured insertions (`git show --numstat`): **21**. The block expected **21**, and each
per-file number also matches the block's own breakdown, including the plan rewrite's diff
insertions of **15** against deletions of 16.

### deeac639 F277 R17 C2: record the sorted test_files pitfall in the closure protocol
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS_closure_protocol.md | +21/-0 | `git apply` of protocol.diff: pitfall (f) beside the five the file already carried |

Measured insertions: **21**. The block expected **21**. They MATCH.

### C3 — THE REBUILT EVIDENCE BUNDLE AND THE PACKAGE (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot table the
commit that writes it. **C3's tracked change set is the handback and nothing else**, which is
what the block ordered: neither the evidence dir nor the zip is committed. Every artifact this
round produced — the driver, five logs, the verification record, the bundle summary and the
evidence dir itself — lives under the gitignored `.remedy-wt/f277-r17-scratch/`.

## External actions

- `git push -u origin feature/f277-machine-contracts` after C2 — outcome
  `f44b8846..deeac639  feature/f277-machine-contracts -> feature/f277-machine-contracts`,
  real exit code **0**.
- `bash scripts/make_review_zip.sh --evidence-dir
  /home/decodeux/Repos/remedy/.remedy-wt/f277-r17-scratch/remedy-job-evidence-f277-r17` —
  real exit code **0**, package **READY_FOR_REVIEW**. Full output in G5. **One attempt only.**
- `git push -u origin feature/f277-machine-contracts` after C3 runs as the round's last act;
  see deviation 2 for why its own transcript cannot live inside the file it pushes.
- No `gh` command was run. No PR was created, edited or merged. **No worktree was added or
  removed this round** — the evidence job and the package both run in the primary checkout, and
  the three `remedy/job-*` worktrees were left alone.

## Verification

### Pre-flight

- `ls .agent/STOP`: `No such file or directory`. There is no STOP on disk.
- `git status --porcelain`: empty (0 lines).
- `git branch --show-current`: `feature/f277-machine-contracts`.
- `git rev-parse HEAD`: `f44b88463d35bce9e5575fc74234d7ed46f4074d`, matching `f44b8846`.
- Block self-verification (R-0954), `.remedy-wt/f277-r17-block.md`:

| reading | measured | given in the delegation message | equal |
|---|---|---|---|
| line count | 245 | 245 | True |
| sha256 | `269d8cd0edb0d33d5f87507f61700d8e6fe33cb1fb02bcb811942ebd396ef625` | `269d8cd0edb0d33d5f87507f61700d8e6fe33cb1fb02bcb811942ebd396ef625` | True |

Neither reading differs, so the round went ahead. The block file is 16376 bytes.

### G1(a) — PAYLOADS transport, twelve readings

| file | lines measured / given | bytes measured / given | sha256 measured (given identical) | equal |
|---|---|---|---|---|
| ledger.md | 4 / 4 | 7966 / 7966 | `bd47e0ff9962ec70109e6254c080162acd8997f9eb47baa636a46ff09f545fe4` | True |
| plan.md | 44 / 44 | 2200 / 2200 | `1fab9568a147897847671aef72084a753c8bf7904737a25fbeea7f342feb9a6e` | True |
| protocol.diff | 31 / 31 | 1976 / 1976 | `749264e80f02c88c389d1becd719ea883426afd61ce3ea5edc9a8ce09543b823` | True |
| slips.md | 2 / 2 | 2460 / 2460 | `b5c2a9d8ae7ad271663c92e594cb25fd9504ac6fd095668da2ceaef46982490d` | True |

**All twelve readings equal: True.** Total payload lines **81**. The separator shapes the block
declares also hold: `ledger.md` begins with a newline (`True`) and `slips.md` does not
(`False`). `protocol.diff` dry-ran with `git apply --check` at real exit code **0** before it
was applied. Nothing was written into `.remedy-wt/f277-r17-payloads/`.

### G1(b) — the five `.agent/authored/f277-r17-*` copies against their sources

Copied with `shutil.copyfile`, then compared byte-for-byte against the originals:

| copy | source | bytes | sha256 | identical |
|---|---|---|---|---|
| f277-r17-block.md | `.remedy-wt/f277-r17-block.md` | 16376 | `269d8cd0edb0d33d…` | True |
| f277-r17-ledger.md | `.remedy-wt/f277-r17-payloads/ledger.md` | 7966 | `bd47e0ff9962ec70…` | True |
| f277-r17-plan.md | `.remedy-wt/f277-r17-payloads/plan.md` | 2200 | `1fab9568a1478978…` | True |
| f277-r17-protocol.diff | `.remedy-wt/f277-r17-payloads/protocol.diff` | 1976 | `749264e80f02c88c…` | True |
| f277-r17-slips.md | `.remedy-wt/f277-r17-payloads/slips.md` | 2460 | `b5c2a9d8ae7ad271…` | True |

**Copies compared: 5. All True.** The chain makes no claim about the bytes emitted into the
worker's prompt, which this workflow cannot measure.

### G1(c) — the two appends at C1b

Byte arithmetic by strict CONCATENATION, not by length. The pre bytes were read back out of
`f44b8846` with `git show`, not from the working tree, so the baseline is the commit's:

| file | pre measured | pre, reviewer's | payload | post measured | post, reviewer's | pre+payload == post |
|---|---|---|---|---|---|---|
| .agent/live_review.md | 479169 | 479169 | 7966 | 487135 | 487135 | True |
| .agent/prose_slips.md | 354909 | 354909 | 2460 | 357369 | 357369 | True |

All four of my numbers equal the reviewer's four.

**Reading (b), the independent structural reader (§3 item 36).** My script COUNTED the
blank-line-separated paragraphs in `ledger.md` rather than taking the number from the block:
**N = 2**. It then compared the LAST 2 such units of the whole committed file against those 2
payload paragraphs IN ORDER: **True**. The two units are, by their first 90 characters:

```
unit 1: '- R-1017 — Medium, ONE FIELD HAS TWO PRODUCERS AND ONLY ONE OF THEM SATISFIES THE VALIDATO'
unit 2: 'Gate: F277 R16 — the F277 round 16 entry. VERDICT PASS ON ALL SIX GATES; THE PACKAGE IS A '
```

**Negative control**, on `.agent/live_review.md` only. I flipped one bit at byte offset 479210,
INSIDE the FIRST appended paragraph (the R-1017 registration), on an in-memory copy; the
committed file was never mutated. Length unchanged: `True`. **BOTH readings return False:**

```
READING 1 strict concatenation pre+payload == mutated: False
READING 2 structural last-N comparison:                False
```

So neither reader is a length comparison and neither can be satisfied by a payload that differs
by a single bit.

### G1(d) — the plan rewrite at C1b

| reading | value |
|---|---|
| payload sha256 | `1fab9568a147897847671aef72084a753c8bf7904737a25fbeea7f342feb9a6e` |
| committed `.agent/plan.md` sha256 | `1fab9568a147897847671aef72084a753c8bf7904737a25fbeea7f342feb9a6e` |
| byte equal | True |
| line count | 44 (under the AGENTS.md 50-line rule: True) |

### G1(e) — open set by distinct id in `.agent/live_review.md`

Computed with the repository's OWN canonical reader rather than a hand-rolled regex: I loaded
`scripts/rotate_live_review.py` and called its `open_finding_ids`, the same function
`packages/orchestration/integrity_gate.py` loads by path (R-0648 is the finding that says a
re-implemented parser drifts).

| rev | OPEN by distinct id |
|---|---|
| f44b8846 | **22** |
| C1b `5bfa7420` | **23** |

Ids added by round 17: **`R-1017`**, exactly one. Ids resolved by round 17: **none**. Both
numbers are the ones the block stated, and the new id is the one it named.

### G2 — THE PROTOCOL EDIT

The new pitfall paragraph's **first four lines, verbatim** from
`docs/roadmap/STATUS_closure_protocol.md` (lines 126–129), sitting directly after pitfall (e):

```
   A sixth, from the F277 R16 attempt (one validator error, packaged
   BLOCKED_EVIDENCE): (f) each verification record's `test_files` must be
   SORTED. `build_review_manifest._vt_safe_files` rejects an unsorted list
   (`if tf != sorted(tf)`), which rejects the whole VerificationTests
```

Count of the string `(f) each verification record` in that file: **1**.

`git diff --name-only 5bfa7420 deeac639` names exactly one path, and its length is **1**:

```
docs/roadmap/STATUS_closure_protocol.md
```

`python3 -m pytest -q -p no:cacheprovider tests/docs/`, real exit code **0**, summary line:

```
314 passed in 85.66s (0:01:25)
```

which equals the `314 passed` the reviewer read at `f44b8846`, so the added prose did not
disturb a suite that reads this file.

### G3 — THE VERIFICATION RECORD IS SORTED AND SELF-CONSISTENT

One driver script, `.remedy-wt/f277-r17-scratch/run_evidence.py`, real exit code **0**. It
DERIVES every number and raises `SystemExit` rather than packaging on any disagreement. No
number below was transcribed from the block.

`test_files` **exactly as I passed it**:

```json
["tests/cli/test_golden_path.py",
 "tests/cli/test_json_envelope.py",
 "tests/cli/test_memory_cmd.py",
 "tests/orchestration/test_event_names.py",
 "tests/ui_contracts/test_humanize_catalog.py"]
```

The boolean my driver evaluated, in the script and not off the block's page — the script calls
`sorted()` on its own list and compares, and exits non-zero if it differs:

```
test_files == sorted(test_files) -> True
```

Collect: `python3 -m pytest -q -p no:cacheprovider --collect-only <5 files>`, real exit code
**0**, summary line `105 tests collected`.

Run: `python3 -m pytest -q -p no:cacheprovider <5 files>`, real exit code **0**, summary line
`105 passed in 137.39s (0:02:17)`.

| reading | mine | round 16's |
|---|---|---|
| collect count | **105** | 105 |
| `len(node_ids)` | **105** | 105 |
| `passed` | **105** | 105 |
| `failed` | **0** | 0 |
| `skipped` | **0** | 0 |
| `exit_code` | **0** | 0 |
| `len(test_files)` | **5** | 5 |
| run summary line | `105 passed in 137.39s (0:02:17)` | `105 passed in 138.29s (0:02:18)` |

The assertion the script evaluated, printed by the script itself:

```
ASSERT len(node_ids) == passed+failed+skipped -> True
```

Every `test_files` entry is a FILE by `os.path.isfile`, all five **true**:

```json
{"tests/cli/test_golden_path.py": true,
 "tests/cli/test_json_envelope.py": true,
 "tests/cli/test_memory_cmd.py": true,
 "tests/orchestration/test_event_names.py": true,
 "tests/ui_contracts/test_humanize_catalog.py": true}
```

No directory entry (pitfall b), `run_id` is `vr-0001` and matches `^vr-\d{4,}$` (pitfall c), the
node-id list is the SCOPED selection and never the full suite (pitfall d), `base_commit` was
passed at full length, and the list is SORTED (pitfall f, the one this round lands). The
fork-point check re-ran inside the driver at my own tip and the two counts are **93 and 93**,
EQUAL, so pitfall (e) is clean.

### G4 — THE PRE-CHECK, THE POINT OF THIS ROUND

Run BEFORE any package build, over the document the bundle had just written. The absolute path
I loaded it from:

```
/home/decodeux/Repos/remedy/.remedy-wt/f277-r17-scratch/remedy-job-evidence-f277-r17/verification_tests.json
```

The script asserted the provenance of that path rather than asserting it in prose — it is
inside THIS round's fresh evidence dir (`True`) and the string `r16` does not occur in it
(`False`), so round 16's document cannot have been read by mistake. This is the specific error
the reviewer's own second prose slip this round records.

```
PRE-CHECK problems = []
PRE-CHECK passed   = 105
PRE-CHECK problems list is empty: True
document runs[0] test_files as written: ["tests/cli/test_golden_path.py", "tests/cli/test_json_envelope.py", "tests/cli/test_memory_cmd.py", "tests/orchestration/test_event_names.py", "tests/ui_contracts/test_humanize_catalog.py"]
```

**The problems list is EMPTY and `passed` is 105**, which are the two values the block required
before a package could be built. The driver would have raised `SystemExit` and built nothing
otherwise. The gate is not one that cannot fail: the reviewer reproduced BOTH colours on round
16's real document at `9dbd8e6d` — unsorted it returns
`['verification_tests.json runs[0] test_files is not sorted']` with `passed` unresolvable, and
the same document with that one list sorted returns `[]` at `passed` 105.

### G5 — THE PACKAGE: READY_FOR_REVIEW

`git status --porcelain` **immediately before the build: empty (0 lines)**, at the pushed head
`deeac639`. The package was NOT built from a dirty tree.

The evidence bundle's returned summary dict, **in full**:

```json
{
 "authority_count": 43,
 "commit_count": 93,
 "head_commit": "deeac639488b1cb1be930a550b2295509652051f",
 "job_id": "f2771701c0de5a17",
 "manual_completion": true,
 "operator_attested_tasks": ["T001", "T002", "T003"],
 "partition": {"T001": 15, "T002": 15, "T003": 13},
 "total_passed": 105,
 "verdict": "PASS_WITH_RISKS"
}
```

- Evidence dir, absolute and FRESH this round:
  `/home/decodeux/Repos/remedy/.remedy-wt/f277-r17-scratch/remedy-job-evidence-f277-r17`
  (it did not exist before the driver ran: `evidence dir exists before build: False`)
- `token_truth.json` is a file in it: **True**
- Job id **`f2771701c0de5a17`**, distinct from round 16's `f2771600aabbccdd`, asserted in the
  driver rather than merely chosen.

Command and full output, real exit code **0**:

```
$ bash scripts/make_review_zip.sh --evidence-dir /home/decodeux/Repos/remedy/.remedy-wt/f277-r17-scratch/remedy-job-evidence-f277-r17
UNCHANGED: runtime_integration_gate.json — rebuilt from source; identical to existing
Evidence refresh completed for staged copy.
Observability index generated from staged bytes: evidence/current/self_run_observability_index.json
{"member_count": 4973, "authoritative_count": 43, "symlink_count": 0, "tombstone_count": 0,
 "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20260921-032054-READY_FOR_REVIEW.zip",
 "final_sha256": "cd8542e0a6d2ec18fa9d171dcc2a762574e57911d48867e762f81b5dd1681723",
 "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW",
 "evidence_authoritative": true, "review_subject_alignment": "PASS",
 "manifest_sha256": "2e6ba42bd9f39a899a79cfa5117cea1a8ea97730f1aba82d8bd3f662f17d9dce"}

============================================
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
PACKAGING_CWD=/home/decodeux/Repos/remedy
EVIDENCE_DIR=/home/decodeux/Repos/remedy/.remedy-wt/f277-r17-scratch/remedy-job-evidence-f277-r17
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260921-032054-READY_FOR_REVIEW.zip
============================================

ZIP CREATED AND READY FOR FINAL REVIEW

28M     /home/decodeux/Repos/remedy-history/zips/remedy-review-20260921-032054-READY_FOR_REVIEW.zip
Included files: 4973
Branch: feature/f277-machine-contracts
Commit: deeac639488b1cb1be930a550b2295509652051f
Evidence: evidence/current/
```

Round 16's build printed `WARNING: Evidence validation failed (is_valid_current_run=false)` and
`DO_NOT_COMMIT=true` at this point; **neither line appears here**, and
`EVIDENCE_AUTHORITATIVE` flipped from `false` to `true`.

**The record DECISION amend0827 D1 and the closure protocol require:**

| field | value |
|---|---|
| package FILENAME | `remedy-review-20260921-032054-READY_FOR_REVIEW.zip` |
| SHA-256 | `cd8542e0a6d2ec18fa9d171dcc2a762574e57911d48867e762f81b5dd1681723` |
| STATUS as the filename carries it | **`READY_FOR_REVIEW`** |
| archived path (absolute directory) | `/home/decodeux/Repos/remedy-history/zips` |

The sandbox did NOT refuse the write, so the record carries the real directory and not
`NOT ARCHIVED`. I re-computed the SHA-256 off the 28355558-byte file on disk myself and it
equals the one the script printed: **True**.

**The manifest, read out of the built package's own `.review_zip_manifest.json`:**

| field | value |
|---|---|
| `committed_review_subject.head_commit` | `deeac639488b1cb1be930a550b2295509652051f` |
| equals the commit I built from | **True** |
| `committed_review_subject.base_commit` | `f2494c0216b33d5f261195789ec9f7a300de5fca` |
| `package_status` | `READY_FOR_REVIEW` |
| `ready_gate_matrix.ok` | **true** |
| `ready_gate_matrix.blocking_reasons` | **`[]`** |
| `current_evidence.validation.validation_errors` | **`[]`** |
| `current_evidence.validation.is_valid_current_run` | **true** |

That head_commit is the value that becomes next round's STATUS `accepted HEAD`; it is
`deeac639488b1cb1be930a550b2295509652051f`, the C2 tip, and C3 (this handback) is deliberately
NOT in it, exactly as the protocol's build order requires.

The eight gate verdicts, unchanged in shape from round 16 but now with an empty blocking list:

```json
{"artifact_contract_gate.json": "PASS",
 "change_provenance_gate.json": "PASS",
 "commit_execution_gate.json": "NEEDS_HUMAN_APPROVAL",
 "final_verifier_report.json": "PASS_WITH_RISKS",
 "fresh_evidence_gate.json": "PASS",
 "manifest_integrity.json": "ok=true",
 "postmortem_integrity.json": "ok=true",
 "runtime_integration_gate.json": "PASS"}
```

**BOTH ARTIFACT-BUILD ATTEMPTS OF THIS CLOSURE**, as AGENTS.md's `### handoff.md` requires
every attempt to appear with its status — the earlier one is a real attempt and is not dropped
from the record now that it has been superseded:

| # | round | package filename | SHA-256 | status | archived path |
|---|---|---|---|---|---|
| 1 | R16 | `remedy-review-20260921-025659-BLOCKED_EVIDENCE.zip` | `8245d4a790ecd9a5342e0511bc5d5253c3a5f0ffd38c266a60df0a1030b5b8fb` | **BLOCKED_EVIDENCE** — blocking reason `verification_tests.json runs[0] test_files is not sorted`, with the consequent `final_verifier_report.json test_status.passed cannot be confirmed` | `/home/decodeux/Repos/remedy-history/zips` |
| 2 | R17 | `remedy-review-20260921-032054-READY_FOR_REVIEW.zip` | `cd8542e0a6d2ec18fa9d171dcc2a762574e57911d48867e762f81b5dd1681723` | **READY_FOR_REVIEW** — no blocking reasons | `/home/decodeux/Repos/remedy-history/zips` |

Round 16's package was left exactly where it is, untouched, as constraint 6 requires.

### G6 — PUSH AND TREE

- **Push after C2**: `git push -u origin feature/f277-machine-contracts`, real exit code **0**:

```
To github.com:UndefinedDatabase/remedy.git
   f44b8846..deeac639  feature/f277-machine-contracts -> feature/f277-machine-contracts
Branch 'feature/f277-machine-contracts' set up to track remote branch 'feature/f277-machine-contracts' from 'origin'.
```

- **POST-PUSH readings, taken after that push and after the package build**, which is the state
  C3 is committed on top of and the state the push of C3 carries forward unchanged:

`git status --porcelain`: **empty (0 lines)**. The evidence dir, the driver and all five logs
are under the gitignored `.remedy-wt/f277-r17-scratch/`, and the packaging script's own staging
directory left no tracked file dirty.

`git worktree list`:

```
/home/decodeux/Repos/remedy                                  deeac639 [feature/f277-machine-contracts]
/home/decodeux/Repos/remedy/.remedy-wt/job-468c8e62a2cc4fac  1b9ae606 [remedy/job-468c8e62a2cc4fac]
/home/decodeux/Repos/remedy/.remedy-wt/job-86f628f5e4fb4e0c  aca27d4a [remedy/job-86f628f5e4fb4e0c]
/home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968  fd23710f [remedy/job-c1dba9c3d7874968]
```

Four entries: the primary checkout and the three `remedy/job-*` worktrees, all three untouched.
I added no worktree and removed none.

- **Push after C3** runs as the round's last act. Its transcript is in the worker's session
  reply: a file cannot record the outcome of the push that ships it without a second write,
  which the template's write-once rule and the block's own "not into a trailing commit" both
  refuse. See deviation 2.

### The round's whole tracked path set

`git diff --name-only f44b8846 deeac639` returns **9** paths, plus `.agent/handoff.md` at C3 for
**10** — set-equal to constraint 3's enumeration:

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f277-r17-block.md | C1a `279059af` |
| 2 | .agent/authored/f277-r17-ledger.md | C1a `279059af` |
| 3 | .agent/authored/f277-r17-plan.md | C1a `279059af` |
| 4 | .agent/authored/f277-r17-protocol.diff | C1a `279059af` |
| 5 | .agent/authored/f277-r17-slips.md | C1a `279059af` |
| 6 | .agent/live_review.md | C1b `5bfa7420` |
| 7 | .agent/plan.md | C1b `5bfa7420` |
| 8 | .agent/prose_slips.md | C1b `5bfa7420` |
| 9 | docs/roadmap/STATUS_closure_protocol.md | C2 `deeac639` |
| 10 | .agent/handoff.md | C3, this commit |

Nothing missing, nothing extra. `scripts/self_use_queue.json` appears **0** times. Nothing under
`packages/`, `apps/`, `tests/` or `scripts/` was touched; the single path outside `.agent/` is
the closure protocol doc C2 was ordered to edit. `.agent/decisions.md` and
`.agent/operator_questions.md` were not touched.

Commit trailers over `f44b8846..deeac639`, read per commit with
`git log --format='%(trailers:key=Co-Authored-By,valueonly)'`: all three read
`Claude Opus 5 <noreply@anthropic.com>`, and this commit carries the same line.

## Authored-text proofs

- The five copies at C1a, compared with the reviewer's originals under
  `.remedy-wt/f277-r17-payloads/` and `.remedy-wt/f277-r17-block.md`: **five readings, all
  True** (G1(b)).
- The REWRITE payload against the committed file: `.agent/plan.md` is sha256-equal to `plan.md`
  at 44 lines (G1(d)).
- The two APPEND payloads against the committed files: strict byte concatenation True for both,
  with all four byte numbers equal to the reviewer's, plus the independent structural reader at
  a COUNTED N of 2, plus a one-bit negative control inside the first appended paragraph driving
  BOTH readers to False (G1(c)).
- The DIFF payload: applied with `git apply`, never retyped; it dry-ran at exit 0 and landed 21
  insertions on the one path it names (G2).
- No payload was edited or retyped. All five copies were made with `shutil.copyfile`; the two
  appends were made by reading the payload's bytes and concatenating them, never by typing.

## Deviations & assumptions

1. **The bundle ran C1a, C1b, C2, C3 — four commits, exactly as ordered. Nothing was added,
   dropped or reordered.** Recorded here because the template asks the question directly.
2. **No trailing commit for the C3 push; its transcript goes in the session reply.** The block
   says to write the post-push readings "into the handback itself after pushing, not into a
   trailing commit". I satisfied both halves as far as a single write allows: the C2 push
   outcome is in G6 verbatim, and the post-push `git status --porcelain` and `git worktree list`
   are in G6 as measured readings taken AFTER that push and after the package build. Only the
   C3 push's own transcript is unobtainable from inside the file it pushes.
3. **`skipped`, `selected`, `deselected`, `duration_seconds`, `head_sha` and `output_hash` were
   supplied on the verification record**, carried forward unchanged from round 16's record,
   which the block instructed. Every one is DERIVED in the driver — the counts from the run's
   own output, `selected` as `len(node_ids)`, `head_sha` from `git rev-parse HEAD`,
   `output_hash` as the sha256 of the scrubbed, truncated `stdout_summary`. None was
   transcribed, and the pre-check confirms the whole document validates.
4. **`test_files` was passed SORTED this round**, which is the one field the block changed. The
   sortedness is not taken on the block's word: the driver calls `sorted()` on its own list,
   compares, prints the boolean, and raises `SystemExit` rather than packaging if it is False.
   Round 16's deviation 4 — the unsorted list that blocked that package — is therefore closed
   by a measurement rather than by a promise.
5. **I read the built package's manifest to obtain the head_commit and the gate matrix.** That
   is a read of the artefact the one permitted build produced, not a second build. The block
   asks for `committed_review_subject.head_commit`, which is only recoverable there.
6. **Scratch and payload hygiene.** The driver, the collect log, the run log, the docs-suite
   log, the zip-build log, the verification record, the bundle summary and the evidence dir
   itself are all under `.remedy-wt/f277-r17-scratch/`, a FRESH directory for this attempt;
   round 16's `.remedy-wt/f277-r16-scratch/` and its evidence dir were not reused, read from or
   written to, so the two attempts remain distinguishable on disk. I wrote nothing into
   `.remedy-wt/f277-r17-payloads/` and nothing under `.agent/` the block did not name.
7. **One tooling note, no effect on any reading.** Loading `scripts/rotate_live_review.py` by
   path for G1(e) raised an `AttributeError` inside `dataclasses` until the module was
   registered in `sys.modules` before `exec_module`; that is a property of loading a
   dataclass-bearing module by spec, not of the ledger or of the reader. The reader used is
   still the repository's canonical `open_finding_ids` and no regex was substituted for it.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a copy block + 4 payloads | done | 326 insertions, matching 81 + 245; cap headroom 174, computed before committing |
| C1b register R-1017, book R16 PASS + 2 slips, rewrite plan | done | 21 insertions by `git show --numstat`, matching the block's 21 (4 + 2 + 15) |
| C2 land pitfall (f) in the closure protocol | done | 21 insertions, matching the block's 21; exactly one path |
| C3 evidence bundle + package + handback | done | bundle clean, pre-check empty, package READY_FOR_REVIEW; tracked change set is this file only |
| G1(a) payload transport, twelve readings | done | 12/12 equal to the table; diff dry-ran at exit 0 |
| G1(b) five authored copies | done | 5/5 byte-identical to their sources |
| G1(c) two appends, concatenation + structural reader + control | done | both True; four byte numbers equal the reviewer's; N counted as 2; one-bit control returns False on BOTH readers |
| G1(d) plan rewrite | done | sha256-equal, 44 lines, under the 50-line rule |
| G1(e) open set | done | 22 at `f44b8846`, 23 at C1b, the one new id being R-1017, by the canonical `rotate_live_review.py` reader |
| G2 the protocol edit | done | first four lines quoted verbatim; marker string count 1; one path; `314 passed` at exit 0 |
| G3 verification record sorted and self-consistent | done | `test_files == sorted(test_files)` True in the script; 105 node ids, 105 passed, 0 failed, exit 0, 5 files all `isfile` true |
| G4 the pre-check | **done — and it is EMPTY** | `problems = []`, `passed = 105`, loaded from this round's fresh evidence dir, provenance asserted in the script |
| G5 the package | **done — READY_FOR_REVIEW** | filename, SHA-256 (re-computed by me), status and archived directory recorded; manifest head_commit equals the built commit; tree clean immediately before; ONE attempt |
| G6 push and tree | done | C2 push exit 0; post-push status empty; four worktrees, the three `job-*` untouched; C3 push transcript in the session reply (deviation 2) |
| Constraint 1 no payload edited or retyped | done | `shutil.copyfile`, byte concatenation and `git apply` only |
| Constraint 2 every commit under 500 | done | 326, 21 and 21; this handoff is a single `.agent/**` state file and exempt |
| Constraint 3 no unnamed file touched | done | 10 paths, set-equal to the enumeration; `scripts/self_use_queue.json` 0 times |
| Constraint 4 stop on red | done | no gate went red; the pre-check, the one gate whose red would have ended the round, is empty |
| Constraint 5 nothing lands in the tracked tree | done | evidence dir, driver and all logs under the gitignored `.remedy-wt/f277-r17-scratch/`; `git status --porcelain` empty after the build |
| Constraint 6 leave the worktrees and R16's package alone | done | three `remedy/job-*` worktrees untouched and still listed; round 16's BLOCKED_EVIDENCE zip left in place and recorded in G5's two-attempt table |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 17: C1a, C1b, C2 and C3, with all six gates — and in particular G4, the
   pre-check, and G5, whose package is **`READY_FOR_REVIEW`** at
   `cd8542e0a6d2ec18fa9d171dcc2a762574e57911d48867e762f81b5dd1681723`.
3. **The package IS `READY_FOR_REVIEW`, so the final closure round is unblocked.** It owes, in
   order: the §3 checklist consolidation carrying `R-1014`, where the fix clause lands merged
   into an existing item and never appended; the ledger rotation by
   `scripts/rotate_live_review.py` as its own commit; the open-finding owner re-assignment of
   every open finding F277 did not resolve to the next findings-paydown feature; and the STATUS
   `[x]` flip with the README capability sync and the `SU-025` `consumed_by` edit in ONE commit,
   last on the branch under Rule A4 — then the pull request, which is **NOT merged this
   session**. The STATUS line's `accepted HEAD` is
   `deeac639488b1cb1be930a550b2295509652051f`, its `package` is
   `remedy-review-20260921-032054-READY_FOR_REVIEW.zip`, its `SHA-256` is
   `cd8542e0a6d2ec18fa9d171dcc2a762574e57911d48867e762f81b5dd1681723`, its `package path` is
   `/home/decodeux/Repos/remedy-history/zips` and its `Evidence job` is `f2771701c0de5a17`.

Open findings count: **23**. Operator-questions count: **2**.
