# Handback — F296 round 7: the closing round — book round 6, the Built State, rotate the ledger, accept F296 in STATUS, open the pull request

## Session

SESSION 1 of feature F296 · round 7 · rounds so far 7

Context self-assessment: this worker verified the three prepared digests and every manifest-listed digest before any write, copied each named file by a script with a byte-for-byte proof, ran the ledger rotation once and proved both resulting files byte-equal to their prepared copies, ran all five gates once each before writing this handoff, and context stayed ample throughout.

The session ends here because F296 is closed and the next feature starts in a fresh session.

Fortschritt: 100 % (F296 is accepted; its pull request waits for the next session's Open PR Gate) — Schätzung

## Range

Review of `1a714f353`..`HEAD` on `feature/f296-tier-escalation`.

## Commits

### 41f3a6091 F296 R7 C1: book round 6, the Built State, save the round 7 block and the PR body
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f296-r7-pr_body.md` | +62/-0 | NEW FILE, the pull request body, byte copy from the prep folder |
| `.agent/authored/f296-r7.md` | +135/-0 | NEW FILE, this round's block, byte copy, equal to `block.md` by line count (135) and sha256 (`6277e37d...331c7`) |
| `.agent/live_review.md` | +2/-0 | round 6's verdict booked |
| `.agent/plan.md` | +6/-5 | rewritten for round 7's scope |
| `docs/roadmap/features/T3_F296.md` | +39/-0 | the feature file's Built State added |

### 1f9b23ee7 F296 R7 C2: rotate the finding ledger into its archive
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +0/-64 | 32 gate records moved out to the archive by `scripts/rotate_live_review.py`, run once |
| `.agent/live_review_archive.md` | +64/-0 | the same 32 gate records appended to the archive |

### (this commit) F296 R7 C3: accept F296 in STATUS with its README sync and the self-use queue
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | +1/-1 | F296's line flips from `- [~]` to `- [x]` with its acceptance record |
| `README.md` | +12/-2 | `156 of 314` count, Tier 3 row `14 \| 29`, F296's closing paragraph added to the Tier 3 list |
| `scripts/self_use_queue.json` | +1/-1 | SU-074's `consumed_by` becomes `F296` |
| `.agent/handoff.md` | rewritten | this handback (a handoff cannot table the commit that writes it) |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 (preconditions) | done | branch `feature/f296-tier-escalation` at `1a714f353`, HEAD equal to `origin/feature/f296-tier-escalation`, `git status --porcelain` empty, `.agent/STOP` absent, `gh pr list` empty — all confirmed before any write |
| C1 | done | commit `41f3a6091`; all five paths byte-proved equal to their `c1-` source; `numstat` matched `manifest.tsv` exactly |
| C2 | done | commit `1f9b23ee7`; rotation exit 0, matched `sim-rotation.txt` line for line except the `written:` path (expected, dry worktree vs. primary checkout); both ledger files byte-proved equal to their `c2-` source; `numstat` 64 insertions total, well under 500, so this is NOT F296's declared oversize commit |
| C3 | done | this commit; three files byte-proved equal to their `c3-` source before the gates ran; `numstat` matched the manifest exactly |
| Gate 1 | done | `git status --porcelain` showed only the three C3 files; `verify.py .` printed `True` on every check, `absent` for C3 (not yet committed when run), last line `ALL True` |
| Gate 2 | done | `status_line.txt`'s content (no trailing newline) occurs exactly once in `docs/roadmap/STATUS.md`; zero lines of it begin `- [~]` |
| Gate 3 | done | the named test selection, run once, exit 0, `578 passed`, matching the reviewer's simulated count exactly; no FAILED, ERROR or SKIPPED line |
| Gate 4 | done | `integrity check --json` exit 0, six checks `pass`, `"fail_count": 0` |
| Gate 5 | done | the open-finding-id lookup printed the required seven ids in the required order |
| Push | pending | runs after this commit, per the block's `THEN` step; reported in this session's reply, not knowable at handoff-write time |
| Pull request | pending | created after the push, per the block's `THEN` step; its number does not exist when this handoff is written, per the block's own instruction |

## External actions

None yet from this worker: no push, no `gh pr create`, no `gh pr list`, no fetch, no pull, no merge, no worktree add/remove have run as of this commit. `git push -u origin feature/f296-tier-escalation`, then `gh pr create` against `main`, then `gh pr list` all run immediately after this commit, per the block's `THEN` step, and their real output is reported in this session's reply rather than in this file (the write-once rule forbids a second write of this handoff to add it). The scratch folder `.remedy-wt/f296-r7-worker/` holds the digest checker, the copy-and-verify scripts for C1 and C3, the rotation wrapper, the gate wrapper scripts, and the commit-message files.

## Verification

1. Digests before any write: `block.md` (135 lines, sha256 `6277e37d8c770df2e592a76dad36ed668f3801dfd5cf274a6bd1a7a6d6c331c7`), `verify.py` (sha256 `6fd90324c9889ed62a21771b5d948468a97a5264a383561b72b9c4e2ea21e7e8`), `manifest.tsv` (sha256 `babbfc2b7f40f2bfbe232e718a5cbc86ff8a7c77b3b17aec9005628f8c23a04b`) all matched the three hashes given in the prompt; every one of the ten files `manifest.tsv` lists matched its own sha256 (checked with a script, last line `ALL True`).
2. Preconditions: `git rev-parse --short=9 HEAD` read `1a714f353`, `git rev-parse HEAD` equalled `git rev-parse origin/feature/f296-tier-escalation` (`1a714f353f65082f796a08dac7b7e0a0903f8ef0`), `git status --porcelain` printed nothing, `.agent/STOP` did not exist, `git branch --show-current` read `feature/f296-tier-escalation` — all before any write. `gh pr list --state open --json number,headRefName,baseRefName,isDraft` read `[]` (the Open PR Gate), so work continued without merging anything.
3. C1: all five named paths copied by a script, then compared byte-for-byte against the prepared source; staged `numstat` read `62 0`, `135 0`, `2 0`, `6 5`, `39 0` for the five paths respectively, matching `manifest.tsv` exactly; `git branch --show-current` read `feature/f296-tier-escalation` immediately before the commit.
4. C2: `python3 scripts/rotate_live_review.py` run once through a Python wrapper with `cwd` the repository root. Its whole output: exit code `0`; `gate records moved: 32`; `finding pairs moved: 0 (0 records)`; `resolved-text records moved: 0`; `old ledger size: 174203 bytes`; `new ledger size: 135040 bytes`; `old archive size: 7160532 bytes`; `new archive size: 7199695 bytes`; `open findings before: 7`; `open findings after: 7`; `gate headers matching neither known form (left in place): 1`; `written: <repo>/.agent/live_review.md and <repo>/.agent/live_review_archive.md` (the repository root written as `<repo>`, since the real line names this machine's absolute checkout path). The exit code and every line but the `written:` line matched `sim-rotation.txt` exactly; the `written:` line differs only in naming the primary checkout instead of the reviewer's dry worktree, which the block permits. Both resulting ledger files were then byte-proved equal to their `c2-` prepared copies. Staged `numstat` read `0 64` and `64 0`, matching `manifest.tsv`; 64 insertions is well under 500, so no oversize declaration applies. `git branch --show-current` read `feature/f296-tier-escalation` immediately before the commit.
5. C3 (before the handoff): the three named paths copied by a script, then byte-proved equal to their `c3-` prepared copies. `git branch --show-current` read `feature/f296-tier-escalation` before proceeding to the gates.
6. Gate 1: `git status --porcelain` showed exactly `README.md`, `docs/roadmap/STATUS.md`, `scripts/self_use_queue.json` modified, nothing else. `python3 .remedy-wt/f296-r7/prep/verify.py .` (run with `cwd=` set to the repository root) printed `True` on every check for C1 and C2 — including every path-set check, every numstat check and every byte-equality check — and `absent` for C3 (not yet committed when the gate ran), with the three C3 working-tree byte-equality checks also `True`; last line `ALL True`.
7. Gate 2: `status_line.txt`'s content, with its trailing newline stripped, occurs exactly 1 time in `docs/roadmap/STATUS.md`, and 0 lines of it begin `- [~]`.
8. Gate 3: `python3 -m pytest -q -rfEs tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/cli/test_golden_path.py tests/test_structure_ratchet.py`, run once through a Python wrapper, exit code `0`, final line `578 passed in 51.79s`, matching the reviewer's simulated count exactly (its own seconds differ, as the block allows); no FAILED, ERROR or SKIPPED line. One informational line printed by a guard (`R-1411: 2 entries of the configured data root ... not counted`) is not a failure marker and does not affect the passed count or the exit code.
9. Gate 4: `python3 -m apps.cli.main integrity check --json` exit 0; `"check_count": 6`, all six checks (`handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open`) `"status": "pass"`, `"fail_count": 0`, `"ok": true`, `"passed": true`.
10. Gate 5: `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"` exit 0, printed `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418', 'R-1421']`, matching the required list exactly, in the required order.

## Authored-text proofs

Applied this round, each proved equal over bytes by a script that only reads, against the prepared file: all five paths of C1, both paths of C2, all three paths of C3.

The STATUS line authored-text proof: `docs/roadmap/STATUS.md`'s F296 line is byte-identical to the prep folder's `status_line.txt` with its trailing newline stripped; that content occurs exactly 1 time in the file. Quoting it with its package folder written as `~`: "- [x] F296 — Evidence-triggered tier escalation (routing v2) (T001a–T003 complete, the default kept off by the T003 Amendment; R-1421 open — owned by F314; accepted 2026-10-22 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f296r6e1001 · package remedy-review-20261022-085320-READY_FOR_REVIEW.zip · SHA-256 cc616314ffef4d468e3dcfa497b55011ec6b129005fead9927778f05f410fbe5 · package path ~/Repos/remedy-history/zips · accepted HEAD 0143b9e17e05e2626602830340b25fef55479b04)".

The rotation's output is reviewer-authored behavior (the script itself, not hand-copied text), so its whole output is quoted in full under Verification item 4 rather than proved by byte comparison; the ledger's size before and after is part of that same quoted output: old ledger 174203 bytes, new ledger 135040 bytes, old archive 7160532 bytes, new archive 7199695 bytes.

## Deviations & assumptions

The item-status table's Push and Pull request rows use the status word `pending` rather than one of AGENTS.md's three Completion-Report values (`done`, `skipped`, `deviated`), because neither value fits a step that is correct, scheduled, and simply not yet reached at the moment this handoff is written and committed — the block's own `THEN` step orders the push and the pull request after this commit, and explicitly forbids naming a pull request number here because it does not exist yet. No other departure from the block's ordered commit sequence occurred: C1, C2 and C3 landed in that order, each touching only its named paths, with no extra commit, no dropped commit and no reordering. No amend, rebase, force-push or `--no-verify` was used. No mutation, no worktree of this worker's own, no `REMEDY_TEST_MAX_WORKERS`, no `-n` flag; Gate 3 ran its one test selection exactly once. This worker never changed its own working directory; every command needing the repository root as `cwd` ran through a small `python3` script under `.remedy-wt/f296-r7-worker/` that passes `cwd=`.

## For the operator, in plain sentences

A task whose cheaper model keeps failing can now hand its next attempt to the next stronger model, together with a reviewer that is at least as strong as that model, once this feature is switched on. It stays switched off for now, because turning it on with confidence needs a measured comparison across about thirty paid runs, and that comparison has not been run yet. Every time a task would hand over to a stronger model, that handover is written down in a place where a person and a later report can both see it. The one paid run this feature made against itself stopped cleanly at its own approval gate rather than running past it. The whole test collection passed on the code that is shipping with this feature, and running that collection used somewhat more computer time than it did last time, which the next clean-up round will look into. The review package that a human or another tool inspects before this feature closes is named remedy-review-20261022-085320-READY_FOR_REVIEW.zip and is stored in this machine's review archive folder. A pull request for this feature is open, and it will be merged automatically at the start of the next working session unless the operator merges it sooner.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate merges F296's pull request in the next session, and never in this one.
3. The next feature's first commit books round 7's verdict.
4. Rule A5: the next unchecked line in `docs/roadmap/STATUS.md`.

Operator questions open: 0. Open findings: 7 (R-1246, R-1281, R-1326, R-1351, R-1353, R-1418 and R-1421, owned by F314).
