/**
 * Remedy Brain Canvas — PixiJS + pixi-viewport semantic zoom graph.
 *
 * Entry point. Reads job_id and token from URL params,
 * fetches brain-view-model, initializes renderer.
 */

import { createRenderer } from "./brain/renderer";
import { DetailCard } from "./brain/detail";

const params = new URLSearchParams(window.location.search);
const jobId = params.get("job") || document.body.dataset.jobId || "__JOB_ID__";
const token = params.get("token") || document.body.dataset.token || "__TOKEN__";

const API_BASE = `${window.location.origin}/api/jobs/${jobId}`;

async function fetchJSON<T>(endpoint: string): Promise<T> {
  const sep = endpoint.includes("?") ? "&" : "?";
  const res = await fetch(`${API_BASE}/${endpoint}${sep}token=${token}`);
  if (!res.ok) throw new Error(`API ${res.status}: ${endpoint}`);
  return res.json() as Promise<T>;
}

interface ViewModelNode {
  id: string;
  type: string;
  label: string;
  status: string | null;
  risk: string | null;
  layer: number;
  visible_from_zoom: number;
  show_label_from_zoom: number;
  importance: number;
  cluster_id: string;
  position: { x: number; y: number };
}

interface ViewModelEdge {
  source: string;
  target: string;
  type: string;
  visible_from_zoom: number;
}

interface LayerInfo {
  level: number;
  name: string;
  node_count: number;
}

interface ViewModel {
  version: number;
  job_id: string;
  total_nodes: number;
  total_edges: number;
  layers: LayerInfo[];
  nodes: ViewModelNode[];
  edges: ViewModelEdge[];
}

export type { ViewModel, ViewModelNode, ViewModelEdge, LayerInfo };

async function main() {
  const container = document.getElementById("canvas-container")!;
  const detailEl = document.getElementById("detail-card")!;
  const zoomIndicator = document.getElementById("zoom-indicator")!;

  // Fetch view model
  let viewModel: ViewModel;
  try {
    viewModel = await fetchJSON<ViewModel>("brain-view-model");
  } catch (e) {
    container.innerHTML = `<div style="padding:40px;font-family:sans-serif;color:#666">
      <p>Loading brain view model failed.</p>
      <p style="font-size:12px;color:#999">${e}</p>
    </div>`;
    return;
  }

  const detailCard = new DetailCard(detailEl, async (nodeId: string) => {
    return fetchJSON(`nodes/${nodeId}/detail`);
  });

  const renderer = await createRenderer(container, viewModel, {
    onNodeClick: (nodeId: string) => detailCard.show(nodeId),
    onZoomChange: (level: number) => {
      const layer = viewModel.layers[level];
      zoomIndicator.textContent = `Zoom: ${layer ? layer.name : "Full"}`;
    },
  });

  // Handle window resize
  window.addEventListener("resize", () => renderer.resize());
}

main();
