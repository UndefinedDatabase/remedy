# Handback — F032 Evidence Triple — Round R17 (the integration gate)

## Session

SESSION 4 of feature F032 · round R17 · rounds so far 17
(R1–R5 session 1, R6–R9 session 2, R10–R14 session 3, R15–R17 this one.)

## Range

Review of `c1e20833..8c42bad2`.

## State

- Branch: `feature/f032-evidence-triple`
- Base of this round: `c1e20833405fc3a5a8f3b50729046578dbc97329` (the R16 handback)
- Merge base with `main`: `a399a3304f9d962cd920c251488c40c486b35fdc`
- Commits, in order: C0a `1fadf8e7`, C0b `897e6ef8`, C1 `cd4c5d0b`,
  C2 `1fa2b3df`, C3 `8c42bad2`, C4 the handoff.
- No pull request was created and nothing was merged.

## Commits

### 1fadf8e7 docs(agent): save the F032 R17 block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f032-r17.md | +407 / -0 | C0a, the block saved verbatim |

### 897e6ef8 docs(agent): mirror the F032 R17 block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +170 / -145 | C0b, the same bytes mirrored |

### cd4c5d0b docs(agent): point the plan at the R17 integration gate
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +16 / -16 | C1, slice PLANF032R17 applied whole |

### 1fa2b3df docs(agent): book the R16 incomplete-round verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | C2, slice LEDGER17 appended |

### 8c42bad2 test(agent): record the F032 R17 integration gate evidence
| Path | +/- | Reason |
|---|---|---|
| .agent/gate_f032_r17/ | +273 / -0 | C3, 9 files under that dir |

### C4 the handoff
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | — | this file; a handoff cannot table the commit that writes it |

## External actions

- `git worktree add -b tmp/base-gate /home/decodeux/Repos/remedy/.remedy-wt/base-gate a399a3304f9d962cd920c251488c40c486b35fdc`
  → `Preparing worktree (new branch 'tmp/base-gate')` / `HEAD is now at a399a330`
- `git worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/base-gate` → removed
- `git worktree prune` → no output
- `git branch -D tmp/base-gate` → `Deleted branch tmp/base-gate (was a399a330).`
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`
- `git push -u origin feature/f032-evidence-triple` after C4
- No PR created. Nothing merged. No build run: `npm`, `npx`, `node` and `vite`
  were never invoked by this worker.

## Verification

G1 HYGIENE, BASE, SENTINEL — `git rev-parse HEAD` before C0a =
`c1e20833405fc3a5a8f3b50729046578dbc97329`; branch =
`feature/f032-evidence-triple`; `git status --porcelain | wc -l` = 0 after each
of C0a, C0b, C1, C2 and C3; `ls -la .agent/STOP` before C0a and again before C4
both printed `ls: cannot access '.agent/STOP': No such file or directory`.

G2 TRANSPORT — one disk-to-disk digest comparison. `.remedy-wt/f032-r17.md`,
`.agent/authored/f032-r17.md` @C0a and `.agent/last_block.md` @C0b all three
sha256
`413f94564628defbf56294e7425416ff3910f6ec6b1ec8c8c883674de0e6750e`, equal =
True; the two committed paths are one blob, `788f63165fea370d53f15581415ac0d9321688ae`.

G3 EXTRACTION AND CAPS, on the committed C0a blob — 2 slice regions found:
PLANF032R17 44 content lines, LEDGER17 1 content line, content total 45; TOTAL
407 lines; PROSE = 407 − 45 = 362, under 400 = True; TOTAL under 490 = True.

G4 THE PLAN @C1 — `.agent/plan.md` byte-equal to PLANF032R17 extracted from the
C0a blob = True; negative control with the trailing newline removed = False;
`wc -l` = 44, under 50 = True; `^## Goal$` = 1, `^## Next Steps$` = 1.

G5 THE APPEND @C2 — reader (a) identity True, 1107888 + 1 + 4656 = 1112545 =
post size, pre-commit blob is a byte PREFIX = True; reader (b) N = 1 paragraph,
last N units match in order = True; negative control (one byte flipped in the
first appended paragraph) rejected by BOTH readers = True. Counts before → after:
`^Gate: F\d+ R\d+ — ` 68 → 69, `^- R-\d+ — ` 274 → 274, `^Done: R-\d+ — ` 24 →
24, `^Landed: R-` 1 → 1; open set 250 → 250, maximum id `R-0713` → `R-0713`,
both unmoved as the block requires. Gate keys ADDED `['F032 R16']`; ids ADDED to
either set `[]`.

G6 THE BRANCH RUN @C2 — S1 first: `_frontend_is_stale()` = `False`;
`apps/ui/dist/index.html` mtime `Fri Aug 28 02:46:30 2026`; newest file under
`apps/ui/src` is `apps/ui/src/components/panels/RightLivePanel.module.css` at
`Fri Aug 28 02:25:15 2026`; `apps/ui/dist/assets` holds exactly
`index-D0y3OK7n.css` and `index-D_a-qpxM.js`, the two the reviewer's build
emitted. Then `python3 -m pytest -n auto -q` from the repository root: exit code
0, wall 180.52 s, raw tail `17982 passed, 20 skipped in 179.96s (0:02:59)`,
COMPLETE `^FAILED` list = 0 ids (the list is empty, not truncated). The full log
lived at `/home/decodeux/Repos/remedy/.remedy-wt/branch_run.txt` while the run
was in flight — gitignored at `.gitignore` line 235, outside every tracked path.

G7 THE BASE RUN @C2, serial after G6 (base started 02:55:51, twenty seconds
after the branch run ended 02:55:31; the two pytest processes never overlapped)
— worktree created with `git worktree add -b tmp/base-gate
/home/decodeux/Repos/remedy/.remedy-wt/base-gate
a399a3304f9d962cd920c251488c40c486b35fdc`. Parity restored by
`shutil.copytree(src, dst, symlinks=True)` for both `apps/ui/node_modules`
(43032 files, 27 symlinks preserved, 1.47 s) and `apps/ui/dist` (3 files, 0
symlinks, 0.0 s); neither existed in the worktree beforehand; no symlink was
created into the worktree and the sandbox raised no refusal.
`_frontend_is_stale()` INSIDE the base worktree = `False` after
`dist/index.html` was stamped `Fri Aug 28 02:55:51 2026`; the run also carried
`REMEDY_UI_NO_AUTO_BUILD=1`. Base run: exit code 1, wall 143.98 s, raw tail
`2 failed, 17832 passed, 20 skipped in 143.33s (0:02:23)`, COMPLETE sorted
`^FAILED` list = 2 ids, both listed under G8. MTIME WINDOW: run window
`Fri Aug 28 02:55:51 2026 → Fri Aug 28 02:58:15 2026`; all three files under the
base worktree's `apps/ui/dist` — `index.html`, `assets/index-D9dcd0E7.js`,
`assets/index-Xx8vqzN3.css` — carry mtime `Fri Aug 28 02:57:08 2026`, INSIDE the
window, and the two asset names changed from the copied-in `index-D_a-qpxM.js` /
`index-D0y3OK7n.css`. THE PARITY CLAIM IS VOID. Cleanup: worktree removed and
pruned, `tmp/base-gate` deleted (`was a399a330`), `git worktree list` = the one
line `/home/decodeux/Repos/remedy 8c42bad2 [feature/f032-evidence-triple]`,
`git branch --list "tmp/*"` = 0 lines.

G8 COMPARISON, ATTRIBUTION, PR GATE @C3 —
`comm -13 base_failed.txt branch_failed.txt` (BRANCH-ONLY) = **0 ids, the set is
empty**. `comm -23` (BASE-ONLY) = 2 ids, in full:
`tests/cli/test_review_bundle_runtime.py::TestSubprocessCleanup::test_timeout_raises_with_cleanup`
and
`tests/orchestration/test_run_manifest_logical_identity.py::TestTwoRealRunsShareLogicalIdentity::test_different_execution_identities_same_logical_hash`.
Per-id attribution, one line each:
- `…test_run_manifest_logical_identity…::test_different_execution_identities_same_logical_hash`
  — xdist / mid-run artifact rewrite; serial at base exit 0 `1 passed in 1.65s`,
  serial on branch exit 0 `1 passed in 1.69s`; rewritten artifact named:
  `apps/ui/dist` in the base worktree, all three files stamped 02:57:08 inside
  the run window with changed content-hash names, which is finding R-0176's
  mechanism; NOT a blocker, not coupled to F032.
- `…test_review_bundle_runtime.py::TestSubprocessCleanup::test_timeout_raises_with_cleanup`
  — xdist parallel contention; serial at base exit 0 `1 passed in 0.29s`, serial
  on branch exit 0 `1 passed in 0.30s`; evidence: the assertion reads
  `pgrep -f "apps.cli.grouped.*--help"` and recorded `returncode=0,
  stdout='2351843'`, a machine-wide predicate that cannot separate this test's
  own child from any other matching process under `-n auto`; no artifact is
  implicated, so the VOID parity claim is not offered as its cause; NOT a
  blocker, not coupled to F032.
NO ID IS A BLOCKER under the block's constraint 12, and no id is unattributed.
Files written under `.agent/gate_f032_r17/`: `attribution.txt`,
`base_failed.txt`, `base_parity.txt`, `branch_failed.txt`, `branch_meta.txt`,
`branch_run_tail.txt`, `comm_base_only_failures.txt`,
`comm_branch_only_failures.txt`, `full_log_provenance.txt` — 9 files, none
matching `\.log$`.
`git diff --name-only c1e20833..8c42bad2` = the 13 paths of the Change set less
`.agent/handoff.md`. BOTH residues: paths in the diff but not in the Change set
= NONE; paths in the Change set but not in the diff = `.agent/handoff.md` alone,
which C4 writes.
`git diff --stat c1e20833..8c42bad2 -- packages/ apps/ tests/ docs/` = EMPTY.
Insertion counts, each single-parent and each under 500, matching the `+/-`
column above cell by cell: C0a +407/−0, C0b +170/−145, C1 +16/−16, C2 +2/−0,
C3 +273/−0.
`git ls-files .remedy-wt` = 0 lines. `git worktree list` = 1 line.
`git branch --list "tmp/*"` = 0 lines.
`gh pr list --state open --json number,headRefName,baseRefName,isDraft` = `[]`.

## Authored-text proofs

Two applied this round, both extracted programmatically from the committed C0a
blob and never retyped.
- PLANF032R17 → `.agent/plan.md`: byte-equal True, negative control False (G4).
- LEDGER17 → `.agent/live_review.md`: append identity True with the pre-commit
  blob a byte prefix, both readers reject the one-byte mutation (G5).
- The block itself: `.remedy-wt/f032-r17.md` = `.agent/authored/f032-r17.md` =
  `.agent/last_block.md`, one sha256 and one blob id (G2).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror the block | done | |
| C1 the plan | done | |
| C2 the R16 verdict | done | |
| C3 the gate evidence directory | done | 9 files |
| C4 the handback | done | this file |
| S1 frontend currency measured | done | `_frontend_is_stale()` False, both assets present |
| S2 branch run then base run, serial | done | 02:52:30–02:55:31, then 02:55:51–02:58:15 |
| S3 base parity restored and measured | done | copytree symlinks=True, 27 links preserved |
| S4 auto-build neutralised twice, event measured | deviated | both steps performed; the mtime window shows the neutralisation FAILED and the parity claim is VOID |
| S5 the comparison | done | branch-only 0, base-only 2, both reported in full |
| S6 attribution of every branch-only id | done | the set is empty; nothing to attribute, no blocker |
| S7 attribution of every base-only id | done | both attributed by direct evidence, artifact named where implicated |
| S8 the evidence directory | done | the nine names of reading (d), none a `.log` |
| S9 spec and bundle agree | done | S1–S7's output is committed as S8's directory in C3 |

## Open findings

250 open (274 registered − 24 resolved), maximum id `R-0713`, unmoved from the
pre-commit reading. This round registered and resolved nothing.

## Deviations & assumptions

1. THE BLOCK'S BASE SHA IS NOT A REAL OBJECT. The block names its base
   `c1e208334cd8c7c0cef0a0ae3e5a1e63a4dc65d5`; `git cat-file -t` on it answers
   `fatal: git cat-file: could not get object info`. The actual tip of
   `feature/f032-evidence-triple` is `c1e20833405fc3a5a8f3b50729046578dbc97329`.
   The first eight hex characters agree and the block's own G8 quotes the short
   form `c1e20833`, so the intended commit is unambiguous and the round ran
   against the real tip. Nothing was changed to accommodate this; it is reported
   because a numeral in the block is wrong.
2. THE PARITY CLAIM IS VOID, AND THE CAUSE IS NAMED. `REMEDY_UI_NO_AUTO_BUILD=1`
   was set for the base run and `apps/ui/dist` was rewritten anyway, inside the
   run window, with changed vite content-hash names — a real build. The suite
   contains a test that removes the variable from the environment and then calls
   the unpatched builder:
   `tests/ui_server/test_dashboard_contract.py::TestAutoBuildBehavior::test_auto_build_runs_by_default`
   does `env.pop("REMEDY_UI_NO_AUTO_BUILD", None)` before
   `_auto_build_frontend()`, and `packages/orchestration/ui_server.py:3083`
   returns early only when that variable equals `"1"`. That test is present in
   the same shape at the merge base `a399a330`, so the behaviour predates this
   branch. S4 exists to catch exactly this, it did, and the consequence it
   prescribes — per-id attribution of every base-only failure by direct
   evidence — was carried out in full.
3. THE SAME REWRITE HAPPENED ON THE BRANCH SIDE. The block orders the mtime
   window for the base run only, but the primary checkout's `apps/ui/dist` was
   also rewritten during the branch run, at `Fri Aug 28 02:53:50 2026`, inside
   `02:52:30 → 02:55:31`. The three asset NAMES were unchanged, so it was a
   byte-identical rebuild from the same sources, and the branch run recorded
   zero failures. It is reported because measuring this at base and staying
   silent about it on the branch would be selective reporting. `git status
   --porcelain` stayed 0 lines throughout: `apps/ui/dist` is gitignored at
   `.gitignore` line 13.
4. CONSTRAINT 7 IN LETTER AND IN FACT. This worker invoked no `npm`, `npx`,
   `node` or `vite`. A build nonetheless ran, twice, because the ordered full
   suite contains the test named in deviation 2. That is a consequence of the
   work the block ordered, not an improvisation, and it is declared here rather
   than left for the reviewer to find in an mtime table.
5. NO FINDING ID WAS MINTED for the observation in deviations 2 and 3. The block
   ordered no registration, and under operator amendment amend0827 rule 2 an
   R-id is the reviewer's to spend. The evidence sits in
   `.agent/gate_f032_r17/full_log_provenance.txt` so the reviewer can decide
   whether this is a recurrence of R-0169 worth an id.
6. NO DEPARTURE FROM THE ORDERED COMMIT SEQUENCE. C0a, C0b, C1, C2, C3, C4 were
   committed in that order and no extra commit was made.

## Next

The reviewer re-reads `git diff c1e20833..8c42bad2` and re-runs G1–G8 to issue
the gate verdict — which is the reviewer's alone — and, if it passes, the next
round is the closure sequence part one per
`docs/roadmap/STATUS_closure_protocol.md`: the evidence job and a fresh review
zip. The next session's first action is Phase 1 rule 1, the `.agent/STOP` check,
before rule 2.
