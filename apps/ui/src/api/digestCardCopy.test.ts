import { describe, it, expect } from "vitest";
import { DIGEST_CTA_RULE_IDS, digestCtaText, digestStateLabel } from "./digestCardCopy";

/** All seven `RunState` values from `packages/core/models.py`, written as a
 *  TABLE so a state added to that enum has an obvious place to land here.
 *
 *  Every expectation below is a phrase and not "Planned": that is the whole
 *  reason this module exists rather than reusing `stateLabel` from
 *  `../copy/humanCopy`, whose vocabulary is the checklist's and which answers
 *  "Planned" for six of these seven rows. */
const STATE_TABLE: readonly { state: string; label: string }[] = [
  { state: "pending", label: "Waiting to start" },
  { state: "planned", label: "Planned" },
  { state: "running", label: "Running" },
  { state: "paused", label: "Paused" },
  { state: "completed", label: "Completed" },
  { state: "failed", label: "Failed" },
  { state: "cancelled", label: "Cancelled" },
];

/** The exact command `escalation.task_decision_answer_command` builds, with a
 *  real eight-character job prefix and a real `td:` decision id. It is written
 *  out rather than abbreviated because the identifiers ARE what §17 objects to,
 *  and a fixture without them would test nothing. */
const ANSWER_COMMAND =
  'remedy decision resolve 1a2b3c4d td:9f8e7d6c --reason "<your answer>"';

/** An evidence ref of the kind `_link` wraps in markdown link syntax. */
const EVIDENCE_REF = "evidence/postmortem.md";

/** The label shapes `recommended_next_action` in
 *  `packages/orchestration/run_report.py` ACTUALLY emits, one row per shape and
 *  not one per rule: `open-decision` degrades to a bare sentence when no blocked
 *  item carries an answer command, and `blocked-failed` degrades to a bare label
 *  when no blocked item carries an evidence ref, so those two rules have two
 *  forms each and both forms are graded.
 *
 *  These are read off the rule table rather than off
 *  `tests/orchestration/fixtures/job_digest/golden/`, because the goldens reach
 *  only four of the five rules — `stopped-by-operator` is exercised by no
 *  fixture at all — and the vocabulary is the table's. */
const CTA_TABLE: readonly {
  ruleId: (typeof DIGEST_CTA_RULE_IDS)[number];
  shape: string;
  label: string;
  text: string;
}[] = [
  {
    ruleId: "open-decision",
    shape: "with an answer command",
    label: `Answer the open decision: \`${ANSWER_COMMAND}\``,
    text: "Answer the open decision",
  },
  {
    ruleId: "open-decision",
    shape: "without an answer command",
    label: "Answer the open decision",
    text: "Answer the open decision",
  },
  {
    ruleId: "stopped-by-operator",
    shape: "as its only form",
    label: "Resume the run (or close it) — it stopped on request, nothing is broken",
    text: "Resume the run (or close it) — it stopped on request, nothing is broken",
  },
  {
    ruleId: "blocked-failed",
    shape: "with an evidence ref",
    label: `Inspect [the postmortem](${EVIDENCE_REF}) and repair the blocked task`,
    text: "Inspect the postmortem and repair the blocked task",
  },
  {
    ruleId: "blocked-failed",
    shape: "without an evidence ref",
    label: "Inspect the postmortem and repair the blocked task",
    text: "Inspect the postmortem and repair the blocked task",
  },
  {
    ruleId: "all-green",
    shape: "as its only form",
    label: "Review and merge the branch",
    text: "Review and merge the branch",
  },
  {
    ruleId: "indeterminate",
    shape: "as its only form",
    label: "No recommendation — the run state is not recorded",
    text: "No recommendation — the run state is not recorded",
  },
];

describe("digestStateLabel", () => {
  for (const row of STATE_TABLE) {
    it(`renders ${row.state} as a phrase of its own`, () => {
      expect(digestStateLabel(row.state)).toBe(row.label);
    });
  }

  it("covers all seven states of RunState in the table", () => {
    expect(STATE_TABLE.map((row) => row.state)).toEqual([
      "pending",
      "planned",
      "running",
      "paused",
      "completed",
      "failed",
      "cancelled",
    ]);
  });

  it("gives every state its own phrase, so no two collapse together", () => {
    const labels = STATE_TABLE.map((row) => row.label);
    expect(new Set(labels).size).toBe(labels.length);
  });

  it("answers a safe phrase for a state it has never heard of", () => {
    expect(digestStateLabel("quantum-tunnelling")).toBe("State not recorded");
  });

  it("shows nothing raw for an empty state", () => {
    expect(digestStateLabel("")).toBe("State not recorded");
  });

  it("does not read a state off the prototype chain", () => {
    // `DIGEST_STATE_LABELS` is a plain object, so an unguarded index would
    // answer a FUNCTION here rather than a sentence.
    expect(digestStateLabel("toString")).toBe("State not recorded");
  });
});

describe("digestCtaText over every shape the run report emits", () => {
  for (const row of CTA_TABLE) {
    it(`renders the ${row.ruleId} label ${row.shape}`, () => {
      expect(digestCtaText(row.label)).toBe(row.text);
    });
  }

  it("grades every rule id the envelope can carry", () => {
    const graded = new Set(CTA_TABLE.map((row) => row.ruleId));
    expect([...graded].sort()).toEqual([...DIGEST_CTA_RULE_IDS].sort());
  });

  it("grades both forms of the two rules that have two", () => {
    const forms = (id: string) => CTA_TABLE.filter((row) => row.ruleId === id).length;
    expect(forms("open-decision")).toBe(2);
    expect(forms("blocked-failed")).toBe(2);
  });
});

describe("digestCtaText keeps report markup out of the cockpit", () => {
  // THE ASSERTION THAT MATTERS MOST. §17 forbids the default UI showing raw
  // identifiers or raw markup, and these four tokens are the whole of what the
  // Markdown surface adds to a label: the command fence, the link's brackets,
  // the link's ref opener and the decision id.
  const FORBIDDEN_TOKENS = ["`", "[", "](", "td:"];

  for (const row of CTA_TABLE) {
    it(`leaves no markup in the ${row.ruleId} label ${row.shape}`, () => {
      const text = digestCtaText(row.label);
      for (const token of FORBIDDEN_TOKENS) {
        expect(text).not.toContain(token);
      }
    });
  }

  it("would see the markup if it were still there", () => {
    // The discriminator: without it every assertion above would pass just as
    // happily over labels that never carried markup in the first place.
    const withMarkup = CTA_TABLE.filter((row) =>
      FORBIDDEN_TOKENS.some((token) => row.label.includes(token)));
    expect(withMarkup.map((row) => `${row.ruleId} ${row.shape}`)).toEqual([
      "open-decision with an answer command",
      "blocked-failed with an evidence ref",
    ]);
  });

  it("drops the whole command rather than only its fences", () => {
    const label = `Answer the open decision: \`${ANSWER_COMMAND}\``;
    expect(digestCtaText(label)).not.toContain("remedy decision resolve");
    expect(digestCtaText(label)).not.toContain("1a2b3c4d");
  });

  it("shows the link text and never the ref behind it", () => {
    const label = `Inspect [the postmortem](${EVIDENCE_REF}) and repair the blocked task`;
    expect(digestCtaText(label)).toContain("the postmortem");
    expect(digestCtaText(label)).not.toContain(EVIDENCE_REF);
  });

  it("converges the two forms of the open-decision rule on one sentence", () => {
    // The command is an artifact of the report, so removing it must land on the
    // sentence that rule already emits when there is no command to offer.
    expect(digestCtaText(`Answer the open decision: \`${ANSWER_COMMAND}\``))
      .toBe(digestCtaText("Answer the open decision"));
  });
});

describe("digestCtaText answers the empty cases without inventing an instruction", () => {
  it("answers the missing-value marker for an empty label", () => {
    expect(digestCtaText("")).toBe("No recommendation recorded");
  });

  it("answers it for a label that is nothing but a command", () => {
    expect(digestCtaText(`\`${ANSWER_COMMAND}\``)).toBe("No recommendation recorded");
  });

  it("answers it for a label that is a bare identifier", () => {
    // `scrubUiText` owns the whole-value identifier test; this pins that the
    // final screen is really being applied rather than merely imported.
    expect(digestCtaText("deadbeef-1234")).toBe("No recommendation recorded");
  });

  it("answers it for a label carrying a forbidden diagnostics word", () => {
    // The other half of `scrubUiText`'s screen, for the same reason.
    expect(digestCtaText("Read the raw_stdout of the worker")).toBe(
      "No recommendation recorded");
  });
});

describe("DIGEST_CTA_RULE_IDS", () => {
  it("names the five rules recommended_next_action can return", () => {
    expect([...DIGEST_CTA_RULE_IDS]).toEqual([
      "open-decision",
      "stopped-by-operator",
      "blocked-failed",
      "all-green",
      "indeterminate",
    ]);
  });

  it("is a closed set with no duplicates", () => {
    expect(new Set(DIGEST_CTA_RULE_IDS).size).toBe(DIGEST_CTA_RULE_IDS.length);
  });
});
