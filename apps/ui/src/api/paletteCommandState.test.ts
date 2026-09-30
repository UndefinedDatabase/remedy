// F044 T001 — whether the palette can offer a command now (DECISION F044 D3).
import { describe, expect, it } from "vitest";
import { normalizeApiFailure } from "./remedyApi";
import type { RemedyDashboard } from "./types";
import { PALETTE_COMMANDS, paletteCommandOf } from "./paletteCommands";
import type { PaletteCommand } from "./paletteCommands";
import {
  PALETTE_ALREADY_PAUSED_REASON,
  PALETTE_ENDED_REASON,
  PALETTE_FORM_REASON,
  PALETTE_NOT_PAUSED_REASON,
  PALETTE_NOT_RUNNING_REASON,
  PALETTE_NO_DECISION_REASON,
  PALETTE_NO_TOKEN_REASON,
  PALETTE_PAUSE_PENDING_REASON,
  paletteCommandFactsOf,
  paletteCommandReason,
  paletteCommandReasons,
} from "./paletteCommandState";
import type { PaletteCommandFacts } from "./paletteCommandState";

function entry(command: string): PaletteCommand {
  const found = paletteCommandOf(command);
  if (found === null) throw new Error(command);
  return found;
}

const RUNNING: PaletteCommandFacts = { hasToken: true, ended: false, pauseAction: "pause", openDecisions: 1 };

describe("the reasons", () => {
  it("are the plain sentences DECISION F044 D3 wrote", () => {
    expect([
      PALETTE_NO_TOKEN_REASON, PALETTE_ENDED_REASON, PALETTE_FORM_REASON, PALETTE_NOT_RUNNING_REASON,
      PALETTE_ALREADY_PAUSED_REASON, PALETTE_PAUSE_PENDING_REASON, PALETTE_NOT_PAUSED_REASON, PALETTE_NO_DECISION_REASON,
    ]).toEqual([
      "This page has no write token, so it cannot send commands.",
      "This job has ended, so it takes no more commands.",
      "The palette cannot ask for this command's arguments yet.",
      "The job is not running, so there is nothing to pause.",
      "The job is already paused.",
      "A pause is already on its way.",
      "The job is not paused.",
      "No decision is waiting for an answer.",
    ]);
  });
});

describe("paletteCommandReason", () => {
  it("refuses everything without a token first, a form entry next, then everything on an ended job", () => {
    expect(paletteCommandReason(entry("job.stop"), { ...RUNNING, hasToken: false })).toBe(PALETTE_NO_TOKEN_REASON);
    expect(paletteCommandReason(entry("job.plan-reorder"), { ...RUNNING, hasToken: false })).toBe(PALETTE_NO_TOKEN_REASON);
    expect(paletteCommandReason(entry("job.plan-reorder"), { ...RUNNING, ended: true })).toBe(PALETTE_FORM_REASON);
    expect(paletteCommandReason(entry("job.stop"), { ...RUNNING, ended: true })).toBe(PALETTE_ENDED_REASON);
    expect(paletteCommandReason(entry("job.pause"), { ...RUNNING, ended: true, pauseAction: "pause" })).toBe(PALETTE_ENDED_REASON);
  });

  it("offers a pause only while the job's own action is to pause", () => {
    const pause = entry("job.pause");
    expect(paletteCommandReason(pause, RUNNING)).toBe("");
    expect(paletteCommandReason(pause, { ...RUNNING, pauseAction: "resume" })).toBe(PALETTE_ALREADY_PAUSED_REASON);
    expect(paletteCommandReason(pause, { ...RUNNING, pauseAction: "take_back" })).toBe(PALETTE_PAUSE_PENDING_REASON);
    expect(paletteCommandReason(pause, { ...RUNNING, pauseAction: null })).toBe(PALETTE_NOT_RUNNING_REASON);
  });

  it("offers a resume while the job is parked or a pause is on its way", () => {
    const unpause = entry("job.unpause");
    expect(paletteCommandReason(unpause, { ...RUNNING, pauseAction: "resume" })).toBe("");
    expect(paletteCommandReason(unpause, { ...RUNNING, pauseAction: "take_back" })).toBe("");
    expect(paletteCommandReason(unpause, RUNNING)).toBe(PALETTE_NOT_PAUSED_REASON);
    expect(paletteCommandReason(unpause, { ...RUNNING, pauseAction: null })).toBe(PALETTE_NOT_PAUSED_REASON);
  });

  it("offers the decision's answer only while one is open", () => {
    expect(paletteCommandReason(entry("decision.resolve"), RUNNING)).toBe("");
    expect(paletteCommandReason(entry("decision.resolve"), { ...RUNNING, openDecisions: 0 })).toBe(PALETTE_NO_DECISION_REASON);
  });

  it("offers every other send and surface on a running job", () => {
    for (const command of ["job.stop", "chat.send", "job.steer", "job.veto-task", "job.rerun-subtree",
      "job.preview-start", "job.preview-stop", "job.edit-task", "job.inject"]) {
      expect(paletteCommandReason(entry(command), RUNNING), command).toBe("");
    }
  });
});

describe("paletteCommandReasons", () => {
  it("holds only the refused commands, by id", () => {
    const reasons = paletteCommandReasons(RUNNING);
    const forms = PALETTE_COMMANDS.filter((row) => row.flow === "form").map((row) => row.command);
    expect(Object.keys(reasons).sort()).toEqual([...forms, "job.unpause"].sort());
    expect(reasons["job.unpause"]).toBe(PALETTE_NOT_PAUSED_REASON);
  });
});

describe("paletteCommandFactsOf", () => {
  const base = normalizeApiFailure("job-1", []);

  function dashboard(over: Partial<RemedyDashboard>): RemedyDashboard {
    return { ...base, ...over };
  }

  it("reads the token, the job's stage, its pause action and its open decisions", () => {
    const running = dashboard({ live: { ...base.live, running: true, stage: "building" } });
    expect(paletteCommandFactsOf(running, "tok")).toEqual({
      hasToken: true, ended: false, pauseAction: "pause", openDecisions: 0,
    });
    const ended = dashboard({ live: { ...base.live, running: false, stage: "Completed" } });
    expect(paletteCommandFactsOf(ended, "")).toEqual({
      hasToken: false, ended: true, pauseAction: null, openDecisions: 0,
    });
  });
});
