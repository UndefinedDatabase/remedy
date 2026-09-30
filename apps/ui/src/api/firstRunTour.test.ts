// F043 T003 — the first-run tour's content and its one stored fact (DECISION F043 D4).
import { describe, expect, it } from "vitest";
import {
  FIRST_RUN_STEPS,
  FIRST_RUN_TOUR_KEY,
  FIRST_RUN_TOUR_SEEN,
  firstRunStepLabel,
  firstRunTourDue,
  markFirstRunTourSeen,
} from "./firstRunTour";
import type { FirstRunTourStorage } from "./firstRunTour";

function memory(initial: Record<string, string> = {}): FirstRunTourStorage & { data: Record<string, string> } {
  const data = { ...initial };
  return {
    data,
    getItem: (key: string) => (Object.prototype.hasOwnProperty.call(data, key) ? data[key] : null),
    setItem: (key: string, value: string) => { data[key] = value; },
  };
}

const broken: FirstRunTourStorage = {
  getItem: () => { throw new Error("storage is off"); },
  setItem: () => { throw new Error("storage is off"); },
};

describe("the first-run tour's steps", () => {
  it("walks the graph, the timeline, the feed, the inbox, the note and the command bar, in that order", () => {
    expect(FIRST_RUN_STEPS.map((step) => step.target)).toEqual([
      "brain-graph-stage", "phase-timeline", "right-live-panel", "decision-inbox-card", "chat-input-row", "command-bar",
    ]);
  });

  it("words every step exactly as DECISION F043 D4 wrote it and DECISION F044 D2 moved its last", () => {
    expect(FIRST_RUN_STEPS).toEqual([
      {
        title: "The graph",
        body: "Every task of this job is a dot joined to the job at the centre. A dot changes colour as its task is planned, runs, and passes or fails. Choose one to see what it did.",
        target: "brain-graph-stage",
      },
      {
        title: "The timeline",
        body: "The job's phases, from its first event to the end. Drag along it to see the job as it stood earlier; LIVE brings you back.",
        target: "phase-timeline",
      },
      {
        title: "What is happening now",
        body: "The newest real action of the job's agents, and below it every event in plain words.",
        target: "right-live-panel",
      },
      {
        title: "Decisions",
        body: "Questions Remedy cannot answer for itself wait here for you, the most urgent first.",
        target: "decision-inbox-card",
      },
      {
        title: "A note for the job",
        body: "Write a note here and the builder reads it at its next round.",
        target: "chat-input-row",
      },
      {
        title: "Jump to anything",
        body: "Type here to jump to any task, switch project, or open the list of every term. Hover an underlined word to see what it means, and start this tour again from here.",
        target: "command-bar",
      },
    ]);
  });

  it("counts its steps for the card", () => {
    expect(firstRunStepLabel(FIRST_RUN_STEPS.length, 0)).toBe("Step 1 of 6");
    expect(firstRunStepLabel(6, 5)).toBe("Step 6 of 6");
  });
});

describe("whether the tour opens by itself", () => {
  it("opens for a browser with no record of it, and never again once it was seen", () => {
    const storage = memory();
    expect(firstRunTourDue(storage)).toBe(true);
    markFirstRunTourSeen(storage);
    expect(storage.data).toEqual({ [FIRST_RUN_TOUR_KEY]: FIRST_RUN_TOUR_SEEN });
    expect(firstRunTourDue(storage)).toBe(false);
  });

  it("stays closed for any stored value, since the key only ever records that it was seen", () => {
    expect(firstRunTourDue(memory({ [FIRST_RUN_TOUR_KEY]: "anything" }))).toBe(false);
  });

  it("stays closed without a storage or with one that throws, and writing to either throws nothing", () => {
    expect(firstRunTourDue(null)).toBe(false);
    expect(firstRunTourDue(broken)).toBe(false);
    expect(() => markFirstRunTourSeen(null)).not.toThrow();
    expect(() => markFirstRunTourSeen(broken)).not.toThrow();
  });

  it("keeps its record under one key and one value", () => {
    expect(FIRST_RUN_TOUR_KEY).toBe("remedy:first-run-tour");
    expect(FIRST_RUN_TOUR_SEEN).toBe("seen");
  });
});
