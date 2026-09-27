import { describe, expect, it } from "vitest";
import { attemptChipText } from "./attemptView";

describe("attemptChipText", () => {
  it("answers `attempt <n>`", () => {
    expect(attemptChipText(2)).toBe("attempt 2");
    expect(attemptChipText(5)).toBe("attempt 5");
  });
});
