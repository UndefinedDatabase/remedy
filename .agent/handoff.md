# Handback — F305 round 1: claim, structural step, and T001

## Session

SESSION 1 of feature F305 · round 1 · rounds so far 1

Context self-assessment: the session verified the block's own line count and sha256, the three
gate scripts' digests, and all eighteen digest-bearing Bundle-listed prepared files' digests
before any write (the three further Bundle files carrying no stated digest —
`head-live_review.md`, `append-live_review.txt`, `append-decisions.txt` — were instead proved by
building `.agent/live_review.md` and `.agent/decisions.md` from them and matching the result,
byte-for-byte, against the digested `dry-live_review.md` and `dry-decisions.md`, exactly gate 1's
own formula); copied every other file by a read-only Python script under
`.remedy-wt/f305-r1-worker/`; confirmed each commit's staged numstat against the Bundle's stated
pairs before every commit; and ran all six gates in one uninterrupted pass, each green on its
first and only run; context remains comfortable at handback.

Fortschritt: ~30 % (T001 landed · T002, T003 and the closure open) — Schätzung

## Range

Review of `f6004fdf1`..HEAD.

## Commits

### 5ab62eaf9 F305 R1 C1: claim F305, book F297 R14, re-head the ledger, DECISIONS F305 D1 and D2 with the feature file's amendment

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f305-r1.md` | +150/-0 | NEW FILE, byte copy of `.remedy-wt/f305-r1/prep/block.md` (150 lines, sha256 `21c8450c28a049464848ef0f3c17c1ba16c8fadbb86adcb017bf9efb162aba7a`) |
| `.agent/context.md` | +12/-9 | rewritten for F305, byte copy of `prep/dry-context.md` |
| `.agent/decisions.md` | +24/-0 | byte copy of base `.agent/decisions.md` plus `prep/append-decisions.txt`: DECISIONS F305 D1 and D2 |
| `.agent/live_review.md` | +25/-27 | re-headed for F305's claim (new heading, paragraph and Steps section), the base `## Findings` body carried byte-identical, F297 R14's `Gate:` entry appended — built per gate 1's `verify.py` formula (`prep/head-live_review.md` + base body from `## Findings` + `prep/append-live_review.txt`), byte-equal to `prep/dry-live_review.md` |
| `.agent/plan.md` | +22/-13 | rewritten in full for F305 round 1, byte copy of `prep/dry-plan.md` |
| `docs/roadmap/STATUS.md` | +1/-1 | F305's line flips `[ ]`→`[~]`, byte copy of `prep/dry-STATUS.md` |
| `docs/roadmap/features/T13_F305.md` | +30/-0 | byte copy of `prep/dry-T13_F305.md`: the `## Amendment — DECISIONS F305 D1 and D2` section, with the slice list T001 to T003 |

### 36afdbf09 F305 R1 C2: every route below a project goes to cockpit_project_routes, and the rows of do_GET and ui_server fall (structural)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/structure-ledger-v1.md` | +9/-2 | byte copy of `prep/dry-structure-ledger-v1.md`: `_RemedyHandler.do_GET`'s boundary and its three steps written; its own row and the file's row lowered, `231`→`230` and `4834`→`4829` |
| `packages/orchestration/cockpit_project_routes.py` | +33/-0 | NEW FILE, byte copy of `prep/c2-cockpit_project_routes.py`: `_build_project_summary_json` and `project_route_answer` moved out of `ui_server.py`, step (1) of DECISION F305 D2 |
| `packages/orchestration/ui_server.py` | +9/-14 | byte copy of `prep/dry-ui_server.py`: the summary builder removed, imported back by name; every path of five parts or more below a project now one call into `project_route_answer` |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | byte copy of `prep/c2-import_reachability_allowlist.txt`: `packages.orchestration.cockpit_project_routes` added |
| `tests/test_structure_ratchet.py` | +2/-2 | byte copy of `prep/dry-test_structure_ratchet.py`: `MAX_FUNCTION_LINES` `30748`→`30747`, `MAX_FILE_LINES` `74823`→`74818`, lowered with the rows they pin |

### 2f92df594 F305 R1 C3: the mission card's server view and its two routes (T001)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/cockpit_project_routes.py` | +21/-2 | byte copy of `prep/dry-cockpit_project_routes.py`: the `.../missions` and `.../missions/<mission id>/orders` routes added, answered through `mission_cockpit` |
| `packages/orchestration/mission_cockpit.py` | +181/-0 | NEW FILE, byte copy of `prep/dry-mission_cockpit.py`: `project_missions_view`, `mission_orders_view`, and the chain/chip/usage helpers (T001, DECISIONS F305 D1 and D2) |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | byte copy of `prep/dry-import_reachability_allowlist.txt`: `packages.orchestration.mission_cockpit` added |
| `tests/orchestration/test_mission_cockpit.py` | +204/-0 | NEW FILE, byte copy of `prep/dry-test_mission_cockpit.py`: unit tests of both views, the chain band across repositories, the usage roll-up, and the missing/unreadable-job labels |

### 16b8c77b8 F305 R1 C4: the route door's tests, the route walk's two new paths and the cockpit page's section (T001)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/operator-cockpit-v1.md` | +23/-0 | byte copy of `prep/dry-operator-cockpit-v1.md`: the "A project's missions" section, documenting the two new routes and their 404 cases |
| `tests/orchestration/test_cockpit_project_routes.py` | +125/-0 | NEW FILE, byte copy of `prep/dry-test_cockpit_project_routes.py`: the route door read directly for every path shape, and through a real server on a free port |
| `tests/ui_server/test_command_channel.py` | +3/-0 | byte copy of `prep/dry-test_command_channel.py`: the route walk's two new paths added to the GET-route inventory |

### this commit F305 R1 C5: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file (self-reference rule, `docs/agents/handback_template.md`) |

## External actions

None yet in this commit. `git -C /home/decodeux/Repos/remedy push -u origin
feature/f305-multi-repo-chain-band` follows this commit, per the block's push-after-C5 instruction.
Its outcome is reported in the final reply, not in this file. No pull request is opened this round
(the block forbids it). No other `gh` command run. No worktree added or removed by the worker.

## Verification

**Preconditions (before C1):** `git branch --show-current` read `main`; `git rev-parse HEAD` read
`f6004fdf1d75315ca49f748d169c7a60def3b94e`; `git status --porcelain` empty; `gh pr list --state
open --json number` printed `[]`. Branch created:
`git -C /home/decodeux/Repos/remedy checkout -b feature/f305-multi-repo-chain-band`.

**Block and Bundle digests (before any write):** `wc -l block.md` read `150`, `sha256sum` read
`21c8450c28a049464848ef0f3c17c1ba16c8fadbb86adcb017bf9efb162aba7a` — both equal to the values the
prompt delivered. All three gate-script digests (`verify.py`, `run_selection.py`, `selection.txt`)
were checked against the prompt's stated values and matched. All eighteen digest-bearing
Bundle-listed prepared files (the `dry-*` and `c2-*` files) were hashed via a python3 sha256
reader: every one matched the block's stated digest exactly (`ALL True`). The three further
Bundle files the block states carry no digest of their own (`head-live_review.md`,
`append-live_review.txt`, `append-decisions.txt`) were read only to build `.agent/live_review.md`
and `.agent/decisions.md`, and that built result was checked byte-for-byte against the digested
`dry-live_review.md` and `dry-decisions.md` before C1 was staged (see C1 below).

**C1:** `c1_build_and_copy.py` byte-copied `dry-plan.md`, `dry-context.md`, `dry-STATUS.md` and
`dry-T13_F305.md` to their destinations; built `.agent/live_review.md` from
`prep/head-live_review.md` + the base ledger's body from `## Findings` onward +
`prep/append-live_review.txt`, and `.agent/decisions.md` from the base file +
`prep/append-decisions.txt`; byte-copied `block.md` to `.agent/authored/f305-r1.md`. Every one of
the nine comparisons (six copies, two built-files-against-`dry-*`, one authored-copy) printed `True`;
the script's own line count (`150`) and sha256 for the authored copy matched the block exactly;
`ALL True`. `git diff --cached --numstat` after `git add` read exactly the Bundle's seven C1 pairs
(see Commits table above), no other path. `git branch --show-current` read
`feature/f305-multi-repo-chain-band` immediately before the commit.

**C2:** `c2_copy.py` byte-copied the five files and re-hashed all five pairs: `True` for each,
`ALL True`. `git diff --cached --numstat` read exactly the Bundle's five C2 pairs, no other path.
`git branch --show-current` re-read correctly before the commit.

**C3:** `c3_copy.py` byte-copied the four files and re-hashed all four pairs: `True` for each,
`ALL True`. `git diff --cached --numstat` read exactly the Bundle's four C3 pairs, no other path.
`git branch --show-current` re-read correctly before the commit.

**C4:** `c4_copy.py` byte-copied the three files and re-hashed all three pairs: `True` for each,
`ALL True`. `git diff --cached --numstat` read exactly the Bundle's three C4 pairs, no other path.
`git branch --show-current` re-read correctly before the commit.

**Gate 1:** `git -C /home/decodeux/Repos/remedy status --porcelain` → empty. Then
`python3 -I /home/decodeux/Repos/remedy/.remedy-wt/f305-r1/prep/verify.py
/home/decodeux/Repos/remedy` →
```
equal True .agent/authored/f305-r1.md
equal True .agent/live_review.md
equal True .agent/decisions.md
equal True .agent/plan.md
equal True .agent/context.md
equal True docs/roadmap/STATUS.md
equal True docs/roadmap/features/T13_F305.md
equal True packages/orchestration/ui_server.py
equal True docs/system/structure-ledger-v1.md
equal True tests/test_structure_ratchet.py
equal True packages/orchestration/mission_cockpit.py
equal True packages/orchestration/cockpit_project_routes.py
equal True tests/orchestration/import_reachability_allowlist.txt
equal True tests/orchestration/test_mission_cockpit.py
equal True tests/orchestration/test_cockpit_project_routes.py
equal True tests/ui_server/test_command_channel.py
equal True docs/system/operator-cockpit-v1.md
equal at C2 True packages/orchestration/cockpit_project_routes.py
equal at C2 True tests/orchestration/import_reachability_allowlist.txt
base plus slice True .agent/decisions.md
new head, base body, appended entry True .agent/live_review.md
ALL True
```
Exit 0, every line `True`, last line `ALL True`.

**Gate 2:** `python3 -m ruff check packages/orchestration/ui_server.py
packages/orchestration/cockpit_project_routes.py packages/orchestration/mission_cockpit.py
tests/orchestration/test_mission_cockpit.py tests/orchestration/test_cockpit_project_routes.py
tests/ui_server/test_command_channel.py tests/test_structure_ratchet.py` → `All checks passed!`,
exit 0.

**Gate 3 (the round's one test selection, run once):**
`python3 -I /home/decodeux/Repos/remedy/.remedy-wt/f305-r1/prep/run_selection.py
/home/decodeux/Repos/remedy` →
```
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
3840 passed, 3 skipped in 30.41s
exit 0
```
Exactly the reviewer's dry-tree reading (seconds differ, as expected): same three SKIPPED lines,
same `3840 passed, 3 skipped`, same `exit 0`; no FAILED or ERROR line; no line containing
`process(es) behind`. The primary checkout also lacks the UI source, so it skipped the same test
the dry tree skipped rather than running it.

**Gate 4:** `python3 -m apps.cli.main integrity check --json` → exit 0,
`{"check_count": 6, "fail_count": 0, "ok": true, "passed": true, ...}`, all six checks `pass`
(`handler_import` handlers=184; `live_review_verdict` last Gate verdict PASS;
`plan_consistency` unchecked=0; `relevant_untracked` untracked=0/relevant=0; `repo_root_hygiene`
clean; `high_blockers_open` none open).

**Gate 5:** `python3 -c "import scripts.rotate_live_review as r;
print(r.open_finding_ids(open('.agent/live_review.md').read()))"` →
`['R-1235', 'R-1246', 'R-1248', 'R-1251', 'R-1252']`, exact match, exit 0.

**Gate 6:** `git -C /home/decodeux/Repos/remedy log --format=%s f6004fdf1..HEAD` →
```
F305 R1 C4: the route door's tests, the route walk's two new paths and the cockpit page's section (T001)
F305 R1 C3: the mission card's server view and its two routes (T001)
F305 R1 C2: every route below a project goes to cockpit_project_routes, and the rows of do_GET and ui_server fall (structural)
F305 R1 C1: claim F305, book F297 R14, re-head the ledger, DECISIONS F305 D1 and D2 with the feature file's amendment
```
Subjects of C1 to C4, newest first, as required.

No mutation run (the block forbids it this round; the reviewer ran them in a disposable worktree).
No test run beyond Gate 3's one pytest selection; `REMEDY_TEST_MAX_WORKERS` was never set, no extra
`-n` was passed, no two test commands ran at once. No full suite. No worktree of the worker's own
beyond the pre-existing, gitignored `.remedy-wt/f305-r1-worker/` scratch directory this session
created for its own copy/hash scripts. No provider call.

## Authored-text proofs

1. `block.md` → `.agent/authored/f305-r1.md` (C1): byte-equal, confirmed by `c1_build_and_copy.py`
   and again by gate 1's `verify.py`.
2. `prep/head-live_review.md` + the base ledger's body from `## Findings` onward +
   `prep/append-live_review.txt` → `.agent/live_review.md` (C1): built by the formula gate 1's
   `verify.py` checks, byte-equal to `prep/dry-live_review.md`, confirmed by `c1_build_and_copy.py`
   and again by gate 1.
3. The base `.agent/decisions.md` + `prep/append-decisions.txt` → `.agent/decisions.md` (C1): built
   the same way, byte-equal to `prep/dry-decisions.md`, confirmed the same way.
4. Every other Bundle-listed prepared file (`dry-plan.md`, `dry-context.md`, `dry-STATUS.md`,
   `dry-T13_F305.md`, `dry-ui_server.py`, `c2-cockpit_project_routes.py`,
   `dry-structure-ledger-v1.md`, `dry-test_structure_ratchet.py`,
   `c2-import_reachability_allowlist.txt`, `dry-mission_cockpit.py`,
   `dry-cockpit_project_routes.py`, `dry-import_reachability_allowlist.txt`,
   `dry-test_mission_cockpit.py`, `dry-test_cockpit_project_routes.py`,
   `dry-test_command_channel.py`, `dry-operator-cockpit-v1.md`) was copied and re-hashed byte-equal
   at its own commit's working tree, per the per-commit verification above — gate 1's `verify.py`
   `ALL True` covers every one of them again, together, against the committed state.

## Deviations & assumptions

1. **Gates 1 and 3 run under `python3 -I`, not the plain `python3` the block's gate lines show.**
   The session's own environment instructions ask that Python reading files under a prepared,
   reviewer-authored scratch directory be run with `-I` to isolate the interpreter from the current
   directory and the script's own directory. Gate 1 (`verify.py`) and gate 3's wrapper
   (`run_selection.py`) both read only `prep/` files and the standard library (`pathlib`,
   `subprocess`, `sys`, `os`); `run_selection.py` itself spawns `pytest` as a child process via
   `subprocess.run`, which does not inherit the parent interpreter's `-I` flag, so the suite under
   test ran exactly as the block's own command would have run it. Both gates' outputs are reported
   above and match the required criteria exactly, so the flag made no difference to any result.
   Gates 2, 4 and 5 were run exactly as the block's gate lines show, with no added flag.

No other deviation. No file was written outside each commit's named path set; no mutation was run
(none was ordered); no two test commands ran at once; `REMEDY_TEST_MAX_WORKERS` was never set and
no extra `-n` was passed; `.agent/STOP` did not appear during the round; no merge, branch
create/switch beyond the one feature branch, or force-push was performed; no pull request was
opened.

## For the operator, in plain sentences

The work on showing an order's jobs across several repositories in the cockpit has begun. This
round taught the cockpit's server to answer, for a project, its missions, and for a mission, its
newest orders, each order with the jobs it started in every repository it reached and the number
of model calls and tokens its jobs used. Nothing a person sees in the cockpit changes yet. A first
step in this round only moved existing code to a better place without changing what it does.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): absent throughout this round; the next session checks it first,
   before anything else, per protocol order.
2. The Open PR Gate.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. The next round's first commit books round 1's verdict.
5. T002, the cockpit's mission card.

Operator questions open: 1.
Open findings: 5 — R-1248, owned by F305, and R-1235, R-1246, R-1251 and R-1252, owned by F306.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | F305 claimed, ledger re-headed, F297 R14 booked, DECISIONS F305 D1 and D2 with the feature file's amendment; all byte proofs `True` |
| C2 | done | structural step: `do_GET`'s boundary written, the summary route moved to `cockpit_project_routes.py`, the ratchet's rows and pins lowered |
| C3 | done | T001's server view: `mission_cockpit.py`'s two views and their routes, with their unit tests |
| C4 | done | the route door's own tests, the route walk's two new paths, the cockpit page's section |
| C5 | done | this handback |
| Structural step (DECISION F305 D2) | done | boundary and steps written on `docs/system/structure-ledger-v1.md`; `do_GET` and `ui_server.py` rows lowered in the same commit; proved by the unchanged tests staying green |
| T001 | done | `mission_cockpit.py`, its two routes through `cockpit_project_routes.py`, their tests, the route walk's two new paths, the cockpit page's section |
| Gate 1 | passed | every line `True`, `ALL True` |
| Gate 2 | passed | `All checks passed!` |
| Gate 3 | passed | exit 0, `3840 passed, 3 skipped`, no FAILED/ERROR, no `process(es) behind` line |
| Gate 4 | passed | exit 0, six checks `pass`, `fail_count` 0 |
| Gate 5 | passed | exact id-list match |
| Gate 6 | passed | subjects of C1 to C4, newest first, as shown above |
