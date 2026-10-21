# Handback — F060 round 4: round 3 booked, the two certificate commands, their tests and the page landed

## Session

SESSION 1 of feature F060 · round 4 · rounds so far 4

Context self-assessment: this worker verified every prepared digest, made C1 and C4 by byte copy, wrote the handler, the catalog module and all tests itself, ran each gate once, and wrote this handback with ample context margin left.

Fortschritt: ~80 % (T001 to T003 landed · the closure open) — Schätzung

## Range

Review of `47aa01140`..`HEAD` on `feature/f060-long-run-certificate`.

## Commits

### c674dcc7f F060 R4 C1: book round 3, resolve R-1405, DECISION F060 D4 and the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f060-r4.md` | 180/0 | this round's block, byte-saved for the authored-text proof |
| `.agent/live_review.md` | 4/0 | round 3 booked, R-1405 resolved |
| `.agent/decisions.md` | 10/0 | DECISION F060 D4 appended |
| `.agent/plan.md` | 7/9 | rewritten |

### fe18a4aee F060 R4 C2: remedy job certificate and remedy verify (T003)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog_certificate.py` | 47/0 | new: `JOB_CERTIFICATE_COMMANDS` and `VERIFY_COMMANDS` |
| `apps/cli/commands/certificate_cmd.py` | 138/0 | new: handlers of `job.certificate` and `verify.run` |
| `apps/cli/command_catalog.py` | 4/4 | import, two splices, group `verify`; four default-repeating lines deleted (2314 lines before and after) |
| `apps/cli/commands/__init__.py` | 2/1 | the module joins the collection |
| `apps/cli/grouped.py` | 1/1 | `"verify": "run"` in the default-command table |
| `tests/cli/test_cli_ux.py` | 5/3 | `verify` joins the internal groups; 36 groups |
| `tests/test_no_orphan_modules.py` | 0/2 | the verifier's unwired entry deleted |
| `tests/orchestration/import_reachability_allowlist.txt` | 7/0 | the seven names the reachability test asked for |
| `docs/guides/exit-codes.md` | 1/0 | row for the certificate command |

### 19d144207 F060 R4 C3: tests of remedy job certificate and remedy verify, and the standalone check
| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_certificate_cmd.py` | 312/0 | new: writes, refusals, verify, and the fresh-folder subprocess check |

### ff5d46ff8 F060 R4 C4: the job certificate page and its index rows
| Path | +/- | Reason |
|---|---|---|
| `docs/system/job-certificate-v1.md` | 72/0 | new: the page |
| `docs/README.md` | 2/0 | two index rows |

### C5 F060 R4 C5: handback (this commit)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | edited | this handback |

## External actions

- `git push origin feature/f060-long-run-certificate` follows this commit; its outcome is reported in the session reply. No pull request was opened. No worktree was added or removed.

## Verification

Preconditions: `block.md`, `verify.py`, `run_selection.py`, `selection.txt` and `digests.txt` matched the digests in the prompt; the six `c1-` and `c4-` files matched `digests.txt`. The saved block copy has 180 lines and sha256 `8ffc08529ace480af3ab3d7f62ce79483d6938a6d37dc307eb5ad50078ee41b6`, equal to `block.md`.

1. Gate 1: `git status --porcelain` empty; `python3 .remedy-wt/f060-r4/prep/verify.py .` — every line `True`, C5 `absent`, last line `ALL True`.
2. Gate 2: `python3 -m ruff check` over the eight Python files C2 and C3 touched — `All checks passed!`
3. Gate 3: `python3 .remedy-wt/f060-r4/prep/run_selection.py . .remedy-wt/f060-r4-worker/selection-output.txt` — `paths 85`, `exit 0`, `4170 passed, 2 skipped in 53.47s`; no FAILED, ERROR or `process(es) behind` line; two SKIPPED lines (the D12 quarantine of the deleted reviewer agent file; install smoke is opt-in).
4. Gate 4: `python3 -m apps.cli.main integrity check --json` — exit 1, `fail_count` 1, only `high_blockers_open`: `12 open blocker/high: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362`.
5. Gate 5: `open_finding_ids` over `.agent/live_review.md` — `88`.
6. Gate 6 (by the reviewer's ruling): `python3 -m apps.cli.main verify --help` — exit 0, names the `run` subcommand; `python3 -m apps.cli.main verify run --help` — exit 0, shows `Usage: remedy verify run [OPTIONS] BUNDLE` and the `bundle` argument.

## Authored-text proofs

C1 and C4: the prepared `c1-` and `c4-` files are byte copies, proven equal by sha256 at copy time and again by `verify.py`. C2 and C3 are the worker's own code and tests.

## Deviations & assumptions

- Gate 6 read by the reviewer's ruling: the group help names the run subcommand and `verify run --help` names the bundle argument; the block's wording expected the group help to name it.
- To pay for the four added lines in the catalog file, the deleted lines are the two default-repeating pairs of `chat.send` and `chat.ask`.
- `--out` and `--max-bytes` carry no catalog default; an absent `--max-bytes` is read as the 8 MiB default in the handler.
- The "id that names no job" test covers both refusals: a malformed id gives the id resolver's refusal (exit 1), and a well-formed unknown id gives `certificate_not_ready` (exit 3).
- No mutation red-proofs and no full-suite run, as the block orders.

## Next

In order: Phase 1 rule 1 (`.agent/STOP`), then rule 2 (Open PR Gate), then book round 4's verdict in the next round's first commit, then the closure sequence.

Operator questions open: 3
Open findings: 88

For the operator: Remedy can now make a small certificate file for a job that has ended, and anyone can check that file on another machine without Remedy's data folder. The two commands, their tests and a documentation page are in place. The tests chosen for this round all passed, including one that runs the check in an empty folder and shows no data folder is created. The certificate is a proof that the files are intact and agree with each other, not a signature. The closure of this feature is still open.
