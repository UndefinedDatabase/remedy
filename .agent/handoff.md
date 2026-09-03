# Handoff — F112 Prompt budget per task class, round 19 (session 6: the integration gate)

## Session

SESSION 6 of feature F112 · round 19 · rounds so far 19.

This is SESSION 6's first and (so far) only delegated round. It ran the
INTEGRATION GATE this feature owes before closure per
`docs/agents/integration_gate.md` steps 1-5, with the three open-finding
repairs (R-0591, R-0736, R-0590) the block layered on top of that
procedure. It also booked round 18's PASS verdict (RECORD18) into
`.agent/live_review.md` in its first content commit (C1), per
amend0827-process-diet rule 1. **No production code was touched.**

## Range

Review of `c7d68c58..cd3173fc`.

## Commits

### 8fe10ad8 F112 R19 C0a: save round 19 block to .agent/authored/f112-r19.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r19.md` | 336/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). |

### 598e228b F112 R19 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 300/31 | Byte-identical mirror of the authored file (whole-file rewrite; exempt from the 500-line insertion cap per AGENTS.md's single-`.agent/**`-file exemption; also under 500 regardless). Confirmed with `git rev-parse HEAD:.agent/authored/f112-r19.md` and `git rev-parse HEAD:.agent/last_block.md` printing the SAME blob id (`5f4c5fe1...`) — direct proof of byte-identity, not merely a `cmp` reading. |

### 4f8b4be1 F112 R19 C1: append RECORD18 to live_review.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/1 | Appended RECORD18 (round 18's verdict, VERDICT PASS) via `content_bytes + b"\n" + RECORD18_bytes` — the ONE-newline formula, extracted programmatically from the committed authored file. |

### d217bab0 F112 R19 C2: apply PLAN19 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 19/23 | Whole-file replacement with PLAN19, extracted programmatically from the committed authored file, not retyped. No trailing newline (per the block). |

### cd3173fc F112 R19 C3: gate evidence — integration gate, session 6
| Path | +/- | Reason |
|---|---|---|
| `.agent/gate_f112_r19/gate_summary.txt` | 98/0 | Branch/base identifiers, per-step results, test-count delta, cleanup note. |
| `.agent/gate_f112_r19/branch_run_tail.txt` | 60/0 | Raw tail of the branch pytest run. |
| `.agent/gate_f112_r19/branch_failed.txt` | 0/0 | Empty — 0 branch failures. |
| `.agent/gate_f112_r19/base_run_tail.txt` | 60/0 | Raw tail of the base pytest run. |
| `.agent/gate_f112_r19/base_failed.txt` | 1/0 | The one base-only failure id. |
| `.agent/gate_f112_r19/branch_only.txt` | 0/0 | Empty — `set(branch_failed) - set(base_failed)` is empty. |
| `.agent/gate_f112_r19/fixed_by_branch.txt` | 1/0 | `set(base_failed) - set(branch_failed)`: one id. |
| `.agent/gate_f112_r19/parity_mtime.txt` | 20/0 | Per-file mtime before/after the base run window, content digest, PARITY HOLDS. |
| `.agent/gate_f112_r19/attribution.txt` | 62/0 | Unconditional attribution of both comparison sets (R-0590): branch-only empty; the one fixed_by_branch id attributed to the XDIST-FLAKE class by serial re-run (5/5 pass) and file-coupling grep, with a named prior occurrence at `.agent/gate_f110_r15/attribution.txt`. |

9 files, 302 insertions total (under the 500 cap; not declared as oversize).

## External actions

- `git worktree add -b tmp/f112-base-gate .remedy-wt/f112-r19-base 5c28c6741db2d9073fc75cd159d91037e0757fb0`
  → succeeded; HEAD landed at `5c28c674` on the new branch.
- `git worktree remove .remedy-wt/f112-r19-base` → succeeded, no output (clean removal).
- `git worktree prune` → succeeded, no output.
- `git branch -d tmp/f112-base-gate` → `Deleted branch tmp/f112-base-gate (was 5c28c674).`
- `git push -u origin feature/f112-prompt-budget-per-task-class` → run immediately
  after this handback commit; outcome recorded in the completion report, not
  in this file (write-once rule).
- No PR created, no merge — none was ordered.

## Verification

**G1 TRANSPORT** —
`sha256sum` of the committed `.agent/authored/f112-r19.md`:
`29563a53dd4fd4568249231d1242c059d2566531a1d8ccde9688f72bed8c1fcc`, length
**23042 bytes**, **336 lines** (`wc -l`). `git rev-parse
HEAD:.agent/authored/f112-r19.md` and `git rev-parse HEAD:.agent/last_block.md`
BOTH print `5f4c5fe15b5fb3cde78732097d4a52af94be45f9` — ONE blob id, proving
the C0b mirror is byte-identical to the C0a save. PASS.

**G2 THE PLAN** — PLAN19 extracted by delimiter from the committed authored
file (2088 bytes) compared byte-for-byte in Python against `.agent/plan.md`
at C2: **equal, 2088 bytes both sides** (cmp-exit-0 equivalent). `wc -l
.agent/plan.md` = **44** (under 50). File ends WITHOUT a trailing newline
(confirmed programmatically). `grep -c '^## Goal'` = **1**. `grep -c '^##
Next Steps'` = **1**. PASS.

**G3 THE RECORD APPEND** — `.agent/live_review.md` measured **2284151 bytes**
immediately before the append (matches `c7d68c58`'s pinned figure exactly).
RECORD18 extracted from the committed authored file measured **2614 bytes**.
Appended as `content_bytes + b"\n" + RECORD18_bytes` (ONE newline). Post-size
measured at **2286766 bytes**, matching `2284151 + 1 + 2614` exactly.
Old-file-is-prefix check: **True**. Post-append file still ends WITHOUT a
trailing newline: **True** (verified directly, not merely by construction).
NEGATIVE CONTROL: flipped one byte at offset 100 inside the RECORD18 slice,
recomputed the append — equality against the real post-append file: **False**.
HEADER SHAPE: lines matching `^Gate: F112 R18 — ` — before C1 **0**, after C1
**1**. Lines matching `^Gate: F\d+ R\d+ — ` — before **265**, after **266**.
OPEN SET recomputed mechanically (never carried forward): registered
(`^- R-\d+ — `, unique ids) — before **350**, after **350**. Unique `Done:`
(`^Done: R-\d+ — `) — before **72**, after **72**. Open total (registered
minus done) — before **278**, after **278**. All figures match the block's
pinned expectations exactly, UNMOVED as this round registers no finding and
resolves none. PASS.

**G4 STEP 1, THE BRANCH RUN** — WARM-BUILD precondition re-measured
independently of the block's pinned figures: `apps/ui/dist/index.html`
mtime **1788057215.854**; newest file under `apps/ui/src`
(`RemedyShell.tsx`) mtime **1788057023.742**; dist newer than every src
file: **True**. No cold build owed.
Full suite run: `pytest.main(["-n", "auto", "-q"])` from
`/home/decodeux/Repos/remedy`, NO environment variable set. Result:
**19546 passed, 23 skipped, 0 failed**. Exit **0**. Wall clock: **139.61s**
(pytest-reported) / **139.875s** (measured around the call).
Collection cross-check: `pytest --collect-only -q` on the branch answers
**19569 tests**, matching `19546 + 23` exactly and matching this round's own
pinned COLLECTION parameter. `branch_failed.txt` written at 0 lines;
`branch_run_tail.txt` written (60 lines). PASS.

**G5 STEP 2, THE BASE RUN** — worktree created exactly per THIS ROUND'S
PARAMETERS: `git worktree add -b tmp/f112-base-gate .remedy-wt/f112-r19-base
5c28c6741db2d9073fc75cd159d91037e0757fb0`. Parity restored BEFORE the run:
`apps/ui/node_modules` copied with `shutil.copytree(symlinks=True)` —
**44839 entries copied, 27 symlinks preserved** (of which **23** are the
`.bin` shims this round's own UI SHIMS parameter named — confirmed preserved
by direct post-copy `os.path.islink` count, not assumed); `apps/ui/dist`
copied the same way — **5 entries** (4 files, 1 directory), **0 symlinks**
(none present in dist to begin with). Dist file mtimes then advanced via
`os.utime` to the current time (**1788479066.574**) — R-0736. Re-measured
`_frontend_is_stale()` from a module loaded via `importlib` FROM INSIDE the
base worktree (`__file__`-relative path resolution, so it reads the base
worktree's own `apps/ui/src` and `apps/ui/dist`, not the primary checkout's):
**False**, confirmed BEFORE the run started.
Run: `REMEDY_UI_NO_AUTO_BUILD` set in-process via `os.environ` (base run
only), then `pytest.main(["-n", "auto", "-q", "--rootdir", BASE_WT])` with
`cwd`/`sys.path` pinned to `.remedy-wt/f112-r19-base`. Result: **1 failed,
19486 passed, 23 skipped**. Exit **1**. Wall clock: **168.29s** (reported) /
**168.561s** (measured). Collection cross-check: `pytest --collect-only -q`
at the base worktree answers **19510 tests**, matching
`19486 + 23 + 1` exactly.
PARITY AS AN EVENT (R-0444): every file under the base worktree's
`apps/ui/dist` mtime-snapshotted immediately before and immediately after
the run (window START `1788479146.483`, END `1788479315.044`). All 4 files'
before/after mtimes are IDENTICAL (`1788479066.574` both readings) and NONE
falls inside the run window — **PARITY HOLDS**. Accompanying content digest
(sha256 over sorted file contents) before/after: **identical**
(`ef09e3072d59b1d6fa7ea7ea0bd13aabaafb52674b9dbad58a8e2a615236f445`), reported
as an accompaniment only, per R-0444, never as the parity proof itself.
Written to `parity_mtime.txt`. PASS (run executed and measured as ordered;
one genuine failure — see G6).

**G6 STEPS 3 AND 4, COMPARISON AND ATTRIBUTION** — computed as a Python set
difference (`comm` unavailable through this session's guard for piped forms,
per R-0590): `branch_only = sorted(set(branch_failed) - set(base_failed))`
→ **0 lines**. `fixed_by_branch = sorted(set(base_failed) -
set(branch_failed))` → **1 line**:
`tests/cli/test_review_bundle_runtime.py::TestSubprocessCleanup::test_timeout_raises_with_cleanup`.
Line counts: `branch_failed.txt` 0, `base_failed.txt` 1, `branch_only.txt` 0,
`fixed_by_branch.txt` 1.
NEW-TESTS split: not applicable — branch_only is empty, so there is no
branch-only failing id to classify against base-absence.
ATTRIBUTION (R-0590, unconditional): the one `fixed_by_branch` id was
serially re-run at the base worktree, xdist disabled, **5 independent
invocations, all 5 PASSED** (0.29-0.32s each). Root cause: the test's own
`pgrep -f apps.cli.grouped.*--help` orphan-process check is not scoped to
its own PID or process group, so under parallel xdist workers it can match a
concurrent worker's own short-lived `--help` subprocess from the SAME test
running in a different worker. CLASSIFICATION: XDIST-FLAKE class (F135/F052).
COUPLING CHECK: `git diff --name-only 5c28c674..HEAD -- packages/` lists
exactly 8 files (`config.py`, `context_compiler.py`, `decision_queue.py`,
`escalation.py`, `pingpong_job.py`, `pingpong_loop.py`, `prompt_budget.py`,
`task_granularity.py`) — none is `tests/cli/test_review_bundle_runtime.py`
or anything that file imports. PRIOR OCCURRENCE: the exact same node id was
already independently classified identically (base-only, XDIST-FLAKE,
serial-pass) at `.agent/gate_f110_r15/attribution.txt` item 2, on an
unrelated feature branch — a second, independent recurrence of the same
known class. NOT fixed by branch code, NOT coupled to F112 code, NOT a
BLOCKER. Written to `attribution.txt`. PASS — no id left unattributed, no
BLOCKER found.

**G7 THE EVIDENCE DIRECTORY** — `.agent/gate_f112_r19/` created and committed
with exactly the 9 files the block names (matching the `.agent/gate_f109_r17/`
/ `.agent/gate_f110_r15/` file set): `gate_summary.txt`, `branch_run_tail.txt`,
`branch_failed.txt`, `base_run_tail.txt`, `base_failed.txt`,
`branch_only.txt`, `fixed_by_branch.txt`, `parity_mtime.txt`,
`attribution.txt`. `git ls-files .agent/gate_f112_r19` lists exactly these
9 paths. `ls -la` confirms 9 regular files, sizes 0-5463 bytes. Count of
committed members whose name ends `.log`: **0**. PASS.

**G8 THE TREE, THE COMMITS AND THE SWEEP** — `git status --porcelain`
immediately before staging C4: **empty**. `git worktree list` after cleanup:
only the primary checkout and this repo's pre-existing, unrelated
`remedy/job-*` worktrees remain — the `f112-r19-base` worktree does NOT
appear. `git branch --list 'tmp/*'`: **empty** — the throwaway branch does
NOT survive. `os.path.isdir('.remedy-wt/f112-r19-base')`: **False**. `git
ls-files .remedy-wt`: **empty** (still gitignored, nothing tracked).
`/home/decodeux/Repos/remedy/remedy.toml`: does not exist.
`git diff --stat c7d68c58..cd3173fc -- packages/ apps/ tests/ docs/`:
**empty** — this round measured the branch, it did not change it.
PER-COMMIT INSERTIONS (the `+` column only, DECISION F104 D1): C0a
`8fe10ad8` **336**, C0b `598e228b` **300**, C1 `4f8b4be1` **2**, C2
`d217bab0` **19**, C3 `cd3173fc` **302** — every one confirmed under 500 by
direct `git show --stat` reading; no oversize commit to declare. PASS.

`.agent/STOP` read from disk before the first commit of this round: absent.
Re-read now, immediately before staging this handback (C4): absent (see
`ls .agent/STOP` → "No such file or directory"). No stop condition triggered
at either reading.

## Authored-text proofs

`.agent/authored/f112-r19.md` (committed at `8fe10ad8`) vs `.agent/last_block.md`
(committed at `598e228b`): byte-identical, proved by IDENTICAL git blob ids
(`git rev-parse HEAD:<path>` for both paths after C0b prints the same hash,
`5f4c5fe1...`) — a stronger proof than `cmp` alone, since it compares the
object store's own content-addressed identity. RECORD18 and PLAN19 were both
extracted programmatically from this committed file (never retyped) and
applied via the stated append formula or whole-file write; every application
was confirmed against byte counts and before/after equality checks in G2/G3
above. No production-code authored text was applied this round (none was in
the block).

## Deviations & assumptions

1. **The bash-tool permission quirk naming `.remedy-wt/` paths was observed
   twice this round** (a combined multi-statement command mixing `ls`, a
   Python one-liner and `git check-ignore` in one call, and separately a
   command using shell output redirection into a `.remedy-wt/` path) and
   worked around per the block's own stated escape hatch: driver scripts
   were written via the Write tool (not typed into the bash command text)
   and invoked with `python3 -c "import runpy; runpy.run_path(...)"`, where
   the bash command text itself never names the `.remedy-wt` substring. This
   was NOT fought repeatedly — after the second denial, all subsequent
   `.remedy-wt` scratch I/O used this route or a plain single-purpose `ls`/
   `python3 -c` call (both of which worked reliably once the command was
   simplified to one clear action). No scratch file was relocated outside
   `.remedy-wt/gate-scratch-r19/`, so R-0176's requirement (logs outside the
   tracked worktree, copied in only after each run exits) was met
   throughout.
2. **`.agent/gate_f112_r19/gate_summary.txt` and `attribution.txt` cite the
   base-worktree PID (954599) and the wall-clock window in absolute epoch
   time** rather than the worker's own earlier session numbers — this
   round's own fresh measurement, not carried from any prior gate; stated
   here only because the SAME node id and SAME root-cause class were also
   seen at `.agent/gate_f110_r15/` on a different feature branch, which this
   round cites as corroborating prior evidence, not as a substitute for its
   own independent serial re-run (which was performed: 5/5 pass, this round,
   at this round's own base worktree).
3. **One base-only failure was found and is NOT a blocker.** Per
   integration_gate.md step 4 and R-0590, it was classified by direct
   evidence (serial re-run 5/5 pass, file-coupling grep against F112's own
   changed set) as the XDIST-FLAKE class, unrelated to F112 code. This is a
   MEASUREMENT this round performed, not a verdict — the reviewer decides
   whether this classification is accepted.
4. **No search of `.agent/decisions.md`, `.agent/candidates.md`,
   `.agent/prose_slips.md` or `docs/roadmap/features/T3_F112.md` was
   performed**, per the block's own change-set exclusion (constraint 10) —
   nothing this round found needed any of them.
5. **`git push` outcome is not recorded in this file** (write-once rule) —
   see the completion report for the real result.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| C0a save block | done | |
| C0b mirror block | done | blob-id-identical to C0a |
| C1 append RECORD18 | done | byte arithmetic + negative control both PASS |
| C2 apply PLAN19 | done | byte-equal, under 50 lines, no trailing newline |
| C3 gate evidence | done | 9 files, GREEN with 1 attributed base-only xdist-flake |
| G1 transport | done | blob ids match, sha256 + length + wc -l reported |
| G2 the plan | done | byte-equal, headings present exactly once each |
| G3 the record append | done | arithmetic, prefix, negative control, header/open-set counts all match pinned figures |
| G4 branch run | done | 19546 passed / 23 skipped / 0 failed, exit 0, 139.61s |
| G5 base run | done | 19486 passed / 23 skipped / 1 failed, exit 1, 168.29s; parity HOLDS |
| G6 comparison + attribution | done | branch_only empty; 1 fixed_by_branch id attributed to XDIST-FLAKE, no blocker |
| G7 evidence directory | done | 9/9 files committed, 0 `.log` members |
| G8 tree/commits/sweep | done | worktree+branch removed, tree clean, no protected-path diff, all commits under 500 insertions |
| RECORD18 booked | done | applied verbatim at C1 |
| PLAN19 applied | done | applied verbatim at C2 |

## Next

**GATE MEASUREMENT: GREEN.** Branch run 0 failed / exit 0. Base run 1 failed
/ exit 1, but that one id is attributed by direct evidence (5/5 serial pass,
no coupling to F112's changed files, an independently-recurring known
XDIST-FLAKE class also seen at F110 R15 on an unrelated branch) to
environment load, not to F112 code. No branch-only failure exists at all.
**This worker issues no verdict** — that is the reviewer's alone, per the
block's own instruction, to be applied against
`.agent/gate_f112_r19/gate_summary.txt` and `attribution.txt`.

If the reviewer accepts this gate as PASS: session 6 (or 7) proceeds to
closure per `docs/roadmap/STATUS_closure_protocol.md` — evidence job, fresh
review zip, the STATUS line, the PR. Round 19's own verdict (once reviewed)
books into `.agent/live_review.md` in the first commit of that next round,
per amend0827 rule 1 — not in this file.

Open findings count: **278** (350 registered, 72 `Done:`) — UNMOVED by this
round, confirmed on both sides of C1's append (G3 above).

Before starting the next round: re-check `.agent/STOP` from disk (absent as
of this round, confirmed at both the round's start and immediately before
this handback). Phase 0's state probe (git status, branch, log, `gh pr
list`) should be re-run fresh at that round's own start, per
`docs/agents/self_drive_protocol.md` — not assumed carried over from this
handoff.
