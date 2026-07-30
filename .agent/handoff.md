# Handback — amend0730 R1 (docs amendment micro-round)

## Range
`9e1ae3a..HEAD` · feature/docs-discoverability-amend · 5 commits
(state · AGENTS.md · F105 · closure-protocol · handback).
Base = main after the #163 merge. PR open, base `main`, **NOT merged**.
Verdict R1: **PENDING**.

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 Open PR Gate | done | exactly #163, `feature/f050-dag-scheduling`→`main`, non-draft → merged + branch deleted; open PR list then empty |
| 2 branch | done | `feature/docs-discoverability-amend` off main `9e1ae3a` |
| 3 five authored texts | done | all five sha256 matched on first computation, no rejoin needed |
| 4 commit 1 state | done | `b0f93d2`, cmp 0 for both state files |
| 5 commit 2 AGENTS.md | done | `672d76c`, sed hash == r1-1 |
| 6 commit 3 F105 | done | `5ec6980`, sed hash == r1-2 |
| 7 commit 4 closure protocol | done | `b17784d`, FROM hash matched before edit, TO hash == r1-3, old-wording grep 0 |
| 8 round gate | done | docs 292 passed exit 0 · canary 42 passed exit 0 |
| 9 commit 5 handback | done | this commit; OUTCOME executed |
| 10 push + PR | done | PR created, not merged |
| 11 handback | done | this file + completion report |

## Authored-text verification — `sha256sum` output verbatim
    e87772f4c4e28fffac2c329620b496096857d686d4caba2d70a21e1e53ba1bad  .agent/authored/amend0730-r1-1.md
    85bc6b5d6e57a756ac6879ac67b299ade62de821078fdc3e8d2064dd049a76c9  .agent/authored/amend0730-r1-2.md
    933265297b8af85a4560028d0b1340b034adb57e23bade37e2f84c5ad5e78d03  .agent/authored/amend0730-r1-3.md
    d88399ee151c3287235d610568c72547790baca8af46f3429bb0d859d2bb7006  .agent/authored/amend0730-r1-4.md
    c1fb7ed71c26fa112c36b46f1024abb65b019dec1bebc02ffb3d8bcc9ff2a00a  .agent/authored/amend0730-r1-5.md
All five equal their BEGIN-marker hashes. **No transport fault in any
authored bytes** — a first for this relay chain. The block's own
instruction text had cosmetic wraps (the five BEGIN markers' trailing
`-----`, the item-6/7 sed commands, three commit-message lines, the
item-10 `--title`); all unambiguous, recorded rejoined in
`.agent/last_block.md` TRANSPORT NOTES. No authored bytes affected.

## Applied-text proofs (in-file, post-edit)
| Proof | Result |
|---|---|
| `sed -n '/^## 🔎 Code Discoverability Conventions$/,/^-\{72\}$/p' AGENTS.md \| sha256sum` | `e87772f4…1bad` == r1-1 |
| `sed -n '/^- \*\*Operator addition 2026-07-30/,/including Remedy itself\.$/p' T2_F105.md \| sha256sum` | `85bc6b5d…76c9` == r1-2 |
| closure-protocol FROM block, before the edit | `240a60c9…3caf` == expected — the reviewed bytes |
| `sed -n '/^   Build order (wording aligned/,/^   handback, always\.$/p' … \| sha256sum` | `93326529…5e78d03` == r1-3 |
| `grep -c "LAST action after ALL commits" docs/roadmap/STATUS_closure_protocol.md` | `0` |
| `cmp .agent/authored/amend0730-r1-4.md .agent/live_review.md` | exit 0 |
| `cmp .agent/authored/amend0730-r1-5.md .agent/plan.md` | exit 0 |

## Commits
### b0f93d2 chore(amend0730): persist micro-round state + authored texts
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/amend0730-r1-{1..5}.md | +new (31/7/8/41/17) | the five authored sources |
| .agent/live_review.md | rewrite (+73/-73) | FULL REPLACE with r1-4 (cmp 0) |
| .agent/plan.md | rewrite (+31/-31) | FULL REPLACE with r1-5 (cmp 0) |
| .agent/last_block.md | rewrite (+284/-…) | block guard, OUTCOME pending → executed at round end, transport notes |

### 672d76c docs(agents): add Code Discoverability Conventions (operator ruling 2026-07-30)
| Path | +/- | Reason |
|---|---|---|
| AGENTS.md | +32/-0 | r1-1 bytes + one empty line inserted immediately before `## 🧩 Documentation Structure` (now at :550); the authored 72-dash separator keeps the section rhythm |

### 5ec6980 docs(roadmap): F105 — distilled discoverability block for builder/reviewer segments
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F105.md | +8/-0 | r1-2 bytes + one empty line immediately before `## Task slicing` — lands as the last Design bullet (:49–55) |

### b17784d docs(roadmap): closure protocol step 2 — align zip build-order wording (D2)
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS_closure_protocol.md | +8/-5 | the 5-line step-2 build-order block replaced by r1-3's 8 lines; the "LAST action after ALL commits" wording is gone |

### handback commit chore(amend0730): handback R1
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback |
| .agent/last_block.md | +1/-1 | OUTCOME → executed |

## Round gate — raw
    $ python3 -m pytest tests/docs/ -q
    ........................................................................ [ 24%]
    ........................................................................ [ 49%]
    ........................................................................ [ 73%]
    ........................................................................ [ 98%]
    ....                                                                     [100%]
    292 passed in 0.30s
    EXIT=0

    $ python3 -m pytest tests/cli/test_golden_path.py -q
    ..........................................                               [100%]
    42 passed in 21.36s
    EXIT=0

## Deviations
**None.** Every item executed as written; no reconstruction, no skip.

## Observations (not deviations)
1. The docs gate covers none of these three files' content — 292 passed
   both before and after the edits. All three edits are verified by the
   sha256/cmp proofs above, not by a test. Same class as R-0156.
2. Item 6's insert leaves the pre-existing blank line before
   `## Task slicing` in front of the new bullet, so F105's Design list
   renders as a loose list. Cosmetic; the block was followed literally
   (authored bytes + ONE empty line). Say the word and it becomes a
   one-line follow-up.
3. Amendments 1 and 2 of the operator's set are not represented in this
   diff, per the block: 1 was already codified, 2 had nothing to clean.

## Open findings
2 open, both planning-routed: **R-0155** (process, Low) and **R-0156**
(process, Medium). Next free ID: **R-0157**.

## Next expected action
Reviewer R1 verdict on the open PR. On PASS: merge under the standing
same-session operator approval (2026-07-30), then continue per
`docs/roadmap/STATUS.md` Rule A5 — next feature F051 (Escalate instead
of block), fresh window.
