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
});

describe("the whole catalog", () => {
  it("words every entry exactly as DECISION F043 D1's first round wrote it", () => {
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
        anchor: "labels itself visibly (\"delayed\") instead of pretending to be live",
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
