# Handoff — F110 Model routing by task class, round 13

## Session

SESSION 3 of feature F110 · round 13 · rounds so far 13

## State

- Branch: `feature/f110-model-routing-by-task-class`, pushed at `be850b92`, NO
  pull request open.
- Base of this round: `f943e436` (F110 R12 C6). HEAD before the handback:
  `be850b92` (C5).
- Fortschritt: THE EVIDENCE IS WIRED AND A DOCUMENTED RUN NOW LICENSES A CHEAPER
  TIER. `role_config.py` gained `PROMOTION_EVIDENCE_CONFIG_KEY` and
  `resolve_promotion_evidence()`, the round-12 parser's ONE production caller:
  it reads `model_routing.promotion_evidence` from the configuration and applies
  the identical three-way guard its sibling applies to the tiers table — unset,
  empty, or not a Mapping all answer an EMPTY mapping — and otherwise returns
  `promotion_evidence_from_mapping(raw)`. Those records now reach BOTH consumers.
  `resolve_effective_task_class_tiers` passes them to
  `build_effective_task_class_tiers` as `promotion_evidence`, which is the line
  that turns round 12's measured `promotion_without_evidence` refusal into an
  accepted promotion; and `resolve_routed_call_evidence` passes the same records
  to `route_role_call`, so a routed call's `promoted_by` NAMES the run instead of
  answering `None`. RUN BY G5 AGAINST TOML WRITTEN OUTSIDE THE REPOSITORY ROOT,
  not read: with both tables configured, `architecture` — a TOP-tier class —
  comes back at `cheap` with ZERO warnings, and `design_worker`, the role that
  declares that class, gets
  `{'task_class': 'architecture', 'tier': 'cheap', 'reason': 'per_project_override',
  'promoted_by': 'qwen3-8b-instruct + q4_k_m@0f1e2d3c4b5a6978 on F082'}` — the
  exact string the reviewer measured at `f943e436`. With the tiers table ALONE
  the same promotion is still refused, one warning naming
  `promotion_without_evidence`, and the class comes back at `top`. With the key
  UNSET, and with a BARE STRING where the table belongs, the reader answers `{}`
  and every routed answer is byte-identical to the pre-round one, with provider,
  model and effort unchanged at `ollama` / `muse-glimmer:latest` / `medium` —
  the D5 principle one layer on. THE SIGNATURES DID NOT MOVE:
  `resolve_effective_task_class_tiers()` still takes no argument and still
  returns a plain dict, and the price is that BOTH paths read the key
  separately; `get_config` is cached, so that costs one dict lookup and one small
  parse, and the code says so in a comment rather than leaving the double read to
  look accidental. `model_routing.py` was edited for its MODULE DOCSTRING ONLY —
  all 13 deletions proven by AST to lie inside base lines 1..171, the module
  docstring's own span — repairing the two sentences this round falsified: the
  parser now names `role_config.resolve_promotion_evidence` as its one production
  caller, and the misdated "it arrives with the resolver-seam round" clause is
  replaced by the measured dating (the loader arrived in TWO halves, the tiers
  table at `76658375` in round 10 and the evidence table in round 13; the
  resolver-seam round `6c7fb4eb` read no config key at all), while the
  paragraph's still-true and still-load-bearing claim — this module reads no
  config file and imports `config.py` from nowhere — is kept word for word in
  substance. `config.py` WAS NOT TOUCHED: `git diff --stat f943e436..be850b92`
  over `packages/` and `apps/` with the two edited files excluded is EMPTY,
  measured at G8. Nine new tests landed, purely additive (265 insertions, ZERO
  deletions), each deriving its class, role, tier, evidence field names and bars
  from the modules' own constants and building the record from REAL TOML written
  to a pytest `tmp_path` and loaded through the REAL `load_config`. The
  documentation gained the registered-key row and a widened table-valued-keys
  section covering both keys.
- `.agent/STOP` read from disk TWICE, as constraint 10 orders: before the first
  commit — ABSENT — and again before C6 — ABSENT. No stop was signalled.
- OPEN FINDING SET after C2, derived at G4 as a SET DIFFERENCE OVER UNIQUE IDS:
  349 unique registered, 71 unique resolved, **278 OPEN**. The ledger holds 73
  `Done:` LINES against those 71 unique ids, because `R-0721` and `R-0725` each
  carry two, so a line count would have read two low. `R-0767` is IN the open
  set, confirmed.
- T003 IS NOW COMPLETE ON THIS BRANCH. Its last unbuilt clause was the caller for
  the promotion-evidence parser, and both consumers now have it: "a promotion
  without evidence refused, with evidence logged" is enforced end to end, from a
  project's TOML through the builder and the seam to a routed call that names the
  run. What remains for the feature is not T003 work: the acceptance round, the
  integration gate round, then closure.

## Range

Review of `f943e436..be850b92` plus this handback commit.

## Commits

### 745c5665 F110 R13 C0a: save the round 13 step block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f110-r13.md` | +316 / -0 | the step block saved verbatim by `shutil.copyfile`, never re-emitted |

### 347a84bb F110 R13 C0b: mirror the block to last_block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +219 / -254 | the committed authored file mirrored by `shutil.copyfile`; the − column is round 12's block being replaced |

### b26b1656 F110 R13 C1: the plan for the evidence wiring round
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +14 / -18 | PLAN13 applied byte for byte; first substantive commit, item 23 |

### 054807b5 F110 R13 C2: book round 12 - the PASS verdict and one prose slip
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +3 / -1 | RECORD12 appended; the − line is the base's last line regaining a newline |
| `.agent/prose_slips.md` | +3 / -1 | SLIPS13 appended, same shape |

### 8efa2330 F110 R13 C3: wire the promotion evidence into the table builder and the seam
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/role_config.py` | +86 / -3 | SPEC (a)-(e): the key constant, the reader, both consumers, the Public API list |
| `packages/orchestration/model_routing.py` | +17 / -13 | SPEC (f): MODULE DOCSTRING ONLY — the two falsified sentences repaired |

### fecfbbed F110 R13 C4: the evidence reaching the table, the seam and a routed call
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_role_config.py` | +265 / -0 | SPEC (g)-(l): nine new tests and three new fixtures, PURELY ADDITIVE |

### be850b92 F110 R13 C5: the configuration document gains the promotion-evidence key
| Path | +/- | Reason |
|------|-----|--------|
| `docs/system/remedy-toml-configuration-system-v0.md` | +36 / -4 | SPEC (m)-(n): the registered-key row, the widened heading, the evidence subsection |

### <this commit> F110 R13 C6: the round 13 handback
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | full rewrite | this file; a handback cannot table the commit that writes it (R-0149 pattern). Exempt from the 500-insertion cap under DECISION F104 D1 — a verbatim rewrite of a single `.agent/**` state file |

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a save the block | done | |
| C0b mirror to last_block | done | |
| C1 PLAN13 | done | |
| C2 RECORD12 + SLIPS13 | done | |
| C3 production | done | |
| C4 tests | done | |
| C5 docs | done | |
| C6 handback | done | this commit |
| SPEC (a) named key constant | done | `PROMOTION_EVIDENCE_CONFIG_KEY`, spelled once |
| SPEC (b) `resolve_promotion_evidence` | done | three-way guard, `get_config` imported in the body |
| SPEC (c) builder receives the evidence | done | signature and return type unchanged |
| SPEC (d) seam receives the evidence | done | double read stated in a comment |
| SPEC (e) Public API docstring | done | both new public names, derived from the round's new names |
| SPEC (f) two falsified sentences | done | docstring-only; all 13 deletions AST-proven inside the module docstring |
| SPEC (g) promotion WITH evidence accepted | done | `test_a_promotion_with_evidence_is_accepted_end_to_end` |
| SPEC (h) routed call names its promoter | done | `test_a_routed_call_names_what_promoted_it`; substring taken from the configured evidence |
| SPEC (i) same promotion without evidence refused | done | `test_the_same_promotion_without_evidence_is_still_refused` |
| SPEC (j) unset evidence key changes nothing | done | `TestUnsetPromotionEvidenceChangesNothing`, two tests |
| SPEC (k) malformed value is not a crash | done | `TestMalformedPromotionEvidenceIsNotACrash`, two tests |
| SPEC (l) class and role read from the tables | done | `_evidence_promotable_role`, pinned by `TestPromotableRoleIsReadFromTheShippedTables` |
| SPEC (m) registered-key row | done | neighbour column shape matched exactly |
| SPEC (n) table-valued-keys section covers both | done | heading widened to the concept; evidence subsection added |
| G1 transport | done | one digest twice |
| G2 the plan | done | `cmp` exit 0 against slice + the target's newline |
| G3 the ledger append | done | arithmetic, prefix, no trailing newline, second reader, negative control, header count 0 → 1 |
| G4 prose_slips + open set | done | byte equality; 278 open over 349/71 unique |
| G5 the two production files | done | numstat, `ast.parse`, every deleted line quoted, shipped code RUN |
| G6 the red proof | done | four mutations, all red, all reverted to control |
| G7 the suites | done | nine invocations, all exit 0 |
| G8 tree, commits, sweep | done | clean tree, empty sweep, every commit under the cap |

## External actions

- `git worktree add /home/decodeux/Repos/remedy-review-r13-redproof HEAD --detach`
  — created, then IMMEDIATELY REMOVED with `git worktree remove` + `git worktree
  prune` because the path sat OUTSIDE the repository and therefore outside the
  gitignored `remedy-review-*` pattern the round ordered. No test was run in it.
- `git worktree add /home/decodeux/Repos/remedy/remedy-review-r13-redproof HEAD
  --detach` — the G6 worktree, gitignored by `.gitignore:223 remedy-review-*`,
  never `cd`-ed into (every command ran with `cwd=` set). Removed by its EXACT
  path with `git worktree remove
  /home/decodeux/Repos/remedy/remedy-review-r13-redproof` followed by `git
  worktree prune`; `ls -d` on that path afterwards answers "No such file or
  directory" and `git worktree list` shows only the primary checkout and the
  five pre-existing, unrelated `.remedy-wt/job-*` worktrees.
- `git push -u origin feature/f110-model-routing-by-task-class` — exit 0,
  `f943e436..be850b92`. A second push carries this handback.
- No PR created, no PR merged, no `gh` command run.

## Verification

**G1 TRANSPORT.** `sha256sum .agent/authored/f110-r13.md .agent/last_block.md`
— exit 0, ONE digest twice:
`b7f4c58449a0d61cbf2a753f29f250dc747843c0d246340ab6796a342de07d29` for both.
`wc -l .agent/authored/f110-r13.md` = **316**. Per
`docs/agents/planner_reviewer_prompt.md` item 37 this proves the saved copy and
its mirror agree and claims nothing about the emitted bytes. The scratch source
`remedy-review-r9-scratch/f110-r13.md` carried the same digest, which the
prompt's own stated digest matched before any work began.

**G2 THE PLAN.** `cmp remedy-review-r9-scratch/plan13.bin .agent/plan.md` —
exit 1, `cmp: EOF on remedy-review-r9-scratch/plan13.bin after byte 1874, in
line 41`: the extraction carries NO trailing newline and `.agent/plan.md`'s
convention takes one, exactly as constraint 4 says ("the TARGET wins").
`cmp remedy-review-r9-scratch/g2_nl.bin .agent/plan.md`, the same extraction plus
that one byte — **exit 0**, no output. `wc -l .agent/plan.md` = **41** (under
50). `grep -c '^## Goal'` = **1**; `grep -c '^## Next Steps'` = **1**.

**G3 THE LEDGER APPEND.** Arithmetic: `2209946 + 2 + 5350 = 2215298`; real size
after C2 = **2215298**; equal = True. Pre-C2 content is an exact byte PREFIX:
True. File still ends WITHOUT a newline: True.
SECOND READER: N counted from the slice = **1**; the last 1 blank-line unit of
the whole file equals the slice's 1 paragraph IN ORDER — True, 5350 bytes
against 5350.
NEGATIVE CONTROL: byte 0 of the FIRST appended paragraph flipped, `'G'` → `'g'`
(`gate: F110 R12 — the round 12 entry. V…`); the second reader ACCEPTS = False,
i.e. it **REJECTS** the mutation. The real file was untouched, re-read at 2215298
bytes.
HEADER COUNT, string copied from the extracted slice (`Gate: F110 R12 — the
round 12 entry.`; the separator's codepoint printed as `0x2014`, U+2014 EM DASH,
confirmed): lines matching BEFORE C2 = **0**; AFTER C2 = **1**.

**G4 prose_slips.md + THE OPEN SET.** `61137 + 2 + 1212 = 62351`; real = **62351**;
equal = True. Base an exact prefix: True. Still ends without a newline: True.
OPEN SET, set difference over UNIQUE IDS: paragraphs matching `^- R-\d+ — ` =
349, unique = **349**. Lines matching `^Done: R-\d+ — ` = 73, unique = **71**;
the ids carrying more than one `Done:` line are `['R-0721', 'R-0725']`, which is
why a LINE count reads two low. Open = 349 − 71 = **278**. `R-0767` in the open
set: **True**. `R-0787` / `R-0788` in the open set: False / False.

**G5 THE TWO PRODUCTION FILES.** `git show --numstat 8efa2330`:
`17 13 packages/orchestration/model_routing.py`,
`86 3 packages/orchestration/role_config.py`.
`ast.parse` over both — `ast.parse OK packages/orchestration/role_config.py`,
`ast.parse OK packages/orchestration/model_routing.py`.
DELETED LINES, `model_routing.py`, VERBATIM (13), every one at base lines 41–43
and 47–56, proven by AST to lie inside the module docstring's own span, base
lines **1..171** — `ALL deletions inside the MODULE DOCSTRING: True`:

    -find it: it arrives with the resolver-seam round, alongside the per-call-site
    -class declarations, because the schema is worth pinning BEFORE anything can be
    -configured to break it. packages/orchestration/config.py is deliberately NOT
    -Remedy deliberately does not CALL :func:`promotion_evidence_from_mapping` from
    -anywhere in production yet, and a reader searching for its caller should find
    -this sentence rather than a silence. The parser turns the raw
    -``model_routing.promotion_evidence`` config table into
    -:class:`PromotionEvidence` records, and the call that hands it that table arrives
    -with the wiring round, in ``packages/orchestration/role_config.py`` beside
    -``resolve_effective_task_class_tiers`` — the config-reading layer, which is
    -already where the per-project TIERS table is read. The schema lands a round
    -BEFORE its reader on purpose, so it is pinned before routing behaviour moves
    -against it.

DELETED LINES, `role_config.py`, VERBATIM (3), with their regions:

    -        return build_effective_task_class_tiers(dict(configured))      [body of resolve_effective_task_class_tiers]
    -    through no second path.                                            [docstring of resolve_routed_call_evidence]
    -        return route_role_call(role, originating_task_class, effective_tiers)  [body of resolve_routed_call_evidence]

THE SHIPPED CODE RUN, against TOML written to `/tmp/remedy-r13-g5-n4t4ore6`
(`inside repo: False`; the directory was removed afterwards and `exists: False`
printed). Derived, not spelled: `class='architecture' seeded='top'
cheapest='cheap' declared-role='design_worker'`. Every load reported
`load warnings: []`.

- SPEC (g) BOTH TABLES — `resolve_promotion_evidence()` RETURNED
  `{'architecture': PromotionEvidence(model_id='qwen3-8b-instruct',
  quantization='q4_k_m', prompt_hash='0f1e2d3c4b5a6978', tokens=12345, cost=0.0,
  assertion_results=PromotionAssertionResults(block_level_pass_rate=95,
  overall_pass_rate=88), reviewer_verdict='PASS', runs_per_fixture=3,
  corpus='F082')}`; `effective['architecture']` RETURNED `'cheap'` (seed
  `'top'`); routed_call for `design_worker` RETURNED `{'task_class':
  'architecture', 'tier': 'cheap', 'reason': 'per_project_override',
  'promoted_by': 'qwen3-8b-instruct + q4_k_m@0f1e2d3c4b5a6978 on F082'}`;
  provider/model/effort `'ollama' 'muse-glimmer:latest' 'medium'`;
  **warnings raised (0)**.
- SPEC (i) TIERS ONLY — reader RETURNED `{}`; `effective['architecture']`
  RETURNED `'top'`; routed_call RETURNED `{'task_class': 'architecture', 'tier':
  'top', 'reason': 'seed_mapping', 'promoted_by': None}`; **warnings raised (2)**,
  both with the FULL TEXT `model_routing.task_class_tiers: per-project
  model-routing overrides REFUSED; routing against the shipped table instead.
  Violated rules: promotion_without_evidence.` (two, because
  `resolve_effective_task_class_tiers` is called once directly and once through
  the seam — unchanged from before this round).
- SPEC (j) NEITHER TABLE — reader RETURNED `{}`; `effective['architecture']`
  RETURNED `'top'`; routed_call RETURNED `{'task_class': 'architecture', 'tier':
  'top', 'reason': 'seed_mapping', 'promoted_by': None}`; warnings raised (0).
- SPEC (k) MALFORMED, a bare string where the table belongs — reader RETURNED
  `{}`; `effective['architecture']` RETURNED `'top'`; routed_call RETURNED
  `{'task_class': 'architecture', 'tier': 'top', 'reason': 'seed_mapping',
  'promoted_by': None}`; provider/model/effort UNCHANGED at `'ollama'
  'muse-glimmer:latest' 'medium'`; warnings raised (2), the same refusal text as
  (i) — the tiers table alone still promotes without evidence.

**G6 THE RED PROOF.** Worktree
`/home/decodeux/Repos/remedy/remedy-review-r13-redproof`, detached at
`be850b92`, NEVER `cd`-ed into. `__pycache__` purged before every run (0 dirs
found each time, because `python3 -B` writes none) and every run used
`python3 -B -m pytest … -q` with `cwd=` the worktree. Module `__file__` printed
FROM INSIDE it — `role_config.__file__ =
/home/decodeux/Repos/remedy/remedy-review-r13-redproof/packages/orchestration/role_config.py`,
`model_routing.__file__ =
/home/decodeux/Repos/remedy/remedy-review-r13-redproof/packages/orchestration/model_routing.py`
— so no editable install shadowed the worktree.

NODE-ID PARSE: as G6 orders, EVERYTHING AFTER THE FIRST SPACE of a `FAILED …`
line. None of this round's tests is parametrized, so for every red line that
parse and the ` - <message>`-trimmed form are IDENTICAL; both were printed side
by side, and one RAW line was printed beside the parsed set each time with
`raw line's own after-first-space IS IN the parsed set: True`.

- CONTROL: exit **0**, **101 passed**, 0 failed, 0 errors, red list empty.
- (i) evidence NOT passed to `build_effective_task_class_tiers`: exit **1**,
  99 passed / **2 failed**. FULL red list:
  `tests/orchestration/test_role_config.py::TestPromotionEvidenceReachesTheSeam::test_a_routed_call_names_what_promoted_it`,
  `tests/orchestration/test_role_config.py::TestPromotionEvidenceReachesTheTableBuilder::test_a_promotion_with_evidence_is_accepted_end_to_end`.
  RAW: `FAILED tests/orchestration/test_role_config.py::TestPromotionEvidenceReachesTheTableBuilder::test_a_promotion_with_evidence_is_accepted_end_to_end`.
  Revert `git checkout -- packages/orchestration/role_config.py` exit 0; back to
  control exit 0, 101 passed — RESTORED.
- (ii) evidence NOT passed to `route_role_call`: exit **1**, 100 passed /
  **1 failed**. FULL red list:
  `tests/orchestration/test_role_config.py::TestPromotionEvidenceReachesTheSeam::test_a_routed_call_names_what_promoted_it`.
  RAW: the same line prefixed `FAILED `. Revert exit 0; back to control exit 0,
  101 passed — RESTORED.
- (iii) the reader returns the RAW mapping instead of the parsed records: exit
  **1**, 99 passed / **2 failed**. FULL red list:
  `…::TestPromotionEvidenceReachesTheSeam::test_a_routed_call_names_what_promoted_it`,
  `…::TestPromotionEvidenceReachesTheTableBuilder::test_a_promotion_with_evidence_is_accepted_end_to_end`.
  RAW: `FAILED tests/orchestration/test_role_config.py::TestPromotionEvidenceReachesTheTableBuilder::test_a_promotion_with_evidence_is_accepted_end_to_end`.
  Revert exit 0; back to control exit 0, 101 passed — RESTORED.
- (iv) the not-a-Mapping guard dropped from the reader: exit **1**, 99 passed /
  **2 failed**. FULL red list:
  `tests/orchestration/test_role_config.py::TestMalformedPromotionEvidenceIsNotACrash::test_a_bare_string_still_resolves_a_routed_call`,
  `tests/orchestration/test_role_config.py::TestMalformedPromotionEvidenceIsNotACrash::test_a_bare_string_where_the_table_belongs_reads_as_empty`.
  RAW: `FAILED tests/orchestration/test_role_config.py::TestMalformedPromotionEvidenceIsNotACrash::test_a_bare_string_where_the_table_belongs_reads_as_empty`.
  Revert exit 0; back to control exit 0, 101 passed — RESTORED.

PAIRWISE DISJOINTNESS, MEASURED — reported as a result, not as a fault:
(i)×(ii) OVERLAP on `…TestPromotionEvidenceReachesTheSeam::test_a_routed_call_names_what_promoted_it`;
(i)×(iii) OVERLAP on BOTH ids — mutation (i) and mutation (iii) produce
IDENTICAL red sets, because a raw mapping reaching the builder and no mapping
reaching it both end the promotion; (i)×(iv) DISJOINT;
(ii)×(iii) OVERLAP on the seam test; (ii)×(iv) DISJOINT; (iii)×(iv) DISJOINT.
So the four red sets are NOT pairwise disjoint; three of the six pairs overlap.
Each mutation is nonetheless individually detected, and (ii) and (iv) each have
a red set no other mutation reproduces.

`git status --porcelain` ON THE PRIMARY CHECKOUT was read immediately after every
mutation and after every revert — `''` (empty) on all eight readings, and `''`
before anything started.

**G7 THE SUITES.** Each its own invocation, run serially, all exit 0. Reviewer's
measurement at `f943e436` in brackets.

| Command | Result | vs base |
|---------|--------|---------|
| `pytest tests/orchestration/test_role_config.py -q` | `101 passed in 0.35s`, exit 0 | [92 at base, +new] — **+9**, the nine tests C4 adds |
| `pytest tests/orchestration/test_model_routing.py -q` | `406 passed, 3 skipped, 1 warning in 2.82s`, exit 0 | [406 passed, 3 skipped] UNMOVED |
| `pytest tests/orchestration/test_config.py -q` | `81 passed in 0.35s`, exit 0 | [81] UNMOVED |
| `pytest tests/orchestration/test_orchestrator_model_routing.py -q` | `20 passed in 0.23s`, exit 0 | [20] UNMOVED |
| `pytest tests/orchestration/test_teacher_model.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_job_role_routing.py tests/cli/test_teach_cmd.py -q` | `68 passed in 4.92s`, exit 0 | [68] UNMOVED |
| `pytest tests/cli/test_init_cmd.py tests/cli/test_worker_facade_cmd.py tests/orchestration/test_budget_stop_integration.py tests/orchestration/test_checkpoints.py tests/orchestration/test_dead_model_list.py tests/orchestration/test_f018_authority_integration.py -q` | `304 passed in 9.34s`, exit 0 | [304] UNMOVED |
| `pytest tests/runtimes/test_runtime_config.py tests/runtimes/test_runtime_lifecycle_safety.py tests/test_data_paths.py tests/ui_server/test_command_channel.py -q` | `199 passed in 55.90s`, exit 0 | [199] UNMOVED |
| `pytest tests/docs/ -q` | `295 passed in 0.44s`, exit 0 | [295] UNMOVED — the docs gate constraint 6 names |
| `pytest tests/cli/test_golden_path.py -q` | `42 passed in 20.75s`, exit 0 | [42] UNMOVED — the canary |

ONLY the suite this round adds to moved. The `1 warning` printed by the
model_routing suite is NOT something I measured at `f943e436` and the block's
bracket names only "406 passed, 3 skipped"; I report it rather than omit it.
This round cannot have introduced it: `model_routing.py` changed in its MODULE
DOCSTRING alone, that suite gained no test, and its pass and skip counts are
unmoved.

**G8 THE TREE, THE COMMITS AND THE SWEEP.**
`git status --porcelain` immediately before C6 is staged — EMPTY.
`git ls-files .remedy-wt` — EMPTY (no output).
`git worktree list` — only the primary checkout and the five pre-existing,
unrelated `.remedy-wt/job-*` worktrees; NO worktree of this round's making
survives, and `ls -d /home/decodeux/Repos/remedy/remedy-review-r13-redproof`
answers `No such file or directory`.
`ls /home/decodeux/Repos/remedy/remedy.toml` — `No such file or directory`;
constraint 12 holds, no `remedy.toml` exists in the repository root.
`git diff --stat f943e436..be850b92 -- packages/ apps/
':(exclude)packages/orchestration/role_config.py'
':(exclude)packages/orchestration/model_routing.py'` — **EMPTY**, which is the
measured proof that `config.py` was not touched.
`git diff --stat f943e436..be850b92 -- docs/` — exactly ONE file:
`docs/system/remedy-toml-configuration-system-v0.md | 40 +++--`,
`1 file changed, 36 insertions(+), 4 deletions(-)`. Nothing under
`docs/roadmap/`.

PER-COMMIT INSERTION COUNT, the `+` column only, cell by cell against the
`## Commits` table above, every one under the AGENTS.md 500-insertion cap
(DECISION F104 D1 counting rule):

| Commit | Insertions (+) | Handback table says | Under 500 |
|--------|----------------|---------------------|-----------|
| `745c5665` C0a | 316 | +316 | yes |
| `347a84bb` C0b | 219 | +219 | yes |
| `b26b1656` C1 | 14 | +14 | yes |
| `054807b5` C2 | 6 (3 + 3) | +3 / +3 | yes |
| `8efa2330` C3 | 103 (17 + 86) | +17 / +86 | yes |
| `fecfbbed` C4 | 265 | +265 | yes |
| `be850b92` C5 | 36 | +36 | yes |

The handback commit itself is a verbatim rewrite of a single `.agent/**` state
file and is exempt under DECISION F104 D1.

## Authored-text proofs

- `.agent/authored/f110-r13.md` — produced by `shutil.copyfile` from
  `remedy-review-r9-scratch/f110-r13.md`, never re-emitted. `sha256sum` of the
  committed file:
  `b7f4c58449a0d61cbf2a753f29f250dc747843c0d246340ab6796a342de07d29`, identical
  to the digest the round's brief stated and to the scratch source on disk.
  316 lines.
- `.agent/last_block.md` — produced by `shutil.copyfile` from the COMMITTED
  `.agent/authored/f110-r13.md`. Same digest,
  `b7f4c58449a0d61cbf2a753f29f250dc747843c0d246340ab6796a342de07d29`.
- PLAN13 — extracted BY DELIMITER INDEX from the committed authored file, marker
  lines excluded, with a script (`remedy-review-r9-scratch/extract.py`, which
  locates `<<<BEGIN PLAN13>>>` / `<<<END PLAN13>>>` by `list.index` and joins the
  lines between them). 1874 bytes, 41 lines, no trailing newline. `cmp` against
  `.agent/plan.md` differs only by the ONE trailing newline the target's
  convention adds; `cmp` of slice-plus-that-byte against the file is exit 0.
- RECORD12 — same extractor, 5350 bytes, 1 line. Appended as `\n\n` + slice.
  Byte arithmetic and the ordered paragraph comparison both exact; see G3.
- SLIPS13 — same extractor, 1212 bytes, 1 line. Appended as `\n\n` + slice.
  Byte arithmetic exact; see G4.
- Nothing was retyped, and no slice was taken from the delegation prompt.

## Deviations & assumptions

1. **A STALE SENTENCE INSIDE `model_routing.py` THAT THE BLOCK FORBADE ME TO
   REPAIR — DECLARED, NOT FIXED.** `promotion_evidence_from_mapping`'s OWN
   docstring (`packages/orchestration/model_routing.py`, base lines 891–896)
   still reads "NOTHING IN PRODUCTION CALLS THIS YET, and a reader searching for
   the caller should find this sentence rather than a silence. The call arrives
   with the wiring round…". This round IS that wiring round, so the sentence is
   now false. Constraint 7 and G5 make ANY deletion outside the MODULE docstring
   a STOP, and repairing a function docstring requires exactly such a deletion.
   I applied the constraint as written and did not touch it. The module docstring
   two paragraphs up now names the caller correctly, so a reader who searches for
   it still lands on the truth first; but the function docstring contradicts it
   and should be repaired by the next round that is allowed to touch that region.
2. **A STALE COMMENT IN `config.py`, OUTSIDE THE CHANGE SET — DECLARED, NOT
   REPAIRED,** as constraint 9 orders. `packages/orchestration/config.py` lines
   672–676 read "NOTHING READS THIS KEY YET — the reader arrives with the wiring
   round, in packages/orchestration/role_config.py beside the one that already
   reads the tiers table." `resolve_promotion_evidence` is now that reader, so
   the first clause is false while the location it predicts is exactly right.
   `config.py` is explicitly outside this round's change set.
3. **THE G6 WORKTREE WAS CREATED TWICE.** My first `git worktree add` used
   `/home/decodeux/Repos/remedy-review-r13-redproof`, a sibling of the repository
   rather than a path inside it. That sits outside the gitignored
   `remedy-review-*` pattern the round names, so I removed and pruned it
   immediately, before running anything in it, and re-created it at
   `/home/decodeux/Repos/remedy/remedy-review-r13-redproof`, which
   `.gitignore:223` covers. Both add/remove pairs are listed under External
   actions. No test ran in the first worktree and no state of it survives.
4. **G2's `cmp` DOES NOT EXIT 0 ON THE BARE EXTRACTION, AND CANNOT.** G2 orders
   "`cmp` the PLAN13 extraction against `.agent/plan.md` — exit 0", while
   constraint 4 fixes `.agent/plan.md` as ending WITH a newline and the extractor
   yields none. The two clauses cannot both hold. I ran BOTH comparisons and
   reported both exit codes rather than picking the flattering one: bare
   extraction exit 1 with `cmp`'s own EOF message, extraction-plus-the-target's-
   newline exit 0. Constraint 4's "the TARGET wins" is what I applied. This is the
   same reading round 12's verdict recorded for PLAN12.
5. **PROSE BEYOND THE SPEC'S LETTER, IN THE MODULES' OWN IDIOM,** as the SPEC's
   own preamble invites ("write it in each module's own idiom and improve on any
   wording below that is worse than what you would write"): `role_config.py`'s
   MODULE docstring gained a paragraph naming where a documented run enters the
   routing, and `resolve_effective_task_class_tiers`' and
   `resolve_routed_call_evidence`' docstrings each gained a short passage about
   the evidence. No behaviour is affected and no existing sentence was made
   false by these additions.
6. **THE DOC EXAMPLE USES `architecture`, NOT the `summarize` of the neighbouring
   tiers example.** `summarize` is seeded at `cheap` — the cheapest tier — so an
   evidence record promoting it would document an impossible promotion. I used
   `architecture`, the class G5 and C4 both actually promote, so the example is
   true rather than merely well-shaped. `runs_per_fixture = 5` and the two pass
   rates 95 / 88 are deliberately NOT the module's bars, so the example does not
   restate the promotion bars SPEC (n) reserves to
   `docs/agents/model_routing_policy.md`.
7. **NO RUFF GATE WAS RUN**, per constraint 5, and none was added. Import blocks
   I touched were sorted the way that constraint describes: in
   `role_config.py` `PromotionEvidence` sits after `OverrideRefused` and before
   the lowercase names, and `promotion_evidence_from_mapping` between
   `build_effective_task_class_tiers` and `route_role_call`; in the test file the
   new ALL-CAPS names sort into the ALL-CAPS run,
   `PromotionAssertionResults` after `OriginatingTaskClassRequired`, and
   `is_task_class_promotion` at the head of the lowercase run. All touched files
   stay under the configured `line-length = 120`, verified by a scan.
8. **NO EXISTING TEST WAS EDITED, RENAMED, DELETED OR SKIPPED.** C4's numstat is
   `265 0` — zero deletions in the test file, which is the measurement rather
   than the claim. No blocked item arose under constraint 8.
9. **`.agent/decisions.md` AND `.agent/candidates.md` WERE NOT TOUCHED,** per
   constraint 4 and the change set. The commit sequence C0a → C0b → C1 → C2 → C3
   → C4 → C5 → C6 ran exactly as ordered, with no extra commit, no dropped commit
   and no reordering; no commit approached the insertion cap, so the
   pre-authorised split was never needed.

## Next

The ACCEPTANCE ROUND: a fixture run whose every call's evidence shows class, tier
and reason, per `docs/roadmap/features/T3_F110.md`'s Acceptance section, plus the
reviewer/worker pairing assertion that section also names. After it, the
INTEGRATION GATE ROUND, which will have to run the full suite against a fresh
worktree with the base-worktree parity repair applied (R-0736: `copytree` keeps
mtimes while `worktree add` stamps newer, which produced ~114 false base
failures), plus a cold-`dist` build so the packaging suites are not red from a
stale build, and then re-run at minimum the nine suites of this round's G7 plus
whatever the gate's own inventory names. Then the closure sequence, which also
runs the one checklist consolidation pass DECISION F110 D1 carries into it and
updates the Design and Task-slicing bullets of
`docs/roadmap/features/T3_F110.md`.
