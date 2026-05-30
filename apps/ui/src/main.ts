/**
 * Remedy Brain Canvas — PixiJS + pixi-viewport + ELK directional layout.
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

export async function fetchJSON<T>(endpoint: string): Promise<T> {
  const sep = endpoint.includes("?") ? "&" : "?";
  const res = await fetch(`${API_BASE}/${endpoint}${sep}token=${token}`);
  if (!res.ok) throw new Error(`API ${res.status}: ${endpoint}`);
  return res.json() as Promise<T>;
}

export function getToken(): string { return token; }
export function getJobId(): string { return jobId; }

// ---------------------------------------------------------------------------
// View model types (v2 — ELK directional)
// ---------------------------------------------------------------------------

export interface ViewModelNode {
  id: string;
  type: string;
  kind: string;
  label_short: string;
  label_full: string;
  layer: number;
  rank: number;
  zone: string;
  importance: number;
  status: string | null;
  risk: string | null;
  x: number;
  y: number;
  width: number;
  height: number;
  cluster_id: string;
  visible_from_zoom: number;
  show_label_from_zoom: number;
  is_origin: boolean;
  is_primary_chain: boolean;
  is_attention: boolean;
}

export interface ViewModelEdge {
  source: string;
  target: string;
  kind: string;
  label: string;
  meaning: string;
  visible_from_zoom: number;
  is_primary_chain: boolean;
  strength: number;
  direction: string;
}

export interface ZoomLevel {
  level: number;
  name: string;
  max_nodes: number;
  visible_count: number;
}

export interface ViewModel {
  version: number;
  job_id: string;
  layout_engine: string;
  direction: string;
  origin: string;
  total_nodes: number;
  total_edges: number;
  default_zoom_level: number;
  max_initial_nodes: number;
  advanced_full_graph_available: boolean;
  full_graph_requires_explicit_toggle: boolean;
  layers: { level: number; name: string; node_count: number }[];
  zoom_levels: ZoomLevel[];
  nodes: ViewModelNode[];
  edges: ViewModelEdge[];
  clusters: { id: string; node_ids: string[]; count: number }[];
}

async function main() {
  const container = document.getElementById("canvas-container")!;
  const detailEl = document.getElementById("detail-card")!;
  const zoomIndicator = document.getElementById("zoom-indicator")!;

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
      const zl = viewModel.zoom_levels[level];
      zoomIndicator.textContent = zl ? zl.name : "Full Graph";
    },
    onEdgeHover: (edge: ViewModelEdge | null) => {
      const tooltip = document.getElementById("edge-tooltip")!;
      if (edge) {
        tooltip.textContent = edge.meaning;
        tooltip.classList.add("visible");
      } else {
        tooltip.classList.remove("visible");
      }
    },
  });

  window.addEventListener("resize", () => renderer.resize());

  // Live polling (Step 95)
  startLivePolling(viewModel, renderer);
}

async function startLivePolling(_viewModel: ViewModel, renderer: { mergeViewModel: (vm: ViewModel) => void }) {
  let lastHash = "";
  const poll = async () => {
    try {
      const state = await fetchJSON<{ view_model_hash?: string }>("live-state");
      if (state.view_model_hash && state.view_model_hash !== lastHash) {
        lastHash = state.view_model_hash || "";
        const newVm = await fetchJSON<ViewModel>("brain-view-model");
        renderer.mergeViewModel(newVm);
      }
    } catch {
      // Silently ignore — server may not have live-state yet
    }
  };

  // Check reduced motion preference
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const interval = reducedMotion ? 5000 : 2000;
  setInterval(poll, interval);
}

main();
