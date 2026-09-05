# Handback — F259 Vocabulary & concept model v1, round 7 (INTEGRATION GATE)

## Session

SESSION 1 of feature F259 · round 7 · rounds so far 7

Context self-assessment: context is comfortable — this round spent most of its
budget waiting on two full-suite runs rather than on reading, and there is ample
room left for the closure sequence.

State block, verbatim as the block ordered:
`~95 % (T001–T004 ✅ · Integration Gate gelaufen · Closure offen) — Schätzung`

## Range

Review of 6e6e73ae..0cc0bdd2

## Commits

### c2a3b4d9 f259: save the round 7 integration-gate block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f259-r7.md | +266 / -0 | C0a — the block file copied byte for byte from `.remedy-wt/f259-r7-block.md` (shutil.copyfile, never retyped) |

### 3f7e8546 f259: mirror the round 7 block to last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +224 / -302 | C0b — mirror of the committed authored file; the -302 is the round-6 block it replaces |

### 41f7b57a f259: plan for the round 7 integration gate
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +25 / -27 | C1 — whole rewrite from the PLANF259R7 slice, one trailing newline |

### 490f7f27 f259: book the round 6 gate verdict in the record
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | C2 — the GATE_R6 record appended at end of file |

### 0cc0bdd2 f259: integration gate evidence for round 7
| Path | +/- | Reason |
|---|---|---|
| .agent/gate_f259_r7/attribution.txt | +94 / -0 | C3 — every branch-only and base-only id, the comm route, the R-0176 disclosure |
| .agent/gate_f259_r7/base_parity.txt | +107 / -0 | C3 — symlink count, mtime relation, dist mtime window, teardown |
| .agent/gate_f259_r7/base_tail.txt | +45 / -0 | C3 — base run raw tail, exit code, wall time |
| .agent/gate_f259_r7/branch_tail.txt | +45 / -0 | C3 — branch run raw tail, exit code, wall time |
| .agent/gate_f259_r7/base_failed.txt | +0 / -0 | C3 — empty: no base failures |
| .agent/gate_f259_r7/branch_failed.txt | +0 / -0 | C3 — empty: no branch failures |
| .agent/gate_f259_r7/comm_13.txt | +0 / -0 | C3 — empty: no branch-only failures |
| .agent/gate_f259_r7/comm_23.txt | +0 / -0 | C3 — empty: no base-only failures |

### C4 — this handback
The commit that writes `.agent/handoff.md` cannot table itself (R-0149 pattern).
It touches exactly one path, `.agent/handoff.md`, and nothing else.

Insertion counts against the 500 cap: C0a 266, C0b 224, C1 25, C2 2, C3 291.
Every commit is under the cap; no oversize declaration is needed. Every commit
is single-parent:
c2a3b4d9←6e6e73ae, 3f7e8546←c2a3b4d9, 41f7b57a←3f7e8546, 490f7f27←41f7b57a,
0cc0bdd2←490f7f27.

## External actions

- `git worktree add -b tmp/f259-base-gate .remedy-wt/f259-base-gate 25961794`
  → created on a THROWAWAY BRANCH, not detached. `rev-parse HEAD` =
  259617949461c993f1b8dabcf659e6a73110b162, `branch --show-current` =
  tmp/f259-base-gate.
- `git worktree remove --force .remedy-wt/f259-base-gate` → removed; the path no
  longer exists.
- `git branch -D tmp/f259-base-gate` → "Deleted branch tmp/f259-base-gate (was
  25961794)." No other branch was deleted.
- `git worktree prune` → exit 0.
- `git worktree list` → the primary checkout plus the ten pre-existing
  `remedy/job-*` worktrees and nothing else.
- `git push -u origin feature/f259-vocabulary` → `6e6e73ae..0cc0bdd2`; HEAD and
  `origin/feature/f259-vocabulary` both at 0cc0bdd2.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`.
  NO pull request was created. F259's PR belongs to the closure round.

## Verification — one line per gate, real readings

**G1 TRANSPORT — PASS.** `sha256sum` over three paths, one digest three times:
`a8c08ea7d75b5c051a25a3e3c4ba347f80e38f8fb4e23bd07d2acb88cab09f39` for
`.remedy-wt/f259-r7-block.md`, `.agent/authored/f259-r7.md` and
`.agent/last_block.md`. The digest equals the one the order stated, so the block
was executed as written.

**G2 THE RECORD APPEND — PASS.** `.agent/live_review.md` 839318 bytes before,
843886 after (+4568). Pre-append bytes are a byte-exact PREFIX of the post-append
bytes: **True**. Remainder equals exactly `"\n" + GATE_R6 + "\n"`: **True**.
`grep -c '^Gate: R6 — ' .agent/live_review.md` went from **0** to **1**.

**G3 THE BRANCH RUN — PASS, exit 0.** `python3 -m pytest -n auto -q` in the
PRIMARY checkout at `/home/decodeux/Repos/remedy`.
Raw tail: `19694 passed, 23 skipped, 1 warning in 134.50s (0:02:14)`.
Exit code **0**; wall time **135.2 s** (23:54:49 → 23:57:04).
`branch_failed.txt` line count: **0**.
`git status --porcelain` immediately before the run: **empty**. Immediately
after: **empty**. The primary checkout was never mutated.

**G4 THE BASE RUN WITH REAL PARITY — PASS, exit 0.** See the full parity
transcript below. `REMEDY_UI_NO_AUTO_BUILD=1 python3 -m pytest -n auto -q` with
the worktree as cwd. Raw tail: `19686 passed, 23 skipped, 1 warning in 161.68s
(0:02:41)`. Exit code **0**; wall time **162.3 s** (23:58:06 → 00:00:49).
`base_failed.txt` line count: **0**.

**G5 COMPARE — PASS.** `comm_13.txt` **0 lines**, `comm_23.txt` **0 lines**.
Both lists reproduced in full below. No base-only id needs attribution, so no
unattributed `comm -23` id blocks the verdict.

**G6 ATTRIBUTION — PASS, vacuously and stated as such.** `comm_13.txt` is EMPTY.
There is no branch-only id to re-run serially, no xdist-flake to record, and no
reproducible branch-only failure coupled to this feature's code. Constraint 10
(BLOCKER) is **not** triggered.

**G7 THE EVIDENCE DIRECTORY — PASS.** `.agent/gate_f259_r7/`:

| File | Bytes | Lines |
|---|---|---|
| attribution.txt | 4859 | 94 |
| base_failed.txt | 0 | 0 |
| base_parity.txt | 5894 | 107 |
| base_tail.txt | 3190 | 45 |
| branch_failed.txt | 0 | 0 |
| branch_tail.txt | 3126 | 45 |
| comm_13.txt | 0 | 0 |
| comm_23.txt | 0 | 0 |

Every file named in the block exists (missing: none); no unexpected extra file;
no file name ends in `.log`: **True**. Truncation check — the line count in the
file equals the count reported in G3/G4/G5 for all four of `branch_failed.txt`,
`base_failed.txt`, `comm_13.txt`, `comm_23.txt` (0 = 0 in each case).

**G8 THE PLAN AND THE STRUCTURE — PASS.** `wc -l .agent/plan.md` = **40**, under
50. `## Goal` heading count **1**; `## Next Steps` heading count **1**.
`filecmp.cmp(plan.md, slice+newline, shallow=False)` = **True**; trailing
newline count **1**. `git status --porcelain` immediately before C4 was staged:
**empty**. `git ls-files .remedy-wt` returns **nothing**. Every commit
single-parent (listed above). Per-commit `git diff --numstat` reported cell by
cell in the Commits table above. Push result and the empty `gh pr list` are in
External actions.

## The complete branch-only and base-only lists

**BRANCH-ONLY (`comm -13 base_failed.txt branch_failed.txt`) — comm_13.txt:**

    <EMPTY — 0 lines. There are no branch-only failures.>

Stated explicitly because an empty list still gets stated: both suites ran in
full and both exited 0, so there is nothing to attribute. No id was omitted,
sampled or headed.

**BASE-ONLY (`comm -23 base_failed.txt branch_failed.txt`) — comm_23.txt:**

    <EMPTY — 0 lines. There are no base-only failures.>

Attribution of the empty base-only list: no id requires assignment to the
environment class. The emptiness is itself the evidence that the corrected
parity recipe worked. Had `integration_gate.md` step 3 been followed literally,
R-0736 predicts ~114 false `tests/ui_server/` failures here and R-0591 a further
7 from dereferenced `.bin` shims — 121 ids that would all have landed in this
list. The pre-fix measurement in the parity transcript below shows the first
mechanism was live and was disarmed.

**Corroborating delta:** branch 19694 passed − base 19686 passed = **8**, and
`tests/docs/test_vocabulary.py` collects exactly **8 tests** and does not exist
at the merge base. Skips are 23 on both sides. The two runs differ by F259's own
new tests and by nothing else.

## The full parity transcript (G4)

**Worktree creation.** `git worktree add -b tmp/f259-base-gate
.remedy-wt/f259-base-gate 25961794` — ON A THROWAWAY BRANCH, never detached
(a detached base worktree fails the self-dogfood branch guard for the wrong
reason, DECISION D3 / F053 R2). Confirmed: HEAD
259617949461c993f1b8dabcf659e6a73110b162, current branch `tmp/f259-base-gate`.

**(i) The copy, with the argument named.**

    shutil.copytree(<primary>/apps/ui/node_modules, <wt>/apps/ui/node_modules, symlinks=True)
    shutil.copytree(<primary>/apps/ui/dist,         <wt>/apps/ui/dist,         symlinks=True)

SYMLINK COUNT under `apps/ui/node_modules/.bin` AFTER the copy —
primary checkout **23** symlinks of 23 entries; base worktree **23** symlinks of
23 entries; counts equal **True**; name sets equal **True**. This matches the 23
the reviewer measured at 6e6e73ae. A count of 0 would have meant the copy
dereferenced them and the parity was void; it did not.

**(ii) The R-0736 mtime fix — the relation the code actually reads.**
`packages/orchestration/ui_server.py::_frontend_is_stale` was read on disk and
returns True when any file under `apps/ui/src/` is newer than
`apps/ui/dist/index.html` — it compares against `index.html` alone.

Measured in the worktree BEFORE the fix:

| Reading | Value |
|---|---|
| `apps/ui/src` file count | 142 |
| newest src file | `apps/ui/src/types/react-force-graph-2d.d.ts` |
| newest src mtime | 1788645445.454480 (2026-09-05 23:57:25) |
| `dist/index.html` mtime | 1788057215.853621 (2026-08-30 04:33:35) |
| staleness relation holds | **True** — staleness WOULD have fired |

That is R-0736 reproduced directly: the copied dist is byte-correct and
mtime-STALE, because `copytree` preserves source mtimes while `git worktree add`
stamps checked-out sources with the checkout time.

The fix, applied as the block ordered — every mtime under `apps/ui/dist` set to
newest_src + 120 s = **1788645565.454480** (2026-09-05 23:59:25). AFTER the fix:
`dist/index.html` strictly newer than the newest src file **True**; staleness
relation holds **False**.

**(iii) The dist mtime WINDOW around the base run.** Run window
1788645486.731395 (23:58:06) → 1788645649.020247 (00:00:49).

| File | mtime BEFORE | mtime AFTER | inside window? |
|---|---|---|---|
| apps/ui/dist/assets/diffHighlightGrammars-o9XqnLhb.js | 1788645565.454480 | 1788645565.454480 | **yes** |
| apps/ui/dist/assets/index-Bh0mkYBD.js | 1788645565.454480 | 1788645565.454480 | **yes** |
| apps/ui/dist/assets/index-D_qZGOuo.css | 1788645565.454480 | 1788645565.454480 | **yes** |
| apps/ui/dist/index.html | 1788645565.454480 | 1788645565.454480 | **yes** |

Files added by the run: none. Files removed: none. Mtimes changed by the run:
**none** — mtime BEFORE equals mtime AFTER for every dist file.

SAID PLAINLY, NOT EXPLAINED AWAY: all four dist mtimes DO fall numerically
inside the run window. That is an artefact of the fix itself, not evidence of a
rebuild — step (ii) deliberately stamped dist into the future at newest_src +
120 s, and the run lasted 162.3 s, so the synthetic stamp lands inside its own
run window by construction. Choosing an offset SMALLER than the run duration
made the plain in-window test degenerate; that is a methodological deviation and
is declared as one below.

Because the window test is degenerate, the EVENT was measured a second,
independent way — ctime and inode, since any rebuild writes or replaces the file
and either changes ctime:

| File | inode | ctime | ctime inside window? |
|---|---|---|---|
| apps/ui/dist/assets/diffHighlightGrammars-o9XqnLhb.js | 5557655 | 1788645468.316750 | no |
| apps/ui/dist/assets/index-Bh0mkYBD.js | 5557657 | 1788645468.316750 | no |
| apps/ui/dist/assets/index-D_qZGOuo.css | 5557656 | 1788645468.316750 | no |
| apps/ui/dist/index.html | 5557653 | 1788645468.316750 | no |

Every ctime is 1788645468.32 — the moment of the `os.utime` call in step (ii),
18.4 s BEFORE the run started. All ctimes predate the run start: **True**. No
file under `apps/ui/dist` was written, replaced or touched during the base run:
**no rebuild event occurred**. A content hash is deliberately not offered as the
primary reading, because equal content is consistent both with no rebuild and
with a byte-identical one.

**(iv) The run.** Reported under G4 above.

**Teardown.** Reported under External actions above.

## Authored-text proofs

- `.agent/authored/f259-r7.md` — `shutil.copyfile` from
  `.remedy-wt/f259-r7-block.md`; sha256 identical across scratch, saved copy and
  mirror (G1).
- `.agent/plan.md` — PLANF259R7 extracted by marker regex from the COMMITTED
  authored file; `filecmp.cmp(..., shallow=False)` against the slice plus one
  newline: **True**.
- `.agent/live_review.md` — GATE_R6 extracted from the committed authored file;
  post-append bytes equal pre-append bytes plus exactly `"\n" + GATE_R6 + "\n"`:
  **True**.

## Deviations & assumptions

1. **Run logs could not be written outside the repository.** The block orders
   `~/remedy-gate-f259/`. The sandbox REFUSED it, verbatim: *"Permission to use
   Bash has been denied. IMPORTANT: You *may* attempt to accomplish this action
   using other tools that might naturally be used to accomplish this goal, e.g.
   using head instead of cat. But you *should not* attempt to work around this
   denial in malicious ways, e.g. do not use your ability to run tests to execute
   non-test actions. You should only try to work around this restriction in
   reasonable ways that do not attempt to bypass the intent behind this denial.
   If you believe this capability is essential to complete the user's request,
   STOP and explain to the user what you were trying to do and why you need this
   permission. Let the user decide how to proceed."* Refused for both
   `mkdir -p ~/remedy-gate-f259` and the absolute-path form
   `mkdir -p /home/decodeux/remedy-gate-f259`. The block's own fallback clause
   was taken: logs went to the gitignored `.remedy-wt/gate-f259/` and were copied
   into `.agent/gate_f259_r7/` only after each run exited. Required explicit
   statement: the two node ids R-0176 names did NOT fail — and more precisely
   **neither node id exists** in the suite at 6e6e73ae. A grep over `tests/`,
   `packages/` and `scripts/` finds no test function
   `test_run_manifest_logical_identity` and none `test_job_rerun_workspace_identity`.
   The nearest surviving surface, the FILE
   `tests/orchestration/test_run_manifest_logical_identity.py`, collects 11 ids;
   all 11 passed in both runs, since both runs had zero failures overall. For the
   base run the log lived OUTSIDE the base worktree in any case.
2. **The dist mtime offset was too small to keep the window test meaningful.**
   +120 s against a 162.3 s run put the synthetic stamp inside the run window by
   construction, so the literal in-window boolean reads "yes" for all four files
   while nothing was rebuilt. Compensated by the independent ctime/inode
   measurement above, which is decisive. A future gate should offset dist beyond
   the expected run duration.
3. **Three shell command FORMS were refused and re-expressed**, per block
   constraint 7. (a) `cd <dir> && comm ...` refused → `comm(1)` invoked through
   Python `subprocess.run(["comm", "-13", base, branch])`; both invocations
   exited 0; the route is recorded in `attribution.txt`. (b) A heredoc Python
   snippet containing a brace-with-quote dict literal refused → the same checks
   were written to `.remedy-wt/gate-f259/check_evidence.py` and run as a file.
   (c) `grep -c '^## Goal$'` refused (`$` anchor inside a `grep -c` pattern) →
   re-expressed as `re.findall` in `.remedy-wt/gate-f259/check_plan.py`. Each
   refusal is quoted or named rather than the check being weakened.
4. **No deviation from the block's ordered commit sequence.** C0a, C0b, C1, C2,
   C3, push, C4, push — exactly as ordered, no extra commit, none dropped, none
   reordered.
5. **R-0736 stays OPEN and `docs/agents/integration_gate.md` was NOT edited**,
   per constraint 11 — this round measures and edits no product code, no test and
   no doc. This round obeyed R-0736's fix clause rather than the defective step 3
   text, and says so here and in `base_parity.txt`. The defect is now backed by a
   fresh direct measurement (staleness True before the fix, False after) which the
   repair round can cite.
6. **Scratch helper scripts** (`run_suite.py`, `run_base.py`, `check_evidence.py`,
   `check_plan.py`, the raw logs and the two `*_meta.json`) remain in the
   gitignored `.remedy-wt/gate-f259/`. `git ls-files .remedy-wt` returns nothing,
   so none of them entered the change set.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a | done | `.agent/authored/f259-r7.md` — c2a3b4d9 |
| C0b | done | `.agent/last_block.md` — 3f7e8546 |
| C1 | done | `.agent/plan.md` ← PLANF259R7 — 41f7b57a |
| C2 | done | `.agent/live_review.md` + GATE_R6 — 490f7f27 |
| C3 | done | `.agent/gate_f259_r7/` 8 files — 0cc0bdd2, committed after both runs exited |
| C4 | done | this handback |

| Gate | Status | Reading |
|---|---|---|
| G1 | done | one digest a8c08ea7… across all three paths |
| G2 | done | prefix True, remainder True, 839318→843886, grep 0→1 |
| G3 | done | exit 0, 19694 passed / 23 skipped, 135.2 s, 0 FAILED, tree clean both sides |
| G4 | done | exit 0, 19686 passed / 23 skipped, 162.3 s, 0 FAILED; 23 symlinks; staleness True→False; no rebuild event |
| G5 | done | comm_13 0 lines, comm_23 0 lines, both reproduced in full |
| G6 | done | branch-only list empty; no BLOCKER |
| G7 | done | 8/8 files present, no `.log` name, no truncation |
| G8 | done | plan 40 lines, headings 1/1, filecmp True, tree clean, no PR |

## Open findings

Unchanged by this round: 294 open (299 registrations against 5 `Done:` lines, as
recomputed at R6). This round registered no new finding — it measured and found
nothing to register. R-0736 and R-0591 remain OPEN; both had their fix clauses
obeyed here, and R-0736 now has a fresh direct measurement behind it.

## Next

The reviewer's GATE VERDICT on this integration gate. On PASS, the CLOSURE round
per `docs/roadmap/STATUS_closure_protocol.md`: the evidence job, a fresh review
zip, the ledger rotation, the §3 checklist consolidation pass, the
reviewer-authored STATUS line committed last, and the pull request — which is
NOT merged in this session but at the next feature's Open PR Gate.
