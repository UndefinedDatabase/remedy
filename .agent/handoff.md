# Handoff — F104 Hard budget enforcement, R8 (CLOSURE)

Feature F104, round **R8 — CLOSURE**, branch `feature/f104-hard-budget-enforcement`,
one-session self-drive, one delegated worker. Closure executed per
docs/roadmap/STATUS_closure_protocol.md. **Nothing was merged.**

**Two values cannot live in this file** (F103 R8 / F080 R5 precedent): this closure
commit's OWN SHA and the PR number/URL. The file is INSIDE the closure commit and
the PR is created after it; recording either would need a commit after the STATUS
edit, which Rule A4 forbids. Both are in the completion report, as is the
post-commit `git status --porcelain`.

## Closure values, as written into the STATUS line
Evidence job **f104-closure** · package
**remedy-review-20260809-033908-READY_FOR_REVIEW.zip** · SHA-256
**6117b6b02ca6f641f0ef3bfebe7518d0eaf705e609e17e8ee9493e6d7fd8bb6a** ·
accepted HEAD **68a7412019e92232a880625b7fce4e48c7198744** (= 68a74120, the head
after the three CONTENT commits, which is what the zip covers). Verdict
**PASS_WITH_RISKS — ACCEPTED**, accepted 2026-08-09.

## Range
Review of `103a854d..HEAD` (HEAD = this closure commit). `LAST_REVIEWED_SHA` is
still **549f2bac**: R6, R7 and now R8 all await the reviewer.

## Commits

### 39f61766 chore(f104): save the R8 closure block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f104-r8-1.md | +190 | the R8 block, verbatim (item 1) |
| .agent/last_block.md | +184/-134 | same bytes; replaces the R7 block |

### 9008334e chore(f104): apply the reviewer resolution for R-0227 and the R8 step
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +20/-13 | reviewer's `Done: R-0227` replaces the worker's placeholder; R8 line appended to `## Steps` |

### 68a74120 docs(f104): add the Built State section to the feature file
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F104.md | +44 | `## Built State`, verbatim (item 3, precondition 4) |

### (this commit) docs(f104): accept F104 in the roadmap ledger and sync the readme
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | +1/-1 | `[~]` → `[x]` with the four recorded values |
| README.md | +2/-2 | 40→41 accepted, Tier 2 2→3 (R-0154: same commit as STATUS) |
| .agent/plan.md | rewrite | closed state, 47 lines |
| .agent/context.md | +4/-4 | F104 now `[x]`; R8 marked done |
| .agent/handoff.md | rewrite | this file (template self-reference exception) |

`.agent/candidates.md` deliberately untouched — I raise no new closure candidates.

## External actions
`git push -u origin feature/f104-hard-budget-enforcement` → `103a854d..68a74120`,
before the zip build, tree clean. `bash scripts/make_review_zip.sh --evidence-dir
.remedy-wt/f104_closure_evidence/remedy-job-evidence-f104-closure` → exit 0. A
second push and the `gh pr create` follow this commit; both are in the completion
report. No merge, no force-push, no worktree added or removed this round.

## Artifact-build attempts (every attempt, including failures)
| # | Artifact | Command | Outcome |
|---|---|---|---|
| 1 | evidence bundle | `create_manual_completion_bundle(review_feature_id="f104", …)` into `.remedy-wt/f104_closure_evidence/remedy-job-evidence-f104-closure` | **exit 0**, first attempt, no failure. verdict PASS_WITH_RISKS, manual_completion true, authority 17 files, partition T001 6 / T002 6 / T003 5, 56 commits, total_passed 546 |
| 2 | bundle pre-check | coordinator's own evaluation over the produced bytes | gate matrix ok **True** (no blocking reasons), manual-completion problems **[]**, `is_valid_current_run` **True**, final-verifier repro **VERIFIED_EQUAL**, token-truth authority **VERIFIED_EQUAL** |
| 3 | review zip | `scripts/make_review_zip.sh --evidence-dir …` | **exit 0**, first attempt, no failure. `PACKAGE_STATUS=READY_FOR_REVIEW`, `REVIEW_SUBJECT_ALIGNMENT=PASS`, `EVIDENCE_AUTHORITATIVE=true`, 2403 members, 11M |
| 4 | zip import check | `zipfile.testzip()` + manifest read | bad member **None**; `.review_zip_manifest.json` reads `package_status=READY_FOR_REVIEW`; `committed_review_subject` = base `94f69b0fc25fd20b2d26d1164f5dd73cac3071e1` → head `68a7412019e92232a880625b7fce4e48c7198744`, `base_is_ancestor true`, 56 commits, 57 files — spans BASE..HEAD |
| 5 | zip hash | `sha256sum` of the zip on disk | `6117b6b02ca6f641f0ef3bfebe7518d0eaf705e609e17e8ee9493e6d7fd8bb6a` — matches the `final_sha256` the script printed |

No attempt failed and nothing was retried; the evidence dir lives only in the
gitignored `.remedy-wt/` and is NOT committed.

## Verification
Run by me from the repo root, real exit codes:

| Gate | Command | Exit | Result |
|---|---|---|---|
| A | `python3 -m pytest tests/docs/ -q` | **0** | 294 passed in 0.25s (re-run after the STATUS/README edit: **0**, 294 passed in 0.31s) |
| B | `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) | **0** | 42 passed in 19.50s |
| C | `python3 -m pytest tests/orchestration/test_job_budgets.py tests/orchestration/test_predictive_budget.py -q` | **0** | 210 passed in 32.28s |
| D | `remedy integrity check --json` | **0** | `"passed": true, "fail_count": 0, "check_count": 5` — handler_import (handlers=328), live_review_verdict, plan_consistency (unchecked=0), relevant_untracked (untracked=0, relevant=0), high_blockers_open (no open blocker/high findings) all `pass` |

Preconditions confirmed before the zip: tree clean (`git status --porcelain`
empty), branch pushed, zero relevant untracked files, Built State section present.

## Authored-text proofs
`cmp .agent/authored/f104-r8-1.md .agent/last_block.md` → **exit 0**.
STATUS line: the applied line equals the block's template with ONLY the four
angle-bracket slots filled — expected and applied both sha256
`6aaa0d1b5bd2633abc8ef21af7b01eb28fa77497bdf62accd3fd9c502f1666bd`, **equal**.
R-0227 resolution: 13 authored lines vs 13 applied lines, **byte-identical**, both
sha256 `a8630afa3cb8cb2684b5d2b6e77ab240e095772e7b8ee2b30d65e761e78aace2`; the
finding text above it is untouched and a blank line follows, as authored.

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 save the block | done | cmp exit 0 |
| 2 R-0227 resolution + R8 step | deviated | the block says to replace `  OPEN.`; that line no longer existed — see D1 |
| 3 Built State | done | appended verbatim; tests/docs/ green |
| 4 preconditions | done | no file changed, so no commit (as the block allows) |
| 5 evidence job | done | `f104-closure`, canonical producer, in `.remedy-wt/` |
| 6 review zip | done | READY_FOR_REVIEW, first attempt |
| 7 closure commit | done | this commit; exactly STATUS/README/.agent state |
| 8 the PR | done | created after this commit, NOT merged — number/URL in the completion report |

## Open findings
**1** — R-0221 (Low, carried, F252 flake-debt class, not F104's code to fix).
R-0222, R-0223, R-0224, R-0225, R-0226, R-0227 are all Resolved with
reviewer-authored text.

## Deviations & assumptions — declared
- **D1 (item 2).** The block orders "REPLACE the single line `  OPEN.` that
  currently terminates the R-0227 finding". No such line exists: the R7 worker
  already replaced it with its own placeholder `Done: R-0227` paragraph
  (commit 103a854d, `-1/+13`). I replaced THAT placeholder with the reviewer's
  authored text, which is the block's stated intent ("the finding text above it
  is untouched") and is the one `Done:` text the Constraints section exempts.
  The finding text itself (lines 112-127) is byte-unchanged.
- **D2 (item 2).** The R8 `## Steps` entry was de-indented by 2 to sit at column 0
  like R1-R7, exactly as the R7 block's Steps entry was applied (103a854d). The
  R-0227 resolution needed no shift — the block authored it at the file's own
  2-space continuation indent. Only the STATUS line and the R-0227 text carry a
  byte-identity obligation, and both are proven above.
- **D3 (item 5).** The bundle's verification records carry the three CLEAN SCOPED
  suites (budget 210 / canary 42 / docs 294, `len(node_ids) == selected` for each,
  `test_files` are FILES), never a full-suite list — closure-protocol pitfall (d).
  The full-suite proof rides in the committed `.agent/gate_f104_r7/`.
- **D4.** `remedy` on PATH is not invocable from this harness; every run went
  through `python3 -c "from apps.cli.grouped import main"`, the same entry point
  `pyproject.toml` binds the console script to. Real exit codes throughout.
- **D5.** The review zip includes 145 members from the gitignored `.remedy-wt/`
  (including the fresh evidence dir). That is pre-existing packaging behaviour —
  earlier scratch dirs are in previous packages too — and it did not affect the
  review subject: alignment PASS, evidence authoritative, 57 subject files.
- **This handoff is 145 lines** (AGENTS.md D15 stated cause): four per-commit
  changed-files tables, the closure-values block, the five-row artifact-attempt
  table the closure protocol mandates, the gate table, the two byte-identity
  proofs, the eight-row item-status table and five declared deviations. No
  section dropped.

## Next
Reviewer re-reads `549f2bac..HEAD` and re-runs gates A-D, then either accepts the
closure or authors a `[!]` line. The closure PR merges at the NEXT feature's start
via the Open PR Gate — never in this session.
