
## DECISION F273 D10 (2026-09-19, reviewer, round 10) — the orchestrator loop continues a paused or out-of-cycles job with `resume_job`; the shipped token sheet defines the four tokens it uses, the colour rule states its carve-out, and R-0622 is carried
CONTEXT: T007's R-0762 and T006's R-0622, R-0661 and R-0755 each needed a ruling taken in the
round that lands the patch (amend0917-throughput rule 3). Measured by research helpers and
re-measured by the reviewer's dry run at `6871f1cd`: the om1 move schema in
`packages/orchestration/orchestrator_move_schema.py` has no resume kind, and the loop's own comment
says re-dispatch is the only way out of a paused job; a job that ended `max_cycles_reached` stays
running, so the loop can neither dispatch for its milestone nor declare it done; `remedy job resume`
holds its three guards inline in `apps/cli/commands/job.py`; four `--remedy-*` properties are used
under `apps/ui/src` and defined nowhere, each rendering its `var()` fallback; 224 raw colour
literals sit outside the token sheet while `tokens_rules.md` names a stylelint gate and a palette
bridge that do not exist; and neither `typescript-eslint` nor any `@typescript-eslint/*` package is
installed in `apps/ui/node_modules` or named in `package-lock.json`.
CHOSEN: (1) R-0762. om1 gains `resume_job`, payload `milestone_id` and an optional `job_id` that
must name the milestone's latest job. The loop continues that SAME job when it is paused, or when
its last run ended `max_cycles_reached` and it has not finished; any other target is refused at
evaluation with a reason. The guards are ONE function, `checkpoints.decide_checkpoint_resume` —
a pending stop request consumed first, worktree drift refused, the plan-approval gate consulted,
an all-green job a no-op — which `remedy job resume` now renders too, so the two doors cannot
disagree; a guard that stops the move gives the non-terminal outcome `resume_not_run`. The resumed
job runs through the executor seam a dispatch uses, which is the authority the loop already holds
for a job it dispatched; `resume_job` grants no new goal. A re-dispatch of a paused job stays
legal. The protocol document goes to v2 and names the move. The watchdog's no-progress trip still
counts dispatches only, so repeated resumes of one milestone are bounded by the iteration budget.
(2) R-0661. `apps/ui/src/styles/tokens.css` defines `--remedy-mono` as an alias of the reference's
`--remedy-font-mono`, and the three warning tokens with the exact values the banner has always
rendered, because the design reference defines no warning token and names that banner unchanged;
`test_design_drift.py`'s allowlist of unresolved properties is now empty. (3) R-0755. The cheap
half first, as its text asks: `tokens_rules.md` states the rule as it is enforced — raw colour
forbidden outside the token sheet, `var()` fallbacks counted, a named carve-out for canvas, SVG and
theme files that cannot resolve `var()`, and no stylelint gate yet — and
`tests/ui_contracts/test_raw_colour_ratchet.py` pins every other file's count exactly, so the count
can only fall. (4) R-0622 IS CARRIED, not built: its repair adds a devDependency, which needs a
network install this session cannot perform, and a lint config naming a parser that is not
installed would turn a loud red into a crash. It stays open under F273 and moves with F273's
closure to the next paydown per amend0911-feedback rule A; the install to make is
`typescript-eslint` at `^8`, and lint enters no gate until it exits 0 (R-0364).
ALTERNATIVES: a resume only for paused jobs, rejected because an out-of-cycles job keeps its pending
work and blocks dispatch; the loop calling the CLI function, rejected because it prints and exits;
mapping the warning tokens to `--remedy-orange-400`, rejected because it recolours a surface the
reference freezes; editing all 224 literals before any gate, rejected as out of scale; stylelint
now, rejected for the same network install.
REVERSE: restore `orchestrator_move_schema.py`, `orchestrator_loop.py`, `checkpoints.py`,
`apps/cli/commands/job.py`, `docs/agents/orchestrator_protocol.md`, `apps/ui/src/styles/tokens.css`,
`docs/ui/design_reference/tokens_rules.md` and `tests/ui_contracts/test_design_drift.py` from
`6871f1cd`, drop the tests this round added, and delete this paragraph.
