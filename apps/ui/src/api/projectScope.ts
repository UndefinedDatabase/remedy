// The multi-project cockpit's client SEAM (T5_F042 T002, DECISION F042 D2): decodes the
// project-list, project-summary and job-project envelopes `project_cockpit.py` and
// `_build_job_project_json` compose, names their paths, reads/writes the address's
// `?project=` parameter, resolves the ACTIVE project by DECISION F042 D1's precedence, and
// gates a project switch so only the LATEST one applies. `remedyApi.ts` carries the doors.
//
// PURE: no `fetch`, no `Date`, no storage, no `window`, no `document`, in code or in any
// string — `tests/ui_contracts/test_project_scope_door.py` pins that absence.

export const PROJECT_COCKPIT_VERSION = 1;

/** Job-scoped address parameters a project switch drops: each names a node, task or job of
 *  the project being left. */
export const JOB_SCOPED_PARAMS: readonly string[] = ["job", "job_id", "focus", "level", "tab"];

export interface ProjectEntry {
  id: string;
  slug: string;
  name: string;
  repo_path: string | null;
  repo_reachable: boolean;
  fix_it: string | null;
}

export interface DefaultProject {
  id: string;
  slug: string;
  source: string;
}

export interface ProjectsView {
  version: number;
  projects: ProjectEntry[];
  default_project: DefaultProject | null;
  single_project: boolean;
  unscoped_jobs: number;
  orphaned_jobs: number;
}

export interface ProjectJobCounts {
  active: number;
  total: number;
}

export interface ProjectLastResult {
  job_id: string;
  title: string;
  state: string;
  headline: string;
}

export interface ProjectCostToday {
  day: string;
  value_usd: number | null;
  basis: string;
  calls: number;
}

export interface ProjectDecisions {
  open_count: number;
  peak_urgency: number;
}

export interface ProjectSummary {
  version: number;
  project_id: string;
  slug: string;
  jobs: ProjectJobCounts;
  last_result: ProjectLastResult | null;
  cost_today: ProjectCostToday;
  decisions: ProjectDecisions;
  degraded: boolean;
}

/** The three scopes `job_project_view` can label a job with. */
export type JobProjectScope = "project" | "unscoped" | "orphaned";

export interface JobProject {
  version: number;
  job_id: string;
  scope: JobProjectScope;
  project: ProjectEntry | null;
}

// Lenient field readers shared by every decoder below — the same reading `jobDigest.ts`
// gives its own payload: a wrong-shaped value degrades to its own absence, never a throw.
function objectOf(value: unknown): Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : {};
}
function stringOf(value: unknown): string {
  return typeof value === "string" ? value : "";
}
function nullableStringOf(value: unknown): string | null {
  return typeof value === "string" ? value : null;
}
function countOf(value: unknown): number {
  const usable = typeof value === "number" && Number.isFinite(value) && value >= 0;
  return usable ? (value as number) : 0;
}
function booleanOf(value: unknown): boolean {
  return value === true;
}
function numberOrNull(value: unknown): number | null {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}
function basisOf(value: unknown): string {
  return typeof value === "string" && value !== "" ? value : "absent";
}

/** One project's list entry, card project or job-project's project — `null` without a string
 *  `id` and `slug`, dropped rather than guessed at. */
function decodeProjectEntry(raw: unknown): ProjectEntry | null {
  const obj = objectOf(raw);
  const id = obj["id"];
  const slug = obj["slug"];
  if (typeof id !== "string" || typeof slug !== "string") return null;
  return {
    id,
    slug,
    name: stringOf(obj["name"]),
    repo_path: nullableStringOf(obj["repo_path"]),
    repo_reachable: booleanOf(obj["repo_reachable"]),
    fix_it: nullableStringOf(obj["fix_it"]),
  };
}

function decodeDefaultProject(raw: unknown): DefaultProject | null {
  const obj = objectOf(raw);
  const id = obj["id"];
  const slug = obj["slug"];
  if (typeof id !== "string" || typeof slug !== "string") return null;
  return { id, slug, source: stringOf(obj["source"]) };
}

function decodeProjectJobCounts(raw: unknown): ProjectJobCounts {
  const obj = objectOf(raw);
  return { active: countOf(obj["active"]), total: countOf(obj["total"]) };
}

/** A project's newest job, or `null` for a `last_result` with no string `job_id`. */
function decodeProjectLastResult(raw: unknown): ProjectLastResult | null {
  const obj = objectOf(raw);
  const jobId = obj["job_id"];
  if (typeof jobId !== "string") return null;
  return {
    job_id: jobId,
    title: stringOf(obj["title"]),
    state: stringOf(obj["state"]),
    headline: stringOf(obj["headline"]),
  };
}

function decodeProjectCostToday(raw: unknown): ProjectCostToday {
  const obj = objectOf(raw);
  return {
    day: stringOf(obj["day"]),
    value_usd: numberOrNull(obj["value_usd"]),
    basis: basisOf(obj["basis"]),
    calls: countOf(obj["calls"]),
  };
}

function decodeProjectDecisions(raw: unknown): ProjectDecisions {
  const obj = objectOf(raw);
  return { open_count: countOf(obj["open_count"]), peak_urgency: countOf(obj["peak_urgency"]) };
}

/** The project list: `null` for anything but a plain object of this version whose `projects`
 *  is an array; a bad entry is dropped, a bad `default_project` reads as `null`. NEVER
 *  THROWS. */
export function decodeProjectsView(raw: unknown): ProjectsView | null {
  if (typeof raw !== "object" || raw === null || Array.isArray(raw)) return null;
  const payload = raw as Record<string, unknown>;
  if (payload["version"] !== PROJECT_COCKPIT_VERSION) return null;
  const rawProjects = payload["projects"];
  if (!Array.isArray(rawProjects)) return null;
  const projects: ProjectEntry[] = [];
  for (const entry of rawProjects) {
    const decoded = decodeProjectEntry(entry);
    if (decoded !== null) projects.push(decoded);
  }
  return {
    version: PROJECT_COCKPIT_VERSION,
    projects,
    default_project: decodeDefaultProject(payload["default_project"]),
    single_project: booleanOf(payload["single_project"]),
    unscoped_jobs: countOf(payload["unscoped_jobs"]),
    orphaned_jobs: countOf(payload["orphaned_jobs"]),
  };
}

/** One project's summary card: `null` for anything but a plain object of this version with a
 *  string `project_id`. NEVER THROWS. */
export function decodeProjectSummary(raw: unknown): ProjectSummary | null {
  if (typeof raw !== "object" || raw === null || Array.isArray(raw)) return null;
  const payload = raw as Record<string, unknown>;
  if (payload["version"] !== PROJECT_COCKPIT_VERSION) return null;
  const projectId = payload["project_id"];
  if (typeof projectId !== "string") return null;
  return {
    version: PROJECT_COCKPIT_VERSION,
    project_id: projectId,
    slug: stringOf(payload["slug"]),
    jobs: decodeProjectJobCounts(payload["jobs"]),
    last_result: decodeProjectLastResult(payload["last_result"]),
    cost_today: decodeProjectCostToday(payload["cost_today"]),
    decisions: decodeProjectDecisions(payload["decisions"]),
    degraded: booleanOf(payload["degraded"]),
  };
}

/** The project a job belongs to: `null` for anything but a plain object of this version with
 *  a string `job_id`, a `scope` of the three named, and — for `scope: "project"` — a
 *  decodable `project`. NEVER THROWS. */
export function decodeJobProject(raw: unknown): JobProject | null {
  if (typeof raw !== "object" || raw === null || Array.isArray(raw)) return null;
  const payload = raw as Record<string, unknown>;
  if (payload["version"] !== PROJECT_COCKPIT_VERSION) return null;
  const jobId = payload["job_id"];
  if (typeof jobId !== "string") return null;
  const scope = payload["scope"];
  if (scope !== "project" && scope !== "unscoped" && scope !== "orphaned") return null;
  if (scope === "project") {
    const project = decodeProjectEntry(payload["project"]);
    if (project === null) return null;
    return { version: PROJECT_COCKPIT_VERSION, job_id: jobId, scope, project };
  }
  return { version: PROJECT_COCKPIT_VERSION, job_id: jobId, scope, project: null };
}

/** The three routes above, every part percent-encoded — the same reasons `jobDigestPath`
 *  documents for its own `&` and `/`. */
export function projectsViewPath(request: { token: string; baseUrl?: string }): string {
  const base = request.baseUrl || "";
  return `${base}/api/projects?token=${encodeURIComponent(request.token)}`;
}
export function projectSummaryPath(request: { project: string; token: string; baseUrl?: string }): string {
  const base = request.baseUrl || "";
  const project = encodeURIComponent(request.project);
  const token = encodeURIComponent(request.token);
  return `${base}/api/projects/${project}/summary?token=${token}`;
}
export function jobProjectPath(request: { jobId: string; token: string; baseUrl?: string }): string {
  const base = request.baseUrl || "";
  const jobId = encodeURIComponent(request.jobId);
  const token = encodeURIComponent(request.token);
  return `${base}/api/jobs/${jobId}/project?token=${token}`;
}

/** The `project` parameter of the page's own address, trimmed, or "" when the address names
 *  none. */
export function projectFromSearch(search: string): string {
  return (new URLSearchParams(search).get("project") ?? "").trim();
}

/** `search` after a switch to *slug*: every `JOB_SCOPED_PARAMS` name is removed (each names a
 *  node, task or job of the project being LEFT), `project` is set to *slug*, and `job` is set
 *  to *jobId* only when that project has one to open. Every other parameter stays in place. */
export function searchForProjectSwitch(search: string, slug: string, jobId: string): string {
  const params = new URLSearchParams(search);
  for (const name of JOB_SCOPED_PARAMS) params.delete(name);
  params.set("project", slug);
  if (jobId !== "") params.set("job", jobId);
  return `?${params.toString()}`;
}

/** The ACTIVE project, by DECISION F042 D1's precedence: the address by slug or id, else the
 *  opened job's own project, else the server's default, else `null`. */
export function resolveActiveProject(
  view: ProjectsView | null,
  urlProject: string,
  jobProject: JobProject | null,
): ProjectEntry | null {
  if (view === null) return null;
  if (urlProject !== "") {
    const bySearch = view.projects.find((p) => p.slug === urlProject || p.id === urlProject);
    if (bySearch) return bySearch;
  }
  const jobProjectId = jobProject?.project?.id;
  if (jobProjectId) {
    const byJob = view.projects.find((p) => p.id === jobProjectId);
    if (byJob) return byJob;
  }
  const defaultId = view.default_project?.id;
  if (defaultId) {
    const byDefault = view.projects.find((p) => p.id === defaultId);
    if (byDefault) return byDefault;
  }
  return null;
}

/** True only for a decoded view that is not `single_project` and carries more than one
 *  project to switch between. */
export function switcherVisible(view: ProjectsView | null): boolean {
  return view !== null && !view.single_project && view.projects.length > 1;
}

/** The job id a switch to this summary's project should open, or "" for a project with none. */
export function switchTargetJob(summary: ProjectSummary | null): string {
  return summary?.last_result?.job_id ?? "";
}

/** A ticket `begin` hands out: current only until the NEXT `begin`, whatever key that one
 *  names — even a second switch to THIS ticket's own key retires it, so a stale answer for a
 *  project the reader left and came back to is still dropped. */
export interface SwitchTicket {
  key: string;
  isCurrent(): boolean;
}

/** The gate a project switch takes its ticket from. */
export interface SwitchGate {
  current(): string;
  begin(key: string): SwitchTicket;
}

/** What a completed switch hands `apply`: the project, the job id to open (possibly none),
 *  and the summary that arrived (possibly none, for a failed read). */
export interface ProjectSwitch {
  slug: string;
  jobId: string;
  summary: ProjectSummary | null;
}

/** A fresh switch gate, its current key starting at `initialKey`. */
export function createSwitchGate(initialKey: string = ""): SwitchGate {
  let key = initialKey;
  let generation = 0;
  return {
    current: () => key,
    begin: (nextKey: string): SwitchTicket => {
      generation += 1;
      const ticketGeneration = generation;
      key = nextKey;
      return { key: nextKey, isCurrent: () => ticketGeneration === generation };
    },
  };
}

/** Switch to project *slug*: takes a ticket from *gate*, awaits `loadSummary(slug)` (a throw
 *  reads as `null`), and calls `apply` ONLY while the ticket is still current — a stale
 *  answer is dropped rather than applied out of order. Answers whether `apply` ran. */
export async function switchProject(
  slug: string,
  gate: SwitchGate,
  loadSummary: (slug: string) => Promise<ProjectSummary | null>,
  apply: (result: ProjectSwitch) => void,
): Promise<boolean> {
  const ticket = gate.begin(slug);
  let summary: ProjectSummary | null;
  try {
    summary = await loadSummary(slug);
  } catch {
    summary = null;
  }
  if (!ticket.isCurrent()) return false;
  apply({ slug, jobId: switchTargetJob(summary), summary });
  return true;
}
