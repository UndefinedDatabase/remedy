# Handoff — F110 Model routing by task class, round 11

## Session

SESSION 3 of feature F110 · round 11 · rounds so far 11

## State

- Branch: `feature/f110-model-routing-by-task-class`, pushed, NO pull request open.
- Base of this round: `0d025469` (F110 R10 C7). HEAD before the handback: `4d61041e`.
- Fortschritt: THE REPAIR ROUND LANDED AND THE TIP IS GREEN AGAIN. Round 10's
  verdict was FAIL over two defects, both in TEST files; both are now registered
  and both are fixed, and NO file under `packages/` or `apps/` was edited — the
  change-set constraint is MEASURED at G8, not asserted. `R-0787` (High): the
  `_FakeConfig` double in `tests/orchestration/test_orchestrator_model_routing.py`
  asserted `key == "orchestrator.model"` and so refused
  `model_routing.task_class_tiers`, the SECOND legitimate reader round 10's wiring
  put on the fall-through path. The refusal is gone and the PROOF IT CARRIED IS
  KEPT: the stub now records every key it is asked for and answers `None` for
  everything but the operator override — `None` being the correct "no per-project
  overrides" answer — `_patch_config` builds ONE instance and returns it, and a new
  test, `TestTheOperatorOverrideKeyIsTheOneRead::test_the_operator_override_key_is_among_the_keys_read`,
  asserts positively that the override key was read. That test is RED-PROOFED at
  G6. `R-0788` (Low): `_TABLE_VALUED_KEYS` moved to the top of the config import
  list in `tests/orchestration/test_config.py`, the single change `ruff check --fix`
  produces; one insertion, one deletion, nothing else in the file touched.
  Round 10's production code is UNCHANGED — the block's constraint 7 was honoured
  and no reader was "fixed" on the production side.
- Open findings: 278 open over 349 registered and 71 resolved. Derived mechanically
  from `.agent/live_review.md`: 349 paragraphs match `^- R-\d+ — `, 71 lines match
  `^Done: R-\d+ — `, 349 − 71 = 278; zero duplicate registered ids. The count is
  UNCHANGED from round 10's 278 over 347/69 because this round registered two new
  ids AND the reviewer's round-10 verdict booked two `Done:` lines with them.
  BOTH `R-0787` AND `R-0788` STAY OPEN: C5 wrote `Landed:` lines only, and only
  reviewer-authored `Done:` text at the next gate resolves them (block constraint 6,
  measured at G4). `R-0767` stays OPEN on the same seam and was not absorbed.
- `.agent/STOP` read TWICE, per constraint 8: before the first commit
  (`test -e .agent/STOP` reported ABSENT) and again before C6
  (`ls -la .agent/STOP` reported "No such file or directory"). ABSENT both times.

## Range

Review of `0d025469`..`HEAD`.

## Commits

### 46262bf2 F110 R11 C0a: save the round 11 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f110-r11.md` | +262 / -0 | the block saved verbatim with `shutil.copyfile` from the reviewer's scratch original |

### 87adb34e F110 R11 C0b: mirror the block to last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +195 / -328 | mirrored from the COMMITTED authored copy with `shutil.copyfile` |

### bf683096 F110 R11 C1: the round 11 plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +10 / -12 | PLAN11 applied byte for byte; first substantive commit (item 23) |

### 9c86b988 F110 R11 C2: book round 10 - the verdict, two findings and the authoring slip
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +7 / -1 | RECORD10, FINDING787, FINDING788 as ONE append in ONE commit, in that order |
| `.agent/prose_slips.md` | +3 / -1 | SLIPS11 appended |

### cc32f16b F110 R11 C3: fix R-0787 - the config double records keys instead of refusing them
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_orchestrator_model_routing.py` | +49 / -6 | SPEC (a)–(e): named key constant, permissive recording stub, `_patch_config` returns one instance, the WHY docstring, the new positive test |

### fdfc7e2c F110 R11 C4: fix R-0788 - sort the config test import block
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_config.py` | +1 / -1 | SPEC (f): `_TABLE_VALUED_KEYS` moved above `ConfigKeySpec`; the ONE move, applied by hand, no formatter run |

### 4d61041e F110 R11 C5: land R-0787 and R-0788
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +5 / -1 | LANDED787 and LANDED788 appended — second append to this file this round |

### C6 (this commit) F110 R11 C6: the round 11 handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this handback; a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach /home/decodeux/Repos/remedy/remedy-review-r11-base 0d025469` | created, detached at `0d025469` |
| `git worktree remove --force /home/decodeux/Repos/remedy/remedy-review-r11-base` + `git worktree prune` | removed by exact path, pruned |
| `git worktree add --detach /home/decodeux/Repos/remedy/remedy-review-r11-red fdfc7e2c` | created, detached at `fdfc7e2c` (C4) |
| `git worktree remove --force /home/decodeux/Repos/remedy/remedy-review-r11-red` + `git worktree prune` | removed by exact path, pruned; `test -e <path>` reports PATH GONE |
| `git push -u origin feature/f110-model-routing-by-task-class` | after C6 — see Verification |

No PR was created, none exists, nothing was merged, no `gh` command was run, the
`remedy` CLI was not invoked, and no `remedy.toml` was created.

## Verification

### G1 TRANSPORT — PASS

    $ sha256sum .agent/authored/f110-r11.md .agent/last_block.md
    46c7e1c308bac396e4690b2c4418d7820f5333fd33400863b20b726273a943d2  .agent/authored/f110-r11.md
    46c7e1c308bac396e4690b2c4418d7820f5333fd33400863b20b726273a943d2  .agent/last_block.md
    exit 0
    $ wc -l .agent/authored/f110-r11.md
    262 .agent/authored/f110-r11.md

ONE digest twice. The same digest also equals the delegating prompt's stated
sha256 for the scratch original, and `shutil.copyfile` was the only transport at
both hops. Per item 37 this proves the saved copy and its mirror agree; it claims
nothing about emitted bytes, because none were emitted.

### G2 THE PLAN — PASS

    $ cmp <PLAN11 extracted by delimiter index from .agent/authored/f110-r11.md> .agent/plan.md
    exit 0 — identical
    $ wc -l .agent/plan.md
    42 .agent/plan.md            (under 50)
    $ grep -c '^## Goal' .agent/plan.md        -> 1
    $ grep -c '^## Next Steps' .agent/plan.md  -> 1

PLAN11 is 1875 bytes and already ends with one newline, so the target's
"ends WITH a newline" convention needed no adjustment; `.agent/plan.md` is 1875
bytes.

### G3 THE C2 LEDGER APPEND — PASS

Slice sizes, re-derived by delimiter index from the COMMITTED authored file:
RECORD10 4382 bytes, FINDING787 2246, FINDING788 1161, each ZERO internal
newlines. Joined by the file's own paragraph separator `\n\n` in that order:
7793 bytes.

    ARITHMETIC: 2196008 + 2 + 7793 = 2203803
    ACTUAL SIZE AFTER C2:            2203803      MATCH
    PRE-C2 CONTENT IS AN EXACT BYTE PREFIX: True
    ends with a newline AFTER the append: False   (target convention held)
    sha256 before C2: dd8ff0425280203b467fc35e44874dbc496b01bd84c31306e478d2e234297f7b
    sha256 after  C2: d313ae162fc2118333932286bbd5b10533a5e16a15722f7844d5f7004c327dfd

SECOND READER — N is COUNTED from the appended text (3), then the LAST 3
blank-line units of the WHOLE file are compared against its 3 paragraphs IN ORDER:

    unit[-3] vs paragraph 1: MATCH (len 4365 vs 4365)
    unit[-2] vs paragraph 2: MATCH (len 2232 vs 2232)
    unit[-1] vs paragraph 3: MATCH (len 1155 vs 1155)
    SECOND READER on the real file: ACCEPT

(The unit lengths are character counts; the byte counts above are the UTF-8
encodings of the same three paragraphs.)

NEGATIVE CONTROL — one byte flipped INSIDE THE FIRST appended paragraph, in
memory only, the on-disk file never written:

    byte at offset 2196020 was ' ' -> 'Z'
    unit[-3] vs paragraph 1: MISMATCH
    unit[-2] vs paragraph 2: MATCH
    unit[-1] vs paragraph 3: MATCH
    SECOND READER on the mutated bytes: REJECT
    on-disk file untouched, bytes: 2203803

RECORD10 HEADER COUNT. The header string was COPIED from the extracted slice, not
retyped: `Gate: F110 R10 — the round 10 entry.` — the separator after "R10" is
U+2014 EM DASH, verified `'—' in header -> True`.

    before C2: grep -c -F -f <header file> .agent/live_review.md  ->  0
    after  C2: grep -c -F -f <header file> .agent/live_review.md  ->  1

### G4 THE C5 LEDGER APPEND AND prose_slips — PASS

Second append to `.agent/live_review.md` in one round; both sizes stated so the
second is shown building on the first:

    SIZE AFTER C2 (the C5 base): 2203803, ends with newline: False
    LANDED787 276 bytes, LANDED788 191 bytes, joined by '\n\n': 469 bytes
    ARITHMETIC: 2203803 + 2 + 469 = 2204274
    ACTUAL SIZE AFTER C5:           2204274      MATCH
    THE C2 CONTENT IS AN EXACT BYTE PREFIX: True
    still ends without a newline: True
    sha256 after C5: 829d4793a8e6394dfca9dc1906e28cefd09bfb6cb861c53ab92c00832b6a1e4e

`.agent/prose_slips.md`, byte-equality only per the gate budget:

    58680 + 2 + 1262 = 59944   ACTUAL 59944   MATCH
    base is an exact byte PREFIX: True   ends without a newline: True

Constraint 6 MEASURED rather than asserted:

    $ grep -c '^Landed: R-0787 — ' .agent/live_review.md  -> 1
    $ grep -c '^Landed: R-0788 — ' .agent/live_review.md  -> 1
    $ grep -c '^Done: R-0787' .agent/live_review.md       -> 0
    $ grep -c '^Done: R-0788' .agent/live_review.md       -> 0

### G5 THE FIX, MEASURED AND RUN — PASS

    $ git show --numstat --format= cc32f16b
    49      6       tests/orchestration/test_orchestrator_model_routing.py
    $ git show --numstat --format= fdfc7e2c
    1       1       tests/orchestration/test_config.py
    $ python3 -c "import ast; ..."   over both real files
    ast.parse OK: tests/orchestration/test_orchestrator_model_routing.py
    ast.parse OK: tests/orchestration/test_config.py
    exit 0

EVERY DELETED LINE, VERBATIM, WITH ITS REGION.

C3, `tests/orchestration/test_orchestrator_model_routing.py` — 6 deletions:

  region `_FakeConfig` class docstring:

        """The one method ``resolve_orchestrator_model`` calls on a config object."""

  region `_FakeConfig.get` body (the refusal R-0787 names, and its return):

            assert key == "orchestrator.model", f"unexpected config key {key!r}"
            return self._value

  region `_patch_config` signature and its docstring summary line:

    def _patch_config(monkeypatch, value) -> None:
        """Make ``orchestrator.model`` answer ``value``.

  region `_patch_config` body, the per-call construction (c) forbids:

            lambda: _FakeConfig(value),

C4, `tests/orchestration/test_config.py` — 1 deletion, region: the
`from packages.orchestration.config import (...)` list, the old position of the
moved name:

        _TABLE_VALUED_KEYS,

THE PREVIOUSLY-RED SUITE, at C4 (primary checkout, `__pycache__` purged, `-B`):

    $ python3 -B -m pytest tests/orchestration/test_orchestrator_model_routing.py -q
    ....................                                                     [100%]
    20 passed in 0.28s
    EXIT CODE: 0

THE SAME COMMAND AT THE BASE `0d025469`, in the disposable worktree
`remedy-review-r11-base`, `role_config` module `__file__` printed from inside it as
`/home/decodeux/Repos/remedy/remedy-review-r11-base/packages/orchestration/role_config.py`:

    $ python3 -B -m pytest tests/orchestration/test_orchestrator_model_routing.py -q
    E       AssertionError: unexpected config key 'model_routing.task_class_tiers'
    tests/orchestration/test_orchestrator_model_routing.py:38: AssertionError
    FAILED tests/orchestration/test_orchestrator_model_routing.py::TestTheAnswerIsAlwaysUsable::test_the_fall_through_answer_is_a_non_empty_string
    1 failed, 18 passed in 0.23s
    EXIT CODE: 1

So the repair is shown against the failure it repairs: 1 failed / 18 passed / exit 1
at the base, exactly the reviewer's reading, becomes 20 passed / exit 0 at C4.

THE STUB'S RECORDING, SHOWN WORKING RATHER THAN ASSERTED — one fall-through call
(operator override unset, `resolve_role_config` NOT patched, so the real
fall-through path runs):

    returned: 'muse-glimmer:latest'
    keys the stub RECORDED: ['orchestrator.model', 'model_routing.task_class_tiers']
    override key present: True

Both keys, in that order — the exact mechanism `R-0787` describes, now recorded
instead of refused.

### G6 THE RED PROOF — PASS

Disposable worktree `/home/decodeux/Repos/remedy/remedy-review-r11-red`, detached
at C4 `fdfc7e2c`, NEVER cd-ed into (every command ran with `cwd=` set),
`__pycache__` purged before every run, `python3 -B` throughout. Module identity
printed from INSIDE the worktree:

    role_config __file__:  /home/decodeux/Repos/remedy/remedy-review-r11-red/packages/orchestration/role_config.py
    test module __file__:  /home/decodeux/Repos/remedy/remedy-review-r11-red/tests/orchestration/test_orchestrator_model_routing.py

CONTROL:

    $ python3 -B -m pytest tests/orchestration/test_orchestrator_model_routing.py -q
    ....................                                                     [100%]
    20 passed in 0.26s
    EXIT CODE: 0

ONE MUTATION — `resolve_orchestrator_model` stops reading the operator override
key; the `get_config().get(...)` call's result is replaced with `None`
(occurrence count asserted == 1 before the write):

    -     configured = get_config().get("orchestrator.model")
    +     configured = None  # MUTATION: stop reading the operator override key

MUTANT RUN:

    $ python3 -B -m pytest tests/orchestration/test_orchestrator_model_routing.py -q
    3 failed, 17 passed in 0.28s
    EXIT CODE: 1

ONE RAW pytest line, verbatim, beside the parsed set — the node id is the SECOND
whitespace-separated token, which is how it was parsed here:

    RAW:    FAILED tests/orchestration/test_orchestrator_model_routing.py::TestConfiguredKeyWins::test_configured_value_is_returned
    TOKEN2: tests/orchestration/test_orchestrator_model_routing.py::TestConfiguredKeyWins::test_configured_value_is_returned
    raw FAILED lines: 3   parsed ids: 3   AGREEMENT: True

FULL LIST OF RED TEST IDS:

    tests/orchestration/test_orchestrator_model_routing.py::TestConfiguredKeyWins::test_configured_value_is_returned
    tests/orchestration/test_orchestrator_model_routing.py::TestConfiguredKeyWins::test_configured_value_wins_over_the_role_config_answer
    tests/orchestration/test_orchestrator_model_routing.py::TestTheOperatorOverrideKeyIsTheOneRead::test_the_operator_override_key_is_among_the_keys_read

THE NEW DISCRIMINATOR IS AMONG THEM — `True`. The mutation reaches it: with the
override key never asked for, `keys_read` no longer contains it and the positive
assertion fails, which is exactly the proof the deleted refusal used to carry.

PRIMARY CHECKOUT, read immediately after the mutation:

    $ git -C /home/decodeux/Repos/remedy status --porcelain
    (empty)

REVERT, by exact path, INSIDE the worktree:

    $ git -C .../remedy-review-r11-red checkout -- packages/orchestration/role_config.py
    $ git -C .../remedy-review-r11-red status --porcelain
    (empty)
    $ python3 -B -m pytest tests/orchestration/test_orchestrator_model_routing.py -q
    20 passed in 0.26s
    EXIT CODE: 0        — back to the control's count

### G7 THE SUITES — PASS, seven invocations, serial, all exit 0

| Command | Reviewer's reading at `0d025469` | Measured here | Exit |
|---|---|---|---|
| `python3 -B -m pytest tests/orchestration/test_orchestrator_model_routing.py -q` | 1 failed / 18 passed | **20 passed** | 0 |
| `python3 -B -m pytest tests/orchestration/test_config.py -q` | 74 | 74 passed | 0 |
| `python3 -B -m pytest tests/orchestration/test_role_config.py -q` | 92 | 92 passed | 0 |
| `python3 -B -m pytest tests/orchestration/test_model_routing.py -q` | 391 passed, 3 skipped | 391 passed, 3 skipped, 1 warning | 0 |
| `python3 -B -m pytest tests/orchestration/test_teacher_model.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_job_role_routing.py tests/cli/test_teach_cmd.py -q` | 68 | 68 passed | 0 |
| `python3 -B -m pytest tests/docs/ -q` | 295 | 295 passed | 0 |
| `python3 -B -m pytest tests/cli/test_golden_path.py -q` | 42 (canary) | 42 passed | 0 |

DIFFERENCES EXPLAINED. Only the first row moved, and it moved by design:
1 failed / 18 passed / exit 1 becomes 20 passed / exit 0 — the repaired test plus
the ONE new test SPEC (c) adds, 19 → 20, and nothing else. The 1 warning on
`test_model_routing.py` is the `UserWarning` that suite raises on purpose for the
refused-override case and is present at the base too; the reviewer's bracket
recorded pass/skip counts only. Every other row matches the reviewer's bracket
exactly.

### G8 THE TREE, THE COMMITS AND THE SWEEP — PASS

    $ git status --porcelain      (immediately before C6 was staged)
    (empty)
    $ git ls-files .remedy-wt
    (empty)
    $ git worktree list
    /home/decodeux/Repos/remedy                                  4d61041e [feature/f110-model-routing-by-task-class]
    /home/decodeux/Repos/remedy/.remedy-wt/job-48a379ab5ca44ec5  f0e6b9a3 [remedy/job-48a379ab5ca44ec5]
    /home/decodeux/Repos/remedy/.remedy-wt/job-5e91e080219342d9  9fdb3b4b [remedy/job-5e91e080219342d9]
    /home/decodeux/Repos/remedy/.remedy-wt/job-7d1c93e2dc98415a  f0e6b9a3 [remedy/job-7d1c93e2dc98415a]
    /home/decodeux/Repos/remedy/.remedy-wt/job-98e9364a83a34872  21a45836 [remedy/job-98e9364a83a34872]
    /home/decodeux/Repos/remedy/.remedy-wt/job-f76686b8435640e9  4b49af98 [remedy/job-f76686b8435640e9]

No worktree of THIS round's making survives; the five `.remedy-wt/job-*` entries are
unrelated pre-existing job worktrees and were never touched.

THE CHANGE-SET CONSTRAINT, MEASURED:

    $ git diff --stat 0d025469..4d61041e -- packages/ apps/ docs/
    (EMPTY — no file under packages/, apps/ or docs/ changed)

    $ git diff --name-only 0d025469..4d61041e
    .agent/authored/f110-r11.md
    .agent/last_block.md
    .agent/live_review.md
    .agent/plan.md
    .agent/prose_slips.md
    tests/orchestration/test_config.py
    tests/orchestration/test_orchestrator_model_routing.py

Exactly the block's change set, minus `.agent/handoff.md` which C6 adds.

PER-COMMIT INSERTIONS, the `+` column only, cell by cell against the Commits table
above, for every commit BEFORE the handback commit:

| Commit | Insertions | Commits-table cells | Under the 500 cap |
|---|---|---|---|
| `46262bf2` C0a | 262 | +262 | yes |
| `87adb34e` C0b | 195 | +195 | yes |
| `bf683096` C1 | 10 | +10 | yes |
| `9c86b988` C2 | 10 | +7 and +3 | yes |
| `cc32f16b` C3 | 49 | +49 | yes |
| `fdfc7e2c` C4 | 1 | +1 | yes |
| `4d61041e` C5 | 5 | +5 | yes |

Every cell agrees and every commit is under the AGENTS.md 500-insertion cap. The
handback commit's own numbers appear in neither place, per the gate. No commit in
this round is oversize, so no inseparability declaration is owed.

## Authored-text proofs

| Slice | Target | Result |
|---|---|---|
| the whole block | `.agent/authored/f110-r11.md` | `shutil.copyfile` from the reviewer's scratch original; sha256 `46c7e1c3…a943d2` equals the prompt's stated digest |
| the whole block | `.agent/last_block.md` | `shutil.copyfile` from the COMMITTED authored file; same sha256, G1 |
| PLAN11 | `.agent/plan.md` | `cmp` against the delimiter-index extraction, exit 0 (G2) |
| RECORD10 | `.agent/live_review.md` | byte arithmetic + prefix + second reader with negative control (G3) |
| FINDING787 | `.agent/live_review.md` | same append, paragraph 2 of 3, second reader MATCH (G3) |
| FINDING788 | `.agent/live_review.md` | same append, paragraph 3 of 3, second reader MATCH (G3) |
| SLIPS11 | `.agent/prose_slips.md` | byte equality 58680 + 2 + 1262 = 59944, base an exact prefix (G4) |
| LANDED787 | `.agent/live_review.md` | byte arithmetic + C2 content an exact prefix (G4) |
| LANDED788 | `.agent/live_review.md` | same append (G4) |

Every slice was extracted BY DELIMITER INDEX from the COMMITTED
`.agent/authored/f110-r11.md`, marker lines excluded, with a script; none was
retyped and none was taken from the delegating prompt.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block | done | |
| C0b mirror the block | done | |
| C1 PLAN11 | done | |
| C2 findings persist first | done | RECORD10 + FINDING787 + FINDING788 + SLIPS11, one commit, before any fix |
| C3 fix R-0787 | done | |
| C4 fix R-0788 | done | |
| C5 Landed lines | done | `Landed:` only; no `Done:` written (constraint 6) |
| C6 handback | done | this file |
| R-0787 | done | fixed in C3, landed in C5; stays OPEN in the ledger until the reviewer writes `Done:` |
| R-0788 | done | fixed in C4, landed in C5; stays OPEN in the ledger until the reviewer writes `Done:` |
| SPEC (a) named key constant | done | `ORCHESTRATOR_MODEL_CONFIG_KEY = "orchestrator.model"`, module level, used in the stub |
| SPEC (b) stub answers instead of refusing | done | configured value for the override key, `None` for every other, `keys_read` records all |
| SPEC (c) proof kept as a positive test | done | `TestTheOperatorOverrideKeyIsTheOneRead`; `_patch_config` builds ONE instance and returns it |
| SPEC (d) docstring says WHY | done | `_FakeConfig` docstring names the refusal, the second legitimate reader and where the proof moved |
| SPEC (e) no other test edited | done | 6 deletions, all inside `_FakeConfig`/`_patch_config`, none in a test body; count rose 19 → 20 |
| SPEC (f) the one import move | done | `_TABLE_VALUED_KEYS` above `ConfigKeySpec`; +1/−1, no import added or removed, no formatter run |
| G1 transport | done | one digest twice, 262 lines |
| G2 the plan | done | `cmp` exit 0, 42 lines, 1 and 1 |
| G3 C2 ledger append | done | arithmetic, prefix, no trailing newline, second reader ACCEPT, negative control REJECT, header 0 → 1 |
| G4 C5 append and prose_slips | done | both sizes, prefix, byte equality, `Landed:` 1/1 and `Done:` 0/0 |
| G5 the fix measured and run | done | numstat, `ast.parse`, all 7 deleted lines quoted, 20 passed at C4 vs 1 failed/18 at base, recorded keys printed |
| G6 red proof | done | control 20/exit 0, mutant 3 failed/exit 1, discriminator among the red ids, revert restores 20 |
| G7 the suites | done | seven invocations, serial, all exit 0 |
| G8 tree, commits, sweep | done | status empty, `ls-files .remedy-wt` empty, `packages/ apps/ docs/` diff EMPTY, every commit under the cap |

## Deviations & assumptions

The block's ordered commit sequence was followed EXACTLY: C0a, C0b, C1, C2, C3, C4,
C5, C6 — no extra commit, none dropped, no reordering. C3 precedes C4 precedes C5
(constraint 3) and C2 is the first commit touching the ledger, before any fix
(constraint 2).

- **D1 — the G3 negative control ran IN MEMORY, not in a worktree.** Constraint 9
  confines DESTRUCTIVE verification to a disposable worktree. The byte flip was
  performed on a `bytearray` copy of the file's bytes and never written to disk;
  the on-disk size was re-read afterwards and is unchanged at 2203803. No worktree
  was created for it because nothing on disk was ever at risk. Declared rather than
  silently done.
- **D2 — the G7 commands were run as `python3 -B -m pytest …`.** The block spells
  them `pytest …`. The `-B` form is what this environment's rules require
  (`__pycache__` purged, no bytecode written); the module set, the node selection
  and the `-q` flag are identical. Same for the G5 and G6 runs.
- **D3 — two throwaway helper files were written under the gitignored
  `remedy-review-r9-scratch/`** — `header.txt`, holding the RECORD10 header copied
  from the extracted slice so `grep -F` could match the U+2014 em dash without any
  retyping, and `plan11.extract`, the PLAN11 extraction `cmp` read. Both were
  removed afterwards BY EXACT PATH. Neither is in the repository's index; the tree
  was clean before C6.
- **D4 — no ruff gate was added and ruff was never run** (constraint 5). SPEC (f)
  was applied as a hand edit of the one import line. The reviewer's own ruff run is
  what confirms `I001` is cleared; nothing in this handback claims it.
- **D5 — no discrepancy was found between the block and reality.** Every measured
  constant matched: `.agent/live_review.md` 2196008 bytes without a trailing
  newline, `.agent/prose_slips.md` 58680 the same, `.agent/plan.md` 2011 bytes with
  one; the base reading 1 failed / 18 passed at `0d025469`; the sole change
  `ruff check --fix` produces; and the "exactly one test is red, because the other
  fall-through cases patch `resolve_role_config` itself" claim, confirmed by the
  base run's single FAILED line. Recorded because a silent "no deviations" cannot
  be told apart from a check not made.
- Assumption, stated because it is load-bearing for G6: the mutation the block
  orders — "replace the `get_config().get(...)` call's result with `None`" — was
  implemented as `configured = None`, which removes the call entirely and so
  genuinely stops the override key from being read. Had it been implemented as
  `get_config().get(...) and None`, the key would still have been recorded and the
  new test would have stayed green, proving nothing.
- `.agent/decisions.md` was NOT touched (constraint 4). `.agent/candidates.md` was
  not touched and is unchanged. `.agent/context.md` needed no update: the branch,
  scope and constraints it records are the same feature and the same branch.

## Next

The promotion-evidence round: read the evidence map from configuration so a
documented benchmark run can license a cheaper tier — the last unbuilt clause of
T003 — on a tip that is now green at every gate this round ran.
