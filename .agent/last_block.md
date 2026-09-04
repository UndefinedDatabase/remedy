── STEP scope-report — F262 List commands v2 ────────────────────────
Goal: Book round 20's already-PASSED verdict (GATE20) into the ledger, register finding R-0795 (`config.list`/`worker.list`/`execution.list` parse all four T003 flags via the catalog's mechanical `_with_list_options` attachment but their handlers silently discard them, measurably violating T2_F262.md's Acceptance bullet on `--sort` validation), and write this session's handback as a SCOPE REPORT per operator amendment amend0827-process-diet rule 6 (docs/agents/planner_reviewer_prompt.md §3, docs/agents/self_drive_protocol.md "Ending a session") — this feature has now run 7 sessions, its stated soft limit, so this round's obligation is a report, not more build work. No production or test code is touched this round.

Bundle:
C0a. Save this entire step block, byte for byte, to a NEW file `.agent/authored/f262-r21.md`.
C0b. Whole-file replace `.agent/last_block.md` with the same bytes (mirror of C0a).
C1. Whole-file replace `.agent/plan.md` with PLAN22 (below) — ordered before the finding registration per planner_reviewer_prompt.md §3 checklist item 23.
C2. Append GATE20 (below) to `.agent/live_review.md`.
C3. Append FINDING R-0795 (below) to `.agent/live_review.md` (same file as C2, separate commit, separate append).
C4. Rewrite `.agent/handoff.md` (handback) per docs/agents/handback_template.md; this is the round's LAST commit. This handback is a SCOPE REPORT, not a normal round handback — see "HANDBACK" section below for its required content.

============================================================
GATE20 — append verbatim as a new line at the end of `.agent/live_review.md`. The current file ends with NO trailing newline. C2 must: read the current file, append exactly one `\n` character followed by the GATE20 text below (with no trailing newline after it either). Do this with Python (`pathlib.Path.write_bytes`), not a shell append.

GATE20 text (copy exactly, it is a single line with zero internal newlines, 2778 bytes UTF-8):
Gate: R20 — the F262 R20 entry. R20 SHIPPED T003 BATCH 8 (FINAL), restructuring `loop.list` (`apps/cli/commands/loop_cmd.py::_cmd_loop_list`) per DECISION F262 D3: the function now builds ONE `(spec, last_run_created_at, last_run_state)` row list UNCONDITIONALLY (the `last_run_for_loop` lookup moved out of the prior `json_output`-only branch), runs `apply_list_options` exactly once with `default_sort_field=None` (config-declaration order stays default, D2/D3 precedent), and renders BOTH the text and json branches from that same post-options row list — the text branch now reads its row's own precomputed `last_run_created_at`/`last_run_state` instead of a second, independent `_last_run_label` lookup, removing the prior duplicate. `_last_run_label` itself is confirmed still present and unmodified, intentionally left unused per constraint 5. AND THE REVIEWER RE-RAN EVERY GATE ITSELF, in a fresh session (session 7), independently: G1 `python3 -c "import py_compile; ..."` printed `OK` for both touched files, reproduced. G2 `python3 -m pytest tests/cli/test_loop_cmd.py -q` read `18 passed`, reproduced exactly. G3 the combined five-suite canary (`tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py`) read `646 passed`, matching 515+52+21+16+42 exactly, unmoved. G4 `sha256sum .agent/authored/f262-r20.md .agent/last_block.md` printed one identical digest for both, `1ebf71f1caaa3a8bed8c976e1840bfcf8254fadb490ecb777fd19d2d5b463855`, reproduced. G5 THE LEDGER APPEND HELD, reproduced by reading the tracked blob at each parent commit directly (`git show <sha>:.agent/live_review.md | wc -c`): `575f1bc0` (pre-C1) read 2470338 bytes, `d659587c` (post-C1) read 2473689 bytes, matching the block's own stated arithmetic (2470338 + 1 + 3350) exactly. G6 `.agent/plan.md` at HEAD `4238fcd0` measured 2189 bytes byte-for-byte, matching PLAN21 exactly. G7 `git status --porcelain` read empty at this review's own start and remains empty. G8 `git ls-files .remedy-wt` read empty. THE DIFF WAS READ, NOT ONLY GATED: `git show 7e4cba95` for both `apps/cli/commands/loop_cmd.py` and `tests/cli/test_loop_cmd.py` was read in full and matches PAIR L1, PAIR L2 and TEST T1 exactly, byte for byte against the R20 block; numstat (`61 25` / `31 0`) matches the handback's own Commits table exactly; no other function in `loop_cmd.py` was touched. The round's full change set (six paths: `.agent/authored/f262-r20.md`, `.agent/last_block.md`, `.agent/live_review.md`, `apps/cli/commands/loop_cmd.py`, `tests/cli/test_loop_cmd.py`, `.agent/plan.md`, plus the handback commit's `.agent/handoff.md`) matches constraint 3 exactly, no scope drift. THE VERDICT IS PASS.

Base file size immediately before C2 must read 2473689 (confirm with a fresh Python byte read before writing). Post-C2 size must read exactly 2476468 (2473689 + 1 + 2778). Verify both numbers yourself and report them.
============================================================
FINDING R-0795 — append verbatim to `.agent/live_review.md`, immediately after C2's GATE20 append. The convention for a NEW finding (distinct from a Gate entry) is a blank line before it: append exactly `\n\n` followed by the text below (with no trailing newline after it either). Do this with Python (`pathlib.Path.write_bytes`), not a shell append.

FINDING R-0795 text (copy exactly, it is a single paragraph with zero internal newlines, 3228 bytes UTF-8):
- R-0795 — Medium, `config.list`/`worker.list`/`execution.list` ACCEPT ALL FOUR T003 FLAGS BUT SILENTLY IGNORE THEM, VIOLATING T2_F262.md's OWN ACCEPTANCE BULLET, AND NO TEST ANYWHERE CATCHES IT. Raised by the reviewer at the start of session 7 (F262 R21), by reading the shipped state fresh rather than recalling `.agent/plan.md`'s own prose. First measured: `apps/cli/command_catalog.py::_with_list_options` (F262 T001) attaches `--sort`/`--desc`/`--since`/`--until`/`--limit` to EVERY catalog entry `_is_list_command` matches — any subcommand named `list` or ending `-list` — mechanically, with no hand-written exclusion list, so `config.list`/`worker.list`/`execution.list` DO parse all four flags at the argparse layer exactly like every other list command; `.agent/plan.md`'s repeated "stay excused per Risks" (present in every PLAN14 through PLAN21, i.e. every round from F262 R13 through R20, first appearing at commit `60d8c312`) is therefore imprecise about WHAT is excused. MEASURED what actually happens: `apps/cli/commands/worker.py`'s `"worker.list"` dispatch lambda is `lambda args: _cmd_workers(json_output=args.json)` — `args.sort`/`.since`/`.until`/`.limit`/`.desc` are parsed by argparse and then discarded before `_cmd_workers` is ever called; `apps/cli/commands/config_cmd.py::_cmd_config_list` reads only `getattr(args, "json", False)`; `apps/cli/commands/managed_builder_execution_cmd.py::_cmd_list` reads only `ns.job_id`. REPRODUCED DIRECTLY: calling `COMMAND_HANDLERS["worker.list"]` with `argparse.Namespace(json=True, sort="bogus-field-xyz", since=None, until=None, limit=None, desc=False)` prints the full, unfiltered, unsorted provider list and raises NOTHING — no `SystemExit`, no error — where T2_F262.md's Acceptance section's third bullet requires "`--sort` with an unknown field exits non-zero and names the valid fields" for every list command. This is a directly measured Acceptance-criterion failure for these three commands, not a hypothetical one, and no existing test would catch it: `tests/orchestration/test_list_options.py` only exercises the shared helper in isolation and no catalog-deriving test exists at all (T001's own Acceptance bullet, "the catalog test proves no list command is missing a flag", was never built either — the same gap, one level up: nothing enumerates the list-command set and asserts each one's HANDLER, not just its argparse signature, actually uses the flags it accepts). FIX: before F262 closure, either (a) wire the three handlers to `apply_list_options` (a real T003 scope addition — `worker.list`/`config.list`/`execution.list` all already receive the parsed values, they only need to be threaded through and the results filtered/sorted), or (b) register a DECISION narrowing T003's Acceptance to explicitly exempt these three by name and reason, and correct `.agent/plan.md`'s Risks section to state the exemption precisely (accepted-but-ignored, not "excused" from parsing) rather than the current imprecise blanket phrase. Searched before minting per §3 checklist item 30: grepped `.agent/live_review.md` for "catalog test", "config.list", "worker.list", "execution.list", "_with_list_options" — no open finding covers either gap.

Base file size immediately before C3 (i.e. immediately after C2) must read 2476468. Post-C3 size must read exactly 2479698 (2476468 + 2 + 3228). Verify both numbers yourself and report them.
============================================================
PLAN22 — whole-file replace of `.agent/plan.md`. Byte length must be exactly 2350 (UTF-8, no trailing newline), confirm with a binary-mode byte comparison after writing. Line count must be 49 (under the AGENTS.md 50-line cap).

PLAN22 text (copy exactly):
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 21, session 7 - SCOPE REPORT per amend0827-process-diet rule 6:
this feature has now run 7 sessions (the operator's soft limit), so
this round books GATE20 (round 20 PASSED), registers R-0795 (T001's
catalog test was never built; `config.list`/`worker.list`/
`execution.list` all PARSE the T003 flags via `_with_list_options`'s
mechanical catalog attachment but their handlers silently discard
them - measured directly, `--sort bogus` raises nothing), and reports
scope instead of opening an eighth build round.

## Next Steps (operator decision needed, per amend0827 rule 6)

- Option A: authorize an 8th session to (1) build the T001 catalog
  test deriving the list-command set from the CLI catalog, (2) wire
  `config.list`/`worker.list`/`execution.list`'s handlers to
  `apply_list_options` (they already receive the parsed flags), (3)
  build the Acceptance ten-second-demo smoke test, then close F262.
- Option B: register a DECISION narrowing T003's Acceptance to
  explicitly exempt these three commands (naming the real reason, if
  one exists, the way D2/D3 did for queue.list/loop.list), correct
  plan.md's Risks section to state the exemption precisely, and close
  F262 without the catalog test or the smoke test.
- change.list's event-log CREATED date stays open, UNRELATED to D1 -
  see DECISION F262 D1's Alternative section.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix.
- R-0795 (this round): config.list/worker.list/execution.list PARSE
  all four T003 flags (attached mechanically, like every list command)
  but their handlers ignore them - `--sort bogus` against any of the
  three raises nothing, violating Acceptance's own "exits non-zero"
  bullet. Not yet resolved.

============================================================
CONSTRAINTS:
1. No file besides these may be written: `.agent/authored/f262-r21.md`, `.agent/last_block.md`, `.agent/plan.md`, `.agent/live_review.md`, `.agent/handoff.md`. No `apps/`, `packages/`, `tests/` or `docs/` path is touched this round — that is the point of a scope-report round.
2. Commit order is exactly C0a, C0b, C1, C2, C3, C4, each its own commit.
3. Run `git status --porcelain` after every commit; it must be empty before proceeding.
4. `.agent/STOP` must be absent before C0a and re-checked before C4. If it appears, stop immediately, finish only a half-written commit, and write the handoff reporting the STOP instead of continuing.
5. Capture REAL exit codes / byte counts for every command — do not report "green" as a bare word.
6. Known sandbox quirks in this repo (from prior rounds): `VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`, and `cp` are denied outright — use `python3 -c "import shutil; shutil.copyfile(a,b)"` if ever needed. Never use a sandbox-override flag to route around a denial.
7. Do not attempt `remedy plan status` / `remedy plan next` — the `remedy` CLI is denied session-wide in this repo's sandbox (confirmed this session); do not retry it.

DONE WHEN (run every one of these EXACTLY as written and record the REAL, complete output of each in your handback — quote actual output, do not summarize as "passed"):
G1. `sha256sum .agent/authored/f262-r21.md .agent/last_block.md` → must print one identical digest for both files. Report both digests.
G2. Byte-read `.agent/live_review.md` immediately before C2 and immediately after C2 (Python, binary mode) → before must be 2473689, after must be 2476468. Report both numbers.
G3. Byte-read `.agent/live_review.md` immediately before C3 and immediately after C3 (Python, binary mode) → before must be 2476468, after must be 2479698. Report both numbers.
G4. Byte-read `.agent/plan.md` immediately after C1, binary mode → must be exactly 2350 bytes, byte-for-byte equal to the PLAN22 text above, and 49 lines.
G5. `git status --porcelain` → empty, checked before C0a and immediately before C4. Report both checks.
G6. `git ls-files .remedy-wt` → empty. Report the output (should be nothing).

HANDBACK: write a full completion report and rewrite `.agent/handoff.md` per docs/agents/handback_template.md and AGENTS.md's "### handoff.md" section. This handback IS A SCOPE REPORT, not a normal round handback, per operator amendment amend0827-process-diet rule 6 (docs/agents/planner_reviewer_prompt.md §3 and docs/agents/self_drive_protocol.md "Ending a session") — this feature has run 7 sessions, its stated soft limit. Include, beyond the normal mandated sections (state block, changed-files table, item-status table, real verification results, next expected action):
1. The literal unmissable line: SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE
2. A SCOPE REPORT: what is DONE (T001 shared surface, T002 dates on every row, T003 sort/filter/limit for job.list/patch.list/queue.list/memory.list/loop.list — five commands fully wired, two of them — queue.list/loop.list — with a deliberate, DECISION-documented default-order opt-out) and what is MISSING (the T001 catalog test that proves no list command lacks a flag; config.list/worker.list/execution.list parse the T003 flags but their handlers silently discard them, per R-0795; the Acceptance ten-second-demo integration smoke test; change.list's CREATED date, tracked separately as out of scope per D1).
3. The two-option proposal from PLAN22's Next Steps (Option A: authorize an 8th session to finish the gaps; Option B: register a DECISION narrowing Acceptance and close without them) — stated as a DOCUMENTED PROPOSAL TO THE OPERATOR ONLY, never executed on this session's own authority.
4. State explicitly that NO code, test or docs path was touched this round (only `.agent/**`), and why: this round's entire obligation was booking GATE20, registering R-0795, and reporting scope, per the soft-limit rule.
After the handoff commit (C4), run `git push -u origin feature/f262-list-commands-v2` and report the push result. Do NOT create a PR. Do NOT merge anything. Do NOT touch `main`.
──────────────────────────────────────────────────────────────
