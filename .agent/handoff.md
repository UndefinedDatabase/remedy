# Handback — F040 · SESSION 4 · round 20 · THE CLOSURE COMMIT AND THE PULL REQUEST

> Written by the WORKER inside C3, the closure commit itself. This is the
> FEATURE'S CLOSING HANDBACK: F040 is accepted on disk as of this commit.

## THE CLOSURE FACTS, as their own labelled lines

Carried verbatim from round 19. Nothing here was re-derived, re-run or
rebuilt this round: the package was built from a clean tree at the accepted
head and this round consumes those values as they stand.

    Evidence job    f040-closure
    package         remedy-review-20260830-033225-READY_FOR_REVIEW.zip
    SHA-256         26bacc72356bea20d765736996cb353033d087c328e7af0156548a533d164be1
    package path    /home/decodeux/Repos/remedy-history/zips
    accepted HEAD   5281987a142b97f222256c987d36c009ae7ab3ae
    self-use        NONE (queue exhausted, per round 18's own reading)
    open findings   262 (R-0570, R-0752, R-0755 routed to the paydown branch;
                     R-0753 carried as this feature's own documented risk)

THE ACCEPTED HEAD IS NOT THIS ROUND'S HEAD, deliberately. `5281987a` is C2 of
round 19, the commit the closure evidence job and package actually cover.
The STATUS line names that head for exactly this reason.

`self-use NONE (queue exhausted)` is the closure protocol's precondition-6
"exhausted, not blocked" branch, read at round 18 and unchanged since;
`scripts/self_use_queue.json` was NOT touched this round — editing it would
have been a false record.

## Session

SESSION 4 of feature F040 · round 20 · rounds so far 20.

This is the LAST round of F040's build. The functional scope closed at round
16 (T001-T003 all PASS); round 17 ran the integration gate; round 18 wrote
the Built State and cleared all six closure preconditions; round 19 built
the READY_FOR_REVIEW evidence package. This round flips the STATUS `[x]`
line and both README ledger numbers in ONE commit (R-0154: README and
STATUS may never disagree in any committed state), records one
closure-candidate finding this round's own README audit surfaced, and opens
the pull request.

WHAT IS MISSING: nothing on this branch. Wiring `onOpenDecisions` and
`onPrimaryAction` to a real in-page action (D5) needs its own resolution
design and is documented in the Built State section as a known post-closure
item, not a blocker to Acceptance.

THIS BRANCH'S LAST CONTENT ROUND HAS NO ON-DISK GATE ENTRY, by
construction — docs/agents/planner_reviewer_prompt.md §4 item 13 rules that
the last round of a branch cannot record a gate on itself. That absence is
the branch TERMINATOR, not a missing review.

## Range

Review of `bdf78bb7`..HEAD on branch `feature/f040-completion-digest`. FIVE
commits, C0a through C3 (C4, the candidates-only commit, follows separately
per DECISION amend0827 D2). The range is not named to a terminal SHA because
C3 is the commit that writes this file and cannot name its own SHA (R-0149
pattern).

## Commits

### cc54d2e4 docs(f040): save the round 20 step block verbatim (C0a)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f040-r20.md | +228/-0 | C0a — the block saved verbatim via `cp`, never retyped |

### 15e96531 docs(f040): mirror the round 20 block to last_block.md (C0b)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +177/-167 | C0b — the same bytes mirrored, copied from the saved file |

### 4e5f8c3e docs(f040): update plan.md for round 20, session 4 (C1)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +15/-16 | C1 — full rewrite from slice PLAN20 |

### 1c914098 docs(f040): append the R19 verdict to the ledger (C2)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +2/-0 | C2 — slice RECORD20 appended: the R19 `Gate:` paragraph. Registers and resolves NOTHING |

### C3 — THE CLOSURE COMMIT (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|------|-----|--------|
| docs/roadmap/STATUS.md | +1/-1 | pair — F040 flipped `[~]` to `[x]`, line 87 |
| README.md | +8/-2 | two pairs (accepted count 63→64, Tier 5 Done 11→12) plus one insertion (F040's capability paragraph, between F257's paragraph and "Full per-feature state:") |
| .agent/handoff.md | rewrite | this file; a handback cannot table the commit that writes it |

C3's path set is EXACTLY those three paths, which is Rule A4's rendering and
the R-0154 pin in one: README and STATUS never disagree in any committed
state, because the flip and the sync are the same commit. C3 IS THE LAST
CONTENT COMMIT ON THIS BRANCH (C4, candidates-only, follows).

## External actions

- `git push origin feature/f040-completion-digest` after C3 — the closure
  push.
- `gh pr create --base main --head feature/f040-completion-digest` — NOT a
  draft. The resulting PR number is recorded in the round report, because
  the PR does not exist at the moment this file is written (constraint 11
  says so explicitly; R-0371's resolution: never fabricate a number before
  its tool runs).
- NO MERGE OF ANY KIND. The PR is deliberately left OPEN: it merges at the
  next feature's start through the Open PR Gate, and that gap is the
  operator's manual-review window. No force-push. No worktree left behind
  (the G3 negative-control worktree `.remedy-wt/wt-negctrl-r20` was created
  and removed within C2's own verification, before C2 was committed).
- No zip rebuilt, no evidence job re-run, no manifest edited or hand-touched.

## Verification

Every exit code below is REAL, taken from `subprocess.run(...).returncode`
inside a script under the gitignored `.remedy-wt/`, never through a pipe.

G1 TRANSPORT, at C0b — REAL, sha256-equal.
    `.remedy-wt/f040-r20-block.md`         16315 bytes
    `.agent/authored/f040-r20.md` (C0a)    16315 bytes
    `.agent/last_block.md`        (C0b)    16315 bytes
    ALL THREE share sha256
      22db3becb6a21fa414165089c09375874efc07ab3163bc4f1816085d3ad90670
    matching the reviewer-stated digest, byte length and 228 lines exactly.

G2 THE PLAN, at C1 — REAL, byte-equal.
    `.agent/plan.md`: 2280 bytes, 45 lines, under 50 True.
    byte-EQUAL to slice PLAN20: True (`diff` exit 0, both 2280 bytes).
    holds `## Goal` True · holds `## Next Steps` True ·
    matches `\bF\d{3}\b` → `F040` True.

G3 THE RECORD APPEND, at C2 — REAL, both readings True.
    base (re-measured at `4e5f8c3e`) 1749253 bytes, trailing-newline
    terminated. RECORD20 slice: sha256
    26a67f437a0b4ccbaaeabc6671513801727fdb7d80987ca2c6c110820ed0e6e1,
    2414 bytes, single dense paragraph (N=1), itself trailing-newline
    terminated. Committed file: 1751668 bytes.
    Reading (a) `base + b"\n" + slice == committed`: True.
    Reading (b) split committed on `\n\n`, 770 units, last unit equals the
    slice exactly: True.
    NEGATIVE CONTROL, inside a disposable worktree
    (`.remedy-wt/wt-negctrl-r20`, branched at `4e5f8c3e`, removed after):
    one printable byte flipped inside the slice (offset 10, a space
    flipped to `_`, length unchanged) → reading (a) False, reading (b)
    False; the unflipped bytes checked the same way → reading (a) True,
    reading (b) True.

G4 THE LEDGER, at C2 — computed by DIFFERENCE between `4e5f8c3e` (base) and
    `1c914098` (committed) `.agent/live_review.md`: registered ids
    (`^- R-\d+ — `) ADDED `[]` REMOVED `[]` (317 distinct both sides);
    resolved ids (`^Done: R-\d+`) ADDED `[]` REMOVED `[]` (55 distinct both
    sides); `DECISION F040 D\d+` ids ADDED `[]` REMOVED `[]` (none this
    round); `^Gate: F040 R19 — ` lines 0 before → 1 after. Open count
    (registered minus resolved) 262 before → 262 after (unchanged).

G5 THE STATUS AND README PAIRS, at C3 — every occurrence count measured
    fresh, before and after:
      STATUS.md `- [~] F040 — Completion/return digest`  before 1, after 0
      STATUS.md STATUSLINE text                            before 0, after 1
      README.md `63 of 257 registered items accepted`      before 1, after 0
      README.md `64 of 257 registered items accepted`      before 0, after 1
      README.md `| 5 | Operator Cockpit | 11 | 31 |`        before 1, after 0
      README.md `| 5 | Operator Cockpit | 12 | 31 |`        before 0, after 1
      README.md anchor `not a gate).\n\nFull per-feature state:` before 1
        (confirmed exactly once at base)
    Ordering confirmed by direct substring search on the committed file:
    the composed string `not a gate).\n\n` + README_PARAGRAPH +
    `\n\nFull per-feature state:` occurs exactly once, and F257's own
    paragraph precedes it — the F040 paragraph sits after F257's and
    before the "Full per-feature state:" line, exactly as ordered.

G6 `tests/docs/` GREEN, at C3 — REAL exit 0, run against the working tree
    with STATUS.md and README.md already carrying this round's edits
    (identical content to what C3 commits): `python3 -m pytest tests/docs/
    -q` — **295 passed** in 0.43s, matching the 295 this branch measured at
    prior rounds; the two moved ledger numbers did not move the pin count.
    THE THREE NAMED PINS, each run individually, each its own REAL exit
    code:
      REAL exit 0  TestPrimaryDocsAreHonest::test_the_readme_accepted_count_equals_the_status_count
      REAL exit 0  TestPrimaryDocsAreHonest::test_the_readme_tier_table_done_column_matches_the_ledger
      REAL exit 0  TestPrimaryDocsAreHonest::test_the_readme_reports_the_accepted_foundation_and_no_later_feature

G7 THE CANDIDATE, at C4 — reported in C4's own commit, not here (C4 is a
    separate commit that follows this one; see the round report for its
    SHA and verification).

G8 THE TREE AND THE PR, at C4/after — reported in the round report: the
    push, the PR creation, and the final `git status --porcelain` /
    `git worktree list` readings all happen after this commit exists and
    therefore cannot be tabled inside it.

## Deviations & assumptions

1. THE README'S TIER 5 PROSE LIST DOES NOT LIST F033's PARAGRAPH, AND THIS
   IS DECLARED RATHER THAN REPAIRED. `README.md`'s "Accepted in Tier 5 so
   far:" list carries F255, F008, F009, F021, F022, F031, F032, F037, F256,
   F257 and now F040 — eleven paragraphs — while the tier table reads 12
   Done. F033 is counted in both pins but has no paragraph of its own. This
   round's block (constraint 8) identifies this as a PRE-EXISTING gap from
   F033's own closure round, not F040's defect to fix inline, and orders it
   recorded as a closure candidate in C4 instead. NO TEST FAILS: the pin
   `test_the_readme_reports_the_accepted_foundation_and_no_later_feature`
   checks ONE direction only — every feature the README lists as accepted
   IS accepted in the ledger — so an unlisted accepted feature is invisible
   to it. NOT touched inline; recorded as a candidate in C4.
2. COMMIT SUBJECTS CARRY NO `Co-Authored-By` TRAILER, matching this
   branch's prior rounds. AGENTS.md's "prefer repository state over session
   memory" governs the session default. No subject contains a leading-slash
   token, an absolute path or a secret-like string.
3. THE `remedy` CONSOLE SCRIPT WAS NOT USED (denied session-wide, per
   memory `remedy_cli_sandbox_split.md`); no step in this round needed it.
4. A `cmd; echo $?` FORM WAS DENIED BY THE SANDBOX on first use this round.
   Every exit code in this file therefore comes from
   `subprocess.run(...).returncode` inside a small runner under
   `.remedy-wt/`; no reading was taken through a pipe.
5. NOTHING OUTSIDE THE CHANGE SET WAS TOUCHED. `scripts/self_use_queue.json`
   was NOT edited (queue exhausted — an edit would be a false record); no
   zip was rebuilt, no evidence job re-run, no manifest edited; and no file
   under `packages/`, `apps/` or `tests/` changed this round.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a — save block to `.agent/authored/f040-r20.md` | done | `cc54d2e4`; G1 sha256-equal, three readings |
| C0b — mirror into `.agent/last_block.md` | done | `15e96531`; byte-equal |
| C1 — rewrite `.agent/plan.md` from PLAN20 | done | `4e5f8c3e`; G2 byte-equal, 45 lines |
| C2 — append RECORD20 to `.agent/live_review.md` | done | `1c914098`; G3 both readings True, negative control rejects the flip; G4 registers and resolves nothing |
| C3 — THE CLOSURE COMMIT (STATUS + README + handoff) | done | this commit; G5 six counts, G6 green |
| C4 — the candidates-only commit | pending | follows this commit; see the round report for its SHA |
| the pull request | pending | created after C3 is pushed, NOT merged, NOT a draft; number in the round report |
| G1 transport | done | sha256-equal, three readings |
| G2 the plan | done | byte-equal, 45 lines |
| G3 the record append | done | both readings True, negative control rejects the flip |
| G4 the ledger | done | nothing registered or resolved, `Gate: F040 R19 —` 0→1 |
| G5 the STATUS/README pairs | done | every occurrence count as ordered |
| G6 `tests/docs/` green | done | REAL exit 0, 295 passed |
| G7 the candidate | pending | booked in C4, see the round report |
| G8 the tree and the PR | pending | reported in the round report, after push and `gh pr create` |

Open findings after this round: **262** (317 registered distinct, 55
resolved distinct, both UNMOVED). R-0570, R-0752 and R-0755 stay OPEN and
routed to the paydown branch; R-0753 stays OPEN as this feature's own
documented risk — none is reachable from F040's Acceptance, which is why
the STATUS line reads PASS_WITH_RISKS.

## Runtime actuals

Rounds: 20 (SESSION 4 alone: rounds 17-20). Wall clock: not-measured (no
per-round timer was kept on this branch). Models/tokens: not-measured (no
per-round token ledger export exists for this branch) — `not-measured`
beats a guess.

## Next

NOTHING IS OWED ON THIS BRANCH after C4 and the pull request. F040 is
accepted on disk as of this commit.

The NEXT SESSION starts a NEW feature (or resumes `amend0829` per the
queued self-use registration) and begins by reading `.agent/STOP`, then
runs the AGENTS.md Open PR Gate — which will find exactly this PR, from
`feature/f040-completion-digest` into `main`, non-draft, and MERGE it
before any new branch is cut. The gap between now and that merge is the
operator's manual-review window, and the operator may merge by hand at any
time instead.

Three carried risks travel with the merge: R-0570, R-0752 and R-0755
(routed to the paydown branch), and R-0753 (this feature's own documented
risk). None is reachable from F040's Acceptance.

**F040 — Completion/return digest: DONE.**

## Addendum (round 21) — the two facts round 20's own C3 could not yet know

Round 20's handback (this file, as committed at `0ec9bb37`) named C4 and the
pull request as "pending," deferred to "the round report" — the worker's
chat reply to the reviewer, which is not a disk artifact and does not
survive a context reset. Both facts are now confirmed and recorded here,
independently, by the reviewer:

**C4** is commit `5ec85b07` — `docs(f040): record the F033 closure
candidate`. Its changed-path set is exactly `.agent/candidates.md`, matching
round 20's own constraint 8 and DECISION amend0827 D2 (a candidates-only
commit is the one permitted successor to the closure commit). G7 (the
candidate) reads PASS: `.agent/candidates.md` was empty at this round's
base and the committed file names the F033 README-paragraph gap, F040 as
the source feature, and 2026-08-30 as the date, with no `R-` id spent.

**The pull request** is **#225** —
`https://github.com/UndefinedDatabase/remedy/pull/225` — head
`feature/f040-completion-digest`, base `main`, `isDraft: false`,
`mergedAt: null`, state `OPEN`. G8 (the tree and the PR) reads PASS: the
tree is clean, `git worktree list` shows one line, the branch is pushed and
matches `origin`, and the PR is open, non-draft, and unmerged, exactly as
self_drive_protocol.md's G1 guardrail requires of a PR opened in the
session that opened it.

F040's own build is complete on disk. The merge itself is deferred to the
Open PR Gate (AGENTS.md; STATUS_closure_protocol.md algorithm step 6): the
next session that runs Phase 0's state probe finds PR #225 via
`gh pr list --state open` independently of this addendum, and merges it
before claiming any new feature, per self_drive_protocol.md Phase 1 rule 2.
This addendum exists so that fact is also readable from this file alone,
without depending on any chat transcript surviving.

## Session 5 — Phase 0 blocked at the Open PR Gate (2026-08-30)

Phase 0's state probe found exactly one open PR, #225
(`feature/f040-completion-digest` → `main`, not a draft), which is the
AGENTS.md Open PR Gate's merge case. `gh pr view 225
--json mergeable,mergeStateStatus` returned `"mergeStateStatus":"DIRTY"`,
`"mergeable":"CONFLICTING"`. AGENTS.md: "If the PR cannot be merged
(conflicts, failing checks, missing approvals, or policy restrictions):
1. stop 2. report the blocker 3. do not proceed with new work." A git merge
conflict is named explicitly in that list; the amend0820-gate-autonomy
exception covers only a CI check that is RUNNING or ended RED, not a merge
conflict, so it does not apply here. This session therefore stopped at
Phase 0/Phase 1 rule 2, before opening any round, before touching
`.agent/candidates.md`'s one open entry (Phase 1 rule 2 precedes rule 3),
and before claiming any new feature.

Root cause, measured via `git merge-tree
f5b1e6c5b815a276f45fcb4cbd0cdf2cfa75f4e1 HEAD origin/main` (merge-base
`f5b1e6c5b815a276f45fcb4cbd0cdf2cfa75f4e1`, `origin/main` tip
`0fd3b7716021dee9037295acd89b315fc0af9e19`): PRs #223
(`feature/amend0829-selfuse-v2`) and #224 (`fix/amend0829-f258-order`)
merged into `main` after this branch was cut, registering F258 and
reordering it in `docs/roadmap/STATUS.md`. Both land on the same lines this
branch's own closure commit `0ec9bb37` touched. Conflict markers appear in
exactly two files:

- `README.md` — the accepted-count line (`64 of 257 registered items
  accepted` on this branch vs `63 of 258 registered items accepted` on
  `origin/main`) and the Tier 5 table row (`| 5 | Operator Cockpit | 12 |
  31 |` vs `| 5 | Operator Cockpit | 11 | 32 |`).
- `docs/roadmap/STATUS.md` — the F040 line: this branch flipped it to
  `- [x] F040 — Completion/return digest (... accepted HEAD
  5281987a142b97f222256c987d36c009ae7ab3ae)`; `origin/main` still has
  `- [ ] F040 — Completion/return digest` immediately followed by a new
  `- [ ] F258 — Self-use track v2 (self-replenishing queue & executed
  items)` line.

`docs/README.md` (the "257-feature" vs "258-feature" plan wording) and
`scripts/self_use_queue.json` merge cleanly with no conflict markers in the
same `git merge-tree` output; `docs/roadmap/features/T5_F258.md` is
add-only on `origin/main`'s side.

This is a genuine content conflict, not a spurious one: `origin/main`'s
ledger now counts 258 registered items total (F258 added) while this
branch's closure commit still assumes 257, so a correct resolution needs to
re-derive the accepted-count and Tier 5 numbers against the true
post-#223/#224 baseline of 258 — a docs-ledger arithmetic problem, not a
mechanical per-side pick — which is why this session did not attempt the
resolution itself.

No code changed this session. No branch created. No PR merged. Git status
was clean at Phase 0 and remains clean after this handoff append (verified
before and after this section's own two commits).

Next expected action: a session resolves PR #225 against current `main`
(merge-base `f5b1e6c5b815a276f45fcb4cbd0cdf2cfa75f4e1`, main tip
`0fd3b7716021dee9037295acd89b315fc0af9e19`) — merging or rebasing `main`
into `feature/f040-completion-digest`, re-deriving the STATUS.md/README.md
accepted-count and Tier 5 numbers against the post-#223/#224 total of 258,
and re-running `python3 -m pytest tests/docs/ -q` — before the Open PR Gate
can merge #225 and before any new feature (including the one entry still
sitting in `.agent/candidates.md`, or the queued `amend0829` self-use
registration) can be claimed.

## 2026-08-30 — session 5, round 22 — merge conflict resolved

Resolved the exact conflict described in the prior section: fetched
`origin/main` and ran `git merge --no-ff origin/main` on
`feature/f040-completion-digest`. Conflicts occurred in exactly two files,
matching the earlier scratch-worktree finding — `README.md` and
`docs/roadmap/STATUS.md`. All other files (`docs/README.md`,
`scripts/self_use_queue.json`, `tests/docs/test_docs_consistency.py`,
`docs/roadmap/features/T5_F258.md`) merged cleanly with no conflict
markers and were carried in unedited.

Resolution applied (both sides' facts kept; only the shared count lines
re-derived against the new total of 258 features):
- `docs/roadmap/STATUS.md` (around line 87): kept F040 as
  `- [x] F040 — Completion/return digest (... accepted HEAD
  5281987a142b97f222256c987d36c009ae7ab3ae)` unchanged from this branch,
  followed immediately by `- [ ] F258 — Self-use track v2
  (self-replenishing queue & executed items)` from `origin/main`.
- `README.md` accepted-count line: `64 of 258 registered items accepted.
  Next: the first unchecked item in docs/roadmap/STATUS.md.`
- `README.md` Tier 5 table row: `| 5 | Operator Cockpit | 12 | 32 |`.

Verified zero conflict markers remained anywhere in the tree
(`grep -rnE "^(<{7} |>{7} )"` over the whole repo, excluding `.git`) before
staging. `git status --porcelain` showed no `U` entries and no changes
beyond what the merge itself brought in plus the two resolved files.

Gates run for real on the merge commit:
- `python3 -m pytest tests/docs/ -q` → `295 passed`.
- `python3 -m pytest tests/cli/test_golden_path.py -q` → `42 passed`.

Merge commit: `f69f1785` — "merge origin/main into
feature/f040-completion-digest (resolve F040/F258 STATUS+README
conflict)". `.agent/plan.md` rewritten in place (same round) to record
round 22 and that F040's own content is unchanged. This handoff section
and the plan.md update are committed separately per normal small-commit
discipline.

F040's own build content was not touched this round. No new branch, no
new feature work, no rebase, no force-push. PR #225 is still OPEN and
UNMERGED on GitHub — it must be merged at the next session's Open PR Gate
before any new feature work is claimed on this repo.
