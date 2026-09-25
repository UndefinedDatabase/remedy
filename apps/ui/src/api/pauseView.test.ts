import { describe, expect, it } from "vitest";
import { normalizeApiFailure } from "./remedyApi";
import type { RemedyDashboard } from "./types";
import {
  PAUSE_OWNER_SOURCES,
  jobPauseAction,
  nowCardPause,
  pauseActionLabel,
  pauseBanner,
  taskPauseAction,
} from "./pauseView";

function baseDashboard(overrides: Partial<RemedyDashboard> = {}): RemedyDashboard {
  const failure = normalizeApiFailure("job-1", []);
  return { ...failure, ...overrides };
}

function parked(source: string): RemedyDashboard {
  return baseDashboard({ pause: { record: { source }, requested: false, pausedTaskIds: [], error: "" } });
}

describe("PAUSE_OWNER_SOURCES", () => {
  it("names exactly cli and ui", () => {
    expect(PAUSE_OWNER_SOURCES).toEqual(["cli", "ui"]);
  });
});

describe("pauseBanner", () => {
  it("answers null when nothing is paused, pending or wrong", () => {
    expect(pauseBanner(baseDashboard())).toBeNull();
  });

  it("shows the read error first, hiding every other reading", () => {
    const dashboard = baseDashboard({
      pause: { record: { source: "cli" }, requested: true, pausedTaskIds: ["t1"], error: "control root missing" },
    });
    const banner = pauseBanner(dashboard);
    expect(banner?.badge).toBe("PAUSE");
    expect(banner?.text).toBe("The pause state could not be read: control root missing");
    expect(banner?.command).toBe("");
    expect(banner?.tone).toBe("warn");
  });

  it("shows parked, by you, over a pending request", () => {
    const dashboard = baseDashboard({
      pause: { record: { source: "ui" }, requested: true, pausedTaskIds: [], error: "" },
    });
    const banner = pauseBanner(dashboard);
    expect(banner?.badge).toBe("PAUSED");
    expect(banner?.text).toBe("Paused by you. Nothing runs until you resume it.");
    expect(banner?.command).toBe("remedy job run job-1");
  });

  it("shows parked, not by you, for a source outside the owner set", () => {
    const banner = pauseBanner(parked("system"));
    expect(banner?.text).toBe("Paused. Nothing runs until it is resumed.");
  });

  it("shows the pending job-scope request when nothing is parked", () => {
    const dashboard = baseDashboard({
      pause: { record: {}, requested: true, pausedTaskIds: [], error: "" },
    });
    const banner = pauseBanner(dashboard);
    expect(banner?.badge).toBe("PAUSING");
    expect(banner?.text).toBe("Pause requested. The job stops before its next step.");
    expect(banner?.command).toBe("");
  });

  it("gives the singular sentence for one paused task", () => {
    const dashboard = baseDashboard({
      pause: { record: {}, requested: false, pausedTaskIds: ["t1"], error: "" },
    });
    const banner = pauseBanner(dashboard);
    expect(banner?.text).toBe("1 task is paused by you. The rest of the job keeps going.");
  });

  it("gives the plural sentence for more than one paused task", () => {
    const dashboard = baseDashboard({
      pause: { record: {}, requested: false, pausedTaskIds: ["t1", "t2", "t3"], error: "" },
    });
    const banner = pauseBanner(dashboard);
    expect(banner?.text).toBe("3 tasks are paused by you. The rest of the job keeps going.");
  });

  it("command is empty except when parked", () => {
    const requested = baseDashboard({ pause: { record: {}, requested: true, pausedTaskIds: [], error: "" } });
    const pausedTasks = baseDashboard({ pause: { record: {}, requested: false, pausedTaskIds: ["t1"], error: "" } });
    expect(pauseBanner(requested)?.command).toBe("");
    expect(pauseBanner(pausedTasks)?.command).toBe("");
  });
});

describe("nowCardPause", () => {
  it("answers null when nothing is paused", () => {
    expect(nowCardPause(baseDashboard())).toBeNull();
  });

  it("says paused by you for a parked job whose source is an owner", () => {
    expect(nowCardPause(parked("cli"))).toEqual({ status: "Paused", detail: "Paused by you" });
  });

  it("says paused, not by you, for a parked job from another source", () => {
    expect(nowCardPause(parked("system"))).toEqual({ status: "Paused", detail: "Paused" });
  });

  it("says paused by you when not running with paused tasks, even unparked", () => {
    const dashboard = baseDashboard({
      live: { ...baseDashboard().live, running: false },
      pause: { record: {}, requested: false, pausedTaskIds: ["t1"], error: "" },
    });
    expect(nowCardPause(dashboard)).toEqual({ status: "Paused", detail: "Paused by you" });
  });

  it("answers null while running, even with paused tasks queued", () => {
    const dashboard = baseDashboard({
      live: { ...baseDashboard().live, running: true },
      pause: { record: {}, requested: false, pausedTaskIds: ["t1"], error: "" },
    });
    expect(nowCardPause(dashboard)).toBeNull();
  });
});

describe("jobPauseAction", () => {
  it("answers resume when parked", () => {
    expect(jobPauseAction(parked("cli"))).toBe("resume");
  });

  it("answers take_back when requested, even while running", () => {
    const dashboard = baseDashboard({
      live: { ...baseDashboard().live, running: true },
      pause: { record: {}, requested: true, pausedTaskIds: [], error: "" },
    });
    expect(jobPauseAction(dashboard)).toBe("take_back");
  });

  it("answers pause while running with nothing pending", () => {
    const dashboard = baseDashboard({ live: { ...baseDashboard().live, running: true } });
    expect(jobPauseAction(dashboard)).toBe("pause");
  });

  it("answers null when idle with nothing pending", () => {
    expect(jobPauseAction(baseDashboard())).toBeNull();
  });
});

describe("taskPauseAction", () => {
  const dashboard = baseDashboard({
    pause: { record: {}, requested: false, pausedTaskIds: ["t1"], error: "" },
  });

  it("answers resume for a paused task", () => {
    expect(taskPauseAction(dashboard, "t1", "current")).toBe("resume");
  });

  it("answers pause for a task that is not done and not paused", () => {
    expect(taskPauseAction(dashboard, "t2", "current")).toBe("pause");
  });

  it("answers null for a done task", () => {
    expect(taskPauseAction(dashboard, "t2", "done")).toBeNull();
  });
});

describe("pauseActionLabel", () => {
  it("labels every job-scope action", () => {
    expect(pauseActionLabel("job", "pause")).toBe("Pause job");
    expect(pauseActionLabel("job", "take_back")).toBe("Take back pause");
    expect(pauseActionLabel("job", "resume")).toBe("Resume");
  });

  it("labels every task-scope action", () => {
    expect(pauseActionLabel("task", "pause")).toBe("Pause task");
    expect(pauseActionLabel("task", "resume")).toBe("Resume task");
  });
});
