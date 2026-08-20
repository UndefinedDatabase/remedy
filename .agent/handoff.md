# Handoff — F086 Release capability, R5 (record + session close)

Branch: feature/f086-release-capability (continued; no branch created, no PR opened).
Base 655661b0 · HEAD = the C4 commit · Open findings 155 (156 registered, 1 resolved).
Fortschritt: ~3 % (F086 beansprucht · R1-R4 gegated · Paketform entschieden · T001/T002/T003 offen) — Schätzung

## Range

Review of 655661b0..HEAD

## Commits

### 9d23807b chore(state): save the F086 R5 authored block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f086-r5.md | +299/-0 | C0a, `shutil.copyfile` of `.remedy-wt/f086-r5.md` |

### 355dea2c chore(state): mirror the R5 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +189/-192 | C0b, whole-file mirror of the COMMITTED C0a blob |

### 18b2cf89 chore(state): advance the plan to the F086 R5 record and close round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +22/-21 | C1, PLAN5 slice byte-verbatim, whole file |

### ed5d4f11 chore(review): record the F086 R4 verdict in the review ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | C2, RECORD3 appended by pure concatenation |

### C3 (this commit) + C4 — grouped, a handoff cannot table itself (R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C3, this commit, per docs/agents/handback_template.md |
| .agent/handoff.md | append | C4, the reviewer's 44-line VERDICT slice; numstat in the round report |

## External actions

`git push origin feature/f086-release-capability` after C4. No worktree added or
removed (`git worktree list` stayed ONE line). `gh pr list --state open` run READ-ONLY
at the handback: no PR created, edited or merged this round.

## Verification

| Gate | Exit | Result |
|---|---|---|
| G1 | 0 | at C3: `git status --porcelain` EMPTY, `git worktree list` ONE line, `.agent/STOP` absent, branch feature/f086-release-capability; re-taken after C4 in the round report |
| G2 | 0 | scratch, committed authored and committed last_block all byte-EQUAL: sha256 101be7cec956c4fa99009d2c0471c2d1c49e8b4b616fd1b2237d280f6de9e37c, 20909 B, 299 lines |
| G3 | 0 | `.agent/plan.md` byte-equal to extracted PLAN5, sha256 314b31c3…7923, 44 lines (<50), has `## Goal`, `## Next Steps`, `F086` |
| G4 | 0 | 156 registered / 1 resolved / 155 open at BOTH SHAs; registered, resolved and OPEN sets IDENTICAL (symdiff empty); 0 dups, 0 unregistered resolutions, 0 `Landed:` |
| G5a | 0 | REQUIRED: compared 152, equal 152 (paragraph = whole block, never its first line); carried set VERIFIED equal to registered-and-unresolved in the 76661dc1 blob |
| G5b | 0 | NEGATIVE CONTROL at 25f7a5af: compared 152, equal 113 — strictly fewer; the halves DISAGREE, so the check can fail |
| G6 | 0 | RECORD3 present verbatim and as EOF suffix, begins `Gate:`, no `^- R-\d+ — ` match; `Steps` present; marker LINES 0 (substring `<<<` also 0 here) |
| G7 | — | measured after C4 in the round report: a handoff written by C3 cannot measure its own append. Known at C3: VERDICT slice sha256 af46e4af4c91c72773285435dc2988bcf0cc7b3f0e870819b4ee849332c5b1a1, 2576 B, 44 lines, extracted from the COMMITTED authored file |
| G8 | 0 | `160 passed in 19.96s`, four state readers, PRIMARY checkout, serial |
| G9 | 0 | `42 passed in 20.29s`, canary, started only after G8 returned |
| G10 | 0 | at C3: authored/f086-r5.md, last_block.md, live_review.md, plan.md (+ handoff.md with this commit); `pyproject.toml` and every path under `packages/`, `apps/`, `tests/`, `docs/`, `scripts/` ABSENT |
| G11 | 0 | insertions 299, 189, 22, 2 — none over 500, no F104 D1 exemption invoked; C3 and C4 in the round report |
| G12 | 0 | one parent per commit (linear) over C0a-C2; reflog `commit:`/`checkout:` only, re-taken after C4 |
| G13 | 0 | `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`; nothing merged, nothing opened |

## Authored-text proofs

PLAN5, RECORD3 and VERDICT were extracted PROGRAMMATICALLY by their one-line
markers from the COMMITTED `.agent/authored/f086-r5.md` and applied byte-verbatim,
never retyped: G3 the plan equality, G6 the ledger append, G7 the handoff append.
The VERDICT text is the reviewer's; this worker wrote no verdict anywhere.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | this commit |
| C4 | done | appends the VERDICT slice to this file |

## Deviations & assumptions

1. NO departure from the ordered sequence: six commits in block order, none extra,
   dropped or reordered. No code, no test, no `docs/` file, no `pyproject.toml`.
2. D15 OVERAGE, declared: this file will stand at 142 lines after C4 — 98 written
   here plus the reviewer's 44-line VERDICT slice — against the 100-line cap that
   >5 per-commit tables allow. Cause: the round that closes a session carries the
   reviewer's authored session verdict as mandated content (finding R-0571), and no
   section was dropped to meet the cap. Written ONCE; no trim commit follows C4.
3. G1, G7, G11 (C3, C4) and the G12 reflog are stated as measured only where they
   were measurable at C3; their post-C4 readings are in the round report, because a
   file cannot record the commit that appends to it.

## Next

Next session: re-read `.agent/STOP` from disk (Phase 1 rule 1), then run the Open PR
Gate (Phase 1 rule 2). Then R6 — T001 under DECISION F086 D1.

## Reviewer's session verdict — authored by the reviewer, applied by the worker

This section exists because finding R-0571, registered by this feature, is that a
verdict issued and never written to disk cannot be told apart from one never
issued. It is appended rather than written into the sections above so that the
next handback rewrite cannot silently destroy it.

Session of 2026-08-20, self-drive per docs/agents/self_drive_protocol.md. The
reviewer wrote nothing in the work tree; one delegated worker made every commit of
every round; every verdict below rests on gates the reviewer re-executed itself
over the committed diff, never on a handback's summary.

| Round | Range | Verdict |
|---|---|---|
| R1 | 76661dc1..25f7a5af | FAIL — R-0572, R-0573 |
| R2 | 25f7a5af..9e855296 | PASS |
| R3 | 9e855296..0cabd17e | PASS |
| R4 | 0cabd17e..655661b0 | PASS |

R1 claimed F086, reset the review record carrying the F085 open set forward and
registered the two closure candidates as R-0570 and R-0571, emptying
`.agent/candidates.md`. It FAILED on the carry: 39 multi-line finding paragraphs
were truncated to their headlines, 52917 characters of the permanent record lost.
The cause was the reviewer's own block wording — "a finding paragraph is a line
matching `^- R-\d+ — `" defines the paragraph as the line — and the worker applied
it literally and reported honestly. No gate caught it because R1's own transport
gate compared both sides with that same broken extractor; R-0572 carries the loss
and R-0573 the gate defect. R2 restored all 39 paragraphs verbatim from the
pre-reset blob and resolved R-0572, under a check whose negative control is
required to reject the corrupt state. R3 measured the packaging shape by building
a real wheel and established that a wheel built from a pristine checkout carries
ZERO members under `apps/ui/dist/` — Remedy currently packages a CLI whose UI
cannot serve. R4 ruled DECISION F086 D1 and D2 on that measurement.

The open set stands at 155, next free id R-0574. R-0573 remains OPEN: its durable
fix promotes a rule into the pre-emission checklist at
docs/agents/planner_reviewer_prompt.md §3, a file F086 does not own, so it routes
to a paydown branch with R-0403, R-0448, R-0482, R-0487 and R-0490.

By docs/agents/planner_reviewer_prompt.md §4 item 13 the LAST round of a branch
has no on-disk gate entry, so R5's own verdict is the terminator and lives in the
reviewer's closing report rather than here. That absence is the rule, not an
omission — and it is precisely the hole R-0571 exists to close.
