# Handoff — F105 R11 (T003 site 1)

F105 Cache-optimal prompt ordering, R11: record the R10 gate, resolve R-0236 and
R-0237, and migrate `packages/orchestration/intake.py::_build_intake_prompt` to
the prompt-segment registry under a content-equality golden. Branch
`feature/f105-cache-optimal-prompt-ordering`; no PR exists or was created.
Composition only — the segment manifest reaches call evidence in R12.

## Range
Review of `9d773b14..HEAD` — the four commits below. `git diff --stat
9d773b14..HEAD` is the source of every path count here (R-0235): 5 paths,
650 insertions / 186 deletions over the range before the C4 commit.

## Commits

### 05bb20bf chore(f105): save the R11 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f105-r11-1.md | +257/-0 | C1 — the R11 block, byte for byte |
| .agent/last_block.md | +196/-179 | C1 — same bytes; 453 ins, under the 500 cap |

### c1a8e74d chore(f105): record the R10 gate and resolve R-0236 and R-0237
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +44/-2 | C2 — pairs A, B (rewrites) and C (append) |

### 4e991639 feat(f105): compose the intake prompt from registered segments
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/intake.py | +40/-5 | C3a/b — three sliced segment constants, `compose_intake_prompt`, `_build_intake_prompt` reduced to one line |
| tests/orchestration/test_intake_prompt_golden.py | +113/-0 | C3c — the site-1 golden, 5 tests |

### C4 (this commit) chore(f105): record the R11 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +18/-21 | C4 — the authored plan, verbatim slice of block lines 190-232 |
| .agent/handoff.md | this file | C4 — a handoff cannot table the commit that writes it (R-0149) |

## External actions
`git push -u origin feature/f105-cache-optimal-prompt-ordering` — run after the
C4 commit; result in the completion report. No PR created, no gh command, no
worktree added or removed.

## Verification
| # | Command | Exit | Real output (trimmed) |
|---|---|---|---|
| A | `cmp .agent/authored/f105-r11-1.md .agent/last_block.md` | 0 | (no output) |
| B | `wc -l -c .agent/authored/f105-r11-1.md` | 0 | `257 16297` — **OVER the 240-line D2 cap by 17 lines**; reviewer text NOT trimmed |
| C | `python3 -c` split proof vs `git show 9d773b14:packages/orchestration/intake.py` (full command below) | 0 | `EQUAL, chars: 634` |
| D | `python3 -m pytest tests/orchestration/test_intake_prompt_golden.py -q` | 0 | `5 passed in 0.13s` |
| E | `python3 -m pytest tests/orchestration/test_intake.py -q` | 0 | `37 passed in 0.37s` (37 before, 37 after) |
| F | `python3 -m pytest tests/orchestration/test_prompt_segments.py tests/orchestration/test_role_conventions.py -q` | 0 | `48 passed in 0.12s` |
| G | `python3 -m pytest tests/orchestration/test_test_runner.py -q -k "live_review or context_md or plan_md"` | 0 | `4 passed, 47 deselected in 0.11s` |
| H | `python3 -m pytest tests/docs/ -q` | 0 | `294 passed in 0.25s` |
| I | `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) | 0 | `42 passed in 19.77s` |
| J | `grep -rn "_INTAKE_PROMPT_TEMPLATE" packages/ apps/` | 1 | 0 hits (one hit in `tests/orchestration/test_intake_prompt_golden.py:10`, the golden's docstring naming the frozen constant) |
| K | `git status --porcelain` | 0 | empty at C3; ` M .agent/plan.md` before the C4 commit |
| L | `git worktree list` | 0 | `/home/decodeux/Repos/remedy 4e991639 [feature/f105-cache-optimal-prompt-ordering]` — the primary checkout alone |
| M | `python3 -m apps.cli.grouped integrity check --json` | 0 | `passed= True fail_count= 0 checks= 5` |
| O | `git log --format='%h %s' --shortstat 9d773b14..HEAD` | 0 | 453, 44, 153 insertions — each under the 500 cap |

Gate C, in full:
`python3 -c 'import subprocess; from packages.orchestration import intake; src =
subprocess.run(["git","show","9d773b14:packages/orchestration/intake.py"],capture_output=True,text=True,check=True).stdout;
ns = {}; exec("".join(src.splitlines(keepends=True)[28:44]), ns); joined =
"\n\n".join([intake._INTAKE_SYSTEM_SEGMENT, intake._INTAKE_MISSION_TEMPLATE,
intake._INTAKE_RULES_SEGMENT]); assert joined == ns["_INTAKE_PROMPT_TEMPLATE"],
"NOT EQUAL"; print("EQUAL, chars:", len(joined))'` → `EQUAL, chars: 634`.

## Authored-text proofs
Every needle was SLICED by line index out of the committed
`.agent/authored/f105-r11-1.md`, never retyped (gate N):
| Pair | Shape | FROM before | FROM after | TO after |
|---|---|---|---|---|
| A (lines 48 → 51-56) | rewrite | 1 | 0 | 1 |
| B (lines 60 → 63-67) | rewrite | 1 | 0 | 1 |
| C (line 71 → 74-107) | append | 1 | 1 | 1 (TO-only addition, lines 75-107: 1) |

`.agent/plan.md` equals block lines 190-232 byte for byte: `sha256sum` of the
file and of the slice both `cde2364d`.

## Deviations & assumptions
1. **Block over cap, declared**: gate B is 257 lines / 16297 bytes against
   DECISION F105 D2's 240; the reviewer's hand-count put it near 235. Per C1 the
   text was NOT trimmed. Same class as R-0236 (which this round resolved on R10's
   evidence); registering a finding is the reviewer's, not the worker's, act —
   flagged here for R-0238. C1's commit still landed at 453 insertions, under 500.
2. **Test 1 wording**: `PromptSegmentManifestEntry` carries name/rank/sha256/
   sizes but NO text, so "the composed manifest's segment texts" is realised as
   `composed.text.split("\n\n")` (3 parts, the fixtures contain no blank line)
   AND, additionally, by comparing the manifest's sha256 set with the sha256 of
   the three frozen parts. Stronger than the letter, same intent.
3. **WHY placement**: a docstring cannot sit above a `def`, so the WHY text is a
   comment block directly above `compose_intake_prompt` (AGENTS.md's own idiom)
   plus a one-line docstring inside it.
4. **Slicing mechanics**: the C3 template split and the golden's frozen constant
   were produced by throwaway scripts under gitignored `.remedy-wt/` so no byte
   was retyped; nothing under `.remedy-wt/` is committed (integrity
   `relevant_untracked untracked=0`).
5. **Handoff length**: over the 60-line cap under DECISION D15 — cause is the
   mandated content: 14-row verification table, the full gate-C command, the
   per-commit tables, the pair-proof table and the item-status table. No section
   dropped.

## Item status
| Item | Status | Reason |
|---|---|---|
| C1 | done | block saved to both paths, `cmp` exit 0; count reported and OVER cap |
| C2 | done | pairs A, B, C applied in one commit, counts verified |
| C3 | done | (a) lossless split proven, (b) registry composition, (c) 5-test golden |
| C4 | done | plan rewritten from the authored slice, handoff written, pushed |

## Open findings
One: R-0221 (Low, carried from F103 R5). R-0236 and R-0237 are RESOLVED this
round. Next free finding ID: R-0238.

## Next
Reviewer gates `9d773b14..HEAD`; then R12 wires the intake segment manifest into
call evidence through `_record_intake_call` at `apps/cli/commands/do_cmd.py:206`.
