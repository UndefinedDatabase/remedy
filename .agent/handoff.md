# Handoff — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 16 · T001's catalog half, last group (D9)

## Session

SESSION 4 of feature F283 · round 16 · rounds so far 16

This round booked round 15's PASS and a prose slip, then narrowed the
`answered` envelope's `next_command` to the bare command (round 15 had put
the whole printed line, prose prefix included, into that key — a prose
slip, now booked) while pinning the derived-decision refusal's text branch
with a new test. Then, the catalog half's LAST group under DECISION F283
D9: the five `project` create and attach commands declared `supports_json`
(`create` → `project_id`/`name`/`slug`; `attach-repo` → `project_id`/`repo`/
`changed`; `attach-job` → `project_id`/`job_id`/`added`; `attach` →
`project_id`/`slug`/`old_repo`/`new_repo`/`changed`, its text branch still
printing the same raw document; `adopt` → `job_id`/`project_id`/`slug`), and
`_cmd_project_attach_repo`'s last unmigrated refusal site (the unprefixed
`ProjectNotFoundError`/`InvalidProjectSelectorError` branch) now answers the
same two tokens `_cmd_project_current` already does, shaped so the shared
`sys.exit(3)` sits AFTER the `if`/`else` rather than inside it — the
print-then-exit pair the AST ratchet counts vanishes rather than joining the
flagged set. Then the five `ui` commands declared `supports_json` (`latest`
→ `url`/`job_id`/`pid`; `status` → `sessions`/`dead`; `stop` →
`stopped`/`failed`; `open` → `url`/`job_id`; `latest`'s and `open`'s
no-session refusals answer `ui_session_not_found` in the same shared-exit
shape); `start_ui_server` gained `json_output`, imported `fail`/`emit_ok`
from `apps.cli.json_envelope` inside the function (this module lives under
`packages/` and must not import `apps/` at module scope), answers
`host_not_allowed` or `job_not_found`/`invalid_job_id` under `--json`, and
once bound prints one `emit_ok(...)` envelope and flushes stdout in place of
its two prose lines, then serves — text path, the localhost allow-list and
the `serve_forever` block are all unchanged. The ratchet's derived set is now
EMPTY and the ten-item pinned constant is deleted, per D9 (6). T001's catalog
half is complete.
Context self-assessment: roughly 35% of the working budget remained at the
point this handoff was written.

## Range

Review of `f6527092`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 232 | 232 | True |
| sha256 | `240786f262fd0926b6ab9a6ffc40f86377ad7274b0f4184c7de6b3b40846fdad` | `240786f262fd0926b6ab9a6ffc40f86377ad7274b0f4184c7de6b3b40846fdad` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `f6527092`, matching the delegation message.

## Commits

### 7d790742 F283 R16 C1: copy round 16 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r16-block.md | +232/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f283-r16-ledger.md | +2/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r16-plan.md | +34/-0 | byte-for-byte copy of plan.md |
| .agent/authored/f283-r16-slips.md | +1/-0 | byte-for-byte copy of slips.md |

Measured insertions (`git show --numstat`): **269** (232+2+34+1).

### f9fb9ccf F283 R16 C2: book round 15's PASS and a prose slip
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | append ledger.md by strict byte concatenation: round-15 `Gate:` entry |
| .agent/plan.md | +9/-10 | rewrite to plan.md payload, byte-identical; git's line diff shows only the lines that changed |
| .agent/prose_slips.md | +1/-0 | append slips.md: one dated prose-slip line |

Measured insertions: **12** (2+9+1); 10 deletions from the plan.md rewrite.

### fd54e1df F283 R16 C3: pin the derived-decision text refusal; next_command is the command
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/decision.py | +2/-2 | `next_command` becomes `f"remedy job resume {job_id_str} --json"` (the bare command); the text branch's `print` gains the `Resume the run: ` prefix inline so its printed bytes are unchanged |
| tests/cli/test_decision_answers.py | +3/-2 | the `answered` envelope test now asserts `next_command == f"remedy job resume {job.job_id} --json"`; class docstring corrected to say "the command alone" |
| tests/cli/test_decision_cmd.py | +18/-0 | new `test_resolve_a_derived_decision_without_json_writes_its_two_old_stderr_lines`: `decision resolve` on a derived decision without `--json` writes exactly its two old stderr lines, byte-for-byte, and exits 1 |

Measured insertions: **23** (2+3+18); 4 deletions.

### 37467dd6 F283 R16 C4: the project create and attach commands answer --json in the envelope
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | +10/-2 | `project.create`, `project.attach-repo`, `project.attach-job`, `project.attach`, `project.adopt` each gain `_JSON_OPT` and `supports_json=True` |
| apps/cli/commands/project.py | +74/-27 | `_cmd_create_project`, `_cmd_attach_project_repo`, `_cmd_attach_project_job`, `_cmd_project_attach_repo`, `_cmd_project_adopt` each take `json_output`, threaded to every refusal; success under `--json` per the SPEC's key lists; `_cmd_project_attach_repo`'s `attach` text branch keeps printing the same raw `_json.dumps(...)` document; its unprefixed selector-exception branch reshapes onto `if json_output: fail(<token>, str(exc), json_output=True, exit_code=3) else: <the original print>` with the shared `sys.exit(3)` AFTER the `if`/`else` — same two tokens, same exit code, as `_cmd_project_current`'s identical branch |
| tests/cli/test_job_refusal_envelope.py | +10/-8 | `TestDecisionsRefusalsAreAllMigrated::test_exactly_one_unflagged_site_remains` renamed `test_no_unflagged_site_remains` (assertion already `unflagged == []`); `TestProjectRefusalsAreAllMigrated::test_exactly_one_unflagged_site_remains` renamed `test_no_unflagged_site_remains`, assertion now `unflagged == []`, class docstring corrected — the attach-repo site left the unflagged set without joining the flagged one, so the flagged count (1) is unchanged |
| tests/cli/test_project_current.py | +116/-0 | new `TestProjectCreateAndAttachAnswerJSONThroughTheDispatcher`: a success envelope per command (`create`, `attach-repo`, `attach-job`, `attach`, `adopt`) and the `attach` selector's `project_not_found` refusal envelope, all through the CLI dispatcher |
| tests/test_command_catalog.py | +3/-9 | ratchet constant loses the five `project.*` ids (10→5, exactly the `ui` group); docstring updated |

Measured insertions: **213** (10+74+10+116+3); 46 deletions.

### 75d9205b F283 R16 C5: the ui commands answer --json in the envelope; the read-only set is empty
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | +10/-3 | `ui.start`, `ui.latest`, `ui.status`, `ui.stop`, `ui.open` each gain `_JSON_OPT` and `supports_json=True` |
| apps/cli/commands/ui.py | +72/-17 | `_cmd_ui_start`, `_cmd_ui_latest`, `_cmd_ui_status`, `_cmd_ui_stop`, `_cmd_ui_open` each take `json_output`; success under `--json` per the SPEC's key lists (`status`'s `dead` is the archived list under `--all`, else empty; `stop`'s `failed` entries carry `error`); `latest`'s and `open`'s no-session refusals answer `ui_session_not_found` in the shared-exit-after shape; text branches, including the opener calls, unchanged |
| packages/orchestration/ui_server.py | +19/-6 | `start_ui_server` gains `json_output`, keyword-only, default `False`; imports `emit_ok`/`fail` from `apps.cli.json_envelope` INSIDE the function (module lives under `packages/`); host refusal answers `host_not_allowed`, job refusal answers `job_not_found` (404) or `invalid_job_id` (400); once bound, prints one `emit_ok(url=..., host=..., port=..., job_id=..., pid=..., info_file=...)` envelope and flushes stdout in place of its two prose lines, then serves; the localhost allow-list literal `("127.0.0.1", "localhost", "::1")` and the absence of `0.0.0.0` are unchanged |
| tests/test_command_catalog.py | +12/-23 | `TestReadOnlyWithoutSupportsJSONRatchet` rewritten: the pinned `_READ_ONLY_WITHOUT_SUPPORTS_JSON` constant is deleted; `test_the_derived_set_equals_the_pinned_constant` renamed `test_the_derived_set_is_empty`, asserting `derived == frozenset()` directly; class docstring rewritten to close out the D9 (6) sequence |
| tests/ui_server/test_live_state.py | +149/-0 | new `TestUISessionCommandsAnswerTheEnvelope` (success envelopes for `latest`, `status`, `status --all`, `stop`, `open`; `ui_session_not_found` refusal envelopes for `latest` and `open`; `stop`'s test mocks `os.kill`/`_is_pid_alive` rather than signalling a real PID) and `TestUIStartAnswersTheEnvelope` (`ui start --json` with `ThreadingHTTPServer.serve_forever` patched to return immediately and `_try_open_browser` mocked) |

Measured insertions: **262** (10+72+19+12+149); 49 deletions.

### C6 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot
table the commit that writes it.

## External actions

- `git worktree add .remedy-wt/f283-r16-redproof 75d9205b` for G5 — used for
  the unmutated control and all seven mutation red-proofs, each reverted with
  `git checkout --` before the next — then `git worktree remove
  .remedy-wt/f283-r16-redproof`.
- `git push origin feature/f283-machine-contracts-part-two` after C6 — real
  outcome reported in the session reply, since it ships this very file.
- `gh pr list --state open ...` after the push — real outcome reported in the
  session reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no `gh pr create`, no checkout of
  `main`, no branch deletion.
- No worktree other than the one disposable G5 worktree above was added; it
  was removed. No `remedy/job-*` worktree existed this round (`git worktree
  list` shows the primary checkout alone both before C1 and again here before
  C6).

## Verification

### G1 — PAYLOADS transport, then four authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| ledger.md | 2/2 | 3705/3705 | True |
| plan.md | 34/34 | 1442/1442 | True |
| slips.md | 1/1 | 504/504 | True |

**All readings equal: True.**

Four `.agent/authored/f283-r16-*` copies (the block copy plus three payloads),
each read back from the committed tree with `git show 7d790742:<path>` and
compared byte-for-byte with its source:

| copy | equal to source |
|---|---|
| f283-r16-block.md | True |
| f283-r16-ledger.md | True |
| f283-r16-plan.md | True |
| f283-r16-slips.md | True |

**Copies compared: 4. All True.**

### G2 — THE BOOKING

**(a) Append arithmetic**, by strict byte concatenation, pre-file read at
`f6527092`:

| file | pre | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 520781 | 3705 | 524486 | True |
| .agent/prose_slips.md | 362485 | 504 | 362989 | True |

Matches the block's stated compositions exactly.

**(b) Line-anchored on the committed ledger**: `^Gate: F283 R15 — ` = **1**.
Open set by distinct id, via `open_finding_ids` from
`scripts/rotate_live_review.py` (imported and called directly):

| rev | OPEN by distinct id |
|---|---|
| `f6527092` | **24** |
| C2 (`f9fb9ccf`) | **24** |

Added: `[]`. Removed: `[]`. Matches the block's stated 24 → 24, ADDED empty,
REMOVED empty, exactly.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**: sha256-equal to
the payload (`840a502b8cfb79fc0755a263563f05f32ada009d3bac7ecee2d3fb10ac6df424`
both). Line count: **34**, under the AGENTS.md 50-line rule.

### G3 — THE CHANGE, COUNTED FROM THE TREE

`git diff --name-only <parent> <commit>` and `git show --numstat` insertions:

| commit | paths changed | insertions |
|---|---|---|
| C3 `f9fb9ccf`→`fd54e1df` | apps/cli/commands/decision.py, tests/cli/test_decision_answers.py, tests/cli/test_decision_cmd.py | 23 |
| C4 `fd54e1df`→`37467dd6` | apps/cli/command_catalog.py, apps/cli/commands/project.py, tests/cli/test_job_refusal_envelope.py, tests/cli/test_project_current.py, tests/test_command_catalog.py | 213 |
| C5 `37467dd6`→`75d9205b` | apps/cli/command_catalog.py, apps/cli/commands/ui.py, packages/orchestration/ui_server.py, tests/test_command_catalog.py, tests/ui_server/test_live_state.py | 262 |

The derived set (D9's rule — neither `may_mutate_repo` nor `may_execute_commands`
nor `supports_json`, computed by importing `CATALOG` fresh in the primary
checkout right after each commit landed):

| commit | derived set |
|---|---|
| C4 `37467dd6` | **5**: `ui.latest`, `ui.open`, `ui.start`, `ui.status`, `ui.stop` — exactly the `ui` group |
| C5 `75d9205b` | **0** — EMPTY |

`python3 .remedy-wt/f283-r6-scratch/pairs.py project.py ui.py decision.py` at
`75d9205b` (C5):

| module | summary |
|---|---|
| project.py | `exits 2 mechanical 1 flagged 1 unflagged 0` |
| ui.py | `exits 2 mechanical 0 flagged 0 unflagged 0` |
| decision.py | `exits 1 mechanical 0 flagged 0 unflagged 0` |

Against the block's `f6527092` reading (`project.py exits 2 mechanical 2
flagged 1 unflagged 1`, `ui.py exits 2 mechanical 2 flagged 0 unflagged 2`,
`decision.py exits 1 mechanical 0 flagged 0 unflagged 0`): `project.py`'s
attach-repo site is unchanged in COUNT but no longer "mechanical" (mechanical
2→1, unflagged 1→0, flagged unchanged at 1) — it now sits behind an `if`/`else`
whose shared `sys.exit(3)` follows rather than a stderr print directly;
`ui.py`'s latest/open sites both lose their mechanical status the same way
(mechanical 2→0, unflagged 2→0); `decision.py` is byte-for-byte unchanged in
this reading, since round 15 already gave it the shared-exit shape.

`git diff --name-only f6527092 75d9205b -- packages/` prints
**`packages/orchestration/ui_server.py`** alone.

### Token list — every token this round's `fail(`/`emit_error(` calls introduce or reuse

Each token's `git grep -c '"<token>"' f6527092 -- apps/ packages/` count
(summed across files) at the round's base:

| token | introduced in | count at `f6527092` | new or reused |
|---|---|---|---|
| ui_session_not_found | ui.py | 0 | **new** |
| host_not_allowed | ui_server.py | 0 | **new** |
| invalid_job_id | ui_server.py | 4 | reused |
| job_not_found | project.py, ui_server.py | 47 | reused |
| project_not_found | project.py | 7 | reused |
| invalid_project_selector | project.py | 1 | reused |

`decision.py` introduces no new `fail()`/`emit_error()` call this round — C3
only narrows the string an existing `emit_ok(next_command=...)` keyword
carries, and the derived-decision refusal's `fail("decision_not_resolvable",
...)` call is unchanged from round 15. Two tokens are genuinely new at
`apps/`/`packages/` level: `ui_session_not_found` and `host_not_allowed` (0
hits each at `f6527092`). Every other token this round's diff touches
(`invalid_job_id`, `job_not_found`, `project_not_found`,
`invalid_project_selector`) already existed before this round.

### G4 — TARGETED SELECTION, ruff, integrity

`.remedy-wt/f283-r16-scratch/selection.txt`: **285** space-separated paths
(`-n auto`). The block's `f6527092` reading: `10983 passed, 13 skipped`, exit 0.

| when | exit code | summary |
|---|---|---|
| after C3 | 0 | 10984 passed, 13 skipped |
| after C4 | 0 | 10990 passed, 13 skipped |
| after C5 | 0 | 10998 passed, 13 skipped |

Zero failed, zero errors at each; the passed count only rose (+1 at C3, +6 at
C4, +8 at C5; skipped unchanged at 13 throughout).

`python3 -m ruff check` over every `.py` path the round touched
(`apps/cli/command_catalog.py`, `apps/cli/commands/decision.py`,
`apps/cli/commands/project.py`, `apps/cli/commands/ui.py`,
`packages/orchestration/ui_server.py`, `tests/cli/test_decision_answers.py`,
`tests/cli/test_decision_cmd.py`, `tests/cli/test_job_refusal_envelope.py`,
`tests/cli/test_project_current.py`, `tests/test_command_catalog.py`,
`tests/ui_server/test_live_state.py`), run after C5: **All checks passed!**

`python3 -m apps.cli.main integrity check --json`, run after C5: `"passed":
true, "fail_count": 0`, all five checks (`handler_import`,
`live_review_verdict`, `plan_consistency`, `relevant_untracked`,
`high_blockers_open`) read `"status": "pass"`.

`python3 -m pytest tests/cli/test_golden_path.py -q`, run once after C5:
**42 passed**, exit 0.

### G5 — RED-PROOFS

Disposable worktree `.remedy-wt/f283-r16-redproof` at `75d9205b` (C5), never
committed. Ran `tests/test_command_catalog.py`, `tests/cli/test_decision_cmd.py`,
`tests/cli/test_decision_answers.py`, `tests/cli/test_project_current.py`,
`tests/orchestration/test_project_resolution.py` and
`tests/ui_server/test_live_state.py` UNMUTATED first, then each mutation
alone, reverted with `git checkout --` before the next:

| step | exit code | result | failing tests |
|---|---|---|---|
| unmutated control | 0 | 279 passed | — |
| (a) `next_command` carries the `Resume the run: ` prefix again | 1 | 1 failed, 29 passed (file-scoped) | `TestDecisionResolveTaskAnswerAnswersJSONThroughTheDispatcher::test_answered_answers_the_envelope` |
| (b) the derived-decision text's first line is reworded | 1 | 1 failed, 12 passed (file-scoped) | `TestDecisionExplainAndResolveAnswerJSONThroughTheDispatcher::test_resolve_a_derived_decision_without_json_writes_its_two_old_stderr_lines` |
| (c) `project attach`'s selector refusal passes `json_output=False` | 1 | 1 failed, 28 passed (file-scoped) | `TestProjectCreateAndAttachAnswerJSONThroughTheDispatcher::test_attach_selector_refusal_answers_the_envelope` |
| (d) `project create --json` prints the bare id instead of the envelope | 1 | 1 failed, 28 passed (file-scoped) | `TestProjectCreateAndAttachAnswerJSONThroughTheDispatcher::test_create_answers_the_envelope` |
| (e) `ui latest`'s no-session refusal passes `json_output=False` | 1 | 1 failed, 54 passed (file-scoped) | `TestUISessionCommandsAnswerTheEnvelope::test_latest_no_session_answers_ui_session_not_found` |
| (f) `start_ui_server` prints its two prose lines even under `--json` | 1 | 1 failed, 54 passed (file-scoped) | `TestUIStartAnswersTheEnvelope::test_ui_start_json_answers_the_envelope` |
| (g) `ui.status`'s catalog entry drops `supports_json=True`, keeping its `--json` arg | 1 | 2 failed, 57 passed (file-scoped) | `TestReadOnlyWithoutSupportsJSONRatchet::test_the_derived_set_is_empty`, `TestReadOnlyWithoutSupportsJSONRatchet::test_every_command_carrying_json_declares_supports_json` |

Each mutation reddened exactly its named target(s) and nothing else. Each was
reverted with `git checkout --` and confirmed clean (`git status --porcelain`,
empty) before the next. `git worktree remove .remedy-wt/f283-r16-redproof`
afterward. `git worktree list` (post-removal): the primary checkout alone —
`/home/decodeux/Repos/remedy 75d9205b [feature/f283-machine-contracts-part-two]`.

## Deviations & assumptions

1. **No unordered commit this round.** C1 through C5 landed in the block's
   exact order with no fix-forward commit between them.
2. **`_cmd_project_attach_repo`'s and `_cmd_ui_latest`/`_cmd_ui_open`'s
   refusals use the shared-`sys.exit`-after-`if`/`else` shape**, not the
   `sys.exit` INSIDE the `else` shape `_cmd_project_current` already carries
   — both answer the same tokens at the same exit code under `--json` and
   print the same byte-for-byte text otherwise, but the AST refusal-site
   ratchet in `tests/cli/test_job_refusal_envelope.py` counts a "mechanical"
   print-then-exit pair only when a `sys.exit` sits DIRECTLY after a stderr
   print in the same body; the shared-after shape (already round 15's pattern
   for `decision.py`'s derived-decision refusal) makes the ratchet stop
   counting the site at all, which is why C4's `project.py` flagged count
   stays at 1 rather than rising to 2, and why C5's `ui.py` mechanical count
   drops to 0. This is the block's own D7 shape as stated in its second
   paragraph, applied consistently across all three modules this round
   touches.
3. **`_cmd_ui_stop`'s new test mocks `os.kill` and `_is_pid_alive`** rather
   than exercising a real PID, because the handler's live path sends
   `SIGTERM` to whatever PID a session file names — using the test process's
   own PID (as an unguarded `os.getpid()` default would) would have
   terminated the test runner. `apps.cli.commands.ui.os.kill` is patched with
   a `MagicMock` and `_is_pid_alive` with a `lambda pid: True`, so the
   envelope's `stopped` entry is asserted without ever signalling a real
   process — no test here launches a real browser, opener or blocking
   server, per the block's guardrail; the same care extends to `latest`'s and
   `open`'s browser-open calls, which are mocked via
   `packages.orchestration.ui_server._try_open_browser` in every test that
   reaches them, and to `ui start --json`'s test, which patches
   `http.server.ThreadingHTTPServer.serve_forever` to return immediately.
4. **Constraints 1, 2, 3, 4, 6 and 7 held throughout.** No payload was edited
   or retyped; every commit stayed under 500 insertions (269, 12, 23, 213,
   262; this handoff exempt as a single `.agent/**` state file); the round's
   tracked path set (18 distinct paths before this commit, 19 after) is
   EXACTLY constraint 3's full enumeration, with nothing outside it and
   nothing missing; `packages/` shows exactly the one file the block predicts
   (`packages/orchestration/ui_server.py`); every commit from C3 on left
   selection A at zero failed and zero errors, the passed count only rising;
   nothing was merged, no PR created, no checkout of `main`; the one G5
   worktree was removed as its own last action.

### The round's whole tracked path set (before this commit)

`git diff --name-only f6527092 75d9205b` — **18** distinct paths
(`apps/cli/command_catalog.py` touched by C4 and C5;
`tests/test_command_catalog.py` touched by C4 and C5 — each counted once);
plus `.agent/handoff.md` from this commit makes **19** — EXACTLY constraint
3's full enumeration:

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r16-block.md | C1 `7d790742` |
| 2 | .agent/authored/f283-r16-ledger.md | C1 `7d790742` |
| 3 | .agent/authored/f283-r16-plan.md | C1 `7d790742` |
| 4 | .agent/authored/f283-r16-slips.md | C1 `7d790742` |
| 5 | .agent/live_review.md | C2 `f9fb9ccf` |
| 6 | .agent/plan.md | C2 `f9fb9ccf` |
| 7 | .agent/prose_slips.md | C2 `f9fb9ccf` |
| 8 | apps/cli/commands/decision.py | C3 `fd54e1df` |
| 9 | tests/cli/test_decision_answers.py | C3 `fd54e1df` |
| 10 | tests/cli/test_decision_cmd.py | C3 `fd54e1df` |
| 11 | apps/cli/command_catalog.py | C4 `37467dd6`, touched again by C5 `75d9205b` |
| 12 | apps/cli/commands/project.py | C4 `37467dd6` |
| 13 | tests/cli/test_job_refusal_envelope.py | C4 `37467dd6` |
| 14 | tests/cli/test_project_current.py | C4 `37467dd6` |
| 15 | tests/test_command_catalog.py | C4 `37467dd6`, touched again by C5 `75d9205b` |
| 16 | apps/cli/commands/ui.py | C5 `75d9205b` |
| 17 | packages/orchestration/ui_server.py | C5 `75d9205b` |
| 18 | tests/ui_server/test_live_state.py | C5 `75d9205b` |
| 19 | .agent/handoff.md | C6 (this commit) |

No path outside constraint 3's enumeration was touched: `.agent/candidates.md`,
`.agent/context.md`, `.agent/operator_questions.md`, `.agent/decisions.md`,
`README.md`, `docs/roadmap/**`, `scripts/**`, `apps/cli/json_envelope.py` and
`apps/cli/grouped.py` appear **0** times.
`tests/orchestration/test_project_resolution.py`, though inside constraint
3's allowed set, was not needed this round — the five `project` envelope
tests landed in `tests/cli/test_project_current.py` instead, which the block
names as the other of the two acceptable locations.

## Authored-text proofs

- The four copies at C1, compared with the block's originals under
  `.remedy-wt/f283-r16-payloads/` and `.remedy-wt/f283-r16-block.md`: **four
  readings, all True** (G1).
- The two APPEND payloads against their committed files: strict byte
  concatenation True for `.agent/live_review.md` (ledger.md) and
  `.agent/prose_slips.md` (slips.md), byte numbers equal to the block's (G2a).
- The one REWRITE payload against its committed file: `.agent/plan.md`'s
  committed sha256 equals the payload's sha256 (G2c).
- No payload was edited or retyped. The block copy and three payload copies
  were made with `shutil.copyfile`; the two appends by reading each payload's
  bytes and writing base+payload back to disk; the plan.md rewrite by
  `shutil.copyfile`.
- Every change under `apps/`, `packages/` and `tests/` this round was
  WORKER-authored to the block's SPEC and DECISIONs F283 D9/D7 — there is no
  reviewer-authored diff to compare against for those files; G3/G4/G5 above
  are the proof they meet the SPEC.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `f6527092`; block 232 lines / matching sha256 |
| C1 copy block + 3 payloads | done | 269 insertions |
| C2 book round 15 PASS and a prose slip | done | 12 insertions (2+9+1, 10 deletions from plan rewrite); open set 24→24, added/removed empty |
| C3 pin the derived-decision text refusal; next_command narrowed | done | 23 insertions, 4 deletions |
| C4 the project create and attach commands answer --json | done | 213 insertions; derived set 5 (exactly `ui.*`) |
| C5 the ui commands answer --json; read-only set empty | done | 262 insertions; derived set 0 |
| C6 the handback | done | this commit |
| G1 payload transport + authored copies | done | 3/3 payload readings equal; 4/4 authored copies byte-identical |
| G2(a) live_review.md + prose_slips.md append | done | 520781+3705=524486; 362485+504=362989 |
| G2(b) open set by distinct id | done | 1 Gate line; 24→24, added none, removed none |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 34 lines, under 50 |
| G3 change counted from the tree | done | per-commit diffs and insertions reported; derived set 5→0; pairs.py project.py/ui.py/decision.py: sites lose mechanical status rather than moving flagged↔unflagged; exactly 1 path under `packages/` |
| Token list | done | `ui_session_not_found` and `host_not_allowed` are new (0 hits at base); 4 other touched tokens reused |
| G4 targeted selection, ruff, integrity, golden path | done | 10984/10990/10998 passed after C3/C4/C5 (up from 10983), 0 failed/errors at each; ruff exit 0; integrity all 5 pass, fail_count 0; golden path 42 passed |
| G5 red-proofs (a)(b)(c)(d)(e)(f)(g) | done | all seven go RED, each reddening exactly its named target(s); unmutated control 279 passed |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile`, byte concatenation only |
| Constraint 2 every commit under 500 insertions | done | 269, 12, 23, 213, 262; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 18 paths before this commit (19 after), EXACTLY the full enumeration |
| Constraint 4 G4 selection at zero failed after every commit | done | 10984/10990/10998 passed, 0 failed/errors at each |
| Constraint 5 STOP if a gate goes red outside constraint 3's path set | done (n/a) | no gate went red outside the named paths; no STOP was needed |
| Constraint 6 nothing is merged | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion |
| Constraint 7 G5 worktree under .remedy-wt/, removed, listed | done | `.remedy-wt/f283-r16-redproof`, removed, `git worktree list` reported after; no other worktree disturbed |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 16 — C1 through C6, all six gates re-derived.
3. Then T002, as `.agent/plan.md` lists it: success envelopes for the
   `supports_json` commands that still print a raw document, the exit-code
   taxonomy under `docs/guides/`, and `tests/cli/test_json_contract.py`'s
   sweep.

Open findings count: **24**. Operator-questions count: **0**.
