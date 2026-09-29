import { useEffect, useRef } from "react";
import { createPortal } from "react-dom";
import type { ArtifactRequest, ImageArtifact } from "../../api/artifactPreview";
import { artifactFilePath, captureCaption, lightboxIndexAfter } from "../../api/artifactPreview";
import styles from "./ArtifactLightbox.module.css";

/**
 * The screenshot lightbox (F041 T003, DECISION F041 D5): one picture at a time, addressed
 * through the file route the panel already carries a token for, stepped by the arrow keys or
 * Previous/Next, closed by Escape, a click on the backdrop, or Close.
 *
 * PORTALED TO `document.body`, for the reason `TourOverlay.tsx`'s own comment records: an
 * ancestor's `backdrop-filter` confines a `position: fixed` descendant to its own box.
 */
export function ArtifactLightbox({ images, index, request, onIndex, onClose }: {
  images: readonly ImageArtifact[];
  index: number;
  request: ArtifactRequest;
  onIndex: (index: number) => void;
  onClose: () => void;
}) {
  const closeRef = useRef<HTMLButtonElement>(null);

  // Close takes focus on mount, so a keyboard user lands on the one control that always works.
  useEffect(() => {
    closeRef.current?.focus();
  }, []);

  // Escape closes; the arrow keys step, mirroring lightboxIndexAfter's own two ends.
  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      if (event.key === "Escape") {
        onClose();
        return;
      }
      if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
        event.preventDefault();
        onIndex(lightboxIndexAfter(index, images.length, event.key));
      }
    }
    window.addEventListener("keydown", onKey);
    return () => { window.removeEventListener("keydown", onKey); };
  }, [index, images.length, onIndex, onClose]);

  const image = images[index];
  const caption = captureCaption(image.path);

  return createPortal(
    <>
      <div data-ui="artifact-lightbox-backdrop" className={styles.backdrop} onClick={onClose} />
      <section
        role="dialog"
        aria-modal="true"
        aria-label="Screenshot"
        data-ui="artifact-lightbox"
        className={styles.card}
      >
        <img
          className={styles.picture}
          src={artifactFilePath(request, "evidence", image.path)}
          alt={caption}
        />
        <p data-ui="artifact-lightbox-caption" className={styles.caption}>
          {`${index + 1} of ${images.length} · ${caption}`}
        </p>
        <div className={styles.actions}>
          <button
            type="button"
            onClick={() => onIndex(lightboxIndexAfter(index, images.length, "ArrowLeft"))}
            disabled={index === 0}
          >
            Previous
          </button>
          <button
            type="button"
            onClick={() => onIndex(lightboxIndexAfter(index, images.length, "ArrowRight"))}
            disabled={index === images.length - 1}
          >
            Next
          </button>
          <button type="button" ref={closeRef} onClick={onClose}>Close</button>
        </div>
      </section>
    </>,
    document.body,
  );
}
