--- STEP R1/F106 — Session resume instead of rebuild ---

Goal: open F106 on its own branch and measure the exact provider call-entry
and evidence shape T001 builds on, writing that measurement to disk. No
code this round — T001 (adapter capability + resume parameter + evidence
fields + tests) is the next round, kept small per the feature file's own
Orchestrator brief ("T001 first and small").

Base: `811c2d7e96b4719b8c76e6fc59ec6d926847a026`, the current tip of `main`
(top commit: "fix(ci): sort self_use_runner test import, restore lint
ceiling"). Cut the branch from it.

Branch: `feature/f106-session-resume`

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f106-r1.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN1
- C2  append slice RECORD1 to `.agent/live_review.md`
- C3  apply pair PAIR-STATUS to `docs/roadmap/STATUS.md`
- C4  rewrite `.agent/context.md` from slice CONTEXT1
- C5  write `.agent/f106_inventory.md` — YOUR measurement, per the SPEC below
- C6  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f106-r1.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    docs/roadmap/STATUS.md
    .agent/context.md
    .agent/f106_inventory.md
    .agent/handoff.md

No file under `packages/`, `apps/`, `tests/` or `docs/roadmap/features/`
changes this round. This round writes NO production code and NO test.

## Constraints

1. Apply every slice BYTE FOR BYTE. Do not fix, rewrap, retitle or improve a
   slice. If a slice looks wrong, apply it as given and DECLARE the problem
   in the handback's deviations.
2. There is no paste relay this session (docs/agents/self_drive_protocol.md).
   The reviewer's scratch original of this exact block is on disk at
   `.remedy-wt/f106-r1-block.md` — for C0a, use `shutil.copyfile` to copy
   THAT file to `.agent/authored/f106-r1.md`, never a retype. For C0b,
   `shutil.copyfile` the committed `.agent/authored/f106-r1.md` into
   `.agent/last_block.md`. Never use `cp`. Apply every slice below by
   extracting it from the COMMITTED `.agent/authored/f106-r1.md` by its
   marker lines. This block states no expected byte count for itself (a
   file cannot carry its own length without invalidating it on the next
   edit) — G1 is where you report what you measured and the reviewer checks
   it independently.
3. C1 is the FIRST substantive commit, ahead of C2, because this round
   touches the finding ledger and AGENTS.md's Commit Gate requires
   `.agent/plan.md` to match the current work before every commit.
4. The record is APPEND-ONLY. C2 appends RECORD1 and revises nothing already
   in `.agent/live_review.md`.
5. NO NEW R-ID IS MINTED THIS ROUND and NO DECISION ID IS MINTED THIS ROUND.
   The count of distinct `^- R-\d+ — ` ids is the same before and after C2,
   the count of distinct `^Done: R-\d+ — ` ids is the same before and after,
   and the count of distinct `^DECISION F\d+ D\d+ — ` ids is the same before
   and after (19 at the base, measured by the reviewer at `811c2d7e`).
6. `.agent/plan.md` stays under 50 lines (AGENTS.md). PLAN1 is authored to
   fit; do not add to it.
7. Every exit code you report is REAL, taken from
   `subprocess.run(...).returncode` inside a script under the gitignored
   `.remedy-wt/`. Never read an exit code through a pipe, and never report a
   colour you did not run.
8. No destructive verification is ordered this round (no code lands). If you
   run one anyway, it runs ONLY inside a disposable `git worktree`, never in
   the primary checkout, which satisfies `git status --porcelain` empty at
   every reading.
9. The `remedy` console script is DENIED in this sandbox. Where you need it,
   use `python3 -m apps.cli.main ...` and say so.
10. Commit subjects carry no leading-slash token, no absolute path and no
    secret-like string. No `Co-Authored-By` trailer.
11. Push the branch after C6 and open NO pull request. This is round 1 of
    the feature; the PR is created at closure.
12. Pair shape, measured not asserted — PAIR-STATUS: `TO contains FROM:
    false`, so it is a REWRITE, and the FROM 1x→0x / TO 0x→1x count applies
    to it. The reviewer measured, at `811c2d7e`: PAIRSTATUS-FROM occurs 1x
    in `docs/roadmap/STATUS.md`, PAIRSTATUS-TO occurs 0x, and the whole file
    holds 0 lines matching `^- \[~\] F\d{3} — `.
13. The inventory (C5) is a MEASUREMENT, and every citation below is a
    HYPOTHESIS you VERIFY independently, not a fact you transcribe. Where a
    citation resolves exactly as stated, quote the current exact text at the
    given path/line. Where it does not — wrong line number, drifted text, or
    absent — say so plainly and give the corrected citation. Where something
    is ABSENT, say so and say how you searched (the exact command). Cite
    every claim with a `file:line` and the command that produced it.

## Slices

The authored units below are PLAN1, RECORD1, CONTEXT1 and the two halves of
PAIR-STATUS. Each is delimited by its own BEGIN and END marker line; the
marker lines are NOT part of the slice, and the slice's own bytes start on
the line after BEGIN and end with the newline before END.

<<<BEGIN PLAN1
# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`. SESSION 1,
opening the feature.

## Goal
Repair rounds stop resending the world: where the provider supports resuming
a session, a repair call resumes the original session and sends only the
findings delta, with an honest automatic fallback to full context when the
session is gone, flagged in evidence. Correctness never depends on resume
working.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the F106 claim and the branch | done | this round |
| the shape inventory | done | this round, `.agent/f106_inventory.md` |
| T001 capability + resume param + evidence fields + tests | open | next round |
| T002 repair-path integration + delta shrink + expired fallback | open | gated on T001; F111 already accepted |
| T003 measured fixture comparison + docs | open | |

## Next Steps
1. This round claims F106 and measures the exact call-entry/evidence shape
   T001 builds on, into `.agent/f106_inventory.md` — no code this round.
2. The next round orders T001: `supports_resume` on the provider protocol
   and its three adapters, an additive `resume` kwarg on `build`/`review`,
   `resume_used`/`resume_session_ref` on `BuilderOutput`/`ReviewerOutput`,
   all False/"" by construction — zero behavior change — plus
   `tests/orchestration/test_session_resume.py`.
3. T002 is gated on diff-repair (F111, "Diff-only repair"); F111 is already
   accepted (STATUS.md, 2026-08-13), so that gate is satisfied.

## Risks
- The orchestrator brief demands the fallback-once rule verbatim in the T002
  order — carry it forward, do not soften it.
- Only `ClaudeCliProvider` reports a session id today; T001 keeps
  `supports_resume` False on all three adapters regardless — turning one
  True is T002's call once resume is actually wired to CLI behavior.
<<<END PLAN1

<<<BEGIN RECORD1
Note: F106 — CLAIMED. `docs/roadmap/STATUS.md`'s amend0830-cost-first pull-forward (operator ruling 2026-08-30) put F106 first in Rule A5 order; `python3 -m apps.cli.main plan next` confirmed it at claim time. `.agent/candidates.md` is EMPTY and no `.agent/STOP` exists, so nothing blocks the claim. F106's own orchestrator brief gates T002 on diff-repair being merged: that is F111 "Diff-only repair" (`docs/roadmap/features/T2_F111.md`), accepted 2026-08-13 with T001-T003 complete, so the gate is satisfied and only T001's own "first, small" ordering governs round 2. This round's measured shape, written in full to `.agent/f106_inventory.md`: the provider call entry is `PingPongProvider` (`packages/orchestration/pingpong_provider.py:132`), with three concrete adapters (`FakeProvider`, `ClaudeProvider`, `ClaudeCliProvider`); `UsageActuals.session_id` (`packages/orchestration/token_actuals.py:37`) is already populated by `ClaudeCliProvider` alone; no `supports_resume`-shaped capability flag exists on that protocol today, the nearest repo precedent being `WorkerSpec.supports_external_builder_package` (`packages/orchestration/worker_registry.py:167`).
<<<END RECORD1

<<<BEGIN CONTEXT1
# Context — F106 Session resume instead of rebuild

## Active Branch
feature/f106-session-resume, cut from `main` at `811c2d7e`.

## Scope
Feature F106, `docs/roadmap/features/T3_F106.md` — Tier 3, session resume
for repair rounds. T001 (this feature's first code round) adds an additive
`supports_resume` capability flag and `resume` parameter to the provider
call entry, plus `resume_used`/`resume_session_ref` evidence fields, with
zero behavior change on every adapter. T002 wires it into the repair path
with a fallback-once rule; T003 measures resume vs full-context tokens.
F106 also covers job/mission resume-from-persisted-state per the feature
file's own Scope note (F075 candidate routing, R-0201) — in scope, not
sliced into T001-T003 yet.

## Do not touch
Failover policy, provider adapter internals beyond the additive surface,
prompt content rules — the feature file's own Do-not-touch. No orchestrator
move schema `resume` kind exists; that is out of T001-T003's own slicing.

## Assumptions
- `ClaudeCliProvider` is the only adapter that populates `session_id` today
  (`UsageActuals.session_id`, `packages/orchestration/token_actuals.py:37`).
  T001 does not turn any adapter's `supports_resume` True — that is T002's
  call once real resume behavior is wired.
- Diff-only repair (F111) is accepted and merged; T002's gate on it is
  satisfied.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaced.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree, never
  in the primary checkout, which satisfies `git status --porcelain` empty at
  every verdict.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE. The full contract
  those readers hold over the three state files, so a rewrite is checked
  against it directly: this file carries `## Active Branch`, a `feature/`
  branch name, a roadmap feature id matching `\bF\d{3}\b` and the word
  `Steps`; `.agent/plan.md` carries `## Goal`, `## Next Steps` and a feature
  id; `.agent/live_review.md` carries `Steps`.
- A new module under `packages/orchestration/` is swept by repo-wide guards
  that name no path: the `REMEDY_DATA_DIR` single-reader invariant, the
  path-utils single-implementation invariant, the bare-`except: pass` ban,
  and the development-artifact boundary.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for this feature lives in the `## Current Step`
section of `.agent/plan.md`. This file deliberately does not restate it.
<<<END CONTEXT1

<<<BEGIN PAIRSTATUS-FROM
- [ ] F106 — Session resume instead of rebuild
<<<END PAIRSTATUS-FROM

<<<BEGIN PAIRSTATUS-TO
- [~] F106 — Session resume instead of rebuild
<<<END PAIRSTATUS-TO

## SPEC for C5 — `.agent/f106_inventory.md`, YOUR measurement

This file is NOT authored above and must not be invented. VERIFY the
citations below against the repository at C4 and write what you find, with
a `file:line` for every claim and the exact command beside every count.
Where something is ABSENT, say so and say how you searched. Seven sections,
in this order:

1. THE PROVIDER PROTOCOL AND ITS CONCRETE ADAPTERS. Verify
   `packages/orchestration/pingpong_provider.py:132` defines
   `class PingPongProvider(Protocol)` with a `name` property and `build`/
   `review` methods taking `timeout_sec`/`max_output_chars` keyword params —
   quote the exact current signatures. List the three concrete adapters
   (`FakeProvider`, `ClaudeProvider`, `ClaudeCliProvider`) with their class
   line numbers, and quote each one's `build`/`review` method signature
   exactly as it stands today.

2. THE SESSION-ID FIELD IN CALL EVIDENCE. Verify
   `packages/orchestration/token_actuals.py:37` (`UsageActuals.session_id:
   str`) and quote the docstring describing it. Grep
   `packages/orchestration/pingpong_provider.py` for `session_id` and report
   every match with its line number and which class's method it sits in —
   confirm or correct the claim that only `ClaudeCliProvider` populates it.

3. THE CALL-ENTRY SIGNATURE — the additive target for `resume`. Quote the
   `Protocol.build`/`Protocol.review` signatures exactly (already covered in
   section 1; cross-reference rather than repeat verbatim).

4. CAPABILITY-FLAG PRECEDENT ELSEWHERE IN THE REPO. Verify
   `packages/orchestration/worker_registry.py:167`
   (`supports_external_builder_package: bool = False`) and quote the two
   neighboring `supports_*` fields. Grep the repo for `supports_[a-z_]*:
   bool` and report every distinct file it appears in.

5. THE REPAIR LOOP'S CALL SITES — LOCATE ONLY. Confirm
   `packages/orchestration/pingpong_loop.py` calls
   `builder_provider.build(...)` and `reviewer_provider.review(...)`; report
   the line numbers of those call sites as they stand today (they may have
   moved since a prior reading).

6. THE DIFF-REPAIR / DELTA MECHANISM. Confirm F111 "Diff-only repair" is
   `[x]` (accepted) in `docs/roadmap/STATUS.md` and quote that exact line.
   Confirm `packages/orchestration/diff_repair.py` exists and quote its
   module docstring's first line.

7. TEST CONVENTIONS FOR PROVIDER-ADAPTER TESTS. List every file under
   `tests/orchestration/` whose name contains `provider` or `pingpong`.
   Confirm, by directory listing, that
   `tests/orchestration/test_session_resume.py` does NOT exist yet.

Report every ABSENCE explicitly. A section that says "not found, searched
with <command>" is worth more than a confident guess, and this inventory is
the evidence the T001 order is built from.

## Done when — the gates

Run each gate and report ONE line per gate in the handback with its REAL
exit code. Every gate below runs at a commit STRICTLY EARLIER than C6, which
writes the handback; C6's own numbers are measured by the reviewer at the
next gate and are not owed here.

G1 TRANSPORT, at C0b. Report the byte length of the committed
   `.agent/authored/f106-r1.md` and of the committed `.agent/last_block.md`,
   and state whether they are byte-equal. This block deliberately states no
   expected length — the reviewer holds the original and checks your
   reported value independently.

G2 THE PLAN, at C1. `.agent/plan.md` is BYTE-EQUAL to slice PLAN1 (report
   sha256 of both), its line count is under 50, and it holds `## Goal` and
   `## Next Steps`.

G3 THE RECORD APPEND, at C2. The MEASURED pre-commit byte length of
   `.agent/live_review.md` plus one separator newline plus RECORD1's byte
   length equals the committed length — re-measure the base yourself at the
   commit you append at; the reviewer read 1809603 at `811c2d7e`. Then TWO
   independent readings: (a) WHOLE RECONSTRUCTION — base + separator + slice
   compared to the entire committed file; (b) PARAGRAPH ORDER — the last
   blank-line unit of the committed file equals RECORD1 exactly (N=1, one
   dense paragraph). NEGATIVE CONTROL, inside a disposable worktree removed
   after: flip one printable byte inside the appended paragraph and report
   that BOTH readings reject the flipped file and accept the unflipped one.

G4 THE LEDGER, at C1 and at C2. Report, for each of the two commits:
   distinct `^- R-\d+ — ` ids, distinct `^Done: R-\d+ — ` ids, and the open
   count. The ADDED registered ids and the ADDED resolved ids must BOTH be
   the empty list — the reviewer measured 318 registered / 55 resolved / 263
   open at `811c2d7e`. Report the distinct `^DECISION F\d+ D\d+ — ` ids
   before and after C2; both counts equal 19 (the reviewer's base reading).

G5 THE CLAIM AND THE DOCS PINS, at C3. In `docs/roadmap/STATUS.md`:
   PAIRSTATUS-FROM occurs 0 times and PAIRSTATUS-TO occurs exactly 1 time;
   `git diff --numstat` for C3 alone reads exactly one insertion and one
   deletion over that one path; the whole file holds exactly 1 line matching
   `^- \[~\] F\d{3} — `. Then, at C3: `python3 -m pytest tests/docs/ -q` and
   `python3 -m pytest tests/orchestration/test_roadmap_index.py -q`, each
   its own REAL exit code. The reviewer measured both green at the base,
   295 passed and 30 passed; report YOUR numbers.

G6 THE CONTEXT FILE, at C4. `.agent/context.md` is BYTE-EQUAL to slice
   CONTEXT1 (report sha256 of both), and it holds `## Active Branch`, the
   branch name `feature/f106-session-resume`, `F106` and the word `Steps`.

G7 THE STATE READERS AND THE CANARY, at C5. Each its own REAL exit code:
   `python3 -m pytest tests/ui_server/ -q`,
   `python3 -m pytest tests/orchestration/test_test_runner.py -q`,
   `python3 -m pytest tests/regression/test_resource_safety.py -q`,
   `python3 -m pytest tests/orchestration/test_integrity_gate.py -q`, and
   the canary `python3 -m pytest tests/cli/test_golden_path.py -q`. The
   reviewer measured these at the base at 515, 52, 21, 16 and 42 passed;
   report YOURS.

G8 THE INVENTORY AND THE TREE, at C5. `.agent/f106_inventory.md` exists and
   carries all seven SPEC sections — report the heading line of each.
   Report the `file:line` count it cites and confirm every cited path
   resolves with `git ls-tree HEAD -- <path>`. Then `git status --porcelain`
   is EMPTY, `git ls-files --others --exclude-standard` has count 0, and the
   per-commit insertion counts for C0a through C5 from `git diff --numstat`,
   every one under 500.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries
the state block, the `## Commits` table with a `+/-` column taken from
`git diff --numstat` (not from file line counts), the deviations, the
item-status table with every bundle item and every gate appearing exactly
once, and the next steps. It states `SESSION 1` of F106 and round 1. It has
NO length cap.
