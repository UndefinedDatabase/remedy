// Owns cluster expansion at the zoom's focus: the focused task's '+N' chip is
// replaced by the runs it stood for, so L1 fans out every run of that task and
// a run the chip hid can be seen and focused (graph_spec.md §10; T5_F023.md:
// "clusters expand per rule; collapse on unfocus"). PURE and a VIEW over the
// clustered model, as `clusterBrainModel` itself is: the reducer's model is
// never touched (DECISION F023 D6).
import type { BrainLink, BrainModel, BrainNode } from "./brainOntology";

/** `clustered` with the cluster of `taskId` replaced by that task's runs from
 *  `model`, in the chip's place and in seq order, each with its own parent
 *  link. A task with no cluster, or no task at all, returns `clustered` itself
 *  (===), so an unfocused layout is the ordinary one. */
export function expandClusterOf(clustered: BrainModel, model: BrainModel, taskId: string): BrainModel {
  const chipIndex = clustered.nodes.findIndex((n) => n.kind === "cluster" && n.parentId === taskId);
  if (chipIndex < 0) return clustered;
  const chipId = clustered.nodes[chipIndex].id;
  const shown = new Set(clustered.nodes.map((n) => n.id));
  const hidden: BrainNode[] = model.nodes
    .filter((n) => n.parentId === taskId && n.kind !== "cluster" && !shown.has(n.id))
    .sort((a, b) => a.seq - b.seq || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  const hiddenIds = new Set(hidden.map((n) => n.id));
  const nodes = [...clustered.nodes.slice(0, chipIndex), ...hidden, ...clustered.nodes.slice(chipIndex + 1)];
  const links: BrainLink[] = [
    ...clustered.links.filter((l) => l.target !== chipId),
    ...model.links.filter((l) => hiddenIds.has(l.target)),
  ];
  return { ...clustered, nodes, links };
}
