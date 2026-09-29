// F042 R5's render harness (evidence, not product), grown from R4's: mounts the REAL `RemedyApp` from
// `apps/ui/src` over a `window.fetch` stand-in that answers the project routes from a fixed
// fixture, delays a summary by `window.__summaryDelays[slug]` milliseconds when the driver asks,
// answers every job route with a 500, and records every request path on `window.__calls`. The
// `fixture` query parameter `single` leaves one project in the list, `none` leaves none, and
// `many` lists thirty projects named p01 to p30 for the grid's pages. Nothing here reads a real
// door. The page mounts into `#root`, as `apps/ui/index.html` does, so `globals.css` sizes it.
import { createRoot } from "react-dom/client";
import "../../apps/ui/src/styles/tokens.css";
import "../../apps/ui/src/styles/globals.css";
import RemedyApp from "../../apps/ui/src/RemedyApp";

type Json = Record<string, unknown>;
declare global {
  interface Window { __calls: string[]; __summaryDelays: Record<string, number>; }
}

const FIXTURE = new URLSearchParams(window.location.search).get("fixture") ?? "";
const SINGLE = FIXTURE === "single";

function entry(slug: string, reachable = true): Json {
  return {
    id: `id-${slug}`, slug, name: slug, repo_path: `/work/${slug}`, repo_reachable: reachable,
    fix_it: reachable ? null : `The folder /work/${slug} is not there any more.`,
  };
}

const MANY: Json[] = Array.from({ length: 30 }, (_, i) => entry(`p${String(i + 1).padStart(2, "0")}`));
const PROJECTS: Json[] = SINGLE ? [entry("alpha")] : FIXTURE === "none" ? [] : FIXTURE === "many" ? MANY
  : [entry("alpha"), entry("beta", false), entry("gamma"), entry("delta")];
const LAST_JOB: Record<string, string> = { delta: "d1" };

function summary(slug: string): Json {
  const jobId = LAST_JOB[slug];
  return {
    version: 1, project_id: `id-${slug}`, slug, jobs: { active: jobId ? 1 : 0, total: jobId ? 1 : 0 },
    last_result: jobId ? { job_id: jobId, title: `${slug} job`, state: "running", headline: "The run is running." } : null,
    cost_today: slug === "alpha" ? { day: "2026-09-29", value_usd: 0.25, basis: "actual", calls: 1 }
      : { day: "2026-09-29", value_usd: null, basis: "absent", calls: 0 },
    decisions: jobId ? { open_count: 2, peak_urgency: 100 } : { open_count: 0, peak_urgency: 0 }, degraded: false,
  };
}

function reply(status: number, body: unknown): Response {
  return new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
}

window.__calls = [];
window.__summaryDelays = {};
window.fetch = async (input: RequestInfo | URL): Promise<Response> => {
  const url = new URL(typeof input === "string" ? input : input instanceof URL ? input.href : input.url, window.location.href);
  window.__calls.push(`${url.pathname}${url.search}`);
  const parts = url.pathname.split("/");
  if (url.pathname === "/api/projects") {
    return reply(200, { version: 1, projects: PROJECTS, default_project: null, single_project: SINGLE, unscoped_jobs: 0, orphaned_jobs: 0 });
  }
  if (parts.length === 5 && parts[2] === "projects" && parts[4] === "summary") {
    const slug = decodeURIComponent(parts[3]);
    const delay = window.__summaryDelays[slug] ?? 0;
    if (delay > 0) await new Promise((resolve) => setTimeout(resolve, delay));
    return reply(200, summary(slug));
  }
  return reply(500, { error: "harness answers no job route" });
};

createRoot(document.getElementById("root")!).render(<RemedyApp />);
