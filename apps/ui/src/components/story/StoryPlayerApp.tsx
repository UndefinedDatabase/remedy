import { useTimelineScrub } from "../timeline/useTimelineScrub";
import { PhaseTimeline } from "../timeline/PhaseTimeline";
import type { StoryExport } from "./storyExport";
import { StoryPanel } from "./StoryPanel";
import styles from "./StoryPlayerApp.module.css";

/**
 * The exported page's whole app (F039 T003, DECISION F039 D8). Remedy deliberately exports
 * only this subset, not the cockpit: the phase bar and the story panel over one
 * `useTimelineScrub`, with no heading and no Close button — there is nothing here to close.
 */
export function StoryPlayerApp({ story }: { story: StoryExport }) {
  const scrub = useTimelineScrub(story.dashboard.jobId, story.dashboard.tasks, story.rows);
  return (
    <main data-ui="story-player" className={styles.page}>
      <PhaseTimeline scrub={scrub} />
      <StoryPanel dashboard={story.dashboard} rows={story.rows} ownership={story.ownership} scrub={scrub} />
    </main>
  );
}
