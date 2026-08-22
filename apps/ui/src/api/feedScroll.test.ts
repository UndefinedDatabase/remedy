import { describe, it, expect } from "vitest";
import {
  FEED_SCROLL_START,
  NEWEST_EDGE_TOLERANCE_PX,
  isPinnedToNewest,
  nextFeedScroll,
  shouldFollowNewest,
  shouldShowNewRowsPill,
} from "./feedScroll";

describe("isPinnedToNewest", () => {
  it("treats the exact edge as pinned", () => {
    expect(isPinnedToNewest(0)).toBe(true);
  });

  it("absorbs sub-pixel rounding up to the tolerance", () => {
    expect(isPinnedToNewest(NEWEST_EDGE_TOLERANCE_PX)).toBe(true);
  });

  it("treats a reader past the tolerance as scrolled away", () => {
    expect(isPinnedToNewest(NEWEST_EDGE_TOLERANCE_PX + 1)).toBe(false);
  });
});

describe("shouldFollowNewest", () => {
  it("follows for a pinned reader", () => {
    expect(shouldFollowNewest(0)).toBe(true);
  });

  it("never moves a reader who scrolled up", () => {
    expect(shouldFollowNewest(400)).toBe(false);
  });
});

describe("nextFeedScroll", () => {
  it("leaves a pinned reader with nothing unseen", () => {
    expect(nextFeedScroll(FEED_SCROLL_START, 3, 0)).toEqual({ unseenRows: 0 });
  });

  it("accumulates rows that arrive while the reader is away", () => {
    const after = nextFeedScroll(FEED_SCROLL_START, 2, 300);
    expect(nextFeedScroll(after, 3, 300)).toEqual({ unseenRows: 5 });
  });

  it("holds the count steady when a re-render brings no new row", () => {
    const away = nextFeedScroll(FEED_SCROLL_START, 4, 300);
    expect(nextFeedScroll(away, 0, 300)).toEqual({ unseenRows: 4 });
  });

  it("clears the count when the reader returns to the newest edge", () => {
    const away = nextFeedScroll(FEED_SCROLL_START, 7, 300);
    expect(nextFeedScroll(away, 0, 0)).toEqual({ unseenRows: 0 });
  });
});

describe("shouldShowNewRowsPill", () => {
  it("stays hidden until something arrives unseen", () => {
    expect(shouldShowNewRowsPill(FEED_SCROLL_START)).toBe(false);
  });

  it("appears once a row arrived while the reader was away", () => {
    expect(shouldShowNewRowsPill(nextFeedScroll(FEED_SCROLL_START, 1, 300))).toBe(true);
  });
});
