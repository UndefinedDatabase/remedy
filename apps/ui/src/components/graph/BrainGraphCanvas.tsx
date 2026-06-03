import { useRef, useState } from "react";
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

const STAGE_W = 1120;
const STAGE_H = 680;
const VB = `${-STAGE_W / 2} ${-STAGE_H / 2} ${STAGE_W} ${STAGE_H}`;
const ROOT_R = 38;
const TASK_R = 14;
const DEG = Math.PI / 180;
const BRANCH_ANGLES = [-145, -70, -15, 40, 105];

function buildDisplayModel(dashboard: RemedyDashboard): { nodes: DisplayNode[]; edges: [string, string][] } {
  const tasks = dashboard.tasks.slice(0, 80);
  const nodes: DisplayNode[] = [];
  const edges: [string, string][] = [];

  nodes.push({ id: "root", label: dashboard.title || "Job", state: "current", kind: "root", x: 0, y: 20, size: ROOT_R });

  const branchCount = Math.min(5, Math.max(2, Math.ceil(tasks.length / 3) || 2));
  const angles = BRANCH_ANGLES.slice(0, branchCount);

  tasks.forEach((t, i) => {
    const branch = i % branchCount;
    const depth = Math.floor(i / branchCount) + 1;
    const rad = angles[branch] * DEG;
    const radius = 110 + depth * 68;
    const bend = Math.sin(depth * 0.85 + branch * 1.2) * 28;
    const x = Math.cos(rad) * radius + Math.cos(rad + Math.PI / 2) * bend;
    const y = Math.sin(rad) * radius + Math.sin(rad + Math.PI / 2) * bend;

    const st = t.state;
    const state = st === "done" ? "done" : st === "current" ? "current" : st === "blocked" ? "blocked" : "planned";
    nodes.push({ id: t.id, label: t.label, state, kind: "task", x, y, size: TASK_R });
    edges.push(["root", t.id]);
  });

  return { nodes, edges };
}

function curvePath(ax: number, ay: number, bx: number, by: number): string {
  const mx = (ax + bx) / 2;
  const my = (ay + by) / 2;
  const dx = bx - ax;
  const dy = by - ay;
  const cx = mx - dy * 0.12;
  const cy = my + dx * 0.12;
  return `M${ax},${ay} Q${cx},${cy} ${bx},${by}`;
}

export function BrainGraphCanvas({ dashboard, filter = "all", onSelectNode }: { dashboard: RemedyDashboard; filter?: string; onSelectNode: (nodeId: string | null) => void }) {
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
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
  const nodeMap = Object.fromEntries(nodes.map(n => [n.id, n]));
  const hovered = hoveredId ? nodeMap[hoveredId] : null;

  const tooltipPos = hovered && containerRef.current ? (() => {
    const rect = containerRef.current.getBoundingClientRect();
    const svgX = (hovered.x + STAGE_W / 2) / STAGE_W;
    const svgY = (hovered.y + STAGE_H / 2) / STAGE_H;
    return { left: svgX * rect.width, top: svgY * rect.height - 28 };
  })() : null;

  return (
    <div className={styles.graphRoot} ref={containerRef}>
      <svg viewBox={VB} className={styles.svg} preserveAspectRatio="xMidYMid meet">
        {edges.map(([s, t], i) => {
          const a = nodeMap[s], b = nodeMap[t];
          if (!a || !b) return null;
          return <path key={i} d={curvePath(a.x, a.y, b.x, b.y)} className={styles.edge} />;
        })}

        {nodes.map(n => (
          <g key={n.id}
            tabIndex={n.kind === "task" ? 0 : undefined}
            role={n.kind === "task" ? "button" : undefined}
            aria-label={n.kind === "task" ? `${n.label} — ${n.state}` : `Root: ${n.label}`}
            onMouseEnter={() => setHoveredId(n.id)}
            onMouseLeave={() => setHoveredId(null)}
            onFocus={() => setHoveredId(n.id)}
            onBlur={() => setHoveredId(null)}
            onClick={() => n.kind === "task" && onSelectNode(n.id)}
            onKeyDown={e => e.key === "Enter" && n.kind === "task" && onSelectNode(n.id)}
            style={{ cursor: n.kind === "task" ? "pointer" : "default", outline: "none" }}
          >
            {n.kind === "root" ? (
              <>
                <circle cx={n.x} cy={n.y} r={n.size} className={styles.rootOrb} />
                <foreignObject x={n.x - 12} y={n.y - 12} width={24} height={24}>
                  <CodeOrbGlyph style={{ width: 24, height: 24, color: "white" }} />
                </foreignObject>
              </>
            ) : (
              <>
                <circle cx={n.x} cy={n.y} r={n.size}
                  className={`${styles.nodeCore} ${styles[`node${n.state.charAt(0).toUpperCase() + n.state.slice(1)}`]}`}
                />
                {hoveredId === n.id && (
                  <circle cx={n.x} cy={n.y} r={n.size + 5} className={styles.hoverHalo} />
                )}
              </>
            )}
          </g>
        ))}
      </svg>

      {hovered && tooltipPos && (
        <div className={styles.tooltip} style={{ left: tooltipPos.left, top: tooltipPos.top }}>
          <strong>{hovered.label}</strong>
          <span>{hovered.state === "done" ? "Completed" : hovered.state === "current" ? "In progress" : hovered.state === "blocked" ? "Blocked" : hovered.kind === "root" ? `${dashboard.tasks.length} tasks` : "Planned"}</span>
        </div>
      )}
    </div>
  );
}
