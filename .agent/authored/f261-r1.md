── STEP T001/1 — F261 — ROUND 1 ──
Goal: Claim F261, cut its branch, re-point the state files, re-head the review record, book
F275's round 110 verdict, resolve R-0889, register R-0890 from the closure candidate, rule
DECISION F261 D1, and land T001's first rename, `do job-evidence` to `job evidence`.

Base: `main` at `7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.
This is SESSION 1 of F261. Read first, and trust nothing below that you can read yourself:
AGENTS.md, docs/agents/self_drive_protocol.md, docs/roadmap/features/T2_F261.md.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block is a run
of a single repeated character, and every box-drawing rule inside the STEP and SLICE header
lines is exactly two characters long.

ENVIRONMENT, so you do not rediscover it:
- `VAR=x cmd`, `env VAR=x cmd` and `export` are denied: set environment in-process. `cp` is
  denied: copy with `shutil.copyfile`. Bare `ruff` is denied: use `python3 -m ruff check`.
- Shell loops, `$(...)` and `$?` inside a compound command are refused by form: write such
  checks as small Python scripts under `.remedy-wt/f261r1w/`. A pipe into `tail` hides pytest's
  exit code: redirect to a file instead.
- The editable install resolves `apps` and `packages` to the PRIMARY checkout. A pytest run
  inside a worktree therefore goes through a runner script that changes into the worktree, puts
  it first on `sys.path` and in `PYTHONPATH`, and asserts that `apps.cli.command_catalog` loaded
  from inside the worktree before it calls `pytest.main`.

## Bundle — the ordered commit sequence

C0a Cut `feature/f261-cli-vocabulary-v2` from `main` at the base, then save the block file the
    delegating message names as `.agent/authored/f261-r1.md` with `shutil.copyfile`.
C0b `.agent/last_block.md`, the same bytes, with `shutil.copyfile`.
C1  `.agent/plan.md` becomes slice PLAN1.
C2  THE RECORD, one commit: in `.agent/live_review.md` everything before the `## Findings` line
    becomes slice HEAD1 and slice RECORD1 is appended at the end; slice DEC1 is appended to
    `.agent/decisions.md`; pairs PC, PA and PD are applied.
C3  THE CLAIM: pair PS is applied, and `.agent/context.md` becomes slice CTX1.
C4  THE RENAME, per SPEC S, with slice TEST1 appended to `tests/test_command_catalog.py`.
C5  `.agent/handoff.md`, the handback; then `git push -u origin feature/f261-cli-vocabulary-v2`.
    No pull request is created in this round.

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3.

## Change — exactly these paths and no others

C0a to C3: `.agent/authored/f261-r1.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md`, `.agent/candidates.md`,
`docs/roadmap/features/T2_F273.md`, `docs/roadmap/features/T2_F261.md`,
`docs/roadmap/STATUS.md` and `.agent/context.md`. C4: the paths SPEC S names. C5:
`.agent/handoff.md`.

## The pairs — each FROM slice occurs exactly once in its target at the base

PC `.agent/candidates.md`: FROM slice PC-FROM, TO slice CAND1. The containment test printed
   `TO contains FROM: false`, so a REWRITE: after it FROM occurs 0 times and TO once.
PA `docs/roadmap/features/T2_F273.md`: FROM slice PA-FROM, TO slice ACC1. `TO contains FROM:
   true`, so APPEND-shaped: proved by whole-file equality, with no FROM-zero count.
PD `docs/roadmap/features/T2_F261.md`: FROM slice PD-FROM, TO slice AMEND1. `TO contains FROM:
   true`, so APPEND-shaped, proved the same way.
PS `docs/roadmap/STATUS.md`: FROM slice PS-FROM, TO slice STATUS1. `TO contains FROM: false`,
   so a REWRITE: after it FROM occurs 0 times and TO once.

THE RECORD'S EDGES. The text `## Findings` also occurs inside the header's own blockquote, so
the head swap splits on the line-anchored expression `^## Findings$` in multi-line mode, which
matches exactly once; the bytes from that line to the end of the file are carried forward
unchanged. HEAD1 ends with its own blank line. RECORD1 and DEC1 each begin with an empty line,
and both targets end in a newline at the base: an append is the file's bytes followed by the
slice's bytes, and nothing else.

## SPEC S — the rename, C4

A rename only: no flag, output or behaviour changes except where output prints the command's own
name. The handler stays in `apps/cli/commands/do_cmd.py`, registered under the new id.
S1 `apps/cli/command_catalog.py`: every `"do.job-evidence"` becomes `"job.evidence"`; in that
   entry `group_id="do",` becomes `group_id="job",` and `subcommand="job-evidence",` becomes
   `subcommand="evidence",`, edited in place.
S2 `apps/cli/commands/do_cmd.py`: `_cmd_do_job_evidence` becomes `_cmd_job_evidence` at its
   definition and in the handler table; every `"do.job-evidence"` becomes `"job.evidence"`;
   every `do job-evidence` becomes `job evidence`; and `so job-flow and job-evidence produce one`
   becomes ``so `do job-flow` and `job evidence` produce one``. The bare `"job-evidence"` step
   labels of `do job-flow` are NOT touched.
S3 Every `do job-evidence` becomes `job evidence` in `packages/orchestration/job_evidence.py`,
   `scripts/make_review_zip.sh`, `tests/cli/test_do_job_flow_review_base.py`,
   `tests/orchestration/test_stream_export_e2e.py` and `tests/orchestration/test_token_ledger.py`.
S4 `packages/orchestration/pingpong_job.py`: `` `job-evidence` `` becomes `` `job evidence` ``.
S5 `tests/orchestration/test_evidence_index.py`: every `_cmd_do_job_evidence` becomes
   `_cmd_job_evidence`. `tests/orchestration/test_job_evidence.py`: every `"do.job-evidence"`
   becomes `"job.evidence"`, and `# job-evidence now executes` becomes
   `# job evidence now executes`. `tests/orchestration/test_review_zip_hygiene.py`:
   `assert "do job-evidence" in proc.stderr` becomes
   `assert "To index: 'job evidence'." in proc.stderr`.
S6 `docs/system/vocabulary.md`: the text
   `` `job evidence <id>` after F261; today `do evidence` and `do job-evidence` `` becomes
   `` `job evidence <id>`; `do evidence` until F261 deletes it ``.
S7 Slice TEST1 is appended to `tests/test_command_catalog.py`, which ends in a newline at the
   base. Nothing else changes.

## Constraints

1. NO SLICE IS EDITED. Extract each as the bytes strictly between its `BEGIN <NAME>` line and its
   `END <NAME>` line, verify them against that BEGIN line's sha256 before use, and let no marker
   line reach a file.
2. READ `.agent/STOP` before C0a, before C2, before C4 and before C5, with real exit codes. If it
   exists: finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished and hand back with the raw output.
4. Scratch, runner scripts and the disposable worktree live under `.remedy-wt/f261r1w/`,
   uncommitted, and no `.py` file goes under `.agent/`. Under `.remedy-wt/` you open only the
   block file and your own directory.
5. Every commit stays under 500 insertions.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph of your own: RECORD1's is the reviewer's.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 447 lines TOTAL and 249 lines of PROSE,
   against the caps of 490 and 400.
8. GATE ORDER. G1 and G2 after C1; G3 after C2; G4 after C3; G5, G6 and G7 after C4 and before
   C5; G8 after C5 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f261-r1.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it. The slices FOUND, each
matching its BEGIN-marker sha256.

G2 THE PLAN, at C1. `.agent/plan.md` is byte-identical to PLAN1, at most 50 lines, with
`^## Goal$` once and `^## Next Steps$` once.

G3 THE RECORD, at C2, against the base blobs read with `git show`. (a) `.agent/live_review.md`
equals HEAD1, then the base bytes from the `^## Findings$` line to the end, then RECORD1; the
sha256 of that carried region is the same in the base blob and at C2. (b) `.agent/decisions.md`
equals its base blob followed by DEC1. (c) For each of PC, PA and PD, the file at C2 equals its
base blob with FROM's one occurrence replaced by TO; for PC, FROM reads 0 and TO 1 at C2.
(d) Over `.agent/live_review.md`: lines matching `^Gate: F\d+ R\d+ — ` read 109 at the base and
110 at C2, and `Gate: F275 R110 — ` once at C2; distinct `^- R-\d+ — ` ids 92 and 93; distinct
`^Done: R-\d+ — ` ids 2 and 3; the open set by distinct id 90 and 90, with C2 minus base exactly
`R-0890` and base minus C2 exactly `R-0889`. (e) No line of `.agent/candidates.md` at C2 begins
with `- `.

G4 THE CLAIM, at C3. In `docs/roadmap/STATUS.md` PS's FROM reads 0 and its TO 1; `^- \[~\] `
matches exactly once; `^- \[x\] F\d{3} — ` reads 77 at the base and at C3.
`.agent/context.md` is byte-identical to CTX1.

G5 THE RENAME, at C4. `git show --numstat` of C4 names exactly `apps/cli/command_catalog.py`,
`apps/cli/commands/do_cmd.py`, `docs/system/vocabulary.md`,
`packages/orchestration/job_evidence.py`, `packages/orchestration/pingpong_job.py`,
`scripts/make_review_zip.sh`, `tests/cli/test_do_job_flow_review_base.py`,
`tests/orchestration/test_evidence_index.py`, `tests/orchestration/test_job_evidence.py`,
`tests/orchestration/test_review_zip_hygiene.py`, `tests/orchestration/test_stream_export_e2e.py`,
`tests/orchestration/test_token_ledger.py` and `tests/test_command_catalog.py`. Each
`git rev-parse <C4>:<dir>` equals the reviewer's dry run: `apps` `34a974f01856d79ed6f91155deb9cb23a7ee5056`,
`packages` `7143da9d2997d07c35d5e262003be2515b3970ae`, `scripts` `79be9d31e1da20b56515616d2b87450257d7d4cf`,
`tests` `222e7bf7fec5444af275dce4e185651716ef95fe`, `docs/system` `6cdd3424fad47180bd50f0d6abce9dbd925aa07b`.
`git grep -n -e _cmd_do_job_evidence -e 'do\.job-evidence' -e 'do job-evidence' <C4> -- ':!.agent'
':!.data' ':!docs/roadmap'` prints exactly one line, the `RENAMED` pair in
`tests/test_command_catalog.py`. `python3 -m ruff check` over every `.py` path of C4 exits 0.

G6 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f261r1w/wt <C4's sha>`, each run through
the runner over `tests/test_command_catalog.py tests/orchestration/test_job_evidence.py` with
`-rf --tb=no`. (a) CONTROL, unmutated: must exit 0. (b) In
`apps/cli/commands/do_cmd.py` the bytes `"job.evidence": lambda args: _cmd_job_evidence(`, whose
count there must read 1, become `"job.evidense": lambda args: _cmd_job_evidence(`: must exit 1,
with `TestRenamedCommands::test_every_new_id_parses_from_its_words_and_has_a_handler` among the
failed nodes. Restore with `git -C .remedy-wt/f261r1w/wt checkout -- apps/cli/commands/do_cmd.py`.
(c) In `apps/cli/command_catalog.py` the bytes `command_id="job.evidence",`, count 1, become
`command_id="do.job-evidence",`: must exit 1, with
`TestRenamedCommands::test_no_old_id_is_left_in_the_catalog` among the failed nodes. Restore the
same way. Report each exit code, summary line and every failed node id; then
`git worktree remove .remedy-wt/f261r1w/wt`.

G7 THE SUITES, in the primary checkout at C4, serially, each path its own
`python3 -B -m pytest -q -p no:randomly <path>` run: `tests/test_command_catalog.py`,
`tests/cli/test_advertised_commands.py`, `tests/cli/test_command_catalog.py`,
`tests/cli/test_job_commands.py`, `tests/cli/test_cli_ux.py`,
`tests/orchestration/test_job_evidence.py`, `tests/orchestration/test_evidence_index.py`,
`tests/orchestration/test_review_zip_hygiene.py`, `tests/orchestration/test_token_ledger.py`,
`tests/orchestration/test_stream_export_e2e.py`, `tests/cli/test_do_job_flow_review_base.py`,
`tests/test_do_job_flow.py`, `tests/docs/`, `tests/orchestration/test_roadmap_index.py`; then the
four state readers as four runs, `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
`tests/regression/test_resource_safety.py` and `tests/orchestration/test_integrity_gate.py`; and
last the canary `tests/cli/test_golden_path.py`. Each must exit 0; report each summary line.

G8 THE TREE, after C5 and the push. `git status --porcelain` prints `''`; the branch is
`feature/f261-cli-vocabulary-v2`; C0a to C5 are single-parent commits in that order on the base;
`git rev-parse HEAD` equals `git rev-parse origin/feature/f261-cli-vocabulary-v2`;
`git worktree list` prints one row.

## The handback, C5

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 1 of feature F261 · round 1 · rounds so far 1`, with one sentence of context
self-assessment. `## Commits` lists C0a to C4, each row's `+/-` cell equal to
`git show --numstat` of that commit; C5's own numbers appear nowhere, per item 31 of §3.
`## Verification` gives G1 to G7 with real exit codes. It states the open findings at 90 by
distinct id with the High ids R-0803, R-0804, R-0806 and R-0807, and
`Operator questions open: 1`. Its `## Next` names, in order: Phase 1 rule 1; the reviewer's
verdict on round 1; T001's rename of `do job-promote` to `job apply`.

── SLICE PLAN1 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN1 sha256=21f4d75eb7e2bd3f1e79fbd73c58d8a995b9cfb474e06e29620367da98016728
# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 1 claims F261, cuts the branch, re-points this file and `.agent/context.md`, re-heads
`.agent/live_review.md`, books F275's round 110 verdict and the resolution of R-0889, registers
F275's closure candidate as R-0890, empties `.agent/candidates.md`, and records DECISION F261 D1,
which re-scopes T001 against the catalog measured at `7cdde89b`. Its code commit lands T001's
first rename, `do job-evidence` to `job evidence`, with a guard that the old id stays deleted.

## Next Steps

1. T001's renames `do job-promote` to `job apply` and `do job-run` to `job run`, one per
   commit, each adding its pair to the rename guard.
2. The deletion of `do job-flow` with its deletion paragraph, in two commits: the command and
   its tests, then the helpers only it used and the script that runs it.
3. The deletions of `do job-plan` and `do plan`, each with its deletion paragraph.
4. T002: `apply` replaces `promote`, and `job show --full` absorbs the read commands and
   `do job-report`.
5. T003, the prune to D4; then T004, descriptions, role labels, help wrapping and the tests.

## Risks

- 90 findings are open by distinct id; four are High, R-0803, R-0804, R-0806 and R-0807, all
  owned by F273. R-0805, R-0806 and R-0809 are named in this feature's Acceptance.
- The canary `tests/cli/test_golden_path.py` names none of T001's commands, so it cannot catch
  a T001 rename; `TestRenamedCommands` in `tests/test_command_catalog.py` and
  `tests/cli/test_advertised_commands.py` are the guards that can.
- A deleted `do` word falls through to `do run` and is read as a goal; DECISION F261 D1
  records why no refusal is added.
END PLAN1

── SLICE HEAD1 ── target `.agent/live_review.md` ── HEAD SWAP ──
BEGIN HEAD1 sha256=41151280ad055a85330d3e775cb8b66fbdbe2e688d7d99ceb1d15e695cb0ffef
# Live Review — F261 CLI vocabulary v2 (rename & prune)

> Round-by-round review record, re-headed at the F261 claim per
> docs/agents/planner_reviewer_prompt.md §1. The heading this replaces named F275, which is
> accepted: its STATUS line went `[x]` at `76283e6936f5f622e80e5fdacaa5a113ec0f0608` and its
> pull request 250 merged at `7cdde89b5d0dc8ef1fb96980105870e956699873`, at this session's
> Open PR Gate. Only the heading, this paragraph and the `## Steps` section below are
> rewritten. Everything from the `## Findings` line to the end of the file is carried forward
> BYTE-IDENTICAL, and finding ids continue the monotonic R-XXXX series across the re-head.
> Measured by the reviewer at `7cdde89b5d0dc8ef1fb96980105870e956699873`: 92 DISTINCT ids
> matching `^- R-\d{4} — ` against 2 DISTINCT ids matching `^Done: R-\d{4} — `, so 90 findings
> are open BY DISTINCT ID; the record carries four `Done:` lines for those two ids.
> F275's last round, round 110, has an entry here: its verdict was written into pull request
> 250, and under docs/agents/self_drive_protocol.md the reviewer books a branch-terminating
> verdict into the next feature's first round. Records of features already `[x]` in
> docs/roadmap/STATUS.md move to `.agent/live_review_archive.md` through
> `scripts/rotate_live_review.py` in each closure sequence, under operator amendment
> amend0905-throughput.

## Steps

THE ORDER BELOW IS T2_F261.md's Orchestrator brief, with T001 as DECISION F261 D1 re-scopes it.
R1 claim F261, re-head this record, book F275 round 110, resolve R-0889, register R-0890, rule
DECISION F261 D1 and rename `do job-evidence` to `job evidence` → the renames `do job-promote`
to `job apply` and `do job-run` to `job run` → the deletion of `do job-flow` → the deletions of
`do job-plan` and `do plan` → T002, `apply` for `promote` and `job show --full` → T003, the
prune to D4 → T004, descriptions, role labels, help wrapping and the catalog tests → the
integration gate → the closure sequence.

END HEAD1

── SLICE RECORD1 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD1 sha256=3bc8d9acd5617765c4c12ccd62d39518ff1a6ab1a1c06a21f4e82abbe3f415f2

Gate: F275 R110 — the F275 round 110 entry, REPAIR ON PULL REQUEST 250. VERDICT PASS. Written by the planner and reviewer of session 36 into pull request 250 as a comment, because round 110 was the last round of its branch, and booked here by F261's round 1 under operator amendment amend0827-process-diet rule 1. The round existed because hosted run `34901124355` on `76283e69` failed its `standard` stage on the two ratchet tests R-0889 names. Re-derived by that reviewer over `76283e69`..`4c055a51`: `.agent/authored/f275-r110.md` at `28a8d338` and `.agent/last_block.md` at `74a17524` are byte-identical to the reviewer's scratch original, sha256 `c688463ddeb435b3f822ccf51ad811865a0021690a2f71305e2e6f97d9654abe`; `.agent/plan.md` at `313b6f0a` equals PLAN110; `.agent/live_review.md` at `313b6f0a` equals its blob at `76283e69` followed by RECORD110 and is unchanged through `4c055a51`, the open set moving from 89 to 90 by exactly R-0889. `cb8f663b` touches exactly `.github/workflows/ci.yml`, 5 insertions and 0 deletions, and `tests/orchestration/test_ci_workflow.py`, 8 and 0, each equal to its authored slice applied to its blob at `313b6f0a`. The reviewer's runs in the primary checkout at `4c055a51` of the workflow guards, the coupling ratchet, `tests/cli/test_golden_path.py`, `tests/docs/` and `tests/ui_server/test_dashboard_contract.py` read 439 passed, exit 0, and `python3 -m ruff check tests/orchestration/test_ci_workflow.py` passed. The worker's committed transcript `.agent/authored/f275-r110-suite.txt` reads `EXIT=0` with 18443 passed, 23 skipped and no bad node. Hosted run `34905977033` on `4c055a51` concluded `success` with the stages fast, standard, ui, smoke and budgets each passed, and this session then merged pull request 250 at the Open PR Gate as `7cdde89b`.

Done: R-0889 — RESOLVED by F275 round 110. `cb8f663b` gives the checkout step of `.github/workflows/ci.yml` `fetch-depth: 0`, so the hosted job holds the history `deleted_modules()` reads, and appends `test_hosted_workflow_checks_out_the_full_history` to `tests/orchestration/test_ci_workflow.py`, which pins that the key sits inside the checkout step; the ratchet in `tests/orchestration/test_event_name_coupling.py` is unchanged. Verified by the reviewer of session 36: in a disposable worktree at `cb8f663b` the guard file read 1 failed and 5 passed with the `fetch-depth: 0` line deleted, the one failure being the new guard, while the same file passed within the reviewer's run in the primary checkout at `4c055a51`; hosted run `34905977033` on `4c055a51` passed every stage, where run `34901124355` on `76283e69` had failed the two ratchet tests.

- R-0890 — Low, THE SELF-USE RUNNER PASSES `run_job` THE ROLE CONFIG'S PROVIDER NAMES BUT NOT ITS MODEL OR EFFORT, SO THE JOB'S EXECUTION RECORD CARRIES AN EMPTY MODEL WITH SOURCE `default` AND NEVER NAMES THE MODEL THAT RAN. Registered by the planner and reviewer of session 36 from the closure candidate F275's closure gate recorded in `.agent/candidates.md` on 2026-09-14, after searching the open set for the defect under §3 item 30: no open finding describes it, and R-0768, its provider-name counterpart, was resolved by F110 round 2. THE DEFECT, read at `7cdde89b`: `run_next_self_use_item` in `packages/orchestration/self_use_runner.py` reads `resolve_role_config(role).provider` for the builder and the reviewer and hands `run_job` only the provider names; `run_job` in `packages/orchestration/pingpong_job.py` resolves each model and effort through `_resolve_cfg` with a literal `""` default, so `ExecutionConfig` records them empty with source `default`, while a provider name falls back to the role config through `default_role_provider_name` and a model has no such fallback. MEASURED in `.agent/selfuse_f275/`: `full_transcript.txt` names provider `ollama`, model `muse-glimmer:latest` and effort `medium` for both roles, and `execution_config.txt` records `builder_model=''` and `reviewer_model=''`, each with source `default`. WHY LOW: on the one provider the runner reaches, `OllamaPingPongProvider` turns an empty model into the `ollama-default` alias, which `packages/orchestration/model_aliases.py` maps to the same `muse-glimmer:latest` the role config names, so the right model ran and the record is what is wrong; for `claude` an empty model selects the provider's `claude-workhorse` default and for `claude-cli` no `--model` at all, while the role config names `claude-flagship` for both, a mismatch the runner cannot reach while its resolution answers `ollama`. FIX: when the runner fills in a provider name it also passes the role config's model and effort, `run_job`'s product default for each model is the role config's model rather than `""`, and a test asserts that an unflagged self-use run records `builder_model` equal to `resolve_role_config("builder").model`. Owner: F273.
END RECORD1

── SLICE DEC1 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC1 sha256=e7308b085f1a1a3c5aa687666973679280a0b3a653bafa5703569dae51207697

## DECISION F261 D1 (2026-09-15, F261 round 1) — T001 is re-scoped against the catalog F275 left: three plain renames first, then three deletions, with `job plan` kept and `do job-report` moved to T002

CONTEXT. `docs/roadmap/features/T2_F261.md` was written on 2026-09-05 against the catalog at `b2ee0a84`. Since then F260, F272, F274 and F275 deleted the prototype cluster, the classic store and the classic runner, and T001's list was never re-read against what survived. Two of its targets already exist as different commands, so taken literally T001 would change the behaviour behind a surviving name, which the feature's own "Do not touch" section forbids.

THE MEASUREMENT, taken by the reviewer at `7cdde89b5d0dc8ef1fb96980105870e956699873` by importing `apps.cli.command_catalog`: 44 groups and 220 commands, not the 60 and 342 the feature file quotes; the `job` group holds 25 commands, and `do` holds the 15 subcommands `continue`, `evidence`, `job-evidence`, `job-flow`, `job-plan`, `job-promote`, `job-report`, `job-resume`, `job-run`, `plan`, `promote`, `repair-attest`, `replan`, `report` and `run`. `job.plan` and `job.show` exist; `job.run`, `job.evidence` and `job.apply` do not. `job plan` dispatches to `_cmd_plan_job_local` in `apps/cli/commands/job.py`, which plans an existing job through the Ollama planner, while `do plan` creates a deterministic scope plan from a task file and `do job-plan` parses a Markdown job file into a new job without a provider call. `job show` dispatches to `_cmd_show_job`, which prints the job record as JSON, while `do job-report` prints the job report. `tests/cli/test_golden_path.py` holds 42 tests and no occurrence of `job-evidence`, `job-promote`, `job-run`, `job-report`, `job-plan`, `job-flow` or `do plan`. `--plan-only` occurs nowhere under `apps/` or `packages/`. In `apps/cli/grouped.py`, `_DEFAULT_COMMAND` maps `do` to `run`, and a word after `do` that is no `do` subcommand and does not start with `-` gets `run` inserted before it.

CHOSEN, FIRST: `job plan` STAYS AS IT IS. It already carries D4's word and shape, `plan <id>`, and neither `do plan` nor `do job-plan` is folded into it. Both are DELETED in T001, each in its own commit with the deletion paragraph amend0905-vocab D3 requires, naming F268's `remedy do <order> --plan-only` as the heir of the idea. Until F268 lands no CLI word plans a job from a Markdown file without a provider; DECISION D-A accepts that gap.

CHOSEN, SECOND: `do job-report` IS NOT RENAMED IN T001. `job show` exists and prints something else, so the report becomes a section of `job show --full` in T002, beside the read commands D4 already folds there.

CHOSEN, THIRD: THE ORDER. The three plain renames land first, one per commit: `do job-evidence` to `job evidence` in round 1, then `do job-promote` to `job apply`, then `do job-run` to `job run`, which keeps `--max-tasks` because D4's `--tasks n` is a flag rename of its own. Then `do job-flow` is deleted with its deletion paragraph in two commits: the command and its tests, then the helpers only it used and `scripts/remedy_self_job_flow.sh`, which runs it. Then `do job-plan` and `do plan`. The other `do` words D4's "Nothing else under `do`" removes and T001 does not list — `do job-resume`, `do report`, `do evidence`, `do continue`, `do replan` and `do repair-attest` — are pruned in T003, and `do promote` becomes `job apply` with D5 in T002.

CHOSEN, FOURTH: ONE RENAME GUARD. Because the canary names none of T001's commands, every rename adds its old and new id to `TestRenamedCommands` in `tests/test_command_catalog.py`, which fails when an old id is back in the catalog or a new id does not parse from its own words to a registered handler; `tests/cli/test_advertised_commands.py` keeps every advertised command string resolving. ALTERNATIVE: one test per rename, rejected because a single table is the readable record of what F261 renamed.

CHOSEN, FIFTH: NO REFUSAL FOR A DELETED `do` WORD. After a deletion the fall-through reads `remedy do job-evidence` as `remedy do run job-evidence`, a goal. That is the designed `remedy do <order>` entry, whose meaning F268 owns, and a list of refused retired words is an alias surface under another name, which DECISION D-B forbids. ALTERNATIVE: refuse each retired word with a pointer to its new name, rejected for that reason.

CONSEQUENCE. `docs/roadmap/features/T2_F261.md` gains one dated paragraph at the end of T001 naming this ruling, and its 2026-09-05 measurements stay as history. HOW TO REVERSE: delete this section and that paragraph; T001 then reads as written, with both collisions unresolved.
END DEC1

── SLICE PC-FROM ── target `.agent/candidates.md` ── FROM OF PC ──
BEGIN PC-FROM sha256=b634ff1fef7e1b7d862418190b9bb5d488343aae639f531e80b63358da5977cb
- THE SELF-USE RUNNER HANDS `run_job` THE ROLE CONFIG'S PROVIDER NAMES BUT NOT ITS MODEL NAMES. In F275 round 107's run of `SU-014`, recorded under `.agent/selfuse_f275/`, `resolve_role_config` named provider `ollama` and model `muse-glimmer:latest` for both the builder and the reviewer, while the job's `execution_config` records `builder_model=''` and `reviewer_model=''`, each with source `default`; so a closure's self-use run may not run the model its role config names. Raised at the closure review of F275 from the worker's declared observation, not yet searched against the open set under §3 item 30 and not measured beyond that record. · F275 · 2026-09-14
END PC-FROM

── SLICE CAND1 ── target `.agent/candidates.md` ── TO OF PC ──
BEGIN CAND1 sha256=a5e626a10653fb2e4a1e536399ac21f0e0706aae6ae9f694326f706159eeec6b
EMPTY — no candidate is open.

The entry F275's closure gate recorded on 2026-09-14 — the self-use runner hands `run_job`
the role config's provider names but not its model names — was registered in F261 round 1 as
finding `R-0890` in `.agent/live_review.md`; the measurement and the routing are on that
record.
END CAND1

── SLICE PA-FROM ── target `docs/roadmap/features/T2_F273.md` ── FROM OF PA ──
BEGIN PA-FROM sha256=73b55887f1aff4fc28d4a1e45b07852848d757228d9118ced79256b29a6a5e05
- T016 (a) and (b) carry the ids they minted and their resolution lines; `R-0839`
  carries a resolution line with the tombstone test named; the CI runs the suite on
  3.10 AND 3.12 and both columns are green.
END PA-FROM

── SLICE ACC1 ── target `docs/roadmap/features/T2_F273.md` ── TO OF PA ──
BEGIN ACC1 sha256=fc60f395bf5f108e99670913562c3fbc600763ba85ada738bd8b9bcb52e4ff4f
- T016 (a) and (b) carry the ids they minted and their resolution lines; `R-0839`
  carries a resolution line with the tombstone test named; the CI runs the suite on
  3.10 AND 3.12 and both columns are green.
- R-0890 carries a resolution line naming the test that proves an unflagged self-use run
  records the role config's builder and reviewer model.
END ACC1

── SLICE PD-FROM ── target `docs/roadmap/features/T2_F261.md` ── FROM OF PD ──
BEGIN PD-FROM sha256=a534ab326364a221f1c9c244ff23a758ae9c683ba8b298a8bab0221dcfac90fc
## T002 — `apply` replaces `promote`; `job show --full`
END PD-FROM

── SLICE AMEND1 ── target `docs/roadmap/features/T2_F261.md` ── TO OF PD ──
BEGIN AMEND1 sha256=760affe6e726609d0e8846d29c450ddf87ccba57e59a297059bc6340c5883429
Amended 2026-09-15 by DECISION F261 D1, measured at `7cdde89b`: `job plan` already carries
D4's word and stays as it is, and `do plan` and `do job-plan` are deleted rather than folded
into it; `do job-report` moves to T002, because `job show` exists and prints something else;
the renames of `do job-evidence`, `do job-promote` and `do job-run` land first, then the
deletion of `do job-flow`, then those of `do job-plan` and `do plan`; and the other `do` words
D4 removes, `do job-resume`, `do report`, `do evidence`, `do continue`, `do replan` and
`do repair-attest`, are pruned in T003.

## T002 — `apply` replaces `promote`; `job show --full`
END AMEND1

── SLICE PS-FROM ── target `docs/roadmap/STATUS.md` ── FROM OF PS ──
BEGIN PS-FROM sha256=212930cb7cd66d2f680f5f00c8e4628d539e96731e281e5f08ddce0cf713a8db
- [ ] F261 — CLI vocabulary v2 (rename & prune)
END PS-FROM

── SLICE STATUS1 ── target `docs/roadmap/STATUS.md` ── TO OF PS ──
BEGIN STATUS1 sha256=bc7c0a7b65da344de73eb4c247320912e85e6b2bc6881d3c8c51979982f45ef4
- [~] F261 — CLI vocabulary v2 (rename & prune)
END STATUS1

── SLICE CTX1 ── target `.agent/context.md` ── FULL REPLACEMENT ──
BEGIN CTX1 sha256=15ff20c97e22e56df73ebe5274a1368b345e6459e05e725ffb1ee412d5fcc01f
# Context — F261 CLI vocabulary v2 (rename & prune)

## Active Branch
feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Scope
F261 (Tier 2; depends on F259, F260, F272, F274 and F275; blocks F266, F268, F269, F270,
F271 and F263): the catalog equals DECISION amend0905-vocab D4. Task slicing per
`docs/roadmap/features/T2_F261.md`: T001 dissolves the plan triplet and the `job-*` family,
T002 makes `apply` replace `promote` and builds `job show --full`, T003 prunes to D4, and T004
lands descriptions, role labels, help wrapping and the catalog tests. DECISION F261 D1
re-scopes T001 against the catalog measured at `7cdde89b`.

## Do not touch
The concept model (F259 owns the words), the job model (F260 owns what a job is), STATUS
semantics, and the behaviour behind a surviving name: this feature renames and prunes.
Accepted `[x]` evidence under `docs/roadmap/` stays byte-identical.

## Assumptions
- Cleanliness before compatibility (DECISION D-A): no alias and no migration shim. A renamed
  command's old id is deleted in the same commit (DECISION D-B), and every test or script that
  depends on it is converted in that commit.
- One rename per commit, and `TestRenamedCommands` in `tests/test_command_catalog.py` gains
  that rename's pair in the same commit.

## Constraints
The bullets below are STANDING project constraints, carried forward from the context this
file replaces.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers, run as four:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree, never in the primary
  checkout, which satisfies `git status --porcelain` empty at every verdict.
- Bare `ruff` is DENIED to this session's shell; `python3 -m ruff check <path>` is the spelling
  every gate of this feature orders.
- `remedy` (the built CLI) is DENIED to this session's reviewer, subagents included; a round
  needing it delegates the run to the worker and reports the exact output.
- The shell guard refuses shell loops, `$(...)` substitution and `$?` inside a compound
  command, so such checks are written in Python; a pipe into `tail` masks the real exit code.
- The editable install resolves `apps` and `packages` to the PRIMARY checkout, so a test run
  inside a worktree puts the worktree first on `sys.path` and proves where the modules loaded
  from before its result is read.
- A fresh worktree has neither `apps/ui/node_modules` nor a built `apps/ui/dist`.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`,
which AGENTS.md's "Completion Report — Item-Status Table" section requires of every completion
report. This file deliberately does not restate it.
END CTX1

── SLICE TEST1 ── target `tests/test_command_catalog.py` ── APPEND ──
BEGIN TEST1 sha256=e5fc2994152130e68d80c16677b214b903e64793844f5b24c99bce406b4efa78


class TestRenamedCommands:
    """F261 renames a command by deleting its old id outright: no alias (DECISION F261 D-B)."""

    RENAMED = (
        ("do.job-evidence", "job.evidence"),
    )

    def test_no_old_id_is_left_in_the_catalog(self) -> None:
        catalog_ids = {cmd.command_id for cmd in CATALOG}
        assert [old for old, _new in self.RENAMED if old in catalog_ids] == []

    def test_every_new_id_parses_from_its_words_and_has_a_handler(self) -> None:
        from apps.cli.grouped import _get_dispatch_table, build_parser

        parser = build_parser()
        dispatch = _get_dispatch_table()
        for _old, new in self.RENAMED:
            group, subcommand = new.split(".", 1)
            args, _unknown = parser.parse_known_args([group, subcommand, "an-id"])
            assert args._command_id == new
            assert new in dispatch
END TEST1
