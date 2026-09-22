# Handoff — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 14 · T001's catalog half, first group (D9)

## Session

SESSION 4 of feature F283 · round 14 · rounds so far 14

This round booked round 13's PASS and a prose slip, and recorded DECISION F283 D9.
Then, in the order D9's groups land: `init run`, `dev status` and `dev smoke-help`
declared `supports_json` (`dev smoke-help` also gained `--json` and now answers
`emit_ok(commands=[...])`; `init run`'s not-a-repository refusal under `--json`
moved onto `fail("not_a_git_repo", ...)`), with a ratchet test class pinning the
commands still missing the declaration. Then `memory store` and the five memory
card mutations declared `supports_json` and answer `emit_ok` on success. Then
`blocker resolve` and the three `patch` commands (`show`, `approve`, `reject`)
declared `supports_json`; `patch show`'s two-line not-found refusal became one
`fail("patch_intent_not_found", ...)` call. No unordered commit was needed this
round.
Context self-assessment: roughly 95% of the working budget remained at the
point this handoff was written.

## Range

Review of `dc4c1e60`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 219 | 219 | True |
| sha256 | `a2b73c87d1ac0eca01f3cd598f281483d6832c0feeb0e5c5d81ff6d44a9d36a0` | `a2b73c87d1ac0eca01f3cd598f281483d6832c0feeb0e5c5d81ff6d44a9d36a0` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `dc4c1e60`, matching the delegation message.

## Commits

### e6709851 F283 R14 C1: copy round 14 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r14-block.md | +219/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f283-r14-decisions.md | +52/-0 | byte-for-byte copy of decisions.md |
| .agent/authored/f283-r14-ledger.md | +2/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r14-plan.md | +37/-0 | byte-for-byte copy of plan.md |
| .agent/authored/f283-r14-slips.md | +1/-0 | byte-for-byte copy of slips.md |

Measured insertions (`git show --numstat`): **311** (219+52+2+37+1).

### 5d1d49e6 F283 R14 C2: book round 13's PASS and a prose slip, record D9
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +52/-0 | append decisions.md: DECISION F283 D9 |
| .agent/live_review.md | +2/-0 | append ledger.md by strict byte concatenation: round-13 `Gate:` entry |
| .agent/prose_slips.md | +1/-0 | append slips.md: one dated prose-slip line |
| .agent/plan.md | +17/-13 | rewrite to plan.md payload, byte-identical; git's line diff shows only the lines that changed |

Measured insertions: **72** (52+2+1+17); 13 deletions from the plan.md rewrite.

### 264ef817 F283 R14 C3: init, dev status and dev smoke-help declare --json; the ratchet
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | +4/-0 | `init.run` and `dev.status` gain `supports_json=True`; `dev.smoke-help` gains `args=(_JSON_OPT,)` and `supports_json=True` |
| apps/cli/commands/dev.py | +10/-2 | `_dev_smoke_help` takes `json_output`; under `--json` answers `emit_ok(commands=[...])` with the two command lines its text prints; text branch unchanged; dispatch lambda threads `getattr(args, "json", False)` |
| apps/cli/commands/init_cmd.py | +8/-2 | `init.run`'s not-a-repository refusal under `--json` moves off the raw `_json.dump({"error": ...})` document onto `fail("not_a_git_repo", <sentence>, json_output=True, exit_code=4)`; text branch byte-for-byte unchanged (DECISION F283 D7); `dev_status`/`init.run` success documents untouched (D9 (4)) |
| tests/test_command_catalog.py | +66/-0 | new `_READ_ONLY_WITHOUT_SUPPORTS_JSON` module constant (30 ids) and `TestReadOnlyWithoutSupportsJSONRatchet`: the derived set (neither `may_mutate_repo` nor `may_execute_commands` nor `supports_json`) equals the constant by EQUALITY, and every command carrying `--json` declares `supports_json` |
| tests/cli/test_init_cmd.py | +13/-0 | new `TestInitJson.test_not_a_git_repo_answers_the_envelope`: `init --json` outside a git repo answers `schema_version` 1, `ok` false, `not_a_git_repo`, exit 4 |
| tests/test_cli_execution_loop_closure.py | +20/-0 | new `TestDevSmokeHelpJson.test_dev_smoke_help_json_through_the_dispatcher`: `dev smoke-help --json` through `apps.cli.grouped.main` answers `ok` true with `commands` |

Measured insertions: **121** (4+10+8+66+13+20); 4 deletions.

### 863cf559 F283 R14 C4: the memory store and card commands answer --json in the envelope
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | +12/-0 | `memory.store` and the five `memory.card-*` mutations gain `_JSON_OPT` and `supports_json=True` |
| apps/cli/commands/memory.py | +30/-7 | `_cmd_memory_store` takes `json_output`, answers `emit_ok(id, key)`; `_cmd_memory_card_approve`/`_reject`/`_stale` answer `emit_ok(id, key, review_status, validity, approved)`; `_cmd_memory_card_supersede` answers `emit_ok(old_id, new_id)`; `_cmd_memory_card_contradict` answers `emit_ok(memory_id, by_id)` — full ids as given, never the `[:8]` text prints; text branches unchanged; `memory.store`'s dispatch lambda threads `json_output` |
| tests/cli/test_memory_cmd.py | +80/-14 | module docstring's gap sentence rewritten to say it closed; `TestTheCatalogStillDeclaresWhatItDeclared` replaced by `TestTheCatalogNowDeclaresJSONForEveryCardCommand` (all six card commands declare `supports_json`); new `TestStoreAndTheCardMutationsAnswerJSONThroughTheDispatcher`: one success envelope per command through `apps.cli.grouped.main`, plus one `memory_card_not_found` refusal envelope |
| tests/test_command_catalog.py | +5/-10 | ratchet constant loses the six memory ids (30→24), docstring updated |

Measured insertions: **127** (12+30+80+5); 31 deletions.

### 998fc192 F283 R14 C5: blocker resolve and the patch commands answer --json in the envelope
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | +8/-3 | `blocker.resolve` gains `_JSON_OPT` and `supports_json=True`; `patch.show`, `patch.approve`, `patch.reject` gain `_JSON_OPT` and `supports_json=True` |
| apps/cli/commands/blocker.py | +5/-2 | `_cmd_blocker_resolve` answers `emit_ok(id=<full id>, reason_code=...)` under `--json`; text branch unchanged |
| apps/cli/commands/patch.py | +52/-25 | `_cmd_show_patch_intent` takes `json_output`; its two-line not-found refusal becomes one `fail("patch_intent_not_found", <two sentences joined by \n>, json_output=json_output)`, text byte-for-byte unchanged; success answers `emit_ok(job_id, intent, diff_preview)`; `_cmd_approve_patch_intent`/`_cmd_reject_patch_intent` take `json_output`, thread it to every `fail()`, and answer `emit_ok(intent_id, target_path, risk, state, reason_recorded)` with `state` `approved`/`rejected`; text branches unchanged; three dispatch lambdas thread `json_output` |
| tests/cli/test_advertised_commands.py | +6/-3 | `test_flag_scanner_reports_a_flag_the_command_does_not_declare` now uses `--not-a-real-flag` (a flag no command declares) instead of `--json`, which `patch approve` now declares; both original assertions kept |
| tests/cli/test_blocker_cmd.py | +31/-0 | new `TestBlockerResolveAnswersJSONThroughTheDispatcher`: a success envelope (`id`, `reason_code`) and a `blocker_not_found` refusal envelope, both through `apps.cli.grouped.main` |
| tests/cli/test_job_refusal_envelope.py | +10/-7 | `TestPatchRefusalsAreAllMigrated.test_exactly_one_unflagged_site_remains` → `test_no_unflagged_site_remains` (the show-intent pair is migrated onto `fail()`, so the unflagged list is empty); class docstring corrected |
| tests/cli/test_patch_cmd.py | +99/-0 | new `TestShowApproveRejectAnswerJSONThroughTheDispatcher`: success envelopes for `show`/`approve`/`reject` and a `patch_intent_not_found` refusal envelope for `show`, all through `apps.cli.grouped.main` |
| tests/test_command_catalog.py | +6/-8 | ratchet constant loses `blocker.resolve` and the three `patch` ids (24→20); now equals exactly the twenty D9 leaves to the later groups; docstring updated |

Measured insertions: **217** (8+5+52+6+31+10+99+6); 48 deletions.

### C6 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot
table the commit that writes it.

## External actions

- `git worktree add .remedy-wt/f283-r14-redproof 998fc192` for G5 — used for
  the unmutated control and all four mutation red-proofs, each reverted with
  the file tool and confirmed byte-identical (`diff`) against the primary
  checkout's committed file before the next — then `git worktree remove
  --force .remedy-wt/f283-r14-redproof`.
- `git push origin feature/f283-machine-contracts-part-two` after C6 — real
  outcome reported in the session reply, since it ships this very file.
- `gh pr list --state open ...` after the push — real outcome reported in the
  session reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no `gh pr create`, no checkout of
  `main`, no branch deletion.
- No worktree other than the one disposable G5 worktree above (removed) was
  added. The three `remedy/job-*` worktrees were left alone throughout.

## Verification

### G1 — PAYLOADS transport, then five authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| ledger.md | 2/2 | 2702/2702 | True |
| decisions.md | 52/52 | 4173/4173 | True |
| plan.md | 37/37 | 1638/1638 | True |
| slips.md | 1/1 | 413/413 | True |

**All readings equal: True.**

Five `.agent/authored/f283-r14-*` copies (the block copy plus four payloads),
each read back from the committed tree with `git show e6709851:<path>` and
compared byte-for-byte (sha256) with its source:

| copy | sha256 equal to source |
|---|---|
| f283-r14-block.md | True |
| f283-r14-decisions.md | True |
| f283-r14-ledger.md | True |
| f283-r14-plan.md | True |
| f283-r14-slips.md | True |

**Copies compared: 5. All True.**

### G2 — THE BOOKING

**(a) Append arithmetic**, by strict byte concatenation:

| file | pre (`dc4c1e60`) | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 514680 | 2702 | 517382 | True |
| .agent/decisions.md | 1819599 | 4173 | 1823772 | True |
| .agent/prose_slips.md | 361415 | 413 | 361828 | True |

Matches the reviewer's stated compositions (514680+ledger.md=517382,
1819599+decisions.md=1823772) exactly; `prose_slips.md`'s composition
(361415+413=361828) confirmed the same way.

**(b) Line-anchored on the committed ledger**: `^Gate: F283 R13 — ` = **1**.
Open set by distinct id, via `open_finding_ids` from
`scripts/rotate_live_review.py` (imported and called directly):

| rev | OPEN by distinct id |
|---|---|
| `dc4c1e60` | **24** |
| C2 (`5d1d49e6`) | **24** |

Added: `[]`. Removed: `[]`. Matches the reviewer's stated 24 → 24, ADDED empty,
REMOVED empty, exactly.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**: sha256-equal to the
payload (`05cbd93bc5c81d45e2a173b8491c228baeaa51f520c424ab71928aa7f1da7f94`
both).

Line count: **37**, under the AGENTS.md 50-line rule.

### G3 — THE CHANGE, COUNTED FROM THE TREE

`git diff --name-only <parent> <commit>` and `git show --numstat` insertions:

| commit | paths changed | insertions |
|---|---|---|
| C3 `5d1d49e6`→`264ef817` | apps/cli/command_catalog.py, apps/cli/commands/dev.py, apps/cli/commands/init_cmd.py, tests/cli/test_init_cmd.py, tests/test_cli_execution_loop_closure.py, tests/test_command_catalog.py | 121 |
| C4 `264ef817`→`863cf559` | apps/cli/command_catalog.py, apps/cli/commands/memory.py, tests/cli/test_memory_cmd.py, tests/test_command_catalog.py | 127 |
| C5 `863cf559`→`998fc192` | apps/cli/command_catalog.py, apps/cli/commands/blocker.py, apps/cli/commands/patch.py, tests/cli/test_advertised_commands.py, tests/cli/test_blocker_cmd.py, tests/cli/test_job_refusal_envelope.py, tests/cli/test_patch_cmd.py, tests/test_command_catalog.py | 217 |

The derived set (D9's rule — neither `may_mutate_repo` nor `may_execute_commands`
nor `supports_json`, computed by importing `CATALOG` from each commit's own
`git show <sha>:apps/cli/command_catalog.py` blob, not from the working tree):

| commit | derived set size |
|---|---|
| C3 `264ef817` | **30** |
| C4 `863cf559` | **24** |
| C5 `998fc192` | **20**, exactly the twenty D9 leaves to `decision`, `job plan`, `brain`, then `ui`, `project` (confirmed by direct set comparison) |

`python3 .remedy-wt/f283-r6-scratch/pairs.py patch.py init_cmd.py` at `998fc192`:

| module | summary |
|---|---|
| patch.py | `exits 3 mechanical 1 flagged 1 unflagged 0` |
| init_cmd.py | `exits 1 mechanical 0 flagged 0 unflagged 0` |

Against the reviewer's `dc4c1e60` reading (`patch.py exits 4 mechanical 2
flagged 1 unflagged 1`, `init_cmd.py exits 1 mechanical 0 flagged 0 unflagged
0`): `patch.py`'s unflagged site is gone (the show-intent print-pair became one
`fail()` call, so its literal `sys.exit(1)` disappears from the AST along with
the two `print(..., file=sys.stderr)` lines — exits drop 4→3, mechanical 2→1);
the flagged revert-blocked site is untouched; `init_cmd.py` is unchanged
(its one `sys.exit(4)` is still preceded by an `if`/`else` compound, never a
bare stderr print, so it was never "mechanical" and stays that way).

`git diff --name-only dc4c1e60 998fc192 -- packages/` prints **nothing** (real
exit code implicit 0, empty stdout) — confirmed `packages/` untouched across
the whole round.

### Token list — every token this round's `fail(`/`emit_error(` calls introduce or reuse

Every `fail(`/`emit_error(` call line this round's diff added or changed, and
its token's `git grep -c '"<token>"' dc4c1e60 -- apps/cli/` count (summed
across files) at the round's base:

| commit | token | call site | count at `dc4c1e60` | new or reused |
|---|---|---|---|---|
| C3 | not_a_git_repo | `init_cmd.py::_handle_init` (new call site) | 2 (`apps/cli/commands/project.py`) | reused |
| C5 | job_not_found | `patch.py::_cmd_show_patch_intent`/`_cmd_approve_patch_intent`/`_cmd_reject_patch_intent` (`json_output` arg threaded; call sites pre-existed) | 44 (summed across 15 files) | reused |
| C5 | patch_intent_not_found | `patch.py::_cmd_show_patch_intent` (new call site); `_cmd_approve_patch_intent`/`_cmd_reject_patch_intent` (arg threaded; pre-existing sites) | 2 (`apps/cli/commands/patch.py`) | reused |

No token this round's `fail()`/`emit_error()` calls use is new at `apps/cli/`
level; C4's `emit_ok()` calls (`memory.py`, `blocker.py`) carry no error token
and the `fail("memory_card_not_found"/"blocker_not_found", ...)` refusal call
LINES those two modules already had were not touched by this round's diff (only
their surrounding success branches gained `emit_ok`), so neither of those two
tokens is part of this round's `fail()`/`emit_error()` token list.

### G4 — TARGETED SELECTION, ruff, integrity

`.remedy-wt/f283-r14-scratch/selection.txt`: **148** space-separated paths
(`-n auto`). The reviewer read at `dc4c1e60`: `5702 passed, 8 skipped`, exit 0.

| when | exit code | summary |
|---|---|---|
| after C3 | 0 | 5706 passed, 8 skipped |
| after C4 | 0 | 5713 passed, 8 skipped |
| after C5 | 0 | 5719 passed, 8 skipped |

Zero failed, zero errors at each; the passed count only rose (+4 at C3, +7 at
C4, +6 at C5, all from new tests this round added; skipped unchanged at 8
throughout).

`python3 -m ruff check` over every `.py` path the round touched
(`apps/cli/command_catalog.py`, `apps/cli/commands/blocker.py`,
`apps/cli/commands/dev.py`, `apps/cli/commands/init_cmd.py`,
`apps/cli/commands/memory.py`, `apps/cli/commands/patch.py`,
`tests/test_command_catalog.py`, `tests/cli/test_init_cmd.py`,
`tests/test_cli_execution_loop_closure.py`, `tests/cli/test_memory_cmd.py`,
`tests/cli/test_blocker_cmd.py`, `tests/cli/test_patch_cmd.py`,
`tests/cli/test_job_refusal_envelope.py`, `tests/cli/test_advertised_commands.py`),
run after C5: **All checks passed!**

`python3 -m apps.cli.main integrity check --json`, run after C5: `"passed":
true, "fail_count": 0`, all five checks (`handler_import`,
`live_review_verdict`, `plan_consistency`, `relevant_untracked`,
`high_blockers_open`) read `"status": "pass"`.

`python3 -m pytest tests/cli/test_golden_path.py -q`, run once after C5:
**42 passed**, exit 0.

### G5 — RED-PROOFS

Disposable worktree `.remedy-wt/f283-r14-redproof` at `998fc192` (C5), never
committed. Ran `tests/test_command_catalog.py`, `tests/cli/test_init_cmd.py`,
`tests/cli/test_memory_cmd.py`, `tests/cli/test_blocker_cmd.py` and
`tests/cli/test_patch_cmd.py` UNMUTATED first, then each mutation alone over
those five files, reverted with the file tool before the next (confirmed
byte-identical to the primary checkout's committed file with `diff`, no
output, after each revert):

| step | exit code | result | failing tests |
|---|---|---|---|
| unmutated control | 0 | 131 passed | — |
| (a) `card-approve`'s success prints its text line even under `--json` | 1 | 1 failed, 130 passed | `TestStoreAndTheCardMutationsAnswerJSONThroughTheDispatcher::test_a_card_mutation_answers_the_envelope[card-approve-approve_memory_card]` |
| (b) `patch show`'s not-found refusal forced `json_output=False` | 1 | 1 failed, 130 passed | `TestShowApproveRejectAnswerJSONThroughTheDispatcher::test_show_refusal_is_the_envelope_through_the_dispatcher` |
| (c) `blocker.resolve`'s catalog entry drops `supports_json=True`, `--json` arg kept | 1 | 2 failed, 129 passed | `TestReadOnlyWithoutSupportsJSONRatchet::test_the_derived_set_equals_the_pinned_constant`, `TestReadOnlyWithoutSupportsJSONRatchet::test_every_command_carrying_json_declares_supports_json` |
| (d) `init`'s `--json` not-a-repository branch prints the old `{"error": ...}` document | 1 | 1 failed, 130 passed | `TestInitJson::test_not_a_git_repo_answers_the_envelope` |

Each mutation reddened exactly its named target(s) and nothing else. Each was
reverted and confirmed byte-identical to the primary checkout's committed file
(`diff`, no output) before the next; a final post-revert control run also read
131 passed, and `git status --porcelain` inside the worktree was empty before
removal. `git worktree remove --force .remedy-wt/f283-r14-redproof` afterward.
`git worktree list` (post-removal): the primary checkout alone at `998fc192` —
`/home/decodeux/Repos/remedy 998fc192 [feature/f283-machine-contracts-part-two]`.
No `remedy/job-*` worktrees existed this round (none were added or touched).

## Deviations & assumptions

1. **Command-catalog.py's edits were written once, then split into three
   commits by restoring and re-applying.** All three groups' catalog and
   handler edits were drafted together first; before any commit, the file was
   restored to its `dc4c1e60` blob and the C3/C4/C5 slices were re-applied and
   committed in order, each verified against the pre-saved full-edit reference
   copy in `.remedy-wt/f283-r14-scratch/`. This is reported because it is a
   real editing-order deviation from a strictly linear "write commit N, then
   write commit N+1" sequence, even though the constraint 4 selection runs and
   every commit's own diff are exactly what the block orders — the same
   caution applied to `blocker.py`/`memory.py`/`patch.py`: handler edits were
   drafted early, then RESTORED to base with `git checkout --` before the C3
   selection run so that run measured the true C3 tree rather than a tree
   carrying uncommitted C4/C5 work, and re-applied from the saved copies at
   C4/C5 respectively.
2. **The `dev smoke-help --json` payload's two command strings drop their
   text-mode leading two-space indent.** The block says the list holds "the
   two command lines its text prints"; read as the runnable shell command
   text (`source scripts/remedy_smoke.sh && remedy_smoke` and `bash
   scripts/remedy_smoke.sh`) rather than the literal printed line including
   its presentation indent, since a machine consumer wants a command it can
   run, not a display string.
3. **`reason_recorded` on `patch approve`/`patch reject`'s JSON payload is
   `bool(reason)`**, matching the text branch's own `'recorded' if reason else
   'none'` condition (a falsy empty-string reason reads the same in both
   shapes), rather than `reason is not None` (which the neighbouring
   `run_log` call uses as `reason_present` for a different purpose).
4. **`not_a_git_repo` and `patch_intent_not_found` are REUSED tokens, not
   new ones**, discovered only by grepping the base commit rather than assumed
   from the block's language — see the Token list above. `job_not_found` is
   reused too (44 pre-existing hits); no `fail()`/`emit_error()` call this
   round introduces touches an unprecedented token string.
5. **Constraints 1, 2, 3, 4, 6 and 7 held throughout.** No payload was edited
   or retyped; every commit stayed under 500 insertions (311, 72, 121, 127,
   217; this handoff exempt as a single `.agent/**` state file); the round's
   tracked path set (23 distinct paths before this commit, 24 after) is
   EXACTLY constraint 3's full enumeration, with nothing outside it and
   nothing missing; `packages/` was never touched; every commit from C3 on
   left selection A at zero failed and zero errors; nothing was merged, no PR
   created, no checkout of `main`; the one G5 worktree was removed as its own
   last action and no `remedy/job-*` worktree existed to disturb.

### The round's whole tracked path set (before this commit)

`git diff --name-only dc4c1e60 998fc192` — **23** distinct paths
(`apps/cli/command_catalog.py` touched by C3, C4 and C5; `tests/test_command_catalog.py`
touched by C3, C4 and C5 — each counted once); plus `.agent/handoff.md` from
this commit makes **24** — EXACTLY constraint 3's full enumeration:

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r14-block.md | C1 `e6709851` |
| 2 | .agent/authored/f283-r14-decisions.md | C1 `e6709851` |
| 3 | .agent/authored/f283-r14-ledger.md | C1 `e6709851` |
| 4 | .agent/authored/f283-r14-plan.md | C1 `e6709851` |
| 5 | .agent/authored/f283-r14-slips.md | C1 `e6709851` |
| 6 | .agent/decisions.md | C2 `5d1d49e6` |
| 7 | .agent/live_review.md | C2 `5d1d49e6` |
| 8 | .agent/prose_slips.md | C2 `5d1d49e6` |
| 9 | .agent/plan.md | C2 `5d1d49e6` |
| 10 | apps/cli/command_catalog.py | C3 `264ef817`, touched again by C4 `863cf559` and C5 `998fc192` |
| 11 | apps/cli/commands/dev.py | C3 `264ef817` |
| 12 | apps/cli/commands/init_cmd.py | C3 `264ef817` |
| 13 | tests/test_command_catalog.py | C3 `264ef817`, touched again by C4 `863cf559` and C5 `998fc192` |
| 14 | tests/cli/test_init_cmd.py | C3 `264ef817` |
| 15 | tests/test_cli_execution_loop_closure.py | C3 `264ef817` |
| 16 | apps/cli/commands/memory.py | C4 `863cf559` |
| 17 | tests/cli/test_memory_cmd.py | C4 `863cf559` |
| 18 | apps/cli/commands/blocker.py | C5 `998fc192` |
| 19 | apps/cli/commands/patch.py | C5 `998fc192` |
| 20 | tests/cli/test_advertised_commands.py | C5 `998fc192` |
| 21 | tests/cli/test_blocker_cmd.py | C5 `998fc192` |
| 22 | tests/cli/test_job_refusal_envelope.py | C5 `998fc192` |
| 23 | tests/cli/test_patch_cmd.py | C5 `998fc192` |
| 24 | .agent/handoff.md | C6 (this commit) |

No path outside constraint 3's enumeration was touched: `.agent/candidates.md`,
`.agent/context.md`, `.agent/operator_questions.md`, `README.md`,
`docs/roadmap/**`, `scripts/**` and `apps/cli/json_envelope.py` appear **0**
times. `apps/cli/grouped.py` appears **0** times. `packages/` appears **0**
times (confirmed above under G3).

## Authored-text proofs

- The five copies at C1, compared with the reviewer's originals under
  `.remedy-wt/f283-r14-payloads/` and `.remedy-wt/f283-r14-block.md`: **five
  readings, all True** (G1).
- The three APPEND payloads against their committed files: strict byte
  concatenation True for `.agent/live_review.md` (ledger.md),
  `.agent/decisions.md` (decisions.md) and `.agent/prose_slips.md` (slips.md),
  byte numbers equal to the reviewer's (G2a).
- The one REWRITE payload against its committed file: `.agent/plan.md`'s
  committed sha256 equals the payload's sha256 (G2c).
- No payload was edited or retyped. All five `.agent/authored/` copies were
  made with `shutil.copyfile`; the three appends by reading each payload's
  bytes and writing base+payload back to disk; the plan.md rewrite by
  `shutil.copyfile`.
- Every change under `apps/` and `tests/` this round was WORKER-authored to
  the block's SPEC and DECISION F283 D9 — there is no reviewer-authored diff
  to compare against for those files; G3/G4/G5 above are the proof they meet
  the SPEC.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `dc4c1e60`; block 219 lines / matching sha256 |
| C1 copy block + 4 payloads | done | 311 insertions |
| C2 book round 13 PASS, record D9 | done | 72 insertions (52+2+1+17, 13 deletions from plan rewrite); open set 24→24, added/removed empty |
| C3 init, dev status, dev smoke-help declare --json; ratchet | done | 121 insertions; derived set 30, matches pinned constant |
| C4 memory store and card commands answer --json | done | 127 insertions; derived set 24 |
| C5 blocker resolve and patch commands answer --json | done | 217 insertions; derived set 20, exactly the D9 leaves to later groups |
| C6 the handback | done | this commit |
| G1 payload transport + authored copies | done | 4/4 payload readings equal; 5/5 authored copies byte-identical |
| G2(a) live_review.md + decisions.md + prose_slips.md append | done | 514680+2702=517382; 1819599+4173=1823772; 361415+413=361828 |
| G2(b) open set by distinct id | done | 1 Gate line; 24→24, added none, removed none |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 37 lines, under 50 |
| G3 change counted from the tree | done | per-commit diffs and insertions reported; derived set 30→24→20; pairs.py patch.py 4/2/1/1→3/1/1/0, init_cmd.py unchanged 1/0/0/0; 0 paths under `packages/` |
| Token list | done | not_a_git_repo (2 hits, reused), job_not_found (44 hits, reused), patch_intent_not_found (2 hits, reused) — none new |
| G4 targeted selection, ruff, integrity, golden path | done | 5706/5713/5719 passed after C3/C4/C5 (up from 5702), 0 failed/errors at each; ruff exit 0; integrity all 5 pass, fail_count 0; golden path 42 passed |
| G5 red-proofs (a)(b)(c)(d) | done | all four go RED, each reddening exactly its named target(s); unmutated control 131 passed; post-revert control 131 passed |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile`, byte concatenation only |
| Constraint 2 every commit under 500 insertions | done | 311, 72, 121, 127, 217; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 23 paths before this commit (24 after), EXACTLY the full enumeration |
| Constraint 4 G4 selection at zero failed after every commit | done | 5706/5713/5719 passed, 0 failed/errors at each |
| Constraint 5 STOP if a gate goes red outside constraint 3's path set | done (n/a) | no gate went red outside the named paths; no STOP was needed |
| Constraint 6 nothing is merged | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion |
| Constraint 7 G5 worktree under .remedy-wt/, removed, listed | done | `.remedy-wt/f283-r14-redproof`, removed, `git worktree list` reported after; no `remedy/job-*` worktree existed to disturb |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 14 — C1 through C6, all six gates re-derived.
3. Then T001's catalog half second group, as `.agent/plan.md` lists it:
   `decision resolve`, `decision explain`, `job plan` and the seven `brain`
   report and viewer commands.

Open findings count: **24**. Operator-questions count: **0**.
