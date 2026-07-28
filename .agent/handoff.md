# Handback — PH v3 (relay ergonomics): five process rulings persisted

## Range
Review of `ae08881c592531a1e68d83bd622e92bed4a4bd1b..HEAD` — `chore/process-hardening-v3`, 4 commits, pushed, PR open, NOT merged.

## Commits
### 253dbdb bookkeeping · a5a017f planner · 4cc76dd split_workflow · f615e12 template
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/phv3-r1-1..8.md | +122 | 253dbdb — eight authored texts, sha256-verified |
| .agent/last_block.md | +173 | 253dbdb — new; duplicate-block guard, self-applied |
| .agent/{live_review,plan}.md | +38 −68 | 253dbdb — full replaces r1-7 / r1-8 (cmp 0) |
| docs/agents/planner_reviewer_prompt.md | +35 −0 | a5a017f — r1-1 §2, r1-2 §3 it.5, r1-3 §4 it.11 |
| docs/agents/split_workflow.md | +33 −0 | 4cc76dd — r1-4 fidelity section, r1-5 bootstrap bullet |
| docs/agents/handback_template.md | +4 −0 | f615e12 — r1-6 extends the cap blockquote |
| .agent/{last_block,handoff}.md | this commit | OUTCOME→executed; this handback (R-0149 self-ref) |

## Item status
| Item | Status | Reason |
|---|---|---|
| 1/2 Open PR Gate (#158) + branch | done | merged; main ae08881 = LAST_REVIEWED_SHA |
| 3 Commit A | done | 253dbdb; 8/8 sha256 matched first try |
| 4/5/6 Commits B,C,D | done | a5a017f, 4cc76dd, f615e12; 6 containment proofs |
| 7 verification a–f | done | all green |
| PR into main | done | created, NOT merged — awaits reviewer PASS |

## External actions
`gh pr merge 158 --merge --delete-branch` → merged, main ae08881 · `git pull --ff-only` clean · push per commit · `gh pr create` → PR open, NOT merged.

## Verification
    7a containment exit 0 ×6 (planner ×3, split_workflow ×2, template ×1)
    7b cmp exit 0: live_review←r1-7, plan←r1-8; last_block.md line 1 present
    7c four .agent contract tests → 4 passed · 7d canary → 42 passed
    7e diff main...HEAD → 14 files, exactly the declared set; docs +72/−0
    7f git status --porcelain → empty (before this commit)

## Authored-text proofs
All eight matched their BEGIN markers on the FIRST attempt (no recovery needed): `a308e164… 770a0b7f… 079fb749… 7d64e779… e74d6304… 736f0988… e22f4033… 3ff59e3b…`

## Transport event — three refused emissions before this one
Emissions 1–3 arrived UNFENCED and were refused at the hash gate; nothing ran,
the repo stayed untouched. The relay's markdown renderer stripped `#`/`##` and
leading indentation, normalised blank lines, and rendered `>` as `▎` — r1-6's
own END marker arrived as `▎ --- END phv3-r1-6 ---`, the exact side-border
failure r1-1 forbids. Emission 3 was byte-identical to 2, so I replied with the
SAME-PROMPT banner rather than re-run a deterministic failure. Diagnosis proven:
r1-7/r1-8 reconstructed to their stated hashes by restoring only the stripped
markup, byte-identical to the texts in this fenced emission (cmp 0).

## Deviations & assumptions
- Four blank-line repairs at insertion boundaries so the tight numbered lists and
  the `## 4.`/`## 5.` headings keep their spacing; docs +72/−0, no line removed,
  authored bytes untouched (containment still 0).
- `.agent/last_block.md` stores the block de-indented by 2 — the transform the
  authored texts need to hash; keep the convention stable or future
  byte-comparisons false-positive.
- No AGENTS.md conflict arose. Open findings: 0.

## Next
Reviewer review of PR; PASS → operator-approved same-session merge.
