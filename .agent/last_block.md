═══════════════════════════════════════════════════════════════
STEP — F262 R9/? — patch.list gains a CREATED date end to end
═══════════════════════════════════════════════════════════════

GOAL: Add a `created_at` timestamp to every patch-intent explanation, stamped once at intent-derivation time in BOTH creation flows (`do_run.py` and `apps/cli/commands/job.py`), surface it through `list_patch_intents()` and `format_intent_list()`'s CREATED column (which flows into `patch.list --json` automatically, since the JSON path prints `list_patch_intents()`'s own dicts verbatim). Book round 8's reviewer verdict into the ledger. Record the design decision that resolves plan.md's stale "no production code emits patch_intent_created" claim.

BACKGROUND FACTS (already verified by the reviewer — do not re-derive, just apply):
- `list_patch_intents()` in `packages/orchestration/approval_queue.py` reads `artifact.metadata["patch_intent_explanations"]`, a list of plain dicts. This is the ONLY place all consumers (patch.list, cockpit, trust_report, etc.) converge — not the event log, not the `PatchIntent`/`Artifact` pydantic models (neither has a timestamp field).
- Two write sites populate `patch_intent_explanations`: `packages/orchestration/do_run.py:514` (`_run_patch_intent_phase`, already imports `datetime`/`timezone` at line 22) and `apps/cli/commands/job.py:612` (`_cmd_run_next_task_local`, does NOT import `datetime` yet).
- No test anywhere does an exact whole-dict `==` equality check on `list_patch_intents()`'s output or a byte-exact string check on `format_intent_list()`'s output — all existing tests check individual keys / substrings, confirmed by the reviewer's own grep. Adding a new dict key and a new table column is safe.

═══ COMMIT SEQUENCE (7 commits total; keep each one exactly as scoped below) ═══

──────────────────────────────────────────────────────────
C0a — save this entire step block verbatim
──────────────────────────────────────────────────────────
Save the FULL literal text of this prompt message (everything between the "STEP —" header above and the final "END OF BLOCK" marker at the very bottom of this message) to `.agent/authored/f262-r9.md`, byte for byte, exactly as received — do not retype, do not summarize, do not reformat. Commit message: `F262 R9 C0a: save block verbatim to .agent/authored/f262-r9.md`

──────────────────────────────────────────────────────────
C0b — mirror to .agent/last_block.md
──────────────────────────────────────────────────────────
Copy `.agent/authored/f262-r9.md` (the file you just committed) to `.agent/last_block.md`, whole-file replace (AGENTS.md's `.agent/**` state-file exemption from the 500-line cap applies — this is a single indivisible artifact). Verify `sha256sum` of both files matches after writing. Commit message: `F262 R9 C0b: mirror block to .agent/last_block.md`

──────────────────────────────────────────────────────────
C1 — append GATE8 to .agent/live_review.md
──────────────────────────────────────────────────────────
Append exactly the text between the GATE8 markers below to the END of `.agent/live_review.md`. The append is: one newline character, then the GATE8 text verbatim (it is a SINGLE LINE — no internal newlines, matching the file's existing GATE entries), with no other bytes added. Do not touch anything else in the file.

<<<BEGIN GATE8>>>
Gate: R8 — the F262 R8 entry. R8 SHIPPED T002 BATCH 6, patch.list gains --json end to end (catalog args gain _JSON_OPT + supports_json=True, handler json_output kwarg + json branch, dispatch lambda passes json_output=args.json) plus a DECIDED column in format_intent_list surfacing the intent's own decided_at — AND THE REVIEWER RE-RAN EVERY GATE ITSELF rather than reading the handback back. TRANSPORT HELD: `.agent/authored/f262-r8.md`/`.agent/last_block.md` share one sha256 digest, `44f83c824b9e9756096948569313664134a71cfeee76f892c4cda66870b37031`, confirmed by the reviewer's own sha256 read of both committed files. THE DIFF WAS READ, NOT ONLY GATED: `git diff 2286919d60503ddd0535eedc49af3ea1242ac047..8108c51c` shows the exact five pairs the handback claimed — command_catalog.py's diff is exactly PAIR P1 (patch.list CommandEntry gains _JSON_OPT and supports_json=True), patch.py's diff is exactly PAIR P2 (handler gains json_output kwarg + json branch) and PAIR P3 (dispatch lambda), approval_queue.py's diff is exactly PAIR P4 (format_intent_list header+row gain DECIDED), test_command_catalog.py's diff is exactly PAIR P7 (expected_json gains patch.list), test_patch_intent_approval.py's diff is exactly PAIR P5/P6 (two new tests appended) — every diff re-read in full, nothing else touched. `python3 -m py_compile` exited 0 on all five touched files, run together by the reviewer. THE GATE7 LEDGER APPEND (commit a850bff6) WAS RE-VERIFIED BYTE-EXACT: base (2437464 bytes) + one newline + GATE7 (3786 bytes, extracted from the committed .agent/authored/f262-r8.md by its own BEGIN/END markers, excluding the marker line's own trailing newline) reproduces the post-commit file (2441251 bytes) exactly; tail-equality, preceding-newline and negative-control byte-flip rejection all confirmed. THE TESTS MOVED EXACTLY AS THE HANDBACK CLAIMED, reproduced independently: `tests/test_patch_intent_approval.py tests/test_command_catalog.py` read 91 passed (matching the handback's own after-C2 reading; the handback's declared 77-vs-89 pre-C2 discrepancy is the worker's own honestly-reported deviation, not re-litigated here). THE STATE READERS AND THE CANARY WERE UNMOVED, reproduced by the reviewer: `tests/ui_server/` 515, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `test_golden_path` 42. HYGIENE HELD: `git status --porcelain` empty at HEAD `74cfbd28`, `git ls-files .remedy-wt` empty. THE VERDICT IS PASS.
<<<END GATE8>>>

Commit message: `F262 R9 C1: append GATE8 to live_review.md - books round 8's PASS verdict`

──────────────────────────────────────────────────────────
C2 — production pairs + tests (one commit, six files)
──────────────────────────────────────────────────────────

PAIR P1 (REWRITE) — `apps/cli/commands/job.py`, add the datetime import.
FROM (exact, currently lines 8-9):
<<<BEGIN PAIR_P1_FROM>>>
from collections.abc import Callable
from typing import TYPE_CHECKING, Any
<<<END PAIR_P1_FROM>>>
TO:
<<<BEGIN PAIR_P1_TO>>>
from collections.abc import Callable
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any
<<<END PAIR_P1_TO>>>
Verify FROM occurs exactly once in the file before applying.

PAIR P2 (REWRITE) — `apps/cli/commands/job.py`, stamp created_at once per task-run and add it to every explanation dict.
FROM (exact, currently lines 612-616):
<<<BEGIN PAIR_P2_FROM>>>
                        pi_artifact.metadata["patch_intent_explanations"] = [
                            {"file": r.target_path, "action": r.action, "risk": r.risk_level,
                             "reason": r.reason, "summary": r.summary}
                            for r in dry_run_results
                        ]
<<<END PAIR_P2_FROM>>>
TO:
<<<BEGIN PAIR_P2_TO>>>
                        pi_created_at = datetime.now(timezone.utc).isoformat()
                        pi_artifact.metadata["patch_intent_explanations"] = [
                            {"file": r.target_path, "action": r.action, "risk": r.risk_level,
                             "reason": r.reason, "summary": r.summary, "created_at": pi_created_at}
                            for r in dry_run_results
                        ]
<<<END PAIR_P2_TO>>>
Verify FROM occurs exactly once in the file before applying.

PAIR P3 (REWRITE) — `packages/orchestration/do_run.py`, add created_at to the fixture explanation dict (datetime/timezone already imported at line 22 — do not add a second import).
FROM (exact, currently lines 514-521):
<<<BEGIN PAIR_P3_FROM>>>
    artifact.metadata["patch_intent_explanations"] = [
        {
            "file": "docs/CHANGES.md",
            "action": "create",
            "risk": "low",
            "summary": "Safe documentation change",
        }
    ]
<<<END PAIR_P3_FROM>>>
TO:
<<<BEGIN PAIR_P3_TO>>>
    artifact.metadata["patch_intent_explanations"] = [
        {
            "file": "docs/CHANGES.md",
            "action": "create",
            "risk": "low",
            "summary": "Safe documentation change",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    ]
<<<END PAIR_P3_TO>>>
Verify FROM occurs exactly once in the file before applying.

PAIR P4 (REWRITE) — `packages/orchestration/approval_queue.py`, surface created_at in `list_patch_intents()`'s returned dict.
FROM (exact, currently within the `result.append({...})` block):
<<<BEGIN PAIR_P4_FROM>>>
                    "summary": exp.get("summary", ""),
                    "state": approval.get("state", APPROVAL_PENDING),
<<<END PAIR_P4_FROM>>>
TO:
<<<BEGIN PAIR_P4_TO>>>
                    "summary": exp.get("summary", ""),
                    "created_at": exp.get("created_at"),
                    "state": approval.get("state", APPROVAL_PENDING),
<<<END PAIR_P4_TO>>>
Verify FROM occurs exactly once in the file before applying.

PAIR P5 (REWRITE) — `packages/orchestration/approval_queue.py`, docstring of `list_patch_intents()`.
FROM (exact):
<<<BEGIN PAIR_P5_FROM>>>
      summary          — truncated intent text
      state            — APPROVAL_PENDING | APPROVAL_APPROVED | APPROVAL_REJECTED
<<<END PAIR_P5_FROM>>>
TO:
<<<BEGIN PAIR_P5_TO>>>
      summary          — truncated intent text
      created_at       — ISO datetime string or None (set once, at intent-derivation time)
      state            — APPROVAL_PENDING | APPROVAL_APPROVED | APPROVAL_REJECTED
<<<END PAIR_P5_TO>>>
Verify FROM occurs exactly once in the file before applying.

PAIR P6 (REWRITE) — `packages/orchestration/approval_queue.py`, `format_intent_list()` gains a CREATED column ahead of DECIDED.
FROM (exact, this is the CURRENT content after R8 — read the file yourself first and confirm this matches before applying; if it does not match exactly, STOP and report the mismatch rather than guessing):
<<<BEGIN PAIR_P6_FROM>>>
    lines = [f"{'ID':<14}  {'STATE':<8}  {'RISK':<8}  {'ACTION':<12}  {'DECIDED':<20}  TARGET PATH"]
    lines.append("-" * 72)
    for item in intents:
        lines.append(
            f"{item['intent_id']:<14}  "
            f"{item['state']:<8}  "
            f"{item['risk']:<8}  "
            f"{item['action']:<12}  "
            f"{(item['decided_at'] or '-'):<20}  "
            f"{item['target_path']}"
        )
<<<END PAIR_P6_FROM>>>
TO:
<<<BEGIN PAIR_P6_TO>>>
    lines = [f"{'ID':<14}  {'STATE':<8}  {'RISK':<8}  {'ACTION':<12}  {'CREATED':<20}  {'DECIDED':<20}  TARGET PATH"]
    lines.append("-" * 92)
    for item in intents:
        lines.append(
            f"{item['intent_id']:<14}  "
            f"{item['state']:<8}  "
            f"{item['risk']:<8}  "
            f"{item['action']:<12}  "
            f"{(item['created_at'] or '-'):<20}  "
            f"{(item['decided_at'] or '-'):<20}  "
            f"{item['target_path']}"
        )
<<<END PAIR_P6_TO>>>
Verify FROM occurs exactly once in the file before applying.

TEST T1 (APPEND) — `tests/orchestration/test_do_run.py`. Insert this new test method immediately after the existing `test_patch_intent_created` method (which ends `assert result.patch_intent_id`) and before `test_artifact_created`, same indentation/class (`TestPhaseModel`... actually check: locate the method by its exact body, insert the new method directly after it, before the blank line + next method):
<<<BEGIN T1>>>
    def test_patch_intent_created_has_created_at(self, tmp_path):
        from uuid import UUID

        from packages.orchestration.approval_queue import list_patch_intents
        from packages.orchestration.storage import load_job

        result = _run_with_tmp(tmp_path, autonomy=3)
        job = load_job(UUID(result.job_id), root=tmp_path / "data")
        intents = list_patch_intents(job)
        assert intents[0]["created_at"]

<<<END T1>>>
(Insert this whole block, including its trailing blank line, directly before `    def test_artifact_created(self, tmp_path):`.)

TEST T2 (APPEND) — `tests/test_patch_intent_approval.py`, class `TestFormatHelpers`. Insert immediately after `test_format_intent_list_shows_decided_when_set` (ends `assert item["decided_at"] in out`) and before `test_format_intent_detail_shows_risk_and_summary`:
<<<BEGIN T2>>>
    def test_format_intent_list_shows_created_when_set(self):
        job = _make_job()
        artifact = Artifact(
            name="builder_proposal",
            content="",
            kind=ArtifactKind.BUILDER_PROPOSAL,
            task_id=uuid4(),
            metadata={
                "patch_intent_explanations": [
                    {"file": "docs/file_0.md", "action": "modify", "risk": RISK_MEDIUM,
                     "reason": "task type 'write_readme'", "summary": "Proposed change 0",
                     "created_at": "2026-09-04T12:00:00+00:00"},
                ],
                "patch_intent_approvals": {},
            },
        )
        job.artifacts.append(artifact)
        out = format_intent_list(list_patch_intents(job))
        assert "2026-09-04T12:00:00+00:00" in out

<<<END T2>>>
(`Artifact` needs importing in this test — check the top of the file: it currently imports `ArtifactKind, Job, RunState, Task` from `packages.core.models` but not `Artifact` at module level, though `_add_patch_artifact` does `from packages.core.models import Artifact` locally inside its own function. Do the same here: add a local `from packages.core.models import Artifact` as the first line of this new test method's body, OR add `Artifact` to the existing module-level import — your choice, pick whichever keeps the diff smaller and matches this file's own existing style; if you add it locally inside the method, put it as the very first line of the method body, before `job = _make_job()`.)

TEST T3 (APPEND) — `tests/test_patch_intent_approval.py`, class `TestCmdListPatchIntents`. Insert immediately after `test_json_output_has_version_and_intents` (the last method in that class, ends `assert data["intents"][0]["decided_at"] is None`), keeping the blank-line spacing this file uses before the next `# ---` section comment:
<<<BEGIN T3>>>
    def test_json_output_has_created_at_key(self, tmp_path, monkeypatch, capsys):
        job = self._save(tmp_path, monkeypatch)
        _add_patch_artifact(job)
        save_job(job)
        from apps.cli.commands.patch import _cmd_list_patch_intents
        _cmd_list_patch_intents(str(job.id), json_output=True)
        data = json.loads(capsys.readouterr().out)
        assert "created_at" in data["intents"][0]
<<<END T3>>>

TEST T4 (APPEND) — `tests/test_run_log_cli.py`, class `TestRunNextTaskPatchIntentCreated`. Insert this new test method immediately after `test_patch_intent_created_writes_event_with_count_and_risks` (the only method currently in that class):
<<<BEGIN T4>>>

    def test_patch_intent_created_writes_created_at_on_explanation(
        self, tmp_path, monkeypatch
    ):
        """Patch intent explanations carry a created_at timestamp (F262 T002)."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

        job = Job(name="test", state=RunState.RUNNING)
        task = Task(description="write readme", inputs={"task_type": "write_readme"})
        job.tasks.append(task)
        save_job(job)

        artifact = Artifact(
            name="task_output_write_readme",
            content=(
                "Summary:\n  Quick summary.\n\nProposed Changes:\n"
                "  - Change A\n  - Change B\n\nNotes:\n  - None\n"
            ),
            mime_type="text/plain",
            task_id=task.id,
            kind=ArtifactKind.BUILDER_PROPOSAL,
            metadata={"task_type": "write_readme", "summary": "done"},
        )
        task.output_artifact_ids.append(artifact.id)
        job.artifacts.append(artifact)

        ws_file = tmp_path / "fake_ws.txt"
        ws_file.write_text("  - Change A\n  - Change B\n")
        artifact.metadata["workspace_file"] = str(ws_file)
        task.status = RunState.RUNNING

        from packages.orchestration.patch_intent import (
            PatchDryRunResult,
            PatchIntent,
            PatchIntentSet,
        )
        from packages.orchestration.task_runner import RunTaskResult
        from packages.orchestration.verifier import VerificationResult
        from packages.orchestration.workspace import MaterializedFile

        run_result = RunTaskResult(job=job, task_id=task.id, changed=True)
        vr = VerificationResult(task_id=task.id, passed=True, checks=[])
        fake_mf = MaterializedFile(path=ws_file, content="  - Change A\n", size=14)

        fake_pis = PatchIntentSet(
            task_id=task.id,
            artifact_id=artifact.id,
            intents=[
                PatchIntent(
                    target_path="README.md",
                    intent="Add installation section",
                )
            ],
        )
        fake_pi_mf = MaterializedFile(
            path=tmp_path / "pi.json", content="{}", size=2
        )
        fake_dry_run = [
            PatchDryRunResult(
                target_path="README.md",
                action="modify",
                risk_level="medium",
                reason="task type 'write_readme'",
                summary="Add installation section",
                diff_preview="--- README.md",
            )
        ]

        def fake_finalize(r, v):
            for t in r.job.tasks:
                if t.id == r.task_id:
                    t.status = RunState.COMPLETED

        builder_instance = MagicMock()
        builder_instance.model = "test-model"
        builder_cls = MagicMock(return_value=builder_instance)

        with (
            patch(
                "packages.providers.ollama_builder.provider.OllamaBuilder",
                builder_cls,
            ),
            patch(
                "packages.orchestration.task_runner.run_next_task",
                return_value=run_result,
            ),
            patch("packages.orchestration.task_runner.annotate_task_result"),
            patch(
                "packages.orchestration.task_runner.materialize_task_output",
                return_value=fake_mf,
            ),
            patch(
                "packages.orchestration.verifier.verify_task_output",
                return_value=vr,
            ),
            patch(
                "packages.orchestration.task_runner.finalize_task",
                side_effect=fake_finalize,
            ),
            patch(
                "packages.orchestration.patch_intent.derive_patch_intents",
                return_value=fake_pis,
            ),
            patch(
                "packages.orchestration.patch_intent.verify_patch_intent_set",
                return_value=[],
            ),
            patch(
                "packages.orchestration.patch_intent.materialize_patch_intents",
                return_value=fake_pi_mf,
            ),
            patch(
                "packages.orchestration.patch_intent.generate_dry_run_preview",
                return_value=fake_dry_run,
            ),
        ):
            from apps.cli.commands.job import _cmd_run_next_task_local

            _cmd_run_next_task_local(str(job.id))

        from packages.orchestration.storage import load_job

        reloaded = load_job(job.id)
        explanations = reloaded.artifacts[0].metadata["patch_intent_explanations"]
        assert explanations[0]["created_at"]
<<<END T4>>>

Apply P1-P6 and T1-T4, run `python3 -m py_compile apps/cli/commands/job.py packages/orchestration/do_run.py packages/orchestration/approval_queue.py tests/orchestration/test_do_run.py tests/test_patch_intent_approval.py tests/test_run_log_cli.py` and confirm exit 0. Then run `python3 -m pytest tests/orchestration/test_do_run.py tests/test_patch_intent_approval.py tests/test_run_log_cli.py tests/test_command_catalog.py -q` and record the exact pass count (report it verbatim — do not round or guess). All 6 files (3 production, 3 test) in ONE commit. Commit message: `F262 R9 C2: patch.list/do_run/job.py gain created_at end to end (T002 batch 7)`

──────────────────────────────────────────────────────────
C3 — append DECISION F262 D1 to .agent/decisions.md
──────────────────────────────────────────────────────────
Append exactly the text between the DECISION markers below to the END of `.agent/decisions.md`: one newline, then the decision text verbatim, nothing else added.

<<<BEGIN DECISION_F262_D1>>>
## DECISION F262 D1 (2026-09-04, F262 R9) — patch.list/loop.list's CREATED date is sourced from a new `created_at` field on each stored patch-intent explanation dict, stamped once at intent-derivation time in both creation flows, not reconstructed from the run-event log

CONTEXT. `.agent/plan.md`'s Next Steps (as of R8) named an open design question for `patch.list`'s CREATED date: "the only production emitter of an intent-creation event (`do_run_patch_intent_created` in do_run.py) is read by NO consumer, while every reader instead checks a bare `patch_intent_created` no production code emits." A fresh read this round (reviewer, read-only) found that claim stale: `apps/cli/commands/job.py:623` (`_cmd_run_next_task_local`, the `remedy job run-next-task-local` flow) DOES emit `log.log("patch_intent_created", task_id=..., outcome="created", intent_count=..., risk_levels=...)` — a real, live emitter. The claim was true only of `do_run.py`'s OWN emission (`do_run_patch_intent_created`, still dead, still unread) and became false the moment job.py's flow was read fresh rather than recalled from plan.md's prose.

MEASURED. `list_patch_intents()` (packages/orchestration/approval_queue.py:129) — the SOLE function `patch.list`, `change.list`'s callers, cockpit, trust_report and eight other consumers all read patch intents through — does not read the event log or the `PatchIntent` pydantic model at all. It reads `artifact.metadata["patch_intent_explanations"]`, a plain list of dicts written directly by BOTH creation flows: `do_run.py:514` (`_run_patch_intent_phase`) and `apps/cli/commands/job.py:612` (`_cmd_run_next_task_local`). Neither the `PatchIntent` model (packages/orchestration/patch_intent.py:78-95) nor the `Artifact` model (packages/core/models.py:91-114) carries any timestamp field, so neither the event log NOR either model can supply a per-intent creation time without a new field somewhere; the two `patch_intent_explanations` write sites are the only place all consumers actually converge, and both already run inside a `datetime`-using module or one line from importing it (do_run.py:22 already imports `datetime`/`timezone`; job.py imports neither, and needed to).

CHOSEN. Both write sites gain a `created_at` key (ISO-8601 UTC, `datetime.now(timezone.utc).isoformat()`) in the explanation dict — do_run.py's fixture-shaped dict gets it directly; job.py's dict-comprehension stamps one `pi_created_at` value shared by every intent derived from the same task-run (accurate: they really are created together in one CLI call). `list_patch_intents()` surfaces it as `exp.get("created_at")` on each returned dict (mirroring how `decided_at` already reads `approval.get("decided_at")`), and `format_intent_list()` gains a CREATED column ahead of DECIDED (chronological order). `patch.list --json` (R8) needed no separate change — it prints `list_patch_intents()`'s own dicts verbatim, so the new key flows through automatically.

ALTERNATIVE CONSIDERED AND REJECTED. Route CREATED through the run-event log instead — either by fixing `do_run.py`'s dead emitter to match the 8 existing `patch_intent_created` readers, or by having `list_patch_intents()` scan `load_run_events()` for a `patch_intent_created`/`do_run_patch_intent_created` event and join it to each intent by `intent_id`/`task_id`. Rejected on two independent grounds: (1) job.py's real `patch_intent_created` event carries no `intent_id` at all (only `task_id`, `outcome`, `intent_count`, `risk_levels`), so it cannot be joined to an individual intent without ALSO changing that call site, at which point the event-log route costs strictly more than the metadata-dict route while solving nothing the dict route doesn't already solve; (2) the event log is a per-JOB append-only history, while `list_patch_intents()` is a pure function of `job.artifacts` metadata with no event-log dependency today — introducing one would add a second data source for a value the existing single source (the explanation dict) can hold directly, for no accuracy gain.

CONSEQUENCE. `apps/cli/commands/job.py` gains a `datetime`/`timezone` import and one `created_at` key in its explanation dict comprehension. `packages/orchestration/do_run.py` gains one `created_at` key in its fixture dict (import already present). `packages/orchestration/approval_queue.py` gains `created_at` in `list_patch_intents()`'s returned dict, its docstring, and a CREATED column in `format_intent_list()`. The stale plan.md claim about `do_run_patch_intent_created`/`patch_intent_created` is corrected in this round's plan.md rewrite rather than repeated; the event-log naming mismatch itself (do_run.py's dead emitter, 8 readers of a string only job.py's flow emits) is UNCHANGED and OUT OF SCOPE for F262 — it is a pre-existing gap in a different subsystem (timeline/cockpit/trust-report event narration) that this DECISION's own MEASURED paragraph documents but does not fix, since nothing in F262's Acceptance depends on it.

REVERSE by deleting this DECISION and reverting the `created_at` additions in `do_run.py`, `apps/cli/commands/job.py` and `approval_queue.py` (including the CREATED column) — which a fresh read of `list_patch_intents()` against `patch.list`'s Acceptance requirement (a CREATED date) would immediately re-discover necessary, `list_patch_intents()` reading only `artifact.metadata` either way.
<<<END DECISION_F262_D1>>>

Commit message: `F262 R9 C3: append DECISION F262 D1 to decisions.md - CREATED date source`

──────────────────────────────────────────────────────────
C4 — replace .agent/plan.md with PLAN10
──────────────────────────────────────────────────────────
Replace the ENTIRE content of `.agent/plan.md` with exactly the text between the PLAN10 markers below (whole-file replace, byte-exact, no trailing content added):

<<<BEGIN PLAN10>>>
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 9, session 4 - patch.list gains a CREATED date end to end
(DECISION F262 D1): both creation flows (do_run.py, job.py) stamp
created_at on the stored patch_intent_explanations dict;
list_patch_intents() surfaces it; format_intent_list() gains a
CREATED column ahead of DECIDED. Corrects a stale R8 claim - job.py:623
DOES emit patch_intent_created; only do_run.py's own
do_run_patch_intent_created is dead. Neither event is the source
list_patch_intents() reads (artifact metadata, not the event log) -
see DECISION F262 D1.

## Next Steps

- loop.list has no created_at of its own (LoopSpec is static
  remedy.toml config); already prints a "last run" label from
  job.created_at, which may be the right substitute - separate design
  pass from D1.
- change.list's event-log CREATED date stays open, UNRELATED to D1:
  do_run.py's event stays dead, job.py's real event carries no
  intent_id to join on - see D1's Alternative section.
- The execution.* trio always prints JSON unconditionally with no
  text branch - the pre-existing --json-ignored quirk Risks excuses.
- T003 (sort/filter/limit) starts once date coverage is far enough
  along to sort by.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix unless it
  blocks T003's sort behavior for them specifically.
<<<END PLAN10>>>

Commit message: `F262 R9 C4: replace plan.md with PLAN10`

──────────────────────────────────────────────────────────
C5 — handback
──────────────────────────────────────────────────────────
Rewrite `.agent/handoff.md` (whole-file, per AGENTS.md's handback contract) with: Session (this is SESSION 4 of feature F262, round 9, rounds so far 9), a Range section stating this handback covers `74cfbd28..<C4 sha>` (state that C5/this handback commit is NOT part of the reviewed content range, matching R8's own convention), an Item Status table (Preconditions, C0a, C0b, C1, C2, C3, C4, C5, plus one row per gate you ran), a Commits table with every file changed per commit and its +/- line counts from `git show --numstat`, a Verification section with the REAL output of every command you ran (py_compile exit codes, the exact pytest pass counts for C2's combined run, the canary suite counts: `tests/ui_server/`, `tests/orchestration/test_test_runner.py`, `tests/regression/test_resource_safety.py`, `tests/orchestration/test_integrity_gate.py`, `tests/cli/test_golden_path.py` — all five, run individually, report exact pass counts), a Deviations & assumptions section (state honestly anything that didn't go exactly as ordered, including if PAIR P6's FROM did not match — do not force it to match), and a Next section naming the next expected action (T003 sort/filter/limit work, or further date-coverage design per plan.md's Next Steps — your call which to name first, state your reasoning in one sentence). Follow the exact structure of the R8 handback (commit 74cfbd28, already on disk — read it for the template) since it is this file's own immediately-preceding instance and demonstrates the required shape.

After committing C5, run `git push -u origin feature/f262-list-commands-v2` (branch already tracks the remote from prior rounds, but include `-u` defensively) and report the push result in your closing message (not inside the handoff file, since it happens after that commit).

Do NOT run any `gh pr` command. Do NOT merge anything. Do NOT touch `main`. This round ships no PR — the branch stays open for round 10.

═══════════════════════════════════════════════════════════════
CONSTRAINTS
═══════════════════════════════════════════════════════════════
1. Every FROM string in P1-P6 must be verified to occur exactly once in its target file, using the file's CURRENT content on disk (re-read each file yourself before applying — do not trust the line numbers cited above blindly, they were correct when the reviewer read them but re-confirm). If a FROM does not match, STOP that pair, do not guess a fix, and report the exact mismatch in your Deviations section instead — do not improvise different bytes.
2. Do not touch any file not named in this block.
3. Do not run `ruff` if it requires approval you don't have — if it's denied, note the refusal in Deviations exactly as prior rounds did, this is expected and not a blocker.
4. If `.agent/STOP` appears at any point mid-round, finish the commit you are mid-way through (if any), then stop and hand off — do not start the next commit.
5. Keep C2 as ONE commit covering exactly the six named files (three production, three test). If total insertions in C2 exceed 500 lines, stop before committing and report — but this should not happen (the additions are small).
6. Report every command's REAL exit code and REAL output. Never write the word "green" or "passed" without the actual number. Never accept your own summary as evidence — the reviewer will independently re-run every gate.

END OF BLOCK
