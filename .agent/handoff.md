# Handoff — F253 round 15: book round 14, S5b create-then-poll an order over HTTP

## Session

SESSION 4 of feature F253 · round 15 · rounds so far 15

Context self-assessment: the reviewer's context is workable after three rounds; the session continues with S5c.

Fortschritt: ~78 % (S1 to S3, S4a to S4c, S5a, S5b, S6a · S5c, S6b, S7 open) — Schätzung

## Range

Review of `e0cabecc5cbb9a02531c85712216156ee0a9bac0`..`8f96bac473cb3accb1d9a2f8add5e9472f8a5c15`
(the last commit before this handback, C4).

## Commits

### 71c11164c F253 R15 C1: book round 14, resolve R-1197 to R-1200, DECISION F253 D14, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r15.md` | 153/0 | new file, byte copy of `block.md` |
| `.agent/decisions.md` | 10/0 | `append-decisions.txt`'s bytes appended: DECISION F253 D14 |
| `.agent/live_review.md` | 10/0 | `append-live_review.txt`'s bytes appended: round 14's gate entry and R-1197 to R-1200 resolved |
| `.agent/plan.md` | 13/15 | `dry-plan.md`, byte for byte |

### bbd877274 F253 R15 C2: a client polls an order over HTTP, as remedy client order reads it (DECISION F253 D14)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/client_cmd.py` | 11/18 | `_cmd_client_order` now builds its payload through the new shared `order_record_payload`/`order_not_found_message` instead of its own inline dict and message |
| `docs/system/public-http-api-v1.md` | 9/1 | hand-written `## Orders` section (polling sentence); version bumped to `1.7`; the generated table regenerated with the new `GET` row |
| `packages/orchestration/public_api.py` | 36/1 | module docstring sentence on the new route; `PUBLIC_API_VERSION = "1.7"`; the `GET /api/v1/orders/{order}` route; `_order_answer`, registered under `client.order` in `_TWIN_ANSWERS` |
| `packages/orchestration/serve_runs.py` | 30/0 | `order_not_found_message` and `order_record_payload`, shared by the command and both routes (D14 (4)) |
| `tests/cli/test_client_interface.py` | 8/0 | `UNRESOLVED_ANSWER_SITES` entry for `_cmd_client_order`'s `**payload`, now a call rather than a dict literal, with its seven keys hand-verified |
| `tests/ui_server/test_public_api.py` | 60/1 | the `GET` route pinned; equal to `remedy client order --json` for an ended stand-in order and for an unknown id (404); `../x` answers `order_not_found` 404; the stale `"1.6"` version assertion on the decision route's own pinned test updated to `"1.7"` |

### 8f96bac47 F253 R15 C3: a client creates an order over HTTP and the supervisor starts it (DECISION F253 D14)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/public-http-api-v1.md` | 14/0 | hand-written sentences on creating an order and on `api_order_project_unknown`; the generated table regenerated with the new `POST` row |
| `docs/system/serve-daemon-v1.md` | 5/4 | the stale "no route starts an order yet" sentence replaced: `POST /api/v1/orders` now does, through the registry's own `OrderLauncher` |
| `packages/orchestration/public_api.py` | 107/8 | `starts_order` field on `PublicApiRoute`; the `POST /api/v1/orders` route; `_order_text_and_options` (parses the body, resolves its header's project, refuses through `PublicApiWriteRefusal`); `answer_public_api_post` gains `start_order` and the `starts_order` branch (405 with no starter, else 202 with `order_record_payload`) |
| `packages/orchestration/serve_daemon.py` | 31/13 | `socket_handler_class` and `public_api_handler_class` both take an `OrderLauncher`; `run_supervisor` makes one and hands it to both |
| `packages/orchestration/ui_server.py` | 7/1 | `_RemedyHandler.order_launcher` (`None` by default); `_send_public_api_post` passes its `.start` (or `None`) to `answer_public_api_post` |
| `tests/orchestration/test_serve_daemon.py` | 69/0 | a real order, through the fake builder and reviewer, started by `POST /api/v1/orders` and followed to `ended` by `GET /api/v1/orders/{order}`, with the call ledger checked; a `POST` naming no project answers 409 and leaves the `orders/` folder untouched |
| `tests/ui_server/test_public_api.py` | 208/1 | the `POST` route pinned; its body checked against `do.run`'s own flags (its twin `client.order` takes none of them); each flag/string passed correctly; the order text reaches the starter byte for byte; 202 with the starter's record; the five pre-start refusals, none of which calls the starter; no starter is 405; the generic `test_every_route_is_well_formed` adjusted for `starts_order` |

### This commit (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handback cannot table the commit that writes it |

## External actions

- `git push origin feature/f253-public-http-api`, once, after this commit: reported in the
  worker's reply, not here (this file is written before the push).
- No pull request opened, no full suite, no mutation, no worktree, no merge, no new branch, no
  force-push, no pull, no `REMEDY_TEST_MAX_WORKERS`, no `-n`. No command read, listed or wrote the
  repository's own `.data`.

## Verification

1. Preconditions, before any write: `git rev-parse HEAD` read
   `e0cabecc5cbb9a02531c85712216156ee0a9bac0`, equal to
   `git rev-parse origin/feature/f253-public-http-api`; `git status --porcelain` was empty;
   `.agent/STOP` was absent; `block.md` read sha256
   `e0cf751ded7483271521c0791a7355cd361148688c9a9d5c4927578b1005a874`, matching the literal the
   task gave, and all four files listed in `digests.txt` matched their own digest (Python
   `hashlib`, 4 of 4 True); `git branch --show-current` read `feature/f253-public-http-api`
   before each commit.
2. Every commit: its staged diff was written to a file in the worker folder and read whole before
   the commit. C1's `.agent/authored/f253-r15.md` (a byte copy of `block.md`) and its two append
   proofs, and `.agent/plan.md`'s copy proof, were each proven byte-equal by script and so not
   re-read line by line (the proof is stated here, per the block's own allowance), though the
   whole cached diff was still read. C2's 154 lines and C3's 441 lines were read whole.
3. **Gate 1**: `git -C /home/decodeux/Repos/remedy status --porcelain` empty; the C1 byte proofs —
   `.agent/authored/f253-r15.md` byte-equal to `block.md` (153 lines, sha256
   `e0cf751ded7483271521c0791a7355cd361148688c9a9d5c4927578b1005a874`); `.agent/live_review.md`
   post == pre + `append-live_review.txt`'s slice, True; `.agent/decisions.md` post == pre +
   `append-decisions.txt`'s slice, True; `.agent/plan.md` byte-equal to `dry-plan.md`, True — all
   True.
4. **Gate 2**, from the primary checkout, once:
   `python3 -m pytest -q -rfEs tests/ui_server/test_public_api.py tests/orchestration/test_serve_daemon.py tests/orchestration/test_serve_runs.py tests/cli/test_client_order_cmd.py tests/cli/test_client_interface.py tests/ui_server/test_command_channel.py tests/orchestration/test_serve_artifacts.py tests/ui_server/test_dashboard_contract.py tests/test_ble001_ratchet.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/docs/ tests/cli/test_golden_path.py`
   — exit 0, `910 passed in 109.76s`; no FAILED, ERROR or SKIPPED line.
5. **Gate 3**: `python3 -m ruff check apps/cli/commands/client_cmd.py packages/orchestration/public_api.py packages/orchestration/serve_runs.py packages/orchestration/serve_daemon.py packages/orchestration/ui_server.py tests/cli/test_client_interface.py tests/ui_server/test_public_api.py tests/orchestration/test_serve_daemon.py`
   — exit 0, `All checks passed!`.
6. **Gate 4**: `python3 -m apps.cli.main integrity check --json` — exit 0, `"check_count": 6`, all
   six `pass`, `"fail_count": 0`, `"ok": true`.
7. **Gate 5**: `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   — exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160',
   'R-1162', 'R-1172', 'R-1176', 'R-1196']`, exactly as ordered.
8. Gate 6 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r15.md`: 153 lines, byte-equal, sha256
  `e0cf751ded7483271521c0791a7355cd361148688c9a9d5c4927578b1005a874`.
- `append-live_review.txt` appended to `.agent/live_review.md`'s base blob at `e0cabecc5`:
  "post equals pre plus slice" True.
- `append-decisions.txt` appended to `.agent/decisions.md`'s base blob at `e0cabecc5`:
  "post equals pre plus slice" True.
- `dry-plan.md` to `.agent/plan.md`: byte-equal.

## Deviations & assumptions

- No departure from the block's ordered commit sequence: exactly C1, C2, C3, in order; no C3b was
  needed because Gate 2 read green on its one and only run.
- **The shared functions' names (D14 (4) asks for "one function" and "one" message builder, not
  specific names).** `order_record_payload(paths, record)` and `order_not_found_message(order_id)`
  in `packages/orchestration/serve_runs.py`; `_cmd_client_order`'s own output is unchanged by a
  byte because `json.dumps(..., sort_keys=True)` makes key order irrelevant to the printed bytes,
  and the function's body is otherwise identical to what `_cmd_client_order` built inline before.
- **The static answer-key reader.** `order_record_payload` is a function call, not a dict literal,
  so `payload = order_record_payload(paths, record)` is unresolved to
  `tests/cli/test_client_interface.py`'s static reader by construction (the same shape the
  project's own notes call out: a payload bound through a call, not a literal, blinds that
  reader). Added the hand-verified entry the block anticipated
  (`apps.cli.commands.client_cmd:_cmd_client_order:**payload`) with the seven keys.
- **`PublicApiRoute.starts_order` (new field, my own name).** D14 (3) asks for "a new argument of
  `answer_public_api_post`, the handler's order starter" and "a route that starts an order is
  never passed to the command runner and locks on no job" — the dispatch inside
  `answer_public_api_post` needed a way to tell the order-create route apart from every other
  write route; I added this one boolean field rather than a side table, since every other route
  property already lives on `PublicApiRoute` itself. `refusal_default` stays `None` on this route
  (asserted by a widened `test_every_route_is_well_formed`): every refusal it can give is explicit
  through `PublicApiWriteRefusal`, so the route never falls through to a route-level default.
- **The order-create route's body does not validate against its own twin's flags.** `route.twin`
  is `client.order` for both new routes (D14 (1): "twin `client.order`, because its answer is what
  `remedy client order` answers"), but the create route's body mirrors `remedy do run`'s flags,
  which `client.order` does not have at all. `test_every_route_is_well_formed`'s generic
  body-to-flag check therefore skips a `starts_order` route (with a comment saying why), and a new
  dedicated test, `test_the_order_create_routes_body_matches_do_runs_own_flags`, checks the same
  body keys against `do.run`'s own catalog entry instead. This is a necessary consequence of
  adding the first route whose body and twin diverge, not a loosening: coverage is equivalent, just
  redirected to the right command.
- **No project header falls back to neither `REMEDY_PROJECT` nor cwd autodetection.**
  `_order_text_and_options` refuses immediately (409 `api_order_project_unknown`) when the header
  names no project, rather than calling `select_project(None, ".")`, which would consult the
  supervisor process's own environment variable and its own working folder — both arbitrary from
  one caller's perspective in a long-running server, and exactly the kind of "folder nobody chose"
  D14 (2) says this refusal exists to prevent. A header that does name a project still goes through
  `select_project` itself, exactly as `_order_repo` in `apps/cli/commands/do_cmd.py` does, so a
  project `select_project` cannot resolve to exactly one (ambiguous, invalid or unregistered) is
  caught the same way.
- **The 202 route never reads `--repo`/`--project`; only the header decides.** Confirmed against
  D14 (1)'s own list of what is deliberately not offered; the pre-start project check exists only
  to refuse early, never to pass a resolved value onward — the child (`remedy do run`) still
  resolves its own repository from the header exactly as it already does today.
- **Test fixtures.** The mocked `POST` tests in `tests/ui_server/test_public_api.py` (flags,
  strings, byte-for-byte text, the five refusals, no-starter) use a stand-in `OrderRecord` whose
  `ended_at` is already set, so `order_state` never touches `/proc` — deterministic without a real
  child process. The one test that checks the full 202 body
  (`test_an_order_create_post_answers_202_with_the_starters_record`) points that record's `out_log`
  at a real temporary file with a known envelope, so the assertion is a real comparison, not a
  tautology against the same code path it is testing. Real-process timing (`state` actually
  reading `running` immediately after a live start) is exercised only by the real-supervisor test
  in `tests/orchestration/test_serve_daemon.py`, which does assert `created["state"] == "running"`.
- **Project registration in tests.** The mocked `POST` tests register a project directly through
  `packages.orchestration.project_registry.register_project_repo` against a bare `git init`
  repository (no commit needed — `register_project_repo` only resolves the git root), avoiding a
  `remedy init` subprocess for every parametrized case. The real-supervisor test instead runs
  `remedy init --json` as a subprocess against the supervisor's own data root, mirroring
  `tests/cli/test_client_order_cmd.py`'s own real-run test, per the block's instruction to follow
  that registration.
- Everything else matches the block exactly: the four production files it named, the two doc
  pages, the two test files (plus `tests/cli/test_client_interface.py` for the one hand-verified
  site the block anticipated), the version bump to `1.7` once (in C2, not bumped again in C3), and
  the gates' order, commands and content.

## Round verdicts

Round 14's PASS, resolving R-1197 to R-1200, is booked by C1 above. Round 15's verdict is the
reviewer's, to be written into round 16's first commit.

## For the operator, in plain sentences

Round fourteen's repairs passed review; a program can now hand Remedy an order through the web
interface, and Remedy starts it in the background and answers at once with a number for the
order; the program then asks with that number how the order is doing and, once it has ended, reads
what Remedy answered; an order that does not name a project Remedy knows is refused before
anything starts, so it can never run in a folder nobody chose.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback
   and stop.
2. Then the Open PR Gate (rule 2): there is no pull request for this branch, so it finds none to
   merge.
3. Then book round 15's verdict in the next round's first commit.
4. Then S5c: two orders at once through HTTP.

Operator questions open: 0.
Open findings: 12 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158,
R-1162, R-1172, R-1176 and R-1196, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 14, resolve R-1197 to R-1200, DECISION F253 D14, the plan and the block | done | `71c11164c` |
| C2: a client polls an order over HTTP, as remedy client order reads it | done | `bbd877274` |
| C3: a client creates an order over HTTP and the supervisor starts it | done | `8f96bac47` |
| Gates 1 to 5 | done | all green, run once each, after C3 and before this file |
| C4: this handback | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
