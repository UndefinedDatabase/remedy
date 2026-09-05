# F259 inventory — the vocabulary as the code spells it today

> Every citation on this page was read at commit `67598164cac1103dea8fc7f11c50e9e0fb34f1b1`, the head of
> `feature/f259-vocabulary` when this file was written; the commit that adds
> this file changes none of the files it cites. Each citation is
> `path:line` followed by that source line quoted verbatim in a backtick
> span, with leading and trailing whitespace removed so the span survives
> Markdown and nothing else altered. This file is a MEASUREMENT of what the
> code spells TODAY: no row is copied from `docs/roadmap/features/T2_F259.md`,
> from `.agent/decisions.md` or from memory.
>
> The CODE group of each word lists every SYMBOL in the seven sources whose
> NAME CONTAINS the word case-insensitively — plain substring containment,
> not a word-boundary match, which is why `repair_rounds_used` counts for
> Round and `truncated_input` counts for Run. A SYMBOL is a class, a
> dataclass or pydantic field, an enum member, a module-level constant, or a
> `def`; a name bound inside a function body is a local and is not a symbol.
> The set was taken with `ast`, not with `grep`.
>
> The seven sources, which are the seven `T2_F259.md` T001 names and the only
> files read for the per-word CODE and CLI groups:
> - `packages/core/models.py`
> - `packages/orchestration/pingpong_job.py`
> - `packages/orchestration/schemas/models.py`
> - `packages/orchestration/flight_plan.py`
> - `packages/orchestration/mission_state.py`
> - `packages/orchestration/data_paths.py`
> - `apps/cli/command_catalog.py`

## Project

- CODE:
  - `packages/core/models.py:235` — field/member — `project_id: str | None = None`
  - `packages/orchestration/mission_state.py:186` — field/member — `project_id: str`
  - `packages/orchestration/mission_state.py:271` — def — `def mission_dir_for_project(project_id: str, root: Path | None = None) -> Path:`
  - `packages/orchestration/mission_state.py:297` — def — `def project_ids_with_missions(root: Path | None = None) -> list[str]:`
  - `packages/orchestration/data_paths.py:83` — def — `def projects_dir(root: Path | None = None) -> Path:`
  - `apps/cli/command_catalog.py:171` — module constant — `_PROJECT_ID = ArgDef("project_id", "UUID or name of the project")`
  - `apps/cli/command_catalog.py:212` — module constant — `_PROJECT_SCOPE_OPT = ArgDef("--project", "Scope to project (slug or UUID)", required=False, is_option=True)`
  - `apps/cli/command_catalog.py:213` — module constant — `_ALL_PROJECTS_FLAG = ArgDef("--all-projects", "Show jobs from all projects", required=False, is_option=True, is_flag=True)`
- CLI:
  - GroupDef id `project` — `apps/cli/command_catalog.py:109` — `"project": GroupDef("project", "Project", "Create, inspect, and manage projects."),`
  - command id `project.create` — `apps/cli/command_catalog.py:677` — `command_id="project.create",`
  - command id `project.list` — `apps/cli/command_catalog.py:689` — `command_id="project.list",`
  - command id `project.show` — `apps/cli/command_catalog.py:698` — `command_id="project.show",`
  - command id `project.attach-repo` — `apps/cli/command_catalog.py:708` — `command_id="project.attach-repo",`
  - command id `project.attach-job` — `apps/cli/command_catalog.py:716` — `command_id="project.attach-job",`
  - command id `project.brain` — `apps/cli/command_catalog.py:724` — `command_id="project.brain",`
  - command id `project.context` — `apps/cli/command_catalog.py:734` — `command_id="project.context",`
  - command id `project.summary` — `apps/cli/command_catalog.py:745` — `command_id="project.summary",`
  - command id `project.current` — `apps/cli/command_catalog.py:755` — `command_id="project.current",`
  - command id `project.attach` — `apps/cli/command_catalog.py:768` — `command_id="project.attach",`
  - command id `project.adopt` — `apps/cli/command_catalog.py:780` — `command_id="project.adopt",`
  - command id `readiness.project` — `apps/cli/command_catalog.py:2431` — `command_id="readiness.project",`
  - command id `dashboard.project` — `apps/cli/command_catalog.py:2733` — `command_id="dashboard.project",`
- COMPETING: none found

## Order

- CODE:
  - `packages/orchestration/flight_plan.py:158` — def — `def make_flight_plan_call_recorder(`
- CLI: none in the catalog
- COMPETING:
  - `packages/orchestration/pingpong_job.py:291` — `job_file_sha256: str = ""`
  - `packages/orchestration/pingpong_job.py:829` — `def parse_job_file(text: str, repo_path: str = ".") -> JobPlan:`
  - `packages/orchestration/pingpong_job.py:943` — `def plan_job_from_file(job_file_path: str, repo_path: str = ".") -> JobPlan:`
  - `packages/orchestration/schemas/models.py:107` — `class JobIntake(_Structured):`
  - `apps/cli/command_catalog.py:3016` — `ArgDef("--job-file", "Path to Markdown job file", required=True, is_option=True),`
  - `apps/cli/command_catalog.py:3362` — `ArgDef("--job-file", "Path to Markdown job file", required=True, is_option=True),`
  - `apps/cli/command_catalog.py:2843` — `ArgDef("--task-file", "Path to large prompt file", required=False, is_option=True, default=""),`
  - `apps/cli/command_catalog.py:2888` — `ArgDef("--task-file", "Path to task file", required=False, is_option=True, default=""),`

## Mission

- CODE:
  - `packages/core/models.py:227` — field/member — `mission: str | None = None`
  - `packages/orchestration/schemas/models.py:127` — field/member — `mission_candidate: bool = False`
  - `packages/orchestration/mission_state.py:64` — module constant — `MISSION_SCHEMA_VERSION = 1`
  - `packages/orchestration/mission_state.py:66` — module constant — `MISSION_STATUS_ACTIVE = "active"`
  - `packages/orchestration/mission_state.py:67` — module constant — `MISSION_STATUS_PAUSED = "paused"`
  - `packages/orchestration/mission_state.py:68` — module constant — `MISSION_STATUS_ACHIEVED = "achieved"`
  - `packages/orchestration/mission_state.py:69` — module constant — `MISSION_STATUS_ABANDONED = "abandoned"`
  - `packages/orchestration/mission_state.py:72` — module constant — `MISSION_STATUSES = (`
  - `packages/orchestration/mission_state.py:80` — module constant — `MISSION_ROLE_INITIAL = "initial"`
  - `packages/orchestration/mission_state.py:81` — module constant — `MISSION_ROLE_FOLLOW_UP = "follow_up"`
  - `packages/orchestration/mission_state.py:82` — module constant — `MISSION_ROLES = (MISSION_ROLE_INITIAL, MISSION_ROLE_FOLLOW_UP)`
  - `packages/orchestration/mission_state.py:85` — module constant — `MAX_MISSION_GOAL_CHARS = 8_000`
  - `packages/orchestration/mission_state.py:97` — class — `class MissionError(RuntimeError):`
  - `packages/orchestration/mission_state.py:101` — class — `class MissionNotFoundError(MissionError):`
  - `packages/orchestration/mission_state.py:105` — class — `class MissionGoalImmutableError(MissionError):`
  - `packages/orchestration/mission_state.py:113` — class — `class MissionJobAlreadyLinkedError(MissionError):`
  - `packages/orchestration/mission_state.py:123` — class — `class MissionLinkRoleError(MissionError):`
  - `packages/orchestration/mission_state.py:127` — class — `class MissionVerifyFirstError(MissionError):`
  - `packages/orchestration/mission_state.py:142` — class — `class MissionJobLink:`
  - `packages/orchestration/mission_state.py:168` — class — `class Mission:`
  - `packages/orchestration/mission_state.py:193` — field/member — `mission_plan: dict[str, Any] | None = None`
  - `packages/orchestration/mission_state.py:266` — def — `def mission_root(root: Path | None = None) -> Path:`
  - `packages/orchestration/mission_state.py:271` — def — `def mission_dir_for_project(project_id: str, root: Path | None = None) -> Path:`
  - `packages/orchestration/mission_state.py:276` — def — `def mission_record_path(project_id: str, mission_id: str,`
  - `packages/orchestration/mission_state.py:283` — def — `def mission_evidence_dir(project_id: str, mission_id: str,`
  - `packages/orchestration/mission_state.py:297` — def — `def project_ids_with_missions(root: Path | None = None) -> list[str]:`
  - `packages/orchestration/mission_state.py:318` — def — `def save_mission(mission: Mission, root: Path | None = None) -> Path:`
  - `packages/orchestration/mission_state.py:340` — def — `def load_mission(project_id: str, mission_id: str,`
  - `packages/orchestration/mission_state.py:359` — def — `def list_missions_safe(project_id: str, root: Path | None = None,`
  - `packages/orchestration/mission_state.py:382` — def — `def list_missions(project_id: str, root: Path | None = None) -> list[Mission]:`
  - `packages/orchestration/mission_state.py:388` — def — `def create_mission(project_id: str, goal: str, *,`
  - `packages/orchestration/mission_state.py:419` — def — `def mission_for_job(job_id: str, root: Path | None = None) -> Mission | None:`
  - `packages/orchestration/mission_state.py:433` — def — `def link_job_to_mission(project_id: str, mission_id: str, job_id: str,`
  - `packages/orchestration/mission_state.py:470` — def — `def set_mission_status(project_id: str, mission_id: str, status: str,`
  - `packages/orchestration/mission_state.py:502` — def — `def set_mission_plan(project_id: str, mission_id: str,`
  - `packages/orchestration/mission_state.py:520` — def — `def resolve_mission_id(project_id: str, raw: str,`
  - `packages/orchestration/mission_state.py:546` — def — `def mission_job_state_label(job_id: str) -> str:`
  - `packages/orchestration/mission_state.py:568` — def — `def render_mission_chain(mission: Mission) -> list[str]:`
  - `packages/orchestration/mission_state.py:593` — def — `def render_mission_row(mission: Mission) -> str:`
  - `packages/orchestration/mission_state.py:609` — module constant — `MISSION_VERIFY_PLANNED_ID = "M000"`
  - `packages/orchestration/mission_state.py:610` — module constant — `MISSION_VERIFY_TASK_TYPE = "mission_verify"`
  - `packages/orchestration/mission_state.py:621` — module constant — `MISSION_VERIFY_FILENAME = "mission_verify.json"`
  - `packages/orchestration/mission_state.py:741` — class — `class MissionVerifyOutcome:`
  - `packages/orchestration/mission_state.py:770` — class — `class MissionFollowupRun:`
  - `packages/orchestration/mission_state.py:778` — field/member — `mission_id: str`
  - `packages/orchestration/mission_state.py:865` — def — `def mission_verify_record_path(job_id: str) -> Path:`
  - `packages/orchestration/mission_state.py:872` — def — `def write_mission_verify_record(run: MissionFollowupRun) -> Path:`
  - `packages/orchestration/mission_state.py:880` — def — `def read_mission_verify_record(job_id: str) -> dict[str, Any] | None:`
  - `packages/orchestration/mission_state.py:890` — module constant — `MISSION_FOLLOW_UP_TASK_TYPE = "mission_follow_up"`
  - `packages/orchestration/mission_state.py:909` — def — `def continue_mission(project_id: str, mission_id: str, next_step: str, *,`
  - `packages/orchestration/mission_state.py:977` — def — `def execute_mission_followup(job: Any, *, cwd: Path | None = None,`
  - `packages/orchestration/data_paths.py:131` — def — `def missions_dir(root: Path | None = None) -> Path:`
  - `apps/cli/command_catalog.py:84` — field/member — `requires_permission: bool = False`
  - `apps/cli/command_catalog.py:208` — module constant — `_AS_MISSION_FLAG = ArgDef(`
- CLI:
  - GroupDef id `mission` — `apps/cli/command_catalog.py:124` — `"mission": GroupDef("mission", "Mission", "Persistent goals above jobs, and the bounded run-loop facade (internal).", user_facing=False),`
  - command id `mission.run` — `apps/cli/command_catalog.py:1752` — `command_id="mission.run",`
  - command id `mission.ledger` — `apps/cli/command_catalog.py:1771` — `command_id="mission.ledger",`
  - command id `mission.watchdog` — `apps/cli/command_catalog.py:1785` — `command_id="mission.watchdog",`
  - command id `mission.handoff` — `apps/cli/command_catalog.py:1799` — `command_id="mission.handoff",`
  - command id `mission.report` — `apps/cli/command_catalog.py:1812` — `command_id="mission.report",`
  - command id `mission.start` — `apps/cli/command_catalog.py:1828` — `command_id="mission.start",`
  - command id `mission.list` — `apps/cli/command_catalog.py:1842` — `command_id="mission.list",`
  - command id `mission.continue` — `apps/cli/command_catalog.py:1852` — `command_id="mission.continue",`
  - command id `mission.plan` — `apps/cli/command_catalog.py:1867` — `command_id="mission.plan",`
  - command id `mission.show` — `apps/cli/command_catalog.py:1882` — `command_id="mission.show",`
  - command id `mission.achieve` — `apps/cli/command_catalog.py:1898` — `command_id="mission.achieve",`
  - command id `mission.abandon` — `apps/cli/command_catalog.py:1912` — `command_id="mission.abandon",`
  - command id `mission.pause` — `apps/cli/command_catalog.py:1926` — `command_id="mission.pause",`
  - command id `mission.resume` — `apps/cli/command_catalog.py:1940` — `command_id="mission.resume",`
- COMPETING:
  - `packages/core/models.py:227` — `mission: str | None = None`
  - `packages/orchestration/mission_state.py:85` — `MAX_MISSION_GOAL_CHARS = 8_000`

## Contract

- CODE: none in the seven sources
- CLI:
  - GroupDef id `contract` — `apps/cli/command_catalog.py:155` — `"contract": GroupDef("contract", "Contract", "Run contract inspection.", user_facing=False),`
  - command id `policy.contract` — `apps/cli/command_catalog.py:1557` — `command_id="policy.contract",`
  - command id `overnight.contract-create` — `apps/cli/command_catalog.py:3566` — `command_id="overnight.contract-create",`
  - command id `overnight.contract-show` — `apps/cli/command_catalog.py:3582` — `command_id="overnight.contract-show",`
  - command id `overnight.contract-readiness` — `apps/cli/command_catalog.py:3622` — `command_id="overnight.contract-readiness",`
  - command id `contract.inspect` — `apps/cli/command_catalog.py:4452` — `command_id="contract.inspect",`
  - command id `contract.check` — `apps/cli/command_catalog.py:4465` — `command_id="contract.check",`
  - command id `contract.set` — `apps/cli/command_catalog.py:4481` — `command_id="contract.set",`
- COMPETING:
  - `packages/orchestration/schemas/models.py:23` — `from packages.orchestration.dod_schema import DOD_SCHEMA_V, DoD`
  - `packages/orchestration/schemas/models.py:253` — `DOD_SCHEMA_V: DoD,`
  - `apps/cli/command_catalog.py:155` — `"contract": GroupDef("contract", "Contract", "Run contract inspection.", user_facing=False),`
  - `apps/cli/command_catalog.py:563` — `command_id="job.dod",`
  - `packages/core/models.py:129` — `class JobBudgets(BaseModel):`
  - `packages/core/models.py:186` — `class JobFences(BaseModel):`

## Job

- CODE:
  - `packages/core/models.py:129` — class — `class JobBudgets(BaseModel):`
  - `packages/core/models.py:186` — class — `class JobFences(BaseModel):`
  - `packages/core/models.py:222` — class — `class Job(BaseModel):`
  - `packages/orchestration/pingpong_job.py:55` — module constant — `JOB_PLANNED = "planned"`
  - `packages/orchestration/pingpong_job.py:56` — module constant — `JOB_RUNNING = "running"`
  - `packages/orchestration/pingpong_job.py:57` — module constant — `JOB_BLOCKED = "blocked"`
  - `packages/orchestration/pingpong_job.py:58` — module constant — `JOB_COMPLETED = "completed"`
  - `packages/orchestration/pingpong_job.py:59` — module constant — `JOB_PAUSED = "paused"`
  - `packages/orchestration/pingpong_job.py:63` — module constant — `JOB_STOPPED = "stopped"`
  - `packages/orchestration/pingpong_job.py:86` — field/member — `existed_before_job: bool = False`
  - `packages/orchestration/pingpong_job.py:288` — class — `class JobPlan:`
  - `packages/orchestration/pingpong_job.py:290` — field/member — `job_id: str = field(default_factory=lambda: uuid4().hex[:16])`
  - `packages/orchestration/pingpong_job.py:291` — field/member — `job_file_sha256: str = ""`
  - `packages/orchestration/pingpong_job.py:293` — field/member — `job_workspace_path: str = ""`
  - `packages/orchestration/pingpong_job.py:294` — field/member — `job_title: str = ""`
  - `packages/orchestration/pingpong_job.py:322` — field/member — `job_initial_tree: str = ""            # tree of the workspace before task 1`
  - `packages/orchestration/pingpong_job.py:323` — field/member — `job_initial_tree_ref: str = ""        # checkpoint ref keeping that tree alive`
  - `packages/orchestration/pingpong_job.py:374` — def — `def _jobs_dir() -> Path:`
  - `packages/orchestration/pingpong_job.py:381` — def — `def _persist_job(job: JobPlan) -> Path:`
  - `packages/orchestration/pingpong_job.py:389` — def — `def save_job_plan(job: JobPlan) -> Path:`
  - `packages/orchestration/pingpong_job.py:394` — def — `def load_job_plan(job_id: str) -> JobPlan | None:`
  - `packages/orchestration/pingpong_job.py:620` — def — `def _export_job(job: JobPlan) -> dict[str, Any]:`
  - `packages/orchestration/pingpong_job.py:729` — def — `def _import_job(data: dict[str, Any]) -> JobPlan:`
  - `packages/orchestration/pingpong_job.py:829` — def — `def parse_job_file(text: str, repo_path: str = ".") -> JobPlan:`
  - `packages/orchestration/pingpong_job.py:943` — def — `def plan_job_from_file(job_file_path: str, repo_path: str = ".") -> JobPlan:`
  - `packages/orchestration/pingpong_job.py:963` — def — `def job_worktree_id(job_id: str) -> str:`
  - `packages/orchestration/pingpong_job.py:967` — def — `def _create_job_workspace_copy(job: JobPlan) -> str:`
  - `packages/orchestration/pingpong_job.py:980` — def — `def _create_job_workspace(job: JobPlan) -> tuple[str, Any]:`
  - `packages/orchestration/pingpong_job.py:1013` — def — `def _acquire_job_workspace(job: JobPlan) -> tuple[str, Any]:`
  - `packages/orchestration/pingpong_job.py:1166` — def — `def _finalize_job_workspace(job: JobPlan, handle: Any) -> None:`
  - `packages/orchestration/pingpong_job.py:1618` — def — `def validate_job_task_result(result: Any) -> tuple[bool, list[str]]:`
  - `packages/orchestration/pingpong_job.py:1792` — def — `def run_job(`
  - `packages/orchestration/pingpong_job.py:2732` — module constant — `JOB_RECOVERABLE_STATES = frozenset({"active", "retained", "failed_recoverable"})`
  - `packages/orchestration/pingpong_job.py:2735` — def — `def resume_job_plan(job_id: str, **run_kwargs: Any) -> JobPlan:`
  - `packages/orchestration/pingpong_job.py:2771` — def — `def _block_job(job: JobPlan, failed_idx: int, error: str) -> None:`
  - `packages/orchestration/pingpong_job.py:2841` — def — `def export_job_report(job: JobPlan) -> dict[str, Any]:`
  - `packages/orchestration/pingpong_job.py:2946` — def — `def format_job_report_text(job: JobPlan) -> str:`
  - `packages/orchestration/pingpong_job.py:3050` — def — `def job_evidence_dir(job_id: str):`
  - `packages/orchestration/pingpong_job.py:3056` — def — `def job_postmortem_path(job_id: str):`
  - `packages/orchestration/pingpong_job.py:3062` — def — `def _write_job_postmortem_record(job: JobPlan, exc: BaseException) -> None:`
  - `packages/orchestration/pingpong_job.py:3149` — def — `def _append_job_stopped_event(job: JobPlan, signal: Any, task_id: str) -> None:`
  - `packages/orchestration/pingpong_job.py:3188` — def — `def _job_stopped_event_exists(job_id: str, request_id: str) -> bool | None:`
  - `packages/orchestration/pingpong_job.py:3220` — def — `def _stop_job(job: JobPlan, signal: Any, *, task: TaskEntry | None,`
  - `packages/orchestration/pingpong_job.py:3404` — def — `def _crosscheck_jobplan_vs_canonical(job: JobPlan, canonical_existing: list,`
  - `packages/orchestration/schemas/models.py:38` — module constant — `JOB_INTAKE_SCHEMA_V = "ji1"`
  - `packages/orchestration/schemas/models.py:107` — class — `class JobIntake(_Structured):`
  - `packages/orchestration/flight_plan.py:436` — def — `def plan_job_llm(`
  - `packages/orchestration/mission_state.py:90` — module constant — `MISSING_JOB_LABEL = "(missing job)"`
  - `packages/orchestration/mission_state.py:91` — module constant — `UNREADABLE_JOB_LABEL = "(unreadable job)"`
  - `packages/orchestration/mission_state.py:113` — class — `class MissionJobAlreadyLinkedError(MissionError):`
  - `packages/orchestration/mission_state.py:142` — class — `class MissionJobLink:`
  - `packages/orchestration/mission_state.py:145` — field/member — `job_id: str`
  - `packages/orchestration/mission_state.py:189` — field/member — `job_links: tuple[MissionJobLink, ...] = ()`
  - `packages/orchestration/mission_state.py:245` — def — `def job_ids(self) -> tuple[str, ...]:`
  - `packages/orchestration/mission_state.py:419` — def — `def mission_for_job(job_id: str, root: Path | None = None) -> Mission | None:`
  - `packages/orchestration/mission_state.py:433` — def — `def link_job_to_mission(project_id: str, mission_id: str, job_id: str,`
  - `packages/orchestration/mission_state.py:546` — def — `def mission_job_state_label(job_id: str) -> str:`
  - `packages/orchestration/mission_state.py:748` — field/member — `previous_job_id: str`
  - `packages/orchestration/mission_state.py:779` — field/member — `job_id: str`
  - `packages/orchestration/data_paths.py:58` — def — `def jobs_dir(root: Path | None = None) -> Path:`
  - `packages/orchestration/data_paths.py:63` — def — `def task_jobs_dir(root: Path | None = None) -> Path:`
  - `packages/orchestration/data_paths.py:112` — def — `def job_evidence_export_dir(job_id: str, root: Path | None = None) -> Path:`
  - `packages/orchestration/data_paths.py:117` — def — `def job_evidence_index_dir(root: Path | None = None) -> Path:`
  - `packages/orchestration/data_paths.py:153` — def — `def _classic_job_id_matches(prefix: str) -> list[str]:`
  - `packages/orchestration/data_paths.py:168` — def — `def _task_job_id_matches(prefix: str) -> list[str]:`
  - `packages/orchestration/data_paths.py:195` — def — `def resolve_job_id(raw: str) -> UUID:`
  - `packages/orchestration/data_paths.py:223` — def — `def resolve_any_job_id(raw: str) -> str:`
  - `apps/cli/command_catalog.py:170` — module constant — `_JOB_ID = ArgDef("job_id", "UUID of the job")`
- CLI:
  - GroupDef id `job` — `apps/cli/command_catalog.py:106` — `"job": GroupDef("job", "Job", "Create, inspect, and manage jobs."),`
  - command id `job.create` — `apps/cli/command_catalog.py:252` — `command_id="job.create",`
  - command id `job.list` — `apps/cli/command_catalog.py:271` — `command_id="job.list",`
  - command id `job.show` — `apps/cli/command_catalog.py:280` — `command_id="job.show",`
  - command id `job.attach-repo` — `apps/cli/command_catalog.py:324` — `command_id="job.attach-repo",`
  - command id `job.permit` — `apps/cli/command_catalog.py:333` — `command_id="job.permit",`
  - command id `job.permissions` — `apps/cli/command_catalog.py:347` — `command_id="job.permissions",`
  - command id `job.rerun` — `apps/cli/command_catalog.py:356` — `command_id="job.rerun",`
  - command id `job.stop` — `apps/cli/command_catalog.py:372` — `command_id="job.stop",`
  - command id `job.budget` — `apps/cli/command_catalog.py:390` — `command_id="job.budget",`
  - command id `job.run-next` — `apps/cli/command_catalog.py:405` — `command_id="job.run-next",`
  - command id `job.run` — `apps/cli/command_catalog.py:416` — `command_id="job.run",`
  - command id `job.plan` — `apps/cli/command_catalog.py:443` — `command_id="job.plan",`
  - command id `job.run-loop` — `apps/cli/command_catalog.py:452` — `command_id="job.run-loop",`
  - command id `job.assumptions` — `apps/cli/command_catalog.py:472` — `command_id="job.assumptions",`
  - command id `job.summary` — `apps/cli/command_catalog.py:482` — `command_id="job.summary",`
  - command id `job.status` — `apps/cli/command_catalog.py:493` — `command_id="job.status",`
  - command id `job.report` — `apps/cli/command_catalog.py:507` — `command_id="job.report",`
  - command id `job.digest` — `apps/cli/command_catalog.py:529` — `command_id="job.digest",`
  - command id `job.fences` — `apps/cli/command_catalog.py:540` — `command_id="job.fences",`
  - command id `job.context` — `apps/cli/command_catalog.py:551` — `command_id="job.context",`
  - command id `job.dod` — `apps/cli/command_catalog.py:563` — `command_id="job.dod",`
  - command id `job.fulfill` — `apps/cli/command_catalog.py:574` — `command_id="job.fulfill",`
  - command id `project.attach-job` — `apps/cli/command_catalog.py:716` — `command_id="project.attach-job",`
  - command id `job.enqueue` — `apps/cli/command_catalog.py:2208` — `command_id="job.enqueue",`
  - command id `job.pause` — `apps/cli/command_catalog.py:2217` — `command_id="job.pause",`
  - command id `job.cancel` — `apps/cli/command_catalog.py:2226` — `command_id="job.cancel",`
  - command id `job.resume-queue` — `apps/cli/command_catalog.py:2236` — `command_id="job.resume-queue",`
  - command id `readiness.job` — `apps/cli/command_catalog.py:2421` — `command_id="readiness.job",`
  - command id `job.checkpoints` — `apps/cli/command_catalog.py:2604` — `command_id="job.checkpoints",`
  - command id `job.resume` — `apps/cli/command_catalog.py:2614` — `command_id="job.resume",`
  - command id `dashboard.job` — `apps/cli/command_catalog.py:2724` — `command_id="dashboard.job",`
  - command id `guide.job` — `apps/cli/command_catalog.py:2773` — `command_id="guide.job",`
  - command id `do.job-plan` — `apps/cli/command_catalog.py:3008` — `command_id="do.job-plan",`
  - command id `do.job-run` — `apps/cli/command_catalog.py:3029` — `command_id="do.job-run",`
  - command id `do.job-resume` — `apps/cli/command_catalog.py:3275` — `command_id="do.job-resume",`
  - command id `do.job-report` — `apps/cli/command_catalog.py:3301` — `command_id="do.job-report",`
  - command id `do.job-evidence` — `apps/cli/command_catalog.py:3317` — `command_id="do.job-evidence",`
  - command id `do.job-promote` — `apps/cli/command_catalog.py:3334` — `command_id="do.job-promote",`
  - command id `do.job-flow` — `apps/cli/command_catalog.py:3354` — `command_id="do.job-flow",`
- COMPETING:
  - `packages/core/models.py:222` — `class Job(BaseModel):`
  - `packages/orchestration/pingpong_job.py:288` — `class JobPlan:`
  - `packages/orchestration/data_paths.py:63` — `def task_jobs_dir(root: Path | None = None) -> Path:`
  - `packages/orchestration/data_paths.py:153` — `def _classic_job_id_matches(prefix: str) -> list[str]:`
  - `packages/orchestration/data_paths.py:168` — `def _task_job_id_matches(prefix: str) -> list[str]:`

## Plan

- CODE:
  - `packages/core/models.py:42` — field/member — `PLANNED = "planned"`
  - `packages/core/models.py:83` — field/member — `PLANNING = "planning"`
  - `packages/core/models.py:237` — field/member — `flight_plan: dict[str, Any] | None = None`
  - `packages/orchestration/pingpong_job.py:55` — module constant — `JOB_PLANNED = "planned"`
  - `packages/orchestration/pingpong_job.py:171` — def — `def task_entry_to_planned_task(task: TaskEntry) -> PlannedTask | None:`
  - `packages/orchestration/pingpong_job.py:207` — def — `def planned_task_to_task_entry(`
  - `packages/orchestration/pingpong_job.py:288` — class — `class JobPlan:`
  - `packages/orchestration/pingpong_job.py:389` — def — `def save_job_plan(job: JobPlan) -> Path:`
  - `packages/orchestration/pingpong_job.py:394` — def — `def load_job_plan(job_id: str) -> JobPlan | None:`
  - `packages/orchestration/pingpong_job.py:943` — def — `def plan_job_from_file(job_file_path: str, repo_path: str = ".") -> JobPlan:`
  - `packages/orchestration/pingpong_job.py:2735` — def — `def resume_job_plan(job_id: str, **run_kwargs: Any) -> JobPlan:`
  - `packages/orchestration/pingpong_job.py:3404` — def — `def _crosscheck_jobplan_vs_canonical(job: JobPlan, canonical_existing: list,`
  - `packages/orchestration/schemas/models.py:36` — module constant — `PLANNER_PLAN_SCHEMA_V = "pp1"`
  - `packages/orchestration/schemas/models.py:39` — module constant — `FLIGHT_PLAN_SCHEMA_V = "flight_plan_v1"`
  - `packages/orchestration/schemas/models.py:75` — class — `class PlannerPlan(_Structured):`
  - `packages/orchestration/schemas/models.py:132` — module constant — `_MAX_FLIGHT_PLAN_TASKS = 25`
  - `packages/orchestration/schemas/models.py:133` — module constant — `_LARGE_PLAN_THRESHOLD = 12`
  - `packages/orchestration/schemas/models.py:136` — class — `class PlannedTask(_Strict):`
  - `packages/orchestration/schemas/models.py:161` — class — `class FlightPlanClarification(_Strict):`
  - `packages/orchestration/schemas/models.py:178` — class — `class FlightPlan(_Structured):`
  - `packages/orchestration/schemas/models.py:195` — field/member — `large_plan: bool = False`
  - `packages/orchestration/flight_plan.py:34` — class — `class FlightPlanResult:`
  - `packages/orchestration/flight_plan.py:37` — field/member — `plan: FlightPlan | None`
  - `packages/orchestration/flight_plan.py:48` — module constant — `_PLAN_SYSTEM_SEGMENT = """\`
  - `packages/orchestration/flight_plan.py:55` — module constant — `_PLAN_INTAKE_TEMPLATE = """\`
  - `packages/orchestration/flight_plan.py:61` — module constant — `_PLAN_REPO_FACTS_TEMPLATE = """\`
  - `packages/orchestration/flight_plan.py:68` — module constant — `_PLAN_RULES_SEGMENT = """\`
  - `packages/orchestration/flight_plan.py:93` — module constant — `_PLAN_SCHEMA_DIRECTIVE_SEGMENT = """\`
  - `packages/orchestration/flight_plan.py:111` — def — `def compose_flight_plan_prompt(`
  - `packages/orchestration/flight_plan.py:141` — def — `def _build_plan_prompt(intake_dict: dict[str, Any], *,`
  - `packages/orchestration/flight_plan.py:158` — def — `def make_flight_plan_call_recorder(`
  - `packages/orchestration/flight_plan.py:340` — module constant — `_SOURCE_PLANNER = "planner"`
  - `packages/orchestration/flight_plan.py:436` — def — `def plan_job_llm(`
  - `packages/orchestration/flight_plan.py:513` — def — `def map_flight_plan_to_tasks(plan: FlightPlan) -> list[Task]:`
  - `packages/orchestration/flight_plan.py:542` — def — `def apply_plan_budgets(`
  - `packages/orchestration/flight_plan.py:563` — def — `def apply_plan_fences(`
  - `packages/orchestration/flight_plan.py:588` — def — `def render_plan_md(`
  - `packages/orchestration/flight_plan.py:682` — def — `def write_plan_md(`
  - `packages/orchestration/flight_plan.py:700` — def — `def flight_plan_blocks_execution(job: Any) -> str | None:`
  - `packages/orchestration/flight_plan.py:715` — def — `def flight_plan_approval_open(job: Any) -> bool:`
  - `packages/orchestration/flight_plan.py:729` — def — `def auto_approve_flight_plan(`
  - `packages/orchestration/flight_plan.py:757` — class — `class ReplanRejectedError(Exception):`
  - `packages/orchestration/flight_plan.py:761` — def — `def replan(`
  - `packages/orchestration/flight_plan.py:795` — def — `def resolve_flight_plan_approval(`
  - `packages/orchestration/mission_state.py:193` — field/member — `mission_plan: dict[str, Any] | None = None`
  - `packages/orchestration/mission_state.py:502` — def — `def set_mission_plan(project_id: str, mission_id: str,`
  - `packages/orchestration/mission_state.py:609` — module constant — `MISSION_VERIFY_PLANNED_ID = "M000"`
- CLI:
  - GroupDef id `plan` — `apps/cli/command_catalog.py:118` — `"plan": GroupDef("plan", "Plan", "Read-only roadmap mirror — what is active, what is next. Proposes, never starts."),`
  - command id `job.plan` — `apps/cli/command_catalog.py:443` — `command_id="job.plan",`
  - command id `mission.plan` — `apps/cli/command_catalog.py:1867` — `command_id="mission.plan",`
  - command id `do.plan` — `apps/cli/command_catalog.py:2880` — `command_id="do.plan",`
  - command id `do.job-plan` — `apps/cli/command_catalog.py:3008` — `command_id="do.job-plan",`
  - command id `overnight.plan` — `apps/cli/command_catalog.py:3508` — `command_id="overnight.plan",`
  - command id `self.plan` — `apps/cli/command_catalog.py:3748` — `command_id="self.plan",`
  - command id `feature.plan` — `apps/cli/command_catalog.py:4367` — `command_id="feature.plan",`
  - command id `plan.status` — `apps/cli/command_catalog.py:4395` — `command_id="plan.status",`
  - command id `plan.next` — `apps/cli/command_catalog.py:4408` — `command_id="plan.next",`
- COMPETING:
  - `packages/core/models.py:237` — `flight_plan: dict[str, Any] | None = None`
  - `packages/orchestration/schemas/models.py:39` — `FLIGHT_PLAN_SCHEMA_V = "flight_plan_v1"`
  - `packages/orchestration/schemas/models.py:178` — `class FlightPlan(_Structured):`
  - `packages/orchestration/schemas/models.py:75` — `class PlannerPlan(_Structured):`
  - `packages/orchestration/mission_state.py:193` — `mission_plan: dict[str, Any] | None = None`
  - `packages/orchestration/flight_plan.py:513` — `def map_flight_plan_to_tasks(plan: FlightPlan) -> list[Task]:`

## Task

- CODE:
  - `packages/core/models.py:112` — field/member — `task_id: UUID | None = None`
  - `packages/core/models.py:117` — class — `class Task(BaseModel):`
  - `packages/core/models.py:230` — field/member — `tasks: list[Task] = Field(default_factory=list)`
  - `packages/orchestration/pingpong_job.py:37` — module constant — `TASK_PENDING = "pending"`
  - `packages/orchestration/pingpong_job.py:38` — module constant — `TASK_RUNNING = "running"`
  - `packages/orchestration/pingpong_job.py:39` — module constant — `TASK_PASSED = "passed"`
  - `packages/orchestration/pingpong_job.py:40` — module constant — `TASK_APPLIED = "applied_to_job_workspace"`
  - `packages/orchestration/pingpong_job.py:41` — module constant — `TASK_BLOCKED = "blocked"`
  - `packages/orchestration/pingpong_job.py:42` — module constant — `TASK_FAILED = "failed"`
  - `packages/orchestration/pingpong_job.py:43` — module constant — `TASK_SKIPPED = "skipped"`
  - `packages/orchestration/pingpong_job.py:48` — module constant — `TASK_SPLIT = "split"`
  - `packages/orchestration/pingpong_job.py:53` — module constant — `TASK_CLASS_DEFAULT = "standard_build"`
  - `packages/orchestration/pingpong_job.py:67` — module constant — `_TASK_BODY_LIMIT = 2000`
  - `packages/orchestration/pingpong_job.py:89` — field/member — `task_id: str = ""`
  - `packages/orchestration/pingpong_job.py:100` — field/member — `task_id: str = ""`
  - `packages/orchestration/pingpong_job.py:112` — class — `class TaskProofSummary:`
  - `packages/orchestration/pingpong_job.py:114` — field/member — `task_id: str = ""`
  - `packages/orchestration/pingpong_job.py:127` — class — `class TaskEntry:`
  - `packages/orchestration/pingpong_job.py:129` — field/member — `task_id: str = ""          # T001, T002, ... (by parse order)`
  - `packages/orchestration/pingpong_job.py:132` — field/member — `task_class: str = TASK_CLASS_DEFAULT`
  - `packages/orchestration/pingpong_job.py:159` — field/member — `task_start_tree: str = ""`
  - `packages/orchestration/pingpong_job.py:160` — field/member — `task_start_tree_ref: str = ""     # checkpoint ref protecting that tree object`
  - `packages/orchestration/pingpong_job.py:161` — field/member — `task_start_recorded_at: str = ""`
  - `packages/orchestration/pingpong_job.py:162` — field/member — `task_attempt_state: str = ""      # "" | "active" | "complete"`
  - `packages/orchestration/pingpong_job.py:171` — def — `def task_entry_to_planned_task(task: TaskEntry) -> PlannedTask | None:`
  - `packages/orchestration/pingpong_job.py:207` — def — `def planned_task_to_task_entry(`
  - `packages/orchestration/pingpong_job.py:283` — field/member — `max_tasks: int = 0`
  - `packages/orchestration/pingpong_job.py:284` — field/member — `max_tasks_source: str = "default"`
  - `packages/orchestration/pingpong_job.py:296` — field/member — `tasks: list[TaskEntry] = field(default_factory=list)`
  - `packages/orchestration/pingpong_job.py:326` — field/member — `reviewed_task_files: list[str] = field(default_factory=list)`
  - `packages/orchestration/pingpong_job.py:823` — module constant — `_TASK_HEADING_RE = re.compile(`
  - `packages/orchestration/pingpong_job.py:1084` — def — `def _reviewed_task_files(job: JobPlan) -> list[str]:`
  - `packages/orchestration/pingpong_job.py:1093` — def — `def _latest_task_proofs(job: JobPlan) -> dict[str, AppliedFileProof]:`
  - `packages/orchestration/pingpong_job.py:1618` — def — `def validate_job_task_result(result: Any) -> tuple[bool, list[str]]:`
  - `packages/orchestration/pingpong_job.py:1698` — def — `def select_next_predictable_task(job) -> tuple[object | None, list]:`
  - `packages/orchestration/pingpong_job.py:1744` — def — `def _recorded_hunk_ledger_for_task(job: Any, task: Any):`
  - `packages/orchestration/pingpong_job.py:2798` — def — `def _build_task_prompt(`
  - `packages/orchestration/pingpong_job.py:3560` — def — `def _task_stream_dir(job_id: str, task_id: str):`
  - `packages/orchestration/schemas/models.py:67` — class — `class ProposedTask(_Strict):`
  - `packages/orchestration/schemas/models.py:70` — field/member — `task_type: str`
  - `packages/orchestration/schemas/models.py:81` — field/member — `proposed_tasks: list[ProposedTask] = Field(min_length=1)`
  - `packages/orchestration/schemas/models.py:132` — module constant — `_MAX_FLIGHT_PLAN_TASKS = 25`
  - `packages/orchestration/schemas/models.py:136` — class — `class PlannedTask(_Strict):`
  - `packages/orchestration/schemas/models.py:188` — field/member — `tasks: list[PlannedTask] = Field(min_length=1)`
  - `packages/orchestration/flight_plan.py:513` — def — `def map_flight_plan_to_tasks(plan: FlightPlan) -> list[Task]:`
  - `packages/orchestration/mission_state.py:610` — module constant — `MISSION_VERIFY_TASK_TYPE = "mission_verify"`
  - `packages/orchestration/mission_state.py:645` — def — `def build_verify_first_task(previous_job: Any) -> Any:`
  - `packages/orchestration/mission_state.py:681` — def — `def is_verify_task(task: Any) -> bool:`
  - `packages/orchestration/mission_state.py:802` — def — `def run_verify_task(task: Any, *, cwd: Path | None = None,`
  - `packages/orchestration/mission_state.py:890` — module constant — `MISSION_FOLLOW_UP_TASK_TYPE = "mission_follow_up"`
  - `packages/orchestration/mission_state.py:893` — def — `def build_follow_up_task(next_step: str) -> Any:`
  - `packages/orchestration/data_paths.py:63` — def — `def task_jobs_dir(root: Path | None = None) -> Path:`
  - `packages/orchestration/data_paths.py:98` — def — `def proposed_tasks_dir(root: Path | None = None) -> Path:`
  - `packages/orchestration/data_paths.py:168` — def — `def _task_job_id_matches(prefix: str) -> list[str]:`
  - `apps/cli/command_catalog.py:176` — module constant — `_TASK_OPT = ArgDef(`
  - `apps/cli/command_catalog.py:190` — module constant — `_TASK_RUN_OPT = ArgDef(`
- CLI: none in the catalog
- COMPETING:
  - `packages/core/models.py:117` — `class Task(BaseModel):`
  - `packages/orchestration/pingpong_job.py:127` — `class TaskEntry:`
  - `packages/orchestration/schemas/models.py:67` — `class ProposedTask(_Strict):`
  - `packages/orchestration/schemas/models.py:136` — `class PlannedTask(_Strict):`
  - `packages/orchestration/pingpong_job.py:171` — `def task_entry_to_planned_task(task: TaskEntry) -> PlannedTask | None:`

## Run

- CODE:
  - `packages/core/models.py:38` — class — `class RunState(str, Enum):`
  - `packages/core/models.py:43` — field/member — `RUNNING = "running"`
  - `packages/orchestration/pingpong_job.py:38` — module constant — `TASK_RUNNING = "running"`
  - `packages/orchestration/pingpong_job.py:56` — module constant — `JOB_RUNNING = "running"`
  - `packages/orchestration/pingpong_job.py:90` — field/member — `run_id: str = ""`
  - `packages/orchestration/pingpong_job.py:101` — field/member — `run_id: str = ""`
  - `packages/orchestration/pingpong_job.py:116` — field/member — `run_id: str = ""`
  - `packages/orchestration/pingpong_job.py:146` — field/member — `run_id: str = ""`
  - `packages/orchestration/pingpong_job.py:341` — field/member — `run_manifest_path: str = ""`
  - `packages/orchestration/pingpong_job.py:342` — field/member — `run_manifest_error: str = ""`
  - `packages/orchestration/pingpong_job.py:343` — field/member — `run_manifest_created_at: str = ""`
  - `packages/orchestration/pingpong_job.py:345` — field/member — `run_manifest_required_v: int = 0          # >0 marks a job created/first-run under F012`
  - `packages/orchestration/pingpong_job.py:353` — field/member — `run_manifest_episodes: list = field(default_factory=list)  # index of episode dicts`
  - `packages/orchestration/pingpong_job.py:358` — field/member — `first_running_at: str = ""`
  - `packages/orchestration/pingpong_job.py:1792` — def — `def run_job(`
  - `packages/orchestration/pingpong_job.py:3434` — def — `def _write_run_manifest_record(job: JobPlan, *, status: str, episode_id: str,`
  - `packages/orchestration/schemas/models.py:120` — field/member — `truncated_input: bool = False`
  - `packages/orchestration/mission_state.py:770` — class — `class MissionFollowupRun:`
  - `packages/orchestration/mission_state.py:802` — def — `def run_verify_task(task: Any, *, cwd: Path | None = None,`
  - `packages/orchestration/mission_state.py:834` — def — `def runner(argv: list[str], cwd: Path | None):  # noqa: E306`
  - `packages/orchestration/data_paths.py:78` — def — `def runs_dir(root: Path | None = None) -> Path:`
  - `apps/cli/command_catalog.py:190` — module constant — `_TASK_RUN_OPT = ArgDef(`
- CLI:
  - command id `init.run` — `apps/cli/command_catalog.py:223` — `command_id="init.run",`
  - command id `status.run` — `apps/cli/command_catalog.py:237` — `command_id="status.run",`
  - command id `job.run-next` — `apps/cli/command_catalog.py:405` — `command_id="job.run-next",`
  - command id `job.run` — `apps/cli/command_catalog.py:416` — `command_id="job.run",`
  - command id `job.run-loop` — `apps/cli/command_catalog.py:452` — `command_id="job.run-loop",`
  - command id `loop.run` — `apps/cli/command_catalog.py:658` — `command_id="loop.run",`
  - command id `test.run` — `apps/cli/command_catalog.py:884` — `command_id="test.run",`
  - command id `execution.run` — `apps/cli/command_catalog.py:1322` — `command_id="execution.run",`
  - command id `worker.run` — `apps/cli/command_catalog.py:1658` — `command_id="worker.run",`
  - command id `mission.run` — `apps/cli/command_catalog.py:1752` — `command_id="mission.run",`
  - command id `do.run` — `apps/cli/command_catalog.py:2834` — `command_id="do.run",`
  - command id `do.job-run` — `apps/cli/command_catalog.py:3029` — `command_id="do.job-run",`
  - command id `overnight.run` — `apps/cli/command_catalog.py:3537` — `command_id="overnight.run",`
  - command id `local-advisor.run` — `apps/cli/command_catalog.py:3905` — `command_id="local-advisor.run",`
  - command id `review.run` — `apps/cli/command_catalog.py:4173` — `command_id="review.run",`
  - command id `ci.run` — `apps/cli/command_catalog.py:4423` — `command_id="ci.run",`
  - command id `dogfood.run-loop` — `apps/cli/command_catalog.py:4667` — `command_id="dogfood.run-loop",`
- COMPETING:
  - `packages/orchestration/pingpong_job.py:1792` — `def run_job(`
  - `packages/orchestration/pingpong_job.py:346` — `active_episode_id: str = ""               # this run episode's id (completed episodes)`
  - `packages/orchestration/pingpong_job.py:341` — `run_manifest_path: str = ""`
  - `packages/orchestration/mission_state.py:770` — `class MissionFollowupRun:`
  - `packages/orchestration/data_paths.py:78` — `def runs_dir(root: Path | None = None) -> Path:`
  - `apps/cli/command_catalog.py:884` — `command_id="test.run",`
  - `apps/cli/command_catalog.py:4667` — `command_id="dogfood.run-loop",`

## Round

- CODE:
  - `packages/orchestration/pingpong_job.py:121` — field/member — `repair_rounds_used: int = 0`
  - `packages/orchestration/pingpong_job.py:122` — field/member — `repair_rounds_allowed: int = 0`
  - `packages/orchestration/pingpong_job.py:151` — field/member — `repair_rounds_used: int = 0`
  - `packages/orchestration/pingpong_job.py:152` — field/member — `repair_rounds_allowed: int = 0`
  - `packages/orchestration/pingpong_job.py:264` — field/member — `max_rounds: int = 3`
  - `packages/orchestration/pingpong_job.py:265` — field/member — `max_rounds_source: str = "default"`
  - `packages/orchestration/pingpong_job.py:266` — field/member — `repair_rounds_allowed: int = 2`
  - `packages/orchestration/pingpong_job.py:267` — field/member — `repair_rounds_source: str = "default"`
  - `packages/orchestration/pingpong_job.py:303` — field/member — `repair_rounds_allowed: int = 0`
  - `packages/orchestration/pingpong_job.py:304` — field/member — `repair_rounds_source: str = ""`
- CLI: none in the catalog
- COMPETING:
  - `packages/orchestration/pingpong_job.py:162` — `task_attempt_state: str = ""      # "" | "active" | "complete"`
  - `packages/orchestration/pingpong_job.py:346` — `active_episode_id: str = ""               # this run episode's id (completed episodes)`

## Worker

- CODE: none in the seven sources
- CLI:
  - GroupDef id `worker` — `apps/cli/command_catalog.py:113` — `"worker": GroupDef("worker", "Worker", "Manage worker connections."),`
  - command id `worker.list` — `apps/cli/command_catalog.py:1589` — `command_id="worker.list",`
  - command id `worker.recommend` — `apps/cli/command_catalog.py:1599` — `command_id="worker.recommend",`
  - command id `worker.show` — `apps/cli/command_catalog.py:1610` — `command_id="worker.show",`
  - command id `worker.explain` — `apps/cli/command_catalog.py:1621` — `command_id="worker.explain",`
  - command id `worker.resources` — `apps/cli/command_catalog.py:1632` — `command_id="worker.resources",`
  - command id `worker.unload` — `apps/cli/command_catalog.py:1642` — `command_id="worker.unload",`
  - command id `worker.run` — `apps/cli/command_catalog.py:1658` — `command_id="worker.run",`
  - command id `worker.status` — `apps/cli/command_catalog.py:1678` — `command_id="worker.status",`
  - command id `worker.registry-list` — `apps/cli/command_catalog.py:1690` — `command_id="worker.registry-list",`
  - command id `worker.registry-show` — `apps/cli/command_catalog.py:1700` — `command_id="worker.registry-show",`
  - command id `worker.registry-integrity` — `apps/cli/command_catalog.py:1710` — `command_id="worker.registry-integrity",`
  - command id `worker.doctor` — `apps/cli/command_catalog.py:1720` — `command_id="worker.doctor",`
  - command id `worker.add` — `apps/cli/command_catalog.py:1730` — `command_id="worker.add",`
  - command id `worker.disable` — `apps/cli/command_catalog.py:1740` — `command_id="worker.disable",`
  - command id `self-repair.worker-prompt` — `apps/cli/command_catalog.py:4859` — `command_id="self-repair.worker-prompt",`
- COMPETING:
  - `packages/orchestration/pingpong_job.py:246` — `builder: str = "fake"`
  - `packages/orchestration/pingpong_job.py:248` — `reviewer: str = "fake"`
  - `packages/orchestration/pingpong_job.py:250` — `builder_model: str = ""`
  - `packages/orchestration/pingpong_job.py:254` — `reviewer_model: str = ""`

## Decision

- CODE: none in the seven sources
- CLI:
  - GroupDef id `decision` — `apps/cli/command_catalog.py:103` — `"decision": GroupDef("decision", "Decision", "Human decision queue."),`
  - command id `decision.list` — `apps/cli/command_catalog.py:2678` — `command_id="decision.list",`
  - command id `decision.show` — `apps/cli/command_catalog.py:2687` — `command_id="decision.show",`
  - command id `decision.resolve` — `apps/cli/command_catalog.py:2700` — `command_id="decision.resolve",`
  - command id `decision.explain` — `apps/cli/command_catalog.py:2714` — `command_id="decision.explain",`
- COMPETING:
  - `packages/orchestration/flight_plan.py:303` — `def apply_clarification_answers(`
  - `packages/orchestration/flight_plan.py:715` — `def flight_plan_approval_open(job: Any) -> bool:`
  - `packages/orchestration/flight_plan.py:729` — `def auto_approve_flight_plan(`
  - `packages/orchestration/flight_plan.py:795` — `def resolve_flight_plan_approval(`

## Evidence

- CODE:
  - `packages/orchestration/pingpong_job.py:281` — field/member — `stream_evidence: bool = False`
  - `packages/orchestration/pingpong_job.py:282` — field/member — `stream_evidence_source: str = "default"`
  - `packages/orchestration/pingpong_job.py:3050` — def — `def job_evidence_dir(job_id: str):`
  - `packages/orchestration/mission_state.py:283` — def — `def mission_evidence_dir(project_id: str, mission_id: str,`
  - `packages/orchestration/data_paths.py:103` — def — `def evidence_exports_dir(root: Path | None = None) -> Path:`
  - `packages/orchestration/data_paths.py:112` — def — `def job_evidence_export_dir(job_id: str, root: Path | None = None) -> Path:`
  - `packages/orchestration/data_paths.py:117` — def — `def job_evidence_index_dir(root: Path | None = None) -> Path:`
- CLI:
  - command id `do.evidence` — `apps/cli/command_catalog.py:2970` — `command_id="do.evidence",`
  - command id `do.job-evidence` — `apps/cli/command_catalog.py:3317` — `command_id="do.job-evidence",`
- COMPETING:
  - `packages/orchestration/pingpong_job.py:112` — `class TaskProofSummary:`
  - `packages/orchestration/pingpong_job.py:154` — `apply_manifest: ApplyManifest | None = None`
  - `packages/orchestration/pingpong_job.py:341` — `run_manifest_path: str = ""`

## Gate

- CODE: none in the seven sources
- CLI: none in the catalog
- COMPETING:
  - `packages/orchestration/flight_plan.py:700` — `def flight_plan_blocks_execution(job: Any) -> str | None:`
  - `packages/orchestration/pingpong_job.py:1618` — `def validate_job_task_result(result: Any) -> tuple[bool, list[str]]:`
  - `packages/orchestration/pingpong_job.py:57` — `JOB_BLOCKED = "blocked"`
  - `apps/cli/command_catalog.py:154` — `"integrity": GroupDef("integrity", "Integrity", "Pre-handoff integrity checks.", user_facing=False),`

## Verdict

- CODE:
  - `packages/orchestration/pingpong_job.py:120` — field/member — `reviewer_verdict: str = ""`
  - `packages/orchestration/pingpong_job.py:150` — field/member — `reviewer_verdict: str = ""`
  - `packages/orchestration/pingpong_job.py:329` — field/member — `handoff_coverage_verdict: str = ""    # "PASS" | "FAIL" | ""`
  - `packages/orchestration/schemas/models.py:35` — module constant — `REVIEW_VERDICT_SCHEMA_V = "rv1"`
  - `packages/orchestration/schemas/models.py:41` — module constant — `Verdict = Literal["pass", "fail", "needs_repair", "blocked"]`
  - `packages/orchestration/schemas/models.py:56` — class — `class ReviewVerdict(_Structured):`
  - `packages/orchestration/schemas/models.py:61` — field/member — `verdict: Verdict`
- CLI: none in the catalog
- COMPETING:
  - `packages/orchestration/pingpong_job.py:39` — `TASK_PASSED = "passed"`
  - `packages/orchestration/pingpong_job.py:42` — `TASK_FAILED = "failed"`
  - `packages/orchestration/schemas/models.py:41` — `Verdict = Literal["pass", "fail", "needs_repair", "blocked"]`

## Roadmap

- CODE: none in the seven sources
- CLI: none in the catalog
- COMPETING:
  - `apps/cli/command_catalog.py:118` — `"plan": GroupDef("plan", "Plan", "Read-only roadmap mirror — what is active, what is next. Proposes, never starts."),`

## Catalog totals

Obtained by importing `apps.cli.command_catalog` and calling `len()`, never
by grepping. The exact expression stands beside each number.

- `len(GROUPS)` = 60
- `len(CATALOG)` = 342
- `len([g for g in GROUPS.values() if g.user_facing])` = 17

The 17 user-facing group ids, in sorted order: `config`, `decision`, `do`, `doctor`, `init`, `job`, `loop`, `memory`, `plan`, `project`, `queue`, `runtime`, `stats`, `status`, `teach`, `ui`, `worker`.

## Where the unrowed words live

DECISION amend0905-vocab D1 names Decision, Evidence, Gate and Verdict
without giving them a table row. Each entry below names the module that
DEFINES the concept, with one citation. This is the only part of this file
that looks outside the seven sources; the paths searched were every `.py`
file under `packages/` and under `apps/`, by class name
(`class [A-Za-z]*<Word>[A-Za-z]*`) and by module name.

- **Decision** — `packages/orchestration/decision_queue.py`, the record type of the human decision queue that the user-facing `decision` command group reads. Citation: `packages/orchestration/decision_queue.py:45` — `class HumanDecision:`
- **Evidence** — `packages/orchestration/pingpong_evidence.py`, the builder of the evidence bundle — the function that says what an evidence folder consists of. Citation: `packages/orchestration/pingpong_evidence.py:98` — `def build_evidence_bundle(`
- **Gate** — `packages/orchestration/dod_gate.py`, the only type in `packages/` named for the concept itself rather than for one particular gate; its docstring reads "What the gate decided, and everything it decided it from.". Citation: `packages/orchestration/dod_gate.py:101` — `class GateResult:`
- **Verdict** — `packages/orchestration/schemas/models.py`, the named type, and one of the seven sources; every other verdict in the seven sources is an untyped `str`. Citation: `packages/orchestration/schemas/models.py:41` — `Verdict = Literal["pass", "fail", "needs_repair", "blocked"]`

The search also measured how far each of the four is spread, which is a fact
about the code and is recorded rather than resolved. Across every `.py` file
under `packages/`, the pattern `class [A-Za-z]*<Word>[A-Za-z]*` matches
19 classes for Evidence, 22 for Decision, 4 for Verdict and 6 for Gate.
