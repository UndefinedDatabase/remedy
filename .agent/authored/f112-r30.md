── STEP CLOSE/4 — F112 round 30 ────────────────────────────────
Goal: Book round 29's PASS verdict, then land F112's closure commit
(STATUS `[x]` line, README capability sync, self_use_queue
`consumed_by`) and open the pull request — not merged this round.

Bundle:
1. C0a/C0b — save this block verbatim (transport proof), `cp` never
   retype.
2. C1 — append RECORD29 (below) to `.agent/live_review.md`: books round
   29's PASS-with-declared-deviation verdict. No new finding is
   registered or resolved.
3. C2 — apply PLAN30 (below) to `.agent/plan.md` (whole-file replace).
4. C3 — THE CLOSURE COMMIT (docs/roadmap/STATUS_closure_protocol.md
   algorithm step 5). Exactly three files, one commit:
   a. `docs/roadmap/STATUS.md` — replace this EXACT line (currently
      line 18; re-find it by content, not by line number, in case
      anything shifted):
        `- [~] F112 — Prompt budget per task class`
      with EXACTLY this line (the em dash is U+2014, matching the
      file's own convention — copy it from the FROM line, do not retype
      it):
        `- [x] F112 — Prompt budget per task class (T001–T003 complete; accepted 2026-09-04 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job 79b21c8cba8b4352 · package remedy-review-20260904-123332-READY_FOR_REVIEW.zip · SHA-256 b0085f28a2c0c50654ed33be647ed986addc07c1c462324b1ee3fc1c8bb05927 · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD 346c178f3241fad3984dca9baea3f37e34c3892a)`
      Every value in that line is REAL, independently re-verified by
      the reviewer against the actual packaged zip
      (`/home/decodeux/Repos/remedy-history/zips/remedy-review-20260904-123332-READY_FOR_REVIEW.zip`,
      sha256 `b0085f28a2c0c50654ed33be647ed986addc07c1c462324b1ee3fc1c8bb05927`,
      manifest `packaged_evidence_job_id=79b21c8cba8b4352`,
      `committed_review_subject.head_commit=346c178f3241fad3984dca9baea3f37e34c3892a`) —
      do not recompute or second-guess any of it, but DO re-run
      `sha256sum` on that exact file path yourself as your own
      independent check before committing, and STOP if it disagrees.
      T-slices use an en DASH (`–`, U+2013) between `T001` and `T003`,
      matching the F109/F110 precedent lines immediately above it in the
      same file — copy the en dash from one of those lines, do not
      retype it either.
   b. `README.md` — INSERT the paragraph below (READMEF112, delimited)
      as a new paragraph AFTER the F110 paragraph's closing text
      `...moving a class to a cheaper tier requires a\ndocumented
      benchmark run, never a bare config edit).` and its following
      blank line, and BEFORE the line `Accepted in Tier 5 so far:` —
      i.e. the sequence becomes: F110's paragraph, one blank line,
      READMEF112's paragraph, one blank line, `Accepted in Tier 5 so
      far:`. Locate the F110 paragraph and the `Accepted in Tier 5 so
      far:` line by their own literal text (grep them), not by a line
      number, since earlier commits in this branch's history do not
      touch this file and the anchor text is stable, but confirm it
      yourself rather than assuming.
   c. `scripts/self_use_queue.json` — the entry with `"id": "SU-007"`
      gets its `"consumed_by"` field changed from `""` to `"F112"`.
      Every other field of every other entry is BYTE-IDENTICAL —
      re-serialize the whole file only if your edit tool requires it,
      and if so confirm with a diff that the ONLY changed value
      anywhere in the file is that one field, no reformatting of
      unrelated entries, no key reordering, no whitespace/indentation
      change elsewhere.
   Nothing else is touched in this commit. `docs/roadmap/features/
   T3_F112.md`'s Built State is already current from round 22
   (precondition 4) — do not edit it.
5. C4 — GATES, run for real and reported:
   - `python3 -m pytest tests/docs/ -q` (docs/roadmap/STATUS.md and
     README.md both changed this round).
   - `python3 -m pytest tests/cli/test_golden_path.py -q` (canary).
   - Re-confirm `from packages.orchestration.integrity_gate import
     run_integrity_checks; run_integrity_checks()` — `.passed=True`,
     `.fail_count=0` — one more time at C3's own commit, since
     precondition 3 must hold at the actual closure commit, not only at
     round 28's earlier reading.
   - `git status --porcelain` — empty.
6. C5 — THE PULL REQUEST (AGENTS.md PR workflow). Push, then
   `gh pr create` from this branch into `main`. Title: short, under 70
   chars. Body: what changed and why (the operator's evidence-packager
   contract fix PLUS F112's own feature work), key decisions (R-0792/
   R-0793 root cause and fix, the round-21-already-discharged self-use
   discovery), how to review, a changed-files table, the latest verdict
   (PASS_WITH_RISKS) and open-findings count, runtime actuals (rounds
   27-30 this session; earlier rounds from prior sessions — state
   `not-measured` for anything the ledger does not carry a number for
   rather than guessing). Do NOT merge it — that is the next round,
   after hosted CI reads green, per the Open PR Gate.
7. Handback — completion report + rewrite `.agent/handoff.md`. Include
   the PR number and URL, and the built zip's filename + SHA-256 once
   more for the operator to archive/formally review.

Change: `docs/roadmap/STATUS.md`, `README.md`,
`scripts/self_use_queue.json`, `.agent/live_review.md`, `.agent/plan.md`,
`.agent/authored/f112-r30.md` (new), `.agent/last_block.md`,
`.agent/handoff.md`. Nothing under `packages/`, `apps/`, `tests/`.
`docs/roadmap/features/T3_F112.md` is NOT touched (already current).

Constraints:
- `.agent/decisions.md`, `.agent/candidates.md`, `.agent/prose_slips.md`
  are NOT touched this round.
- The closure commit (C3) touches EXACTLY the three files item 4 names —
  nothing else, not even a whitespace-only touch elsewhere.
- Never force-push, never work on `main`. The PR is created, never
  merged, this round.
- If ANY gate at C4 is not green, STOP before C5 (no PR on a red gate)
  and declare the failure fully — do not attempt a fix on this round's
  own initiative beyond what the block already ordered.

Done when — run every gate and report its REAL exit code/output:
- `git status --porcelain` — empty before C0a and immediately before the
  handback commit.
- `.agent/live_review.md` reproduces at exactly `2342756` bytes
  immediately after C1 (pre-append `2338544` + 1 + RECORD29's `4211`
  bytes), byte-exact suffix; registered/`Done:`/open counts unmoved
  (354/74/280) both sides of C1.
- `.agent/plan.md` reproduces byte-identical to PLAN30 (`1925` bytes, no
  trailing newline, `## Goal`/`## Next Steps` each exactly once,
  `wc -l` under 50) after C2.
- `docs/roadmap/STATUS.md`'s F112 line reproduces byte-identical to the
  TO text above; count of lines matching `^\- \[x\] F112 — ` — 0 before,
  1 after; count matching `^\- \[~\] F112 — ` — 1 before, 0 after.
- `README.md`'s new paragraph reproduces byte-identical to READMEF112;
  it appears exactly once, between the F110 paragraph and `Accepted in
  Tier 5 so far:`, confirmed by reading the surrounding 10 lines on both
  sides after the edit.
- `scripts/self_use_queue.json`'s SU-007 entry's `consumed_by` reads
  `"F112"`; every OTHER field of every OTHER entry byte-unchanged
  (report a diff confirming only that one value changed).
- `python3 -m pytest tests/docs/ -q` — real pass count.
- `python3 -m pytest tests/cli/test_golden_path.py -q` — real pass
  count.
- `run_integrity_checks()` — `.passed`, `.fail_count`, per-check status,
  taken at C3's own commit.
- The `gh pr create` outcome — real PR number and URL.

Handback: completion report + rewrite `.agent/handoff.md`.
──────────────────────────────────────────────────────────────

--- BEGIN RECORD29 sha256=ad73d8470015e65618bdb6577d297fc2f2e9251ce37adee39f4f7d1e3bac2b0d ---
Gate: F112 R29 — the round 29 entry, closure precondition 6's self-use step. VERDICT PASS WITH A DECLARED REVIEWER-SIDE DEVIATION, over the range `6dd06718..0c08d6d9` (commits C0a `6132c7af`, C0b `d0d38a82`, C1 `2d2b07af`, C2 `05852956`, C3 `0c08d6d9` — five real content commits — plus handback commit `a5df6f2b`), independently re-verified by the reviewer. TRANSPORT HELD: `git rev-parse HEAD:.agent/authored/f112-r29.md` and `HEAD:.agent/last_block.md` both print blob `ecf064052b64d4ca72e578de479f318a5e534b4f`, reproduced directly; `sha256sum .agent/authored/f112-r29.md` reproduced `10d7a6247bee952420a1da3a12d2269a14f8831025742a608bcdc5a12f2812e2` at 14694 bytes. THE RECORD APPEND AT C1 HELD: `.agent/live_review.md` reproduced at 2338544 bytes immediately after C1, matching the round's own pinned figure exactly; registered/`Done:` counts read 354/74 both before and after, unmoved, correct since RECORD28 mints and resolves nothing. THE PLAN REPLACEMENT AT C2 HELD BYTE-IDENTICAL TO PLAN29 (reproduced 2249 bytes against the committed authored slice) BEFORE C3 CORRECTED IT: this round's own block (authored by the reviewer) carried a STALE PREMISE — it ordered SU-007 planned and run as F112's first self-use execution, when in fact round 21 (commit `1b9ac1ca`, RECORD21, read and reproduced by the reviewer directly) had ALREADY planned and RUN SU-007 to the approval gate (job `848fc4c67d7b405b`, blocked, evidence already added to the already-open `R-0784` per §3 item 30) and explicitly recorded "closure precondition 6 is now DISCHARGED for F112 pending only the `consumed_by=F112` edit, which lands in the closure commit itself" — a fact this round's own reviewer-authored PLAN29 failed to carry forward from the ledger. THE WORKER'S HANDLING IS CORRECT AND IS WHAT THIS VERDICT CREDITS: it executed `pending_self_use_items()`/`next_self_use_item()` exactly as ordered (both matched the block's stated expectation, since queue STATE alone does not reveal run HISTORY), ran `run_next_self_use_item` exactly as ordered (job `962cb3c9b96244ed`, 129.5s, `status='blocked'`, `error='task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail'`, `resolve_role_config` reading `provider='ollama'`/`model='muse-glimmer:latest'` for both roles — a REAL run against a real local provider, not simulated), THEN discovered the duplication before committing the evidence copy, and — rather than land a misleading SECOND "first run" record over round 21's real one — discarded the redundant run's `.agent/selfuse_f112/` output with `git checkout --` and used C3 instead to correct `.agent/plan.md`'s now-false premise, exactly per AGENTS.md's "if blocked" guidance and self_drive_protocol.md G8 ("ambiguity ends the round... never guess"). REPRODUCED INDEPENDENTLY BY THE REVIEWER: `git diff 1b9ac1ca..HEAD -- .agent/selfuse_f112/` is EMPTY — `.agent/selfuse_f112/SU-007.md` and `run.txt` on disk right now are BYTE-IDENTICAL to round 21's own committed copies, so no duplicate or corrupted record landed; `.agent/plan.md` at C3 reproduced 49 lines (under 50), 2438 bytes, `## Goal`/`## Next Steps` each exactly once, and its new text accurately states the discovery and names job `962cb3c9b96244ed` as the (uncommitted, discarded) redundant run. `scripts/self_use_queue.json`'s `SU-007.consumed_by` reproduced as the empty string, unchanged, exactly as ordered. `git status --porcelain` reads empty. THE DEVIATION IS THE REVIEWER'S OWN, NOT THE WORKER'S: PLAN29 should have stated precondition 6 was already discharged at round 21 and ordered ONLY the `consumed_by=F112` edit as part of the closure commit; instead it re-ordered a run that had already happened, costing one redundant (uncommitted, harmless) job execution against the local `ollama` provider. NO NEW FINDING IS WARRANTED for this: it is a reviewer-authoring slip inside the amend0827-process-diet regime, not a defect on disk, and R-0784 already carries the correct evidence class from round 21 without needing a third note for a run that was never committed. Closure precondition 6 remains DISCHARGED (round 21), and round 30 proceeds straight to the closure commit — no further self-use work is owed.
--- END RECORD29 ---

--- BEGIN PLAN30 sha256=2f33269d4192efe07ca13fb2bb6757804649229b4a7144ee3982e50318721f43 ---
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1. Round 27 fixed the evidence-packager
contract (R-0792, R-0793); round 28 rebuilt the closure evidence bundle
and review zip, confirmed READY_FOR_REVIEW/true on the real packaged
artifact; round 29 booked round 28's verdict and discovered closure
precondition 6 (self-use) was already discharged at round 21, so no
further self-use work is owed. All six closure preconditions are now
satisfied. Round 30 is the closure commit and the pull request.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion
cascade with full omission disclosure, and a context that cannot fit
raises a task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 30 books round 29's PASS verdict, then lands the closure commit
per docs/roadmap/STATUS_closure_protocol.md algorithm step 5: the
authored STATUS `[x]` line, the README capability-sync paragraph (same
commit, R-0154 pin), `scripts/self_use_queue.json`'s SU-007
`consumed_by=F112` — nothing else. Then the AGENTS.md PR workflow opens
the pull request; it is NOT merged this round.

## Next Steps

- Round 31: Open PR Gate — hosted CI green, docs gate/canary/touched
  suites pass, planner merges per the standing merge-autonomy rule; hand
  back the built zip's name and SHA-256 to the operator for archiving
  and the formal package review.

## Risks

- `R-0784` and `R-0767` (both OPEN, unrelated to F112) are documented,
  pre-existing risks; F112's live-review verdict is PASS_WITH_RISKS for
  exactly this reason, matching F109's and F110's own closed precedent.
- Hosted CI must read green before the PR is merged; a red hosted run is
  a blocker, not something to route around.
--- END PLAN30 ---

--- BEGIN READMEF112 sha256=04b5c0b34aa40cd453a58ae70fa96db1620331582ed1ea467a6d79e3dfbb0b11 ---
F112 prompt budget per task class (every task carries a class-scoped
input-token ceiling; the context compiler fits under it via the existing
demotion cascade with full omission disclosure — no new selection logic,
only a class-specific number the cascade already enforces. When even
tier-1 content alone still cannot fit after full demotion, a task-split
decision is raised — "task context exceeds its class cap" — with
auto-apply-safe-default splitting the oversized task into children
rather than running it truncated; "raise cap"/"proceed-overcap" stay
deliberately unbuilt, since no audited or attended-mode seam exists to
hook them to yet. Caps are config defaults labeled with an honest
default basis until a calibration feature replaces them with measured
ones).
--- END READMEF112 ---
