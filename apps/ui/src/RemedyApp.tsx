import { useCallback, useEffect, useState } from "react";
import { CircularProgress } from "@mui/material";
import { loadRemedyDashboard } from "./api/remedyApi";
import type { RemedyDashboard } from "./api/types";
import {
  MISSING_ADDRESS_LINE,
  EMPTY_PROJECT_LINE,
  addressFromSearch,
  cockpitFaceOf,
  homeSearch,
  shellKeyOf,
} from "./api/cockpitAddress";
import type { CockpitAddress } from "./api/cockpitAddress";
import { searchForProjectSwitch } from "./api/projectScope";
import type { ProjectSwitch } from "./api/projectScope";
import { RemedyShell } from "./components/shell/RemedyShell";
import { ReducedMotionProvider } from "./components/shell/ReducedMotionProvider";
import { ProjectProvider } from "./components/shell/ProjectProvider";
import { ProjectSwitcher } from "./components/shell/ProjectSwitcher";
import { HomeGrid } from "./components/home/HomeGrid";

function readUrlState(): CockpitAddress {
  return addressFromSearch(window.location.search);
}

export default function RemedyApp() {
  const [address, setAddress] = useState<CockpitAddress>(readUrlState);
  const [dashboard, setDashboard] = useState<RemedyDashboard | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  const { jobId, project, token } = address;
  const face = cockpitFaceOf(address);

  // Clears the dashboard, the error and the selection before the new address loads, so no
  // panel, stream or selection of the OLD project survives into the new one.
  const openAddress = useCallback((search: string) => {
    setDashboard(null);
    setError(null);
    setSelectedNodeId(null);
    setAddress(addressFromSearch(search));
  }, []);

  useEffect(() => {
    function onPopState(): void {
      openAddress(window.location.search);
    }
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
  }, [openAddress]);

  // The ONE writer of the page's address: pushes for a switch or the way home, so Back returns
  // to the page left, and replaces for the single-project skip, so Back never returns to a grid
  // that would only skip forward again to reach.
  const writeAddress = useCallback((search: string, replace: boolean) => {
    const url = `${window.location.pathname}${search}${window.location.hash}`;
    if (replace) {
      window.history.replaceState(window.history.state, "", url);
    } else {
      window.history.pushState(window.history.state, "", url);
    }
    openAddress(search);
  }, [openAddress]);

  const onSwitched = useCallback((target: ProjectSwitch, replace: boolean) => {
    writeAddress(searchForProjectSwitch(window.location.search, target.slug, target.jobId), replace);
  }, [writeAddress]);

  const onHome = useCallback(() => {
    writeAddress(homeSearch(window.location.search), false);
  }, [writeAddress]);

  // DECISION F292 D3: a write that changed what the dashboard shows asks for the dashboard
  // again at once rather than waiting for the next five-second read. Each request raises the
  // count, which re-runs the read below immediately and restarts its timer.
  const [reloadRequest, setReloadRequest] = useState(0);
  const requestReload = useCallback(() => setReloadRequest((count) => count + 1), []);

  useEffect(() => {
    if (face !== "job") return;
    let cancelled = false;
    async function load() {
      try {
        const data = await loadRemedyDashboard({ jobId, token });
        if (!cancelled) setDashboard(data);
      } catch (e) {
        if (!cancelled) setError(e instanceof Error ? e.message : "Could not load Remedy UI.");
      }
    }
    load();
    const timer = window.setInterval(load, 5000);
    return () => { cancelled = true; window.clearInterval(timer); };
  }, [face, jobId, token, reloadRequest]);

  let body: React.ReactNode;
  if (face === "missing") {
    body = (
      <div data-ui="remedy-app" style={{ display: "grid", placeItems: "center", height: "100%", color: "#14254b" }}>
        {MISSING_ADDRESS_LINE}
      </div>
    );
  } else if (face === "home") {
    body = (
      <div data-ui="remedy-home" style={{ height: "100%", overflowY: "auto" }}>
        <HomeGrid />
      </div>
    );
  } else if (face === "empty_project") {
    // R-1108: `alignContent` and `gap` group the switcher and the sentence into one cluster
    // instead of each taking its own row of half the page's height.
    body = (
      <div
        data-ui="remedy-app"
        style={{ display: "grid", placeItems: "center", alignContent: "center", gap: 16, height: "100%" }}
      >
        <ProjectSwitcher fallback={null} />
        <p data-ui="empty-project">{EMPTY_PROJECT_LINE}</p>
      </div>
    );
  } else if (error) {
    body = (
      <div data-ui="remedy-app" style={{ display: "grid", placeItems: "center", height: "100%", color: "var(--remedy-red-500)" }}>
        {error}
      </div>
    );
  } else if (!dashboard) {
    body = <div data-ui="remedy-app" style={{ display: "grid", placeItems: "center", height: "100%" }}><CircularProgress /></div>;
  } else {
    // The per-run token travels as a PROP from here to the decision inbox's answer
    // buttons, because this is the only place that reads it and a component that
    // re-read the URL would be a second source for one credential.
    body = <RemedyShell key={shellKeyOf(address)} dashboard={dashboard} serverToken={token} selectedNodeId={selectedNodeId} onSelectNode={setSelectedNodeId} onReload={requestReload} />;
  }

  return (
    <ReducedMotionProvider>
      <ProjectProvider token={token} jobId={jobId} project={project} onSwitched={onSwitched} onHome={onHome}>
        {body}
      </ProjectProvider>
    </ReducedMotionProvider>
  );
}
