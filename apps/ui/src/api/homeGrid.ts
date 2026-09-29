// T5_F042 T003, DECISION F042 D4 — the home grid's own rules: which projects a page shows, the
// tone and words a job's state draws, cost today in words with its basis, and one project's
// card composed from its list entry and its summary — none of it borrowed from a component.
//
// PURE: no `fetch`, no `Date`, no storage, no `window`, no `document`, in code or in any string.
import type { ProjectCostToday, ProjectEntry, ProjectSummary } from "./projectScope";

/** Cards to a page, DECISION F042 D4 (2). */
export const HOME_PAGE_SIZE = 12;

export const NO_PROJECTS_LINE = "No projects yet. Run remedy init in a project's folder to add it.";
export const SUMMARY_UNAVAILABLE_LINE = "This project's summary could not be read.";
export const NO_JOBS_LINE = "No jobs yet.";
export const DEGRADED_LINE = "Some job records could not be read.";
export const NO_FOLDER_HINT = "No folder attached";

export interface HomePage<T> {
  items: T[];
  page: number;
  pages: number;
}

/** *items* sliced to `HOME_PAGE_SIZE` a page, *page* clamped into range (at least 1, at most
 *  the page count) and the page count itself at least 1, even for an empty list. */
export function homePage<T>(items: readonly T[], page: number): HomePage<T> {
  const pages = Math.max(1, Math.ceil(items.length / HOME_PAGE_SIZE));
  const clamped = Math.min(Math.max(page, 1), pages);
  const start = (clamped - 1) * HOME_PAGE_SIZE;
  return { items: items.slice(start, start + HOME_PAGE_SIZE), page: clamped, pages };
}

/** The colour family a card's result line draws from. */
export type ResultTone = "done" | "current" | "blocked" | "open" | "none";

/** *state*, lowercased, sorted into its family: `completed`/`done` finish, `running` is
 *  current, `blocked`/`failed`/`cancelled` are blocked, "" has none, anything else is open. */
export function resultToneOf(state: string): ResultTone {
  const lowered = state.toLowerCase();
  if (lowered === "completed" || lowered === "done") return "done";
  if (lowered === "running") return "current";
  if (lowered === "blocked" || lowered === "failed" || lowered === "cancelled") return "blocked";
  if (lowered === "") return "none";
  return "open";
}

/** Today's cost, in words, never a bare zero: "not measured" for an absent basis or a null
 *  value, else the figure to two places, prefixed "at least " for a lower bound. */
export function costTodayLine(cost: ProjectCostToday): string {
  if (cost.basis === "absent" || cost.value_usd === null) return "Cost today: not measured";
  const prefix = cost.basis === "lower_bound" ? "at least " : "";
  return `Cost today: ${prefix}$${cost.value_usd.toFixed(2)}`;
}

export interface ProjectCard {
  slug: string;
  name: string;
  folderHint: string;
  reachable: boolean;
  fixIt: string | null;
  activeChip: string;
  resultLine: string;
  resultTone: ResultTone;
  costLine: string;
  decisionsChip: string;
  urgent: boolean;
  degraded: boolean;
}

/** One project's card, from its list *entry* and its *summary* — `null` while the summary is
 *  unreadable, drawn as its own absence (empty chips and lines, `SUMMARY_UNAVAILABLE_LINE`)
 *  rather than as zeros. The name falls back to the slug; the fix-it carries only for an
 *  unreachable folder. */
export function projectCardOf(entry: ProjectEntry, summary: ProjectSummary | null): ProjectCard {
  const base = {
    slug: entry.slug,
    name: entry.name || entry.slug,
    folderHint: entry.repo_path ?? NO_FOLDER_HINT,
    reachable: entry.repo_reachable,
    fixIt: entry.repo_reachable ? null : entry.fix_it,
  };
  if (summary === null) {
    return {
      ...base,
      activeChip: "",
      resultLine: SUMMARY_UNAVAILABLE_LINE,
      resultTone: "none",
      costLine: "",
      decisionsChip: "",
      urgent: false,
      degraded: false,
    };
  }
  const state = summary.last_result?.state ?? "";
  const openCount = summary.decisions.open_count;
  return {
    ...base,
    activeChip: `${summary.jobs.active} active`,
    resultLine: summary.last_result?.headline ?? NO_JOBS_LINE,
    resultTone: resultToneOf(state),
    costLine: costTodayLine(summary.cost_today),
    decisionsChip: `${openCount} open decision${openCount === 1 ? "" : "s"}`,
    urgent: openCount > 0 && summary.decisions.peak_urgency > 0,
    degraded: summary.degraded,
  };
}
