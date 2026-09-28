// F036 R5 T003's second half — the render harness (evidence, not product): mounts the real
// `TourOverlay` from `apps/ui/src` reading ONE fixed six-stop view through a `window.fetch`
// this page replaces (DECISION F036 D6), the way `.agent/authored/f035-r7-render_main.tsx`
// mounts `DetailPopover` and `EvidencePanel` against one fixed `OwnershipView`. The first stop's
// anchor names the demo recording's own first task (`brainDemoRecording.ts`), never invented;
// the other five are two diff stops, an evidence stop, a command stop and a second evidence
// stop, in that order, so `drive.mjs` can prove the step label, the progress dots, Previous and
// Next at both ends, "Show me" lifting the backdrop for a diff stop, a command's code and an
// evidence stop's absent "Show me". Every `onShowAnchor` call and the close are recorded on
// `window` rather than a second copy retyped into the driver script.
//
// `window.__remountUnreadable()` (called by drive.mjs for C-h) installs a fetch answering a
// payload `decodeTourView` refuses — an object with none of its required keys, carrying a
// marker string that must never reach the page — and remounts the overlay under a fresh `key`,
// so its own read effect fires again against the new fetch.
import { useState } from "react";
import { createRoot } from "react-dom/client";
import "../../apps/ui/src/styles/tokens.css";
import type { TourAnchor } from "../../apps/ui/src/api/resultTour";
import { tourViewPath } from "../../apps/ui/src/api/resultTour";
import { BRAIN_DEMO_JOB_ID, BRAIN_DEMO_TASKS } from "../../apps/ui/src/components/graph/brainDemoRecording";
import { TourOverlay } from "../../apps/ui/src/components/tour/TourOverlay";

const JOB_ID = BRAIN_DEMO_JOB_ID;
const TOKEN = "harness-token";
// The demo recording's own first task — never retyped, read off it.
const FIRST_TASK_ID = BRAIN_DEMO_TASKS[0].id;

// The marker C-h proves never reaches the page: present only in the unreadable remount's raw
// payload, which `decodeTourView` refuses whole before any of it is rendered.
const UNREADABLE_MARKER = "SECRET_MARKER_TEXT_NOT_SHOWN";

const STOPS = [
  {
    title: "How the run started",
    body: "The first task carried out the order's own work.",
    anchor: { kind: "node", ref: FIRST_TASK_ID },
  },
  {
    title: "The main change",
    body: "The path pattern was repaired.\nSee the diff for the whole change.",
    anchor: { kind: "diff", ref: "packages/orchestration/result_tour.py" },
  },
  {
    title: "The browser's half",
    body: "The pure module gained the overlay's own rules.",
    anchor: { kind: "diff", ref: "apps/ui/src/api/resultTour.ts" },
  },
  {
    title: "The evidence",
    body: "The job's own report records the outcome.",
    anchor: { kind: "evidence", ref: "report.md" },
  },
  {
    title: "How to check it",
    body: "Run the suite that proves the repair.",
    anchor: { kind: "command", ref: "pytest tests/orchestration/test_result_tour.py" },
  },
  {
    title: "A second piece of evidence",
    body: "The golden fixture records the repaired case.",
    anchor: { kind: "evidence", ref: "golden_generated.json" },
  },
];

const READABLE_WIRE = {
  stored: true,
  version: 1,
  tour: {
    schema: "remedy.tour.v1",
    job_id: JOB_ID,
    generator: "summary-role",
    stops: STOPS,
    dropped: [],
  },
  error: "",
};

const UNREADABLE_WIRE = { marker: UNREADABLE_MARKER };

const TOUR_URL = tourViewPath({ jobId: JOB_ID, token: TOKEN });

const originalFetch = window.fetch.bind(window);

function installFetch(payload: unknown) {
  window.fetch = (async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = typeof input === "string" ? input : input instanceof URL ? input.toString() : input.url;
    if (url === TOUR_URL) {
      return new Response(JSON.stringify(payload), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      });
    }
    return originalFetch(input, init);
  }) as typeof window.fetch;
}

installFetch(READABLE_WIRE);

// Exposed for drive.mjs: every anchor "Show me" hands the shell, and whether Escape (or the
// close button) fired — never a second copy of the recorded facts kept only in the DOM.
(window as unknown as { __onShowAnchorCalls: TourAnchor[] }).__onShowAnchorCalls = [];
(window as unknown as { __onCloseCalled: boolean }).__onCloseCalled = false;

function Harness() {
  const [remountKey, setRemountKey] = useState(0);

  (window as unknown as { __remountUnreadable: () => void }).__remountUnreadable = () => {
    installFetch(UNREADABLE_WIRE);
    setRemountKey((key) => key + 1);
  };

  return (
    <TourOverlay
      key={remountKey}
      jobId={JOB_ID}
      serverToken={TOKEN}
      onClose={() => {
        (window as unknown as { __onCloseCalled: boolean }).__onCloseCalled = true;
      }}
      onShowAnchor={(anchor) => {
        (window as unknown as { __onShowAnchorCalls: TourAnchor[] }).__onShowAnchorCalls.push(anchor);
      }}
    />
  );
}

const container = document.getElementById("app");
if (container) createRoot(container).render(<Harness />);
