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
FLOW = UI_SRC / "api" / "decisionAnswerFlow.ts"


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


def decision_outcome_css_rules(css: str) -> str:
    """Every rule in the stylesheet whose selector names a `.decisionOutcome`
    class, comments already gone. Scoped on purpose: `overflow: hidden` and
    friends live elsewhere in this sheet quite legitimately, and a whole-file
    sweep for a hiding mechanism would read them as this region's."""
    rules: list[str] = []
    for chunk in strip_ts_comments(css).split("}"):
        selector, brace, body = chunk.partition("{")
        if brace and selector.strip().startswith(".decisionOutcome"):
            rules.append(f"{selector.strip()} {{{body}}}")
    return "\n".join(rules)


def css_rule_body(css: str, selector: str) -> str:
    """The BODY of the one rule whose selector is exactly `selector`, comments
    already gone. Scoped for the same reason `decision_outcome_css_rules` is: a
    whole-file sweep would read a neighbouring block's declarations as this
    rule's, and the point of asking for this class is that it has declarations
    of its OWN. The empty string when no such rule exists, which is what an
    absent class looks like to a stylesheet and therefore to a browser."""
    for chunk in strip_ts_comments(css).split("}"):
        head, brace, body = chunk.partition("{")
        if brace and head.strip().rpartition("\n")[2].strip() == selector:
            return body
    return ""


def ts_function_body(code: str, name: str) -> str:
    """The BODY of one top-level `function <name>(...) { ... }`, comments already
    gone. Scoped on purpose (finding R-0689): "only its own key" is implemented
    inside these braces, and a whole-file sweep for a bulk operation would read
    the `useState` initialiser two hundred lines away as this helper's."""
    head = code.index(f"function {name}(")
    opened = code.index("{", head)
    depth = 0
    for i in range(opened, len(code)):
        if code[i] == "{":
            depth += 1
        elif code[i] == "}":
            depth -= 1
            if depth == 0:
                return code[opened + 1:i]
    raise AssertionError(f"function {name} never closes its body brace")


def jsx_between_answer_button_and_live_paragraph(code: str) -> str:
    """Everything the source puts BETWEEN the answer button's closing tag and the
    opening `<p` of the outcome paragraph, comments already gone. ANY conditional
    operator in here gates the live region on something, which is conditional
    creation however it is spelled (finding R-0690)."""
    live = code.rindex('aria-live="polite"')
    tag = code.rindex("<", 0, live)
    assert code.startswith("<p", tag), (
        "the LAST aria-live in this file must be the outcome paragraph's; if it "
        "is not, this reader is aimed at the wrong node and pins nothing"
    )
    closing = code.rindex("</button>", 0, tag) + len("</button>")
    return code[closing:tag]


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
        assert "answerDecisionCard(target, decision, answer.value, clarificationAnswers)" in code, (
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
        assert "disabled={sendingKeys.has(answerKey)}" in code, (
            "a button is disabled only while ITS OWN answer is on the wire, and "
            "it reads its own key alone to know that (finding R-0687)"
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


class TestTheOutcomeRegionExistsBeforeItSpeaks:
    """Finding R-0686. Assistive technology registers a live region when the node
    ENTERS the accessibility tree and announces later MUTATIONS of it, so the
    region must be rendered from a row's first render and only its TEXT may be
    conditional. No source predicate can see the accessibility tree, so what is
    pinned here is the SHAPE that produces it — and, just as hard, the three
    hiding mechanisms that would quietly undo it."""

    def test_the_region_is_rendered_empty_rather_than_created_with_its_sentence(self):
        code = strip_ts_comments(CARD.read_text())
        assert '{outcome === null ? "" : outcome.sentence}' in code, (
            "the paragraph carrying aria-live must exist before there is an "
            "outcome; only the sentence inside it may be conditional"
        )

    def test_the_null_ternary_shape_r0686_was_registered_against_is_absent(self):
        code = strip_ts_comments(CARD.read_text())
        assert "outcome === null ? null :" not in code, (
            "a region inserted already populated announces nothing, which is "
            "exactly the shape finding R-0686 registered"
        )

    def test_the_region_is_created_under_no_conditional_operator_at_all(self):
        region = jsx_between_answer_button_and_live_paragraph(
            strip_ts_comments(CARD.read_text())
        )
        for operator in ("?", "&&", "||"):
            assert operator not in region, (
                f"{operator} between the answer button and the paragraph gates "
                "the live region on something, and a region that arrives with "
                "its first sentence already in it announces nothing. That is "
                "R-0686 whatever the spelling, and the literal check above "
                "holds only one member of the family (finding R-0690)"
            )

    def test_the_empty_region_is_collapsed_out_of_flow(self):
        rules = decision_outcome_css_rules(CARD_CSS.read_text())
        assert ".decisionOutcomeQuiet { position: absolute; }" in rules, (
            "the empty region is collapsed by leaving the flow, which keeps the "
            "node in the accessibility tree and forces no flex line on the "
            "answer strip"
        )

    def test_the_outcome_rules_never_use_a_mechanism_that_removes_the_node(self):
        rules = decision_outcome_css_rules(CARD_CSS.read_text())
        for forbidden in ("display: none", "visibility: hidden"):
            assert forbidden not in rules, (
                f"{forbidden} removes the region from the accessibility tree "
                "and reinstates R-0686 in a form that looks fixed"
            )

    def test_the_card_never_hides_the_region_with_the_hidden_attribute(self):
        code = strip_ts_comments(CARD.read_text())
        assert "hidden" not in code, (
            "the hidden attribute removes the node from the accessibility tree "
            "just as surely as display: none does; the WHY comment naming all "
            "three is stripped before this assertion, so only real markup counts"
        )


class TestOnePressTouchesOnlyItsOwnButton:
    """Finding R-0687. A button must stay disabled until ITS OWN send settles,
    which a single in-flight key could not promise: a second press overwrote it
    and re-enabled the first answer's button mid-flight."""

    def test_a_press_removes_only_its_own_key_when_it_settles(self):
        code = strip_ts_comments(CARD.read_text())
        assert "setSendingKeys((sofar) => withoutAnswerKey(sofar, answerKey))" in code, (
            "a settled send clears its own key out of the set and no other, so "
            "one answer's outcome can never re-enable another's button"
        )

    def test_no_third_writer_can_clear_the_in_flight_set(self):
        code = strip_ts_comments(CARD.read_text())
        assert code.count("setSendingKeys(") == 2, (
            "exactly two writers — the press that adds its key and the settle "
            "that removes it; a third would be the bulk clear this finding is "
            "about"
        )


class TestTheInFlightHelpersTouchOnlyTheirOwnKey:
    """Finding R-0689. The two assertions above read CALL SITES, and a call site
    cannot say what the function it calls does: `next.delete(answerKey)` becoming
    `next.clear()` leaves every one of them green while a settled send clears
    EVERY answer's key and reinstates R-0687. These read the two helper BODIES,
    which is where "only its own" is actually implemented."""

    def test_the_add_helper_copies_the_set_before_it_changes_it(self):
        body = ts_function_body(strip_ts_comments(CARD.read_text()), "withAnswerKey")
        assert "new Set(sending)" in body, (
            "mutating the passed set in place would both skip React's re-render "
            "and make one press the owner of every other answer's disabled state"
        )
        assert "next.delete(" not in body, (
            "and this really is the adder's body alone: the two helpers are "
            "adjacent, so a reader that overshot a closing brace would sweep "
            "both as one and prove nothing about either"
        )

    def test_the_add_helper_adds_the_passed_key_and_nothing_else(self):
        body = ts_function_body(strip_ts_comments(CARD.read_text()), "withAnswerKey")
        assert "next.add(answerKey)" in body, (
            "a press marks ITS OWN answer in flight, named by the key it was "
            "handed rather than by anything this body decides for itself"
        )

    def test_the_remove_helper_copies_the_set_before_it_changes_it(self):
        body = ts_function_body(strip_ts_comments(CARD.read_text()), "withoutAnswerKey")
        assert "new Set(sending)" in body, (
            "the settle path copies too, so a resolved send never edits the set "
            "a still-pending press is holding"
        )
        assert "next.add(" not in body, (
            "and this really is the remover's body alone, by the same argument "
            "the adder's makes"
        )

    def test_the_remove_helper_deletes_the_passed_key_and_nothing_else(self):
        body = ts_function_body(strip_ts_comments(CARD.read_text()), "withoutAnswerKey")
        assert "next.delete(answerKey)" in body, (
            "a settled send takes ITS OWN key out of the set and no other, which "
            "is the whole of finding R-0687 in a single line"
        )

    def test_neither_helper_carries_a_bulk_operation(self):
        code = strip_ts_comments(CARD.read_text())
        for name in ("withAnswerKey", "withoutAnswerKey"):
            body = ts_function_body(code, name)
            for forbidden in (".clear(", "new Set()"):
                assert forbidden not in body, (
                    f"{forbidden} in {name} empties the in-flight set, which "
                    "re-enables every other answer's button mid-flight and "
                    "reinstates R-0687 with every call site left untouched"
                )


class TestTheFlowHeaderNamesItsCard:
    """Finding R-0688. A forward reference written as a ROUND NUMBER resolves to
    nothing a reader can open and goes stale on a schedule nobody tracks."""

    def test_the_header_names_the_component_that_shows_the_sentence(self):
        raw = FLOW.read_text()
        assert "DecisionInboxCard.tsx" in raw, (
            "the card that shows the flow's sentence is a path a reader can "
            "open, and it is the one this header must name"
        )

    def test_the_header_routes_no_reader_to_a_round_number(self):
        raw = FLOW.read_text()
        assert "R37" not in raw, (
            "the sentence being fixed IS a comment, so this one reads the RAW "
            "text: stripping would delete the very evidence"
        )


class TestARefusedAnswerIsTextRatherThanAButton:
    """Finding R-0693, DECISION F031 D22. The write door answers exactly one of
    the eight producing decision types, so an enabled button on the other seven
    claims a send that would be refused. The model stamps `posts` per answer and
    this component projects it; without the guards below the text branch is
    UNGUARDED — the existing R-0686 region reader forbids the wrong ORDER but
    never requires the right RENDER, so a component that simply kept posting
    buttons everywhere would leave every assertion above green."""

    def test_the_card_discriminates_on_the_per_answer_posts_flag(self):
        code = strip_ts_comments(CARD.read_text())
        assert "answer.posts ?" in code, (
            "the choice between a control and pasteable text is made from the "
            "boolean decisionCard.ts derived, which is the only reading that "
            "keeps DECISION F031 D5's rule out of markup no vitest reaches"
        )

    def test_a_refused_answer_renders_its_value_as_pasteable_text(self):
        code = strip_ts_comments(CARD.read_text())
        assert "<code className={styles.decisionAnswerText}>{answer.value}</code>" in code, (
            "the command must stay ON SCREEN and carry the answer's own value: "
            "hiding a refused answer would lose the question, which is the one "
            "thing this inbox exists not to do"
        )

    def test_the_conditional_sits_before_the_button_and_never_after_it(self):
        code = strip_ts_comments(CARD.read_text())
        choice = code.index("answer.posts ?")
        live = code.rindex('aria-live="polite"')
        tag = code.rindex("<", 0, live)
        closing = code.rindex("</button>", 0, tag)
        assert choice < closing, (
            "the button is the ternary's TRUE arm, so the `?` lands before the "
            "button's closing tag rather than inside the region the reader "
            "below sweeps; the other order fails a live-region check for a "
            "reason that has nothing to do with the live region"
        )

    def test_the_pasteable_text_class_really_has_a_rule_in_the_stylesheet(self):
        body = css_rule_body(CARD_CSS.read_text(), ".decisionAnswerText")
        assert body.strip(), (
            "a className with no rule behind it renders the command with the "
            "browser's default `code` styling and none of this card's"
        )
        assert "user-select: all" in body, (
            "one click must select the whole command — pasteable is the point "
            "of the affordance, not a description of it"
        )
        assert "var(--remedy-font-mono)" in body, (
            "it is a command, and it says so in the mono face this repository "
            "already defines rather than in a font this rule invents"
        )

    def test_the_pasteable_text_is_not_dressed_as_a_control(self):
        body = css_rule_body(CARD_CSS.read_text(), ".decisionAnswerText")
        for forbidden in ("cursor: pointer", "background:", "border:"):
            assert forbidden not in body, (
                f"{forbidden} gives the text button chrome, and the chrome is "
                "exactly what made the refused affordance lie (R-0693)"
            )


class TestTheClarificationFormIsFilledFromTheCard:
    """DECISION F031 D24. A pending flight-plan approval carries still-open
    questions, and until now no caller ever filled the `answers` map that
    `answerDecisionCard` has accepted since the write channel learned it. The
    card now renders one field per question and hands the collected map on.

    THE ONE RULE THAT CANNOT BE SPELLED HERE IS A PREFILL. The server reads a
    blank or absent answer as "accept this question's default", so a field
    carrying the default as its VALUE would post the default as though the
    operator had typed it — silently answering a question nobody read. The
    default is shown as text BESIDE the field, and the two assertions below are
    what make that difference mechanical rather than a matter of care."""

    def test_the_card_imports_both_form_rules_from_their_own_module(self):
        code = strip_ts_comments(CARD.read_text())
        assert (
            'import { collectDecisionClarificationAnswers, decisionClarificationFieldKey } '
            'from "../../api/decisionClarificationForm";'
        ) in code, (
            "the key rule and the collection rule live in a module the shipped "
            "vitest config reaches (DECISION F031 D5); a card that reimplemented "
            "either would put it where no suite can see it"
        )

    def test_the_field_reads_the_store_under_its_own_key_and_falls_back_to_empty(self):
        code = strip_ts_comments(CARD.read_text())
        assert 'value={clarificationValues[fieldKey] ?? ""}' in code, (
            "the field's value is the operator's typing under THIS field's key "
            "and nothing else; the fallback is the EMPTY STRING, because the "
            "blank is exactly what the server reads as accepting the default"
        )

    def test_a_questions_default_is_never_an_inputs_value(self):
        code = strip_ts_comments(CARD.read_text())
        for forbidden in (
            "value={clarification.defaultAnswer}",
            "?? clarification.defaultAnswer",
            "|| clarification.defaultAnswer",
        ):
            assert forbidden not in code, (
                f"{forbidden} prefills the field with the default, which posts "
                "it as though it had been typed (DECISION F031 D24)"
            )
        assert code.count("clarification.defaultAnswer") == 1, (
            "the default is read exactly once, for the line that SHOWS it; a "
            "second reader is the prefill arriving under another spelling"
        )
        shown = code[code.index("clarification.defaultAnswer"):]
        assert shown.startswith("clarification.defaultAnswer}`;"), (
            "and that one reader is the visible meta line, not an attribute"
        )

    def test_the_field_block_sits_above_the_answer_strip(self):
        code = strip_ts_comments(CARD.read_text())
        fields = code.index("styles.decisionClarifications")
        answers = code.index("styles.decisionAnswers")
        assert fields < answers, (
            "the operator reads what the plan is waiting on BEFORE the control "
            "that resolves it, and the guard reading the live region sweeps "
            "everything after the last answer button (finding R-0690): a field "
            "block below the strip would land inside that region"
        )

    def test_every_field_class_the_card_names_has_a_rule_of_its_own(self):
        code = strip_ts_comments(CARD.read_text())
        css = CARD_CSS.read_text()
        for class_name in (
            "decisionClarifications",
            "decisionClarification",
            "decisionClarificationQuestion",
            "decisionClarificationInput",
            "decisionClarificationMeta",
        ):
            assert f"styles.{class_name}" in code, f"the card must name {class_name}"
            assert css_rule_body(css, f".{class_name}").strip(), (
                f"{class_name} has no rule behind it, so the field renders with "
                "the browser's defaults and none of this card's"
            )


class TestTheCardShowsTheEvidenceTriple:
    """T5_F032 T003b. The model has carried the triple since T003a — a card's
    `evidenceRefs` and `evidenceNote`, and each answer's own `expectedOutcome`
    and `downside` — and until this round nothing rendered any of it, which is
    the whole of F032's promise unkept: no decision without its receipts.

    TWO THINGS ARE PINNED HERE AND THEY PULL IN OPPOSITE DIRECTIONS. That the
    four fields really reach the markup, and that the ONE field beside them
    never does: §17 of docs/ui/design_reference/ux_spec.md forbids the default
    UI to show a raw id, and a ref's `target` is frequently exactly one — a test
    run id, an escalation id — carried on the model only for the deep link the
    next task adds."""

    # Every empty state this round introduces, collapsed the way the outcome
    # region already is. Named once, here, so the two readings below — that the
    # collapse EXISTS and that it uses no mechanism removing the node — can
    # never drift apart and leave one selector read by only one of them.
    COLLAPSE_SELECTORS = (
        ".decisionEvidence:empty",
        ".decisionEvidenceNote:empty",
        ".decisionExpectedOutcome:empty",
        ".decisionDownside:empty",
    )

    def test_the_card_maps_the_models_evidence_refs(self):
        code = strip_ts_comments(CARD.read_text())
        assert "decision.evidenceRefs.map(" in code, (
            "the receipts behind a decision must reach the operator who is "
            "being asked to approve it; the model has carried them since T003a"
        )

    def test_the_card_renders_the_note_that_says_why_there_are_none(self):
        code = strip_ts_comments(CARD.read_text())
        assert "{decision.evidenceNote}" in code, (
            "a card with no receipts says so in the model's own sentence — the "
            "raw evidence_status is the present/missing signal §17 excludes, "
            "which is why the model turns it into prose before it gets here"
        )

    def test_each_answer_shows_its_own_expected_outcome_and_downside(self):
        code = strip_ts_comments(CARD.read_text())
        for field in ("{answer.expectedOutcome}", "{answer.downside}"):
            assert field in code, (
                f"{field} must ride under the answer it belongs to: consent is "
                "informed by the option actually being pressed, which is why "
                "T003a hung both on the ANSWER rather than on the card"
            )

    def test_no_refs_target_ever_reaches_the_markup(self):
        code = strip_ts_comments(CARD.read_text())
        assert code.count(".target") == 1, (
            "a ref's target is frequently a raw id and §17 forbids the default "
            "UI to show one, so the only `.target` this component may carry is "
            "the DOM event's; a second occurrence is the leak arriving under "
            "whatever name the map's variable happens to have"
        )
        assert "const typed = event.target.value;" in code, (
            "and the survivor really is the clarification input's own event "
            "target, which has nothing to do with a ref's"
        )

    def test_every_receipt_class_the_card_names_has_a_rule_of_its_own(self):
        code = strip_ts_comments(CARD.read_text())
        css = CARD_CSS.read_text()
        for class_name in (
            "decisionEvidence",
            "decisionEvidenceChip",
            "decisionEvidenceNote",
            "decisionExpectedOutcome",
            "decisionDownside",
        ):
            assert f"styles.{class_name}" in code, f"the card must name {class_name}"
            assert css_rule_body(css, f".{class_name}").strip(), (
                f"{class_name} has no rule behind it, so the receipt renders "
                "with the browser's defaults and none of this card's"
            )

    def test_every_new_empty_state_is_collapsed_out_of_flow(self):
        css = CARD_CSS.read_text()
        for selector in self.COLLAPSE_SELECTORS:
            assert "position: absolute" in css_rule_body(css, selector), (
                f"{selector} must leave the flow: a card with no receipts and "
                "an answer with no stakes would otherwise still claim their "
                "parent's gap and show as stray blank bands"
            )

    def test_the_new_collapse_rules_never_remove_the_node(self):
        css = CARD_CSS.read_text()
        for selector in self.COLLAPSE_SELECTORS:
            body = css_rule_body(css, selector)
            for forbidden in ("display: none", "visibility: hidden"):
                assert forbidden not in body, (
                    f"{forbidden} in {selector} removes the node from the "
                    "accessibility tree, which is finding R-0686 reinstated in "
                    "a form that looks tidy"
                )
        code = strip_ts_comments(CARD.read_text())
        assert "hidden" not in code, (
            "and the attribute spelling is excluded here too, over the whole "
            "file: the regions this class pins live in it, so a class name or "
            "an attribute carrying it would hide one of them just as surely"
        )

    def test_the_answer_stakes_sit_after_the_live_region_and_add_no_operator(self):
        code = strip_ts_comments(CARD.read_text())
        # The module's own reader, not a second one of the same shape: it
        # asserts the LAST aria-live in the file is still the outcome
        # paragraph's, which is exactly what a stakes paragraph carrying one of
        # its own would break.
        region = jsx_between_answer_button_and_live_paragraph(code)
        for operator in ("?", "&&", "||"):
            assert operator not in region, (
                f"{operator} between the answer button and the paragraph gates "
                "the live region on something (finding R-0690); the stakes are "
                "strings the model guarantees, EMPTY rather than absent, so "
                "rendering them needs no operator at all"
            )
        live = code.rindex('aria-live="polite"')
        for field in ("{answer.expectedOutcome}", "{answer.downside}"):
            assert code.index(field) > live, (
                f"{field} must sit AFTER the outcome paragraph in source order "
                "or the reader above aims at the wrong node and pins nothing"
            )


class TestTheReceiptIsAnEntryPointRatherThanALink:
    """T5_F032 T003c, DECISION F032 D8. The evidence panel the feature file sends
    these chips to is `docs/roadmap/features/T5_F023.md` T003 and F023 is
    unclaimed, so F032 ships the ENTRY POINT and F023 wires it: the card takes an
    OPTIONAL `onOpenEvidence` handler, a receipt renders as a control only when
    one is supplied, and the plain chip T003b shipped is what every card in this
    release still shows.

    NOTHING RUNS THE HANDLER'S ARM. No call site supplies the prop, this
    repository has no DOM environment, and the shipped vitest config reaches
    none of this markup — so what stands between the two arms and a silent
    regression is `tsc --noEmit` and the readings below, and they are written to
    fail on the two ways the honesty could be lost: a control that appears with
    no handler behind it, and a handler handed a FIELD of a ref instead of the
    ref itself, which is how a raw `target` would start travelling alone."""

    def test_the_props_type_declares_the_optional_handler(self):
        code = strip_ts_comments(CARD.read_text())
        assert "onOpenEvidence?: (evidenceRef: DecisionEvidenceRef) => void;" in code, (
            "the handler is declared in the card's own props type and is "
            "OPTIONAL, which is the whole reason no existing call site had to "
            "change; a required prop would make F032 edit RightLivePanel for a "
            "panel that does not exist yet"
        )
        assert "onSelectNode, onOpenEvidence }" in code, (
            "and it is really destructured beside the callback it sits next to; "
            "a prop declared but never taken out of the object is a type that "
            "pins nothing"
        )

    def test_the_ref_type_is_imported_as_a_type_from_the_model_module(self):
        code = strip_ts_comments(CARD.read_text())
        assert (
            'import type { DecisionCardModel, DecisionEvidenceRef } '
            'from "../../api/decisionCard";'
        ) in code, (
            "the ref's shape is the model module's, imported as a TYPE so no "
            "value crosses at runtime, and it joins the line already importing "
            "from that module rather than opening a second one"
        )
        assert 'import type { DecisionEvidenceRef }' not in code, (
            "one import line per module: a second type import from "
            "decisionCard would be the synonym drift AGENTS.md forbids, spelled "
            "in import statements"
        )

    def test_the_control_arm_hands_the_handler_the_whole_ref(self):
        code = strip_ts_comments(CARD.read_text())
        assert code.count("onOpenEvidence(") == 1, (
            "exactly one call site: a second would be a rule about a receipt "
            "arriving in markup no vitest reaches (DECISION F031 D5)"
        )
        call = code[code.index("onOpenEvidence("):]
        assert call.startswith("onOpenEvidence(evidenceRef)"), (
            "the handler takes the WHOLE ref, so the panel F023 builds reads "
            "`kind` and `target` for itself and this component reads neither; "
            "handing it a field instead is how a raw id starts travelling alone "
            "and is the leak §17 of docs/ui/design_reference/ux_spec.md forbids"
        )
        assert "onClick={() => onOpenEvidence(evidenceRef)}" in code, (
            "and the call really is the receipt's click, not a bare reference "
            "the markup never invokes"
        )

    def test_a_card_with_no_handler_still_renders_the_plain_chip(self):
        code = strip_ts_comments(CARD.read_text())
        assert "onOpenEvidence ? (" in code, (
            "the discriminator is the PRESENCE of the handler and nothing this "
            "file reads off the ref, which is the jump chip's own rule one row "
            "above: only a receipt that can really open something gets the "
            "control, so the affordance never lies"
        )
        assert (
            "<span key={`${evidenceIndex}-${evidenceRef.label}`} "
            "className={styles.decisionEvidenceChip}>"
        ) in code, (
            "the span arm is what every card in this release renders, because "
            "nothing supplies the handler yet; losing it would ship a pressable "
            "chip with no panel behind it (finding R-0693's shape)"
        )
        arm = code[code.index("onOpenEvidence ? ("):code.index("<span key={`${evidenceIndex}")]
        assert "<button" in arm and 'type="button"' in arm, (
            "and the control arm is a real button with an explicit type, not a "
            "clickable span: a span carries no keyboard affordance at all, and "
            "a button with no type submits the form it may one day sit in"
        )

    def test_both_arms_wear_the_same_receipt_class(self):
        code = strip_ts_comments(CARD.read_text())
        assert code.count("className={styles.decisionEvidenceChip}") == 2, (
            "exactly two arms and both wear the receipt class: a receipt must "
            "read as the same object whether or not it can be pressed, and a "
            "second class here would make the entry point a different chip"
        )

    def test_the_pressable_receipt_shows_where_the_keyboard_is(self):
        body = css_rule_body(CARD_CSS.read_text(), "button.decisionEvidenceChip:focus-visible")
        assert body.strip(), (
            "a control with no focus-visible rule of its own is invisible to "
            "the keyboard operator the moment it takes focus"
        )
        assert "outline: 2px solid var(--remedy-blue-strong)" in body, (
            "the ring is the one .decisionJumpChip already spells, in a custom "
            "property tokens.css really defines — an unresolved one would drop "
            "the whole declaration and leave no ring at all (R-0661)"
        )
        assert "outline-offset: 2px" in body, (
            "and it sits off the pill's own border, or the ring reads as part "
            "of the chip rather than as focus"
        )
        assert "outline: none" not in body, (
            "removing the outline is the regression this whole test exists to "
            "catch, and it is spelled in one declaration"
        )
        pressable = css_rule_body(CARD_CSS.read_text(), "button.decisionEvidenceChip")
        assert "cursor: pointer" in pressable, (
            "the control arm says it is pressable under the mouse too, exactly "
            "as .decisionJumpChip does"
        )
        assert "cursor: pointer" not in css_rule_body(CARD_CSS.read_text(), ".decisionEvidenceChip"), (
            "and the SHARED rule stays untouched: a pointer cursor on the span "
            "arm would dress an inert chip as a control, which is the lie "
            "R-0693 registered"
        )
