// F043 T001 — the explanation catalog's own tests (DECISION F043 D1): the shape of every entry,
// the anchor each entry keeps to the file that defines what it explains, the whole key set, and
// the spot goldens T5_F043.md's Acceptance names.
import { describe, expect, it } from "vitest";
import { TERM_BODY_MAX_CHARS, TERM_CATALOG, TERM_KEY_PATTERN, termEntry } from "./terminology";

// `node:fs` and `node:url` are reached through a dynamic import whose specifier is a variable,
// as `costMetric.test.ts` does, because the app's tsconfig carries no Node types.
const FS_MODULE = "node:fs";
const URL_MODULE = "node:url";
type FsModule = { readFileSync: (path: string, encoding: string) => string };
type UrlModule = { fileURLToPath: (url: URL) => string };

/** A file's text, by its path from the repository root, which is four levels above this file. */
async function repoFile(relative: string): Promise<string> {
  const fs = (await import(FS_MODULE)) as FsModule;
  const url = (await import(URL_MODULE)) as UrlModule;
  return fs.readFileSync(url.fileURLToPath(new URL(`../../../../${relative}`, import.meta.url)), "utf8");
}

/** Runs of white space read as one space, so an anchor matches across a wrapped line. */
function flatten(text: string): string {
  return text.replace(/\s+/g, " ");
}

describe("the explanation catalog's entries", () => {
  it("holds exactly the terms the shipped surfaces render", () => {
    expect(Object.keys(TERM_CATALOG).sort()).toEqual([
      "agent.live",
      "blocked.task",
      "graph.scrubbed",
      "metric.done",
      "metric.open",
      "metric.planned",
      "metric.progress",
      "metric.proof",
      "metric.tests",
      "panel.activity",
      "panel.agent_now",
      "panel.decisions",
      "panel.tasks",
      "phase.build",
      "phase.finalized",
      "phase.job",
      "phase.planning",
      "phase.review",
      "phase.test",
      "status.delayed",
      "status.idle",
      "status.live",
      "status.reconnecting",
      "status.replay",
      "task.done",
      "task.in_progress",
      "task.partially_applied",
      "task.planned",
    ]);
  });

  it("keys every entry by dotted lowercase words", () => {
    for (const key of Object.keys(TERM_CATALOG)) {
      expect(key, key).toMatch(TERM_KEY_PATTERN);
    }
    expect("status").not.toMatch(TERM_KEY_PATTERN);
    expect("Status.live").not.toMatch(TERM_KEY_PATTERN);
    expect("status..live").not.toMatch(TERM_KEY_PATTERN);
  });

  it("gives every entry a title, a bounded body, a source path and an anchor", () => {
    for (const [key, entry] of Object.entries(TERM_CATALOG)) {
      expect(entry.title.trim(), key).not.toBe("");
      expect(entry.body.trim(), key).not.toBe("");
      expect(entry.body.length, key).toBeLessThanOrEqual(TERM_BODY_MAX_CHARS);
      expect(entry.anchor.trim(), key).not.toBe("");
      expect(entry.source, key).toMatch(/^[a-z][A-Za-z0-9_./-]*$/);
      expect(entry.source.split("/"), key).not.toContain("..");
    }
    expect(TERM_BODY_MAX_CHARS).toBe(240);
  });

  it("anchors every entry to a phrase its source file still states", async () => {
    const lost: string[] = [];
    for (const [key, entry] of Object.entries(TERM_CATALOG)) {
      const text = flatten(await repoFile(entry.source));
      if (!text.includes(flatten(entry.anchor))) lost.push(`${key}: ${entry.source}`);
    }
    expect(lost).toEqual([]);
  });

  it("reads an anchor across a wrapped line and refuses one the file does not state", async () => {
    const text = flatten(await repoFile("docs/roadmap/features/T5_F008.md"));
    expect(text.includes(flatten("labels itself visibly\n(\"delayed\") instead"))).toBe(true);
    expect(text.includes(flatten("labels itself quietly (\"delayed\")"))).toBe(false);
  });
});

describe("the spot goldens", () => {
  it("explains the delayed transport as T5_F008 defines it", () => {
    expect(termEntry("status.delayed")).toEqual({
      title: "Delayed",
      body: "The live connection is not available, so the cockpit asks for new events at intervals instead. What you see can lag behind the job.",
      source: "docs/roadmap/features/T5_F008.md",
      anchor: "labels itself visibly (\"delayed\") instead of pretending to be live",
    });
  });

  it("explains the replay pill as T5_F024 defines it", () => {
    expect(termEntry("status.replay")).toEqual({
      title: "Replay",
      body: "You are looking at an earlier moment of this job, chosen on the timeline. Press LIVE on the timeline to return to the present.",
      source: "docs/roadmap/features/T5_F024.md",
      anchor: "the pill says REPLAY",
    });
  });

  it("explains the finalized phase as T5_F024 defines it", () => {
    expect(termEntry("phase.finalized")).toEqual({
      title: "Finalized",
      body: "Reached when every task has passed, and held only while that stays true.",
      source: "docs/roadmap/features/T5_F024.md",
      anchor: "holds only while every task has passed",
    });
  });
  it("explains the decision inbox's order by the urgency formula decisionOrder.ts defines", () => {
    expect(termEntry("panel.decisions")).toEqual({
      title: "Decision inbox",
      body: "Questions Remedy cannot answer for itself, waiting for you. Open ones come first, the most urgent at the top: a question grows more urgent the longer it waits and the more tasks it holds up.",
      source: "apps/ui/src/api/decisionOrder.ts",
      anchor: "`(blockedCount + 1) * ageSeconds`, and the inbox reads open cards first",
    });
  });
});

describe("the whole catalog", () => {
  it("words every entry exactly as DECISIONS F043 D1 and D2 wrote it", () => {
    expect(TERM_CATALOG).toEqual({
      "status.live": {
        title: "Live",
        body: "This job is running, and the cockpit receives its events the moment they happen.",
        source: "docs/roadmap/features/T5_F008.md",
        anchor: "(live | reconnecting | delayed)",
      },
      "status.idle": {
        title: "Idle",
        body: "No part of this job is running right now. The cockpit shows the job as it last stood.",
        source: "apps/ui/src/cockpitLogic.ts",
        anchor: "return dashboard.live.running === true;",
      },
      "status.reconnecting": {
        title: "Reconnecting",
        body: "The live connection dropped and the cockpit is opening it again. Events that arrive meanwhile are not lost: they are replayed once it is back.",
        source: "docs/roadmap/features/T5_F008.md",
        anchor: "resume replays exactly the missed span",
      },
      "status.delayed": {
        title: "Delayed",
        body: "The live connection is not available, so the cockpit asks for new events at intervals instead. What you see can lag behind the job.",
        source: "docs/roadmap/features/T5_F008.md",
        anchor: 'labels itself visibly ("delayed") instead of pretending to be live',
      },
      "status.replay": {
        title: "Replay",
        body: "You are looking at an earlier moment of this job, chosen on the timeline. Press LIVE on the timeline to return to the present.",
        source: "docs/roadmap/features/T5_F024.md",
        anchor: "the pill says REPLAY",
      },
      "phase.job": {
        title: "Job",
        body: "The job phase begins with the job's first event.",
        source: "docs/roadmap/features/T5_F024.md",
        anchor: "Job begins at the ledger's first row",
      },
      "phase.planning": {
        title: "Planning",
        body: "The planning phase begins when planning starts.",
        source: "docs/roadmap/features/T5_F024.md",
        anchor: "sends the three `planning_*` kinds to Planning",
      },
      "phase.build": {
        title: "Build",
        body: "The build phase begins when the first task run starts.",
        source: "docs/roadmap/features/T5_F024.md",
        anchor: "`task_run_started` and the two `builder_*` kinds to Build",
      },
      "phase.test": {
        title: "Test",
        body: "The test phase begins when the first test or verification runs.",
        source: "docs/roadmap/features/T5_F024.md",
        anchor: "the `test_run_*` and `verification_*` kinds to Test",
      },
      "phase.review": {
        title: "Review",
        body: "The review phase begins when the first review verdict arrives.",
        source: "docs/roadmap/features/T5_F024.md",
        anchor: "a `task_round_completed` carrying a reviewer's verdict to Review",
      },
      "phase.finalized": {
        title: "Finalized",
        body: "Reached when every task has passed, and held only while that stays true.",
        source: "docs/roadmap/features/T5_F024.md",
        anchor: "holds only while every task has passed",
      },
      "metric.open": {
        title: "Open",
        body: "Questions this job is waiting for you to answer. You find them in the decision inbox.",
        source: "packages/orchestration/ui_server.py",
        anchor: "Number of still-open human decisions for a job",
      },
      "metric.planned": {
        title: "Planned",
        body: "Tasks of this job that have not started yet.",
        source: "packages/orchestration/ui_server.py",
        anchor: "\"planned\": sum(1 for t in job.tasks if",
      },
      "metric.done": {
        title: "Done",
        body: "Tasks of this job that have finished.",
        source: "packages/orchestration/ui_server.py",
        anchor: "\"done\": sum(1 for t in job.tasks if",
      },
      "metric.progress": {
        title: "Progress",
        body: "The share of this job's tasks that have finished. A job without tasks shows 0%.",
        source: "packages/orchestration/ui_server.py",
        anchor: "\"progress_percent\": round((sum(1 for t in job.tasks",
      },
      "metric.tests": {
        title: "Tests",
        body: "How many of this job's recorded test runs passed. The dot shows whether the latest run passed or failed.",
        source: "packages/orchestration/ui_server.py",
        anchor: "Safe test counters from the event ledger. Counts only, no output.",
      },
      "metric.proof": {
        title: "Proof",
        body: "How many of this job's changes carry a verified proof, out of all its changes. A dash means the proof could not be read.",
        source: "packages/orchestration/ui_server.py",
        anchor: "Counts only (total changes vs verified).",
      },
      "task.done": {
        title: "Done",
        body: "This task has finished.",
        source: "apps/ui/src/api/remedyApi.ts",
        anchor: "if (text.includes(\"done\") || text.includes(\"pass\") || text.includes(\"complete\") || text.includes(\"applied\")) return \"done\";",
      },
      "task.in_progress": {
        title: "In progress",
        body: "This task is running now.",
        source: "apps/ui/src/api/remedyApi.ts",
        anchor: "text.includes(\"running\") || text.includes(\"progress\")) return \"current\";",
      },
      "blocked.task": {
        title: "Blocked",
        body: "This task stopped: it failed, or something blocked it.",
        source: "apps/ui/src/api/remedyApi.ts",
        anchor: "if (text.includes(\"block\") || text.includes(\"fail\")) return \"blocked\";",
      },
      "task.planned": {
        title: "Planned",
        body: "This task is not running: it has not started yet, or it was paused or cancelled.",
        source: "apps/ui/src/api/remedyApi.ts",
        anchor: "if (text.includes(\"suggest\")) return \"suggested\"; return \"pending\";",
      },
      "task.partially_applied": {
        title: "Partially applied",
        body: "Only some of this task's changes landed in the project; the rest did not apply.",
        source: "packages/orchestration/proof_chain.py",
        anchor: "The apply fold agrees or it says \"partial\"",
      },
      "panel.tasks": {
        title: "Tasks",
        body: "The steps of this job's plan. The planner decides how many there are, up to a configured limit.",
        source: "docs/system/vocabulary.md",
        anchor: "One step in a job plan; the planner chooses how many",
      },
      "panel.decisions": {
        title: "Decision inbox",
        body: "Questions Remedy cannot answer for itself, waiting for you. Open ones come first, the most urgent at the top: a question grows more urgent the longer it waits and the more tasks it holds up.",
        source: "apps/ui/src/api/decisionOrder.ts",
        anchor: "`(blockedCount + 1) * ageSeconds`, and the inbox reads open cards first",
      },
      "panel.activity": {
        title: "Activity",
        body: "What this job has been doing, in plain words. Choose a row to find its task in the graph.",
        source: "docs/roadmap/features/T5_F021.md",
        anchor: "feed rows carry their seq and click-jump to their node in the graph",
      },
      "panel.agent_now": {
        title: "Agent is doing now",
        body: "The newest real action of this job's agents. Reading files and other bookkeeping are left out.",
        source: "apps/ui/src/components/panels/AgentNowCard.tsx",
        anchor: "Bookkeeping is excluded on purpose",
      },
      "agent.live": {
        title: "Live",
        body: "Shown while the job is running and its agents did something in the last half minute.",
        source: "apps/ui/src/components/panels/AgentNowCard.tsx",
        anchor: "RUNNING AND RECENT, never either alone.",
      },
      "graph.scrubbed": {
        title: "Scrubbed",
        body: "The graph shows this job as it stood at the moment chosen on the timeline. New events keep arriving and wait until you return to LIVE.",
        source: "docs/roadmap/features/T5_F024.md",
        anchor: "scrubbed mode is unmistakably labeled with live updates queuing behind the toggle",
      },
    });
  });
});

describe("termEntry", () => {
  it("answers the entry a key names", () => {
    expect(termEntry("status.live")?.title).toBe("Live");
  });

  it("answers null for a key the catalog lacks, an inherited name included", () => {
    expect(termEntry("status.unknown")).toBeNull();
    expect(termEntry("toString")).toBeNull();
    expect(termEntry("constructor")).toBeNull();
    expect(termEntry("")).toBeNull();
  });
});
