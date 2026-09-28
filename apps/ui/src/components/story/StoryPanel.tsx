import { useCallback, useEffect, useMemo, useState } from "react";
import { createPortal } from "react-dom";
import type { RemedyDashboard } from "../../api/types";
import type { OwnershipView } from "../../api/ownership";
import type { BrainEventRow } from "../graph/brainOntology";
import { dashboardBrainSeeds } from "../graph/brainView";
import { useReducedMotion } from "../shell/ReducedMotionProvider";
import type { TimelineScrub } from "../timeline/useTimelineScrub";
import { autoplayStep } from "./storyAutoplay";
import { cardAt, chapterAt } from "./storyNarration";
import { STORY_RUNNING_LINE, storyBeatsAt, storyPlayStart, storyPositionLabel } from "./storyPlayer";
import { buildStoryView } from "./storyView";
import styles from "./StoryPanel.module.css";

/**
 * The in-app story panel (F039 T002, DECISION F039 D6): a docked glass card that narrates a
 * job's ledger through the timeline's OWN scrub — every chapter button, Previous, Next and
 * Play move `scrub.scrubTo`, the same handle `PhaseTimeline` and the graph already read, so
 * the story never carries a second position of its own to fall out of step with them.
 *
 * PORTALED to `document.body` as `TourOverlay.tsx` is, but WITHOUT a backdrop: the story is
 * told BY the graph and the phase bar underneath it, so both must stay visible while it plays
 * (DECISION F039 D6, ALTERNATIVES).
 *
 * IT OWNS EXACTLY ONE TIMER: while playing, the effect below asks `autoplayStep` for the next
 * move and schedules it, and any unmount, pause or position change cancels it — never a plan
 * of steps scheduled all at once, which a manual scrub or a pause would then have to unwind.
 */
export function StoryPanel({ dashboard, rows, ownership, scrub, onClose }: {
  dashboard: RemedyDashboard;
  rows: readonly BrainEventRow[];
  ownership: OwnershipView | null;
  scrub: TimelineScrub;
  onClose: () => void;
}) {
  const reducedMotion = useReducedMotion();
  const [playing, setPlaying] = useState(false);

  const view = useMemo(
    () => buildStoryView(dashboard.jobId, dashboardBrainSeeds(dashboard.tasks), rows, ownership, dashboard.story),
    [dashboard.jobId, dashboard.tasks, dashboard.story, rows, ownership],
  );

  const position = scrub.state.position;
  const currentIndex = chapterAt(view.chapters, position);
  const previousDisabled = currentIndex <= 0;
  const nextDisabled = currentIndex === -1 || currentIndex >= view.chapters.length - 1;
  const card = cardAt(view.chapters, view.cards, position);

  function goToChapter(startSeq: number) {
    setPlaying(false);
    scrub.scrubTo(startSeq);
  }

  const startPlaying = useCallback(() => {
    const live = scrub.state.mode === "live";
    const start = storyPlayStart(view, position, live);
    if (live || start !== position) scrub.scrubTo(start);
    setPlaying(true);
  }, [scrub, view, position]);

  const togglePlaying = useCallback(() => {
    if (playing) setPlaying(false);
    else startPlaying();
  }, [playing, startPlaying]);

  // THE ONE TIMER (see the header comment): re-armed by `position` itself, so a manual scrub
  // while playing reschedules from the new position rather than racing an old plan.
  useEffect(() => {
    if (!playing) return;
    const step = autoplayStep(view.chapters, view.seqs, position, view.pacing, reducedMotion);
    if (step === null) {
      setPlaying(false);
      return;
    }
    const id = window.setTimeout(() => scrub.scrubTo(step.position), step.delayMs);
    return () => window.clearTimeout(id);
  }, [playing, position, view, reducedMotion, scrub]);

  // Escape stops play and closes; Space toggles play unless a text field has focus, so typing
  // a space elsewhere on the page never pauses the story by accident.
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setPlaying(false);
        onClose();
        return;
      }
      if (event.key === " " || event.code === "Space") {
        const active = document.activeElement as HTMLElement | null;
        const tag = active ? active.tagName.toLowerCase() : "";
        if (tag === "input" || tag === "textarea") return;
        event.preventDefault();
        togglePlaying();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => { window.removeEventListener("keydown", onKey); };
  }, [onClose, togglePlaying]);

  return createPortal(
    <section role="region" aria-label="Story" data-ui="story-panel" className={styles.panel}>
      <header className={styles.header}>
        <h2>Story</h2>
      </header>
      <p data-ui="story-position" className={styles.position}>{storyPositionLabel(view, position)}</p>
      {dashboard.live.running && (
        <p data-ui="story-running" className={styles.running}>{STORY_RUNNING_LINE}</p>
      )}
      <ol data-ui="story-chapters" className={styles.chapters}>
        {view.chapters.map((chapter, index) => (
          <li key={`${chapter.phase}-${chapter.part}`}>
            <button
              type="button"
              className={index === currentIndex ? styles.chapterCurrent : styles.chapterButton}
              aria-current={index === currentIndex ? "step" : undefined}
              onClick={() => goToChapter(chapter.startSeq)}
            >
              {chapter.title}
            </button>
          </li>
        ))}
      </ol>
      {card !== null && (
        <div data-ui="story-card" className={styles.card}>
          {storyBeatsAt(card, position).map((beat) => (
            <p key={beat.seq} className={styles.beat}>
              <span>{beat.line}</span>
              {beat.verdict !== null && <span className={styles.beatMeta}>{beat.verdict}</span>}
              {beat.actor !== null && <span className={styles.beatMeta}>{beat.actor}</span>}
            </p>
          ))}
          {card.cost !== null && <p data-ui="story-cost" className={styles.cost}>{card.cost}</p>}
        </div>
      )}
      <div className={styles.actions}>
        <button
          type="button"
          onClick={() => goToChapter(view.chapters[currentIndex - 1]?.startSeq ?? position)}
          disabled={previousDisabled}
        >
          Previous chapter
        </button>
        <button
          type="button"
          onClick={() => goToChapter(view.chapters[currentIndex + 1]?.startSeq ?? position)}
          disabled={nextDisabled}
        >
          Next chapter
        </button>
        <button type="button" onClick={togglePlaying} disabled={scrub.state.head < 0}>
          {playing ? "Pause" : "Play"}
        </button>
        <button type="button" onClick={onClose}>Close story</button>
      </div>
    </section>,
    document.body,
  );
}
