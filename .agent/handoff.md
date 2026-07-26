# Handoff — F034 Bundled clarification in the Flight Plan — CLOSED

Branch: feature/f034-bundled-clarification · PR #151 (NOT merged — the Open
PR Gate merges it at the next feature start)
Review range: 8027d48..HEAD (closure round)
Feature range: 34878f3..d1c036a (accepted HEAD = the pre-zip head the
package and verdict cover)
Open findings: 0. Next expected action: reviewer closure verdict / end of
Window 1.

## Closure facts

- Evidence job: `fd549b82-64b0-49c5-85d9-f5d8bf44a266`
- Evidence dir: `.data/evidence_exports/fd549b82-64b0-49c5-85d9-f5d8bf44a266`
- Package: `remedy-review-20260726-202004-READY_FOR_REVIEW.zip`
- SHA-256: `429e6243f9c4b7b4e5c3a7465b75c490ae9f9ff567f67401c742bff4f6c348c7`
- accepted HEAD: `d1c036ace9802d20bdb521e77905bdb7998c552e`
- LAST_REVIEWED_SHA: `8027d48`

## Item status

| Item | Status | Reason |
|------|--------|--------|
| Commit A — state files, repair verdict, closure opened | done | 2f74aee |
| Commit B — Built State in the feature file | done | d1c036a |
| Integrity check | done | PASS, 5/5 checks |
| Evidence job (T001–T004 attested) | done | validate_manual_completion -> [] |
| Review zip | done | READY_FOR_REVIEW, first attempt, no failures |
| Commit C — zip + evidence dir + handoff + STATUS line | done | this commit |
| PR #151 description | done | not merged, per protocol §6 |
| Canary | done | 42 passed |
| Production code | untouched | closure round changes no code |

## Commits (ordered, changed files with +/-)

### 2f74aee chore(f034): persist repair-round verdict; open closure
| File | + | - |
|------|---|---|
| .agent/live_review.md | 8 | 1 |
| .agent/plan.md | 8 | 6 |

### d1c036a docs(f034): built state in the feature file
| File | + | - |
|------|---|---|
| docs/roadmap/features/T1_F034.md | 93 | 0 |

### (this commit) chore(f034): close F034 — evidence job, review package, STATUS line
| File | Change |
|------|--------|
| docs/roadmap/STATUS.md | 1 line (F034 only, `[~]` -> `[x]`) |
| .agent/handoff.md | rewritten |
| remedy-review-20260726-202004-READY_FOR_REVIEW.zip | added (7.9M) |
| .data/evidence_exports/fd549b82-.../** | added (force-added; `.data/` is gitignored at .gitignore:211, same as the F016 precedent) |

## Zip build attempts

ONE attempt, succeeded. No failed attempts to report.

    $ bash scripts/make_review_zip.sh --evidence-dir .data/evidence_exports/fd549b82-64b0-49c5-85d9-f5d8bf44a266
    {"member_count": 1469, "authoritative_count": 13, "symlink_count": 0,
     "tombstone_count": 0,
     "final_path": "remedy-review-20260726-202004-READY_FOR_REVIEW.zip",
     "final_sha256": "429e6243f9c4b7b4e5c3a7465b75c490ae9f9ff567f67401c742bff4f6c348c7",
     "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW",
     "evidence_authoritative": true, "review_subject_alignment": "PASS",
     "manifest_sha256": "d36653c4ca5632ce6ee73ff961059be98e4c61fa36364f05772b03c67d1ad314"}
    ============================================
    REVIEW_PACKAGE_CREATED=true
    PACKAGE_STATUS=READY_FOR_REVIEW
    REVIEW_SUBJECT_ALIGNMENT=PASS
    EVIDENCE_AUTHORITATIVE=true
    ============================================
    ZIP_EXIT=0

committed_review_subject read back out of the built zip
(`.review_zip_manifest.json`):

    base: 34878f34a3374d73fd8e5b8dbc8eb2192f46b781
    head: d1c036ace9802d20bdb521e77905bdb7998c552e
    package_status: READY_FOR_REVIEW

    $ sha256sum remedy-review-20260726-202004-READY_FOR_REVIEW.zip
    429e6243f9c4b7b4e5c3a7465b75c490ae9f9ff567f67401c742bff4f6c348c7  remedy-review-20260726-202004-READY_FOR_REVIEW.zip

Evidence-dir ordering honoured: the dir was built and validated, the zip was
built from the clean pushed tree, and only then was the dir committed (F147
lesson).

## Integrity check (raw)

    $ python3 -m apps.cli.main integrity check --json
    {
      "version": 1, "passed": true, "fail_count": 0, "check_count": 5,
      "checks": [
        {"name": "handler_import", "status": "pass", "message": "handlers=307"},
        {"name": "live_review_verdict", "status": "pass", "message": "- Round 1 (Setup+T001–T004, 34878f3..0891b8d): PASS."},
        {"name": "plan_consistency", "status": "pass", "message": "unchecked=1, context_complete=False"},
        {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
        {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
      ]
    }
    exit=0

## Evidence bundle

    validate_manual_completion(ev) -> []
    ERROR_COUNT = 0

Bundle summary from the producer:

    {"job_id": "fd549b82-64b0-49c5-85d9-f5d8bf44a266",
     "head_commit": "d1c036ace9802d20bdb521e77905bdb7998c552e",
     "authority_count": 13, "partition": {"T001": 4, "T002": 4, "T003": 4, "T004": 1},
     "commit_count": 13, "verdict": "PASS_WITH_RISKS", "manual_completion": true,
     "operator_attested_tasks": ["T001", "T002", "T003", "T004"],
     "total_passed": 220}

Two producer pitfalls hit and fixed before packaging (both surfaced by
`validate_manual_completion`, neither reached the zip):

1. `run_id` must match `^vr-\d{4,}$` — `vr-f034-slice` was rejected;
   renamed to `vr-0001`…`vr-0004`.
2. `node_ids` must list every selected test (count == `selected`), and
   `test_files` must be sorted. Node ids were collected for real via
   `pytest --collect-only -q` per run; counts matched the pass counts
   exactly (67 / 6 / 42 / 105).

A third was hit at build time: an explicit `task_partition` must cover the
attestable authority set EXACTLY. A hand-written file list would drift, so
the producer derives the partition from the real review subject.

## Verification runs recorded in the bundle (raw)

    $ python3 -m pytest tests/orchestration/test_bundled_clarification.py tests/cli/test_decision_answers.py -q
    67 passed in 0.66s          exit=0

    $ python3 -m pytest tests/test_no_interactive_guard.py -q
    6 passed in 0.82s           exit=0

    $ python3 -m pytest tests/cli/test_golden_path.py -q
    42 passed in 18.95s         exit=0

    $ python3 -m pytest tests/cli/test_plan_approval.py tests/orchestration/test_flight_plan.py tests/schemas/ -q
    105 passed in 4.21s         exit=0

**Discrepancy to note:** the closure brief listed this last run as
"plan_approval+flight_plan+schemas (100)". The real count at this head is
**105** (test_plan_approval 27 + test_flight_plan 29 + test_flight_plan_schema
23 + test_job_intake 26). No combination of those files yields 100. The
bundle records 105 — the number actually observed — not the briefed 100.

## Byte-identity proofs of applied authored text

STATUS line (the four `<…>` fields masked back out, then diffed against the
authored block):

    $ diff authored_status.txt applied_status_masked.txt
    IDENTICAL — byte-for-byte, modulo the four filled fields

Repair-round verdict in .agent/live_review.md:

    $ diff authored_verdict.txt applied_verdict.txt
    IDENTICAL — byte-for-byte

    $ grep -n "^LAST_REVIEWED_SHA:" .agent/live_review.md
    4:LAST_REVIEWED_SHA: 8027d48

One deliberate formatting decision: the authored STATUS line arrived wrapped
across two lines in the brief. Every accepted line in STATUS.md (F017, F018,
F146, F081) is a single line, and the protocol §4 template is single-line, so
it was applied as one line. No characters were added, removed, or reordered.

## Canary (raw)

    $ python3 -m pytest tests/cli/test_golden_path.py -q
    ..........................................                               [100%]
    42 passed in 18.90s
    exit=0

## Residual risks carried into closure (PASS_WITH_RISKS)

1. The interactive-input guard covers `packages/` only — `apps/cli` stays
   deliberately interactive-capable. Runner entry points live in
   `packages/`, which is what is guarded.
2. Conditional-answer predicates skipped as OPTIONAL scope
   (`.agent/decisions.md`). No DONE criterion depends on them.
3. Pre-existing full-suite nondeterminism: base is RED by 197 tests;
   branch-vs-base attribution showed zero F034-attributable regressions.
   Backlog F135/F052.

## Not done, by protocol

PR #151 is NOT merged. Protocol §6: the closure PR merges at the next
feature's start via the Open PR Gate, and the gap is the operator's
manual-review window.
