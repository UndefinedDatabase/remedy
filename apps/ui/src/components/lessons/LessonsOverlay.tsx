import { useEffect, useState } from "react";
import type { LessonRow, LessonsIndex } from "../../api/lessons";
import {
  LESSON_STATUS_READY,
  currentLessonIndex,
  lessonIndexTag,
  lessonNeighbours,
  lessonProvenanceLine,
  lessonStatusLine,
  lessonsEmptyLine,
} from "../../api/lessons";
import { loadLessonsIndex } from "../../api/remedyApi";
import styles from "./LessonsOverlay.module.css";

/** What the overlay says while the index is in flight. */
const LESSONS_PENDING_TEXT = "Reading this job's lessons…";
/** What it says when the read failed or the envelope could not be decoded. */
const LESSONS_UNREADABLE_TEXT = "This job's lessons could not be read.";

/**
 * The learning overlay (T5_F265 T002, DECISION F265 D3): the index of the job's lessons on the
 * left, the chosen lesson on the right, and previous and next beneath it. It READS stored
 * lessons and generates nothing; every rule it applies lives in `api/lessons.ts`.
 *
 * `refreshKey` is the newest stream position that announced a stored lesson, so the index is
 * read again when the stream says there is something new, never on a timer.
 */
export function LessonsOverlay({ jobId, serverToken, refreshKey, onClose }: {
  jobId: string; serverToken: string; refreshKey: number; onClose: () => void;
}) {
  // `null` until the first answer; after it, the index or `null` for "could not be read".
  const [read, setRead] = useState<{ index: LessonsIndex | null } | null>(null);
  const [chosen, setChosen] = useState<number | null>(null);

  // THE READ. `cancelled` answers a response that arrives after the job, the token or the
  // refresh key moved on, exactly as the diff panel's read does: a slow answer to an older
  // question is dropped instead of painted over a newer one.
  useEffect(() => {
    let cancelled = false;
    void loadLessonsIndex({ jobId, token: serverToken }).then((index) => {
      if (!cancelled) setRead({ index });
    });
    return () => { cancelled = true; };
  }, [jobId, serverToken, refreshKey]);

  // Esc closes the overlay, as the reference's sheets and popovers do.
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => { window.removeEventListener("keydown", onKey); };
  }, [onClose]);

  return (
    <section className={styles.overlay} role="dialog" aria-label="Lessons" data-ui="lessons-overlay">
      <header className={styles.header}>
        <h2>Lessons</h2>
        <button type="button" className={styles.close} onClick={onClose}>Close lessons</button>
      </header>
      {read === null ? (
        <p className={styles.quiet}>{LESSONS_PENDING_TEXT}</p>
      ) : read.index === null ? (
        <p className={styles.quiet}>{LESSONS_UNREADABLE_TEXT}</p>
      ) : (
        <LessonsBody index={read.index} chosen={chosen} onChoose={setChosen} />
      )}
    </section>
  );
}

function LessonsBody({ index, chosen, onChoose }: {
  index: LessonsIndex; chosen: number | null; onChoose: (at: number) => void;
}) {
  const empty = lessonsEmptyLine(index);
  const rows = index.rows;
  if (rows.length === 0) return <p className={styles.quiet}>{empty}</p>;
  const current = currentLessonIndex(rows, chosen);
  const row = rows[current];
  const { previous, next } = lessonNeighbours(rows.length, current);
  return (
    <div className={styles.body}>
      <nav className={styles.index} aria-label="Lesson index">
        <ol>
          {rows.map((entry, at) => (
            <li key={`${entry.taskId}-${at}`}>
              <button
                type="button"
                className={at === current ? styles.entryOn : styles.entry}
                aria-current={at === current ? "true" : undefined}
                onClick={() => onChoose(at)}
              >
                <span className={styles.entryTitle}>{entry.title || entry.taskId}</span>
                <span className={styles.entryTag}>{lessonIndexTag(entry)}</span>
              </button>
            </li>
          ))}
        </ol>
      </nav>
      <article className={styles.lesson} aria-label={row.title || row.taskId}>
        {empty !== null && <p className={styles.quiet}>{empty}</p>}
        <h3>{row.title || row.taskId}</h3>
        {row.status === LESSON_STATUS_READY
          ? <LessonText row={row} />
          : <p className={styles.quiet}>{lessonStatusLine(row)}</p>}
        <footer className={styles.pager}>
          <button type="button" disabled={previous === null} title={previous === null ? "This is the first lesson." : undefined}
            onClick={() => { if (previous !== null) onChoose(previous); }}>Previous</button>
          <span>{current + 1} of {rows.length}</span>
          <button type="button" disabled={next === null} title={next === null ? "This is the last lesson." : undefined}
            onClick={() => { if (next !== null) onChoose(next); }}>Next</button>
        </footer>
      </article>
    </div>
  );
}

function LessonText({ row }: { row: LessonRow }) {
  return (
    <>
      <p className={styles.summary}>{row.summary}</p>
      {row.constructs.length > 0 && (
        <dl className={styles.constructs}>
          {row.constructs.map((construct, at) => (
            <div key={`${construct.name}-${at}`} className={styles.construct}>
              <dt><code>{construct.name}</code></dt>
              <dd>{construct.what}</dd>
              <dd><strong>Why here:</strong> {construct.whyHere}</dd>
              <dd><strong>Judgement:</strong> {construct.judgement}</dd>
            </div>
          ))}
        </dl>
      )}
      <p className={styles.quiet}>{lessonProvenanceLine(row)}</p>
    </>
  );
}
