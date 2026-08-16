# F085 R15 — record the R14 PASS and give the claude CLI seam its guarded runner

Feature T2_F085 Sandbox hardening (stage 1) · Round R15 · Branch feature/f085-sandbox-hardening
Base of this round: the R14 handback commit, `git rev-parse HEAD` at start = c5d80471.
Fortschritt: ~55 % (T001 gebaut · R13/R14 PASS · T002a: Builder-Site migriert, diese Runde der
CLI-Runner samt Version-Probe · zwei gekoppelte CLI-Sites, `stream_evidence.py`, T002b-d, T003 offen).

## Goal

First the record: R14 passed the reviewer's gate — including its `.agent/STOP` halt, correct and
honestly reported — and that verdict is written by C1, with one finding the reviewer measured
against its own scoping work. Then the work: `pingpong_provider.py` gains the stage-1 CLI policy,
the text-decode contract and `_guarded_cli_run`, and `_resolve_version` — the ONE site no test's
mock reaches (R-0507) — stops calling `subprocess.run`. R14's owed plan pair lands as C3.

Evidence already taken by the reviewer, so the worker does not repeat it: this exact change was
applied to a `git archive HEAD` extraction, where the goldens are 8 passed and stable over ten runs,
the seven-file regression set is 333 passed at BOTH base and the extraction, ruff is exit 0 on both
touched paths, and SEVEN red controls each reddened exactly their own tests. Those controls earned
their keep — an earlier draft asserted the wall trip through `_resolve_version`, which swallows every
exception, and stayed GREEN with the re-raise deleted (the R-0504 vacuity family).

## Bundle — in this order, none added, dropped or reordered

- C0a `docs(f085): save the R15 step block verbatim` — `.agent/authored/f085-r15.md`
- C0b `docs(f085): mirror the R15 block into last_block` — `.agent/last_block.md`
- C1 `docs(review): record the R14 PASS and register a scoping finding` — `.agent/live_review.md`
- C2 `feat(f085): give the claude CLI seam its guarded runner` — source and new test file together,
  since a commit adding the runner without its goldens would land an ungated seam
- C3 `docs(f085): advance the plan to the R15 CLI runner round` — `.agent/plan.md`
- C4 `docs(f085): rewrite the handback for R15` — `.agent/handoff.md`

## Change set — exactly these SIX paths, nothing else

`.agent/authored/f085-r15.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
`.agent/handoff.md`, `packages/orchestration/pingpong_provider.py` and
`tests/orchestration/test_claude_cli_exec_guard.py` (NEW). Nothing under `docs/`, `apps/` or
`scripts/`; no other file under `packages/` or `tests/`. `test_structured_cli_envelope.py`,
`exec_guard.py`, `managed_builder_execution.py`, `.agent/context.md` and `.agent/decisions.md` are
NOT touched — the first three are R16's, and scope is otherwise unchanged.

## Constraints

1. `cp` and the `remedy` CLI are denied here: copy with `shutil.copyfile` and prove the BYTE
   property, never the tool. Gate scratch lives under the gitignored `.remedy-wt/`.
2. Extract every slice programmatically by its one-line marker pair and apply it byte-verbatim,
   never retyped, reformatted or reworded: the review slices' regex-looking text and backticks are
   prose and land as prose.
3. Apply each FROM/TO pair by locating the FROM exactly once and replacing it with the TO; if it
   does not occur exactly once, STOP and report. CLST is APPEND-shaped — its TO CONTAINS CLSF — so
   CLSF still occurs once after it lands, and no "FROM 0x" proof applies to it (§4.9). Every other
   pair is a REWRITE. `TESTNEW` is a whole NEW file, written as-is.
4. This round orders NO destructive check — the seven red controls behind it were run by the
   reviewer before emission and are reported in the Goal, not re-ordered here. No gate below needs a
   disposable tree, and no worktree is added, removed or pruned.
5. Re-read `.agent/STOP` from disk before the FIRST commit and again before the LAST. If it exists
   at either point, finish the commit in flight, write the handback and end.

<<<SLICE RECORD1>>>
Gate: R14 — PASS, the record round `.agent/STOP` halted after its third commit. All eight ordered
gates were re-run by the reviewer from the repository root and every one reproduces the handback's
reading. TRANSPORT, disk-to-disk and not by digest fallback: the reviewer's `.remedy-wt/f085-r14.md`,
the committed `.agent/authored/f085-r14.md` and `.agent/last_block.md` are byte-EQUAL at sha256
77447503b8bc9e86e2f8f905172874568777ae8d25b074c0d3662b912b10d32e, 15023 B, 214 lines. C1 IS A PURE
APPEND: the pre-C1 blob is a byte-exact PREFIX of the post-C1 file, HEAD equals it, and the
7296-byte remainder is exactly blank + RECORD1 + blank + FIND1 + blank + FIND2 in that order, each
slice occurring ONCE, none carrying trailing whitespace, no marker line reaching it. THE ARITHMETIC: 119 / 3 / 0 at base against 121 / 3 / 0 at HEAD, so the open set rose
116 to 118 by exactly two registrations against no resolution; the registered difference is R-0505
and R-0506, the resolved difference empty, no duplicate id, no resolution naming an unregistered id.
THE HALT WAS CORRECT AND HONESTLY REPORTED. `.agent/STOP` appeared mid-round, C2 was never started,
`.agent/plan.md` is byte-IDENTICAL to base at sha256
8dae6b41813aff162aeb1c5a877ab667be909c723c30bbb4dc5b3fce42f65f6d, and PLANF still occurs EXACTLY
once in it — so the round did not half-apply a pair and then round the number, which is what this
gate catches. G5 is red by the sentinel, not by a misapplication. THE HONESTY GATE HOLDS: `exec_guard.py`,
`managed_builder_execution.py` and `test_managed_builder_execution.py` are byte-identical between
base and HEAD, so no containment claim follows from that round. State readers 157 passed and canary
42 passed, both matching base; the change set is three `.agent` paths before C3, short of the ordered
four by `.agent/plan.md` alone, which IS the skipped commit; insertions 214, 150 and 80, none over
500; four single-parent commits, every reflog entry `commit:`-prefixed, no amend, rebase, reset or
force-push; `.agent/handoff.md` measures 79 lines against its D15 declaration of 79; all seven
declared deviations are accurate. The sentinel is ABSENT at this round's start, so Phase 1 rule 1
does not fire. TWO SCOPE REASSIGNMENTS, recorded because each contradicts text already on
disk: R-0506 stays OPEN with its fix moved from R15 to R16, and T002a's CLI half is split — R15
migrates the version probe, while `_call`, `_call_reviewer_structured` and the envelope mock are ONE
indivisible unit (R-0507) R16 carries whole, already dry-run green. LAST_REVIEWED_SHA advances to
the R14 handback commit.
<<<END RECORD1>>>
<<<SLICE FIND1>>>
- R-0507 — Medium, A GREP OVER MOCK TARGETS WAS READ AS AN ENUMERATION OF THE CALL PATHS THOSE
MOCKS COVER, AND THE SCOPE IT PRODUCED WAS WRONG. Raised by the reviewer against its own R15
scoping work, before this block was emitted. Planning this round the reviewer grepped the suite for
tests that patch the CLI spawn, found exactly one — `test_structured_cli_envelope.py` patching
`packages.orchestration.pingpong_provider.subprocess.run` in its `_review` helper — read that helper
as reaching `_call_reviewer_structured` alone, and concluded that the version probe and `_call` could
migrate without touching a single test. FALSE: `test_4_legacy_non_schema_call_uses_result` sets
`REMEDY_REVIEWER_FREETEXT=1`, which routes the same helper through `_call`, so migrating `_call`
alone leaves that test patching a function the code no longer calls. The error was not the grep,
which was right about WHERE the mocks are; it was reading a list of patch TARGETS as a list of the
paths reached under them, when the reaching is decided by branches inside the tested code and by
environment variables the tests set — the R-0258 family, a source guard the block never named. It
cost no round only because the mandated dry run (planner_reviewer_prompt.md §3 checklist item 12)
ran the candidate slices against those suites in a `git archive` extraction, where it surfaced as
one red test in a set green at base. Counter-measure, binding on the reviewer from this round on:
when a block moves a call site, never infer the affected tests from a grep over mock targets — RUN
the candidate change against every suite touching the file and let the failures enumerate
themselves. The plan consequence is recorded, not hidden: `_call`, `_call_reviewer_structured` and
that mock are ONE indivisible unit, since re-pointing the mock at `_guarded_cli_run` reddens every
envelope test still on the stdlib spawn. R15 migrates the independent version probe; R16 carries the
coupled unit, already dry-run green. OPEN.
<<<END FIND1>>>
<<<SLICE PLANF>>>
## Current Step
R13, this round: record the R12 PASS, register R-0504, and migrate the FIRST of
T002a's five builder sites — `managed_builder_execution.py`:1160 — onto
`run_guarded` under a stage-1 builder policy, with behaviour-equality tests.
`exec_guard` gains its first caller in the running system.

## Next Steps
1. T002a's four REMAINING builder sites of amendment F085 D1 —
   `pingpong_provider.py`:952, 1075, 1208 and `stream_evidence.py`:595 — move to
   `run_guarded` the same way `managed_builder_execution.py` did at R13, each with
   its own behaviour-equality goldens.
<<<END PLANF>>>
<<<SLICE PLANT>>>
## Current Step
R15, this round: record the R14 PASS, register R-0507, and give the claude CLI seam
its guarded runner — `_cli_exec_policy`, `_decode_cli_stream`, `_guarded_cli_run` —
migrating `_resolve_version`, the one site no test's mock reaches, with goldens that
spawn a real fake CLI instead of mocking the stdlib.

## Next Steps
1. R16 migrates the coupled unit of R-0507: `_call`, `_call_reviewer_structured` and
   the envelope test's mock, which must move together, plus R-0506's fix — the stale
   absence claims in `exec_guard.py` and `managed_builder_execution.py`.
2. `stream_evidence.py`:595 is T002a's last site and is NOT a `subprocess.run` swap:
   it streams incrementally where `run_guarded` buffers, so its shape is decided first.
<<<END PLANT>>>
<<<SLICE IMP1F>>>
import json
import os
<<<END IMP1F>>>
<<<SLICE IMP1T>>>
import json
import locale
import os
<<<END IMP1T>>>
<<<SLICE IMP2F>>>
import shutil
import subprocess
import time
<<<END IMP2F>>>
<<<SLICE IMP2T>>>
import shutil
import signal
import subprocess
import time
<<<END IMP2T>>>
<<<SLICE IMP3F>>>
from packages.orchestration.model_aliases import resolve_model_alias
<<<END IMP3F>>>
<<<SLICE IMP3T>>>
from packages.orchestration.exec_guard import ExecGuardPolicy, run_guarded
from packages.orchestration.model_aliases import resolve_model_alias
<<<END IMP3T>>>
<<<SLICE CLSF>>>
class ClaudeCliProvider:
<<<END CLSF>>>
<<<SLICE CLST>>>
def _cli_exec_policy(timeout_sec: float, cwd: str | None) -> ExecGuardPolicy:
    """Stage-1 CLI-provider policy (F085 T002a) — only the limits this seam can prove.

    `output_cap_bytes` stays None on purpose: this seam parses the CLI's WHOLE JSON
    envelope, so a byte cap would cut a valid one mid-token and turn a working call
    into a parse failure. `env_allowlist` stays None for a kindred reason: the child
    is the operator's authenticated `claude` CLI and reads its credentials from the
    inherited environment. Both are stage-1 gaps, owed to T003's limitations
    document. Enforced and real: the wall deadline, the cwd pin, a zero core.
    """
    return ExecGuardPolicy(
        wall_timeout_seconds=float(timeout_sec), cwd=cwd, core_file_bytes=0,
    )


def _decode_cli_stream(raw: bytes) -> str:
    """Decode one guarded stream the way `text=True` decoded it.

    Text mode wrapped the pipe in a `TextIOWrapper` with the locale encoding and
    universal newlines; both are reproduced. The ONE intended difference is
    `errors="replace"` — text mode raised UnicodeDecodeError from inside the spawn
    and no caller here handled it, so a mojibake CLI now parses honestly instead.
    """
    text = raw.decode(locale.getpreferredencoding(False), errors="replace")
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _guarded_cli_run(cmd: list[str], timeout_sec: float,
                     cwd: str | None) -> subprocess.CompletedProcess[str]:
    """Run a CLI command under the stage-1 policy, shaped like `subprocess.run`.

    The single spawn point this module's provider calls migrate onto, and the seam
    the tests mock instead of the stdlib. A wall trip is re-raised as
    `subprocess.TimeoutExpired` and a signal death republished in the -SIGNUM form,
    so every caller keeps the error text it already produced: the migration changes
    the mechanism, never the observable outcome.
    """
    guarded = run_guarded(cmd, _cli_exec_policy(timeout_sec, cwd))
    if guarded.tripped_limit == "wall_timeout":
        raise subprocess.TimeoutExpired(cmd, timeout_sec)
    code = guarded.returncode
    if code is None:
        try:
            code = -int(signal.Signals[guarded.term_signal].value)
        except (KeyError, ValueError, TypeError):
            code = -1
    return subprocess.CompletedProcess(
        cmd, code,
        _decode_cli_stream(guarded.stdout), _decode_cli_stream(guarded.stderr),
    )


class ClaudeCliProvider:
<<<END CLST>>>
<<<SLICE PROBEF>>>
            proc = subprocess.run(
                [claude, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                # Pinned like every other provider call: an unpinned probe runs in
                # the operator's cwd and any stray write lands in the repo root.
                cwd=self._cwd,
            )
<<<END PROBEF>>>
<<<SLICE PROBET>>>
            proc = _guarded_cli_run(
                [claude, "--version"],
                # Pinned like every other provider call: an unpinned probe runs in
                # the operator's cwd and any stray write lands in the repo root.
                timeout_sec=5, cwd=self._cwd,
            )
<<<END PROBET>>>
<<<SLICE TESTNEW>>>
"""F085 T002a — the claude CLI seam gains its guarded runner, with equal behaviour.

Every case spawns a REAL fake-CLI script rather than mocking `subprocess`: a mock of
the spawn would pin the mechanism this round replaces, and could not tell a
translated wall trip from a forwarded `timeout=` keyword.
"""
from __future__ import annotations

import ast
import inspect
import stat
import subprocess
import textwrap

import pytest

from packages.orchestration import pingpong_provider as pp
from packages.orchestration.pingpong_provider import ClaudeCliProvider


def _provider(tmp_path, body: str) -> ClaudeCliProvider:
    """A provider whose `claude` binary is an executable stand-in running `body`."""
    path = tmp_path / "claude"
    path.write_text("#!/usr/bin/env python3\n" + textwrap.dedent(body))
    path.chmod(path.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    prov = ClaudeCliProvider()
    prov._claude_path = str(path)
    prov._cwd = str(tmp_path)
    return prov


class TestGuardedVersionProbe:
    def test_the_probe_reads_its_line_through_the_guard(self, tmp_path):
        prov = _provider(tmp_path, 'print("1.2.3 (Claude Code)")\n')
        assert prov._resolve_version() == "1.2.3 (Claude Code)"

    def test_a_failing_probe_yields_none_and_never_raises(self, tmp_path):
        assert _provider(tmp_path, "import sys; sys.exit(3)\n")._resolve_version() is None

    def test_a_wall_trip_is_republished_as_the_timeout_callers_already_catch(self, tmp_path):
        """On the runner, not the probe: the probe swallows every exception."""
        prov = _provider(tmp_path, "import time; time.sleep(30)\n")
        with pytest.raises(subprocess.TimeoutExpired):
            pp._guarded_cli_run([prov._claude_path], timeout_sec=1, cwd=prov._cwd)


class TestStageOnePolicyAndShape:
    def test_the_policy_enforces_what_it_can_and_leaves_the_rest_none(self):
        policy = pp._cli_exec_policy(12, "/somewhere")
        assert policy.wall_timeout_seconds == 12.0 and policy.cwd == "/somewhere"
        assert policy.core_file_bytes == 0
        # Deliberate stage-1 gaps, pinned so a later round cannot close them in silence.
        assert policy.output_cap_bytes is None and policy.env_allowlist is None
        assert policy.cpu_seconds is None and policy.address_space_bytes is None

    def test_the_probe_and_the_runner_hold_no_subprocess_spawn(self):
        def spawns(func):
            tree = ast.parse(textwrap.dedent(inspect.getsource(func)))
            return [n for n in ast.walk(tree)
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                    and n.func.attr in {"run", "Popen", "call", "check_output"}
                    and isinstance(n.func.value, ast.Name) and n.func.value.id == "subprocess"]

        assert spawns(ClaudeCliProvider._resolve_version) == []
        assert spawns(pp._guarded_cli_run) == []

    def test_a_signal_death_is_republished_as_the_negative_returncode(self, tmp_path):
        """`subprocess.run` reported a signal death as -SIGNUM; the guard reports a NAME."""
        prov = _provider(tmp_path, "import os, signal; os.kill(os.getpid(), signal.SIGKILL)\n")
        proc = pp._guarded_cli_run([prov._claude_path], timeout_sec=30, cwd=prov._cwd)
        assert proc.returncode == -9

    def test_text_mode_newline_translation_is_reproduced(self):
        assert pp._decode_cli_stream(b"a\r\nb\rc\nd") == "a\nb\nc\nd"

    def test_an_undecodable_byte_is_replaced_instead_of_raising(self):
        assert pp._decode_cli_stream(b"ok\xff") == "ok\ufffd"
<<<END TESTNEW>>>

## Application order

C1 appends RECORD1, then FIND1, to `.agent/live_review.md`, each preceded by exactly one blank line,
appending only — never rewriting a byte already there. C2 applies to
`packages/orchestration/pingpong_provider.py` the pairs IMP1, IMP2, IMP3, then CLST (whose FROM is
CLSF, the class statement, so the three helpers land immediately above it), then PROBE; and writes
`TESTNEW` as `tests/orchestration/test_claude_cli_exec_guard.py`. C3 applies PLANF→PLANT.

## Gates — every one is RUN and its real exit code recorded; "green" as a word is a finding

This session's Bash tool rejects `$?`, loops and command substitution BY FORM: read every exit code
as a real `subprocess.returncode` from `python3`.

G1 HYGIENE. `git status --porcelain` EMPTY before EVERY commit in the bundle; `.agent/STOP` re-read
from disk before the first and the last; `git worktree list` prints ONE line.

G2 TRANSPORT. `.agent/authored/f085-r15.md` after C0a, `.agent/last_block.md` after C0b and the
reviewer's original are byte-EQUAL: report one sha256, byte length and line count for all three.
C0b copies the COMMITTED C0a blob, never the scratch file.

G3 C1 SHAPE. The pre-C1 blob is a byte-exact PREFIX of the post-C1 file; HEAD equals it; the
remainder is byte-equal to blank + RECORD1 + blank + FIND1, in that order; each slice occurs exactly
ONCE in the whole file at HEAD and no `<<<SLICE` or `<<<END` line reaches it. Report C1's numstat as
a READING, not a prediction.

G4 ARITHMETIC over `.agent/live_review.md`, regexes `^- R-\d+ — `, `^Done: R-\d+ — `,
`^Landed: R-\d+`. Base 121 / 3 / 0, 118 open; expected at HEAD 122 / 3 / 0 → 119 open, a rise of
exactly one from one registration against no resolution. Report both symmetric differences,
duplicate-id counts, any resolution naming an unregistered id, and the max and next-free id.

G5 PLAN PAIR. PLANF is a REWRITE: 0 occurrences at HEAD, PLANT once. Report `.agent/plan.md` sha256,
bytes and a line count under 50, with `## Goal` and `## Risks` byte-IDENTICAL to base and
`## Current Step` and `## Next Steps` not.

G6 THE MIGRATION ITSELF. `python3 -m pytest tests/orchestration/test_claude_cli_exec_guard.py -q`
exits 0 with 8 passed. Then, by AST and not by text, over `pingpong_provider.py` at HEAD:
`_resolve_version` and `_guarded_cli_run` each hold ZERO
`subprocess.run/Popen/call/check_output` call nodes, and `_call` with `_call_reviewer_structured`
still hold ONE each — the coupled unit R16 carries. Report all four counts.

G7 REGRESSION EQUALITY, the seven files that drive this provider:
`python3 -m pytest tests/orchestration/test_structured_cli_envelope.py
tests/orchestration/test_pingpong.py tests/orchestration/test_provider_mode.py
tests/orchestration/test_failure_wiring.py
tests/orchestration/test_run_manifest_call_ref_canonical_numbers.py
tests/orchestration/test_provider_evidence_integration.py
tests/orchestration/test_stream_evidence_integration.py -q` exits 0 at HEAD with the SAME passed
count it reports at base. Take the base reading at C1, the last commit before C2 changes any code,
and report both numbers.

G8 LINT, scoped and deliberately not repo-wide: `python3 -m ruff check
packages/orchestration/pingpong_provider.py tests/orchestration/test_claude_cli_exec_guard.py`
exits 0. A repo-wide `ruff check packages/ tests/` is ALREADY RED at base (UP035 in `dag_schedule.py`,
F821 in `gauntlet_injection.py`, F401 and I001 in `test_plan_approval.py`), so it could not fail
honestly for this round and is not ordered.

G9 STATE READERS, because this round rewrites `.agent/` state: `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -q` exits 0
with 157 passed. CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` exits 0 with 42
passed. Both must match base.

G10 COMMIT HYGIENE, three readings. `git diff --name-only c5d80471..HEAD` measured BEFORE C4 equals
the six declared paths minus `.agent/handoff.md` — report the list; 0 paths outside it. The `+`
column of `git show --numstat` for C0a, C0b, C1, C2 and C3: none exceeds 500. C4's own count is
ordered nowhere, because a commit cannot measure itself; report it in the round report instead.
`git log --format=%h %p c5d80471..HEAD` shows ONE parent per commit and a linear chain; `git reflog`
shows every entry prefixed `commit:`, no amend, rebase, reset or force-push.

## Done when

Every commit in the bundle exists in order, the branch is pushed, every gate has been RUN with its exit
code recorded, `git status --porcelain` is empty, and `.agent/handoff.md` is rewritten per
docs/agents/handback_template.md with an item-status table covering C0a through C4. Run `gh pr list
--state open --json number,headRefName,baseRefName,isDraft` after the final push and report its
output; create NO pull request and merge nothing. Report what the commands PRINTED — a gate whose
result you did not read is a finding. If a gate contradicts this block, report the contradiction and
STOP: never repair text to make a number come out, never widen the change set. Declare every
deviation.
