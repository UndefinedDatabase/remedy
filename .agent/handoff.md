# Handback — F115 Prompt breakdown & cost report · Round 19 (repair)

Branch: feature/f115-prompt-cost-report. Open findings: 12 — R-0338 landed,
not resolved; the reviewer authors its `Done:`.
Deviations, declared: this file is 85 lines against the 60-line cap. Cause: the
four mandated per-commit tables (22 lines), the 13-line raw verification
transcript the block ordered, the transport + claim-check proofs, and the gate
(h) deviation record. No section is dropped (AGENTS.md DECISION D15).

Fortschritt: 97 % (T001 ✅ · T002 ✅ · T003 ✅ — Integration-Gate und Closure offen) — Schätzung

## Range

Review of b047aa38..HEAD, 10 commits; the first six (29d9ed44, f80c49bd,
025f27d7, 5c756122, 2e082d24, 07bd70fe) are R18's close-out, tabled at 07bd70fe.

## Commits

### 8411913c chore(f115): save the R19 repair block verbatim
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/authored/f115-r19-1.md | +140/-0 | C0 — block saved verbatim |
| .agent/last_block.md | +113/-323 | C0 — same bytes mirrored |

### e19c68ad docs(f115): name the real owner of the per-role limit note
| Path | +/- | Reason |
| --- | --- | --- |
| docs/guides/cost-report-user-guide-v0.md | +4/-2 | C1 — R-0338 repair |

### fdce0a1b chore(f115): record R-0338 as landed
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/live_review.md | +1/-0 | C2 — worker `Landed:` line only |

### C3, this commit — chore(f115): refresh the plan and write the R19 handoff
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/plan.md | rewrite | C3 — R19 state, 42 lines |
| .agent/handoff.md | rewrite | C3 — this file (self-reference) |

## External actions

`git push -u origin feature/f115-prompt-cost-report` after C3. No PR, no merge,
no gh command, no worktree add/remove.

## Verification

    cmp .agent/authored/f115-r19-1.md .agent/last_block.md  → exit 0
    grep -c "The existing" G                                → 0
    grep -c "remedy stats cost" G                           → 0
    grep -c "remedy stats cache --by role" G                → 1
    grep -c "does not print that limit" G                   → 1
    grep -c "role_limit" G                                  → 1
    wc -l G                                                 → 144
    git show --numstat e19c68ad -- G                        → 4  2  (deviation)
    wc -l .agent/plan.md                                    → 42
    python3 -m pytest tests/docs/ -q                        → 294 passed in 0.31s
    python3 -m pytest tests/cli/test_golden_path.py -q      → 42 passed in 20.42s
    git status --porcelain                                  → ` M scripts/make_review_zip.sh`
    git worktree list                                       → 1 line, /home/decodeux/Repos/remedy

G = docs/guides/cost-report-user-guide-v0.md.

## Authored-text proofs

Block f115-r19-1: `cmp` exit 0, sha256
`dbd9a399c6b5fff416190dc9fd0318f5d967e3c4a2f81f21c2600dbb73794e1e` over both
copies, `wc -lc` 140 8155. C1's TO text applied verbatim.
Claim check before C1: `_ROLE_LIMIT_NOTE` (stats_ledger_cmd.py:373) is printed
by `_render_cache_human:489` under `report.by == "role"` and keyed `role_limit`
by `_cache_payload:436`; both are reached only from `_cmd_stats_cache`,
registered as `stats.cache`. The new sentence is true against source.

## Deviations & assumptions

Gate (h) expected numstat `5 3`; the real value is `4 2`. FROM and TO share
their first line byte-identically, so git keeps it as context: -2/+4. `5 3` is
the FROM/TO line count, not a diff, and forcing it would mean editing that
shared line — which the block's Change clause forbids. Gate (g) 142→144 agrees
with -2/+4, and content gates (b)-(g) all hold: the repair is as ordered.
R-0336 class — a predicted numstat rather than a semantic assertion.

## Next

Reviewer gates R19 and authors `Done: R-0338`; then the integration gate.
