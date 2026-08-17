# Handback - F085 R49 (record + amend)

Feature F085 sandbox hardening, round R49. Branch feature/f085-sandbox-hardening.
Base SHA 1e0c14e0. Head before this commit: ad9a38a8.

## Range

Review of 1e0c14e0..HEAD.

## Commits

### 6f084636 docs(f085): save the R49 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r49.md | +345/-0 | C0a - block saved byte-verbatim |

### 8862abce docs(f085): mirror the R49 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +283/-151 | C0b - identical bytes mirrored |

### d5fb16a5 docs(f085): advance the plan to R49
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +9/-9 | C1 - PLAN3F to PLAN3T, first substantive commit |

### 0131b21b docs(f085): record the R48 PASS and register R-0550 and R-0551
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +94/-0 | C2 - RECORD17 appended |

### 7df0bf33 docs(f085): split the dod policy row into dod-process and dod-app
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F085.md | +8/-5 | C3a - AMEND7F to AMEND7T |

### ad9a38a8 docs(f085): append amendment F085 D7 for the dod policy split
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F085.md | +26/-0 | C3b - DEC7 appended |

### (this commit) docs(f085): rewrite the handback for R49
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | full rewrite | C4 - a handoff cannot table its own commit (R-0149) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3a | done | |
| C3b | done | |
| C4 | done | this commit |

## External actions

`git push -u origin feature/f085-sandbox-hardening` immediately after this commit; result in the
round report. No worktree add/remove, no `gh`, no PR, no merge.

## Verification

G1 STATE, exit 0: `.agent/STOP` read from disk before C0a and again before C4, absent both times;
`git status --porcelain` empty at round start and after each of the six commits;
`git worktree list` one line throughout - no worktree was created, none was ordered.
G2 TRANSPORT, exit 0, disk-to-disk, no digest fallback: `.remedy-wt/f085-r49.md`, the committed
and the working `.agent/authored/f085-r49.md`, and the committed and the working
`.agent/last_block.md` are all five byte-EQUAL. Measured on every copy: sha256
fe04d524d02f044891f9ffb591b5aa83335a07c9ac0471bde02b6b20f13319dc, 24858 B, 345 lines, 12 markers.
G3 SHAPES, measured separately per pair and per path:
- C1 / PLAN3F->PLAN3T / `.agent/plan.md`, REWRITE: `TO contains FROM: false`; PLAN3F 0x and
  PLAN3T exactly 1x in the post-commit file; numstat `9 9`.
- C2 / RECORD17 / `.agent/live_review.md`, PROSE APPEND: pre-commit blob a byte-exact prefix,
  remainder exactly one blank line plus the slice, slice an exact suffix, 0 lines matching
  `^(BEGIN|END)-[A-Z0-9]+$`; 93 slice lines of which 3 empty against 94 added, and every
  non-empty slice line occurs exactly once among that path's added lines; numstat `94 0`.
- C3a / AMEND7F->AMEND7T / `docs/roadmap/features/T2_F085.md`, REWRITE: `TO contains FROM: false`;
  AMEND7F 0x and AMEND7T exactly 1x; numstat `8 5`.
- C3b / DEC7 / same path, PROSE APPEND on the blob C3a left: prefix, remainder of one blank line
  plus the slice, exact suffix, 0 marker LINES; 25 slice lines of which 3 empty against 26 added,
  per-line obligation held; numstat `26 0`.
G4 SUITE, primary checkout, exit 0: the four `.agent/` state readers print `159 passed in 19.95s`
against the ordered base 159. CANARY exit 0: `42 passed in 20.32s` against base 42.
G5 DOCS TIER, exit 0: `295 passed in 0.42s` against base 295. It guards the feature file's
existence and F-id mapping, not its body; G3 is the evidence for the amended text.
G6 PLAN CONTRACT on `.agent/plan.md` after C1: 39 lines against the 50-line cap; `## Goal` true,
`## Next Steps` true, `\bF\d{3}\b` true.
G7 ARITHMETIC. Base 1e0c14e0: 164 registered / 27 done / 0 landed, 137 open, max registered
R-0549, max resolved R-0532, 0 duplicate ids, 0 resolutions naming an unregistered id. HEAD:
166 / 27 / 0, 139 open, 0 duplicates, 0 orphan resolutions. Symmetric differences: registered
exactly {R-0550, R-0551}, done EMPTY, landed EMPTY. Next free id R-0552. Landed is the
line-start form `^Landed:`, 0 at both SHAs; a case-insensitive `^Landed\b` instead matches 12
wrapped PROSE lines at both SHAs, so that difference is empty under either reading.
G8 HYGIENE, measured before C4: `git diff --name-only 1e0c14e0..HEAD` holds exactly
`.agent/authored/f085-r49.md`, `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`
and `docs/roadmap/features/T2_F085.md`, nothing else. Per-commit INSERTIONS before C4: 345, 283,
9, 94, 8, 26 - none over 500, so no second call on the oversize allowance spent at d4473f85. All
six commits are single-parent.
BLOCK SIZE re-measured from the committed `.agent/authored/f085-r49.md`: TOTAL 345, PROSE 180,
RECORD17 93 - all three agree with the block's constraint 9.
No lint gate and no code suite ran: no `.py` file is in the change set, and the block declares
that absence rather than filling it.

## Authored-text proofs

Every slice was extracted PROGRAMMATICALLY from the committed `.agent/authored/f085-r49.md` by
its BEGIN-/END- marker pair and applied byte-verbatim; none retyped, none taken from the prompt.
PLAN3F 723 B / 12 lines, PLAN3T 845 B / 12, AMEND7F 556 B / 10, AMEND7T 841 B / 13, DEC7
1730 B / 25, RECORD17 8168 B / 93. Five-copy disk-to-disk equality under G2; 0 marker lines
reached any target.

## Deviations & assumptions

None to the bundle: C0a, C0b, C1, C2, C3a, C3b, C4 ran exactly as ordered - no extra commit, no
dropped commit, no reordering, no worktree, no PR, no merge, no force-push, no widened change set.
Deviations, declared: this file is 145 lines against the >5-commit allowance of 100, under
DECISION D15 stated-cause overage. The cause is mandated content, not prose: seven per-commit
changed-files tables (5 lines each), the seven-row item-status table, and the G1-G8 verification
transcript whose per-pair shape readings, per-commit insertion counts and G7 id arithmetic are
each individually required. No section was dropped to meet the cap.

Open findings: 139 open, next free id R-0552. This round registered R-0550 and R-0551 and
resolved nothing.

Fortschritt: ~85 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R48 PASS ·
T002a KOMPLETT · T002b KOMPLETT · T002c entsperrt durch Amendment F085 D7, noch nicht gebaut ·
T002d, T003 offen) — Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

## Next

ONE: the next round is R50, started by a FRESH session, and it implements T002c under the policy
DECISION F085 D7 rules - `_run_process_check` onto the guard seam KEEPING its wall timeout and
closing its `env=os.environ.copy()` gap, and `_run_app_once` under the dod-app policy with no
wall timeout and network allowed; T002d, T003, the integration gate and closure follow.
TWO: R49's own verdict is NOT on disk as a gate entry, because the round that records a verdict
cannot record one on itself (docs/agents/planner_reviewer_prompt.md 4.13) - that absence is the
terminator, not a missing gate, and R50 must not open a repair round to close it; R49's verdict,
when the reviewer issues it, is recorded by R50's OWN record slice.
THREE: 139 findings are open and the next free id is R-0552.
FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, because the self-drive protocol
requires every handoff that names the next session's first action to name that rule ahead of the
Open PR Gate.
