// The catalog turns a raw stream event into a sentence a human can read.
// Remedy deliberately keeps the catalog DATA in humanizeCatalog.ts: its key set is
// gated against the Python run-log emitters by
// tests/ui_contracts/test_humanize_catalog.py, and a data-only module keeps that
// extractor's job a line scan rather than a parse.
import { STREAM_EVENT_CATALOG } from "./humanizeCatalog";

/** One humanized stream event: the line a feed row renders, and whether the
 *  catalog recognised the kind at all. `known` is what a dev console note counts. */
export interface HumanizedStreamEvent {
  line: string;
  known: boolean;
}

// The honest generic line, and the load-bearing half of this module's contract.
// Eleven run-log writers compute their event name at runtime, so no static
// catalog can ever be complete; an unrecognised kind renders as itself rather
// than vanishing from the story the feed is supposed to tell.
export function humanizeStreamEvent(kind: unknown): HumanizedStreamEvent {
  if (typeof kind !== "string" || kind === "") {
    return { line: "unknown event", known: false };
  }
  // hasOwnProperty, never a bare lookup: a kind named `toString` or `constructor`
  // resolves against Object.prototype and would be reported as known.
  if (!Object.prototype.hasOwnProperty.call(STREAM_EVENT_CATALOG, kind)) {
    return { line: `${kind} event`, known: false };
  }
  return { line: STREAM_EVENT_CATALOG[kind], known: true };
}
