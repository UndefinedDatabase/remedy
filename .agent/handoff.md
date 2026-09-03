# Handoff — F110 Model routing by task class, round 10

## Session

SESSION 3 of feature F110 · round 10 · rounds so far 10

## State

- Branch: `feature/f110-model-routing-by-task-class`, pushed, NO pull request open.
- Base of this round: `a1368633` (F110 R9 C5). HEAD before the handback: `e1da68d8`.
- Fortschritt: THE CONFIGURATION ROUND LANDED, and one BLOCKED ITEM came with it.
  `config.py` now understands TABLE-VALUED keys — a spec whose `value_type is dict`
  resolves to the WHOLE TOML sub-table as one value through the precedence chain it
  already had, and the stop-set `_flatten_toml` consults is DERIVED FROM THE
  REGISTRY (`_TABLE_VALUED_KEYS`), never hand-listed. F110 registers
  `model_routing.task_class_tiers` as the first such key, default `None` and not
  `{}`. `role_config.resolve_effective_task_class_tiers` reads that table and lays
  it over the seed mapping through round 6's `build_effective_task_class_tiers`, and
  `resolve_routed_call_evidence` passes the result to `route_role_call` as
  `effective_tiers`, so a per-project override reaches every routed call through one
  argument and no second path. A REFUSED map warns once, names the config key and
  every violated rule, and routes against the SHIPPED table — DECISION F110 D5,
  recorded this round. Round 9's PASS verdict and its two prose slips are booked.
  THE BLOCKED ITEM: one EXISTING test, untouched per constraint 8, is now RED —
  see "Blocked item" below and deviation D1.
- Open findings: 278 open over 347 registered and 69 resolved — UNCHANGED, carried
  from the round-9 verdict booked this round; this round minted no id and resolved
  none. `R-0767` stays OPEN on the same seam and was not absorbed.
- `.agent/STOP` read TWICE, per constraint 10: before the first commit (`ls -la
  .agent/STOP` reported "No such file or directory") and again before C7 (same).
  ABSENT both times.

## Blocked item — one existing test is RED and was NOT edited

`tests/orchestration/test_orchestrator_model_routing.py::TestTheAnswerIsAlwaysUsable::test_the_fall_through_answer_is_a_non_empty_string`
FAILS at `e1da68d8`. It is GREEN at the block's base `a1368633` — measured in a
disposable worktree, 19 passed — so this round causes it.

CAUSE, read from the traceback and not guessed. That module's `_FakeConfig` stub
asserts the ONLY key `resolve_orchestrator_model` ever asks the config for:

    def get(self, key):
        assert key == "orchestrator.model", f"unexpected config key {key!r}"

SPEC (e) and (g) make `resolve_routed_call_evidence` read
`model_routing.task_class_tiers` from the config on every routed call, and
`resolve_orchestrator_model`'s FALL-THROUGH branch calls the real
`resolve_role_config("orchestrator")`. The stub therefore receives a second key and
raises. The failing assertion is:

    AssertionError: unexpected config key 'model_routing.task_class_tiers'

WHY IT WAS NOT REPAIRED. Constraint 8 is explicit: "If you find an existing test
that must change, STOP, do not change it, and report it as a blocked item in the
handback." The test was not edited, renamed, deleted or skipped, and the production
code was not bent to keep a stub's assumption true. THE STUB'S ASSUMPTION IS NOW
FALSE ABOUT PRODUCTION, which is what the test is reporting; the shipped behaviour
is the one SPEC (e), (g) and DECISION F110 D5 ordered, and the G5 probe shows it
answering correctly.

WHY THE BLOCK'S CONSTRAINT-8 MEASUREMENT DID NOT CATCH IT: constraint 8 records
that the reviewer applied "this round's `config.py` change" and ran
`test_config.py`, `test_role_config.py` and `test_model_routing.py`. The break is
caused by the `role_config.py` change (C4), not the `config.py` one, and
`test_orchestrator_model_routing.py` is in NEITHER the measured file set nor the
measured suite set. The block's own G7 list DOES reach it, in the 87-test unmoved
group, which is where it surfaced.

THE ONE-LINE REPAIR A FUTURE ROUND SHOULD ORDER (not applied here): widen
`_FakeConfig.get` to answer `None` for any key other than `orchestrator.model`
instead of asserting — the fake would then model a config object rather than a
single-key oracle. That is a change to an existing test and needs an explicit order.

## Range

Review of `a1368633..HEAD`.

## Commits

### 9eb79b10 F110 R10 C0a: save the round 10 step block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f110-r10.md` | +395 / -0 | the block saved by `shutil.copyfile`, byte-identical by construction |

### b9d32e3d F110 R10 C0b: mirror the block to last_block
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +315 / -399 | the mirror, copied from the COMMITTED authored file by `shutil.copyfile` |

### 54574326 F110 R10 C1: the plan for the configuration round
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +15 / -17 | PLAN10 applied; first substantive commit, item 23 |

### 36ac459f F110 R10 C2: book round 9 - the verdict, two prose slips and DECISION D5
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +3 / -1 | RECORD9 appended — the round 9 PASS verdict |
| `.agent/prose_slips.md` | +5 / -1 | SLIPS10 appended — the two round 9 prose slips |
| `.agent/decisions.md` | +55 / -0 | DECISION5 appended — DECISION F110 D5 |

### 9f609b21 F110 R10 C3: config.py learns table-valued keys and registers F110's
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/config.py` | +85 / -5 | SPEC (a)-(d): the flatten stop-set derived from the registry, the F110 key, the `dict` validate branch, the docstring paragraph |

### 76658375 F110 R10 C4: route against the configured effective task-class table
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/role_config.py` | +85 / -3 | SPEC (e)-(h): `resolve_effective_task_class_tiers`, the `OverrideRefused` catch, the seam's `effective_tiers` argument |

### e004848f F110 R10 C5: the config surface and the configured routing layer
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_config.py` | +159 / -0 | SPEC (i)-(k): the table resolves as one dict, precedence on a table, shape-only validation |
| `tests/orchestration/test_role_config.py` | +209 / -0 | SPEC (l)-(n): a legal override reaches a routed call, an illegal one is refused and routes seeded, config resolution survives |

### e1da68d8 F110 R10 C6: document the table-valued model routing key
| Path | +/- | Reason |
|---|---|---|
| `docs/system/remedy-toml-configuration-system-v0.md` | +27 / -0 | SPEC (o): the new key's row, the TOML example, hard rules win, TOML-only |

### <this commit> F110 R10 C7: the round 10 handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewrite | this file; a handoff cannot table the commit that writes it |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save block | done | |
| C0b mirror block | done | |
| C1 PLAN10 | done | |
| C2 RECORD9 / SLIPS10 / DECISION5 | done | |
| C3 production config.py | done | |
| C4 production role_config.py | done | |
| C5 tests | done | |
| C6 docs | done | |
| C7 handback | done | this commit |
| SPEC (a) table keys are a KIND | done | stop-set derived from the registry, not hand-listed |
| SPEC (b) F110's key registered | done | `dict`, default `None`, env var declared |
| SPEC (c) `validate_config` dict branch | done | shape only; no `model_routing` import added |
| SPEC (d) module docstring paragraph | done | Public API list unchanged in config.py |
| SPEC (e) effective table read | deviated | non-`Mapping` value treated as nothing configured — deviation D2 |
| SPEC (f) refusal warns, routes seeded | done | one `UserWarning` per resolution, key + every rule named |
| SPEC (g) seam routes against it | done | `effective_tiers` passed; still swallows exactly one exception |
| SPEC (h) provider/model/effort untouched | done | measured by G8's empty `packages/`+`apps/` sweep and by test (n) |
| SPEC (i) table resolves as ONE dict | done | |
| SPEC (j) unset -> None, PROJECT over USER | done | |
| SPEC (k) non-string entry reported | done | |
| SPEC (l) legal override reaches a routed call | done | class/role/tier DERIVED from `ROLE_TASK_CLASSES` + `TASK_CLASS_TIERS` |
| SPEC (m) illegal override refused, rule named | done | rule asserted by READING the constant |
| SPEC (n) config faults do not break resolution | done | |
| SPEC (o) documentation | done | |
| G1 transport | done | ONE digest twice |
| G2 the plan | done | `cmp` exit 0, 44 lines |
| G3 ledger append forensics | done | five readings, negative control REJECTS |
| G4 decisions append forensics | done | five readings + prose_slips byte equality |
| G5 production files measured and run | done | |
| G6 the red proof | done | control green, 4 mutations all red, all reverts back to control |
| G7 the suites | deviated | 6 of 7 exit 0; the 87-group is 1 failed / 86 passed — the blocked item |
| G8 tree, commits, sweep | done | |

## External actions

- `git worktree add --detach /home/decodeux/Repos/remedy/remedy-review-r10-wt e004848f`
  — created for G6. `git worktree remove <same exact path>` then `git worktree
  prune`; `ls -d` on that exact path afterwards: "No such file or directory".
- `git worktree add --detach /home/decodeux/Repos/remedy/remedy-review-r10-base a1368633`
  — created to measure the blocked item at BASE. `git worktree remove <same exact
  path>` then `git worktree prune`; `git worktree list | grep -c remedy-review-r10`
  afterwards: `0`.
- `git push -u origin feature/f110-model-routing-by-task-class` — see the
  Verification transcript.
- No pull request created, edited or merged. No `gh` command run.
- `remedy` CLI: NOT run (refused in this sandbox). `ruff`: NOT run — constraint 5
  orders no lint gate and the reviewer lints instead.

## Verification

Eight gates, each with its real command and its real exit code.

### G1 TRANSPORT — PASS

    $ sha256sum .agent/authored/f110-r10.md .agent/last_block.md
    9af2d6cef398ae7fe766cf0a23ee1c4d9901b190c67508620740ec229bed1dae  .agent/authored/f110-r10.md
    9af2d6cef398ae7fe766cf0a23ee1c4d9901b190c67508620740ec229bed1dae  .agent/last_block.md
    $ wc -l .agent/authored/f110-r10.md
    395 .agent/authored/f110-r10.md

ONE digest twice, 395 lines. Per `docs/agents/planner_reviewer_prompt.md` item 37
this proves the saved copy and its mirror agree and claims NOTHING about the
emitted bytes. The delegation prompt's stated sha256 for the scratch original is
the same digest, and `shutil.copyfile` produced both files from it.

### G2 THE PLAN — PASS

    $ cmp remedy-review-r10-scratch/plan10.txt .agent/plan.md && echo "CMP EXIT 0"
    CMP EXIT 0
    $ wc -l .agent/plan.md
    44 .agent/plan.md          (under 50)
    $ grep -c '^## Goal' .agent/plan.md
    1
    $ grep -c '^## Next Steps' .agent/plan.md
    1

The compared file is PLAN10 extracted by delimiter index from the COMMITTED
`.agent/authored/f110-r10.md` plus the one trailing newline the target's own
convention takes.

### G3 THE LEDGER APPEND, `.agent/live_review.md` — PASS

    $ python3 -B remedy-review-r10-scratch/append_forensics.py
    .agent/live_review.md
      (1) arithmetic  2190200 + 2 + 5806 + 0 = 2196008   real = 2196008   AGREE=True
      (2) base is an exact byte PREFIX: True
      (3) ends with newline: False (convention: False)  trailing bytes=b'en.'
      (4) SECOND READER: N counted from the slice = 1; last 1 blank-line units of
          the file match IN ORDER: True
      (5) NEGATIVE CONTROL: flipped byte at offset 2180361 of the file (' ' -> 'Z'),
          inside the FIRST appended paragraph; second reader accepts: False
          (must be False)

    RECORD9 header, taken from the slice: 'Gate: F110 R9 —'
      lines matching it in .agent/live_review.md AFTER C2: 1
      lines matching it BEFORE C2 (at a1368633): 0

The header string is SLICED OUT of the extracted RECORD9 (`record9[:record9.index(
"—") + 1]`), never retyped, so the U+2014 EM DASH after "R9" is the slice's own
byte. Exit code 0.

### G4 THE DECISIONS APPEND, `.agent/decisions.md` — PASS

    .agent/decisions.md
      (1) arithmetic  734845 + 1 + 3157 + 1 = 738004   real = 738004   AGREE=True
      (2) base is an exact byte PREFIX: True
      (3) ends with newline: True (convention: True)  trailing bytes=b'h.\n'
          exactly ONE trailing newline: True
      (4) SECOND READER: N counted from the slice = 7; last 7 blank-line units of
          the file match IN ORDER: True
      (5) NEGATIVE CONTROL: flipped byte at offset 731628 of the file ('C' -> 'Z'),
          inside the FIRST appended paragraph; second reader accepts: False
          (must be False)

    DECISION5 header prefix, taken from the slice: '## DECISION F110 D5 '
      grep -c '^## DECISION F110 D5 ' AFTER C2: 1
      grep -c '^## DECISION F110 D5 ' BEFORE C2 (at a1368633): 0

    .agent/prose_slips.md
      BYTE EQUALITY final == before + 2 newlines + SLIPS10: True
      base is an exact byte PREFIX: True
      final bytes = 58680

READING (4) FAILED ON ITS FIRST RUN AND THE FIRST READING IS DECLARED RATHER THAN
QUIETLY REPLACED — this is the round 9 lesson (SLIPS10 entry 2) applied to my own
harness. The first version compared the file's last 7 blank-line units against the
slice's 7 and reported False. The raw bytes were printed before any conclusion was
drawn: file tail `'pagate,\nand by deleting this paragraph.\n'` against slice tail
`'opagate,\nand by deleting this paragraph.'`. The ONLY difference is the TARGET's
own trailing newline, which constraint 4 assigns to the target and not to the
slice. The reader now strips that one byte before splitting, and the arithmetic in
(1) — which counts the newline explicitly — was correct throughout.

### G5 THE PRODUCTION FILES, MEASURED AND RUN — PASS

    $ git show --numstat --format="%H %s" 9f609b21
    9f609b211fe25eaa7e544dc5d40c1bda62c79662 F110 R10 C3: ...
    85      5       packages/orchestration/config.py
    $ git show --numstat --format="%H %s" 76658375
    7665837551c8f269ec5117e596b50b7c49cf0b7b F110 R10 C4: ...
    85      3       packages/orchestration/role_config.py

    $ python3 -c "ast.parse over the REAL files"
    packages/orchestration/config.py ast.parse OK, top-level nodes 37
    packages/orchestration/role_config.py ast.parse OK, top-level nodes 21

EVERY DELETED LINE, VERBATIM, WITH ITS REGION — 8 in total, 5 + 3.

C3, `packages/orchestration/config.py`:

    -    value_type supports: str, int, float, bool, list.
        region: the ConfigKeySpec docstring; replaced by the same list plus `dict`.
    -def _flatten_toml(d: dict[str, Any], prefix: str = "") -> dict[str, Any]:
        region: the _flatten_toml signature; replaced by a 3-parameter signature.
    -        if isinstance(v, dict):
    -            result.update(_flatten_toml(v, f"{full_key}."))
        region: the _flatten_toml recursion; the stop-set condition is added and the
        set is threaded into the recursive call.
    -    """Validate config values against key specs. Returns list of warnings."""
        region: the validate_config docstring; replaced by the same sentence plus
        the shape-only paragraph.

C4, `packages/orchestration/role_config.py`:

    -tier into a model id will not find it, and that absence is deliberate.
        region: the module docstring's "recording, not selecting" paragraph; the
        sentence is kept WORD FOR WORD and two sentences are added after it.
    -    promoted it come from that ONE seam and cannot disagree with it.
        region: the resolve_routed_call_evidence docstring; sentence kept, the
        effective-table sentence added after it.
    -        return route_role_call(role, originating_task_class)
        region: the seam call; replaced by the 3-argument form.

NO LINE OF SHIPPED LOGIC WAS REMOVED. Seven of the eight deletions are prose lines
that reappear with text added; the eighth is the seam call gaining its argument.

THE SHIPPED CODE RUN, against TOML written to `tempfile.mkdtemp()` — OUTSIDE the
repository root, and no `remedy.toml` created in it:

    $ python3 -B remedy-review-r10-scratch/g5_probe.py
    scratch dir: /tmp/f110-r10-g5-3zpljkpu
    scratch is OUTSIDE the repository root: True
    no remedy.toml in the repository root: True

    1. A CONFIGURED TABLE
       toml written: [remedy.model_routing.task_class_tiers] | summarize = "mid"
       RETURNED value : {'summarize': 'mid'}
       RETURNED source: ConfigSource.PROJECT
       load_report.warnings: []

    2. validate_config warnings list
       well-formed table -> []   (must be empty)
       non-string entry {'summarize': 3} ->
         ["model_routing.task_class_tiers: expected string entries, got 'summarize' = 3"]

    3. THE EFFECTIVE TABLE in three states, and the routed_call a declared role gets
       [NO CONFIG]
         effective table  : {'format': 'cheap', 'extract': 'cheap', 'summarize':
           'cheap', 'boilerplate': 'cheap', 'standard_build': 'mid',
           'standard_review': 'mid', 'architecture': 'top', 'mission': 'top',
           'vision': 'top', 'prompt_authoring_for_other_agents': 'top'}
         is the SHIPPED table object: True
         routed_call('summary') : {'task_class': 'summarize', 'tier': 'cheap',
           'reason': 'seed_mapping', 'promoted_by': None}
         warnings emitted : 0
       [LEGAL OVERRIDE summarize=mid]
         effective table  : ... 'summarize': 'mid' ...  (every other class unmoved)
         is the SHIPPED table object: False
         routed_call('summary') : {'task_class': 'summarize', 'tier': 'mid',
           'reason': 'per_project_override', 'promoted_by': None}
         warnings emitted : 0
       [ILLEGAL OVERRIDE mission=cheap]
         effective table  : ... 'mission': 'top' ...   (the SHIPPED table)
         is the SHIPPED table object: True
         routed_call('orchestrator') : {'task_class': 'mission', 'tier': 'top',
           'reason': 'seed_mapping', 'promoted_by': None}
         warnings emitted : 2   (one per resolve_* call the probe makes; see below)

    4. FULL TEXT of the warning the illegal map produces
       category: UserWarning
       text    : model_routing.task_class_tiers: per-project model-routing overrides
                 REFUSED; routing against the shipped table instead. Violated rules:
                 orchestration_below_top_tier, promotion_without_evidence.
       contains RULE_ORCHESTRATION_BELOW_TOP_TIER ('orchestration_below_top_tier'): True
       contains the config key ('model_routing.task_class_tiers'): True

    scratch removed by exact path: /tmp/f110-r10-g5-3zpljkpu exists: False
    no remedy.toml in the repository root: True

ON "warnings emitted : 2". SPEC (f) orders ONE warning per refusal, and that is
what the code does: each call to `resolve_effective_task_class_tiers` emits exactly
one. The probe calls it TWICE in that state (once directly, once through
`resolve_role_config`), so two are RECORDED by a `catch_warnings(record=True)` with
`simplefilter("always")`. Under Python's DEFAULT filters an operator sees it once —
MEASURED, not assumed:

    $ python3 -B  (five resolve_role_config('orchestrator') calls, default filters)
    stderr lines emitted for 5 resolutions under DEFAULT filters: 1

The map also violates `promotion_without_evidence`: demoting `mission` from `top`
to `cheap` IS a promotion in this module's vocabulary (cheaper), so the builder
reports both names and the warning carries both. That is the shipped behaviour of
round 6's validator, unchanged this round.

### G6 THE RED PROOF — PASS

Disposable worktree `/home/decodeux/Repos/remedy/remedy-review-r10-wt` at `e004848f`
(C5), NEVER cd-ed into: pytest was given ABSOLUTE paths inside it and no `cwd` was
set. `__pycache__` purged before every run (0 found each time — `python3 -B` writes
none), `python3 -B` throughout.

    $ python3 -B -c "sys.path.insert(0, <worktree>); import ..."
    config.py     __file__: /home/decodeux/Repos/remedy/remedy-review-r10-wt/packages/orchestration/config.py
    role_config   __file__: /home/decodeux/Repos/remedy/remedy-review-r10-wt/packages/orchestration/role_config.py
    model_routing __file__: /home/decodeux/Repos/remedy/remedy-review-r10-wt/packages/orchestration/model_routing.py

CONTROL, UNMUTATED, RUN FIRST:

    exit code: 0    summary: 166 passed in 0.58s    failures: 0
    PRIMARY CHECKOUT git status --porcelain: EMPTY (clean)

Then one mutation at a time, reverting between each. The primary checkout's
`git status --porcelain` was read IMMEDIATELY AFTER every mutation, in the same
step, and was EMPTY (clean) EVERY TIME — 4 of 4. Every revert is
`git -C <worktree> checkout -- <exact path>`, exit 0, and every one returned the
worktree to the control's 166 passed / exit 0.

(i) `_flatten_toml` recurses into table-valued keys again — `config.py`
    exit 1, 8 failed, 158 passed.
    RAW: `FAILED remedy-review-r10-wt/tests/orchestration/test_config.py::TestTableValuedKeys::test_flatten_stops_at_a_table_valued_key`
    parsed node id (the SECOND whitespace-separated token): identical. AGREE: True.
    FULL LIST (8, not truncated) — paths relative to the worktree:
      tests/orchestration/test_config.py::TestTableValuedKeys::test_flatten_stops_at_a_table_valued_key
      tests/orchestration/test_config.py::TestTableValuedKeys::test_a_project_table_resolves_as_one_dict_with_no_warning
      tests/orchestration/test_config.py::TestTableValuedKeys::test_a_project_table_replaces_a_user_table_whole
      tests/orchestration/test_config.py::TestTableValuedKeys::test_a_user_table_resolves_when_no_project_file_has_one
      tests/orchestration/test_config.py::TestTableValuedKeyShapeValidation::test_a_non_string_entry_is_reported
      tests/orchestration/test_role_config.py::TestEffectiveTaskClassTiers::test_a_legal_table_is_laid_over_the_shipped_one
      tests/orchestration/test_role_config.py::TestConfiguredOverrideReachesARoutedCall::test_a_legal_override_reaches_a_routed_call
      tests/orchestration/test_role_config.py::TestRefusedOverrideWarnsAndRoutesSeeded::test_an_illegal_override_warns_with_the_rule_named
    revert exit 0; back to control: True.

(ii) the `OverrideRefused` catch is removed — `role_config.py`
    exit 1, 4 failed, 162 passed.
    RAW: `FAILED remedy-review-r10-wt/tests/orchestration/test_role_config.py::TestRefusedOverrideWarnsAndRoutesSeeded::test_an_illegal_override_warns_with_the_rule_named`
    parsed node id: identical. AGREE: True.
    FULL LIST (4, not truncated):
      tests/orchestration/test_role_config.py::TestRefusedOverrideWarnsAndRoutesSeeded::test_an_illegal_override_warns_with_the_rule_named
      tests/orchestration/test_role_config.py::TestRefusedOverrideWarnsAndRoutesSeeded::test_an_illegal_override_routes_against_the_shipped_table
      tests/orchestration/test_role_config.py::TestRefusedOverrideWarnsAndRoutesSeeded::test_a_refused_table_does_not_break_config_resolution
      tests/orchestration/test_role_config.py::TestRefusedOverrideWarnsAndRoutesSeeded::test_every_declared_role_still_resolves_under_a_refused_table
    revert exit 0; back to control: True.

(iii) the refusal path returns the CONFIGURED map — the silent-downgrade mutation
    exit 1, 2 failed, 164 passed.
    RAW: `FAILED remedy-review-r10-wt/tests/orchestration/test_role_config.py::TestRefusedOverrideWarnsAndRoutesSeeded::test_an_illegal_override_routes_against_the_shipped_table`
    parsed node id: identical. AGREE: True.
    FULL LIST (2, not truncated):
      tests/orchestration/test_role_config.py::TestRefusedOverrideWarnsAndRoutesSeeded::test_an_illegal_override_routes_against_the_shipped_table
      tests/orchestration/test_role_config.py::TestRefusedOverrideWarnsAndRoutesSeeded::test_every_declared_role_still_resolves_under_a_refused_table
    revert exit 0; back to control: True.

(iv) the effective table is ignored; `route_role_call` called without it
    exit 1, 1 failed, 165 passed.
    RAW: `FAILED remedy-review-r10-wt/tests/orchestration/test_role_config.py::TestConfiguredOverrideReachesARoutedCall::test_a_legal_override_reaches_a_routed_call`
    parsed node id: identical. AGREE: True.
    FULL LIST (1, not truncated):
      tests/orchestration/test_role_config.py::TestConfiguredOverrideReachesARoutedCall::test_a_legal_override_reaches_a_routed_call
    revert exit 0; back to control: True.

THE PARSE WAS CHECKED AGAINST THE BYTES IT CAME FROM. For each mutation the harness
printed ONE RAW `FAILED ...` line beside its parsed node id and confirmed
`raw.split()[1] == parsed[0]` — True in all four. That is the round 9 slip
(SLIPS10 entry 2) closed by construction rather than by care.

PAIRWISE DISJOINTNESS — MEASURED, NOT ASSUMED. The red sets are NOT pairwise
disjoint, which the block names a REPORTABLE RESULT rather than a fault:

      (i)  vs (ii)  -> 1 shared: test_an_illegal_override_warns_with_the_rule_named
      (i)  vs (iii) -> 0 shared
      (i)  vs (iv)  -> 1 shared: test_a_legal_override_reaches_a_routed_call
      (ii) vs (iii) -> 2 shared (set (iii) is a strict SUBSET of set (ii))
      (ii) vs (iv)  -> 0 shared
      (iii) vs (iv) -> 0 shared
      ALL PAIRS DISJOINT: False
      (i) owns 6 ids no other mutation reddens
      (ii) owns 1 id no other mutation reddens
      (iii) owns 0 — its 2 ids are both in (ii)'s set
      (iv) owns 0 — its 1 id is also in (i)'s set

EVERY MUTATION IS STILL DETECTED, which is what the gate asks. The overlap is
structural and readable: (i) breaks the CONFIG READ, so every test that needs a
configured table fails, which necessarily includes the tests (iv) and part of those
(ii) exercise; and (iii) is a weaker mutation than (ii) — returning the wrong table
is a subset of not catching the exception at all. Neither (iii) nor (iv) is
therefore redundant: (iii) is the ONLY mutation that distinguishes "refused and
downgraded silently" from "refused and routed seeded" while the catch is present,
and (iv) is the only one that isolates the seam's argument from the config read.

    $ git -C <worktree> status --porcelain      (empty)
    $ git worktree remove /home/decodeux/Repos/remedy/remedy-review-r10-wt
    $ git worktree prune
    $ ls -d /home/decodeux/Repos/remedy/remedy-review-r10-wt
    ls: cannot access '.../remedy-review-r10-wt': No such file or directory

### G7 THE SUITES — 6 of 7 exit 0; ONE FAILURE, the blocked item

Each its own invocation, run serially. Bracketed numbers are the block's
measurements at `a1368633`.

    $ python3 -m pytest tests/orchestration/test_config.py -q
    74 passed in 0.35s                                            exit 0
      [63 at base, +11 new] — the number I MEASURE is 74; the block names no target.

    $ python3 -m pytest tests/orchestration/test_role_config.py -q
    92 passed in 0.34s                                            exit 0
      [82 at base, +10 new] — the number I MEASURE is 92; the block names no target.

    $ python3 -m pytest tests/orchestration/test_model_routing.py -q
    391 passed, 3 skipped, 1 warning in 3.25s                     exit 0
      [391 passed, 3 skipped — UNMOVED] — MATCHES. `model_routing.py` was not edited.

    $ python3 -m pytest tests/docs/ -q
    295 passed in 0.54s                                           exit 0
      [295] — MATCHES, with a file under `docs/` edited this round.

    $ python3 -m pytest tests/orchestration/test_teacher_model.py \
        tests/orchestration/test_self_use_runner.py \
        tests/orchestration/test_orchestrator_model_routing.py \
        tests/orchestration/test_job_role_routing.py tests/cli/test_teach_cmd.py -q
    FAILED tests/orchestration/test_orchestrator_model_routing.py::TestTheAnswerIsAlwaysUsable::test_the_fall_through_answer_is_a_non_empty_string
    1 failed, 86 passed in 4.62s                                  exit 1
      [87 — UNMOVED] — the COLLECTION is unmoved at 87; one of them is now RED.
      This is the blocked item. Its cause, its base-green measurement and the reason
      it was NOT repaired are in the "Blocked item" section above.

    $ python3 -m pytest tests/test_do_job_flow.py \
        tests/orchestration/test_job_evidence.py \
        tests/orchestration/test_execution_config_evidence.py \
        tests/orchestration/test_task_plan_evidence.py \
        tests/orchestration/test_token_cost_policy.py \
        tests/orchestration/test_model_aliases.py -q
    333 passed in 47.62s                                          exit 0
      [333 — UNMOVED] — MATCHES.

    $ python3 -m pytest tests/cli/test_golden_path.py -q
    42 passed in 20.66s                                           exit 0
      [42 — the canary] — MATCHES.

THE CONFIRMATION THE UNMOVED SUITES WERE ORDERED TO GIVE: `config.py` is imported
almost everywhere, and the flatten change surfaced NO fault in any of them. 333, 42,
295 and 391/3 all match the block's numbers exactly. The single red is caused by the
`role_config.py` change and by a test stub's single-key assumption, not by the
flatten change.

### G8 THE TREE, THE COMMITS AND THE SWEEP — PASS

    $ git status --porcelain          (immediately before C7 is staged)
    (empty)
    $ git ls-files .remedy-wt
    (empty)
    $ git worktree list
    (only the primary checkout and five pre-existing .remedy-wt job worktrees; no
     worktree of this round's making survives)
    $ ls remedy.toml
    ls: cannot access 'remedy.toml': No such file or directory
    $ git ls-files remedy.toml
    (empty)                           — constraint 12 held

    $ git diff --stat a1368633..e1da68d8 -- packages/ apps/ \
        ':(exclude)packages/orchestration/config.py' \
        ':(exclude)packages/orchestration/role_config.py'
    (empty)                           — constraint 7 MEASURED: no call site edited,
                                        model_routing.py untouched
    $ git diff --stat a1368633..e1da68d8 -- packages/orchestration/model_routing.py
    (empty)
    $ git diff --stat a1368633..e1da68d8 -- docs/
     docs/system/remedy-toml-configuration-system-v0.md | 27 ++++++++++++++++++++++
     1 file changed, 27 insertions(+)
    $ git diff --stat a1368633..e1da68d8 -- docs/roadmap/
    (empty)                           — constraint 6 MEASURED

PER-COMMIT INSERTIONS, the `+` column only, cell by cell against the Commits table
above, for every commit BEFORE the handback commit:

    9eb79b10  395  under 500  (table: +395)
    b9d32e3d  315  under 500  (table: +315)
    54574326   15  under 500  (table: +15)
    36ac459f   63  under 500  (table: +3 +5 +55 = 63)
    9f609b21   85  under 500  (table: +85)
    76658375   85  under 500  (table: +85)
    e004848f  368  under 500  (table: +159 +209 = 368)
    e1da68d8   27  under 500  (table: +27)

Every one under the AGENTS.md 500-insertion cap (DECISION F104 D1: insertions only).
The handback commit's own numbers appear in neither place — the reviewer measures
them at the next gate.

## Authored-text proofs

Four reviewer-authored slices, all extracted BY DELIMITER INDEX from the COMMITTED
`.agent/authored/f110-r10.md` with `remedy-review-r10-scratch/extract.py` (marker
lines EXCLUDED), never retyped and never taken from the delegation prompt.

| Slice | bytes | applied to | proof |
|---|---|---|---|
| PLAN10 | 2010 | `.agent/plan.md` | `cmp` against the extraction + the target's one trailing newline, exit 0 |
| RECORD9 | 5806 | `.agent/live_review.md` | 2190200 + 2 + 5806 = 2196008 real; base an exact byte prefix; second reader over its 1 paragraph; negative control REJECTS |
| SLIPS10 | 1885 | `.agent/prose_slips.md` | byte equality: final == base + 2 newlines + SLIPS10, base an exact prefix, 58680 bytes |
| DECISION5 | 3157 | `.agent/decisions.md` | 734845 + 1 + 3157 + 1 = 738004 real; base an exact byte prefix; second reader over its 7 paragraphs; negative control REJECTS |

The block file itself reached disk by `shutil.copyfile` twice — scratch original to
`.agent/authored/f110-r10.md` (C0a), then that COMMITTED file to
`.agent/last_block.md` (C0b) — so both are byte-identical to the source by
construction and not by transcription. Its sha256 on disk equals the digest the
delegation prompt stated, and `wc -l` is 395.

## Deviations & assumptions

D1. THE BLOCKED ITEM IS A DEVIATION FROM G7's ORDERED OUTCOME. G7 orders "all exit
0"; the 87-test unmoved group exits 1 with one failure. I did NOT edit, rename,
delete or skip the failing test, and I did NOT bend production code to satisfy its
stub — constraint 8 orders exactly this handling. Full cause and the un-applied
repair are in the "Blocked item" section. THE ROUND'S OWN WORK IS COMPLETE; what is
open is a one-line widening of an existing test's fake, which needs an explicit
order.

D2. SPEC (e) DEVIATION, DECLARED: a NON-MAPPING configured value is treated as
"nothing configured" and returns the shipped table. SPEC (e) names only "missing or
empty". The guard is required for correctness, not for tidiness:
`build_effective_task_class_tiers` calls `.items()` on its argument, so handing it
the string an env var would produce raises `AttributeError` INSIDE
`resolve_role_config` — the config-resolution fault DECISION F110 D5's rejected
alternative (1) exists to prevent, arriving through a different door. `config.py`'s
`validate_config` already reports that shape fault, so nothing is hidden. The
behaviour is stated in the function's docstring and exercised by
`test_a_scalar_where_a_table_belongs_is_reported`.

D3. THE G3/G4 SECOND READER FAILED ON ITS FIRST RUN AND THE FIRST READING IS
DECLARED, NOT REPLACED. See the G4 transcript. The reader compared the file's last
7 blank-line units against DECISION5's 7 and reported False; the raw bytes were
printed before any conclusion, and the only difference was the TARGET's own
trailing newline, which constraint 4 assigns to the target. The reader now removes
that one byte before splitting. Declaring the wrong first reading instead of quietly
correcting it is the behaviour round 9's D4 established.

D4. SPEC (f)'s WARNING TEXT lists every violated rule NAME in the order
`OverrideRefused` carries them, without the class each is attributed to. For
`mission = "cheap"` that reads "orchestration_below_top_tier,
promotion_without_evidence". The exception's own message already carries the
class-to-rule pairing for anyone who sees a traceback; the warning names the CONFIG
KEY plus the rules, which is what SPEC (f) ordered. Naming duplicates is possible if
two classes break the same rule — it is not deduplicated, because "EVERY violated
rule name it carries" is what the block asked for.

D5. STALE SENTENCE OUTSIDE THE CHANGE SET, DECLARED AND NOT REPAIRED, per
constraint 9: `docs/roadmap/features/T3_F110.md`'s T001/T003 bullets still describe
the per-project override map as unbuilt configuration. It is now read from
`remedy.toml`. `docs/roadmap/` is outside this round's change set and constraint 6
forbids touching it; the closure sequence already owns that file's Design bullet.

D6. `docs/system/remedy-toml-configuration-system-v0.md`'s own sentence "The table
above is not exhaustive — later features added their own keys" remains true and was
not edited; the new key was added as a row because that IS the file's convention,
and the seed mapping is deliberately NOT restated, per SPEC (o).

D7. No lint was run (constraint 5 orders none and forbids adding the gate); the
`remedy` CLI was not run (refused in this sandbox); no `remedy.toml` was created in
the repository root (constraint 12, measured twice).

No departure from the block's ordered commit sequence: C0a, C0b, C1, C2, C3, C4,
C5, C6, C7 were committed in exactly that order, no commit was added, dropped,
split or reordered.

## Next

The reviewer's round 10 verdict, which must ALSO rule on the blocked item: whether
to order the one-line widening of `_FakeConfig.get` in
`tests/orchestration/test_orchestrator_model_routing.py` (answer `None` for any key
other than `orchestrator.model` instead of asserting), or a different repair. No
further F110 build round should start until that test is green again, because it is
the only red in the suite and it sits on the same seam this feature is wiring.
