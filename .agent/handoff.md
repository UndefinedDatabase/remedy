# Handback — F303 round 5: book round 4, repair R-1409, and the MCP tools, the command and the page

## Session

SESSION 2 of feature F303 · round 5 · rounds so far 5

Context self-assessment: this worker verified every prepared digest, byte-copied the C1 files, wrote the three tools, the command, their tests and the page from the block and DECISION F303 D5, hit two guards the block did not foresee (the reachability allowlist and the vocabulary check), and ran the gates after C5.

Fortschritt: ~75 % (every task landed · closure open) — Schätzung

## Range

Review of `024a573ad`..`HEAD` on `feature/f303-face-public-api`.

## Commits

### 6677de1fa F303 R5 C1: book round 4, register R-1409, DECISION F303 D5 and the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f303-r5.md` | 167/0 | this round's block, byte copy (167 lines, sha256 `812281310fa47cbd2fb635d627aa65eef52aca36bca8813298d8d90ef37c0441`, equal to `block.md`) |
| `.agent/live_review.md` | 4/0 | prepared file, byte copy: Gate F303 R4 and R-1409 |
| `.agent/decisions.md` | 12/0 | prepared file, byte copy: DECISION F303 D5 and the operator answers' entries |
| `.agent/plan.md` | 6/5 | prepared file, byte copy |

### 9dda121a5 F303 R5 C2: a tool name that is not a string is refused, not a crash (R-1409)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/mcp_server.py` | 1/1 | `tools/call`: a `tool_name` that is not a `str` is answered `MCP_INVALID_PARAMS` with the not-offered message |
| `tests/orchestration/test_mcp_server.py` | 3/0 | the case `a_tool_name_that_is_a_list` (id 10) joins the parametrized refusal test |

### a9b89f156 F303 R5 C3: the three MCP tools run their twin commands (DECISION F303 D5 (1))
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/mcp_tools.py` | 143/0 | NEW FILE: `MCP_TOOL_NAMES`, `MCP_TOOL_TIMEOUT_SECONDS`, `run_remedy_json`, `remedy_mcp_tools` |
| `tests/orchestration/test_mcp_tools.py` | 115/0 | NEW FILE: 23 cases over a fake `run`, and three real-child cases of `run_remedy_json` |
| `tests/test_no_orphan_modules.py` | 2/2 | `mcp_tools.py` joins `ALLOWED_UNWIRED` as the block says, and `mcp_server.py`'s entry leaves, because `mcp_tools.py` now imports it and the list's own stale-entry test requires that |

### 5672e1058 F303 R5 C4: remedy client mcp serves the tools over stdio, closed by default
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog_client.py` | 16/0 | the `client.mcp` entry after `client.diff` |
| `apps/cli/commands/client_mcp_cmd.py` | 37/0 | NEW FILE: `_cmd_client_mcp`, `COMMAND_HANDLERS`; version read with `apps.cli.version_report.resolve_distribution_version` (the reader `remedy --version` uses; it answers `dev` in a checkout) |
| `apps/cli/commands/__init__.py` | 2/1 | the module registered |
| `tests/cli/test_client_mcp_cmd.py` | 123/0 | NEW FILE: four real child-process sessions (a) to (d) |
| `tests/orchestration/import_reachability_allowlist.txt` | 3/0 | guard-demanded: the three new modules joined the measured closure, in sorted position |
| `tests/test_no_orphan_modules.py` | 0/2 | `mcp_tools.py` leaves `ALLOWED_UNWIRED` |

### d7b0a599b F303 R5 C4: the client mcp description carries the word check the vocabulary guard needs
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog_client.py` | 1/1 | "verify" became "verify check" in the description: `tests/docs/test_vocabulary.py` refuses the word Gate without one of `check`, `pass`, `block` |

### a34715078 F303 R5 C5: the MCP server page and its index line
| Path | +/- | Reason |
|---|---|---|
| `docs/system/mcp-server-v1.md` | 81/0 | NEW FILE: closed by default, the server entry, the three tools, one exchange, "Remedy deliberately does not" |
| `docs/README.md` | 2/0 | quick-find row "MCP / Model Context Protocol" and the index line |

### (this commit) F303 R5 C6: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |
| `.agent/operator_questions.md` | byte copy | `c6-.agent__operator_questions.md` (the empty line the operator's commit left out) |

## External actions

- `git push origin feature/f303-face-public-api` follows this commit; its outcome is in the session reply.
- No pull request, no merge, no worktree added or removed, no provider call.

## Verification

Preconditions: the five prepared digests and the five `c1-`/`c6-` digests matched; the saved block and `block.md` both read 167 lines and the sha256 above. Before the first write `HEAD` was `024a573ad`, equal to `origin/feature/f303-face-public-api`, the tree was clean and `.agent/STOP` was absent.

1. Gate 1: `git status --porcelain` empty. `python3 .remedy-wt/f303-r5s2/prep/verify.py .` (after C5) read `ALL False`: two lines were `False`, "every commit carries a F303 R5 Cn subject: 5 of 6" and "C4 paths ['apps/cli/command_catalog_client.py']", both caused by the one extra commit `d7b0a599b` (see Deviations); every other line was `True`, `absent` for C6.
2. Gate 2: `python3 -m ruff check` over the nine Python files C2 to C4 touched — `All checks passed!`
3. Gate 3: `python3 .remedy-wt/f303-r5s2/prep/run_selection.py . .remedy-wt/f303-r5s2-worker/selection-output.txt` — exit 0; changed tests `tests/cli/test_client_interface.py, tests/cli/test_client_mcp_cmd.py, tests/cli/test_job_steer.py, tests/orchestration/test_client_story.py, tests/orchestration/test_mcp_server.py, tests/orchestration/test_mcp_tools.py, tests/test_structure_ratchet.py, tests/ui_server/test_public_api.py`; `paths 95`; `4591 passed, 2 skipped in 109.31s`; no FAILED, ERROR or "process(es) behind" line. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine) and `tests/test_install_smoke.py:175` (opt-in).
4. Gate 4: `python3 -m apps.cli.main integrity check --json` — `fail_count` 1, only `high_blockers_open`: R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362, the same twelve.
5. Gate 5: `open_finding_ids` over `.agent/live_review.md` — `91`.
6. Gate 6: `git -C . diff --stat 024a573ad HEAD -- packages/orchestration/ui_server.py packages/orchestration/serve_daemon.py apps/cli/command_catalog.py docs/guides/exit-codes.md` — prints nothing.

## Authored-text proofs

C1's `.agent/authored/f303-r5.md` is a byte copy of `c1-.agent__authored__f303-r5.md` and of `block.md` (167 lines, sha256 `812281310fa47cbd2fb635d627aa65eef52aca36bca8813298d8d90ef37c0441`); the other three C1 files and the C6 operator-questions file matched their `digests.txt` sha256 after copy. The code, tests and page of C2 to C5 are this worker's own, written from the block and DECISION F303 D5.

## Deviations & assumptions

**An extra commit, `d7b0a599b`, between C4 and C5.** After C4 the page's docs tests ran (`tests/docs`) and `test_vocabulary.py` refused the `client.mcp` description, because it used the word Gate without `check`, `pass` or `block`. The fix is one word in the catalog entry. I did not amend C4, so it is its own commit with a C4 subject; this is why `verify.py` reads two `False` lines.

**Two guard-demanded paths.** `tests/orchestration/import_reachability_allowlist.txt` (C4) and `mcp_server.py`'s entry leaving `ALLOWED_UNWIRED` already in C3 (the block placed that exit in C4 for `mcp_tools.py` only).

**Test runs outside the gates.** To see guards refuse or pass before committing I ran `tests/orchestration/test_mcp_server.py`, `test_mcp_tools.py`, `tests/test_no_orphan_modules.py`, `tests/test_command_catalog.py`, `tests/cli/test_exit_codes.py`, `tests/orchestration/test_import_reachability.py`, `tests/cli/test_client_mcp_cmd.py` and `tests/docs`, one command at a time. No mutation or full-suite run.

**Assumptions.** `gate_status` keeps the four keys that are present in an `ok` story and adds no `ok` key, following DECISION F303 D5 literally; a given `out` that is `null` is refused like any non-string.

## Next

The next session's first action names Phase 1 rule 1 (`.agent/STOP`) before rule 2 (the Open PR Gate). Book round 5's verdict in the next round's first commit. Round 6: the closure's integration gate.

Operator questions open: 0
Open findings: 91

## For the operator, in plain sentences

Remedy can now be started as an MCP server by a program that orchestrates other tools: `remedy client mcp --allow verify` offers only the tools you name, and with no `--allow` it offers nothing. The three tools check a certificate, read a job's gate status, and write a job's evidence certificate; each runs the matching Remedy command and answers exactly what that command prints. A real session through the command passed in tests, including a second write to the same path being refused. The page `docs/system/mcp-server-v1.md` explains how to start it and what it will not do. Round 4's small finding, that a tool name sent as a list crashed the server, is repaired.
