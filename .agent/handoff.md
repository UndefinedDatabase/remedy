# Handoff — F115 · R20 (integration gate)

Deviations, declared: 100 lines against the 60-line cap (AGENTS.md DECISION D15). The cause is
mandated content, not prose — the R20 block ordered eleven gates a–k whose raw transcripts carry
two full `comm` outputs and per-id attribution for all 15 ids, plus four per-commit tables and the
authored-text proofs. No section is dropped.

## Range
Review of e7127c63..HEAD (branch feature/f115-prompt-cost-report).

## Commits
### 182e1625 chore(f115): save the R20 integration-gate block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f115-r20-1.md | +164/-0 | R20 block, BEGIN..END inclusive |
| .agent/last_block.md | +158/-134 | same bytes, cmp exit 0 |

### ce812bc0 docs(f115): record the R19 verdict, resolve R-0338, register R-0339
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +5/-1 | PAIR 1 rewrite + PAIR 2 append, committed BEFORE the gate ran |

### 8081982f chore(f115): commit the R20 integration-gate evidence
| Path | +/- | Reason |
|---|---|---|
| .agent/gate_f115_r20/ | +497/-0 | 25 .txt files: run tails, failed lists, comm outputs, serial re-runs, dist hashes, attribution, cleanup proof |

### this commit — chore(f115): refresh the plan and write the R20 handoff
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | rewrite | R19 PASS, R20 ran, blocker named, 12 open findings, next ID R-0340 |
| .agent/decisions.md | append | packager decision, registered as D7 (D4 was taken) |
| .agent/handoff.md | rewrite | this file |

## External actions
`git worktree add -b tmp/base-gate .remedy-wt/.cache/base_r20 0d6c97aa` → created, on a branch.
`git worktree remove --force` + `prune` + `git branch -D tmp/base-gate` → "Deleted branch tmp/base-gate (was 0d6c97aa)".
`git push -u origin feature/f115-prompt-cost-report` → run after the last commit. No PR, no merge, no other gh call.

## Verification
(a) `cmp .agent/authored/f115-r20-1.md .agent/last_block.md` → exit 0, no output.
(b) C1 gates raw: `Landed: R-0338` 0 · `^Done: R-0338` 1 · `^- R-0339 — Low` 1 · `^Gate: R19 — PASS` 1 · `^## Steps` 1.
(c) BRANCH, repo root, `python3 -m pytest -n auto -q`: `11 failed, 16700 passed, 19 skipped in 166.52s (0:02:46)`, EXIT_CODE=1, WALL 167s.
    FAILED = 5× test_role_conventions[reviewer] (R-0322) + 6× test_run_log_cli::TestPlanJobLocalRunLog.
(d) BASE at 0d6c97aa on tmp/base-gate, `REMEDY_UI_NO_AUTO_BUILD=1`: `13 failed, 16626 passed, 19 skipped in 128.26s`, EXIT_CODE=1, WALL 129s.
    `apps/ui/dist` aggregate hash before = after: base worktree `c7c847f9…`, primary `856780f4…` — no write-through in run 1.
    BASE run 2, same worktree, dist in place: `6 failed, 16633 passed`, exit 1, 136s.
(e) `comm -13` branch-only = 6, identical against base run1 and run1∪run2, all in
    `tests/test_run_log_cli.py::TestPlanJobLocalRunLog::` — test_plan_job_local_output_includes_log_path,
    test_planning_completed_noop_outcome, test_planning_completed_outcome_changed,
    test_planning_started_includes_provider_role_model, test_writes_planning_completed_on_success, test_writes_planning_started.
    `comm -23` base-only (union) = 9: 8 in `tests/ui_server/test_live_state.py::TestUIServerIntegration::` — test_api_invalid_token_403,
    test_api_requires_token, test_app_shell_served_without_token, test_brain_endpoint, test_dashboard_no_raw_leaks, test_put_rejected,
    test_readiness_endpoint, test_server_starts_and_writes_info — plus
    `tests/cli/test_review_bundle_runtime.py::TestSubprocessCleanup::test_timeout_raises_with_cleanup`.
    R-0322's five are in BOTH failed lists and NEITHER comm output, exactly as the block predicted.
(f) Attribution of all 15 ids — `.agent/gate_f115_r20/attribution.txt`:
    · branch-only 6: serial on branch 6/6 FAIL (exit 1); serial at merge base 6/6 PASS (exit 0) ⇒ reproducible,
      not xdist-flake, introduced here. **BLOCKER — no fix attempted.** Cause: cb17024a put
      `on_prompt_composed=_plan_compositions.append` on the call at apps/cli/commands/job.py:288 while the stub at
      tests/test_run_log_cli.py:78 is `def fake_plan_job_with_llm(job, _call_planner)`; TypeError → broad
      `except Exception` → sys.exit(1) at job.py:309. `git log 0d6c97aa..HEAD -- tests/test_run_log_cli.py` is EMPTY.
      F115's cover for that call site is a source-TEXT assert (test_structured_planner_cli.py:302) that reads the file
      instead of executing it, so it could not see the stale stub.
    · base-only 8: "ERROR: React UI not built" ×8 in the raw base log (ui_server.py:2848). Pass serially 8/8, pass under
      `-n auto` (42 passed), gone in base run 2 once apps/ui/dist is in place;
      `git diff 0d6c97aa HEAD -- packages/orchestration/ui_server.py apps/ui` is EMPTY.
    · base-only 1: passes serially at base AND on branch ⇒ base-side timing flake. No unattributed id remains.
(g) `git worktree list` → `/home/decodeux/Repos/remedy  ce812bc0 [feature/f115-prompt-cost-report]`, ONE line;
    `git branch --list tmp/base-gate` empty; base worktree path ABSENT.
(h) `ls .agent/gate_f115_r20/` → 25 files, all `.txt`, no `.log`; 497 lines total.   (i) `wc -l .agent/plan.md` → 46.
(j) `git status --porcelain` → VERBATIM, exactly one line: ` M scripts/make_review_zip.sh`.
(k) `git log --oneline e7127c63..HEAD` → the four commits tabled above.

## Authored-text proofs
R20 block: `cmp` exit 0; sha256 of both copies `e3a5535fe489cf89bfdee071c7f6a28fde755c7ac5817fcc4d94dc76c6d71d1d`; `wc -lc` 164 14809 both;
zero trailing-whitespace lines; first line `BEGIN BLOCK f115-r20-1`, last `END BLOCK f115-r20-1`.
PAIR 1's TO line, PAIR 2's R-0339 bullet and PAIR 2's `Gate: R19` line were EXTRACTED from the committed authored file and inserted
unmodified: each occurs exactly 1× in `.agent/live_review.md` and 1× in `.agent/authored/f115-r20-1.md`. PAIR 1's FROM occurs 0×.
DECISION D7's body is the block's decision text verbatim; only the heading and the ID note differ.

## Deviations & assumptions
1. **Decision ID.** The block ordered `DECISION F115 D4`; that ID has been taken since R8 ("the manifest gets its own table, not a
   ledger column"). A second D4 would corrupt the ledger, so the entry landed as **DECISION F115 D7** with an explicit ID note mapping
   the block's and the R19 verdict's "D4" onto it. Body verbatim; plan.md names D7.
2. **Gate evidence trimmed to procedure shape.** The four full run logs total 5305 lines; committing them would put one commit ~5.6k
   insertions over the AGENTS.md 500 cap. Committed is what integration_gate.md step 1 names — raw tail, full FAILED list, exit code,
   wall time — plus every comm output and serial result in full and the decisive tail of one blocker traceback.
   `full_log_provenance.txt` records each full log's line count and sha256. Nothing was re-run to a better number; every committed line
   is a verbatim slice. The commit is 497 insertions.
3. **A second base run was added** (not ordered) so base run 1's 8 ui_server reds could be shown non-genuine instead of explained away.
   Base failures are compared as run1 ∪ run2 — the conservative direction, which can only shrink the branch-only set. It did not: same
   6 ids. REPORTED, not charged to F115: `base_run2_env.txt` shows the base worktree's `apps/ui/dist/index.html` mtime moving
   12:57:29 → 13:03:20 during run 2 despite `REMEDY_UI_NO_AUTO_BUILD=1` — the R-0169 flag-ignored-by-a-spawned-build class, an
   observation about the gate harness.
No pass/fail count was predicted anywhere; every number above was measured after the fact.

## Next
Reviewer gates R20 and issues the gate verdict. The gate's finding is a BLOCKER: the repair — widening the stub at
tests/test_run_log_cli.py:78 — is its own reviewer-gated round, not this one.
