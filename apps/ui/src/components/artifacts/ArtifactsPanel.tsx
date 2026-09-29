import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import type { ArtifactsView } from "../../api/artifactPreview";
import {
  ARTIFACTS_LOADING_LINE,
  ARTIFACTS_UNREADABLE_LINE,
  CAPTURES_ABSENT_LINE,
  README_ABSENT_LINE,
  README_TRUNCATED_LINE,
  README_UNREADABLE_LINE,
  artifactFilePath,
  captureCaption,
  readmeCockpitHtml,
} from "../../api/artifactPreview";
import { loadArtifactsView } from "../../api/remedyApi";
import { AppPreviewCard } from "./AppPreviewCard";
import { ArtifactLightbox } from "./ArtifactLightbox";
import styles from "./ArtifactsPanel.module.css";

/**
 * The job's results panel (F041 T003, DECISION F041 D5): the app preview card, the job's
 * README as the server's own sanitized fragment, and a grid of its screenshots that open in a
 * lightbox. Opened from `RightLivePanel.tsx`'s "Results" button and mounted by
 * `RemedyShell.tsx` as a sibling outside `<main>`, the same place the tour and the story mount.
 *
 * PORTALED TO `document.body`, for the reason `TourOverlay.tsx`'s own comment records.
 *
 * THE ONE `dangerouslySetInnerHTML` OF `apps/ui/src`: the README's html already comes back
 * sanitized by the server (`artifact_markdown.render_markdown`) and rewritten for this cockpit
 * by `readmeCockpitHtml`, which is the one function in this codebase allowed to hand a string of
 * markup to React rather than to a text node.
 */
export function ArtifactsPanel({ jobId, serverToken, onClose }: {
  jobId: string;
  serverToken: string;
  onClose: () => void;
}) {
  const [view, setView] = useState<ArtifactsView | null | undefined>(undefined);
  const [lightboxIndex, setLightboxIndex] = useState<number | null>(null);
  const request = { jobId, token: serverToken };

  useEffect(() => {
    let cancelled = false;
    void loadArtifactsView({ jobId, token: serverToken }).then((answer) => {
      if (!cancelled) setView(answer);
    });
    return () => { cancelled = true; };
  }, [jobId, serverToken]);

  // Escape closes the panel only while no lightbox is open — a lightbox open on top of it takes
  // Escape for itself first.
  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.key === "Escape" && lightboxIndex === null) {
        onClose();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => { window.removeEventListener("keydown", onKey); };
  }, [lightboxIndex, onClose]);

  const images = view?.images ?? [];

  return createPortal(
    <section role="region" aria-label="Results" data-ui="artifacts-panel" className={styles.panel}>
      <header className={styles.header}>
        <h2>Results</h2>
        <button type="button" onClick={onClose}>Close results</button>
      </header>
      <AppPreviewCard jobId={jobId} serverToken={serverToken} />
      {view === undefined && <p className={styles.quiet}>{ARTIFACTS_LOADING_LINE}</p>}
      {view === null && <p className={styles.quiet}>{ARTIFACTS_UNREADABLE_LINE}</p>}
      {view !== undefined && view !== null && (
        <>
          <h3 className={styles.sectionHeading}>README</h3>
          {view.error !== "" ? (
            <p className={styles.quiet}>{README_UNREADABLE_LINE}</p>
          ) : view.readme === null ? (
            <p className={styles.quiet}>{README_ABSENT_LINE}</p>
          ) : (
            <>
              <article
                data-ui="artifacts-readme"
                className={styles.readme}
                dangerouslySetInnerHTML={{
                  __html: readmeCockpitHtml(view.readme.html, view.images, request),
                }}
              />
              {view.readme.truncated && (
                <>
                  <p className={styles.quiet}>{README_TRUNCATED_LINE}</p>
                  <a
                    data-ui="artifacts-readme-full"
                    className={styles.link}
                    href={artifactFilePath(request, view.readme.root, view.readme.path)}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Open the full README
                  </a>
                </>
              )}
            </>
          )}
          <h3 className={styles.sectionHeading}>Screenshots</h3>
          {images.length === 0 ? (
            <p className={styles.quiet}>{CAPTURES_ABSENT_LINE}</p>
          ) : (
            <ul data-ui="artifacts-captures" className={styles.captures}>
              {images.map((image, index) => {
                const caption = captureCaption(image.path);
                return (
                  <li key={image.path}>
                    <button
                      type="button"
                      aria-label={`Open screenshot ${caption}`}
                      onClick={() => setLightboxIndex(index)}
                    >
                      <img
                        src={artifactFilePath(request, "evidence", image.path)}
                        alt=""
                        loading="lazy"
                      />
                    </button>
                    <span className={styles.captureLabel}>{caption}</span>
                  </li>
                );
              })}
            </ul>
          )}
        </>
      )}
      {lightboxIndex !== null && (
        <ArtifactLightbox
          images={images}
          index={lightboxIndex}
          request={request}
          onIndex={setLightboxIndex}
          onClose={() => setLightboxIndex(null)}
        />
      )}
    </section>,
    document.body,
  );
}
