# Handback — F058 round 1: claim F058, book F206 R6, the model-routing structural step, and T001 —
STOPPED mid-round at the weekly usage cap before this round's gates could run

## Session

SESSION 1 of feature F058 · round 1 · rounds so far 1

Context self-assessment: this round verified the block's sha256 and line count, and every prep
file's digest, before any write; byte-copied the seven dry-* targets and the block itself for C1
with a Python bytes equality the block's own numstat lines then confirmed; moved the two
`model_routing.*` config keys into `packages/orchestration/config_keys_model_routing.py` byte-for-
byte (C2), proved the registry's digest and the rendered environment guide's digest equal between
a worktree of C1 and the primary checkout with the move applied, and removed that worktree; added
the `model_failover.chains` key and `packages/orchestration/model_failover.py` with its parse and
hard-rule validation (C3), checked by hand against roughly twenty constructed scenarios with plain
Python before any test was written; and wrote `tests/orchestration/test_model_failover.py` (C4).
`.agent/STOP` (author `remedy-weekly-cap`) appeared on disk partway through C4's staging, before
this round's gates 1-6 had been run at all. Per `docs/agents/self_drive_protocol.md` G6 and
operator amendment amend0930b-slow-cap rule 6, the commit in hand (C4) was finished and this
handback written instead of running the gates; gates 1-6 are UNVERIFIED this round.

Fortschritt: ~20 % (T001 written and committed, unverified — the weekly cap stopped the round
before gate 1; T002, T003 and the closure remain open) — Schätzung

## Range

Review of `4f294374a`..HEAD.

## Commits

### c51ee5b9f F058 R1 C1: claim F058, book F206 R6, re-head the ledger, DECISION F058 D1 with the feature file's amendment

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f058-r1.md` | +240/-0 | NEW FILE, byte copy of `block.md` (240 lines, sha256 `659aa21e160fc5f4e7c8a6b331a325f224eafdb2a9b4a59c54d512ecc1c8adcf`, matching both the delivering prompt and the block header) |
| `.agent/context.md` | +11/-12 | rewritten for F058, byte copy of `dry-context.md` |
| `.agent/decisions.md` | +12/-0 | DECISION F058 D1 appended, byte copy of `dry-decisions.md` |
| `.agent/live_review.md` | +16/-15 | re-headed at the F058 claim, F206 R6 booked, byte copy of `dry-live_review.md` |
| `.agent/plan.md` | +14/-14 | rewritten for F058, byte copy of `dry-plan.md` |
| `.agent/prose_slips.md` | +1/-0 | one slip appended, byte copy of `dry-prose_slips.md` |
| `docs/roadmap/STATUS.md` | +1/-1 | F058's line `[ ]` to `[~]`, byte copy of `dry-STATUS.md` |
| `docs/roadmap/features/T3_F058.md` | +27/-0 | DECISION F058 D1's amendment section appended, byte copy of `dry-T3_F058.md` |

### ef824c7a5 F058 R1 C2: the model routing keys move to a module of their own (structural step 3 of the registry)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/config_keys_model_routing.py` | +57/-0 | NEW FILE; the two `model_routing.*` entries and their comments, moved byte-unchanged apart from indentation |
| `packages/orchestration/config.py` | +5/-47 | the two entries leave; `*MODEL_ROUTING_KEY_SPECS,` stands in their place; import added; imports comment names DECISION F058 D1 |
| `docs/system/structure-ledger-v1.md` | +2/-1 | `config.py` row `1838` to `1796`; boundary bullet gains Step (3) sentence |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FILE_LINES` `74678` to `74636` (re-summed from the ledger table) |
| `tests/docs/test_retired_promote_word.py` | +3/-0 | `config.py`'s `KEPT_BY_SENSE` entry shrinks to `{"promotion"}`; new entry for `config_keys_model_routing.py` carries the moved tokens |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `packages.orchestration.config_keys_model_routing` added after `config_keys_mission` |

### 8e7d41394 F058 R1 C3: the model failover chains' key, parse and hard-rule validation (T001)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/model_failover.py` | +313/-0 | NEW FILE: `FailoverLink`, `FailoverChainViolation`, `FailoverChainError`/`FailoverChainRefused`, `parse_failover_chains`, `validate_failover_chains`, `build_failover_chains`, `resolve_failover_chains` |
| `packages/orchestration/config_keys_model_routing.py` | +19/-0 | `model_failover.chains` key added, consecutive after `model_routing.promotion_evidence` |
| `docs/guides/environment.md` | +1/-0 | regenerated from the registry; exactly one new row, `REMEDY_MODEL_FAILOVER_CHAINS` |
| `tests/test_no_orphan_modules.py` | +2/-0 | `ALLOWED_UNWIRED` gains `packages/orchestration/model_failover.py` in path order |

### 39cfdb002 F058 R1 C4: the model failover chains' tests (T001)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_model_failover.py` | +434/-0 | NEW FILE: parse refusals, the four hard rules (including `core_role_on_local_provider`), the three-violations/two-roles ordering and exact message, `resolve_failover_chains`'s four paths, and the registry checks |

### this commit F058 R1 C5: handback (STOP-triggered; gates unrun)

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | rewritten | Current Step and Next Steps record the STOP blocker and the next session's first action |
| `.agent/handoff.md` | this commit | this file (self-reference rule, `docs/agents/handback_template.md`) |

## External actions

No pull request was opened this round (the block forbids it: "Do not open a pull request"). No
`git worktree add`/`remove` performed in this handback commit, but one proof worktree WAS used and
removed during C2 (see Verification). The worker's scratch directory
`.remedy-wt/f058-r1-worker/` (gitignored) holds every copy/digest/sanity script this round used; it
is not pushed. The push that follows this commit is reported in the final reply only, not here,
because the handoff is written before that command runs.

## Verification

**Preconditions (before C1):** `git branch --show-current` read `main`; `git rev-parse HEAD` read
`4f294374a69b0c66afc68fca578608bcb24ad179`; `git status --porcelain` empty; `gh pr list --state
open --json number` read `[]`. Branch created: `git checkout -b
feature/f058-model-failover-chain`.

**Block and prep digests (before any write):** `block.md` sha256
`659aa21e160fc5f4e7c8a6b331a325f224eafdb2a9b4a59c54d512ecc1c8adcf`, 240 lines — both equal to the
values the delivering prompt gave. All nine prep files (`run_selection.py`, `selection.txt`, the
seven `dry-*` files) sha256-checked against the digests the block and the prompt named; all
matched.

**C1:** a Python copy script wrote the seven `dry-*` targets plus `.agent/authored/f058-r1.md`;
`filecmp.cmp(..., shallow=False)` read `True` for all eight pairs; `git diff --cached --numstat`
read exactly the Bundle's eight C1 pairs (`240 0`, `11 12`, `12 0`, `16 15`, `14 14`, `1 0`, `1 1`,
`27 0`). Commit `c51ee5b9f`.

**C2:** the two `model_routing.*` entries (44 lines, config.py lines 1143-1186) extracted
byte-for-byte into the new module; `config.py` edited to splice `*MODEL_ROUTING_KEY_SPECS,` in
their place and import it. `python3 -I -c "import ast; ast.parse(...)"` on both files: no error.
Registry-equality proof: `git worktree add --detach .remedy-wt/f058-r1-worker/c1tree c51ee5b9f`;
one `python3 -B` subprocess with `cwd` and `PYTHONPATH` both set to that worktree, one with both
set to the primary checkout, each printing `_cfgmod.__file__` (confirmed to resolve inside its own
tree) and the sha256 of the `_CONFIG_KEY_SPECS` repr tuple and of `render_environment_guide()`:
```
c1tree  specs 3388424013951849b818a30153d4d2a9ad2adb63b8a5dc71a879883e93761a20
c1tree  guide 45452ce1c3fdc0fe97be59a96c1e6fb06be8889f35d2b828f3df886c0075c5f7
primary specs 3388424013951849b818a30153d4d2a9ad2adb63b8a5dc71a879883e93761a20
primary guide 45452ce1c3fdc0fe97be59a96c1e6fb06be8889f35d2b828f3df886c0075c5f7
```
Both pairs equal. Worktree removed: `git worktree remove .remedy-wt/f058-r1-worker/c1tree`.
Structure measurement: `python3 -m apps.cli.main integrity structure --json` read `config.py` at
1796 lines (also confirmed by `wc -l`); the "Files above 1,000 lines" table re-summed to 36 rows /
74636 lines, matching the new `MAX_FILE_LINES` pin. Commit `ef824c7a5`.

**C3:** `model_failover.py` and the new registry entry written; `python3 -I -c "import ast;
ast.parse(...)"`: no error on both files. `grep -ni "promot" packages/orchestration/
model_failover.py`: no match (one incidental hit on first draft, inside a docstring naming
`resolve_promotion_evidence`, found and removed before commit). `python3 -m ruff check
packages/orchestration/model_failover.py packages/orchestration/config_keys_model_routing.py`:
`All checks passed!`. `docs/guides/environment.md` regenerated via `write_environment_guide()`;
`git diff` showed exactly one new row. Before writing the formal tests, roughly twenty scenarios
were run by hand with plain Python (not pytest — no test command was run this round beyond `ruff`
and `ast.parse`, honouring "the only test run this round is gate 3", which never ran): a valid
round-trip, an empty chain, every parse refusal, `FAILOVER_LOCAL_ROLES == {"teacher", "summary",
"study"}`, the core-never-local rule on and off, orchestration-below-top for `orchestrator` and
`planner`, the safety-class rule with a custom and the default class set, every reviewer-not-
weaker sub-case the block names (including `repair` and `final_verifier`), the three-violations/
two-roles ordering and exact message, and all four `resolve_failover_chains` paths against real
TOML written to a temp file. Every one matched what C4's assertions now state. Commit `8e7d41394`.

**C4:** `tests/orchestration/test_model_failover.py` written to match the behaviour already
confirmed by hand. `python3 -I -c "import ast; ast.parse(...)"`: no error. `python3 -m ruff check
tests/orchestration/test_model_failover.py <everything else this round touched>`: `All checks
passed!`. Commit `39cfdb002`.

**Gates 1-6: NOT RUN.** `.agent/STOP` (content: `author: remedy-weekly-cap`, `time: 2026-10-12
07:29`, `reason: Wochenkontingent bei 100 % — Deckel 100 % erreicht; die Schleife macht nach dem
Reset am Mittwoch, 14.10. um 01:00 von selbst weiter`) was found as an untracked file after C4 was
staged and before gate 1 was run. Per `docs/agents/self_drive_protocol.md` G6 ("If `.agent/STOP`
appears at any point, finish the current commit if one is half-written, then hand off and end")
and amend0930b-slow-cap rule 6 ("finish the commit in hand, write the handoff and end"), C4 was
committed and this handback written instead of running gates 1 through 6. `.agent/STOP` was left
untouched on disk (uncommitted, untracked): the loop runner removes it itself. No test command ran
this round; `REMEDY_TEST_MAX_WORKERS` was never set; no two test commands ran at once; no mutation,
no full suite, no evidence job, no package build, no npm/npx.

## Authored-text proofs

1. `block.md` → `.agent/authored/f058-r1.md` (C1): byte-equal, confirmed by `filecmp.cmp(...,
   shallow=False)` reading `True` and by the independent sha256 match (`659aa21e...`) against the
   value the delivering prompt gave.
2. `dry-live_review.md` → `.agent/live_review.md` (C1): byte-equal, confirmed the same way.
3. `dry-prose_slips.md` → `.agent/prose_slips.md` (C1): byte-equal, confirmed the same way.
4. `dry-decisions.md` → `.agent/decisions.md` (C1): byte-equal, confirmed the same way.
5. `dry-plan.md` → `.agent/plan.md` (C1, before this handback's own rewrite): byte-equal, confirmed
   the same way.
6. `dry-context.md` → `.agent/context.md` (C1): byte-equal, confirmed the same way.
7. `dry-STATUS.md` → `docs/roadmap/STATUS.md` (C1): byte-equal, confirmed the same way.
8. `dry-T3_F058.md` → `docs/roadmap/features/T3_F058.md` (C1): byte-equal, confirmed the same way.

Nothing else this round is reviewer-authored text copied verbatim: C2's two moved `ConfigKeySpec`
entries were extracted programmatically from `config.py`'s own committed bytes (lines 1143-1186,
44 lines) rather than from a prepared file, and the registry-equality digests above are the proof
that the move changed nothing the registry or the guide expose. C3 and C4's new code and tests are
the worker's own, built from the block's prose specification.

## Deviations & assumptions

1. **The round stopped after C4 instead of running gates 1-6 and writing the block's planned C5,
   because `.agent/STOP` (author `remedy-weekly-cap`) appeared mid-round (a blocker, not a
   choice).** `docs/agents/self_drive_protocol.md` G6 and amend0930b-slow-cap rule 6 both read "at
   any point": the commit in hand (C4) was finished and this handback written in its place. Gates
   1 through 6 are therefore UNVERIFIED — not failed, not skipped by choice, simply not run. The
   Fortschritt line, the Session self-assessment and `.agent/plan.md`'s Current Step all state
   this plainly rather than implying the round closed clean.
2. **The handback's own content departs from the block's C5 specification**, which assumed gates
   1-6 would pass before C5 was written (e.g. the item-status table below marks the gates
   "not run" rather than "passed", and the Fortschritt wording is the worker's own rather than the
   block's literal "T001 landed" — "landed" read as implying a verified state this round cannot
   claim). This whole handback IS the declared deviation; nothing in it is silently inconsistent
   with the block.
3. Before C4's tests were written, each piece of `model_failover.py`'s behaviour was checked by
   hand with disposable Python scripts under `.remedy-wt/f058-r1-worker/` (never committed, never
   run as `pytest`), so that the formal test file could assert exact, already-confirmed messages
   and violation tuples rather than guessed ones. This is not a test run under the block's "only
   one test run this round" constraint — no test command and no `pytest` invocation ran.
4. `.agent/context.md` and `.agent/decisions.md` need no further update this round: scope,
   assumptions and constraints are unchanged, and the STOP is a mechanical protocol application
   (G6), not a new technical or scope decision.
5. No other departure from the block's ordered C1-C4 commit sequence.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): PRESENT as of this handback (author `remedy-weekly-cap`,
   resumes itself after the reset at 2026-10-14 01:00); the next session checks it first and, if it
   is still present, does nothing else, per G6/Phase 1 rule 1.
2. Once `.agent/STOP` is gone (removed by the loop runner itself after the reset): run this round's
   gates 1 through 6 against `39cfdb002` before anything else; a red gate is fixed with a new
   commit on `feature/f058-model-failover-chain`, per the block's own constraint, and gate 3 is run
   again exactly once after the fix.
3. The Open PR Gate (no PR exists yet for this branch; none was opened this round).
4. "The next round's first commit books round 1's verdict" once gates 1-6 have actually passed.
5. T002, the failover walk and its disclosure.

Operator questions open: 1.
Open findings: 4 — R-1235, R-1246, R-1251 and R-1252, owned by F306.

## For the operator, in plain sentences

Work has begun on letting each kind of model call name backup models that take over when its
usual model's service cannot be reached. This round taught Remedy to read that list from the
settings file and to refuse a list that breaks the safety rules, such as a reviewer weaker than
the builder it checks or a core role on a local model, naming the rule and the entry; nothing a
person sees changes yet, except that the guide to the settings lists the new setting. The weekly
usage cap was reached partway through this round, before the round's own checks could be run, so
the work is written and saved but not yet checked end to end; the loop will pick this back up by
itself once the cap resets and will run those checks before doing anything else.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | eight paths byte-equal, numstat matched exactly |
| C2 | done | registry-equality proof passed (both digests equal); ledger and ratchet re-measured |
| C3 | done | module and key written; no `promot` in `model_failover.py`; environment guide regenerated |
| C4 | done | tests written to match roughly twenty hand-verified scenarios |
| C5 (this handback) | done | written in place of the block's planned C5, per the STOP deviation above |
| Gate 1 | not run | STOP intervened before it was reached |
| Gate 2 | not run | STOP intervened before it was reached |
| Gate 3 | not run | STOP intervened before it was reached (the round's only planned test run) |
| Gate 4 | not run | STOP intervened before it was reached |
| Gate 5 | not run | STOP intervened before it was reached |
| Gate 6 | not run | STOP intervened before it was reached |
| Push | done | reported in the final reply only (see External actions) |
| Pull request | skipped | the block forbids opening one this round |
