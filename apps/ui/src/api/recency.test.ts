import { describe, it, expect } from "vitest";
import {
  FRESH_WINDOW_MS,
  QUIET_WINDOW_MS,
  isLiveByRecency,
  recencyLevel,
} from "./recency";

const T0 = 1_700_000_000_000;

describe("recencyLevel", () => {
  it("reports none before anything has acted", () => {
    expect(recencyLevel(null, T0)).toBe("none");
  });

  it("reports fresh at the moment of the action", () => {
    expect(recencyLevel(T0, T0)).toBe("fresh");
  });

  it("stays fresh just inside the fresh window", () => {
    expect(recencyLevel(T0, T0 + FRESH_WINDOW_MS - 1)).toBe("fresh");
  });

  it("starts fading exactly at the fresh boundary", () => {
    expect(recencyLevel(T0, T0 + FRESH_WINDOW_MS)).toBe("fading");
  });

  it("still fades just inside the quiet window", () => {
    expect(recencyLevel(T0, T0 + QUIET_WINDOW_MS - 1)).toBe("fading");
  });

  it("goes idle exactly at the quiet boundary", () => {
    expect(recencyLevel(T0, T0 + QUIET_WINDOW_MS)).toBe("idle");
  });

  it("stays idle long after the quiet window", () => {
    expect(recencyLevel(T0, T0 + QUIET_WINDOW_MS * 100)).toBe("idle");
  });

  it("reports fresh rather than idle when the clocks disagree", () => {
    expect(recencyLevel(T0 + 60_000, T0)).toBe("fresh");
  });
});

describe("isLiveByRecency", () => {
  it("counts fresh and fading as live", () => {
    expect(isLiveByRecency("fresh")).toBe(true);
    expect(isLiveByRecency("fading")).toBe(true);
  });

  it("counts idle as not live", () => {
    expect(isLiveByRecency("idle")).toBe(false);
  });

  it("counts the pre-stream state as not live", () => {
    expect(isLiveByRecency("none")).toBe(false);
  });
});
