
## DECISION F268 D1 (2026-09-18, reviewer, round 1) — F268 is claimed before F269, and `do` reports the contract as absent
CONTEXT: `docs/roadmap/features/T2_F268.md` lists F269 (contract) under "Depends on", while the
operator's order of DECISION amend0905-vocab D12, recorded in the comment above the Tier 2 block of
`docs/roadmap/STATUS.md`, runs F266, F268, F269 in that order, and Rule A5 proposes F268 now. F269
is `[ ]`: measured at `8e075bbe`, `mission_state.Mission.contract` exists and nothing writes it.
CHOSEN: claim F268 under Rule A5. Until F269 is `[x]`, `do` writes no contract, its `--json`
carries `"contract": null`, and `--contract <template>` lands with T004's pass-through family
printing "not yet available (F269)" — the same documented-dependency form the feature file already
prescribes for F270's flags. The Acceptance line reading "`--plan-only` writes mission plan,
contract and job plans" is met for the contract half by F269's own closure, not by a stub here.
ALTERNATIVES: claim F269 first, rejected because it overrides the operator's recorded order on the
reviewer's own authority; invent a placeholder contract, rejected because F269 owns its shape and a
stub is what the feature file forbids. REVERSE: move F269's STATUS line above F268's in a docs
round and delete this paragraph.

## DECISION F268 D2 (2026-09-18, reviewer, round 1) — `do`'s init step registers and ignores, and writes no file into the repository
CONTEXT: measured at `8e075bbe`, `_handle_init` in `apps/cli/commands/init_cmd.py` writes
`remedy.toml` and `.remedy/config.toml` into the repository root and adds only the worktree
directory and the data directory to `.git/info/exclude`, so a `do` that ran all of `init` would
leave two untracked paths in `git status` — against the Acceptance line "`git status` in the target
is unchanged until `--apply`".
CHOSEN: `do`'s init step performs registration (`register_project_repo`) and the
`.git/info/exclude` entries, and nothing else; the two ignore helpers move out of `init_cmd.py`
into a `packages/orchestration/` module that both `remedy init` and the step import, with `remedy
init`'s own behaviour unchanged. `remedy init` stays the command that writes the two config files;
both are optional, measured at `8e075bbe`: `load_config_spec` in `packages/runtimes/runtime_config.py`
returns None for an absent `.remedy/config.toml`, and the loader in `packages/orchestration/config.py`
reads an absent project `remedy.toml` as an empty table.
ALTERNATIVES: run the whole of `init`, rejected by the Acceptance line above; add the two config
files to `.git/info/exclude` as well, rejected because it would hide files `remedy init` writes on
purpose for the operator to commit. REVERSE: call the full init body from the step and delete this
paragraph.

## DECISION F268 D3 (2026-09-18, reviewer, round 1) — study-once lives on the project record and both study paths write it
CONTEXT: T2_F268.md's Design says F266 adds the `studied_at` / `studied_head` write and `do` reads
it; measured at `8e075bbe`, no Python file carries either name, so F266 closed without the write.
CHOSEN: `RemyProject.metadata["studied_at"]` (ISO-8601 UTC) and `["studied_head"]` (the repository's
HEAD commit id at study time) are written by ONE function in `packages/orchestration/study.py`, which
both `remedy study run` and `do`'s study step call after a study pass completes. `do` studies only
when the repository has at least one commit holding at least one tracked file AND `studied_at` is
absent; otherwise the step is skipped with the reason printed. ALTERNATIVES: infer "studied" from
the presence of `machine-study` memory cards, rejected because cards can be deleted by card hygiene
and a deleted card must not re-trigger a paid pass; write the fields from `do` only, rejected
because a study run by hand must count as the one study. REVERSE: delete the function and its two
calls; delete this paragraph.

## DECISION F268 D4 (2026-09-18, reviewer, round 1) — the sequence module, and what T001 does at the steps later slices own
CHOSEN: `packages/orchestration/do_sequence.py` holds `DO_SEQUENCE`, the ordered tuple `("init",
"study", "plan", "shape", "run", "ui", "apply")`, a table mapping each name to its step function,
and one walker that calls steps only through that table, in that order. The plan step creates the
mission record for every order (DECISION amend0905-vocab D2) and plans it through
`mission_compiler.plan_mission`, deterministically when no planner provider is available. In T001
the shape step always yields ONE job linked to the mission, with `repo_path` set to the repository
root; T002 replaces that with the planner's structured shape output and the force flags. The ui
step is skipped under `--no-ui` and otherwise, until T004, prints the real `remedy ui start` command
for the job; the apply step always stops before apply until T004 adds `--apply`. A skipped or
stopped step prints why, with real ids. ALTERNATIVES: place the module under `apps/cli/commands/`,
rejected because its steps call package functions and must be testable without the CLI.
REVERSE: route bare `do` back to the pre-F268 handler from git history; delete the module and this
paragraph.
