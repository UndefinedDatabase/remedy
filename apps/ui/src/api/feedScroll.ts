// The rule that decides whether the live feed follows new rows or holds still.
// Remedy deliberately keeps this a PURE function over numbers rather than a
// component effect: this repository has no DOM environment, so a rule written
// as scroll side effects could not be tested at all, and the one behaviour that
// matters -- never yanking a reader who has scrolled up -- would ship unverified.

/** Px of slack that still counts as sitting at the newest edge. Sub-pixel
 *  layout rounding leaves a pinned viewport a fraction off zero, so an exact
 *  comparison would unpin a reader who never moved. */
export const NEWEST_EDGE_TOLERANCE_PX = 8;

/** What the feed carries besides its rows: how many rows arrived while the
 *  reader was away from the newest edge and has therefore not seen. */
export interface FeedScrollState {
  readonly unseenRows: number;
}

/** The state a feed starts in and returns to whenever the reader is pinned. */
export const FEED_SCROLL_START: FeedScrollState = { unseenRows: 0 };

/** True when the viewport still sits at the newest edge, within tolerance. */
export function isPinnedToNewest(distanceFromNewest: number): boolean {
  return distanceFromNewest <= NEWEST_EDGE_TOLERANCE_PX;
}

/** True when the feed may scroll itself to the newest row. A reader who has
 *  scrolled away is NEVER moved: that is the whole point of this module. */
export function shouldFollowNewest(distanceFromNewest: number): boolean {
  return isPinnedToNewest(distanceFromNewest);
}

/** The state after `arrived` rows reach a viewport `distanceFromNewest` px from
 *  the newest edge. A pinned reader sees them at once, so nothing is unseen; a
 *  reader who scrolled up accumulates them until returning to the edge. */
export function nextFeedScroll(
  prev: FeedScrollState,
  arrived: number,
  distanceFromNewest: number,
): FeedScrollState {
  if (isPinnedToNewest(distanceFromNewest)) {
    return FEED_SCROLL_START;
  }
  return { unseenRows: prev.unseenRows + arrived };
}

/** The "new rows" pill appears only once rows have arrived unseen. Returning to
 *  the newest edge clears it, through nextFeedScroll. */
export function shouldShowNewRowsPill(state: FeedScrollState): boolean {
  return state.unseenRows > 0;
}
