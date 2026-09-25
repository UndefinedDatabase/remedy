import { describe, expect, it } from "vitest";
import { GOLDEN_B_MODEL } from "./brainReducer.fixtures";
import { ZOOM_HOME, zoomGraphOf, zoomTransition, type ZoomState } from "./semanticZoom";
import { searchWithZoom, zoomLinkEvents, zoomLinkFromSearch } from "./zoomDeepLink";

describe("zoomLinkFromSearch", () => {
  it.each([
    ["?job=j&focus=task%3At1&level=1", { focusId: "task:t1", tab: null }],
    ["?focus=run%3At1%3A2&level=2&tab=prompt", { focusId: "run:t1:2", tab: null }],
    ["?focus=run%3At1%3A2&level=3&tab=prompt", { focusId: "run:t1:2", tab: "prompt" }],
    ["?focus=run%3At1%3A2&level=3", { focusId: "run:t1:2", tab: "diff" }],
    ["?focus=run%3At1%3A2&level=3&tab=logs", { focusId: "run:t1:2", tab: "diff" }],
    ["?job=j&token=t", null],
    ["?focus=&level=1", null],
    ["?focus=task%3At1", null],
    ["?focus=task%3At1&level=0", null],
    ["?focus=task%3At1&level=4", null],
    ["", null],
  ] as const)("%s", (search, expected) => {
    expect(zoomLinkFromSearch(search)).toEqual(expected);
  });
});

describe("zoomLinkEvents", () => {
  it("is a click, and at L3 the tab after it", () => {
    expect(zoomLinkEvents({ focusId: "task:t1", tab: null })).toEqual([{ type: "click", nodeId: "task:t1" }]);
    expect(zoomLinkEvents({ focusId: "run:t1:2", tab: "chat" })).toEqual([
      { type: "click", nodeId: "run:t1:2" }, { type: "open_evidence", tab: "chat" },
    ]);
  });
});

describe("searchWithZoom", () => {
  it("adds the zoom after every other parameter and keeps those as they were", () => {
    expect(searchWithZoom("?job=j&token=t", { level: 3, focusId: "run:t1:2", tab: "prompt" }))
      .toBe("?job=j&token=t&focus=run%3At1%3A2&level=3&tab=prompt");
    expect(searchWithZoom("?job=j", { level: 1, focusId: "task:t1", tab: null })).toBe("?job=j&focus=task%3At1&level=1");
  });

  it("replaces a stale zoom and removes it at L0", () => {
    expect(searchWithZoom("?job=j&focus=x&level=3&tab=chat&token=t", { level: 2, focusId: "run:t1:2", tab: null }))
      .toBe("?job=j&token=t&focus=run%3At1%3A2&level=2");
    expect(searchWithZoom("?job=j&focus=x&level=1&token=t", ZOOM_HOME)).toBe("?job=j&token=t");
    expect(searchWithZoom("?focus=x&level=1", ZOOM_HOME)).toBe("");
  });
});

describe("a link restores the state it was written from", () => {
  const graph = zoomGraphOf(GOLDEN_B_MODEL.nodes);
  const states: ZoomState[] = [
    { level: 1, focusId: "task:t2", tab: null },
    { level: 2, focusId: "run:t1:2", tab: null },
    { level: 3, focusId: "run:t1:6", tab: "prompt" },
  ];

  it.each(states)("level $level on $focusId", (state) => {
    const link = zoomLinkFromSearch(searchWithZoom("?job=job-b", state));
    expect(link).not.toBeNull();
    let restored: ZoomState = ZOOM_HOME;
    for (const event of zoomLinkEvents(link!)) restored = zoomTransition(graph, restored, event).state;
    expect(restored).toEqual(state);
  });

  it("a link to a node the graph does not hold leaves the zoom at home", () => {
    let restored: ZoomState = ZOOM_HOME;
    for (const event of zoomLinkEvents({ focusId: "run:t9:1", tab: "diff" })) restored = zoomTransition(graph, restored, event).state;
    expect(restored).toBe(ZOOM_HOME);
  });
});
