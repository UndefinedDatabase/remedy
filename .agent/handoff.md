# Handback — F085 R67 (repair round, worker)

Branch `feature/f085-sandbox-hardening` · base SHA 261dce53 · head before C5 3440efe4.

## Range

Review of 261dce53..HEAD.

## Commits

### 69ee1209 docs(f085): save the R67 repair block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r67.md | +386/-0 | C0a — block saved byte-verbatim |

### a0723c7c docs(f085): mirror the R67 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +294/-287 | C0b — mirror of the authored block |

### 7c0dca8b docs(f085): advance the plan to the R67 repair round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +5/-5 | C1 — PLAN21F→PLAN21T |

### 60057260 docs(f085): record the R66 FAIL and register two findings
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +71/-0 | C2 — RECORD35 appended; R-0561, R-0562 |

### 5f09088a docs(f085): correct which classes run under the guard
| Path | +/- | Reason |
|---|---|---|
| docs/system/exec-guard-limitations-v0.md | +15/-6 | C3 — FIXDOCF→FIXDOCT |

### 3440efe4 docs(f085): retire the stale runtime-unsupervised claim in the guard docstring
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/exec_guard.py | +5/-2 | C4 — FIXMODF→FIXMODT, docstring bytes only |

### C5 — this commit (self-reference; a handoff cannot table the commit that writes it)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C5 — this handback |

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this commit |

## External actions

`git push -u origin feature/f085-sandbox-hardening` after C5. No PR, no merge, no worktree add/remove.

## Verification

G1 STATE PASS. `.agent/STOP` absent on both re-reads (before C0a, before C5); `git status --porcelain` empty at round start and after each of the six commits; `git worktree list` one line at start and at end — no worktree created.
G2 TRANSPORT PASS. Committed authored, committed last_block, both working copies and the received block: all five byte-EQUAL, sha256 8f1d0218ad4e0796a9618d46cf2737b8fd0d60ecb022431e5d73ebae92a99db1, 29948 B, 386 lines, 14 marker lines. Sizes from the committed file: TOTAL 386 ≤ 490; slices 127; PROSE 259 ≤ 400; RECORD35 71 ≤ 140.
G3 SHAPES PASS. Three REWRITES, each `TO contains FROM: false`, FROM 1x pre-commit / 0x post-commit, TO exactly 1x post-commit, and re-applying FROM→TO to the pre-commit blob reproduces the post-commit blob BYTE-EXACTLY: PLAN21 on `.agent/plan.md` at 7c0dca8b, FIXDOC on the limitations doc at 5f09088a, FIXMOD on `exec_guard.py` at 3440efe4. RECORD35 at 60057260 — ordered equality on every clause: PREFIX true, SUFFIX true, `pre + slice` == post byte for byte, ADDED lines == slice lines IN ORDER (71 and 71); no FROM measured. Marker LINES matching `^(BEGIN|END)-[A-Z0-9]+$` are 0 in all four edited files. numstat per path/commit in the tables above.
G4 SUITES PASS — primary checkout, serially, one pytest at a time, each exit 0: exec_guard readers `331 passed`; docs consistency `295 passed`; state readers `160 passed`; canary `42 passed`. Each equals its base reading.
G5 PLAN CONTRACT PASS. `.agent/plan.md` after C1 is 40 lines ≤ 50 (the block projected 40); contains `## Goal` true, contains `## Next Steps` true, matches `\bF\d{3}\b` true.
G6 ARITHMETIC PASS. 261dce53: 175 registered / 28 done / 0 landed, 147 open, max registered R-0560, max resolved R-0558. HEAD: 177 / 28 / 0, 149 open, max registered R-0562, max resolved R-0558. Registered symmetric difference exactly {R-0561, R-0562}; done and landed symmetric differences both EMPTY. Duplicate ids 0 and orphan resolutions 0 at both SHAs. Next free id R-0563. RECORD35 carries exactly two `- R-` lines and zero `Done:` lines.
G7 LINT PASS. `python3 -m ruff check packages/orchestration/exec_guard.py` exit 0, `All checks passed!`; `python3 -m ruff check --preview packages/orchestration/exec_guard.py` exit 0, `All checks passed!`.
G8 TRUTH AND INERTNESS PASS — all six readings. (1) INERTNESS: pre- and post-commit blobs of `exec_guard.py` at C4 parsed with `ast.parse`, each module docstring set to None, `ast.dump` of the two trees IDENTICAL; additionally each file with its module docstring removed is byte-identical — C4 changed docstring bytes and nothing executable. (2) `the runtime, git and packaging classes still spawn unsupervised` occurs 0x in `exec_guard.py` at HEAD; `The git, packaging, runtime and other call sites still spawn unsupervised` occurs 0x in the limitations doc at HEAD. (3) `grep -rn "spawn unsupervised"` over `packages/ apps/ docs/ tests/` at HEAD returns EXACTLY 2 hits, one per repaired file, and neither names `runtime` among its subjects. (4) the limitations doc at HEAD contains all six stage-1 class names: builder true, test true, dod-process true, dod-app true, runtime-server true, runtime-build true. (5) that file contains `SCOPE ruling` true and `can hang` true. (6) the old heading `## Only three command classes run under the guard at all` occurs 0x.
G9 HYGIENE PASS. `git diff --name-only 261dce53..HEAD` before C5 is exactly the six-path change set minus `.agent/handoff.md`. None of `packages/runtimes/dev_server.py`, `packages/runtimes/runtime_supervisor.py`, `apps/cli/commands/runtime_cmd.py`, `packages/orchestration/ui_server.py` appears; `git ls-tree 261dce53 -- <path>` resolves all four (EXISTS ×4). Insertions per commit before C5: 386, 294, 5, 71, 15, 5 — none exceeds 500. All commits single-parent.

## Authored-text proofs

All four slices were extracted PROGRAMMATICALLY from the committed `.agent/authored/f085-r67.md` by marker pair under the block's CONVENTION, applied with `bytes.replace` (PLAN21, FIXDOC, FIXMOD) and `pre + slice` (RECORD35), with no joiner and no terminator byte added. Disk-to-disk comparison against the committed authored file: EQUAL, sha256 8f1d0218…92a99db1. Nothing was retyped or reflowed; no marker line reached a target file (G3).

## Deviations & assumptions

No departure from the ordered commit sequence: C0a, C0b, C1, C2, C3, C4, C5 were committed in exactly that order, with C2 landing before C3 and C4 per constraint 6. No extra, dropped or reordered commit. No red control ordered or invented; no worktree created. No ledger text authored by the worker (constraint 8).
DISAGREEMENT DECLARED, reported and NOT fixed, per constraints 8 and 13. The block's prose ("THE SWEEP BEHIND THIS ROUND") and RECORD35's closing sentence in R-0562 both state that the `spawn unsupervised` sweep has two further hits beyond the two live claims — `OWNER_UNSUPERVISED` in `packages/runtimes/dev_server.py` and an example sentence in `docs/agents/planner_reviewer_prompt.md`. Measured with `git grep -n "spawn unsupervised"` over `packages/ apps/ docs/ tests/`, that phrase returns EXACTLY 2 hits at 261dce53 and EXACTLY 2 at HEAD — never 4. The `dev_server.py` lines match only the bare word `unsupervised` (4 occurrences, the `OWNER_UNSUPERVISED` constant), not the phrase; and `docs/agents/planner_reviewer_prompt.md` contains 0 occurrences of `unsupervised` in any case at either SHA. This does not fail G8, whose ordered reading is the 2-hit total and which passed; the defect is in the block's explanatory prose and in the reviewer-authored RECORD35 text now on disk. RECORD35 was left byte-verbatim.

## Next

FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk` — ahead of the PR Gate. Next expected action: R68.
ONE: R68 measures T2_F085's remaining acceptance line — a network access from a guarded test command fails under deny — against a loopback server that is really listening, with the red control that line needs; the integration gate and closure follow it.
TWO: R67 carries no verdict of its own, because the round that records a verdict cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13); R68 carries it, and R68's record is also where R-0561 and R-0562 are marked `Done:` if the reviewer's re-reading of both repaired files agrees.
THREE: 149 findings open; next free id R-0563.
Fortschritt: ~99 % (T001 gebaut · R13-R65 PASS · R66 FAIL, Fehler des Reviewers, in dieser Runde
repariert · T002 KOMPLETT · T003 fast fertig: Netz-Posture verdrahtet und gepinnt, Limitations-
Dokument steht, verlinkt und jetzt inhaltlich korrekt; offen bleibt allein die Akzeptanzmessung am
echt lauschenden Server) — Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.
