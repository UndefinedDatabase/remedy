# Handback — F085 Sandbox hardening (stage 1) · Round R19

Branch: feature/f085-sandbox-hardening. R18 recorded; R-0511 registered and resolved — the
pre-emission checklist's own introduction no longer states a count of the items beneath it.
Fortschritt: ~70 % (T001 gebaut · R13-R18 PASS · T002a: Builder-Site und CLI-Half fertig ·
`stream_evidence.py`, T002b-d, T003 offen) — Schätzung.

## Range
Review of 646092ce..HEAD (this handback commit sits on 1c6b8e32).

## Commits

### 3085fbf9 docs(f085): save the R19 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r19.md | +236/-0 | C0a: the block's exact bytes, 17340 B, 236 lines |

### 7448bd11 docs(f085): mirror the R19 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +155/-200 | C0b: byte-write of the COMMITTED C0a blob, not the scratch file |

### 64532a38 docs(review): record the R18 PASS and register R-0511
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +58/-0 | C1: RECORD1 then REG1 — findings persist in the first content commit |

### 99234e5d docs(agents): drop the stale check count from the checklist heading
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +2/-2 | C2 HEADF→HEADT (REWRITE): "Run all twelve checks" becomes "Run EVERY check below" |

### 0c7591dd docs(review): resolve R-0511 now that the heading carries no count
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +13/-0 | C3: DONE1, appended AFTER C2 landed — separate commit on purpose |

### 1c6b8e32 docs(f085): advance the plan to the stream-evidence round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +4/-4 | C4 PLANF→PLANT: Current Step rewritten; Goal, Next Steps and Risks untouched |

### this commit docs(f085): rewrite the handback for R19
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5: this file — a handoff cannot table the commit that writes it (R-0149) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | deviated | byte-identical result; written as seven sequential heredoc writes — see Deviations |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |

## Verification
- G1 `git status --porcelain` rc=0, output `''` before every commit in the bundle and after C4; `git worktree list` rc=0, ONE line (`/home/decodeux/Repos/remedy 1c6b8e32`); `.agent/STOP` re-read from disk before C0a and before C5 — absent both times. No worktree added, removed or pruned.
- G2 committed C0a blob, committed last_block blob and both working copies all byte-EQUAL: sha256 4d750d6c237b25d7bd6e990ca0fee97bd3c9b47a03c5d2340ebda2ea81a13fba, 17340 B, 236 lines, 14 marker lines (7 slice pairs). C0b's source was `git show 3085fbf9:.agent/authored/f085-r19.md` (rc=0), written as bytes; `cp` not used.
- G3 C1: pre-commit blob 297276 B is a byte-exact PREFIX of the post-commit file 302599 B True, remainder == blank+RECORD1+blank+REG1 True, HEAD blob == working copy True; numstat READING +58/-0. C3: pre 302599 B is a prefix of post 303775 B True, remainder == blank+DONE1 True, HEAD blob == working copy True; READING +13/-0. At HEAD RECORD1 1×, REG1 1×, DONE1 1×; marker lines `^<<<` in the file: 0.
- G4 base 125/8/0 → 117 open; after C1 126/8/0 → 118 open (the registration landed); HEAD 126/9/0 → 117 open. Symmetric differences base↔HEAD: registered exactly `['R-0511']`, resolved exactly `['R-0511']`. 0 duplicate registered ids, 0 duplicate resolved ids, 0 resolutions naming an unregistered id. Max R-0511, next free R-0512.
- G5 HEADF 0× and HEADT 1× at HEAD. `twelve` occurs 0× in the WHOLE file. Region from `**Pre-emission block checklist` to the `  Why this is on disk` line parses to [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17] — contiguous, 0 repeats, 0 gaps.
- G6 PLANF 0× and PLANT 1× at HEAD. plan.md sha256 5684439dfacac31c052cd4e63bb661ed8a1b25218ae68c51fc09c3c7e1865d04, 2341 B, 40 lines (under 50). `## Goal`, `## Next Steps` and `## Risks` byte-IDENTICAL to base: True/True/True. `## Next Steps` parses to 1, 2, 3.
- G7 `python3 -m pytest tests/test_agent_tooling.py tests/docs/ -q` rc=0, "305 passed, 1 skipped in 0.53s". No ruff gate ordered: the change set holds no `.py` file.
- G8 state readers (test_test_runner, test_resource_safety, test_integrity_gate, test_dashboard_contract) rc=0, READING "157 passed in 19.79s" — one run, no red, so the re-run branch did not trigger. CANARY `tests/cli/test_golden_path.py` rc=0, "42 passed in 20.46s".
- G9 `git diff --name-only 646092ce..HEAD` BEFORE C5: `.agent/authored/f085-r19.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `docs/agents/planner_reviewer_prompt.md` — equals the declared set minus handoff, 0 paths outside. Insertions C0a 236, C0b 155, C1 58, C2 2, C3 13, C4 4 — none over 500 (C5's own count is not ordered here; it is in the round report). `git log --format=%h %p 646092ce..HEAD`: 6 commits, one parent each, linear chain. `git reflog -12`: every entry prefixed `commit:`, 0 non-commit entries; no amend, rebase, reset or force-push.

## Authored-text proofs
All 7 slices extracted programmatically by their one-line marker pairs from the COMMITTED block file and applied byte-verbatim; 0 marker lines reached any target file. Pair shapes re-classified MECHANICALLY by containment before applying, per constraint 3 and checklist item 15: HEADF→HEADT containment False → REWRITE, FROM 1× before and 0× after, TO 1× after; PLANF→PLANT containment False → REWRITE, FROM 1× before and 0× after, TO 1× after. Both readings agree with the block's printed classification. Disk-to-disk equality is G2.

## External actions
`git push -u origin feature/f085-sandbox-hardening` and `gh pr list --state open --json number,headRefName,baseRefName,isDraft` run after C5; outputs in the round report. No PR created, nothing merged, no worktree added, removed or pruned.

## Deviations & assumptions
Bundle ran C0a, C0b, C1, C2, C3, C4, C5 in the block's order — none added, dropped or reordered. No gate contradicted the block and no gate came out red. Deviations, declared: (1) C0a's file was written by SEVEN sequential `python3 - <<'PY'` calls (one write plus six appends) rather than one, because this session's Bash parser aborted the single ~17 KB command with "Parser aborted (timeout, resource limit, or over-length)"; constraint 6 permits exactly this, the ordered method (programmatic write, never retyping) was kept, and G2 proves the result byte-identical. (2) This handback measures 80 lines and roughly 1.9k tokens: within the ≤100 lines the template allows when per-commit tables of more than five commits require it, but over the 800-token hard cap — cause: seven per-commit changed-files tables, the item-status table, and nine ordered gates whose real readings the block requires; no section was dropped. No defect outside the change set was found this round, so nothing is deferred to the reviewer as an unrepaired observation. The block's own sweep claim was spot-checked and holds — a number-word beside one of the eight listed nouns matched exactly the four lines the block names at base (174, 223, and the quoted examples in items 16 and 17), and only line 174 was a heading counting its own contents.

## Next
Reviewer re-runs G1-G9 over 646092ce..HEAD and issues the R19 verdict, re-reading `.agent/STOP` first. If PASS, the next round leaves the review machinery and takes `stream_evidence.py`:595 — T002a's last site, and not a `subprocess.run` swap, so its shape is decided before any code moves.
