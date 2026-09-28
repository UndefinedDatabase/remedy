# Handoff — F036, round 1 (claim F036, move F286 behind it, book F035 R10, land T001: the
tour's stop shape, the anchor check against the job's own records, and the mechanical tour)

## Session

SESSION 1 of feature F036 · round 1 · rounds so far 1. Context remaining at handback: a large
majority of the context budget is left — this round read AGENTS.md, the block, the eight
required source files in full, the three PAYLOADS plus the claim diff, DECISION F036 D1/D2 in the
applied claim, and `docs/agents/handback_template.md` once each; wrote the module and its tests
and the mutation tool from the specification; ran the payload-verification script, the G1/G2
byte-equality and hash scripts, ruff, the G4 pytest selection, `integrity check`, and the G5
mutation tool once each.

## Range

Review of `9dc2f2a79..HEAD` (`HEAD` is this handback's own commit, `F036 R1 C5`, on
`feature/f036-guided-result-tour`).

## Commits

### 3ac8dbb81 F036 R1 C1a: copy round 1 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r1-block.md | 340/0 | copy of the block, verified line count and sha256 |
| .agent/authored/f036-r1-context.md | 37/0 | copy of the reviewer's context.md payload |
| .agent/authored/f036-r1-plan.md | 29/0 | copy of the reviewer's plan.md payload |

### f28f32d2b F036 R1 C1b: copy round 1 claim diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r1-claim.diff | 217/0 | copy of the reviewer's claim diff |

### 202f8ddd0 F036 R1 C2: claim F036, move F286 behind it, book F035 R10, record D1 and D2
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | 15/14 | rewritten to plan.md's context payload |
| .agent/decisions.md | 84/0 | DECISIONS F036 D1 and D2 appended by claim.diff |
| .agent/live_review.md | 24/24 | re-headed; F035 R10 gate entry appended by claim.diff |
| .agent/operator_questions.md | 20/1 | Q6 replaces EMPTY, by claim.diff |
| .agent/plan.md | 16/12 | rewritten to the reviewer's plan.md payload |
| docs/roadmap/STATUS.md | 1/1 | F036 `[ ]` to `[~]`, moved above F286's Tier 2 heading |
| docs/roadmap/features/T2_F286.md | 2/0 | one two-line note: moved behind F036 by D2 |

### 89081e1f2 F036 R1 C3: build the result tour's stops, anchor check and mechanical tour
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/result_tour.py | 448/0 | NEW module: S1–S7, the tour, stop shape, anchor check, resolver, mechanical tour |
| tests/test_no_orphan_modules.py | 3/0 | ALLOWED_UNWIRED entry for result_tour.py (S7) |

### 8b32f9d83 F036 R1 C4a: test the result tour's anchors and mechanical stops
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_result_tour.py | 450/0 | NEW test file, all 12 required cases (see Deviations) |

### 6fcf64887 F036 R1 C4b: add the mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f036-r1-mutations.py | 139/0 | the G5 red-proof tool: 12 mutations, all caught |

### <this commit> F036 R1 C5: rewrite handoff for round 1
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, per docs/agents/handback_template.md |

## External actions

- `git checkout -b feature/f036-guided-result-tour` — new branch created off `9dc2f2a79`, no
  pull first (Open PR Gate had already run and `main` was at the merge commit). Outcome: branch
  created, confirmed by `git branch --show-current`.
- `git worktree add --detach .remedy-wt/f036-r1-mut 6fcf64887` — created for the G5 red proofs.
  Outcome: worktree created at detached HEAD `6fcf64887`.
- `git worktree remove --force .remedy-wt/f036-r1-mut` then `git worktree prune` — the G5
  worktree's own cleanup (constraint 6). Outcome: removed; `git worktree list | wc -l` read 62,
  matching the round's step-4 reading.
- `git push -u origin feature/f036-guided-result-tour` — pending, run immediately after this
  commit per the bundle order. Its real outcome is reported in the round's reply (G6), not here,
  because this file is written before the push happens.
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch deletion, no force-push,
  no `git stash` — none of these were run, per constraint 5.

## Verification

**G1 TRANSPORT** — PAYLOADS table readings (before use):
```
claim.diff:  217 lines, 23898 bytes, sha256 4fe060f8…830e8ddc  MATCH
context.md:   37 lines,  1584 bytes, sha256 5449d15b…80dc2567f MATCH
plan.md:      29 lines,  1015 bytes, sha256 641a2a58…dedd11167 MATCH
```
Block self-check: 340 lines, sha256 `eac92ff3…8c910e7f6` — MATCH on both readings.
`.agent/authored/f036-r1-*` copies vs. sources, read back via `git show <commit>:<path>`, all
byte-identical (script exit 0):
```
f036-r1-block.md    vs .remedy-wt/f036-r1/block.md            byte-identical = True
f036-r1-plan.md     vs .remedy-wt/f036-r1-payloads/plan.md    byte-identical = True
f036-r1-context.md  vs .remedy-wt/f036-r1-payloads/context.md byte-identical = True
f036-r1-claim.diff  vs .remedy-wt/f036-r1-payloads/claim.diff byte-identical = True
```

**G2 THE CLAIM** — every file's sha256 at C2 (`git show 202f8ddd0:<path>`) MATCHED the reviewer's
table (all 7 rows: decisions.md, live_review.md, operator_questions.md, STATUS.md, T2_F286.md,
plan.md, context.md — bytes and sha256 both exact). `open_finding_ids` over `.agent/live_review.md`
TEXT read `[]` at both `9dc2f2a7` and `202f8ddd0` (reviewer's claim: empty at both — confirmed).
At C2 the ledger has exactly one `## Findings` line (27) and one `## Steps` line (17); its last
non-empty line begins `Gate: F035 R10 — ` (confirmed verbatim). STATUS.md at C2: line 171 reads
`- [~] F036 — Guided result tour`, line 175 reads `- [ ] F286 — Findings paydown v5` — F036
precedes F286. `git diff --name-only f28f32d2b 202f8ddd0` named exactly the 7 paths of the G2
table, no more, no fewer.

**G3 THE CODE** — `python3 -m ruff check packages/orchestration/result_tour.py
tests/orchestration/test_result_tour.py tests/test_no_orphan_modules.py` at C4 (C4b):
`All checks passed!`, REAL_EXIT=0. `anchor_problem`, `resolve_tour_stops` and the area
grouping/room arithmetic (`_diff_areas`, `_changed_area_stops`, `fallback_tour_stops`'s room
computation) were quoted whole from `git show 89081e1f2` — see the round's reply for the full
text; behaviour matches S4–S6 exactly.

**G4 THE TESTS** — the full 24-target serial selection:
```
887 passed, 1 skipped in 105.80s (0:01:45)
REAL_EXIT=0
```
SKIPPED: `tests/test_agent_tooling.py:43: D12 quarantine (F252)` — the one expected quarantine
skip, unchanged. Node count of `tests/orchestration/test_result_tour.py` by `--collect-only -q`:
13. Reviewer's pre-change reading (selection minus this file, at `9dc2f2a7`): `874 passed, 1
skipped`. 874 + 13 = 887 — no discrepancy. `python3 -m apps.cli.main integrity check --json`:
all six checks `pass`, `fail_count` 0, `ok` true.

**G5 THE RED PROOFS** — `git worktree add --detach .remedy-wt/f036-r1-mut 6fcf64887` then
`python3 -B .agent/authored/f036-r1-mutations.py <worktree>`, whole output:
```
control (before): exit=0 failed=0 nodes=[]
m1  [a node anchor resolves whatever its ref]: RED (caught)
m2  [the resolver keeps every sound stop, with no ceiling]: RED (caught)
m3  [a dropped stop is logged but not listed in dropped]: RED (caught)
m4  [a command anchor resolves when a recorded command merely starts with its ref]: RED (caught)
m5  [the context lists directories of the evidence directory as evidence files]: RED (caught)
m6  [an area is the file's whole directory instead of its first segment]: RED (caught)
m7  [when the areas outnumber the room, every area still gets its own stop]: RED (caught)
m8  [stop (a) anchors to the first task even when report.md exists]: RED (caught)
m9  [an over-long text is not cut]: RED (caught)
m10 [the Definition-of-Done stop counts every check as passed]: RED (caught)
m11 [a title holding a newline is accepted]: RED (caught)
m12 [the run stop uses the LAST recorded command]: RED (caught)
control (after): exit=0 failed=0 nodes=[]
restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
No mutation stayed green; no extra test was needed. `git worktree remove --force
.remedy-wt/f036-r1-mut`, `git worktree prune`, `git worktree list | wc -l` = 62 (matches step 4).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4a | deviated | split from the block's single C4 (constraint 2: combined 589 insertions > 500) |
| C4b | deviated | split from the block's single C4 (constraint 2: combined 589 insertions > 500) |
| C5 | done | this handback |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | every mutation caught first run; no extra test needed |

## Authored-text proofs

`claim.diff` applied via `git apply --check` (exit 0) then `git apply` (exit 0) — never edited,
never retyped. The three payloads (`claim.diff`, `plan.md`, `context.md`) were verified line
count/byte count/sha256 against the PAYLOADS table before use, and the committed
`.agent/authored/f036-r1-*` copies read back byte-identical to their sources via `git show`
(G1, above). `.agent/plan.md` and `.agent/context.md` were REWRITTEN to the payload files by
`shutil.copyfile`, never hand-edited; their post-write sha256 equal the payload table's own
`641a2a58…` and `5449d15b…` rows. C2's resulting file hashes matched the reviewer's G2 table
exactly for all 7 files (see Verification, G2). No reviewer-authored text was applied outside
these four; the module, its tests and the mutation tool are worker-authored against the block's
specification (S1–S7 and the TESTS section), not transcribed from a payload.

## Deviations & assumptions

- **C4 split into C4a and C4b (constraint 2).** The block's C4 bundles "THE TESTS AND THE TOOL"
  as one commit. Staged together, `tests/orchestration/test_result_tour.py` (450 insertions) plus
  `.agent/authored/f036-r1-mutations.py` (139 insertions) total 589 insertions — over the 500-line
  cap. Per constraint 2's own contingency ("split a commit that would reach it into parts with
  their own subjects (C3a and C3b, C4a and C4b), and say so"), this round split C4 into C4a (the
  test file alone, 450 insertions) and C4b (the mutation tool alone, 139 insertions), each under
  the cap. Both commits carry the `F036 R1 C4a` / `F036 R1 C4b` subjects. G5's worktree was cut
  from C4b (the completed C4 payload), matching the block's `<C4>` reference.
- No other deviation. Every mutation in G5 was caught on the first run; no additional test was
  needed. No red gate was hit; nothing under AGENTS.md "If Blocked" applies this round.

## Next

Per the block's `## Next` order: (1) Phase 1 rule 1 — read `.agent/STOP` from disk at session
start. (2) The review of this round (F036 round 1). (3) T002 — the generation call with its
fallback, the no-new-claims goldens, `tour.json` stored and versioned at the job terminal, and
the command line. Open-findings count: 0. Operator-questions count: 1 (Q6).
