import { useEffect, useState } from "react";
import type { RemedyDashboard } from "../../api/types";
import type { DiffEnvelope } from "../../api/diffViewModel";
import type { JobDigest } from "../../api/jobDigest";
import { loadDiffEnvelope, loadJobDigest } from "../../api/remedyApi";
import { digestVisibility } from "../../api/digestVisibility";
import type { DigestDismissal } from "../../api/digestVisibility";
import { newestActionRow } from "../../api/actionClass";
import { browserDigestVisibilityPort } from "../../api/browserDigestPort";
import { DigestHeroCard } from "../digest/DigestHeroCard";
import { DiffFileSidebar } from "../diff/DiffFileSidebar";
import { DiffView } from "../diff/DiffView";
import { LeftBrandRail } from "../rail/LeftBrandRail";
import { TopMetricsBar } from "../metrics/TopMetricsBar";
import { CommandBar } from "../command/CommandBar";
import { BrainGraphStage } from "../graph/BrainGraphStage";
import { RightLivePanel } from "../panels/RightLivePanel";
import { PhaseTimeline } from "../timeline/PhaseTimeline";
import { DetailPopover } from "../detail/DetailPopover";
import { DegradedBanner } from "./DegradedBanner";
import styles from "./RemedyShell.module.css";
import { browserBrainStreamEnv, createBrainStreamHostDeps } from "../../api/brainStreamDeps";
import { useBrainStream } from "../../api/useBrainStream";
import { metricsWithCostTicker } from "../../api/costTicker";
import { metricsWithCostReconciliation } from "../../api/costReconciliation";

/** What the diff panel says while its envelope is still in flight. Plain words
 *  rather than an empty `DiffView`, because a viewer showing no files is
 *  indistinguishable from a change that touched none. */
const DIFF_PENDING_TEXT = "Reading the change for this task run…";

/** What it says when the server answered but has no diff to give. `available`
 *  and `reason` are both guaranteed present by `readDiffEnvelope`, so this
 *  branch reads them directly; the reason is appended only when the envelope
 *  carries one, since `reason` is legitimately null on a plain empty diff. */
const DIFF_UNAVAILABLE_TEXT = "No diff is available for this task run.";

export function RemedyShell({ dashboard, serverToken, selectedNodeId, onSelectNode }: { dashboard: RemedyDashboard; serverToken: string; selectedNodeId: string | null; onSelectNode: (nodeId: string | null) => void }) {
  // The cockpit subscribes HERE rather than in RemedyApp: the shell renders
  // only once a dashboard has loaded, so `dashboard.jobId` is always a real
  // job, where RemedyApp would have to open a stream against an empty id on
  // every URL that carries none (DECISION F008 D3).
  const stream = useBrainStream(dashboard.jobId, (jobId) =>
    createBrainStreamHostDeps(jobId, browserBrainStreamEnv(window)));
  let selectedNode = selectedNodeId ? (dashboard.graph.nodes.find(n => n.nodeId === selectedNodeId || n.id === selectedNodeId) ?? null) : null;
  // Prompt satellite nodes carry the prompt item id as their node id. Resolve
  // such a selection to its owning task node so the popover (and its Prompt
  // Trace panel) opens with the prompt highlighted.
  let selectedPromptId: string | null = null;
  if (!selectedNode && selectedNodeId) {
    const promptItem = dashboard.promptTrace?.items.find(p => p.id === selectedNodeId);
    if (promptItem) {
      selectedPromptId = promptItem.id;
      const owningTask = dashboard.tasks.find(t => t.id === promptItem.taskId);
      if (owningTask) {
        selectedNode = dashboard.graph.nodes.find(n => n.nodeId === owningTask.nodeId) ?? null;
      }
    }
  }
  // WHICH task run's diff is open, and the envelope last read for it. Two pieces
  // of state rather than one, because "a panel is open" and "its content has
  // arrived" are different facts and the panel has to render the gap between
  // them honestly.
  const [openDiffTaskId, setOpenDiffTaskId] = useState<string | null>(null);
  const [diffEnvelope, setDiffEnvelope] = useState<DiffEnvelope | null>(null);

  // THE READ. `loadDiffEnvelope` never throws — every failure arrives as a total
  // envelope with `available` false — so there is deliberately no error branch
  // here and none is written.
  //
  // TWO PROPERTIES THIS EFFECT MUST KEEP, both because a viewer that lies is
  // worse than one that is slow. First, clearing the stored envelope on every
  // run means closing the panel empties it and re-opening it cannot flash the
  // previous task's diff. Second, `cancelled` is the answer to a response that
  // comes back AFTER the selection moved on: React re-runs the cleanup before
  // the next effect, so a slow first request finds the flag set and stores
  // nothing, instead of painting one task's change under another task's name.
  useEffect(() => {
    let cancelled = false;
    setDiffEnvelope(null);
    if (openDiffTaskId !== null) {
      void loadDiffEnvelope({
        jobId: dashboard.jobId,
        token: serverToken,
        taskId: openDiffTaskId,
      }).then((envelope) => {
        if (!cancelled) setDiffEnvelope(envelope);
      });
    }
    return () => { cancelled = true; };
  }, [openDiffTaskId, dashboard.jobId, serverToken]);

  // THE DIGEST LOAD, once per mounted shell. UNLIKE THE DIFF-ENVELOPE EFFECT
  // ABOVE, this effect does NOT clear `digest` to `null` on re-run: that
  // effect clears because the diff panel re-opens DIFFERENT task ids
  // repeatedly across one session, and a stale diff under a new task's name
  // would be a wrong answer. `dashboard.jobId` and `serverToken` are
  // effectively stable for the whole life of one mounted shell — a job's
  // page does not swap jobs under the operator — so there is no repeated
  // re-selection this effect needs to guard against. The `cancelled` guard is
  // kept regardless: a slow first request racing a token refresh is still
  // possible even if rare.
  const [digest, setDigest] = useState<JobDigest | null>(null);
  useEffect(() => {
    let cancelled = false;
    void loadJobDigest({ jobId: dashboard.jobId, token: serverToken }).then((loaded) => {
      if (!cancelled) setDigest(loaded);
    });
    return () => { cancelled = true; };
  }, [dashboard.jobId, serverToken]);

  // THE STORAGE EDGE, BOUND HERE because this is the edge: `digestVisibility.ts`
  // DECLARES `DigestVisibilityPort` and implements nothing, exactly as
  // `browserBrainStreamEnv(window)` above binds the stream's own globals at
  // this same mount. `window.localStorage` occurs nowhere else in this file.
  const digestPort = browserDigestVisibilityPort(window.localStorage);

  // Read once, before the write below ever runs, so the digest visibility
  // rule sees the instant the operator was last here rather than the one
  // this very mount is about to record.
  const [lastSeenMs] = useState<number | null>(() => digestPort.readLastSeen(dashboard.jobId));
  useEffect(() => {
    digestPort.writeLastSeen(dashboard.jobId, Date.now());
  }, [dashboard.jobId]);

  const [dismissedAtMs, setDismissedAtMs] = useState<DigestDismissal>(
    () => digestPort.readDismissal(dashboard.jobId),
  );

  // The brain stream's own ring buffer already carries every action this
  // session has seen; the digest trigger asks only for the newest of them.
  const latestActivityMs = newestActionRow(stream.recent ?? [])?.receivedAtMs ?? null;

  // THE MOUNT'S OWN CLOCK READ (DECISION F040 D8, R11 constraint 7) — the
  // file's only `Date.now()` call outside `writeLastSeen`'s own argument
  // above. A separate read from that one on purpose: one clock read per
  // concern, never a value reused for both.
  const visibility = digestVisibility({
    digest,
    lastSeenMs,
    dismissedAtMs,
    latestActivityMs,
    nowMs: Date.now(),
  });

  // Jump-to: case-insensitive match over real task labels; focus the first match's node.
  const handleJump = (query: string) => {
    const q = query.toLowerCase();
    const match = dashboard.tasks.find(t => t.label.toLowerCase().includes(q));
    if (match) onSelectNode(match.nodeId);
  };
  return (
    <div className={styles.viewport}>
      <DegradedBanner apiHealth={dashboard.apiHealth} />
      {digest !== null && (
        <DigestHeroCard
          digest={digest}
          visibility={visibility}
          port={digestPort}
          onDismissed={() => setDismissedAtMs(digestPort.readDismissal(dashboard.jobId))}
        />
      )}
      <div className={`${styles.shell} remedy-journey-shell`} data-ui="remedy-visual-v2">
        <LeftBrandRail dashboard={dashboard} />
        <main className={styles.main} data-testid="main-column">
          {/* The live tick composes the tile while the job runs; the terminal
              reconciliation WRAPS that output and replaces the tile with the
              ledger's own figure once the job has stopped (DECISION F022 D8). */}
          <TopMetricsBar
            metrics={metricsWithCostReconciliation(
              metricsWithCostTicker(dashboard.metrics, stream.budget),
              dashboard.budgetFinal,
              stream.budget,
              dashboard.live.running,
            )}
          />
          <CommandBar nextAction={dashboard.nextAction} onJump={handleJump} />
          <BrainGraphStage dashboard={dashboard} selectedNodeId={selectedNodeId} onSelectNode={onSelectNode} />
          <PhaseTimeline phases={dashboard.phases} timelineEvents={dashboard.timelineEvents} />
        </main>
        <RightLivePanel dashboard={dashboard} serverToken={serverToken} onSelectNode={onSelectNode} streamStatus={stream.status} recent={stream.recent} recentDropped={stream.recentDropped} />
      </div>
      {selectedNode && <DetailPopover dashboard={dashboard} selectedNode={selectedNode} selectedPromptId={selectedPromptId} onClose={() => onSelectNode(null)} onOpenDiff={setOpenDiffTaskId} />}
      {/* THE DIFF PANEL. A sibling of the popover rather than a child of
          `<main>`, which the main-column guard holds to exactly four children.
          NO CLASS ON THE WRAPPER, for the same reason `DiffView`'s own root
          carries none: `DiffView.module.css` is a transcription of the feature
          file's binding CSS and this round is not authorised to add a layout
          class to it, so the panel is a bare landmark. */}
      {openDiffTaskId !== null && (
        <section data-ui="diff-panel" aria-label="Change for this task run">
          <button type="button" onClick={() => setOpenDiffTaskId(null)}>Close diff</button>
          {diffEnvelope === null ? (
            <p>{DIFF_PENDING_TEXT}</p>
          ) : diffEnvelope.available ? (
            // THE SIDEBAR AND THE BODY APPEAR AND DISAPPEAR TOGETHER, under this
            // one `available` condition, because a file list beside a panel that
            // is saying "no diff" would offer rows to jump to that are not on the
            // screen. They are siblings rather than nested for the same reason
            // the panel wears no class: the layout that puts one beside the other
            // is the ruling this round defers.
            <>
              <DiffFileSidebar envelope={diffEnvelope} />
              <DiffView envelope={diffEnvelope} />
            </>
          ) : (
            <p>{diffEnvelope.reason === null ? DIFF_UNAVAILABLE_TEXT : `${DIFF_UNAVAILABLE_TEXT} ${diffEnvelope.reason}`}</p>
          )}
        </section>
      )}
    </div>
  );
}
