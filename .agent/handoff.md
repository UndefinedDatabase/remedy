# Handback — F111 Diff-only repair · Round 20 (worker)

## Range
Review of ed7eaeef..HEAD — 7 commits on feature/f111-diff-only-repair.

## Item status
| Item | Status | Reason |
|---|---|---|
| C1 | deviated | split C1a/C1b — deviation 1 |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6 | deviated | plan is 43 lines, gate (g) says 44 — deviation 2 |

## Commits
### 57a1572f chore(f111): save the R20 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f111-r20-1.md | +329 | block saved verbatim (C1a) |

### 700a76c5 chore(f111): mirror the R20 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +294/-163 | byte copy (C1b, single-state-file exemption) |

### 7a7099f0 docs(f111): document the diff-only repair path
| Path | +/- | Reason |
|---|---|---|
| docs/system/diff-only-repair-v1.md | +108 | TEXT-A, sliced programmatically (C2) |

### ad2e1fe1 docs(f111): register the diff-only repair doc in the index
| Path | +/- | Reason |
|---|---|---|
| docs/README.md | +2 | TEXT-B pairs B1, B2 (C3) |

### d81b0b69 fix(f111): complete the metadata enumeration in the diff comment
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/builder_bridge.py | +3/-2 | TEXT-C, comment only; R-0318 (C4) |

### ee4d9de1 chore(f111): record the R19 gate in the live review
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +30 | TEXT-D plus one `Landed:` line (C5) |

### C6 — plan + handoff (grouped, R-0149 self-reference)
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | rewrite | TEXT-E verbatim, 43 lines |
| .agent/handoff.md | rewrite | this file |

## External actions
`git push origin feature/f111-diff-only-repair` after C6. No PR, no merge, no
force-push, no worktree; scratch under gitignored `.remedy-wt/`.

## Verification
a. `cmp` authored vs last_block → exit 0; sha256 of both
   `9c7497d0e5a849ee2a30de9fc063db37c38b20da45422e1bc14c22db21d43560`;
   `wc -lc` authored → `329 17746`.
b. doc extraction proof → `MATCH`.
c. `grep -c 'diff-only-repair-v1.md' docs/README.md` → `2`.
d. old enumeration → `0`; new enumeration → `1`. Run as
   `subprocess.run(['grep','-cF',…])` — this shell refuses backticks.
e. builder_bridge diff: one hunk at line 376, 2 comment lines out, 3 in,
   nothing else (full diff in the round report).
f. `^Done:` 11, `^Landed:` 1, `^### R19 — PASS` 1, `^- R-0` 43.
g. `wc -l .agent/plan.md` → **43**, not 44 (deviation 2).
h. `pytest tests/docs/ -q` → `294 passed in 0.30s`, exit 0.
i. `pytest tests/orchestration/test_builder_repair_loop.py -q` →
   `14 passed in 4.45s`, exit 0 (unchanged).
j. canary `tests/cli/test_golden_path.py -q` → `42 passed in 19.66s`, exit 0.
k. `ruff check packages/orchestration/builder_bridge.py` → `All checks
   passed!`, exit 0.
l. `git status --porcelain` empty; `git diff --name-only ed7eaeef..HEAD` = the
   eight ordered paths; rev-list vs origin → `0 0` after the push.

## Authored-text proofs
TEXT-A, TEXT-D, TEXT-E sliced from the authored file by marker index, never
retyped; TEXT-A re-read and compared → `MATCH`. TEXT-B, TEXT-C applied as
FROM→TO pairs, each FROM unique before the edit. No written line has trailing
whitespace.

## Deviations & assumptions
1. C1 split in two: 623 insertions in one commit breaks the 500 cap, and
   DECISION F105 D5 prescribes this exact split.
2. Gate (g) expects 44 lines; TEXT-E is 43. Bytes applied verbatim and the
   count reported as found — the Constraints forbid "improving" authored text.
3. TEXT-D calls `last_block.md` identical to `f111-r19-1.md`; true at session
   start, before C1b overwrote it. Applied verbatim, noted here.
Deviations, declared: 100 lines, over the 60-line cap and over the 800-token
thrift target — per-commit tables for 7 commits plus the mandated a-l block.
The ≤100 allowance for >5 commits applies; no section was dropped.

Fortschritt: ~95 % (T001 ✅ · T002 ✅ · T003 ✅ · Doku ✅ ·
Integration Gate offen · Closure offen) — Schätzung

## Next
Main-session review of ed7eaeef..HEAD, then the integration gate
(docs/agents/integration_gate.md).
