// The cockpit's mission card, its client SEAM (F305 T002, DECISIONS F305 D1 and D2; R-1248):
// decodes the two envelopes `mission_cockpit.py` answers, names their paths, and words what the
// card shows — a mission's size, an order's calls and tokens, its chain's reach and a chip's
// label. `missionCardDoor.ts` carries the doors.
//
// A cost in US dollars is never worded here: the operator reads calls and tokens (DECISION
// amend1007b D7), and the server sends no such figure for an order.
//
// PURE: no `fetch`, no `Date`, no storage, no `window`, no `document`, in code or in any string —
// `tests/ui_contracts/test_mission_card_door.py` pins that absence.

export const MISSION_COCKPIT_VERSION = 1;

/** The two labels `mission_state.py` gives a chain link whose job cannot be read; a chip that
 *  carries one has no cockpit to open. */
export const MISSING_JOB_LABEL = "(missing job)";
export const UNREADABLE_JOB_LABEL = "(unreadable job)";

export const MISSIONS_LOADING_LINE = "Loading this project's missions…";
export const MISSIONS_UNREADABLE_LINE = "This project's missions could not be read.";
export const NO_PROJECT_LINE = "No project is open, so there are no missions to show.";
export const NO_MISSIONS_LINE = "This project has no mission yet.";
export const ORDERS_LOADING_LINE = "Loading the orders…";
export const ORDERS_UNREADABLE_LINE = "The orders of this mission could not be read.";
export const NO_ORDERS_LINE = "This mission has no order yet.";
export const UNTITLED_ORDER_LINE = "An order with no text";

export interface MissionCardEntry {
  mission_id: string;
  goal: string;
  status: string;
  created_at: string;
  order_count: number;
  job_count: number;
}

export interface ProjectMissions {
  version: number;
  project_id: string;
  slug: string;
  missions: MissionCardEntry[];
  degraded: boolean;
  skipped_count: number;
}

export interface MissionTokens {
  input: number | null;
  output: number | null;
  cache_read: number | null;
  cache_creation: number | null;
}

export interface MissionOrderUsage {
  calls: number | null;
  tokens: MissionTokens;
}

export interface MissionChip {
  job_id: string;
  project_id: string;
  slug: string;
  repo_name: string;
  title: string;
  state: string;
}

export interface MissionOrderRow {
  order_id: string;
  title: string;
  created_at: string;
  kind: string;
  sealed: boolean;
  correlation_id: string;
  job_count: number;
  usage: MissionOrderUsage;
  chain: MissionChip[];
}

export interface MissionOrders {
  version: number;
  project_id: string;
  slug: string;
  mission_id: string;
  goal: string;
  orders: MissionOrderRow[];
  earlier_orders: number;
  degraded: boolean;
}

// Lenient field readers, the same reading `projectScope.ts` gives its own envelopes: a
// wrong-shaped value degrades to its own absence, never a throw.
function objectOf(value: unknown): Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : {};
}
function stringOf(value: unknown): string {
  return typeof value === "string" ? value : "";
}
function countOf(value: unknown): number {
  const usable = typeof value === "number" && Number.isFinite(value) && value >= 0;
  return usable ? (value as number) : 0;
}
function countOrNull(value: unknown): number | null {
  const usable = typeof value === "number" && Number.isFinite(value) && value >= 0;
  return usable ? (value as number) : null;
}
function booleanOf(value: unknown): boolean {
  return value === true;
}
function arrayOf(value: unknown): unknown[] {
  return Array.isArray(value) ? value : [];
}

/** One mission's card, or `null` without a string `mission_id`. */
function decodeMissionCardEntry(raw: unknown): MissionCardEntry | null {
  const obj = objectOf(raw);
  const missionId = obj["mission_id"];
  if (typeof missionId !== "string" || missionId === "") return null;
  return {
    mission_id: missionId,
    goal: stringOf(obj["goal"]),
    status: stringOf(obj["status"]),
    created_at: stringOf(obj["created_at"]),
    order_count: countOf(obj["order_count"]),
    job_count: countOf(obj["job_count"]),
  };
}

/** One chip of a chain, or `null` without a string `job_id` and `slug`. */
function decodeMissionChip(raw: unknown): MissionChip | null {
  const obj = objectOf(raw);
  const jobId = obj["job_id"];
  const slug = obj["slug"];
  if (typeof jobId !== "string" || jobId === "" || typeof slug !== "string") return null;
  return {
    job_id: jobId,
    project_id: stringOf(obj["project_id"]),
    slug,
    repo_name: stringOf(obj["repo_name"]),
    title: stringOf(obj["title"]),
    state: stringOf(obj["state"]),
  };
}

function decodeMissionOrderUsage(raw: unknown): MissionOrderUsage {
  const obj = objectOf(raw);
  const tokens = objectOf(obj["tokens"]);
  return {
    calls: countOrNull(obj["calls"]),
    tokens: {
      input: countOrNull(tokens["input"]),
      output: countOrNull(tokens["output"]),
      cache_read: countOrNull(tokens["cache_read"]),
      cache_creation: countOrNull(tokens["cache_creation"]),
    },
  };
}

/** One order row, or `null` for a value that is not an object. A row whose `order_id` is "" is
 *  kept: it holds the jobs linked before order records existed. */
function decodeMissionOrderRow(raw: unknown): MissionOrderRow | null {
  if (typeof raw !== "object" || raw === null || Array.isArray(raw)) return null;
  const obj = raw as Record<string, unknown>;
  const chain: MissionChip[] = [];
  for (const entry of arrayOf(obj["chain"])) {
    const chip = decodeMissionChip(entry);
    if (chip !== null) chain.push(chip);
  }
  return {
    order_id: stringOf(obj["order_id"]),
    title: stringOf(obj["title"]),
    created_at: stringOf(obj["created_at"]),
    kind: stringOf(obj["kind"]),
    sealed: booleanOf(obj["sealed"]),
    correlation_id: stringOf(obj["correlation_id"]),
    job_count: countOf(obj["job_count"]),
    usage: decodeMissionOrderUsage(obj["usage"]),
    chain,
  };
}

/** A project's missions: `null` for anything but a plain object of this version with a string
 *  `project_id` and an array `missions`; a bad card is dropped. NEVER THROWS. */
export function decodeProjectMissions(raw: unknown): ProjectMissions | null {
  if (typeof raw !== "object" || raw === null || Array.isArray(raw)) return null;
  const payload = raw as Record<string, unknown>;
  if (payload["version"] !== MISSION_COCKPIT_VERSION) return null;
  const projectId = payload["project_id"];
  const rawMissions = payload["missions"];
  if (typeof projectId !== "string" || !Array.isArray(rawMissions)) return null;
  const missions: MissionCardEntry[] = [];
  for (const entry of rawMissions) {
    const card = decodeMissionCardEntry(entry);
    if (card !== null) missions.push(card);
  }
  return {
    version: MISSION_COCKPIT_VERSION,
    project_id: projectId,
    slug: stringOf(payload["slug"]),
    missions,
    degraded: booleanOf(payload["degraded"]),
    skipped_count: countOf(payload["skipped_count"]),
  };
}

/** One mission's orders: `null` for anything but a plain object of this version with a string
 *  `mission_id` and an array `orders`; a bad row is dropped. NEVER THROWS. */
export function decodeMissionOrders(raw: unknown): MissionOrders | null {
  if (typeof raw !== "object" || raw === null || Array.isArray(raw)) return null;
  const payload = raw as Record<string, unknown>;
  if (payload["version"] !== MISSION_COCKPIT_VERSION) return null;
  const missionId = payload["mission_id"];
  const rawOrders = payload["orders"];
  if (typeof missionId !== "string" || !Array.isArray(rawOrders)) return null;
  const orders: MissionOrderRow[] = [];
  for (const entry of rawOrders) {
    const row = decodeMissionOrderRow(entry);
    if (row !== null) orders.push(row);
  }
  return {
    version: MISSION_COCKPIT_VERSION,
    project_id: stringOf(payload["project_id"]),
    slug: stringOf(payload["slug"]),
    mission_id: missionId,
    goal: stringOf(payload["goal"]),
    orders,
    earlier_orders: countOf(payload["earlier_orders"]),
    degraded: booleanOf(payload["degraded"]),
  };
}

/** The two routes, every part percent-encoded, as `projectScope.ts` encodes its own. */
export function projectMissionsPath(request: { project: string; token: string; baseUrl?: string }): string {
  const base = request.baseUrl || "";
  const project = encodeURIComponent(request.project);
  const token = encodeURIComponent(request.token);
  return `${base}/api/projects/${project}/missions?token=${token}`;
}
export function missionOrdersPath(
  request: { project: string; missionId: string; token: string; baseUrl?: string },
): string {
  const base = request.baseUrl || "";
  const project = encodeURIComponent(request.project);
  const missionId = encodeURIComponent(request.missionId);
  const token = encodeURIComponent(request.token);
  return `${base}/api/projects/${project}/missions/${missionId}/orders?token=${token}`;
}

function plural(count: number, one: string, many: string): string {
  return `${count} ${count === 1 ? one : many}`;
}

/** A card's size line: "2 orders · 5 jobs". */
export function missionCardLine(card: MissionCardEntry): string {
  return `${plural(card.order_count, "order", "orders")} · ${plural(card.job_count, "job", "jobs")}`;
}

/** An order's calls and tokens in words; never a cost in US dollars. */
export function orderUsageLine(usage: MissionOrderUsage): string {
  if (usage.calls === null) return "Model calls: not readable";
  if (usage.calls === 0) return "No model calls";
  const calls = plural(usage.calls, "model call", "model calls");
  const { input, output } = usage.tokens;
  if (input === null && output === null) return `${calls} · tokens not reported`;
  return `${calls} · ${input ?? 0} tokens in, ${output ?? 0} out`;
}

/** How far an order's chain reached: "3 jobs in 2 projects". */
export function chainReachLine(chain: readonly MissionChip[]): string {
  const projects = new Set(chain.map((chip) => chip.project_id || chip.slug)).size;
  return `${plural(chain.length, "job", "jobs")} in ${plural(projects, "project", "projects")}`;
}

/** A chip's first line: the project and the folder of its repository. */
export function chipLabel(chip: MissionChip): string {
  return chip.repo_name === "" ? chip.slug : `${chip.slug} · ${chip.repo_name}`;
}

/** Whether a chip's job has a cockpit to open: not one the job store no longer holds or cannot
 *  read. */
export function chipOpenable(chip: MissionChip): boolean {
  return chip.state !== MISSING_JOB_LABEL && chip.state !== UNREADABLE_JOB_LABEL;
}

/** The line under a mission's orders when older ones are not shown, or "" when none are. */
export function earlierOrdersLine(count: number): string {
  if (count <= 0) return "";
  return count === 1 ? "1 earlier order is not shown." : `${count} earlier orders are not shown.`;
}
