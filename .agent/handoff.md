# Handoff — Process-Hardening v1 (chore round, no feature)

Branch `chore/process-hardening-v1` · open findings 0 · PR created, NOT merged.

## Range

Review of `89c4ef0..HEAD` (8 commits). Note: every commit below also touches
`.agent/plan.md` (+4 −2, Commit Gate) unless its table says otherwise.

## Commits

### 5fc83e9 chore(ph1): persist reviewer-authored texts for process-hardening round
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/phv1-r1-{1..10}.md | +133 −0 | 10 files, verbatim paste texts |
| .agent/plan.md | +44 −17 | round plan rewritten |

### 681d430 docs(agents): add mandatory handback template
| Path | +/- | Reason |
|---|---|---|
| docs/agents/handback_template.md | +50 −0 | C1 — cp of phv1-r1-1 |

### c95876d docs(agents): add canonical integration-gate procedure
| Path | +/- | Reason |
|---|---|---|
| docs/agents/integration_gate.md | +25 −0 | C5 — cp of phv1-r1-2 |

### 1aecc51 docs(agents): wire fidelity protocol and handback template into split workflow
| Path | +/- | Reason |
|---|---|---|
| docs/agents/split_workflow.md | +25 −0 | C2 — phv1-r1-3 + phv1-r1-4 |

### 74bd4f8 docs(agents): reviewer worktree hygiene, gate reference, flake-debt brief item
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +23 −3 | C3+C6 — phv1-r1-5/6/7 |

### 7aadea4 docs: bounded waiver rule for oversize commits in AGENTS.md
| Path | +/- | Reason |
|---|---|---|
| AGENTS.md | +6 −0 | C4 — phv1-r1-8 |

### 03438de docs: register handback template and integration gate in index
| Path | +/- | Reason |
|---|---|---|
| docs/README.md | +5 −0 | IDX — phv1-r1-9 + phv1-r1-10 |

### HEAD chore(ph1): handback — handoff per the new template
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback |
| .agent/plan.md | +2 −2 | round complete |

## External actions

| # | command | outcome |
|---|---|---|
| 1 | `gh pr list --state open …` | PR #153 open (F047) — NOTED, untouched per D1 |
| 2 | `git push -u origin chore/process-hardening-v1` | new remote branch |
| 3 | `git push` (handback) | HEAD pushed |
| 4 | `gh pr create` | PR #154 into main; NOT merged (D3) |

## Verification

```
$ python3 - <<'PY'  (Part-3 proof script)
OK ×10 (2 full-file byte compares, 8 substring compares)
PROOFS: PASS
EXIT=0
$ python3 -m pytest tests/cli/test_golden_path.py -q
..........................................          [100%]
42 passed in 14.71s
EXIT=0
$ git status --porcelain     # empty
```
Docs lint: none found — no markdownlint/remark/vale config and no
`.github/workflows/` in this repo.

## Authored-text proofs

All ten texts were saved to `.agent/authored/` in commit 5fc83e9 BEFORE any
application, then applied by copying from those files. Proof = the Part-3
script above: `read_bytes()` equality for the two full files, `snippet in
target` for the eight inserts. No retype anywhere. 10/10 OK, exit 0.

## Deviations & assumptions

- D1/D2/D3 applied verbatim (operator process-hardening directive
  2026-07-27): PR #153 untouched; branch is `chore/*`; PR unmerged.
- A1 (assumption): the paste block is uniformly indented by 2 spaces; that
  frame was stripped so files start at column 0. Relative indent inside
  each text preserved.
- REPORT ITEM 1 — suspected authored-text error, NOT fixed per the no-fix
  rule: phv1-r1-10's second table row is hard-wrapped after "by paste",
  so `blocks) |` lands on its own line and breaks that markdown table row
  in docs/README.md. Applied verbatim; proof passes; needs an authored
  one-line replacement to render.
- REPORT ITEM 2 — this file is 106 lines, over the AGENTS.md ≤60 cap. With
  8 commits, one table per commit costs ~45 lines, so the new template's
  "all sections, in order" and the 60-line cap collide on any round with
  more than ~5 commits. Transcripts are already trimmed to command + exit
  code and no section was dropped. Needs an authored ruling.

## Next

Window 1 reviews `89c4ef0..HEAD`; on PASS the operator merges the PR.
