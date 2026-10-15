// amend1015 P4.2: the rail shows this job's order, never a design mock's headline.
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { normalizeDashboardPayload } from "../../api/remedyApi";
import { LeftBrandRail } from "./LeftBrandRail";

describe("LeftBrandRail", () => {
  it("names the job's order and carries no mock copy", () => {
    const dashboard = normalizeDashboardPayload("j1", { job_id: "j1", legacy: { job_name: "pass die readme an" }, tasks: [] });
    const html = renderToStaticMarkup(createElement(LeftBrandRail, { dashboard }));
    expect(html).toContain("pass die readme an");
    for (const mock of ["CONCEPT 01", "GROWING BRAIN", "scans and summarizes", "Growing Brain Overview"]) {
      expect(html).not.toContain(mock);
    }
  });
});
