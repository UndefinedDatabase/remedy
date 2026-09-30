// F043 T003 — the '?' panel's markup, rendered with `renderToStaticMarkup` (DECISION F043 D3).
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { TERM_CATALOG } from "../../api/terminology";
import { searchTermEntries, termPlace } from "../../api/termSearch";
import { TERM_PANEL_LABEL, TERM_SEARCH_LABEL, TermPanel, termPanelEmptyLine } from "./TermPanel";

function renderPanel(): string {
  return renderToStaticMarkup(createElement(TermPanel, { onClose: () => {} }));
}

describe("the '?' panel", () => {
  it("is a dialog named Terms with a labelled search field", () => {
    const markup = renderPanel();
    expect(TERM_PANEL_LABEL).toBe("Terms");
    expect(TERM_SEARCH_LABEL).toBe("Search the terms");
    expect(markup).toMatch(/^<section [^>]*role="dialog"[^>]*aria-label="Terms"[^>]*data-ui="term-panel"/);
    expect(markup).toMatch(/<input [^>]*type="search"[^>]*aria-label="Search the terms"/);
  });

  it("lists every catalog entry once, in the search's order, with its title, place and body", () => {
    const markup = renderPanel();
    const listed = [...markup.matchAll(/data-term-entry="([^"]+)"><dt>([^<]*)<\/dt><dd [^>]*>([^<]*)<\/dd><dd>([^<]*)<\/dd>/g)];
    expect(listed.map((row) => row[1])).toEqual(searchTermEntries(TERM_CATALOG, "").map((row) => row.key));
    for (const [, key, title, place, body] of listed) {
      const unescape = (text: string) => text.replace(/&#x27;/g, "'").replace(/&quot;/g, "\"").replace(/&amp;/g, "&");
      expect(unescape(title), key).toBe(TERM_CATALOG[key].title);
      expect(place, key).toBe(termPlace(key));
      expect(unescape(body), key).toBe(TERM_CATALOG[key].body);
    }
  });

  it("carries no data-term, so it can never stand in for a surface in the audit", () => {
    expect(renderPanel()).not.toMatch(/\sdata-term="/);
  });

  it("offers the tour again only when the shell hands it a way to start one", () => {
    expect(renderPanel()).not.toContain("Take the tour");
    const offered = renderToStaticMarkup(createElement(TermPanel, { onClose: () => {}, onStartTour: () => {} }));
    expect(offered).toMatch(/<button type="button" class="[^"]*">Take the tour<\/button>/);
  });

  it("words an empty search plainly", () => {
    expect(termPanelEmptyLine("  zebra ")).toBe("No term matches “zebra”.");
  });
});
