# F085 R17 — record the R16 PASS and complete T002a's CLI half

Feature T2_F085 Sandbox hardening (stage 1) · Round R17 · Branch feature/f085-sandbox-hardening
Base of this round: the R16 handback commit, `git rev-parse HEAD` at start = 396ad913.
Fortschritt: ~65 % (T001 gebaut · R13-R16 PASS · T002a: Builder-Site und CLI-Half fertig nach dieser
Runde · `stream_evidence.py`, T002b-d, T003 offen).

## Goal

First the record: R16 passed the reviewer's gate and that verdict is written by C1. Then the work
R-0507 has been pointing at since R15 — `_call`, `_call_reviewer_structured` and the envelope
suite's mock move to `_guarded_cli_run` in ONE commit, because the finding proved they cannot move
separately. Five behaviour-equality goldens land with them. C3 then resolves R-0507 and R-0509,
after their fixes exist and not before.

Evidence already taken by the reviewer, reported so the worker does not repeat it: this exact change
was applied to a `git archive HEAD` extraction, where the eight-file provider suite goes from 341
passed at base to 346 at the extraction — the five new goldens, and no other movement — and ruff is
exit 0 on all three touched paths. FOUR red controls, each reddening exactly what it should:
restoring the stdlib spawn at the `_call` site reddens the AST guard and the one freetext envelope
test, restoring it at the structured site reddens ELEVEN, reverting the mock target alone reddens
the same eleven, and dropping the wall-trip re-raise reddens both timeout assertions.

## Bundle — in this order, none added, dropped or reordered

- C0a `docs(f085): save the R17 step block verbatim` — `.agent/authored/f085-r17.md`
- C0b `docs(f085): mirror the R17 block into last_block` — `.agent/last_block.md`
- C1 `docs(review): record the R16 PASS` — `.agent/live_review.md`
- C2 `feat(f085): route the remaining claude CLI calls through the guard` — the source file and both
  test files together, since the mock and the spawns are one indivisible unit (R-0507)
- C3 `docs(review): resolve R-0507 and R-0509 now that their fixes have landed` — `.agent/live_review.md`
- C4 `docs(f085): advance the plan to the checklist-promotion round` — `.agent/plan.md`
- C5 `docs(f085): rewrite the handback for R17` — `.agent/handoff.md`

C3 is a separate commit ON PURPOSE and must not be folded into C1: a resolution written before its
fix lands would claim on disk something no commit had yet done (planner_reviewer_prompt.md §4.4).

## Change set — exactly these paths, nothing else

`.agent/authored/f085-r17.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
`.agent/handoff.md`, `packages/orchestration/pingpong_provider.py`,
`tests/orchestration/test_claude_cli_exec_guard.py`,
`tests/orchestration/test_structured_cli_envelope.py`. Nothing under `docs/`, `apps/` or `scripts/`;
no other file under `packages/` or `tests/`. `exec_guard.py` and `managed_builder_execution.py` are
NOT touched — R16 settled them. `.agent/context.md` and `.agent/decisions.md` are NOT touched.

## Constraints

1. `cp` and the `remedy` CLI are denied here: copy with `shutil.copyfile` and prove the BYTE
   property, never the tool. Gate scratch lives under the gitignored `.remedy-wt/`.
2. Extract every slice programmatically by its one-line marker pair and apply it byte-verbatim,
   never retyped, reformatted or reworded: the review slices' regex-looking text and backticks are
   prose and land as prose.
3. Apply each FROM/TO pair by locating the FROM exactly once and replacing it with the TO; if it
   does not occur exactly once, STOP and report. Pair shapes, classified MECHANICALLY by containment
   at build time and printed here rather than judged by eye: CALLF→CALLT REWRITE, STRUCTF→STRUCTT REWRITE, MOCKF→MOCKT REWRITE, ASTF→ASTT REWRITE, GOLDF→GOLDT APPEND, PLANF→PLANT REWRITE. No "FROM 0x" reading is ordered for
   any pair not listed REWRITE — for GOLDF the FROM legitimately survives inside its own TO.
4. CALLT and STRUCTT are byte-identical lines applied at two DIFFERENT sites. Apply CALLF→CALLT
   first, then STRUCTF→STRUCTT; each FROM is distinct and occurs once, so locate by the FROM and
   never by the TO.
5. This round orders NO destructive check and no mutation red-proof. No gate below needs a
   disposable tree, and no worktree is added, removed or pruned.
6. Re-read `.agent/STOP` from disk before the FIRST commit and again before the LAST. If it exists
   at either point, finish the commit in flight, write the handback and end.

<<<SLICE RECORD1>>>
Gate: R16 — PASS, the record-and-repair round that paid down R-0506 and fixed the numbering its
predecessor broke. All ten ordered gates were re-run by the reviewer over 7185d949..396ad913 and
every one reproduces the handback's reading. TRANSPORT, disk-to-disk and not by digest fallback: the
reviewer's scratch original, the committed `.agent/authored/f085-r16.md` and `.agent/last_block.md`
are byte-EQUAL at sha256 bda1ca21008ed866792258791cd785bbde79b9aa975c7c018fbaf50fe82e903e, 22488 B,
316 lines. THE TWO APPEND COMMITS BOTH HOLD THEIR SHAPE: for C1 and again for C3 the pre-commit blob
is a byte-exact PREFIX of the post-commit file, each remainder is byte-equal to blank plus exactly
the slices that commit was given, every slice occurs ONCE in the whole file, and neither commit adds
a marker line; the numstat readings are 74 and 17, both append-only. Keeping the resolution in its
own commit AFTER the fix was the right shape and it verifies cleanly: at C1 the file reads
125 / 3 / 0 and only at C3 does it read 125 / 4 / 0, so at no commit did disk claim a resolution
whose fix had not landed. THE ARITHMETIC: 122 / 3 / 0 at base against 125 / 4 / 0 at HEAD, the open
set moving 119 to 121 by three registrations against one resolution, registered difference exactly
R-0508, R-0509 and R-0510, resolved difference exactly R-0506, no duplicate id and no resolution
naming an unregistered id. THE R-0509 REPAIR IS MEASURED, NOT ASSERTED: `## Next Steps` parses to
1, 2, 2, 3 at base and to 1, 2, 3, 4 at HEAD, with `## Goal` and `## Risks` byte-identical and the
file at 43 lines under its cap. THE R-0506 RESOLUTION HOLDS: all three retired phrases count 0 in
the HEAD blobs of both source files, and the caller grep scoped to `-- packages tests` names four
paths — the two modules that import the guard and the two suites that test them — which is exactly
the claim `exec_guard.py` no longer contradicts. The three suites owning those files are 152 passed
at C1 and 152 at HEAD, ruff is exit 0 on both touched paths, state readers 157 passed and the canary
42 passed. The change set is exactly the declared paths with 0 outside; insertions are 316, 240, 74,
16, 17 and 9, none over 500; seven single-parent commits, every reflog entry `commit:`-prefixed, no
amend, rebase, reset or force-push; the tree is clean and `git worktree list` is ONE line;
`.agent/handoff.md` measures 79 lines against its own declaration of 79, and its single declared
deviation — the token cap, cause named, no section dropped — is accurate. LAST_REVIEWED_SHA advances
to the R16 handback commit.
<<<END RECORD1>>>
<<<SLICE DONE1>>>
Done: R-0507 — the coupled unit this finding identified has been migrated as one commit, which is
the only way it could be migrated. `_call` and `_call_reviewer_structured` now reach the CLI through
`_guarded_cli_run`, and `tests/orchestration/test_structured_cli_envelope.py` patches that runner
instead of `subprocess.run`. The coupling the finding predicted is now MEASURED rather than argued:
in a `git archive` extraction the reviewer reverted each half alone, and restoring the stdlib spawn
at the structured site reddened ELEVEN tests while reverting the mock target alone reddened the same
eleven — neither half is separable, exactly as the finding said. The counter-measure it bound the
reviewer to has now been exercised for three consecutive rounds: every block since has been applied
to an extraction and run against the suites that touch its files before emission, and that practice
has caught a mis-scoped migration (this finding), a vacuous timeout assertion (R15) and a
self-contradicting marker gate (R16). Five behaviour-equality goldens land with the migration —
result text, non-zero exit with its stderr tail, the wall trip's message, a signal death's -SIGNUM
form and the caller-side character cap — and four red controls each reddened their own tests.
<<<END DONE1>>>
<<<SLICE DONE2>>>
Done: R-0509 — the malformed numbering is repaired on disk and the repair is measured at both ends.
`.agent/plan.md`'s `## Next Steps` parsed to 1, 2, 2, 3 at 7185d949 and parses to 1, 2, 3, 4 at
396ad913, with no repeated number, `## Goal` and `## Risks` byte-identical to base and the file at
43 lines under its 50-line cap. The repair was made the way the finding prescribed: R16's plan pair
spanned the WHOLE `## Next Steps` section rather than a prefix of it, so the surviving items were
renumbered by the pair itself instead of being left to collide with the new ones. The standing rule
the finding states — when a TO changes how many items a numbered list or table holds, the FROM spans
the whole structure — is not yet written into docs/agents/planner_reviewer_prompt.md §3, and this
resolution does not claim that it is; R-0508 and R-0510 stay OPEN for that promotion round, which is
where all three counter-measures stop being reviewer habit and start binding on disk.
<<<END DONE2>>>
<<<SLICE CALLF>>>
            proc = subprocess.run(
                argv,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
                cwd=self._cwd,
            )
<<<END CALLF>>>
<<<SLICE CALLT>>>
            proc = _guarded_cli_run(argv, timeout_sec=timeout_sec, cwd=self._cwd)
<<<END CALLT>>>
<<<SLICE STRUCTF>>>
            proc = subprocess.run(
                argv, capture_output=True, text=True, timeout=timeout_sec, cwd=self._cwd,
            )
<<<END STRUCTF>>>
<<<SLICE STRUCTT>>>
            proc = _guarded_cli_run(argv, timeout_sec=timeout_sec, cwd=self._cwd)
<<<END STRUCTT>>>
<<<SLICE MOCKF>>>
    with patch("packages.orchestration.pingpong_provider.subprocess.run", return_value=proc):
<<<END MOCKF>>>
<<<SLICE MOCKT>>>
    with patch("packages.orchestration.pingpong_provider._guarded_cli_run", return_value=proc):
<<<END MOCKT>>>
<<<SLICE ASTF>>>
        assert spawns(ClaudeCliProvider._resolve_version) == []
        assert spawns(pp._guarded_cli_run) == []
<<<END ASTF>>>
<<<SLICE ASTT>>>
        assert spawns(ClaudeCliProvider._resolve_version) == []
        assert spawns(ClaudeCliProvider._call) == []
        assert spawns(ClaudeCliProvider._call_reviewer_structured) == []
        assert spawns(pp._guarded_cli_run) == []
<<<END ASTT>>>
<<<SLICE GOLDF>>>
class TestStageOnePolicyAndShape:
<<<END GOLDF>>>
<<<SLICE GOLDT>>>
_ENVELOPE = """
    import json, sys
    sys.stdout.write(json.dumps({"type": "result", "subtype": "success",
                                 "is_error": False, "result": "HELLO"}))
"""


class TestGuardedProviderCalls:
    """The two paths that reach the CLI through `_call`; the envelope suite mocks
    `_guarded_cli_run`, so these are the only cases that spawn a real child."""

    def test_a_well_behaved_call_returns_its_result_text(self, tmp_path):
        text, dur, tokens, actuals, _ = _provider(tmp_path, _ENVELOPE)._call(
            "PROMPT", timeout_sec=30, max_output_chars=1000)
        assert text == "HELLO" and dur >= 0 and tokens == 0 and actuals is None

    def test_a_nonzero_exit_raises_with_the_code_and_the_stderr_tail(self, tmp_path):
        prov = _provider(tmp_path, 'import sys; sys.stderr.write("boom"); sys.exit(7)\n')
        with pytest.raises(RuntimeError) as err:
            prov._call("PROMPT", timeout_sec=30, max_output_chars=1000)
        assert "exited 7" in str(err.value) and "boom" in str(err.value)

    def test_a_wall_trip_reaches_the_timeout_message_this_seam_already_raised(self, tmp_path):
        prov = _provider(tmp_path, "import time; time.sleep(30)\n")
        with pytest.raises(RuntimeError) as err:
            prov._call("PROMPT", timeout_sec=1, max_output_chars=1000)
        assert "timed out after 1s" in str(err.value)

    def test_a_signal_death_keeps_the_negative_returncode_the_message_formats(self, tmp_path):
        prov = _provider(tmp_path, "import os, signal; os.kill(os.getpid(), signal.SIGKILL)\n")
        with pytest.raises(RuntimeError) as err:
            prov._call("PROMPT", timeout_sec=30, max_output_chars=1000)
        assert "exited -9" in str(err.value)

    def test_the_caller_side_char_cap_still_truncates(self, tmp_path):
        prov = _provider(tmp_path, _ENVELOPE.replace('"HELLO"', '"X" * 50'))
        text, _, _, _, _ = prov._call("PROMPT", timeout_sec=30, max_output_chars=10)
        assert text == "X" * 10 + "\n[OUTPUT TRUNCATED]"


class TestStageOnePolicyAndShape:
<<<END GOLDT>>>
<<<SLICE PLANF>>>
## Current Step
R16, this round: record the R15 PASS, register R-0508, R-0509 and R-0510 — three
defects in the reviewer's own R15 block that its worker reported rather than
repaired — resolve R-0506 by correcting the two falsified absence claims, and repair
the malformed numbering this section carried.

## Next Steps
1. R17 migrates the coupled unit of R-0507: `_call`, `_call_reviewer_structured` and
   the envelope test's mock, which must move together. The reviewer has already
   dry-run it green against an extraction, so the round is pairs and goldens only.
<<<END PLANF>>>
<<<SLICE PLANT>>>
## Current Step
R17, this round: record the R16 PASS, migrate R-0507's coupled unit — `_call`,
`_call_reviewer_structured` and the envelope test's mock move as one commit — with
five behaviour-equality goldens, then resolve R-0507 and R-0509. T002a's CLI half is
complete after this round; every `ClaudeCliProvider` spawn runs under the guard.

## Next Steps
1. Promote three standing rules into docs/agents/planner_reviewer_prompt.md §3, which
   is what R-0508 and R-0510 are still open for: classify pair shapes mechanically,
   let no heading count its own contents, and span a whole structure when a pair
   changes its arity. Reviewer habit binds nothing until it is on disk.
<<<END PLANT>>>

## Application order

C1 appends RECORD1 to `.agent/live_review.md`, preceded by exactly one blank line, appending only.
C2 applies CALLF→CALLT then STRUCTF→STRUCTT to `packages/orchestration/pingpong_provider.py`,
ASTF→ASTT then GOLDF→GOLDT to `tests/orchestration/test_claude_cli_exec_guard.py`, and MOCKF→MOCKT
to `tests/orchestration/test_structured_cli_envelope.py`. C3 appends DONE1 then DONE2 to
`.agent/live_review.md`, each preceded by exactly one blank line. C4 applies PLANF→PLANT.

## Gates — every one is RUN and its real exit code recorded; "green" as a word is a finding

This session's Bash tool rejects `$?`, loops and command substitution BY FORM: read every exit code
as a real `subprocess.returncode` from `python3`.

G1 HYGIENE. `git status --porcelain` EMPTY before EVERY commit in the bundle; `.agent/STOP` re-read
from disk before the first and the last; `git worktree list` prints ONE line.

G2 TRANSPORT. `.agent/authored/f085-r17.md` after C0a, `.agent/last_block.md` after C0b and the
reviewer's original are byte-EQUAL: report one sha256, byte length and line count for all three.
C0b copies the COMMITTED C0a blob, never the scratch file.

G3 APPEND SHAPE, twice. For C1 and again for C3: the pre-commit blob is a byte-exact PREFIX of the
post-commit file, HEAD equals it, and the remainder is byte-equal to blank + the ordered slices for
that commit — RECORD1 for C1, and DONE1 then DONE2 for C3. Each occurs exactly ONCE in the whole
file at HEAD, and neither commit adds a marker line. Report both numstat pairs as READINGS.

G4 ARITHMETIC over `.agent/live_review.md`, regexes `^- R-\d+ — `, `^Done: R-\d+ — `,
`^Landed: R-\d+`. Base 125 / 4 / 0, 121 open; after C1 unchanged at 125 / 4 / 0, because a record
adds no id; expected at HEAD 125 / 6 / 0 → 119 open, two resolutions and NO registration. Report the
reading after C1 as well as at HEAD, both symmetric differences, duplicate-id counts, any resolution
naming an unregistered id, and the max and next-free id.

G5 PLAN PAIR. PLANF occurs 0 times at HEAD and PLANT once. Report `.agent/plan.md` sha256, bytes and
a line count under 50, with `## Goal` and `## Risks` byte-IDENTICAL to base, and report the ordered
numbers `## Next Steps` parses to — they must have no repeat, which is the R-0509 rule holding.

G6 THE MIGRATION. By AST and not by text, over `pingpong_provider.py` at HEAD: `_resolve_version`,
`_call`, `_call_reviewer_structured` and `_guarded_cli_run` each hold ZERO
`subprocess.run/Popen/call/check_output` call nodes — report all four counts. That is T002a's CLI
half complete, so also report the count of such nodes in the WHOLE module, which must be 0.

G7 THE PROVIDER SUITE, eight files: `python3 -m pytest
tests/orchestration/test_claude_cli_exec_guard.py tests/orchestration/test_structured_cli_envelope.py
tests/orchestration/test_pingpong.py tests/orchestration/test_provider_mode.py
tests/orchestration/test_failure_wiring.py
tests/orchestration/test_run_manifest_call_ref_canonical_numbers.py
tests/orchestration/test_provider_evidence_integration.py
tests/orchestration/test_stream_evidence_integration.py -q` exits 0 at both ends. Take the base
reading at C1, the last commit before C2 changes anything, and report BOTH numbers: they are NOT
equal — the count must rise by exactly the five goldens C2 adds, and reporting an equality here
would be reporting a number that cannot be true.

G8 LINT, scoped and deliberately not repo-wide: `python3 -m ruff check
packages/orchestration/pingpong_provider.py tests/orchestration/test_claude_cli_exec_guard.py
tests/orchestration/test_structured_cli_envelope.py` exits 0. A repo-wide `ruff check packages/
tests/` is ALREADY RED at base (UP035 in `dag_schedule.py`, F821 in `gauntlet_injection.py`, F401
and I001 in `test_plan_approval.py`), so it could not fail honestly here and is not ordered.

G9 STATE READERS, because this round rewrites `.agent/` state: `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -q` exits 0
with 157 passed. CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` exits 0 with 42
passed. Both must match base.

G10 COMMIT HYGIENE, three readings. `git diff --name-only 396ad913..HEAD` measured BEFORE C5 equals
the declared paths minus `.agent/handoff.md` — report the list; 0 paths outside it. The `+` column
of `git show --numstat` for C0a, C0b, C1, C2, C3 and C4: none exceeds 500. C5's own count is ordered
nowhere, because a commit cannot measure itself; report it in the round report instead.
`git log --format=%h %p 396ad913..HEAD` shows ONE parent per commit and a linear chain; `git reflog`
shows every entry prefixed `commit:`, no amend, rebase, reset or force-push.

## Done when

Every commit in the bundle exists in order, the branch is pushed, every gate has been RUN with its
exit code recorded, `git status --porcelain` is empty, and `.agent/handoff.md` is rewritten per
docs/agents/handback_template.md with an item-status table covering C0a through C5. Run `gh pr list
--state open --json number,headRefName,baseRefName,isDraft` after the final push and report its
output; create NO pull request and merge nothing. Report what the commands PRINTED — a gate whose
result you did not read is a finding. If a gate contradicts this block, report the contradiction and
STOP: never repair text to make a number come out, never widen the change set. Declare every
deviation.
