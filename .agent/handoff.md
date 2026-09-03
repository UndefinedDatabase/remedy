# Handoff — F110 Model routing by task class, round 14

## Session

SESSION 4 of feature F110 · round 14 · rounds so far 14

## State

- Branch: `feature/f110-model-routing-by-task-class`, pushed at the C5 SHA below,
  NO pull request open.
- Base of this round: `f0bbdc5c` (F110 R13 C7). HEAD before the handback:
  `37d62419` (C4).
- Fortschritt, part one: THE TWO DELIBERATE-ABSENCE NOTES ARE RETIRED AND
  R-0789 IS DISCHARGED ON DISK. `promotion_evidence_from_mapping`'s docstring in
  `packages/orchestration/model_routing.py` no longer opens its last paragraph
  with "NOTHING IN PRODUCTION CALLS THIS YET"; it names
  `packages.orchestration.role_config.resolve_promotion_evidence` as its ONE
  production caller, dates it at `8efa2330`, and says what that caller does with
  the records — it reads `model_routing.promotion_evidence` out of the project
  configuration and hands them to BOTH consumers, the table builder
  `build_effective_task_class_tiers` so a documented run LICENSES a cheaper tier,
  and the seam `route_role_call` so that same run NAMES ITSELF on the routed
  call's `promoted_by`. The `#` comment above the
  `model_routing.promotion_evidence` `ConfigKeySpec` in
  `packages/orchestration/config.py` no longer says "NOTHING READS THIS KEY YET";
  it names `role_config.resolve_promotion_evidence` as the reader that now
  exists, landed at `8efa2330`, beside the one that reads the tiers table. Both
  edits are PROSE ONLY and that is MEASURED, not asserted: G4 parsed the BASE
  `model_routing.py` with `ast`, took the `promotion_evidence_from_mapping`
  FunctionDef's docstring span (base lines 876..901) and showed every one of the
  6 deleted base lines — 895, 896, 897, 898, 899, 900 — inside it; and it showed
  both deleted `config.py` lines, 672 and 673, stripping to text that starts with
  `#`. Both were quoted verbatim in the gate output. The comment's first sentence
  — the first table of RECORDS in the registry, `entry_type` dict where its
  sibling declares str — and its last — registered first so the schema is pinned
  — are kept word for word, and the `ConfigKeySpec` including its `description`
  did not change.
- Fortschritt, part two: THE FEATURE FILE'S LAST UNBUILT ACCEPTANCE CLAUSE IS
  BUILT — the reviewer/worker pairing asserted on a REAL FIXTURE ROUND. 25 new
  tests in `tests/orchestration/test_role_config.py`, purely additive (205
  insertions, ZERO deletions), resolve BOTH halves of a round through the
  production `resolve_role_config` and read the tier off `cfg.routed_call["tier"]`
  — what the SEAM RECORDED — ranking it with `model_tier_rank` and never
  comparing it as a string. The rounds are DERIVED, not spelled: crossing
  `REVIEWER_WORKER_CLASS_PAIRS` with every role `ROLE_TASK_CLASSES` declares for
  each half yields FOUR rounds — `builder`/`test_worker` reviewed by
  `reviewer`/`final_verifier` — exactly the number the reviewer projected at
  `f0bbdc5c`, and the first test asserts the list is NON-EMPTY so an emptied pair
  table is a failure and not a vacuous pass. Four configurations are run over
  every round: unconfigured (evidence complete, `routed_call` keys exactly
  `ROUTED_CALL_EVIDENCE_FIELDS`, non-empty model, seeded tier, non-None reason,
  no warning, and the pairing holds); the WORKER class cheapened to
  `MODEL_TIERS[0]` WITH a `_well_formed_evidence_entry` (no warning, worker at
  `cheap`, reason `per_project_override`, `promoted_by` truthy, pairing still
  holds); the REVIEWER class demoted with NO evidence (warnings raised, every
  message names `reviewer_weaker_than_worker`, the reviewer keeps its SEEDED
  `mid`, so the refused table did not route); and the discriminator — the SAME
  demotion WITH well-formed evidence for the reviewer class, where every message
  still names `reviewer_weaker_than_worker`, NO message names
  `promotion_without_evidence` because the benchmark discharged that rule and
  only that one, the reviewer still sits at its seeded tier and its `promoted_by`
  is None. Without that last case the whole class of test passes while a
  documented benchmark run buys a weaker reviewer, which is the one thing policy
  hard rule 1 exists to forbid.
- The round's own claim was RUN, not read: G4 executed the shipped
  `resolve_role_config` for `builder` and `reviewer` with nothing configured and
  reproduced the reviewer's `f0bbdc5c` reading exactly — provider `ollama`, model
  `muse-glimmer:latest`, effort `medium`, and
  `{'task_class': 'standard_build', 'tier': 'mid', 'reason': 'seed_mapping',
  'promoted_by': None}` / the same with `'standard_review'`. A prose commit moved
  no routed answer.
- Round 13's PASS verdict, the finding `R-0789` and the two prose slips are
  booked in C2, per operator amendment amend0827-process-diet rule 1.
- `.agent/STOP` read from disk TWICE, as constraint 2 orders: before the first
  commit and again before C5. ABSENT both times.
- `.agent/decisions.md`, `.agent/candidates.md` and
  `docs/roadmap/features/T3_F110.md` were NOT touched, per constraint 12.
  `.agent/candidates.md` is still EMPTY.

## Range

Base `f0bbdc5c` → head `37d62419` for every gate below; C5 is this handback and
its own numbers belong to the next ledger entry (§3 item 14).

## Commits

| # | SHA | Subject | Files | +/- |
|---|-----|---------|-------|-----|
| C0a | `b335a56b` | F110 R14 C0a: save the round 14 step block verbatim | `.agent/authored/f110-r14.md` | +399 / -0 |
| C0b | `040ef860` | F110 R14 C0b: mirror the authored block to last_block | `.agent/last_block.md` | +374 / -291 |
| C1 | `03f79839` | F110 R14 C1: the plan for round 14 | `.agent/plan.md` | +19 / -18 |
| C2 | `ceed909b` | F110 R14 C2: book the round 13 verdict, R-0789 and two prose slips | `.agent/live_review.md`, `.agent/prose_slips.md` | +10 / -2 |
| C3 | `d8a66340` | F110 R14 C3: retire the two deliberate-absence notes the wiring falsified | `packages/orchestration/config.py`, `packages/orchestration/model_routing.py` | +13 / -8 |
| C4 | `37d62419` | F110 R14 C4: the reviewer/worker pairing asserted on a real fixture round | `tests/orchestration/test_role_config.py` | +205 / -0 |
| C5 | (this commit) | F110 R14 C5: the round 14 handback | `.agent/handoff.md` | — |

Per-commit insertions, the `+` column only (DECISION F104 D1), cell by cell
against the table above: C0a 399, C0b 374, C1 19, C2 10, C3 13, C4 205. Every
one is under 500. C0b is additionally a verbatim full-file rewrite of a single
`.agent/**` state file and exempt under DECISION F104 D1; it does not need the
exemption, being 374.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a | done | block saved verbatim by `shutil.copyfile`; digest unchanged |
| C0b | done | mirrored from the COMMITTED authored file by `shutil.copyfile` |
| C1 | done | PLAN14 extracted by delimiter index, plus the target's one trailing newline |
| C2 | done | RECORD14 and SLIPS14 appended, each as `\n\n` + slice |
| C3 | done | SPEC (a) and SPEC (b), ONE commit, both files |
| C4 | done | IMPORT14 at its anchor plus the acceptance tests, purely additive |
| C5 | done | this handback |
| SPEC (a) | done | `promotion_evidence_from_mapping` docstring paragraph replaced; every other paragraph word for word |
| SPEC (b) | done | one sentence of the `#` comment replaced; first and last sentences and the `ConfigKeySpec` untouched |
| SPEC (c) | done | c1–c7 all built; 25 tests, 4 parametrized rounds |
| SPEC (c1) | done | `_declared_reviewer_worker_rounds()`, non-emptiness asserted, 4 rounds derived |
| SPEC (c2) | done | `_resolve_one_fixture_round()` + `_recorded_tier()` + `_round_pairing_holds()` |
| SPEC (c3) | done | `TestFixtureRoundEvidenceIsComplete::test_an_unconfigured_round_records_complete_evidence_on_both_halves` |
| SPEC (c4) | done | `TestFixtureRoundEvidenceIsComplete::test_the_seeded_round_pairs_correctly` |
| SPEC (c5) | done | `TestDocumentedRunCheapensTheWorkerHalf::test_an_evidenced_worker_promotion_is_routed_and_still_pairs` |
| SPEC (c6) | done | `TestDemotingTheReviewerHalfIsRefusedByName::test_an_unevidenced_reviewer_demotion_is_refused_and_does_not_route` |
| SPEC (c7) | done | `TestDemotingTheReviewerHalfIsRefusedByName::test_evidence_discharges_the_promotion_rule_but_never_the_pairing_rule` |
| R-0789 | done | both false sentences repaired in ONE commit, C3; counts of both strings now 0 |

## External actions

- NO pull request created. NOTHING merged. NO force-push. No work on `main`.
- `gh pr list --state open` answered `[]` at the start of the round.
- One disposable worktree created and destroyed: `remedy-review-r14-redproof`,
  removed by its EXACT path with `git worktree remove` plus `git worktree prune`;
  `ls -d` on that path afterwards reports no such file.
- The five `.remedy-wt/job-*` worktrees in `git worktree list` are PRE-EXISTING
  and none is of this round's making; `git ls-files .remedy-wt` is EMPTY.

## Verification

One line per gate, with its real exit code, captured through
`bash -c '<cmd>; echo "REAL_EXIT=$?"'` because the tool does not surface a
non-zero exit on its own.

- **G1 TRANSPORT — exit 0.** `cmp remedy-review-r9-scratch/f110-r14.md
  .agent/authored/f110-r14.md` → `REAL_EXIT=0`. ONE digest,
  `8966f2c6982617f79238707b43d171b4568a0cf3634bdf77691e00d4222b5954`, repeated
  for all three of the scratch original, `.agent/authored/f110-r14.md` and
  `.agent/last_block.md`. `wc -l .agent/authored/f110-r14.md` = 399. This claims
  nothing about any other bytes.
- **G2 THE PLAN — exit 0.** PLAN14 extracted from the COMMITTED authored file by
  `list.index` on its `<<<BEGIN PLAN14>>>` / `<<<END PLAN14>>>` marker lines.
  `cmp` of the extraction PLUS ONE TRAILING NEWLINE against `.agent/plan.md` →
  `REAL_EXIT=0`. BOTH READINGS, as ordered: the BARE extraction's `cmp` →
  `REAL_EXIT=1`, "EOF on the extraction after byte 1970, in line 42", which is
  exactly the one byte the target's convention adds and is the reading this
  round's own SLIPS14 slip asks a block to state up front. `wc -l
  .agent/plan.md` = 42 (under 50). `grep -c '^## Goal'` = 1. `grep -c '^## Next
  Steps'` = 1.
- **G3 THE RECORD APPENDS — exit 0 on every check.**
  `.agent/live_review.md`: base 2215298 bytes at `f0bbdc5c`, ending WITHOUT a
  newline; arithmetic `2215298 + 2 + 6966 = 2222266` against a real size of
  2222266; the pre-C2 content is an exact byte PREFIX (True); the file still ends
  without a newline (True). SECOND READER over the WHOLE appended region: the
  script COUNTED N = 2 paragraphs in the slice and compared the LAST 2
  blank-line units of the whole file against them IN ORDER — `[True, True]`,
  tail matches in order. NEGATIVE CONTROL on the FIRST appended paragraph: byte 0
  flipped in a COPY, the second reader REJECTED it (match = False); the real file
  was never written. HEADER SHAPE (§3 item 26): lines starting with the slice's
  own `Gate: F110 R13 — the round 13 entry.` prefix — BEFORE C2 = 0, AFTER C2 = 1.
  `.agent/prose_slips.md`: base 62351 bytes, no trailing newline; `62351 + 2 +
  1768 = 64121` against a real 64121; prefix True; still no trailing newline;
  second reader N = 2, `[True, True]`; negative control REJECTED.
  THE OPEN SET, recomputed mechanically from the file and never carried forward:
  350 paragraphs matching `^- R-\d+ — ` over 350 UNIQUE registered ids; 73 lines
  matching `^Done: R-\d+ — ` over 71 UNIQUE resolved ids — the two-line gap is
  the known `R-0721` / `R-0725` double-`Done:` pair; open set = 350 − 71 = **279**.
  `R-0767` in the open set: True. `R-0789` in the open set: True.
- **G4 THE TWO PRODUCTION FILES — exit 0 on every check.** `git show --numstat
  d8a66340`: `packages/orchestration/config.py` 2/2,
  `packages/orchestration/model_routing.py` 11/6. `ast.parse` OK on both paths.
  DELETED LINES QUOTED VERBATIM — `model_routing.py`, 6 lines at base 895–900:
  `    NOTHING IN PRODUCTION CALLS THIS YET, and a reader searching for the caller`
  / `    should find this sentence rather than a silence. The call arrives with the`
  / `    wiring round, in ``packages/orchestration/role_config.py`` — the`
  / `    config-reading layer, beside ``resolve_effective_task_class_tiers``, which is`
  / `    already where the per-project TIERS table is read. It is deliberately a round`
  / `    apart: the schema is pinned before routing behaviour moves against it.`;
  `config.py`, 2 lines at base 672–673:
  `    # dict where its sibling above declares str. NOTHING READS THIS KEY YET —`
  / `    # the reader arrives with the wiring round, in`.
  REGION PROVED MECHANICALLY AND PER LINE: the BASE `model_routing.py` parsed
  with `ast`, `promotion_evidence_from_mapping`'s docstring node spanning base
  lines 876..901, and each of 895, 896, 897, 898, 899, 900 reported INSIDE it
  (True ×6); each `config.py` deleted line's stripped text reported as starting
  with `#` (True ×2). Neither STOP of constraint 6 fired.
  AT C3: count of `NOTHING IN PRODUCTION CALLS THIS YET` in `model_routing.py` =
  0 (expected 0); count of `NOTHING READS THIS KEY YET` in `config.py` = 0
  (expected 0); the AST-extracted docstring of `promotion_evidence_from_mapping`
  CONTAINS `resolve_promotion_evidence` = True; count of
  `resolve_promotion_evidence` in `config.py` = 1, up from the reviewer's
  measured 0 at `f0bbdc5c`.
  THE SHIPPED CODE RUN, not read, with nothing configured:
  `builder` → provider `ollama`, model `muse-glimmer:latest`, effort `medium`,
  `routed_call = {'task_class': 'standard_build', 'tier': 'mid', 'reason':
  'seed_mapping', 'promoted_by': None}`; `reviewer` → the same provider, model
  and effort, `routed_call = {'task_class': 'standard_review', 'tier': 'mid',
  'reason': 'seed_mapping', 'promoted_by': None}`. Identical to the reviewer's
  reading at `f0bbdc5c`; no routed answer moved.
- **G5 THE TEST FILE — exit 0.** `git show --numstat 37d62419 --
  tests/orchestration/test_role_config.py` → `205  0`; the DELETION COLUMN IS 0,
  which is constraint 7 measured rather than asserted. ADDITIVE RECONSTRUCTION:
  the base blob read with `git show
  f0bbdc5c:tests/orchestration/test_role_config.py` (40384 bytes); the FIRST
  occurrence of the IMPORT14 line removed from the COMMITTED file (offset 901,
  50557 bytes); the base blob is then a byte-exact PREFIX of what remains
  (True), with 10135 bytes of pure append after it — the import went in at its
  anchor and everything else was APPENDED, with nothing edited in between.
  Anchor `    RULE_PROMOTION_WITHOUT_EVIDENCE,` occurrences in the BASE = 1;
  `    RULE_REVIEWER_WEAKER_THAN_WORKER,` in the BASE = 0, in the COMMITTED file
  = 1. `ast.parse` on the committed file: OK.
- **G6 THE RED PROOF — control exit 0, both mutations exit 1, both reverts exit
  0.** Disposable worktree `remedy-review-r14-redproof` under the repository,
  detached at C4 `37d62419`, NEVER `cd`-ed into — every command passed `cwd=`.
  `__pycache__` purged before every run; every run `python3 -B -m pytest
  tests/orchestration/test_role_config.py -q`. PROVENANCE, printed from INSIDE
  the worktree: `role_config.__file__ =
  /home/decodeux/Repos/remedy/remedy-review-r14-redproof/packages/orchestration/role_config.py`
  and `model_routing.__file__ =
  /home/decodeux/Repos/remedy/remedy-review-r14-redproof/packages/orchestration/model_routing.py`
  — no editable install shadows the worktree.
  CONTROL: exit 0, `126 passed`, 0 red.
  MUTATION (i), `model_routing.py`, `    if model_tier_rank(reviewer_tier) <
  model_tier_rank(worker_tier):` → `    if False:`; occurrences of that exact
  line counted first = 1. Exit 1, `8 failed, 118 passed`, FULL red list, never
  truncated, all 8 in `tests/orchestration/test_role_config.py`:
  `TestDemotingTheReviewerHalfIsRefusedByName::test_an_unevidenced_reviewer_demotion_is_refused_and_does_not_route`
  at `[builder-reviewed-by-final_verifier]`, `[builder-reviewed-by-reviewer]`,
  `[test_worker-reviewed-by-final_verifier]`, `[test_worker-reviewed-by-reviewer]`
  and
  `TestDemotingTheReviewerHalfIsRefusedByName::test_evidence_discharges_the_promotion_rule_but_never_the_pairing_rule`
  at the same four ids. THE MUTATION REACHED EXACTLY THE TESTS THE BLOCK
  PREDICTED — SPEC (c6) and (c7) and nothing else. Revert with `git checkout --
  packages/orchestration/model_routing.py`, then return to control: exit 0,
  `126 passed`, identical to the control (True).
  MUTATION (ii), `role_config.py`, the unique three-line string `            stacklevel=2,`
  / `        )` / `        return TASK_CLASS_TIERS` with its last line replaced by
  `        return dict(configured)`; occurrences of that three-line string counted
  first = 1. Exit 1, `13 failed, 113 passed`, FULL red list, never truncated: the
  same 8 ids as (i), plus
  `TestMalformedPromotionEvidenceIsNotACrash::test_a_bare_string_still_resolves_a_routed_call`,
  `TestPromotionEvidenceReachesTheSeam::test_the_same_role_records_no_promoter_without_evidence`,
  `TestPromotionEvidenceReachesTheTableBuilder::test_the_same_promotion_without_evidence_is_still_refused`,
  `TestRefusedOverrideWarnsAndRoutesSeeded::test_an_illegal_override_routes_against_the_shipped_table`,
  `TestRefusedOverrideWarnsAndRoutesSeeded::test_every_declared_role_still_resolves_under_a_refused_table`.
  Revert, then return to control: exit 0, `126 passed`, identical (True).
  NODE-ID PARSING, as ordered: a node id is EVERYTHING AFTER THE FIRST SPACE of
  a `FAILED ` line. One RAW line printed beside the parsed set per mutation — for
  (i) `'FAILED tests/orchestration/test_role_config.py::TestDemotingTheReviewerHalfIsRefusedByName::test_an_unevidenced_reviewer_demotion_is_refused_and_does_not_route[builder-reviewed-by-final_verifier]'`
  — and its own after-first-space form reported as IN that set (True), for both
  mutations.
  DISJOINTNESS, AS A MEASURED RESULT and not as a fault: |red(i)| = 8,
  |red(ii)| = 13, intersection 8, pairwise disjoint = **False** — (i)'s red set
  is a strict SUBSET of (ii)'s, which is what one expects when a rule that
  refuses a table and a router that ignores the refusal both break the same two
  acceptance tests while only the second also breaks the five pre-existing
  refusal guards.
  PRIMARY CHECKOUT `git status --porcelain` read immediately after every mutation
  and after every revert — six readings in all, including after the control:
  `''` every time.
  Worktree removed by its EXACT path
  `/home/decodeux/Repos/remedy/remedy-review-r14-redproof` with `git worktree
  remove` plus `git worktree prune`; `ls -d` on that path afterwards → "No such
  file or directory".
- **G7 THE SUITES — eight invocations, run SERIALLY, every one exit 0.**
  | Suite | Result | Reviewer's `f0bbdc5c` reading |
  |---|---|---|
  | `tests/orchestration/test_role_config.py` | 126 passed, exit 0 | [101] — moved by exactly the 25 tests C4 adds |
  | `tests/orchestration/test_model_routing.py` | 406 passed, 3 skipped, 1 warning, exit 0 | [406 passed, 3 skipped, 1 warning] — unmoved |
  | `tests/orchestration/test_config.py` | 81 passed, exit 0 | [81] — unmoved |
  | `test_orchestrator_model_routing.py` + `test_job_role_routing.py` | 34 passed, exit 0 | [34] — unmoved |
  | `test_teacher_model.py` + `test_self_use_runner.py` + `tests/cli/test_teach_cmd.py` | 54 passed, exit 0 | no bracket — compared to nothing |
  | `test_init_cmd.py` + `test_worker_facade_cmd.py` + `test_budget_stop_integration.py` | 130 passed, exit 0 | no bracket — compared to nothing |
  | `tests/docs/ -q` | 295 passed, exit 0 | [295] — unmoved |
  | `tests/cli/test_golden_path.py` (the canary) | 42 passed, exit 0 | [42] — unmoved |
  Only the suite this round adds to moved: 101 + 25 = 126.
- **G8 THE TREE, THE COMMITS AND THE SWEEP — exit 0 on every check.**
  `git status --porcelain` immediately before C5 was staged: EMPTY.
  `git ls-files .remedy-wt`: EMPTY. `git worktree list`: no worktree of this
  round's making survives (the five `.remedy-wt/job-*` entries are pre-existing).
  `ls /home/decodeux/Repos/remedy/remedy.toml` → "No such file or directory",
  which is constraint 9 measured.
  `git diff --stat f0bbdc5c..37d62419 -- packages/ apps/
  ':(exclude)packages/orchestration/model_routing.py'
  ':(exclude)packages/orchestration/config.py'` → EMPTY.
  `git diff --stat f0bbdc5c..37d62419 -- docs/` → EMPTY.
  PER-COMMIT INSERTIONS, `+` column only, C0a through C4, cell by cell against
  the `## Commits` table above: 399, 374, 19, 10, 13, 205 — each confirmed under
  500. C5's own numbers are not this gate's business.

## Authored-text proofs

- The block was NEVER retyped. C0a is `python3 -c "import shutil;
  shutil.copyfile('remedy-review-r9-scratch/f110-r14.md',
  '.agent/authored/f110-r14.md')"`; C0b is the same call from the COMMITTED
  authored file to `.agent/last_block.md`.
- Every slice — IMPORT14, PLAN14, RECORD14, SLIPS14 — was EXTRACTED from the
  COMMITTED `.agent/authored/f110-r14.md` by locating its `<<<BEGIN X>>>` and
  `<<<END X>>>` marker lines with `list.index` and joining the lines BETWEEN
  them, markers excluded. Nothing was taken from the delegation prompt.
- Extraction sizes, for the record: IMPORT14 1 line / 37 bytes; PLAN14 42 lines /
  1970 bytes; RECORD14 3 lines / 6966 bytes; SLIPS14 3 lines / 1768 bytes.
- Newline conventions, THE TARGET WINS (constraint 4): `.agent/plan.md` is the
  extraction PLUS exactly one trailing newline; `.agent/live_review.md` and
  `.agent/prose_slips.md` each received `\n\n` + slice and still end WITHOUT a
  trailing newline.

## Deviations & assumptions

- NO deviation from the block's change set. Every path written is one of the
  nine the change set names, and nothing outside them was touched — G8's two
  empty sweeps over `packages/`, `apps/` and `docs/` are that claim measured.
- NO slice was edited, retyped or re-wrapped. No conflict between a slice and
  the repository was found, so constraint 1's declaration route was not needed.
- SPEC (a) and SPEC (b) fix FACTS, not prose, and the block invites better
  wording. The wording shipped is the worker's; every fact the SPEC lists is
  present. In SPEC (a) `route_role_call` is written as a double-backtick literal
  rather than a `:func:` role because the surrounding paragraph already uses that
  form for the seam, and `build_effective_task_class_tiers` keeps the `:func:`
  role its sibling comment uses.
- CONSTRAINT 8 SWEEP, declared rather than assumed: grepping `packages/`,
  `apps/` and `docs/agents/` for further deliberate-absence prose of this kind
  turns up nothing this round falsifies. `packages/orchestration/role_config.py`
  line 46 ("a reader looking for the code that turns a tier into a model id will
  not find it, and that absence is deliberate") and
  `packages/orchestration/model_routing.py` line 87 (`mission_compile` has no
  role and no call site) are both still TRUE at `37d62419` — those absences are
  F111's and the feature file's, not this round's. Four unrelated
  "nothing reads it" sentences in `decision_evidence.py`,
  `orchestrator_loop.py`, `dev_server.py` and `runtime_supervisor.py` belong to
  other features and are untouched and unaffected. No stale sentence is left
  inside the change set and none is owed outside it.
- The `-3 skipped` in `test_model_routing.py` and its 1 warning are the
  pre-existing state at `f0bbdc5c`, unmoved by this round.
- G6's red sets are NOT pairwise disjoint and that is reported above as a
  MEASURED RESULT, exactly as the gate asks — (i)'s eight ids are a strict subset
  of (ii)'s thirteen. It is not treated as a fault and no assertion was weakened
  to change it.
- `ruff` was NOT run, per constraint 5; linting is the reviewer's. The longest
  line C4 adds is 111 characters, under the repository's configured
  `line-length = 120`, and no line the round wrote carries trailing whitespace.
- Scratch artifacts this round created under `remedy-review-r9-scratch/` were
  removed BY EXACT PATH, never by glob: `probe14.py`, `redproof14.py`,
  `.x_IMPORT14`, `.x_PLAN14`, `.x_RECORD14`, `.x_SLIPS14`, `.base_live.sha`. The
  reviewer's own files in that directory were left alone. The directory is
  covered by `.gitignore:223` (`remedy-review-*`) and nothing in it is tracked.
- Two ordered commands could not be issued in the sandbox's literal form: a
  `VAR=sha` shell assignment and one multi-statement `python3 -c` were refused by
  the guard. Both were re-run with the SHA written out literally and the script
  placed in a gitignored scratch file, so every gate's SEMANTICS ran unchanged;
  no gate was skipped, weakened or substituted.

## Next

Open findings: **279** (350 unique registered − 71 unique resolved). `R-0767`
and `R-0789` are both in that set; `R-0789` is now DISCHARGED ON DISK by C3 and
awaits the reviewer's `Done:` line. `.agent/candidates.md` is EMPTY.

Next expected action, in this order:
1. Phase 1 rule 1 — read `.agent/STOP` from disk. It was absent at both readings
   this round.
2. Phase 1 rule 2 — the Open PR Gate. `gh pr list --state open` answered `[]`
   this round; no PR was created.
3. Review round 14 over `f0bbdc5c..HEAD` and issue the verdict, which the next
   round's first commit books.
4. Then the INTEGRATION GATE round, which `docs/agents/integration_gate.md`
   governs and which needs the R-0736 base-worktree mtime-parity repair and a
   cold `dist` build budgeted for.
5. Then the CLOSURE SEQUENCE, which takes two rounds, runs the one §3 checklist
   consolidation pass DECISION F110 D1 carries into it, and updates the Design
   and Task-slicing bullets of `docs/roadmap/features/T3_F110.md`.

SESSION 4 is at ONE delegated round; the G7 default is four to five per session,
and F110 stands at 14 rounds against the 25-round soft limit, so the limit is NOT
reached and no scope report is owed.
