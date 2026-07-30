# Handback — f052-r3 (Window 2 → Window 1)

## Range
Review of d410ce5..HEAD (`feature/f052-self-healing-rounds`, pushed, no PR, nothing merged). Closure remains its own round.

## Commits

### 3779bf6 chore(f052): persist R2 verdict (integration gate PASS) + register R-0158/R-0159
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +38/-8 | R2 Steps bullet := r3-1; `- Next free ID: R-0158.` := r3-2 (registers R-0158 + R-0159, next free R-0160); r3-3 appended to `## Verdicts` after the R1 PASS entry |
| .agent/authored/f052-r3-{1..5}.md | +61 | 5 authored texts, hashes verified before use |
| .agent/last_block.md | +212/-102 | R3 block, OUTCOME pending |

### f9dadc0 docs(agents): integration gate — parity path correction + .git-dir class (R-0158)
| Path | +/- | Reason |
|------|-----|--------|
| docs/agents/integration_gate.md | +16/-12 | the 13-line R-0155 paragraph in step 3 replaced by r3-4 (17 lines): parity targets are `apps/ui/node_modules` + `apps/ui/dist`, ROOT `node_modules` named as a `.vite` cache only, non-restorable `.git`-directory class folded into the attribution rule |

### fc9d71c chore(f052): resolve R-0158 in the ledger
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +6/-8 | `- Open: R-0158 …` bullet replaced by the substituted r3-5 resolution; R-0159 left Open |

### \<handback\> chore(f052): handback R3
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewrite | this file (R-0149 self-reference) |
| .agent/last_block.md | 1 line | OUTCOME pending → executed |

## External actions
`git push` after each commit (d410ce5→3779bf6→f9dadc0→fc9d71c). No PR created, nothing merged, no worktrees this round.

## Verification
`python3 -m pytest tests/docs/ -q` → `293 passed in 0.26s`, exit 0.
`python3 -m pytest tests/cli/test_golden_path.py -q` → `42 passed in 19.03s`, exit 0.
Clean tree at gate time (`git status --porcelain` empty).

## Authored-text proofs
`sha256sum .agent/authored/f052-r3-*.md` — all five matched the BEGIN-marker hashes on FIRST computation (no transport fault, no rejoin):
```
6895916ba53c8eea285e38c7abbc33f1147df6357d11e03f4ceeb06c7acf39d5  .agent/authored/f052-r3-1.md
8140e4314ef5c606fe9e5ae557a32337bb6b84e11ffa11f570c623437f3b668f  .agent/authored/f052-r3-2.md
a48b560a7cac4429738b1114f77506042df829cc1afa307fca4cad21c7d4c8d4  .agent/authored/f052-r3-3.md
0b4fe00e52a49baa5f770b5730e9cd5315210c74800c3019cc5120f79e3be661  .agent/authored/f052-r3-4.md
04d8fd85e39a33cda1f5de64521eeb7451b906e527f77e197c9c97b3cfdd799e  .agent/authored/f052-r3-5.md
```
- `cmp` of each applied region against its authored file → **0** for all three live_review regions (Steps, Findings/registrations, Verdicts) and for the substituted R-0158 resolution.
- Occurrence counts after applying: r3-1/r3-2/r3-3 each 1×; old R2 "In progress." bullet 0; old `- Next free ID: R-0158.` 0; `- Open: R-0158` 0; `- Open: R-0159` still 1 (deliberately Open).
- R-0158 fix grep proofs: `path corrected per R-0158` 0→1; `` the ROOT `node_modules`, `apps/ui/dist` `` 1→0. r3-4 occurs exactly 1× in `integration_gate.md`; paragraph bounds asserted before replacement (first line matched, last line ended `gate verdict.`).
- Placeholder proof: `<SHA_R0158>` in the COPY 1→0, substituted with `f9dadc0`; the original `.agent/authored/f052-r3-5.md` hash is unchanged (`04d8fd85…`).

## Deviations & assumptions
None. Every step ran as the block specified; R-0159 is left Open as the documented Low risk, and closure was not touched.

Item status: | 1 persist verdict + registrations done | 2 R-0158 fix done (SHA_R0158 = f9dadc0) | 3 resolution done | 4 gates + handback done | no skips.

## Next
Reviewer verdict on f052-r3, then the F052 closure round (its own round). Open findings: 1 (R-0159, process, Low, documented). Next free ID: R-0160.
