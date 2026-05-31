import { BaseEdge, getBezierPath, type EdgeProps } from "@xyflow/react";

export function SoftGlowEdge(props: EdgeProps) {
  const [path] = getBezierPath(props);
  const state = String(props.data?.state || "pending");
  const stroke = state === "done" ? "rgba(76,198,129,.34)" : state === "current" ? "rgba(76,131,255,.48)" : state === "suggested" ? "rgba(162,140,255,.28)" : "rgba(99,126,178,.18)";
  return (
    <>
      <BaseEdge path={path} style={{ stroke: "rgba(76,131,255,.10)", strokeWidth: 8 }} />
      <BaseEdge path={path} style={{ stroke, strokeWidth: state === "current" ? 2.2 : 1.4 }} />
    </>
  );
}
