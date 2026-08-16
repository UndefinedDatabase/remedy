# Handback — F085 Sandbox hardening (stage 1) · Round R18

Branch: feature/f085-sandbox-hardening. R17 recorded; three standing rules now bind on disk as
pre-emission checklist items 15, 16 and 17.

## Range
Review of 88dbcefa..HEAD (this handback commit sits on bb02c15a).

## Commits

### 9dfaba9c docs(f085): save the R18 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r18.md | +281/-0 | C0a: the block's exact bytes, 20616 B, 281 lines |

### ec6378e1 docs(f085): mirror the R18 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +198/-226 | C0b: byte-write of the COMMITTED C0a blob, not the scratch file |

### 482c772b docs(review): record the R17 PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +44/-0 | C1: RECORD1 only — a record registers no id |

### d93ee9b2 docs(agents): promote three standing rules into the pre-emission checklist
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +34/-0 | C2 PROMF→PROMT (APPEND): items 15, 16, 17 land before the "why this is on disk" closer |

### bde77180 docs(review): resolve R-0508 and R-0510 now that the promotion has landed
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +21/-0 | C3: DONE1 then DONE2, appended AFTER C2 landed — separate commit on purpose |

### bb02c15a docs(f085): advance the plan to the stream-evidence round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +7/-11 | C4 PLANF→PLANT: Current Step rewritten, the promotion item dropped, Next Steps renumbered 1-3 |

### this commit docs(f085): rewrite the handback for R18
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5: this file — a handoff cannot table the commit that writes it (R-0149) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | deviated | byte-identical result; written as four sequential heredoc appends — see Deviations |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |

## Verification
- G1 `git status --porcelain` rc=0, output `''` before every commit in the bundle; `git worktree list` rc=0, ONE line; `.agent/STOP` re-read from disk before C0a and before C5 — absent both times. No worktree added, removed or pruned.
- G2 committed C0a blob, committed last_block blob and both working copies all byte-EQUAL: sha256 7187303bf16c3414278b5cbcf7efe2ddb082e3e4c4405e31fc65247ca9ccbac8, 20616 B, 281 lines. C0b's source was `git show 9dfaba9c:.agent/authored/f085-r18.md` (rc=0), written as bytes; `cp` not used.
- G3 C1: pre-commit blob 3bf90058 (291333 B) is a byte-exact PREFIX of post-commit c186eb98 (295507 B) True, remainder == blank+RECORD1 True, HEAD blob == working copy True, RECORD1 1× in the whole file; numstat READING +44/-0. C3: pre 295507 B is a prefix of post 297276 B True, remainder == blank+DONE1+blank+DONE2 True, DONE1 1× and DONE2 1× (RECORD1 still 1×); READING +21/-0. Marker lines `^<<<` in the file after both commits: 0.
- G4 base 125/6/0 → 119 open; after C1 125/6/0 → 119 open (a record adds no id); HEAD 125/8/0 → 117 open. Symmetric differences base↔HEAD: registered `[]` (NO registration), resolved exactly `['R-0508', 'R-0510']`. 0 duplicate registered ids, 0 duplicate resolved ids, 0 resolutions naming an unregistered id. Max R-0510, next free R-0511.
- G5 PROMF 1× in docs/agents/planner_reviewer_prompt.md at HEAD (APPEND pair — no 0× reading ordered or taken). Among C2's own 34 added lines each title occurs exactly once: `Pair shapes are classified` 1, `No heading states a count` 1, `spans the whole structure` 1. Region from `**Pre-emission block checklist` to the PROMF line parses to [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17] — contiguous, 0 repeats, 0 gaps.
- G6 PLANF 0× and PLANT 1× at HEAD. plan.md sha256 65f9287c4ef71975c8b956a9df25793cd2e5584fb528cc816a374c39d5ca0253, 2344 B, 40 lines (under 50). `## Goal` and `## Risks` byte-IDENTICAL to base: True/True. `## Next Steps` parses to 1, 2, 3 — no repeat.
- G7 `python3 -m pytest tests/test_agent_tooling.py tests/docs/ -q` rc=0, "305 passed, 1 skipped in 0.54s". No ruff gate ordered: the change set holds no `.py` file.
- G8 state readers (test_test_runner, test_resource_safety, test_integrity_gate, test_dashboard_contract) rc=0, READING "157 passed in 19.68s" — one run, no red, so the re-run branch did not trigger. CANARY `tests/cli/test_golden_path.py` rc=0, "42 passed in 20.26s".
- G9 `git diff --name-only 88dbcefa..HEAD` BEFORE C5: `.agent/authored/f085-r18.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `docs/agents/planner_reviewer_prompt.md` — equals the declared set minus handoff, 0 paths outside. Insertions C0a 281, C0b 198, C1 44, C2 34, C3 21, C4 7 — none over 500 (C5's own count is not ordered here; it is in the round report). `git log --format=%h %p 88dbcefa..HEAD`: 6 commits, one parent each, linear chain. `git reflog -15`: every action `commit`, 0 non-commit entries; no amend, rebase, reset or force-push.

## Authored-text proofs
All 7 slices extracted programmatically by their one-line marker pairs from the COMMITTED block file and applied byte-verbatim; 0 marker lines reached any target file. Pair shapes re-classified MECHANICALLY by containment before applying, per constraint 3 and the new item 15: PROMF→PROMT containment True → APPEND, FROM 1× before and 1× after (it legitimately survives inside its own TO, so no "FROM 0×" was read); PLANF→PLANT containment False → REWRITE, FROM 1× before and 0× after. Both readings agree with the block's printed classification. Disk-to-disk equality is G2.

## External actions
`git push -u origin feature/f085-sandbox-hardening` and `gh pr list --state open --json number,headRefName,baseRefName,isDraft` run after C5; outputs in the round report. No PR created, nothing merged, no worktree added, removed or pruned.

## Deviations & assumptions
Bundle ran C0a, C0b, C1, C2, C3, C4, C5 in the block's order — none added, dropped or reordered. No gate contradicted the block and no gate came out red. Deviations, declared: (1) C0a's file was written by FOUR sequential `python3 - <<'PY'` heredoc appends rather than one, because this session's Bash parser aborted the single ~20 KB command with "Parser aborted (timeout, resource limit, or over-length)"; the method the block ordered (python heredoc, never retyping into a target) was kept and the result is proven byte-identical by G2. (2) This handback measures 78 lines and roughly 1.8k tokens: within the ≤100 lines the template allows when per-commit tables of more than five commits require it, but over the 800-token hard cap — cause: seven per-commit changed-files tables, the item-status table, and nine ordered gates whose real readings the block requires; no section was dropped. Observation for the reviewer, NOT repaired because the block's change set forbids widening: `docs/agents/planner_reviewer_prompt.md` still opens the checklist with "Run all twelve checks" over a list that now holds 17 — a heading stating a count of its own contents, which is exactly what the item 16 landed this round forbids.

## Next
Reviewer re-runs G1-G9 over 88dbcefa..HEAD and issues the R18 verdict, re-reading `.agent/STOP` first. If PASS, the next round takes `stream_evidence.py`:595 — T002a's last site, and not a `subprocess.run` swap, so its shape is decided before any code moves.
