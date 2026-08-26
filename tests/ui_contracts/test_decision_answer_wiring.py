"""Contract tests for the decision inbox's ANSWER WIRING (T5_F031 T003).

The last step of T003 makes a decision card answerable: the per-run server token
travels from `RemedyApp`'s `readUrlState` through `RemedyShell` and
`RightLivePanel` to `DecisionInboxCard`, and an answer click calls
`answerDecisionCard`. This repository has no DOM environment and the shipped
vitest config collects `src/**/*.test.ts` only, so nothing renders that markup;
the wiring is gated the way every other component here is gated — by reading its
source, exactly as `test_remedy_shell_stream.py` gates the stream subscription.

Every assertion runs against COMMENT-STRIPPED source. These files carry long
prose headers that NAME the very symbols asserted below — `serverToken`,
`answerDecisionCard`, `ANSWER_PENDING_TITLE` — so an unstripped guard would be
satisfied by the comment describing the code rather than by the code itself
(finding R-0584).
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
APP = UI_SRC / "RemedyApp.tsx"
SHELL = UI_SRC / "components" / "shell" / "RemedyShell.tsx"
PANEL = UI_SRC / "components" / "panels" / "RightLivePanel.tsx"
CARD = UI_SRC / "components" / "panels" / "DecisionInboxCard.tsx"
CARD_CSS = UI_SRC / "components" / "panels" / "RightLivePanel.module.css"


def strip_ts_comments(text: str) -> str:
    """Drop // and /* */ comments. These files contain no string literal holding
    either marker, which is what lets so plain a scanner be trustworthy here."""
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        pair = text[i:i + 2]
        if pair == "//":
            nl = text.find("\n", i)
            i = n if nl == -1 else nl
        elif pair == "/*":
            end = text.find("*/", i + 2)
            i = n if end == -1 else end + 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


class TestCommentStripping:
    """Without this, a stripper that silently returned its input would make every
    assertion below vacuous — each one would pass on the prose alone."""

    def test_stripper_removes_a_comment_the_card_really_carries(self):
        raw = CARD.read_text()
        assert "// NO DOM TEST REACHES THIS MARKUP." in raw, (
            "the card must keep the header that names this very test as its guard"
        )
        assert "NO DOM TEST REACHES THIS MARKUP." not in strip_ts_comments(raw), (
            "stripper must remove it"
        )

    def test_stripper_removes_a_block_comment_the_card_really_carries(self):
        raw = CARD.read_text()
        assert "COLOUR AND PLACEMENT ARE THIS COMPONENT'S" in raw, (
            "the tone map must keep its WHY comment"
        )
        assert "COLOUR AND PLACEMENT ARE THIS COMPONENT'S" not in strip_ts_comments(raw), (
            "stripper must remove /* */ comments too"
        )


class TestServerTokenReachesTheCard:
    """One spelling per concept at every hop: the prop is `serverToken` from
    `RemedyApp` down to the card, so this chain greps to itself."""

    def test_app_passes_the_url_token_to_the_shell(self):
        code = strip_ts_comments(APP.read_text())
        assert "serverToken={token}" in code, (
            "RemedyApp reads the token out of the URL and is the only place that "
            "does; a card cannot answer unless it is handed down from here"
        )

    def test_shell_passes_the_token_to_the_live_panel(self):
        code = strip_ts_comments(SHELL.read_text())
        assert "serverToken={serverToken}" in code, (
            "the shell must pass the credential on rather than swallow it"
        )
        assert "serverToken: string" in code, (
            "every hop declares the prop in its own props type, which is what "
            "makes tsc --noEmit notice a broken chain"
        )

    def test_live_panel_passes_the_token_to_the_decision_inbox(self):
        code = strip_ts_comments(PANEL.read_text())
        assert "serverToken={serverToken}" in code, (
            "the panel is the last hop before the card that spends the token"
        )
        assert "serverToken: string" in code

    def test_live_panel_addresses_the_dashboard_job_not_the_url(self):
        code = strip_ts_comments(PANEL.read_text())
        assert "jobId={dashboard.jobId}" in code, (
            "the inbox addresses the job the dashboard names, the same value the "
            "stream is opened against (DECISION F008 D3)"
        )

    def test_card_declares_both_halves_of_the_send_target(self):
        code = strip_ts_comments(CARD.read_text())
        assert "serverToken: string" in code
        assert "jobId: string" in code
        assert "{ jobId, serverToken }" in code, (
            "the target is built with NAMED fields, so the transposition finding "
            "R-0684 forbade cannot be expressed at this call site"
        )


class TestAnswerClickCallsTheFlow:
    def test_card_imports_the_flow_from_its_own_module(self):
        code = strip_ts_comments(CARD.read_text())
        assert 'import { answerDecisionCard } from "../../api/decisionAnswerFlow";' in code, (
            "the whole answer sequence lives in a module the shipped vitest "
            "config reaches (DECISION F031 D5)"
        )

    def test_card_calls_the_flow_with_the_target_the_decision_and_the_answer(self):
        code = strip_ts_comments(CARD.read_text())
        assert "answerDecisionCard(target, decision, answer.value)" in code, (
            "one click, one flow: the card must really call it, not merely import it"
        )

    def test_card_reaches_the_network_through_nothing_else(self):
        code = strip_ts_comments(CARD.read_text())
        for forbidden in ("fetch(", "XMLHttpRequest", "buildDecisionSendRequest", "submitDecisionSendRequest"):
            assert forbidden not in code, (
                f"{forbidden} in the component would put a rule in markup no "
                "vitest reaches"
            )


class TestTheSentenceIsRenderedByItsTone:
    def test_card_maps_the_three_tones_to_three_classes(self):
        code = strip_ts_comments(CARD.read_text())
        assert "Record<DecisionOutcomeTone, string>" in code, (
            "a Record lookup is a projection; a switch over a tone would be a "
            "branch this file is not allowed to carry"
        )
        for tone, class_name in (
            ("ok", "decisionOutcomeOk"),
            ("warn", "decisionOutcomeWarn"),
            ("error", "decisionOutcomeError"),
        ):
            assert f"{tone}: styles.{class_name}" in code, f"tone {tone} needs its class"
            assert f".{class_name}" in CARD_CSS.read_text(), (
                f"{class_name} must exist in the stylesheet or the tone renders unstyled"
            )

    def test_card_renders_the_flows_own_sentence(self):
        code = strip_ts_comments(CARD.read_text())
        assert "outcome.sentence" in code, (
            "every word an operator reads comes from decisionOutcome.ts"
        )

    def test_the_sentence_region_announces_itself(self):
        code = strip_ts_comments(CARD.read_text())
        assert 'aria-live="polite"' in code, (
            "the sentence appears under a control the operator just pressed"
        )


class TestTheRetiredAndDeliberateAbsences:
    def test_the_pending_title_is_gone(self):
        code = strip_ts_comments(CARD.read_text())
        assert code.count("ANSWER_PENDING_TITLE") == 0, (
            "the constant said answering arrives later; it arrived, so the "
            "sentence and its disabled button must not survive it"
        )

    def test_the_buttons_are_not_unconditionally_disabled(self):
        code = strip_ts_comments(CARD.read_text())
        assert "disabled={sendingKey === answerKey}" in code, (
            "a button is disabled only while ITS OWN answer is on the wire"
        )

    def test_the_card_never_dispatches_on_a_decisions_type_or_status(self):
        code = strip_ts_comments(CARD.read_text())
        for forbidden in (
            "decision.type ===",
            "decision.type !==",
            "=== decision.type",
            "!== decision.type",
            "decision.status",
            "switch (",
        ):
            assert forbidden not in code, (
                f"{forbidden} would move a real branch into markup no vitest "
                "reaches, which is the absence this component's own header "
                "promises (DECISION F031 D5)"
            )
