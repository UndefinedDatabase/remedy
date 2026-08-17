# Handback — F085 (Sandbox Hardening), Round R43

Branch: `feature/f085-sandbox-hardening` · Base SHA: 4c7bcb3a · No PR, no merge.

## Range

Review of 4c7bcb3a..HEAD (5 commits: C0a, C0b, C1, C2, C3).

## Commits

### 5ddea9f5 docs(f085): save the R43 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r43.md | 245/0 | C0a — the R43 block, byte-verbatim from the reviewer's scratch |

### 4da31634 docs(f085): mirror the R43 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 201/288 | C0b — identical bytes mirrored |

### 007f18df docs(review): record the R42 PASS and register R-0537 and R-0538
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 82/0 | C1 — RECORD11 appended (blank line + 81 slice lines) |

### 921e8712 docs(f085): advance the plan to R43
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 6/4 | C2 — PLANF11→PLANT11 and PLANF12→PLANT12, both rewrites |

### (this commit) docs(f085): rewrite the handback for R43
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | — | C3 — this handback; a handoff cannot table its own SHA (R-0149/R-0371) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |

## External actions

`git push -u origin feature/f085-sandbox-hardening` after C3 — outcome in the round report.
No PR, no merge, no worktree add/remove, no `gh` command.

## Verification

G1 STATE — exit 0. `.agent/STOP` absent before C0a and before C3 (`os.path.exists` → False
both times). `git status --porcelain` empty at round start and after each of C0a, C0b, C1, C2
(`''`). `git worktree list` one line throughout: `/home/decodeux/Repos/remedy … [feature/f085-sandbox-hardening]`.

G2 TRANSPORT — exit 0. All FIVE byte-EQUAL: `.remedy-wt/f085-r43.md`, working and committed
`.agent/authored/f085-r43.md`, working and committed `.agent/last_block.md`. sha256
3f7e01574171525480ed8139262c0cf34487b97a355973db2faad6e393a2b426, 17166 B, 245 lines,
10 marker lines. Region 1-100: 708961ae3d989f4e over 6906 B. Region 101-end:
de50ec15e79f8664 over 10260 B. 6906+10260 = 17166. Disk-to-disk, no digest fallback.

G3 APPEND SHAPE — exit 0. Pre-commit blob 426006 B is a byte-exact PREFIX of the 432672 B
post-commit file; the 6666 B remainder is exactly one blank line plus RECORD11 (sha256
2442e139ff6a0836…, 6665 B, 81 lines, 4 empty, 77 non-empty, 0 duplicate non-empty) and the
slice is an exact suffix. 0 marker LINES reached the file (the substring `END-` occurs 13x in
that file's prose, which is why lines were counted). Every one of the 77 non-empty slice
lines occurs exactly once among the 82 added lines; ordered equality added == blank+slice
holds. `git show --numstat` → `82	0	.agent/live_review.md`.

G4 THE PLAN — exit 0. Reconstruction: plan.md at 4c7bcb3a
(7b95158a6cc7b35c60a9ed596d511655ab080dcc7630781caece164588c0836d) with PLANF11→PLANT11 and
PLANF12→PLANT12 gives 5928c3c5dd067836e006685b4666a8cf5f614c80ab6d332cd4c6507e0a550999 —
byte-identical to the committed file at HEAD, same sha256. At HEAD: PLANF11 0x, PLANT11 1x,
PLANF12 0x, PLANT12 1x; `## Goal` and `## Next Steps` both present; 0 marker lines. File
measures 47 lines (`splitlines`) against the 50-line AGENTS.md cap. numstat → `6	4	.agent/plan.md`.

G5 ARITHMETIC — exit 0. Patterns `^- R-\d{4} ` / `^Done: R-\d{4}` / `^Landed: R-\d{4}`.
Base 4c7bcb3a: 151 / 27 / 0, 124 open, max registered R-0536, max resolved R-0532.
HEAD: 153 / 27 / 0, 126 open, max registered R-0538, max resolved R-0532.
Registered symmetric difference exactly {R-0537, R-0538}; done and landed symmetric
differences both empty. 0 duplicate ids, 0 resolutions naming an unregistered id at either
SHA. Next free id moves R-0537 → R-0539.

G6 SUITES — both in the PRIMARY checkout `/home/decodeux/Repos/remedy`, no worktree existed.
`python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q`
→ exit 0, `159 passed in 20.16s` (base 159). No R-0518 red.
CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, `42 passed in 20.40s` (base 42).

G7 HYGIENE — exit 0. `git diff --name-only 4c7bcb3a..HEAD` before C3 holds exactly
`.agent/authored/f085-r43.md`, `.agent/last_block.md`, `.agent/live_review.md`,
`.agent/plan.md` — the change set minus `.agent/handoff.md`, nothing else. Per-commit
insertions before C3: 245, 201, 82, 6 — none over 500 (C3's own count is in the round
report). All four commits single-parent. `git reflog -10` → 10 entries, all of kind
`commit:`.

## Authored-text proofs

Every slice was extracted PROGRAMMATICALLY from the committed
`.agent/authored/f085-r43.md` by its `BEGIN-`/`END-` marker pair; none was retyped and none
was taken from the prompt. RECORD11 (append, no FROM): applied verbatim, exact-suffix proof
in G3. PLANF11→PLANT11 and PLANF12→PLANT12: containment test `TO contains FROM` = false for
both, so both are REWRITES; each FROM measured 1x and each TO 0x in `.agent/plan.md` at
4c7bcb3a, and 0x / 1x at HEAD. Disk-to-disk five-way equality against the reviewer's own
`.remedy-wt/f085-r43.md` in G2.

## Deviations & assumptions

Ordered commit sequence C0a·C0b·C1·C2·C3 was followed exactly — no extra commit, none
dropped, no reordering. No deviation from the block.

DECISION D15 stated cause: this handback runs to 165 lines against the 60-line cap. The
mandated content behind the overage is the five-commit changed-files table, the item-status
table, the G1-G7 verification transcripts with their transport, pair and arithmetic proofs,
the authored-text proof section, and the constraint-8 declarations below. No section was
dropped.

Constraint 8 (STALENESS), declared and NOT repaired (constraint 9 — the registration is the
correction, checklist item 20). Re-read after C2: `.agent/authored/f085-r43.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`. Nothing this round wrote
was falsified by a later commit of the same round: RECORD11's transport, arithmetic and plan
readings are all SHA-anchored to 0e2cdacd / 7b02da1c / dc34997a / 5695c2b0 / 4c7bcb3a, and
each was re-measured and reproduces (R42 five-way equality b6ba3371…f7161c25 / 23195 B / 332
lines / 8 markers / 3bc171fb05e29fa9 over 6720 B / d0ad2b78183925d3 over 16475 B; 149/27/0
and 122 open at 0e2cdacd; plan 46 at 0e2cdacd and 45 at 4c7bcb3a; handoff 153 lines at
4c7bcb3a; insertions 332, 273, 72, 61, 7, 122; RECORD10 and DEC4 append shapes reproduce in
every reported value). Three readings differ from what RECORD11 states:

1. RECORD11 states "the path set at 7c4a2583 is exactly the five ordered paths". Measured:
   `git show --name-only 7c4a2583` is exactly ONE path, `.agent/plan.md`. The five-path set
   belongs to the RANGE `git diff --name-only 0e2cdacd..7c4a2583`, which is what R42's G8
   ordered. Mis-scoped qualifier — the R-0534 / R-0535 / R-0538 shape, inside the RECORD that
   registers R-0538 for that shape.
2. RECORD11 states "lines matching `^## DECISION F085 D\d+ —` number 2 at 0e2cdacd against 3
   at 4c7bcb3a" and names no file. In `.agent/live_review.md`, the file RECORD11 is written
   into and the file its neighbouring paragraphs measure, the count is 0 at BOTH SHAs. The
   reading is true only of `.agent/decisions.md` (2 → 3, D4 exactly 1x, no D1 at either SHA),
   which the sentence never names.
3. R-0537 states the R41 block's "other numerals of that family are the 50-line and 60-line
   caps it quotes as standing rules and the 45 and 69". Measured at 9cc4772c: the block also
   quotes "the 500-line cap" TWICE, by the same construction as the 50- and 60-line caps.
   R-0537's load-bearing conclusion survives (three predictions; none of the others is a
   prediction or is quoted by R-0536), but its enumeration is incomplete — inside a finding
   whose own subject is an incomplete count.

Unverifiable rather than differing: RECORD11's "at 4c7bcb3a `git reflog -10` held ten
entries" is not re-measurable now, the reflog having advanced. The block's "its block
measures 487 lines" describes a text that is not in this repository.

Open findings: 126 (124 + R-0537 + R-0538). Next free id R-0539.

Fortschritt: ~77 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R42 PASS ·
T002a KOMPLETT · T002b 10 von 12 Sites auf dem Seam, `ci_run.py` als DECISION F085 D4 gerulet
und die Migration fertig vermessen, R44 setzt sie um · T002c-d, T003 offen) — Schätzung, gegen
die Klassentabelle aus Amendment F085 D1 gemessen.

## Next

R44. It applies DECISION F085 D4 to `packages/orchestration/ci_run.py`:
`_run_via_subprocess` onto `run_guarded_test_command`, the per-stage budget carried through
the `extra_env` overlay that landed at dce66faa, the captured stdout and stderr re-emitted
before returning, the guard's wall set above `stage.timeout_sec` as a backstop, and five
tests covering the three behavioural deltas. `packages/orchestration/builder_bridge.py`
follows as the last `test`-class site, then T002c-d, then T003 and the integration gate.
R44's first reviewed act is recording R43's gate entry.
