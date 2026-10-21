# Handback — F303 round 4: book round 3, repair R-1407 and R-1408, and the MCP protocol core

## Session

SESSION 1 of feature F303 · round 4 · rounds so far 4

Context self-assessment: this worker verified every prepared digest, byte-copied the four C1
files, repaired the two findings round 3 raised exactly as their THE FIX sentences say, wrote the
new MCP stdio protocol core and its tests from the block's own specification, and closed all six
gates green.

Fortschritt: ~60 % (note route and MCP core landed · MCP tools and command open) — Schätzung

## Range

Review of `10102fa9e`..`HEAD` on `feature/f303-face-public-api`.

## Commits

### 4fb49f8c3 F303 R4 C1: book round 3, register R-1407 and R-1408, DECISION F303 D4 and the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f303-r4.md` | 144/0 | this round's block, byte copy (144 lines, sha256 `df997675a7e0ea45265f21ffb3368a6a419a8aee7411e6b25537fbec9f099ebd`, equal to `block.md`) |
| `.agent/live_review.md` | 6/0 | prepared file, byte copy: Gate F303 R3, R-1407, R-1408 appended |
| `.agent/decisions.md` | 12/0 | prepared file, byte copy: DECISION F303 D4 appended |
| `.agent/plan.md` | 7/10 | prepared file, byte copy: rewritten for F303 round 4 |

### 821f8d980 F303 R4 C2: job steer declares its outcome key, and an ended job's note_open is tested (R-1407, R-1408)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/job_steer_cmd.py` | 2/2 | `JOB_STEER_ANSWER_KEYS` gains `outcome` in sorted position (R-1407) |
| `tests/cli/test_client_interface.py` | 5/6 | the `_cmd_job_steer:**result` `UNRESOLVED_ANSWER_SITES` entry names the site's real keys and drops the sentence that justified leaving `outcome` out; the now-unused `JOB_STEER_ANSWER_KEYS` import removed |
| `tests/cli/test_job_steer.py` | 11/0 | `test_an_accepted_note_answers_exactly_the_declared_keys`: an accepted note's JSON keys, less `RESERVED_KEYS`, equal `set(JOB_STEER_ANSWER_KEYS) - {"matches"}` (R-1407) |
| `tests/orchestration/test_client_story.py` | 15/0 | `test_note_open_is_false_for_an_ended_job_with_a_pending_task`, parametrized over `failed` and `cancelled`, a pending task included (R-1408) |
| `docs/system/machine-client-contract-v1.md` | 1/1 | generated section regenerated (`write_client_interface_page`) for `job.steer`'s new answer key |

### 5dfc84318 F303 R4 C3: the MCP protocol core, closed by default (DECISION F303 D4)
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/mcp_server.py` | 155/0 | NEW FILE: `serve_mcp`, `McpTool`, `McpServerError`, the protocol version and the four JSON-RPC error codes, standard library only (DECISION F303 D4 (1), (2)) |
| `tests/test_no_orphan_modules.py` | 2/0 | `ALLOWED_UNWIRED` gains the new module in sorted position: "F303's MCP protocol core; round 5's client mcp command wires it (DECISION F303 D4)" |

### a85c71620 F303 R4 C4: tests of the MCP protocol core
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_mcp_server.py` | 164/0 | NEW FILE: 15 tests over `io.StringIO`, two stand-in tools (`echo`, `fails`) — `initialize`/notification/`tools/list`, the closed-by-default allowlist, the call result's three keys, seven parametrized refusals, a notification of an unknown method, `ping`, the two `McpServerError` cases, and the blank-line/return-value case |

### (this commit) F303 R4 C5: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## External actions

- `git push origin feature/f303-face-public-api` follows this commit; its outcome is reported in
  the session reply.
- No pull request (the block orders none). No merge, no worktree added or removed, no provider
  call. `gh pr list --state open` was not re-checked this round (no new branch was created; the
  Open PR Gate was already satisfied in round 1).

## Verification

Preconditions: `block.md` (144 lines), `verify.py`, `run_selection.py`, `selection.txt` and
`digests.txt` matched the digests given in the prompt; the four `c1-` files matched the digests in
`digests.txt`, and `c1-.agent__authored__f303-r4.md` read the same sha256 as `block.md`
(`df997675a7e0ea45265f21ffb3368a6a419a8aee7411e6b25537fbec9f099ebd`, both 144 lines). Before the
first write, `HEAD` read `10102fa9e`, the tree was clean, and `.agent/STOP` was absent.

1. Gate 1: `git status --porcelain` empty. `python3 .remedy-wt/f303-r4/prep/verify.py .` (run after
   C4, before this handback) — every check `True` (18 of them), `absent` for C5, last line
   `ALL True`.
2. Gate 2: `python3 -m ruff check` over every Python file C2 to C4 touched (7 files) —
   `All checks passed!`
3. Gate 3: `python3 .remedy-wt/f303-r4/prep/run_selection.py . .remedy-wt/f303-r4-worker/selection-output.txt`
   — exit 0; `changed tests: ['tests/cli/test_client_interface.py', 'tests/cli/test_job_steer.py',
   'tests/orchestration/test_client_story.py', 'tests/orchestration/test_mcp_server.py',
   'tests/test_no_orphan_modules.py', 'tests/test_structure_ratchet.py',
   'tests/ui_server/test_public_api.py']`; `paths 91`; `4157 passed, 2 skipped in 107.40s`; no
   FAILED, ERROR or "process(es) behind" line. The two SKIPPED lines: `tests/test_agent_tooling.py:43`
   (D12 quarantine, pre-existing) and `tests/test_install_smoke.py:175` (opt-in, pre-existing).
4. Gate 4: `python3 -m apps.cli.main integrity check --json` — `fail_count` 1, only
   `high_blockers_open`: `R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359,
   R-1360, R-1361, R-1362` — the same twelve findings as rounds 1 to 3.
5. Gate 5: `python3 -c "import scripts.rotate_live_review as r;
   print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` — `90`.
6. Gate 6: `git -C . diff --stat 10102fa9e HEAD -- packages/orchestration/ui_server.py
   packages/orchestration/serve_daemon.py apps/cli/command_catalog.py` — prints nothing.

## Authored-text proofs

C1's `.agent/authored/f303-r4.md`: byte copy of `c1-.agent__authored__f303-r4.md`, itself
byte-equal to `block.md` (144 lines, sha256
`df997675a7e0ea45265f21ffb3368a6a419a8aee7411e6b25537fbec9f099ebd`), both readings matching before
the commit (reported at the start of this session) and again by `verify.py`'s four `C1 ... equals
...` lines, every one `True`. C2 through C4 applied no reviewer-authored text; `mcp_server.py` and
its tests are this worker's own, written from `## Change set — C3` and `C4` of `block.md` and from
DECISION F303 D4's literal text; C2's two fixes follow R-1407's and R-1408's THE FIX sentences
literally.

## Deviations & assumptions

**The Session line carries the template's `rounds so far` suffix, which the block's own quoted
text (`SESSION 1 of feature F303 · round 4`) does not include.** `docs/agents/handback_template.md`
makes the full line — `SESSION <n> of feature <Fxxx> · round <r> · rounds so far <total>` —
mandatory, and round 3's own handback carried it (`· rounds so far 3`). Added `· rounds so far 4`,
following F060 round 1's accepted precedent for the same gap.

No other deviation. Every path, body shape, protocol method, error code, refusal wording and
test case follows `block.md`'s C1 through C4 and DECISIONs F303 D4, R-1407 and R-1408's literal
THE FIX sentences; `docs/system/machine-client-contract-v1.md`'s regeneration is the one "pinned
generated artifact" C2's own instructions anticipated and name by its writer
(`write_client_interface_page`).

## Next

The next session's first action names Phase 1 rule 1 (`.agent/STOP`) before rule 2 (the Open PR
Gate). Book this round's verdict in round 5's first commit. Round 5: the MCP tools (`verify`,
`gate_status`, `evidence_bundle`), the `remedy client mcp --allow <tool>` command, and the
`docs/system/mcp-server-v1.md` page (DECISION F303 D4 (3)).

Operator questions open: 3
Open findings: 90

## For the operator, in plain sentences

Round 3's two small findings are repaired: `remedy job steer`'s JSON answer now declares the
`outcome` key it always actually sends, and the run story's note-open flag is now proven false for
a job that has already failed or been cancelled even while one of its tasks is still waiting — not
just for one that finished cleanly. The bigger piece of this round is new: a small, self-contained
module that speaks the Model Context Protocol's wire format over standard input and output, the
same way any MCP-aware tool starts a server as a child process and talks to it. It understands four
requests — say hello, check it's alive, list its tools, and call one — and it offers nothing at all
unless the person who starts it names which tools to turn on. It does not yet do anything useful by
itself: round 5 gives it the three real tools (verify, gate status, evidence bundle), the command
that starts it, and its documentation page.
