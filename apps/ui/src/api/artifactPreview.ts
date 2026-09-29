// F041 T003's PURE RULES (DECISION F041 D5): everything the results panel decides about a
// job's README, screenshots and app preview, as values and total functions over them. The
// shipped vitest config collects `src/**/*.test.ts` only and no DOM harness exists, so — as
// `pauseSend.ts` and `resultTour.ts` already do — every rule that CAN be a value is one here,
// and the panel, the card and the lightbox each render what this module already decided.
//
// TWO VIEWS, TWO DECODERS. `decodeArtifactsView` reads `_build_artifacts_json`'s envelope —
// the README (or none) and the screenshot list `artifacts_view` in
// `packages/orchestration/artifact_preview.py` answers; `decodePreviewView` reads
// `_build_preview_json`'s envelope, the state machine `packages/orchestration/preview_control.py`
// keeps. Both REFUSE WHOLE, exactly as `ownership.ts`'s own decoder does: a payload with one key
// out of shape answers `null` rather than a view that is silently shorter or wrong, because a
// truncated README or a link shown past its state would say something the server never claimed.
//
// THE README IS REWRITTEN, NOT PARSED. The server's sanitizer emits exactly one image shape,
// `<img src="…" alt="…">`, with a source that is either a listed capture's relative path (with an
// optional leading `./`) or something this browser must not trust as a link. `readmeCockpitHtml`
// addresses every image the file route can serve, through the token this cockpit already
// carries, and turns any other image into its own alt text — never into a link the server's
// sanitizer did not vouch for by listing it. A capture's own address is protected from the second,
// broad removal pass below through a one-shot placeholder, so the tag this function just built is
// never mistaken for one of the "other shapes" that pass removes.
//
// THE DELIBERATE ABSENCES, written down here because a reader looking for the missing code will
// search this file for it. No `window.`, no `document.`, no `fetch(`, no `Date`, no
// `Math.random`, no React import: this module opens no socket, mints nothing and renders
// nothing. It reads no clock — `previewPollDelayMs` answers a DURATION, never a deadline, and the
// card that schedules the timer owns the one `window.setTimeout` this feature ever calls.

/** The two roots a README or a screenshot may resolve under, `artifact_preview.py`'s own
 *  `ARTIFACT_ROOTS` in the server's own spelling. */
export type ArtifactRoot = "workspace" | "evidence";

/** One README, as `_readme_view` in `artifact_preview.py` answers it, camel-cased. */
export interface ReadmeArtifact {
  root: ArtifactRoot;
  path: string;
  html: string;
  truncated: boolean;
  sourceBytes: number;
}

/** One screenshot, as `_images_view` in `artifact_preview.py` answers it, camel-cased. */
export interface ImageArtifact {
  root: ArtifactRoot;
  path: string;
  bytes: number;
  contentType: string;
}

/** The whole artifacts view `_build_artifacts_json` answers: the README (or none), every
 *  screenshot, and an error that is "" when nothing went wrong. */
export interface ArtifactsView {
  readme: ReadmeArtifact | null;
  images: ImageArtifact[];
  error: string;
}

/** Every state a preview record may hold, `preview_control.py`'s own `PREVIEW_STATES`, in that
 *  module's own order. */
export const PREVIEW_STATES = [
  "stopped",
  "starting",
  "probing",
  "live",
  "failed",
  "not_applicable",
] as const;

export type PreviewState = (typeof PREVIEW_STATES)[number];

/** The cockpit-facing slice of the preview record, `preview_view` in `preview_control.py`'s own
 *  answer, camel-cased. */
export interface PreviewView {
  state: PreviewState;
  url: string;
  port: number;
  reason: string;
  updatedAt: string;
}

/** What every door and path below is addressed against: one job, one per-run token, and an
 *  optional origin the caller supplies — `ownershipViewPath`'s own shape. */
export interface ArtifactRequest {
  jobId: string;
  token: string;
  baseUrl?: string;
}

function recordOf(value: unknown): Record<string, unknown> | null {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>) : null;
}

function stringOf(value: unknown): string | null {
  return typeof value === "string" ? value : null;
}

function finiteNumberOf(value: unknown): number | null {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}

function booleanOf(value: unknown): boolean | null {
  return typeof value === "boolean" ? value : null;
}

function artifactRootOf(value: unknown): ArtifactRoot | null {
  return value === "workspace" || value === "evidence" ? value : null;
}

function readmeArtifactOf(value: unknown): ReadmeArtifact | null {
  const record = recordOf(value);
  if (record === null) return null;
  const root = artifactRootOf(record["root"]);
  const path = stringOf(record["path"]);
  const html = stringOf(record["html"]);
  const truncated = booleanOf(record["truncated"]);
  const sourceBytes = finiteNumberOf(record["source_bytes"]);
  if (root === null || path === null || html === null || truncated === null || sourceBytes === null) {
    return null;
  }
  return { root, path, html, truncated, sourceBytes };
}

function imageArtifactOf(value: unknown): ImageArtifact | null {
  const record = recordOf(value);
  if (record === null) return null;
  const root = artifactRootOf(record["root"]);
  const path = stringOf(record["path"]);
  const bytes = finiteNumberOf(record["bytes"]);
  const contentType = stringOf(record["content_type"]);
  if (root === null || path === null || bytes === null || contentType === null) {
    return null;
  }
  return { root, path, bytes, contentType };
}

/** The artifacts route's envelope, or `null` when ANY part of it cannot be read: the whole
 *  view is refused rather than shortened, `ownership.ts`'s own rule. */
export function decodeArtifactsView(payload: unknown): ArtifactsView | null {
  const record = recordOf(payload);
  if (record === null) return null;
  const error = stringOf(record["error"]);
  if (error === null) return null;
  const rawReadme = record["readme"];
  let readme: ReadmeArtifact | null = null;
  if (rawReadme !== null) {
    readme = readmeArtifactOf(rawReadme);
    if (readme === null) return null;
  }
  const rawImages = record["images"];
  if (!Array.isArray(rawImages)) return null;
  const images = rawImages.map(imageArtifactOf);
  if (images.some((image) => image === null)) return null;
  return { readme, images: images as ImageArtifact[], error };
}

/** The preview route's envelope, or `null` when ANY part of it cannot be read, or when
 *  `state` names something outside `PREVIEW_STATES` — the one state machine this cockpit
 *  understands. */
export function decodePreviewView(payload: unknown): PreviewView | null {
  const record = recordOf(payload);
  if (record === null) return null;
  const stateCandidate = record["state"];
  if (typeof stateCandidate !== "string"
      || !(PREVIEW_STATES as readonly string[]).includes(stateCandidate)) {
    return null;
  }
  const url = stringOf(record["url"]);
  const port = finiteNumberOf(record["port"]);
  const reason = stringOf(record["reason"]);
  const updatedAt = stringOf(record["updated_at"]);
  if (url === null || port === null || reason === null || updatedAt === null) {
    return null;
  }
  return { state: stateCandidate as PreviewState, url, port, reason, updatedAt };
}

/** The artifacts route, `ownershipViewPath`'s own base rule and every value through
 *  `encodeURIComponent`. */
export function artifactsViewPath(request: ArtifactRequest): string {
  const base = request.baseUrl ?? "";
  return `${base}/api/jobs/${encodeURIComponent(request.jobId)}/artifacts`
    + `?token=${encodeURIComponent(request.token)}`;
}

/** The preview route, shaped exactly as `artifactsViewPath` is. */
export function previewViewPath(request: ArtifactRequest): string {
  const base = request.baseUrl ?? "";
  return `${base}/api/jobs/${encodeURIComponent(request.jobId)}/preview`
    + `?token=${encodeURIComponent(request.token)}`;
}

/** The file route: a screenshot's bytes or the whole README, `read_artifact_file`'s own two
 *  query parameters, `root` and `path`, both through `encodeURIComponent`. */
export function artifactFilePath(request: ArtifactRequest, root: ArtifactRoot, path: string): string {
  const base = request.baseUrl ?? "";
  return `${base}/api/jobs/${encodeURIComponent(request.jobId)}/artifacts/file`
    + `?root=${encodeURIComponent(root)}&path=${encodeURIComponent(path)}`
    + `&token=${encodeURIComponent(request.token)}`;
}

/** The one image shape the server's renderer and sanitizer emit. */
const README_IMG_PATTERN = /<img src="([^"]*)" alt="([^"]*)">/g;

/** Every `<img …>` of any other shape, removed once the shape above has already been handled. */
const STRAY_IMG_PATTERN = /<img\b[^>]*>/g;

/** An address this cockpit may offer as a link: `http` or `https` only. */
const HTTP_URL_PATTERN = /^https?:\/\//i;

/** A README image's `src`, decoded the way the sanitizer's own escaping is undone: the four
 *  named entities that are not `&amp;` first, `&amp;` last (so a doubly-escaped ampersand never
 *  decodes twice), then one leading `./` dropped. */
function decodeReadmeImageSrc(raw: string): string {
  const decoded = raw
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, "\"")
    .replace(/&#x27;/g, "'")
    .replace(/&amp;/g, "&");
  return decoded.startsWith("./") ? decoded.slice(2) : decoded;
}

/** The address `U` this function writes into an `src` attribute: every `&` and `"` escaped so
 *  the URL stays one attribute value. */
function escapeAttributeValue(value: string): string {
  return value.replace(/&/g, "&amp;").replace(/"/g, "&quot;");
}

/** The README's html, rewritten for the cockpit (DECISION F041 D5): every image whose decoded
 *  source names a listed capture becomes a link through the file route, with `loading="lazy"`;
 *  every other recognised image becomes its own alt text; every image of another shape is
 *  dropped. Nothing else in the html changes. */
export function readmeCockpitHtml(
  html: string, images: readonly ImageArtifact[], request: ArtifactRequest,
): string {
  // A recognised image is placed behind a MARKER, printable ASCII a real README could not spell
  // as this exact run, rather than its final tag: the broad removal pass below has to run AFTER
  // this replacement (S1's own stated order), and without a marker it would delete the very
  // `<img …>` this function just built, mistaking it for one of the "other shapes" it exists to
  // drop.
  const finals: string[] = [];
  const withPlaceholders = html.replace(README_IMG_PATTERN, (_match, src: string, alt: string) => {
    const decodedSrc = decodeReadmeImageSrc(src);
    const found = images.find((image) => image.path === decodedSrc);
    if (found === undefined) {
      return alt;
    }
    const address = escapeAttributeValue(artifactFilePath(request, "evidence", found.path));
    const index = finals.push(`<img src="${address}" alt="${alt}" loading="lazy">`) - 1;
    return `@@artifact-image-${index}@@`;
  });
  const withoutStray = withPlaceholders.replace(STRAY_IMG_PATTERN, "");
  return withoutStray.replace(/@@artifact-image-(\d+)@@/g, (_match, index: string) => finals[Number(index)]);
}

/** A screenshot's caption: its last path segment without its own suffix, with every run of
 *  `_`, `-` and white space folded to one space and trimmed; the whole last segment when that
 *  is empty. */
export function captureCaption(path: string): string {
  const segments = path.split("/");
  const last = segments[segments.length - 1] ?? "";
  const dotIndex = last.lastIndexOf(".");
  const stem = dotIndex === -1 ? last : last.slice(0, dotIndex);
  const spaced = stem.replace(/[-_\s]+/g, " ").trim();
  return spaced === "" ? last : spaced;
}

/** The lightbox's next index after one key: the arrow keys step and stop at both ends; any
 *  other key changes nothing. */
export function lightboxIndexAfter(index: number, count: number, key: string): number {
  if (key === "ArrowRight") return Math.min(index + 1, count - 1);
  if (key === "ArrowLeft") return Math.max(index - 1, 0);
  return index;
}

/** How often the app card re-reads the preview view while it is on screen: fast while a start
 *  is still under way, slow once the state has settled. */
export const PREVIEW_POLL_FAST_MS = 2000;
export const PREVIEW_POLL_SLOW_MS = 15000;

export function previewPollDelayMs(view: PreviewView | null): number {
  if (view !== null && (view.state === "starting" || view.state === "probing")) {
    return PREVIEW_POLL_FAST_MS;
  }
  return PREVIEW_POLL_SLOW_MS;
}

/** The panel's only words for a state this module cannot otherwise explain, or is still
 *  waiting to read. */
export const ARTIFACTS_LOADING_LINE = "Reading this job's results…";
export const ARTIFACTS_UNREADABLE_LINE = "This job's results could not be read.";
export const README_UNREADABLE_LINE = "The README could not be read.";
export const README_ABSENT_LINE = "This job has no README.";
export const README_TRUNCATED_LINE = "The README is long, so only its beginning is shown.";
export const CAPTURES_ABSENT_LINE = "No screenshots were captured.";
export const PREVIEW_LOADING_LINE = "Reading the app's state…";
export const PREVIEW_UNREADABLE_LINE = "The app's state could not be read.";

/** What the app card shows: its line, an optional detail beneath it, the action its one button
 *  takes (or none), that button's label, and a link offered only while it is trustworthy. */
export interface PreviewCard {
  line: string;
  detail: string;
  action: "start" | "stop" | null;
  actionLabel: string;
  link: string | null;
}

/** THE APP CARD'S WHOLE VOCABULARY, keyed by state, and nothing else: a fresh object every
 *  call, so no caller can mutate the vocabulary for every other caller. */
export function previewCardView(view: PreviewView | null): PreviewCard {
  if (view === null) {
    return { line: PREVIEW_UNREADABLE_LINE, detail: "", action: null, actionLabel: "", link: null };
  }
  switch (view.state) {
    case "stopped":
      return {
        line: "The app is not running.", detail: view.reason,
        action: "start", actionLabel: "Start app", link: null,
      };
    case "starting":
      return {
        line: "Starting the app…", detail: "",
        action: "stop", actionLabel: "Stop app", link: null,
      };
    case "probing":
      return {
        line: "The app started. Checking that it answers…", detail: "",
        action: "stop", actionLabel: "Stop app", link: null,
      };
    case "live":
      return {
        line: `Live on port ${view.port}.`, detail: "",
        action: "stop", actionLabel: "Stop app",
        link: HTTP_URL_PATTERN.test(view.url) ? view.url : null,
      };
    case "failed":
      return {
        line: "The app could not be shown.", detail: view.reason,
        action: "start", actionLabel: "Try again", link: null,
      };
    case "not_applicable":
      return {
        line: "This project has no app to run.", detail: view.reason,
        action: null, actionLabel: "", link: null,
      };
    default:
      return { line: PREVIEW_UNREADABLE_LINE, detail: "", action: null, actionLabel: "", link: null };
  }
}
