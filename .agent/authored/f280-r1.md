── STEP T001/1 — F280 — ROUND 1 ──
Goal: Claim F280, cut its branch, re-point the state files, re-head the review record, book F261's
round 28 verdict and its prose slip, record DECISION F280 D1, and wire `job run`'s provider flags
into the runner by one table.

Base: `main` at `9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.
This is SESSION 1 of F280. Read first, and trust nothing below that you can read yourself:
AGENTS.md, docs/agents/self_drive_protocol.md, docs/roadmap/features/T2_F280.md, and DECISION
F280 D1 once C1 has landed it.

THE FRAME RULE, per item 37 of §3, measured over the final bytes: NO LINE of this block that is two
or more characters long is a run of a single repeated character, and every box-drawing rule inside
the STEP and SLICE header lines is exactly two characters long.

ENVIRONMENT: `VAR=x cmd`, `env` and `export` are denied, so set environment in-process; `cp` is
denied, so copy with `shutil.copyfile`; bare `ruff` is denied, so use `python3 -m ruff check`.
Shell loops, `$(...)` and `$?` in a compound command are refused by form, so write such checks
as Python scripts under `.remedy-wt/f280r1w/`, and never name a script after a standard-library
module; a pipe into `tail` hides pytest's exit code. The editable install resolves `apps` and
`packages` to the PRIMARY checkout, so a pytest run inside a worktree goes through a runner
script that changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, and
asserts `apps.cli.commands.do_cmd` loaded from inside it. Never call `run_job` or any runner
yourself: a job run started from inside a checkout creates a `remedy/job-*` branch in it.
`git branch --list 'remedy/job-*'` reads 17 lines now; keep it so.

## Bundle — the ordered commit sequence

C0a Cut `feature/f280-cli-vocabulary-v2-part-two` from `main` at the base, then save
    `.remedy-wt/f280-block/f280-r1.md`, the block file the delegating message names, as
    `.agent/authored/f280-r1.md` by `shutil.copyfile`
C0b `.agent/last_block.md`, the same bytes
C1  THE RECORD, one commit: `.agent/plan.md` becomes slice PLAN1; in `.agent/live_review.md`
    everything before the `## Findings` line becomes slice HEAD1 and slice RECORD1 is appended at
    the end; slice DEC1 is appended to `.agent/decisions.md` and slice SLIP1 to
    `.agent/prose_slips.md`; pair PF is applied to `docs/roadmap/features/T2_F280.md`
C2  THE CLAIM: pair PS is applied to `docs/roadmap/STATUS.md`, and `.agent/context.md` becomes
    slice CTX1
C3  THE TABLE: copy `.remedy-wt/f280-block/f280-r1-jobrun.jsonl` to
    `.agent/authored/f280-r1-jobrun.jsonl` and apply it per THE TABLE, in one commit
C4  `.agent/handoff.md`, the handback; then
    `git push -u origin feature/f280-cli-vocabulary-v2-part-two`

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3. No pull request is created.

## Change — exactly these paths and no others

C0a to C2: `.agent/authored/f280-r1.md`, `.agent/last_block.md`, `.agent/plan.md`,
`.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md`,
`docs/roadmap/features/T2_F280.md`, `docs/roadmap/STATUS.md` and `.agent/context.md`. C3: the
table's own carrier and the paths G4 names. C4: `.agent/handoff.md`. The mutation carrier G5
names is READ from `.remedy-wt/f280-block/` and is never committed.

## The record's edges and the pairs

The text `## Findings` also occurs inside prose of the record, so the head swap splits on the
line-anchored expression `^## Findings$` in multi-line mode, which matches exactly once at the
base; the bytes from that line to the end of the file are carried forward unchanged. HEAD1 ends
with its own blank line. RECORD1, DEC1 and SLIP1 each begin with an empty line, and all three
targets end in a newline at the base: an append is the file's bytes followed by the slice's bytes,
and nothing else. Each FROM slice occurs exactly once in its target at the base.
PF `docs/roadmap/features/T2_F280.md`: FROM slice PF-FROM, TO slice AMEND1. The containment test
   printed `TO contains FROM: true`, so APPEND-shaped: proved by whole-file equality with FROM's
   one occurrence replaced by TO, and never by a FROM-zero count.
PS `docs/roadmap/STATUS.md`: FROM slice PS-FROM, TO slice STATUS1. The containment test printed
   `TO contains FROM: false`, so a REWRITE: after it FROM occurs 0 times and TO once.

## THE TABLE

The carrier holds one JSON array per line; its sha256, to verify before copying, is
`91c80c258f7edf0d1b334f87e6b631f043f446afab3d387ed85ba4a579e4b92f`. Apply its rows strictly in
the order they appear, each against the tree as the previous rows left it, from the repository
root: `["edit", path, old, new, count]` opens the path with `encoding="utf-8", newline=""`,
requires the number of occurrences of `old` to equal `count` exactly, and replaces every
occurrence with `new`. A count that differs is a STOP: touch nothing further, commit nothing of
the table, and hand back with the row and the reading. Stage the commit with `git add -A` after
the table and its carrier. The table is the research helper's build of DECISION F280 D1 on the
base, which the reviewer re-applied there with its own applier and tested.

## Constraints

1. NO SLICE AND NO CARRIER IS EDITED. Extract each slice as the bytes strictly between its
   `BEGIN <NAME>` line and its `END <NAME>` line, verify them against that BEGIN line's sha256
   before use, and let no marker line reach a file.
2. READ `.agent/STOP` before C0a, before C3 and before C4, with real exit codes. If it exists:
   finish a half-written commit, write the handoff, push, stop.
3. A red gate is a STOP: commit what is honestly finished and hand back with the raw output.
4. Scratch, runner scripts and your worktree live under `.remedy-wt/f280r1w/`, uncommitted; no
   `.py` file goes under `.agent/`. Under `.remedy-wt/` open only `.remedy-wt/f280-block/` and
   your own directory. `git worktree list` reads one row now; leave it so. Create no symlink.
5. Every commit stays under 500 insertions, read as the first column of `git show --numstat
   --format= <commit>`.
6. NEVER merge, open a pull request, force-push, rewrite history or delete a branch. No `remedy`.
   Write no `Done:` paragraph: this round resolves no finding.
7. THE BLOCK'S OWN SIZE, measured on its final bytes: 372 lines TOTAL and 218 lines of PROSE,
   against the caps of 490 and 400, where PROSE is every line that is not a line of slice
   CONTENT — the `BEGIN` and `END` marker lines count as prose.
8. GATE ORDER. G1 and G2 after C1; G3 after C2; G4, G5 and G6 after C3 and before C4; G7 after
   C4 and the push, reported in the completion message only.
9. Every commit message ends with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`, and
   no subject carries a leading-slash token or an absolute path.

## Done when — every gate run for real, its exit code recorded

G1 TRANSPORT. The sha256 of `.agent/authored/f280-r1.md` at C0a equals the digest the delegating
message gives, and `.agent/last_block.md` at C0b is byte-identical to it; the slices FOUND, each
matching its BEGIN-marker sha256.

G2 THE RECORD, at C1, against the base blobs read with `git show`. (a) `.agent/plan.md` is
byte-identical to PLAN1, at most 50 lines, with `^## Goal$` once and `^## Next Steps$` once.
(b) `.agent/live_review.md` equals HEAD1, then the base bytes from the `^## Findings$` line to the
end, then RECORD1; the sha256 of that carried region is the same in the base blob and at C1.
(c) `.agent/decisions.md` equals its base blob followed by DEC1, and `.agent/prose_slips.md` its
base blob followed by SLIP1. (d) `docs/roadmap/features/T2_F280.md` equals its base blob with
PF-FROM's one occurrence replaced by AMEND1. (e) Over `.agent/live_review.md`: lines matching
`^Gate: F\d+ R\d+ — ` read 27 at the base and 28 at C1, and `Gate: F261 R28 — ` 0 and 1;
distinct `^- R-\d+ — ` ids 127 and 127; distinct `^Done: R-\d+ — ` ids 2 and 2; the open set by
distinct id 125 and 125, with identical membership.

G3 THE CLAIM, at C2. In `docs/roadmap/STATUS.md` PS-FROM reads 0 and STATUS1 1; `^- \[~\] `
matches exactly once; `^- \[x\] F\d{3} — ` reads 78 at the base and at C2. `.agent/context.md` is
byte-identical to CTX1. From the primary checkout at C2, `python3 -B -m pytest -q
tests/docs/` and `python3 -B -m pytest -q tests/orchestration/test_roadmap_index.py`, each its
own run, exit 0; report both summary lines.

G4 THE TABLE, at C3. `git diff --no-renames --name-only` from C3's parent prints exactly
`.agent/authored/f280-r1-jobrun.jsonl`, `apps/cli/command_catalog.py`,
`apps/cli/commands/do_cmd.py`, `tests/orchestration/test_job_run_refs.py`,
`tests/orchestration/test_job_task_runner.py`, `tests/orchestration/test_job_worktree_handoff.py`
and `tests/test_role_override_flags.py`. `git rev-parse C3:<object>` for `apps`, `packages`,
`scripts`, `tests`, `docs/guides`, `docs/system`, `README.md` and `.claude`, in that order, equals
the reviewer's dry run, which applied the table on the base, the record and the claim touching
none of these objects: `f3c2c62a068a994b598463703e5c2de241537e34`,
`ec2c3efd7541c8cc7d30b2b226b109e1b285da45`, `4bea3f9f084c3987c399f39746b5b2c57be6ffca`,
`3d7381b44fa1038901c5c01be2fb0ba1d098fb23`, `52e345b71419d519c98eba49cea68cc424c249ce`,
`cc42698197076bc70d79a91b05ca633d7ebd2df8`, `3c6b8d40ec4f4d76e05dc352a4b0ce8ef8970be5`,
`e3cd5e0ac262f3f993506e95825e270e39c03ec0`. Report C3's insertions and deletions per constraint
5. `python3 -m ruff check` over the six `.py` paths above exits 0.

G5 THE RED-PROOF, in `git worktree add --detach .remedy-wt/f280r1w/wt <C3's sha>`, each run
through the runner over `tests/test_role_override_flags.py`,
`tests/orchestration/test_job_run_refs.py` and `tests/orchestration/test_job_task_runner.py`
with `-p no:randomly -p no:cacheprovider -rf --tb=no`, under `python3 -B`. The mutations are the
rows of `.remedy-wt/f280-block/f280-r1-mutations.jsonl`, whose sha256 must equal
`56d2b30989440182c1a51a17790c6df2ca03c296d9be578a001bc1169dc864c6`; each row is
`[label, path, from, to, node]`, the `from` bytes must occur EXACTLY ONCE in that path inside the
worktree, and the file is restored with `git -C .remedy-wt/f280r1w/wt checkout -- <path>` after
each run. Read that carrier; never retype its bytes. (a) CONTROL, unmutated, first: must exit 0.
(b) Each row must exit 1 with its row's node AMONG the failed nodes; further failed nodes are
expected, not a STOP. Report each exit code, summary line, each FROM's occurrence count and every
failed node id; then `git worktree remove --force .remedy-wt/f280r1w/wt` and read
`git branch --list 'remedy/job-*'`.

G6 THE SUITES, in the primary checkout at C3, serially, each path its own
`python3 -B -m pytest -q -p no:randomly <path>` run: `tests/test_role_override_flags.py`,
`tests/orchestration/test_job_run_refs.py`, `tests/orchestration/test_job_task_runner.py`,
`tests/orchestration/test_job_worktree_handoff.py`, `tests/test_command_catalog.py`,
`tests/cli/test_advertised_commands.py`, `tests/cli/test_cli_ux.py`,
`tests/orchestration/test_live_review_rotation.py`; then the four state readers as four runs,
`tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
`tests/regression/test_resource_safety.py` and `tests/orchestration/test_integrity_gate.py`; and
last the canary `tests/cli/test_golden_path.py`. Each must exit 0; report each summary line.

G7 THE TREE, after C4 and the push. `git status --porcelain` prints `''`; the branch is
`feature/f280-cli-vocabulary-v2-part-two`; C0a to C4 are single-parent commits in that order on
the base; `git rev-parse HEAD` equals
`git rev-parse origin/feature/f280-cli-vocabulary-v2-part-two`; `git worktree list` prints one
row; `git branch --list 'remedy/job-*'` prints 17 lines.

## The handback, C4

`.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 1 of feature F280 · round 1 · rounds so far 1`, with one sentence of context
self-assessment. `## Commits` lists C0a to C3, each row's `+/-` cell equal to constraint 5's
reading of that commit and its deletions column; C4's own numbers appear nowhere, per item 31 of
§3. `## Verification` gives G1 to G6 with real exit codes. It states the open findings at 125 by
distinct id, with the High ids R-0803, R-0804 and R-0807, and `Operator questions open: 1`. Its
`## Next` names, in order: Phase 1 rule 1; the reviewer's verdict on round 1; and the deletion of
the ping-pong path of `do run` with its flags and the scope plan, R-0894.

── SLICE PLAN1 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN1 sha256=97c4d9ed9e3347ae6f6e06f47b87eaadc9206115886cc1b8b57e65ac8f3b62cf
# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and the help surface of
T002 holds, per `docs/roadmap/features/T2_F280.md`.

## Current Step

ROUND 1 claims F280, cuts the branch, re-points this file and `.agent/context.md`, re-heads
`.agent/live_review.md`, books F261's round 28 verdict and its prose slip, and records DECISION
F280 D1. Its table commit hands `job run`'s `--builder-provider` and `--reviewer-provider` to the
runner, deletes `--builder` and `--reviewer` from `job run`, and refuses `fixture` there.

## Next Steps

1. The ping-pong path of `do run` with the flags only it reads, `--scope-file`, `--approve-scope`
   and the scope plan module (R-0894), with `_VALID_PINGPONG_PROVIDERS`, the `--builder` and
   `--reviewer` special-casing of `apps/cli/grouped.py`, the root help's quick start and the two
   provider messages that name the deleted flags; then R-0767's resolution.
2. `job budget <id> set` over the run-contract budget fields and the token budget profile
   (R-0906, R-0909), then `job fulfill`.
3. The fixtures and smoke sections moved off `job create`, then `job create`, `job attach-repo`
   and `job permit`.
4. `propose`, with the DECISION on the two surviving gates DECISION F261 D22 names.
5. The `flight_plan` rename; `worker doctor` and `job run --tasks`; then T002.

## Risks

- 125 findings are open by distinct id; three are High, R-0803, R-0804 and R-0807, none of them
  this feature's.
- Two provider error messages in `packages/orchestration/pingpong_provider.py` name `--builder`
  and `--reviewer`, which `job run` no longer has, until the next step re-points them.
- Argparse prefix matching refuses `--builder` on `job run` only as an ambiguous prefix of the
  three `--builder-*` flags; `TestJobRunProviderWiring` pins the refusal.
END PLAN1

── SLICE HEAD1 ── target `.agent/live_review.md` ── HEAD SWAP ──
BEGIN HEAD1 sha256=664246e1135f616b2213b4988ece26c47c282f2653e653905eb32cc3232c72ef
# Live Review — F280 CLI vocabulary v2, part two

> Round-by-round review record, re-headed at the F280 claim per
> docs/agents/planner_reviewer_prompt.md §1. The heading this replaces named F261, which is
> accepted: its STATUS line went `[x]` at `ea5b08f78be401efc227072f1b3a31fe764abda7` and its
> pull request 251 merged at `9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, at this session's
> Open PR Gate. Only the heading, this paragraph and the `## Steps` section below are
> rewritten. Everything from the `## Findings` line to the end of the file is carried forward
> BYTE-IDENTICAL, and finding ids continue the monotonic R-XXXX series across the re-head.
> Measured by the reviewer at `9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`: 127 DISTINCT ids
> matching `^- R-\d{4} — ` against 2 DISTINCT ids matching `^Done: R-\d{4} — `, so 125 findings
> are open BY DISTINCT ID.
> F261's last round, round 28, has an entry here: its verdict was written into pull request
> 251, and under docs/agents/self_drive_protocol.md the reviewer books a branch-terminating
> verdict into the next feature's first round. Records of features already `[x]` in
> docs/roadmap/STATUS.md move to `.agent/live_review_archive.md` through
> `scripts/rotate_live_review.py` in each closure sequence, under operator amendment
> amend0905-throughput.

## Steps

THE ORDER BELOW IS T2_F280.md's Orchestrator brief, with T001 in the order of the inventory
`.agent/f261_t003_inventory.md`, rounds J to P.
R1 claim F280, re-head this record, book F261 round 28, rule DECISION F280 D1 and hand `job run`'s
provider flags to the runner → the ping-pong path of `do run` with its flags and the scope plan,
R-0894 → `job budget <id> set`, R-0906 and R-0909, then `job fulfill` → the fixtures off
`job create`, then `job create`, `job attach-repo` and `job permit` → `propose`, with the ruling
on its two surviving gates → the `flight_plan` rename → `worker doctor` and `job run --tasks` →
T002 → the integration gate → the closure sequence.

END HEAD1

── SLICE RECORD1 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD1 sha256=fda0f6dea575c6bab85fd5bc3db9e46eddc9a8d5b815bb9d4dadf1ee9c96aa75

Gate: F261 R28 — the F261 round 28 entry, CLOSURE ROUND B. VERDICT PASS. Written by the planner and reviewer of session 42 into pull request 251 as a comment, because the closure commit `ea5b08f7` is the last commit on its branch by Rule A4, and booked here by F280's round 1 under operator amendment amend0827-process-diet rule 1. That reviewer read the committed range `7a97e74d`..`ea5b08f7` and re-derived each reading it states: `.agent/authored/f261-r28.md` at `462bb6e3` and `.agent/last_block.md` at `b4342378` equal its scratch original, and the committed table `.agent/authored/f261-r28-closure.jsonl` at `a6046a6d` equals its carrier, sha256 `6c9a60eb…8fcb6417`; at `a6046a6d`, `.agent/plan.md` equals PLAN28 and `.agent/live_review.md` equals its `7a97e74d` blob followed by RECORD28, and `ea5b08f7` leaves the ledger unchanged; `ea5b08f7` has one parent and changes exactly `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and `.agent/handoff.md`, and re-applying the committed table to the `a6046a6d` blobs reproduces the three non-handoff files byte for byte; STATUS carries 78 `[x]` lines, README says `78 of 280`, the Tier 2 row reads 21 of 33, no `[~]` line remains and the first unchecked line is F280; through the queue loaders `SU-015`'s `consumed_by` is `F261`. Its runs in the primary checkout at `ea5b08f7` of `tests/docs/`, `tests/cli/test_golden_path.py` and the three self-use test files read 406 passed. The closure values on the STATUS line are evidence job `234c8e6f18905013`, package `remedy-review-20260916-151540-READY_FOR_REVIEW.zip`, SHA-256 `8bc443e91657986bcbb83ad3b6d81cb55afd4b111ff7d4e6930983606f545275` and accepted commit `30343f927800784c464eaf56706d5b82ece39c81`; the close is PASS_WITH_RISKS for the open High findings R-0803, R-0804 and R-0807, none of them F261's. Re-read by the planner and reviewer of session 43, F280's first: hosted run `35102202968` on `ea5b08f7` concluded `success`, that session merged pull request 251 at the Open PR Gate as `9f1b6d25`, and at `9f1b6d25` STATUS reads 78 `[x]` lines and no `[~]` line and the open set reads 125 by distinct id.
END RECORD1

── SLICE DEC1 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC1 sha256=aca454cf2ae41fca3c36e64012368385dfb054433ebfeeba31ff2ef17fc82c82

## DECISION F280 D1 (2026-09-16, F280 round 1) — `job run` hands `--builder-provider` and `--reviewer-provider` to the runner, `--builder` and `--reviewer` leave `job run`, and `fixture` is refused there

CONTEXT. The Do-not-touch section of `docs/roadmap/features/T2_F280.md` makes the `job run` provider wiring one of the three places this feature may change what a surviving command does, and only by a dated DECISION with a feature-file amendment. Ruling 4 of `.agent/f261_t003_inventory.md` proposes the wiring, and R-0767 records that `--builder` and `--reviewer` refuse `ollama`, a provider the factory builds. Measured at `9f1b6d25` by the reviewer's research helper in its own detached worktree, and re-applied by the reviewer on its own dry-run tree, whose eight tree objects equal the helper's: `_cmd_job_run` in `apps/cli/commands/do_cmd.py` validates `--builder` and `--reviewer` against `_VALID_PINGPONG_PROVIDERS` (`none`, `fake`, `claude`, `claude-cli`) and hands them to `run_job` as `builder_name` and `reviewer_name`, while `--builder-provider` and `--reviewer-provider` pass `_resolve_cli_role_configs` and are then dropped, so `job run --builder-provider claude` runs whatever provider is persisted or defaulted; `_VALID_ROLE_PROVIDERS` accepts `fixture`, which `create_provider` in `packages/orchestration/pingpong_provider.py` does not build, so a run given it persists the name in the job's execution config and ends `provider_unavailable` on that run and every continuation; `_cmd_job_run` is reached in production only through the `job.run` dispatch entry, and `_VALID_ROLE_PROVIDERS` is read only by `_validate_role_override`, which only `_cmd_job_run` reaches.

CHOSEN, FIRST: `job run` hands `--builder-provider` and `--reviewer-provider` to `run_job` as `builder_name` and `reviewer_name`. An omitted flag passes None, so `run_job`'s own order — explicit, then persisted, then the role config's default — is unchanged, and the value is persisted on continuation as before. `--repair-provider` already reached `run_job` and is untouched.

CHOSEN, SECOND: `--builder` and `--reviewer` leave `job run` — its catalog entry, handler signature and dispatch entry — with no alias, per DECISION D-B of `docs/roadmap/features/T2_F261.md`, and the tests that drove `job run` with them move to the provider flags. `do run` keeps both flags for now: its ping-pong path, `_VALID_PINGPONG_PROVIDERS` and the special-casing of both names in `apps/cli/grouped.py` go together with R-0894.

CHOSEN, THIRD: `_VALID_ROLE_PROVIDERS` becomes exactly the names `create_provider` builds — `claude`, `claude-cli`, `fake` and `ollama` — so `fixture` is refused with exit 2 on all three role flags of `job run` instead of being persisted and failing at run time, and `none`, which the deleted `--builder` accepted, is refused the same way. `fixture` stays a value of `do run`'s own `--builder-provider`, a different flag.

ALTERNATIVES. Adding `ollama` to `_VALID_PINGPONG_PROVIDERS`, the repair R-0767 first proposed, rejected because DECISION amend0905-vocab D4 gives `job run` the provider flags and neither `--builder` nor `--reviewer`. Keeping `fixture` accepted, rejected because no role can run it.

CONSEQUENCE. `remedy job run <id> --builder-provider ollama --reviewer-provider ollama` reaches the runner with both names, and `remedy job run <id> --builder fake` exits 2. Argparse prefix matching is on, so `--builder` is refused as an ambiguous prefix of `--builder-provider`, `--builder-model` and `--builder-effort`; `TestJobRunProviderWiring` in `tests/test_role_override_flags.py` pins the refusal, so a later round that removes two of those flags meets a red test rather than a silent abbreviation. At `9f1b6d25` two provider error messages in `packages/orchestration/pingpong_provider.py` name `--builder` and `--reviewer`, and they are re-pointed together with R-0894. R-0767 is resolved once no catalog entry declares either flag. HOW TO REVERSE: revert the round's table commit, and delete this section and the dated paragraph it adds to T001 of `docs/roadmap/features/T2_F280.md`.
END DEC1

── SLICE SLIP1 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIP1 sha256=50fc88b67c6c77f8dbe17f78bfb4315c05f7c4e59beea974d290e71573a24e4d

2026-09-16, F261 round 28 — the round 28 block said the handback carries no scope report "for the reason round 26's handback gave", while that reason is stated in round 26's block, `.agent/authored/f261-r26.md`; the worker followed the order and declared the misattribution. Carried in pull request 251's verdict comment and booked by F280 round 1.
END SLIP1

── SLICE PF-FROM ── target `docs/roadmap/features/T2_F280.md` ── FROM OF PF ──
BEGIN PF-FROM sha256=2b187749b6089feea315f5cc0f46fe92749ea17b3d565f42a68d3c756a643524
## T002 — Descriptions, role labels, help wrapping, tests (carried over from F261's T004, whole)
END PF-FROM

── SLICE AMEND1 ── target `docs/roadmap/features/T2_F280.md` ── TO OF PF ──
BEGIN AMEND1 sha256=64901382a05881924ea12201591ae63e63998a288fbf8c384f288119a8563caf
Amended 2026-09-16 by DECISION F280 D1, measured at `9f1b6d25`: `job run` hands
`--builder-provider` and `--reviewer-provider` to the runner, `--builder` and `--reviewer` leave
`job run` with no alias, and the three role flags of `job run` refuse `fixture`, which no provider
factory builds; `do run` keeps both flags until its ping-pong path goes with R-0894.

## T002 — Descriptions, role labels, help wrapping, tests (carried over from F261's T004, whole)
END AMEND1

── SLICE PS-FROM ── target `docs/roadmap/STATUS.md` ── FROM OF PS ──
BEGIN PS-FROM sha256=6e0a65c356abab9e8b471eb4977916fd6a3f6381ab7c7924a0a74c2ee806a548
- [ ] F280 — CLI vocabulary v2, part two — the gated prunes, the flight-plan rename and the help surface
END PS-FROM

── SLICE STATUS1 ── target `docs/roadmap/STATUS.md` ── TO OF PS ──
BEGIN STATUS1 sha256=62e20d8b726b5f23aae01a14f79b62e69b9abb7d0a624f145403d829453126d6
- [~] F280 — CLI vocabulary v2, part two — the gated prunes, the flight-plan rename and the help surface
END STATUS1

── SLICE CTX1 ── target `.agent/context.md` ── FULL REPLACEMENT ──
BEGIN CTX1 sha256=9c1da1e218a981cc6d358afeec4856c6536eba8c7d46696e56f4435493e3a4d1
# Context — F280 CLI vocabulary v2, part two

## Active Branch
feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Scope
F280 (Tier 2; depends on F259 and F261; blocks F266, F268, F269, F270, F271 and F263): what
F261 could not reach inside its soft limit, per DECISION F261 D25. Task slicing per
`docs/roadmap/features/T2_F280.md`: T001 finishes the prune to DECISION amend0905-vocab D4 in the
order of `.agent/f261_t003_inventory.md` rounds J to P, and T002 lands descriptions, role labels,
help wrapping, the visible group order and the catalog tests.

## Do not touch
The concept model (F259 owns the words), the job model (F260 owns what a job is), STATUS
semantics, and the behaviour behind a surviving name: this feature renames and prunes, and the
three places T001 must change a surviving command are each taken by a dated DECISION. Accepted
`[x]` evidence under `docs/roadmap/` stays byte-identical.

## Assumptions
- Cleanliness before compatibility (DECISION D-A of `docs/roadmap/features/T2_F261.md`): no
  alias and no migration shim; a deleted word's id joins `TestDeletedCommands` in
  `tests/test_command_catalog.py` in the same commit.
- A deletion that would break a surviving command is deferred to a round that can rule on it,
  never shipped with a finding.

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
- Never call `run_job` or any runner from inside a checkout: a job run creates a
  `remedy/job-*` branch there.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`,
which AGENTS.md's "Completion Report — Item-Status Table" section requires of every completion
report. This file deliberately does not restate it.
END CTX1
