// amend1015 P2.2: the pill tells the dashboard's truth about a finished job.
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { LiveStatusPill } from "./LiveStatusPill";

const pill = (props: Parameters<typeof LiveStatusPill>[0]) => renderToStaticMarkup(createElement(LiveStatusPill, props));

describe("LiveStatusPill on a finished job", () => {
  it("says FINISHED, never RECONNECTING, when the dashboard says the job completed", () => {
    for (const streamStatus of ["reconnecting", "delayed", "live", null] as const) {
      const html = pill({ live: false, stage: "completed", streamStatus });
      expect(html).toContain("FINISHED");
      expect(html).not.toContain("RECONNECTING");
    }
  });

  it("says IDLE for a job that is not running and not finished", () => {
    expect(pill({ live: false, stage: "planned", streamStatus: "reconnecting" })).toContain("IDLE");
  });

  it("keeps the transport's word while the job runs", () => {
    expect(pill({ live: true, stage: "running", streamStatus: "reconnecting" })).toContain("RECONNECTING");
    expect(pill({ live: true, stage: "running", streamStatus: "delayed" })).toContain("DELAYED");
    expect(pill({ live: true, stage: "running", streamStatus: "live" })).toContain("LIVE");
  });
});
