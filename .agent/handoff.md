# Handoff — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 13 · `remedy runtime` refuses through `fail()`, D8

## Session

SESSION 3 of feature F283 · round 13 · rounds so far 13

This round booked round 12's PASS and recorded DECISION F283 D8. Then, one
commit each: `runtime_cmd.py`'s local `_fail` is deleted and every call site
becomes `_runtime_refusal(error_class, ...)`, a helper that looks `error_class`
up in a new `RUNTIME_ERROR_TOKENS` table and calls `fail()` with that token,
keeping `error_class` in the payload; then the four result-shaped failure
exits (probe cleanup survivors, probe readiness, a served runtime's failed
health check, `stop` that did not stop) answer the same envelope shape under
`--json`, built with `emit_error()`, text branches and exit codes unchanged.
No unordered commit was needed this round.
Context self-assessment: roughly 70% of the working budget remained at the
point this handoff was written.

## Range

Review of `2ac999da`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 190 | 190 | True |
| sha256 | `1990bb378a5c4f2b50b95523950aff8d0543df328efb6c744cee3ba1d154e247` | `1990bb378a5c4f2b50b95523950aff8d0543df328efb6c744cee3ba1d154e247` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `2ac999da`, matching the delegation message.

## Commits

### e8a1e6b8 F283 R13 C1: copy round 13 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r13-block.md | +190/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f283-r13-decisions.md | +33/-0 | byte-for-byte copy of decisions.md |
| .agent/authored/f283-r13-ledger.md | +2/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r13-plan.md | +33/-0 | byte-for-byte copy of plan.md |

Measured insertions (`git show --numstat`): **258** (190+33+2+33).

### c38cab8a F283 R13 C2: book round 12's PASS, record D8
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +33/-0 | append decisions.md: DECISION F283 D8 |
| .agent/live_review.md | +2/-0 | append ledger.md by strict byte concatenation: round-12 `Gate:` entry |
| .agent/plan.md | +10/-10 | rewrite to plan.md payload, byte-identical; git's line diff shows only the lines that changed |

Measured insertions: **45** (33+2+10); 10 deletions from the plan.md rewrite.

### aa42e451 F283 R13 C3: runtime refusals answer through fail(), keyed on error_class (D8)
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/runtime_cmd.py | +124/-112 | `_fail` deleted; `RUNTIME_ERROR_TOKENS` (7 classes) and `_runtime_refusal(error_class, message, exit_code, *, json_output, **payload) -> NoReturn` added, calling `fail()`; all 26 former `_fail` call sites become `_runtime_refusal` calls, same message/code/payload keys, `error_class` now the leading argument instead of a payload dict entry; module docstring names the envelope and the token table beside the exit-code contract |
| tests/cli/test_job_refusal_envelope.py | +37/-0 | new `TestRuntimeCmdRefusalsAreAllMigrated`: no `_fail` function defined, no print-then-exit pair (mechanical or branched) survives — the four D8 result-shaped exits print behind an `if json_output: ... else: ...` whose `sys.exit` is never immediately preceded by a bare `print(..., file=sys.stderr)`, so both lists read empty — and `fail` is imported from `apps.cli.json_envelope` |
| tests/cli/test_runtime_cmd.py | +26/-0 | new `TestRuntimeErrorTokens` (every token value distinct; every literal `error_class` the source passes to `_runtime_refusal` is a table key); `test_a_missing_runtime_exits_2` (both `TestServe` and `TestProbe`) extended to assert `schema_version==1`, `ok is False`, `error=="runtime_config_error"` |
| tests/runtimes/test_runtime_cli_process_boundary.py | +1/-1 | `test_an_application_that_dies_before_readiness_is_a_start_failure`: `"exited before readiness" in out["error"]` → `out["message"]` |
| tests/runtimes/test_runtime_lifecycle_safety.py | +1/-1 | `test_serve_blocks_when_a_different_runtime_is_running`: `"runtime_spec_mismatch" in out["error"]` → `out["message"]` |
| tests/runtimes/test_runtime_state_machine.py | +1/-1 | `test_a_changed_config_blocks_a_second_serve` (4 parametrizations): same `error`→`message` repair |
| tests/runtimes/test_supervisor_portability.py | +4/-4 | four assertions reading the old sentence out of `error` (`"no verified running state"`, `"different runtime instance"`, twice negated) repaired to read `message` |

Measured insertions: **194** (124+37+26+1+1+1+4); 119 deletions.

### 77b36204 F283 R13 C4: runtime result-shaped failures answer one envelope under --json
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/runtime_cmd.py | +30/-8 | `emit_error` imported; the four D8 result-shaped exits (probe cleanup survivors, probe readiness, served-runtime health check, `stop`) each gain an `if <ok>: print(raw payload) else: emit_error(<token>, <message>, **rest-of-payload-minus-ok/error)` branch under `--json`; text branches and exit codes byte-for-byte unchanged; module docstring gains a paragraph naming the four exits and the envelope rule |
| tests/cli/test_runtime_cmd.py | +29/-0 | `test_a_probe_timeout_exits_4` extended: `out["error"]=="runtime_not_ready"`, `out["error_class"]=="ready"`; new sibling `test_stop_answers_the_envelope_when_identity_cannot_be_trusted` (a project-digest mismatch, `ok=False`, exit 5, `runtime_state_error`) — `test_stop_never_kills_a_reused_pid` itself never reaches this exit (its reused-pid record auto-clears, `ok` stays True) |

Measured insertions: **59** (30+29); 8 deletions.

### C5 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot
table the commit that writes it.

## External actions

- `git worktree add .remedy-wt/f283-r13-redproof 77b36204` for G5 — used for
  the unmutated control and all four mutation red-proofs, each reverted with
  the file tool and confirmed clean with `diff` against the primary
  checkout's committed file before the next — then `git worktree remove
  --force .remedy-wt/f283-r13-redproof`.
- `git push origin feature/f283-machine-contracts-part-two` after C5 — real
  outcome reported in the session reply, since it ships this very file.
- `gh pr list --state open ...` after the push — real outcome reported in the
  session reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no `gh pr create`, no checkout of
  `main`, no branch deletion.
- No worktree other than the one disposable G5 worktree above (removed) was
  added. The three `remedy/job-*` worktrees were left alone throughout.

## Verification

### G1 — PAYLOADS transport, then four authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| decisions.md | 33/33 | 2560/2560 | True |
| ledger.md | 2/2 | 3391/3391 | True |
| plan.md | 33/33 | 1311/1311 | True |

**All readings equal: True.**

Four `.agent/authored/f283-r13-*` copies (the block copy plus three payloads),
each read back from the committed tree with `git show e8a1e6b8:<path>` and
compared byte-for-byte (sha256) with its source:

| copy | sha256 equal to source |
|---|---|
| f283-r13-block.md | True |
| f283-r13-decisions.md | True |
| f283-r13-ledger.md | True |
| f283-r13-plan.md | True |

**Copies compared: 4. All True.**

### G2 — THE BOOKING

**(a) Append arithmetic**, by strict byte concatenation:

| file | pre (`2ac999da`) | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 504225 | 3391 | 507616 | True |
| .agent/decisions.md | 1806637 | 2560 | 1809197 | True |

Matches the reviewer's stated compositions (504225+ledger.md=507616,
1806637+decisions.md=1809197) exactly.

**(b) Line-anchored on the committed ledger**: `^Gate: F283 R12 — ` = **1**.
Open set by distinct id, via `open_finding_ids` from
`scripts/rotate_live_review.py` (imported and called directly):

| rev | OPEN by distinct id |
|---|---|
| `2ac999da` | **22** |
| C2 (`c38cab8a`) | **22** |

Added: `[]`. Removed: `[]`. Matches the reviewer's stated 22 → 22, ADDED empty,
REMOVED empty, exactly.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**: sha256-equal to the
payload (`b755761d22094dc38d0d150954fa67fe14425cd58f7cccd5bb92a72e974a2195`
both).

Line count: **33**, under the AGENTS.md 50-line rule.

### G3 — THE CHANGE, COUNTED FROM THE TREE

`git diff --name-only <parent> <commit>` and `git show --numstat` insertions:

| commit | paths changed | insertions |
|---|---|---|
| C3 `c38cab8a`→`aa42e451` | apps/cli/commands/runtime_cmd.py, tests/cli/test_job_refusal_envelope.py, tests/cli/test_runtime_cmd.py, tests/runtimes/test_runtime_cli_process_boundary.py, tests/runtimes/test_runtime_lifecycle_safety.py, tests/runtimes/test_runtime_state_machine.py, tests/runtimes/test_supervisor_portability.py | 194 |
| C4 `aa42e451`→`77b36204` | apps/cli/commands/runtime_cmd.py, tests/cli/test_runtime_cmd.py | 59 |

Lines holding `_fail(` in `runtime_cmd.py`: **0** at both C3 and C4 (baseline
at `2ac999da` was **27**, definition included — matches the block's stated
target of 0 by C4). Lines holding `_runtime_refusal(` at C4: **28** (1 module
docstring mention + the 1-line def + 26 call sites).

`python3 .remedy-wt/f283-r6-scratch/pairs.py runtime_cmd.py`:

| when | summary |
|---|---|
| baseline `2ac999da` | `exits 5 mechanical 0` |
| after C3 | `exits 4 mechanical 0` |
| after C4 | `exits 4 mechanical 0` |

The drop from 5 to 4 is `_fail`'s own `sys.exit(code)` line disappearing with
the function; the remaining 4 are the D8 result-shaped exits' manual
`sys.exit(...)` calls, unchanged by C4 (their shape gains an envelope, their
`sys.exit` sites do not move) and never "mechanical" by the AST rule (each
`sys.exit`'s immediate predecessor is an `if`/`else` compound, never a bare
`print(..., file=sys.stderr)`).

`git diff --name-only 2ac999da 77b36204 -- packages/` prints **nothing** (real
exit code implicit 0, empty stdout) — confirmed `packages/` untouched across
the whole round.

### Token list — every token C3 and C4 use, confirmed absent before its introducing commit

| commit | token | error_class | confirmed absent (`git grep 'fail("<token>"' <parent> -- apps/cli/`) |
|---|---|---|---|
| C3 | runtime_config_error | config | 0 hits at `c38cab8a` |
| C3 | runtime_start_failed | start | 0 hits at `c38cab8a` |
| C3 | runtime_not_ready | ready | 0 hits at `c38cab8a` |
| C3 | runtime_handshake_timeout | handshake | 0 hits at `c38cab8a` |
| C3 | runtime_state_error | state | 0 hits at `c38cab8a` |
| C3 | runtime_lock_busy | lock | 0 hits at `c38cab8a` |
| C3 | runtime_stop_failed | stop | 0 hits at `c38cab8a` |
| C3 | runtime_error | (fallback, unnamed class) | 0 hits at `c38cab8a` |

All 8 are new as `fail()` tokens; none reused from another module. C4 emits
the same 4 of these 8 (`runtime_stop_failed`, `runtime_not_ready`,
`runtime_state_error`, plus whichever the probe's dynamic `error_class`
resolves to) through `emit_error()` directly rather than through
`_runtime_refusal`, using the same `RUNTIME_ERROR_TOKENS` table — no new
token is introduced at C4.

### G4 — TARGETED SELECTION, ruff, integrity

`.remedy-wt/f283-r13-scratch/selection.txt`: **109** space-separated paths
(round 12's selection minus `tests/docs/`, `tests/cli/test_runtime_cmd.py`
added, `tests/docs/` appended back, the 5 `tests/runtimes/` files removed
into selection_serial.txt — pre-built by the reviewer). `selection_serial.txt`:
the 5 `tests/runtimes/` paths, run serially (`test_supervisor_portability.py`
flakes under xdist).

| when | selection | exit code | summary |
|---|---|---|---|
| after C3 | A (`-n auto`) | 0 | 4570 passed, 1 skipped |
| after C3 | B (serial) | 0 | 204 passed |
| after C4 | A (`-n auto`) | 0 | 4571 passed, 1 skipped |
| after C4 | B (serial) | 0 | 204 passed |

Zero failed, zero errors at each; the reviewer read `4565 passed, 1 skipped`
(A) and `204 passed` (B) at `2ac999da` — the passed count only rose (+5 at C3
from 5 new tests, +1 at C4 from 1 new test; B unchanged, no new tests added to
the four `tests/runtimes/` files this round, only assertion repairs).

`python3 -m ruff check` over every `.py` path the round touched
(`apps/cli/commands/runtime_cmd.py`, `tests/cli/test_runtime_cmd.py`,
`tests/cli/test_job_refusal_envelope.py`,
`tests/runtimes/test_runtime_cli_process_boundary.py`,
`tests/runtimes/test_runtime_lifecycle_safety.py`,
`tests/runtimes/test_runtime_state_machine.py`,
`tests/runtimes/test_supervisor_portability.py`), run after C4: **All checks
passed!**

`python3 -m apps.cli.main integrity check --json`, run after C4: `"passed":
true, "fail_count": 0`, all five checks (`handler_import`,
`live_review_verdict`, `plan_consistency`, `relevant_untracked`,
`high_blockers_open`) read `"status": "pass"`.

### G5 — RED-PROOFS

Disposable worktree `.remedy-wt/f283-r13-redproof` at `77b36204` (C4), never
committed. Ran `tests/cli/test_runtime_cmd.py` and
`tests/cli/test_job_refusal_envelope.py` unmutated first, then each mutation
alone over those two files, reverted with the file tool before the next
(confirmed identical to the primary checkout's committed file with `diff`
after each revert):

| step | exit code | result | failing tests |
|---|---|---|---|
| unmutated control | 0 | 98 passed | — |
| (a) `RUNTIME_ERROR_TOKENS["config"]` changed to `"runtime_config_error_MUTATED"` | 1 | 2 failed, 96 passed | `TestServe::test_a_missing_runtime_exits_2`, `TestProbe::test_a_missing_runtime_exits_2` |
| (b) `_runtime_refusal` stops passing `error_class` to `fail()` | 1 | 3 failed, 95 passed | `TestServe::test_a_readiness_timeout_exits_4_and_leaves_no_state`, `TestServe::test_a_missing_runtime_exits_2`, `TestProbe::test_a_missing_runtime_exits_2` |
| (c) the one-shot probe's not-ready branch forced to `if False:` (never takes the `--json` path) | 1 | 3 failed, 95 passed | `TestProbe::test_a_one_shot_probe_starts_stops_and_leaves_nothing`, `TestProbe::test_a_second_probe_runs_cleanly`, `TestProbe::test_a_probe_timeout_exits_4` |
| (d) `stop`'s failure envelope class swapped (`"stop"/"state"` → `"lock"/"config"`) | 1 | 1 failed, 97 passed | `TestStop::test_stop_answers_the_envelope_when_identity_cannot_be_trusted` |

Mutation (c)'s three failures include two tests beyond the named probe-timeout
target (`test_a_one_shot_probe_starts_stops_and_leaves_nothing`,
`test_a_second_probe_runs_cleanly`) — forcing `if False:` also breaks the
SUCCESS path's `--json` print at that same site, since the mutated condition
guards both the success and failure branches; `test_a_probe_timeout_exits_4`,
the block's named target, is confirmed among the three. Each mutation was
reverted and confirmed byte-identical to the primary checkout's committed
file (`diff`, no output) before the next. `git worktree remove --force
.remedy-wt/f283-r13-redproof` afterward. `git worktree list` (post-removal):
the primary checkout at `77b36204` plus the three `remedy/job-*` worktrees —
`.remedy-wt/job-468c8e62a2cc4fac`, `.remedy-wt/job-86f628f5e4fb4e0c`,
`.remedy-wt/job-c1dba9c3d7874968` — untouched throughout.

## Deviations & assumptions

1. **Mutation (c)'s red-proof reddened three tests, not one.** The block names
   `test_a_probe_timeout_exits_4` as the target; the mutation forces the
   shared `if json_output:` guard covering BOTH the probe's success print and
   its failure envelope to `if False:`, so two success-path tests
   (`test_a_one_shot_probe_starts_stops_and_leaves_nothing`,
   `test_a_second_probe_runs_cleanly`) also lose their JSON output and fail on
   `json.loads("")`. The named target is confirmed among the three failures;
   this is reported rather than narrowed to a single-test mutation, since a
   mutation isolated to only the `else` (not-ok) sub-branch would not
   faithfully exercise "the one-shot probe's not-ready failure passes
   `json_output=False`" as stated.
2. **`test_a_probe_timeout_exits_4` was extended in place, not given a
   sibling**, for the probe envelope assertion; `stop`'s envelope assertion
   uses a NEW sibling (`test_stop_answers_the_envelope_when_identity_cannot_be_trusted`)
   because `test_stop_never_kills_a_reused_pid` itself never reaches the
   `ok=False` exit path (its reused-pid record classifies as `OWNER_GONE` and
   clears automatically, `ok` stays `True`, nothing exits) — both satisfy the
   block's "`<test>` or a sibling" phrasing.
3. **`RUNTIME_ERROR_TOKENS` distinctness/coverage is proved by two tests**
   (`TestRuntimeErrorTokens.test_every_token_is_distinct`,
   `test_every_class_the_module_passes_is_a_key`), not the "one test" the
   block's prose suggests; both together are the single check the block
   describes, split for one assertion per test per this repo's existing
   convention (every other ratchet class in `test_job_refusal_envelope.py`
   follows the same one-assertion-per-test shape).
4. **Constraints 1, 2, 3, 4, 6 and 7 held throughout.** No payload was edited
   or retyped; every commit stayed under 500 insertions (258, 45, 194, 59;
   this handoff exempt as a single `.agent/**` state file); the round's
   tracked path set (14 distinct paths before this commit, 15 after) is a
   SUBSET of constraint 3's enumeration (the omitted allowed path is
   `tests/runtimes/test_apps_ui_probe.py`, which needed no repair — it never
   reads `runtime_cmd.py`'s failure shape); `packages/` was never touched;
   every commit from C3 on left both G4 selections at zero failed; nothing was
   merged, no PR created, no checkout of `main`; the one G5 worktree was
   removed as its own last action and the three `remedy/job-*` worktrees were
   left alone.

### The round's whole tracked path set (before this commit)

`git diff --name-only 2ac999da 77b36204` — **14** distinct paths
(`runtime_cmd.py` touched by C3 and C4; `test_runtime_cmd.py` touched by C3
and C4 — each counted once); plus `.agent/handoff.md` from this commit makes
**15** — a SUBSET of constraint 3's enumeration:

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r13-block.md | C1 `e8a1e6b8` |
| 2 | .agent/authored/f283-r13-decisions.md | C1 `e8a1e6b8` |
| 3 | .agent/authored/f283-r13-ledger.md | C1 `e8a1e6b8` |
| 4 | .agent/authored/f283-r13-plan.md | C1 `e8a1e6b8` |
| 5 | .agent/decisions.md | C2 `c38cab8a` |
| 6 | .agent/live_review.md | C2 `c38cab8a` |
| 7 | .agent/plan.md | C2 `c38cab8a` |
| 8 | apps/cli/commands/runtime_cmd.py | C3 `aa42e451`, touched again by C4 `77b36204` |
| 9 | tests/cli/test_job_refusal_envelope.py | C3 `aa42e451` |
| 10 | tests/cli/test_runtime_cmd.py | C3 `aa42e451`, touched again by C4 `77b36204` |
| 11 | tests/runtimes/test_runtime_cli_process_boundary.py | C3 `aa42e451` |
| 12 | tests/runtimes/test_runtime_lifecycle_safety.py | C3 `aa42e451` |
| 13 | tests/runtimes/test_runtime_state_machine.py | C3 `aa42e451` |
| 14 | tests/runtimes/test_supervisor_portability.py | C3 `aa42e451` |
| 15 | .agent/handoff.md | C5 (this commit) |

No path outside constraint 3's enumeration was touched: `.agent/candidates.md`,
`.agent/context.md`, `.agent/operator_questions.md`, `.agent/prose_slips.md`,
`README.md`, `docs/roadmap/**`, `scripts/**` and `apps/cli/json_envelope.py`
appear **0** times. `packages/` appears **0** times (confirmed above under
G3). `tests/runtimes/test_apps_ui_probe.py`, allowed but unneeded, appears
**0** times.

## Authored-text proofs

- The four copies at C1, compared with the reviewer's originals under
  `.remedy-wt/f283-r13-payloads/` and `.remedy-wt/f283-r13-block.md`: **four
  readings, all True** (G1).
- The two APPEND payloads against their committed files: strict byte
  concatenation True for `.agent/live_review.md` (ledger.md) and
  `.agent/decisions.md` (decisions.md), byte numbers equal to the reviewer's
  (G2a).
- The one REWRITE payload against its committed file: `.agent/plan.md`'s
  committed sha256 equals the payload's sha256 (G2c).
- No payload was edited or retyped. All four `.agent/authored/` copies were
  made with `shutil.copyfile`; the two appends by reading each payload's bytes
  and writing base+payload back to disk; the plan.md rewrite by
  `shutil.copyfile`.
- Every change under `apps/` and `tests/` this round was WORKER-authored to
  the block's SPEC and DECISION F283 D8 — there is no reviewer-authored diff
  to compare against for those files; G3/G4/G5 above are the proof they meet
  the SPEC.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `2ac999da`; block 190 lines / matching sha256 |
| C1 copy block + 3 payloads | done | 258 insertions |
| C2 book round 12 PASS, record D8 | done | 45 insertions (33+2+10, 10 deletions from plan rewrite); open set 22→22, added/removed empty |
| C3 runtime refusals answer through fail(), keyed on error_class (D8) | done | 194 insertions; `_fail` deleted, 26 call sites converted, `_fail(` count 27→0; 8 new tokens, all confirmed absent before this commit |
| C4 runtime result-shaped failures answer one envelope under --json | done | 59 insertions; four D8-named exits gain the envelope under `--json`, text/exit codes byte-for-byte unchanged |
| C5 the handback | done | this commit |
| G1 payload transport + authored copies | done | 3/3 payload readings equal; 4/4 authored copies byte-identical |
| G2(a) live_review.md + decisions.md append | done | 504225+3391=507616; 1806637+2560=1809197 |
| G2(b) open set by distinct id | done | 1 Gate line; 22→22, added none, removed none |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 33 lines, under 50 |
| G3 change counted from the tree | done | per-commit diffs and insertions reported; `_fail(` 27→0; pairs.py exits 5→4→4, mechanical 0 throughout; 0 paths under `packages/` |
| G4 targeted selection, ruff, integrity | done | 4570/4571 passed (A), 204/204 passed (B), 0 failed/errors at each (A up from 4565); ruff exit 0; integrity all 5 pass, fail_count 0 |
| G5 red-proofs (a)(b)(c)(d) | done | all four go RED, each reddening its named target test (mutation (c) also reddens two success-path siblings — see Deviations item 1); unmutated control 98 passed |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile`, byte concatenation only |
| Constraint 2 every commit under 500 insertions | done | 258, 45, 194, 59; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 14 paths before this commit (15 after), a SUBSET of the enumeration (only `test_apps_ui_probe.py` unused) |
| Constraint 4 G4 selection at zero failed after every commit | done | 4570/4571 passed (A), 204/204 (B), 0 failed/errors at each |
| Constraint 5 STOP if a gate goes red outside constraint 3's path set | done (n/a) | no gate went red outside the named paths; no STOP was needed |
| Constraint 6 nothing is merged | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion |
| Constraint 7 G5 worktree under .remedy-wt/, removed, listed | done | `.remedy-wt/f283-r13-redproof`, removed, `git worktree list` reported after; the three `remedy/job-*` worktrees untouched |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 13 — C1 through C5, all six gates re-derived.
3. Then T001's catalog half as `.agent/plan.md` lists it: the read-only
   commands without `supports_json`, and the catalog test asserting that set
   is empty.

Open findings count: **22**. Operator-questions count: **2**.
