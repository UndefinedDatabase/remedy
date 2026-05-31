import { useMemo } from "react";
import styles from "./ConstellationBackdrop.module.css";

interface ConstellationNode {
  x: number;
  y: number;
  r: number;
  kind: "white" | "blue" | "cyan" | "purple";
}

interface ConstellationEdge {
  x1: number; y1: number; x2: number; y2: number;
  faint: boolean;
}

interface ConstellationParticle {
  x: number; y: number; r: number;
}

interface ConstellationModel {
  nodes: ConstellationNode[];
  edges: ConstellationEdge[];
  particles: ConstellationParticle[];
}

function seededRandom(seed: number) {
  let s = seed;
  return () => {
    s = (s * 1664525 + 1013904223) & 0x7fffffff;
    return s / 0x7fffffff;
  };
}

function hashString(str: string): number {
  let h = 0;
  for (let i = 0; i < str.length; i++) {
    h = ((h << 5) - h + str.charCodeAt(i)) | 0;
  }
  return Math.abs(h);
}

export function buildConstellation(jobId: string): ConstellationModel {
  const rng = seededRandom(hashString(jobId || "remedy-default"));
  const cx = 488;
  const cy = 276;
  const nodes: ConstellationNode[] = [];
  const edges: ConstellationEdge[] = [];
  const particles: ConstellationParticle[] = [];

  // Central orb
  nodes.push({ x: cx, y: cy, r: 18, kind: "blue" });

  // 9 major branches radiating from center
  const branchCount = 9;
  const branchAngles: number[] = [];
  for (let b = 0; b < branchCount; b++) {
    const angle = (b / branchCount) * Math.PI * 2 + (rng() - 0.5) * 0.3;
    branchAngles.push(angle);
    const branchLen = 120 + rng() * 180;
    const segCount = 4 + Math.floor(rng() * 5);
    let px = cx, py = cy;
    for (let s = 0; s < segCount; s++) {
      const dist = (branchLen / segCount) * (s + 1);
      const spreadAngle = angle + (rng() - 0.5) * 0.6;
      const nx = cx + Math.cos(spreadAngle) * dist + (rng() - 0.5) * 40;
      const ny = cy + Math.sin(spreadAngle) * dist + (rng() - 0.5) * 30;
      const kinds: ConstellationNode["kind"][] = ["white", "blue", "cyan", "purple"];
      const kind = kinds[Math.floor(rng() * kinds.length)];
      const r = 2.5 + rng() * 4;
      nodes.push({ x: nx, y: ny, r, kind });
      edges.push({ x1: px, y1: py, x2: nx, y2: ny, faint: rng() > 0.5 });
      px = nx; py = ny;

      // Sub-branches
      if (rng() > 0.4) {
        const subCount = 2 + Math.floor(rng() * 3);
        for (let ss = 0; ss < subCount; ss++) {
          const subAngle = spreadAngle + (rng() - 0.5) * 1.4;
          const subDist = 20 + rng() * 60;
          const sx = nx + Math.cos(subAngle) * subDist;
          const sy = ny + Math.sin(subAngle) * subDist;
          if (sx > 10 && sx < 966 && sy > 10 && sy < 542) {
            const subKind = kinds[Math.floor(rng() * kinds.length)];
            nodes.push({ x: sx, y: sy, r: 1.8 + rng() * 3, kind: subKind });
            edges.push({ x1: nx, y1: ny, x2: sx, y2: sy, faint: true });
          }
        }
      }
    }
  }

  // Fill to at least 160 nodes
  while (nodes.length < 160) {
    const angle = rng() * Math.PI * 2;
    const dist = 40 + rng() * 240;
    const x = cx + Math.cos(angle) * dist + (rng() - 0.5) * 80;
    const y = cy + Math.sin(angle) * dist + (rng() - 0.5) * 60;
    if (x > 5 && x < 971 && y > 5 && y < 547) {
      const kinds: ConstellationNode["kind"][] = ["white", "blue", "cyan", "purple"];
      nodes.push({ x, y, r: 1.5 + rng() * 2.5, kind: kinds[Math.floor(rng() * kinds.length)] });
      // Connect to nearest existing node
      let minDist = Infinity, minIdx = 0;
      for (let i = 0; i < nodes.length - 1; i++) {
        const d = Math.hypot(nodes[i].x - x, nodes[i].y - y);
        if (d < minDist) { minDist = d; minIdx = i; }
      }
      if (minDist < 120) {
        edges.push({ x1: nodes[minIdx].x, y1: nodes[minIdx].y, x2: x, y2: y, faint: true });
      }
    }
  }

  // Fill edges to at least 200
  while (edges.length < 200) {
    const a = Math.floor(rng() * nodes.length);
    const b = Math.floor(rng() * nodes.length);
    if (a !== b && Math.hypot(nodes[a].x - nodes[b].x, nodes[a].y - nodes[b].y) < 100) {
      edges.push({ x1: nodes[a].x, y1: nodes[a].y, x2: nodes[b].x, y2: nodes[b].y, faint: true });
    }
  }

  // Star particles
  for (let i = 0; i < 40; i++) {
    particles.push({ x: rng() * 976, y: rng() * 552, r: 0.8 + rng() * 1.5 });
  }

  return { nodes, edges, particles };
}

export function ConstellationBackdrop({ jobId }: { jobId: string }) {
  const model = useMemo(() => buildConstellation(jobId), [jobId]);
  return (
    <svg className={styles.constellation} viewBox="0 0 976 552" aria-hidden="true" data-ui="constellation-backdrop">
      <defs>
        <filter id="nodeGlow">
          <feGaussianBlur stdDeviation="3" result="blur" />
          <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
        </filter>
      </defs>
      <g>
        {model.edges.map((e, i) => (
          <line key={i} x1={e.x1} y1={e.y1} x2={e.x2} y2={e.y2} className={e.faint ? styles.edgeFaint : styles.edge} />
        ))}
      </g>
      <g filter="url(#nodeGlow)">
        {model.nodes.map((n, i) => (
          <circle key={i} cx={n.x} cy={n.y} r={n.r}
            className={n.kind === "blue" ? styles.nodeBlue : n.kind === "cyan" ? styles.nodeCyan : n.kind === "purple" ? styles.nodePurple : styles.node} />
        ))}
      </g>
      <g>
        {model.particles.map((p, i) => (
          <circle key={i} cx={p.x} cy={p.y} r={p.r} className={styles.particle} />
        ))}
      </g>
    </svg>
  );
}
