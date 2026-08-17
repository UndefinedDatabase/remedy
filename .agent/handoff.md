# Handback — F085 Sandbox hardening, R39

Branch `feature/f085-sandbox-hardening`, base SHA cbcb5c23.
Deviations, declared (DECISION D15): this file is 185 lines. Cause is mandated content — six
per-commit tables, the item-status table, the G1-G7 transcripts, the per-pair authored-text
proofs, the constraint-8 measurements and two verbatim blocks. No section dropped.

## Range

Review of cbcb5c23..HEAD (6 commits).

## Commits

### eba5de68 docs(f085): save the R39 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f085-r39.md | +349/-0 | C0a — the block, byte-for-byte |

### 757be21c docs(f085): mirror the R39 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +295/-230 | C0b — same bytes as C0a |

### 607050ba docs(review): record the R38 PASS and register R-0530
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +50/-0 | C1 — RECORD7 appended |

### dce66faa feat(f085): add an extra_env overlay to the test-class exec seam
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/exec_guard.py | +17/-3 | C2 — SEAMA→B, C→D, E→F, G→H |
| tests/orchestration/test_exec_guard.py | +49/-0 | C2 — SEAMTESTS appended |

### f31802f0 docs(f085): advance the plan to R39
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +3/-3 | C3 — PLANF7→PLANT7 |

### (this commit) docs(f085): rewrite the handback for R39
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C4 — a handback cannot table itself |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |

## External actions

`git fetch origin main` — ok. `git worktree add --detach .remedy-wt/base-main origin/main`, used
for the ordered origin/main ruff run, then `git worktree remove` + `git worktree prune`;
`git worktree list` is one line. `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

## Verification

G1 STATE — pass. `.agent/STOP` absent before C0a and again before C4 (`ls` exit 2 both times);
`git status --porcelain` empty at round start and after each of the five commits; `git worktree
list` one line at the handback.

G2 TRANSPORT — pass, disk-to-disk, no digest fallback. Reviewer `.remedy-wt/f085-r39.md`, both
working copies and both committed blobs are five-way byte-EQUAL: sha256
32415af6db43f9228459a2bb05241c35c0a39073ab4ffb638d01758448f1181a, 19352 B, 349 lines, 24 marker
lines. Regions measured, not computed, trailing newlines included: 1-100 6673 B 84af37ab3ad18bcf…;
101-200 5284 B e8ae19eb0bb28eb3…; 201-300 4155 B d78747c143a2305d…; 301-end 3240 B 64aa4ed98c296d61….

G3 APPEND SHAPE — pass. Pre-commit blob 402603 B is a byte-exact PREFIX of the 406554 B post-commit
file; remainder 3951 B == one blank line + RECORD7 exactly; RECORD7 an exact suffix; its first line
occurs 1x among the commit's 50 added lines; 0 LINES match `^(BEGIN|END)-[A-Z0-9]+$`. numstat 50/0.

G4 ARITHMETIC — pass, matching every expected reading. Base cbcb5c23 144 / 24 / 0, 120 open, max
registered R-0529, max resolved R-0527; HEAD 145 / 24 / 0, 121 open, max registered R-0530, max
resolved R-0527. Registered symmetric difference exactly `['R-0530']`; done and landed symmetric
differences empty; 0 duplicate ids; 0 resolutions naming an unregistered id; maximum id R-0530;
next free id R-0530 → R-0531.

G5 THE SEAM — pass on every ordered reading but one, which is unattainable (Deviation 1). In
`exec_guard.py` at HEAD each of the four FROMs occurs 0x and each of the four TOs 1x. Floor
untouched: `    keep = set(allowlist) - FORBIDDEN_ENV_KEYS` 1x at base and 1x at HEAD; `def
scrub_child_env` through its `return` byte-identical base vs HEAD, 540 B each. 0 marker lines
reached either file. C2 numstat 17/3 and 49/0. SEAMTESTS, what holds: added lines == `['','']` +
SEAMTESTS's 47 lines in order; pre 21388 B a byte-exact prefix of post 23271 B; remainder == two
blank lines + SEAMTESTS; slice an exact suffix. After C3: PLANF7 0x, PLANT7 1x, `.agent/plan.md`
45 lines against the 50-line cap.

G6 SUITES — every command in the PRIMARY checkout, each exit 0 except the origin/main ruff
sub-order (Deviation 2):
- `python3 -m pytest tests/orchestration/test_exec_guard.py -q` → 0, `27 passed in 13.22s` (base 24).
- `python3 -m pytest tests/orchestration/test_mission_state.py tests/orchestration/test_job_promote.py
  tests/orchestration/test_pingpong.py tests/orchestration/test_pingpong_promote.py -q` → 0,
  `262 passed in 9.98s`, equal to base.
- `python3 -m pytest tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
  tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` → 0,
  `159 passed in 20.55s`. No R-0518 red.
- `python3 -m ruff check packages/orchestration/exec_guard.py tests/orchestration/test_exec_guard.py`
  → 0, `All checks passed!`. Same command at origin/main → exit 1, Deviation 2.
- CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` → 0, `42 passed in 22.27s`.

G7 HYGIENE — pass. `git diff --name-only cbcb5c23..HEAD` before C4 is exactly the declared change
set minus `.agent/handoff.md`, nothing else. Insertions before C4: 349, 295, 50, 66, 6 — none over
500; C4's own insertions are in the round report, since C4 cannot measure itself. Every commit has
exactly one parent; `git reflog -10` holds only `commit:` entries.

## Authored-text proofs

Every slice extracted PROGRAMMATICALLY from the committed `.agent/authored/f085-r39.md` by its
marker pair, never retyped; five-way disk equality is G2.
- SEAMA→SEAMB, SEAMC→SEAMD, SEAME→SEAMF, SEAMG→SEAMH and PLANF7→PLANT7 — REWRITE, the shape
  constraint 2 assigns: `TO contains FROM: false` measured for each, each FROM 1x in its target
  before and 0x after, each TO 1x after (counts in G5).
- RECORD7 — APPEND, no FROM and no FROM-zero count reported. §4.9 met: first line 1x among the
  added lines, plus G3's prefix / remainder / suffix proofs.
- SEAMTESTS — APPEND, no FROM and no FROM-zero count reported. §4.9 AS ORDERED is unattainable
  (Deviation 1); the proofs that do hold are in G5.

## Deviations & assumptions

Commit sequence: NO departure. C0a, C0b, C1, C2, C3, C4 in the block's order — nothing extra,
dropped or reordered.

1. G5's SEAMTESTS per-line obligation is unmeetable by construction; nothing was edited, this is
declared instead. Ordered: "every line SEAMTESTS contains occurs exactly once AMONG THE LINES C2'S
DIFF ADDS". Measured: 19 of SEAMTESTS's 47 lines fail it, because the slice repeats lines
internally — `''` 12x, `    )` 4x, `        _child(_ENV_DUMP), timeout_sec=30, cwd=None,` 3x,
`@pytest.mark.subprocess` 2x. §4.9 scopes that count to TO-ONLY additions and bends for
legitimately repeated PROSE; a CODE slice repeats lines structurally, so no correct application of
this slice could satisfy the count as written.

2. The ordered `ruff` run at origin/main exits 1, not 0. `python3 -m ruff check
packages/orchestration/exec_guard.py tests/orchestration/test_exec_guard.py` in a detached worktree
at origin/main (a5a70621): exit 1, `E902 No such file or directory (os error 2)` for each of the
two paths, `Found 2 errors.` Cause measured: NEITHER path exists at origin/main — `git ls-tree
origin/main` over both paths is empty, and `exec_guard.py` was ADDED on this branch at e0d4d880.
The reading the sub-order wanted survives, more strongly: zero pre-existing ruff errors on those
paths at main because the paths are not there, so HEAD's `All checks passed!` is entirely this
branch's. Two defects in one bullet — ordered without being executed at its own base (R-0364), and
G6's preamble orders every command "in the PRIMARY checkout and never in a worktree" while an
origin/main run of it requires one. The HEAD ruff gate is exit 0; no repair was improvised.

3. Observation only, text this round did NOT write, not repaired (constraint 9): `.agent/plan.md`
Next Steps 1 says "R38's `extra_env` overlay unblocks both". The overlay CODE landed this round at
dce66faa; R38's 275a294e landed DECISION F085 D3 alone. No slice touches that paragraph.

Constraint 8, staleness — re-read all six files this round wrote; the measurements:
- RECORD7's R-0530 paragraph quantifies over a CLOSED set of SHAs, so C0b cannot falsify it.
  Measured: sha256 of `.agent/last_block.md` is 208ad9d3… at 483975b3, c8efc5c0… at 857ca31a AND
  c3201976, 5fa4d096… at b9d5050b AND cbcb5c23 — exactly what the paragraph states — and
  32415af6… at 757be21c, a commit the paragraph does not reach.
- RECORD7 quotes the R-0528 clause; that clause occurs 1x in `.agent/live_review.md` at 3b915e3c,
  the commit RECORD7 names (matched over flattened whitespace — it is line-wrapped on disk).
- SEAMD's "Both `test`-class call sites still on a bare spawn overlay one variable onto a copy of
  `os.environ`" measured TRUE: `ci_run.py:78` and `builder_bridge.py:219` are the two, no third.
- PLANT7's "No call site is migrated" measured TRUE: the cbcb5c23..HEAD path set holds no call site.
- Borderline, NOT registered: RECORD7's trailing "next free R-0530" carries no SHA of its own,
  though the sentence's other readings are anchored at c3201976 and cbcb5c23; C1 registers R-0530
  in the very commit that lands the clause, so a reader dropping the anchor reads it false at HEAD.

Open findings: 121 (was 120 — R-0530 registered, nothing resolved). Next free id R-0531.

Fortschritt: ~76 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R38
PASS · T002a KOMPLETT · T002b 10 von 12 Sites auf dem Seam, die letzten 2 ab R40
migrierbar · T002c-d, T003 offen) — Schätzung, gegen die Klassentabelle aus Amendment
F085 D1 gemessen.

## Next

The next session's FIRST action is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2,
the Open PR Gate (`gh pr list --state open --json number,headRefName,baseRefName,isDraft`). R39's
own verdict is NOT a §4.13 terminator because this branch continues, and the next reviewed round
records R39's gate entry.

  R40 migrates `packages/orchestration/ci_run.py` onto the seam, passing the per-stage
  budget through `extra_env`. It still owes its own DECISION on where the stage output
  goes: at cbcb5c23 `_run_via_subprocess` streams straight to the console and returns
  only the returncode, while the seam CAPTURES both streams, so the migration changes
  observable behaviour rather than preserving it and that decision is the round's own
  work. `packages/orchestration/builder_bridge.py` follows it, and R41 or later takes
  T002c-d.
