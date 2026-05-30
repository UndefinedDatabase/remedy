/**
 * Brain Renderer — PixiJS v8 + pixi-viewport canvas for the semantic brain graph.
 *
 * Grey gradient background, white nodes with subtle depth/glow,
 * smooth wheel zoom, drag/pan, click selection, high-DPI.
 */

import { Application, Graphics, Text, TextStyle, Container } from "pixi.js";
import { Viewport } from "pixi-viewport";
import type { ViewModel, ViewModelNode, ViewModelEdge } from "../main";

interface RendererCallbacks {
  onNodeClick: (nodeId: string) => void;
  onZoomChange: (level: number) => void;
}

export interface RendererHandle {
  resize: () => void;
  destroy: () => void;
  setZoomLevel: (level: number) => void;
}

// Visual constants
const NODE_RADIUS = 14;
const NODE_COLOR = 0xffffff;
const NODE_BORDER = 0xd0d8e0;
const NODE_GLOW_COLOR = 0xc8d8ea;
const SELECTED_BORDER = 0x4a9eff;
const EDGE_COLOR = 0xc8cdd4;
const EDGE_ALPHA = 0.35;
const BG_COLOR = 0xe8ecf1;

const LABEL_STYLE = new TextStyle({
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  fontSize: 11,
  fill: 0x4a5568,
  align: "center",
});

function zoomLevelFromScale(scale: number): number {
  if (scale < 0.4) return 5;
  if (scale < 0.6) return 4;
  if (scale < 0.85) return 3;
  if (scale < 1.2) return 2;
  if (scale < 2.0) return 1;
  return 0;
}

export async function createRenderer(
  container: HTMLElement,
  viewModel: ViewModel,
  callbacks: RendererCallbacks,
): Promise<RendererHandle> {
  const width = container.clientWidth || 800;
  const height = container.clientHeight || 600;

  // PixiJS v8: Application.init is async
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

  // Viewport for pan/zoom
  const viewport = new Viewport({
    screenWidth: width,
    screenHeight: height,
    worldWidth: 2000,
    worldHeight: 2000,
    events: app.renderer.events,
  });

  viewport
    .drag()
    .pinch()
    .wheel({ smooth: 5 })
    .decelerate({ friction: 0.92 })
    .clampZoom({ minScale: 0.15, maxScale: 4.0 });

  viewport.moveCenter(0, 0);
  app.stage.addChild(viewport);

  // Layers
  const edgeLayer = new Container();
  const nodeLayer = new Container();
  const labelLayer = new Container();
  viewport.addChild(edgeLayer);
  viewport.addChild(nodeLayer);
  viewport.addChild(labelLayer);

  // Build node map
  const nodeMap = new Map<string, ViewModelNode>();
  for (const n of viewModel.nodes) {
    nodeMap.set(n.id, n);
  }

  // Draw edges
  const edgeGraphics: { g: Graphics; edge: ViewModelEdge }[] = [];
  for (const edge of viewModel.edges) {
    const src = nodeMap.get(edge.source);
    const tgt = nodeMap.get(edge.target);
    if (!src || !tgt) continue;
    const g = new Graphics();
    g.setStrokeStyle({ width: 1.5, color: EDGE_COLOR, alpha: EDGE_ALPHA });
    g.moveTo(src.position.x, src.position.y);
    g.lineTo(tgt.position.x, tgt.position.y);
    g.stroke();
    edgeLayer.addChild(g);
    edgeGraphics.push({ g, edge });
  }

  // Draw nodes
  let selectedNodeId: string | null = null;

  interface NodeEntry {
    container: Container;
    glow: Graphics;
    circle: Graphics;
    node: ViewModelNode;
  }
  const nodeEntries: NodeEntry[] = [];

  for (const node of viewModel.nodes) {
    const nc = new Container();
    nc.position.set(node.position.x, node.position.y);

    // Glow (subtle shadow)
    const glow = new Graphics();
    glow.circle(0, 0, NODE_RADIUS + 6);
    glow.fill({ color: NODE_GLOW_COLOR, alpha: 0.25 });
    nc.addChild(glow);

    // Main circle
    const circle = new Graphics();
    circle.circle(0, 0, NODE_RADIUS);
    circle.fill(NODE_COLOR);
    circle.setStrokeStyle({ width: 2, color: NODE_BORDER });
    circle.stroke();
    nc.addChild(circle);

    // Make interactive
    circle.eventMode = "static";
    circle.cursor = "pointer";
    circle.hitArea = {
      contains: (x: number, y: number) =>
        x * x + y * y < (NODE_RADIUS + 4) * (NODE_RADIUS + 4),
    };
    circle.on("pointerdown", () => {
      selectedNodeId = node.id;
      callbacks.onNodeClick(node.id);
      updateVisibility(currentZoomLevel);
    });

    nodeLayer.addChild(nc);
    nodeEntries.push({ container: nc, glow, circle, node });

    // Label
    const label = new Text({
      text: node.label.length > 20 ? node.label.slice(0, 18) + "..." : node.label,
      style: LABEL_STYLE,
    });
    label.anchor.set(0.5, 0);
    label.position.set(node.position.x, node.position.y + NODE_RADIUS + 4);
    label.label = `label-${node.id}`;
    labelLayer.addChild(label);
  }

  let currentZoomLevel = 0;

  function updateVisibility(level: number) {
    for (const entry of nodeEntries) {
      const visible = entry.node.visible_from_zoom <= level;
      entry.container.visible = visible;

      // Redraw circle with selection highlight
      entry.circle.clear();
      entry.circle.circle(0, 0, NODE_RADIUS);
      entry.circle.fill(NODE_COLOR);
      const borderColor = entry.node.id === selectedNodeId ? SELECTED_BORDER : NODE_BORDER;
      const borderWidth = entry.node.id === selectedNodeId ? 3 : 2;
      entry.circle.setStrokeStyle({ width: borderWidth, color: borderColor });
      entry.circle.stroke();

      entry.glow.alpha = entry.node.id === selectedNodeId ? 0.5 : 0.25;
    }

    // Labels
    for (const child of labelLayer.children) {
      const nodeId = child.label?.replace("label-", "");
      if (!nodeId) continue;
      const node = nodeMap.get(nodeId);
      if (!node) continue;
      child.visible =
        node.visible_from_zoom <= level && node.show_label_from_zoom <= level;
    }

    // Edges
    for (const { g, edge } of edgeGraphics) {
      g.visible = edge.visible_from_zoom <= level;
    }
  }

  // Initial state: only origin visible
  updateVisibility(0);

  // Zoom tracking
  viewport.on("zoomed", () => {
    const scale = viewport.scale.x;
    const newLevel = zoomLevelFromScale(scale);
    if (newLevel !== currentZoomLevel) {
      currentZoomLevel = newLevel;
      updateVisibility(newLevel);
      callbacks.onZoomChange(newLevel);
    }
  });

  function resize() {
    const w = container.clientWidth;
    const h = container.clientHeight;
    app.renderer.resize(w, h);
    viewport.resize(w, h);
  }

  return {
    resize,
    destroy: () => app.destroy(),
    setZoomLevel: (level: number) => {
      currentZoomLevel = level;
      updateVisibility(level);
      callbacks.onZoomChange(level);
    },
  };
}
