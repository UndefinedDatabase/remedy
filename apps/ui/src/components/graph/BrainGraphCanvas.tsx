import { useState } from "react";
import type { RemedyDashboard } from "../../api/types";
import { CodeOrbGlyph } from "../icons/RemedyGlyphs";
import styles from "./BrainGraphCanvas.module.css";

interface DisplayNode {
  id: string;
  label: string;
  state: string;
  kind: "root" | "task";
  x: number;
  y: number;
  size: number;
}

function buildDisplayModel(dashboard: RemedyDashboard): { nodes: DisplayNode[]; edges: [string, string][] } {
  const tasks = dashboard.tasks.slice(0, 80);
  const nodes: DisplayNode[] = [];
  const edges: [string, string][] = [];

  nodes.push({ id: "root", label: dashboard.title || "Job", state: "current", kind: "root", x: 0, y: 0, size: 28 });

  const branchCount = Math.min(5, Math.max(2, Math.ceil(tasks.length / 4)));
  const angles = [-2.55, -1.35, -0.15, 0.95, 2.15].slice(0, branchCount);

  tasks.forEach((t, i) => {
    const branch = i % branchCount;
    const depth = Math.floor(i / branchCount) + 1;
    const radius = 90 + depth * 54;
    const bend = Math.sin(depth * 0.9 + branch) * 22;
    const angle = angles[branch];
    const x = Math.cos(angle) * radius + Math.cos(angle + Math.PI / 2) * bend;
    const y = Math.sin(angle) * radius + Math.sin(angle + Math.PI / 2) * bend;

    const st = t.state;
    const state = st === "done" ? "done" : st === "current" ? "current" : st === "blocked" ? "blocked" : "planned";
    nodes.push({ id: t.id, label: t.label, state, kind: "task", x, y, size: 10 });
    edges.push(["root", t.id]);
  });

  return { nodes, edges };
}

export function BrainGraphCanvas({ dashboard, filter = "all", onSelectNode }: { dashboard: RemedyDashboard; filter?: string; onSelectNode: (nodeId: string | null) => void }) {
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const model = buildDisplayModel(dashboard);
  const filteredNodes = model.nodes.filter(n => {
    if (n.kind === "root") return true;
    if (filter === "all") return true;
    if (filter === "open") return n.state === "current" || n.state === "blocked";
    if (filter === "planned") return n.state === "planned";
    if (filter === "done") return n.state === "done";
    return true;
  });
  const visibleIds = new Set(filteredNodes.map(n => n.id));
  const nodes = filteredNodes;
  const edges = model.edges.filter(([s, t]) => visibleIds.has(s) && visibleIds.has(t));

  const pad = 40;
  const xs = nodes.map(n => n.x);
  const ys = nodes.map(n => n.y);
  const minX = Math.min(...xs) - pad;
  const maxX = Math.max(...xs) + pad;
  const minY = Math.min(...ys) - pad;
  const maxY = Math.max(...ys) + pad;
  const vw = maxX - minX || 400;
  const vh = maxY - minY || 400;

  const nodeMap = Object.fromEntries(nodes.map(n => [n.id, n]));
  const hovered = hoveredId ? nodeMap[hoveredId] : null;

  return (
    <div className={styles.graphRoot}>
      <svg viewBox={`${minX} ${minY} ${vw} ${vh}`} className={styles.svg} preserveAspectRatio="xMidYMid meet">
        {edges.map(([s, t], i) => {
          const a = nodeMap[s], b = nodeMap[t];
          if (!a || !b) return null;
          return <line key={i} x1={a.x} y1={a.y} x2={b.x} y2={b.y} className={styles.edge} />;
        })}

        {nodes.map(n => (
          <g key={n.id}
            onMouseEnter={() => setHoveredId(n.id)}
            onMouseLeave={() => setHoveredId(null)}
            onClick={() => n.kind === "task" && onSelectNode(n.id)}
            style={{ cursor: n.kind === "task" ? "pointer" : "default" }}
          >
            {n.kind === "root" ? (
              <>
                <circle cx={n.x} cy={n.y} r={n.size} className={styles.rootOrb} />
                <foreignObject x={n.x - 10} y={n.y - 10} width={20} height={20}>
                  <CodeOrbGlyph style={{ width: 20, height: 20, color: "white" }} />
                </foreignObject>
              </>
            ) : (
              <>
                <circle cx={n.x} cy={n.y} r={n.size}
                  className={`${styles.nodeCore} ${styles[`node${n.state.charAt(0).toUpperCase() + n.state.slice(1)}`]}`}
                />
                {hoveredId === n.id && (
                  <circle cx={n.x} cy={n.y} r={n.size + 4} className={styles.hoverHalo} />
                )}
              </>
            )}
          </g>
        ))}
      </svg>

      {hovered && hovered.kind === "task" && (
        <div className={styles.tooltip} style={{ left: "50%", bottom: "12px" }}>
          <strong>{hovered.label}</strong>
          <span>{hovered.state}</span>
        </div>
      )}
    </div>
  );
}
