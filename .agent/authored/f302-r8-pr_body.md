## What and why

F302 makes the `claude-cli` worker spend fewer tokens before it does any work. Each builder,
reviewer and planner call is a whole Claude Code session, and before F302 it loaded everything the
operator's account and the project carry: every built-in tool's description, `CLAUDE.md`, skills,
plugins, hooks and MCP servers. Measured at the claim on `6689c581e` through `remedy run show`
(`.agent/f302_inventory.md`): 77 recorded calls carry all four token figures, a builder's first call
wrote a median of 40,960 tokens into the cache and read 280,965 from it against 12 tokens of plain
input, and the jobs' `total_tokens` named 1.0 percent of what the calls moved.

Now:
- **Structural steps first (structure rule 2; DECISION F302 D1).** `build_claude_cli_args` moved to
  `packages/orchestration/claude_cli_command.py`, the catalog's `stats` group to
  `apps/cli/command_catalog_stats.py`, and the Claude CLI planner's keys to
  `packages/orchestration/config_keys_claude.py`. No behaviour changed; every row and pin of the
  structure ratchet they shrank fell with them.
- **T002, attribution (`.agent/f302_attribution.md`).** One fixed question, twenty calls through
  Remedy's own provider path, everything loaded and each source left out, in an empty repository and
  in a worktree of Remedy. The tools a builder does not use cost about 9,100 tokens; safe mode saved
  about 4,300 and 10,400; `--disable-slash-commands` raised the count; `--bare` refused the
  subscription's sign-in.
- **T003, the cut (DECISION F302 D2).** Every worker command line ends with `--safe-mode` and
  `--tools` naming the role's tools; `claude_cli.customizations` and `claude_cli.all_tools` turn each
  back on, and with both true the command line is the one before F302. Measured
  (`.agent/f302_after.md`): the fixed question fell from 21,533 to 7,051 tokens in an empty
  repository and from 28,056 to 7,407 in Remedy's; `SU-054` ran as a job each way, passed its review
  in two calls with the same change, and its builder's first call fell from 725,658 to 435,183.
- **T004, `remedy stats calls` (DECISION F302 D4).** Tokens of each kind per provider call, by role
  and provider, read from the run records, and per change a `remedy job apply` landed; an absent
  figure reads `unmeasured`, never 0.

## Key decisions
- DECISION F302 D1: the records are read through Remedy's own commands; the command line leaves
  `pingpong_provider.py` first; T002 runs through the provider path, at most twenty calls.
- DECISION F302 D2: the lean start is safe mode and the role's tools, each with a key; the settings
  files stay; a real job before and after replaces the gauntlet, whose builder is Ollama.
- DECISION F302 D3: a job's record of the configuration is carried to F297 as R-1235, because every
  writer of that record is on the structure page or bound by the run manifest's validation.
- DECISION F302 D4: `remedy stats calls` reads the run records; a landed change is a job whose
  `remedy job apply` landed.

## How to review
Read `docs/system/claude-cli-worker-launch-v1.md`, then `packages/orchestration/claude_cli_command.py`
with `tests/orchestration/test_claude_cli_command.py`, then `packages/orchestration/call_tokens.py`
and `apps/cli/commands/stats_calls_cmd.py` with their tests, then the two measurement pages under
`.agent/`.

## Changed files (at the accepted head `eff8cf434`, against the fork point `6689c581e`)

| Path | Lines |
|---|---|
| `apps/cli/command_catalog.py` | +5 / -162 |
| `apps/cli/command_catalog_stats.py` | +200 / -0 |
| `apps/cli/commands/__init__.py` | +2 / -1 |
| `apps/cli/commands/stats_calls_cmd.py` | +77 / -0 |
| `docs/README.md` | +2 / -0 |
| `docs/agents/planner_reviewer_prompt.md` | +8 / -0 |
| `docs/guides/environment.md` | +2 / -0 |
| `docs/roadmap/STATUS.md` | +1 / -1 |
| `docs/roadmap/features/T3_F302.md` | +48 / -0 |
| `docs/system/claude-cli-worker-launch-v1.md` | +68 / -0 |
| `docs/system/structure-ledger-v1.md` | +10 / -6 |
| `packages/orchestration/call_tokens.py` | +143 / -0 |
| `packages/orchestration/claude_cli_command.py` | +115 / -0 |
| `packages/orchestration/config.py` | +5 / -23 |
| `packages/orchestration/config_keys_claude.py` | +59 / -0 |
| `packages/orchestration/lessons.py` | +4 / -3 |
| `packages/orchestration/pingpong_provider.py` | +16 / -63 |
| `scripts/self_use_queue.json` | +8 / -0 |
| `tests/cli/test_stats_calls.py` | +109 / -0 |
| `tests/orchestration/import_reachability_allowlist.txt` | +5 / -0 |
| `tests/orchestration/test_call_tokens.py` | +132 / -0 |
| `tests/orchestration/test_claude_cli_command.py` | +160 / -0 |
| `tests/orchestration/test_lessons.py` | +8 / -0 |
| `tests/test_structure_ratchet.py` | +1 / -1 |
| `.agent/` (34 files: blocks, scripts, ledger, decisions, plan, inventory, readings, self-use record, closure suite) | +3003 / -245 |

The closing round adds the ledger's rotation, the STATUS line, the README sync, SU-054's
`consumed_by`, the Built State's closure paragraph and the handoff.

## Verification
- The closure's one full suite on the tree that ships: `22422 passed, 22 skipped`, exit 0
  (`.agent/authored/f302-closure-suite.txt`), 1213.06 CPU seconds, 1.3 percent below F301's.
- Evidence job `f302r7e1001` on `eff8cf434`: 2648 node ids, 2644 passed, 4 skipped,
  `is_valid_current_run True`.
- Package `remedy-review-20261010-110542-READY_FOR_REVIEW.zip`, SHA-256
  `f6139e2cda0c61198d62947ad819184bccbb7c058b49d6af5e5b9807b5ff75fd`, `READY_FOR_REVIEW`, review
  subject `6689c581e`..`eff8cf434`, in `/home/decodeux/Repos/remedy-history/zips`.
- Every production change was mutation-proved by the reviewer in a disposable worktree: thirteen
  mutations of the lean start and seventeen of `remedy stats calls`, each turning a test red.

## Latest verdict and findings
Rounds 1 to 7 reviewed; round 8, the closing round, is reviewed on this pull request. F302 is
accepted PASS_WITH_RISKS: R-1235, the job record of the configuration, and 15 earlier findings stay
open, all owned by the findings paydown F297.

## Runtime actuals
Eight delegated rounds in one session on 2026-10-10. Provider calls F302 itself made: 20 for T002,
4 for the fixed question and 4 in two jobs for T003, and 2 in the closure's self-use job, all on
`claude-cli` with `claude-sonnet-4-6`; the session's own model calls are not measured by Remedy's
ledger.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
