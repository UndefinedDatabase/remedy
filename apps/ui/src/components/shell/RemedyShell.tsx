import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type { RemedyDashboard } from "../../api/types";
import type { DiffEnvelope } from "../../api/diffViewModel";
import { buildDiffFileSummaries } from "../../api/diffViewModel";
import type { JobDigest } from "../../api/jobDigest";
import type { TourAnchor } from "../../api/resultTour";
import { tourDiffRowKey } from "../../api/resultTour";
import { loadDiffEnvelope, loadJobDigest, loadOwnershipView } from "../../api/remedyApi";
import type { OwnershipView } from "../../api/ownership";
import { ownershipRefreshKey } from "../../api/ownership";
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
import { ChatSheet } from "../command/ChatSheet";
import { jumpTargetsOf } from "../../api/paletteJump";
import { paletteCommandFactsOf, paletteCommandReasons } from "../../api/paletteCommandState";
import { AddTaskSheet } from "../panels/AddTaskSheet";
import { useProjectContext } from "./ProjectProvider";
import { BrainGraphStage } from "../graph/BrainGraphStage";
import { shellSelectionIdOf } from "../graph/brainView";
import type { EvidenceTab } from "../graph/semanticZoom";
import { brainLedgerPrefix } from "../graph/brainLedger";
import { useBrainLedger } from "../graph/useBrainLedger";
import { RightLivePanel } from "../panels/RightLivePanel";
import { steeringFocusTaskId } from "../../api/steeringNote";
import { PhaseTimeline } from "../timeline/PhaseTimeline";
import { useTimelineScrub } from "../timeline/useTimelineScrub";
import { DetailPopover } from "../detail/DetailPopover";
import { LessonsOverlay } from "../lessons/LessonsOverlay";
import { lessonsRefreshKey } from "../../api/lessons";
import { TourOverlay } from "../tour/TourOverlay";
import { StoryPanel } from "../story/StoryPanel";
import { ArtifactsPanel } from "../artifacts/ArtifactsPanel";
import { TermPanel } from "../term/TermPanel";
import { FirstRunTourMount } from "../tour/FirstRunTour";
import { keymapAction } from "../../api/keymap";
import { KeymapOverlay } from "../command/KeymapOverlay";
import { useHeldHelpKey } from "./useHeldHelpKey";
import { DegradedBanner } from "./DegradedBanner";
import styles from "./RemedyShell.module.css";
import { browserBrainStreamEnv, createBrainStreamHostDeps, eventsSincePath } from "../../api/brainStreamDeps";
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
  // The graph's ledger reader shares the same real environment and the same
  // path builder the stream above uses, built once so the callback handed to
  // the stage stays referentially stable across a render the stream itself
  // did not cause (DECISION F019 D5).
  const brainStreamEnv = useMemo(() => browserBrainStreamEnv(window), []);
  const readEventsPage = useCallback(
    (cursor: number) => brainStreamEnv.fetchJson(eventsSincePath(dashboard.jobId, cursor)),
    [brainStreamEnv, dashboard.jobId],
  );
  // ONE ledger per job, read here so the graph and the timeline fold the same
  // complete, contiguous prefix (DECISIONS F019 D5 and F024 D4), and the
  // timeline's scrubber, whose position the graph draws while it is scrubbed.
  const ledger = useBrainLedger(dashboard.jobId, stream.recent, readEventsPage);
  const ledgerRows = useMemo(() => brainLedgerPrefix(ledger), [ledger]);
  const scrub = useTimelineScrub(dashboard.jobId, dashboard.tasks, ledgerRows);
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
  // F030 T003: the steering input addresses whichever task the graph selection
  // names — a prompt already resolved to its owning task above — and the whole
  // job when the selection names none.
  const focusedTaskId = steeringFocusTaskId(dashboard.tasks, selectedNode ? selectedNode.nodeId : null);
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

  // THE OWNERSHIP LOAD (F035 T003, DECISION F035 D5): who did what, read once per job and
  // token, again when the stream shows a frame of an event the ledger reads
  // (`ownershipRefreshKey`), and again when the selected task changes — the detail's "Who did
  // what" section reads only the entries `ownershipEntriesForTask` picks for that task, so a
  // newly selected task must not go on showing the previous one's history. `DetailPopover`
  // itself never fetches; this is the one load the popover is handed.
  const [ownership, setOwnership] = useState<OwnershipView | null>(null);
  const ownershipKey = ownershipRefreshKey(stream.recent ?? []);
  useEffect(() => {
    let cancelled = false;
    void loadOwnershipView({ jobId: dashboard.jobId, token: serverToken }).then((loaded) => {
      if (!cancelled) setOwnership(loaded);
    });
    return () => { cancelled = true; };
  }, [dashboard.jobId, serverToken, ownershipKey, focusedTaskId]);

  // THE STORAGE EDGE, BOUND HERE because this is the edge: `digestVisibility.ts`
  // DECLARES `DigestVisibilityPort` and implements nothing, exactly as
  // `browserBrainStreamEnv(window)` above binds the stream's own globals at
  // this same mount. `window.localStorage` occurs nowhere else in this file.
  // Built ONCE per mount (R-0622's first real lint finding): a port rebuilt every
  // render would have to stay out of the effect's dependencies below, or rewrite
  // "last seen" on every render.
  const digestPort = useMemo(() => browserDigestVisibilityPort(window.localStorage), []);

  // Read once, before the write below ever runs, so the digest visibility
  // rule sees the instant the operator was last here rather than the one
  // this very mount is about to record.
  const [lastSeenMs] = useState<number | null>(() => digestPort.readLastSeen(dashboard.jobId));
  useEffect(() => {
    digestPort.writeLastSeen(dashboard.jobId, Date.now());
  }, [digestPort, dashboard.jobId]);

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

  // THE LEARNING OVERLAY (T5_F265 T002, DECISION F265 D3): open or closed, and the newest
  // stream position that announced a stored lesson, which is what makes an open overlay read
  // its index again. No timer: the stream is the only trigger.
  const [lessonsOpen, setLessonsOpen] = useState(false);
  const lessonsKey = lessonsRefreshKey(stream.recent ?? []);

  // THE GUIDED TOUR (F036 T003, DECISION F036 D6): open or closed, and the diff path a "Show
  // me" on a diff stop asked to be scrolled into view once the job's whole diff has loaded.
  const [tourOpen, setTourOpen] = useState(false);
  const [tourDiffPath, setTourDiffPath] = useState<string | null>(null);

  // THE STORY (F039 T002, DECISION F039 D6): open or closed; the panel reads the ledger, the
  // ownership view and the timeline's own scrub this shell already owns, and drives that same
  // scrub rather than keeping a position of its own.
  const [storyOpen, setStoryOpen] = useState(false);

  // THE RESULTS PANEL (F041 T003, DECISION F041 D5): open or closed; the panel reads the
  // job's README and screenshots and the app preview through its own doors, so it carries no
  // state this shell needs to own beyond whether it is open.
  const [resultsOpen, setResultsOpen] = useState(false);

  // THE '?' PANEL (F043 T003, DECISION F043 D3): open or closed.
  const [termsOpen, setTermsOpen] = useState(false);
  // THE FIRST-RUN TOUR'S RELAUNCH (DECISION F043 D4): the count the Terms panel's "Take the
  // tour" raises, the only fact the tour's own mount needs from this shell.
  const [tourRelaunch, setTourRelaunch] = useState(0);
  // THE PROJECT CONTEXT, read here rather than beside the palette's own inputs further down:
  // the one window key listener directly below needs `goHome` for its "go-projects" action.
  const projectContext = useProjectContext();
  const { goHome } = projectContext;
  // T5_F044 T002, DECISION F044 D5: THE ONE WINDOW KEY LISTENER. Every key press this shell
  // reacts to is read through the keymap, never through a rule of this file's own.
  // `barFocusRequest` is raised once per press the keymap answers "open-bar" for; `pendingG`
  // holds the "g" wait a "g then p" chord needs across presses.
  const [barFocusRequest, setBarFocusRequest] = useState(0);
  const pendingG = useRef(false);
  // DECISION F044 D6: the held "?" shows the keymap's own overlay; a quick press still opens the
  // terms panel, exactly as before.
  const { shortcutsOpen, press: pressHelp } = useHeldHelpKey(() => setTermsOpen(true));
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      const target = event.target instanceof HTMLElement ? event.target : null;
      const dialogOpen = document.querySelector('[role="dialog"]') !== null;
      const result = keymapAction(event, target, pendingG.current, dialogOpen);
      pendingG.current = result.pendingG;
      if (result.action === "open-terms") {
        event.preventDefault();
        pressHelp(event.repeat);
      } else if (result.action === "open-bar") {
        event.preventDefault();
        setBarFocusRequest((count) => count + 1);
      } else if (result.action === "go-projects") {
        event.preventDefault();
        goHome();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => { window.removeEventListener("keydown", onKey); };
  }, [goHome, pressHelp]);

  // THE SCROLL. A diff stop's "Show me" opens the job's whole diff (below) and records the
  // path it named; once that diff's envelope has arrived, this effect finds the path's row key
  // through the SAME model `DiffFileSidebar.tsx` uses and scrolls to the SAME id that row
  // carries, then clears the path so a later envelope (a different task's diff, reopened) does
  // not scroll again.
  useEffect(() => {
    if (diffEnvelope === null || tourDiffPath === null) return;
    const rowKey = tourDiffRowKey(buildDiffFileSummaries(diffEnvelope), tourDiffPath);
    if (rowKey !== null) {
      document.getElementById(rowKey)?.scrollIntoView({ block: "start" });
    }
    setTourDiffPath(null);
  }, [diffEnvelope, tourDiffPath]);

  // "Show me": a task stop opens the task's detail through the same selection path the graph
  // and the popover already use; a diff stop opens the job's WHOLE diff (an empty task id) and
  // names the path the scroll effect above resolves once it has loaded.
  function handleTourShowAnchor(anchor: TourAnchor) {
    if (anchor.kind === "node") {
      onSelectNode(shellSelectionIdOf(dashboard.tasks, anchor.ref));
    } else if (anchor.kind === "diff") {
      setTourDiffPath(anchor.ref);
      setOpenDiffTaskId("");
    } else if (anchor.kind === "preview") {
      // DECISION F041 D6: a preview stop's "Show me" opens the Results panel, where the app
      // card lives, the same way a diff stop opens the job's whole diff.
      setResultsOpen(true);
    }
  }

  // THE PALETTE'S OWN INPUTS (T5_F044 T001, DECISIONS F044 D2 and D3): its jump targets, one per
  // task of the dashboard, ranked by the palette's fuzzy rule; and the project context's own list
  // restated as the palette's `{ slug, name }` shape — none while the context has not loaded a
  // view yet.
  const jumpTargets = useMemo(() => jumpTargetsOf(dashboard), [dashboard]);
  const paletteProjects = useMemo(
    () => (projectContext.view ? projectContext.view.projects.map((p) => ({ slug: p.slug, name: p.name })) : []),
    [projectContext.view],
  );

  // DECISION F044 D3: every command's own refusal reason, by command id, read once per dashboard
  // and token — `paletteCommandFactsOf` reads the job's stage, pause action and open decisions.
  const commandReasons = useMemo(
    () => paletteCommandReasons(paletteCommandFactsOf(dashboard, serverToken)),
    [dashboard, serverToken],
  );
  // THE ADD-TASK SHEET'S OWN OPEN STATE (DECISION F044 D3 (5)): the palette's "Add a task to the
  // plan" command opens it here, beside the tasks card's own state, which this shell does not
  // otherwise reach into.
  const [addTaskOpen, setAddTaskOpen] = useState(false);

  // THE CHAT SHEET'S OWN ASK (DECISION F044 D4 (2)): `null` while closed; otherwise the text the
  // bar's Ask row handed it and a key one higher than the last, so a repeated question still
  // mounts a fresh sheet that asks it.
  const [chatAsk, setChatAsk] = useState<{ key: number; text: string } | null>(null);

  // DECISION F044 D4 (4): the chat sheet's own evidence-item handler. A diff item opens the
  // diff panel at the chat's own scope, exactly as the detail popover's does; a prompt item
  // opens the focused task's detail, and opens nothing at the whole project's scope, where no
  // task is named for it to open.
  function handleChatEvidenceTab(tab: EvidenceTab) {
    if (tab === "diff") {
      setOpenDiffTaskId(focusedTaskId);
    } else if (tab === "prompt" && focusedTaskId !== "") {
      onSelectNode(shellSelectionIdOf(dashboard.tasks, focusedTaskId));
    }
  }

  // DECISION F044 D3 (5): where a completed command's own surface opens. "add-task-sheet" and
  // "task-edit-form" are surfaces this shell already owns a way to open; every other surface is a
  // card already on the page, found by its own `data-ui` marker, scrolled into view and focused.
  function handleOpenSurface(surface: string, taskNodeId: string) {
    if (surface === "add-task-sheet") {
      setAddTaskOpen(true);
      return;
    }
    if (surface === "task-edit-form") {
      onSelectNode(taskNodeId);
      return;
    }
    const element = document.querySelector(`[data-ui="${surface}"]`);
    if (element instanceof HTMLElement) {
      element.scrollIntoView({ block: "center" });
      element.querySelector<HTMLElement>("button, input, textarea, select")?.focus();
    }
  }

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
          <CommandBar
            nextAction={dashboard.nextAction}
            targets={jumpTargets}
            projects={paletteProjects}
            activeSlug={projectContext.active?.slug ?? ""}
            jobId={dashboard.jobId}
            serverToken={serverToken}
            commandReasons={commandReasons}
            focusedTaskId={focusedTaskId}
            onJump={onSelectNode}
            onSwitchProject={projectContext.switchTo}
            onOpenTerms={() => setTermsOpen(true)}
            onStartTour={() => setTourRelaunch((count) => count + 1)}
            onOpenSurface={handleOpenSurface}
            onAskChat={(text) => setChatAsk((previous) => ({ key: (previous?.key ?? 0) + 1, text }))}
            focusRequest={barFocusRequest}
          />
          <BrainGraphStage dashboard={dashboard} selectedNodeId={selectedNodeId} onSelectNode={onSelectNode} rows={ledgerRows} scrub={scrub} serverToken={serverToken} />
          <PhaseTimeline scrub={scrub} />
        </main>
        <RightLivePanel dashboard={dashboard} serverToken={serverToken} onSelectNode={onSelectNode} streamStatus={stream.status} replay={scrub.state.mode === "scrubbed"} recent={stream.recent} recentDropped={stream.recentDropped} onOpenLessons={() => setLessonsOpen(true)} onOpenTour={() => setTourOpen(true)} onOpenStory={() => setStoryOpen(true)} onOpenResults={() => setResultsOpen(true)} onOpenTerms={() => setTermsOpen(true)} focusedTaskId={focusedTaskId} />
      </div>
      {selectedNode && <DetailPopover dashboard={dashboard} selectedNode={selectedNode} selectedPromptId={selectedPromptId} onClose={() => onSelectNode(null)} onOpenDiff={setOpenDiffTaskId} serverToken={serverToken} onSelectTask={(taskId) => onSelectNode(shellSelectionIdOf(dashboard.tasks, taskId))} ownership={ownership} />}
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
      {/* THE ADD-TASK SHEET (DECISION F044 D3 (5)), mounted here as well as by the tasks card's
          own state, so the palette's "Add a task to the plan" command can open it too. */}
      {addTaskOpen && (
        <AddTaskSheet target={{ jobId: dashboard.jobId, serverToken }} tasks={dashboard.tasks}
          onClose={() => setAddTaskOpen(false)} />
      )}
      {/* THE CHAT SHEET (DECISION F044 D4 (2)), mounted directly after the add-task sheet for
          the same reason it is a sibling outside <main>. */}
      {chatAsk !== null && (
        <ChatSheet key={chatAsk.key} jobId={dashboard.jobId} serverToken={serverToken}
          taskId={focusedTaskId} question={chatAsk.text} onClose={() => setChatAsk(null)}
          onOpenTab={handleChatEvidenceTab} />
      )}
      {/* THE KEYMAP OVERLAY (DECISION F044 D6), a sibling directly after the chat sheet for the
          reason every overlay above is a sibling outside <main>. */}
      {shortcutsOpen && <KeymapOverlay />}
      {/* THE LEARNING OVERLAY, a sibling outside <main> for the reason the diff panel is. */}
      {lessonsOpen && (
        <LessonsOverlay
          jobId={dashboard.jobId}
          serverToken={serverToken}
          refreshKey={lessonsKey}
          onClose={() => setLessonsOpen(false)}
        />
      )}
      {/* THE GUIDED TOUR (F036 T003, DECISION F036 D6), a sibling directly after the learning
          overlay for the reason both are siblings outside <main>. */}
      {tourOpen && (
        <TourOverlay
          jobId={dashboard.jobId}
          serverToken={serverToken}
          onClose={() => setTourOpen(false)}
          onShowAnchor={handleTourShowAnchor}
        />
      )}
      {/* THE STORY (F039 T002, DECISION F039 D6), a sibling directly after the guided tour for
          the reason both are siblings outside <main>. */}
      {storyOpen && (<StoryPanel dashboard={dashboard} rows={ledgerRows} ownership={ownership} scrub={scrub} onClose={() => setStoryOpen(false)} />)}
      {/* THE RESULTS PANEL (F041 T003, DECISION F041 D5), a sibling directly after the story for
          the reason both are siblings outside <main>. */}
      {resultsOpen && (<ArtifactsPanel jobId={dashboard.jobId} serverToken={serverToken} onClose={() => setResultsOpen(false)} />)}
      {/* THE '?' PANEL (DECISION F043 D3), a sibling directly after the results panel for the
          reason every overlay above is a sibling outside <main>. */}
      {termsOpen && (<TermPanel onClose={() => setTermsOpen(false)} onStartTour={() => { setTermsOpen(false); setTourRelaunch((count) => count + 1); }} />)}
      {/* THE FIRST-RUN TOUR (F043 T003, DECISION F043 D4), a sibling directly after the '?'
          panel for the reason every overlay above is a sibling outside <main>. */}
      <FirstRunTourMount relaunch={tourRelaunch} />
    </div>
  );
}
