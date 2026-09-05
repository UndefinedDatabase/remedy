# Handoff — F262 List commands v2 (dates, sort, filter), round 23 (scope-correction, no code)

## Session

SESSION 8 of feature F262 · round 23 · rounds so far 23.

23 of the 25-round soft cap — 2 rounds of headroom left before the cap.

THIS ROUND FOUND NEW SCOPE THE REMAINING BUDGET CANNOT ABSORB, AND THIS IS
REPORTED HERE, NOT HIDDEN. Round 22 (R-0795) wired 3 named commands
(`worker.list`, `config.list`, `execution.list`) and PLAN23 assumed those
3 were the whole gap. This round's FINDING R-0796 shows the real count was
13 unwired commands, not 3: after the 3 landed, 13 more of the catalog's
28 list-shaped commands were STILL never wired to `apply_list_options` —
9 of them with genuine dates (squarely T003's target class), 3 static
registries with no date concept at all, and 1 hybrid config-catalog. DECISION
F262 D4 (registered this round) scopes T003's closure Acceptance to 24 of
28 commands, excluding the 3 registries and the hybrid by name, and leaves
the 9 genuine gaps IN scope but DEFERRED — they do not fit in the 2 rounds
of budget left at this feature's historical pace (roughly 1-3 commands per
round across R13-R22). This round wrote NO code and NO tests by design — it
is a finding routed to planning (docs/agents/planner_reviewer_prompt.md §4
item 7), not an oversight. The next action is an OPERATOR DECISION between
Option A (authorize sessions past the 7-session/25-round soft caps) and
Option B (split the 9 remaining wirings into a follow-up feature and close
F262 on the 24-of-28 scope) — see `.agent/plan.md`'s Next Steps. No further
F262 round should be delegated before that decision is made.

## Range

Review of 2e7e68b6..e89d302f

## Commits

### df0d10cc F262 R23 C0a: save step block to .agent/authored/f262-r23.md
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f262-r23.md | +138/-0 | Save the reviewer's round-23 step block byte-for-byte (new file), per C0a and the write-once transport rule. |

### 220780e1 F262 R23 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +96/-351 | Whole-file replace with the identical bytes committed in C0a (mirror), per C0b. |

### b022e1e1 F262 R23 C1: append GATE22 to live_review.md - books round 22's PASS verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +3/-1 | Append GATE22 (the reviewer's verbatim PASS verdict text for round 22, 3174 bytes) as a new paragraph, two `\n` separator, no trailing newline, per C1. |

### 1ce38723 F262 R23 C2: append Done: R-0795 to live_review.md - converts finding to resolved
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +3/-1 | Append the Done: R-0795 text (1269 bytes) converting the LANDED entry to reviewer-verified Done, two `\n` separator, no trailing newline, per C2. |

### b3e09695 F262 R23 C3: append FINDING R-0796 to live_review.md - config.list/worker.list/execution.list...
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +3/-1 | Append FINDING R-0796 (4126 bytes) — T003's scope was undercounted, 13 of 28 catalog list commands never wired, not just the 3 R-0795 named — two `\n` separator, no trailing newline, per C3. |

### 70d08235 F262 R23 C4: append DECISION F262 D4 to decisions.md - scope T003 Acceptance to 24 of 28 commands
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +8/-1 | Append DECISION F262 D4 (3213 bytes), one `\n` separator (this file's own consecutive-DECISION convention), no trailing newline, per C4. |

### 89ac80ba F262 R23 C5: append DECISION F262 D4 amendment to T2_F262.md - scope pointer
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F262.md | +12/-0 | Append the D4 amendment (728 bytes incl. leading and trailing newline) pointing the Goal/Acceptance scope at DECISION F262 D4 and FINDING R-0796, per C5. |

### e89d302f F262 R23 C6: replace plan.md with PLAN24 - scope-correction proposal (Option A/B)
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +30/-29 | Whole-file replace with PLAN24 (Current Step reflects round 23's scope correction; Next Steps hands the operator the Option A/Option B round-budget proposal). |

### (this commit) F262 R23 C7: rewrite .agent/handoff.md
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | Round-23 handback per docs/agents/handback_template.md; this is the round's last commit (write-once rule). |

## Item Status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | done | |
| C7 | done | this commit |
| G1 | done | sha256 identical, see Verification |
| G2 | done | all six byte numbers matched exactly |
| G3 | done | both byte numbers matched exactly |
| G4 | done | both byte numbers matched exactly |
| G5 | done | plan.md 2248 bytes, byte-for-byte equal to PLAN24 |
| G6 | done | tests/docs/ 295 passed |
| G7 | done | tests/cli/test_golden_path.py 42 passed |
| G8 | done | git status/ls-files/.agent/STOP all clean at both checkpoints |

## External actions

`git push -u origin feature/f262-list-commands-v2` — run after this commit; result reported below (Verification section).

No PR created, nothing merged, `main` untouched.

## Verification

**G1** — `sha256sum .agent/authored/f262-r23.md .agent/last_block.md`:
```
f14fce8e5ce2f78e6d3d75c3ba3c504bd0d0349aeafcc70aef213be9c6d6a167  .agent/authored/f262-r23.md
f14fce8e5ce2f78e6d3d75c3ba3c504bd0d0349aeafcc70aef213be9c6d6a167  .agent/last_block.md
```
Identical digest for both files. Exit code 0.

**G2** — byte-reads of `.agent/live_review.md`, Python binary mode:
- Immediately before C1: 2482540
- Immediately after C1: 2485716 (2482540 + 2 + 3174, GATE22 text)
- Immediately before C2: 2485716
- Immediately after C2: 2486987 (2485716 + 2 + 1269, Done: R-0795 text)
- Immediately before C3: 2486987
- Immediately after C3: 2491115 (2486987 + 2 + 4126, FINDING R-0796 text)

All six numbers match the block's stated arithmetic exactly, each verified with an `assert` in the writing script before commit (no AssertionError raised).

**G3** — byte-reads of `.agent/decisions.md`, Python binary mode:
- Immediately before C4: 806068
- Immediately after C4: 809282 (806068 + 1 + 3213, DECISION F262 D4 text)

Both numbers match the block's stated arithmetic exactly, verified with an `assert` before commit.

**G4** — byte-reads of `docs/roadmap/features/T2_F262.md`, Python binary mode:
- Immediately before C5: 3504
- Immediately after C5: 4232 (3504 + 728, amendment text incl. its own leading and trailing newline)

Both numbers match the block's stated arithmetic exactly, verified with an `assert` before commit.

**G5** — byte-read of `.agent/plan.md` immediately after C6, binary mode: 2248 bytes, byte-for-byte equal (`after == plan_bytes`, asserted) to the PLAN24 text in the step block. Note: the PLAN24 text as authored has NO trailing newline (first attempt with a trailing `\n` measured 2249 bytes, one over target; removing the single trailing newline byte landed on the mandated 2248 exactly) — declared here per constraint 6's substitution-declaration requirement, though no Write-tool/heredoc substitution was needed this round (the `python3 -c` heredoc route worked directly for every file this round).

**G6** — `python3 -m pytest tests/docs/ -q`:
```
........................................................................ [ 24%]
........................................................................ [ 48%]
........................................................................ [ 73%]
........................................................................ [ 97%]
.......                                                                  [100%]
295 passed in 0.45s
```
295 passed. Exit code 0. Docs-round gate triggered because C5 touches `docs/roadmap/**`.

**G7** — `python3 -m pytest tests/cli/test_golden_path.py -q`:
```
..........................................                               [100%]
42 passed in 20.90s
```
42 passed. Exit code 0. Mandatory canary, unmoved.

**G8** — `git status --porcelain`: empty, checked before C0a (clean at session start) and immediately before C7 (checked again just above, empty after C6's commit). `git ls-files .remedy-wt`: empty, both checks. `.agent/STOP`: absent, both checks (`ls: cannot access '.agent/STOP': No such file or directory`).

## Authored-text proofs

- GATE22 text (3174 bytes UTF-8): appended via Python `pathlib.Path.write_bytes`, byte length asserted equal to 3174 before writing (assertion held), before/after sizes cross-checked in G2.
- Done: R-0795 text (1269 bytes UTF-8): same method, byte length asserted equal to 1269 before writing (assertion held), before/after sizes cross-checked in G2.
- FINDING R-0796 text (4126 bytes UTF-8): same method, byte length asserted equal to 4126 before writing (assertion held), before/after sizes cross-checked in G2.
- DECISION F262 D4 text (3213 bytes UTF-8, 7 lines): same method, byte length asserted equal to 3213 before writing (assertion held), before/after sizes cross-checked in G3.
- T2_F262.md amendment text (728 bytes UTF-8 incl. leading/trailing newline): same method, byte length asserted equal to 728 before writing (assertion held), before/after sizes cross-checked in G4.
- PLAN24 (2248 bytes UTF-8, no trailing newline): written via Python `pathlib.Path.write_bytes` after removing one trailing-newline byte from the first draft (see G5); final on-disk content matches the step block's PLAN24 text exactly, final byte count 2248, `after == plan_bytes` asserted true.
- `.agent/authored/f262-r23.md` / `.agent/last_block.md`: identical per G1's sha256sum.
- All five embedded sub-texts (GATE22, Done: R-0795, FINDING R-0796, DECISION D4, T2_F262.md amendment) were also independently byte-counted by extracting them out of the saved `.agent/authored/f262-r23.md` before any append, confirming each matched its stated byte count (3174 / 1269 / 4126 / 3213 / 728) prior to being used for the live appends.

## Deviations & assumptions

- PLAN24's byte target (2248) required the plan text to end with NO trailing newline, unlike the natural output of a Python triple-quoted string ending in `\n"""` (which measured 2249). This was resolved by writing the text without a trailing newline, not by a Write-tool/trim substitution — no bash-guard refusal occurred this round for any of the six writes (GATE22, Done, FINDING, DECISION, amendment, PLAN24 all went through directly via `python3 -c`-style heredocs run as here-doc scripts, no refusal encountered). Recorded because a byte-count correction happened, even though the write route itself needed no substitution.
- No other departure from the block's ordered commit sequence (C0a, C0b, C1, C2, C3, C4, C5, C6, C7, in that exact order).
- Per constraint 5, none of the 9 or 13 named commands were wired this round — verified by `git diff --stat` across all seven content commits (C0a-C6) showing no path under `apps/cli/commands/` or `tests/cli/` touched, only `.agent/**` and `docs/roadmap/features/T2_F262.md`.
- No mutation red-proof was ordered or needed this round — there is no code change to mutate against; this round's bundle is prose-only (finding + DECISION + plan), per the recognized "wrong spec is a finding routed to planning" round shape (docs/agents/planner_reviewer_prompt.md §4 item 7).

## Next

**OPERATOR DECISION REQUIRED before any further F262 round is delegated.** FINDING R-0796 (this round) discovered that T003's real remaining scope is 9 genuine command wirings, not the 3 R-0795 named — a round-budget mismatch, not a routine next step. `.agent/plan.md`'s Next Steps lays out the two routes:
- **Option A**: authorize sessions beyond the 7-session/25-round soft caps (already session 8, round 23) to wire the 9 remaining commands (test.list, repair.item-list, builder.session-list, execution.approval-list, mission.list, change.list, event.list, external-builder.package-list, self-repair.proposal-list) plus the T001 catalog-driven handler test plus the Acceptance smoke test.
- **Option B**: split the 9 remaining into a NEW follow-up feature (STATUS.md line), build the T001/Acceptance tests scoped to the 24 D4-covered commands only, and close F262 within the 2 rounds of budget left.

No code or test work should be delegated on F262 until the operator picks one of these two options.
