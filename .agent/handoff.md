# Handoff — F046 Multi-cycle loop — CLOSED

Branch: feature/f046-multi-cycle-loop · PR #152 (NOT merged — the Open PR
Gate merges it at the next feature start)
Closure range: `994398c..HEAD` · Feature range: `c14a83a..HEAD`
accepted HEAD: `0216d871290362d4ee81a80c767aa4ba1d2bb985` (Commit B — the
pre-zip head the package and verdicts cover)
LAST_REVIEWED_SHA: `994398c` · Open findings: 0 (R-0145 resolved by this
handback). Next expected action: reviewer closure verdict / end of Window 1.

## Closure facts

- Evidence job: `b4df73c4-f867-4869-b097-62aab0e6974f`
- Evidence dir: `.data/evidence_exports/b4df73c4-f867-4869-b097-62aab0e6974f`
- Package: `remedy-review-20260726-215057-READY_FOR_REVIEW.zip`
- SHA-256: `8dfb264f92b3736a9a58bb5df82693f543fc5877a9b907a897bfb53a54ab7f90`
- committed_review_subject (read back OUT of the built zip):
  base `c14a83a2d38cf8b91870f4c7bae225effb26f1af`,
  head `0216d871290362d4ee81a80c767aa4ba1d2bb985`, file_count 13

## Item status

| Item | Status | Reason |
|------|--------|--------|
| Commit A — gate verdict + R-0145 persisted | done | add00a2 |
| Commit B — Built State | done | 0216d87 |
| Preconditions (integrity, clean tree, pushed) | done | raw output below |
| Evidence job | done | attempt 2 of 2 — attempt 1 recorded verbatim below |
| Review zip | done | attempt 1 of 1, READY_FOR_REVIEW |
| Commit C — STATUS + handoff + zip + evidence dir | done | this commit |
| PR #152 updated (not merged) | done | action reported below |

## Every commit in the closure range (R-0145 predicate 1)

Listed in full, including the round-1 handback commit whose omission the
finding names. `65fbdba` predates the closure range (it sits in the gate
range `d87a3e0..994398c`) and is listed here because R-0145 says it went
unreported.

**65fbdba** chore(f046): plan, decisions and round-1 handoff *(gate range — the omitted one)*

| file | +/- |
|------|-----|
| .agent/decisions.md | +16 −0 |
| .agent/handoff.md | +116 −189 |
| .agent/plan.md | +4 −3 |

**1055ae0** chore(f046): persist the round-1 reviewer verdict; open the integration gate

| file | +/- |
|------|-----|
| .agent/live_review.md | +19 −2 |
| .agent/plan.md | +1 −3 |

**994398c** chore(f046): integration-gate results; restore plan.md Next Steps

| file | +/- |
|------|-----|
| .agent/decisions.md | +14 −0 |
| .agent/handoff.md | +127 −94 |
| .agent/plan.md | +4 −0 |

**add00a2** chore(f046): persist gate verdict and finding R-0145; open closure *(Commit A)*

| file | +/- |
|------|-----|
| .agent/live_review.md | +30 −2 |
| .agent/plan.md | +3 −2 |

**0216d87** docs(f046): built state in the feature file *(Commit B — accepted HEAD)*

| file | +/- |
|------|-----|
| docs/roadmap/features/T1_F046.md | +103 −0 |

**HEAD** chore(f046): close F046 — STATUS line, evidence job, review package *(Commit C)*

| file | +/- |
|------|-----|
| docs/roadmap/STATUS.md | +1 −1 |
| .agent/plan.md | +1 −1 |
| .agent/handoff.md | rewritten |
| remedy-review-20260726-215057-READY_FOR_REVIEW.zip | new (7.9M) |
| .data/evidence_exports/b4df73c4-…/** | new (force-added) |

Earlier feature-range commits (already tabled in previous handoffs):
`c6e2389` Setup, `a4a6874` T001, `8ad17ce` T002 evidence+config,
`d87a3e0` T002 CLI.

## Every external action taken (R-0145 predicate 2)

| # | action | when | result |
|---|--------|------|--------|
| 1 | `gh pr merge 151 --merge --delete-branch` | feature start, Open PR Gate | F034 merged, main at c14a83a |
| 2 | `git push -u origin feature/f046-multi-cycle-loop` | round-1 handback | new remote branch |
| 3 | **`gh pr create` → PR #152** | round-1 handback | created (AGENTS.md PR workflow); previously stated as a fact, never reported as an action — the R-0145 omission |
| 4 | `git push` | gate handback | 994398c pushed |
| 5 | `git push` | closure, after Commit B | 0216d87 pushed (pre-zip, clean tree) |
| 6 | `git push` | closure, after Commit C | STATUS/zip/evidence pushed |
| 7 | **`gh pr edit 152 --title --body`** | closure | PR description replaced with the final closure text; NOT merged |

No other remote or outbound action was taken this feature.

## Byte-identical proof for reviewer-authored text

The three authored blocks were saved to disk exactly as pasted and compared
as substrings against the files they were applied to — not eyeballed:

```
$ python3 - <<'PY'
... block in live_review.md / STATUS.md ...
PY
authored_finding: IDENTICAL (substring present verbatim)
authored_verdict: IDENTICAL (substring present verbatim)
STATUS line: IDENTICAL
```

```
$ grep -n "^- \[x\] F046" docs/roadmap/STATUS.md
31:- [x] F046 — Multi-cycle loop (T001–T002 complete; accepted 2026-07-26 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job b4df73c4-f867-4869-b097-62aab0e6974f · package remedy-review-20260726-215057-READY_FOR_REVIEW.zip · SHA-256 8dfb264f92b3736a9a58bb5df82693f543fc5877a9b907a897bfb53a54ab7f90 · accepted HEAD 0216d871290362d4ee81a80c767aa4ba1d2bb985)
$ git diff --numstat -- docs/roadmap/STATUS.md
1       1       docs/roadmap/STATUS.md
```

One line inserted, one removed — no other STATUS line touched. (A first
attempt at this proof used `grep -c "^[+-][^+-]"` on the diff and reported
0; the pattern is wrong for a line whose own content begins with `- `, so
the numstat above is the proof that stands.)

The four `<…>` fields were the only substitutions into the authored STATUS
template; the wrapped two-line paste was applied as ONE line per the
instruction.

## Preconditions — raw output

```
$ python3 -m apps.cli.main integrity check --json
{
  "version": 1,
  "passed": true,
  "fail_count": 0,
  "check_count": 5,
  "checks": [
    {"name": "handler_import",      "status": "pass", "message": "handlers=308"},
    {"name": "live_review_verdict", "status": "warn", "message": "no verdict found"},
    {"name": "plan_consistency",    "status": "pass", "message": "unchecked=1, context_complete=False"},
    {"name": "relevant_untracked",  "status": "pass", "message": "untracked=0, relevant=0"},
    {"name": "high_blockers_open",  "status": "pass", "message": "no open blocker/high findings"}
  ]
}
EXIT=0
```

`passed: true`, exit 0. Reported honestly rather than glossed: the
`live_review_verdict` check emits **warn — "no verdict found"** even though
two PASS verdicts are present; it is a warn (not a fail), it did not affect
`passed`, and its matcher appears not to recognise this file's verdict
format. Not investigated in a closure round; worth a backlog gap item.

```
$ git status --short          # (no output — clean)
$ git log --oneline -1
0216d87 docs(f046): built state in the feature file
$ git status -sb
## feature/f046-multi-cycle-loop...origin/feature/f046-multi-cycle-loop
```

## Evidence job — 2 attempts, first one recorded

**Attempt 1** (job `ac6bb034-…`) — bundle built, then REJECTED by its own
validation before any zip was attempted:

```
validate_manual_completion: ['verification_tests.json runs[0] has the wrong field set',
                             'verification_tests.json runs[1] has the wrong field set']
gate_matrix ok: False ['final_verifier_report.json test_status.passed cannot be confirmed: the
 VerificationTests total is missing or invalid', 'verification_tests.json runs[0] has the wrong
 field set', 'verification_tests.json runs[1] has the wrong field set']
```

Cause: the v1.1.0 run field set requires exactly 14 keys; the runs were
missing `duration_seconds` and carried a non-schema `base_commit`. Directory
deleted, not patched.

**Attempt 2** (job `b4df73c4-f867-4869-b097-62aab0e6974f`) — clean:

```
{"authority_count": 8, "commit_count": 9,
 "head_commit": "0216d871290362d4ee81a80c767aa4ba1d2bb985",
 "job_id": "b4df73c4-f867-4869-b097-62aab0e6974f", "manual_completion": true,
 "operator_attested_tasks": ["T001", "T002"], "partition": {"T001": 2, "T002": 6},
 "total_passed": 91, "verdict": "PASS_WITH_RISKS"}

validate_manual_completion: []
gate_matrix ok: True []
```

Producer: `job_evidence.create_manual_completion_bundle(review_feature_id="f046", …)`.
Pitfalls honored: run ids `vr-0001`/`vr-0002` (`^vr-\d{4,}$`); `node_ids`
collected via `pytest --collect-only -q` and `selected == len(node_ids)`
(49 and 42); sha256-hex `output_hash` over the real stdout; full-length
`base_commit`/`head_sha`; `task_partition` derived from
`resolve_review_subject` + `is_attestable_source` and asserted equal to the
authority set before the call (the script raises otherwise).

Partition (8 attestable files):

| task | files |
|------|-------|
| T001 | packages/orchestration/long_run_executor.py, tests/orchestration/test_long_run_executor.py |
| T002 | apps/cli/command_catalog.py, apps/cli/commands/job.py, packages/orchestration/config.py, docs/system/remedy-toml-configuration-system-v0.md, docs/roadmap/STATUS.md, docs/roadmap/features/T1_F046.md |

Scoping note, stated not hidden: the two roadmap docs are closure artifacts
rather than T002 work; with only T001/T002 attestable they were placed in
T002 (the docs-carrying slice) so the partition covers the authority set
exactly, as the producer requires.

Verification runs recorded in the bundle (both re-run fresh at closure):

```
$ python3 -m pytest tests/orchestration/test_long_run_executor.py -q
49 passed in 0.24s          exit=0
$ python3 -m pytest tests/cli/test_golden_path.py -q
42 passed in 18.91s         exit=0
```

## Review zip — 1 attempt

```
$ bash scripts/make_review_zip.sh --evidence-dir .data/evidence_exports/b4df73c4-f867-4869-b097-62aab0e6974f
{"member_count": 1445, "authoritative_count": 8, "symlink_count": 0, "tombstone_count": 0,
 "final_path": "remedy-review-20260726-215057-READY_FOR_REVIEW.zip",
 "final_sha256": "8dfb264f92b3736a9a58bb5df82693f543fc5877a9b907a897bfb53a54ab7f90",
 "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW",
 "evidence_authoritative": true, "review_subject_alignment": "PASS",
 "manifest_sha256": "64f71e86351a06f7119f553ce4e5c1afb43c15e04f046689370cf4951ba8f2b8"}
============================================
REVIEW_PACKAGE_CREATED=true
PACKAGE_STATUS=READY_FOR_REVIEW
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
ZIP_PATH=/home/decodeux/Repos/remedy/remedy-review-20260726-215057-READY_FOR_REVIEW.zip
============================================
$ sha256sum remedy-review-20260726-215057-READY_FOR_REVIEW.zip
8dfb264f92b3736a9a58bb5df82693f543fc5877a9b907a897bfb53a54ab7f90
```

Read back out of the built zip (`.review_zip_manifest.json`):
`package_status: READY_FOR_REVIEW`, committed_review_subject
base `c14a83a2d38cf8b91870f4c7bae225effb26f1af` →
head `0216d871290362d4ee81a80c767aa4ba1d2bb985`, file_count 13.
Build order honored: tree clean and pushed at Commit B, zip built, evidence
dir committed only afterwards (F147 lesson).

## Canary

```
$ python3 -m pytest tests/cli/test_golden_path.py -q
..........................................                               [100%]
42 passed in 18.91s
exit=0
```

## Runtime actuals

| metric | value |
|--------|-------|
| rounds | 3 (build, integration gate, closure) |
| commits on the branch | 9 |
| provider calls / tokens / cost | **not-measured** — zero-provider feature; the evidence bundle's token truth is `character_heuristic`, `provider_call_count: 0` |
| full-suite wall clock | branch 161.28s, base 196.88s |
| slice suite | 49 tests, 0.24s |
| package | 1445 members, 8 authoritative, 7.9M |

## Carried risks

1. The conductor writes no postmortem record itself — stopped/budget classes
   derive at evidence export from the job status it sets (revisit for F053).
2. The multi-cycle CLI branch is unreachable while `CYCLE_SAFETY_CAP == 1`;
   exercised in tests with the cap raised.
3. Full-suite nondeterminism (F135/F052): base is RED by 179 tests.
4. Three pre-existing `.agent` state-file contract failures fail identically
   on base and branch — backlog gap item, deliberately not swept up.
5. `integrity check`'s `live_review_verdict` matcher reports warn "no verdict
   found" against a file holding two verdicts — backlog gap item.
