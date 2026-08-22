// Resolving one activity-feed row to the graph node it belongs to. T003's
// click-jump lives here rather than in the component so the node environment's
// vitest can reach it, which is the pattern DECISION F021 D4 fixed for this
// feature.
import type { FeedRow } from "./feedRow";

/** The only two fields of a dashboard task this resolution reads. Narrowed on
 *  purpose: the rule is about ids, and a resolver taking the whole
 *  `RemedyTaskItem` would churn every time an unrelated task field moved. */
export interface FocusableTask {
  id: string;
  nodeId: string;
}

/** The graph node a feed row jumps to, or null when it cannot jump.
 *
 *  Remedy deliberately resolves this through the task list the dashboard
 *  already carries, rather than by matching a row against the graph on seq or
 *  timestamp: DECISION F021 D2 rejected inventing a second client-side mapping
 *  for exactly this, and two events sharing a timestamp would make that one
 *  wrong. `related_node_id` is what `remedyApi.ts` reads a task's `nodeId`
 *  from, so this lands on a node the graph really has.
 *
 *  A null is not a failure. Heartbeats and job-level events carry no task
 *  linkage at all, and a row that cannot jump must render as a row that does
 *  not OFFER the jump — never as one that jumps somewhere arbitrary. */
export function nodeIdForFeedRow(
  row: Pick<FeedRow, "taskId">,
  tasks: readonly FocusableTask[],
): string | null {
  if (!row.taskId) {
    return null;
  }
  const owner = tasks.find(task => task.id === row.taskId);
  return owner ? owner.nodeId : null;
}
