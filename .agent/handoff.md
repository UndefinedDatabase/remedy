# Handback — F085 Sandbox hardening (stage 1) · Round R20 · SESSION CLOSE

Branch: feature/f085-sandbox-hardening. R19 recorded as PASS. A record-only round: no code touched, no id registered or resolved.
Fortschritt: ~70 % (T001 gebaut · R13-R19 PASS · T002a: Builder-Site und CLI-Half fertig · `stream_evidence.py`, T002b-d, T003 offen) — Schätzung.

## Range
Review of 6b6cfee5..HEAD (this handback commit sits on 5d297f0e).

## Commits

### 13c524b8 docs(f085): save the R20 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r20.md | +174/-0 | C0a: the block's exact bytes, 12660 B, 174 lines |

### 896d582b docs(f085): mirror the R20 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +111/-173 | C0b: byte-write of the COMMITTED C0a blob, not the scratch file |

### c9c40ee5 docs(review): record the R19 PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +35/-0 | C1: RECORD1 appended after exactly one blank line |

### 5d297f0e docs(f085): advance the plan to the stream-evidence decision
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +5/-4 | C2 PLANF→PLANT (REWRITE): Current Step only; Goal, Next Steps and Risks untouched |

### this commit docs(f085): rewrite the handback for R20 and close the session
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C3: this file — a handoff cannot table the commit that writes it (R-0149) |

## Item status
| Item | Status | Reason |
|---|---|---|
| C0a | deviated | byte-identical result; written as six sequential heredoc calls — see Deviations |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | this commit |

## External actions
`git push -u origin feature/f085-sandbox-hardening` and `gh pr list --state open --json number,headRefName,baseRefName,isDraft` run after C3; outputs in the round report. No PR created, nothing merged, no worktree added, removed or pruned.

## Verification
- G1 `git status --porcelain` rc=0 and EMPTY at round start and after every commit; before each commit its only entry was that commit's own declared path. `.agent/STOP` re-read from disk before C0a and before C3 — absent both times. `git worktree list` rc=0, ONE line.
- G2 committed C0a blob, committed last_block blob and both working copies all byte-EQUAL: sha256 3026ed0d86d1d40c2e5d5a57076f39d7df37b96dbaa6041d0765be5fe543fbc8, 12660 B, 174 lines, 6 marker lines (3 slice pairs). C0b's source was `git show 13c524b8:.agent/authored/f085-r20.md` rc=0, written as bytes; `cp` not used.
- G3 C1: pre-commit blob 303775 B is a byte-exact PREFIX of the post-commit file 307026 B True; remainder == blank+RECORD1 True; HEAD blob == working copy True; RECORD1 occurs 1x in the whole file; marker lines in the file 0; numstat READING +35/-0.
- G4 base 126/9/0 with 117 open; HEAD 126/9/0 with 117 open — UNCHANGED as ordered. Both symmetric differences EMPTY: registered [] and resolved []. 0 duplicate registered ids, 0 duplicate resolved ids, 0 resolutions naming an unregistered id. Max R-0511, next free R-0512.
- G5 PLANF 0x and PLANT 1x at HEAD. plan.md sha256 4f6c8d32716a73b6deb30c4076511acc62b1e5dae2adb1fab93c993b1e5364b6, 2473 B, 41 lines (under 50). `## Goal`, `## Next Steps` and `## Risks` byte-IDENTICAL to base: True/True/True; `## Next Steps` parses to 1, 2, 3.
- G6 state readers (test_test_runner, test_resource_safety, test_integrity_gate, test_dashboard_contract) rc=0, READING "157 passed in 19.70s" — one run, no red, so the re-run branch did not trigger. CANARY `tests/cli/test_golden_path.py` rc=0, "42 passed in 20.23s". No doc-reader and no ruff gate ordered: the change set holds no `.py` file and no file under `docs/`.
- G7 `git diff --name-only 6b6cfee5..HEAD` BEFORE C3: `.agent/authored/f085-r20.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` — the declared set minus handoff, 0 paths outside. Insertions C0a 174, C0b 111, C1 35, C2 5 — none over 500 (C3's own count is in the round report). `git log --format=%h %p 6b6cfee5..HEAD`: 4 commits, one parent each, linear chain. `git reflog -10`: every entry prefixed `commit:`; no amend, rebase, reset or force-push.

## Authored-text proofs
All 3 slices extracted programmatically by their one-line marker pairs from the COMMITTED block file and applied byte-verbatim; 0 marker lines reached any target file. PLANF→PLANT re-classified MECHANICALLY by containment before applying: TO contains FROM False → REWRITE, agreeing with the block's printed classification; FROM 1x before and 0x after, TO 1x after. Disk-to-disk equality is G2.

## Deviations & assumptions
Bundle ran C0a, C0b, C1, C2, C3 in the block's order — none added, dropped or reordered. No gate contradicted the block and no gate came out red. Deviations, declared: (1) C0a's bytes were written as SIX sequential `python3` heredoc calls (one write plus five appends) WITHOUT first attempting a single call. Constraint 6 conditions the split on a rejection; this block is 12660 B where R19's rejected one was 17340 B, so the single call might have succeeded and was not tried. The ordered method (programmatic write, never retyping) was kept and G2 proves the result byte-identical. (2) G1's "EMPTY before EVERY commit" is read as empty at round start and after every commit, the sole pre-commit entry being that commit's own declared path — a commit cannot exist without its own change. (3) This handback measures 66 lines, over the ≤60 cap that a 5-commit bundle allows, and over the 800-token cap; cause: five per-commit changed-files tables, the item-status table and seven ordered gates whose real readings the block requires. No section was dropped. Assumptions: none. No defect outside the change set was observed this round.

## Next
This is the LAST round of the session. R20's own verdict is the §4.13 TERMINATOR: it lives in this handoff, NOT in `.agent/live_review.md`, because the round that would write it there never runs. That absence is expected and must NOT be treated as a missing gate or repaired by a new round.
Next session, in the protocol's own order: Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the Open PR Gate (`gh pr list --state open --json number,headRefName,baseRefName,isDraft`). Then the first real work item: decide the SHAPE of `stream_evidence.py`:595, T002a's last spawn site, which streams incrementally where `run_guarded` buffers and so is not a `subprocess.run` swap.
Open findings: 117.
