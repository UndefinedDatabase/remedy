# Handback — F274 round 2 — the D11c reachability ratchet landed, DECISION F274 D1 ruled, R-0830 registered

Every gate below was RUN and its exit code read from the process, never inferred. Where a gate
went a different way than the block predicted it is said so in Deviations, not smoothed over.

## Session

SESSION 2 of feature F274 · round 2 · rounds so far 2

Round 1 was the whole of session 1 and ended on `.agent/STOP`. This session delegates round 2,
which is the first round under operator amendment amend0907-cluster-first: DECISION
amend0907-cluster-first D1 reordered the feature so T003 runs first, which voided the round 2
block authored in session 1 (`.remedy-wt/f274-r2-block.md`, kept on disk, not read and not
applied) and replaced it with `.remedy-wt/f274-r2v2-block.md`.

CONTEXT SELF-ASSESSMENT (amend0905-throughput, one sentence): context stayed comfortable —
every large state file (`decisions.md` 878 KB, `live_review.md` 501 KB, `prose_slips.md` 154 KB)
was handled by measurement in Python rather than read, and the only files read whole were
`AGENTS.md`, `.agent/context.md`, the step block and the handback template.

## Range

Review of `9c65a9225cdf4d60822d459d698b66d2d7cb19d7`..`2a0287d6` (plus the handoff commit that
carries this file, which cannot table itself — R-0149 pattern).

## Commits

Eight commits, single-parent, in the block's ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6,
plus the C7 handoff commit. `git status --porcelain` was EMPTY immediately before each commit
except for that commit's own path, and EMPTY immediately after each.

### 24d0b6bc F274 R2 C0a: save the round 2 step block to .agent/authored
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f274-r2.md` | +360 / -0 | C0a — the step block saved by `shutil.copyfile`, first link of the transport chain |

### 4d78bbac F274 R2 C0b: mirror the round 2 block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +296 / -337 | C0b — same bytes mirrored by `shutil.copyfile`, replacing round 1's block |

### ce0aef81 F274 R2 C1: advance the plan to round 2, the D11c reachability ratchet
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +26 / -21 | C1 — whole-file replacement by slice PLANF274R2; plan advances before the finding is registered (§3 item 23) |

### d2cc78cd F274 R2 C2: re-head the live review for the reordered slice sequence
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +14 / -11 | C2 — HEAD region replaced by slice HEADF274R2; the append-only findings region untouched |

### a09d4ea5 F274 R2 C3: book round 1's PASS verdict and register R-0830
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +4 / -0 | C3 — slice RECORDR2 appended to the findings region; the head region untouched |

### 88543f2d F274 R2 C4: rule the reachability proof as a ratchet and T003's split boundary
| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +42 / -0 | C4 — slice D1SLICE274 appended; DECISION F274 D1 |

### 1c36e9f7 F274 R2 C5: land the D11c import-reachability ratchet and its measured allowlist
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_import_reachability.py` | +145 / -0 | C5 — NEW, built to the block's SPEC; static `ast` closure of the six D11 (c) entry points, three assertions |
| `tests/orchestration/import_reachability_allowlist.txt` | +324 / -0 | C5 — NEW, GENERATED from the closure the test itself computes: 5 comment lines + 319 measured modules |

### 2a0287d6 F274 R2 C6: record the two round 1 reviewer slips and the stale-block slip
| Path | +/- | Reason |
|---|---|---|
| `.agent/prose_slips.md` | +6 / -0 | C6 — slice SLIPS274R2 appended, three dated lines |

### C7 — the handoff commit (self-reference)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | n/a | C7 — this file; a handback cannot table the commit that writes it |

PER-COMMIT INSERTIONS against the DECISION F104 D1 cap of 500, from
`git diff --numstat <parent> <commit>`, matching the `+` cells above cell by cell:
C0a 360, C0b 296, C1 26, C2 14, C3 4, C4 42, C5 469, C6 6. Every one under the cap; no oversize
commit was declared and none was needed.

## External actions

| Action | Command | Outcome |
|---|---|---|
| worktree add | `git worktree add /home/decodeux/Repos/remedy/.remedy-wt/f274-r2-redctl 1c36e9f7 --detach` | created, detached at the C5 commit; count 14 → 15 |
| worktree remove | `git worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f274-r2-redctl --force` then `git worktree prune` | removed BY EXACT PATH; count 15 → 14 |
| push | `git push origin feature/f274-one-world-completion-part-two` | run after C7 |

No pull request was created, nothing was merged, nothing was force-pushed, no branch was cut.
`git worktree list` counted 14 at the start of the round and 14 at the end.

## Verification

`.agent/STOP` read with `os.path.exists` three times as constraint 3 orders: before C0a FALSE,
before C5 FALSE, before C7 FALSE.

EXIT CODES: this session's shell guard refuses `$?` inside a compound command
(`.agent/context.md`), so the exit-code read is re-expressed in Python at
`.remedy-wt/f274r2_run.py`, which runs each command in its own process with `subprocess.run` and
prints `proc.returncode` directly. There is no pipe between the command and the exit reading.

### G1 TRANSPORT — PASS
All three artefacts are 35679 bytes and byte-identical, and all three hash to the digest the
delegation states beside the block:
`1e2a7bb50df1f497b424dd87289fcdf3f477c5601d57f9fd891e4c6e58408e3f`
— `.remedy-wt/f274-r2v2-block.md`, `.agent/authored/f274-r2.md`, `.agent/last_block.md`.
Per §3 item 37 this chain covers those three artefacts and claims nothing about the bytes that
were emitted to the worker.

### G2 THE RECORD HEAD (C2) — PASS
`\n## Findings\n` occurred exactly ONCE before and exactly ONCE after.
HEAD region BEFORE: 3063 bytes / 40 lines, sha256 `77b1cd43268d4f21ab8fffeafed1df64c15972f7090bca271c09910fd97998f4`.
HEAD region AFTER: 3396 bytes / 43 lines, sha256 `9622379fe041a62bb69372e6b6dc2266ee639e2be6bdf87a12d905c3db998cda`,
byte-equal to slice HEADF274R2.
FINDINGS region sha256 `09f49be742173d4ae4b05fe71c465dc3fde583a71406b66ef977f148988565d5`
BOTH before and after the commit — the append-only region did not move.

### G3 THE RECORD APPEND (C3) — PASS, all four parts
(a) BYTE: pre-image is a byte-exact PREFIX of the post-image, and post == pre + RECORDR2 with no
separator of the worker's own (the slice carries its own leading blank line). The HEAD region was
byte-identical across the commit, sha256 `9622379f…` before and after.
Findings region 501473 bytes / 505 lines → 511593 bytes / 509 lines, sha256
`09f49be742173d4ae4b05fe71c465dc3fde583a71406b66ef977f148988565d5` →
`991f2c0e4b6eb6184dc9f96799ee02681d9a962d9ece80ee51ef1aa1165e911e`.
(b) STRUCTURAL: N was COUNTED by the script from the slice as 2, not taken from the block; the
last 2 blank-line separated units of the whole file equal the slice's 2 paragraphs in order.
(c) NEGATIVE CONTROL, in memory only: the flip was located by searching the ENCODED bytes at or
after the append point — `post.index(b"VERDICT PASS", append_point)` — landing at byte offset
504912, with the append point at 504869 and the first appended paragraph ending at 510133, so the
flip is provably INSIDE the first appended paragraph. BOTH readers REJECTED the flipped image and
BOTH ACCEPTED the real one, and the file on disk was byte-unchanged by the control.
(d) COUNTS, before → after: distinct `^- R-\d{4}` 63 → 64; distinct `^Done: R-\d{4}` 3 → 3;
OPEN SET BY DISTINCT ID 60 → 61; `^Gate: ` 32 → 33; `^Gate: F274 R1` 0 → 1 as the block states;
`^- R-0830` 0 → 1 as the block states.

### G4 THE DECISION APPEND (C4) — PASS
`.agent/decisions.md` 878136 bytes / 10919 lines → 881507 bytes / 10961 lines. Pre-image is a
byte-exact PREFIX of the post-image and post == pre + D1SLICE274.
sha256 `b3aece0b92c2fdcd7f33753e5d6828fca9e144e3c661434418b22b12075b6cd5` →
`d2981fda0c5d1e103e97220fd0c71bbe3cc03fa1a0abedea6694e10b5258c477`.
`^## DECISION F274 D` 0 before, exactly 1 after. `^## DECISION F274 D1 ` heads exactly one section.

### G5 THE REACHABILITY TEST (C5) — PASS, all four parts
Constraint 8 confirmed FIRST: `git ls-tree 9c65a9225cdf4d60822d459d698b66d2d7cb19d7 -- tests/orchestration/test_import_reachability.py`
returned EMPTY, and the same command for `tests/orchestration/import_reachability_allowlist.txt`
returned EMPTY. Both files are genuinely new.

(a) GREEN. `python3 -B -m pytest tests/orchestration/test_import_reachability.py -q -p no:randomly`
→ `3 passed in 1.28s`, REAL EXIT CODE 0. Allowlist LINE COUNT 324 = 5 comment lines + 319 module
entries. The closure measured 319 modules out of 367 first-party `.py` files on disk — the same
two numbers the reviewer's own dry run reported, arrived at independently.

(b) RED CONTROL ONE, the orphan. Disposable worktree at the C5 commit `1c36e9f7`. Baseline there
first: EXIT 0, 3 passed. Then a single line
`import packages.orchestration.bench_run  # RED CONTROL ONE` appended to
`packages/orchestration/self_use_runner.py` (7662 → 7721 bytes). Same command → REAL EXIT CODE 1,
`1 failed, 2 passed`, failing at `test_no_module_outside_the_allowlist_is_reachable_from_the_entry_points`
and naming EIGHT newly reachable modules, one per line:
`packages.orchestration.bench_dry_run`, `packages.orchestration.bench_orders`,
`packages.orchestration.bench_run`, `packages.orchestration.gauntlet_evaluator`,
`packages.orchestration.gauntlet_evidence`, `packages.orchestration.gauntlet_injection`,
`packages.orchestration.gauntlet_orders`, `packages.orchestration.gauntlet_runner`.
Eight is the count the reviewer's dry run saw. That ONE file was then restored by exact path with
`git -C <worktree> checkout -- packages/orchestration/self_use_runner.py`, the worktree's
`git status --porcelain` was EMPTY, and the re-run was REAL EXIT CODE 0, 3 passed.

(c) RED CONTROL TWO, the stale entry. In the same worktree, one line
`packages.orchestration.this_module_has_no_file_on_disk` appended to the allowlist
(11875 → 11930 bytes, 324 → 325 lines). Same command → REAL EXIT CODE 1, `1 failed, 2 passed`,
failing at `test_every_allowlist_entry_still_resolves_to_a_file_on_disk` and naming exactly that
module. The appended line was then removed by exact path, after asserting it was the file's
terminal bytes (back to 11875 bytes / 324 lines), and the re-run was REAL EXIT CODE 0, 3 passed.

(d) THE CEILING. `python3 -m ruff check .` in the PRIMARY checkout → `Found 26 errors.`,
REAL EXIT CODE 1 — 26 is the frozen ceiling and is UNCHANGED from the base measurement of 26
taken before C5, so DECISION F083 D5 is not touched. `python3 -m ruff check tests/orchestration/test_import_reachability.py`
→ `All checks passed!`, REAL EXIT CODE 0, so the new file contributes zero to the ceiling.
`python3 -B -m pytest tests/orchestration/test_ci_budgets.py -q -p no:randomly` → `10 passed`,
REAL EXIT CODE 0.

WHAT WAS BUILT, since the block specified the property and not the bytes.
`tests/orchestration/test_import_reachability.py` pins `ENTRY_POINTS` as a module-level tuple of
the six dotted names the block names, and `FIRST_PARTY_ROOTS = ("packages", "apps")`.
`resolve_module_path` maps a dotted name to `<root>/a/b/c.py` or `<root>/a/b/c/__init__.py`, and
returns `None` otherwise. `first_party_imports` parses with `ast.parse` and walks the WHOLE tree
with `ast.walk`, so imports inside `if TYPE_CHECKING:` blocks and inside function bodies are
followed; `ast.ImportFrom` with a non-zero `level` is skipped, and `from X import y` contributes
both `X` and `X.y`, with `X.y` dropped later when it resolves to no file. `reachable_closure`
is a worklist that never imports anything. `read_allowlist` ignores blank lines and lines
beginning with `#`. The three test functions are
`test_every_entry_point_resolves_to_a_file_on_disk`,
`test_no_module_outside_the_allowlist_is_reachable_from_the_entry_points` and
`test_every_allowlist_entry_still_resolves_to_a_file_on_disk`; each failure message names the
offending modules one per line via a shared `_one_per_line` helper. The module docstring states
why the walk is static (importing the cockpit runs module-level side effects), why
over-approximation is the safe direction (this test guards a DELETION, so a false "reachable" is
harmless and a missed edge deletes working code), and names DECISION amend0905-vocab D11 (c),
F274 T003, DECISION F274 D1 and finding R-0830.
The allowlist was GENERATED, not typed: `.remedy-wt/f274r2_gen_allowlist.py` imports
`reachable_closure` and `ALLOWLIST_PATH` FROM THE SHIPPED TEST MODULE and writes the sorted
closure under a five-line comment header.

### G6 THE TWO PROSE FILES — PASS
`.agent/plan.md` is BYTE-EQUAL to slice PLANF274R2, 2292 bytes / 41 LINES against the AGENTS.md
cap of 50, and carries both `## Goal` and `## Next Steps`.
`.agent/prose_slips.md` BEFORE 154472 bytes / 573 lines, sha256
`7a71913871e7e2baaa0f40fa927d69b897185d399e5ba8bb1682b1a76cad6ee5`; AFTER 156171 bytes / 579
lines, sha256 `30bda63333cdae55c6be0e19da8e4faa6523a471d8489d1367f6ee68a8e9a3cb`. Pre-image is a
byte-exact PREFIX of the post-image and post == pre + SLIPS274R2.

### G7 THE SUITES AND THE TREE — PASS
Run SERIALLY in the primary checkout, each as its own command, each exit code read from the
process. THE FOUR STATE READERS AS FOUR:

| Command | Result | Real exit code |
|---|---|---|
| `python3 -B -m pytest tests/ui_server/ -q -p no:randomly` | 515 passed in 33.64s | 0 |
| `python3 -B -m pytest tests/orchestration/test_test_runner.py -q -p no:randomly` | 52 passed in 5.97s | 0 |
| `python3 -B -m pytest tests/regression/test_resource_safety.py -q -p no:randomly` | 21 passed in 11.31s | 0 |
| `python3 -B -m pytest tests/orchestration/test_integrity_gate.py -q -p no:randomly` | 16 passed in 0.26s | 0 |
| `python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly` (canary) | 42 passed in 22.49s | 0 |

`git status --porcelain` was EMPTY immediately after every commit and carried only the committing
path immediately before each. `git ls-files .remedy-wt` returned EMPTY — the scratch directory is
gitignored and nothing from it was ever staged. Per-commit insertion counts against the cap of
500 are tabled under Commits; C7's own numbers cannot exist while its text is being written, as
the block says.

BASE MEASUREMENTS, constraint 7, ALL CONFIRMED ON DISK BEFORE USE with no divergence:
`.agent/plan.md` 1909 bytes / 36 lines; `.agent/live_review.md` 504536 bytes / 545 lines; its
HEAD region 3063 bytes / 40 lines at `77b1cd43…`; its FINDINGS region 501473 bytes / 505 lines at
`09f49be7…`; `.agent/decisions.md` 878136 bytes / 10919 lines at `b3aece0b…`;
`.agent/prose_slips.md` 154472 bytes / 573 lines at `7a719138…`.

## Authored-text proofs

Disk-to-disk, re-extracted from the COMMITTED `.agent/authored/f274-r2.md` (not from the
`.remedy-wt/` copy the slices were applied from) by matching the `<<<BEGIN <NAME> ` prefix line
and the exact `<<<END <NAME>>>` line, then compared against the region each landed in:

| Slice | Bytes | sha256 | Disk-to-disk result |
|---|---|---|---|
| PLANF274R2 | 2292 | `77f01eddfc250a2a92ca65c4f08d8b31f6c96e2063e79590474f84ab42e440a3` | `.agent/plan.md` BYTE-EQUAL |
| HEADF274R2 | 3396 | `9622379fe041a62bb69372e6b6dc2266ee639e2be6bdf87a12d905c3db998cda` | live_review HEAD region BYTE-EQUAL |
| RECORDR2 | 10120 | `4dda2c1674cd5ab54188991df115e8dd596cfd6d60a361ea51d3907704bb8637` | findings region ends with these exact bytes |
| D1SLICE274 | 3371 | `5819f93fac7b4141ba44c333b772a60c94e9e610aaba2b8b1245cc5099a99089` | `.agent/decisions.md` ends with these exact bytes |
| SLIPS274R2 | 1699 | `e842e4df778390cb27510fc71cd157d31faeee80707111d04817b2331a1d893f` | `.agent/prose_slips.md` ends with these exact bytes |

No slice was retyped and no digest was hand-typed. RECORDR2, D1SLICE274 and SLIPS274R2 each carry
their own leading blank line and were appended as-is with no separator added.

## Deviations & assumptions

The block's ordered commit sequence C0a, C0b, C1, C2, C3, C4, C5, C6, C7 was followed EXACTLY: no
extra commit, no dropped commit, no reordering. Every slice was applied VERBATIM; nothing was
silently repaired. The Change set was respected exactly — the nine listed paths and nothing else,
nothing under `packages/`, `apps/`, `docs/` or `scripts/`, and nothing deleted.

1. STANDING SHELL RE-EXPRESSION, declared per `.agent/context.md`. `$?` inside a compound command
   is refused by this session's guard, so every exit code in this handback was read in Python by
   `.remedy-wt/f274r2_run.py` using `subprocess.run(...).returncode`, printed alongside the
   command and its output tail. No exit code here is inferred from the absence of an error.

2. THE COMMIT GATE AND THE BLOCK'S ORDER DISAGREE FOR TWO COMMITS, AND THE BLOCK WON.
   AGENTS.md's Commit Gate requires `.agent/plan.md` to reflect the current work before EVERY
   commit, but the block's constraint 2 fixes C0a and C0b ahead of C1 and says the order "is not
   varied". So `24d0b6bc` and `4d78bbac` landed while `plan.md` still described round 1. Applied
   as ordered under constraint 1 and declared here rather than repaired. The exposure is two
   commits wide and self-healing: `ce0aef81` is the very next commit.

3. G3(b)'s "blank-line separated units" NEEDED A DEFINITION AND I HAD TO CHOOSE ONE, which is the
   one thing in this round that took two attempts. Read literally with boundary newlines kept, the
   comparison CANNOT succeed: RECORDR2's first unit begins with the slice's own leading newline
   while the same unit read out of the whole file does not, because there the blank line belongs
   to the preceding record. My first structural reader kept those newlines and REJECTED the real
   image. I restored `.agent/live_review.md` to HEAD with `git checkout --` before changing
   anything — the rejected image was never committed and the findings-region digest was re-read as
   `09f49be7…` after the restore to prove it — then redefined a unit as stripped of its boundary
   newlines and re-ran the whole of G3 from the clean pre-image. The negative control still
   REJECTS under the stripped definition, so the reader is not weakened by the change: the flipped
   byte is interior to the paragraph, not on its boundary. Flagged as an imprecision in the block,
   not as a defect in the slice.

4. CONSTRAINT 7's HEAD AND FINDINGS FIGURES RESOLVE ONLY UNDER THE BLOCK'S OWN SPLIT RULE, and are
   correct under it. Constraint 4 defines the head as the text BEFORE `\n## Findings\n` and the
   findings region as the marker AND everything after, so the newline preceding `## Findings`
   belongs to the FINDINGS region. Under that rule every one of the block's six numbers matched to
   the byte. Under the more common convention of giving that newline to the head, the same file
   measures 3064 / 41 and 501472 / 504 — an off-by-one in each direction. Recording it because a
   reviewer re-measuring with the other convention will see a divergence that is not there.

5. WORKTREE HYGIENE. The destructive verification of G5 (b) and (c) ran ONLY inside
   `/home/decodeux/Repos/remedy/.remedy-wt/f274-r2-redctl`, detached at the C5 commit; the primary
   checkout was never mutated and `git status --porcelain` was empty at every commit boundary. The
   worktree was removed BY EXACT PATH and pruned. `git worktree list` counted 14 at the start of
   the round and 14 at the end (15 while the control worktree was alive). The 13 pre-existing
   `remedy/job-*` worktrees are not this round's and were not touched.

6. SCRATCH KEPT AND SCRATCH LEFT. `.remedy-wt/f274-r2v2-block.md` is KEPT as the first link of the
   transport chain and `.remedy-wt/f274-r2-block.md`, the SUPERSEDED block, is KEPT UNTOUCHED and
   was never opened, both per constraint 6. Four helper scripts written this round remain under
   the gitignored `.remedy-wt/` — `f274r2_extract.py`, `f274r2_c3.py`, `f274r2_c4.py`,
   `f274r2_gen_allowlist.py`, `f274r2_run.py` — so the reviewer can re-run any gate byte for byte.
   `git ls-files .remedy-wt` is empty, so none of them is tracked.

WHAT I BELIEVE IS WRONG IN THE BLOCK, stated as disagreement rather than acted on:

- G3(b) as discussed in deviation 3. The clause should say a unit is compared without its boundary
  newlines, or the slice should not carry a leading blank line into a comparison that also reads
  the file. As written it is satisfiable only by choosing the definition, and the worker's choice
  is the thing the gate was supposed to constrain.
- Constraint 2's justification cites "§3 item 23" for C1 preceding the substantive commits, and
  the block also cites "§3 item 37" in G1 and "§4 item 4" inside RECORDR2. Those references are to
  `docs/agents/planner_reviewer_prompt.md`, which this worker was not given and did not read; they
  are carried through unverified. Nothing in this round depends on them being accurate.
- Nothing else. The SPEC in particular was buildable exactly as written, and the two numbers it
  offered as the reviewer's own — closure 319 out of 367, and eight modules named by red control
  one — both reproduced independently here, which is a stronger result than the block asked for.

## Item-status table

Every C and G item of the block, exactly once.

| Item | Status | Reason |
|---|---|---|
| C0a | done | `.agent/authored/f274-r2.md` written by `shutil.copyfile`, commit `24d0b6bc` |
| C0b | done | `.agent/last_block.md` mirrored by `shutil.copyfile`, commit `4d78bbac` |
| C1 | done | `.agent/plan.md` = PLANF274R2, commit `ce0aef81` |
| C2 | done | live_review HEAD region = HEADF274R2, findings untouched, commit `d2cc78cd` |
| C3 | done | RECORDR2 appended to the findings region, head untouched, commit `a09d4ea5` |
| C4 | done | D1SLICE274 appended to `.agent/decisions.md`, commit `88543f2d` |
| C5 | done | reachability test + generated allowlist built to the SPEC, commit `1c36e9f7` |
| C6 | done | SLIPS274R2 appended to `.agent/prose_slips.md`, commit `2a0287d6` |
| C7 | done | this file, rewritten in full per `docs/agents/handback_template.md` |
| G1 | done | PASS — three artefacts byte-identical at `1e2a7bb5…`, the delegation's digest |
| G2 | done | PASS — head byte-equal to slice, findings digest identical before and after, marker once |
| G3 | done | PASS — byte, structural (N=2 counted from the slice), negative control, and all six counts |
| G4 | done | PASS — prefix true, post == pre + slice, `^## DECISION F274 D` 0 → 1 |
| G5 | done | PASS — (a) exit 0 / 3 passed / 324 allowlist lines, (b) exit 1 naming 8 modules then exit 0, (c) exit 1 naming 1 module then exit 0, (d) ruff 26 unchanged and ci_budgets exit 0 |
| G6 | done | PASS — plan byte-equal at 41 lines under the cap of 50; slips prefix true, 154472 → 156171 bytes |
| G7 | done | PASS — four state readers AS FOUR plus the canary, all exit 0; tree empty, `git ls-files .remedy-wt` empty, every commit under the 500 cap |

## Open findings

61 open BY DISTINCT ID, measured on the post-C3 `.agent/live_review.md`: 64 distinct ids matching
`^- R-\d{4}` against 3 distinct ids matching `^Done: R-\d{4} `. The round moved that count by
exactly one, R-0830, which this round REGISTERS and does not resolve — DECISION F274 D1 says so in
terms, and no `Done:` paragraph was written, per constraint 5. The four open High findings are
R-0803, R-0804, R-0806 and R-0807, all of them F273's rather than this feature's per DECISION
F272 D12.

## Next

The two carry-overs F260's Design names, done BEFORE the first `git rm`: overnight readiness and
the overnight report become read-only `mission readiness` / `mission report`, and every
user-settable route-policy knob is checked against F110's config keys — existing knob deleted,
missing knob registered as a finding and never rebuilt. DECISION F260 D3, the deletion paragraph,
follows; the `git rm` sequence itself is NEVER started by a session that cannot finish it.
