// The SIDEBAR half of F037's viewer (T5_F037 T003): the file summaries
// `../../api/diffViewModel` builds, turned into a list of controls. It DERIVES
// NOTHING, which is the same division `DiffView.tsx` states in its own header
// and holds for the same reason: WHICH files exist, in which order, with which
// counts and under which key is `buildDiffFileSummaries`' answer, computed in
// the layer `apps/ui/vitest.config.ts` reaches. A hunk count re-derived here
// would be a rule no suite in this repository can execute, and a second spelling
// of a number the model already decided.
//
// NO CLASS ON ANY ELEMENT BELOW, AND THAT IS A RULING DEFERRED RATHER THAN AN
// OVERSIGHT. `DiffView.module.css` is a transcription of the binding CSS of
// `docs/roadmap/features/T5_F037.md`, whose vocabulary amendment A5 fixes, and
// the CANONICAL DESIGN REFERENCE banner forbids inventing a visual language.
// That feature file's Design section names "paths + stats bars" for this
// sidebar, and the binding CSS defines no rule for either of them — so this
// round ships SEMANTIC MARKUP ONLY: a list, real numbers, no class. What a stats
// bar should LOOK like needs a ruling this round does not make, and inventing
// one here would be the visual language the banner forbids. The diff panel
// wrapper in `RemedyShell.tsx` and `DiffView`'s own root already take exactly
// this posture.
//
// NOTHING IN THIS REPOSITORY CAN RENDER THIS FILE — no DOM environment, and the
// shipped vitest config reaches no markup — so what gates it is
// `tests/ui_contracts/test_diff_file_sidebar.py`, which reads its
// COMMENT-STRIPPED source, and `tsc --noEmit`.
import { buildDiffFileSummaries } from "../../api/diffViewModel";
import type { DiffEnvelope } from "../../api/diffViewModel";

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
                <strong>{summary.path}</strong>
                {/* Absent far more often than present, so both render only when
                    the file really carries one — an always-present element
                    holding an empty string is a row of blank space. */}
                {summary.oldPath === null ? null : <span>{`${OLD_PATH_LABEL} ${summary.oldPath}`}</span>}
                <span>{summary.status}</span>
                <span>{`+${summary.added}`}</span>
                <span>{`-${summary.deleted}`}</span>
                <span>{`${HUNK_COUNT_LABEL}: ${summary.hunkCount}`}</span>
                {summary.note === null ? null : <span>{summary.note}</span>}
              </button>
            </li>
          ))}
        </ul>
      )}
    </nav>
  );
}
