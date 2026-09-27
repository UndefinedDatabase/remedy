import { describe, expect, it } from "vitest";
import { rerunAnswerView } from "./rerunView";

describe("rerunAnswerView", () => {
  it("is null for a null body", () => {
    expect(rerunAnswerView(null)).toBeNull();
  });

  it("is null for any outcome other than needs_confirmation or prepared", () => {
    expect(rerunAnswerView({ outcome: "refused" })).toBeNull();
    expect(rerunAnswerView({ outcome: "something_else" })).toBeNull();
    expect(rerunAnswerView({})).toBeNull();
  });

  it("prices a needs_confirmation estimate with one task after the root", () => {
    const view = rerunAnswerView({
      outcome: "needs_confirmation",
      subtree: ["aaaaaaaa", "bbbbbbbb"],
      estimate: { band_usd_low: 1.5, band_usd_high: 3.25, basis: "plan" },
      confirm_above_usd: 2,
    });
    expect(view).toEqual({
      kind: "needs_confirmation",
      sentence: "Rerunning task aaaaaaaa and 1 task after it is estimated at $1.50 to $3.25, "
        + "above the $2.00 you asked to confirm.",
      runCommand: "",
    });
  });

  it("prices a needs_confirmation estimate with three tasks after the root", () => {
    const view = rerunAnswerView({
      outcome: "needs_confirmation",
      subtree: ["aaaaaaaa", "bbbbbbbb", "cccccccc", "dddddddd"],
      estimate: { band_usd_low: 4, band_usd_high: 10, basis: "plan" },
      confirm_above_usd: 5,
    });
    expect(view?.sentence).toBe(
      "Rerunning task aaaaaaaa and 3 tasks after it is estimated at $4.00 to $10.00, "
      + "above the $5.00 you asked to confirm.");
  });

  it("reads an unavailable estimate as cannot-be-estimated, singular", () => {
    const view = rerunAnswerView({
      outcome: "needs_confirmation",
      subtree: ["aaaaaaaa", "bbbbbbbb"],
      estimate: { band_usd_low: null, band_usd_high: null, basis: "unknown" },
      confirm_above_usd: 2,
    });
    expect(view?.sentence).toBe(
      "The cost of rerunning task aaaaaaaa and 1 task after it cannot be estimated in advance.");
  });

  it("reads an unavailable estimate as cannot-be-estimated, plural", () => {
    const view = rerunAnswerView({
      outcome: "needs_confirmation",
      subtree: ["aaaaaaaa", "bbbbbbbb", "cccccccc"],
      estimate: { band_usd_low: null, band_usd_high: null, basis: "unknown" },
      confirm_above_usd: 2,
    });
    expect(view?.sentence).toBe(
      "The cost of rerunning task aaaaaaaa and 2 tasks after it cannot be estimated in advance.");
  });

  it("names the prepared sentence and its run command", () => {
    const view = rerunAnswerView({
      outcome: "prepared",
      root_task_id: "aaaaaaaa",
      subtree: ["aaaaaaaa", "bbbbbbbb", "cccccccc"],
      run_command: "remedy job run 0123456789abcdef",
    });
    expect(view).toEqual({
      kind: "prepared",
      sentence: "Task aaaaaaaa and 2 tasks after it were reset to run again.",
      runCommand: "remedy job run 0123456789abcdef",
    });
  });

  it("reads a prepared answer with one task after the root, singular", () => {
    const view = rerunAnswerView({
      outcome: "prepared",
      root_task_id: "aaaaaaaa",
      subtree: ["aaaaaaaa", "bbbbbbbb"],
      run_command: "remedy job run 0123456789abcdef",
    });
    expect(view?.sentence).toBe("Task aaaaaaaa and 1 task after it were reset to run again.");
  });

  it("never throws on a body with every field missing", () => {
    expect(() => rerunAnswerView({ outcome: "needs_confirmation" })).not.toThrow();
    expect(() => rerunAnswerView({ outcome: "prepared" })).not.toThrow();
    const view = rerunAnswerView({ outcome: "prepared" });
    expect(view?.kind).toBe("prepared");
    expect(view?.runCommand).toBe("");
  });
});
