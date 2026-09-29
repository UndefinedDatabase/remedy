import React from "react";
import { createRoot } from "react-dom/client";
import "./styles/globals.css";
import { ReducedMotionProvider } from "./components/shell/ReducedMotionProvider";
import { StoryPlayerApp } from "./components/story/StoryPlayerApp";
import { readEmbeddedStory, STORY_DATA_ELEMENT_ID } from "./components/story/storyExport";

/**
 * F039 T003, DECISION F039 D8 — the exported page's own entry. The story is read from the
 * page itself, embedded by `render_story_html` into `#remedy-story-data`, and never from a
 * route: a page opened from `file://` has no server on the other end of a network call.
 */
const decoded = readEmbeddedStory(document.getElementById(STORY_DATA_ELEMENT_ID)?.textContent ?? null);

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ReducedMotionProvider>
      {decoded.ok
        ? <StoryPlayerApp story={decoded.story} />
        : <p data-ui="story-export-error">{decoded.message}</p>}
    </ReducedMotionProvider>
  </React.StrictMode>,
);
