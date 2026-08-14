── STEP T001 — F057 · ROUND 1 ────────────────────────────────────────

Goal:        Claim F057, reset the round state carrying the one open finding
             forward instead of dropping it, record DECISION F057 D1, and
             build T001: ONE place that turns the rate-limit signal shapes
             this repo really emits into a normalized signal, with unit tests
             over samples extracted from existing evidence. Nothing calls the
             new module yet — T001 is normalization only.

Bundle:      C0a save this block · C0b point last_block at it · C1 the
             live_review reset + DECISION F057 D1 · C2 the STATUS claim and
             the plan/context rewrites · C3 T001 module + tests · C4 handback.

Change:      Exactly these files, nothing beyond them:
             - `.agent/authored/f057-r1.md` (NEW, C0a)
             - `.agent/last_block.md` (C0b)
             - `.agent/live_review.md` (C1, full replacement)
             - `.agent/decisions.md` (C1, APPEND only)
             - `docs/roadmap/STATUS.md` (C2, ONE line)
             - `.agent/plan.md` (C2, full replacement)
             - `.agent/context.md` (C2, full replacement)
             - `packages/orchestration/rate_governor.py` (NEW, C3)
             - `tests/orchestration/test_rate_governor.py` (NEW, C3)
             - `.agent/handoff.md` (C4)
             NO other production file. In particular
             `packages/orchestration/provider_timeouts.py`,
             `packages/orchestration/pingpong_loop.py`,
             `packages/orchestration/stream_evidence.py` and every provider
             adapter stay BYTE-IDENTICAL this round — they are the feature
             file's Do-not-touch list plus the T003 seam.

Staging:     EXPLICIT PATHS ONLY. Never `git add -A`. Push after every commit.

── STEP 0 — the branch ────────────────────────────────────────────────
`git status --porcelain` must be empty and `.agent/STOP` must not exist. If
either fails, STOP and report.
    git checkout main
    git pull --ff-only
    git checkout -b feature/f057-rate-limit-scheduler
main is expected at 21c8148e. If it is not, report the SHA and continue.

── C0a / C0b ─────────────────────────────────────────────────────────
Save this ENTIRE block — from the `── STEP T001` line through the end of the
gate list — verbatim to `.agent/authored/f057-r1.md`; commit alone.
  Subject: `chore(f057): save the R1 block verbatim`
Copy that file to `.agent/last_block.md`, byte-identical (`cp`, then `cmp` them
— exit 0); commit alone.
  Subject: `chore(f057): point last_block at the R1 block`

Every authored text below is applied DISK TO DISK: extract it from the
committed `.agent/authored/f057-r1.md` between its markers with `sed`, write
that to the target, then prove the applied bytes equal the extracted bytes.
Do not retype an authored text by hand. The marker lines themselves
(`>>> NAME >>>` / `<<< NAME <<<`) are never written into a target file.

── C1 — findings persist FIRST ────────────────────────────────────────
Two files, ONE commit.

(a) `.agent/live_review.md` — REPLACE THE WHOLE FILE with the LIVE-REVIEW text
below, then append ONE more line to it: the R-0361 paragraph carried forward
VERBATIM from the previous record. Get that line from git, never by retyping:

    git show 21c8148e:.agent/live_review.md | grep '^- R-0361 — ' >> .agent/live_review.md

That paragraph is ONE physical line of 1797 bytes whose sha256 is
`70a8c9fb1a6ddebd2a1592b467cf9cb7e18f43ad0449c245d110bc0f1f056a7b`. Verify
with `grep '^- R-0361 — ' .agent/live_review.md | sha256sum` and report the
digest. If it differs, STOP.

The LIVE-REVIEW text ends with the R-0362 paragraph and a blank line, so the
carried R-0361 line lands after exactly one blank line. R-0361 must be the LAST
line of the finished file.

>>> LIVE-REVIEW >>>
# Live Review — F057 Rate-limit-aware scheduler

> Round-by-round review record for the F057 branch, reset at the feature claim.
> The paydown0814 record closed with PR #198, merged 2026-08-14; that branch's
> closing verdict lives in its handoff and in the PR, per
> docs/agents/planner_reviewer_prompt.md §4 item 13. Finding ids continue the
> monotonic R-XXXX series across the reset. Next free id: R-0363.
>
> This reset CARRIES the open set forward rather than dropping it. R-0361 was
> open when the previous record closed and is reproduced verbatim at the end of
> this file, byte for byte out of `21c8148e:.agent/live_review.md`. See
> DECISION F057 D1 in `.agent/decisions.md`.

## Steps
R1 claim F057, reset this record carrying R-0361 forward, register R-0362,
record DECISION F057 D1, and build T001 — one place that normalizes the
rate-limit signal shapes this repo really emits, with unit tests over samples
extracted from existing evidence → R2 T002, the governor itself: per-provider
cooldown state, `acquire()` with a budget deadline, an injected clock, and the
stop-beats-wait ordering → R3 T003, the seam integration at the provider-call
choke point, wait evidence, the report line, and the limit-emitting fixture
end-to-end → integration gate → closure.

## Findings

- R-0362 — Medium — the open-finding set is silently discarded at every branch claim, and Rule A2 forbids the claim that discards it. ROADMAP.md:27 states Rule A2 as "Every block ends with a final review: PASS or FINDINGS. No new feature is started while findings are open", and `docs/agents/reviewer_conventions.md` restates it as "No new feature starts while findings are open (A2)". At the F045 closure the reviewer's own GATE-R15 entry recorded the open set as exactly three — R-0350, R-0354 and R-0358, all Low — after RECOMPUTING it from the record per the pre-emission checklist's item 10. None of those three ids appears anywhere in the paydown0814 record that replaced it: `git show f789ebc8:.agent/live_review.md` carries only R-0359, R-0360 and R-0361. The reset therefore did not resolve them, did not defer them and did not name them; it dropped them, and the same mechanism was about to drop R-0361 at this claim. Two rules are in conflict and neither yields on its own: A2 read literally blocks every feature claim that follows a PASS_WITH_RISKS closure, which is six of the last seven closures in `docs/roadmap/STATUS.md`, while the reset as practised makes A2 unenforceable by erasing its input. No governing document authorises the erasure — `docs/agents/planner_reviewer_prompt.md` §1 says the record is reset at the claim but says nothing about what happens to findings that are open when it is, and `docs/roadmap/STATUS_closure_protocol.md` routes only CLOSURE CANDIDATES, which are explicitly not findings and spend no id. Registered here rather than acted on silently, per §2's rule that a practice invoked without a doc pointer is a finding candidate in the same brief. The structural half of the fix is applied in this round: this record carries R-0361 forward verbatim instead of dropping it, and DECISION F057 D1 states the reading under which the claim proceeds. The documentation half — an explicit carry-forward rule in `docs/agents/planner_reviewer_prompt.md` §1, and whatever becomes of R-0350, R-0354 and R-0358 — is NOT in this feature's scope: AGENTS.md forbids mixing an unrelated fix into a feature branch, so it belongs on its own paydown branch, exactly as DECISION F045 D8 routed the reviewer-conventions repair. OPEN.

<<< LIVE-REVIEW <<<

(b) `.agent/decisions.md` — APPEND the DECISION text below to the very END of
the file, preceded by exactly one blank line. Change nothing above it.

>>> DECISION >>>
## DECISION F057 D1 (2026-08-14) — Rule A2's open-finding bar is read per review record, and the reset CARRIES open findings instead of dropping them

F057 is claimed with R-0361 open. Rule A2 (ROADMAP.md:27) says no new feature
is started while findings are open, so this decision states the reading under
which the claim proceeds, and pays for it structurally rather than by
exception.

WHY this reading and not the literal one. Six of the last seven closures in
`docs/roadmap/STATUS.md` are PASS_WITH_RISKS — F104, F105, F107, F111, F115 and
F045 — and a PASS_WITH_RISKS closure by construction leaves findings open. Read
literally, A2 would have blocked every feature claim since F103, including the
five the ledger records as accepted. The literal reading is therefore not the
one this project has been operating under, and adopting it now would stall the
roadmap on findings the closure protocol already decided were acceptable to
accept. A2's enforceable content is that a REVIEW RECORD does not close over
unresolved work, which the closure protocol's PASS_WITH_RISKS path already
gates.

WHAT IS WRONG WITH THE PRACTICE, and what this decision fixes. The practice did
not just read A2 narrowly; it erased A2's input. At the F045 closure the
reviewer recorded the open set as R-0350, R-0354 and R-0358, and the very next
record — `git show f789ebc8:.agent/live_review.md` — contains none of them. The
reset dropped three live findings without resolving, deferring or naming them.
So from this branch on, a reset CARRIES the open set forward verbatim: this
record reproduces R-0361 byte for byte out of `21c8148e:.agent/live_review.md`,
and a carried finding stays open until reviewer-authored `Done:` text closes it.
Carrying costs one line per open finding and makes A2 measurable again; dropping
costs nothing and makes it meaningless.

WHY A2 ITSELF IS NOT AMENDED HERE. AGENTS.md forbids agents editing
`docs/roadmap/ROADMAP.md` unless the operator explicitly requests it, so the
reading lives here and in the operator brief, where the operator can veto it at
any later relay. Nothing waits for an answer
(docs/agents/planner_reviewer_prompt.md §4 item 7).

SCOPE, stated so it cannot drift. This decision authorises the F057 claim and
the carry-forward. It does NOT resolve R-0361, and it does NOT recover R-0350,
R-0354 or R-0358 — that recovery and the matching rule text in
`docs/agents/planner_reviewer_prompt.md` §1 belong to their own paydown branch,
because AGENTS.md forbids mixing an unrelated fix into a feature branch. This is
the same routing DECISION F045 D8 used for the reviewer-conventions repair.

HOW TO REVERSE. Delete this decision and read A2 literally. Doing so requires
first resolving R-0361 and recovering R-0350, R-0354 and R-0358 on a paydown
branch, because otherwise no feature can be claimed at all.
<<< DECISION <<<

Commit C1 ALONE.
  Subject: `docs(f057): reset the review record and carry R-0361 forward`
Gates: `grep -c '^## Steps' .agent/live_review.md` → 1 ·
       `grep -c '^- R-0362 — ' .agent/live_review.md` → 1 ·
       `grep -c '^- R-0361 — ' .agent/live_review.md` → 1 ·
       `grep '^- R-0361 — ' .agent/live_review.md | sha256sum` → the digest above ·
       `tail -n 1 .agent/live_review.md | cut -c1-12` → `- R-0361 — ` ·
       `grep -c '^## DECISION F057 D1 ' .agent/decisions.md` → 1

── C2 — the claim ─────────────────────────────────────────────────────
Three files, ONE commit.

(a) `docs/roadmap/STATUS.md` — ONE line, a REWRITE pair (the TO does not
contain the FROM):
    FROM: `- [ ] F057 — Rate-limit-aware scheduler`
    TO:   `- [~] F057 — Rate-limit-aware scheduler`
Change nothing else in that file. After the edit, FROM must appear 0x and TO
exactly 1x.

(b) `.agent/plan.md` — REPLACE THE WHOLE FILE:

>>> PLAN >>>
# Plan — F057 Rate-limit-aware scheduler

Branch: feature/f057-rate-limit-scheduler, cut from main at 21c8148e after
PR #198 merged. Next free finding id: R-0363. Open findings: R-0361, R-0362.

## Goal
Provider rate limits stop looking like failures. A per-provider governor reads
normalized limit signals out of call evidence and makes a run WAIT visibly —
with a reason and an expected retry — instead of burning retries or failing the
task. Providers that emit no limit signal behave exactly as they do today.

## Current Step
R1 — claim F057, reset the review record carrying R-0361 forward, register
R-0362, record DECISION F057 D1, and build T001: one place that turns the
rate-limit signal shapes this repo really emits into a normalized signal, with
unit tests over samples extracted from evidence that already exists. Nothing
calls the new module yet.

## Next Steps
1. T002 — the governor itself: per-provider cooldown state, `acquire()` with a
   deadline taken from budgets, an injected clock, and the stop-beats-wait
   ordering. No real sleeps in unit tests.
2. T003 — seam integration at the provider-call choke point
   (`_call_with_retry`), wait evidence, the report line, and the
   limit-emitting fixture end-to-end.
3. Integration gate, then closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- The seam is shared with the safe-point check. The ordering stop, then budget,
  then acquire is load-bearing and gets its own test in T002 rather than a
  comment.
- `is_rate_limit_error` must not swallow strings the existing transport
  predicates already own. T001 adds no wiring at all, so that precedence is
  settled with evidence in T003 and is not guessed now.
<<< PLAN <<<

(c) `.agent/context.md` — REPLACE THE WHOLE FILE:

>>> CONTEXT >>>
# Context — F057 Rate-limit-aware scheduler

## Active Branch
feature/f057-rate-limit-scheduler, cut from main at 21c8148e after the
paydown0814 PR #198 merged at the Open PR Gate. F057 is claimed `[~]` in
docs/roadmap/STATUS.md for the life of this branch.

## Scope
In: `packages/orchestration/rate_governor.py` and
`tests/orchestration/test_rate_governor.py`, both new, plus the `.agent/**`
round state and the one claimed STATUS line. R1 builds T001 only — signal
normalization — so nothing imports the new module yet.

Out: the per-call retry policy in `packages/orchestration/provider_timeouts.py`,
parallelism itself, and the provider adapters' internals. All three are the
feature file's Do-not-touch list. `packages/orchestration/pingpong_loop.py`
holds the seam and stays untouched until T003.

## Constraints
- The main session writes nothing in the work tree; a delegated worker subagent
  makes every commit (docs/agents/self_drive_protocol.md).
- Merges only at the Open PR Gate and never a PR this session created; never
  force-push; never work on main.
- Verification is pytest, scoped per round, plus the canary
  tests/cli/test_golden_path.py. A round that touches docs/roadmap/** also
  gates tests/docs/. Destructive and red-proof checks run only inside a
  disposable git worktree under .remedy-wt/, so resource safety stays intact
  and no background pytest process is ever left running.
- Unit tests use an injected clock. A real sleep in a unit test is a finding
  the feature file names in its Orchestrator brief.
- A round pushes after EVERY commit, not once at its last step (R-0289).

## Steps
R1 claim and T001 signal normalization → R2 T002 governor and acquire
semantics → R3 T003 seam, wait evidence and the fixture end-to-end →
integration gate → closure.
<<< CONTEXT <<<

Commit C2 ALONE.
  Subject: `docs(f057): claim F057 and reset the round state`
Gates: `grep -c '^- \[~\] F057 — Rate-limit-aware scheduler$' docs/roadmap/STATUS.md` → 1 ·
       `grep -c '^- \[ \] F057' docs/roadmap/STATUS.md` → 0 ·
       `wc -l < .agent/plan.md` → under 50 ·
       `python3 -m pytest tests/docs/ -q` → exit 0 (baseline on main: 295 passed;
         report the number you actually observe, do not assume it) ·
       `python3 -m pytest tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py -q`
         → exit 0 (these are the state-file contract readers)

── C3 — T001, signal normalization ────────────────────────────────────
Two NEW files, ONE commit. This is production code: it is specified here, not
dictated line by line, and you write it.

STEP 1, BEFORE writing any code — INVENTORY. Find every shape in this repo in
which a provider rate-limit / overload / throttle signal can actually reach us.
Start from these four, which the reviewer verified on disk at 21c8148e:
  - `packages/orchestration/stream_evidence.py:296-302` — `normalize_stream_object`
    turns a `{"type": "api_retry"|"retry", ...}` object into
    `{"event_type": "api_retry", "attempt": int, "reason": str}` (reason bounded
    to 300 chars, falling back to the object's `error` key).
  - `packages/orchestration/stream_evidence.py:290-295` — the same function turns
    `{"type": "error"|"provider_error", ...}` into
    `{"event_type": "provider_error", "error": str}` (bounded to 500 chars).
  - `packages/orchestration/pingpong_loop.py:2211` — each `retry_reasons` entry is
    `f"{role}:attempt{attempt + 1}:{out.error[:120]}"`.
  - `tests/orchestration/test_stream_evidence_integration.py:50` and
    `tests/orchestration/test_stream_evidence.py:136` — the only literal sample in
    the repo: `reason == "overloaded_error"`.
Then grep for more yourself (`rg -i 'overload|throttl|too many requests|429|rate.?limit' packages/ tests/ apps/`).
Record what you find. Finding nothing beyond the four above is a perfectly good
result — say so; do not invent a sample.

STEP 2 — write `packages/orchestration/rate_governor.py`. T001 slice ONLY:
normalization. No state, no clock, no waiting, no `acquire()` — those are T002.
Nothing in the repo imports this module at the end of this round, and that is
correct.

  - Module docstring: what the module is for, and a section listing the
    inventory from step 1 — each observed shape with the `file:line` it came
    from. This is the "list the real signal samples in the diff" requirement
    from the feature file's Orchestrator brief.
  - A frozen dataclass `RateLimitSignal` with at least: `provider: str`,
    `reason: str` (a normalized token, not free text), `retry_after_s: float |
    None` (None when the provider gave no hint — do not default it to a number),
    `source: str` (which evidence shape it came from), `raw: str` (the bounded
    original text). Give it `to_json()` returning a plain dict, matching how
    `StopSignal.to_json` in `packages/orchestration/safe_points.py` does it —
    this object ends up in evidence a person reads.
  - Named source constants rather than bare strings at call sites, one per
    evidence shape in the inventory.
  - `is_rate_limit_error(text: str | None) -> bool` — the ONE predicate.
    Follow the shape and the docstring style of `is_timeout_error` /
    `is_nonzero_exit_error` in `packages/orchestration/provider_timeouts.py`:
    the same repo already decided that a second definition of "what counts as
    X" is the bug. EVERY pattern it matches carries a one-line comment naming
    either the in-repo `file:line` that evidences it, or the exact words
    `no in-repo sample; provider vocabulary` when you are covering a real
    provider spelling for which this repo has no sample. The reviewer will
    grep for that marker — an unmarked speculative pattern is a finding.
    It must return False for the strings the existing predicates own: a bare
    timeout message and a bare non-zero-exit message are NOT rate limits.
  - `parse_retry_after_seconds(text: str | None) -> float | None` — pull a
    retry-after hint out of the text when one is there, None when it is not.
    Absent is not zero. Reject negatives and absurd values with a documented
    upper bound.
  - A normalizer that turns one piece of evidence into a `RateLimitSignal |
    None`, plus one small reader per evidence shape in the inventory (the
    `run_events` event dicts, and the `retry_reasons` string list). Reuse the
    predicate — do not re-spell the matching logic per reader.
  - Naming follows AGENTS.md "Code Discoverability Conventions": 2-4 words
    including a domain word, one spelling per concept, a one-line WHY comment
    directly above each non-obvious definition. State the deliberate absence in
    prose — this module does not wait, does not sleep and is not wired into the
    retry path in T001 — because a reader will search for that and text search
    cannot find code that does not exist.

STEP 3 — write `tests/orchestration/test_rate_governor.py`. It must cover:
  - every sample from the step-1 inventory, by its real shape;
  - the negatives: a timeout string and a non-zero-exit string are not rate
    limits, and neither is an empty/None input;
  - retry-after present, absent (None, not 0), negative, and over the bound;
  - each reader end-to-end on a realistic list of event dicts / retry reasons,
    including one that contains a mix of rate-limit and non-rate-limit entries;
  - `to_json()` round-tripping to plain JSON types.
  NO `time.sleep`, no real clock, no network, no filesystem.

Commit C3 ALONE.
  Subject: `feat(f057): normalize provider rate-limit signals`
Gates: `python3 -m pytest tests/orchestration/test_rate_governor.py -q` → exit 0,
         report the count ·
       `python3 -m ruff check` → exit 0 ·
       `grep -rn 'rate_governor' packages/ apps/ --include=*.py | grep -v 'rate_governor.py:'`
         → EMPTY (T001 wires nothing) ·
       `git diff --stat 21c8148e..HEAD -- packages/orchestration/provider_timeouts.py packages/orchestration/pingpong_loop.py packages/orchestration/stream_evidence.py`
         → EMPTY (Do-not-touch held) ·
       `grep -c 'time.sleep' tests/orchestration/test_rate_governor.py` → 0

RED-PROOF, as a PROBE — report the outcome, do not assume a colour. It runs
ONLY inside a disposable worktree, never in this checkout:
    git worktree add .remedy-wt/f057_r1_red HEAD
In that worktree, first PROVE the import path — run
`python3 -c "import packages.orchestration.rate_governor as m; print('MODULE', m.__file__)"`
from inside `.remedy-wt/f057_r1_red` and report the printed path; if it does not
point inside the worktree, the probe proves nothing and you must say so. Then
make `is_rate_limit_error` return False unconditionally, run
`python3 -m pytest tests/orchestration/test_rate_governor.py -q` there, and
report WHICH test ids fail and how many. Then:
    git worktree remove --force .remedy-wt/f057_r1_red && git worktree prune
`git worktree list` must return to ONE line and `git status --porcelain` in the
primary checkout must be empty.

── C4 — handback ──────────────────────────────────────────────────────
Rewrite `.agent/handoff.md` (never append) per AGENTS.md: feature + round,
branch, commit SHAs, a changed-files table, REAL verification results with real
exit codes, the open-findings count, and the next expected action. Under 60
lines, or carry a "Deviations, declared" line naming the real line count and the
mandated content that caused the overage (DECISION D15). Include the
item-status table with every bundle item C0a, C0b, C1, C2, C3, C4 exactly once,
status `done` / `skipped` / `deviated` with a reason.

Never write a `Done:` paragraph in `.agent/live_review.md` — that text is the
reviewer's alone (docs/agents/planner_reviewer_prompt.md §4 item 4). If a fix
lands before the reviewer has authored a resolution, write
`Landed: R-XXXX — <one line>` and nothing else.

Commit C4 ALONE.
  Subject: `chore(f057): handback R1`

── ROUND GATES — run every one, record the REAL exit code ─────────────
 1. `git status --porcelain` → empty
 2. `git worktree list` → exactly one line
 3. `git branch --show-current` → `feature/f057-rate-limit-scheduler`
 4. `grep -c '^- \[~\] F057 — Rate-limit-aware scheduler$' docs/roadmap/STATUS.md` → 1
 5. `grep -c '^- \[ \] F057' docs/roadmap/STATUS.md` → 0
 6. `grep -c '^## Steps' .agent/live_review.md` → 1
 7. `grep '^- R-0361 — ' .agent/live_review.md | sha256sum` → `70a8c9fb1a6ddebd2a1592b467cf9cb7e18f43ad0449c245d110bc0f1f056a7b`
 8. `grep -c '^- R-0362 — ' .agent/live_review.md` → 1
 9. `grep -c '^## DECISION F057 D1 ' .agent/decisions.md` → 1
10. `wc -l < .agent/plan.md` → under 50
11. `python3 -m pytest tests/orchestration/test_rate_governor.py -q` → exit 0
12. `python3 -m pytest tests/docs/ -q` → exit 0
13. `python3 -m pytest tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py -q` → exit 0
14. `python3 -m ruff check` → exit 0
15. `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0 (the canary; baseline on main is 42 passed)
16. `cmp .agent/authored/f057-r1.md .agent/last_block.md` → exit 0
17. the red-proof probe outcome above, with the printed MODULE path

Report every gate with its real output. "Green" as a word is not a result — a
gate you did not run is a gate that failed. If a gate goes red, STOP, do not
paper over it, and report the exact output.
