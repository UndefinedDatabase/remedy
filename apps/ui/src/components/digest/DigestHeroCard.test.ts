// amend1015 P3.4: the card's primary action copies the recommended command, or is plain text.
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import type { JobDigest } from "../../api/jobDigest";
import type { DigestVisibility, DigestVisibilityPort } from "../../api/digestVisibility";
import { DigestHeroCard } from "./DigestHeroCard";

const port: DigestVisibilityPort = {
  readDismissal: () => null, writeDismissal: () => {}, readLastSeen: () => null, writeLastSeen: () => {},
} as unknown as DigestVisibilityPort;
const visibility = { show: true, reason: "terminal" } as unknown as DigestVisibility;

const digest = (label: string, rule_id: string): JobDigest => ({
  version: 1, job_id: "j1", state: "completed", headline: "The run is completed.",
  cost: { value: "builder: 2 harness invocations", basis: "actual" }, ownership: [],
  decisions: { open_count: 0, peak_urgency: 0 }, primary_action: { label, rule_id },
});

const card = (d: JobDigest) => renderToStaticMarkup(createElement(DigestHeroCard, { digest: d, visibility, port, onPrimaryAction: () => {} }));

describe("the digest card's primary action (amend1015 P3.4)", () => {
  it("offers to copy the apply command and shows it", () => {
    const html = card(digest("Apply the reviewed result: `remedy job apply j1 --repo /tmp/r --approve`", "apply-pending"));
    expect(html).toMatch(/<button[^>]*>Copy the command<\/button>/);
    expect(html).toContain("<code>remedy job apply j1 --repo /tmp/r --approve</code>");
    expect(html).toContain("Apply the reviewed result");
  });

  it("is plain text when the recommendation carries no command", () => {
    const html = card(digest("Review and merge the branch", "all-green"));
    expect(html).toContain("Review and merge the branch");
    expect(html).not.toContain("Copy the command");
    expect(html).not.toMatch(/<button[^>]*>Review and merge the branch<\/button>/);
  });
});
