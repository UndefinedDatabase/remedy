/**
 * Brain Renderer — PixiJS v8 + pixi-viewport + ELK directional layout.
 *
 * Grey background, white nodes, subtle edges with arrowheads,
 * screen-space HTML labels (don't scale with zoom),
 * semantic zoom visibility, smooth wheel zoom.
 */

import { Application, Graphics, Container } from "pixi.js";
import { Viewport } from "pixi-viewport";
import type { ViewModel, ViewModelNode, ViewModelEdge } from "../main";

interface RendererCallbacks {
  onNodeClick: (nodeId: string) => void;
  onZoomChange: (level: number) => void;
  onEdgeHover: (edge: ViewModelEdge | null) => void;
}

export interface RendererHandle {
  resize: () => void;
  destroy: () => void;
  setZoomLevel: (level: number) => void;
  mergeViewModel: (vm: ViewModel) => void;
}

// Visual constants
const NODE_RADIUS = 14;
const NODE_COLOR = 0xffffff;
const NODE_BORDER = 0xd0d8e0;
const NODE_GLOW_COLOR = 0xc8d8ea;
const SELECTED_BORDER = 0x4a9eff;
const ATTENTION_BORDER = 0xe8a060;
const PRIMARY_EDGE_COLOR = 0xd8dce2;
const PRIMARY_EDGE_ALPHA = 0.6;
const SECONDARY_EDGE_COLOR = 0xc8cdd4;
const SECONDARY_EDGE_ALPHA = 0.25;
const BLOCKER_EDGE_COLOR = 0xe8a0a0;
const BG_COLOR = 0xe8ecf1;
const ARROW_SIZE = 6;

function zoomLevelFromScale(scale: number): number {
  if (scale < 0.2) return 6;
  if (scale < 0.35) return 5;
  if (scale < 0.5) return 4;
  if (scale < 0.7) return 3;
  if (scale < 1.0) return 2;
  if (scale < 1.8) return 1;
  return 0;
}

export async function createRenderer(
  container: HTMLElement,
  viewModel: ViewModel,
  callbacks: RendererCallbacks,
): Promise<RendererHandle> {
  const width = container.clientWidth || 800;
  const height = container.clientHeight || 600;

  const app = new Application();
  await app.init({
    width,
    height,
    backgroundColor: BG_COLOR,
    antialias: true,
    resolution: window.devicePixelRatio || 1,
    autoDensity: true,
  });

  container.appendChild(app.canvas as HTMLCanvasElement);

  const viewport = new Viewport({
    screenWidth: width,
    screenHeight: height,
    worldWidth: 3000,
    worldHeight: 2000,
    events: app.renderer.events,
  });

  viewport
    .drag()
    .pinch()
    .wheel({ smooth: 5 })
    .decelerate({ friction: 0.92 })
    .clampZoom({ minScale: 0.1, maxScale: 5.0 });

  // Center on origin node
  const originNode = viewModel.nodes.find(n => n.is_origin);
  if (originNode) {
    viewport.moveCenter(originNode.x, originNode.y);
  } else {
    viewport.moveCenter(0, 0);
  }

  app.stage.addChild(viewport);

  const edgeLayer = new Container();
  const nodeLayer = new Container();
  viewport.addChild(edgeLayer);
  viewport.addChild(nodeLayer);

  // HTML label overlay (screen-space, fixed font size)
  const labelOverlay = document.createElement("div");
  labelOverlay.id = "label-overlay";
  labelOverlay.style.cssText = "position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;overflow:hidden;z-index:10;";
  container.style.position = "relative";
  container.appendChild(labelOverlay);

  const nodeMap = new Map<string, ViewModelNode>();
  for (const n of viewModel.nodes) nodeMap.set(n.id, n);

  // ---------------------------------------------------------------------------
  // Draw edges with directional arrowheads
  // ---------------------------------------------------------------------------
  interface EdgeEntry { g: Graphics; edge: ViewModelEdge }
  const edgeEntries: EdgeEntry[] = [];

  function drawEdge(edge: ViewModelEdge): EdgeEntry | null {
    const src = nodeMap.get(edge.source);
    const tgt = nodeMap.get(edge.target);
    if (!src || !tgt) return null;

    const g = new Graphics();
    const isPrimary = edge.is_primary_chain;
    const isBlocker = edge.kind === "blocked_by";
    const color = isBlocker ? BLOCKER_EDGE_COLOR : isPrimary ? PRIMARY_EDGE_COLOR : SECONDARY_EDGE_COLOR;
    const alpha = isPrimary ? PRIMARY_EDGE_ALPHA : SECONDARY_EDGE_ALPHA;
    const lineWidth = isPrimary ? 2.0 : 1.2;

    // Line
    g.setStrokeStyle({ width: lineWidth, color, alpha });
    g.moveTo(src.x, src.y);
    g.lineTo(tgt.x, tgt.y);
    g.stroke();

    // Arrowhead
    const dx = tgt.x - src.x;
    const dy = tgt.y - src.y;
    const len = Math.sqrt(dx * dx + dy * dy);
    if (len > NODE_RADIUS * 2) {
      const nx = dx / len;
      const ny = dy / len;
      const ax = tgt.x - nx * (NODE_RADIUS + 4);
      const ay = tgt.y - ny * (NODE_RADIUS + 4);
      const px = -ny * ARROW_SIZE;
      const py = nx * ARROW_SIZE;
      g.setStrokeStyle({ width: 0 });
      g.beginFill(color, alpha);
      g.moveTo(ax, ay);
      g.lineTo(ax - nx * ARROW_SIZE * 1.5 + px, ay - ny * ARROW_SIZE * 1.5 + py);
      g.lineTo(ax - nx * ARROW_SIZE * 1.5 - px, ay - ny * ARROW_SIZE * 1.5 - py);
      g.closePath();
      g.endFill();
    }

    // Edge hover for tooltip
    g.eventMode = "static";
    g.hitArea = {
      contains: (hx: number, hy: number) => {
        // Simple distance-to-line check
        const ax2 = src.x, ay2 = src.y, bx = tgt.x, by = tgt.y;
        const t = Math.max(0, Math.min(1, ((hx - ax2) * (bx - ax2) + (hy - ay2) * (by - ay2)) / (len * len)));
        const px2 = ax2 + t * (bx - ax2);
        const py2 = ay2 + t * (by - ay2);
        return (hx - px2) ** 2 + (hy - py2) ** 2 < 100;
      },
    };
    g.on("pointerover", () => callbacks.onEdgeHover(edge));
    g.on("pointerout", () => callbacks.onEdgeHover(null));

    edgeLayer.addChild(g);
    return { g, edge };
  }

  for (const edge of viewModel.edges) {
    const entry = drawEdge(edge);
    if (entry) edgeEntries.push(entry);
  }

  // ---------------------------------------------------------------------------
  // Draw nodes
  // ---------------------------------------------------------------------------
  let selectedNodeId: string | null = null;

  interface NodeEntry {
    container: Container;
    glow: Graphics;
    circle: Graphics;
    node: ViewModelNode;
    labelEl: HTMLDivElement | null;
  }
  const nodeEntries: NodeEntry[] = [];

  for (const node of viewModel.nodes) {
    const nc = new Container();
    nc.position.set(node.x, node.y);

    const glow = new Graphics();
    glow.circle(0, 0, NODE_RADIUS + 6);
    glow.fill({ color: NODE_GLOW_COLOR, alpha: 0.2 });
    nc.addChild(glow);

    const circle = new Graphics();
    const borderColor = node.is_attention ? ATTENTION_BORDER : NODE_BORDER;
    circle.circle(0, 0, NODE_RADIUS);
    circle.fill(NODE_COLOR);
    circle.setStrokeStyle({ width: 2, color: borderColor });
    circle.stroke();
    nc.addChild(circle);

    circle.eventMode = "static";
    circle.cursor = "pointer";
    circle.hitArea = {
      contains: (x: number, y: number) => x * x + y * y < (NODE_RADIUS + 4) ** 2,
    };
    circle.on("pointerdown", () => {
      selectedNodeId = node.id;
      callbacks.onNodeClick(node.id);
      updateVisibility(currentZoomLevel);
    });

    nodeLayer.addChild(nc);

    // HTML label (screen-space)
    const labelEl = document.createElement("div");
    labelEl.className = "screen-label";
    labelEl.textContent = node.label_short;
    labelEl.style.cssText = "position:absolute;font-size:11px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#4a5568;white-space:nowrap;transform:translate(-50%,4px);pointer-events:none;display:none;";
    labelOverlay.appendChild(labelEl);

    nodeEntries.push({ container: nc, glow, circle, node, labelEl });
  }

  let currentZoomLevel = 0;
  let fullGraphMode = false;

  function updateVisibility(level: number) {
    const effectiveLevel = fullGraphMode ? 6 : level;

    for (const entry of nodeEntries) {
      const visible = entry.node.visible_from_zoom <= effectiveLevel;
      entry.container.visible = visible;

      // Selection highlight
      entry.circle.clear();
      entry.circle.circle(0, 0, NODE_RADIUS);
      entry.circle.fill(NODE_COLOR);
      const isSelected = entry.node.id === selectedNodeId;
      const borderColor = isSelected ? SELECTED_BORDER : entry.node.is_attention ? ATTENTION_BORDER : NODE_BORDER;
      entry.circle.setStrokeStyle({ width: isSelected ? 3 : 2, color: borderColor });
      entry.circle.stroke();
      entry.glow.alpha = isSelected ? 0.4 : 0.2;

      // Label visibility (show only for selected, or at appropriate zoom)
      const showLabel = visible && (
        isSelected ||
        entry.node.show_label_from_zoom <= effectiveLevel
      );
      if (entry.labelEl) entry.labelEl.style.display = showLabel ? "block" : "none";
    }

    for (const { g, edge } of edgeEntries) {
      g.visible = edge.visible_from_zoom <= effectiveLevel;
    }

    updateLabelPositions();
  }

  function updateLabelPositions() {
    const transform = viewport.worldTransform;
    for (const entry of nodeEntries) {
      if (!entry.labelEl || entry.labelEl.style.display === "none") continue;
      // World → screen coordinate
      const sx = transform.a * entry.node.x + transform.c * entry.node.y + transform.tx;
      const sy = transform.b * entry.node.x + transform.d * entry.node.y + transform.ty;
      entry.labelEl.style.left = `${sx}px`;
      entry.labelEl.style.top = `${sy + NODE_RADIUS + 2}px`;
    }
  }

  // Initial state: only origin
  updateVisibility(0);

  // Update labels on viewport move/zoom
  viewport.on("moved", updateLabelPositions);
  viewport.on("zoomed", () => {
    const scale = viewport.scale.x;
    const newLevel = zoomLevelFromScale(scale);
    if (newLevel !== currentZoomLevel) {
      currentZoomLevel = newLevel;
      if (!fullGraphMode) {
        updateVisibility(newLevel);
        callbacks.onZoomChange(newLevel);
      }
    }
    updateLabelPositions();
  });

  // Ticker for smooth label updates
  app.ticker.add(updateLabelPositions);

  function resize() {
    const w = container.clientWidth;
    const h = container.clientHeight;
    app.renderer.resize(w, h);
    viewport.resize(w, h);
    updateLabelPositions();
  }

  function mergeViewModel(newVm: ViewModel) {
    // Update node positions and add new nodes
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    for (const newNode of newVm.nodes) {
      nodeMap.set(newNode.id, newNode);
      const existing = nodeEntries.find(e => e.node.id === newNode.id);
      if (existing) {
        // Update position
        if (reducedMotion) {
          existing.container.position.set(newNode.x, newNode.y);
        } else {
          // Simple lerp toward new position
          existing.container.position.set(
            existing.container.position.x + (newNode.x - existing.container.position.x) * 0.3,
            existing.container.position.y + (newNode.y - existing.container.position.y) * 0.3,
          );
        }
        Object.assign(existing.node, newNode);
      }
      // New nodes would need full creation — skip for now, require reload
    }
    updateVisibility(currentZoomLevel);
  }

  return {
    resize,
    destroy: () => {
      labelOverlay.remove();
      app.destroy();
    },
    setZoomLevel: (level: number) => {
      currentZoomLevel = level;
      updateVisibility(level);
      callbacks.onZoomChange(level);
    },
    mergeViewModel,
  };
}
