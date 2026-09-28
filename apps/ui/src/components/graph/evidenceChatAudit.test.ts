// F038 T003 — THE DOM AUDIT: `ChatTurnBlock` rendered with `react-dom/server`'s
// `renderToStaticMarkup`, the one DOM surface this repository's vitest config can reach
// (DECISION F031 D5: `apps/ui/vitest.config.ts` collects `src/**/*.test.ts` in a node
// environment with no DOM library). The markup is inspected with plain regex rather than a DOM
// parser, exactly because no DOM library is available here.
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { CHAT_NOT_IN_EVIDENCE } from "../../api/chatTurn";
import type { ChatAnswerView, ChatCardView } from "../../api/chatTurn";
import { ChatTurnBlock } from "./EvidenceChatTab";

const EVIDENCE = [
  { number: 1, kind: "node", ref: "task-1", text: "Task task-1: Write the README" },
  { number: 2, kind: "round", ref: "task-1#1", text: "Round 1: tests passed" },
];

/** Three checked sentences (cited once, unsupported, cited twice) plus the absence sentence,
 *  which the block's own THE TESTS section asks for by name. */
const ANSWER: ChatAnswerView = {
  kind: "answer",
  scope: "node",
  subject: "task-1",
  question: "Did the tests pass?",
  generator: "mechanical",
  sentences: [
    { text: "Tests passed [1].", citations: [1], supported: true, problem: "" },
    { text: "Something else.", citations: [], supported: false, problem: "cites no evidence item" },
    { text: "Two facts [1][2].", citations: [1, 2], supported: true, problem: "" },
    { text: CHAT_NOT_IN_EVIDENCE, citations: [], supported: true, problem: "" },
  ],
  evidence: EVIDENCE,
  omitted: 0,
};

function renderAnswer(): string {
  return renderToStaticMarkup(createElement(ChatTurnBlock, {
    question: "Did the tests pass?",
    view: ANSWER,
    turnKey: "k1",
    outcome: null,
    onConfirm: () => {},
    onOpenTab: () => {},
  }));
}

/** Every `<p ... data-ui="chat-sentence" ... data-mark="...">...</p>` block, in source order.
 *  No sentence nests a `<p>`, so the first `</p>` after each opening tag is its own close. */
function sentenceBlocks(markup: string): Array<{ mark: string; inner: string }> {
  const found: Array<{ mark: string; inner: string }> = [];
  const re = /<p[^>]*data-ui="chat-sentence"[^>]*data-mark="([^"]+)"[^>]*>(.*?)<\/p>/gs;
  let match = re.exec(markup);
  while (match !== null) {
    found.push({ mark: match[1], inner: match[2] });
    match = re.exec(markup);
  }
  return found;
}

describe("ChatTurnBlock's DOM audit — an answer", () => {
  it("every sentence carries a chip or the unsupported mark, and the absence sentence carries neither", () => {
    const blocks = sentenceBlocks(renderAnswer());
    expect(blocks).toHaveLength(4);
    expect(blocks[0].mark).toBe("cited");
    expect(blocks[0].inner).toContain('data-ui="chat-chip"');
    expect(blocks[0].inner).not.toContain('data-ui="chat-unsupported"');
    expect(blocks[1].mark).toBe("unsupported");
    expect(blocks[1].inner).toContain('data-ui="chat-unsupported"');
    expect(blocks[1].inner).not.toContain('data-ui="chat-chip"');
    expect(blocks[2].mark).toBe("cited");
    expect(blocks[2].inner).toContain('data-ui="chat-chip"');
    expect(blocks[2].inner).not.toContain('data-ui="chat-unsupported"');
    expect(blocks[3].mark).toBe("absence");
    expect(blocks[3].inner).not.toContain('data-ui="chat-chip"');
    expect(blocks[3].inner).not.toContain('data-ui="chat-unsupported"');
  });

  it("no sentence's own text keeps an [n] marker", () => {
    for (const { inner } of sentenceBlocks(renderAnswer())) {
      const withoutMarkup = inner.replace(/<a[^>]*>.*?<\/a>/gs, "").replace(/<span[^>]*>.*?<\/span>/gs, "");
      expect(withoutMarkup).not.toMatch(/\[\d+\]/);
    }
  });

  it("each chip's link number equals its label, and each chip's target id is rendered", () => {
    const markup = renderAnswer();
    const chipRe = /<a[^>]*data-ui="chat-chip"[^>]*href="#chat-k1-ev-(\d+)"[^>]*>\[(\d+)\]<\/a>/g;
    const chips: string[] = [];
    let match = chipRe.exec(markup);
    while (match !== null) {
      expect(match[1]).toBe(match[2]);
      chips.push(match[1]);
      expect(markup).toContain(`id="chat-k1-ev-${match[1]}"`);
      match = chipRe.exec(markup);
    }
    expect(chips.length).toBe(3);
  });
});

describe("ChatTurnBlock's DOM audit — a card", () => {
  const completeCard: ChatCardView = {
    kind: "card", verb: "job.pause", title: "Pause the job",
    lines: ["Job: job-1", "Command: job.pause"], args: {}, missing: [], confirmable: true,
  };

  function renderCard(card: ChatCardView): string {
    return renderToStaticMarkup(createElement(ChatTurnBlock, {
      question: "pause",
      view: card,
      turnKey: "k2",
      outcome: null,
      onConfirm: () => {},
      onOpenTab: () => {},
    }));
  }

  it("Confirm renders for a complete card", () => {
    expect(renderCard(completeCard)).toContain('data-ui="chat-card-confirm"');
  });

  it("Confirm does not render for a card that is not confirmable", () => {
    expect(renderCard({ ...completeCard, confirmable: false })).not.toContain('data-ui="chat-card-confirm"');
  });

  it("Confirm does not render for a card missing an argument", () => {
    expect(renderCard({ ...completeCard, missing: ["message"] })).not.toContain('data-ui="chat-card-confirm"');
  });
});
