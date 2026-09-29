/**
 * The guided result tour's pure half (F036 T003, DECISION F036 D5).
 *
 * The overlay shows the tour the job's terminal state offers a human, as the job's tour
 * route serves it (`GET /api/jobs/<job_id>/tour`) — the SAME view the command line's `tour`
 * section shows (`_tour_section` in `apps/cli/commands/job.py`), built by `tour_view` in
 * `packages/orchestration/result_tour.py`. This module decodes that view, builds its path,
 * and holds every rule the overlay applies: its loading/unreadable/empty/stops states, which
 * stop neighbours next and previous reach, the step label, each stop's progress, and a plain
 * label for each anchor kind.
 *
 * IT OPENS NO SOCKET, READS NO CLOCK AND KEEPS NO STORAGE: the one read goes through
 * `loadTourView` in `remedyApi.ts`, and this module owns nothing but the view it is handed.
 *
 * THE DECODER REFUSES WHOLE. A stop, anchor or dropped entry it cannot read makes the whole
 * view unreadable rather than silently shorter — a tour that quietly drops a stop would say
 * less than the job's own records do.
 */

/** One anchor into the job's own records, as a tour stop points to it. */
export interface TourAnchor {
  kind: string;
  ref: string;
}

/** One tour stop: a title, a body and where it points. */
export interface TourStop {
  title: string;
  body: string;
  anchor: TourAnchor;
}

/** One stop the resolver dropped, with the reason it gives. */
export interface TourDrop {
  title: string;
  reason: string;
}

/** The tour itself, as `result_tour.py` builds it. */
export interface ResultTour {
  schema: string;
  jobId: string;
  generator: string;
  stops: TourStop[];
  dropped: TourDrop[];
}

/** The tour route's whole envelope: the tour to show, and whether it is the stored one. */
export interface TourView {
  stored: boolean;
  version: number;
  tour: ResultTour;
  error: string;
}

const TOUR_SCHEMA = "remedy.tour.v1";

/** The five anchor kinds, in `TOUR_ANCHOR_KINDS`'s own order in `result_tour.py`. */
export const TOUR_ANCHOR_KINDS = ["node", "diff", "evidence", "command", "preview"] as const;

/** The most stops a tour may hold — `MAX_TOUR_STOPS` in `result_tour.py`. */
export const MAX_TOUR_STOPS = 8;

function recordOf(value: unknown): Record<string, unknown> | null {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>) : null;
}

function textOf(value: unknown): string | null {
  return typeof value === "string" ? value : null;
}

function tourAnchorOf(value: unknown): TourAnchor | null {
  const anchor = recordOf(value);
  if (anchor === null) return null;
  const kind = textOf(anchor["kind"]);
  const ref = textOf(anchor["ref"]);
  if (kind === null || !(TOUR_ANCHOR_KINDS as readonly string[]).includes(kind)) return null;
  if (ref === null || ref === "") return null;
  return { kind, ref };
}

function tourStopOf(value: unknown): TourStop | null {
  const stop = recordOf(value);
  if (stop === null) return null;
  const title = textOf(stop["title"]);
  const body = textOf(stop["body"]);
  const anchor = tourAnchorOf(stop["anchor"]);
  if (title === null || body === null || anchor === null) return null;
  return { title, body, anchor };
}

function tourDropOf(value: unknown): TourDrop | null {
  const drop = recordOf(value);
  if (drop === null) return null;
  const title = textOf(drop["title"]);
  const reason = textOf(drop["reason"]);
  if (title === null || reason === null) return null;
  return { title, reason };
}

function resultTourOf(value: unknown): ResultTour | null {
  const tour = recordOf(value);
  if (tour === null) return null;
  const schema = textOf(tour["schema"]);
  const jobId = textOf(tour["job_id"]);
  const generator = textOf(tour["generator"]);
  const rawStops = tour["stops"];
  const rawDropped = tour["dropped"];
  if (schema !== TOUR_SCHEMA || jobId === null || generator === null
      || !Array.isArray(rawStops) || !Array.isArray(rawDropped)) {
    return null;
  }
  if (rawStops.length > MAX_TOUR_STOPS) return null;
  const stops = rawStops.map(tourStopOf);
  if (stops.some((s) => s === null)) return null;
  const dropped = rawDropped.map(tourDropOf);
  if (dropped.some((d) => d === null)) return null;
  return { schema, jobId, generator, stops: stops as TourStop[], dropped: dropped as TourDrop[] };
}

/** The tour route's envelope, or `null` when any part of it cannot be read. Never throws. */
export function decodeTourView(raw: unknown): TourView | null {
  const payload = recordOf(raw);
  if (payload === null) return null;
  const stored = payload["stored"];
  const version = payload["version"];
  const tour = resultTourOf(payload["tour"]);
  const error = textOf(payload["error"]);
  if (typeof stored !== "boolean") return null;
  if (typeof version !== "number" || !Number.isInteger(version) || version < 0) return null;
  if (tour === null || error === null) return null;
  return { stored, version, tour, error };
}

/** The job's tour route, with the token the cockpit already carries. */
export function tourViewPath(request: { jobId: string; token: string; baseUrl?: string }): string {
  const base = request.baseUrl ?? "";
  return `${base}/api/jobs/${encodeURIComponent(request.jobId)}/tour`
    + `?token=${encodeURIComponent(request.token)}`;
}

/** The one line the overlay shows for a view that could not be read. */
export const TOUR_UNREADABLE_LINE = "This job's tour could not be read.";

/** The one line the overlay shows for a tour with no stops. */
export const TOUR_EMPTY_LINE = "This job's tour has no stops.";

/** One state of the tour overlay: loading while the read is in flight, the fixed unreadable
 *  line for a `null` view, the fixed empty line for a tour with no stops, or every stop in
 *  the tour's own order. PURE, so the overlay's four readings are goldened here rather than
 *  through a render. */
export type TourPanelState =
  | { kind: "loading" }
  | { kind: "unreadable"; line: string }
  | { kind: "empty"; line: string }
  | { kind: "stops"; stops: TourStop[] };

/** The tour overlay's one state function. */
export function tourPanelState(view: TourView | null, loaded: boolean): TourPanelState {
  if (!loaded) return { kind: "loading" };
  if (view === null) return { kind: "unreadable", line: TOUR_UNREADABLE_LINE };
  if (view.tour.stops.length === 0) return { kind: "empty", line: TOUR_EMPTY_LINE };
  return { kind: "stops", stops: view.tour.stops };
}

/** Where previous and next lead from `current`; `null` at either end. */
export function tourNeighbours(count: number, current: number): {
  previous: number | null; next: number | null;
} {
  return {
    previous: current > 0 ? current - 1 : null,
    next: current + 1 < count ? current + 1 : null,
  };
}

/** The step label the overlay shows above its stop, one-based. */
export function tourStepLabel(count: number, current: number): string {
  return `Stop ${current + 1} of ${count}`;
}

/** Every stop's progress against `current`: "done" before it, "current" at it, "ahead" after
 *  it — one entry per stop, in stop order. */
export function tourProgress(count: number, current: number): Array<"done" | "current" | "ahead"> {
  return Array.from({ length: count }, (_unused, index) =>
    index < current ? "done" : index === current ? "current" : "ahead");
}

/** The plain label the overlay shows for one anchor, by kind. */
export function tourAnchorLabel(anchor: TourAnchor): string {
  switch (anchor.kind) {
    case "node": return `Task ${anchor.ref}`;
    case "diff": return `Changed file ${anchor.ref}`;
    case "evidence": return `Evidence file ${anchor.ref}`;
    case "command": return `Command ${anchor.ref}`;
    case "preview": return "The app preview";
    default: return anchor.ref;
  }
}

/** The generator name of `TOUR_GENERATOR_SUMMARY_ROLE` in `result_tour.py`, restated here so
 *  this module imports nothing. */
const TOUR_GENERATOR_SUMMARY_ROLE = "summary-role";

/** The line the overlay shows for how the tour was built: the summary model's own claim,
 *  checked against the job's records, or the mechanical fallback built straight from them. */
export function tourGeneratorLabel(generator: string): string {
  return generator === TOUR_GENERATOR_SUMMARY_ROLE
    ? "Written by the summary model and checked against the job's records"
    : "Built from the job's records";
}

/** Whether "Show me" has a place to take the operator: a task, a diff or the preview (DECISION
 *  F041 D6), the anchor kinds the cockpit can navigate to directly. An evidence or a command
 *  anchor names something the cockpit has no place to open, so the card shows it as text
 *  instead. */
export function tourCanShow(anchor: TourAnchor): boolean {
  return anchor.kind === "node" || anchor.kind === "diff" || anchor.kind === "preview";
}

/** The `rowKey` of the FIRST diff summary whose `path` equals `path`, or `null` when none
 *  does. Takes a plain array of `{path, rowKey}` rather than importing `DiffFileSummary` from
 *  `diffViewModel.ts`, so this module keeps importing nothing. */
export function tourDiffRowKey(
  summaries: Array<{ path: string; rowKey: string }>,
  path: string,
): string | null {
  const found = summaries.find((summary) => summary.path === path);
  return found ? found.rowKey : null;
}
