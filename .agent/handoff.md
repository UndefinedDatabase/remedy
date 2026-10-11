# Handback — F297 round 11: book round 10, land T025 (R-1241), the structural step

## Session

SESSION 2 of feature F297 · round 11 · rounds so far 11

Context self-assessment: the session verified the block and all 17 Bundle-listed prepared files'
digests before any write, read every diff in full against the current tree (including the dry
files' prefixes against the three commit-sized production files via `git diff --no-index
--numstat` and a small python3 tail check for the two large `.agent/` record files) before
staging, and executed the three commits and six gates in one uninterrupted pass with no retries;
context remains comfortable at handback.

Fortschritt: ~93 % (T001 to T025 landed · the closure sequence open) — Schätzung

## Range

Review of `08c7943fe`..`HEAD`.

## Commits

### 39844ea11 F297 R11 C1: book round 10 and the resolutions of R-1240 and R-1249, DECISION F297 D12

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f297-r11.md` | +128/-0 | saved copy of the reviewer's block, byte-equal to `.remedy-wt/f297-r11/prep/block.md` |
| `.agent/decisions.md` | +12/-0 | DECISION F297 D12: how round 11 takes the structural step and repairs R-1241 |
| `.agent/live_review.md` | +6/-0 | appended the `Gate: F297 R10` paragraph (VERDICT PASS) and the `Done:` paragraphs for R-1240 and R-1249 |
| `.agent/plan.md` | +9/-9 | rewritten in full for F297 round 11 |

### b50eabc80 F297 R11 C2: the burn alarm's trip handler leaves run_job for job_burn, and the ledger's rows and pins fall by what moved (R-1241, structural)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | +2/-3 | `run_job`'s row falls from 1652 to 1559 lines; the deleted `run_job._stop_check` row (186 lines) removed; `pingpong_job.py`'s file row falls from 5719 to 5626 |
| `packages/orchestration/job_burn.py` | +78/-5 | `record_burn_trip`, moved whole from `run_job._stop_check`, with the module docstring corrected to describe it instead of the old inline handler |
| `packages/orchestration/pingpong_job.py` | +11/-104 | the ~100-line nested trip handler replaced by one call to `job_burn.record_burn_trip`, its error signal translated back into the existing `_PauseSignal` |
| `tests/test_structure_ratchet.py` | +3/-3 | `MAX_FUNCTION_ROWS` 161→160, `MAX_FUNCTION_LINES` 31027→30748, `MAX_FILE_LINES` 74916→74823, matching the ledger's new rows exactly |

### 1c49a2872 F297 R11 C3: a job's burn samples are kept in its record, so a continued job keeps its baseline (R-1241)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/cost-anomaly-alarm-v1.md` | +4/-3 | says the samples are kept in the job's record, under `burn_samples` in its metadata, and drops the deliberate absence that said samples do not survive a stop and relaunch |
| `packages/orchestration/job_burn.py` | +48/-6 | `BURN_SAMPLES_KEY`, `_kept_sample` (a torn-entry-safe reader), and `JobBurnMonitor` taking an optional `store` (the job's metadata): it reads kept samples back on construction and appends every new one to the store as it records a call |
| `packages/orchestration/pingpong_job.py` | +1/-1 | the monitor is built with the job's own metadata dict as its store |
| `tests/orchestration/test_job_burn.py` | +48/-0 | three new tests: a monitor keeps every call in its store and a new one reads them back; a kept sample that is not one is left out and never raises; a paused job's record keeps its samples and a continued monitor reads the same trip |

### this commit F297 R11 C4: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file (self-reference rule, docs/agents/handback_template.md) |

## External actions

None before this commit. `git push origin feature/f297-findings-paydown-v7` after this commit,
reported below with the post-push `git rev-parse HEAD origin/feature/f297-findings-paydown-v7`. No
`gh` command run this round; no PR opened, merged or touched; no worktree added or removed.

## Verification

**Preconditions (before C1):** `git status --porcelain` empty; `git rev-parse HEAD` read
`08c7943feba3e341697ef01e92bbca5fb085e995`, the required base; `git branch --show-current` read
`feature/f297-findings-paydown-v7`; `.agent/STOP` absent throughout the round.

**Block and prepared-file digests (before any write):** `wc -l
.remedy-wt/f297-r11/prep/block.md` read `128`; `sha256sum` read
`8854f682268c6ccaa45a0b16b3eee1f8bcbc28280a9f6ce54de97a5935308bbe` — both equal to the values the
prompt delivered. All 17 other Bundle-listed prepared files (10 `dry-*` files, 4 `c2-*` files, 2
`append-*.txt` files, `verify.py`, `run_selection.py` and `selection.txt` — 17 counting both
`verify.py`/`run_selection.py` once each) hashed via `sha256sum`: every one matched the block's
stated digest exactly. Every file's numstat against the file it replaces was predicted with `git
diff --no-index --numstat` (current tree file vs. `c2-*`, `c2-*` vs. `dry-*`, or current tree file
vs. `dry-*` for the C1 `.agent/` files) before any copy, and every reading matched the block's
stated numstat per path exactly: C1 `6 0` / `12 0` / `9 9` / (block.md's own 128 lines for the new
authored file); C2 `78 5` / `11 104` / `2 3` / `3 3`; C3 `48 6` / `1 1` / `48 0` / `4 3`. The two
appended tails (`.agent/live_review.md`'s 6 new lines, `.agent/decisions.md`'s 12 new lines) were
confirmed to equal `append-live_review.txt` and `append-decisions.txt` exactly via a python3 script
(`check_tails.py`) comparing `dry-*.md`'s tail slice to each `append-*.txt` file: both `True`.

**Content review before staging:** every diff was read in full with `diff -u` against the current
tree before the corresponding `git add`: the C1 diffs (the `Gate: F297 R10` paragraph plus the two
`Done:` paragraphs for R-1240 and R-1249 appended to `live_review.md`; DECISION F297 D12's full
text appended to `decisions.md`; `plan.md` rewritten for round 11); the C2 diffs (the trip
handler's ~100 lines removed from `pingpong_job.py`'s `_stop_check` and replaced by one call into
the new `record_burn_trip` in `job_burn.py`; the ledger's two rows lowered and one row deleted; the
ratchet's three constants lowered to match); the C3 diffs (`BURN_SAMPLES_KEY`, `_kept_sample`, and
`JobBurnMonitor`'s new `store` parameter in `job_burn.py`; the one-argument change at
`pingpong_job.py`'s construction site; the cost-anomaly-alarm page's new paragraph and dropped
deliberate-absence bullet; the three new tests in `test_job_burn.py`). Content matched the block's
descriptions and DECISION F297 D12's text exactly in every case.

**C1:** `python3 -I c1_copy.py` copied the three `dry-*` whole files and the block to
`.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/authored/f297-r11.md`;
each printed `cmp_equal= True`. `.agent/authored/f297-r11.md` read `wc -l` 128 and the same sha256
as `block.md`. `git branch --show-current` read `feature/f297-findings-paydown-v7` before staging.
`git diff --cached --numstat` read exactly `128 0 .agent/authored/f297-r11.md`,
`12 0 .agent/decisions.md`, `6 0 .agent/live_review.md`, `9 9 .agent/plan.md` — matching the
block's required readings exactly, no other path staged.

**C2:** `python3 -I c2_copy.py` copied the four `c2-*` files; each printed `cmp_equal= True`. `git
diff --cached --numstat` read `2 3 docs/system/structure-ledger-v1.md`,
`78 5 packages/orchestration/job_burn.py`, `11 104 packages/orchestration/pingpong_job.py`,
`3 3 tests/test_structure_ratchet.py` — matching the block exactly, no other path staged. `git
branch --show-current` read `feature/f297-findings-paydown-v7` before staging.

**C3:** `python3 -I c3_copy.py` copied the four `dry-*` files; each printed `cmp_equal= True`. `git
diff --cached --numstat` read `4 3 docs/system/cost-anomaly-alarm-v1.md`,
`48 6 packages/orchestration/job_burn.py`, `1 1 packages/orchestration/pingpong_job.py`,
`48 0 tests/orchestration/test_job_burn.py` — matching the block exactly, no other path staged.
`git branch --show-current` read `feature/f297-findings-paydown-v7` before staging.

**Gate 1:** `git status --porcelain` → empty, exit 0. Then
`python3 .remedy-wt/f297-r11/prep/verify.py /home/decodeux/Repos/remedy` → every line `True` (10
file-equality checks, 2 C2-snapshot checks, 2 base-plus-slice checks), last line `ALL True`, exit
0.

**Gate 2:** `python3 -m ruff check packages/orchestration/job_burn.py
packages/orchestration/pingpong_job.py tests/orchestration/test_job_burn.py
tests/test_structure_ratchet.py` → `All checks passed!`, exit 0.

**Gate 3:** `python3 .remedy-wt/f297-r11/prep/run_selection.py /home/decodeux/Repos/remedy` → 3
SKIPPED lines (`tests/test_agent_tooling.py:43` D12 quarantine, `tests/test_install_smoke.py:175`
opt-in install smoke, `tests/test_repair_context_reviewer_memory.py:257` UI source not found), no
FAILED or ERROR line, no `process(es) behind` line, summary `5790 passed, 3 skipped in 57.99s`,
`exit 0` — matching the reviewer's dry-tree reading of `5790 passed, 3 skipped` named in the
prompt exactly, same three SKIPPED lines.

**Gate 4:** `python3 -m apps.cli.main integrity check --json` →
`{"check_count": 6, "fail_count": 0, "ok": true, "passed": true, ...}`, all six checks `pass`
(`handler_import` 184 handlers, `live_review_verdict` last Gate PASS, `plan_consistency`
unchecked=0, `relevant_untracked` untracked=0 relevant=0, `repo_root_hygiene` clean,
`high_blockers_open` none open), exit 0.

**Gate 5:**
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1235', 'R-1241', 'R-1246', 'R-1248', 'R-1251']` — the 5 ids in the required order, exit 0.

**Gate 6:** `git log --format=%s 08c7943fe..HEAD` → the three subjects of C3, C2 and C1, newest
first, exactly as required, exit 0.

No mutation red-proof was run (amend0930-test-load rule 4; the block's own Constraints also forbid
it this round). No full suite was run beyond the selection gate 3 names; `REMEDY_TEST_MAX_WORKERS`
was never set. No two test commands ran at once; each gate ran exactly once.

## Authored-text proofs

Reviewer-authored texts applied this round, each by a python3 copy script followed by
`filecmp.cmp` (disk-to-disk, not shallow), all read `True`; the 18-file digest pre-check (above,
block.md plus the 17 other Bundle-listed files) additionally confirmed every prepared source's
sha256 against the Bundle's stated values before any copy:

1. `.remedy-wt/f297-r11/prep/block.md` → `.agent/authored/f297-r11.md`: cmp equal, 128 lines both,
   sha256 `8854f682268c6ccaa45a0b16b3eee1f8bcbc28280a9f6ce54de97a5935308bbe` both.
2. `dry-live_review.md` → `.agent/live_review.md`: cmp equal, 296 lines both.
3. `dry-decisions.md` → `.agent/decisions.md`: cmp equal, 29200 lines both.
4. `dry-plan.md` → `.agent/plan.md`: cmp equal, 26 lines both.
5. `c2-job_burn.py` → `packages/orchestration/job_burn.py` (C2), then `dry-job_burn.py` over the
   same path (C3): cmp equal at each step; final file 308 lines.
6. `c2-pingpong_job.py` → `packages/orchestration/pingpong_job.py` (C2), then
   `dry-pingpong_job.py` over the same path (C3): cmp equal at each step; final file 5626 lines.
7. `c2-structure-ledger-v1.md` → `docs/system/structure-ledger-v1.md`: cmp equal, 398 lines both.
8. `c2-test_structure_ratchet.py` → `tests/test_structure_ratchet.py`: cmp equal, 181 lines both.
9. `dry-test_job_burn.py` → `tests/orchestration/test_job_burn.py`: cmp equal, 741 lines both.
10. `dry-cost-anomaly-alarm-v1.md` → `docs/system/cost-anomaly-alarm-v1.md`: cmp equal, 89 lines
    both.

The two `append-*.txt` files (`append-live_review.txt`, `append-decisions.txt`) were listed in the
Bundle and digest-checked (both `True`), but C1 orders copying the two whole `dry-*.md` files,
which already carry that content baked in; the `append-*.txt` files were not applied separately,
and nothing in the block calls for that (same note as F297's prior rounds' handbacks).

## Deviations & assumptions

1. **Shell shape.** Most read-only checks this round (`git status`, `git branch --show-current`,
   `wc -l`, `sha256sum`, the ruff invocation, `integrity check`, the gate-1/gate-3/gate-4/gate-5
   script invocations, the `git diff --no-index --numstat` digest-prediction calls) were run with
   the working directory set to `/home/decodeux/Repos/remedy` rather than `git -C ...` as the
   top-level task instructions prefer; none were refused by the sandbox. Every commit, every staged
   `git add`/`git diff --cached`, and gate 6's `git log` were run with explicit
   `git -C /home/decodeux/Repos/remedy`. All three copy steps used the mandated python3 scripts
   under `.remedy-wt/f297-r11-worker/`. (Same note as F297's prior rounds' handbacks.)
2. **Staging.** Each commit's staging used `git add -- <explicit path list>` with no `-A` flag.
3. **Digest-prediction tooling.** Rather than a bespoke prefix-equality script over the three large
   `.agent/` files (as round 10 used), this round predicted every path's numstat with
   `git diff --no-index --numstat` between the current-tree file (or the matching `c2-*` snapshot)
   and the prepared file, for every pair the block names, before any copy; every reading matched
   the block's stated numstat exactly. The two appended tails of `.agent/live_review.md` and
   `.agent/decisions.md` were confirmed against `append-live_review.txt` and
   `append-decisions.txt` by a small python3 script (`check_tails.py`) rather than a plain `diff`,
   to avoid printing a multi-thousand-line file inline.

No other deviation. No mutation runs; no full suite; no two test commands run at once; no file
written outside the paths each commit names; no write under `.remedy-wt/f297-r11/`; no pull
request opened; no `main` touch; `REMEDY_TEST_MAX_WORKERS` never set; `.agent/STOP` did not appear
during the round.

## Next

1. Phase 1 rule 1: check `.agent/STOP` first; follow whatever it orders before anything else.
2. Phase 1 rule 2: the Open PR Gate.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. The next round's first commit books round 11's verdict and the resolution of R-1241.
5. The closure sequence.

Operator questions open: 2.
Open findings: 5, all owned by F297 except R-1248, owned by F305, and R-1251, owned by the next
findings paydown.

## For the operator, in plain sentences

This round made two kinds of change. First, it took a block of code that handles one specific
alarm inside the project — the one that watches a running piece of work for spending too fast —
and moved it to a better-organized place nearby, right next to the rest of that alarm's own logic
instead of buried inside a much larger piece of code that does many other things. That move
changed nothing about what happens when the alarm trips; it only put the code where it belongs,
which is the kind of tidying the project checks for on its own so that its largest pieces never
quietly grow back. Second, it changed what happens once that alarm has paused a piece of work and
someone later picks it back up, or once the work has simply stopped and is later picked back up:
before this change, picking it back up meant judging only the activity that happened after the
restart, as though nothing earlier had counted; now, picking it back up means judging everything
that happened in that run, both before and after the pause or stop, together, which is what the
alarm was always meant to do. To make that possible, the record the project keeps for each piece of
work now carries one small note for every step the alarm counts. Nothing else a person watching the
project day to day will notice has changed.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | book round 10, resolutions of R-1240 and R-1249, DECISION F297 D12; numstat matched exactly |
| C2 | done | T025 first half landed: the burn alarm's trip handler moved from `run_job._stop_check` into `record_burn_trip` in `job_burn.py`, behaviour unchanged, ledger rows and ratchet pins lowered by what moved; numstat and diff content matched exactly |
| C3 | done | T025 second half landed (R-1241): a job's burn samples are kept in its record under `burn_samples`, so a continued job keeps its earlier baseline; the cost-anomaly-alarm page says so; numstat and diff content matched exactly |
| C4 | done | this handback |
| Gate 1 | passed | `verify.py` all `True`, `ALL True` |
| Gate 2 | passed | ruff `All checks passed!` |
| Gate 3 | passed | `5790 passed, 3 skipped`, exit 0, matching the reviewer's dry-tree reading |
| Gate 4 | passed | `fail_count` 0 |
| Gate 5 | passed | 5 ids, exact order |
| Gate 6 | passed | three subjects, newest first |
| T025 (R-1241) | done | the trip handler now lives in `job_burn.record_burn_trip`, with the ledger's rows and the ratchet's pins lowered by what moved, and a job's burn samples are kept in its record so a continued job judges its next calls against every call it made before |
