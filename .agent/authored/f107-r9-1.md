── STEP T004 part 2a / F107 R9 — the first caller ──────────────
Goal:        `remedy job context <id> --task <tid>` compiles one task's
             context and renders what it received and what was omitted, so
             `context_compiler.py` finally has a caller outside its own tests.
Bundle:      C1 save this block · C2 mirror it · C3 apply the four authored
             live_review pairs · C4 the new command module · C5 catalog +
             registration · C6 its test module · C7 plan · C8 handoff.
Change:      exactly these nine paths, nothing else:
             .agent/authored/f107-r9-1.md (new, C1)
             .agent/last_block.md (C2)
             .agent/live_review.md (C3, the four pairs below ONLY)
             apps/cli/commands/job_context_cmd.py (new, C4)
             apps/cli/command_catalog.py (C5, ONE new CommandEntry)
             apps/cli/commands/__init__.py (C5, import + module tuple)
             tests/cli/test_job_context_cmd.py (new, C6)
             .agent/plan.md (C7, full replacement by slice PLAN9)
             .agent/handoff.md (C8)

Constraints:
 - AGENTS.md is the highest authority. Self-review loop before every commit,
   one logical step per commit, push after the last one, clean tree at hand
   back. Never work on main, never force-push, never amend or rebase.
 - Do-not-touch (docs/roadmap/features/T2_F107.md): prompt composition,
   retrieval/embedding approaches, repo-map features. Reject any TS parser
   dependency. Do NOT edit `packages/orchestration/context_compiler.py` — it
   is frozen this round; R9 CONSUMES it and adds nothing to it.
 - `compile_task_context` deliberately never walks a tree (its docstring at
   packages/orchestration/context_compiler.py:733 says so). The listing is
   therefore the CLI's job and lives in the new module, not in the compiler.
 - Verify every claim against the file before you write it. If anything below
   names a symbol, line or field that does not exist, STOP, do the safe thing,
   and DECLARE the correction in the handback — that is wanted behavior, not a
   deviation (four findings already record reviewer citation errors).

Detail for C4 — apps/cli/commands/job_context_cmd.py (new):
 - Follow the shape of `_cmd_job_fences` (apps/cli/commands/job.py:1964): a
   read-only handler, `load_job(resolve_job_id(...))`, exit 1 on
   JobNotFoundError, exit 2 when `job.metadata["target_repo"]` is missing or is
   not a directory, `--json` producing the same fields as the text view.
 - `list_repo_candidate_paths(root: Path) -> list[str]` — the candidate listing
   `compile_task_context` requires. Primary: `git ls-files -z` run in `root`,
   NUL-split. Fallback when root is not a git checkout or git fails: an
   `rglob("*")` over files, pruning `.git`, `__pycache__`, `node_modules`,
   `.venv` and `dist`. Sorted and deduplicated either way, so the view is
   deterministic. One WHY line above it saying which branch ran and why the
   compiler does not do this itself.
 - Task resolution: match `--task` against `task.inputs["flight"]["planned_id"]`
   (the planned id, e.g. `T001`, written by `map_flight_plan_to_tasks` at
   packages/orchestration/flight_plan.py:513) FIRST, then against a prefix of
   `str(task.id)`. Ambiguous prefix or no match → a named error on stderr and
   exit 3. `--task` omitted with exactly one task → that task; omitted with
   several → exit 3 naming the candidates. Never guess a task.
 - Fenced paths = that task's `inputs["flight"]["files_hint"]`. When the list
   is empty, say so in the output and still render — an empty declared scope is
   a real answer, not an error. Job fence globs are OUT OF SCOPE this round;
   state that limitation in the module docstring so the absence is findable.
 - Render, from `compile_task_context(root, fenced, candidates)` at its
   defaults: the budget line (`estimated_tokens` / `budget_tokens`, plus
   `over_budget` when true), then included files grouped by tier with their
   `rendering` and `estimated_tokens`, then the omissions with `tier`,
   `reason` and `outcome`. `--json` emits the same via
   `export_omitted_context_json(compiled)` for the omissions plus an
   `included` list built from the `SelectedFile` fields. Write NOTHING to disk:
   this command does not call `write_omitted_context_json`.

Detail for C5 — registration:
 - One `CommandEntry` in apps/cli/command_catalog.py beside `job.fences`
   (apps/cli/command_catalog.py:451): command_id `job.context`, group_id `job`,
   subcommand `context`, action_class `read_only`, supports_json True,
   description naming F107, related `("job.fences", "job.show")`. Args:
   `_JOB_ID`, a new `--task` option ArgDef following the shape of `_JSON_OPT`
   (apps/cli/command_catalog.py:164), and `_JSON_OPT`.
 - A `COMMAND_HANDLERS` dict at the bottom of the new module mapping
   `"job.context"`, exactly as apps/cli/commands/job_rerun_cmd.py:165 does, and
   the module added to BOTH the import list and the module tuple in
   apps/cli/commands/__init__.py (the tuple is at line 92).

Detail for C6 — tests/cli/test_job_context_cmd.py (new):
 Build a real tmp_path repo (a fenced file that imports a neighbor, the
 neighbor, a distant module, an unrelated module) and a real Job whose task
 carries `inputs["flight"] = {"planned_id": "T001", "files_hint": [...]}`.
 Assert on REAL VALUES, never truthiness, and cover at least:
 1. the fenced file is tier 1 and rendered `full`;
 2. its direct neighbor appears at tier 2;
 3. the unrelated module appears in the omissions with reason `distance`;
 4. `--json` carries the same paths as the text view;
 5. resolution by planned id `T001` and by task-UUID prefix reach the same task;
 6. an unknown `--task` exits 3 and names nothing it did not find;
 7. a job with no `target_repo` exits 2;
 8. `list_repo_candidate_paths` excludes `.git` and is sorted.

<<<BEGIN SLICE HDRFROM sha256=dfab3095c1f500db92907ec5357292f8056a89a3e4b435f8122e9d5b5f6d0e5b lines=1>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0271.
<<<END SLICE HDRFROM>>>
<<<BEGIN SLICE HDRTO sha256=969938dbfbdb7a576cf8b0b68c4144ab60b0703e3266b46e8f18847bb5a1dc3d lines=1>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0277.
<<<END SLICE HDRTO>>>
<<<BEGIN SLICE LRF5FROM sha256=21a6a3f6e468922f9afbce887927f32579b8535f42122796dacd766f51465cc8 lines=1>>>
  value that cannot exist. OPEN.
<<<END SLICE LRF5FROM>>>
<<<BEGIN SLICE LRF5TO sha256=21a8b66c38bd0d4b73853df52acb983982eb6db008e506fced403a21042e346a lines=23>>>
  value that cannot exist. OPEN.
- R-0275 (Low, F107 R8-close): the R8 handoff reported commit C2's `+/-` column
  as the file's before/after LINE COUNTS, `218/328`, where
  `git show --numstat 627ca2c9 -- .agent/last_block.md` returns `169	279`; gate
  g then repeated the same 218 in its per-commit insertion list. Nothing rests
  on the error — both readings are far under 500, and a verbatim rewrite of a
  single `.agent/**` state file is cap-exempt outright (AGENTS.md Commit
  Discipline, DECISION F104 D1) — but a `+/-` column is a counted value and the
  counting rule names one measure, the `+` column of the diff. Worker-side
  member of the contract-accuracy class after R-0239, R-0247, R-0272 and
  R-0274: every number in the return channel is the output of the command it
  claims to come from. OPEN.
- R-0276 (Medium, F107 R8-close): this file's own header line 8 reads
  `Next free ID: R-0271` while R-0271, R-0272, R-0273 and R-0274 all exist in
  the Findings section above it — stale since R3 registered R-0271.
  `.agent/plan.md` and `.agent/handoff.md` both carry the correct R-0275, so
  the one carrier that OWNS the sequence is the one that is wrong, and it is
  the carrier a reviewer reads to allocate an ID
  (docs/agents/planner_reviewer_prompt.md §4.4, "IDs continue
  monotonically"). A session that trusted the header would reuse R-0271 and
  silently overwrite a live finding. Fixed in this round: the header now reads
  R-0277, allocated past the two findings this gate registers. OPEN until the
  reviewer confirms the applied value.
<<<END SLICE LRF5TO>>>
<<<BEGIN SLICE LR8FROM sha256=686e2302c46d1fd12e793dbc77f38b087fe31965ddaee2ead1138d3da814ce16 lines=1>>>
  6acb3f04.
<<<END SLICE LR8FROM>>>
<<<BEGIN SLICE LR8TO sha256=4894b692be4f86d22965c55cfce1a782aaf98aac7f3bd6093a695bd032c28d0e lines=34>>>
  6acb3f04.

- Reviewer gate on R8-close (2026-08-12, first gate of a NEW session; the
  round it certifies was the terminating round of the previous one, so per
  docs/agents/planner_reviewer_prompt.md §4.13 its verdict had lived only in
  `.agent/handoff.md` until now): PASS. Range 6acb3f04..7acb406d = five commits
  touching exactly the five paths the R8 block named — no production code, no
  test module, no docs. Transport by the PRIMARY shape: the reviewer original
  `.remedy-wt/f107-r8-1.block.md` survived the session boundary, `cmp` against
  `.agent/authored/f107-r8-1.md` and against `.agent/last_block.md` is silent,
  and all three sha256 to 607d240a3a067a4c… at 218 lines. All five slice bodies
  recompute to their BEGIN-marker digests at their declared lengths (LRF4FROM
  d129628f… 1 line, LRF4TO b36108ed… 13, LR7FROM cdc1e3cf… 1, LR7TO 47bc40dd…
  48, PLAN7 a065b87c… 28), and `sha256sum .agent/plan.md` returns that same
  PLAN7 digest over 28 lines. Both C3 pairs were APPEND-shaped and proven as
  such rather than asserted: `git show --numstat 3e704610 -- .agent/live_review.md`
  reads `59  0` — ZERO deletions, so neither anchor was edited — each FROM
  occurs exactly 1x in the file, each of the 12 LRF4TO and 47 LR7TO TO-only
  lines occurs exactly 1x among the 59 added lines, and 0 added lines belong to
  neither body. Every scoped gate was RE-RUN by this reviewer rather than read
  from the handback: `python3 -m pytest tests/orchestration/test_context_compiler.py -q`
  returns 55 passed, the canary `python3 -m pytest tests/cli/test_golden_path.py -q`
  returns 42 passed, `grep -c '^## Steps'` is 1, `grep -c '^- R-0274'` is 1,
  `grep -c '^Done:'` is 1 and `grep -c '^Landed:'` is 1, the stray-marker count
  is 0 across the three state files, `git status --porcelain` is empty,
  `git worktree list` shows the primary checkout alone, and HEAD equals
  `origin/feature/f107-context-compiler-v2`. One counted value in the handback
  did NOT survive re-measurement and is registered above as R-0275: C2's real
  numstat is `169 279`, not the reported `218/328`. The verdict is PASS anyway
  and deliberately so — the error is in the report of a commit that is
  cap-exempt by construction, every other figure re-measured true, and the
  round's substance (transport, application, gates) is verified correct. The
  stale next-free-ID header this gate also found is R-0276. `LAST_REVIEWED_SHA`
  advances 6acb3f04 -> 7acb406d.
<<<END SLICE LR8TO>>>
<<<BEGIN SLICE LRDFROM sha256=62450c778cb700ad9844ede768202a46b1383eae9b90bd642b9e549f1612495e lines=6>>>
Landed: R-0273 — `CompiledContext` gained a fifth field `line_cap`, set by
`compile_task_context` from the caller's cap, and `render_compiled_context_text`
now renders signature bodies at `compiled.line_cap` instead of
`DEFAULT_SIGNATURE_LINE_CAP` (commit "fix(f107): render signatures at the
compiled line cap", C5 of R7 — its own SHA is not writable into itself). Stays
OPEN: only reviewer-authored text resolves a finding.
<<<END SLICE LRDFROM>>>
<<<BEGIN SLICE LRDTO sha256=39b40890313fed32b1ac76a06e72509ae20c69b53889ab92c663a84b181d4e6b lines=12>>>
Done: R-0273 — RESOLVED. `CompiledContext` carries a fifth field `line_cap`,
`compile_task_context` sets it from the caller's cap, and
`render_compiled_context_text` renders signature bodies at `compiled.line_cap`
instead of `DEFAULT_SIGNATURE_LINE_CAP` (commit e0f0a0d1 "fix(f107): render
signatures at the compiled line cap", C5 of R7). The fix was MEASURED, not
read: on the same three-file fixture at `line_cap=3` that produced the finding,
the rendered text's estimate falls from 128 tokens to 46 against an
`estimated_tokens` of 25, so the 5.1x divergence is gone, and two mutation
probes in a disposable worktree put the module back to red (1 failed / 3
failed) — the regression test genuinely bites. The residual 21-token gap is the
one header line the renderer adds per included file, uniform at every cap and
not drift. Open findings 11 -> 10.
<<<END SLICE LRDTO>>>
<<<BEGIN SLICE PLAN9 sha256=33ad21444aed68cd28d1f1c45a977260afa8a8a6245a077a8c5d9de2d870109a lines=28>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0277. R8-close reviewed PASS at 7acb406d.

## Goal
The context compiler selects fenced-path files, their direct import
neighbors, and only SIGNATURES of distant dependencies, under a total
context token budget with tier demotion — and writes an omissions record
naming everything it left out and why. DONE when a fixture repo's task
context shrinks measurably versus whole-files with the fixture task still
solvable by the fake provider, and the omissions record explains every
exclusion (docs/roadmap/features/T2_F107.md).

## Current Step
R9 — T004 part 2a, the FIRST CALLER: `remedy job context <id> --task <tid>`,
a read-only view that compiles the task's context and renders what it received
and what was omitted. New module `apps/cli/commands/job_context_cmd.py` owns
the repo listing the compiler deliberately does not do. This is the round that
turns F107 from a library into something a user can run.

## Next Steps
1. R10 — T004 part 2b: the end-to-end fixture task solved by the fake provider
   using the compiled context, plus the whole-file size comparison recorded in
   evidence via `compare_context_size`.
2. Integration gate per docs/agents/integration_gate.md.
3. Closure per docs/roadmap/STATUS_closure_protocol.md; the branch has no PR
   yet, it is created at closure and never merged in the same session.
<<<END SLICE PLAN9>>>

PROCEDURE — in this order, one commit per numbered step:
 1. Save this ENTIRE block, byte for byte, from the `── STEP` line to the last
    line of this procedure, to `.agent/authored/f107-r9-1.md`. Verify with
    `sha256sum` against BLOCK_SHA256 below BEFORE anything else. On mismatch,
    STOP and report — do not repair the bytes. Commit C1.
 2. Copy that file over `.agent/last_block.md`; `cmp` the two, exit 0 and
    silent. Commit C2.
 3. Apply the four pairs below to `.agent/live_review.md`, each by exact-string
    replacement of its FROM body with its TO body, verifying each slice's
    sha256 BEFORE use. HDR and LRD are REWRITES (FROM and TO are disjoint);
    LRF5 and LR8 are APPENDS (each TO literally contains its FROM). Commit C3
    alone — findings persist before any code moves.
 4. C4, C5, C6 in that order, each its own commit, self-review loop before
    each.
 5. Replace `.agent/plan.md` entirely with slice PLAN9; `cmp` and `sha256sum`
    against the marker. Commit C7.
 6. Run every gate in Done-when, record the REAL exit code and counted value of
    each, then rewrite `.agent/handoff.md` (≤60 lines, or a declared
    stated-cause overage per AGENTS.md D15) and commit C8. Push.
 7. Do NOT write a `Done:` line of your own. If something lands that a finding
    covers, write `Landed: R-XXXX — <one line>` and nothing else.

Done when — run each, record exit code AND counted value:
 a. `cmp .agent/authored/f107-r9-1.md .agent/last_block.md` → exit 0, silent;
    `sha256sum` of both == BLOCK_SHA256.
 b. Each of the nine slice bodies recomputes to its BEGIN-marker digest at its
    declared line count.
 c. `git show --numstat <C3> -- .agent/live_review.md` → the deletion column is
    exactly 7 (HDRFROM's 1 line + LRDFROM's 6), because only the two REWRITE
    pairs delete anything. Then, all against `.agent/live_review.md`:
    `grep -c '^Landed:'` → 0; `grep -c '^Done:'` → 2;
    `grep -c 'Next free ID: R-0277'` → 1; `grep -c 'Next free ID: R-0271'` → 0;
    `grep -c '^- R-0275'` → 1; `grep -c '^- R-0276'` → 1;
    `grep -c '^## Steps'` → 1; `grep -c '^<<<'` → 0.
 d. `python3 -m pytest tests/cli/test_job_context_cmd.py -q` → exit 0, and
    report the passed count.
 e. `python3 -m pytest tests/test_command_catalog.py tests/test_grouped_cli.py -q`
    → exit 0, with the counts.
 f. Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, 42
    passed.
 g. `python3 -m ruff check apps/cli/commands/job_context_cmd.py
    tests/cli/test_job_context_cmd.py apps/cli/command_catalog.py` → exit 0.
 h. THE REAL RUN, and this one decides the round: create a real job against a
    real repo path, give its task a `files_hint`, then invoke the CLI the way a
    user would — `remedy job context <id> --task T001` — and paste the FULL
    stdout into the handoff verbatim, plus the `--json` run. A passing test
    module is NOT this gate: the round exists to prove a user can run it.
 i. `git status --porcelain` → empty; `git worktree list` → primary checkout
    alone; HEAD == origin/feature/f107-context-compiler-v2; insertions per
    commit, each < 500.
 j. `git diff --name-only 7acb406d..HEAD` → exactly the nine paths of the
    Change list, nothing else.

Handback: completion report + rewrite `.agent/handoff.md` per
docs/agents/handback_template.md, with the changed-files table, the item-status
table covering C1-C8, and every gate above with its real exit code and counted
value. Declare any deviation; a declared deviation costs nothing, an undeclared
one costs the round.
──────────────────────────────────────────────────────────────
