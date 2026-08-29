# F033 — Hunk-level diff approval · ROUND 14 · THE CLI COMMAND AND ITS HANDLER

SESSION 4 of feature F033. Round 14, rounds so far 14.

You are the WORKER for this round. AGENTS.md is the highest authority and binds
you in full. Do not review your own work and write no verdict on it.

## Conventions (read once, they bind every slice below)

1. A SLICE is the bytes BETWEEN its `<<<SLICE <NAME>` and `<<<END <NAME>` lines,
   exclusive. Apply slices BYTE FOR BYTE — never reflow, re-wrap or "fix" one. If
   a slice looks wrong, apply it anyway and say so in the deviations.
2. Delimiters are transport only. ANCHOR extraction to the NAMED delimiter at
   line start — `<<<END RECORDF033R14`.
3. Every WHOLE-FILE slice ends with exactly one trailing newline. Every APPEND
   slice is joined to its file as: the base blob, then one newline, then the
   slice, and the result ends in exactly one newline. Take a slice as the bytes
   from the end of its `<<<SLICE` marker line up to and INCLUDING the newline
   that ends its last content line.
4. Extract every slice from the COMMITTED blob you save at C0a, never by retyping.
5. THE PYTHON IS A SPEC, NOT A SLICE. You write the code and the tests from the
   description. Names, signatures and the behaviours the SPEC fixes are binding;
   structure, comment wording and test names are yours. If the SPEC is
   impossible, STOP and say so rather than inventing past it.
6. Guard re-expressions: the shell rejects loops, `$( )`, `${arr[0]}` and `cp` by
   FORM. Copy with `shutil.copyfile`; route measurement through Python under the
   gitignored `.remedy-wt/`, run with `python3 -B`. Python 3.10 forbids a
   backslash inside an f-string expression — hoist regexes to module level.
7. Capture REAL exit codes; piping to `tail` otherwise masks a red.
8. Read a NON-CURRENT revision with `git show <sha>:<path>`. NEVER write a base
   blob over a tracked file.
9. Purge `__pycache__` or use `python3 -B` whenever a mutation must reach a test.
10. Byte OFFSETS and byte SPANS are measured on BYTES, never on a decoded string.
11. IF A GATE AND A SPEC PARAGRAPH DISAGREE, the GATE is load-bearing: satisfy it,
    satisfy the SPEC's INTENT around it, and declare the disagreement.

## Base

BASE is `34d5e4e48418536bfcd21fd9403403b96ea66220`, the round 13 handback commit,
on branch `feature/f033-hunk-approval-v2`. Confirm with `git rev-parse HEAD`
before C0a and STOP if it differs.

## Why this round exists

Round 13 PASSED and C2 books that verdict. The reviewer re-ran every gate from
scripts of its own, and additionally built a DIFFERENTIAL proof the block never
ordered: the old `_resolve_evidence_dir`, reconstructed by `git show` from the
round 13 base, against the shipped `resolve_job_evidence_dir` and against the
delegation, over fifteen cases including the three that raise `AttributeError`
and both precedence cases — no divergence. The move is a move.

C2 ALSO REGISTERS ONE FINDING, R-0743, which the reviewer raised with a mutation
the round 13 block never ordered: swapping the two branches so the CWD-relative
`remedy-job-evidence-<job_id>` directory is consulted BEFORE the index left the
whole file GREEN at 32 passed. Precedence is real and load-bearing — the index
names the exported bundle, the relative directory is the deprecated root-style
fallback — and nothing pins it. YOU FIX IT THIS ROUND, at C5, because this
round's handler is the first caller that can be handed the wrong diff by it.

NOW THE COMMAND. `record_hunk_decision_from_view` takes the viewer's envelope,
`build_diff_view` produces it from a directory, and `resolve_job_evidence_dir`
now answers which directory. Every piece exists; this round wires them to an
operator.

MEASURED AT BASE, so the SPEC rests on readings rather than expectations:

- `apps/cli/grouped.py` line 298 ends its option chain with a catch-all
  `else: parser.add_argument(arg.name, default=arg.default, help=arg.help)`, and
  a repeatable argument is caught EARLIER, at the `elif arg.is_repeatable` branch
  that adds `action="append", default=None` with `dest` the name minus its
  dashes, hyphens turned to underscores. So a NEW option name needs NO parser
  edit, and `apps/cli/grouped.py` is on the do-not-touch list below.
- `apps/cli/grouped.py` dispatches by `command_id` through
  `collect_all_handlers()` and prints `Error: no handler for <id>` when there is
  none. So the catalog entry and the handler land in ONE commit, C4.
- `tests/test_command_catalog.py`'s `TestCatalogLookups.test_get_commands_for_group`
  asserts `len(cmds) == 6` for the `patch` group AND an exact set of six
  subcommands. It is an EQUALITY guard: a seventh entry reddens BOTH assertions
  unless it is widened in the SAME commit. That widening is C4's, and it is the
  R-0697 shape this checklist exists to catch.
- `tests/cli/test_command_catalog.py` pins the `ui` group at 5, not `patch`, and
  no test anywhere counts `CATALOG` as a whole. `tests/test_grouped_cli.py`
  parametrizes over GROUPS and not over commands, so its collection count does
  not move.
- `decide_hunk_approval` already accepts a rejection as a `tuple[str, str]` and
  already mints `missing_reason` for an empty reason. THE HANDLER THEREFORE MINTS
  NO REFUSAL VOCABULARY OF ITS OWN: every refusal the operator sees comes from
  `hunk_approval` or `hunk_decision_record`. One fault, one word for it.

## Bundle (in this order)

- C0a save this block · C0b mirror it
- C1 `.agent/plan.md`
- C2 the round 13 verdict AND the R-0743 registration into `.agent/live_review.md`
- C3 one dated prose slip into `.agent/prose_slips.md`
- C4 the catalog entry, the widened catalog guard and the handler — ONE commit,
  because a catalog entry without its handler answers `Error: no handler`
- C5 the R-0743 precedence pin and the handler's tests
- C6 the handback

You write NO `Done:` paragraph — `Done:` is the reviewer's word. R-0743 is
registered by C2 and FIXED by C5; mark that fix with a single line
`Landed: R-0743 — <one line: what changed, which commit>` appended in C5, and
nothing else. The reviewer replaces it with the authored `Done:` text at the next
gate.

## Change set — these paths and nothing else

    .agent/authored/f033-r14.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    apps/cli/command_catalog.py
    apps/cli/commands/patch.py
    tests/test_command_catalog.py
    tests/orchestration/test_evidence_index.py
    tests/cli/test_patch_cmd.py
    .agent/handoff.md

NEW FILES, named rather than counted: `.agent/authored/f033-r14.md` and
`tests/cli/test_patch_cmd.py`. This round does NOT touch
`packages/orchestration/hunk_decision_record.py`,
`packages/orchestration/hunk_ledger.py`,
`packages/orchestration/hunk_approval.py`,
`packages/orchestration/hunk_apply.py`,
`packages/orchestration/hunk_subset_diff.py`,
`packages/orchestration/diff_view_source.py`,
`packages/orchestration/diff_parser.py`,
`packages/orchestration/ui_server.py`, `apps/cli/grouped.py`,
`tests/ui_server/test_command_channel.py` or `docs/roadmap/STATUS.md`. THE WRITE
DOOR IS PROVABLY UNTOUCHED and G8 measures it. `.agent/context.md` is
deliberately NOT touched. `packages/orchestration/evidence_index.py` is touched
by NO commit of this round — the R-0743 fix is a TEST, because the code's
precedence is already correct and only unpinned.

## SPEC — `apps/cli/command_catalog.py`

An EDIT that ADDS three argument shorthands and ONE catalog entry. Every existing
name, value and entry is untouched.

Beside the existing shorthands, in the same idiom and with the same comment
style:

    _TASK_RUN_OPT     --task-run      valued, not required, not a flag
    _APPROVE_HUNK_OPT --approve-hunk  repeatable
    _REJECT_HUNK_OPT  --reject-hunk   repeatable

`--task-run` names ONE task run whose diff to decide over, and its help says that
omitting it decides over the JOB-level diff. It is deliberately NOT the existing
`_TASK_OPT`: that one promises "planned id (T001) or task-id prefix", and
`build_diff_view` does no prefix resolution at all — it requires exact membership
in the real `task_runs/` listing. Promising a prefix match the code does not
perform is worse than a second option name. Say that in a comment.

`--approve-hunk` and `--reject-hunk` are `is_repeatable=True`. `--reject-hunk`'s
help states the shape `<hunk-id>=<reason>` and shows it.

Then the entry, placed after `patch.revert` inside the `patch` group:

    command_id      "patch.approve-hunks"
    group_id        "patch"
    subcommand      "approve-hunks"
    description     one sentence, ending in a period
    action_class    "approval_gate"        — its neighbours patch.approve and patch.reject
    args            (_JOB_ID, _TASK_RUN_OPT, _APPROVE_HUNK_OPT, _REJECT_HUNK_OPT, _JSON_OPT)
    supports_json   True
    may_mutate_repo False                  — DECISION F033 D4: it records, it never applies
    related         ("patch.approve", "patch.apply")

`may_mutate_repo` and `requires_permission` are LEFT AT THEIR DEFAULTS of False
and that is load-bearing, not laziness: this command writes `job.metadata` and
touches no repository, and claiming otherwise would misdescribe DECISION F033 D4
in the one table the UI reads capability from.

THE DESCRIPTION AND EVERY ARG HELP MUST SURVIVE `TestCatalogSensitivity` in
`tests/test_command_catalog.py`, which scans both against a list of forbidden
terms and credential prefixes. READ that class and check your strings against
the list it actually holds rather than against a copy of it here — a copy would
be free to drift, and the terms are exactly the kind of string this repository
does not restate. Plain words about approving and rejecting hunks are fine.

## SPEC — `tests/test_command_catalog.py`

An EDIT of ONE test, in the SAME commit as the entry above.
`TestCatalogLookups.test_get_commands_for_group` becomes `len(cmds) == 7` and its
subcommand set gains `"approve-hunks"`. Change NOTHING else in this file: the
guard is being widened by exactly the entry that widens it, which is why the two
share a commit.

## SPEC — `apps/cli/commands/patch.py`

An EDIT that ADDS one private handler and ONE `COMMAND_HANDLERS` entry. Every
existing handler is untouched.

    "patch.approve-hunks": lambda args: _cmd_approve_hunks(
        args.job_id,
        task_run=getattr(args, "task_run", None),
        approve=getattr(args, "approve_hunk", None),
        reject=getattr(args, "reject_hunk", None),
        json_output=getattr(args, "json", False),
    )

`getattr` with a default is the file's own idiom for optional arguments and it is
what keeps the handler callable from a hand-built `Namespace` in a test.

`_cmd_approve_hunks` does exactly this, in this order:

1. `resolve_job_id`, then `load_job` inside `try/except JobNotFoundError`, which
   prints `Error: {exc}` to stderr and exits 1 — byte-for-byte the idiom the five
   handlers above it already use.
2. Parse the rejections. Each `--reject-hunk` value splits on its FIRST `=` into
   an id and a reason, and both halves are kept VERBATIM including surrounding
   whitespace, because `HunkRejection` documents that T003 quotes the reason into
   the next repair prompt and this is not the layer that reformats an operator's
   words. A value with NO `=` yields that value as the id and an EMPTY reason,
   and is passed on unchanged — `decide_hunk_approval` answers `missing_reason`
   for it with a message written for exactly that case, and a second refusal
   vocabulary here would give one fault two names. State that in a comment; it is
   the whole reason this step does not validate.
3. Resolve the evidence directory with
   `evidence_index.resolve_job_evidence_dir(job_id_str)` and build the envelope
   with `diff_view_source.build_diff_view(evidence_dir, task_id=task_run)`.
   Pass `task_run` through UNCHANGED, including None, because None is exactly
   what selects the job-level scope.
4. Call `record_hunk_decision_from_view` with `attempt_view` the envelope,
   `approved` the `--approve-hunk` list or an empty list, `rejected` the parsed
   pairs, `now=datetime.now(timezone.utc)`, and the two key halves derived from
   the ENVELOPE and never asked of the operator:
   `task_id` is `view["task_id"]` when it is not None and `DIFF_SCOPE_JOB`
   otherwise, and `attempt` is `view["source"]`. WHY from the envelope: the
   operator has already named the only axis that exists at this door — WHICH
   DIFF — and `source` is the artifact-relative path of the very bytes decided
   over, so it is distinct for every scope the viewer can serve and stable across
   re-decisions of the same artifact, which `_attempt_key` documents as REPLACING
   the earlier record rather than appending. Say that in a comment.
5. If the result is a `HunkApprovalRefusal`, print it and exit 1 WITHOUT calling
   `save_job` — a refused decision is not a decision. Under `--json` print a
   JSON object carrying the refusal's `code`, `message` and `hunk_ids`; otherwise
   print `Error: <message>` to stderr, and the offending ids when there are any.
6. Otherwise `save_job(job)`, then report. Under `--json` print
   `record.exported` with `sort_keys=True`, which is JSON-safe by construction.
   Otherwise print the attempt key and one line per state count — approved,
   rejected and pending — derived from `record.ledger`, plus the line that every
   neighbour in this file ends on: that this is metadata only and no files have
   been modified.

IMPORT THE THREE ORCHESTRATION MODULES INSIDE THE FUNCTION, not at module top:
every other handler in this file defers its heavy imports the same way, and the
grouped CLI imports this module to build its dispatch table on every invocation.

## SPEC — `tests/orchestration/test_evidence_index.py`

An EDIT that ADDS ONE test, and it is the R-0743 fix. Every existing test stays.

Add a test pinning PRECEDENCE: with BOTH an index record naming an existing
directory AND a real `remedy-job-evidence-<job_id>` directory in the CWD, the
INDEX record wins. Its one-line docstring says why the order is load-bearing —
the index names the exported bundle and the relative directory is the deprecated
root-style fallback, so an inverted order lets a stale leftover shadow the real
bundle and hand a decision door the wrong diff. G7 mutation (iv) is the proof
this test is what pins it.

## SPEC — `tests/cli/test_patch_cmd.py`

A NEW FILE covering `apps/cli/commands/patch.py`'s handlers, named after its
source per AGENTS.md's Code Discoverability Conventions. Before writing it, READ
two existing files under `tests/cli/` and follow their idiom for building a job,
isolating the data root and capturing output — do not invent a third.

Add tests for: the command_id resolves through `get_command` and appears in
`collect_all_handlers()`; a clean mixed decision records under the envelope-derived
attempt key and `save_job` really persisted it, proved by loading the job again;
`--reject-hunk id=reason` keeps the reason VERBATIM; a `--reject-hunk` value with
no `=` produces the `missing_reason` refusal and NOT a handler-minted one; an
unknown job id exits 1; a job whose evidence directory does not resolve produces
the `no_diff_available` refusal and writes NOTHING; a refusal exits 1 and leaves
`job.metadata` without the decisions key; and `--json` prints parseable JSON on
both the success and the refusal path.

## The slices

<<<SLICE PLANF033R14
# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 4 of this feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 stable ids, viewer v2, consolidation | done | round 5 |
| decision core · subset diff · all-or-nothing apply | done | rounds 6, 7, 8 |
| failed-rollback truth · ledger · the door's effect | done | rounds 9-11, D4 |
| the recorder takes the viewer's envelope | done | round 12 |
| one evidence-directory resolver for viewer and doors | done | round 13 |
| the CLI command and its handler | open | this round |
| the write door's exposure and dispatch | open | next |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. The CLI command `patch.approve-hunks` and its handler, in ONE commit, because
   `apps/cli/grouped.py` answers `Error: no handler` for a catalog entry that has
   none. The `patch` group's size and exact subcommand set are pinned by an
   EQUALITY guard in `tests/test_command_catalog.py`, widened in that same commit.
   The handler mints no refusal vocabulary: every refusal comes from
   `hunk_approval` or `hunk_decision_record`. R-0743 is fixed here too — a test
   pinning that the index record beats the CWD-relative fallback.
2. Then the write door. `UI_EXPOSED_COMMANDS` is a SUBSET of the catalog pinned
   at exactly two ids by `TestUiExposedCommands`, so exposure needs step 1 first.
   `DOOR_METHODS` and `ALLOWED_IMPORTS` in
   `tests/ui_server/test_command_channel.py` are EQUALITY guards widened in the
   same commit as the dispatch, and `packages.orchestration.hunk_apply` joins
   `FORBIDDEN_MODULES` so DECISION F033 D4's forbidden mistake cannot be made
   silently later.
3. Then T003: rejection reasons quoted verbatim into the next repair prompt, the
   report line derived from the ledger, and partial state rendered truthfully in
   viewer, node and report.

## Risks
- The door's import guard is an EQUALITY guard: a new import reddens the branch
  tip unless it is ruled in the same commit. R-0738 is T003's to repair.
<<<END PLANF033R14

<<<SLICE RECORDF033R14
Gate: F033 R13 — THE SHARED EVIDENCE-DIRECTORY RESOLVER. THE ROUND PASSED. Every gate was re-executed by the reviewer at `34d5e4e4` from scripts of its own, and every ordered reading reproduced. TRANSPORT: the C0a blob is 29026 bytes at sha256 `7655c0b3…03a2f`, EQUAL to the reviewer's own scratchpad original, with ONE blob id `74999041` across `.agent/authored/f033-r13.md` and `.agent/last_block.md` at C0b — a chain walking the saved copy, its mirror and the working copy, which is what this workflow can measure and is not a claim about the emitted bytes. THE RECORD APPEND at `2e521057` reconstructs 1512826 plus one newline plus 5021 to 1517848, the committed blob exactly, base a byte PREFIX, N COUNTED at 1, the last unit equal to the slice's paragraph, and a negative control at byte 1515337 — proved to lie inside the FIRST appended paragraph, whose span the reviewer computed independently — rejected by BOTH readers. THE LEDGER: registered 303 UNMOVED, `Done:` 48 lines over 46 distinct UNMOVED, `Landed:` 15 UNMOVED, `Gate:` 129 to 130 with `^Gate: F033 R12 — ` going 0 to exactly 1, `DECISION F033 D` 4 UNMOVED, and the open set 257 at BOTH ends, exactly as ordered for a round that registers and resolves nothing. THE PROSE FILES: `.agent/plan.md` byte-EQUAL to its slice at 2750 bytes over 49 lines, under the 50-line cap; `.agent/prose_slips.md` reconstructs 23007 plus one newline plus 785 to 23793, with the round 12 slip lines going 0 to 2 and `- R-` lines 0. THE CODE: `ruff` over all three touched files exits 0 at "All checks passed!"; the moved function's `except` clause names exactly `ImportError`, `OSError`, `ValueError`, `KeyError` in that order, holds `remedy-job-evidence-` and holds neither `find_record` nor `load_index_records`; the delegation's extracted body calls `resolve_job_evidence_dir` and holds none of `json`, `resolve_data_root`, `evidence_dir_local` or `remedy-job-evidence-`; and `git show --numstat` on `packages/orchestration/ui_server.py` reads 8 and 16, confined to that one function. THE REVIEWER BUILT A PROOF THE BLOCK NEVER ORDERED, and it is the strongest reading in this entry: the OLD `_resolve_evidence_dir` was reconstructed by `git show` from the round 13 base blob, exec'd in isolation, and compared against the shipped `resolve_job_evidence_dir` AND against the delegation over fifteen constructed cases — an absent index, a named-and-present directory, a named-and-absent directory, a record with no `job_id` key, an empty and a missing `evidence_dir_local`, malformed JSON, a JSON list, a JSON null, a JSON string, an empty file, a path naming a FILE rather than a directory, the CWD-relative fallback alone, both sources present, and the index naming an absent directory with the fallback present. All three agree on every case, including the three that raise `AttributeError` rather than answering, so the move preserves the behaviour it found INCLUDING the inputs it does not handle, which is what the SPEC required and what a refactor is. THE MUTATIONS were re-run by the reviewer in its own disposable worktree at `55c365d6` with its OWN anchors, each asserted UNIQUE in its named file, the import first proved to resolve inside the worktree and the file restored byte-identically after each: the UNMUTATED CONTROL is a real exit 0 at 32 passed against 25 at the base; dropping the `is_dir()` check is exit 1 at 1 failed naming `test_record_naming_an_absent_directory_answers_none`; requiring the `job_id` key — the `find_record` re-expression this round refuses — is exit 1 at 1 failed naming `test_record_without_a_job_id_key_still_resolves`; and making the delegation return None is exit 1 at 1 failed naming `test_ui_server_resolver_answers_the_same_directory`. Each ordered mutation therefore kills exactly one test, which is a sharper result than a red. THE SUITES were re-run SERIALLY by the reviewer in the primary checkout, every REAL exit 0: `test_evidence_index.py` 32, `test_final_audit_evidence.py` 37, `test_diff_endpoint.py` 8, `test_hunk_decision_record.py` 15, `test_command_catalog.py` 18 and the canary 42. THE STRUCTURE: seven single-parent commits over the range ending at C5, of 408, 259, 14, 2, 4, 46 and 91 insertions, every one under 500; the path set EQUALS the declared change set in BOTH directions; the marker residue is 0 in all five applied targets against a non-zero control; `git ls-files .remedy-wt` 0; and ALL THIRTEEN do-not-touch paths byte-identical by blob id. THE HANDBACK carries every mandated section, and its `## Commits` cells agree with the reviewer's own `git diff --numstat` walk. THE WORKER'S FIVE DECLARED DEVIATIONS ARE ALL CORRECT AND NONE IS A FINDING: deviation 1 reports that G6(a) was headed "at C4" while naming the test file whose edit the Bundle put at C5, and the worker ran it at both commits rather than choosing — that is a reviewer-prose defect in the block, it damaged nothing on disk, and it is a dated line in `.agent/prose_slips.md`; deviation 2 reports that G8's path set cannot see `.agent/handoff.md` because C6 writes it, which is checklist item 14's shape and was handled honestly in both directions.

- R-0743 — Low, PRECEDENCE BETWEEN THE INDEX RECORD AND THE CWD-RELATIVE FALLBACK IS LOAD-BEARING AND NO TEST PINS IT. Raised by the reviewer at the F033 R13 gate by a mutation the block never ordered. `resolve_job_evidence_dir` in `packages/orchestration/evidence_index.py` at `34d5e4e4` reads the index record `<job_id>.json` FIRST and only then falls back to a CWD-relative `remedy-job-evidence-<job_id>` directory. That order is not arbitrary: the index record names the exported evidence bundle, while the relative directory is what this module's own docstring calls the deprecated root-style fallback, so an inverted order lets a stale leftover directory in an operator's repository root SHADOW the real indexed bundle. MEASURED in the reviewer's own disposable worktree at `55c365d6`, by moving the relative-fallback branch above the `try` and leaving every other byte alone: the file stays GREEN at 32 passed, while the three mutations the block DID order each go red at exactly one test. The seven tests added at `55c365d6` pin the index branch, the `is_dir()` check, the by-name read, the malformed-record fall-through, the fallback in both directions and the delegation — and none of them ever constructs BOTH sources at once, which is the only state in which precedence is observable. The behaviour on disk is CORRECT and this finding claims no defect in it; what is missing is the test that stops a later edit inverting it silently, in a function whose whole purpose is that the F037 viewer and the F033 decision doors resolve one directory rather than two. It is Low because nothing is wrong today and the fix is one test. FIX: a test constructing an index record naming an existing directory AND a real `remedy-job-evidence-<job_id>` directory in the CWD, asserting the index record wins, with a one-line docstring stating why the order is load-bearing. This finding belongs to the R-0671 class — an honesty rule a module states and no test pins — and resolving it here discharges that class for this function only, nowhere else.
<<<END RECORDF033R14

<<<SLICE SLIPSF033R14
2026-08-29 · F033 R13 · The block's G6 was headed "THE CODE AGAINST THE SPEC at C4" while its clause (a) ordered `ruff` over `tests/orchestration/test_evidence_index.py`, whose edit the same block's Bundle placed at C5, so at C4 that path still held its BASE content; the worker read the gate as load-bearing, ran it at C4 and again over the C5 tree, reported both as exit 0 and declared the disagreement, which is the required behaviour and left nothing wrong on disk.
<<<END SLIPSF033R14

## Done when — the gates

Run every one. Record the REAL exit code and the actual numbers, never the word
"green". One line per gate in the handback. Every gate below runs at or before
C5, so the handback at C6 can quote all of them; C6's own numbers are NOT
ordered here.

- **G1 HYGIENE.** `.agent/STOP` read from disk before C0a and again before C6,
  absent both times. `git status --porcelain` empty after EVERY commit. Branch
  `feature/f033-hunk-approval-v2` throughout. No force-push, no rewrite, no
  branch deletion; `git rev-parse feature/f033-hunk-approval` still `ed040812`.
- **G2 TRANSPORT.** Report sha256 and byte length of
  `<C0a>:.agent/authored/f033-r14.md` and of `.remedy-wt/f033-r14-block.md`, and
  whether they are EQUAL. Then `git rev-parse <C0b>:.agent/authored/f033-r14.md`
  and `git rev-parse <C0b>:.agent/last_block.md` must print ONE blob id.
- **G3 THE RECORD APPEND at C2.** (a) the BASE blob of `.agent/live_review.md`,
  which must be 1517848 bytes, plus one newline plus RECORDF033R14 equals the C2
  blob byte for byte; BASE a byte PREFIX; result ending in exactly one newline.
  (b) let N be the paragraph count your script COUNTS in RECORDF033R14 — report
  it — and compare the LAST N blank-line units of the C2 blob against the
  slice's paragraphs IN ORDER. NEGATIVE CONTROL at a BYTE offset your script
  PROVES lies inside the FIRST appended paragraph, whose span you compute in
  BYTES per convention 10 and report; BOTH readers must reject it.
- **G4 THE LEDGER at C2 and at C5.** At BASE, at C2 and at C5 count
  `^- R-\d+ — ` with distinct ids, `^Done: R-\d+ — ` lines with distinct ids,
  `^Landed: R-`, `^Gate: F\d+ R\d+ — ` and `^DECISION F033 D\d+ — `; report the
  open set at all three. Ordered: registered 303 to 304 at C2 with the ADDED id
  exactly `R-0743`; `Done:` 48 lines over 46 distinct UNMOVED throughout — this
  round resolves nothing, because only the reviewer may; `Landed:` 15 at BASE and
  C2 and 16 at C5, the added line matching `^Landed: R-0743 — `; `Gate:` 130 to
  131 with `^Gate: F033 R13 — ` exactly 1; `DECISION F033 D` 4 UNMOVED; and the
  open set 257 to 258.
- **G5 THE PROSE FILES.** `.agent/plan.md` at C1 is byte-EQUAL to PLANF033R14 —
  report its byte length and its line count, which must be under the 50-line cap
  AGENTS.md sets. `.agent/prose_slips.md` at C3 is the BASE blob, which must be
  23793 bytes, plus one newline plus SLIPSF033R14, byte for byte, with BASE a
  byte PREFIX; report the count of lines matching
  `^2026-\d\d-\d\d · F033 R13 · ` at BASE, which must be 0, and at C3, and the
  count of lines beginning `- R-` in the whole file at C3, which must be 0.
- **G6 THE CATALOG AND ITS GUARD at C4.** (a) `ruff check` over
  `apps/cli/command_catalog.py`, `apps/cli/commands/patch.py` and
  `tests/test_command_catalog.py` exits 0 — report the summary line. (b) Import
  the catalog at C4 and report: `get_command("patch.approve-hunks")`'s
  `group_id`, `subcommand`, `action_class`, `supports_json`, `may_mutate_repo`,
  `requires_permission`, its `args` NAMES in order, and which of those args carry
  `is_repeatable`. `may_mutate_repo` and `requires_permission` must both read
  False. (c) Report `len(get_commands_for_group("patch"))` and the sorted
  subcommand set, and report that `"patch.approve-hunks"` is in
  `collect_all_handlers()` — the entry and its handler must both exist at THIS
  commit. (d) Report the total `len(CATALOG)` and
  `len(collect_all_handlers())` at BASE and at C4, and the count of catalog
  command_ids with NO handler at both, which must be 0 at both. (e) Report
  `sorted(UI_EXPOSED_COMMANDS)` at C4, which must still be exactly
  `["decision.resolve", "job.stop"]` — the write door is NOT opened this round.
- **G7 THE MUTATION RED-PROOFS at C5.** In a DISPOSABLE `git worktree` at C5,
  never in the primary checkout, with `python3 -B`, having first proved the
  import resolves to the WORKTREE's copy. FIRST the UNMUTATED CONTROLS — REAL
  exit 0 with counts — over `tests/cli/test_patch_cmd.py` and
  `tests/orchestration/test_evidence_index.py`, the second of which must exceed
  the 32 BASE gives. Then, one at a time, reverting fully between each, asserting
  the anchor is UNIQUE inside the named FILE before replacing it, and reporting
  the REAL exit code, the failure count and the NAME of each failing test:
  (i) in `apps/cli/commands/patch.py`, call `save_job` on the refusal path too;
  (ii) in `apps/cli/commands/patch.py`, split each `--reject-hunk` value on its
      LAST `=` instead of its first;
  (iii) in `apps/cli/commands/patch.py`, pass `task_id` and `attempt` to the
      recorder the other way round;
  (iv) in `packages/orchestration/evidence_index.py`, move the relative-fallback
      branch ABOVE the `try`, so the CWD directory is consulted first — this is
      R-0743's proof and it MUST now go red, where at `55c365d6` it was green.
  Each MUST go RED. If any comes back GREEN, report that plainly and do NOT
  adjust anything to force a red. Remove the worktree BY EXACT PATH, then
  `git worktree prune`.
- **G8 SUITES AND STRUCTURE.** Serially, one pytest process at a time, each a
  REAL exit 0 with its count: `tests/cli/test_patch_cmd.py`,
  `tests/orchestration/test_evidence_index.py` (32 at BASE),
  `tests/test_command_catalog.py` (18 at BASE),
  `tests/cli/test_command_catalog.py` (23 at BASE),
  `tests/test_grouped_cli.py` (511 at BASE — report the count at C5 and whether
  it moved; a move is information, not a failure),
  `tests/ui_server/test_command_channel.py` (106 at BASE) and the canary
  `tests/cli/test_golden_path.py` (42 at BASE). Then walk
  `git rev-list --reverse BASE..C5`: each commit exactly ONE parent, each under
  500 INSERTIONS — the `+` column of `git diff --numstat`, never insertions plus
  deletions — and report the per-commit list. Report the range's path set against
  the change set in BOTH directions. Count `<<<SLICE ` and `<<<END ` in
  `.agent/plan.md`, `.agent/prose_slips.md`, `apps/cli/command_catalog.py`,
  `apps/cli/commands/patch.py` and `tests/cli/test_patch_cmd.py`: each 0, against
  `.agent/authored/f033-r14.md` as a non-zero control whose count you report.
  `git ls-files .remedy-wt` must read 0. Finally report that each of the
  do-not-touch paths named in the change-set section is byte-identical at BASE
  and at C5, by blob id — one line per path, with the count you measured.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: SESSION 4,
round 14, BASE, the changed-files table with real `+/-` from `git diff --numstat`
— derive that column from the tool, not from the files' line counts, and compare
it cell by cell against the numbers G8 produced — one line per gate with real
numbers, the item-status table with every ordered item exactly once, and your
deviations. Write external actions as command plus outcome. Quote the catalog
entry's fields from G6(b), the handler's `COMMAND_HANDLERS` line, and the test
names you wrote with the property each pins.

Carry SESSION 4 forward and name the next session's first actions in this order:
read `.agent/STOP` from disk, then run the Open PR Gate, then book this round's
verdict and resolve R-0743, then the plan's step 2. No length cap. Write no
verdict on your own work.
