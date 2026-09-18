
## DECISION F269 D2 (2026-09-18, reviewer, round 1) — the contract record's shape on the mission
CONTEXT: `docs/roadmap/features/T2_F269.md` Design names the fields — `contract.criteria[]` with
`text`, `blocking`, `check`, `status`, `evidence_ref`, the `origin` of DECISION amend0911-feedback
D5, `contract.template` and `contract.amendments[]` — and leaves their exact encoding open. Measured
at `0955dd4c`: `Mission.contract` in `packages/orchestration/mission_state.py` is an optional dict
that `set_mission_contract` stores without a shape, and only tests call that setter. The feature
file reserves the number D1 for the template format, which T003 records; this round takes D2 and D3.
CHOSEN: the body is one JSON object `{"schema": "contract_v1", "template": <name or null>,
"criteria": [...], "amendments": [...]}`, owned by a new module
`packages/orchestration/mission_contract.py` that validates it on read and on write and is the only
production writer of `Mission.contract`. A criterion is `{"id", "text", "blocking", "origin",
"milestones", "check", "status", "evidence_ref"}`: `id` is `C` plus three digits, unique in the
contract, kept in list order; `text` is non-empty after stripping; `blocking` is a bool, true by
default; `origin` is one of `template`, `planner`, `amendment`; `milestones` is a list of mission-plan
milestone ids, empty meaning the whole mission; `check` is null until T002 compiles it through
F061's compiler, otherwise an object; `status` is one of `open`, `met`, `unmet`, `open` by default;
`evidence_ref` is null or a non-empty string. `amendments` is a list of objects stored verbatim;
T004 rules an entry's fields. A body that breaks any of these rules is refused with an error naming
the rule, on read as well as on write — never repaired and never half-loaded.
`set_mission_contract` stays the storage call underneath, and its docstring points at the new module.
ALTERNATIVES: a pydantic model beside `dod_schema.py`, rejected because the mission record is a
frozen dataclass stored through `to_json`, and the smaller shape keeps one serialisation style per
record; criteria keyed by id in an object, rejected because order is what the renderers print.
REVERSE: delete `packages/orchestration/mission_contract.py` with its tests and this paragraph;
`Mission.contract` is still an optional dict underneath.

## DECISION F269 D3 (2026-09-18, reviewer, round 1) — the job slice is computed from the milestone a job was dispatched for, and the two renderers
CONTEXT: T2_F269.md Design rules "which criteria this job's tasks serve, computed from the mission
plan". Measured at `0955dd4c`: the mission plan holds milestones, and the orchestrator's dispatch
branch in `packages/orchestration/orchestrator_loop.py` passes `payload["milestone_id"]` to
`attach_milestone_dod` but writes it nowhere on the job, so no stored field says which milestone a
job serves. A job made by `remedy do` or by `mission continue` serves no milestone.
CHOSEN: (1) the dispatch branch records the milestone on the job as `metadata["milestone_id"]`,
through one function of `mission_contract.py` that returns False and writes nothing when the job
record does not exist. (2) A job's slice is every criterion whose `milestones` is empty plus every
criterion whose `milestones` contains the job's milestone, in contract order; a job with no
milestone gets the whole-mission criteria only. The slice is a subset of the mission's criteria by
construction. (3) `remedy mission contract <id>` and `remedy job contract <id>` are read-only,
support `--json`, and live in a new `apps/cli/commands/contract_cmd.py`; `mission contract` takes
the same project scope option `mission show` takes. A mission or job id that matches nothing exits
1. A mission with no contract, and a job that belongs to no mission, print one sentence saying so
and exit 0, with `"contract": null` under `--json`. A contract body that fails D2's rules exits 1
with the rule it broke.
ALTERNATIVES: derive the milestone from the job's `dod.json`, rejected because a milestone without
a `dod_ref` stores no DoD and would then serve nothing; record the milestone on the mission's job
link, rejected because `MissionJobLink` is shared with every mission reader and a job-side key
changes no mission record. REVERSE: drop the dispatch call, delete the two commands with their
catalog entries and tests, and delete this paragraph.
