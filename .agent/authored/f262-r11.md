═══════════════════════════════════════════════════════════════
STEP — F262 R11/? — review.list gains a CREATED date end to end
═══════════════════════════════════════════════════════════════

GOAL: Give `review.list` a CREATED date end to end, the same shape as R9's patch.list and R10's loop.list batches: `ReviewerRecommendation` gains a `created_at` field stamped once at construction time in `run_reviewer()`, persisted through `store_recommendations()`, surfaced automatically in `--json` (no separate change needed there — `_cmd_review_list`'s json branch already prints `list_recommendations()`'s own dicts verbatim) and rendered as a `(created=...)` suffix in the text branch. Also book round 10's reviewer verdict into the ledger.

BACKGROUND FACTS (already verified by the reviewer — do not re-derive):
- `packages/orchestration/reviewer.py`'s `ReviewerRecommendation` dataclass currently has NO timestamp field at all, and `store_recommendations()`'s persisted dict has no `created_at` key either — this is a real, unexcused gap (unlike execution.list/worker.list/config.list, which are separately excused in `.agent/plan.md`'s Risks section for having no timestamp concept or a pre-existing quirk).
- `apps/cli/commands/review_cmd.py`'s `_cmd_review_list` already has full `--json`/text branches and `supports_json=True` is already set in the catalog — this round only adds the date field, not `--json` support itself (unlike R6/R7/R10 which added `--json` from scratch).
- There is currently NO dedicated CLI test file for `review_cmd.py` (no `tests/cli/test_review_cmd.py`). This round creates one, matching the repo's naming convention (`test_x.py` covers `x.py`, AGENTS.md "Code Discoverability Conventions").
- `tests/orchestration/test_approval_queue.py`'s `TestReviewerLoop` class already exercises `run_reviewer`/`store_recommendations`/`list_recommendations` directly (no CLI layer) — this round adds one more test there for the round-trip of the new field.

═══ COMMIT SEQUENCE (5 commits total) ═══

──────────────────────────────────────────────────────────
C0a — save this entire step block verbatim
──────────────────────────────────────────────────────────
Save the FULL literal text of this prompt message (everything between the "STEP —" header above and the final "END OF BLOCK" marker at the bottom) to `.agent/authored/f262-r11.md`, byte for byte, exactly as received. Commit message: `F262 R11 C0a: save block verbatim to .agent/authored/f262-r11.md`

──────────────────────────────────────────────────────────
C0b — mirror to .agent/last_block.md
──────────────────────────────────────────────────────────
Copy `.agent/authored/f262-r11.md` to `.agent/last_block.md`, whole-file replace. Verify `sha256sum` of both files matches after writing. Commit message: `F262 R11 C0b: mirror block to .agent/last_block.md`

──────────────────────────────────────────────────────────
C1 — append GATE10 to .agent/live_review.md
──────────────────────────────────────────────────────────
Append exactly the text between the GATE10 markers below to the END of `.agent/live_review.md`: one newline, then the GATE10 text verbatim (it is a SINGLE LINE — no internal newlines), nothing else added.

<<<BEGIN GATE10>>>
Gate: R10 — the F262 R10 entry. R10 SHIPPED T002 BATCH 8, loop.list gains --json end to end (catalog args gain _JSON_OPT + supports_json=True, handler json_output kwarg + json branch sourcing last_run_created_at/last_run_state from the existing last_run_for_loop() call, dispatch lambda passes json_output=args.json) — AND THE REVIEWER RE-RAN EVERY GATE ITSELF. TRANSPORT HELD: `.agent/authored/f262-r10.md`/`.agent/last_block.md` share one sha256 digest, `bfdaf95dbb4abdc8c6adcc94917a62ddf503eb54cdaef734e0adb09b47b9a46a`, confirmed by the reviewer's own sha256sum of both committed files. THE DIFF WAS READ, NOT ONLY GATED: `git diff 9adfbc53..9aaaedcb` for command_catalog.py and loop_cmd.py shows exactly PAIR P1 (json import), PAIR P2 (_cmd_loop_list gains json_output kwarg and a json branch, tail unchanged), PAIR P3 (loop.list CommandEntry gains _JSON_OPT and supports_json=True), PAIR P4 (dispatch lambda), every other line in both files untouched, confirmed by reading the full diff. `python3 -m py_compile` exited 0 on all three touched files (command_catalog.py, loop_cmd.py, test_loop_cmd.py), run together by the reviewer. THE GATE9 LEDGER APPEND (commit b5c152d1) WAS RE-VERIFIED BYTE-EXACT: base (2443709 bytes) + one newline + GATE9 (3112 bytes, 0 internal newlines) reproduces the post-commit file (2446822 bytes) exactly. THE PROSE_SLIP APPEND (same commit) WAS RE-VERIFIED BYTE-EXACT the same way: base 72104 + one newline + the 893-byte slip reproduces 72998 exactly. THE TESTS MOVED EXACTLY AS THE HANDBACK CLAIMED, reproduced independently: `tests/cli/test_loop_cmd.py tests/test_command_catalog.py` read 41 passed. ONE DEVIATION VERIFIED AS HONEST, NOT A DEFECT: PAIR P4's new `_cmd_loop_list(json_output=args.json)` dispatch made three PRE-EXISTING tests calling the bare `_dispatch(command_id)` helper (which builds an attribute-less Namespace) fail with `AttributeError: 'Namespace' object has no attribute 'json'`; the worker's fix — switching those three call sites to the file's own pre-existing `_dispatch_with(command_id, **attributes)` helper with `json=False` — is confirmed present in the diff, does not touch PAIR P1-P5/T1-T2 themselves, and `_dispatch_with` is confirmed pre-existing (already used by every `loop.run` test in the same file before this round). THE STATE READERS AND THE CANARY WERE UNMOVED, reproduced by the reviewer: `tests/ui_server/` 515, and the four-file combined run (`test_test_runner.py`, `test_resource_safety.py`, `test_integrity_gate.py`, `test_golden_path.py`) 131 passed (52+21+16+42). HYGIENE HELD: `git status --porcelain` empty at HEAD `c37fd166`, `git ls-files .remedy-wt` empty, `.agent/STOP` absent. THE PLAN HELD: `.agent/plan.md` measured 1928 bytes, matching the handback's own reported byte-for-byte comparison of the authored PLAN11 slice against the written file. THE VERDICT IS PASS.
<<<END GATE10>>>

Commit message: `F262 R11 C1: append GATE10 to live_review.md - books round 10's PASS verdict`

──────────────────────────────────────────────────────────
C2 — production pairs + tests (one commit, two production files, two test files)
──────────────────────────────────────────────────────────

PAIR P1 (REWRITE) — `packages/orchestration/reviewer.py`, add the `datetime`/`timezone` import.
FROM (exact):
<<<BEGIN PAIR_P1_FROM>>>
from dataclasses import dataclass
from typing import Any
<<<END PAIR_P1_FROM>>>
TO:
<<<BEGIN PAIR_P1_TO>>>
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
<<<END PAIR_P1_TO>>>
Verify FROM occurs exactly once in the file before applying.

PAIR P2 (APPEND) — `packages/orchestration/reviewer.py`, `ReviewerRecommendation` gains a `created_at` field.
FROM (exact):
<<<BEGIN PAIR_P2_FROM>>>
    source: str = "reviewer"
    origin_task_id: str = ""
    status: str = "pending"  # pending, accepted, rejected
<<<END PAIR_P2_FROM>>>
TO:
<<<BEGIN PAIR_P2_TO>>>
    source: str = "reviewer"
    origin_task_id: str = ""
    status: str = "pending"  # pending, accepted, rejected
    created_at: str = ""
<<<END PAIR_P2_TO>>>
Verify FROM occurs exactly once in the file before applying. This pair is APPEND-shaped: TO contains FROM verbatim as a prefix.

PAIR P3 (REWRITE) — `packages/orchestration/reviewer.py`, `run_reviewer()` stamps `created_at` at construction time.
FROM (exact):
<<<BEGIN PAIR_P3_FROM>>>
            source="reviewer",
            origin_task_id=after_task_id or "",
        )
<<<END PAIR_P3_FROM>>>
TO:
<<<BEGIN PAIR_P3_TO>>>
            source="reviewer",
            origin_task_id=after_task_id or "",
            created_at=datetime.now(timezone.utc).isoformat(),
        )
<<<END PAIR_P3_TO>>>
Verify FROM occurs exactly once in the file before applying.

PAIR P4 (REWRITE) — `packages/orchestration/reviewer.py`, `store_recommendations()` persists `created_at` in the saved dict.
FROM (exact):
<<<BEGIN PAIR_P4_FROM>>>
            "origin_task_id": rec.origin_task_id,
            "status": rec.status,
        })
<<<END PAIR_P4_FROM>>>
TO:
<<<BEGIN PAIR_P4_TO>>>
            "origin_task_id": rec.origin_task_id,
            "status": rec.status,
            "created_at": rec.created_at,
        })
<<<END PAIR_P4_TO>>>
Verify FROM occurs exactly once in the file before applying.

PAIR P5 (REWRITE) — `apps/cli/commands/review_cmd.py`, `_cmd_review_list`'s text branch gains a `created=` suffix.
FROM (exact):
<<<BEGIN PAIR_P5_FROM>>>
        for r in recs:
            status = r.get("status", "?")
            title = r.get("title", "?")
            rid = r.get("id", "?")
            print(f"  [{status}] {rid}  {title}")
<<<END PAIR_P5_FROM>>>
TO:
<<<BEGIN PAIR_P5_TO>>>
        for r in recs:
            status = r.get("status", "?")
            title = r.get("title", "?")
            rid = r.get("id", "?")
            created = r.get("created_at", "?")
            print(f"  [{status}] {rid}  {title}  (created={created})")
<<<END PAIR_P5_TO>>>
Verify FROM occurs exactly once in the file before applying. Do NOT touch the JSON branch above this loop or the `if not recs:` early return — both are unchanged; `--json` needs no code change because it already prints `list_recommendations()`'s own dicts verbatim, which will now include `created_at` automatically once P2-P4 land.

TEST T1 (REWRITE) — `tests/orchestration/test_approval_queue.py`, add a round-trip test for the new field, inserted between `test_store_and_list_recommendations` and `test_accept_recommendation`.
FROM (exact):
<<<BEGIN T1_FROM>>>
        assert stored[0]["status"] == "pending"

    def test_accept_recommendation(self, tmp_path, monkeypatch):
<<<END T1_FROM>>>
TO:
<<<BEGIN T1_TO>>>
        assert stored[0]["status"] == "pending"

    def test_store_and_list_recommendations_carries_created_at(self):
        from datetime import datetime

        from packages.orchestration.reviewer import list_recommendations, run_reviewer, store_recommendations

        job = _make_job_s101(1)

        def custom_reviewer(context):
            return [{"title": "Add caching", "task_type": "perf", "reason": "latency"}]

        recs = run_reviewer(job, reviewer_fn=custom_reviewer)
        store_recommendations(job, recs)
        stored = list_recommendations(job)
        assert stored[0]["created_at"] != ""
        datetime.fromisoformat(stored[0]["created_at"])

    def test_accept_recommendation(self, tmp_path, monkeypatch):
<<<END T1_TO>>>
Verify FROM occurs exactly once in the file before applying. This class (`TestReviewerLoop`) already imports `_make_job_s101` at module scope in this file — do not re-import it.

TEST T2 (NEW FILE) — create `tests/cli/test_review_cmd.py` with EXACTLY this content:
<<<BEGIN T2_NEWFILE>>>
"""
Domain tests: cli/test_review_cmd.py
"""

from __future__ import annotations

import json
from argparse import Namespace
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4


def _recs():
    return [{
        "id": "rec1",
        "title": "Add tests",
        "status": "pending",
        "created_at": "2026-09-04T00:00:00+00:00",
    }]


def test_text_output_shows_created_date(capsys):
    from apps.cli.commands.review_cmd import _cmd_review_list

    job_stub = SimpleNamespace(id=uuid4())
    args = Namespace(job_id=str(job_stub.id), json=False)
    with patch("packages.orchestration.storage.load_job", return_value=job_stub), \
         patch("packages.orchestration.reviewer.list_recommendations", return_value=_recs()):
        _cmd_review_list(args)

    out = capsys.readouterr().out
    assert "created=2026-09-04T00:00:00+00:00" in out


def test_json_output_carries_created_at(capsys):
    from apps.cli.commands.review_cmd import _cmd_review_list

    job_stub = SimpleNamespace(id=uuid4())
    args = Namespace(job_id=str(job_stub.id), json=True)
    with patch("packages.orchestration.storage.load_job", return_value=job_stub), \
         patch("packages.orchestration.reviewer.list_recommendations", return_value=_recs()):
        _cmd_review_list(args)

    data = json.loads(capsys.readouterr().out)
    assert data["recommendations"][0]["created_at"] == "2026-09-04T00:00:00+00:00"
<<<END T2_NEWFILE>>>

Apply P1-P5, T1 and T2 (create the new file). All four files (2 production: `packages/orchestration/reviewer.py`, `apps/cli/commands/review_cmd.py`; 2 test: `tests/orchestration/test_approval_queue.py`, `tests/cli/test_review_cmd.py`) in ONE commit.

Run `python3 -m py_compile packages/orchestration/reviewer.py apps/cli/commands/review_cmd.py tests/orchestration/test_approval_queue.py tests/cli/test_review_cmd.py` and confirm exit 0. Then run `python3 -m pytest tests/cli/test_review_cmd.py tests/orchestration/test_approval_queue.py -q` and record the exact pass count verbatim — expected 28 (25 pre-existing in test_approval_queue.py + 1 new there + 2 new in the new file). Commit message: `F262 R11 C2: review.list gains a CREATED date end to end (T002 batch 9)`

──────────────────────────────────────────────────────────
C3 — replace .agent/plan.md with PLAN12
──────────────────────────────────────────────────────────
Replace the ENTIRE content of `.agent/plan.md` with exactly the text between the PLAN12 markers below (whole-file replace, byte-exact — verify with an actual byte-for-byte binary comparison, not `wc -l`/diffstat):

<<<BEGIN PLAN12>>>
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 11, session 5 - review.list gains a CREATED date end to end:
ReviewerRecommendation gains a created_at field stamped once in
run_reviewer() at construction time (datetime/timezone, matching
patch.list/loop.list's stamp-at-creation pattern), carried through
store_recommendations()'s persisted dict, and rendered as a
(created=...) suffix in _cmd_review_list's text branch - its --json
branch needed no change since it already prints list_recommendations()'s
own dicts verbatim. New tests/cli/test_review_cmd.py covers both
branches.

## Next Steps

- Round 11's own audit of all 18 catalog list commands against T002:
  job/queue/loop/project/patch/memory/tournament/blocker/decision/
  propose/review all carry a date now; execution.list/worker.list/
  config.list stay excused (Risks); change.list's event-log CREATED
  date stays open per DECISION F262 D1; event.list already surfaces
  `timestamp` per row under a different field name, satisfying
  Acceptance as-is.
- test.list's --json already carries created_at but its TEXT branch
  prints a bare count with no per-row listing at all - a pre-existing
  gap wider than a missing date, flagged rather than folded into T002.
- T003 (sort/filter/limit) can start once the gaps above are resolved
  or explicitly excused - review.list (this round) was the last
  unexcused, undated list command the audit found.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands, and
  test.list's missing per-row text listing, are pre-existing quirks
  this feature does not need to fix unless they block T003.
<<<END PLAN12>>>

Commit message: `F262 R11 C3: replace plan.md with PLAN12`

──────────────────────────────────────────────────────────
C4 — handback
──────────────────────────────────────────────────────────
Rewrite `.agent/handoff.md` (whole-file, per AGENTS.md's handback contract) with: Session (SESSION 5 of feature F262, round 11, rounds so far 11), a Range section stating this handback covers `c37fd166..<C3 sha>` (C4/this handback commit is NOT part of the reviewed content range), an Item Status table (Preconditions, C0a, C0b, C1, C2, C3, C4, plus one row per gate you ran), a Commits table with every file changed per commit and its +/- line counts from `git show --numstat`, a Verification section with the REAL output of every command you ran (py_compile exit codes, the exact pytest pass count for C2's combined run, the canary suite run as ONE combined invocation: `python3 -m pytest tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q`, expected 646 passed), a Deviations & assumptions section (state honestly anything that didn't go exactly as ordered, including the plan.md byte-equality check result), and a Next section naming round 12's likely focus (your call — T003 sort/filter/limit design, or the test.list text-listing gap named in PLAN12 — state your one-sentence reasoning). Follow the exact structure of the R10 handback (commit c37fd166, already on disk — read it for the template).

After committing C4, run `git push -u origin feature/f262-list-commands-v2` and report the push result in your closing message.

Do NOT run any `gh pr` command. Do NOT merge anything. Do NOT touch `main`. This round ships no PR — the branch stays open for round 12.

═══════════════════════════════════════════════════════════════
CONSTRAINTS
═══════════════════════════════════════════════════════════════
1. Every FROM string in P1-P5 and T1 must be verified to occur exactly once in its target file, using the file's CURRENT content on disk (re-read each file yourself before applying, do not trust cited context blindly). If a FROM does not match, STOP that pair, do not guess a fix, report the exact mismatch in Deviations instead.
2. Do not touch any file not named in this block.
3. Do not run `ruff` if it requires approval you don't have — note the refusal in Deviations if so, not a blocker.
4. If `.agent/STOP` appears at any point mid-round, finish the commit you are mid-way through (if any), then stop and hand off.
5. Keep C2 as ONE commit covering exactly the four named files.
6. Report every command's REAL exit code and REAL output. Never write "green"/"passed" without the actual number.
7. The C3 plan.md gate MUST be an actual byte-for-byte comparison (read both files in binary mode and compare with `==`), not a line-count or diffstat proxy.
8. Do not add `--json` handling logic to `review_cmd.py` — it already exists and already carries whatever keys `list_recommendations()` returns; the json branch is NOT part of this round's change set beyond what P2-P4 make it inherit automatically.

END OF BLOCK
