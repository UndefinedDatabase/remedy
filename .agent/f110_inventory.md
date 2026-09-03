# F110 T001a — call-site and role inventory

MEASURED AT BASE = `6f2230cea29af36a75fea253afc10f4dfe5a79f0`, the merge commit
of pull request 232 and the commit this branch was cut from. Every present-tense
sentence below is a statement about the tree at BASE and nowhere else; re-read it
at a later commit before trusting it (planner_reviewer_prompt.md §3 item 20).
`git diff --stat edb16a46 6f2230cea29af36a75fea253afc10f4dfe5a79f0` produces no
output, so BASE and `edb16a46` carry the same tree.

This file is T001a's deliverable. `docs/roadmap/features/T3_F110.md`'s
Orchestrator brief requires the full call-site list with roles BEFORE T002.

## Method

Sections A, B and C are produced by a command, not by hand, and each section
records its command verbatim so it can be re-run. The commands walk the
PRODUCTION roots — packages, apps, scripts — parse each .py file with
`ast.parse`, and report every `ast.Call` whose callee resolves to the target
name. Tests are excluded because `tests` is not among the roots. A grep was
rejected here: a grep over these three names also matches docstrings that spell
the call out (two such lines exist — one in `packages/orchestration/artifact_summary.py`
and one in `packages/orchestration/teacher_model.py`), and a call site set that
includes prose is not a call site set.

Backtick-quoted tokens containing a path separator or a file extension are
repository paths; every other backtick-quoted token is a Python symbol.

Each command prints ONE line per call site, so its output line count equals the
row count of the table beneath it. That is the discriminator: a hand-written
table cannot survive the re-run.

## A — production call sites of resolve_role_config

Excluded: its own module `packages/orchestration/role_config.py`, and tests.

Command:

    python3 - <<'PY'
    import ast, pathlib
    ROOT = pathlib.Path('.')
    TARGET = 'resolve_role_config'
    EXCLUDE = ['packages/orchestration/role_config.py']
    def enclosing(tree, lineno):
        best = None
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if node.lineno <= lineno <= (node.end_lineno or node.lineno):
                    if best is None or node.lineno > best.lineno:
                        best = node
        return best.name if best is not None else '<module>'
    for r in ['packages', 'apps', 'scripts']:
        for p in sorted((ROOT / r).rglob('*.py')):
            rel = p.as_posix()
            if rel in EXCLUDE:
                continue
            try:
                tree = ast.parse(p.read_text(encoding='utf-8'))
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    f = node.func
                    name = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else None)
                    if name == TARGET:
                        print('%s:%d %s' % (rel, node.lineno, enclosing(tree, node.lineno)))
    PY

Output at BASE, five lines:

    packages/orchestration/artifact_summary.py:355 summary_call_fn
    packages/orchestration/self_use_runner.py:137 run_next_self_use_item
    packages/orchestration/teacher_model.py:182 resolve_teacher_transport
    packages/orchestration/teacher_model.py:228 ask_teacher
    apps/cli/commands/do_cmd.py:155 _resolve_cli_role_configs

| # | Path | Line | Enclosing symbol | Role argument | What the caller does with the result |
|---|------|------|------------------|---------------|--------------------------------------|
| A1 | `packages/orchestration/artifact_summary.py` | 355 | summary_call_fn | literal `"summary"` | reads `.model` only and passes it straight into make_structured_call_fn as `model=role_cfg.model`. The single site in the repository where a role-resolved model reaches a call_fn factory. |
| A2 | `packages/orchestration/self_use_runner.py` | 137 | run_next_self_use_item | loop variable over `_ROLE_KWARGS`, i.e. `"builder"` then `"reviewer"` | reads `.provider` only; refuses the run with SelfUseRunError when it is empty or `"fake"`, otherwise injects it as `run_job(builder_name=…)` / `run_job(reviewer_name=…)`. The resolved MODEL is never read here. |
| A3 | `packages/orchestration/teacher_model.py` | 182 | resolve_teacher_transport | module constant `TEACHER_ROLE` = `"teacher"` | returns `(provider, model)` when the provider is in `TEACHER_TRANSPORTS`, else None. This tuple is the teacher's whole transport decision. |
| A4 | `packages/orchestration/teacher_model.py` | 228 | ask_teacher | module constant `TEACHER_ROLE` = `"teacher"` | a SECOND resolve of the same role in the same call path, used only to name provider and model inside the refusal message when A3 returned None. |
| A5 | `apps/cli/commands/do_cmd.py` | 155 | _resolve_cli_role_configs | loop variable over `_ROLE_OVERRIDE_ROLES` = `("builder", "reviewer", "repair")` | flattens provider/model/effort into a plain dict per role. See the note below — at one of the two callers that dict is DISCARDED, at the other it is only recorded. |

Note on A5, measured because it decides section E. `_resolve_cli_role_configs`
has exactly two production callers, both in `apps/cli/commands/do_cmd.py`:
at line 1409 (`_cmd_do_job_run`) the return value is not bound to anything at
all — the call is made for its exit-2 validation side effect only — and at line
2603 (`_cmd_do_job_flow`) the returned dict is bound to `role_configs` and used
in exactly one place, line 2823, where it is written into job_flow.json as
the `"role_configs"` key. Neither caller feeds it into provider or model
selection. What both then pass into `run_job` is the RAW flag value
(`builder_model=builder_model` at lines 1486 and 2700), not the resolved config.

## B — production call sites of make_structured_call_fn

Command: the same script as section A with `TARGET = 'make_structured_call_fn'`
and `EXCLUDE = []`. The defining module is NOT excluded here, because the block
orders the exclusion for section A only and `packages/orchestration/intake.py`
holds a real production call site of its own.

    python3 - <<'PY'
    import ast, pathlib
    ROOT = pathlib.Path('.')
    TARGET = 'make_structured_call_fn'
    EXCLUDE = []
    def enclosing(tree, lineno):
        best = None
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if node.lineno <= lineno <= (node.end_lineno or node.lineno):
                    if best is None or node.lineno > best.lineno:
                        best = node
        return best.name if best is not None else '<module>'
    for r in ['packages', 'apps', 'scripts']:
        for p in sorted((ROOT / r).rglob('*.py')):
            rel = p.as_posix()
            if rel in EXCLUDE:
                continue
            try:
                tree = ast.parse(p.read_text(encoding='utf-8'))
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    f = node.func
                    name = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else None)
                    if name == TARGET:
                        print('%s:%d %s' % (rel, node.lineno, enclosing(tree, node.lineno)))
    PY

Output at BASE, eight lines:

    packages/orchestration/artifact_summary.py:356 summary_call_fn
    packages/orchestration/gauntlet_runner.py:216 _default_plan_call_fn
    packages/orchestration/gauntlet_runner.py:225 _default_move_call_fn
    packages/orchestration/intake.py:331 make_provider_call_fn
    apps/cli/commands/do_cmd.py:2955 _cmd_do_replan
    apps/cli/commands/do_cmd.py:246 _cmd_do_mission
    apps/cli/commands/mission_cmd.py:385 _orchestrator_call_fn
    apps/cli/commands/mission_cmd.py:227 _cmd_mission_plan

| # | Path | Line | Enclosing symbol | Role (implied) | Is a resolved model passed? | What the caller does with the result |
|---|------|------|------------------|----------------|-----------------------------|--------------------------------------|
| B1 | `packages/orchestration/artifact_summary.py` | 356 | summary_call_fn | summary | YES — `model=role_cfg.model`, resolved at A1 | returns the call_fn to whoever generates an artifact summary. |
| B2 | `packages/orchestration/gauntlet_runner.py` | 216 | _default_plan_call_fn | none declared | NO — no `model` argument at all | returns the mission-plan call_fn for a gauntlet run. |
| B3 | `packages/orchestration/gauntlet_runner.py` | 225 | _default_move_call_fn | orchestrator | NO, not a ROLE resolution — `model=get_config().get("orchestrator.model") or None`, a raw config key read that never touches role_config | returns the orchestrator move call_fn for a gauntlet run. |
| B4 | `packages/orchestration/intake.py` | 331 | make_provider_call_fn | none declared | NO | the intake call_fn; the module's own public convenience wrapper. |
| B5 | `apps/cli/commands/do_cmd.py` | 2955 | _cmd_do_replan | none declared | NO | binds FlightPlan for a replan; exits 1 when the factory answers None. |
| B6 | `apps/cli/commands/do_cmd.py` | 246 | _cmd_do_mission | none declared | NO | binds FlightPlan for mission planning; falls back to the deterministic skeleton when the factory answers None. |
| B7 | `apps/cli/commands/mission_cmd.py` | 385 | _orchestrator_call_fn | orchestrator | NO, not a ROLE resolution — same `orchestrator.model` config read as B3 | the orchestrator role's call_fn for the mission loop. |
| B8 | `apps/cli/commands/mission_cmd.py` | 227 | _cmd_mission_plan | none declared | NO | binds MissionPlanDraft for `remedy mission plan`; the provider is then LABELLED `"ollama"` by hand at the plan_mission call two lines later. |

The factory itself decides the provider and it is not configurable: at
`packages/orchestration/intake.py` lines 280-326, make_structured_call_fn
constructs `OllamaPlanner(model=model)` or `OllamaPlanner()` unconditionally and
returns None when the `ollama` package or the server is unreachable. So six of
the eight sites above pick NO model, and none of the eight picks a PROVIDER.
The factory does stamp `_call.resolved_model = planner.model` on the returned
callable, so the model that actually served is observable after the fact — which
is the honest reading F110 must preserve when it adds a routed_model and reason.

## C — production call sites of create_provider

Command: the same script with `TARGET = 'create_provider'` and `EXCLUDE = []`.

    python3 - <<'PY'
    import ast, pathlib
    ROOT = pathlib.Path('.')
    TARGET = 'create_provider'
    EXCLUDE = []
    def enclosing(tree, lineno):
        best = None
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if node.lineno <= lineno <= (node.end_lineno or node.lineno):
                    if best is None or node.lineno > best.lineno:
                        best = node
        return best.name if best is not None else '<module>'
    for r in ['packages', 'apps', 'scripts']:
        for p in sorted((ROOT / r).rglob('*.py')):
            rel = p.as_posix()
            if rel in EXCLUDE:
                continue
            try:
                tree = ast.parse(p.read_text(encoding='utf-8'))
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    f = node.func
                    name = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else None)
                    if name == TARGET:
                        print('%s:%d %s' % (rel, node.lineno, enclosing(tree, node.lineno)))
    PY

Output at BASE, one line:

    packages/orchestration/pingpong_loop.py:4164 _create_provider_with_cwd

| # | Path | Line | Enclosing symbol | Role argument | What the caller does with the result |
|---|------|------|------------------|---------------|--------------------------------------|
| C1 | `packages/orchestration/pingpong_loop.py` | 4164 | _create_provider_with_cwd | the enclosing function's `role` keyword, `"builder"` or `"reviewer"` | returns the constructed PingPongProvider. It is the non-`claude-cli` tail of the function: a `claude-cli` name returns a ClaudeCliProvider a few lines above and never reaches this call. |

`_create_provider_with_cwd` itself is called at two places, both in
`packages/orchestration/pingpong_loop.py`: line 3084 with `role="builder"` and
line 3098 with `role="reviewer"`, each guarded by "only when the caller injected
no provider object". The `name` and `model` it receives come from run_pingpong's
`builder_name`/`builder_model`/`reviewer_name`/`reviewer_model` parameters,
which `packages/orchestration/pingpong_job.py` resolves at lines 1740-1774 with
`_resolve_cfg(explicit, persisted, default)` — and the DEFAULT there is the raw
literal `"fake"` for the provider and `""` for the model. role_config is not
imported by either module.

## D — every role in KNOWN_ROLES against sections A, B and C

`packages/orchestration/role_config.py` line 70 declares nine roles. Read at
BASE with `python3 -c "from packages.orchestration import role_config; print(role_config.KNOWN_ROLES)"`,
which answers
`('builder', 'reviewer', 'repair', 'design_worker', 'test_worker', 'final_verifier', 'orchestrator', 'teacher', 'summary')`.

| Role | Found in A? | Found in B? | Found in C? | Reading |
|------|-------------|-------------|-------------|---------|
| builder | YES — A2, A5 | no | YES — C1 with `role="builder"` | the only role reached by both a resolver and a provider factory, and the two do not talk to each other: A2's provider name reaches run_job, A5's is discarded, and C1's `name` comes from run_job's own `"fake"`-defaulted resolution. |
| reviewer | YES — A2, A5 | no | YES — C1 with `role="reviewer"` | identical shape to builder. |
| repair | YES — A5 only | no | no | a repair provider name is resolved at A5, resolved again by `_resolve_cfg` in `packages/orchestration/pingpong_job.py` at line 1769 with default `""`, recorded in ExecutionConfig, and reported by `packages/orchestration/run_manifest.py` — but NO provider is ever constructed from it; line 4243 there falls back to the builder's provider. |
| design_worker | no | no | no | NO PRODUCTION CALL SITE. The string occurs exactly once in packages, apps and scripts: its own declaration in `packages/orchestration/role_config.py`. A registered role nothing resolves. |
| test_worker | no | no | no | NO PRODUCTION CALL SITE. The string occurs once in `packages/orchestration/role_config.py`; the three further hits under scripts are test FILENAMES (test_worker_execution.py and friends), not the role. |
| final_verifier | no | no | no | NO PRODUCTION CALL SITE for model selection. `packages/orchestration/final_verifier.py` is a deterministic evidence gate that makes no provider call; the role name is registered but never resolved. |
| orchestrator | no | YES — B3, B7 | no | routed TODAY by a raw config key, `orchestrator.model` read through `packages/orchestration/config.py`, bypassing role_config entirely. `packages/orchestration/role_config.py` lines 50-55 say this explicitly and deliberately. |
| teacher | YES — A3, A4 | no | no | the cleanest role in the tree: one resolver, one transport allow-list, an honest refusal, and no second path. |
| summary | YES — A1 | YES — B1 | no | the ONLY role whose resolved model reaches an actual call_fn. |

Five of the nine roles reach no provider call at all through their own name
(repair reaches none directly; design_worker, test_worker and final_verifier
reach none at all; orchestrator reaches one only by a different mechanism).
That absence is a result, not an omission.

## E — the verdict: model selection is SCATTERED, not consolidated

It is scattered. There are FOUR independent mechanisms at BASE and no single
seam any of them must pass through:

1. role_config.resolve_role_config — the intended seam. Five call sites (A1-A5),
   of which one (A1) actually forwards the resolved MODEL, one (A2) forwards
   only the resolved PROVIDER, two (A3, A4) serve one role that no other
   mechanism touches, and one (A5) has its result discarded at one caller and
   merely recorded at the other.
2. `_resolve_cfg` in `packages/orchestration/pingpong_job.py`, lines 1740-1774 —
   a SECOND precedence chain (explicit > persisted > literal default) that
   decides the provider and model for the builder, reviewer and repair roles of
   every real run. Its default is the literal `"fake"`, not
   `role_config.DEFAULT_PROVIDER`, and this module does not import role_config.
3. The `orchestrator.model` config key, read directly at B3 and B7.
4. make_structured_call_fn's own hard-wired provider: every call_fn in the repo
   is an Ollama planner, chosen by the factory rather than by any caller.

Consequence, and it is the fact T001a exists to produce: an operator's
`--builder-model` never reaches the provider, because mechanism 1 computes it
and mechanism 2 overwrites the decision from the raw flag. Two mechanisms
answer "what is the product default" differently — mechanism 1 says
`role_config.DEFAULT_PROVIDER`, mechanism 2 says `"fake"` — and both are live.

THE CONSOLIDATION ORDER T001b WILL CARRY, stated here so T002 does not have to
rediscover it:

- a. Make `packages/orchestration/pingpong_job.py`'s provider/model resolution
  call role_config instead of carrying its own literal defaults, so mechanism 2
  becomes a caller of mechanism 1 rather than a rival to it. This is the seam
  that changes behaviour, so it lands alone, with its own red proof.
- b. Give the orchestrator role the same treatment: keep `orchestrator.model`
  as the config key, but read it THROUGH role_config so mechanism 3 stops being
  a third answer.
- c. Leave make_structured_call_fn's Ollama binding alone. It is a PROVIDER
  choice, not a model-tier choice, and rebinding it is failover work, which
  `docs/roadmap/features/T3_F110.md` puts out of scope.
- d. Only then add the task-class declaration at each site, because a class
  declaration on a site whose model is later overwritten by mechanism 2 would
  record a routing reason that did not happen — the one thing the feature's
  acceptance line forbids.

## F — the overlap with the open finding set

Both findings sit on exactly this seam. Both stay REGISTERED and unrepaired on
this branch: repairing another feature's defect from here is the scope drift
AGENTS.md forbids, and neither belongs to F110.

- R-0767, Medium, OPEN in `.agent/live_review.md`. The CLI rejects
  `--builder ollama` / `--reviewer ollama` although create_provider constructs
  that provider. WHAT IT WOULD CHANGE HERE: nothing in sections A-C moves, but
  the allow-list in `apps/cli/commands/do_cmd.py` and the help text in
  `apps/cli/command_catalog.py` are a FIFTH place where a provider name is
  decided, and F110's class table must not silently become a sixth. Its expected
  fix widens the allow-list; it does not touch the resolver.
- R-0768, Medium, OPEN in `.agent/live_review.md`. An unflagged
  `remedy do job-run` still runs under `fake` rather than the resolved product
  default, because `apps/cli/commands/do_cmd.py` line 1409 discards the resolved
  config and `packages/orchestration/pingpong_job.py` defaults to the literal
  `"fake"`. WHAT IT WOULD CHANGE HERE: this is verbatim consolidation order E.a.
  The finding's own expected fix — "resolve builder/reviewer through
  role_config.resolve_role_config at whichever of the two seams the repo rules
  authoritative" — is the same edit T001b needs. F110 MUST NOT silently absorb
  it: when T001b lands that edit, R-0768 is resolved by name, with its own
  red proof, and this overlap is named in the round that does it. What F110 may
  not do is let the repair ride in unannounced under a routing commit.

## G — the routing layers this repository already has

Three distinct things in this repository are called routing. They are not the
same layer and no later reader should conflate them.

| Layer | Where | Decides | Relation to F110 |
|-------|-------|---------|------------------|
| class-to-tier routing | does not exist yet; F110 builds it | WHICH model a declared task class gets, and records the reason | this feature |
| expensive-builder routing | `packages/orchestration/builder_routing.py` | WHEN Remedy should spend a deterministic, local-advisory, local-candidate or expensive-external builder at all, under budget and anti-loop governors | a spend gate that runs BEFORE any model is picked. It executes no provider and names no model. F110 neither edits nor absorbs it. |
| model/route tournament | `packages/orchestration/model_route_tournament.py` | which worker/route the accumulated evidence RECOMMENDS, after the fact, from durable scoring | a metadata and reporting layer. It never calls a provider and produces no winner without sufficient evidence. It could later feed F110's promotion evidence; it is not a router. |

`docs/agents/model_routing_policy.md` is the fourth thing and it is not code: it
is the human-readable policy carrying the seed mapping, the hard rules, the
promotion rule and an honest ceiling. F110 seeds its class table FROM that
document and enforces it in code, and the acceptance line is a sync test that
diffs the two.
