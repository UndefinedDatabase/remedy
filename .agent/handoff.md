# Handback — F303 round 2: book round 1, the catalog split, blocked at the note route's body shape

## Session

SESSION 1 of feature F303 · round 2 · rounds so far 2

Context self-assessment: this worker verified every prepared digest, byte-copied the four C1
files, moved the `job.steer` catalog entry to its own module exactly as C2 specified, and then
found that C3's literal route body makes an existing well-formedness guard red; it stopped before
writing any note-route code rather than guess past the block, and wrote this handback with ample
context margin left.

Fortschritt: ~20 % (round 1 booked, `job.steer` modularized · the note route blocked, MCP facet
open) — Schätzung

## Range

Review of `5486f7d03`..`HEAD` on `feature/f303-face-public-api`.

## Commits

### bc26a84d2 F303 R2 C1: book round 1, DECISION F303 D2 and the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f303-r2.md` | 154/0 | this round's block, byte copy (154 lines, sha256 `5685ecab52e997661396465aad521381628e9af760d6cd737318e5f1cd6c546f`, equal to `block.md`) |
| `.agent/live_review.md` | 2/0 | prepared file, byte copy |
| `.agent/decisions.md` | 13/0 | DECISION F303 D2 appended (prepared file, byte copy) |
| `.agent/plan.md` | 6/8 | rewritten for F303 round 2 (prepared file, byte copy) |

### 502611ea1 F303 R2 C2: the job steer catalog entry moves to its own module (structure step)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog.py` | 2/23 | the `job.steer` entry (with its comment line) replaced by `*JOB_STEER_COMMANDS,` at the same place; one import line added beside the certificate import |
| `apps/cli/command_catalog_steer.py` | 36/0 | NEW FILE: `JOB_STEER_COMMANDS`, the entry moved unchanged, as F060 placed `JOB_CERTIFICATE_COMMANDS` |
| `docs/system/structure-ledger-v1.md` | 1/1 | the catalog's row lowered 2314 → 2293 |
| `tests/test_structure_ratchet.py` | 1/1 | `MAX_FILE_LINES` lowered 64177 → 64156 (the same delta, confirmed by `structure_measure.measure_repository`) |
| `tests/orchestration/import_reachability_allowlist.txt` | 1/0 | extra path a guard test demanded: `apps.cli.command_catalog_steer` added, sorted, after `test_no_module_outside_the_allowlist_is_reachable_from_the_entry_points` went red |

`remedy job steer --help` was captured before C2 (via `git stash` of the three WIP files) and
after; the two captures are byte-identical (confirmed with `diff`, exit 0).

### (this commit) F303 R2: handback recording the C3 stop
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | rewritten | Current Step and Next Steps now name the C3 blocker and its three candidate resolutions |
| `.agent/handoff.md` | rewritten | this handback |

## External actions

- `git push origin feature/f303-face-public-api` follows this commit; its outcome is reported in
  the session reply.
- No pull request (the block orders none, and this round is not reviewable as a whole).
- No merge, no worktree added or removed, no provider call. `gh pr list --state open` was not
  re-checked this round (the Open PR Gate was already satisfied at round 1 and no new branch was
  created).

## Verification

Preconditions: `block.md` (154 lines), `verify.py`, `run_selection.py`, `selection.txt` and
`digests.txt` matched the digests given in the prompt; the four `c1-` files matched the digests in
`digests.txt`, and `c1-.agent__authored__f303-r2.md` read the same sha256 as `block.md`
(`5685ecab52e997661396465aad521381628e9af760d6cd737318e5f1cd6c546f`). Before the first write,
`HEAD` read `5486f7d03`, the tree was clean, and `.agent/STOP` was absent.

1. Gate 1: `git status --porcelain` — empty after each commit. `python3
   .remedy-wt/f303-r2/prep/verify.py .` (run after C2, before this handback) — every check `True`
   (12 of them) for C1 and C2, `absent` for C3 through C6, last line `ALL True`.
2. Gate 2 (narrowed to what C2 touched; C3's files do not exist yet): `python3 -m ruff check
   apps/cli/command_catalog.py apps/cli/command_catalog_steer.py` — `All checks passed!`
3. Gate 3 was NOT run as the single full selection: `run_selection.py` is "the run that counts"
   for a complete round, and this round is not complete, so it was not spent on a partial tree.
   Instead, targeted tests over what C1/C2 touch: `python3 -m pytest -q -p no:cacheprovider
   tests/test_structure_ratchet.py tests/cli/test_command_catalog.py
   tests/orchestration/test_import_reachability.py` — first run: 1 failed (the import-reachability
   allowlist test, before the allowlist was updated), 24 passed; after adding the allowlist entry:
   `25 passed in 3.96s`, no FAILED/ERROR line.
4. Gate 4 (run for diligence, matches round 1's state): `python3 -m apps.cli.main integrity check
   --json` — `fail_count` 1, only `high_blockers_open`: `R-1335, R-1336, R-1337, R-1338, R-1345,
   R-1346, R-1348, R-1349, R-1359, R-1360, R-1361, R-1362` — the same twelve findings as round 1's
   handback.
5. Gate 5 (run for diligence): `python3 -c "import scripts.rotate_live_review as r;
   print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` — `88`.
6. Gate 6 (run for diligence): `git -C . diff --stat 5486f7d03 HEAD -- packages/orchestration/ui_server.py
   packages/orchestration/serve_daemon.py` — prints nothing.

## Authored-text proofs

C1's `.agent/authored/f303-r2.md`: byte copy of `c1-.agent__authored__f303-r2.md`, itself
byte-equal to `block.md` (154 lines, sha256
`5685ecab52e997661396465aad521381628e9af760d6cd737318e5f1cd6c546f`), both readings matching
before the commit (reported at the start of this session). The other three C1 paths: prepared
files, proven equal over bytes at copy time (a Python sha256 reader, not shell `cp`) and again by
`verify.py` (every `equals` line `True`). C2 applied no reviewer-authored text; its new module,
the catalog splice and the ledger/ratchet edits are this worker's own, written from the block's
literal specification in `## Change set — C2` of `block.md`.

## Deviations & assumptions

**The round stopped before C3.** DECISION F303 D2 (3) and block.md's C3 item 5 specify the note
route's body literally as `body=(("task", "string"), ("text", "string"))`, dispatched through the
ordinary `_TWIN_ARGV` path (not `starts_order` or `starts_run`). `tests/ui_server/test_public_api.py
::test_every_route_is_well_formed` holds, for every such route and every body key of kind
`"string"` or `"strings"`, that `"--" + key.replace("_", "-")` is a value-taking option
(`is_option` and not `is_flag`) of the route's twin catalog command — confirmed empirically
against the real catalog (`value_options` for `job.steer` is `{'--json', '--task'}`, and C3 item 2
only adds `--source`, never `--text`). `job.steer`'s `text` is a required POSITIONAL CLI argument
(`remedy job steer <job> <text> --task <task>`), not an option, and neither DECISION F303 D2 nor
block.md's C3 asks to change that shape; changing it would break the shipped CLI and the tests
that already drive it positionally (`tests/cli/test_job_steer.py`, written against the positional
form). The only existing precedent for a free-text body value with no CLI-option equivalent is the
`starts_order` exemption (`if route.starts_order: continue`, before the body-shape checks in
`answer_public_api_post`), which does not apply here. This is a guard test demanding something the
block does not foresee, and it cannot be resolved within the block's rules without either
weakening `test_every_route_is_well_formed` (forbidden) or changing `job.steer`'s shipped CLI shape
(out of C3's stated scope and a breaking change) — exactly the stop condition this session's work
order names.

Three candidate resolutions, for an operator decision (none applied — this worker invented
nothing):
(a) Give `PublicApiRoute` a field naming which body keys are passed positionally rather than as
`--options` (e.g. `positional_body_keys: tuple[str, ...]`), and have `test_every_route_is_well_formed`
skip those keys the way it already skips every key of a `starts_order` route; `_job_steer_argv`
would stay exactly as block.md specifies.
(b) Add a real `--text` option to `job.steer`'s catalog entry as an alternative to the positional
form, and have `_job_steer_argv` build the route's argv with `--text=<value>` instead of a
trailing positional — this changes `_job_steer_argv`'s literal return value from block.md's C3
item 4 and adds a second way to pass the same argument to the shipped CLI.
(c) Narrow `test_every_route_is_well_formed`'s check so it only requires a `--option` for a body
key when the route is not already covered by some other named exemption, with a DECISION
recording why `job.steer`'s `text` is the second such exemption after `starts_order`.
This worker's own reading favours (a): it keeps block.md's `_job_steer_argv` untouched, adds no
second CLI surface for the same argument, and the exemption generalizes to any future route whose
twin takes a positional value.

No other deviation. C1 and C2's paths, byte content and ledger/ratchet numbers all follow the
block exactly; the one extra path (the import-reachability allowlist entry) is named above and in
C2's own commit message.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | blocked | the note route's literal body conflicts with `test_every_route_is_well_formed`; see Deviations |
| C4 | skipped | depends on C3 |
| C5 | skipped | depends on C3 |
| C6 | deviated | this handback replaces the block's C6; it is not commit 6 of a completed sequence |
| Gate 1 | done | ALL True for C1, C2; `absent` for C3–C6 |
| Gate 2 | done | All checks passed! (narrowed to C2's files) |
| Gate 3 | skipped | not spent on a partial round; targeted tests run instead (see Verification) |
| Gate 4 | done | fail_count 1, high_blockers_open only, same twelve findings |
| Gate 5 | done | 88 |
| Gate 6 | done | prints nothing |
| Push | pending | reported in the session reply |

## Next

An operator decision on the note route's body shape (the three candidates above), then a fresh
block for C3 through C6 of this round. Round 3 and 4 remain the MCP facet. Book this round's
verdict in the next round's first commit.

Operator questions open: 4 (3 carried from round 1, plus this round's body-shape question)
Open findings: 88

## For the operator, in plain sentences

This round landed two clean, independent steps — it recorded round 1's result and DECISION F303
D2, and it moved the `job steer` command's catalog entry into a module of its own so the catalog
file has room again, with no change anyone running the command would notice. It then stopped
before writing the new HTTP route for a steering note, because the exact shape the decision
describes for that route's request body does not fit a rule this codebase already enforces: every
write route's body value must correspond to a real command-line option, and the note's text is
not one — it is typed directly after the job, the way `remedy job steer <job> "text"` already
works today. Changing that would alter a command people already use. Three ways to close the
gap are written out above, with a recommendation; nothing further happens on the note route until
one is chosen.
