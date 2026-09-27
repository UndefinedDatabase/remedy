// Births a `synapse` node per prompt-trace item onto the live model —
// `synapse` is the tool/prompt call kind graph_spec.md §2 already names, and
// §3's hierarchy places it as a child of its task. DECISION F288 D5: the
// parent is the task, not the run, exactly as D3 made every run a child of
// its task — every consumer of the layout (the filter, the clustering, the
// selection, the zoom) reads a non-task node's parent as its task, and D5
// (3) keeps that one rule rather than adding a third depth for the run a
// prompt happens to belong to; the run is named instead in the synapse's own
// `meta.attemptId`. PURE and TOTAL, and a VIEW composed onto the model from
// OUTSIDE the reducer: the prompt trace is dashboard state, not a stream
// frame, so `brainReducer.ts` itself never births a synapse
// (brainOntology.ts's own header names this module as the reason).
import type { RemedyPromptTraceItem } from "../../api/types";
import type { BrainLink, BrainModel, BrainNode } from "./brainOntology";

/** The layout id of the synapse a prompt-trace item births. */
export function promptNodeId(itemId: string): string {
  return `prompt:${itemId}`;
}

/** `model` with one `synapse` node and one link appended per `items` entry,
 *  IN ITEM ORDER, whose task node `task:<item.taskId>` the model holds and
 *  whose own synapse it does not yet hold: the born node carries that task
 *  node's own state, `parentId` the task, `seq` 0, and `meta` holding the
 *  item's `promptId`, `role`, `promptKind`, `round` and its run id as
 *  `attemptId`; the born link runs from the task to the synapse, built the
 *  way the reducer builds its own links. An item whose task the model lacks,
 *  or whose synapse already exists (including one born earlier in this same
 *  call, for a repeated item), is skipped. A call that appends nothing
 *  returns `model` itself (===). */
export function withPromptNodes(
  model: BrainModel,
  items: readonly RemedyPromptTraceItem[],
): BrainModel {
  const knownIds = new Set(model.nodes.map((n) => n.id));
  const taskStateById = new Map(model.nodes.map((n) => [n.id, n.state]));
  const bornNodes: BrainNode[] = [];
  const bornLinks: BrainLink[] = [];

  for (const item of items) {
    const taskId = `task:${item.taskId}`;
    const taskState = taskStateById.get(taskId);
    if (taskState === undefined) continue;
    const id = promptNodeId(item.id);
    if (knownIds.has(id)) continue;
    knownIds.add(id);
    bornNodes.push({
      id,
      kind: "synapse",
      state: taskState,
      parentId: taskId,
      seq: 0,
      meta: {
        promptId: item.id,
        role: item.role,
        promptKind: item.promptKind,
        round: item.round,
        attemptId: item.runId,
      },
    });
    bornLinks.push({ id: `${taskId}->${id}`, source: taskId, target: id });
  }

  if (bornNodes.length === 0) return model;
  return {
    ...model,
    nodes: [...model.nodes, ...bornNodes],
    links: [...model.links, ...bornLinks],
  };
}
