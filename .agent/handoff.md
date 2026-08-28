# Handback — F037 Rendered diff viewer, round 25 (THE INTEGRATION GATE)

## Session

SESSION 8 of feature F037 · round 25 · rounds so far 25

Rounds planned for this session: R25 (this one), R26, R27. R27 ends the session
and F037's closure sequence. This round is permitted past the seven-session soft
limit by operator amendment amend0827-process-diet rule 1, which names a
feature's CLOSURE SEQUENCE as the one exception to the ban on bookkeeping-only
rounds; the rule-6 scope-report obligation was already discharged at R24 (D11,
amendment A6, and the report in the `38966bf3` handback).

## Range

Review of `38966bf3..HEAD`.

## Commits

### 1e5f423a docs(agent): save the F037 R25 integration-gate block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f037-r25.md` | +346 / -0 | C0a — the block saved verbatim |

### fe72ccae docs(agent): mirror the R25 block into last_block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +301 / -296 | C0b — same bytes, one blob with C0a |

### 3d99164d docs(agent): point the plan at the F037 integration gate

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +19 / -18 | C1 — the PLANF037R25 slice, rewritten not appended |

### 9a7e5f16 docs(review): book the R24 verdict and resolve R-0719

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +12 / -0 | C2 — GATER24 then DONE719, in that order |

### 7c2a45d2 test(gate): record the F037 integration-gate evidence

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/gate_f037_r25/attribution.txt` | +160 / -0 | C3h — per-id attribution, both sets |
| `.agent/gate_f037_r25/auto_build_neutralization.txt` | +32 / -0 | C3e — the real predicate's answer |
| `.agent/gate_f037_r25/base_failed.txt` | +1 / -0 | C3f — sorted FAILED lines at base |
| `.agent/gate_f037_r25/base_run.txt` | +68 / -0 | C3f — base run, tail, exit, wall |
| `.agent/gate_f037_r25/branch_failed.txt` | +1 / -0 | C3b — sorted FAILED lines on branch |
| `.agent/gate_f037_r25/branch_run.txt` | +66 / -0 | C3b — branch run, tail, exit, wall |
| `.agent/gate_f037_r25/canary.txt` | +21 / -0 | G7 — canary and state contracts |
| `.agent/gate_f037_r25/comm.txt` | +17 / -0 | C3g — both comm sets in full |
| `.agent/gate_f037_r25/parity.txt` | +33 / -0 | C3f — the mtime window and verdict |
| `.agent/gate_f037_r25/summary.txt` | +48 / -0 | C3i — the one-screen summary |

10 files under `.agent/gate_f037_r25/`; commit total +447 / -0.

### C4 docs(agent): hand back F037 R25 with the integration-gate result

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | (self-reference) | C4 — this file; a handback cannot table the commit that writes it (R-0149 pattern). Its insertion count belongs to the next round's ledger entry and was not gated here, as G8 states. |

## External actions

| Command | Outcome |
|---------|---------|
| `git worktree add -b tmp/f037-r25-base .remedy-wt/f037-r25-base 9dde54956afbe5f432bfd429bf4ba0bb272f6d07` | Created on a BRANCH, never detached. "Preparing worktree (new branch 'tmp/f037-r25-base') / HEAD is now at 9dde5495 Merge pull request #217…" |
| `git worktree remove --force .remedy-wt/f037-r25-base` | Removed |
| `git worktree prune` | Ran, exit 0 |
| `git branch -D tmp/f037-r25-base` | "Deleted branch tmp/f037-r25-base (was 9dde5495)." |
| `git worktree list` | One line: `/home/decodeux/Repos/remedy  9a7e5f16 [feature/f037-rendered-diff-viewer]` |
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | `[]` — no open PRs |
| `git push -u origin feature/f037-rendered-diff-viewer` | Runs immediately AFTER the commit that writes this file; see the note below |

No PR was created. No merge. No force-push, no history rewrite, no work on `main`.

THE PUSH OUTCOME IS NOT STATED HERE, and that is deliberate. The push necessarily
happens after the commit that writes this file, so any outcome printed here would
be a value that could not exist when the text was written — and the write-once
rule forbids a second handoff commit to fill it in. The outcome is reported in
this round's session output instead, and the reviewer can measure it directly:
`git rev-parse HEAD` equals
`git rev-parse origin/feature/f037-rendered-diff-viewer` if and only if the push
succeeded.

## Verification

**G1 HYGIENE — PASS.** `.agent/STOP` read from disk before C0a: `ls` reported
"No such file or directory" — ABSENT. Read again before C4:
`pathlib.Path('.agent/STOP').exists()` → `False` — ABSENT. `git rev-parse HEAD`
before C0a = `38966bf309bd92deca3bc928818df55b18050860`, equal to the BASE
`38966bf3`. `git branch --show-current` = `feature/f037-rendered-diff-viewer`.
`git status --porcelain | wc -l` = 0 after C0a, after C0b, after C1, after C2 and
after C3 — five readings, all 0.

**G2 TRANSPORT — PASS.** sha256 of the committed `.agent/authored/f037-r25.md`
blob = `790f708e7f3492ea3a369baf52f0a54b67a74ec214528dc54dc1a9d5da4c9980`
(25345 bytes, 346 lines). sha256 of the reviewer's own original at
`.remedy-wt/f037-r25-block.md` = the same digest, same 25345 bytes. They are
EQUAL. That file existed before this worker did and was not written by it, so
this reading covers the EMISSION and not merely the worker's own
self-consistency. No digest is stated here that was not computed here. At C0b,
`git rev-parse HEAD:.agent/authored/f037-r25.md` and
`git rev-parse HEAD:.agent/last_block.md` both print
`0888befa412e7ae0923fa7f14fd7a5f00d8c57c3` — ONE blob.

**G3 THE PLAN AT C1 — PASS.** PLANF037R25 was re-extracted from the COMMITTED
C0a blob via `git show 1e5f423a:.agent/authored/f037-r25.md` and compared with
`.agent/plan.md` at `3d99164d`: BYTE EQUAL including the trailing newline
(`True`). Negative control, the same comparison with the trailing newline
dropped: `False`. `wc -l` = 44, strictly under 50. Lines exactly `## Goal`: 1.
Lines exactly `## Next Steps`: 1.

**G4 THE RECORD AT C2, both readers — PASS.** (a) `38966bf3` blob of
`.agent/live_review.md` + `\n` + GATER24 + `\n` + DONE719 == the C2 blob →
`True`. NEGATIVE CONTROL: byte offset 20 of GATER24 — inside the FIRST appended
paragraph, `h` → `H` — recomputed, equality `False`. REJECTED as required.
(b) The C2 blob split on blank lines; N, counted by the script from the two
slices themselves, is **6** (5 paragraphs in GATER24, 1 in DONE719); the LAST 6
units of the file match those 6 paragraphs IN ORDER, unit by unit, all `True`.
The pre-round blob is a byte PREFIX of the C2 blob: `True`, 1316230 bytes growing
to 1322142. Every non-current revision was read with `git show <sha>:<path>` into
memory; no tracked file was written for a measurement.

**G5 THE LEDGER — PASS.** Base figures re-measured by this worker at `38966bf3`,
not inherited: registrations `^- R-\d+ — ` 292, all DISTINCT; `^Done: R-\d+ — `
42; `^Landed: R-` 11; `^Gate: F\d+ R\d+ — ` 94; OPEN SET as a set 252. Every one
equals the figure the block states. Over the C2 blob: registrations **292**,
UNMOVED, all 292 DISTINCT; `^Done: R-\d+ — ` **43**, a rise of exactly ONE;
`^Landed: R-` **11**, UNMOVED; `^Gate: F\d+ R\d+ — ` **95**, a rise of exactly
ONE; OPEN SET **251**, a fall of exactly one from 252. `Gate: F037 R24` occurs
exactly **1** time in the C2 blob. `R-0719` now has a `Done:` line: `True`.

**G6 THE INTEGRATION GATE — EXECUTED IN FULL; ONE ITEM VOID AND REPORTED VOID.**
All of C3 (a) through (i) ran; 10 evidence files are present under
`.agent/gate_f037_r25/`.

- (a) DIST READINGS, measured rather than taken on trust:
  `apps/ui/dist/index.html` EXISTS; its mtime is `1787917601.759354`
  (Fri Aug 28 13:46:41 2026). The newest of the 128 files under `apps/ui/src` is
  `apps/ui/src/api/diffViewModel.ts` at `1787914723.6506479`
  (Fri Aug 28 12:58:43 2026). dist mtime EXCEEDS every source file: `True`. The
  dist is WARM; nothing was rebuilt and no handoff was owed.
- (b) BRANCH RUN, `python3 -m pytest -n auto -q` from the repository root, output
  captured in memory by `subprocess.run(capture_output=True)` and written to the
  evidence directory only after the process exited: **exit code 1**, **wall
  161.0s**, `1 failed, 18118 passed, 20 skipped in 160.41s`. **1** `FAILED` line.
- (c) BASE WORKTREE created on a BRANCH at
  `9dde54956afbe5f432bfd429bf4ba0bb272f6d07`, which this worker re-measured with
  `git merge-base main HEAD` and which matched the block's SHA. Never detached.
- (d) PARITY COPY with `shutil.copytree(src, dst, symlinks=True)` — the argument
  passed explicitly, not left to `copytree`'s `symlinks=False` default (R-0591):
  `apps/ui/node_modules` 44839 entries with **27 symlinks preserved as
  symlinks**, `apps/ui/dist` 4 entries. Neither directory is itself a symlink.
- (e) STALENESS PREDICATE NEUTRALISED AND PROVED BY CALLING IT. Base
  `apps/ui/dist` mtimes raised to `1787918420.63`, above the base worktree's
  newest source file `1787918120.63`. Then the REAL function was imported from
  the BASE WORKTREE's own module with that worktree as the working directory:
  module file
  `/home/decodeux/Repos/remedy/.remedy-wt/f037-r25-base/packages/orchestration/ui_server.py`,
  `_frontend_is_stale()` → **False**, exit 0.
- (f) BASE RUN, same command, cwd the base worktree, `REMEDY_UI_NO_AUTO_BUILD=1`
  supplied through `subprocess.run(env=...)` and not exported: **exit code 1**,
  **wall 155.2s**, `1 failed, 17981 passed, 20 skipped in 154.66s`. **1** `FAILED`
  line.
- (f) PARITY VERDICT: **VOID.** Run window `1787918225.502663`
  (13:57:05) → `1787918380.7180617` (13:59:40). All four files under the base
  worktree's `apps/ui/dist` carry mtime `1787918302.0531702` (13:58:22) after the
  run, which falls INSIDE that window, and the hashed asset filenames changed
  across it — `index-B5aVi7qQ.js` → `index-D_a-qpxM.js`,
  `index-DBZlPUBM.css` → `index-D0y3OK7n.css`. Changed hashed filenames are a
  real vite rebuild, not a touch. Reported as VOID and NOT repaired, exactly as
  C3(f) orders. The block's clause that a void claim costs nothing when the
  base-only set is empty does NOT apply here — the base-only set holds one id, so
  an attribution was owed, and it is given below.
- (g) COMPARE, both sets in full, never truncated. `comm -13 base_failed.txt
  branch_failed.txt` = **1** id; `comm -23` = **1** id; intersection EMPTY.
  - branch-only:
    `FAILED tests/orchestration/test_product_smoke.py::test_no_zombie_processes_after_the_suite`
  - base-only (fixed by the branch):
    `FAILED tests/cli/test_review_bundle_runtime.py::TestSubprocessCleanup::test_timeout_raises_with_cleanup`
- (h) ATTRIBUTION, unconditional and per id.
  - BRANCH-ONLY `test_no_zombie_processes_after_the_suite` — failed under `-n
    auto` with `AssertionError: port 5273 still open` at
    `tests/orchestration/test_product_smoke.py:500`. Serial re-run of the exact
    node id, alone, in the primary checkout, **10 runs, exit codes
    [0,0,0,0,0,0,0,0,0,0], 10 of 10 PASS**. SERIAL-PASS ⇒ the xdist-flake class;
    recorded, NOT a blocker. Not coupled to feature code, by direct evidence:
    the file is not among the 57 paths of `git diff --name-only 9dde5495..HEAD`;
    the test builds two synthetic apps under its own `tmp_path` and reaches none
    of `diff_parser.py`, `diff_view_source.py`, the diff endpoint or any
    `apps/ui/src` diff component; and the assertion is a 0.2 s grace window on a
    child's socket teardown, which is a race under load. Constraint 5 does not
    fire.
  - BASE-ONLY `TestSubprocessCleanup::test_timeout_raises_with_cleanup` — failed
    at base with `AssertionError: Orphan process found after timeout cleanup` at
    `tests/cli/test_review_bundle_runtime.py:327`. NO MISSING ARTIFACT EXPLAINS
    IT, and that is stated plainly rather than forced into the environment
    bucket: both artifacts `integration_gate.md` names were PRESENT (44839
    `node_modules` entries and `dist` copied in), and the assertion reads no
    build output — it shells out to `pgrep -f "apps.cli.grouped.*--help"`, a
    MACHINE-WIDE match that another xdist worker satisfies. Serial re-run of the
    exact node id, alone, IN THE BASE WORKTREE at the merge base, **10 runs, exit
    codes [0,0,0,0,0,0,0,0,0,0], 10 of 10 PASS**. It does not reproduce serially
    at the commit that produced it, so it is neither a genuine base failure nor a
    failure the branch fixed. The file is likewise untouched by the branch.
  - THE VOID'S CAUSE IS NAMED AND MEASURED, not inferred. In the base worktree
    `tests/ui_server/test_dashboard_contract.py::TestAutoBuildBehavior::test_auto_build_runs_by_default`
    (lines 574-584) pops `REMEDY_UI_NO_AUTO_BUILD` from a CLEARED environment and
    calls the real, unmocked `_auto_build_frontend()`. Its docstring assumes the
    call cannot build; a git worktree is a full checkout, so `apps/ui/package.json`
    is present and `npm run build` ran. Re-run ALONE with the flag set through
    `env=`, that one passing test moved all four `apps/ui/dist` mtimes again —
    `1787918302.05` → `1787918576.12`, exit 0, `1 passed in 1.74s`. The `env=`
    the block ordered was passed and was honoured at `ui_server.py:3083`; it was
    removed inside the process by a test. This is the R-0169 class
    `integration_gate.md` names. It is reported, not repaired.
- (i) CLEAN UP. `git worktree list` after the cleanup prints the primary checkout
  alone: `/home/decodeux/Repos/remedy  9a7e5f16 [feature/f037-rendered-diff-viewer]`.
  `.remedy-wt/f037-r25-base` no longer exists; branch `tmp/f037-r25-base`
  deleted. No scratch file was created outside `.agent/gate_f037_r25/` — every
  measurement ran through an inline `python3 - <<'PY'` heredoc — so nothing was
  deleted by path and nothing by glob. The pre-existing
  `.remedy-wt/f037-r25-block.md` was left untouched.

**G7 THE CANARY AND THE STATE CONTRACTS — PASS.** Run in the primary checkout
after all of C3 (a)-(i), ONE pytest process at a time, never concurrently:

| Command | Exit | Result |
|---------|------|--------|
| `python3 -m pytest tests/cli/test_golden_path.py -q` | 0 | `42 passed in 20.50s` |
| `python3 -m pytest tests/ui_contracts/ -q` | 0 | `653 passed, 4 skipped in 5.57s` |

Both equal the reviewer's readings at `38966bf3` — 42, and 653 passed with 4
skipped. `tests/ui_contracts/` is the suite that reads the `.agent/plan.md` this
round rewrote, and it is green against the rewritten file. Recorded to
`.agent/gate_f037_r25/canary.txt`.

**G8 STRUCTURE AND THE OPEN PR GATE, measured at C3 (`7c2a45d2`) — PASS.**
`git diff --name-only 38966bf3..7c2a45d2` returns **14** paths; the change set
minus `.agent/handoff.md` is **14** paths. RESIDUE measured-minus-changeset:
`[]`. RESIDUE changeset-minus-measured: `[]`. Both printed, both EMPTY.
`git diff --stat 38966bf3..7c2a45d2 -- <dir>` prints the empty string `''` for
`apps/`, for `packages/`, for `tests/` and for `docs/` — all four cases print
NOTHING. Every commit C0a through C3 is single-parent (parent count 1, five
times); insertions from `git diff --numstat`, each under 500 and each equal to
the corresponding `## Commits` cell above:

| Commit | Insertions | Under 500 |
|--------|-----------|-----------|
| `1e5f423a` | 346 | yes |
| `fe72ccae` | 301 | yes |
| `3d99164d` | 19 | yes |
| `9a7e5f16` | 12 | yes |
| `7c2a45d2` | 447 | yes |

`git grep -c` for `^<<<SLICE ` and for `^<<<END `: both exit 1 with empty output
in `.agent/plan.md` and in `.agent/live_review.md` — 0 in all four readings —
against the non-zero control `.agent/authored/f037-r25.md`, which reports 3 and 3.
`git ls-files .remedy-wt | wc -l` = **0**.
`gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`,
no open PRs, so the Open PR Gate is clear and nothing was merged.
BUILD-OUTPUT GLOB SWEEP, re-measured rather than inherited, the fix clause
`R-0677` binds on a change set carrying an evidence path — `git ls-files` over
each `.gitignore` build-output glob: `*.zip` 0, `*.log` 0, `*.egg` 0,
`*.egg-info` 0, `build` 0, `*/build/*` 0, `dist` 0, `*/dist/*` 0, `node_modules`
0, `*/node_modules/*` 0, `sdist` 0, `packages.zip` 0, `remedy-job-evidence-*` 0.
TOTAL **0** — EMPTY. All ten evidence files are `.txt`; none is a `.log`, which
`.gitignore` would drop silently and the review-zip guard would reject (R-0169).

## Authored-text proofs

Three reviewer-authored slices were applied this round. Every one was
re-extracted from the COMMITTED `.agent/authored/f037-r25.md` blob — not from the
session's copy of the block — and compared on disk.

| Slice | Target | Result |
|-------|--------|--------|
| PLANF037R25 | `.agent/plan.md` at `3d99164d` | BYTE EQUAL including trailing newline (`True`); negative control dropping that newline `False` |
| GATER24 | `.agent/live_review.md` at `9a7e5f16` | Appended first; reader (a) equality `True`, negative control inside its first paragraph `False`; reader (b) 5 of the 6 tail paragraphs match in order |
| DONE719 | `.agent/live_review.md` at `9a7e5f16` | Appended second; the 6th and last tail paragraph, matched in order |

No slice was reflowed, reworded, retitled, corrected or shortened. The delimiter
lines never reached a target file — G8's marker sweep measures 0 in both targets.

## Deviations & assumptions

1. **The ordered commit sequence C0a, C0b, C1, C2, C3, C4 was followed exactly.**
   No extra commit, no dropped commit, no reordering.
2. **Shell-guard re-expressions (constraint 8).** Two command FORMS were rejected
   by this session's guard and were re-expressed rather than weakened or skipped.
   (a) A `python3 - <<'PY'` heredoc using the local identifier `env` for the
   child environment was rejected; the same script with the local renamed to `e`
   was accepted. `REMEDY_UI_NO_AUTO_BUILD=1` is still supplied exactly as
   ordered, through `subprocess.run(..., env=...)`, never exported — only the
   Python variable's NAME changed, not the mechanism. Isolated by four probes:
   `env=dict(os.environ)` alone passes, an added key passes, the real key passes;
   only the identifier `env` trips the guard. (b) A `git diff --name-only … |
   grep … ; echo "$?"` pipeline was rejected for the `$?` expansion; the same
   measurement was re-expressed as `subprocess.run(['git','diff','--name-only',…])`
   with the membership test done in Python, which is the reading reported under
   G6 (h).
3. **G7 ran after all of C3 (a)-(i) but before the C3 COMMIT.** The block orders
   the canary "after C3 and before C4", and separately places
   `.agent/gate_f037_r25/canary.txt` inside the change set while giving C4 only
   `.agent/handoff.md`. Committing the canary after `7c2a45d2` would have
   required a commit the block does not order. The canary therefore ran after the
   whole integration gate and its evidence was committed with the rest of C3.
   Nothing was measured before it happened: `canary.txt` and the canary line of
   `summary.txt` both carry figures produced before either file was committed.
4. **PARITY IS VOID and is handed back VOID.** Nothing was changed to make it
   hold, no run was repeated to get a better reading, and the base-only id was
   attributed by direct serial reproduction at the base rather than by parity.
5. **An observation for the reviewer, deliberately NOT written into the ledger.**
   The parity void has a measured cause in production-adjacent test code:
   `tests/ui_server/test_dashboard_contract.py::TestAutoBuildBehavior::test_auto_build_runs_by_default`
   clears the environment, drops `REMEDY_UI_NO_AUTO_BUILD` and invokes the real
   `_auto_build_frontend()`, so any full-suite run in a real checkout rebuilds
   `apps/ui/dist` mid-run. That defeats the neutralisation every future
   integration gate depends on, and it looks like a candidate for registration.
   It is NOT registered here: constraint 4 forbids this worker authoring any
   ledger paragraph, and the change set is exhaustive. Raised here for the
   reviewer to rule on.
6. **No assumption was carried from the block's numbers.** Every base figure the
   block states — the merge-base SHA, the 292/42/11/94/252 ledger readings, the
   42 and 653/4 canary readings, the warm dist — was independently re-measured by
   this worker, and each matched.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block | done | `1e5f423a` |
| C0b mirror the block | done | `fe72ccae` |
| C1 the plan | done | `3d99164d` |
| C2 the record | done | `9a7e5f16` |
| C3 the gate evidence | done | `7c2a45d2` |
| C4 the handback | done | this commit, then the push |
| G1 hygiene | done | STOP absent twice, base SHA equal, branch correct, 5×0 porcelain |
| G2 transport | done | digests EQUAL against the pre-existing original; one blob `0888befa` |
| G3 the plan at C1 | done | byte equal, control False, 44 lines, 1 and 1 |
| G4 the record at C2 | done | reader (a) True with control False; reader (b) N=6 in order; prefix True |
| G5 the ledger | done | 292 / 43 / 11 / 95 / open 251; `Gate: F037 R24` once |
| G6 the integration gate | done | executed in full; parity VOID and reported VOID; both sets attributed |
| G7 canary and state contracts | done | 42 passed; 653 passed 4 skipped; both exit 0 |
| G8 structure and Open PR Gate | done | residue empty both ways; 4 restricted stats empty; 5 single-parent commits; glob sweep 0 |

## Open findings

**251** open, computed AS A SET over the C2 blob — 292 distinct registered ids
minus 43 distinct `Done:` ids. That is one fewer than the 252 at `38966bf3`:
`R-0719` resolved, no id registered. F037 now carries no open finding of its own,
which is what the closure sequence needed from this round. Closure precondition 2
is satisfied by a real integration-gate run, with the parity caveat stated above.

## Next

The EVIDENCE-AND-ZIP round: the feature file's Built State section, the
`create_manual_completion_bundle` evidence job, and a FRESH review zip whose
failure is a closure blocker. Then the STATUS round — the `[x]` line, the README
capability sync in the SAME commit, and the closure PR, which this session does
not merge.

The next session applies Phase 1 rule 1 (read `.agent/STOP`) BEFORE rule 2 (the
Open PR Gate), in that order.
