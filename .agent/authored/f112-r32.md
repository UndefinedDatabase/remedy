── STEP CLOSE/6 — F112 round 32 (bookkeeping only) ──────────────
Goal: Book round 31's PASS verdict. This round writes NO code and
touches nothing outside `.agent/` — permitted under amend0827 rule 1's
own exception for a feature's closure sequence, since precondition work
is done and only the merge (performed by the reviewer directly, per the
operator's own explicit instruction, once hosted CI reads green) and the
next feature's session remain.

Bundle: C0a save this block · C0b mirror it · C1 append RECORD31 · C2
apply PLAN32 · C3 handback.

Change: `.agent/authored/f112-r32.md` (new), `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`. Nothing
else.

Constraints:
1. Apply every slice byte for byte. `cp`, never retype.
2. `.agent/decisions.md`, `.agent/candidates.md`, `.agent/prose_slips.md`,
   `docs/roadmap/features/T3_F112.md`, `docs/roadmap/STATUS.md`,
   `README.md`, `scripts/self_use_queue.json` are NOT touched.
3. No PR action of any kind this round — no `gh pr` command. The merge
   is the reviewer's own next step, outside this delegated round.
4. Never force-push, never work on `main`.

Done when:
- `git status --porcelain` — empty before C0a and immediately before the
  handback commit.
- TRANSPORT: `git rev-parse HEAD:.agent/authored/f112-r32.md` and
  `HEAD:.agent/last_block.md` print ONE blob id; report sha256 and bytes
  for the committed authored file.
- THE RECORD APPEND: RECORD31 extracted from the committed authored
  file by its `--- BEGIN RECORD31 sha256=... ---` /
  `--- END RECORD31 ---` markers must be exactly `2358` bytes and match
  the stamped sha256. Append as `content_bytes + b"\n" + RECORD31_bytes`.
  `.agent/live_review.md` must reproduce at exactly `2349237` bytes
  immediately after C1 (pre-append `2346878` + 1 + `2358`), byte-exact
  prefix, no trailing newline. Report registered/`Done:`/open counts
  before and after (expect UNMOVED: 354 registered, 74 `Done:`, 280
  open, both sides — this round mints and resolves nothing).
- THE PLAN: PLAN32 extracted the same way must be exactly `1624` bytes
  and match its stamped sha256 (`b550af7f2138ef6fe09525010702bcb9533200b714574297762739de69eacb34`).
  `.agent/plan.md` must reproduce byte-identical to it after C2 —
  `wc -l` under 50, no trailing newline, `## Goal`/`## Next Steps` each
  exactly once.
- `git diff --stat 9b30be51..HEAD` outside `.agent/` — empty.

Handback: completion report + rewrite `.agent/handoff.md`. State plainly
in the handoff that the reviewer, not a delegated worker, performs the
merge next (checking hosted CI status and merging as two separate
commands) once CI reads green, per this session's opening operator
ruling — no further delegated round is expected before that, and the
NEXT delegated round (if any) belongs to the next feature.
──────────────────────────────────────────────────────────────

--- BEGIN RECORD31 sha256=3121e880e5d58bc7deb7ecd9545af4b89319955e2fa294ba2030ab36d88236a6 ---
Gate: F112 R31 — the round 31 entry, the README numeral sweep and the pull request. VERDICT PASS, over the range `9b30be51..71820a17` (commits C0a `b3b02146`, C0b `718fc035`, C1 `619b1fa2`, C2 `98027a76`, C3 `71820a17` — five real content commits — plus handback commit `94b29ba4`), independently re-verified by the reviewer. TRANSPORT HELD: `git rev-parse HEAD:.agent/authored/f112-r31.md` and `HEAD:.agent/last_block.md` both print blob `243f97e1f7340dfed0ce145bf7bcea460069bde5`, reproduced directly; `sha256sum .agent/authored/f112-r31.md` reproduced `d956918ba8b6670d26cad7435495ddbb507aa002ef524c0a94982622ad5f23d9` at 12589 bytes. THE README FIX AT C3 HELD BYTE-EXACT, REPRODUCED INDEPENDENTLY: `git diff 9b30be51..HEAD -- README.md` shows exactly two lines changed — `69 of 266 registered items accepted.` to `70 of 266 registered items accepted.` (rest of the line byte-identical) and the Tier 3 table row's Done cell `4` to `5` (its Total cell `26` unchanged) — nothing else in the file moved. `python3 -m pytest tests/docs/ -q`, reproduced by the reviewer at this round's own HEAD, reads `295 passed`, fully green, up from round 30's `2 failed, 293 passed`. `python3 -m pytest tests/cli/test_golden_path.py -q` reproduced 42 passed. `git status --porcelain` reads empty. THE PULL REQUEST WAS OPENED, REPRODUCED INDEPENDENTLY BY THE REVIEWER: `gh pr view 234` reads `state=OPEN`, `isDraft=false`, `baseRefName=main`, `headRefName=feature/f112-prompt-budget-per-task-class`, `mergeable=MERGEABLE` — exactly the single non-draft `feature/*`-to-`main` PR the Open PR Gate expects, NOT merged this round, per constraint and per self_drive_protocol.md G1 ("never merge a PR this session created in the same session"). Closure preconditions 1-6 are ALL now satisfied and landed on this branch's own HEAD; the only remaining step is hosted CI turning green and the merge itself, which — per the operator's own explicit instruction in this session's opening ruling ("merge this amendment's own PR yourself at the end after the gate battery... passes; check status and merge as two separate commands") — this session performs directly once CI reads green, as an explicit, in-session operator authorization that supersedes the general default of deferring the merge to a later session's Open PR Gate. `git status --porcelain` reads empty now.
--- END RECORD31 ---

--- BEGIN PLAN32 sha256=b550af7f2138ef6fe09525010702bcb9533200b714574297762739de69eacb34 ---
# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #234 OPEN (not
merged), base main. All six closure preconditions satisfied; the
evidence-packager contract fix (R-0792, R-0793) landed and independently
verified end to end against the real packaged zip
(remedy-review-20260904-123332-READY_FOR_REVIEW.zip, SHA-256
b0085f28a2c0c50654ed33be647ed986addc07c1c462324b1ee3fc1c8bb05927,
PACKAGE_STATUS=READY_FOR_REVIEW, EVIDENCE_AUTHORITATIVE=true).

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion
cascade with full omission disclosure, and a context that cannot fit
raises a task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md). ACHIEVED and CLOSED.

## Current Step

Round 32 books round 31's PASS verdict (bookkeeping only, closure
sequence exempt per amend0827 rule 1). The reviewer then waits for
hosted CI on PR #234 and merges directly once green, per the operator's
own explicit instruction opening this session.

## Next Steps

- Merge PR #234 once hosted CI is green (check status, then merge, as
  two separate commands).
- Hand back the built zip's name and SHA-256 to the operator for
  archiving and the formal package review.
- Next feature per STATUS order (Rule A5) starts a fresh session.

## Risks

- R-0784 and R-0767 (both OPEN, unrelated to F112) are documented,
  pre-existing risks; F112's live-review verdict is PASS_WITH_RISKS.
- A red hosted CI run is a blocker; the merge waits for it honestly
  rather than being forced.
--- END PLAN32 ---
