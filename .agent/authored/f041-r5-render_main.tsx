// F041 R5 T003's render harness (evidence, not product): mounts the real `ArtifactsPanel` from
// `apps/ui/src` over a `window.fetch` stand-in that answers a fixed fixture — a README with one
// listed capture, one image outside `captures/` and three screenshots, and a preview record that
// walks stopped -> starting -> probing -> live once a start is posted and back to stopped once a
// stop is posted (DECISION F041 D5) — the way `.agent/authored/f039-r5-render_main.tsx` mounts a
// real overlay over one fixed view. No real door is read here: every request `window.fetch`
// intercepts is answered in memory, and every call is recorded on `window.__previewCalls` so
// `drive.mjs` can inspect what the card actually sent. `window.__previewReadCount` counts every
// `/preview` read, and `window.__artifactsClosed` records the panel's own close — never a second
// copy of the DOM's own state retyped into the driver script. The `preview` query parameter
// (`?preview=failed` or `?preview=na`) fixes the preview view to `failed` or `not_applicable`
// instead of the normal stopped/starting/probing/live walk, for the two states no button click in
// this harness can reach.
import { useState } from "react";
import { createRoot } from "react-dom/client";
import "../../apps/ui/src/styles/tokens.css";
import "../../apps/ui/src/styles/globals.css";
import { ArtifactsPanel } from "../../apps/ui/src/components/artifacts/ArtifactsPanel";

const JOB_ID = "render-job";
const SERVER_TOKEN = "render-token";
const FORCE_PREVIEW = new URLSearchParams(window.location.search).get("preview");
const UPDATED_AT = "2026-09-29T00:00:00+00:00";

const README_HTML =
  '<h1>Fixture app</h1><p>Before <img src="captures/one.png" alt="first shot"> after '
  + '<img src="docs/elsewhere.png" alt="elsewhere shot"></p>';

const ARTIFACTS_VIEW = {
  readme: {
    root: "workspace",
    path: "README.md",
    html: README_HTML,
    truncated: true,
    source_bytes: README_HTML.length,
  },
  images: [
    { root: "evidence", path: "captures/one.png", bytes: 100, content_type: "image/png" },
    { root: "evidence", path: "captures/two.png", bytes: 100, content_type: "image/png" },
    { root: "evidence", path: "captures/three.png", bytes: 100, content_type: "image/png" },
  ],
  error: "",
};

interface PreviewCall {
  path: string;
  method: string;
  headers: Record<string, string>;
  body: string | null;
}

(window as unknown as { __previewCalls: PreviewCall[] }).__previewCalls = [];
(window as unknown as { __previewReadCount: number }).__previewReadCount = 0;
(window as unknown as { __artifactsClosed: boolean }).__artifactsClosed = false;

// THE PREVIEW STATE MACHINE this fixture walks: `previewStarted` is set by a posted
// `job.preview-start` and cleared by a posted `job.preview-stop`; `previewStep` counts the reads
// since the last start, so the first read after a start answers `starting`, the second `probing`,
// and the third (and every one after it) `live`.
let previewStarted = false;
let previewStep = 0;

function currentPreviewView(): Record<string, unknown> {
  if (FORCE_PREVIEW === "failed") {
    return {
      state: "failed", url: "", port: 0,
      reason: "started but health check failed: connection refused",
      updated_at: UPDATED_AT,
    };
  }
  if (FORCE_PREVIEW === "na") {
    return {
      state: "not_applicable", url: "", port: 0,
      reason: "the job has no project folder to run",
      updated_at: UPDATED_AT,
    };
  }
  if (!previewStarted) {
    return { state: "stopped", url: "", port: 0, reason: "", updated_at: UPDATED_AT };
  }
  previewStep += 1;
  if (previewStep === 1) {
    return { state: "starting", url: "", port: 0, reason: "", updated_at: UPDATED_AT };
  }
  if (previewStep === 2) {
    return { state: "probing", url: "", port: 0, reason: "", updated_at: UPDATED_AT };
  }
  return { state: "live", url: "http://127.0.0.1:5173/", port: 5173, reason: "", updated_at: UPDATED_AT };
}

function jsonResponse(body: unknown): Response {
  return new Response(JSON.stringify(body), { status: 200, headers: { "Content-Type": "application/json" } });
}

const realFetch = window.fetch.bind(window);

window.fetch = ((input: RequestInfo | URL, init?: RequestInit) => {
  const path = typeof input === "string" ? input : input.toString();
  // Only this feature's own API calls are intercepted; anything else (there is none in this
  // harness) would fall through to the real fetch untouched.
  if (!path.startsWith("/api/jobs/")) {
    return realFetch(input, init);
  }
  const method = (init?.method ?? "GET").toUpperCase();
  const headers = (init?.headers as Record<string, string> | undefined) ?? {};
  const body = typeof init?.body === "string" ? init.body : null;
  (window as unknown as { __previewCalls: PreviewCall[] }).__previewCalls.push({ path, method, headers, body });

  if (path.includes("/artifacts?")) {
    return Promise.resolve(jsonResponse(ARTIFACTS_VIEW));
  }
  if (path.includes("/preview?")) {
    (window as unknown as { __previewReadCount: number }).__previewReadCount += 1;
    return Promise.resolve(jsonResponse(currentPreviewView()));
  }
  if (path.includes("/commands")) {
    const parsed = body ? (JSON.parse(body) as { command?: string }) : {};
    if (parsed.command === "job.preview-start") {
      previewStarted = true;
      previewStep = 0;
    } else if (parsed.command === "job.preview-stop") {
      previewStarted = false;
      previewStep = 0;
    }
    return Promise.resolve(jsonResponse({
      command: parsed.command, outcome: "accepted", state: previewStarted ? "starting" : "stopped",
    }));
  }
  return Promise.reject(new Error(`unhandled fetch in render harness: ${path}`));
}) as typeof window.fetch;

function Harness() {
  const [open, setOpen] = useState(true);
  return (
    <>
      {open && (
        <ArtifactsPanel
          jobId={JOB_ID}
          serverToken={SERVER_TOKEN}
          onClose={() => {
            (window as unknown as { __artifactsClosed: boolean }).__artifactsClosed = true;
            setOpen(false);
          }}
        />
      )}
    </>
  );
}

const container = document.getElementById("app");
if (container) {
  createRoot(container).render(<Harness />);
}
