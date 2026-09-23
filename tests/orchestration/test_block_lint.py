"""`remedy integrity block`: each rule, the command, and the guard on the items the rules cite.

T2_F279 T003 and DECISION F279 D5. The checklist in `docs/agents/planner_reviewer_prompt.md` §3
retires a merged item's number for good and never renumbers the survivors, so a rule citing a
retired number would enforce a rule the checklist no longer states. The guard below reads the
live item numbers from the checklist itself and holds every rule to one of them, and to a
sentence that item really contains.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pytest

from packages.orchestration.block_lint import (
    CHECKLIST_PATH,
    RULES,
    lint_block,
    live_checklist_items,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SHA = "0" * 64


def _normalized(text: str) -> str:
    return " ".join(text.split())


def _items() -> dict[int, str]:
    return live_checklist_items((REPO_ROOT / CHECKLIST_PATH).read_text(encoding="utf-8"))


def _by_item(results, item):
    return next(r for r in results if r.item == item)


def _fake_repo(tmp_path, *, ledger="", archive=""):
    (tmp_path / ".agent").mkdir()
    (tmp_path / ".agent" / "live_review.md").write_text(ledger, encoding="utf-8")
    (tmp_path / ".agent" / "live_review_archive.md").write_text(archive, encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_here.py").write_text("", encoding="utf-8")
    return tmp_path


class TestTheRulesCiteLiveItems:
    def test_the_checklist_parse_sees_the_live_items_and_not_the_retired_ones(self):
        items = _items()
        assert {1, 10, 31, 37} <= set(items)
        assert {17, 19, 32} & set(items) == set()

    def test_no_rule_references_a_retired_item_number(self):
        live = set(_items())
        assert [rule.item for rule in RULES if rule.item not in live] == []

    def test_every_rule_quotes_a_sentence_its_item_really_contains(self):
        items = _items()
        for rule in RULES:
            assert _normalized(rule.sentence) in _normalized(items[rule.item]), rule.item

    def test_one_result_per_rule_in_item_order(self):
        results = lint_block("x\n")
        assert [r.item for r in results] == [rule.item for rule in RULES]
        assert [r.item for r in results] == sorted(r.item for r in results)


class TestEachRule:
    def test_size_counts_lines_against_four_hundred(self, tmp_path):
        assert _by_item(lint_block("a\n" * 400, tmp_path), 1).ok
        assert not _by_item(lint_block("a\n" * 401, tmp_path), 1).ok

    def test_a_plan_payload_must_stay_under_fifty_lines(self, tmp_path):
        ok = lint_block(f"| plan.md | 49 | 10 | {SHA} |\n", tmp_path)
        over = lint_block(f"| plan.md | 50 | 10 | {SHA} |\n", tmp_path)
        assert _by_item(ok, 3).ok and not _by_item(over, 3).ok
        assert "plan.md at 50 lines" in _by_item(over, 3).detail

    def test_a_stated_open_count_is_recomputed_from_the_ledger(self, tmp_path):
        repo = _fake_repo(tmp_path, ledger="- R-0001 — Low, a.\n- R-0002 — Low, b.\nDone: R-0002 — fixed.\n")
        assert _by_item(lint_block("the open-findings count, 1\n", repo), 10).ok
        wrong = _by_item(lint_block("the open-findings count, 2\n", repo), 10)
        assert not wrong.ok and "holds 1" in wrong.detail

    def test_a_stated_count_is_the_open_set_after_the_payloads_the_block_names(self, tmp_path):
        """R-1041: a block that registers one id and resolves one states the count AFTER."""
        repo = _fake_repo(tmp_path, ledger="- R-0001 — Low, a.\n- R-0002 — Low, b.\n")
        payloads = repo / ".remedy-wt" / "fx-r1-payloads"
        payloads.mkdir(parents=True)
        (payloads / "ledger.diff").write_text(
            "--- a/.agent/live_review.md\n+++ b/.agent/live_review.md\n@@ -2 +2,5 @@\n"
            " - R-0002 — Low, b.\n+\n+- R-0003 — Low, a new one.\n+\n"
            "+Done: R-0001 — repaired.\n", encoding="utf-8")
        (payloads / "plan.md").write_text("- R-0009 — Low, quoted in a plan, not booked.\n",
                                          encoding="utf-8")
        head = (f"PAYLOADS — under `.remedy-wt/fx-r1-payloads/`.\n| ledger.diff | 7 | 1 | {SHA} |\n"
                f"| plan.md | 1 | 1 | {SHA} |\n")
        after = _by_item(lint_block(head + "the open-findings count, 2\n", repo), 10)
        assert after.ok, after.detail
        assert after.detail == ("states 2; .agent/live_review.md holds 2 open by distinct id, and the "
                                "block registers 1 and resolves 1, leaving 2")
        before = _by_item(lint_block(head + "the open-findings count, 3\n", repo), 10)
        assert not before.ok and "leaving 2" in before.detail

    def test_only_lines_a_diff_adds_to_the_ledger_count(self, tmp_path):
        repo = _fake_repo(tmp_path, ledger="- R-0001 — Low, a.\n- R-0002 — Low, b.\n")
        payloads = repo / ".remedy-wt" / "fx-r2-payloads"
        payloads.mkdir(parents=True)
        (payloads / "ledger.diff").write_text(
            "--- a/.agent/live_review.md\n+++ b/.agent/live_review.md\n@@ -1,2 +1 @@\n"
            "-Done: R-0002 — a line this diff removes.\n"
            "--- a/.agent/decisions.md\n+++ b/.agent/decisions.md\n@@ -1 +1,2 @@\n"
            "+Done: R-0001 — a decision quoting a resolution.\n", encoding="utf-8")
        head = f"under `.remedy-wt/fx-r2-payloads/`\n| ledger.diff | 7 | 1 | {SHA} |\n"
        check = _by_item(lint_block(head + "the open-findings count, 2\n", repo), 10)
        assert check.ok, check.detail
        assert "registers 0 and resolves 0, leaving 2" in check.detail

    def test_a_path_a_command_names_must_resolve_unless_the_block_creates_it(self, tmp_path):
        repo = _fake_repo(tmp_path)
        fence = "```\npython3 -m pytest tests/test_here.py tests/test_new.py\n```\n"
        missing = _by_item(lint_block(fence, repo), 24)
        assert not missing.ok and "tests/test_new.py" in missing.detail
        declared = "a NEW FILE at `tests/test_new.py`\n" + fence
        assert _by_item(lint_block(declared, repo), 24).ok

    def test_a_minted_id_must_be_new_to_the_ledger_and_the_archive(self, tmp_path):
        repo = _fake_repo(tmp_path, ledger="- R-0001 — Low, a.\n", archive="- R-0002 — Low, b.\n")
        assert _by_item(lint_block("- R-0003 — Low, c.\n", repo), 30).ok
        for taken in ("R-0001", "R-0002"):
            assert not _by_item(lint_block(f"- {taken} — Low, again.\n", repo), 30).ok
        assert not _by_item(lint_block("- R-0003 — Low, c.\n- R-0003 — Low, c.\n", repo), 30).ok

    def test_a_gate_the_handback_quotes_may_not_run_after_it(self, tmp_path):
        head = "G1 to G2 run before C4 is written.\n"
        good = head + "G1 TRANSPORT — at C1.\nG2 TESTS — at C3.\nG3 TREE — after C4: status.\n"
        bad = head + "G1 TRANSPORT — at C1.\nG2 TREE — after C4: status.\n"
        assert _by_item(lint_block(good, tmp_path), 31).ok
        late = _by_item(lint_block(bad, tmp_path), 31)
        assert not late.ok and "G2 runs after C4" in late.detail

    def test_a_run_of_one_repeated_character_is_refused_but_a_code_fence_is_not(self, tmp_path):
        assert _by_item(lint_block("```\nls\n```\n", tmp_path), 37).ok
        run = _by_item(lint_block("title\n━━━━━━━━\n", tmp_path), 37)
        assert not run.ok and "lines 2" in run.detail


class TestTheCommand:
    def _run(self, path, capsys, *, json_output=True):
        from apps.cli.commands.integrity_cmd import _cmd_integrity_block

        code = 0
        try:
            _cmd_integrity_block(argparse.Namespace(path=str(path), json=json_output))
        except SystemExit as exc:
            code = exc.code
        return code, capsys.readouterr().out

    def test_a_clean_block_exits_zero_with_one_result_per_rule(self, tmp_path, capsys):
        block = tmp_path / "block.md"
        block.write_text("STEP\nnothing to check\n", encoding="utf-8")
        code, out = self._run(block, capsys)
        document = json.loads(out)
        assert code == 0 and document["ok"] is True and document["violations"] == 0
        assert [r["item"] for r in document["results"]] == [rule.item for rule in RULES]

    def test_a_violation_exits_one_and_names_its_item(self, tmp_path, capsys):
        block = tmp_path / "block.md"
        block.write_text("x\n" * 401, encoding="utf-8")
        code, out = self._run(block, capsys)
        document = json.loads(out)
        assert code == 1 and document["error"] == "block_lint_failed"
        assert [r["item"] for r in document["results"] if not r["ok"]] == [1]

    def test_text_mode_prints_one_line_per_item(self, tmp_path, capsys):
        block = tmp_path / "block.md"
        block.write_text("x\n" * 401, encoding="utf-8")
        code, out = self._run(block, capsys, json_output=False)
        assert code == 1
        assert len(re.findall(r"^  \[(?:OK|FAIL)\] item \d+ ", out, re.M)) == len(RULES)
        assert "[FAIL] item 1 (size): 401 lines, limit 400" in out

    def test_a_missing_block_is_refused(self, tmp_path, capsys):
        code, out = self._run(tmp_path / "absent.md", capsys)
        assert code == 1 and json.loads(out)["error"] == "block_not_found"


@pytest.mark.parametrize("block", sorted((REPO_ROOT / ".agent" / "authored").glob("f279-r*-block.md")))
def test_this_features_own_blocks_pass_the_size_and_plan_items(block):
    """The blocks F279 itself shipped are the first real input the rules met."""
    results = lint_block(block.read_text(encoding="utf-8"))
    assert _by_item(results, 1).ok and _by_item(results, 3).ok
