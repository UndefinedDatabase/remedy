── STEP scope-correction (no code) — F262 List commands v2 ────────────────
Goal: Book round 22's PASS verdict, convert R-0795 to Done, register FINDING R-0796 (T003's scope was undercounted — 13 of 28 list-shaped commands were never wired, not 3), register DECISION F262 D4 (scope the closure Acceptance to 24 of 28), point T2_F262.md at that DECISION, and hand the operator a corrected-scope proposal in `.agent/plan.md`.

Bundle:
C0a. Save this entire step block, byte for byte, to a NEW file `.agent/authored/f262-r23.md`.
C0b. Whole-file replace `.agent/last_block.md` with the same bytes (mirror of C0a).
C1. Append GATE22 (below) to `.agent/live_review.md`.
C2. Append the Done: R-0795 text (below) to `.agent/live_review.md`.
C3. Append FINDING R-0796 (below) to `.agent/live_review.md`.
C4. Append DECISION F262 D4 (below) to `.agent/decisions.md`.
C5. Append the T2_F262.md amendment (below) to `docs/roadmap/features/T2_F262.md`.
C6. Whole-file replace `.agent/plan.md` with PLAN24 (below).
C7. Rewrite `.agent/handoff.md` (handback) per docs/agents/handback_template.md; this is the round's LAST commit.

============================================================
GATE22 — append verbatim to `.agent/live_review.md`. The file currently ends with the LANDED R-0795 line (a prose entry, no trailing newline). Append exactly TWO `\n` characters followed by the GATE22 text below (no trailing newline after it). Python `pathlib.Path.write_bytes`.

GATE22 text (single line, zero internal newlines, 3174 bytes UTF-8):
Gate: R22 — the F262 R22 entry. R22 SHIPPED R-0795's FIX (option a): `worker.list`, `config.list` and `execution.list` all wired to `apply_list_options` — `worker.list`/`config.list` with `default_sort_field=None` (no date field on either row shape, matching D2/D3's precedent for a command with no natural recency), `execution.list` with `default_sort_field="started_at"` (a real ISO date on every row) — plus six new regression tests (two per command) proving `--limit` and an unknown `--sort` field now behave identically to every other list command, and no mutation red-proof was ordered this round by the block's own constraint 9 (deferred) — AND THE REVIEWER RE-RAN EVERY GATE ITSELF, in a fresh session (session 8), independently. TRANSPORT HELD: `sha256sum .agent/authored/f262-r22.md .agent/last_block.md` printed one identical digest, `be063df027d5daf0fae01a1b422d5aee83829025e985ca98342f833c4f9f4697`, for both files, reproduced exactly. THE DIFF WAS READ, NOT ONLY GATED: `git diff c129b4f2..2e7e68b6` for `apps/cli/commands/worker.py`, `apps/cli/commands/config_cmd.py`, `apps/cli/commands/managed_builder_execution_cmd.py`, `tests/cli/test_config_cmd.py`, `tests/cli/test_managed_builder_execution_cli.py` and `tests/cli/test_worker_facade_cmd.py` shows exactly PAIR W1/W2, PAIR CFG1, PAIR EXE1, and TEST T1/T2/T3's six new test functions, every other line in all six files untouched, confirmed by reading the full diff. `python3 -c "import py_compile; ..."` printed OK for all six touched files, run independently by the reviewer. THE TESTS MOVED EXACTLY AS THE HANDBACK CLAIMED, reproduced independently: `python3 -m pytest tests/cli/test_worker_facade_cmd.py tests/cli/test_config_cmd.py tests/cli/test_managed_builder_execution_cli.py -q` read `98 passed` (92 pre-existing plus 6 new). THE STATE READERS AND THE CANARY WERE UNMOVED, reproduced by the reviewer as ONE combined invocation: `tests/ui_server/ tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py` read `646 passed`, matching 515+52+21+16+42 exactly. THE GATE21 AND LANDED LEDGER APPENDS WERE RE-VERIFIED BYTE-EXACT: base 2479698 plus two newlines plus GATE21 (2545 bytes) equals 2482245 (after C1); 2482245 plus two newlines plus the LANDED line (293 bytes) equals 2482540 (after C6) — both exact, matching the file's own on-disk size (2482540 bytes, confirmed by a fresh byte read). THE PLAN HELD: `.agent/plan.md` measured 1959 bytes at HEAD `2e7e68b6`, byte-for-byte equal to PLAN23. HYGIENE HELD: `git status --porcelain` empty at HEAD `2e7e68b6`, `git ls-files .remedy-wt` empty, `.agent/STOP` absent. ONE DEVIATION VERIFIED AS HARMLESS: the worker's `python3 -c` heredoc for PLAN23 was refused by the sandbox's bash guard (a `#` heading inside the heredoc looked like a hidden-argument attempt), so the worker used the Write tool instead and then trimmed one stray trailing-newline byte with a follow-up `write_bytes` call to reach the exact 1959-byte target — the final on-disk bytes match PLAN23 exactly regardless of the write route, confirmed above. THE VERDICT IS PASS.

Base size immediately before C1 must read 2482540. Post-C1 size must read exactly 2485716 (2482540 + 2 + 3174). Verify both numbers yourself.
============================================================
Done: R-0795 — append verbatim to `.agent/live_review.md` immediately after C1 (append exactly TWO `\n` then the text below, no trailing newline after it).

Done: R-0795 text (single line, zero internal newlines, 1269 bytes UTF-8):
Done: R-0795 — RESOLVED at `175ddfa1`/`36088098`/`4d51ea23` (F262 R22, C2/C3/C4), verified by the reviewer independently above (GATE22). `worker.list`, `config.list` and `execution.list` now all call `apply_list_options`, and `--sort bogus` against any of the three exits non-zero naming the valid fields — reproduced directly: `python3 -m pytest tests/cli/test_worker_facade_cmd.py::TestWorkerListOptions::test_unknown_sort_field_exits_nonzero tests/cli/test_config_cmd.py::TestConfigCli::test_config_list_unknown_sort_field_exits_nonzero tests/cli/test_managed_builder_execution_cli.py::TestManagedBuilderExecutionCLI::test_execution_list_unknown_sort_field_exits_nonzero -q` reads 3 passed. The mutation red-proof this finding's own FIX clause did not require (only options (a) or (b) were named) was not additionally ordered; the behavioural proof above is the resolution condition, matching FIX option (a) exactly. T001's own separate, never-built catalog-level enumeration gap — proving no list command's HANDLER, not just its argparse signature, ignores its flags — is NOT resolved by this and stays open, tracked as its own item in `.agent/plan.md`, not under this id (per §3 checklist item 30, searched and confirmed no separate id exists for it yet).

Base size immediately before C2 must read 2485716. Post-C2 size must read exactly 2486987 (2485716 + 2 + 1269). Verify both numbers yourself.
============================================================
FINDING R-0796 — append verbatim to `.agent/live_review.md` immediately after C2 (append exactly TWO `\n` then the text below, no trailing newline after it).

FINDING R-0796 text (single line, zero internal newlines, 4126 bytes UTF-8):
- R-0796 — Medium, T003's OWN SCOPE WAS UNDERCOUNTED: 13 OF THE CATALOG'S 28 LIST-SHAPED COMMANDS WERE NEVER WIRED TO `apply_list_options` AT ALL, AND `.agent/plan.md` HAS CLAIMED "T003 is now DONE for every list command in scope" SINCE PLAN21 (round 20) WITHOUT THAT SCOPE EVER BEING MEASURED AGAINST THE FULL CATALOG. Raised by the reviewer at the start of session 8's round 23, by mechanically listing every `_is_list_command`-matched `CommandEntry` in `apps/cli/command_catalog.py::CATALOG` (28 total) against every file `grep -rl "apply_list_options(" apps/cli/commands/` names (15 files, one per wired command: job.list, queue.list, loop.list, project.list, patch.list, worker.list, tournament.list, memory.list, blocker.list, decision.list, external-builder.submission-list, review.list, propose.list, config.list, execution.list — the last three landed this session in F262 R22). The 13 UNWIRED command ids, characterized by whether their rows carry a genuine date field: test.list (`apps/cli/commands/real_test_execution_cmd.py::_cmd_test_list`, has `created_at`), repair.item-list (`repair_loop_v2_cmd.py::_cmd_item_list`, `RepairWorkItem.created_at`, already pre-sorted by it), builder.session-list (`main_builder_adapter_cmd.py::_cmd_session_list`, `BuilderSessionRecord.started_at`/`ended_at`), execution.approval-list (`managed_builder_execution_cmd.py::_cmd_approval_list`, `ExecutionApproval.approved_at`), mission.list (`mission_cmd.py::_cmd_mission_list`, `Mission.created_at`, `list_missions_safe` already sorts `reverse=True` by it), change.list (`change.py::_cmd_change_list`, recency lives in nested `approval`/`apply`/`proof`/`test`/`revert` dicts, no flat field), event.list (`event.py::_cmd_event_list`, has `timestamp`, already closest to wired per the catalog's own `_with_list_options` comment naming it the one pre-existing exception), external-builder.package-list (`external_builder_cmd.py::_cmd_external_builder_package_list`, has `created_at` in JSON only) and self-repair.proposal-list (`self_repair_cmd.py::_cmd_proposal_list`, has `created_at`/`updated_at`, already printed) — NINE commands with a genuine date field, squarely the class T003's Design section targets. THREE MORE have NO date field at all and no "newest" concept: builder.adapter-list (`main_builder_adapter_cmd.py::_cmd_adapter_list`, `BuilderAdapterSpec` carries no timestamp), execution.template-list (`managed_builder_execution_cmd.py::_cmd_template_list`, `CommandTemplate` carries no timestamp) and worker.registry-list (`route_policy_cmd.py::_cmd_worker_registry_list`, `WorkerSpec` carries no timestamp) — static configuration registries, not temporal history, the same class DECISION F262 D2/D3 already recognized for a command with its own non-arbitrary order, except here there is no order to preserve at all because there is nothing to order BY. ONE is a borderline hybrid: approval.policy-list (`worker_facade_cmd.py::_cmd_approval_policy_list`, `ExecutionApprovalPolicy.created_at`/`updated_at`, already printed) — has real dates but reads as a small named-policy catalog a user browses by policy id or enabled state, not by recency. FIX: DECISION F262 D4 (this round) scopes T003's closure Acceptance to the 9 genuine temporal-history gaps plus the 15 already-wired commands (24 of 28), explicitly excluding the 3 static registries and the 1 hybrid by name and reason; the 9 remaining genuine gaps do not fit the round budget left in this feature (3 of the 25-round soft cap remain) and are the subject of this round's scope proposal in `.agent/plan.md`. Searched before minting per §3 checklist item 30: grepped `.agent/live_review.md` for "test.list", "repair.item-list", "builder.adapter-list", "builder.session-list", "execution.template-list", "execution.approval-list", "worker.registry-list", "mission.list", "approval.policy-list", "change.list", "event.list", "external-builder.package-list" and "self-repair.proposal-list" as fixed strings — the only hit was test.list inside GATE12's own T002 text (round 12's date-only work, unrelated to T003 wiring), no open finding covers this gap.

Base size immediately before C3 must read 2486987. Post-C3 size must read exactly 2491115 (2486987 + 2 + 4126). Verify both numbers yourself.
============================================================
DECISION F262 D4 — append verbatim to `.agent/decisions.md`. The file currently ends with D3's text (a "## DECISION" headed entry, no trailing newline) — consecutive `## DECISION` entries in this file use a SINGLE `\n` separator (confirmed directly: D2-to-D3's boundary uses exactly 1 newline), unlike the blank-line separator prose findings use. C4 must: append exactly ONE `\n` character followed by the text below (no trailing newline after it). Python `pathlib.Path.write_bytes`.

DECISION D4 text (copy exactly, it has internal blank lines between its own paragraphs — that is normal, matching D1/D2/D3's own internal shape; the WHOLE text below, 3213 bytes UTF-8, 7 lines, is what gets appended as one unit):
## DECISION F262 D4 (2026-09-05, F262 R23) — T003's closure Acceptance is scoped to 24 of the catalog's 28 list-shaped commands, excluding 3 static registries and 1 hybrid config-catalog by name; the 9 remaining genuine temporal-history gaps are deferred, not silently dropped

CHOSEN. T003's "every list command" is read as every list-shaped command whose rows carry a genuine, meaningful date (T2_F262.md's own Design section: "Newest-first is the DEFAULT... A list whose store cannot order says so"). `builder.adapter-list`, `execution.template-list` and `worker.registry-list` carry no date field on their row shape at all - `BuilderAdapterSpec`, `CommandTemplate` and `WorkerSpec` are static configuration registries with no created/updated concept to sort by, matching the class DECISION F262 D2/D3 already carved out for a command with its own non-arbitrary order, one step further: there D2/D3 had an order to preserve, here there is no order to preserve because there is nothing to order BY. `approval.policy-list` has real `created_at`/`updated_at` fields but is read as a small named-policy catalog browsed by policy id or enabled state rather than by recency, and is excluded on the same reasoning. These four are OUT of T003's Acceptance permanently, not deferred - a later feature adding genuine per-policy history would revisit `approval.policy-list` specifically, not reopen this DECISION. The remaining 9 unwired commands with genuine dates (test.list, repair.item-list, builder.session-list, execution.approval-list, mission.list, change.list, event.list, external-builder.package-list, self-repair.proposal-list - FINDING R-0796) stay IN T003's scope and are NOT excluded by this DECISION; they are DEFERRED, tracked in `.agent/plan.md`'s Next Steps as the actual remaining work, because F262 has 3 rounds left of its 25-round soft cap and wiring nine more commands with tests each does not fit that budget at the pace this feature has run (roughly 1-3 commands per round across R13-R22).

ALTERNATIVE CONSIDERED AND REJECTED. Exclude all 13 unwired commands from Acceptance to make T003 "done" immediately. Rejected: nine of them have exactly the shape T003 exists to fix (a real date, no sort/filter/limit), and declaring them out of scope would be a scope-narrowing dressed as a DECISION rather than a genuine one - the same failure mode R-0795 itself measured when `.agent/plan.md` said "excused" too broadly for three commands that turned out to parse the flags and silently ignore them.

CONSEQUENCE. F262 cannot close this session under either PLAN23's Option A or Option B from round 21 - both assumed only 3 commands remained. The corrected count is 9 genuine wirings plus the T001 catalog-level handler test plus the Acceptance smoke test, none of which fit the 3 rounds of budget left. `.agent/plan.md`'s Next Steps (this round) proposes the operator choose between authorizing sessions beyond the 7-session/25-round soft caps, or splitting the 9 remaining wirings into a follow-up feature and closing F262 now on this DECISION's narrowed-but-honest Acceptance (24 of 28 commands, both static exclusions and the temporal 9 explicitly named as follow-up work, not silently dropped).

Base size immediately before C4 must read 806068. Post-C4 size must read exactly 809282 (806068 + 1 + 3213). Verify both numbers yourself.
============================================================
T2_F262.md amendment — append verbatim to `docs/roadmap/features/T2_F262.md`. The file currently ends with "...T003 depends on both.\n" (one trailing newline, no blank line before it). Append the text below EXACTLY as given (it already starts with its own leading blank-line newline and ends with a single trailing newline, matching this file's own convention) — i.e. just concatenate the bytes below onto the end of the current file content.

Amendment text (copy exactly, 728 bytes UTF-8, 12 internal newlines):

## Amendment (DECISION F262 D4, 2026-09-05)
"Every list command" (Goal) and the `--sort` Acceptance bullet are scoped
to list-shaped commands whose rows carry a genuine date: 24 of the
catalog's 28. `builder.adapter-list`, `execution.template-list`,
`worker.registry-list` (no date field on their row shape) and
`approval.policy-list` (has dates, browsed by name/state, not recency) are
OUT of Acceptance permanently. The other 9 unwired commands with genuine
dates (test.list, repair.item-list, builder.session-list,
execution.approval-list, mission.list, change.list, event.list,
external-builder.package-list, self-repair.proposal-list) stay IN scope,
deferred per `.agent/decisions.md` DECISION F262 D4 and FINDING R-0796.

Base size immediately before C5 must read 3504. Post-C5 size must read exactly 4232 (3504 + 728). Verify both numbers yourself (this triggers the docs-round gate, G6 below, since the changed path is under docs/roadmap/**).
============================================================
PLAN24 — whole-file replace of `.agent/plan.md`. Byte length must be exactly 2248 (UTF-8), confirm with a binary-mode byte comparison after writing.

PLAN24 text (copy exactly):
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md, scoped by DECISION F262 D4).

## Current Step

Round 23, session 8 - SCOPE CORRECTION, no code this round: booked
GATE22 (round 22 PASSED), converted R-0795 to Done. Registered
FINDING R-0796 - 13 of 28 list-shaped catalog commands were never
wired at all, not just the 3 R-0795 named. Registered DECISION F262
D4 scoping Acceptance to 24 of 28 commands (3 static registries + 1
hybrid catalog excluded by name); the other 9 have genuine dates and
stay IN scope, deferred. T2_F262.md amended with a pointer to D4.

## Next Steps (round-budget mismatch - a DECISION-routed proposal per
amend0827 rule 6's mechanism, not a question)

- Option A: authorize sessions beyond the 7-session/25-round soft
  caps (already session 8, round 23) to wire the 9 remaining commands
  (test.list, repair.item-list, builder.session-list,
  execution.approval-list, mission.list, change.list, event.list,
  external-builder.package-list, self-repair.proposal-list) plus the
  T001 catalog-driven handler test plus the Acceptance smoke test.
- Option B: split the 9 remaining into a NEW follow-up feature
  (STATUS.md line), build the T001/Acceptance tests scoped to the 24
  D4-covered commands only, and close F262 within the 3 rounds left.
- change.list's event-log CREATED date (a separate, older gap) stays
  open either way - see DECISION F262 D1's Alternative section.

## Risks

- Stores with no timestamp concept render "unknown" permanently - now
  formalized as D4's static-registry exclusion, not an informal note.
- R-0796's 9 gaps are real product debt regardless of option chosen -
  Option B moves them, it does not remove them.
- Round 23 has NO code/test path in its change set (only `.agent/**`
  plus T2_F262.md's pointer) - a finding-routed-to-planning round per
  §4 item 7, matching the DECISION F112 D5 precedent shape.

============================================================
CONSTRAINTS:
1. This round writes NO code and NO test file — only `.agent/authored/f262-r23.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/decisions.md`, `docs/roadmap/features/T2_F262.md`, `.agent/plan.md`, `.agent/handoff.md`. Do not touch anything else.
2. Commit order is exactly C0a, C0b, C1, C2, C3, C4, C5, C6, C7, each its own commit.
3. Run `git status --porcelain` after every commit; it must be empty before proceeding. Capture REAL exit codes for every command — do not report "green" as a bare word.
4. `.agent/STOP` must be absent before C0a and re-checked before C7. If it appears, stop immediately, finish only a half-written commit, and write the handoff reporting the STOP instead of continuing.
5. Do NOT wire any of the 9 or 13 commands named above this round — that is explicitly out of scope, deferred per the DECISION.
6. Known sandbox quirks: `VAR=x cmd`, `export VAR=x; cmd`, `cp` are denied — use a `python3 -c "import shutil; shutil.copyfile(a,b)"` one-liner if ever needed. The `remedy` CLI is denied session-wide — use `python3 -m apps.cli.grouped`/`python3 -m pytest`. If a `python3 -c` heredoc is refused by the bash guard, use the Write tool and verify/trim bytes with a follow-up read/write, declaring the substitution.

DONE WHEN (run every one of these EXACTLY as written and record the REAL, complete output of each in your handback):
G1. `sha256sum .agent/authored/f262-r23.md .agent/last_block.md` → must print one identical digest for both files.
G2. Byte-read `.agent/live_review.md` before/after C1 (2482540/2485716), before/after C2 (2485716/2486987), before/after C3 (2486987/2491115). Python, binary mode. Report all six numbers.
G3. Byte-read `.agent/decisions.md` before/after C4 (806068/809282). Report both numbers.
G4. Byte-read `docs/roadmap/features/T2_F262.md` before/after C5 (3504/4232). Report both numbers.
G5. Byte-read `.agent/plan.md` after C6, binary mode → must be exactly 2248 bytes, byte-for-byte equal to PLAN24 above.
G6. `python3 -m pytest tests/docs/ -q` → report the real result (docs-round gate, since C5 touches `docs/roadmap/**`).
G7. `python3 -m pytest tests/cli/test_golden_path.py -q` → report the real result (mandatory canary, every handback).
G8. `git status --porcelain` → empty, checked before C0a and immediately before C7. `git ls-files .remedy-wt` → empty. `.agent/STOP` → absent, both checks.

HANDBACK: write a full completion report and rewrite `.agent/handoff.md` per docs/agents/handback_template.md and AGENTS.md — changed-files table for every commit, item-status table covering C0a..C7 and G1..G8, real verification results for every gate, SESSION NUMBER 8 of feature F262 round 23, and the next expected action: **an OPERATOR DECISION between Option A and Option B in `.agent/plan.md`'s Next Steps — this is a genuine round-budget/scope mismatch discovered this round (FINDING R-0796), not a routine next-step, and no further F262 round should be delegated without it.** State clearly in the handback's Session section that this round found NEW scope (9 more commands, not 3) that the round budget cannot absorb, and that this is reported, not hidden. After the handoff commit (C7), run `git push -u origin feature/f262-list-commands-v2` and report the push result. Do NOT create a PR. Do NOT merge anything. Do NOT touch `main`.
──────────────────────────────────────────────────────────────