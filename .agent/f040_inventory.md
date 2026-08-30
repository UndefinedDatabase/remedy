# F040 seam inventory — the four read paths the digest composes over

Measured by the F040 round-1 worker in the primary checkout at C5
(`3ef0b5a0`, branch `feature/f040-completion-digest`, base `f5b1e6c5`). Every
claim below carries a `file:line`, every count carries the exact command that
produced it, and every ABSENCE names the search that looked for it. Nothing here
is taken from the feature file's prose: `docs/roadmap/features/T5_F040.md` is the
ORDER, this file is the MEASUREMENT, and where the two disagree the disagreement
is stated rather than smoothed over. Line references are 1-indexed.

The `remedy` console script is DENIED in this sandbox, so every CLI reading below
is quoted from its registration site rather than invoked.

---

## 1. The next-action rule table — the one-source seam for the digest's CTA

**The table.** `NEXT_ACTION_RULES` is declared at
`packages/orchestration/run_report.py:175` with the exact annotated type

    NEXT_ACTION_RULES: tuple[tuple[str, str], ...]

so it is a tuple of `(rule id, condition)` PAIRS — two elements, not three.
The comment two lines above it, `packages/orchestration/run_report.py:170`, reads
`#:   (rule id, condition, action template)` and names THREE. That comment is
stale against the value beside it: the action template is not in the table, it is
built inside `recommended_next_action`. A T001 order that reads the comment
rather than the value will specify a three-tuple that does not exist.

The five rules, in the file's own order — which IS the priority order, per the
comment at `packages/orchestration/run_report.py:172-174` ("an open decision
outranks a failure"):

| # | rule id | condition string | line |
|---|---------|------------------|------|
| 1 | `open-decision` | `an open decision is waiting for an answer` | :176 |
| 2 | `stopped-by-operator` | `the run stopped on operator request` | :180 |
| 3 | `blocked-failed` | `the run is blocked or a task failed` | :181 |
| 4 | `all-green` | `every task completed and nothing is open` | :182 |
| 5 | `indeterminate` | `no rule matched the recorded state` | :183 |

Count, from the SHIPPED value rather than from a text pattern:
`python3 -c "from packages.orchestration.run_report import NEXT_ACTION_RULES as R; print(len(R), [r[0] for r in R])"`
printed `5 ['open-decision', 'stopped-by-operator', 'blocked-failed', 'all-green', 'indeterminate']`
— the literal spans `packages/orchestration/run_report.py:175-184`.

`NEXT_ACTION_CONDITIONS: dict[str, str] = dict(NEXT_ACTION_RULES)` at
`packages/orchestration/run_report.py:188` is the id→condition index, and it is
LOAD-BEARING: `NextAction.__post_init__`
(`packages/orchestration/run_report.py:198-200`) raises `ReportError` for a rule
id the dict does not hold. A digest that mints its own rule id cannot construct a
`NextAction` at all — which is the enforcement that makes "one source" real
rather than a convention.

**The function.**

    def recommended_next_action(sources: ReportSources) -> NextAction:

at `packages/orchestration/run_report.py:383`. It takes ONE argument and returns
a `NextAction`, the frozen dataclass at `packages/orchestration/run_report.py:191`
with exactly two fields, `rule_id: str` (:195) and `action: str` (:196), plus a
`render()` method at :202 that appends `_(rule: <id> — <condition>)_` to the
action text. The five branches are at :385 (`open_decision_count` truthy), :397
(`terminal_status` lowercased equals `stopped_by_operator`), :404
(`sources.blocked` non-empty OR terminal in
`{"blocked", "budget_exhausted", "deadline_reached"}`, :403), :409 (`sources.tasks`
non-empty and EVERY task status lowercased equals `completed`) and the
unconditional fallback at :413. First match wins, per the docstring at :384.

**What a caller must construct.** `ReportSources` is the frozen dataclass at
`packages/orchestration/run_report.py:291`. EVERY field is defaulted (:294 "Every
field is optional and every absent field renders `not recorded`"), so
`recommended_next_action(ReportSources())` is legal and returns the
`indeterminate` rule. The four fields the function actually reads:

| field | declared | what feeds it in production |
|-------|----------|------------------------------|
| `open_decision_count: int \| None` | :325 | `_evidence_sources`, `packages/orchestration/run_report.py:881` — `len(open_decisions(list_decisions(job, [])))` |
| `blocked: tuple[BlockedItem, ...]` | :315 | `_evidence_sources`, :883-891 — one `BlockedItem` per still-open decision, `answer_command` from `d.next_actions[0]` (:888) |
| `terminal_status: str` | :309 | `collect_report_sources`, :797 — `metadata["cycle_terminal_status"]` |
| `tasks: tuple[TaskOutcome, ...]` | :314 | `collect_report_sources`, :779-787, from `job.tasks` |

`BlockedItem` is the frozen dataclass at :262 (`task_id`, `reason`,
`failure_class`, `answer_command`, `evidence_ref`); `TaskOutcome` at :239.

Two ready-made constructors exist and the digest should call one rather than
build a `ReportSources` by hand:

- `collect_report_sources(job) -> ReportSources` at :767 — the in-memory half.
  It reads the STATUS mirror (:800) and touches no evidence area.
- `build_report_sources(job) -> ReportSources` at :967 — `collect_report_sources`
  plus `_evidence_sources(job)` (:809) merged through `replace()` at :980. This
  is the ONLY one of the two that populates `open_decision_count` and `blocked`,
  which are branches 1 and 3 of the rule table. **A digest that calls
  `collect_report_sources` would never fire the `open-decision` rule.**

`_evidence_sources` (:809) reads five sources, each inside its own `try` with a
documented broad `except` (:823, :846, :869, :892): cycle records (:820-822),
budget actuals (:829-845), the DoD gate record (:851-868) and the decision queue
(:872-891). Every read is guarded independently so one unreadable source does not
cost the report the others (:810-814).

---

## 2. The decision inbox read path

**Signature.** `packages/orchestration/decision_inbox.py:131-135`:

    def build_decision_inbox(
        job: Any,
        events: list[dict[str, Any]],
        now: datetime | None = None,
    ) -> dict[str, Any]:

**What it returns** — `packages/orchestration/decision_inbox.py:159-163`, exactly
three top-level keys:

    {"version": DECISION_INBOX_VERSION, "job_id": <str>, "decisions": [<card>, ...]}

`DECISION_INBOX_VERSION = 1` at `packages/orchestration/decision_inbox.py:37`.

**Per-card fields.** A card is `export_decision_json(decision)`
(`packages/orchestration/decision_queue.py:1030`, the dict literal at :1045-1066)
plus exactly three added keys, set at
`packages/orchestration/decision_inbox.py:152-155`:

- base 16 keys from `export_decision_json` — `id`, `type`, `status`, `severity`,
  `source`, `related_node_id`, `related_intent_id`, `related_file`,
  `safe_summary`, `next_actions`, `created_at`, `resolved_at`, `payload`,
  `evidence_refs`, `outcomes` (:1046-1060) and `evidence_status` (:1061-1065);
- `age_seconds` (:152) — `_decision_age_seconds` at :40, `None` for an unreadable
  `created_at` (:50-51), clamped at 0 (:54);
- `blocked_count` (:153) — `_blocked_subtree_size` at :57, `len(blocked_downstream(...))`;
- `answerable_by_decision_resolve` (:154) — `_answerable_by_decision_resolve` at
  :78, which mirrors the write door's own refusals.

**The ordering rule it applies: NONE OF ITS OWN.** The loop at
`packages/orchestration/decision_inbox.py:150` iterates `list_decisions(job, events)`
and appends in arrival order (:157). `list_decisions` is
`packages/orchestration/decision_queue.py:83` and its single `return decisions`
is at `packages/orchestration/decision_queue.py:995` — the list is returned in
PRODUCING-BRANCH order with no sort. Verified by
`grep -n "^    return decisions\|^def " packages/orchestration/decision_queue.py`,
which shows `return decisions` at 995 as the only one inside `list_decisions`
(the next `def` is at 998), and by
`grep -n "sort\|order" packages/orchestration/decision_queue.py`, whose only
sorting hits are at :1074 (`sort_open_decisions_first`), :1082 and :1091
(`open_decisions`) — both DEFINED AFTER and neither called by
`build_decision_inbox` (`git grep -n "sort_open_decisions_first\|open_decisions"
-- packages/orchestration/decision_inbox.py` returns nothing).

**URGENCY / SIGNIFICANCE: NOT COMPUTED IN PYTHON AND NOT IMPORTABLE. This is the
inventory's most consequential finding for T001.**

Search: `git grep -n -i -E "urgency|significance" -- packages/ apps/` returns
matches in exactly TWO files, both TypeScript, both under `apps/ui/src/api/`:
`decisionOrder.ts` and `decisionOrder.test.ts`.
`git grep -c -i -E "urgency|significance" -- packages/ apps/` prints
`apps/ui/src/api/decisionOrder.test.ts:15` and `apps/ui/src/api/decisionOrder.ts:10`
and nothing else — ZERO matches anywhere under `packages/`.

The formula lives at `apps/ui/src/api/decisionOrder.ts:21-39`:

    export function decisionUrgency(model: DecisionCardModel): number
    ...
    return (blockedCount + 1) * age;                      // line 38

with the total order applied in `orderDecisionInbox` at
`apps/ui/src/api/decisionOrder.ts:47-69`: open before resolved (:52-54), then
urgency DESCENDING (:57-61), then `id` ascending (:64-66). Its own header comment
at :3-5 states the rule "is written down nowhere else", and :7-11 records that
Remedy deliberately does NOT sort in `decisionCardModels`, in the `remedyApi.ts`
projection, or inside `DecisionInboxCard`.

Consequence, stated plainly because the T001 decision rests on it: the feature
file requires at `docs/roadmap/features/T5_F040.md:57-58` that digest significance
be "the urgency formula, one source with the inbox". That formula is a
browser-side TypeScript function and a Python digest endpoint CANNOT import it.
Its two inputs — `blocked_count` and `age_seconds` — ARE both carried by the
Python card (`packages/orchestration/decision_inbox.py:152-153`), so the
arithmetic is reproducible server-side, but reproducing it creates a SECOND home
for the rule, which is exactly what `apps/ui/src/api/decisionOrder.ts:9-11`
refuses. The three routes (compute in Python and accept two homes; have the
digest carry the inputs and let the client score; or move the formula to Python
and have the client import the number) are a decision for the T001 order.

---

## 3. The cost line and its basis

**There are TWO distinct "basis" vocabularies in this repository and they are not
the same field.** A digest that says "cost with its basis" must name which.

**(a) The report's basis = PROVENANCE.** `ReportSources.cost_basis:
tuple[str, ...]` at `packages/orchestration/run_report.py:321`, documented one
line above as "Where that number came from (BudgetCounters.actual_sources). Every
cost line names its basis (P6); a cost without a basis is not printed."
It is filled at `packages/orchestration/run_report.py:844` from
`counters.actual_sources`, and its closed value set is
`VALID_ACTUAL_SOURCES` at `packages/orchestration/budget_guard.py:34-37`:
`pingpong_actuals`, `pingpong_live`, `persisted_job_actuals`, `token_actuals`,
`aggregate_actuals` — five strings, enforced at
`packages/orchestration/budget_guard.py:100-102`. None of them says "estimated".

**(b) The ticker's basis = EXACTNESS.** Produced by `_budget_tick_payload` at
`packages/orchestration/safe_points.py:600`, key `basis` at :637-640, a nested
dict of exactly two keys with a three-value vocabulary:

    payload["basis"] = {
        "tokens": "lower_bound" if evaluation.token_lower_bound else "actual",
        "cost": cost_basis,     # "absent" | "lower_bound" | "actual"  (:631-636)
    }

**One function or two sources?** For (a), ONE: `BudgetCounters`
(`packages/orchestration/budget_guard.py:45`) carries the figure and its
provenance on the same object — `token_description()` at :178 renders the value
(`">= N tokens (M provider calls unmeasured)"` at :180-183, or `"N tokens"` at
:184), `cost_description()` at :187 renders the money
(`"not-measured"` at :190 when `measured_cost_usd is None`, `">= $X.XXXX (M
provider calls unpriced)"` at :192-195, else `"$X.XXXX"` at :196), and
`actual_sources` at :55 carries the basis. `packages/orchestration/run_report.py:839-845`
takes value AND basis AND `elapsed_seconds` off the SAME `counters` object, so no
join is needed. The renderer `_cost_lines` at
`packages/orchestration/run_report.py:550` proves the pairing is mandatory: with
no `token_description` it prints `Tokens: not recorded (no actuals persisted for
this run).` (:555) and NEVER a zero (:553-554); with one it prints
`- Tokens: <desc> — basis: <", ".join(cost_basis) or "not recorded">` (:557-558).

For (b), the value and the basis also travel together, on one tick payload, but
that payload is produced in a DIFFERENT module by a DIFFERENT function than (a).
Joining (a) and (b) into one digest line WOULD be a two-source join.

**The exact vocabulary the live cost ticker renders for an estimated basis.**
Client side, `apps/ui/src/api/costMetric.ts`:

- `const ACTUAL_BASIS = "actual";` at :58 — "The only basis string that means the
  figure is not an estimate."
- `isEstimated(basis, unit)` at :126-129: `basis[unit === "usd" ? "cost" : "tokens"] !== ACTUAL_BASIS`.
  So `lower_bound`, `absent`, an unknown string and a MISSING key all read as
  estimated (:122-125).
- `basisLine(estimated)` at :164-166 returns the tooltip sentence
  **`"Figures are an estimate"`** (or `"Figures are actual"`), pushed at :197.

And in the component `apps/ui/src/components/metrics/TopMetricsBar.tsx`:

- `const ESTIMATE_MARK = "~";` at :46 — declared to be "the BASIS channel and
  never the threshold channel" (:43-45), rendered at :106.
- `const ESTIMATE_PHRASE = ", estimated";` at :50 — "Said in words beside the
  mark, because the mark alone is punctuation a screen reader does not narrate"
  (:48-49), composed into the `aria-label` at :80 and :95.
- The literal word `estimated` is also rendered as a standing sub-label under the
  TOKENS metric at :120, styled by `.estimated` at
  `apps/ui/src/components/metrics/TopMetricsBar.module.css:116`; the `~` mark is
  styled by `.estimateMark` at the same file :107.

So the ticker's estimated vocabulary is, verbatim: the mark `~`, the aria phrase
`, estimated`, and the tooltip line `Figures are an estimate`. The feature file's
"the '~'/basis treatment (the ticker's vocabulary)" at
`docs/roadmap/features/T5_F040.md:52-53` resolves to those three strings.

`costMetricOf` (`apps/ui/src/api/costMetric.ts:171`) is the single home for every
cost render decision; its callers are `apps/ui/src/api/costReconciliation.ts:66-67`
and `apps/ui/src/api/costTicker.ts:11`
(`git grep -n "costMetricOf" -- apps/ui/src`, excluding `.test.`).

---

## 4. The ownership seam — ABSENT, and here is how it was searched

The feature file orders "top ownership sentences (≤3)" at
`docs/roadmap/features/T5_F040.md:41` and names "ownership's top entries (the
phrase catalog)" at :32-33. The producer it means is F035, which is
`docs/roadmap/STATUS.md:99`:

    - [ ] F035 — Ownership ledger

— unchecked. `docs/roadmap/features/T5_F035.md:18-20` describes the intended
producer as `ownership.py` aggregating into `ownership.json`, "rendered by ONE
phrase catalog" (:35-36 of that file).

**RESULT: no importable ownership source exists.** The commands, verbatim, and
what each matched:

| command | result |
|---------|--------|
| `git ls-files -- 'packages/*ownership*' 'apps/*ownership*' 'packages/**/*ownership*' 'apps/**/*ownership*'` | 0 paths (rc 0, empty) |
| `git grep -n -E 'ownership\.json\|ownership_ledger\|OWNERSHIP_\|OwnershipEntry' -- packages/ apps/` | 0 lines (rc 1) |
| `git grep -n -i -E 'phrase[_ ]catalog\|PHRASE_CATALOG' -- packages/ apps/` | 0 lines (rc 1) |
| `git grep -n -E 'def build_ownership\|def ownership\|class Ownership\|def .*ownership.*\(' -- packages/ apps/` | 0 lines (rc 1) |
| `git grep -n -i -E 'ownership' -- packages/orchestration/run_report.py` | 0 lines (rc 1) |
| `git grep -l -i -E 'ownership' -- packages/ apps/` | 9 files |

The nine files the last command matched are the WIDEST reading — every
case-insensitive occurrence of the substring anywhere under `packages/` or
`apps/` — and not one of them is an ownership ledger. Each was opened and
classified:

1. `apps/cli/commands/project.py:76,96,357,381` — `RepoOwnershipConflictError`, a
   git-repo binding conflict.
2. `apps/cli/commands/runtime_cmd.py:84,273,340,437,488,499,501,585` —
   process ownership of a dev-server runtime.
3. `apps/ui/src/components/diff/DiffView.tsx:103` — the word in a prose comment
   ("the ownership rule of that ...").
4. `packages/orchestration/project_registry.py:450` — repo ownership check.
5. `packages/orchestration/run_manifest.py:1960,2091,2135,2215,2381,4793,4806,5473` —
   episode/job ownership of manifest entries.
6. `packages/orchestration/safe_publish.py:7,345` — file/inode ownership at publish.
7. `packages/orchestration/structured_outputs.py:12` — "Reviewer vs planner
   ownership of the retry", a prose comment.
8. `packages/runtimes/dev_server.py:1044-2046` — process-supervision ownership
   (`OWNER_SUPERVISED`, `ownership: str` field at :1144).
9. `packages/runtimes/runtime_supervisor.py:441` — the same process ownership.

Every one is PROCESS, FILE or REPO ownership. Not one is the human-attribution
ledger F035 describes and F040's Design composes over. The absence is as wide as
the search: it covers all of `packages/` and all of `apps/`, tracked files only
(`git grep`/`git ls-files` do not read untracked or ignored paths).

The plan's second Risk (`.agent/plan.md:36-37`) states this in one line; this
section is the measurement behind it.

---

## 5. The server seam

**Registration and dispatch.** `packages/orchestration/ui_server.py` dispatches
per-job read endpoints from ONE dict comprehension of the path. The route shape
is `/api/jobs/<job_id>/<endpoint>` (comment at :3443); the guard is
`if len(parts) == 5 and parts[1] == "api" and parts[2] == "jobs":` at :3445,
`job_id_str = parts[3]` (:3446), `endpoint = parts[4]` (:3447), the job is loaded
ONCE at :3448 with `_load_job(job_id_str)` and a route that cannot load a job
returns its error before any handler runs (:3449-3451). Then a literal
`handlers` dict at :3452-3468 maps endpoint name to builder, and :3469-3472:

    handler = handlers.get(endpoint)
    if handler:
        self._send_json(200, handler(job))
        return

Fifteen endpoints are registered there: `dashboard`, `brain`, `brain-view-model`,
`live-state`, `task-progress`, `decisions`, `next-action`, `guide`, `events`,
`readiness`, `context-budget`, `story`, `checklist`, `diagnostics`, `diff`
(:3453-3467). A `remedy job digest` sibling adds exactly one line to that dict
plus one `_build_*_json(job)` function.

`_send_json` at :4144-4151 does NOT wrap: it `json.dumps(data, default=str)` and
writes the dict AS the body, with `Content-Type: application/json` and
`Cache-Control: no-store`. **There is no outer envelope** — the builder's own dict
IS the response body.

**Whether a route carries an explicit version field: YES, by convention, in the
BUILDER — never in the router.** `grep -n '"version":' packages/orchestration/ui_server.py`
returns 11 lines: :1622 (3), :1918 (3), :2428 (1), :2512 (1), :2529 (1), :2544
(2, an error envelope), :2560 (1), :2734 (3), :2797 (1), :3200 (1), :4251 (1).
Values are per-payload integers; the router at :3469-3472 adds nothing.

**The nearest endpoint to model the digest on: `decisions`.** It is the same
shape the digest is (a pure composition over one job, no storage of its own), it
is the read path the digest's open-decision count comes from, and its builder is
three lines. Its registration line, quoted from `packages/orchestration/ui_server.py:3458`:

                "decisions": _build_decisions_json,

and the builder at :2771-2775:

    def _build_decisions_json(job: Any) -> dict[str, Any]:
        """Build the decision inbox payload — every open question of one job."""
        from packages.orchestration.decision_inbox import build_decision_inbox
        events = _load_events(job)
        return build_decision_inbox(job, events)

Note the two conventions it demonstrates and the digest should follow: the
package import is LOCAL to the function, not module-level; and the version field
is owned by the composed module (`DECISION_INBOX_VERSION`,
`packages/orchestration/decision_inbox.py:37`), not by the server. The F037 diff
route at :2587-2592 is the same pattern with the envelope owned by
`packages/orchestration/diff_view_source.py`, and `_build_events_since_json` at
:2785-2801 shows the inline `"version": 1` form (:2797).

**Budget figures on the wire** reach the client through the event stream rather
than a job endpoint: `BUDGET_TICK_SUMMARY_FIELDS` at
`packages/orchestration/ui_server.py:2826`, `BUDGET_TICK_BASIS_FIELDS = ("tokens", "cost")`
at :2837, and `_budget_tick_summary_payload` at :2840, which whitelists the
nested `basis` dict field-by-field at :2868-2876 and lets an absent key stay
absent (:2851-2855). A digest endpoint wanting the ticker's basis would have to
read a budget tick event or re-derive it; it is not on any per-job read route.

---

## 6. The UI and CLI seams

**Design-reference files that bind a card of this kind.** `ls docs/ui/design_reference/`
lists 17 entries. The binding ones for a hero digest card:

- `docs/ui/design_reference/ux_spec.md` — `## 4. Glass card rules` (:36),
  `## 5. Typography` (:46), `## 8. Buttons` (:78) for the CTA,
  `## 14. States (global rules)` (:147), `## 15. Responsive behavior` (:159),
  `## 16. Reduced motion` (:167) and `## 17. Copy rules` (:173), which is the
  section the Acceptance copy audit at `docs/roadmap/features/T5_F040.md:76-77`
  ("since you were last here", not "while you slept") answers to.
- `docs/ui/design_reference/component_spec.md` — the card catalogue. Named by
  F040 at `docs/roadmap/features/T5_F040.md:14` ("digest card per
  `component_spec.md`"). ABSENCE, measured with
  `grep -n -i "hero\|digest" docs/ui/design_reference/component_spec.md`: the two
  hits are :30 and :126 and BOTH are about `LayerSwitcher` being kept out of the
  hero bar. **There is no digest card and no hero card entry in
  `component_spec.md`.** The nearest existing card entries are `AgentNowCard`
  (:75), `ActivityFeedCard` (:82), `TaskChecklistCard` (:95) and
  `NeedsAttentionCard` (:125).
- `docs/ui/design_reference/tokens.css` and `docs/ui/design_reference/tokens_rules.md`
  (`## Forbidden` at :20, `## Deviations` at :28), plus
  `docs/ui/design_reference/motion_spec.md` and
  `docs/ui/design_reference/assets_spec.md` per the feature file's own banner
  (`docs/roadmap/features/T5_F040.md:3-14`).

**The `--remedy-*` tokens of F040's binding CSS.** The CSS excerpt at
`docs/roadmap/features/T5_F040.md:46-50` uses seven tokens. Measured against the
SHIPPED sheet `apps/ui/src/styles/tokens.css` — which the feature file itself
calls the source (:14) — by extracting every `--remedy-*` NAME AT A DECLARATION
SITE (regex `(--remedy-[A-Za-z0-9-]+)\s*:`), 58 distinct tokens defined:

| token | in shipped `apps/ui/src/styles/tokens.css` | in `docs/ui/design_reference/tokens.css` |
|-------|--------------------------------------------|-------------------------------------------|
| `--remedy-radius-lg` | YES, :57 | YES, :105 |
| `--remedy-card` | YES, :48 | YES, :36 |
| `--remedy-shadow-soft` | YES, :66 | YES, :76 |
| `--remedy-font-ui` | YES, :3 | YES, :13 |
| `--remedy-ink` | YES, :6 | YES, :23 |
| `--remedy-radius-pill` | YES, :63 | YES, :106 |
| `--remedy-blue` | YES, :21 | YES, :46 |

**NONE of the seven is missing.** The reference sheet defines 131 distinct
`--remedy-*` tokens against the shipped sheet's 58, so the shipped sheet is a
subset — but not a subset that costs F040 anything. Note the one token the
feature's CSS uses that is NOT a `--remedy-*`: the literal `#fff` at
`docs/roadmap/features/T5_F040.md:50`, which `tokens_rules.md`'s `## Forbidden`
section (:20) is the authority on.

**The CLI seam for `remedy job digest <id>`.** Two registration sites, both
required:

1. The handler table `COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]]`
   at `apps/cli/commands/job.py:2354`, keyed `"<group>.<subcommand>"`. It is
   collected into the CLI at `apps/cli/commands/__init__.py:98`
   (`table.update(mod.COMMAND_HANDLERS)`, the collector docstring at :27). The
   sibling to copy, quoted from `apps/cli/commands/job.py:2395-2398`:

        "job.summary": lambda args: _cmd_job_summary(
            args.job_id,
            json_output=getattr(args, "json", False),
        ),

   The three-mode `"job.report"` entry at :2429-2440 is the richer sibling and
   the one the digest is "the report's little sibling" to
   (`docs/roadmap/features/T5_F040.md:59-60`); note it dispatches on flags
   INSIDE the lambda rather than registering a second command id.

2. The catalog entry `CommandEntry(...)` in `apps/cli/command_catalog.py`. The
   `job.summary` sibling, quoted from `apps/cli/command_catalog.py:470-479`:

        CommandEntry(
            command_id="job.summary",
            group_id="job",
            subcommand="summary",
            description="Print an honest summary of job state (truth contract).",
            action_class="read_only",
            args=(_JOB_ID, _JSON_OPT),
            supports_json=True,
            related=("job.show",),
        ),

   `job.report`'s entry at :495-512 shows the flag form
   (`ArgDef("--final", ..., is_option=True, is_flag=True)`, :504-507) a
   `--json`-plus-flags digest would need. `action_class="read_only"` is the right
   class for a pure composition.

Command-catalog conformance is guarded by `tests/cli/test_command_catalog.py`
(`git grep -ln "command_catalog" -- tests/ | wc -l` prints 65 — the catalog is
read by 65 test files, so a new entry is swept widely;
`grep -n "def test_" tests/cli/test_command_catalog.py` shows the first at :70).
The feature file's suggested test path `tests/ui_contract/test_digest.py`
(`docs/roadmap/features/T5_F040.md:92-93`) does not yet exist —
`git ls-files -- tests/ui_contract/test_digest.py` returns nothing.

---

## What T001 inherits from this measurement

1. Call `build_report_sources`, not `collect_report_sources` — only the former
   fills `open_decision_count` and `blocked`, so only the former fires rule 1.
2. `packages/orchestration/run_report.py:170` says three-tuple; the value is PAIRS.
3. The urgency formula is TypeScript-only, so "one source with the inbox" cannot
   be an import in Python — that needs a decision, not an assumption.
4. "Basis" is two vocabularies, provenance and exactness; only the second is the
   `~` the ticker renders.
5. No ownership source exists anywhere under `packages/` or `apps/`.
6. The endpoint is one line in the `handlers` dict at
   `packages/orchestration/ui_server.py:3452` plus a builder that owns its own
   version field.
