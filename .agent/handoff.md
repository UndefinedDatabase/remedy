# Handback — F085 Sandbox hardening (stage 1), R44

Branch: feature/f085-sandbox-hardening · Base SHA: f3e9687a · Worker: self-drive round R44.

Fortschritt: ~80 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R43 PASS ·
T002a KOMPLETT · T002b 11 von 12 Sites auf dem Seam, `ci_run.py` migriert, nur noch
`builder_bridge.py` offen · T002c-d, T003 offen) — Schätzung, gegen die Klassentabelle aus
Amendment F085 D1 gemessen.

## Range

Review of f3e9687a..HEAD.

## Commits

### d4473f85 docs(f085): save the R44 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r44.md | +516/-0 | C0a — the R44 block saved byte-verbatim |

### a70b8602 docs(f085): mirror the R44 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +454/-183 | C0b — identical bytes mirrored |

### da47ee40 docs(f085): record the R43 PASS and rule DECISION F085 D5
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +56/-0 | C1 — RECORD12 appended |
| .agent/decisions.md | +47/-0 | C1 — DEC5 appended |

### fccd7b04 feat(f085): run CI stages through the stage-1 guard
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ci_run.py | +57/-15 | C2 — CIF1-4 → CIT1-4 |
| tests/orchestration/test_ci_run.py | +55/-0 | C2 — TIMPF → TIMPT plus TESTS |

### 91ad51ae docs(f085): advance the plan to R44
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +10/-13 | C3 — PLANF13/14 → PLANT13/14 |

### C4 (this commit, self-reference exception R-0149)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4 — this handback; its own insertions are in the round report |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | 516 insertions — declared oversize, see Deviations |
| C0b | done | |
| C1  | done | |
| C2  | done | |
| C3  | done | |
| C4  | done | this commit |

## External actions

`git push -u origin feature/f085-sandbox-hardening` after C4. No PR created, nothing merged.
No worktree added or removed — `git worktree list` was one line at every point of the round.

## Verification

G1 STATE — PASS. `.agent/STOP` absent before C0a and again before C4 (`ls` exit 2, "No such
file or directory" both times). `git status --porcelain` empty at round start and after each
of C0a, C0b, C1, C2, C3. `git worktree list` one line throughout.

G2 TRANSPORT — PASS. All FIVE copies byte-EQUAL, disk-to-disk: committed
`.agent/authored/f085-r44.md`, committed `.agent/last_block.md`, both working copies and the
reviewer's `.remedy-wt/f085-r44.md`. sha256
d8bf11c96b39cb7c7d130fd10bbca7d4199e69f00a0ab98c7ab045a31c062be5, 30615 B, 516 lines,
34 marker lines. Region 1-100: 6817 B, sha256 24978de0633a269e…; region 101-end: 23798 B,
sha256 799790952c803f61…; the two regions reassemble to the whole file.

G3 APPEND SHAPE — PASS, measured separately per path.
- `.agent/live_review.md` / RECORD12: pre-commit blob 432672 B is a byte-exact PREFIX of the
  437362 B post-commit file; the 4690 B remainder is exactly one blank line + RECORD12
  (4689 B, 55 lines, sha256 ead2dd2cb45dbcd1…, 2 empty lines, 0 duplicate non-empty lines);
  slice is an exact suffix; 0 marker LINES in the file; each of the 53 non-empty slice lines
  occurs exactly once among the 56 added lines; numstat 56/0.
- `.agent/decisions.md` / DEC5: pre-commit blob 363135 B is a byte-exact PREFIX of the
  366584 B post-commit file; the 3449 B remainder is exactly one blank line + DEC5 (3448 B,
  46 lines, sha256 9f2c72d53d7abe7e…, 6 empty lines, 0 duplicate non-empty lines); slice is
  an exact suffix; 0 marker LINES in the file; each of the 40 non-empty slice lines occurs
  exactly once among the 47 added lines; numstat 47/0.

G4 THE CODE — PASS on every clause except one that is unmeetable as worded (below).
- `packages/orchestration/ci_run.py`: base f3e9687a sha256 bf26df59aa3249bf…; applying
  CIF1→CIT1, CIF2→CIT2, CIF3→CIT3, CIF4→CIT4 in that order gives sha256 01266d9d728b6f51…,
  byte-identical to the committed file. At HEAD: CIF1 0x / CIT1 1x, CIF4 0x / CIT4 1x
  (the two REWRITE pairs); CIT2 1x and CIT3 1x (the two APPEND pairs); 0 marker lines.
  numstat 57/15.
- `tests/orchestration/test_ci_run.py`: base sha256 656f0cf62dd86bc5…; TIMPF→TIMPT plus the
  TESTS append gives sha256 78952570ca542867…, byte-identical to the committed file. At HEAD
  TIMPF 0x, TIMPT 1x, 0 marker lines. numstat 55/0. ORDERED EQUALITY: TESTS is an exact
  SUFFIX (2111 B) — TRUE; the 55 lines C2 adds to that path are exactly the 4 lines TIMPT
  adds plus the 51 lines of TESTS, in order — TRUE. The clause "the pre-commit blob is a
  byte-exact PREFIX of the post-commit file" is FALSE as worded (measured) and cannot be
  true: C2 rewrites the import block of the same file, so the pre-commit blob (4089 B,
  identical to the base blob) is not a prefix of it. The meetable form was measured instead
  and holds: the base blob with TIMPF→TIMPT applied (4206 B) IS a byte-exact prefix of the
  6317 B post-commit file, and the remainder is exactly TESTS. Reported, not repaired.

G5 LINT — PASS, exit 0. `python3 -m ruff check packages/orchestration/ci_run.py
tests/orchestration/test_ci_run.py` → `All checks passed!`, run in the primary checkout.
Both paths resolve at f3e9687a via `git ls-tree` (blobs cb2fba07, 377bc2b8).

G6 SUITES — PASS, each in the PRIMARY checkout, each exit 0.
- the seven-file command with `-rf -q` → `190 passed in 21.79s` (base reading 186; the
  four new tests are the delta). No `TestVitestFrontendTestFoundation` red.
- `python3 -m pytest tests/orchestration/test_ci_run.py --collect-only -q` → `14 tests
  collected`. Each of the four names TESTS defines is collected exactly once:
  `test_the_guard_wall_sits_above_the_stage_budget`,
  `test_a_stages_captured_output_is_re_emitted_to_the_console`,
  `test_a_wall_trip_comes_back_as_the_timeout_exit_code`,
  `test_a_secret_like_parent_variable_does_not_reach_the_stage_child`.
- CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` → `42 passed in 22.25s`
  against a base reading of 42.

G7 THE PLAN — PASS. `.agent/plan.md` base f3e9687a sha256 5928c3c5dd067836…; applying
PLANF13→PLANT13 and PLANF14→PLANT14 gives 06ffae3297341860…, byte-identical to the committed
file at 91ad51ae. At HEAD PLANF13 0x, PLANT13 1x, PLANF14 0x, PLANT14 1x; `## Goal` and
`## Next Steps` both present; 0 marker lines; 44 lines against the 50-line AGENTS.md cap;
numstat 10/13.

G8 ARITHMETIC — PASS. Registered / done / landed from the line-start patterns
`^- R-\d{4} —`, `^Done: R-\d{4}` and `^Landed: R-\d{4}`: 153 / 27 / 0 at f3e9687a and
153 / 27 / 0 at HEAD, 126 open at both, max registered R-0538, max resolved R-0532 at both.
All three symmetric differences EMPTY. Duplicate ids 0 and resolutions naming an unregistered
id 0, at both SHAs. Next free id stays R-0539.

G9 HYGIENE — one clause FAILS, measured before C4. `git diff --name-only f3e9687a..HEAD`
holds exactly the seven paths of the change set minus `.agent/handoff.md` and nothing else.
Every commit has exactly one parent. `git reflog -10` holds ten entries, none of a
non-`commit:` kind. Per-commit insertions before C4: d4473f85 516, a70b8602 454, da47ee40
103, fccd7b04 112, 91ad51ae 10. C0a's 516 EXCEEDS 500 — the clause "confirm none exceeds
500" is therefore RED and is reported as red, not as green. See Deviations.

Round report, ordered by constraint 10 (measured from the committed
`.agent/authored/f085-r44.md`, not taken from the block): the R44 block is 516 lines TOTAL,
of which 277 lines are slice content inside the 17 marker pairs, giving 239 lines of PROSE
counting the 34 marker lines as prose — 239 against the 400-line cap DEC5 rules on.
C4's own insertions cannot be measured by C4; the round report names them to the reviewer.

## Authored-text proofs

Every slice was extracted PROGRAMMATICALLY from the committed `.agent/authored/f085-r44.md`
by its BEGIN-/END- marker pair (helper under the gitignored `.remedy-wt/`, nothing from it
committed). 17 slices extracted; none retyped, none hand-edited. Disk-to-disk equality
against the reviewer's own `.remedy-wt/f085-r44.md` is G2 above — five copies, no digest
fallback. Reconstruction proofs for the three edited targets are G4 and G7; both append
proofs are G3 and G4.

## Deviations & assumptions

1. OVERSIZE COMMIT, DECLARED. C0a (d4473f85) carries 516 insertions against the AGENTS.md
   500 cap, so G9's "none exceeds 500" is red. Inseparability reason: the commit is the
   verbatim save of ONE `.agent/**` artifact whose bytes constraint 1 makes load-bearing —
   every slice this round applied was extracted from that committed file — and splitting it
   would put a truncated block on disk at an intermediate commit. DECISION F105 D5 rules
   that `.agent/authored/<round>.md` counts NORMALLY (only `last_block.md` is exempt), so
   the exemption is not claimed; the AGENTS.md declared-exception route is used instead.
   Clause (b) verified mechanically: no commit on this branch exceeded 500 before this one
   (262 commits, previous maximum 400 at a1726eb7), so this is the only such commit in F085
   and the allowance is now spent. THE CAUSE IS THE BLOCK, NOT THE WORK: DEC5 lifts the
   400-line cap off slices while leaving "a commit under 500 insertions" standing, and a
   516-line block cannot be saved under 500 in one commit. R45 owes a rule reconciling the
   two, or a 500-aware block budget.
2. DEC5 CONTRADICTS THE BLOCK IT DESCRIBES. DEC5, landed at C1, says "The R44 block is the
   first measured under this counting and declares both of its numbers in its own
   constraints." Constraint 10 declines to state them — "the worker measures them from the
   committed `.agent/authored/f085-r44.md` rather than taking them from here" — and neither
   239 nor 516 appears anywhere in the block's prose (measured). The numbers are in the
   round report above instead. Applied byte-verbatim as ordered; not repaired.
3. PLANT13 OVERCOUNTS THE TESTS. `.agent/plan.md` now says R44 applies DECISION F085 D4
   "with five tests". C2 adds FOUR: `def test_` count in
   `tests/orchestration/test_ci_run.py` goes 10 → 14. The block's own goal line says "four
   tests". Applied byte-verbatim; not repaired.
4. CONSTRAINT 2's BASE READING IS WRONG FOR ONE PAIR. Constraint 2 asserts "each TO 0x
   there" at f3e9687a. CIT1 reads 1x at f3e9687a, not 0x, because CIF1 CONTAINS CIT1 —
   `import subprocess` is the line CIF1 keeps. The reading is structurally impossible for a
   deletion-shaped rewrite. Every FROM did read exactly 1x, so no application was ambiguous.
5. G4's PREFIX clause is unmeetable as worded for `tests/orchestration/test_ci_run.py` —
   measured false, with the meetable form measured true. Detail under G4.

No worktree was created. No slice was edited to make a gate green. Nothing outside the
declared change set was touched. The round registers and resolves nothing: open findings
126, next free id R-0539.

## Deviations, declared (DECISION D15)

This handback is 204 lines, over the 60-line cap. Stated cause: the mandated content does
not fit — the per-commit changed-files tables for six commits, the item-status table, the
authored-text proofs, and the nine gate transcripts G1-G9 with their sha256 pairs,
reconstruction results and real numbers. No section was dropped to meet the cap.

## Next

The next round is R45. R45 registers the three findings RECORD12 states as owed, migrates
`packages/orchestration/builder_bridge.py` — the last `test`-class site on a bare spawn —
and makes the two checklist promotions RECORD12 names. T002c-d, T003, the integration gate
and closure follow. R45's first reviewed act is recording R44's gate entry.
