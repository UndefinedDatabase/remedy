── STEP F110 R18 — CLOSURE ROUND 3: THE BUILT STATE SECTION ──
Round 18 · SESSION 7 of F110 · base `2fe36572` (F110 R17 C3)

Goal:
  Book round 17's PASS verdict (the evidence job and review zip) as the
  `Gate: F110 R17` ledger entry, then give
  `docs/roadmap/features/T3_F110.md` its Built State section plus two
  small "AS BUILT" corrections to the Design section — appended after
  the original intent text, never a silent rewrite — closing closure
  precondition 4. No STATUS line, no README edit, no pull request happen
  here — that is round 19.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f110-r18.md`
  C0b  mirror the committed authored file to `.agent/last_block.md`
  C1   apply PLAN18 to `.agent/plan.md` (whole-file replacement)
  C2   append RECORD18 to `.agent/live_review.md`
  C3   apply the two FROM/TO pairs and append BUILTSTATE to
       `docs/roadmap/features/T3_F110.md`
  C4   the handback: rewrite `.agent/handoff.md`

Change set — NOTHING outside these paths:
  `.agent/authored/f110-r18.md`
  `.agent/last_block.md`
  `.agent/plan.md`
  `.agent/live_review.md`
  `docs/roadmap/features/T3_F110.md`
  `.agent/handoff.md`
  NO file under `packages/`, `apps/`, `tests/`, `.agent/decisions.md`,
  `.agent/prose_slips.md`, `.agent/candidates.md` or
  `scripts/self_use_queue.json` is touched by this round's own commits.
  This round mints NO finding id, writes no `- R-` entry and no `Done:`
  line.

Constraints:
  1. `.agent/STOP` is read FROM DISK before the first commit and again
     before C4. If it exists at either reading: finish the commit in
     hand, write the handback, push, and stop.
  2. Transport is PROMPT-EMBEDDED, not a scratch file (the reviewer is
     100% read-only and holds no separate scratch original). Copy the
     bytes between BEGIN BLOCK / END BLOCK (excluding those sentinel
     lines) verbatim into `.agent/authored/f110-r18.md`.
  3. Extract every slice from the COMMITTED `.agent/authored/f110-r18.md`
     by locating its `<<<BEGIN X>>>` / `<<<END X>>>` marker lines and
     taking the lines strictly between them — never from this prompt
     directly, never retyped.
  4. `.agent/plan.md` at C1 is REPLACED IN FULL by PLAN18. Report `wc -l`
     (must be under 50) and sha256.
  5. `.agent/live_review.md` at C2: the reviewer measured the base at
     `2fe36572` as exactly 2238252 bytes, ending WITHOUT a trailing
     newline. RECORD18 is 3221 bytes, one paragraph, zero internal
     newlines. The append is TWO newlines followed by RECORD18 verbatim,
     so the committed file must be EXACTLY 2238252 + 2 + 3221 = 2241475
     bytes, and the base bytes must be an exact PREFIX. Report the
     arithmetic and the prefix confirmation directly (compare the first
     2238252 bytes of the new file against the old file).
  6. Do NOT author any `- R-` entry, any `Done:` line, any
     `.agent/decisions.md` DECISION, or any `.agent/prose_slips.md` line
     this round.
  7. `docs/roadmap/features/T3_F110.md` at C3: apply PAIR1 (PAIR1_FROM
     replaced by PAIR1_TO — an APPEND-shaped pair, PAIR1_TO CONTAINS
     PAIR1_FROM verbatim as its own prefix, verified by the reviewer
     before this block was emitted: `PAIR1_FROM` occurs exactly ONCE in
     the base file), then PAIR2 the same way (`PAIR2_FROM` also occurs
     exactly ONCE, `PAIR2_TO` also CONTAINS `PAIR2_FROM` as its prefix).
     Apply both pairs as ONE commit (C3). Then APPEND BUILTSTATE to the
     end of the file: the reviewer measured the base (after both pairs
     are applied, before the append) as 3818 + (712 added by PAIR1) +
     (529 added by PAIR2) bytes, ending WITH exactly one trailing
     newline. The append is ONE newline (a blank line separator, matching
     every other `##`-heading boundary in this file) followed by
     BUILTSTATE verbatim (BUILTSTATE itself already ends with its own
     trailing newline, so no extra newline is added after it). Report the
     file's final byte count, confirm it ends with exactly one trailing
     newline, and confirm `grep -c '^## Built State'` reads 1.
  8. Do NOT run `ruff`, `npm`, or any formatter — this round touches no
     `.py` file.

Done when — each gate run and reported as ONE LINE in the handback with
its real exit code, at a commit STRICTLY EARLIER than C4:

G1 TRANSPORT — sha256sum of `.agent/authored/f110-r18.md` and
   `.agent/last_block.md` — must match. Report `wc -l`.

G2 THE PLAN — `wc -l .agent/plan.md` under 50; sha256; `grep -c '^## Goal$'`
   and `grep -c '^## Next Steps$'` each 1.

G3 THE LEDGER APPEND — the arithmetic from constraint 5, reproduced
   directly against the committed file; `grep -c '^Gate: F110 R17'` 0
   before C2, 1 after; confirm no new `^- R-` or `^Done: R-` line
   anywhere in the file (identical counts before/after C2).

G4 THE FEATURE FILE — for each pair, report the containment check
   (`TO.startswith(FROM)` — true/false) and the FROM count in the base
   file (must be 1 for each). Report the file's byte count after C3 and
   confirm it ends with exactly one trailing newline. Report
   `grep -c '^## Built State'` = 1, `grep -c '^## Design'` = 1 (unchanged
   heading count), `grep -c 'AS BUILT'` = 2 (one per pair).

G5 THE TREE, THE COMMITS AND THE SWEEP.
   `git status --porcelain` immediately before C4 — EMPTY.
   `git diff --stat 2fe36572..<C3-sha> -- packages/ apps/ tests/
   .agent/decisions.md .agent/prose_slips.md .agent/candidates.md
   scripts/self_use_queue.json` — must be EMPTY.
   PER-COMMIT INSERTIONS, the `+` column only, for C0a, C0b, C1, C2 and
   C3, reported cell by cell against the handback's own `## Commits`
   table and each confirmed under 500 (C0b may be a whole-file rewrite;
   report the real `git diff --numstat` cells).

Handback: rewrite `.agent/handoff.md` in full per
   docs/agents/handback_template.md — feature and round, SESSION 7 of
   F110, branch, base and head SHAs, the per-commit changed-files table
   with its `+/-` column, ONE line per gate above with its real exit
   code, the item-status table AGENTS.md mandates, the deviations, the
   open-findings count (278, UNCHANGED — no new id minted). Its `## Next`
   section names round 19 (the closure commit: STATUS line, README sync,
   `SU-006` `consumed_by=F110`, pull request) as the next expected
   action, and states plainly that round 17 already built the review zip
   (package `remedy-review-20260903-181544-READY_FOR_REVIEW.zip`,
   SHA-256
   `767304077110354d0005b2f6c70cd53502b831c4161be6a5f6a65a31c136457b`,
   accepted HEAD `953cade0`) so round 19 does not need to rebuild it. It
   has NO length cap. Then `git push -u origin
   feature/f110-model-routing-by-task-class` after C4; create NO pull
   request, merge nothing.

<<<BEGIN PLAN18>>>
# Plan — F110 Model routing by task class

Branch: feature/f110-model-routing-by-task-class, cut from `main` after
pull request 232 was merged at the Open PR Gate.

## Goal

End one-model-for-everything: every provider call declares a TASK CLASS, a
router maps classes to model tiers, and each routed call records the routed
model WITH its reason. The hard rules of
`docs/agents/model_routing_policy.md` are ENFORCED IN CODE, and moving a
class to a cheaper tier is possible only against documented benchmark
evidence — never by editing a mapping casually.

## Current Step

Round 18 — CLOSURE ROUND 3: THE BUILT STATE SECTION. Round 17's evidence
job and review zip are booked (`Gate: F110 R17`, PASS): package
`remedy-review-20260903-181544-READY_FOR_REVIEW.zip`, SHA-256
`767304077110354d0005b2f6c70cd53502b831c4161be6a5f6a65a31c136457b`,
accepted HEAD `953cade0`. This round gives
`docs/roadmap/features/T3_F110.md` its Built State section and corrects
two Design bullets against what actually shipped (the module is
`model_routing.py`, not `routing.py`; a violating override WARNS per
DECISION F110 D5, it does not fail validation) — both as APPENDED "AS
BUILT" corrections, never a silent rewrite of the original intent text.

## Next Steps

- Round 19: the closure commit — the authored STATUS `[x]` line and the
  README capability sync in the SAME commit, `SU-006`'s `consumed_by` set
  to `F110`, and the pull request.

## Risks

- The zip already built at round 17 is the one closure references; round
  19 does not rebuild it.
- `R-0767` stays OPEN on the same seam and must not be absorbed.
- `R-0784` stays OPEN; its fix belongs to F258's generator, not to F110.
<<<END PLAN18>>>

<<<BEGIN RECORD18>>>
Gate: F110 R17 — the round 17 entry. VERDICT PASS, over the range `e9e319e2..2fe36572`. THE ROUND BOOKED ROUND 16'S VERDICT AND BUILT THE CLOSURE EVIDENCE BUNDLE AND ZIP, AND THE REVIEWER RE-DERIVED EVERY VALUE FROM DISK RATHER THAN FROM THE HANDBACK. TRANSPORT, digest-fallback per docs/agents/self_drive_protocol.md: `.agent/authored/f110-r17.md` and `.agent/last_block.md` are byte-identical, sha256 `562a1f00c6b29d9fc645c6649fc37fe386e47bc55092a7822038ae629ec8523f` over 364 lines, reproduced by the reviewer directly against the committed blob and against the prompt bytes it emitted. THE PLAN IS BYTE-CORRECT: `.agent/plan.md` at C1 is 42 lines with `## Goal` and `## Next Steps` each occurring once. THE LEDGER APPEND HOLDS UNDER THE REVIEWER'S OWN ARITHMETIC: base at `e9e319e2` measured 2232554 bytes ending without a trailing newline, RECORD17 measured 5696 bytes with zero internal newlines, and the committed file is exactly 2232554 + 2 + 5696 = 2238252 bytes, its first 2232554 bytes an exact byte-for-byte PREFIX of the base — the reviewer re-read both files off disk and confirmed the prefix and the arithmetic independently rather than trusting the reported sum. NO NEW `- R-` OR `Done:` LINE WAS ADDED: `R-0784` is referenced by number inside RECORD17's own prose as new evidence rather than as a fresh registration, per §3 item 30 — the reviewer had already searched the open set before authoring the round and found `R-0784` open since F109 R19 describing the identical defect class. THE EVIDENCE JOB WAS RE-RUN BY THE REVIEWER, NOT READ: `run_integrity_checks()` answers `passed=True`, `fail_count=0`, five checks all PASS, reproducing the round's own G5 reading exactly. THE ZIP WAS VERIFIED AGAINST THE ARCHIVED ARTEFACT ITSELF: `sha256sum`-equivalent hashing of `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260903-181544-READY_FOR_REVIEW.zip` on disk reproduces `767304077110354d0005b2f6c70cd53502b831c4161be6a5f6a65a31c136457b` exactly, and `.review_zip_manifest.json` read directly out of that zip shows `base_commit=6f2230cea29af36a75fea253afc10f4dfe5a79f0`, `head_commit=953cade0f62b2687d7dafb5cf1e0b9631849b532` (C2's real SHA), `base_is_ancestor=true`, `commit_count=129`, `ready_gate_matrix.ok=true` and `3785` zip members — every one reproduced by the reviewer from the file on disk, not copied from the handback. THE TREE AND THE SWEEP HELD: `git diff --stat e9e319e2..2fe36572` over `packages/`, `apps/`, `tests/`, `docs/`, `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/candidates.md` and `scripts/self_use_queue.json` is EMPTY, reproduced directly; the branch is pushed at `2fe36572` with no pull request open. THE OUTCOME IS THE CLOSURE PROTOCOL'S ALGORITHM STEPS 1-2 DISCHARGED HONESTLY: `PACKAGE_STATUS=READY_FOR_REVIEW`, `EVIDENCE_AUTHORITATIVE=true`, `REVIEW_SUBJECT_ALIGNMENT=PASS` — nothing green is claimed that was not run, and the two throwaway dry-run artefacts the reviewer built to verify this round's own script BEFORE authoring it (a `-dryrun`-suffixed evidence dir and zip, at the same base) were deleted before the block was emitted, so the bundle directory this round's own G4 names did not pre-exist. NO FINDING IS OWED BY THIS ROUND.
<<<END RECORD18>>>

<<<BEGIN PAIR1_FROM>>>
- `routing.py`: resolve(task_class, context) → {model, tier, reason};
  class table from config seeded by the policy document; per-project
  overrides allowed but hard rules always win.
<<<END PAIR1_FROM>>>

<<<BEGIN PAIR1_TO>>>
- `routing.py`: resolve(task_class, context) → {model, tier, reason};
  class table from config seeded by the policy document; per-project
  overrides allowed but hard rules always win.
  AS BUILT: the module is `packages/orchestration/model_routing.py`, not
  `routing.py`. `resolve_task_class_tier(task_class) -> (tier, reason)`
  returns a tuple, not a `{model, tier, reason}` dict — MODEL selection is
  `role_config.resolve_role_config`'s job, which now also carries
  `RoleConfig.routed_call` (the four `ROUTED_CALL_EVIDENCE_FIELDS`) so a
  caller reads model and routing evidence from the SAME resolved config
  rather than two return values. The class table `TASK_CLASS_TIERS` is
  SEEDED FROM the policy document (parsed and synced by a test), not read
  FROM CONFIG — config only carries the PER-PROJECT OVERRIDE on top of it,
  exactly as this bullet's own next clause already says.
<<<END PAIR1_TO>>>

<<<BEGIN PAIR2_FROM>>>
- Hard rules enforced in code (each a named check with a test):
  reviewer never routed weaker than its paired worker; orchestrator and
  mission-compile calls always top tier; safety-relevant classes
  (fence/DoD evaluation prompts, if any become LLM calls) never below
  mid. Violating overrides fail config validation with the rule named.
<<<END PAIR2_FROM>>>

<<<BEGIN PAIR2_TO>>>
- Hard rules enforced in code (each a named check with a test):
  reviewer never routed weaker than its paired worker; orchestrator and
  mission-compile calls always top tier; safety-relevant classes
  (fence/DoD evaluation prompts, if any become LLM calls) never below
  mid. Violating overrides fail config validation with the rule named.
  AS BUILT (DECISION F110 D5): a violating override WARNS rather than
  failing validation, naming every violated rule, and routes against the
  SHIPPED table instead of the requested one — raising would turn one
  `remedy.toml` typo into an outage across every one of the seven call
  sites `resolve_role_config` now serves. `SAFETY_RELEVANT_CLASSES` ships
  EMPTY in production: the fence and DoD evaluation are deterministic
  Python today, not LLM calls, so that rule is wired and tested but inert
  until one becomes one.
<<<END PAIR2_TO>>>

<<<BEGIN BUILTSTATE>>>
## Built State — what F110 delivered

T001-T003 built model routing by task class end to end: every role Remedy
resolves a runtime configuration for now carries a DECLARED task class, one
resolver seam routes it to a model tier with a reason, and moving a class to
a cheaper tier requires documented benchmark evidence recorded alongside the
override.

- `packages/orchestration/model_routing.py` — `TASK_CLASS_TIERS` (10 classes:
  `format`/`extract`/`summarize`/`boilerplate` -> `cheap`; `standard_build`/
  `standard_review` -> `mid`; `architecture`/`mission`/`vision`/
  `prompt_authoring_for_other_agents` -> `top`), seeded from and synced against
  `docs/agents/model_routing_policy.md`'s "Seed mapping" section by a parser
  test in `tests/orchestration/test_model_routing.py`, so the document and
  the table cannot drift apart silently. `resolve_task_class_tier` returns
  `(tier, reason)`, defaulting an undeclared class to `TOP_TIER` with reason
  `unknown_class_conservative` rather than guessing. The three hard rules of
  the policy document are named checks — `RULE_REVIEWER_WEAKER_THAN_WORKER`,
  `RULE_ORCHESTRATION_BELOW_TOP_TIER`, `RULE_SAFETY_CLASS_BELOW_MID_TIER` —
  each returning its own token rather than a prose sentence, collected in
  order by `validate_routing_choice`. `ORCHESTRATION_TASK_CLASSES` is
  `{orchestrator, mission_compile, mission}` — wider than the feature file's
  two literal call kinds by DECISION F110 D2, so the seed table's own
  `mission -> top` entry is a CHECKED rule an override cannot silently
  demote, not just a table default. `SAFETY_RELEVANT_CLASSES` ships EMPTY by
  design: no fence/DoD evaluation prompt is an LLM call today, so the rule
  has nothing to bind yet and is wired to fire the moment one becomes one.
- Promotion discipline: `PROMOTION_MINIMUM_RUNS_PER_FIXTURE=3`,
  `PROMOTION_MINIMUM_BLOCK_ASSERTION_PASS_RATE=90`,
  `PROMOTION_MINIMUM_OVERALL_PASS_RATE=75` and the seven-field
  `PROMOTION_EVIDENCE_DOCUMENT_FIELDS` are all seeded from and synced against
  the policy document's "Promotion rule" section the same way the tier table
  is. `promotion_evidence_from_mapping` is a pure, fail-closed parser (a
  malformed entry is skipped, never raised past); its one production caller
  is `role_config.resolve_promotion_evidence`, reading config key
  `model_routing.promotion_evidence`. `check_promotion_backed_by_evidence`
  refuses a move to a cheaper tier below the documented bars, naming which
  bar failed; WITH evidence and a real benchmark run, `architecture` —
  seeded at `top` — routes `cheap` with `promoted_by` naming the run
  (measured at `f0bbdc5c`, F110 R13).
- `packages/orchestration/role_config.py` — `RoleConfig.routed_call` (a
  `compare=False` field so the frozen dataclass stays hashable) carries the
  four `ROUTED_CALL_EVIDENCE_FIELDS` (`task_class`, `tier`, `reason`,
  `promoted_by`) for every resolved role, populated by
  `resolve_routed_call_evidence` and wired into `resolve_role_config` itself
  — the ONE shared resolver every inventoried call site already used before
  this feature. Seven call expressions across six files now route through
  it: `teacher_model.py` (x2), `artifact_summary.py`, `self_use_runner.py`,
  `pingpong_job.py`'s `default_role_provider_name` (F110 R2, commit
  `5bbb0cde`, replacing a literal `"fake"` fallback), and
  `apps/cli/commands/do_cmd.py`. `resolve_role_task_class(role,
  originating_task_class=None)` maps a role to its declared class via
  `ROLE_TASK_CLASSES` (builder -> `standard_build`, reviewer ->
  `standard_review`, design_worker -> `architecture`, orchestrator ->
  `mission` — DECISION F110 D3); a role in `TASK_CLASS_INHERITING_ROLES`
  (`repair`) inherits the originating call's class instead, raising
  `OriginatingTaskClassRequired` if none is supplied, rather than guessing
  one.
- `packages/orchestration/config.py` — TABLE-VALUED KEYS: a
  `ConfigKeySpec.entry_type` declares that a key's TOML entries are
  themselves tables, and `_TABLE_VALUED_KEYS` (derived from the registry,
  not hand-listed) tells `_flatten_toml` to stop recursing at such a key
  rather than flattening a routing table into scalar-shaped leaves.
  `model_routing.task_class_tiers` (`entry_type=str`, a class->tier override
  map) and `model_routing.promotion_evidence` (`entry_type=dict`, a table of
  per-class evidence tables) are both registered this way.
- A refused override WARNS rather than raises (DECISION F110 D5): a
  malformed or rule-violating `remedy.toml` entry names every violated rule
  and routes against the SHIPPED table instead, because raising would turn
  one operator typo into an outage across all seven call sites.
- Measured on the fixture chain at commit `f0bbdc5c` (F110 R13): with both
  tables configured, `architecture` routes `cheap` with `promoted_by` naming
  the run and no warning; with tiers alone the same promotion is REFUSED
  with one `promotion_without_evidence` warning and the class stays `top`;
  with evidence alone and no promotion asked, the table is unchanged and
  `promoted_by` is correctly `None`; with nothing configured every answer
  matches the seed table; and a bare string where the evidence table
  belongs is read as "expected table, got str" with no crash.
- SCOPE LIMIT, stated because it is the first thing a reader should know:
  `SAFETY_RELEVANT_CLASSES` is empty in production — the fence and DoD
  evaluation are deterministic Python today, not LLM calls — so hard rule 2
  is wired and tested but inert on every real run until one becomes an LLM
  call.
<<<END BUILTSTATE>>>
──────────────────────────────────────────────────────────────
