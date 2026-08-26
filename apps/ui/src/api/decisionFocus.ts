// Resolving one decision card to the graph node the card's deep link jumps to.
// T003's jump lives here rather than in the component so the node environment's
// vitest can reach it, which is the pattern DECISION F031 D5 fixed for this
// feature and DECISION F021 D4 fixed for the activity feed.
import type { DecisionCardModel } from "./decisionCard";
import type { FocusableTask } from "./feedFocus";

/** The graph node a decision card jumps to, or null when it cannot jump.
 *
 *  This is the SIBLING of `nodeIdForFeedRow` in `./feedFocus.ts`, not a second
 *  design: Remedy deliberately resolves through the task list the dashboard
 *  already carries, keyed by the decision's own `taskId`, rather than matching a
 *  decision against the graph. DECISION F021 D2 rejected inventing a second
 *  client-side mapping for exactly this, and a decision id is not a node id —
 *  nothing on the wire relates them. `FocusableTask` is IMPORTED from that
 *  module for the same reason: one spelling per concept, so a duplicated type
 *  cannot drift into the second mapping D2 refused.
 *
 *  A null is NOT a failure. A decision naming no task, or naming one this
 *  dashboard does not carry, is a card that must not OFFER the jump — never one
 *  that jumps somewhere arbitrary.
 *
 *  Remedy deliberately keeps no clock, no fetch and no component in this
 *  module: it is a pure rule over two values, which is what lets a test pin it
 *  under DECISION F031 D5. */
export function nodeIdForDecisionCard(
  decision: Pick<DecisionCardModel, "taskId">,
  tasks: readonly FocusableTask[],
): string | null {
  if (!decision.taskId) {
    return null;
  }
  const owner = tasks.find(task => task.id === decision.taskId);
  return owner ? owner.nodeId : null;
}
