# Handoff — F110 Model routing by task class, round 12

## Session

SESSION 3 of feature F110 · round 12 · rounds so far 12

## State

- Branch: `feature/f110-model-routing-by-task-class`, pushed at `6177329c`, NO
  pull request open.
- Base of this round: `ccb736b9` (F110 R11 C6). HEAD before the handback:
  `6177329c` (C5).
- Fortschritt: THE PROMOTION-EVIDENCE SCHEMA LANDED AND NOTHING IS WIRED, which
  is the point. `config.py` learned that a TABLE-VALUED key declares what its
  ENTRIES hold — `ConfigKeySpec.entry_type`, `str` for a flat map, `dict` for a
  table of records, `None` for entries left unchecked — and
  `validate_config` now checks entries against that per-key declaration instead
  of against one hard-coded "entries are strings" rule. Round 10's
  `model_routing.task_class_tiers` declares `str`, which is exactly what it
  already validated; the new `model_routing.promotion_evidence` declares `dict`.
  Registering the key is by itself what stops `_flatten_toml` recursing into it,
  so a nested evidence record resolves WHOLE, with its `assertion_results`
  sub-table intact and ZERO "Unknown key" diagnostics — MEASURED at G5, printed
  from the shipped code. `model_routing.py` gained
  `promotion_evidence_from_mapping`, a PURE function of a plain mapping that
  turns a raw config table into `PromotionEvidence` records: class keys pass
  through `normalize_task_class` exactly as an override map's do, the nested
  `assertion_results` becomes a `PromotionAssertionResults` whose two field names
  are read off the record class itself, and a malformed entry is SKIPPED per
  entry rather than guessed at or raised on. A malformed record therefore fails
  CLOSED — the promotion it would have licensed is refused by
  `check_promotion_backed_by_evidence` with `RULE_PROMOTION_WITHOUT_EVIDENCE` and
  the class keeps its seeded, stronger tier — which is the opposite direction
  from a malformed OVERRIDE, refused loudly because dropping it would leave the
  operator believing a re-tier took effect. Both refusals are stated in the code
  beside each other. NO PRODUCTION CALL READS THE NEW KEY: `role_config.py` was
  not touched, and `git diff --stat ccb736b9..6177329c -- packages/ apps/` with
  the two edited files EXCLUDED is EMPTY, so constraints 6 and 7 are measured at
  G8 rather than asserted. The deliberate absence is recorded twice in the
  AGENTS.md idiom — in the module docstring and in the parser's own docstring —
  each naming `role_config.resolve_effective_task_class_tiers` as where the
  wiring will go. Rounds 4–11's shipped behaviour is unrevised: C4 is 162
  insertions and ZERO deletions.
- Round 11's PASS verdict is booked, `R-0787` and `R-0788` are RESOLVED, and one
  prose slip is recorded — all three ledger paragraphs in ONE append in ONE
  commit, byte-exact, with the arithmetic shown at G3.
- Open findings: 278 open, over 349 UNIQUE registered ids and 71 UNIQUE resolved
  ids, derived mechanically after C2 as a SET DIFFERENCE OVER UNIQUE IDS and not
  as a line count. `.agent/live_review.md` carries 73 lines matching
  `^Done: R-\d+ — ` but only 71 distinct ids among them: `R-0721` and `R-0725`
  each carry TWO `Done:` paragraphs, landed history that must not be rewritten.
  That is exactly the slip SLIPS12 records — the line reading would have read 276
  here. `R-0787` and `R-0788` are NOT in the open set; `R-0767` IS, unabsorbed, on
  the same seam.
- `.agent/STOP` read TWICE, per constraint 10: before the first commit
  (`test -e .agent/STOP` → ABSENT) and again before C6 (`ls -la .agent/STOP` →
  "No such file or directory"). ABSENT both times.
- `.agent/candidates.md` untouched. `.agent/decisions.md` untouched, per
  constraint 4. NO docs edited. NO `remedy.toml` in the repository root.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block | done | `shutil.copyfile`, digest unchanged |
| C0b mirror the block | done | `shutil.copyfile` from the COMMITTED copy |
| C1 PLAN12 → plan.md | done | first substantive commit, item 23 |
| C2 RECORD11 + DONE787 + DONE788 + SLIPS12 | done | one ledger append, one slips append |
| C3 config.py | done | entry_type, the key, the entry check, the docstring |
| C4 model_routing.py | done | the pure parser, purely additive |
| C5 the tests | done | 7 new in test_config.py, 15 new in test_model_routing.py |
| C6 the handback | done | this file |
| SPEC (a) entry_type on ConfigKeySpec | done | `entry_type: type \| None = None`; tiers key declares `str` |
| SPEC (b) promotion_evidence registered | done | env var, value_type dict, entry_type dict, default None, F110 named |
| SPEC (c) validate_config checks entries, stays shape-only | done | no model_routing import; policy questions left to model_routing |
| SPEC (d) module docstring gains an entry-type sentence | done | one sentence in the table-valued-key paragraph |
| SPEC (e) the pure parser | done | `promotion_evidence_from_mapping`; no config read, no new import |
| SPEC (f) nested assertion_results | done | names read off `PromotionAssertionResults` — see deviation 1 |
| SPEC (g) malformed entry SKIPPED, fails closed | done | reason stated in code beside the override contrast |
| SPEC (h) return value the existing consumers take | done | reproduced the reviewer's exact reading at G5 |
| SPEC (i) the deliberate absence | done | module docstring AND parser docstring, both naming role_config.py |
| SPEC (j) evidence table resolves whole | done | `TestThePromotionEvidenceTableResolvesWhole` |
| SPEC (k) entry type discriminates between the two keys | done | `TestTheDeclaredEntryTypeDiscriminatesBetweenTheTwoTables` |
| SPEC (l) parser round-trips a complete record | done | `TestThePromotionEvidenceParserRoundTripsACompleteRecord` |
| SPEC (m) parser skips what it cannot read, per entry | done | `TestThePromotionEvidenceParserSkipsWhatItCannotRead` |
| SPEC (n) the parsed record licenses a real promotion | done | `TestTheParsedRecordLicensesARealPromotion` |
| G1 transport | done | one digest twice, 351 lines |
| G2 the plan | done | `cmp` exit 0, 45 lines, 1 + 1 |
| G3 the ledger append | done | arithmetic, prefix, second reader, negative control |
| G4 prose_slips + open set | done | byte equality; 349 / 71 / 278 over UNIQUE ids |
| G5 the two production files | done | numstat, ast.parse, every deletion quoted, code RUN |
| G6 the red proof | done | control + 4 mutations, each reverted to the control |
| G7 the suites | done | 9 invocations, serial, every one exit 0 |
| G8 the tree, commits, sweep | done | clean tree, empty sweeps, every commit under the cap |

## Range

Review of `ccb736b9..6177329c` plus this handback commit.

## Commits

### f16aa7b1 F110 R12 C0a: save the round 12 step block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f110-r12.md` | +351/-0 | the block saved verbatim by `shutil.copyfile` |

### d125db16 F110 R12 C0b: mirror the block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +282/-193 | mirrored from the COMMITTED copy by `shutil.copyfile` |

### 8249fd72 F110 R12 C1: the round 12 plan
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +16/-13 | PLAN12, extracted by delimiter index |

### 67dbe616 F110 R12 C2: book round 11 - the verdict, two resolutions and a prose slip
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +7/-1 | RECORD11 + DONE787 + DONE788 as ONE append |
| `.agent/prose_slips.md` | +3/-1 | SLIPS12 |

### c65c8efc F110 R12 C3: typed table entries and the promotion-evidence key
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/config.py` | +48/-8 | `entry_type`, the new key, the entry check, two docstrings |

### 5cc77f29 F110 R12 C4: the pure promotion-evidence parser
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/model_routing.py` | +162/-0 | the parser, its two constants, the Public API list, the deliberate absence |

### 6177329c F110 R12 C5: the config surface and the evidence parser under test
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_config.py` | +182/-1 | SPEC (j) and (k); the one deletion is the widened `model_routing` import |
| `tests/orchestration/test_model_routing.py` | +197/-0 | SPEC (l), (m) and (n) |

### C6 — this handback
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

- `git worktree add --detach /home/decodeux/Repos/remedy/remedy-review-r12-redproof 6177329c…` — exit 0. Path matches the gitignored `remedy-review-*`; `.remedy-wt/` was never touched.
- `git worktree remove /home/decodeux/Repos/remedy/remedy-review-r12-redproof --force` — exit 0, BY ITS EXACT PATH; `git worktree prune` — exit 0. `ls -d` on that path afterwards: "No such file or directory".
- `git push -u origin feature/f110-model-routing-by-task-class` — exit 0, `ccb736b9..6177329c`.
- No PR created, edited or merged. No `gh` command run.

## Verification

**G1 TRANSPORT** — `sha256sum .agent/authored/f110-r12.md .agent/last_block.md`, exit 0:

    ec790b803cdbfceb424d8a74f956536e2d0b92fdd0d3b2f40aa290513a098acf  .agent/authored/f110-r12.md
    ec790b803cdbfceb424d8a74f956536e2d0b92fdd0d3b2f40aa290513a098acf  .agent/last_block.md

ONE digest twice. `wc -l .agent/authored/f110-r12.md` → 351. Per
`docs/agents/planner_reviewer_prompt.md` item 37 this proves the saved copy and
its mirror agree and claims NOTHING about the emitted bytes.

**G2 THE PLAN** — `cmp <PLAN12 extraction> .agent/plan.md` exit 0.
`wc -l .agent/plan.md` → 45 (under 50). `grep -c '^## Goal'` → 1;
`grep -c '^## Next Steps'` → 1.

**G3 THE LEDGER APPEND** — one append, one commit (`git show --name-only 67dbe616`
lists `.agent/live_review.md` and `.agent/prose_slips.md` and nothing else).

    arithmetic: 2204274 + 2 + 5670 = 2209946 | real after C2: 2209946 | equal: True
    pre-C2 content is an exact byte PREFIX: True
    file still ends WITHOUT a newline: True

SECOND READER — N counted from the appended text, then the LAST N blank-line
units of the whole file compared against its N paragraphs IN ORDER:

    N = 3
    unit -3 matches paragraph 1: True
    unit -2 matches paragraph 2: True
    unit -1 matches paragraph 3: True
    verdict: True

NEGATIVE CONTROL — one byte flipped inside the FIRST appended paragraph
(index 40, `'ERDIC'` → `'ERXIC'`):

    unit -3 matches paragraph 1: False
    unit -2 matches paragraph 2: True
    unit -1 matches paragraph 3: True
    verdict (must be False): False

RECORD11 header, the string COPIED FROM THE EXTRACTED SLICE (the separator after
"R11" is U+2014 EM DASH): `'Gate: F110 R11 — the round 11 entry.'`; em dash
present: True. Lines starting with it: **before C2 → 0, after C2 → 1**.
`grep -c '^Done: R-0787 — ' .agent/live_review.md` → **1**;
`grep -c '^Done: R-0788 — ' .agent/live_review.md` → **1** (both run as real
`grep`, exit 0).

**G4 PROSE SLIPS, BYTE EQUALITY + THE OPEN FINDING SET**

    arithmetic: 59944 + 2 + 1191 = 61137 | real: 61137 | equal: True
    base is an exact byte PREFIX: True
    still ends WITHOUT a newline: True

Open set, derived mechanically after C2 as SETS OF UNIQUE IDS:

    unique registered ('^- R-\d+ — ' paragraphs): 349
    unique resolved   ('^Done: R-\d+ — ' lines):   71   [LINES: 73]
    open (set difference over unique ids):        278
    R-0787 in open set: False
    R-0788 in open set: False
    R-0767 in open set: True

The 73-vs-71 gap is `R-0721` and `R-0725`, each carrying two `Done:` paragraphs;
a line count would read 276 and be silently wrong, which is SLIPS12's lesson.

**G5 THE TWO PRODUCTION FILES, MEASURED AND RUN**

    git show --numstat c65c8efc → 48  8  packages/orchestration/config.py
    git show --numstat 5cc77f29 → 162 0  packages/orchestration/model_routing.py

    ast.parse OK: packages/orchestration/config.py (1130 lines)
    ast.parse OK: packages/orchestration/model_routing.py (1426 lines)

EVERY DELETED LINE, VERBATIM, WITH ITS REGION — `packages/orchestration/config.py`,
8 deletions:

  Region: the MODULE DOCSTRING, table-valued-key paragraph (1)

    'by :func:`validate_config` rather than silently read as a table.'

  Region: `validate_config`'s DOCSTRING (3)

    '    and that every key and every value in it is a string. WHETHER a task class'
    '    exists, whether a tier exists and whether an override breaks a hard rule are'
    '    POLICY questions, and they are answered where the policy lives —'

  Region: `validate_config`'s `value_type is dict` BRANCH (4)

    '            else:'
    '                    if isinstance(entry_key, str) and isinstance(entry_value, str):'
    '                        f"{spec.key}: expected string entries, got "'
    '                        f"{entry_key!r} = {entry_value!r}")'

`packages/orchestration/model_routing.py` — **0 deleted lines**. The clause
"every deletion must be inside the MODULE DOCSTRING" is satisfied because the
commit is purely additive; see deviation 1 for the design choice that made it so.

RUNNING THE SHIPPED CODE, against TOML written OUTSIDE the repository root
(`/tmp/f110-r12-g5-…/remedy.toml`; `no remedy.toml in the repository root: True`):

    resolved value: {'architecture': {'model_id': 'qwen3-8b-instruct', 'quantization': 'q4_k_m',
      'prompt_hash': '0f1e2d3c4b5a6978', 'tokens': 1234, 'cost': 0.42,
      'reviewer_verdict': 'pass', 'runs_per_fixture': 3, 'corpus': 'F082',
      'assertion_results': {'block_level_pass_rate': 92, 'overall_pass_rate': 81}}}
    source: ConfigSource.PROJECT
    load warnings: []
    validate_config, WELL-FORMED table: []
    spec.value_type / entry_type: <class 'dict'> <class 'dict'>
    validate_config, MALFORMED table (entry is a scalar):
      ["model_routing.promotion_evidence: expected dict entries, got 'architecture' = 'cheap'"]
    validate_config, TIERS key with a sub-table entry:
      ["model_routing.task_class_tiers: expected str entries, got 'architecture' = {'tier': 'cheap'}"]

The nested sub-table resolved WHOLE and produced ZERO "Unknown key" diagnostics,
where the reviewer measured TEN for the unregistered key. The last two lines are
(a)'s discrimination measured on one loaded config: the SAME shape is a fault
under one key and well formed under the other.

    parser, COMPLETE record: {'architecture': PromotionEvidence(model_id='qwen3-8b-instruct',
      quantization='q4_k_m', prompt_hash='0f1e2d3c4b5a6978', tokens=1234, cost=0.42,
      assertion_results=PromotionAssertionResults(block_level_pass_rate=92, overall_pass_rate=81),
      reviewer_verdict='pass', runs_per_fixture=3, corpus='F082')}

    parser, malformed shapes of SPEC (m) — sibling 'vision' is well formed:
      entry is not a mapping           -> parsed keys ['vision']
      assertion_results is a scalar    -> parsed keys ['vision']
      wrong-typed field (tokens)       -> parsed keys ['vision']

    SPEC (n), WITH evidence:
      effective['architecture'] = cheap
      routed evidence: {'task_class': 'architecture', 'tier': 'cheap',
        'reason': 'per_project_override',
        'promoted_by': 'qwen3-8b-instruct + q4_k_m@0f1e2d3c4b5a6978 on F082'}
    SPEC (n), NO evidence:
      OverrideRefused: (OverrideViolation(task_class='architecture', rule_name='promotion_without_evidence'),)
      rule_name is RULE_PROMOTION_WITHOUT_EVIDENCE: True

That reproduces the reviewer's ccb736b9 reading of SPEC (h) exactly, field for
field, including the `promoted_by` string.

**G6 THE RED PROOF** — disposable worktree at C5 `6177329c`,
`/home/decodeux/Repos/remedy/remedy-review-r12-redproof`, NEVER cd-ed into (every
command ran through `subprocess` with `cwd=`), `__pycache__` purged before every
run, `python3 -B`. Module `__file__` printed FROM INSIDE it:

    /home/decodeux/Repos/remedy/remedy-review-r12-redproof/packages/orchestration/model_routing.py
    /home/decodeux/Repos/remedy/remedy-review-r12-redproof/packages/orchestration/config.py

Suites under mutation: `tests/orchestration/test_config.py` and
`tests/orchestration/test_model_routing.py`, one invocation.

CONTROL — exit 0, `487 passed, 3 skipped, 1 warning`, 0 failures.

(i) THE ENTRY-TYPE CHECK IS DROPPED FROM `validate_config` — exit **1**,
`4 failed, 483 passed, 3 skipped`. PRIMARY CHECKOUT `git status --porcelain`
immediately after the mutation: `''`. Red ids, FULL LIST:

    tests/orchestration/test_config.py::TestTableValuedKeyShapeValidation::test_a_non_string_entry_is_reported
    tests/orchestration/test_config.py::TestTheDeclaredEntryTypeDiscriminatesBetweenTheTwoTables::test_an_evidence_entry_that_is_a_scalar_is_reported
    tests/orchestration/test_config.py::TestTheDeclaredEntryTypeDiscriminatesBetweenTheTwoTables::test_the_tiers_key_still_reports_a_sub_table_entry
    tests/orchestration/test_config.py::TestTheDeclaredEntryTypeDiscriminatesBetweenTheTwoTables::test_the_tiers_key_still_reports_a_non_string_scalar_entry

The first of those is ROUND 10's OWN test, so the entry check still carries the
behaviour it inherited. Revert `git checkout -- packages/orchestration/config.py`
exit 0 → back to the control's counts and exit code: True.

(ii) THE PARSER ACCEPTS A MALFORMED ENTRY INSTEAD OF SKIPPING IT — exit **1**,
`3 failed, 484 passed, 3 skipped`. PRIMARY CHECKOUT status: `''`. FULL LIST:

    tests/orchestration/test_model_routing.py::TestThePromotionEvidenceParserSkipsWhatItCannotRead::test_the_malformed_entry_produces_no_record[a wrong-typed field-entry2]
    tests/orchestration/test_model_routing.py::TestThePromotionEvidenceParserSkipsWhatItCannotRead::test_a_well_formed_sibling_in_the_same_mapping_still_produces_one[a wrong-typed field-entry2]
    tests/orchestration/test_model_routing.py::TestTheParsedRecordLicensesARealPromotion::test_a_map_whose_only_evidence_entry_was_skipped_is_refused_the_same_way

Revert exit 0 → back to the control: True.

(iii) THE PARSER DROPS `assertion_results`, LEAVING IT `None` — exit **1**,
`7 failed, 480 passed, 3 skipped`. PRIMARY CHECKOUT status: `''`. FULL LIST:

    tests/orchestration/test_model_routing.py::TestThePromotionEvidenceParserRoundTripsACompleteRecord::test_the_nested_table_comes_back_as_the_record_type_with_both_readings
    tests/orchestration/test_model_routing.py::TestThePromotionEvidenceParserRoundTripsACompleteRecord::test_the_whole_record_equals_the_one_the_mapping_describes
    tests/orchestration/test_model_routing.py::TestThePromotionEvidenceParserSkipsWhatItCannotRead::test_the_malformed_entry_produces_no_record[assertion_results is a scalar-entry1]
    tests/orchestration/test_model_routing.py::TestThePromotionEvidenceParserSkipsWhatItCannotRead::test_a_well_formed_sibling_in_the_same_mapping_still_produces_one[not a mapping-cheap]
    tests/orchestration/test_model_routing.py::TestThePromotionEvidenceParserSkipsWhatItCannotRead::test_a_well_formed_sibling_in_the_same_mapping_still_produces_one[assertion_results is a scalar-entry1]
    tests/orchestration/test_model_routing.py::TestThePromotionEvidenceParserSkipsWhatItCannotRead::test_a_well_formed_sibling_in_the_same_mapping_still_produces_one[a wrong-typed field-entry2]
    tests/orchestration/test_model_routing.py::TestTheParsedRecordLicensesARealPromotion::test_the_promotion_is_accepted_and_routed_with_what_promoted_it

Revert exit 0 → back to the control: True.

(iv) THE FLATTEN STOP-SET NO LONGER INCLUDES THE NEW KEY — exit **1**,
`3 failed, 484 passed, 3 skipped`. PRIMARY CHECKOUT status: `''`. FULL LIST:

    tests/orchestration/test_config.py::TestTableValuedKeys::test_the_stop_set_is_derived_from_the_registry
    tests/orchestration/test_config.py::TestThePromotionEvidenceTableResolvesWhole::test_the_key_is_registered_as_a_table_of_records
    tests/orchestration/test_config.py::TestThePromotionEvidenceTableResolvesWhole::test_the_nested_record_resolves_whole_with_no_load_warning

Revert exit 0 → back to the control: True.

RAW-LINE CHECK. One raw pytest line printed beside each parsed set, e.g. for (ii):

    'FAILED tests/orchestration/test_model_routing.py::TestThePromotionEvidenceParserSkipsWhatItCannotRead::test_the_malformed_entry_produces_no_record[a wrong-typed field-entry2]'

The block's rule — "the node id is the SECOND whitespace-separated token" — reads
this as `…test_the_malformed_entry_produces_no_record[a`, i.e. TRUNCATED at the
space inside the parametrization. See deviation 2: the harness reads the node id
as everything between `FAILED ` and the ` - ` reason, both readings are printed,
and `raw line starts with 'FAILED ' + parsed id` is True for every mutation. For
the non-parametrized ids the two readings AGREE (True for (i), (iii), (iv)).

PAIRWISE DISJOINTNESS, MEASURED (non-disjoint is a REPORTABLE RESULT, not a
fault):

    (i) vs (ii): 0    (i) vs (iii): 0    (i) vs (iv): 0
    (ii) vs (iv): 0   (iii) vs (iv): 0
    (ii) vs (iii): 1
        …TestThePromotionEvidenceParserSkipsWhatItCannotRead::test_a_well_formed_sibling_in_the_same_mapping_still_produces_one[a wrong-typed field-entry2]

Five of the six pairs are disjoint. The one overlap is expected and is not a
weak discriminator: mutation (ii) makes the wrong-typed entry produce a partial
record, and mutation (iii) makes the well-formed SIBLING produce an incomplete
one, so that single parametrization reddens under both for different reasons —
each mutation still owns 2, 6 and 2 ids nothing else touches.

**G7 THE SUITES** — nine invocations, each its own, run SERIALLY. The exit code
printed is pytest's OWN returncode, captured through `subprocess`, not a
pipeline's (a piped `| tail` would report tail's status).

    exit=0  tests/orchestration/test_config.py                      81 passed                      [base 74, +7 new]
    exit=0  tests/orchestration/test_model_routing.py               406 passed, 3 skipped          [base 391 passed 3 skipped, +15 new]
    exit=0  tests/orchestration/test_role_config.py                 92 passed                      [92 — UNMOVED]
    exit=0  tests/orchestration/test_orchestrator_model_routing.py  20 passed                      [20 — UNMOVED]
    exit=0  tests/cli/test_init_cmd.py (+5 more)                    304 passed                     [304 — UNMOVED]
    exit=0  tests/orchestration/test_fence_e2e.py (+4 more)         433 passed                     [433 — UNMOVED]
    exit=0  tests/runtimes/test_runtime_config.py (+3 more)         199 passed                     [199 — UNMOVED]
    exit=0  tests/docs/                                             295 passed                     [295 — UNMOVED]
    exit=0  tests/cli/test_golden_path.py                           42 passed                      [42 — the canary]

Only the two suites this round adds to moved, and both moved UP by exactly the
number of tests added; every UNMOVED group matches the reviewer's ccb736b9
measurement cell for cell, with no difference to explain. The list is wider than
round 10's because `config.py` is read by 25 test files.

**G8 THE TREE, THE COMMITS AND THE SWEEP**

    git status --porcelain (exit 0): ''                      -> EMPTY
    git ls-files .remedy-wt  (exit 0): ''                    -> returns nothing
    remedy.toml in the repository root exists: False
    git worktree list: only the primary checkout and five UNRELATED .remedy-wt/job-* worktrees;
      no worktree of this round's making survives

    git diff --stat ccb736b9..6177329c -- docs/                                     -> '' EMPTY
    git diff --stat ccb736b9..6177329c -- packages/ apps/
        ':!packages/orchestration/config.py' ':!packages/orchestration/model_routing.py'
                                                                                    -> '' EMPTY
    role_config.py in that excluded-diff output: False

Constraints 6 and 7 are therefore MEASURED, not asserted, and the second sweep is
what proves `role_config.py` was not touched.

PER-COMMIT INSERTIONS, the `+` column only, cell by cell against the `## Commits`
table above, every commit before the handback:

| Commit | Insertions | Handback table says | Under the 500 cap |
|--------|-----------|---------------------|-------------------|
| f16aa7b1 C0a | 351 | +351 | yes |
| d125db16 C0b | 282 | +282 | yes |
| 8249fd72 C1 | 16 | +16 | yes |
| 67dbe616 C2 | 10 | +7 and +3 = 10 | yes |
| c65c8efc C3 | 48 | +48 | yes |
| 5cc77f29 C4 | 162 | +162 | yes |
| 6177329c C5 | 379 | +182 and +197 = 379 | yes |

Every cell agrees and every commit is under the AGENTS.md 500-insertion cap.
`d125db16` is a verbatim rewrite of a single `.agent/**` state file and would be
exempt under DECISION F104 D1 in any case; it does not need the exemption.

## Authored-text proofs

Every slice was extracted BY DELIMITER INDEX from the COMMITTED
`.agent/authored/f110-r12.md`, marker lines EXCLUDED, by
`remedy-review-r9-scratch/extract.py`, and written by script. Nothing was
retyped and nothing was read from the delegation prompt.

| Slice | bytes | sha256 (of the extracted text) | Applied to | Result |
|-------|-------|-------------------------------|------------|--------|
| PLAN12 | 2106 | `b820fcb35d8009d7a1b9532306fe503d5a778a3ef8c65c0cb362834f13080c50` | `.agent/plan.md` | `cmp` exit 0 |
| RECORD11 | 3906 | `81538fab7320677ca928e630d66bc15e954f1a1905b321aa9e2fb4791a9240ba` | `.agent/live_review.md` | second reader unit -3 True |
| DONE787 | 1232 | `3cec59ec0fc411c2cfc4163dc0bb11aea9ee71cbedab7d4a4890f3c282069000` | `.agent/live_review.md` | second reader unit -2 True |
| DONE788 | 531 | `1090e343df982320949e89bbe278c7bf5c9cebccd2a1fa39e06e2bc97b292bdf` | `.agent/live_review.md` | second reader unit -1 True |
| SLIPS12 | 1192 | `8439cb6f35772ae2dfdff562b9a73ace1d3f90f2d00a6a9b7f6d6691639cdeb3` | `.agent/prose_slips.md` | byte arithmetic exact |

Newline conventions, RE-MEASURED at this round's base `ccb736b9` and not carried
forward: `.agent/live_review.md` 2204274 bytes ending WITHOUT a newline;
`.agent/prose_slips.md` 59944 bytes, same shape; `.agent/plan.md` 1875 bytes
ending WITH one. The paragraph separator was MEASURED on both append targets
(newline-run census: `\n` and `\n\n` only in `live_review.md`) and is `\n\n`.
Each extraction's single trailing newline was dropped where the TARGET does not
take one, per constraint 4 — the target wins. PLAN12 already ended with exactly
one newline, which is `.agent/plan.md`'s own convention, so nothing was added or
stripped there.

`.agent/authored/f110-r12.md` was produced by `shutil.copyfile` from the block
file, and `.agent/last_block.md` by `shutil.copyfile` from that COMMITTED copy —
neither by re-emitting text. G1's single digest covers both.

## Deviations & assumptions

The block's ordered commit sequence was followed EXACTLY: C0a, C0b, C1, C2, C3,
C4, C5, C6 — no extra commit, none dropped, none reordered, no split needed
(the largest is C5 at 379 insertions).

1. **SPEC (f) is satisfied WITHOUT touching the import line, and this was forced
   by G5.** The natural way to read `PromotionAssertionResults`' own field names
   is `from dataclasses import dataclass, fields`. That MODIFIES an existing line
   and therefore produces a DELETION in `model_routing.py` outside the module
   docstring, which G5 declares a **STOP**. SPEC (e) independently says the
   parser "imports nothing new beyond what the module already has". Both clauses
   point the same way, so the field names are read off
   `PromotionAssertionResults.__dataclass_fields__` instead. The names still come
   from the class and never from a spelling in the parser; C4 is 162 insertions
   and ZERO deletions; the import block is untouched, so constraint 5's sorting
   rule has nothing to sort here. Declared rather than silently taken.
2. **G6's node-id rule under-reads a parametrized id.** "The node id is the
   SECOND whitespace-separated token" is true for a plain id and FALSE for
   `…::test_the_malformed_entry_produces_no_record[a wrong-typed field-entry2]`,
   whose parametrization contains spaces — the token reading truncates it at
   `[a`. Applied as written AND beside it the correct reading (everything between
   `FAILED ` and the ` - ` reason); both are printed for every mutation, and
   `raw line starts with 'FAILED ' + parsed id` is True throughout. The FIRST run
   of the harness used the block's rule alone and produced a truncated red set
   and therefore an unreliable disjointness reading; that run was discarded and
   the whole gate re-run. The numbers reported above are from the corrected run.
   The same first run also compared "back to the control" over the summary LINE,
   which carries the elapsed time — F110 R9's own recorded slip, reproduced and
   then fixed to compare counts and exit code.
3. **Two constants the SPEC did not name.** The parser needs a RAW TYPE per
   field, and `from __future__ import annotations` makes a dataclass field's
   `type` the STRING `"int | None"`, so deriving it would mean evaluating
   annotations at import time. `PROMOTION_EVIDENCE_ENTRY_FIELD_TYPES` declares
   them and `PROMOTION_EVIDENCE_NESTED_FIELD` names the one field that is itself
   a table. Neither is a free-floating literal: a test asserts the first is
   EXACTLY `PromotionEvidence`'s own fields minus the second, so a field added to
   the record without a reading is a red test.
4. **The new config key is spelled as a literal in one place in
   `tests/orchestration/test_config.py`.** Its reader-side constant — the sibling
   of `role_config.TASK_CLASS_TIERS_CONFIG_KEY` — cannot land this round because
   constraint 6 keeps `role_config.py` out of the change set. The literal is
   guarded by `test_the_key_is_registered_as_a_table_of_records`, which reddens
   on a rename, and it belongs in `role_config.py` with the wiring round.
5. **Two readings of "wrong type" that SPEC (g) does not rule on, stated in the
   code.** A `bool` is never accepted for an `int` or `float` field, because
   `bool` subclasses `int` and TOML's `tokens = true` would otherwise land in the
   record as 1. An `int` IS accepted where a `float` is declared and is widened,
   because TOML writes `0` for a free run and that is a cost, not a fault.
6. **`d125db16` (C0b) shows 282 insertions against 193 deletions** because
   `.agent/last_block.md` previously held round 11's block. It is the verbatim
   rewrite of a single `.agent/**` state file; the insertion count is under the
   cap either way, so DECISION F104 D1's exemption is not being leaned on.

**Sentences OUTSIDE the change set that this round makes stale, DECLARED and NOT
repaired (constraint 9; NO DOCS ARE EDITED):**

- `docs/system/remedy-toml-configuration-system-v0.md`, the registered-key table
  at line 60: it lists `model_routing.task_class_tiers` and now omits
  `model_routing.promotion_evidence`, which is registered as of `c65c8efc`.
- The same file's section heading at line 84, "Table-valued keys:
  `model_routing.task_class_tiers`", and its first sentence at line 86, "Most
  keys carry a scalar. `model_routing.task_class_tiers` (F110) carries a whole
  TOML sub-table": the heading is plural but names ONE key, and there are now
  TWO table-valued keys, the second a table of RECORDS rather than of strings.
  The section also does not mention `entry_type`.

Both belong to the same section and are one edit for whichever round is allowed
to touch `docs/`; the wiring round is the natural place, since that is when the
key acquires a reader and the document can describe end-to-end behaviour.

**Pre-existing staleness INSIDE the change set, NOT falsified by this round and
therefore NOT repaired:** `packages/orchestration/model_routing.py`'s module
docstring still says that a reader searching for "the loader that turns a
project's TOML table into that mapping … arrives with the resolver-seam round,
alongside the per-call-site class declarations". That round has already landed —
`role_config.resolve_effective_task_class_tiers` is the loader. Constraint 9
binds only sentences THIS round makes stale, and constraint 7 forbids revising
rounds 4–11's shipped work, so it is flagged here for the wiring round rather
than edited. It is a pointer that under-describes, not one that misdirects.

## Next

The WIRING ROUND: `role_config.resolve_effective_task_class_tiers` reads
`model_routing.promotion_evidence` as well as the tiers table, passes the parsed
records to `build_effective_task_class_tiers` and on to `route_role_call`, so a
documented benchmark run actually licenses a cheaper tier at a routed call — and
the two stale paragraphs of
`docs/system/remedy-toml-configuration-system-v0.md` named above are repaired in
the same round, since that is when `docs/` may be touched and when the key has a
reader to describe.
