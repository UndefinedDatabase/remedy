# Handback — F255 R18 (the INTEGRATION GATE; R17's verdict recorded)
## Range
Review of b3146e91..HEAD on `feature/f255-teacher-role`.
## Commits
### db723372 chore(state): save the F255 R18 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f255-r18.md | 273/0 | C0a — the R18 block COPIED verbatim from `.remedy-wt/f255-r18.md`, never retyped |

### fcab228e chore(state): mirror the F255 R18 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 205/216 | C0b — the same file copied again, not regenerated |

### 77f5f0b4 chore(plan): advance the plan to F255 R18
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 18/16 | C1 — the plan, the FIRST substantive commit (constraint 3; R-0377, R-0491, R-0548) |

### b926a473 docs(review): record the R17 verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C2 — RECORDR17 appended after exactly one blank line; a `Gate:` paragraph, so it registers and resolves nothing. Lands BEFORE the measuring (constraint 4) |

### 4d1d3304 test(gate): record the F255 R18 integration gate evidence
| Path | +/- | Reason |
|---|---|---|
| .agent/gate_f255_r18/attribution.txt | 94/0 | C3 — every differing id classified; 0 branch-only, 9 base-only |
| .agent/gate_f255_r18/base_failed.txt | 9/0 | C3 — sorted `FAILED` lines of the base run |
| .agent/gate_f255_r18/base_parity.txt | 86/0 | C3 — worktree, parity copy, before/after digest+mtime, `PARITY_CLAIM=VOID` |
| .agent/gate_f255_r18/branch_failed.txt | 0/0 | C3 — sorted `FAILED` lines of the branch run; EMPTY, and empty is the real result |
| .agent/gate_f255_r18/branch_meta.txt | 16/0 | C3 — checkout, revision, command, exit code, wall seconds, summary, FAILED count |
| .agent/gate_f255_r18/branch_run_tail.txt | 42/0 | C3 — the last 40 lines of the branch log |
| .agent/gate_f255_r18/comm_base_only_failures.txt | 9/0 | C3 — `comm -23`, as exact argv over the two sorted files |
| .agent/gate_f255_r18/comm_branch_only_failures.txt | 0/0 | C3 — `comm -13`; EMPTY, which is the gate's passing shape |
| .agent/gate_f255_r18/full_log_provenance.txt | 28/0 | C3 — each raw log's scratch path, line count and sha256; raw logs stay OUTSIDE the tracked tree |

### C4 docs(state): write the F255 R18 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | self-reference | C4 — a handoff cannot table the commit that writes it (R-0149); its cell and the complete change set are in the round report |

| Item | Status | Reason |
|---|---|---|
| C0a | done | |
| C0b | done | |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |

## External actions
`git worktree add -b tmp/base-gate-r18 .remedy-wt/base-r18 b35d350b` → "Preparing worktree (new branch 'tmp/base-gate-r18')", HEAD b35d350b, `branch --show-current` = tmp/base-gate-r18, so ON A BRANCH and never detached (DECISION D3). `git worktree remove --force .remedy-wt/base-r18` → then `git worktree prune`, then `git branch -D tmp/base-gate-r18` → "Deleted branch tmp/base-gate-r18 (was b35d350b)". `--force` was needed because the parity copy leaves untracked `apps/ui/node_modules` and `apps/ui/dist` in that worktree. `git worktree list` afterwards reports the primary checkout ALONE. `git push` after C4 — real output in the round report. NO pull request created and NO CI run awaited (constraint 12).

## Verification
G1 `.agent/STOP` read from disk before C0a and ABSENT; branch `feature/f255-teacher-role`; `git status --porcelain` EMPTY after every commit and at the handback; `git worktree list` = `/home/decodeux/Repos/remedy 4d1d3304 [feature/f255-teacher-role]` and nothing else; `git branch --list "tmp/*"` empty.
G2 `.remedy-wt/f255-r18.md`, `.agent/authored/f255-r18.md` at C0a and `.agent/last_block.md` at C0b are each sha256 e77dce39574bf45a9d544c4ae3496850b8607038ed87d0a7cc01d7e9a6981117 over 24576 B and 273 lines — ALL THREE BYTE-EQUAL, and equal to the digest stated at delegation.
G3 TWO slices, a count taken from my own ordered extraction of the COMMITTED `.agent/authored/f255-r18.md` at db723372 rather than written beside it (R-0604): PLAN255R18 acd7ca19d47f9bc59939ab951e3f36da1ac5511e54f8ba0106c6a6bbf4494870 2241 B 40 lines; RECORDR17 96a561d9a623821023329524441705185aaebb51744933070153669e1087459f 6104 B 1 line. Newline convention NEWLINE-INCLUDED — a body is the lines strictly between its markers, each keeping its own LF; marker lines excluded (R-0600).
G4 `.agent/plan.md` at C1 byte-equals PLAN255R18: sha256 acd7ca19d47f9bc59939ab951e3f36da1ac5511e54f8ba0106c6a6bbf4494870, 2241 B, 40 lines — under the 50-line cap — with `## Goal` 1x, `## Next Steps` 1x and the roadmap F-id F255 present. C1 is the FIRST commit other than C0a and C0b: `git log --reverse b3146e91..77f5f0b4` opens db723372, fcab228e, 77f5f0b4.
G5 The b3146e91 blob of `.agent/live_review.md` is a byte-exact PREFIX of the C2 blob; remainder sha256 0ddd98ad002ff0ea9048d7b89ed8f0818a45bbffea9170700a664dbe277d7082 at 6105 B / 2 lines, byte-equal to one newline followed by RECORDR17, the byte after that leading newline being `G`, not a newline. SECOND, INDEPENDENT blank-line paragraph split of the C2 blob: 211 units whose LAST unit IS RECORDR17 — newline-INCLUDED 96a561d9a623821023329524441705185aaebb51744933070153669e1087459f at 6104 B, newline-EXCLUDED 01b0e236f83408a2353f3d5abc51031fb4862c990a99d661e2b4bd41aa389681 at 6103 B. I RE-MEASURED constraint 5 rather than trusting it: RECORDR17 holds 0 interior blank lines, so it is exactly 1 unit and the LAST-UNIT reading is exact. Negative control: a one-byte mutant of the expected remainder is REJECTED by BOTH readings — the remainder-equality reading and the last-paragraph-equality reading — while the real blob is accepted by both.
G6 Sets over `.agent/live_review.md`, registered being lines matching `^- R-\d+ — ` and resolved lines matching `^Done: R-\d+ — `, counted LINE-ANCHORED and never as substrings (R-0584): 186 / 3 / 183 / 0 at b3146e91 and the SAME 186 / 3 / 183 / 0 at C2, a `Gate:` paragraph adding neither kind of line — this round registers NO finding and resolves NONE. `Gate: R18 — the R17 entry.` occurs 0x at b3146e91 and 1x at C2, is the LAST of the 18 lines beginning `Gate: R`, and all 18 header keys are distinct.
G7 THE BRANCH RUN, in the PRIMARY checkout at b926a473, `python3 -m pytest -n auto -q` with `REMEDY_UI_NO_AUTO_BUILD` NOT set: exit 0, `17315 passed, 20 skipped in 144.91s (0:02:24)`, wall 145.5 s measured around `subprocess.run`, FAILED count 0. Log written to `.remedy-wt/.cache/gate_r18/branch_run.log`, OUTSIDE the tracked tree (R-0176). Under the ~5-minute budget of integration_gate.md step 5, so no perf note is owed.
G8 THE BASE RUN, in `.remedy-wt/base-r18` at b35d350b — which is BOTH `git merge-base main HEAD` and `git rev-parse main` — after `shutil.copytree(src, dst, symlinks=True)` of `apps/ui/node_modules` and `apps/ui/dist`, each destination verified a REAL DIRECTORY and NOT itself a symlink. `REMEDY_UI_NO_AUTO_BUILD=1` passed through the `env=` parameter of `subprocess.run` as a copy of `os.environ` plus that key, never as a shell prefix (constraint 7). Exit 1, `9 failed, 17188 passed, 20 skipped in 155.50s (0:02:35)`, wall 156.0 s. NEUTRALISATION VERIFIED, NOT TRUSTED: the `apps/ui/dist` digest 09463f4379b4702ce090a0396c4b92256e122e0567b30d896cd2919291b03e51 and the file count 3 are unchanged on BOTH sides, and the primary checkout's `index.html` mtime is unchanged at 1787279383323951913 — but the BASE worktree's moved, 1787279383323951913 → 1787279587674706567. A moved mtime voids the claim by rule, because `_frontend_is_stale` decides by MTIME and the digest is blind to a byte-identical rebuild (R-0565). **PARITY_CLAIM=VOID.**
G9 `comm -13 base_failed.txt branch_failed.txt` and `comm -23` were invoked as EXACT ARGV over the two sorted files, not through a shell. BRANCH-ONLY FAILURES: 0. BASE-ONLY FAILURES: 9. A count of 0 branch-only failures is the gate's passing shape, and 0 is the real number here, not a claimed one.
G10 ATTRIBUTION. No branch-only id exists, so none is re-run serially and constraint 13's blocker rule is not reached — no blocker is declared because none was found. The parity claim is VOID, so ALL NINE base-only ids are attributed individually by direct evidence rather than by a blanket claim. Eight are `tests/ui_server/test_live_state.py::TestUIServerIntegration::{test_api_invalid_token_403, test_api_missing_job_404, test_brain_endpoint, test_dashboard_no_raw_leaks, test_put_rejected, test_readiness_endpoint, test_server_starts_and_writes_info, test_url_is_localhost_only}` and each carries, in the base run's own captured stderr, `ERROR: React UI not built.` — the named artifact is `apps/ui/dist`, which read STALE because `git worktree add` wrote `apps/ui/src` at mtime_ns 1787279477444570086 while `copytree` preserved the older 1787279383323951913 on the copied `dist/index.html`. The ninth, `tests/cli/test_review_bundle_runtime.py::TestSubprocessCleanup::test_timeout_raises_with_cleanup`, is the xdist-flake class: its repo-wide `pgrep -f "apps.cli.grouped.*--help"` matched pid 3247941, another worker's subprocess. CONFIRMING PROBE, serial, at the SAME base commit, after both suite runs: all nine exit 0 / `1 passed`. `full_log_provenance.txt` names every raw log's scratch path, line count and sha256 and states that raw logs stay outside the tracked tree while only derived `.txt` evidence is committed.
G11 R-0607's rule obeyed UNCONDITIONALLY, serially in the PRIMARY checkout AFTER both suite runs, never two pytest processes at once: `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf` exit 0, `160 passed in 20.44s`; then `python3 -m pytest tests/cli/test_golden_path.py -q -rf` exit 0, `42 passed in 21.98s`.
G12 `git diff --name-only b3146e91..4d1d3304` equals the Change list minus `.agent/handoff.md`, which C4 itself adds — 13 paths, none on either side alone. Each of the SIX paths named untouched is PRESENT at the base and ABSENT from the range. Every commit in the range has exactly one parent. Per-commit insertions 273, 205, 18, 2 and 284, every one under 500; each per-file `+/-` cell above is byte-identical to `git diff --numstat` (checklist item 28). Reflog, read from the OPERATION PREFIX before the first colon, TWO measured claims and NEITHER a total (R-0601, R-0605): taken AT commit 4d1d3304, where the round has made 5 commits, this round's entries whose prefix reads exactly `commit` number 5 — the two are EQUAL. Entries of this round whose prefix contains `amend`, `rebase` or `cherry` number 0 (R-0608), and this round produced NO `reset` entry at all, so none is owed a destination demonstration. Creating and removing the base worktree added NO entry to this HEAD reflog — the five entries above HEAD@{5}, which is the base b3146e91, are exactly the five commits — so there is no navigation entry to report as such. C4 is unwritten as this is composed (R-0494).
G13 Lines beginning `<<<SLICE ` or `<<<END `: 0 in `.agent/plan.md` at C1, 0 in `.agent/live_review.md` at C2, and 0 in `.agent/handoff.md` at C4 — the last measured after that commit and reported in the round report. `git push` run after C4; its real output is in the round report. No pull request created and no CI run awaited.
THE FOUR LOAD-BEARING NUMBERS: branch exit 0 / `17315 passed, 20 skipped in 144.91s (0:02:24)`; base exit 1 / `9 failed, 17188 passed, 20 skipped in 155.50s (0:02:35)`; branch-only failures 0; base-only failures 9. PARITY_CLAIM=VOID, honoured by per-id attribution. R18 IS THE ONLY ROUND OF F255 ENTITLED TO THE WORDS "full suite" — integration_gate.md reserves that claim for the gate entry.

## Authored-text proofs
Both slices were extracted programmatically by their marker lines from the COMMITTED `.agent/authored/f255-r18.md` at db723372 — never retyped, never re-wrapped, never edited — and applied byte for byte. Disk-to-disk transport equality is G2. The plan is proven by G4's byte-equality; the append by G5's prefix, remainder, separator, dual-reading and negative-control equalities. NO FROM/TO pair exists this round, so no containment reading and no FROM-zero count is owed (constraint 8, §4.9, R-0207). The nine evidence files are NOT authored text: they are generated from the runs and carry no transport proof.

## Deviations & assumptions
NO DEVIATIONS. The ordered bundle C0a..C4 was executed in order, one commit each, with no extra commit, no dropped commit and no reordering; no slice was edited and no slice is declared wrong. ASSUMPTION: G8 does not say WHICH checkout's `apps/ui/dist` to measure, so I measured BOTH the primary and the base worktree before and after; the void verdict rests on the base worktree's moved mtime, and the primary's unchanged reading is reported alongside it. ASSUMPTION: G10 mandates serial re-runs only for branch-only ids; I ran them for the nine BASE-only ids too, as the direct evidence the VOID claim demands. NOT CLAIMED: which process moved the base worktree's `dist` mtime was not identified — the base log holds 0 lines matching `auto-build (`, so `_auto_build_frontend` did not launch npm, and beyond that I assert nothing. ASSUMPTION: this session's shell guard rejects `VAR=value cmd` prefixes, shell loops, `$( )`, `${arr[0]}` and brace literals containing quotes, so every copy, extraction, measurement and run went through short Python scripts under the gitignored `.remedy-wt/.cache/gate_r18/` — scratch, NOT in the change set — with git, pytest and comm spawned as exact argv through `subprocess.run`, so every exit code above is the real one. ASSUMPTION on the reflog reading: this round's entries are those newer than the entry recording the base b3146e91, taken positionally from `git reflog`.

## Next
FIRST action of the next session: Phase 1 rule 1 — re-read `.agent/STOP` from disk. SECOND: the CLOSURE round per docs/roadmap/STATUS_closure_protocol.md — the evidence job, a FRESH review zip, the STATUS line authored by the reviewer and committed LAST, and the pull request, which is created THERE and merged at the NEXT feature's Open PR Gate, never in the session that creates it. R17 PASSED with no finding, and its verdict is ON DISK at C2. R-0607, R-0608 and R-0609 REMAIN OPEN: R-0607 needs a docs round promoting its rule into the docs/agents/planner_reviewer_prompt.md §3 checklist, and R-0608 and R-0609 bind the shape of future blocks rather than any code. R18 ITSELF IS THE ROUND WHOSE VERDICT IS NOT ON DISK, so it awaits review — and the gate verdict is the reviewer's to issue, not mine. There is no open pull request.
Fortschritt: ~95 % (T001 through T004 COMPLETE and REVIEWED · the integration gate ran the full suite on both sides at this round · only closure remains — evidence job, review zip, STATUS line and the pull request) — Schätzung
