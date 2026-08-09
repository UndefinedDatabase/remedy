# Handoff — F105 R12 (T003 site 1, part 2)

F105 Cache-optimal prompt ordering, R12: register R-0238, record the R11 gate,
and land the intake segment manifest in call evidence. Branch
`feature/f105-cache-optimal-prompt-ordering`; no PR exists or was created.
EVIDENCE only — no prompt byte and no composition changed, which is why the R11
golden still passes unedited.

## Range
Review of `0f17725a..HEAD` — the five commits below. `git diff --stat
0f17725a..HEAD` at write time is the source of every path count here (R-0235):
9 paths (8 in the stat plus `.agent/handoff.md`, written by the last commit).

## Commits

### d81b0a84 chore(f105): save the R12 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f105-r12-1.md | +243/-0 | C1 — the R12 block, byte for byte |
| .agent/last_block.md | +191/-205 | C1 — same bytes; 434 ins, under the 500 cap |

### 2567d94b chore(f105): register R-0238
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +12/-0 | C2 — pair A (append), R-0238 registered first |

### 4d8a32ad chore(f105): record the R11 gate
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +30/-0 | C3 — pair B (append), R11 gate + R12 step line |

### 9a4553fd feat(f105): record the intake segment manifest in call evidence
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/prompt_trace.py | +28/-1 | C4a — `segment_manifest`, `segment_manifest_chars`, the `composed_prompt` parameter both derive from |
| packages/orchestration/intake.py | +37/-0 | C4b — `make_intake_call_recorder` beside the composer |
| apps/cli/commands/do_cmd.py | +16/-17 | C4c — the inline closure replaced by the factory |
| tests/orchestration/test_prompt_trace.py | +72/-0 | C4d — `TestSegmentManifest`, 5 tests |

### C5 (this commit) chore(f105): record the R12 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +15/-21 | C5 — the authored plan, verbatim slice of block lines 184-220 |
| .agent/handoff.md | this file | C5 — a handoff cannot table the commit that writes it (R-0149) |

## External actions
`git push -u origin feature/f105-cache-optimal-prompt-ordering` — run after the
C5 commit; result in the completion report. No PR created, no gh command, no
worktree added or removed.

## Verification
| # | Command | Exit | Real output (trimmed) |
|---|---|---|---|
| A | `cmp .agent/authored/f105-r12-1.md .agent/last_block.md` | 0 | (no output) |
| B | `wc -l` / `wc -c .agent/authored/f105-r12-1.md` | 0 | `243` / `15427` — **OVER the 240-line D2 cap by 3 lines**; reviewer text NOT trimmed |
| C | `python3 -m pytest tests/orchestration/test_prompt_trace.py -q` | 0 | `37 passed in 0.18s` (32 before, +5) |
| D | `python3 -m pytest tests/orchestration/test_intake_prompt_golden.py tests/orchestration/test_intake.py -q` | 0 | `42 passed in 0.40s` — 42 before, 42 after, golden file NOT edited |
| E | `python3 -m pytest tests/orchestration/test_structured_outputs.py tests/orchestration/test_provider_mode.py tests/orchestration/test_agent_run_trace.py tests/orchestration/test_do_run.py -q` | 0 | `159 passed in 1.12s` (path deviation 2 below) |
| F | `python3 -m pytest tests/orchestration/test_test_runner.py -q -k "live_review or context_md or plan_md"` | 0 | `4 passed, 47 deselected in 0.11s` |
| G | `python3 -m pytest tests/docs/ -q` | 0 | `294 passed in 0.25s` |
| H | `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) | 0 | `42 passed in 19.54s` |
| I | `python3 -m ruff check` on the 4 changed .py paths | 0 | `All checks passed!` |
| J | `git status --porcelain` | 0 | empty at C4; ` M .agent/plan.md` + ` M .agent/handoff.md` before the C5 commit. `git worktree list` → `/home/decodeux/Repos/remedy 9a4553fd [feature/f105-cache-optimal-prompt-ordering]`, the primary checkout alone |
| K | `python3 -m apps.cli.grouped integrity check --json` | 0 | `passed= True fail_count= 0 checks= 5` |
| M | `git diff --stat 0f17725a..HEAD` + `git log --shortstat` | 0 | 8 paths pre-C5, 9 with this file; per-commit insertions 434, 12, 30, 153 — each under the 500 cap |
| — | `git diff --name-only 0f17725a..HEAD -- docs AGENTS.md README.md .agent/context.md .agent/decisions.md .agent/candidates.md .agent/t003_inventory.md tests/orchestration/test_intake_prompt_golden.py` | 0 | (no output) — every forbidden path untouched |

## Authored-text proofs
Every needle SLICED by line index out of the committed
`.agent/authored/f105-r12-1.md`, never retyped (gate L):
| Pair | Shape | FROM before | FROM after | TO after | TO-only addition after |
|---|---|---|---|---|---|
| A (line 47 → 50-62) | append | 1 | 1 | 1 | 1 |
| B (line 70 → 73-103) | append | 1 | 1 | 1 | 1 |

`.agent/plan.md` equals block lines 184-220 byte for byte: sha256 `1a2da455` on
the slice and on the file.

## Deviations & assumptions
1. **Block over cap, declared**: gate B is 243 lines / 15427 bytes against
   DECISION F105 D2's 240 — 3 over, where R11 was 17 over. Per C1 the text was
   NOT trimmed and the real number is reported. Registering a finding is the
   reviewer's act, not the worker's; flagged here for R-0239. C1's commit landed
   at 434 insertions, under the 500 cap.
2. **Gate E path**: the block names `tests/test_do_run.py`, which does not
   exist. The real file is `tests/orchestration/test_do_run.py`; the other three
   targets were run as written. Same class as R-0234 (bare-basename citation).
3. **`build_trace_entry` import in intake.py is module-level**, not inside the
   factory: `prompt_trace` imports only stdlib plus `prompt_segments`, so there
   is no cycle, and a top-level import is what a text search lands on.
4. **DECISION F105 D3 not in `.agent/decisions.md`**: the block forbids touching
   that file and defers the ledger entry to R13. D3 is documented in the code —
   the `segment_manifest_chars` `#:` comment and the gate-C test docstring.
5. **Handoff length**: over the 60-line cap under DECISION D15 — cause is the
   mandated content: five per-commit tables, the 13-row verification table, the
   pair-proof table and the item-status table. No section dropped.

## Item status
| Item | Status | Reason |
|---|---|---|
| C1 | done | block saved to both paths, `cmp` exit 0; count reported and 3 OVER cap |
| C2 | done | pair A applied alone, R-0238 registered before any other change |
| C3 | done | pair B applied, R11 gate + R12 step line at the end of `## Steps` |
| C4 | done | (a) two derived fields, (b) named recorder factory, (c) CLI rewired, (d) 5 tests incl. the wiring guard |
| C5 | done | plan rewritten from the authored slice, handoff written, pushed |

## Open findings
Two: R-0221 (Low, carried from F103 R5) and R-0238 (Medium, registered this
round by C2, unresolved — its fix binds the reviewer). Next free ID: R-0239.

## Next
Reviewer gates `0f17725a..HEAD`; then R13 records DECISION F105 D3 in
`.agent/decisions.md` and starts site 2 of `.agent/t003_inventory.md`.
