import { useEffect, useMemo, useState } from "react";
import { CircularProgress } from "@mui/material";
import { loadRemedyDashboard } from "./api/remedyApi";
import type { RemedyDashboard } from "./api/types";
import { RemedyShell } from "./components/shell/RemedyShell";
import { ReducedMotionProvider } from "./components/shell/ReducedMotionProvider";

function readUrlState() {
  const p = new URLSearchParams(window.location.search);
  return { jobId: p.get("job") || p.get("job_id") || "", token: p.get("token") || "" };
}

export default function RemedyApp() {
  const { jobId, token } = useMemo(readUrlState, []);
  const [dashboard, setDashboard] = useState<RemedyDashboard | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      if (!jobId || !token) { setError("Missing job or token in the URL."); return; }
      try {
        const data = await loadRemedyDashboard({ jobId, token });
        if (!cancelled) {
          setDashboard(data);
          setSelectedNodeId(data.graph.nodes[0]?.nodeId ?? null);
        }
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : "Could not load Remedy UI.");
      }
    }
    load();
    const timer = window.setInterval(load, 5000);
    return () => { cancelled = true; window.clearInterval(timer); };
  }, [jobId, token]);

  if (error) return <div data-ui="remedy-app" style={{ display: "grid", placeItems: "center", height: "100%", color: "#14254b" }}>{error}</div>;
  if (!dashboard) return <div data-ui="remedy-app" style={{ display: "grid", placeItems: "center", height: "100%" }}><CircularProgress /></div>;
  return <ReducedMotionProvider><RemedyShell dashboard={dashboard} selectedNodeId={selectedNodeId} onSelectNode={setSelectedNodeId} /></ReducedMotionProvider>;
}
