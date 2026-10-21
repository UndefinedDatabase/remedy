# Handback — F303 round 3: book round 2, DECISION F303 D3, and the note route landed

## Session

SESSION 1 of feature F303 · round 3 · rounds so far 3

Context self-assessment: this worker verified every prepared digest, byte-copied the five C1
files, then implemented the note route exactly as DECISION F303 D3 resolved round 2's stop
(`positional_body`, the widened guard, `job.steer` as a client operation, the `api` channel and
`note_open`), wrote and ran every test the block named plus the ones the client-interface's own
static readers and the matrix demanded, regenerated every generated artifact, and closed all six
gates green, with ample context margin left.

Fortschritt: ~45 % (note route landed · MCP facet open) — Schätzung

## Range

Review of `8ee55fd5b`..`HEAD` on `feature/f303-face-public-api`.

## Commits

### 78f766a85 F303 R3 C1: book round 2, DECISION F303 D3, a prose slip and the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f303-r3.md` | 158/0 | this round's block, byte copy (158 lines, sha256 `c308a699d962609881bb28076a8de4a7bf44e7c0f045e95096b6be1610153fc3`, equal to `block.md`) |
| `.agent/decisions.md` | 13/0 | DECISION F303 D3 appended (prepared file, byte copy) |
| `.agent/live_review.md` | 2/0 | prepared file, byte copy |
| `.agent/plan.md` | 7/16 | rewritten for F303 round 3 (prepared file, byte copy) |
| `.agent/prose_slips.md` | 1/0 | prepared file, byte copy |

### 8d5bc53c3 F303 R3 C2: the note route, the api channel, job steer --source, the client operation and note_open
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/steering.py` | 3/2 | `STEERING_CHANNELS` gains `api` |
| `apps/cli/command_catalog_steer.py` | 3/1 | `--source` option added after `--task`; docstring tense fixed |
| `apps/cli/commands/job_steer_cmd.py` | 32/9 | `--source` validated before the job id resolves; `JOB_STEER_ANSWER_KEYS`, `JOB_STEER_ANSWER_TREE`, `JOB_STEER_REFUSAL_TOKENS` defined; docstring and handler updated |
| `apps/cli/client_interface.py` | 11/5 | imports the three constants; `job.steer` added to `CLIENT_OPERATION_IDS` and the three tables; `CLIENT_INTERFACE_VERSION` → `1.25` |
| `packages/orchestration/public_api_routes.py` | 27/0 | `PublicApiRoute.positional_body` field; the note route |
| `packages/orchestration/public_api_writes.py` | 10/0 | `_job_steer_argv`; `_TWIN_ARGV["job.steer"]` |
| `packages/orchestration/public_api.py` | 3/2 | `PUBLIC_API_VERSION` → `1.25`; version-history comment |
| `packages/orchestration/client_story.py` | 17/3 | `_note_open(plan)`; `note_open` reads it; docstring |
| `docs/system/public-http-api-v1.md` | 2/1 | generated section regenerated (`write_public_api_page`) |
| `docs/system/machine-client-contract-v1.md` | 19/1 | generated section regenerated (`write_client_interface_page`) |
| `docs/system/api-release-matrix-v1.json` | 19/2 | `current` → `1.25`; a `1.25` version entry; the note route in `inventory.routes` |
| `docs/system/client-answers-v1/*.json` (5 files) | 1/1 each | regenerated via `scripts/record_client_answers.py`; `client-story-working.json`'s `note_open` is now `true`, the other four only their type-checked `host`/timestamp fields moved |

### fac095d3c F303 R3 C3: tests of the note route, the positional body key, the api channel and note_open
| Path | +/- | Reason |
|---|---|---|
| `tests/ui_server/test_public_api.py` | 195/9 | `test_every_route_is_well_formed` widened for `positional_body`; `test_only_the_note_route_sets_a_positional_body_key`; `PINNED_ROUTES` entry; `test_the_note_route_is_pinned_with_its_body_and_its_statuses`; `test_the_note_route_takes_a_steering_note_for_one_task` (real `CommandRunner` over a bare TCP handler and the socket handler); `test_a_client_note_for_a_job_of_another_project_through_the_socket_handler_runs_nothing`; every `PUBLIC_API_VERSION == "1.24"` → `"1.25"` (8 sites); the story test's `note_open is False` → `is True` (the fixture job is queued with a pending task) |
| `tests/cli/test_client_interface.py` | 19/1 | `JOB_STEER_ANSWER_KEYS` import; `UNRESOLVED_TOKEN_SITES` and `UNRESOLVED_ANSWER_SITES` entries for `_cmd_job_steer`'s dynamic `code` and `**result` sites; the version pin → `"1.25"` |
| `tests/cli/test_job_steer.py` | 38/0 | `TestSteerSource`: `--source api` records channel `api`; an unknown `--source` exits 2 `invalid_argument` and writes nothing; the default records `cli` |
| `tests/orchestration/test_client_story.py` | 46/2 | three `note_open` tests (true/running+pending, false/completed, false/running+all-done); the shared `_story()` helper's blanket `note_open is False` replaced with a cross-check computed from the plan's own state and task statuses |

### b9fd64776 F303 R3 C4: the steering note in the guides and the face's inventory
| Path | +/- | Reason |
|---|---|---|
| `docs/guides/steering-user-guide-v1.md` | 12/0 | new "From a client, over the public API" section: the route, `--source`, `note_open` |
| `docs/roadmap/design/face-v1.md` | 1/1 | Steering note row: the route, "built by F303" |
| `docs/system/public-http-api-v1.md` | 3/2 | hand-written `note_open` sentence rewritten to what it now reads |

### (this commit) F303 R3 C5: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | rewritten | Current Step and Next Steps now name round 4 (the MCP facet) |
| `.agent/handoff.md` | rewritten | this handback |

## External actions

- `git push origin feature/f303-face-public-api` follows this commit; its outcome is reported in
  the session reply.
- No pull request (the block orders none).
- No merge, no worktree added or removed, no provider call. `gh pr list --state open` was not
  re-checked this round (no new branch was created; the Open PR Gate was already satisfied).

## Verification

Preconditions: `block.md` (158 lines), `verify.py`, `run_selection.py`, `selection.txt` and
`digests.txt` matched the digests given in the prompt; the five `c1-` files matched the digests in
`digests.txt`, and `c1-.agent__authored__f303-r3.md` read the same sha256 as `block.md`
(`c308a699d962609881bb28076a8de4a7bf44e7c0f045e95096b6be1610153fc3`). Before the first write,
`HEAD` read `8ee55fd5b`, the tree was clean, and `.agent/STOP` was absent.

1. Gate 1: `git status --porcelain` empty. `python3 .remedy-wt/f303-r3/prep/verify.py .` (run after
   C4, before this handback) — every check `True` (17 of them), `absent` for C5, last line
   `ALL True`.
2. Gate 2: `python3 -m ruff check` over every Python file C2 and C3 touched (12 files) —
   `All checks passed!`
3. Gate 3: `python3 .remedy-wt/f303-r3/prep/run_selection.py . .remedy-wt/f303-r3-worker/selection-output.txt`
   — exit 0; `changed tests: ['tests/cli/test_client_interface.py', 'tests/cli/test_job_steer.py',
   'tests/orchestration/test_client_story.py', 'tests/test_structure_ratchet.py',
   'tests/ui_server/test_public_api.py']`; `paths 90`; `4139 passed, 2 skipped in 95.85s`; no
   FAILED, ERROR or "process(es) behind" line. The two SKIPPED lines: `tests/test_agent_tooling.py:43`
   (D12 quarantine, pre-existing) and `tests/test_install_smoke.py:175` (opt-in, pre-existing).
4. Gate 4: `python3 -m apps.cli.main integrity check --json` — `fail_count` 1, only
   `high_blockers_open`: `R-1335, R-1336, R-1337, R-1338, R-1345, R-1346, R-1348, R-1349, R-1359,
   R-1360, R-1361, R-1362` — the same twelve findings as rounds 1 and 2.
5. Gate 5: `python3 -c "import scripts.rotate_live_review as r;
   print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` — `88`.
6. Gate 6: `git -C . diff --stat 8ee55fd5b HEAD -- packages/orchestration/ui_server.py
   packages/orchestration/serve_daemon.py` — prints nothing.

## Authored-text proofs

C1's `.agent/authored/f303-r3.md`: byte copy of `c1-.agent__authored__f303-r3.md`, itself
byte-equal to `block.md` (158 lines, sha256
`c308a699d962609881bb28076a8de4a7bf44e7c0f045e95096b6be1610153fc3`), both readings matching
before the commit (reported at the start of this session) and again by `verify.py`'s five `C1 ...
equals ...` lines, every one `True`. C2 through C4 applied no reviewer-authored text; every line
is this worker's own, written from `## Change set — C2` through `C4` of `block.md` and from
DECISION F303 D3's literal text.

## Deviations & assumptions

**`JOB_STEER_ANSWER_KEYS` carries `matches`, which DECISION F303 D3 (2)'s literal list of six
keys does not name.** `job.steer` reaches `apps/cli/job_id_arg.py:resolve_job_id_or_fail`'s
ambiguous-id branch, which answers `matches` in its envelope exactly as `job.decline` and
`job.stop` already do (both of which DO list `matches` in their own `OPERATION_ANSWER_KEYS`
entries). `tests/cli/test_client_interface.py::test_declared_answer_keys_equal_the_keys_the_handler_reaches[job.steer]`
reads this mechanically from the real code (not from a hand-verified registration this worker
controls), so there was no way to satisfy that guard without adding the key — the guard is never
weakened or routed around. Added `matches` to the tuple, sorted; everywhere else follows the
decision's six keys unchanged.

**The accepted answer's `outcome` key (always `"accepted"` on that branch) is not declared.**
`steer_task_command`'s accepted envelope also carries `outcome`, which the CLI's
`emit_ok(job_id=job_id, **result)` still prints (unchanged behaviour — `test_the_json_form_emits_the_answers_own_keys`
in `tests/cli/test_job_steer.py` still asserts `body["outcome"] == "accepted"`). This key IS
hideable from the static reader, because it is read only through a hand-verified
`UNRESOLVED_ANSWER_SITES` registration this worker writes, not mechanically derived; its real-run
cross-check (`test_a_real_runs_answers_return_only_keys_the_interface_names`) never reaches this
operation's accept path (it only drives the refusal `job_not_steerable`, which has no `outcome`
key), so the omission ships silently green. Followed DECISION F303 D3 (2)'s literal six keys
here, reading `outcome` as redundant with the envelope's own `ok` on this command's single accept
shape, and said so in the registration's own comment — flagging it for an operator read rather
than inventing a widened declaration the decision does not ask for.

No other deviation. Every path, body shape, argv, refusal list, version bump and docstring change
follows `block.md`'s C2 through C4 and DECISION F303 D3 literally; the extra test-file edits
(`tests/cli/test_client_interface.py`'s two `UNRESOLVED_*_SITES` registrations and the big
real-run integration test's new `job.steer` call, required by that file's own existing guards
once `job.steer` joined `CLIENT_OPERATION_IDS`) are named above and are the only paths outside the
block's literal per-commit lists; `tests/cli/test_client_interface.py` is "the test file named
after" `client_interface.py`, itself named in C2's bundle.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | this handback |
| Gate 1 | done | every check True, `absent` for C5, `ALL True` |
| Gate 2 | done | All checks passed! |
| Gate 3 | done | exit 0, 90 paths, 4139 passed, 2 pre-existing skips, no FAILED/ERROR |
| Gate 4 | done | fail_count 1, high_blockers_open only, same twelve findings |
| Gate 5 | done | 88 |
| Gate 6 | done | prints nothing |
| Push | pending | reported in the session reply |

## Next

Book this round's verdict in round 4's first commit. Round 4: the MCP facet (its server, its
allowlist closed by default, its three tools, its page). Then round 5 and the closure.

Operator questions open: 3
Open findings: 88

## For the operator, in plain sentences

Round 2's stop is resolved: the steering note now has its route. A client can address a note to
one task of a running job over `POST /api/v1/jobs/{job}/note`, the same way `remedy job steer`
already does from the command line, and the note is recorded as having come through the `api`
door. The one wrinkle round 2 found — the note's text is typed right after the job on the command
line, not given as an option, and a rule this codebase already enforces wants every value a route
sends to be an option — is closed by letting a route say, explicitly, which of its values are
positional instead, checked against the real command the same way every option already is. The
job's run story now also tells a client whether a note would even be accepted right now. Two small
details of the new client operation's declared answer differ from the decision's own list by one
key each, in opposite directions — one has to be added because the code actually sends it, one is
left out even though the code actually sends it too — both explained above; nothing else about
this round's build needed a judgment call.
