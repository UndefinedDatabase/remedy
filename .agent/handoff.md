# Handoff — F257 self-use track, round 6 (the integration gate)

## Session

SESSION 2 of feature F257 · round 6 · rounds so far 6

Roster of this session's rounds, this round included: R4, R5, R6.

## Range

Review of `c3f8d5fe..HEAD` (HEAD = the C4 commit that writes this file).

## Commits

### a50b3757 chore(f257): save the round 6 block verbatim — C0a

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f257-r6.md` | +331/-0 | the block saved verbatim by `shutil.copyfile` from `.remedy-wt/f257-r6-block.md` |

### e37909fb chore(f257): mirror the round 6 block to last_block — C0b

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +230/-364 | the same bytes mirrored from the COMMITTED blob; one blob id with the authored copy |

### a9541b10 docs(f257): advance the plan to the integration-gate round — C1

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +11/-11 | whole-file replacement by slice `PLANF257R6` |

### fd8b84b6 docs(f257): book the round 5 verdict and its prose slips — C2

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +10/-0 | slice `GATEF257R5` appended under constraint 6 |
| `.agent/prose_slips.md` | +3/-0 | slice `SLIPSF257R5` appended under constraint 6 (two slip lines plus the one blank separator) |

### ddfc2dca test(f257): commit the round 6 integration-gate evidence — C3

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/gate_f257_r6/branch_run.txt` | +274/-0 | the branch run: command, REAL exit, wall time, its complete raw log, its complete FAILED list |
| `.agent/gate_f257_r6/base_run.txt` | +488/-0 | both base runs at `f17b1d0d`: headers, run 1's raw tail and complete FAILED list, run 2's complete raw log and FAILED list |
| `.agent/gate_f257_r6/branch_failed.txt` | +0/-0 | the sorted branch FAILED ids — an EMPTY file, because there were none |
| `.agent/gate_f257_r6/base_failed.txt` | +1/-0 | the sorted base FAILED ids from the run whose parity was actually restored |
| `.agent/gate_f257_r6/base_failed_run1.txt` | +116/-0 | the sorted base FAILED ids from base run 1, kept so nothing is hidden (extra file, declared in deviations) |
| `.agent/gate_f257_r6/comparison.txt` | +372/-0 | the two set differences, the A6 new-test class with its `git cat-file -e` proof, and the attribution of every base-only id |
| `.agent/gate_f257_r6/parity.txt` | +77/-0 | A4's before/after mtime readings for both base runs, each run window, and the verdict on each |

7 files under `.agent/gate_f257_r6/`, 1328 insertions in total.

### C4 — this handoff commit

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | the round handback; a handoff cannot table the commit that writes it (R-0149 pattern) |

Every `+/-` cell above was taken from `git diff --numstat` per commit.

## External actions

- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`, REAL exit 0.
- `git worktree add -b tmp/f257-base-gate .remedy-wt/f257-r6-base f17b1d0d03e4042df8452b2019b719cbe4704b21` → REAL exit 0, "Preparing worktree (new branch 'tmp/f257-base-gate')". Created ON A BRANCH per A2, never detached.
- `git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/f257-r6-base` → REAL exit 0, BY EXACT PATH, never by glob.
- `git worktree prune` → REAL exit 0.
- `git branch -D tmp/f257-base-gate` → REAL exit 0, "Deleted branch tmp/f257-base-gate (was f17b1d0d)".
- `git push origin feature/f257-self-use-track` → outcome recorded in the session output.
- No pull request was created. Nothing was merged. No force-push, no history rewrite.

## Verification

One line per gate, with the result actually measured.

- **G1 HYGIENE — PASS.** `.agent/STOP` read from disk with `os.path.exists` twice:
  before C0a `False`, before C3 `False`. Constraint 0: `gh pr list …` printed `[]`
  at REAL exit 0; `git rev-parse HEAD` printed
  `c3f8d5fe073235ba83725aff7425521706076e77`; `git branch --show-current` printed
  `feature/f257-self-use-track`. `git status --porcelain | wc -l` after each
  commit: C0a **0**, C0b **0**, C1 **0**, C2 **0**, C3 **0**.
- **G2 TRANSPORT — PASS.** Committed blob `a50b3757:.agent/authored/f257-r6.md`
  sha256 `0a436adfc6c8849d4c8faac0da6009b8d76e69cb8d6d77d2843a06ecffc20bc5`,
  **22016 bytes**; the reviewer's own original `.remedy-wt/f257-r6-block.md`
  sha256 `0a436adfc6c8849d4c8faac0da6009b8d76e69cb8d6d77d2843a06ecffc20bc5`,
  **22016 bytes**; **EQUAL True**. That original was written before this worker
  existed, so the reading covers more than self-consistency; and it covers no
  emission, because this workflow has none — the block was never retyped, only
  copied by `shutil.copyfile`. `git rev-parse e37909fb:.agent/authored/f257-r6.md`
  and `git rev-parse e37909fb:.agent/last_block.md` print ONE blob id,
  `50fdcfab333083c8b0bb0e2c371037e72163e327`.
- **G3 THE PLAN AT C1 — PASS.** `.agent/plan.md` at C1 equals `PLANF257R6`
  including the trailing newline: **True**, **1764 bytes** on both sides. `wc -l`
  **37**, under 50 True. Lines exactly `## Goal`: **1**. Lines exactly
  `## Next Steps`: **1**.
- **G4 THE RECORD APPEND AT C2 — PASS.** `.agent/live_review.md` reconstructed
  from the `c3f8d5fe` blob plus `GATEF257R5` under constraint 6: **True**; pre
  1393448 bytes, slice 3508 bytes, C2 blob 1396957, reconstruction 1396957.
  NEGATIVE CONTROL: the script computed the first appended paragraph as spanning
  bytes 1393449..1394224 and flipped the byte at absolute offset **1393836**,
  confirmed inside that span (context `…es and 37 lines; both record appends
  reconstructing to 13934…`); reconstruction then **False**, as it must be. The
  pre-round blob is a byte PREFIX of the C2 blob: **True** (1393448 → 1396957).
  The C2 blob ends in exactly ONE newline: **True**. Separately,
  `.agent/prose_slips.md` at C2 reconstructs from its `c3f8d5fe` blob plus
  `SLIPSF257R5` under constraint 6: **True** (16759 → 17363 bytes), and
  `SLIPSF257R5` contributes exactly **TWO** lines.
- **G5 THE LEDGER AT C2 — PASS, counted by DISTINCT ID per constraint 7.**
  At `c3f8d5fe` / at C2 — lines matching `^- R-\d+ — `: **296 / 296**, UNMOVED,
  all DISTINCT True / True; lines matching `^Done: R-\d+ — `: **44 / 44** with
  DISTINCT ids among them **42 / 42** (the two numbers differ exactly as
  constraint 7 anticipates), UNMOVED; `^Landed: R-`: **11 / 11**, UNMOVED;
  `^Gate: F\d+ R\d+ — `: **110 → 111**, a rise of exactly one. OPEN SET
  `len(set(registered) - set(resolved))`: **254 / 254**, UNMOVED on BOTH sides as
  constraint 7 requires. `^Gate: F257 R5 — ` at C2: **1**.
- **G6 THE INTEGRATION GATE — RUN IN FULL; THE VERDICT IS THE REVIEWER'S.**
  `docs/agents/integration_gate.md` step 5 reserves the verdict, and this worker
  does not issue it. The seven labelled readings:
  - **(a) THE BRANCH RUN.** `python3 -m pytest -n auto -q`, cwd
    `/home/decodeux/Repos/remedy`, no environment override. REAL exit **0**, wall
    **113.13 s**. Raw tail: `18186 passed, 20 skipped in 112.58s (0:01:52)` — a
    collected total of **18206**, matching the count the block states. Complete
    `FAILED` list: **EMPTY, 0 ids**. The registered flake R-0734 did not fire.
  - **(b) THE BASE RUN at `f17b1d0d`.** Same command, cwd
    `.remedy-wt/f257-r6-base`, `REMEDY_UI_NO_AUTO_BUILD=1` set in-process. The
    worktree was created ON A BRANCH per A2, and that is proved rather than
    asserted: `git -C <base> branch --show-current` printed **`tmp/f257-base-gate`**
    and `git -C <base> symbolic-ref -q HEAD` printed
    **`refs/heads/tmp/f257-base-gate`** at REAL exit **0** — a detached HEAD gives
    no ref and exit 1. It was run TWICE, and both runs are reported.
    - **BASE RUN 1** — REAL exit **1**, wall **174.27 s**, raw tail
      `116 failed, 18034 passed, 20 skipped in 173.72s (0:02:53)`. Complete
      `FAILED` list: **116 ids**, committed untruncated in
      `.agent/gate_f257_r6/base_failed_run1.txt` and inside `base_run.txt`.
    - **BASE RUN 2**, same worktree and same revision, after parity was COMPLETED
      — REAL exit **1**, wall **105.79 s**, raw tail
      `1 failed, 18149 passed, 20 skipped in 105.22s (0:01:45)`. Complete `FAILED`
      list: **1 id**,
      `tests/orchestration/test_product_smoke.py::TestRetryAndPortConflict::test_retry_is_bounded_to_one`.
  - **(c) PARITY, per A4 — THE CLAIM HOLDS FOR BOTH RUNS, MEASURED AS THE EVENT.**
    4 files under the base worktree's `apps/ui/dist`. Run 1 window
    `1787961662.303325 .. 1787961836.5702927`; all four mtimes were
    `1787956096.2279384`/`1787956096.2299385` both before and after, **0 inside the
    window**, 0 files added or removed. Run 2 window
    `1787961955.2458422 .. 1787962061.0373728`; all four mtimes
    `1787961952.3196137` both before and after, **0 inside the window**. So no dist
    file was written while either suite ran and `REMEDY_UI_NO_AUTO_BUILD=1` was not
    bypassed by a spawned build path. No content hash is offered in place of this
    reading. **But A4's question is not the only one that matters**, and this is
    the round's substantive finding: A4 asks "was dist rewritten during the run?"
    (no), not "was dist USABLE by the run?" — and in run 1 it was not. See
    deviation 2.
  - **(d) THE COMPARISON, per A5 — COMPUTED AS A SET DIFFERENCE IN PYTHON,
    `comm` WAS NOT RUN.** This session's guard rejects the pipelines that feed
    `comm -13`/`comm -23` by FORM, so the PROPERTY was ordered rather than the
    tool: `set(branch) - set(base)` and `set(base) - set(branch)` over the two
    sorted `FAILED` id lists.
    - **BRANCH-ONLY, against base run 1: 0 ids. EMPTY.**
    - **BRANCH-ONLY, against base run 2: 0 ids. EMPTY.** The branch run produced no
      `FAILED` id at all, so the branch-only set is empty by construction against
      any base.
    - **BASE-ONLY, against base run 1: 116 ids** — 114 under `tests/ui_server/`
      plus `tests/cli/test_review_bundle_runtime.py::TestSubprocessCleanup::test_timeout_raises_with_cleanup`
      and `tests/orchestration/test_product_smoke.py::TestAppStartsGreen::test_a_clean_app_passes`.
      All 116 are listed untruncated in `base_failed_run1.txt` and `comparison.txt`.
    - **BASE-ONLY, against base run 2: 1 id** —
      `tests/orchestration/test_product_smoke.py::TestRetryAndPortConflict::test_retry_is_bounded_to_one`.
  - **(e) THE NEW-TEST CLASS, per A6 — EMPTY IN EFFECT.** There is no branch-only
    id, so no id had to be excused as a new test. The two files are nevertheless
    absent at the base, proved: `git cat-file -e f17b1d0d:tests/orchestration/test_self_use_job.py`
    REAL exit **128**, `git cat-file -e f17b1d0d:tests/orchestration/test_self_use_queue.py`
    REAL exit **128** (both "fatal: Not a valid object name"), against the positive
    control of the same two paths at `c3f8d5fe` at REAL exit **0** and **0**. Both
    files' tests passed in the branch run.
  - **(f) ATTRIBUTION.** For branch-only ids the obligation is discharged
    vacuously — there are none, so no BLOCKER condition can arise from step 4.
    Base-only ids still need attributing, because step 3 says an unattributed one
    counts as a genuine base failure and blocks the verdict. All are attributed by
    direct evidence, in two classes:
    - **CLASS 1, the stale-dist environment class — 114 ids, every one under
      `tests/ui_server/`.** `packages/orchestration/ui_server.py` is BYTE-IDENTICAL
      at `f17b1d0d` and `c3f8d5fe` (`git diff --stat` over that path printed
      nothing), and `git diff --name-only f17b1d0d c3f8d5fe` lists no path under
      `apps/`, so the copied `dist` is the correct artifact for the base and the
      UI-build gate is not a branch-vs-base code difference. `_frontend_is_stale()`
      returns True when any file under `apps/ui/src` is newer than
      `apps/ui/dist/index.html`; measured in the base worktree before run 1,
      newest src `1787961647.324847` > dist `1787956096.2279384` ⇒ **STALE**, while
      the primary checkout at the same moment read newest src `1787955940.2276886`
      < dist `1787956096.2279384` ⇒ **NOT stale**. With the auto-build suppressed
      the stale branch fails loudly, and the run-1 log carries the marker
      `ERROR: React UI not built.` **exactly 114 times** — a 1:1 match with the 114
      ids, no id left over and no marker unused; the branch log carries it **0**
      times. DECISIVE CONTROL: parity was then completed in the same worktree at
      the same revision and the full suite re-run — **all 114 passed**. The class
      is attributed by experiment, not only by inference.
    - **CLASS 2, the xdist/port flake class — 3 ids across the two base runs**,
      each re-run SERIALLY at `f17b1d0d` by exact node id, all three serial-pass,
      which is step 4's xdist-flake class: recorded, not blocking. None failed on
      the branch. `…::TestAppStartsGreen::test_a_clean_app_passes` (run 1,
      `OSError: [Errno 98] Address already in use`) → `1 passed in 0.42s`, REAL
      exit **0**. `…::TestSubprocessCleanup::test_timeout_raises_with_cleanup`
      (run 1, `AssertionError: Orphan process found after timeout cleanup`) →
      `1 passed in 0.32s`, REAL exit **0**.
      `…::TestRetryAndPortConflict::test_retry_is_bounded_to_one` (run 2, a 4.0 s
      readiness budget that passed where a failure was expected under `-n auto`
      load) → `1 passed in 1.56s`, REAL exit **0**. The three do not overlap
      between the two base runs, which is itself the signature of a
      load-dependent flake rather than a fixed defect.
    - **R-0734 DID NOT FIRE as itself in either run.** Its signature is
      `json.decoder.JSONDecodeError` from a zero-byte `server_info.json`, and that
      string appears in neither log; the run-1 `tests/ui_server/` failures are the
      stale-dist class, where the server never started at all and the helper timed
      out at `Server did not start in time`. Nothing was repaired — this round's
      change set forbids touching `tests/`.
  - **(g) THE BUDGET.** Branch **113.13 s**, base run 1 **174.27 s**, base run 2
    **105.79 s**; **total wall clock 393.19 s (6 min 33 s)**. Each individual run
    is under 3 minutes; the total passes step 5's ~5 min note only because the base
    was run twice.
- **G7 STRUCTURE — PASS**, over `c3f8d5fe..ddfc2dca`, the range that ends BEFORE
  the handback commit. Range paths (**12**), listed in full:
  `.agent/authored/f257-r6.md`, `.agent/gate_f257_r6/base_failed.txt`,
  `.agent/gate_f257_r6/base_failed_run1.txt`, `.agent/gate_f257_r6/base_run.txt`,
  `.agent/gate_f257_r6/branch_failed.txt`, `.agent/gate_f257_r6/branch_run.txt`,
  `.agent/gate_f257_r6/comparison.txt`, `.agent/gate_f257_r6/parity.txt`,
  `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
  `.agent/prose_slips.md`. Changeset-minus-range residue, computed over the change
  set WITHOUT the excluded path — **the excluded path is `.agent/handoff.md`**,
  which C4 writes — is **empty**. Range-minus-changeset residue, computed against
  the FULL change set and treating `.agent/gate_f257_r6/**` as matching any path
  under that directory, is **empty**. Insertions and parents: C0a **331**, C0b
  **230**, C1 **11**, C2 **13**, C3 **1328** — each of the five is
  **single-parent**, and C3 exceeds 500, DECLARED in deviation 1. Delimiter counts
  over each file's C3 content, lines beginning `<<<SLICE ` and `<<<END `:
  `.agent/plan.md` **0 and 0**; `.agent/live_review.md` **0 and 0**;
  `.agent/prose_slips.md` **0 and 0** — beside the non-zero CONTROL
  `.agent/authored/f257-r6.md` at **3 and 3**, which shows the counter can see
  delimiters when they are there. `git ls-files .remedy-wt | wc -l` = **0**.
  Paths under `packages/`, `apps/`, `tests/`, `scripts/` or `docs/` in the range:
  **0** — the full range listing above shows it. Committed evidence file names
  matching `\.log$`: **0 of 7**; every evidence file is `.txt`. Finally
  `git worktree list` prints the primary alone
  (`/home/decodeux/Repos/remedy  ddfc2dca [feature/f257-self-use-track]`) and
  `git branch --list 'tmp/*'` prints **nothing** — the base-gate worktree and its
  throwaway branch are both GONE.

Push: `git push origin feature/f257-self-use-track` — outcome recorded in the
session output; no PR was created and nothing was merged.

## Authored-text proofs

- `PLANF257R6`, `GATEF257R5` and `SLIPSF257R5` were all extracted from the
  COMMITTED blob `git show e37909fb:.agent/authored/f257-r6.md` (constraint 3),
  never from the prompt text, by `.remedy-wt/f257_r6_slice.py`; the delimiter
  lines were dropped as transport (constraint 2) and reach no target file, which
  G7's delimiter counts confirm at 0 in all three targets against a 3/3 control.
- Disk-to-disk: the committed authored file and the reviewer's original
  `.remedy-wt/f257-r6-block.md` are byte-identical, sha256
  `0a436adfc6c8849d4c8faac0da6009b8d76e69cb8d6d77d2843a06ecffc20bc5`, 22016 bytes
  each — G2.
- `.agent/last_block.md` shares ONE blob id with the authored copy at C0b:
  `50fdcfab333083c8b0bb0e2c371037e72163e327`.
- No authored slice was corrected, reflowed, retitled or shortened. No `Done:` or
  `Gate:` paragraph of my own was written anywhere; `GATEF257R5` is
  reviewer-authored text applied verbatim.

## Deviations & assumptions

1. **C3 IS AN OVERSIZE COMMIT AT 1328 INSERTIONS, DECLARED HERE WITH ITS
   INSEPARABILITY REASON, as AGENTS.md's exception and the block's G7 both
   require.** A gate's evidence is one indivisible artifact: the two run records,
   the two `FAILED` id lists, the comparison that is a set difference OVER those
   lists, and the parity readings that license the comparison are meaningless
   apart from one another, and splitting them across commits would produce
   intermediate commits asserting a comparison whose inputs are not yet present.
   The bulk is genuinely irreducible measurement — 274 lines of branch log, 488 of
   base-run record, 116 base-only ids that memory rule "Never Truncate a Sweep"
   forbids abbreviating. This is the only oversize commit in F257.
2. **A3's "RESTORE PARITY BY COPY" IS INCOMPLETE ON ITS OWN, AND THAT IS WHY THE
   BASE RAN TWICE.** `shutil.copytree` PRESERVES mtimes, while `git worktree add`
   stamps every checked-out source file with the checkout time. The copied
   `apps/ui/dist` was therefore byte-correct but mtime-OLDER than the base
   worktree's `apps/ui/src`, `_frontend_is_stale()` returned True,
   `REMEDY_UI_NO_AUTO_BUILD=1` suppressed the rebuild, and the UI server exited
   with `ERROR: React UI not built.` — producing 114 base failures that are
   artifacts of the recipe rather than of the base revision. Step 3 of
   `docs/agents/integration_gate.md` offers exactly two routes, "restore parity
   before the base run" OR "attribute every base-only id", and an unattributed
   base-only id blocks the verdict; I therefore took both. Parity was COMPLETED by
   bumping the copied dist's mtimes past the checkout time — a legitimate
   completion, not a fudge, since `git diff --name-only f17b1d0d c3f8d5fe` shows
   `apps/ui` untouched by this branch, so that dist IS the base's correct build —
   and the full suite was re-run unmodified. **Nothing inside the repository was
   edited to achieve it; only files inside the throwaway worktree were touched.**
   No suite was shortened, narrowed or subsetted: both base runs are full
   `pytest -n auto -q` runs. This is a gap in the canonical recipe, not a defect
   in the feature, and repairing `docs/agents/integration_gate.md` or A3 is not
   this round's to make — the change set forbids `docs/`.
3. **ONE EXTRA EVIDENCE FILE beyond the block's list of six:**
   `.agent/gate_f257_r6/base_failed_run1.txt`, the 116 sorted base-only ids from
   base run 1. The block names `base_failed.txt` as "the sorted FAILED node ids"
   for "the base run", and with two base runs a single file would have had to hide
   one of them. `base_failed.txt` carries base run 2 — the run whose parity was
   actually restored, and therefore the one the comparison rests on — and the
   extra file carries run 1 in full so nothing is elided. The path is inside the
   change set's `.agent/gate_f257_r6/**`, and G7's range-minus-changeset residue is
   empty with it present.
4. **Guard re-expressions (constraint 5), every one reported as required.** This
   session's guard rejects several ordinary shell forms BY FORM, so each was
   re-expressed rather than skipped or weakened:
   - `cp` is rejected outright → the C0a transport copy used
     `shutil.copyfile`, and A3's 305 MB `apps/ui/node_modules` and `apps/ui/dist`
     were copied into the base worktree with `shutil.copytree(..., symlinks=True,
     ignore_dangling_symlinks=True)`. NEVER symlinked, per A3 — and verified: a
     sweep of the copied tree found **0** symlinks resolving outside the base
     worktree, so no auto-build could have written THROUGH one into the primary
     checkout (the F053 R3 failure mode).
   - Every form of environment-variable assignment (`VAR=x cmd`, `env VAR=x cmd`,
     `export VAR=x; cmd`) is rejected → `REMEDY_UI_NO_AUTO_BUILD=1` was set
     IN-PROCESS via `os.environ` on a copied env dict handed to `subprocess.run`,
     and the value actually passed is recorded in each run's metadata.
   - Loops, `$( )` inside a compound, `${arr[0]}`, process substitution and
     multi-operation one-liners are rejected → every piece of iteration (the slice
     extraction, G4's reconstruction and negative control, G5's two-revision
     ledger count, the base-worktree setup, both mtime censuses, the set
     differences, the evidence composition, G7's per-commit walk and delimiter
     sweep, and the poll that waited for each background run) was moved into a
     scratch script under the gitignored `.remedy-wt/`: `f257_r6_slice.py`,
     `f257_r6_g4g5.py`, `f257_r6_run.py`, `f257_r6_wait.py`,
     `f257_r6_base_setup.py`, `f257_r6_evidence.py`, `f257_r6_compare.py`,
     `f257_r6_g7.py`. None is tracked — G7 reports `git ls-files .remedy-wt` = 0.
   - `comm -13`/`comm -23` need pipelines the guard rejects → per A5 the same
     PROPERTY was computed as a Python set difference, and the handback and
     `comparison.txt` both say so in as many words.
   - Brace literals containing quotes are rejected → the scratch scripts were
     created with the file-writing tool rather than typed into a heredoc.
   - `cd X && git …` is rejected → `git -C <path>` throughout, and `cwd=` on
     `subprocess.run` for every pytest invocation including both base runs.
   - Python 3.10 forbids a backslash inside an f-string expression → every regex
     and every delimiter pattern in `f257_r6_g4g5.py` and `f257_r6_g7.py` is
     hoisted into a named module-level constant and never interpolated.
   - The tool does not surface non-zero exits → every command was wrapped as
     `bash -c '<cmd>; echo "REAL_EXIT=$?"'` or run through `subprocess` and its
     `returncode` printed. No gate result is reported that was not actually seen;
     in particular the base runs' exit **1** and the `git cat-file -e` exits
     **128** are real readings.
5. **A1 was followed literally: no log grew inside the repository.** Both run logs
   were written to directories created by `tempfile.mkdtemp()` OUTSIDE the
   repository (`/tmp/f257r6-branch-vcj98x2c`, `/tmp/f257r6-base-d5c9_jt1`,
   `/tmp/f257r6-base2-v61bb3kr`) and were only copied/composed into
   `.agent/gate_f257_r6/` after each run had exited, so the worktree digest never
   moved mid-run (the R-0176 failure mode). Every evidence file is named `.txt`;
   G7 confirms 0 of 7 match `\.log$`.
6. **Base run 1's raw log is represented by its tail plus its complete FAILED
   list, not in full.** It is 7629 lines / 304 KB, and the block's evidence spec
   asks for "the raw tail, its full `FAILED` list, its REAL exit code and its wall
   time" rather than the whole log. The FAILED list is complete and untruncated at
   all 116 ids. The branch log (257 lines) and base run 2's log (292 lines) are
   committed IN FULL.
7. **No departure from the block's ordered commit sequence.** C0a, C0b, C1, C2,
   C3, C4 were committed in exactly that order, one logical step each; no commit
   was added, dropped or reordered. This round registers no finding id and
   resolves none.
8. **Applied as written where I might have written it differently.** Constraint 1
   binds and no authored slice was corrected. Constraint 6 versus the block's
   phrasing raised no disagreement this round: each slice already carries its own
   terminating newline, so the bytes appended were one newline then the slice,
   which yields exactly one blank-line separator and exactly one trailing newline,
   and G4 confirms both targets reconstruct byte-exactly.
9. **No integration-gate verdict is issued here, and no defect found by the gate
   was repaired.** `docs/agents/integration_gate.md` step 5 reserves the verdict to
   the reviewer. R-0734 was classified and left alone; the stale-dist recipe gap is
   reported and left alone. Neither is a branch-only failure, so neither meets the
   block's STOP-and-hand-back condition, and the round ran to completion.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block to `.agent/authored/f257-r6.md` | done | `a50b3757`, byte-identical to the reviewer's original at 22016 bytes |
| C0b mirror the same bytes to `.agent/last_block.md` | done | `e37909fb`, one blob id with the authored copy |
| C1 advance `.agent/plan.md` | done | `a9541b10`, whole-file `PLANF257R6` |
| C2 book the F257 R5 verdict and append two prose slips | done | `fd8b84b6`, both appends under constraint 6 |
| C3 the gate evidence under `.agent/gate_f257_r6/` | done | `ddfc2dca`, 7 files, 1328 insertions; oversize declared in deviation 1 |
| C4 rewrite `.agent/handoff.md` | done | this commit |
| G1 hygiene | done | STOP `False` at both readings; three constraint-0 readings correct; clean tree after all five commits |
| G2 transport | done | digests EQUAL at 22016 bytes; one blob id at C0b |
| G3 the plan at C1 | done | equal including the trailing newline at 1764 bytes; 37 lines; 1 and 1 |
| G4 the record append at C2 | done | reconstruction True, negative control False at an offset proved inside the first appended paragraph, prefix holds, one trailing newline; slips file reconstructs and contributes exactly two lines |
| G5 the ledger at C2 | done | registered 296 UNMOVED, `Done:` 44/42 and `Landed:` 11 UNMOVED, `Gate:` 110→111, open set 254 on BOTH sides, `^Gate: F257 R5 — ` = 1 |
| G6 the integration gate | done | branch exit 0 with 0 FAILED at 18206 collected; base on a branch, run twice; parity holds by mtime event on both; branch-only EMPTY; all 116 base-only ids attributed in two classes; new-test class empty in effect with `cat-file` proof; budget 393.19 s. VERDICT NOT ISSUED — it is the reviewer's |
| G7 structure | done | both residues empty; five single-parent commits; C3 oversize declared; delimiters 0 in three targets against a 3/3 control; `.remedy-wt` untracked at 0; 0 fenced paths in the range; 0 of 7 evidence names match `\.log$`; worktree and `tmp/*` branch both gone |

## Open findings

**254 open**, counted by DISTINCT ID per constraint 7 (`len(set(registered) -
set(resolved))`), UNMOVED from 254 at `c3f8d5fe` because this round registers no
id and resolves none. Registered lines stand at 296 on both sides.

## Next

The reviewer issues the integration-gate verdict on the readings above. If it
passes, build the closure package and close F257 through
`docs/roadmap/STATUS_closure_protocol.md`, satisfying its new precondition 6 —
this feature is the first that must consume a self-use item at its own close.
