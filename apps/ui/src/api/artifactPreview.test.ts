import { describe, expect, it } from "vitest";
import {
  PREVIEW_POLL_FAST_MS,
  PREVIEW_POLL_SLOW_MS,
  PREVIEW_UNREADABLE_LINE,
  artifactFilePath,
  artifactsViewPath,
  captureCaption,
  decodeArtifactsView,
  decodePreviewView,
  lightboxIndexAfter,
  previewCardView,
  previewPollDelayMs,
  previewViewPath,
  readmeCockpitHtml,
} from "./artifactPreview";
import type { ArtifactsView, ImageArtifact, PreviewState, PreviewView } from "./artifactPreview";

const VALID_ARTIFACTS_PAYLOAD = {
  readme: {
    root: "workspace", path: "README.md", html: "<p>hi</p>", truncated: false, source_bytes: 42,
  },
  images: [
    { root: "evidence", path: "captures/one.png", bytes: 10, content_type: "image/png" },
  ],
  error: "",
};

const DECODED_ARTIFACTS_VIEW: ArtifactsView = {
  readme: { root: "workspace", path: "README.md", html: "<p>hi</p>", truncated: false, sourceBytes: 42 },
  images: [{ root: "evidence", path: "captures/one.png", bytes: 10, contentType: "image/png" }],
  error: "",
};

describe("decodeArtifactsView", () => {
  it("decodes a whole valid payload", () => {
    expect(decodeArtifactsView(VALID_ARTIFACTS_PAYLOAD)).toEqual(DECODED_ARTIFACTS_VIEW);
  });

  it("decodes a payload with no README as a null readme", () => {
    expect(decodeArtifactsView({ readme: null, images: [], error: "" })).toEqual({
      readme: null, images: [], error: "",
    });
  });

  it("answers null when the payload itself is not an object", () => {
    expect(decodeArtifactsView(null)).toBeNull();
    expect(decodeArtifactsView("nope")).toBeNull();
    expect(decodeArtifactsView([])).toBeNull();
  });

  it("answers null when error is not a string", () => {
    expect(decodeArtifactsView({ ...VALID_ARTIFACTS_PAYLOAD, error: 1 })).toBeNull();
  });

  it("answers null when images is not an array", () => {
    expect(decodeArtifactsView({ ...VALID_ARTIFACTS_PAYLOAD, images: {} })).toBeNull();
  });

  it("answers null when readme is neither null nor an object", () => {
    expect(decodeArtifactsView({ ...VALID_ARTIFACTS_PAYLOAD, readme: "nope" })).toBeNull();
  });

  const readmeFieldCases: [string, unknown][] = [
    ["root", "elsewhere"],
    ["path", 1],
    ["html", 1],
    ["truncated", "yes"],
    ["source_bytes", "42"],
  ];
  for (const [field, badValue] of readmeFieldCases) {
    it(`answers null when readme.${field} is out of shape`, () => {
      const payload = {
        ...VALID_ARTIFACTS_PAYLOAD,
        readme: { ...VALID_ARTIFACTS_PAYLOAD.readme, [field]: badValue },
      };
      expect(decodeArtifactsView(payload)).toBeNull();
    });
  }

  const imageFieldCases: [string, unknown][] = [
    ["root", "elsewhere"],
    ["path", 1],
    ["bytes", "10"],
    ["content_type", 1],
  ];
  for (const [field, badValue] of imageFieldCases) {
    it(`answers null when images[0].${field} is out of shape`, () => {
      const payload = {
        ...VALID_ARTIFACTS_PAYLOAD,
        images: [{ ...VALID_ARTIFACTS_PAYLOAD.images[0], [field]: badValue }],
      };
      expect(decodeArtifactsView(payload)).toBeNull();
    });
  }
});

const VALID_PREVIEW_PAYLOAD = {
  state: "live", url: "http://127.0.0.1:5173/", port: 5173, reason: "", updated_at: "2026-09-29T00:00:00+00:00",
};

const DECODED_PREVIEW_VIEW: PreviewView = {
  state: "live", url: "http://127.0.0.1:5173/", port: 5173, reason: "", updatedAt: "2026-09-29T00:00:00+00:00",
};

describe("decodePreviewView", () => {
  it("decodes a whole valid payload", () => {
    expect(decodePreviewView(VALID_PREVIEW_PAYLOAD)).toEqual(DECODED_PREVIEW_VIEW);
  });

  it("answers null when the payload itself is not an object", () => {
    expect(decodePreviewView(null)).toBeNull();
    expect(decodePreviewView([])).toBeNull();
  });

  it("answers null when state names something outside PREVIEW_STATES", () => {
    expect(decodePreviewView({ ...VALID_PREVIEW_PAYLOAD, state: "paused" })).toBeNull();
    expect(decodePreviewView({ ...VALID_PREVIEW_PAYLOAD, state: 1 })).toBeNull();
  });

  const fieldCases: [string, unknown][] = [
    ["url", 1],
    ["port", "5173"],
    ["reason", 1],
    ["updated_at", 1],
  ];
  for (const [field, badValue] of fieldCases) {
    it(`answers null when ${field} is out of shape`, () => {
      expect(decodePreviewView({ ...VALID_PREVIEW_PAYLOAD, [field]: badValue })).toBeNull();
    });
  }
});

const PATH_JOB_ID = "job one";
const PATH_TOKEN = "tok&en";
const PATH_REQUEST = { jobId: PATH_JOB_ID, token: PATH_TOKEN };

describe("the three paths", () => {
  it("builds the artifacts view path with a spaced job id and an ampersand token", () => {
    expect(artifactsViewPath(PATH_REQUEST)).toBe("/api/jobs/job%20one/artifacts?token=tok%26en");
  });

  it("builds the preview view path with a spaced job id and an ampersand token", () => {
    expect(previewViewPath(PATH_REQUEST)).toBe("/api/jobs/job%20one/preview?token=tok%26en");
  });

  it("builds the file path with a spaced job id, an ampersand token, root and path", () => {
    expect(artifactFilePath(PATH_REQUEST, "evidence", "captures/one.png")).toBe(
      "/api/jobs/job%20one/artifacts/file?root=evidence&path=captures%2Fone.png&token=tok%26en",
    );
  });
});

const README_IMAGES: ImageArtifact[] = [
  { root: "evidence", path: "captures/one.png", bytes: 1, contentType: "image/png" },
];
const README_REQUEST = { jobId: "job1", token: "tok" };
const CAPTURE_ADDRESS =
  "/api/jobs/job1/artifacts/file?root=evidence&amp;path=captures%2Fone.png&amp;token=tok";

describe("readmeCockpitHtml", () => {
  it("addresses a listed capture through the file route with loading=lazy", () => {
    const html = '<img src="captures/one.png" alt="Shot one">';
    expect(readmeCockpitHtml(html, README_IMAGES, README_REQUEST)).toBe(
      `<img src="${CAPTURE_ADDRESS}" alt="Shot one" loading="lazy">`,
    );
  });

  it("strips one leading ./ before matching a listed capture", () => {
    const html = '<img src="./captures/one.png" alt="Shot one">';
    expect(readmeCockpitHtml(html, README_IMAGES, README_REQUEST)).toBe(
      `<img src="${CAPTURE_ADDRESS}" alt="Shot one" loading="lazy">`,
    );
  });

  it("turns an image outside captures/ into its own alt text", () => {
    const html = '<img src="docs/elsewhere.png" alt="Elsewhere shot">';
    expect(readmeCockpitHtml(html, README_IMAGES, README_REQUEST)).toBe("Elsewhere shot");
  });

  it("turns a capture not in the listed images into its own alt text", () => {
    const html = '<img src="captures/two.png" alt="Shot two">';
    expect(readmeCockpitHtml(html, README_IMAGES, README_REQUEST)).toBe("Shot two");
  });

  it("leaves an alt text holding &quot; unchanged", () => {
    const html = '<img src="captures/one.png" alt="Quote &quot; mark">';
    expect(readmeCockpitHtml(html, README_IMAGES, README_REQUEST)).toBe(
      `<img src="${CAPTURE_ADDRESS}" alt="Quote &quot; mark" loading="lazy">`,
    );
  });

  it("removes a stray <img> of another shape", () => {
    const html = '<img class="foo" src="x">';
    expect(readmeCockpitHtml(html, README_IMAGES, README_REQUEST)).toBe("");
  });

  it("rewrites a whole fragment with text and every shape around the images", () => {
    const html = '<h1>Fixture app</h1><p>Before <img src="captures/one.png" alt="first shot"> '
      + 'after <img src="docs/elsewhere.png" alt="elsewhere shot"> and '
      + '<img class="foo" src="x"> done.</p>';
    expect(readmeCockpitHtml(html, README_IMAGES, README_REQUEST)).toBe(
      `<h1>Fixture app</h1><p>Before <img src="${CAPTURE_ADDRESS}" alt="first shot" loading="lazy"> `
      + "after elsewhere shot and "
      + " done.</p>",
    );
  });
});

describe("captureCaption", () => {
  it("drops the directory and the suffix, folding separators to one space", () => {
    expect(captureCaption("captures/one.png")).toBe("one");
    expect(captureCaption("captures/two_three-four.png")).toBe("two three four");
    expect(captureCaption("nested/dir/five  six.jpeg")).toBe("five six");
  });

  it("keeps the whole segment when nothing survives trimming", () => {
    expect(captureCaption("captures/___.png")).toBe("captures/___.png".split("/")[1]);
    expect(captureCaption(".hidden")).toBe(".hidden");
  });

  it("keeps the whole segment when it has no suffix to drop", () => {
    expect(captureCaption("captures/noext")).toBe("noext");
  });
});

describe("lightboxIndexAfter", () => {
  it("steps right and stops at the last picture", () => {
    expect(lightboxIndexAfter(0, 3, "ArrowRight")).toBe(1);
    expect(lightboxIndexAfter(2, 3, "ArrowRight")).toBe(2);
  });

  it("steps left and stops at the first picture", () => {
    expect(lightboxIndexAfter(2, 3, "ArrowLeft")).toBe(1);
    expect(lightboxIndexAfter(0, 3, "ArrowLeft")).toBe(0);
  });

  it("changes nothing on any other key", () => {
    expect(lightboxIndexAfter(1, 3, "Enter")).toBe(1);
  });
});

describe("previewPollDelayMs", () => {
  const STATES: PreviewState[] = ["stopped", "starting", "probing", "live", "failed", "not_applicable"];

  it("answers the slow delay for a null view", () => {
    expect(previewPollDelayMs(null)).toBe(PREVIEW_POLL_SLOW_MS);
  });

  for (const state of STATES) {
    it(`answers the right delay while ${state}`, () => {
      const view: PreviewView = { state, url: "", port: 0, reason: "", updatedAt: "" };
      const expected = state === "starting" || state === "probing" ? PREVIEW_POLL_FAST_MS : PREVIEW_POLL_SLOW_MS;
      expect(previewPollDelayMs(view)).toBe(expected);
    });
  }
});

function previewView(state: PreviewState, extra: Partial<PreviewView> = {}): PreviewView {
  return { state, url: "", port: 0, reason: "", updatedAt: "", ...extra };
}

describe("previewCardView", () => {
  it("answers the unreadable card for a null view", () => {
    expect(previewCardView(null)).toEqual({
      line: PREVIEW_UNREADABLE_LINE, detail: "", action: null, actionLabel: "", link: null,
    });
  });

  it("answers the stopped card with the reason and a start action", () => {
    expect(previewCardView(previewView("stopped", { reason: "not started yet" }))).toEqual({
      line: "The app is not running.", detail: "not started yet",
      action: "start", actionLabel: "Start app", link: null,
    });
  });

  it("answers the starting card with no detail and a stop action", () => {
    expect(previewCardView(previewView("starting"))).toEqual({
      line: "Starting the app…", detail: "", action: "stop", actionLabel: "Stop app", link: null,
    });
  });

  it("answers the probing card with no detail and a stop action", () => {
    expect(previewCardView(previewView("probing"))).toEqual({
      line: "The app started. Checking that it answers…", detail: "",
      action: "stop", actionLabel: "Stop app", link: null,
    });
  });

  it("answers the live card with the port and an http link", () => {
    expect(previewCardView(previewView("live", { port: 5173, url: "http://127.0.0.1:5173/" }))).toEqual({
      line: "Live on port 5173.", detail: "",
      action: "stop", actionLabel: "Stop app", link: "http://127.0.0.1:5173/",
    });
  });

  it("offers no link for a live view whose url is not http or https", () => {
    expect(previewCardView(previewView("live", { port: 5173, url: "javascript:alert(1)" }))).toEqual({
      line: "Live on port 5173.", detail: "",
      action: "stop", actionLabel: "Stop app", link: null,
    });
  });

  it("answers the failed card with the reason and a try-again action", () => {
    expect(previewCardView(previewView("failed", { reason: "started but health check failed: boom" }))).toEqual({
      line: "The app could not be shown.", detail: "started but health check failed: boom",
      action: "start", actionLabel: "Try again", link: null,
    });
  });

  it("answers the not_applicable card with the reason and no action", () => {
    expect(previewCardView(previewView("not_applicable", { reason: "the job has no project folder to run" }))).toEqual({
      line: "This project has no app to run.", detail: "the job has no project folder to run",
      action: null, actionLabel: "", link: null,
    });
  });
});
