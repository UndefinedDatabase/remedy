declare module "react-force-graph-2d" {
  import type { Component, RefObject } from "react";

  interface GraphData {
    nodes: object[];
    links: object[];
  }

  interface ForceGraph2DProps {
    graphData?: GraphData;
    width?: number;
    height?: number;
    backgroundColor?: string;
    nodeId?: string;
    nodeRelSize?: number;
    nodeVal?: string | number | ((node: object) => number);
    nodeColor?: string | ((node: object) => string);
    nodeCanvasObject?: (node: object, ctx: CanvasRenderingContext2D, globalScale: number) => void;
    nodeCanvasObjectMode?: string | ((node: object) => string);
    nodePointerAreaPaint?: (node: object, color: string, ctx: CanvasRenderingContext2D, globalScale: number) => void;
    linkSource?: string;
    linkTarget?: string;
    linkColor?: string | ((link: object) => string);
    linkWidth?: number | ((link: object) => number);
    linkCurvature?: number | string | ((link: object) => number);
    linkCanvasObject?: (link: object, ctx: CanvasRenderingContext2D, globalScale: number) => void;
    linkCanvasObjectMode?: string | ((link: object) => string);
    linkDirectionalParticles?: number | ((link: object) => number);
    linkDirectionalParticleWidth?: number | ((link: object) => number);
    d3AlphaDecay?: number;
    d3VelocityDecay?: number;
    d3AlphaMin?: number;
    cooldownTicks?: number;
    cooldownTime?: number;
    warmupTicks?: number;
    onNodeClick?: (node: object, event: MouseEvent) => void;
    onNodeHover?: (node: object | null, prevNode: object | null) => void;
    onBackgroundClick?: (event: MouseEvent) => void;
    enableNodeDrag?: boolean;
    enableZoomInteraction?: boolean;
    enablePanInteraction?: boolean;
    minZoom?: number;
    maxZoom?: number;
    onEngineStop?: () => void;
    ref?: RefObject<ForceGraph2DInstance | null>;
  }

  interface ForceGraph2DInstance {
    d3Force: (forceName: string, force?: object) => object | undefined;
    d3ReheatSimulation: () => void;
    zoom: (scale?: number, duration?: number) => number;
    centerAt: (x?: number, y?: number, duration?: number) => { x: number; y: number };
    screen2GraphCoords: (x: number, y: number) => { x: number; y: number };
    graph2ScreenCoords: (x: number, y: number) => { x: number; y: number };
  }

  const ForceGraph2D: React.ForwardRefExoticComponent<ForceGraph2DProps & React.RefAttributes<ForceGraph2DInstance>>;
  export default ForceGraph2D;
  export type { ForceGraph2DProps, ForceGraph2DInstance, GraphData };
}
