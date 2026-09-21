# Handoff — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 8 · the single pass, R-1019, R-1025, the `do` group

## Session

SESSION 2 of feature F283 · round 8 · rounds so far 8

This round booked round 7's PASS, resolved R-1023 and R-1024, registered R-1025,
recorded DECISION F283 D3, repaired R-1025 (the product-spine test now asserts the
envelope), landed D3 part (a) (the single-pass `job run --json` answers in the
envelope on success/failure/no-pending-task) and part (b) (a blocked resume
refuses through `fail()`), gave round 7's `patch list` coverage gap its test,
repaired R-1019 (`worker unload` checks `--model`/`--all` before it probes
`ollama`), and moved 14 of the `do_cmd.py` group's 18 mechanical refusal pairs
onto `fail()` — 4 stayed, each a deviation recorded below. Context
self-assessment: roughly 98% of the working budget remained at the point this
handoff was written (about 14.67M of 15M tokens).

## Range

Review of `a8b8d547`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 230 | 230 | True |
| sha256 | `7c6d85ecb58c5b72b639d48a7b3e6d73cb28e65edc462fba12263dfd6d383223` | `7c6d85ecb58c5b72b639d48a7b3e6d73cb28e65edc462fba12263dfd6d383223` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `a8b8d547`, matching the delegation message.

## Commits

### 98e732d2 F283 R8 C1: copy round 8 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r8-block.md | +230/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f283-r8-decisions.md | +45/-0 | byte-for-byte copy of decisions.md |
| .agent/authored/f283-r8-ledger.md | +8/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r8-plan.md | +38/-0 | byte-for-byte copy of plan.md |

Measured insertions (`git show --numstat`): **321** (230+45+8+38).

### 91e425a3 F283 R8 C2: book round 7's PASS, resolve R-1023 and R-1024, register R-1025
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +45/-0 | append decisions.md: DECISION F283 D3 |
| .agent/live_review.md | +8/-0 | append ledger.md by strict byte concatenation: round-7 `Gate:` entry, `Done: R-1023`, `Done: R-1024`, `R-1025` registration |
| .agent/plan.md | +17/-15 | rewrite to plan.md payload, byte-identical; git's line diff shows only the lines that changed, not the whole file |

Measured insertions (`git show --numstat`): **70** (45+8+17); 15 deletions from the plan.md rewrite.

### b4f4f8f3 F283 R8 C3: the product-spine test asserts the envelope job show answers in
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_product_spine.py | +12/-7 | `TestJobFacadeNoAgent::test_job_status_invalid_id_safe` keeps its invocation; now asserts a non-zero exit, empty stderr, one JSON object on stdout with `ok` false, `error` `invalid_job_id`, `message` containing `not-a-uuid`, no `Traceback` in either stream; docstring names R-1025 and F283 round 3 |

Measured insertions: **12**.

### 56d7d812 F283 R8 C4: the single-pass run answers in the envelope under --json
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/job.py | +30/-1 | `_cmd_run_next_task_local` only: `emit_ok` imported alongside `fail`; the no-pending-task branch answers `emit_ok(job_id=..., outcome="no_pending_tasks", log=...)` under the flag; the verified-run branch answers `emit_ok(verified=True, **envelope_payload)`; the verification-failed branch answers `fail("verification_failed", "<n> verification check(s) failed", json_output=True, verified=False, **envelope_payload)` at exit 1 — same exit code the text branch already used. Flag off: every byte and exit code unchanged |
| tests/test_run_log_cli.py | +43/-5 | one new test per outcome under `json_output=True` (noop, success, verification-failure), each parsing the WHOLE of stdout as one object and asserting `ok`, the outcome's distinguishing keys and the exit code; the three helper functions (`_run_success`, `_run_verification_failure`) gained an optional `json_output=False` parameter so the existing text-mode tests' calls and assertions are byte-for-byte unchanged |

Measured insertions: **73** (30+43).

### 786eecb0 F283 R8 C5: a blocked resume refuses through fail() with its keys kept
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/job.py | +16/-21 | `_cmd_resume` only: both hand-rolled blocked branches (`ambiguous_recoverable_worktrees`, `worktree_recovery_blocked`) become `fail("resume_blocked", <message>, json_output=json_output, resumed=False, blocked_reason=<same>, worktrees=<same list>)` at exit 1; the text message carries one indented continuation line per blocked worktree (D3 part (b)) |
| tests/orchestration/test_worktree_lifecycle.py | +2/-0 | added assertions that the object also carries `ok` false and `error` `resume_blocked`, on the test that already asserts the top-level `blocked_reason` |
| tests/orchestration/test_worktree_resume_cli.py | +2/-0 | same addition, on the test that already asserts the top-level `blocked_reason` for the other blocked branch |

Measured insertions: **20** (16+2+2); 21 deletions from replacing the two hand-rolled `_json.dumps`/`print`/`sys.exit` blocks.

### 578a7784 F283 R8 C6: patch list's list-option refusal gets its envelope test
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_patch_cmd.py | +24/-0 | `TestListPatchIntentsInvalidListOptionIsAnEnvelope`: `_cmd_list_patch_intents` with an invalid `--sort` field under `json_output=True` exits 1 with empty stderr and envelope `invalid_list_option`; no product change (the call site already passed `json_output=json_output`, confirmed by reading it before writing the test) |

Measured insertions: **24**.

### 4048f470 F283 R8 C7: worker unload refuses a missing target before it probes the provider
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/worker.py | +4/-3 | `_cmd_worker_unload`: the `missing_argument` refusal for neither `--model` nor `--all` moves above the `shutil.which("ollama")` probe; same token, message, exit code; the unavailable branch otherwise unchanged |
| tests/cli/test_worker.py | +15/-0 | one new test, `shutil.which` patched to return `None`, asserting the missing-argument envelope fires anyway (R-1019); the existing path-probe test is untouched |

Measured insertions: **19** (4+15).

### 259651df F283 R8 C8: do refusals answer through fail()
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/do_cmd.py | +45/-43 | `fail` imported; 14 of `do_cmd.py`'s 18 mechanical print-then-exit pairs move onto `fail()` — 3 in `_validate_role_override` (`invalid_argument`, hardcoded `json_output=False`, no flag in scope), `_cmd_do_order`'s order-empty and force-conflict refusals (`invalid_argument`) and its budget-resolution refusal (`invalid_budget`), `_cmd_do`'s planner-provider refusal (`unsupported_provider`), `_cmd_job_run`'s write-mode refusal, repair-rounds refusal (`invalid_argument`), job-stopped refusal (`job_stopped`, new), budget-resolution refusal (`invalid_budget`) and resume-refusal (`job_not_resumable`, new), `_cmd_job_evidence`'s unsafe-task-id refusal (`unsafe_task_id`, new) and job-not-found refusal (`job_not_found`, reused). 4 sites stay, each a deviation (see below): `_cmd_do_order`'s `ctx.failed` site, `_cmd_do`'s no-such-contract-template site, `_cmd_run_show`'s no-such-run site, `_cmd_run_list`'s invalid-sort-field site |
| tests/cli/test_do_flags.py | +9/-2 | `test_an_invalid_budget_value_exits_2_and_leaves_the_repository_unregistered` repaired: it drove `--json` yet asserted the OLD shape (empty stdout, "Nothing was run." on stderr); now asserts `ok` false, `error` `invalid_budget`, the message on the ONE parsed stdout object, empty stderr — this is C8's required `do`-group envelope test |
| tests/cli/test_job_refusal_envelope.py | +55/-1 | `TestDoRefusalsAreAllMigrated`: no unflagged site remains, and exactly the 4 deviation sites remain flagged; `TestTheFlaggedRefusalsAreAllMigrated::test_the_module_calls_the_shared_helper` repaired to read the import with `ast` instead of an exact substring — C4's `from apps.cli.json_envelope import emit_ok, fail` broke the old literal-string check, caught by this round's own broad verification sweep, not by C4's self-review |

Measured insertions: **109** (45+9+55).

### C9 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot
table the commit that writes it.

## External actions

- `git worktree add .remedy-wt/f283-r8-g5 259651df` for G5 — used for the
  unmutated control and all five mutation red-proofs, then
  `git worktree remove .remedy-wt/f283-r8-g5` — a plain remove sufficed because
  every mutation was reverted by hand back to the original text (verified clean
  with `git status --porcelain` after the last revert) before removal.
- `git push origin feature/f283-machine-contracts-part-two` after C9 — real
  outcome reported in the session reply, since it ships this very file.
- `gh pr list --state open ...` after the push — real outcome reported in the
  session reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no `gh pr create`, no checkout of
  `main`, no branch deletion.
- No worktree other than the one disposable G5 worktree was added or removed.
  The three `remedy/job-*` worktrees were left alone throughout.

## Verification

### G1 — PAYLOADS transport, then four authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| decisions.md | 45/45 | 3407/3407 | True |
| ledger.md | 8/8 | 7231/7231 | True |
| plan.md | 38/38 | 1724/1724 | True |

**All readings equal: True.**

Four `.agent/authored/f283-r8-*` copies (the block copy plus three payloads), each
read back from the committed tree with `git show 98e732d2:<path>` and compared
byte-for-byte with its source:

| copy | bytes | identical to source |
|---|---|---|
| f283-r8-block.md | 15025 | True |
| f283-r8-decisions.md | 3407 | True |
| f283-r8-ledger.md | 7231 | True |
| f283-r8-plan.md | 1724 | True |

**Copies compared: 4. All True.**

### G2 — THE BOOKING

**(a) Append arithmetic**, by strict byte concatenation:

| file | pre (`a8b8d547`) | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 479875 | 7231 | 487106 | True |
| .agent/decisions.md | 1793909 | 3407 | 1797316 | True |

Matches the reviewer's stated `479875 + ledger.md = 487106` and
`1793909 + decisions.md = 1797316` exactly.

**(b) Line-anchored on the committed ledger**: `^Done: R-1023 — ` = **1**;
`^Done: R-1024 — ` = **1**; `^- R-1025 — ` = **1**; `^Done: R-1025 — ` = **0**.
Open set by distinct id, via `open_finding_ids` from
`scripts/rotate_live_review.py` (imported and called directly):

| rev | OPEN by distinct id |
|---|---|
| `a8b8d547` | **25** |
| C2 (`91e425a3`) | **24** |

Added: `['R-1025']`. Removed: `['R-1023', 'R-1024']`. Matches the reviewer's
stated 25 → 24, ADDED `R-1025`, REMOVED `R-1023`/`R-1024`, exactly.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**: `diff` reports no
difference (identical).

Line count: **38**, under the AGENTS.md 50-line rule.

### G3 — THE CHANGE, COUNTED FROM THE TREE

`git diff --name-only <parent> <commit>` and `git show --numstat` insertions, for
every commit C3 to C8 (parent → commit):

| commit | paths changed | insertions |
|---|---|---|
| C3 `91e425a3`→`b4f4f8f3` | tests/cli/test_product_spine.py | 12 |
| C4 `b4f4f8f3`→`56d7d812` | apps/cli/commands/job.py, tests/test_run_log_cli.py | 73 |
| C5 `56d7d812`→`786eecb0` | apps/cli/commands/job.py, tests/orchestration/test_worktree_lifecycle.py, tests/orchestration/test_worktree_resume_cli.py | 20 |
| C6 `786eecb0`→`578a7784` | tests/cli/test_patch_cmd.py | 24 |
| C7 `578a7784`→`4048f470` | apps/cli/commands/worker.py, tests/cli/test_worker.py | 19 |
| C8 `4048f470`→`259651df` | apps/cli/commands/do_cmd.py, tests/cli/test_do_flags.py, tests/cli/test_job_refusal_envelope.py | 109 |

At C8, `python3 .remedy-wt/f283-r6-scratch/pairs.py job.py do_cmd.py`:

```
job.py exits 2 mechanical 0 flagged 0 unflagged 0
   1119 _cmd_run_next_task_local False json_output
   1260 _cmd_job_run_cycles False json_output
do_cmd.py exits 5 mechanical 4 flagged 4 unflagged 0
   142 _refuse_before_any_step False None
   390 _cmd_do_order True json_output
   484 _cmd_run_show True json_output
   455 _cmd_do True json_output
   523 _cmd_run_list True json_output
```

The reviewer read at `a8b8d547` `job.py exits 4 mechanical 0 flagged 0
unflagged 0` and `do_cmd.py exits 19 mechanical 18 flagged 15 unflagged 3`.
`job.py`'s exit count fell from 4 to 2 because C4 and C5 (this round, not the
block's own migration target) removed 3 of its 4 literal `sys.exit` calls by
converting them to `fail()`/`emit_ok()` (whose own `sys.exit` lives inside
`json_envelope.py`, invisible to this AST scan of `job.py` alone) and left one
new one from `emit_ok(...); return` paths that never called `sys.exit` at all —
the two remaining exits (`_cmd_run_next_task_local`, `_cmd_job_run_cycles`) were
already non-mechanical before this round and are untouched. `do_cmd.py` fell from
`exits 19 mechanical 18 flagged 15 unflagged 3` to `exits 5 mechanical 4 flagged 4
unflagged 0`: 14 of 18 mechanical pairs migrated (all 3 unflagged sites among
them); 4 flagged sites stay, each a deviation from the block (below), plus the
one never-mechanical site (`_refuse_before_any_step`) unchanged throughout.

`git diff --name-only a8b8d547 259651df -- packages/` prints **nothing** (real
exit code implicit 0, empty stdout) — confirmed `packages/` untouched across the
whole round.

### Token list — every `fail()` token C4, C5, C7 and C8 use, its line, new or reused

| commit | line | token | new/reused | search behind a `new` one |
|---|---|---|---|---|
| C4 | 897 | (emit_ok, no token) | — | `emit_ok` carries no `error` token; `outcome="no_pending_tasks"` is a payload value, not a `fail()` token |
| C4 | 1094 | (emit_ok, no token) | — | same — success envelope, no token |
| C4 | 1097 | verification_failed | new | `grep -rn 'fail("' apps/cli/` before this commit: 0 hits for `verification_failed` as a `fail()` token (the string existed only as a `log.log(...)` EVENT name at job.py:978, a different vocabulary) |
| C5 | 1644 | resume_blocked | new | same full search: 0 hits before this commit; DECISION F283 D3 part (b) names this exact token |
| C5 | 1661 | resume_blocked | new (second site, same commit) | same search as L1644 |
| C7 | 158 | missing_argument | reused (pre-existing at this exact site; the migration REORDERS the check, not its token — worker.py's own line 158 and job.py:63 already used it) | — |
| C8 | 54 | invalid_argument | reused (job.py:1157, mission_cmd.py:490) | — |
| C8 | 61 | invalid_argument | reused (second site, same commit) | — |
| C8 | 68 | invalid_argument | reused (third site, same commit) | — |
| C8 | 269 | invalid_argument | reused (fourth site, same commit) | — |
| C8 | 272 | invalid_argument | reused (fifth site, same commit) | — |
| C8 | 299 | invalid_budget | reused (job.py:113, `resolve_job_budgets` raising the same `(BudgetConfigError, ValueError)` pair) | — |
| C8 | 442 | unsupported_provider | reused (worker.py:154, "a provider not supported for this operation/role" condition) | — |
| C8 | 675 | invalid_argument | reused (sixth site, same commit) | — |
| C8 | 688 | invalid_argument | reused (seventh site, same commit) | — |
| C8 | 704 | job_stopped | new | `grep -rn 'fail("job_stopped"' apps/cli/` before this commit: 0 hits; the condition (a job's OWN state, not a CLI flag, forbids the operation) has no existing `fail()` token, so it is named for the state constant `JOB_STOPPED` already used product-wide |
| C8 | 719 | invalid_budget | reused (second site, same commit, same underlying `resolve_job_budgets` exception pair) | — |
| C8 | 734 | job_not_resumable | new | `grep -rn 'fail("job_not_resumable"' apps/cli/` before this commit: 0 hits; `packages/orchestration/pingpong_job.py::job_resume_refusal` already embeds this exact spelling as the prefix of its own returned message (`"job_not_resumable: worktree cleanup_status=..."`) for the majority case, so this is the closest existing spelling to reuse, per DECISION F277 D8's "an existing spelling wins" |
| C8 | 809 | unsafe_task_id | new | `grep -rn 'fail("unsafe_task_id"' apps/cli/` before this commit: 0 hits; named for the `UnsafeTaskIdError` exception class the site catches |
| C8 | 819 | job_not_found | reused (the ONLY way `export_job_evidence`'s top-level `result["error"]` is truthy is its own `"Job {job_id!r} not found"` early return — confirmed by reading the whole function body — the exact condition `job_not_found` already names everywhere else) | — |

New tokens this round: `verification_failed`, `resume_blocked`, `job_stopped`,
`job_not_resumable`, `unsafe_task_id` — five, each confirmed absent from a
`fail("<token>"` search over `apps/cli/` before its introducing commit.

## Deviations & assumptions

1. **The bundle ran C1 through C8 — eight commits, exactly as ordered — before
   this handback commit C9.** Nothing was added, dropped or reordered.
2. **No expected insertion figure is given for C2's rewrite or for any C3–C8
   code commit, per the block's own convention**: only measured figures are
   reported above, and none of them was forced to match a prediction.
3. **`_cmd_do_order`'s `ctx.failed` site was NOT migrated**, though the AST rule
   reaches it (single `Error: `-prefixed print immediately before its
   `sys.exit(1)`). Migrating it broke `tests/cli/test_do_commit_flags.py` (4
   tests) and `tests/cli/test_do_sequence_cli.py` (2 tests) with a genuine NEW
   defect, not an old-shape repair: `_cmd_do_order` already prints the WHOLE
   result document to stdout, unconditionally, earlier in the SAME function
   under `--json`; wrapping the trailing print+exit in `fail()` makes `fail()`
   print a SECOND JSON object to stdout, so `json.loads(stdout)` raises
   `json.decoder.JSONDecodeError: Extra data` — the one-envelope invariant
   `fail()` exists to enforce, broken instead of upheld. The AST-only migration
   rule cannot see the prior print. A comment at the site records this. No
   choice of the round's one repairable `do` test file fixes this, because it
   is a correctness regression, not a shape the feature intends to change.
4. **`_cmd_do`'s no-such-contract-template site, `_cmd_run_show`'s no-such-run
   site and `_cmd_run_list`'s invalid-sort-field site were NOT migrated**,
   though each is a clean single-print mechanical pair whose migration would
   be a straightforward, CORRECT old-shape repair (empty stdout under `--json`
   becomes the envelope). Each breaks a test outside this round's tracked file
   set: the contract-template test lives in
   `tests/cli/test_do_sequence_cli.py::test_contract_naming_no_template_exits_2_naming_the_templates_and_writes_nothing`;
   the run-show and run-list tests live in
   `tests/cli/test_cli_ux.py::TestRunShow::test_missing_run_exits_one` and
   `::TestRunList::test_unknown_sort_field_exits_without_a_traceback`. Constraint
   3 permits repairing an old-shape break in only ONE named `do` test file this
   round, and `tests/cli/test_do_flags.py` was chosen (below) — so these three
   were reverted rather than shipped broken outside the allowed set. All three
   sites are candidates for a future round that names one of their own test
   files.
5. **`tests/cli/test_do_flags.py` was chosen as "the ONE do test file C8
   names"**, over `tests/cli/test_do_sequence_cli.py`, `test_do_commit_flags.py`
   or `test_cli_ux.py`, because it is explicitly about CLI flag validation
   (DECISION F268 D16) and is the natural home for the majority of this round's
   migrated sites (`_validate_role_override` ×3, order-empty, force-conflict,
   both budget sites, write-mode, repair-rounds, job-stopped). Its existing
   `test_an_invalid_budget_value_exits_2_and_leaves_the_repository_unregistered`
   already drove `--json` and asserted the OLD broken shape, so repairing it
   IS this round's required envelope test — no separate new test function was
   added on top of it.
6. **A test broken by C4, not caught until this round's own broad verification
   sweep, was repaired in C8**:
   `tests/cli/test_job_refusal_envelope.py::TestTheFlaggedRefusalsAreAllMigrated::test_the_module_calls_the_shared_helper`
   asserted the exact substring `"from apps.cli.json_envelope import fail"` in
   `job.py`'s source; C4 legitimately changed that import line to
   `"from apps.cli.json_envelope import emit_ok, fail"` (to import the new
   `emit_ok` alongside `fail`), which broke the substring match though `fail`
   is still imported and still called. Repaired with an `ast`-based check for
   `fail` in the module's imports from `apps.cli.json_envelope`, tolerant of
   whatever else shares that import line. Fixed here, in C8, rather than by
   amending C4, per AGENTS.md git discipline (no amend); `tests/cli/test_job_refusal_envelope.py`
   is already in this round's tracked file set for other reasons, so the repair
   needed no new file added to the set.
7. **No trailing commit for the C9 push or `gh pr list`; both go in the session
   reply**, consistent with DECISION amend0827 D2 and prior rounds' own
   precedent: the push carries this very file, so its outcome cannot be known
   before the commit exists.
8. **One disposable worktree (`.remedy-wt/f283-r8-g5`) was reused for the
   unmutated control and all five G5 mutations sequentially**, each reverted by
   hand and confirmed clean via `git status --porcelain` before removal.
9. **Before settling on the final C8 diff, every one of the 18 mechanical sites
   was migrated once, then a full sweep of every test file in the repository
   that imports `do_cmd` (plus files matching each site's exact old message
   text) was run to find breakage; the 4 sites named in deviations 3–4 were
   found broken and reverted, one at a time, confirmed green after each
   reversion.** No broken state was ever committed; every commit's tree was
   green before `git commit` ran.
10. **Constraints 1, 3 and 4 held throughout.** No payload was edited or
    retyped; only the sixteen paths named in the block's enumeration were
    touched (verified by set-equality below, C9 included); `packages/` was
    never touched; the rule reached exactly the 14 sites migrated (3 unflagged
    + 11 flagged among the 15 the block's own SPEC estimate implied, the
    remaining 4 flagged sites excluded for the reasons in deviations 3–4);
    every commit left the targeted G4 selection no redder than its base — the
    only red state anywhere this round was inside the exploratory edit/run/revert
    cycle described in deviation 9, never committed.

### The round's whole tracked path set (before this commit)

`git diff --name-only a8b8d547 259651df` — **18** distinct paths (job.py
touched by both C4 and C5, worker.py by C7 alone, do_cmd.py by C8 alone, each
counted once); plus `.agent/handoff.md` from this commit makes **19** — set-equal
to constraint 3's enumeration (4 authored copies + live_review.md + decisions.md
+ plan.md + handoff.md + job.py + worker.py + do_cmd.py + 8 named test files,
one of which, `test_do_flags.py`, is the ONE `do` test file C8 names):

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r8-block.md | C1 `98e732d2` |
| 2 | .agent/authored/f283-r8-decisions.md | C1 `98e732d2` |
| 3 | .agent/authored/f283-r8-ledger.md | C1 `98e732d2` |
| 4 | .agent/authored/f283-r8-plan.md | C1 `98e732d2` |
| 5 | .agent/decisions.md | C2 `91e425a3` |
| 6 | .agent/live_review.md | C2 `91e425a3` |
| 7 | .agent/plan.md | C2 `91e425a3` |
| 8 | tests/cli/test_product_spine.py | C3 `b4f4f8f3` |
| 9 | apps/cli/commands/job.py | C4 `56d7d812`, touched again by C5 `786eecb0` |
| 10 | tests/test_run_log_cli.py | C4 `56d7d812` |
| 11 | tests/orchestration/test_worktree_lifecycle.py | C5 `786eecb0` |
| 12 | tests/orchestration/test_worktree_resume_cli.py | C5 `786eecb0` |
| 13 | tests/cli/test_patch_cmd.py | C6 `578a7784` |
| 14 | apps/cli/commands/worker.py | C7 `4048f470` |
| 15 | tests/cli/test_worker.py | C7 `4048f470` |
| 16 | apps/cli/commands/do_cmd.py | C8 `259651df` |
| 17 | tests/cli/test_do_flags.py | C8 `259651df` |
| 18 | tests/cli/test_job_refusal_envelope.py | C8 (first touch) |
| 19 | .agent/handoff.md | C9 (this commit) |

No path outside the enumeration was touched: `.agent/candidates.md`,
`.agent/context.md`, `.agent/operator_questions.md`, `.agent/prose_slips.md`,
`README.md`, `docs/roadmap/**`, and `apps/cli/json_envelope.py` appear **0**
times. `packages/` appears **0** times (confirmed above under G3).

## Authored-text proofs

- The four copies at C1, compared with the reviewer's originals under
  `.remedy-wt/f283-r8-payloads/` and `.remedy-wt/f283-r8-block.md`: **four
  readings, all True** (G1).
- The one REWRITE payload against its committed file: `.agent/plan.md` is
  byte-identical to its payload (G2c, confirmed with `diff`).
- The two APPEND payloads against their committed files: strict byte
  concatenation True for `.agent/live_review.md` (ledger.md) and
  `.agent/decisions.md` (decisions.md), byte numbers equal to the reviewer's
  (G2a).
- No payload was edited or retyped. All four `.agent/authored/` copies and the
  one product-file rewrite were made with `shutil.copyfile`; the two appends by
  reading each payload's bytes and writing base+payload back to disk.
- Every change under `apps/` and `tests/` this round was WORKER-authored to the
  block's SPEC — there is no reviewer-authored diff to compare against for those
  files; the block's SPEC prose is the standard they were written to, and
  G3/G4/G5 above are the proof they meet it.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `a8b8d547`; block 230 lines / matching sha256 |
| C1 copy block + 3 payloads | done | 321 insertions |
| C2 book round 7 PASS, resolve R-1023/R-1024, register R-1025 | done | 70 insertions (45+8+17, 15 deletions from plan rewrite); open set 25→24, added R-1025, removed R-1023/R-1024 |
| C3 R-1025's test asserts the envelope | done | 12 insertions; test passes |
| C4 the single-pass run answers in the envelope | done | 73 insertions; 2 paths; DECISION F283 D3 part (a) |
| C5 a blocked resume refuses through fail() | done | 20 insertions; 3 paths; DECISION F283 D3 part (b) |
| C6 patch list's list-option refusal test | done | 24 insertions; no product change |
| C7 worker unload refuses before the probe | done | 19 insertions; 2 paths; R-1019 |
| C8 do refusals answer through fail() | done | 109 insertions; 3 paths; 14/18 mechanical pairs migrated, 4 deviations recorded |
| C9 the handback | done | this commit |
| G1 payload transport + authored copies | done | 3/3 payload readings equal; 4/4 authored copies byte-identical |
| G2(a) live_review.md + decisions.md append | done | 479875+7231=487106; 1793909+3407=1797316 |
| G2(b) R-1023/R-1024/R-1025 pairing + open set by distinct id | done | 1 Done R-1023 / 1 Done R-1024 / 1 R-1025 reg / 0 Done R-1025; 25→24, added R-1025, removed R-1023/R-1024 |
| G2(c) plan.md rewrite | done | byte-identical to payload; 38 lines, under 50 |
| G3 change counted from the tree | done | per-commit diffs and insertions all reported; `pairs.py` matches at C8; 0 paths under `packages/` |
| G4 targeted selection, ruff, integrity | done | 3215 passed/0 failed/0 xfailed (up from 3207+1); ruff exit 0; integrity all 5 pass, fail_count 0 |
| G5 red-proofs (a)(b)(c)(d)(e) | done | all five go RED at exactly the test(s) predicted; unmutated control 257 passed |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile`, byte concatenation only |
| Constraint 2 every commit under 500 insertions | done | 321, 70, 12, 73, 20, 24, 19, 109; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 18 paths after this commit, set-equal to the enumeration |
| Constraint 4 G4 selection no redder than base | done | red only inside an uncommitted edit/run/revert exploration (deviation 9); every commit's own tree was green before it was committed |
| Constraint 5 STOP if a gate goes red outside constraint 3's path set | done (n/a) | four sites were reverted rather than shipped broken outside the named paths (deviations 3–4); no STOP was needed since the round completed |
| Constraint 6 nothing is merged | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion |
| Constraint 7 G5 worktree under .remedy-wt/, removed, listed | done | `.remedy-wt/f283-r8-g5`, removed as G5's last action, `git worktree list` reported after; the three `remedy/job-*` worktrees untouched |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 8 — C1 through C9, with all six gates re-derived.
3. Then round 9 — the `Done:` lines of R-1019 and R-1025 booked in its first
   commit, and the `project` group with a ruling on its uppercase `ERROR:`
   prefix. The four sites this round left unmigrated in `do_cmd.py`
   (`_cmd_do_order`'s `ctx.failed`, `_cmd_do`'s contract-template lookup,
   `_cmd_run_show`'s run lookup, `_cmd_run_list`'s list-option refusal) remain
   for a round that can name one of `tests/cli/test_do_sequence_cli.py` or
   `tests/cli/test_cli_ux.py` as its own test file, or that restructures
   `_cmd_do_order`'s success-path JSON emission so the `ctx.failed` site no
   longer risks a double envelope.

Open findings count: **24** (unchanged in NET terms by this round's own
repairs — R-1023 and R-1024 closed this round; R-1025 opened this round and
stays open until round 9 books its `Done:` line). Operator-questions count:
**2** (unchanged this round).
