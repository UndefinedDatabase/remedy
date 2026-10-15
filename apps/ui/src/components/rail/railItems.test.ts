// amend1015 P4.1: every rail button does something, or is not there.
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { RAIL_KEYS, railItemsOf } from "./railItems";
import type { RailActions } from "./railItems";
import { SideIconDock } from "./SideIconDock";

function recording() {
  const calls: string[] = [];
  const actions: RailActions = {
    onChecks: () => calls.push("plan"), onActivity: () => calls.push("activity"),
    onFiles: () => calls.push("results"), onHistory: () => calls.push("story"),
    onDocs: () => calls.push("terms"), onSettings: () => calls.push("system"),
  };
  return { calls, actions };
}

describe("railItemsOf", () => {
  it("gives every rendered button its own action, so no button is a no-op", () => {
    const { calls, actions } = recording();
    const items = railItemsOf(() => calls.push("home"), actions);
    expect(items.map((i) => i.key)).toEqual([...RAIL_KEYS]);
    for (const item of items) item.onClick();
    expect(calls).toEqual(["home", "plan", "activity", "results", "story", "terms", "system"]);
    for (const item of items) expect(item.title.length).toBeGreaterThan(0);
  });

  it("drops a button whose panel the mount did not hand over", () => {
    const items = railItemsOf(() => {}, { onDocs: () => {} });
    expect(items.map((i) => i.key)).toEqual(["Overview", "Docs"]);
  });

  it("marks the open panel's button active, and Overview when none is open", () => {
    const { actions } = recording();
    expect(railItemsOf(() => {}, actions).filter((i) => i.active).map((i) => i.key)).toEqual(["Overview"]);
    expect(railItemsOf(() => {}, { ...actions, active: "Files" }).filter((i) => i.active).map((i) => i.key)).toEqual(["Files"]);
  });
});

describe("SideIconDock", () => {
  it("renders each button with a label, a tooltip and its pressed state", () => {
    const { actions } = recording();
    const html = renderToStaticMarkup(createElement(SideIconDock, { actions: { ...actions, active: "History" } }));
    expect(html.match(/<button/g)?.length).toBe(7);
    expect(html).toContain('aria-label="History"');
    expect(html).toMatch(/aria-label="History"[^>]*aria-pressed="true"|aria-pressed="true"[^>]*aria-label="History"/);
    expect(html).toContain('title="Story: how this job unfolded"');
  });
});
