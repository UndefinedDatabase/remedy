// T5_F042 T002 and T003, DECISIONS F042 D3 and D4 — the cockpit's own address: what the page's
// query string names, which face it opens (the fourth, `home`, a token with neither a job nor a
// project), the key a new project or a new job remounts the shell under, and the address the way
// home writes.
//
// PURE: no `fetch`, no `Date`, no storage, no `window`, no `document`, in code or in any
// string.
import { JOB_SCOPED_PARAMS } from "./projectScope";

export interface CockpitAddress {
  jobId: string;
  project: string;
  token: string;
}

/** The four faces `RemedyApp.tsx` can open. */
export type CockpitFace = "missing" | "empty_project" | "job" | "home";

export const MISSING_ADDRESS_LINE = "Missing job or token in the URL.";
export const EMPTY_PROJECT_LINE = "This project has no jobs yet.";

/** The page's own address: the job (`job`, then the older `job_id`), the trimmed project, and
 *  the token — each "" when absent. */
export function addressFromSearch(search: string): CockpitAddress {
  const params = new URLSearchParams(search);
  const jobId = params.get("job") || params.get("job_id") || "";
  const project = (params.get("project") ?? "").trim();
  const token = params.get("token") || "";
  return { jobId, project, token };
}

/** Which face this address opens: `missing` without a token, else `job` with a job, else
 *  `empty_project` with a project, else `home` — a token with neither a job nor a project. */
export function cockpitFaceOf(address: CockpitAddress): CockpitFace {
  if (!address.token) return "missing";
  if (address.jobId) return "job";
  if (address.project) return "empty_project";
  return "home";
}

/** The key a new project or a new job remounts the shell under — the PAIR, not their
 *  concatenation, so a project carrying a `|` can never collide with a job id split across the
 *  boundary a plain join would draw. Changes with the project and the job only. */
export function shellKeyOf(address: CockpitAddress): string {
  return JSON.stringify([address.project, address.jobId]);
}

/** The address the way home writes: `search` with `project` and every `JOB_SCOPED_PARAMS` name
 *  dropped — each names the project or a node, task or job of the project being LEFT — and the
 *  rest kept in place. "" for an address left with nothing, else "?" plus the rest. */
export function homeSearch(search: string): string {
  const params = new URLSearchParams(search);
  params.delete("project");
  for (const name of JOB_SCOPED_PARAMS) params.delete(name);
  const rest = params.toString();
  return rest === "" ? "" : `?${rest}`;
}
