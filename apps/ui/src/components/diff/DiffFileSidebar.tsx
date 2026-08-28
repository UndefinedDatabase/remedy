// The SIDEBAR half of F037's viewer (T5_F037 T003): the file summaries
// `../../api/diffViewModel` builds, turned into a list of controls. It DERIVES
// NOTHING, which is the same division `DiffView.tsx` states in its own header
// and holds for the same reason: WHICH files exist, in which order, with which
// counts and under which key is `buildDiffFileSummaries`' answer, computed in
// the layer `apps/ui/vitest.config.ts` reaches. A hunk count re-derived here
// would be a rule no suite in this repository can execute, and a second spelling
// of a number the model already decided.
//
// THE VISUAL TREATMENT OF THIS SURFACE IS RULED BY DECISION F256 D3, and the
// deferral this header carried from F037 until F256 R5 is discharged rather than
// renewed. D3 DERIVES the treatment from the diff body's own vocabulary instead
// of inventing one, which is what keeps it inside what the CANONICAL DESIGN
// REFERENCE banner allows: the path takes `DiffView.module.css`'s mono family
// with ligatures off, the added and removed counts take the same green and
// orange the diff rows are tinted with, and every other piece of metadata takes
// the same de-emphasis that sheet already gives the line-number gutter. No new
// hue and no new custom property enter the stylesheet.
//
// REMEDY DELIBERATELY DOES NOT DRAW A PROPORTIONAL STATS BAR HERE, and this is
// where a reader searching for one will look, because text search cannot find
// code that does not exist. The Design section of
// `docs/roadmap/features/T5_F037.md` names "paths + stats bars" and D3 reads
// that as satisfied by the two counts themselves: they carry the magnitude
// exactly rather than approximately, while a bar is a visual primitive no
// authority in this repository defines — it would need a track, a fill, a
// minimum width for a one-line change and a rule for a pure deletion, and
// inventing all four is what the banner forbids.
//
// NOTHING IN THIS REPOSITORY CAN RENDER THIS FILE — no DOM environment, and the
// shipped vitest config reaches no markup — so what gates it is
// `tests/ui_contracts/test_diff_file_sidebar.py`, which reads its
// COMMENT-STRIPPED source, and `tsc --noEmit`.
import { buildDiffFileSummaries } from "../../api/diffViewModel";
import type { DiffEnvelope } from "../../api/diffViewModel";
import styles from "./DiffView.module.css";

/** What the sidebar says INSTEAD of an empty container. An envelope with no
 *  files is a real answer — an empty diff, or a ceiling that admitted none of
 *  them — and an empty `<ul>` renders as a sidebar that failed rather than as a
 *  diff that has nothing in it. */
const DIFF_NO_FILES_TEXT = "This diff lists no files.";

/** The label before a rename's previous name. A renamed file's new path is often
 *  nothing the reader recognises, and the old one is their only way back to the
 *  file they know. */
const OLD_PATH_LABEL = "was";

/** The label before a file's hunk count. The colon form is used for the reason
 *  `DiffView.tsx` uses it: it stays grammatical at every count, so no plural
 *  branch is written into markup no rendering test in this repository reaches. */
const HUNK_COUNT_LABEL = "Hunks";

export interface DiffFileSidebarProps {
  /** The SAME already-read envelope `DiffView` draws, and for the same reason:
   *  `readDiffEnvelope` is the single door a payload comes through, so every
   *  field below is a value that door already made total and this component is
   *  never the second place a malformed payload is handled. */
  envelope: DiffEnvelope;
}

export function DiffFileSidebar({ envelope }: DiffFileSidebarProps) {
  // ONE WALK, and the list is the model's own — same order, same counts, same
  // keys. `buildDiffFileSummaries` has been exported since the round that built
  // the model precisely so this component could draw it without deciding
  // anything.
  const summaries = buildDiffFileSummaries(envelope);

  // MOVING THE READER IS A DOM LOOKUP, AND THE STRING IT LOOKS UP IS THE MODEL'S.
  // `rowKey` here and `id` on the file row in `DiffView.tsx` are the SAME string
  // from the SAME builder, which is why the two halves agree without either of
  // them recomputing it. Navigating by a path would be a second identity for the
  // same file — and two files can share neither key nor id, but a path is the
  // model's DATA rather than its address. A row that is not on screen yet
  // resolves to null and the click is simply inert; that is the honest answer,
  // not an error.
  const goToFileRow = (rowKey: string) => {
    document.getElementById(rowKey)?.scrollIntoView({ block: "start" });
  };

  return (
    <nav data-ui="diff-file-sidebar" aria-label="Files in this diff">
      {summaries.length === 0 ? (
        <p>{DIFF_NO_FILES_TEXT}</p>
      ) : (
        <ul>
          {summaries.map((summary) => (
            // KEYED ON THE MODEL'S `rowKey` AND NEVER ON A PATH OR AN INDEX THIS
            // FILE COUNTS: an index would re-derive the very thing the model
            // handed over, and a path is data the parser read out of the diff.
            <li key={summary.rowKey}>
              <button type="button" onClick={() => goToFileRow(summary.rowKey)}>
                <strong className={styles.filePath}>{summary.path}</strong>
                {/* Absent far more often than present, so both render only when
                    the file really carries one — an always-present element
                    holding an empty string is a row of blank space. */}
                {summary.oldPath === null ? null : <span className={styles.fileMeta}>{`${OLD_PATH_LABEL} ${summary.oldPath}`}</span>}
                <span className={styles.fileMeta}>{summary.status}</span>
                <span className={styles.statAdd}>{`+${summary.added}`}</span>
                <span className={styles.statDel}>{`-${summary.deleted}`}</span>
                <span className={styles.fileMeta}>{`${HUNK_COUNT_LABEL}: ${summary.hunkCount}`}</span>
                {summary.note === null ? null : <span className={styles.fileMeta}>{summary.note}</span>}
              </button>
            </li>
          ))}
        </ul>
      )}
    </nav>
  );
}
