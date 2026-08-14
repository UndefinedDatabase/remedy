── STEP T002-PREP — F057 · ROUND 2 ───────────────────────────────────

Goal:        Persist the R1 verdict and findings R-0363 to R-0366, then fix
             R-0365 (a docstring that claims a call graph the code does not
             have) and R-0366 (a test asserting a bare Exception). T002 itself
             is NOT in this round.

Bundle:      C0a save this block · C0b point last_block at it · C1 the R1
             verdict + the four findings · C2 the R-0365 fix · C3 the R-0366
             fix · C4 handback.

Change:      Exactly these files:
             - `.agent/authored/f057-r2.md` (NEW, C0a)
             - `.agent/last_block.md` (C0b)
             - `.agent/live_review.md` (C1, APPEND only)
             - `packages/orchestration/rate_governor.py` (C2, ONE docstring)
             - `tests/orchestration/test_rate_governor.py` (C3, one test + one import)
             - `.agent/plan.md` (C4, current step)
             - `.agent/handoff.md` (C4)
             Nothing else. No new module, no governor, no `acquire`, no clock.

Staging:     EXPLICIT PATHS ONLY. Never `git add -A`. Push after every commit.

── C0a / C0b ─────────────────────────────────────────────────────────
Save this ENTIRE block verbatim (from the `── STEP T002-PREP` line to the end
of the ROUND GATES list) to `.agent/authored/f057-r2.md`; commit alone.
  Subject: `chore(f057): save the R2 block verbatim`
Copy it to `.agent/last_block.md`, byte-identical; `cmp` → exit 0; commit alone.
  Subject: `chore(f057): point last_block at the R2 block`

Apply every authored text below DISK TO DISK: extract it from the committed
`.agent/authored/f057-r2.md` between its markers, write that to the target,
then prove applied == extracted. Never retype an authored text.

── C1 — the verdict and the findings, persisted FIRST ─────────────────
File `.agent/live_review.md`. The file currently ENDS with the carried R-0361
line. APPEND the block below at the very END, preceded by exactly one blank
line. Change nothing above it. R-0361 must remain byte-identical — its sha256
is still `70a8c9fb1a6ddebd2a1592b467cf9cb7e18f43ad0449c245d110bc0f1f056a7b`.

Each `- R-XXXX — ` finding is ONE physical line. Do not re-wrap them.

REVIEWER-AUTHORED. Apply byte for byte. Never write a `Done:` paragraph of your
own — that text is the reviewer's alone (planner_reviewer_prompt.md §4 item 4).
If a fix lands before the reviewer has authored its resolution, write
`Landed: R-XXXX — <one line: what changed, which commit>` and nothing else.

>>> GATE-R1 >>>
Gate: R1 — PASS. Verification tier: round gate plus canary. Every value below was re-measured by the reviewer against the disk rather than read out of the handback. Re-run by the reviewer: `tests/orchestration/test_rate_governor.py` → `46 passed`; `tests/docs/` together with the three state-file contract readers (`tests/ui_server/test_dashboard_contract.py`, `tests/regression/test_resource_safety.py`, `tests/orchestration/test_test_runner.py`) → `437 passed`; the canary `tests/cli/test_golden_path.py` → `42 passed`; `wc -l < .agent/plan.md` → 34; `cmp .agent/authored/f057-r1.md .agent/last_block.md` → exit 0. The change set is exactly the ten files the R1 block named — `git diff --name-only 21c8148e..HEAD` lists no eleventh — and the Do-not-touch set held: `git diff --stat` over `provider_timeouts.py`, `pingpong_loop.py` and `stream_evidence.py` is EMPTY, and `grep -rn 'rate_governor' packages/ apps/` outside the module itself returns nothing, so T001 is correctly unwired. TRANSPORT was proved disk to disk by the reviewer and not by the worker's script: the PLAN and CONTEXT slices extracted from the committed `.agent/authored/f057-r1.md` equal the applied files byte for byte, `.agent/live_review.md` starts with the extracted LIVE-REVIEW slice and its remaining tail is exactly the carried R-0361 line at sha256 `70a8c9fb1a6ddebd2a1592b467cf9cb7e18f43ad0449c245d110bc0f1f056a7b`, and the DECISION slice occurs exactly once in `.agent/decisions.md`. The RED-PROOF was reproduced by the reviewer in its own disposable worktree at `36b745bd`, import path printed first and confirmed inside that worktree: `is_rate_limit_error` replaced by `return False` gives `10 failed, 36 passed`, and `classify_rate_limit_reason` replaced by `return None` gives `17 failed, 29 passed` — both identical to the worker's report. The T001 inventory was verified citation by citation: `tests/orchestration/fixtures/stream/retry_and_error.jsonl` really carries `overloaded_error` on line 2 and `rate_limit` on line 3, `packages/orchestration/mission_dossier.py:980` really is `RecallFact("R003", "the vendor sandbox rate-limits the nightly run")` and is correctly excluded as demo prose, and the worker found one real sample beyond the four the block seeded. No block condition was hit: no fabricated value, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change. The two declared deviations are both accepted — the C3 split is AGENTS.md's own remedy for a 633-insertion pair that nothing imports, and the red `ruff check` is a property of `main` that this round did not add to, which the reviewer confirmed independently at `21c8148e`. That the ruff gate was ordered at all is the reviewer's defect and is recorded below as R-0364, not charged to the round.
<<< GATE-R1 <<<

>>> FINDINGS-R1 >>>
- R-0363 — Low — the R1 block was emitted over its own 400-line cap. `wc -l < .agent/authored/f057-r1.md` is 404, against the 400-line limit DECISION F105 D5 sets and which pre-emission checklist item 1 (docs/agents/planner_reviewer_prompt.md §3) orders measured mechanically on the FINAL bytes before any block leaves the reviewer. The reviewer never measured it. Nothing downstream broke — the worker saved the block verbatim as required and declared the end boundary it used — but the check exists precisely because a worker required to save a block byte for byte cannot trim it, so an oversize block becomes a declared deviation on a round that did nothing wrong. The counter-measure is not a new rule, it is running the rule that already exists. OPEN.
- R-0364 — Medium — the R1 block ordered a round gate the reviewer had never executed, and that gate was already red before the round began. Gate 14 of the R1 block demanded `python3 -m ruff check` → exit 0. The reviewer's pre-emission baseline covered `tests/docs/` (`295 passed`) and `tests/cli/test_golden_path.py` (`42 passed`) and did not cover ruff at all. At the base commit `21c8148e`, in the reviewer's own disposable worktree, `python3 -m ruff check --statistics` reports 20 I001, 4 F401, 1 F821 and 1 UP035 — 26 errors, exit 1 — statistically identical to the branch, so R1 added none of them, and `ruff check` over the two new files alone is `All checks passed!`, exit 0. This is the R-0361 family recurring exactly one round after R-0361 was deliberately carried forward to keep its counter-measure in force, and it is the same class as R-0252, R-0336 and R-0350: a gate whose expected value the reviewer never computed from the tool that produces it. The worker behaved correctly — it ran the gate, reported the real exit code, proved the condition pre-existing, and declined to repair an unrelated defect on a feature branch — which means the round spent a declared deviation to prove a reviewer mistake. Counter-measure, binding from R2 on and additional to R-0361's: every gate a block orders is executed by the reviewer at the base commit BEFORE emission, and a gate already red at the base is either dropped from the block or ordered with its known-red baseline stated inline, so the worker is never asked to meet an unreachable condition. OPEN.
- R-0365 — Low — a docstring in the new module claims a call graph the code does not have. In `packages/orchestration/rate_governor.py` the docstring of `is_rate_limit_error` states that "The governor, the readers below and anything T003 wires up all call this one function". The readers do not: `read_run_event_signals` and `read_retry_reason_signals` both call `normalize_rate_limit_signal`, which calls `classify_rate_limit_reason` directly, and nothing in the module calls the predicate at all. The reviewer proved it by mutation in its own disposable worktree at `36b745bd` — replacing `is_rate_limit_error` with `return False` leaves every reader test green at `10 failed, 36 passed`, while replacing `classify_rate_limit_reason` with `return None` reaches them at `17 failed, 29 passed`. There is no behavioural defect: the predicate is that function's emptiness test, so the two can never disagree, and the anti-drift property the module argues for is real. But it is carried by `classify_rate_limit_reason`, and a T003 author who reads this docstring would believe that wiring to `is_rate_limit_error` puts them on the shared path. AGENTS.md's discoverability rules make the one-line WHY above a definition the thing a searcher lands on, which is exactly why it may not describe a call graph that does not exist. Fix by naming the function that actually owns the table and saying what the predicate is for. OPEN.
- R-0366 — Low — the frozen-dataclass test asserts a bare `Exception`. `tests/orchestration/test_rate_governor.py::test_signal_is_frozen` wraps `signal.provider = "other"` in `pytest.raises(Exception)`. It does discriminate the property under test, because assigning to a field of a non-frozen dataclass raises nothing and the test would fail, so this is imprecision rather than a false green. But `Exception` also passes on an unrelated failure — a misspelled attribute, an import-time error inside the block — so the test cannot distinguish "the dataclass is frozen" from "something went wrong". Fix by asserting the exception the property actually raises, `dataclasses.FrozenInstanceError`. OPEN.
<<< FINDINGS-R1 <<<

Commit C1 ALONE.
  Subject: `docs(f057): record the R1 verdict and register four findings`
Gates: R-0363, R-0364, R-0365, R-0366 each present exactly once as a line
       starting `- R-XXXX — ` · `Gate: R1 — PASS` present exactly once ·
       the R-0361 line still sha256 `70a8c9fb1a6ddebd2a1592b467cf9cb7e18f43ad0449c245d110bc0f1f056a7b` ·
       `## Steps` still exactly 1

── C2 — fix R-0365 ────────────────────────────────────────────────────
File `packages/orchestration/rate_governor.py`, the docstring of
`is_rate_limit_error` ONLY. This is a REWRITE pair: FROM and TO are disjoint.

FROM (4 physical lines, currently the 2nd paragraph of that docstring):
>>> R0365-FROM >>>
    THE rate-limit predicate. The governor, the readers below and anything T003 wires up
    all call this one function, for the reason ``is_timeout_error`` in
    ``packages/orchestration/provider_timeouts.py`` states: two definitions of "what
    counts as X" drift apart, and the drift is the bug.
<<< R0365-FROM <<<

TO:
>>> R0365-TO >>>
    THE rate-limit predicate, for callers that only need a yes or no — T003's seam, and
    any guard that branches on "is this a rate limit at all". It is the emptiness test of
    :func:`classify_rate_limit_reason`, which owns the single wording table; the readers
    in this module reach that table through :func:`normalize_rate_limit_signal` rather
    than through this predicate, so the two can never disagree about a marker. That
    single-table shape is what ``is_timeout_error`` in
    ``packages/orchestration/provider_timeouts.py`` argues for: two definitions of "what
    counts as X" drift apart, and the drift is the bug.
<<< R0365-TO <<<

After the edit the FROM text must appear 0 times and the TO text exactly once.
Change nothing else in the file — no code, no other docstring.

Commit C2 ALONE.
  Subject: `docs(f057): correct the rate-limit predicate's call-graph claim`
Gates: `python3 -m pytest tests/orchestration/test_rate_governor.py -q` → exit 0 ·
       `python3 -m ruff check packages/orchestration/rate_governor.py` → exit 0 ·
       `git show --numstat HEAD -- packages/orchestration/rate_governor.py` → `8 4`

── C3 — fix R-0366 ────────────────────────────────────────────────────
File `tests/orchestration/test_rate_governor.py`. Two edits, one commit.

(a) Add `import dataclasses` to the stdlib import group, keeping the group
    alphabetically sorted as ruff's I001 expects (it currently reads
    `import json` then `from pathlib import Path`).

(b) REWRITE pair on the test body:

FROM:
>>> R0366-FROM >>>
    with pytest.raises(Exception):
        signal.provider = "other"  # type: ignore[misc]
<<< R0366-FROM <<<

TO:
>>> R0366-TO >>>
    with pytest.raises(dataclasses.FrozenInstanceError):
        signal.provider = "other"  # type: ignore[misc]
<<< R0366-TO <<<

After the edit `pytest.raises(Exception)` must appear 0 times in the file.

Commit C3 ALONE.
  Subject: `test(f057): assert FrozenInstanceError instead of bare Exception`
Gates: `python3 -m pytest tests/orchestration/test_rate_governor.py -q` → exit 0,
         report the count (it was 46 before this round) ·
       `python3 -m ruff check tests/orchestration/test_rate_governor.py` → exit 0 ·
       occurrences of `pytest.raises(Exception)` in that file → 0

RED-PROOF for C3, as a PROBE — report the outcome, do not assume a colour. It
runs ONLY inside a disposable worktree under `.remedy-wt/`, never in this
checkout. Create the worktree at HEAD, first print the import path with
`python3 -c "import packages.orchestration.rate_governor as m; print('MODULE', m.__file__)"`
run from inside it and report the printed path — if it is not inside the
worktree the probe proves nothing and you must say so. Then remove
`frozen=True` from the `RateLimitSignal` dataclass decorator there, run
`python3 -m pytest tests/orchestration/test_rate_governor.py -q`, and report
which ids fail and how many. Then remove and prune the worktree;
`git worktree list` must return to ONE line and the primary checkout's
`git status --porcelain` must be empty.

── C4 — handback ──────────────────────────────────────────────────────
Update `.agent/plan.md` — rewrite the `## Current Step` section only, so it
names R2 as done and T002 as next; keep the file under 50 lines and keep the
`## Goal` and `## Next Steps` headings. Update the open-findings line at the
top to read `Open findings: R-0361, R-0362, R-0363, R-0364, R-0365, R-0366` and
`Next free finding id: R-0367`.

Rewrite `.agent/handoff.md` (never append) per AGENTS.md: feature + round,
branch, commit SHAs, changed-files table, REAL verification results with real
exit codes, open-findings count, next expected action. Under 60 lines, or carry
a "Deviations, declared" line naming the real count and the mandated content
that caused it (DECISION D15). Include the item-status table with C0a, C0b, C1,
C2, C3, C4 each exactly once.

State in the handoff, under "Next", that the next session's first action is
Phase 0 of docs/agents/self_drive_protocol.md and then Phase 1 rule 1 —
re-read `.agent/STOP` — BEFORE rule 2, and that the work itself is T002.

Commit C4 ALONE.
  Subject: `chore(f057): handback R2`

── ROUND GATES — run every one, record the REAL exit code ─────────────
 1. `git status --porcelain` → empty
 2. `git worktree list` → exactly one line
 3. `git branch --show-current` → `feature/f057-rate-limit-scheduler`
 4. `Gate: R1 — PASS` in `.agent/live_review.md` → exactly 1
 5. each of `- R-0363 — `, `- R-0364 — `, `- R-0365 — `, `- R-0366 — ` → exactly 1
 6. the R-0361 line's sha256 → `70a8c9fb1a6ddebd2a1592b467cf9cb7e18f43ad0449c245d110bc0f1f056a7b`
 7. `## Steps` in `.agent/live_review.md` → exactly 1
 8. `pytest.raises(Exception)` in the test file → 0
 9. `python3 -m pytest tests/orchestration/test_rate_governor.py -q` → exit 0
10. `python3 -m pytest tests/docs/ -q` → exit 0
11. `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0 (canary; 42 on main)
12. `python3 -m ruff check packages/orchestration/rate_governor.py tests/orchestration/test_rate_governor.py` → exit 0
13. `wc -l < .agent/plan.md` → under 50
14. `cmp .agent/authored/f057-r2.md .agent/last_block.md` → exit 0
15. `git diff --stat 21c8148e..HEAD -- packages/orchestration/provider_timeouts.py packages/orchestration/pingpong_loop.py packages/orchestration/stream_evidence.py` → EMPTY
16. the C3 red-proof probe outcome, with the printed MODULE path

KNOWN-RED BASELINE, stated per R-0364's counter-measure: repository-wide
`python3 -m ruff check` exits 1 with 26 errors (20 I001, 4 F401, 1 F821,
1 UP035) at base `21c8148e`, verified by the reviewer in its own worktree. It
is therefore NOT a gate this round. Gate 12 is scoped to the two files this
feature owns, where the reviewer measured `All checks passed!`, exit 0.

Report every gate with its real output. "Green" as a word is not a result. If a
gate goes red, STOP and report the exact output.
