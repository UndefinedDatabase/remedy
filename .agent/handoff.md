# Handoff — F061 R4 (CLOSURE)

Review of `f6a05214..HEAD` (branch `feature/f061-dod-compiler`).
Accepted HEAD (the head the zip and the verdict cover): `8dc6086c`.

F061 is closed: STATUS `[x]`, README synced in the same commit, Built State in
the feature file, evidence job built and validated READY, review zip
READY_FOR_REVIEW. The PR is open and **NOT merged** — it merges at the next
feature's Open PR Gate.

---

## Commits

### 1 — `16fd64ac` chore(f061): persist the R3 integration-gate verdict

| path | +/- | reason |
| --- | --- | --- |
| `.agent/authored/f061-r4-1.md` | +75/-0 | authored live_review text |
| `.agent/authored/f061-r4-2.md` | +43/-0 | authored Built State text |
| `.agent/authored/f061-r4-3.md` | +4/-0 | authored STATUS FROM/TO template |
| `.agent/authored/f061-r4-4.md` | +8/-0 | authored README edits |
| `.agent/live_review.md` | +50/-49 | full replacement, byte copy of f061-r4-1 |
| `.agent/last_block.md` | +205/-231 | this round's block recorded verbatim |

### 2 — `03df53fb` docs(f061): record the accepted Built State in the feature file

| path | +/- | reason |
| --- | --- | --- |
| `docs/roadmap/features/T1_F061.md` | +43/-0 | f061-r4-2 byte-appended (precondition 4) |

### 3 — `8dc6086c` test(f061): package-safe parametrize ids for the cwd-escape cases

| path | +/- | reason |
| --- | --- | --- |
| `tests/orchestration/test_dod_compiler.py` | +8/-1 | explicit ids so no node id reads as a local absolute path (deviation 1) |

### 4 — `<closure>` chore(f061): close F061 — STATUS [x] + README sync

| path | +/- | reason |
| --- | --- | --- |
| `docs/roadmap/STATUS.md` | +1/-1 | the F061 line only, `[~]` → `[x]` with the four recorded values |
| `README.md` | +2/-2 | the two authored ledger edits (R-0154 pin: same commit as STATUS) |
| `.agent/handoff.md` | rewrite | this report |
| `.agent/last_block.md` | +N/-N | OUTCOME appended |

The closure commit touches exactly `docs/roadmap/STATUS.md`, `README.md` and
`.agent/` — nothing else.

---

## Phase 2 gate — Built State

Byte-append verified before committing: the authored bytes occur in the file
**exactly once**, the file **ends** with them, and the prior content is intact
as a prefix.

```
$ python3 -m pytest tests/docs/ -q
........................................................................ [ 98%]
.....                                                                    [100%]
293 passed in 0.19s
EXIT=0

$ python3 -m pytest tests/cli/test_golden_path.py -q
..........................................                               [100%]
42 passed in 15.18s
EXIT=0
```

## Phase 3 — preconditions

```
$ remedy integrity check --json
{
  "version": 1,
  "passed": true,
  "fail_count": 0,
  "check_count": 5,
  "checks": [
    {"name": "handler_import",     "status": "pass", "message": "handlers=320"},
    {"name": "live_review_verdict","status": "pass", "message": "- R1: PASS (SPLIT round, 2026-08-01). Range 1869d89a..785f8cbd."},
    {"name": "plan_consistency",   "status": "pass", "message": "unchecked=0, context_complete=False"},
    {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
    {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
  ]
}
EXIT=0

$ git status --porcelain
(no output)

$ git push -u origin feature/f061-dod-compiler
 * [new branch]        feature/f061-dod-compiler -> feature/f061-dod-compiler
EXIT=0
```

## Phase 4 — evidence job

**Evidence job `c5185517fa2443bf`.**

Producer: `job_evidence.create_manual_completion_bundle(review_feature_id="f061", …)`
at `base_commit=1869d89a22718dce0f16c25289f927e8374571bb`,
`head_commit=8dc6086c4da87ca2ec63c33c3e17904c29ee394d`.

```
{"authority_count": 21, "commit_count": 27,
 "head_commit": "8dc6086c4da87ca2ec63c33c3e17904c29ee394d",
 "job_id": "c5185517fa2443bf", "manual_completion": true,
 "operator_attested_tasks": ["T001", "T002", "T003"],
 "partition": {"T001": 7, "T002": 7, "T003": 7},
 "total_passed": 196, "verdict": "PASS_WITH_RISKS"}
```

Two real verification runs, both executed at this head:

| run_id | command | exit | passed | node_ids |
| --- | --- | --- | --- | --- |
| `vr-0001` | `pytest tests/orchestration/test_dod_{compiler,runners,gate}.py -q` | 0 | 154 | 154 |
| `vr-0002` | `pytest tests/cli/test_golden_path.py -q` | 0 | 42 | 42 |

Every listed producer pitfall was handled at AUTHORING time, and asserted
before the producer was called:

* `test_files` sorted, files only — each `Path(f).is_file()` asserted; no
  directory entries;
* `output_hash` **omitted deliberately** so the producer derives it from the
  STORED 2000-char `stdout_summary` (`job_evidence.py:1637-1644`) — supplying
  one computed over the untruncated log is the documented trap;
* real node ids from `--collect-only`, with `len(node_ids) == passed` asserted
  per run;
* `run_id` matched against `^vr-\d{4,}$`;
* full-length 40-char `base_commit`.

Coordinator validation over the produced bytes, BEFORE any zip was built:

```
ready_gate_matrix ok: True
blocking_reasons: []
validate_manual_completion: []
is_valid_current_run: True
validation_errors: []
final_verifier reproducibility: VERIFIED_EQUAL
token_truth authority: VERIFIED_EQUAL
```

### The rejected first bundle (recorded before the retry, as ordered)

The first bundle — built at `03df53fb`, the original accepted HEAD — was
REJECTED by that same pre-zip validation. Raw output:

```
ready_gate_matrix ok: False
blocking_reasons: [
 'final_verifier_report.json test_status.passed cannot be confirmed: the VerificationTests total is missing or invalid',
 'verification_tests.json field verification_tests.runs[0].node_ids[39] carries a local absolute path',
 'verification_tests.json field verification_tests.runs[0].node_ids[40] carries a local absolute path',
 'verification_tests.json field verification_tests.runs[0].node_ids[41] carries a local absolute path']
is_valid_current_run: False
```

The three ids:

```
39 tests/orchestration/test_dod_compiler.py::TestNonsenseSpecRejection::test_cwd_may_not_escape_the_worktree[/etc]
40 …::test_cwd_may_not_escape_the_worktree[../outside]
41 …::test_cwd_may_not_escape_the_worktree[a/../../b]
```

No zip was built from it. The rejected evidence dir was **deleted** before the
rebuild (`rm -rf`), and the bundle was regenerated from scratch at the new head
after the fix in commit 3. See deviation 1.

## Phase 5 — review zip

Built from a clean tree at `8dc6086c`, branch pushed first.

```
$ git status --porcelain
(no output)
$ bash scripts/make_review_zip.sh --evidence-dir <evidence dir>
{"member_count": 1750, "authoritative_count": 21, "symlink_count": 0,
 "tombstone_count": 0,
 "final_path": "remedy-review-20260801-190945-READY_FOR_REVIEW.zip",
 "final_sha256": "486948228f6dd3413ba8cdd9947622b08b8803b40e9f7a0c7c547470150bcbd8",
 "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW",
 "evidence_authoritative": true, "review_subject_alignment": "PASS",
 "manifest_sha256": "b116f33cc1d9b05e0cf8af5abb19b46986ea5f98f5889cdf48700bf7386b23e3"}

REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
Commit: 8dc6086c4da87ca2ec63c33c3e17904c29ee394d
EXIT=0
```

**package `remedy-review-20260801-190945-READY_FOR_REVIEW.zip`**
**SHA-256 `486948228f6dd3413ba8cdd9947622b08b8803b40e9f7a0c7c547470150bcbd8`**

Recomputed independently from disk:

```
$ sha256sum remedy-review-20260801-190945-READY_FOR_REVIEW.zip
486948228f6dd3413ba8cdd9947622b08b8803b40e9f7a0c7c547470150bcbd8  remedy-review-20260801-190945-READY_FOR_REVIEW.zip
```

Required properties, each checked against the packaged bytes:

| requirement | result |
| --- | --- |
| READY_FOR_REVIEW | `PACKAGE_STATUS=READY_FOR_REVIEW` |
| is_valid_current_run true | True (pre-zip coordinator validation) |
| validation_errors [] | `[]` |
| ready_gate_matrix ok=true | True, `blocking_reasons: []` |
| committed_review_subject spans BASE..accepted HEAD | `base_commit 1869d89a22718dce0f16c25289f927e8374571bb` → `head_commit 8dc6086c4da87ca2ec63c33c3e17904c29ee394d` (from the packaged `evidence/current/review_subject.json`) |
| zip import check | see below |

Zip integrity and import check over the PACKAGED sources (extracted to a
temporary directory, imported there, then removed):

```
$ python3 -c "zipfile … testzip()"
zip integrity testzip: OK (no bad member)

$ cd <extracted> && python3 -c "import packages.orchestration.dod_{schema,compiler,runners,gate}; …"
packaged modules import OK
dod_v1 registered in packaged sources: True
EXIT=0
```

## Phase 6 gates

```
$ python3 -m pytest tests/docs/ -q
293 passed
EXIT=0

$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed
EXIT=0
```

---

## Authored-text proofs

```
$ sha256sum .agent/authored/f061-r4-1.md .agent/authored/f061-r4-2.md .agent/authored/f061-r4-3.md .agent/authored/f061-r4-4.md
1d12e62d274729984399ec5050b594c1be42f2dca56075a4505f277a23edec10  .agent/authored/f061-r4-1.md
c3a5bd8da1cb98c31ce26d6811c3b66a770c128fa6cb78c5e50d8d601c186165  .agent/authored/f061-r4-2.md
45212872599183cb674e4d2795395a0761e0d71b57361cca4cbbb9fbbbed152d  .agent/authored/f061-r4-3.md
0dbdb6eed0f24a458c3beaf33fc182fadf5d8fdb25579d11bdf7f9811d3f3876  .agent/authored/f061-r4-4.md
```

All four match their BEGIN-marker hashes.

**Transport wrap (R-0148), f061-r4-3:** its TO line arrived wrapped across
three lines. Both candidate forms were hashed before anything was written:

```
wrapped      28a2bf4956ebec25de3b8d510b8313e081ace0626f840c2e6946daefad546342
single-line  45212872599183cb674e4d2795395a0761e0d71b57361cca4cbbb9fbbbed152d  MATCH
```

The single-line form is therefore the authored text — the same resolution the
F056 r4-3 precedent recorded, decided by the hash rather than by appearance.

```
$ cmp .agent/authored/f061-r4-1.md .agent/live_review.md ; echo EXIT=$?
EXIT=0
```

**STATUS grep proof.** The FROM/TO strings were read out of the saved authored
file (`splitlines()[1]` and `[3]`), never retyped. Substituting the four
recorded values BACK into the applied line reproduces the authored TO line
byte-for-byte:

```
round-trip identical to authored TO line: True

FROM count after: 0
TO   count after: 1
$ git diff --numstat docs/roadmap/STATUS.md
1	1	docs/roadmap/STATUS.md
```

Applied line:

```
- [x] F061 — Definition-of-Done compiler (T001–T004 complete; accepted 2026-08-01 · live review PASS — ACCEPTED · Evidence job c5185517fa2443bf · package remedy-review-20260801-190945-READY_FOR_REVIEW.zip · SHA-256 486948228f6dd3413ba8cdd9947622b08b8803b40e9f7a0c7c547470150bcbd8 · accepted HEAD 8dc6086c4da87ca2ec63c33c3e17904c29ee394d)
```

**README grep proof** — both authored edits, each FROM gone and each TO present
exactly once:

```
FROM gone: True | TO once: True  <- 31 of 252 registered items accepted. Next: F062 (Product smoke as the closing gate).
FROM gone: True | TO once: True  <- | 1 | Self-Build Bootstrap | 15 | 22 |
$ git diff --numstat README.md
2	2	README.md
```

---

## Deviations & assumptions (A9)

1. **Accepted HEAD is `8dc6086c`, not commit 2 (`03df53fb`).** The block set
   accepted HEAD = commit 2, assuming no further content commit. The first
   evidence bundle, built at `03df53fb`, was rejected by the packaging
   validator because three R1-era parametrize cases produce node ids that read
   as local absolute paths (`…test_cwd_may_not_escape_the_worktree[/etc]`).

   I fixed the cause rather than working around it: the three cases now carry
   explicit ids (`absolute`, `parent-escape`, `nested-escape`). This is a
   genuine improvement — a node id embedding `/etc` is hostile to any tooling
   that scans a bundle for leaked paths — and it changes no assertion; the
   suite is still 154 passed.

   The protocol supports this ordering: "the zip is built from a clean tree
   after all CONTENT commits — the reviewed head the manifest records as
   accepted HEAD." Commit 3 is that content commit, so the zip, the manifest's
   `committed_review_subject.head_commit`, and the STATUS line all name
   `8dc6086c` consistently. **The reviewer should confirm this substitution**,
   since it changes a value the block specified.

   Rejected alternatives, both dishonest: narrowing the verification run to
   deselect the three tests (hiding evidence to satisfy a validator), or
   hand-editing the produced `verification_tests.json`.

2. **The rejected bundle was deleted before the rebuild**, and no zip was ever
   built from it — so there is no failed package to report, only a failed
   pre-zip validation, recorded above with its raw `blocking_reasons`.

3. **`output_hash` was deliberately omitted** from the verification runs so the
   producer derives it from the stored 2000-char `stdout_summary`. Supplying it
   by hand is exactly how the documented pitfall is hit.

4. **The "zip import check" was interpreted as an import smoke over the
   packaged sources**, since no dedicated import-check script exists in
   `scripts/`. I extracted the zip to a temporary directory, imported the four
   F061 modules from the packaged tree, confirmed `dod_v1` resolves there, and
   removed the directory. `testzip()` reported no bad member.

5. **`verdict: PASS_WITH_RISKS`** is what the manual-completion producer emits
   for an operator-attested bundle (its documented value for this path, matching
   the reference shape test) — it is not a new risk finding. Open findings
   remain 0; R-0164 and R-0165 are both Resolved.

6. **Evidence dir kept outside the repo** (session scratch), so it never enters
   the base..HEAD review subject — the F147 attempt-2 lesson. Nothing was
   committed from it; `git status --porcelain` stayed empty throughout.

7. **The pre-existing `dag_schedule.py` ruff error** (R3 deviation 5) is still
   present and still out of scope. It reproduces at base.

---

## Closure-candidate findings

None raised during this closure round.

---

## Runtime actuals

4 rounds (R1–R4) on 2026-08-01. R3 integration gate: branch 14900 passed / 19
skipped in 140.76s, base 14744 / 19 in 137.49s, both exit 0. Tokens/cost:
**not-measured** — the ledger has no per-round token record for this feature.

## Honest boundary

DoD compilation is **not yet wired into job creation**. The schema, compiler,
all five runners, the gate seam, the report matrix and the CLI are built and
proven; what does not exist yet is a production caller of `compile_dod` at real
job start. F062 registers the product-smoke standard check into the seam, and
F069/F070 wire compilation into the mission/orchestrator flow. The Built State
section records this in the feature file so the closure cannot be read as
claiming more than was built.
