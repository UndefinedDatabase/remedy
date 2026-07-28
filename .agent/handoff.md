# Handback — Planning amendment: flake-debt reorder + F070/F075 corpus (R1)

## Range
Review of `73ac5cc15b60900cd4030968f9a32fd2ee311abf..HEAD` — branch
`chore/plan-amendment-flake-debt`, PR **#157**, NOT merged.
73ac5cc = main head at branch creation = LAST_REVIEWED_SHA.

## Commits
### 2f32853 chore(plan): amendment round bookkeeping — authored texts, live-review reset
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/pamend-r1-1..8.md | +124 (8 files) | operator texts saved verbatim, sha256-verified before use |
| .agent/live_review.md | +6 −46 | full replace from r1-1 (round reset) |
| .agent/plan.md | +24 −53 | full replace from r1-8 |

### 916a29f docs(roadmap): register F251 full-suite stabilization
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T1_F251.md | +45 | new file, full copy of r1-2 |

### 20298f9 docs(roadmap): F251 ordered before F050 in STATUS and ROADMAP tier 1
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | +1 | r1-3 line after the F048 `[x]` line, before F050 |
| docs/roadmap/ROADMAP.md | +8 | r1-4 paragraph after F048, before F050 (7 lines + blank) |

### 82b490b docs(f070): ledger-fixture corpus + integrity-pattern note
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T1_F070.md | +21 | r1-5 at end of Design, r1-6 at end of Acceptance |

### 63e76bb docs(f075): gauntlet inherits era-fixture classes
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T1_F075.md | +5 | r1-7 at end of Acceptance |

### handoff commit (self-reference, R-0149 grouped table)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback; cannot table its own commit |

## Item status
| Item | Status | Reason |
|---|---|---|
| Commit A | done | |
| Commit B | done | |
| Commit C | done | |
| Commit D | done | |
| Commit E | done | |

## External actions
- `gh pr list --state open …` → exactly `#156 feature/f048-job-queue → main, isDraft false`; gate passed.
- `gh pr merge 156 --merge --delete-branch` → merged, 91 files, `40c7e4d..73ac5cc`.
- `git checkout main && git pull --ff-only` → up to date at 73ac5cc, worktree clean.
- `git push -u origin chore/plan-amendment-flake-debt` → `* [new branch]`, tracking set.
- `gh pr create …` → https://github.com/UndefinedDatabase/remedy/pull/157 — open, NOT merged.

## Verification
    4a cmp → exit 0: live_review.md/r1-1 · T1_F251.md/r1-2 · plan.md/r1-8
    4b containment → exit 0: r1-3→STATUS.md · r1-4→ROADMAP.md · r1-5→T1_F070.md
                             r1-6→T1_F070.md · r1-7→T1_F075.md
    4c git diff main...HEAD --stat → 15 files, 234 insertions(+), 99 deletions(-);
       only .agent/authored/pamend-r1-*, .agent/{live_review,plan}.md,
       docs/roadmap/{STATUS,ROADMAP}.md, docs/roadmap/features/{T1_F070,T1_F075,T1_F251}.md
    4d git diff main...HEAD --numstat -- docs/roadmap/STATUS.md → "1  0"
    4e python3 -m pytest tests/cli/test_golden_path.py -q → exit 0, "42 passed in 14.63s"
    4f git status --porcelain → (empty), before the handoff commit

## Authored-text proofs
All eight `sha256sum .agent/authored/pamend-r1-<n>.md` matched the BEGIN
markers byte-for-byte BEFORE the first commit: r1-1 `6b3f006c…`, r1-2
`62925f29…`, r1-3 `44c2463d…`, r1-4 `1e2baad2…`, r1-5 `541f1c0d…`, r1-6
`0d443cb7…`, r1-7 `cbc235cb…`, r1-8 `58a3ad7b…`. Applied texts re-proven
disk-to-disk under 4a/4b.

## Deviations & assumptions
- Branch is `chore/plan-amendment-flake-debt` per the operator step text.
  AGENTS.md requires `feature/*`, and its Open PR Gate stops on a
  non-`feature/*` PR — the next gate run will halt on #157. Followed as
  written, flagged here and in the PR body; not silently altered.
- `docs/roadmap/ROADMAP.md` is normally agent-off-limits; this single Tier-1
  ordering entry is operator-authorized.
- `.agent/plan.md` is byte-identical to r1-8 as ordered, so its checkboxes stay
  unticked although A–E are done; the item-status table above is authoritative.
- `docs/README.md` untouched: `docs/roadmap/features/` files are not indexed
  there individually, and it is outside the declared change set.
- Findings this round: 0. Next free finding ID: R-0150.

## Next
Window 1 reviews `73ac5cc..HEAD` on PR #157 (docs only); merge is the
operator's call.
