# Handoff — F253 round 1: claim, DECISION F253 D1, and S1: `/api/v1`, the registry, `GET /api/v1/interface`, the page

## Session

SESSION 1 of feature F253 · round 1 · rounds so far 1

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~8 % (claim, S1 of seven slices · S2 to S7 open) — Schätzung

## Range

Review of `1474a65ea6ed9f8063ce57f5294f9afaf95deee4`..HEAD (HEAD is C4 below, which carries this
handback and is the last commit on the branch).

## Commits

### c7a00839d F253 R1 C1: claim F253, book F304 R24, DECISION F253 D1, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r1.md` | 250/0 | new file, byte copy of `block.md` |
| `.agent/context.md` | 13/9 | `dry-context.md`, byte for byte |
| `.agent/decisions.md` | 10/0 | `append-decisions.txt`'s bytes appended, never read whole |
| `.agent/live_review.md` | 27/29 | `dry-live_review.md`, byte for byte (re-head at the F253 claim) |
| `.agent/plan.md` | 24/17 | `dry-plan.md`, byte for byte |
| `docs/roadmap/STATUS.md` | 1/1 | `dry-STATUS.md`, byte for byte (F253's line becomes `[~]`) |
| `docs/roadmap/features/T12_F253.md` | 5/0 | `dry-T12_F253.md`, byte for byte (DECISION F253 D1 amendment) |
| `docs/roadmap/features/T12_F303.md` | 6/0 | `dry-T12_F303.md`, byte for byte (the MCP facet moves here) |

### bb01d85cf F253 R1 C2: the public HTTP API's route registry and GET /api/v1/interface on the shared handler (S1, DECISION F253 D1)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/public_api.py` | 195/0 | new file: `PUBLIC_API_PREFIX`, `PUBLIC_API_VERSION`, `PublicApiRoute`, `PUBLIC_API_ROUTES` (one route), `PUBLIC_API_EXCLUDED_COMMANDS`, `command_is_excluded`, `is_public_api_path`, `public_api_token_refusal`, `answer_public_api_get`, `render_public_api_markdown`, `write_public_api_page` |
| `packages/orchestration/ui_server.py` | 31/1 | top-level import of `is_public_api_path`; `do_GET` branch after `/assets/` and before the query-token check; new `_send_public_api_get`; `_send_json` gains optional `headers` |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | adds `packages.orchestration.public_api` — not a path the block named for C2; see Deviations |
| `tests/ui_server/test_command_channel.py` | 7/1 | `_walkable_paths` adds every `PUBLIC_API_ROUTES` path, docstring says so |
| `tests/ui_server/test_public_api.py` | 261/0 | new file: the route's answer over TCP and the supervisor's unix socket, the six refusal/shape cases, the `PINNED_ROUTES` drift guard, route well-formedness, the exclusion list, deprecation |

### 4a0e39b24 F253 R1 C3: the public HTTP API page with its version rule, its exclusion list and the generated route table

| Path | +/- | Reason |
|---|---|---|
| `docs/README.md` | 2/0 | quick-find row after `machine client`; system-pages row after `machine-client-contract-v1.md`'s |
| `docs/system/public-http-api-v1.md` | 75/0 | new file: hand-written rules above the markers, generated section via `write_public_api_page()` |
| `tests/ui_server/test_public_api.py` | 19/0 | page's generated section equals `render_public_api_markdown()`; page states the prefix, the auth scheme and both refusal tokens plus `Deprecation: true` |

### F253 R1 C4: handback (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handoff cannot table the commit that writes it |

## External actions

- `git -C /home/decodeux/Repos/remedy checkout -b feature/f253-public-http-api` (C0); confirmed HEAD
  `1474a65ea6ed9f8063ce57f5294f9afaf95deee4`, `git status --porcelain` empty, `.agent/STOP` absent.
- Single test files run while writing C2 and C3, one at a time, none of them the round's gate-2
  selection: `tests/ui_server/test_command_channel.py` (110 passed), `tests/ui_server/test_public_api.py`
  (run repeatedly while writing it; 15, then 17, passed at each stopping point),
  `tests/orchestration/test_import_reachability.py` (3 passed, after the allowlist fix),
  `tests/test_no_orphan_modules.py` (6 passed), `tests/cli/test_client_interface.py` (65 passed),
  and `tests/docs/test_docs_consistency.py`, `tests/docs/test_named_source_paths.py`,
  `tests/docs/test_retired_promote_word.py`, `tests/docs/test_vocabulary.py`,
  `tests/docs/test_environment_guide.py`, `tests/docs/test_operator_questions_shape.py`,
  `tests/docs/test_toolchain_refresh_order.py`, `tests/docs/test_bootstrap_reads_decisions_by_part.py`
  (302 + 3 + 25 passed across those files).
- `git push -u origin feature/f253-public-http-api`, once, after this commit: reported in the
  worker's reply, not here (Rule A4: this file is written before the push).
- No full suite, no mutation, no other pytest command beyond the above and the round's one gate-2
  selection, no worktree, no merge, no new branch beyond C0, no force-push, no pull, no checkout
  or switch away from the feature branch.

## Verification

0. Before any write: all twelve files under `.remedy-wt/f253-r1/` matched their sha256 (Python
   `hashlib`, 12 of 12 True; `block.md` 250 lines, sha256
   `ad7baf86db0387652f620a634cc097d2ed55d186bd125409f13ec857025db9e4`). `git rev-parse HEAD` read
   `1474a65ea6ed9f8063ce57f5294f9afaf95deee4`, `git status --porcelain` was empty, `.agent/STOP` was
   absent, `gh pr list --state open` read `[]`. `git branch --show-current` read
   `feature/f253-public-http-api` before each commit.
1. C1: every copy byte-equal to its prepared file (7 of 7 True); `.agent/decisions.md` equal to its
   blob at `1474a65ea` followed by `append-decisions.txt`'s bytes (True). `git diff --cached
   --numstat` read `250 0`, `13 9`, `10 0`, `27 29`, `24 17`, `1 1`, `5 0`, `6 0`. The staged diff
   (478 lines) was written to a file and read whole as the self-review.
2. **Gate 1** (after C3, before C4): `git -C /home/decodeux/Repos/remedy status --porcelain` —
   empty. The C1 step-3 byte proofs, re-run: all seven True, plus the decisions.md proof True (8 of
   8 True).
3. **Gate 2**, from the primary checkout, once:

       python3 -m pytest -q -rfEs tests/ui_server/test_public_api.py tests/ui_server/test_command_channel.py tests/orchestration/test_serve_daemon.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/cli/test_client_interface.py tests/docs/ tests/cli/test_golden_path.py

   exit 0, `590 passed in 94.82s`, no FAILED, ERROR or SKIPPED line.
4. **Gate 3**:

       python3 -m ruff check packages/orchestration/public_api.py packages/orchestration/ui_server.py tests/ui_server/test_public_api.py tests/ui_server/test_command_channel.py

   exit 0, `All checks passed!`.
5. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, `"check_count": 6`,
   `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`,
   `repo_root_hygiene` and `high_blockers_open` all `pass`, `"fail_count": 0`, `"ok": true`.
6. **Gate 5** (`python3 -c "import scripts.rotate_live_review as r;
   print(r.open_finding_ids(open('.agent/live_review.md').read()))"`): exit 0,
   `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162',
   'R-1172', 'R-1176']`.
7. Gate 6 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r1.md`: 250 lines, byte-equal, sha256
  `ad7baf86db0387652f620a634cc097d2ed55d186bd125409f13ec857025db9e4`.
- `dry-STATUS.md` to `docs/roadmap/STATUS.md`, `dry-live_review.md` to `.agent/live_review.md`,
  `dry-plan.md` to `.agent/plan.md`, `dry-context.md` to `.agent/context.md`, `dry-T12_F253.md` to
  `docs/roadmap/features/T12_F253.md`, `dry-T12_F303.md` to `docs/roadmap/features/T12_F303.md`:
  byte-equal, each (Verification item 1).
- `.agent/decisions.md` equal to its blob at `1474a65ea` followed by `append-decisions.txt`'s bytes:
  True (Verification item 1).
- `docs/system/public-http-api-v1.md`'s generated section equal to `render_public_api_markdown()`:
  proved by `tests/ui_server/test_public_api.py::test_the_pages_generated_section_equals_the_rendering`,
  part of Gate 2's green run.

## Deviations & assumptions

- `tests/orchestration/import_reachability_allowlist.txt` was touched in C2, a path the block did
  not name for that commit. The block's own C2 instruction puts a top-level
  `from packages.orchestration.public_api import is_public_api_path` in
  `packages/orchestration/ui_server.py`, which is one of the six D11 (c) entry points
  `tests/orchestration/test_import_reachability.py` walks; that import makes
  `packages.orchestration.public_api` statically reachable from it, and the test (named in Gate 2)
  reds without the new module in the allowlist. One line added, alphabetically between
  `packages.orchestration.provider_token_evidence` and `packages.orchestration.rate_governor`;
  verified green by the single-file run in External actions and by Gate 2.
- No other departure from the block's ordered commit sequence or its named paths. C0 through C3
  landed in the order and under the subjects the block gave; the git-commit-time `--stat` summary
  line for C1 printed `345 insertions(+), 65 deletions(-)` (a `rewrite .agent/plan.md (90%)` line
  was shown alongside it), where a fresh `git show --stat`/`--numstat` immediately after and now
  both read `336 insertions(+), 56 deletions(-)`; the lower, consistently reproduced number is what
  is reported throughout this file and is the one the 500-insertion cap is checked against.

## Round verdicts

F304's round 24 PASS is booked by this round's C1. Round 1's verdict is the reviewer's.

## For the operator, in plain sentences

The second part of the machine client contract is merged into the main line after both of
GitHub's checks passed. The new feature gives a program a public web interface on this machine,
through which it can do what the command line already lets it do. This round started it with the
first address, which tells a program what this Remedy can do, and a page that lists every
address, how a program proves who it is, how the interface may change over time, and which
maintenance commands are never offered over it. A part meant for other tools that plug into
Remedy, called the MCP server, moved to the later feature that moves the cockpit onto the same
interface. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then the Open PR Gate.
3. Then the booking of round 1's verdict in the next round's first commit.
4. Then S2: a ledger entry for every call, the digest and the proof.

Operator questions open: 0.
Open findings: 11 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162,
R-1172 and R-1176, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0: the branch | done | `feature/f253-public-http-api`, cut from `main` at `1474a65ea` |
| C1: claim F253, book F304 R24, DECISION F253 D1, the plan | done | `c7a00839d` |
| C2: the route registry and `GET /api/v1/interface` | done | `bb01d85cf`, with the allowlist deviation noted above |
| C3: the published page | done | `4a0e39b24` |
| Gates 1 to 5 | done | all green, run once each, before this file was written |
| C4: this handback | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
