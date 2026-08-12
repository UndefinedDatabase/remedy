# Live Review — F107 Context compiler v2

> Reviewer: the main session of a one-session self-drive build
> (docs/agents/self_drive_protocol.md). Worker: one delegated subagent per
> round. Findings are authored here by the reviewer only. A worker marks a
> landed fix `Landed: R-XXXX`; only reviewer-authored `Done:` text sets
> Resolved (docs/agents/planner_reviewer_prompt.md §4.4).
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0295.

## Findings

- R-0221 (Low, carried from F103 through F104 and F105):
  `TestAutoBuildBehavior::test_auto_build_runs_by_default` in
  `tests/ui_server/test_dashboard_contract.py` pops `REMEDY_UI_NO_AUTO_BUILD`
  and runs a real `npm install` + `npm run build` in whatever checkout it runs
  in, refreshing `apps/ui/dist` mtimes mid-suite — costing every integration
  gate phantom base-only failures through `_frontend_is_stale()` (exactly
  seven at the F105 R49 gate, all attributed). Not this feature's code;
  AGENTS.md Scope Control bars the "while I'm here" edit; routed to the F252
  flake-debt class. OPEN.
- R-0239 (Low, carried from F105): a reviewer-authored gate citation named a
  path that does not exist. The worker caught it, ran the real path and
  declared the correction, so nothing was skipped and no number is wrong. It
  stays open as the record of the citation-accuracy lesson, not as
  outstanding work. OPEN.
- R-0247 (Low, carried from F105): a reviewer-authored finding cited a line
  count of 101 where the file was 100. The substance was untouched and the
  finding's own subject was fixed. Same class as R-0239, same reason for
  staying open. OPEN.
- R-0262 (Low, carried from F105): `plan_job_llm` composes its prompt OUTSIDE
  the `try` that turns a provider failure into a renderable result, so a
  raising composer escapes the function. Pre-existing, real, and deliberately
  outside F105's change set — F105 moved composition, it did not own error
  handling. OPEN.
- R-0265 (Medium, carried from F105): a provider that reports usage but no
  cache field leaves a measured-looking `0` the token ledger cannot
  distinguish from a real zero. Documented in
  `docs/system/cache-optimal-prompt-ordering-v1.md` rather than worked
  around; the fix belongs to the actuals producer. OPEN.
- R-0266 (Medium, carried from F105): the token ledger's `role` is a
  hardcoded `builder` in production data, so a per-role split of production
  rows is one bucket. `remedy stats cache` prints that limit in its own
  output instead of burying it. The fix is a producer change. OPEN.
- R-0268 (Low, carried from F105): a `.agent/STOP` file carries no
  provenance — nothing distinguishes an operator stop from any other writer.
  Belongs to the self-drive protocol, not to prompt composition. OPEN.
- R-0270 (Medium, F107 R1, registered from `.agent/candidates.md` per
  STATUS_closure_protocol.md "Closure-candidate findings"): the review zip
  packages the gitignored scratch tree `.remedy-wt/`.
  `scripts/make_review_zip.sh` prunes `.git`, `.data`, caches and root-level
  `remedy-job-evidence-*` directories, but it sweeps the working tree with
  `find` and never consults `.gitignore` — measured at the F105 R50 gate:
  1091 of the 3646 members of
  `remedy-review-20260812-092055-READY_FOR_REVIEW.zip` come from
  `.remedy-wt/`. Three measured consequences. (1) A PRIOR feature's complete
  evidence bundle ships inside the package — 114 members under
  `.remedy-wt/f104_closure_evidence/remedy-job-evidence-f104-closure/` —
  which is exactly what the root-level exclusion exists to prevent; nesting
  one level deeper evades it. (2) The current bundle is packaged twice: 339
  authoritative members under `evidence/current/` plus 334 raw copies under
  `.remedy-wt/f105_closure_evidence/`. (3) 244 packaged scratch members
  contain the literal local path `/home/decodeux` while the manifest reports
  `external_paths_detected: []` — the local-path scanner reads evidence
  fields, not packaged tree members. The package itself stayed valid
  (`package_status` READY_FOR_REVIEW, alignment PASS), which is why this was
  a candidate and not a closure blocker. The fix belongs to
  `scripts/make_review_zip.sh` and docs/agents/self_drive_protocol.md
  together — it is neither F107's code nor F107's scope. OPEN.
- R-0271 (Low, F107 R3): `packages/orchestration/context_compiler.py` imports
  `Iterable` from `typing`, which ruff reports as UP035. The repo's ruff
  baseline already carries 24 other errors, so no gate turns red and nothing
  is blocked — but this one is F107's own new code, it is one line, and the
  module is open for editing in R4 anyway, so it is cheaper to clear than to
  carry. RESOLVED at the R4 gate (2026-08-12) — the `Done:` text closing it is
  the last entry of this file.
- R-0272 (Low, F107 R5): the R5 step block specified tier 2 as
  `build_import_neighbor_graph(...)` yielding "every `files` entry", but
  `ImportNeighbors` has no `files` field — its neighbor tuple is named
  `resolved` (the T001 dataclass in
  `packages/orchestration/context_compiler.py`). The worker implemented
  `resolved`, which is correct, so nothing on disk is wrong and no work is
  outstanding. Registered as the record of the citation-accuracy lesson, the
  same class as R-0239 and R-0247: a reviewer-authored contract must name
  fields that exist. OPEN.
- R-0273 (Medium, F107 R6): a CompiledContext compiled with a NON-DEFAULT
  `line_cap` is RENDERED at the module default, so the budget's numbers stop
  describing the text that would actually be sent.
  `render_compiled_context_text` calls `_signature_render_text(root, path,
  DEFAULT_SIGNATURE_LINE_CAP)` unconditionally, while `compile_task_context`
  estimated every signatures file at the CALLER's `line_cap`
  (`packages/orchestration/context_compiler.py`). Measured by the reviewer on
  a three-file fixture at `line_cap=3`: `compiled.estimated_tokens` reads 25
  while the rendered text estimates at 128 — 5.1x — and `compare_context_size`
  reports `saved_ratio=0.84`, a saving that does not exist. Both the budget
  enforcement and the size comparison therefore rest on a figure that does not
  describe the segment. The cause is the R6 step block, which fixed the
  rendering signature at `(root, compiled)` with no cap; the worker followed
  that contract and DISCLOSED the consequence in its handback instead of
  widening scope, which is exactly the right worker behavior and is why this
  is a finding against the contract, not against the round. No caller passes a
  custom cap today, so nothing on disk is wrong yet — but T004 part 2 is the
  first caller and must not inherit it. Fixed in R7 per DECISION D-F107-2.
  OPEN.
- R-0274 (Low, F107 R7): the R7 step block CONTRADICTED ITSELF about where the
  `Landed: R-0273` line belongs. Its Change line scoped `.agent/live_review.md`
  to "authored pairs LRF3 and LR6 in C3 only", while PROCEDURE step 8 directed
  the worker to write the `Landed:` line and carry it in commit C5. The same
  step also asked for "which commit" INSIDE the very commit that writes the
  line, which no commit can satisfy: a commit cannot contain its own SHA. The
  worker read both, applied the safe reading, named the commit by subject
  instead of by SHA, and DISCLOSED both points in its handback rather than
  guessing silently — the wanted behavior, and the reason neither cost a round.
  Fourth entry in the contract-accuracy class after R-0239, R-0247 and R-0272:
  a reviewer-authored block must not contradict itself and must not order a
  value that cannot exist. OPEN.
- R-0275 (Low, F107 R8-close): the R8 handoff reported commit C2's `+/-` column
  as the file's before/after LINE COUNTS, `218/328`, where
  `git show --numstat 627ca2c9 -- .agent/last_block.md` returns `169	279`; gate
  g then repeated the same 218 in its per-commit insertion list. Nothing rests
  on the error — both readings are far under 500, and a verbatim rewrite of a
  single `.agent/**` state file is cap-exempt outright (AGENTS.md Commit
  Discipline, DECISION F104 D1) — but a `+/-` column is a counted value and the
  counting rule names one measure, the `+` column of the diff. Worker-side
  member of the contract-accuracy class after R-0239, R-0247, R-0272 and
  R-0274: every number in the return channel is the output of the command it
  claims to come from. OPEN.
- R-0276 (Medium, F107 R8-close): this file's own header line 8 reads
  `Next free ID: R-0271` while R-0271, R-0272, R-0273 and R-0274 all exist in
  the Findings section above it — stale since R3 registered R-0271.
  `.agent/plan.md` and `.agent/handoff.md` both carry the correct R-0275, so
  the one carrier that OWNS the sequence is the one that is wrong, and it is
  the carrier a reviewer reads to allocate an ID
  (docs/agents/planner_reviewer_prompt.md §4.4, "IDs continue
  monotonically"). A session that trusted the header would reuse R-0271 and
  silently overwrite a live finding. Fixed in this round: the header now reads
  R-0277, allocated past the two findings this gate registers. OPEN until the
  reviewer confirms the applied value.
- R-0277 (Low, F107 R9): the R9 block's procedure step 1 ordered the saved bytes
  verified "against BLOCK_SHA256 below", but no such line exists inside the
  region that same step orders saved — `grep -n BLOCK_SHA256
  .agent/last_block.md` returns only the two prose references at lines 221 and
  242. The digest lives on line 277 of the reviewer original
  `.remedy-wt/f107-r9-1.block.md`, one line PAST the block body, so the gate was
  meetable only against an artifact the block never names. The worker met it
  there and DECLARED the correction, which is the wanted behaviour. Fixed
  forward: the R10 block states where the digest lives instead of saying
  "below". OPEN until a reviewer confirms the new wording landed.
- R-0278 (Medium, F107 R9): gate c ordered `grep -c 'Next free ID: R-0271'` -> 0
  over `.agent/live_review.md` while slice LRF5TO of the SAME block wrote that
  exact string into that same file, inside R-0276's body, which quotes the stale
  value it reports. The gate was unmeetable by construction; the worker reported
  the real 1 and edited nothing to move it, which is correct under the block's
  own "verify every claim" constraint. Seventh recurrence of the
  self-counting-gate class that docs/agents/planner_reviewer_prompt.md §3
  pre-emission checklist item 2 exists to stop, and the first inside F107. The
  standing fix is the one the R10 block uses: a zero-gate over a string any TO
  slice writes is scoped to the ANCHOR LINE (`^> Branch:.*R-0271`), never to the
  whole file. OPEN.
- R-0279 (Medium, F107 R9): `remedy job context` shipped as user-facing
  behaviour with no entry anywhere under `docs/` — no guide, no row in the
  `docs/README.md` index — because the R9 block's Change list was nine paths
  "and nothing else", none under docs/. AGENTS.md Documentation Updates orders
  docs when a feature introduces new behaviour, so the omission is the
  REVIEWER's: the worker flagged the absence in its handoff instead of widening
  scope, which is exactly right. R10 C6 fixes it. OPEN.
- R-0280 (Medium, F107 R10): the R10 block contradicted itself about which
  commit carries the two `docs/README.md` pairs — its Bundle line and Change
  list put that file in C6, while PROCEDURE step 3 and gate c put all six pairs
  in C3. Applied as step 3 read it, C3 would have added an index row pointing at
  a guide that only C6 creates, and
  `tests/docs/test_docs_consistency.py:276` (`TestPrimaryDocLinksResolve`)
  asserts every relative link in `docs/README.md` resolves — so C3, C4 and C5
  would each have been committed on a RED docs suite. The worker took the safe
  reading, put the rows in C6, and declared both readings. Same class as
  R-0274: a block that says two different things costs the round a deviation to
  prove the reviewer wrong. OPEN.
- R-0281 (Low, F107 R10): `tests/orchestration/test_context_compiler.py:801`
  still calls `write_omitted_context_json` "The one writing function", which
  stopped being true when C4 added `write_context_size_comparison_json`. C4
  corrected the same stale absolute claim in two module docstrings; the test's
  copy survived because C5's own constraint was append-only, so the worker
  flagged it instead of editing outside its instruction. The stale-claim class
  is worth one line: the next reader trusts it. Fixed in this round's C6. OPEN.
- R-0282 (Low, F107 R11): the R11 block's Change line said "exactly these nine
  paths" and gate l repeated "nine", while the list under it enumerates EIGHT.
  The worker measured 8, touched nothing outside the list, and declared the
  discrepancy. Reviewer arithmetic, costing a deviation on a round that did
  nothing wrong — the same tax R-0274, R-0277 and R-0280 record. OPEN.
- R-0283 (Medium, F107 R11): `test_compiled_run_shrinks_the_context_and_still`
  `_solves_the_task` — the test that stands for the FEATURE'S DONE CONDITION —
  passes with the entire compiled path disabled. The reviewer measured it rather
  than reading the disclosure: setting `use_compiled_context = False` in a
  disposable worktree at 04154822 turns the e2e module to `3 failed, 3 passed`
  and that test is among the THREE THAT STILL PASS. The cause is that the
  baseline run passes `mentioned_files` while the fall-through compiled run
  passes none, so its context is smaller for a reason that has nothing to do
  with F107. A shrink assertion that a bypass satisfies pins nothing. The worker
  found this itself, reported it, and deliberately did NOT repair it after
  measuring, which would have made its own probe self-fulfilling — that is
  exactly right, and it is why this is a finding against the round's test
  strength and not against its honesty. Fixed in R12 C4 by pinning the compiled
  run's `context_chars` to the length of `render_compiled_context_text` over the
  same fixture, which no fall-through can satisfy. OPEN.
- R-0284 (Low, F107 R11): two line citations in the R11 block were wrong —
  `build_scope_contract_for_builder` sits at pingpong_loop.py:2741, not :2694,
  and the stale "one writing function" string sat at
  test_context_compiler.py:805, not :801. Both were declared, neither cost
  anything but the declaring, and both are the reviewer-citation class the
  block's own constraint tells workers to expect. OPEN.
- R-0285 (Low, F107 R12): the R12 block's gate c ordered `grep -c '^Landed:'` ->
  0 over `.agent/live_review.md` in the one round whose C4 LANDED a fix for
  R-0283, and its Change line confined that file to the four authored pairs.
  docs/agents/planner_reviewer_prompt.md §4.4 tells a worker to mark exactly
  that case `Landed: R-XXXX` in this file, so the block's own zero-gate made the
  protocol's marker unwritable. The worker obeyed the gate, put the landed note
  in the handoff header instead, and declared the conflict as its deviation 4 —
  the right call, and the fifth reviewer-block defect this feature has taxed a
  worker with (R-0274, R-0277, R-0280, R-0282). The rule the next block follows:
  a zero-gate over `^Landed:` is safe only in a round that lands no fix. OPEN.

- R-0286 (Medium, F107 R13 integration gate): the full suite is RED at the merge
  base 2e4142c3 and on this branch with the SAME five ids — every `[reviewer]`
  parametrization in `tests/orchestration/test_role_conventions.py` — because
  `docs/agents/reviewer_conventions.md` estimates 954 tokens against the 800-token
  cap `packages/orchestration/role_conventions.py` declares, so composing the
  segment raises `PromptSegmentError` before any assertion in those tests runs.
  It is pre-existing and not F107's: the document last changed at merge a85e82f5
  ("keep both sections", +17 lines), an ancestor of the merge base, and
  `git diff 2e4142c3..HEAD` touches neither that document nor
  `role_conventions.py` nor `prompt_segments.py`. F107 does not repair it —
  AGENTS.md Core Workflow bars mixing an unrelated fix into a feature branch —
  and the gate verdict is unaffected, because ids failing in BOTH runs are
  common failures and appear in neither comm file. The severity is Medium and
  not High deliberately: a High finding sets `high_blockers_open`, which blocks
  `remedy integrity check`, the review zip and therefore this feature's closure,
  charging F107 for a defect that landed on `main` before the branch was cut.
  The reviewer prompt-segment path stays broken in production until a follow-up
  trims the document under its cap or raises the cap on purpose. OPEN.
- R-0287 (Low, F107 R13 integration gate): `docs/agents/planner_reviewer_prompt.md`
  §4.4 routes every severity decision to "the canonical scale in
  review_protocol.md", but no `docs/agents/review_protocol.md` exists on disk.
  The repository's severity scale therefore has no carrier, and every Low,
  Medium and High in this file was assigned from precedent rather than from a
  written rule. Same citation-accuracy class as R-0239 and R-0247, one level up:
  the dangling pointer sits in a governing document instead of in a round's
  block. Recorded, not repaired here — editing an agent-governance document is
  outside this feature's change set. OPEN.
- R-0288 (Medium, F107 R15 integration gate): the R15 gate ran BOTH suites to
  completion in `.remedy-wt/gate-scratch/f107-r15/` and then lost its session
  before the evidence reached the repository. Its scalar outputs survived —
  exit codes, wall clocks, UTC stamps, the two full logs and the three comm
  lists — because the run drivers redirected them into files. The three parity
  steps did not survive: `mtimes.sh`, `touch_dist.sh` and `dist_hash.sh`
  printed to stdout only. Their output was the SOLE proof that the base
  worktree's `apps/ui/dist` was byte-identical to the primary checkout's and
  mtime-newer than its own sources, so `base_worktree.txt` and
  `dist_hashes.txt` became unrecoverable the moment the session died and the
  worktree was removed. A base run whose parity cannot be shown is not a
  comparison, and an empty `comm -23` proves parity only if you already trust
  the run that produced it. Rule, forward-looking: every gate step that
  produces evidence redirects it to its scratch file AS IT RUNS — a step whose
  only record is a terminal is a step that did not happen. R16 re-runs the
  whole gate from a rebuilt base worktree rather than transcribe a
  half-provable one. OPEN.
- R-0289 (Medium, F107 R16): the R16 block ordered its ONLY push at C6, the
  last commit of the round. The session died after C4, so twelve commits — the
  entire committed output of R13, R14, R15 and R16, the complete
  integration-gate evidence included — sat on local disk alone, invisible to
  the operator and one disk failure from gone. AGENTS.md Push Discipline reads
  "After committing: git push -u origin <branch>", not "after the last commit
  of the round". Four consecutive sessions have now died mid-round, which makes
  the tail of a round the least likely part to run and therefore the worst
  possible home for the only durability step a round has. The R16 block was
  otherwise careful — it redirected every gate value to a file precisely
  because a session might die — and then staked the survival of all of it on
  reaching its own last step. Rule, forward-looking: a round pushes after EVERY
  commit; a block that names a single push at its last step is authoring the
  loss it will later have to report. OPEN.
- R-0290 (Medium, F107 R18, reviewer-side protocol defect, found by this
  session against itself): docs/agents/self_drive_protocol.md Phase 0 lists six
  probe commands — `git status --porcelain`, `git branch --show-current`,
  `git log --oneline -n 8`, `gh pr list`, `remedy plan status` and `remedy plan
  next` — and NOT ONE of them can see a feature branch that is not checked out.
  This session ran the probe exactly as written while standing on `main` after
  merging PR #192, read the F105-era `.agent/` state that `main` carries,
  selected F107 by Rule A5 because `main`'s STATUS.md says `- [ ] F107`, and
  authored a complete R1 claim block for a feature that was already 102 commits
  deep on this branch — integration gate green at R16, seventeen findings
  registered, its own `.agent/candidates.md` emptied by its own R1. The
  delegated worker refused to write anything and reported the collision with
  `git for-each-ref` evidence, so the round cost zero commits. The
  single-writer rule is the only reason this is a near-miss rather than a
  rewind: the authored payloads replaced `.agent/live_review.md` WHOLESALE at
  "Next free ID: R-0271" while the file on disk stood at R-0290. Two
  compounding causes, both worth naming. (1) `.agent/` read on `main` is
  LAST-MERGE state, never latest-worker state, whenever a feature's work sits
  on an unmerged branch — the file the protocol calls "the only return channel"
  is invisible from the branch the probe stands on. (2) The closure protocol
  defers each feature's PR to the NEXT feature's start, so a
  completed-but-unclosed feature has BY DESIGN no open PR, and `gh pr list` —
  the one probe command that could have surfaced it — returns empty exactly
  when the risk is highest. Fix, forward-looking: Phase 0 gains `git branch -a
  --list 'feature/*'` plus `git log --oneline -1` and `git show
  <branch>:.agent/handoff.md | head -20` for every feature branch ahead of
  `main`, and Phase 1 gains a rule that such a branch whose own STATUS line
  reads `[~]` is a PENDING FEATURE that outranks Rule A5 selection. Registered
  NOT fixed here: editing the self-drive protocol is outside F107's change set,
  the same boundary R-0287 respects. OPEN.
- R-0291 (Medium, F107 R18): two bullets of the feature file's Design are UNMET
  on disk and no DECISION records the deviation, so the roadmap promises
  behaviour the code deliberately does not have. (a)
  `docs/roadmap/features/T2_F107.md` Design says "The compiled context becomes
  a registry segment with its manifest hash in evidence".
  `register_compiled_context_segment`
  (`packages/orchestration/context_compiler.py:984`) exists and is unit-tested,
  but `grep -rn 'register_compiled_context_segment' --include=*.py` returns only
  its definition, its docstring line and five lines of
  `tests/orchestration/test_context_compiler.py` — no production caller. The one
  production path that compiles a context during a run,
  `packages/orchestration/pingpong_loop.py:2682-2683`, calls
  `render_compiled_context_text` and sets `categories =
  [COMPILED_CONTEXT_SEGMENT_NAME]`: a context string and a label, not a
  `PromptSegment`, with no registry, no rank and no manifest. The module says so
  itself at `context_compiler.py:66-68` — "The segment manifest is not written
  into evidence here… wiring the manifest and the size comparison into run
  evidence is a later round" — so the deferral is honest in the code and
  invisible everywhere an operator would look. (b) The same Design section
  defines tier 1 as the files_hint AND the fence allow scope, while the only
  tier-1 producer, `apps/cli/commands/job_context_cmd.py:242`, passes
  `_task_files_hint(task)` alone, documented at that file's lines 8-13 and in
  the user guide. Neither gap is a defect of the code that exists — both are
  deliberate, both are documented at the source, and neither touches the
  feature's DONE sentence, which is about selection, shrink and the omissions
  record. What is missing is the operator-visible record that
  planner_reviewer_prompt.md §4.7 requires for a spec deviation. DECISION F107
  D1 lands in this round and states both deferrals; the reviewer resolves this
  finding at the R18 gate, once that text is verified on disk. OPEN.
- R-0292 (Medium, F107 R18, F107's own code against F107's own spec): an
  unparseable file that is NOT tier 1 is included with an EMPTY signature
  rendering and no omissions record, so the record does not explain why the
  model saw nothing for it. The feature file's Edge-cases section rules
  "Unparseable files: included-whole if tier 1 (better safe), signature-skipped
  WITH REASON otherwise". On disk the tier-3 loop
  (`packages/orchestration/context_compiler.py:820-831`) reads the file, calls
  `_signature_render_text` and appends the result to `chosen` without ever
  consulting `FileSignatures.parse_failed`; `_signature_render_text` (`:701-704`)
  returns `"\n".join(...lines)`, which is `""` when parsing failed, so the file
  lands in `included` claiming a `"signatures"` rendering with a near-zero token
  estimate while contributing no content at all. The same blind spot sits in the
  tier-2 over-cap path (`:807-818`): it records `"size"` / `"signatures"` but not
  that the signatures came back empty. `parse_failed` is computed by the
  extractor and then discarded by the selector. No test covers an unparseable
  non-tier-1 file — the selector suite at
  `tests/orchestration/test_context_compiler.py:574-842` never creates one.
  Fixed in THIS round rather than deferred: this is F107's own module
  contradicting F107's own Edge-cases clause, so AGENTS.md Scope Control does
  not bar the repair.
- R-0293 (Medium, F107 R19, found at the R18 gate by probing the code the R18
  block did not name): the unparseable blind spot R-0292 recorded lives in
  THREE selector paths, and R18 closed two. The budget path — phase A of
  `compile_task_context`, `packages/orchestration/context_compiler.py:866-880`
  — demotes the largest FULL tier-2 file to signatures, calls
  `_signature_render_text`, and appends only an `OMISSION_REASON_BUDGET` /
  `_OUTCOME_SIGNATURES` record. When that file cannot be parsed, its signature
  rendering is `""` exactly as in R-0292, and the record blames the budget for
  a blank the budget did not cause: the file would have rendered empty under an
  infinite budget too. Reachable, and probed rather than argued — a root with
  `app.py` (tier 1, padded) importing `broken.py` (tier 2, small, `def broken(:`)
  compiled at a budget one token under the unconstrained total puts
  `('broken.py', 2, 'signatures', 0)` in `included` with exactly one record,
  `('broken.py', 2, 'budget', 'signatures')`, and no `unparseable` record. The
  same reviewer-side omission produced this gap and R-0292's repair scope: the
  R18 block named the tier-2 over-cap path and the tier-3 path from a reading
  of the module, without enumerating every call site that renders signatures.
  Fixed in THIS round, on the same ground R-0292 was: F107's own module against
  F107's own Edge-cases clause.
- R-0294 (Low, F107 R19, reviewer-side process defect): the R18 block was
  emitted without the §3 pre-emission checklist being run on its final bytes,
  and two of the seven items caught it after the fact rather than before.
  Item 1, size: the block is 407 lines against the cap of 400 (DECISION F105
  D5), so the worker had to apply an oversize block byte for byte and declare
  gate B RED on a round that did nothing wrong. Item 2, no self-counting gate:
  gate C ordered `Next free ID: R-0290` to be 0x in `.agent/live_review.md`
  while the block's own PAIR_LRG_TO writes that string into that same file at
  line 905, quoting the R17 gate's own marker as evidence — unmeetable by
  construction, and the sixth recurrence of that item's class across F104,
  F105 and F107. Neither cost a repair round, because the worker reported both
  RED honestly instead of massaging a number; that honesty is what kept a
  process defect from becoming a data defect. Registered against the reviewer
  role, not the worker. Forward-looking fix, already applied to THIS block:
  count the lines and re-read every zero-gate against every TO in the same
  block before emission, mechanically, on the final bytes.

## Steps

R1 claim, candidate sweep and state reset → R2 T001 import-neighbor graphs
(Python via ast, TS/JS via the documented line scanner) → T002 signature
extractors + size caps + goldens → T003 tiered selector + budget demotion +
omissions writer → T004 segment integration + `remedy job context` CLI view +
end-to-end fixture task → integration gate → closure per
docs/roadmap/STATUS_closure_protocol.md.

- Reviewer gate on R1 (2026-08-12): PASS. Range 2e4142c3..d2b962af = eight
  commits touching exactly the eight paths the R1 block named — no production
  code, no test module, no docs beyond the one STATUS.md line. Transport by
  the primary shape: `cmp` of every applied state file against the reviewer's
  surviving `.remedy-wt/` originals silent; the block original, the committed
  `.agent/authored/f107-r1-1.md` and `.agent/last_block.md` byte-identical at
  274 lines. The claim commit's numstat for STATUS.md reads `1 1`, the TO line
  counts 1x and the FROM 0x after the edit. Every scoped gate was RE-RUN by
  the reviewer instead of read from the handback: `python3 -m pytest
  tests/docs/ -q` returns 294 passed, the canary
  `python3 -m pytest tests/cli/test_golden_path.py -q` returns 42 passed,
  `grep -c '^## Steps'` is 1 and `grep -c '^<<<'` is 0 across the five state
  files, `.agent/plan.md` is 29 lines, `git status --porcelain` is empty,
  `git worktree list` shows the primary checkout alone, and HEAD equals
  `origin/feature/f107-context-compiler-v2`. Insertions per commit 274, 265,
  1, 62, 2, 22, 30, 53 — each under 500. R-0270 is registered and
  `.agent/candidates.md` is empty, so the feature-claim block condition is
  discharged. `LAST_REVIEWED_SHA` advances 2e4142c3 -> d2b962af.

- Reviewer gate on R2 (2026-08-12): PASS, partial round — `.agent/STOP`
  truncated it after the module commit and the worker declared the truncation
  (guardrail G6, docs/agents/self_drive_protocol.md). Range d2b962af..5a9951d5
  is six commits touching six of the seven paths the R2 block named; the
  seventh, tests/orchestration/test_context_compiler.py, is the declared skip.
  Transport by the primary shape: `cmp` of the surviving reviewer original
  `.remedy-wt/f107-r2-1.block.md` against the committed
  `.agent/authored/f107-r2-1.md` is silent, and so is the authored copy
  against `.agent/last_block.md` — all three 182 lines. Both slice bodies
  recompute to their BEGIN-marker digests, the PLAN body is byte-equal to
  `.agent/plan.md`, and the LRAPP body is the verbatim tail of this file. That
  pair was APPEND-shaped and `git show --numstat 72d79079` reads `19 0`: zero
  deletions, which proves the FROM line was never edited. Every scoped gate
  was RE-RUN by the reviewer instead of read from the handback — the canary
  `python3 -m pytest tests/cli/test_golden_path.py -q` returns 42 passed,
  `grep -c` for the Steps heading is 1, `.agent/plan.md` is 28 lines,
  `git status --porcelain` is empty, `git worktree list` shows the primary
  checkout alone, and HEAD equals `origin/feature/f107-context-compiler-v2`.
  Insertions per commit 182, 155, 19, 10, 302, 49 — each under 500. Gate d
  could not run at all, because the round's own test module is the missing
  seventh path: `packages/orchestration/context_compiler.py` is REVIEWED AND
  PROBED BUT NOT GATED. The reviewer probe, on a throwaway fixture tree under
  `.remedy-wt/`, reproduced every case the T001 contract names — absolute
  import, from-module against from-symbol, single- and double-dot relative,
  two-file cycle terminating, stdlib to external, SyntaxError and missing file
  to parse_failed, no self-listing, './x' beating an x/index.ts sibling,
  './dir' to dir/index.ts, export-from, require(), .tsx and .jsx, 'react'
  external, an escaping specifier external, and a graph that is sorted,
  deduplicated, twice-equal and parse_failed on an unknown suffix — but a
  reviewer probe is not committed evidence and this file does not treat it as
  any. R3 commits that test module and R3's gate d is what certifies the
  module; until it is green, no verdict here claims T001 is test-covered.
  Recorded as an observation and not a finding: the R2 handoff is 62 lines
  where the R2 block asked for 60, which AGENTS.md permits outright for a
  per-commit table of more than five commits, and this one has six.
  `LAST_REVIEWED_SHA` advances d2b962af -> 5a9951d5.

- Reviewer gate on R3 (2026-08-12): PASS. Range 5a9951d5..ef64cf72 = six
  commits touching exactly the six paths the R3 block named. Transport by the
  primary shape: `cmp` of the reviewer original `.remedy-wt/f107-r3-1.block.md`
  against the committed `.agent/authored/f107-r3-1.md` silent, and the authored
  copy against `.agent/last_block.md` silent, all 232 lines; both slice bodies
  recompute to their BEGIN-marker digests, PLAN2 is byte-equal to
  `.agent/plan.md` and LR2 is the verbatim tail of this file. The LR2 pair was
  APPEND-shaped and `git show --numstat 0dbdaa83` reads `37 0` — zero
  deletions. No worker-authored `Done:` line exists in this file. Gates were
  RE-RUN by the reviewer rather than read from the handback: the T001 gate
  `python3 -m pytest tests/orchestration/test_context_compiler.py -q` returns
  16 passed, the canary returns 42 passed, `.agent/plan.md` is 29 lines, the
  Steps heading count is 1, `git status --porcelain` is empty and
  `git worktree list` shows the primary checkout alone. Insertions per commit
  232, 189, 37, 7, 274, 63 — each under 500. The 16 test functions carry all
  26 numbered obligations of the R3 contract, each as an equality assertion on
  real values rather than a truthiness check, and the deliberate external
  renderings ('os', 'typing.Iterable', '...x', '../../escape', 'react') are
  pinned verbatim. The reviewer ran TWO independent mutation probes in a
  disposable worktree at ef64cf72, one of them deliberately different from the
  worker's: removing the self-discard line reddens exactly
  `test_python_file_importing_its_own_module_name_does_not_list_itself`, and
  swapping the TS candidate order reproduces the worker's reported failure
  `AssertionError: assert ('x/index.ts',) == ('x.ts',)` in
  `test_typescript_suffix_candidate_beats_index_file_candidate` — so the
  handback's probe evidence is confirmed true and the goldens bite. That
  worktree was removed and pruned before this verdict. The 75-line handoff is
  a declared stated-cause overage carrying its mandated tables, which
  AGENTS.md permits for a per-commit table of more than five commits. T001 is
  now test-covered on the branch and the R2 ungated-module caveat is
  discharged. `LAST_REVIEWED_SHA` advances 5a9951d5 -> ef64cf72.
- Reviewer gate on R4 (2026-08-12): PASS. Range ef64cf72..2c75bddf = eight
  commits touching exactly the seven paths the R4 block named. Transport by the
  PRIMARY shape, the reviewer original having survived the session boundary:
  `sha256sum` of `.remedy-wt/f107-r4-1.block.md`, of the committed
  `.agent/authored/f107-r4-1.md` and of `.agent/last_block.md` returns
  7cf9a5f065db… for all three. This session's permission layer denies `cmp`,
  so byte identity was proven by digest instead — strictly stronger than the
  ordered check, never weaker. All three slice bodies recompute to their
  BEGIN-marker digests at their declared lengths (LRF fac600cb… 7 lines, LR3
  1dc20c0b… 33 lines, PLAN3 4b98f108… 29 lines), and `sha256sum
  .agent/plan.md` returns that same PLAN3 digest: the plan on disk IS the
  authored slice, not a retype of it. The C3 pair was ANCHOR-PRESERVING and
  `git show --numstat 657b98fb -- .agent/live_review.md` reads `38  0` — zero
  deletions; both FROM lines occur exactly 1x in the file and 0x among the 38
  added lines, and every TO-only line of both slices occurs exactly 1x among
  those added lines, with no strays. Every scoped gate was RE-RUN by the
  reviewer rather than read from the handback: `python3 -m pytest
  tests/orchestration/test_context_compiler.py -q` returns 29 passed (the 16
  frozen T001 tests plus 13 new), the canary `python3 -m pytest
  tests/cli/test_golden_path.py -q` returns 42 passed, `python3 -m ruff check`
  over the module and its test file returns "All checks passed!" — which is
  what closes R-0271 — `.agent/plan.md` is 29 lines, the Steps heading count
  is 1, `grep -c '^<<<'` is 0 across all three state files, `git status
  --porcelain` is empty, HEAD equals `origin/feature/f107-context-compiler-v2`
  and `git worktree list` shows the primary checkout alone. Insertions per
  commit 326, 280, 38, 2, 11, 242, 271, 80 — each under 500. The 13 test
  functions carry all 13 numbered obligations of the R4 contract as exact
  tuple equalities rather than truthiness checks, and the goldens are
  mechanically captured rather than hand-written — `limit: int=10` is
  `ast.unparse` spacing, which no human would type on purpose. The reviewer
  ran THREE mutation probes in a disposable worktree at 2c75bddf, two of them
  deliberately different from the worker's: turning the size cap's `<=` into
  `<` reddens exactly `test_fits_inline_size_cap_is_inclusive_at_the_cap_and`
  `_false_when_absent` with `AssertionError: assert False is True`, and
  deleting the nested-declaration recursion line reddens exactly the Python
  whole-file golden and
  `test_python_file_without_any_docstring_renders_headers_only`. The worker's
  own probe reproduces verbatim — `1 failed, 28 passed`, failing
  `test_typescript_signature_golden_renders_exported_lines_only` on
  `'export function renderWidget(id: string): void {' !=` the same line
  without its brace — so the handback's probe evidence is confirmed TRUE
  rather than taken on trust. That worktree was removed and pruned before this
  verdict and `git worktree list` shows the primary alone. The 96-line handoff
  is a declared stated-cause overage carrying its mandated tables, which
  AGENTS.md DECISION D15 permits; both declared deviations are accurate and
  neither weakens a proof. No new findings this round.
  `LAST_REVIEWED_SHA` advances ef64cf72 -> 2c75bddf.
- Reviewer gate on R5 (2026-08-12): PASS. Range 2c75bddf..54bc56c2 = seven
  commits touching exactly the seven paths the R5 block named. The round spanned
  TWO worker sessions: a prior worker committed C1-C6 and ended before PROCEDURE
  step 7, and this session's worker ran the mutation probe, re-verified the disk
  state and committed C7 alone. The single-writer rule held throughout — the
  reviewer wrote nothing, and no existing commit was amended, rebased, reverted
  or reordered. Transport by the PRIMARY shape: `cmp` of
  `.remedy-wt/f107-r5-1.block.md` against `.agent/authored/f107-r5-1.md`, and of
  that copy against `.agent/last_block.md`, is silent, and all three sha256 to
  220d64ec8aa4… at 393 lines each. All five slice bodies recompute to their
  BEGIN-marker digests at their declared lengths (FIX1FROM 06f8ce67… 1 line,
  FIX1TO 547f5a52… 2, LR4FROM 3541d8ff… 1, LR4TO b07a255e… 53, PLAN4 320c4890…
  28), and `cmp .agent/plan.md` against the extracted PLAN4 body is silent: the
  plan on disk IS the authored slice, not a retype of it. Both C3 pairs were
  REWRITES and `git show --numstat 4860115e -- .agent/live_review.md` reads
  `55  2` — both FROM strings now occur 0x, each of the 2 FIX1TO and 53 LR4TO
  lines occurs exactly 1x among the 55 added lines, and 0 added lines belong to
  neither body. Every scoped gate was RE-RUN by the reviewer rather than read
  from the handback: `python3 -m pytest
  tests/orchestration/test_context_compiler.py -q` returns 42 passed (the 29
  frozen T001+T002 tests plus 13 new T003 tests), the canary `python3 -m pytest
  tests/cli/test_golden_path.py -q` returns 42 passed, `python3 -m ruff check`
  over the module and its test file returns "All checks passed!",
  `.agent/plan.md` is 28 lines, the Steps heading count is 1, the stray-marker
  count is 0 across the three state files, `git status --porcelain` is empty,
  HEAD equals `origin/feature/f107-context-compiler-v2`, and `git worktree list`
  shows the primary checkout alone. Insertions per commit 393, 322, 55, 11, 351,
  284, 76 — each under 500. The 13 new test functions carry all 13 numbered
  obligations of the R5 contract as exact equality assertions on real values,
  and every token figure is asserted against a direct `estimate_text_tokens`
  call rather than against a hand-copied number. The reviewer ran THREE mutation
  probes in a disposable worktree at 54bc56c2, two of them deliberately
  different from the worker's: pointing budget phase B at TIER_NEIGHBOR instead
  of TIER_DISTANT reddens exactly
  `test_budget_omits_tier_three_before_it_omits_tier_two` and
  `test_tier_one_is_never_cut_by_the_budget_and_the_overflow_is_reported`, while
  suppressing the tier-4 distance records reddens exactly the tier-assignment
  test, the export-keys test and the completeness test. The worker's own probe
  reproduces verbatim — `1 failed, 41 passed`, failing
  `test_budget_demotes_the_largest_tier_two_file_first` on `At index 1 diff:`
  the big neighbor rendering `full` where the test requires `signatures` — so
  the handback's probe evidence is confirmed TRUE rather than taken on trust.
  That worktree was removed and pruned before this verdict. The 95-line handoff
  is a declared stated-cause overage carrying its mandated tables, which
  AGENTS.md DECISION D15 permits. One new finding, R-0272, is registered above.
  Recorded as an observation and NOT as a finding: `context_compiler.py` still
  has no caller outside its own test module, because T003 is a library layer by
  design and T004 is the round that wires it — a green gate here is not yet a
  working feature, and no verdict in this file claims otherwise.
  `LAST_REVIEWED_SHA` advances 2c75bddf -> 54bc56c2.
- Reviewer gate on R6 (2026-08-12): PASS, with one new finding. Range
  54bc56c2..861eb371 = seven commits touching exactly the seven paths the R6
  block named. Transport by the PRIMARY shape: `cmp` of
  `.remedy-wt/f107-r6-1.block.md` against `.agent/authored/f107-r6-1.md`, and
  of that copy against `.agent/last_block.md`, is silent, and all three sha256
  to c263869d4444… at 364 lines each. All five slice bodies recompute to their
  BEGIN-marker digests at their declared lengths (LRF2FROM 2bb66673… 1 line,
  LRF2TO 830262c1… 10, LR5FROM b96097af… 1, LR5TO 98b340c5… 51, PLAN5
  27f9c8ef… 28), and `sha256sum .agent/plan.md` returns that same PLAN5
  digest. Both C3 pairs were APPEND-shaped and were proven as such rather than
  as rewrites: `git show --numstat 2afec22b -- .agent/live_review.md` reads
  `59  0` — ZERO deletions, which is what proves neither anchor line was
  edited — each FROM still occurs exactly 1x in the file, each of the 9 LRF2TO
  and 50 LR5TO TO-only lines occurs exactly 1x among the 59 added lines, and 0
  added lines belong to neither body. Every scoped gate was RE-RUN by the
  reviewer rather than read from the handback: `python3 -m pytest
  tests/orchestration/test_context_compiler.py -q` returns 52 passed (the 42
  frozen tests plus 10 new), `tests/orchestration/test_prompt_segments.py`
  returns 25 passed — that module's suite was gated because this round imports
  from it for the first time — the canary `tests/cli/test_golden_path.py`
  returns 42 passed, `python3 -m ruff check` over the module and its test file
  returns "All checks passed!", `.agent/plan.md` is 28 lines, the Steps
  heading count is 1, `grep -c '^- R-0272'` is 1, the stray-marker count is 0
  across the three state files, `git status --porcelain` is empty, HEAD equals
  `origin/feature/f107-context-compiler-v2` and `git worktree list` shows the
  primary checkout alone. Insertions per commit 364, 285, 59, 10, 162, 190, 75
  — each under 500. The reviewer ran FOUR mutation probes in a disposable
  worktree at 861eb371, three of them deliberately different from the
  worker's: collapsing the block separator from a blank line to a single
  newline and dropping the tier number from the header line each redden
  exactly `test_render_compiled_context_text_builds_one_block_per_included`
  `_file`, and making the zero-baseline ratio guard return a fabricated 1.0
  reddens exactly `test_compare_context_size_reports_no_ratio_for_a_zero`
  `_baseline`. The worker's own probe reproduces verbatim — moving the
  registered rank from JOB_CONTEXT to TASK gives `2 failed, 50 passed`,
  reddening the segment-rank test and the manifest-row test — so the
  handback's probe evidence is confirmed TRUE rather than taken on trust. That
  worktree was removed and pruned before this verdict. All three declared
  deviations are accurate: the 100-line handoff sits exactly at the AGENTS.md
  D15 ceiling with its stated cause, the greedy `rstrip` is the reading that
  actually delivers the stated invariant, and the two docstring header updates
  are inside files the change set already names. What the round did NOT do is
  the finding: the worker's third disclosure — that a custom `line_cap` is
  rendered at the module default — is real, is larger than the note implied,
  and was MEASURED by the reviewer rather than accepted as written. It is
  registered above as R-0273 and R7 fixes it. Recorded as an observation and
  not a finding: `context_compiler.py` still has no caller outside its own
  test module, so F107 remains a library that is not yet wired to anything a
  user can run. `LAST_REVIEWED_SHA` advances 54bc56c2 -> 861eb371.
- Reviewer gate on R7 (2026-08-12): PASS. Range 861eb371..6acb3f04 = eight
  commits touching exactly the seven paths the R7 block named. Transport by the
  PRIMARY shape: `cmp` of `.remedy-wt/f107-r7-1.block.md` against
  `.agent/authored/f107-r7-1.md` and against `.agent/last_block.md` is silent,
  all three at 328 lines, and all five slice bodies recompute to their
  BEGIN-marker digests at their declared lengths (LRF3FROM 4ad9497d… 1 line,
  LRF3TO e3fdd106… 20, LR6FROM d85c84ac… 1, LR6TO dac43442… 50, PLAN6
  047fcc7a… 28); `sha256sum .agent/plan.md` returns that same PLAN6 digest.
  Both C3 pairs were APPEND-shaped and proven as such: `git show --numstat
  4909b1b1 -- .agent/live_review.md` reads `68  0` — ZERO deletions — each FROM
  still occurs exactly 1x, each of the 19 LRF3TO and 49 LR6TO TO-only lines
  occurs exactly 1x among the 68 added lines, and 0 added lines belong to
  neither body. Every scoped gate was RE-RUN by the reviewer: the module suite
  returns 55 passed (the 52 frozen tests plus 3 new), the canary returns 42
  passed, `python3 -m ruff check` returns "All checks passed!", `.agent/plan.md`
  is 28 lines, the Steps heading count is 1, `grep -c '^- R-0273'` is 1, the
  stray-marker count is 0 across the three state files, `git status
  --porcelain` is empty, HEAD equals `origin/feature/f107-context-compiler-v2`
  and `git worktree list` shows the primary checkout alone. Insertions per
  commit 328, 255, 68, 9, 16, 113, 75, 18 — each under 500. THE FIX WAS
  MEASURED, not read: the reviewer re-ran the same three-file fixture at
  `line_cap=3` that produced the R-0273 numbers, and the rendered text's
  estimate falls from 128 tokens to 46 against an `estimated_tokens` of 25 —
  the 5.1x divergence is gone. The residual 21-token gap is the block HEADER
  lines the renderer adds, it is the same ~20 tokens at the default cap, and it
  is therefore uniform overhead rather than cap drift; it is recorded here as
  an observation for R8's evidence work, NOT as a finding, because
  `estimated_tokens` is documented as a sum over file contents and the headers
  are one bounded line per included file. The reviewer ran TWO probes in a
  disposable worktree at 6acb3f04 and both reproduce the worker's numbers
  verbatim: putting the renderer back on the module default gives `1 failed, 54
  passed` on `test_signature_blocks_render_at_the_cap_the_context_was_compiled`
  `_at`, and storing the default in the constructor instead of the caller's cap
  gives `3 failed, 52 passed` — so the regression test genuinely bites and the
  handback's evidence is confirmed TRUE rather than taken on trust. That
  worktree was removed and pruned before this verdict. Both declared deviations
  are accepted. The 114-line handoff exceeds even the D15 100-line ceiling, and
  the cause is mandated content this reviewer ORDERED — gate i was required to
  carry both step-7 transcripts with failing test names and assertion texts —
  so it is a stated-cause overage and not verbosity; no section was dropped.
  The eighth commit is the right call and not a scope breach: it corrects a
  stale grep line number in the handoff, touches only a path the Change line
  already names, and was made in its own commit because amending C7 is
  forbidden — leaving a false counted value in the return channel would have
  been the worse error. One new finding, R-0274, is registered above for the
  block's own self-contradiction. `LAST_REVIEWED_SHA` advances 861eb371 ->
  6acb3f04.

- Reviewer gate on R8-close (2026-08-12, first gate of a NEW session; the
  round it certifies was the terminating round of the previous one, so per
  docs/agents/planner_reviewer_prompt.md §4.13 its verdict had lived only in
  `.agent/handoff.md` until now): PASS. Range 6acb3f04..7acb406d = five commits
  touching exactly the five paths the R8 block named — no production code, no
  test module, no docs. Transport by the PRIMARY shape: the reviewer original
  `.remedy-wt/f107-r8-1.block.md` survived the session boundary, `cmp` against
  `.agent/authored/f107-r8-1.md` and against `.agent/last_block.md` is silent,
  and all three sha256 to 607d240a3a067a4c… at 218 lines. All five slice bodies
  recompute to their BEGIN-marker digests at their declared lengths (LRF4FROM
  d129628f… 1 line, LRF4TO b36108ed… 13, LR7FROM cdc1e3cf… 1, LR7TO 47bc40dd…
  48, PLAN7 a065b87c… 28), and `sha256sum .agent/plan.md` returns that same
  PLAN7 digest over 28 lines. Both C3 pairs were APPEND-shaped and proven as
  such rather than asserted: `git show --numstat 3e704610 -- .agent/live_review.md`
  reads `59  0` — ZERO deletions, so neither anchor was edited — each FROM
  occurs exactly 1x in the file, each of the 12 LRF4TO and 47 LR7TO TO-only
  lines occurs exactly 1x among the 59 added lines, and 0 added lines belong to
  neither body. Every scoped gate was RE-RUN by this reviewer rather than read
  from the handback: `python3 -m pytest tests/orchestration/test_context_compiler.py -q`
  returns 55 passed, the canary `python3 -m pytest tests/cli/test_golden_path.py -q`
  returns 42 passed, `grep -c '^## Steps'` is 1, `grep -c '^- R-0274'` is 1,
  `grep -c '^Done:'` is 1 and `grep -c '^Landed:'` is 1, the stray-marker count
  is 0 across the three state files, `git status --porcelain` is empty,
  `git worktree list` shows the primary checkout alone, and HEAD equals
  `origin/feature/f107-context-compiler-v2`. One counted value in the handback
  did NOT survive re-measurement and is registered above as R-0275: C2's real
  numstat is `169 279`, not the reported `218/328`. The verdict is PASS anyway
  and deliberately so — the error is in the report of a commit that is
  cap-exempt by construction, every other figure re-measured true, and the
  round's substance (transport, application, gates) is verified correct. The
  stale next-free-ID header this gate also found is R-0276. `LAST_REVIEWED_SHA`
  advances 6acb3f04 -> 7acb406d.

- Reviewer gate on R9 (2026-08-12): PASS. Range 7acb406d..f86bda87 = eight
  commits touching exactly the nine paths the R9 block named. C1-C7 were made by
  the previous session's worker and C8 by this session's; the handoff says so and
  it changes nothing about the evidence. Transport by the PRIMARY shape: the
  reviewer original `.remedy-wt/f107-r9-1.block.md` survives at 277 lines, its
  first 17862 bytes `cmp` silent against BOTH `.agent/authored/f107-r9-1.md` and
  `.agent/last_block.md`, and all three sha256 to f8e42fd684fe2367… at 276 lines
  — the value the original's own trailer declares. All nine slice bodies
  recompute to their BEGIN-marker digests at their declared lengths (HDRFROM
  dfab3095… 1L, HDRTO 969938db… 1L, LRF5FROM 21a6a3f6… 1L, LRF5TO 21a8b66c… 23L,
  LR8FROM 686e2302… 1L, LR8TO 4894b692… 34L, LRDFROM 62450c77… 6L, LRDTO
  39b40890… 12L, PLAN9 33ad2144… 28L), and `sha256sum .agent/plan.md` returns
  that PLAN9 digest over 28 lines. Each pair was proven by ITS OWN shape rather
  than asserted: `git show --numstat 61adb419 -- .agent/live_review.md` reads
  `68  7`, the seven deletions being HDRFROM's 1 line plus LRDFROM's 6 — both
  REWRITES, whose FROM lines now occur 0x and whose TO lines occur 1x — while the
  two APPENDS keep their FROM exactly 1x and their 22 and 33 TO-only lines each
  occur exactly 1x among the 68 added lines, with 0 added lines belonging to no
  TO body. Every scoped gate was RE-RUN by this reviewer rather than read from
  the handback: 9 passed on the new CLI test module, 505 passed on the catalog
  and grouped-CLI suites, 42 passed on the canary, `ruff check` "All checks
  passed!", `git status --porcelain` empty, `git worktree list` the primary
  checkout alone, HEAD == origin/feature/f107-context-compiler-v2, and insertions
  per commit 276, 253, 68, 273, 19, 231, 12, 254 — each under 500. GATE h WAS
  RE-RUN, not read: with `REMEDY_DATA_DIR` pointed at the worker's scratch data
  root, `remedy job context 994eb8d1-… --task T001` reproduces the handoff's
  stdout line for line (164/24000 tokens; tier 1 src/payment_gateway.py full,
  tier 2 src/retry_policy.py full, tier 3 src/clock_source.py signatures;
  README.md and src/invoice_report.py omitted for distance), `--json` reproduces
  the same values, `--task T999` exits 3 with `Error: no task matches --task
  'T999'`, and a spot-check the block did not order — resolving the same task by
  its UUID prefix `52c783f1` — reaches the identical task. F107 HAS A CALLER and
  is no longer a library. All five declared deviations re-measured accurate, and
  TWO of them are reviewer errors, registered above as R-0277 and R-0278; the
  docs gap the worker flagged rather than silently fixed is R-0279.
  `LAST_REVIEWED_SHA` advances 7acb406d -> f86bda87.

- Reviewer gate on R10 (2026-08-12): PASS. Range f86bda87..c50080e0 = eight
  commits touching exactly the nine paths the R10 block named. Transport by the
  PRIMARY shape: the reviewer original `.remedy-wt/f107-r10-1.block.md` is 312
  lines, its first 311 lines are byte-identical to BOTH
  `.agent/authored/f107-r11-1.md`'s predecessor `.agent/authored/f107-r10-1.md`
  and `.agent/last_block.md`, and all three sha256 to
  d0117326ae081a8d… — the value the original's own trailer declares. All
  thirteen slice bodies recompute to their BEGIN-marker digests at their
  declared lengths, and `sha256sum .agent/plan.md` returns the PLAN10 digest
  fd7a81e4… over 28 lines. Pair shapes were proven, not asserted: `git show
  --numstat 58742979 -- .agent/live_review.md` reads `79  1` — the single
  deletion being HDRFROM, the only REWRITE targeting that file — while LRF6, LR9
  and LRD2 each keep their FROM exactly 1x and their 28, 37 and 13 TO-only lines
  each occur exactly 1x among the 79 added lines; the only lines that fail an
  exactly-1x count are BLANK lines, which is the R-0253 case where whole-file
  and whole-diff counting bends rather than the text. 0 added lines belong to no
  TO body, and the same holds for `docs/README.md`, whose two rows arrive in C6
  with numstat `2  0`. Every scoped gate was RE-RUN by this reviewer: 61 passed
  on the compiler suite (55 before, +6), 9 passed on the CLI view, 42 passed on
  the canary, 294 passed on `tests/docs/`, `ruff check` "All checks passed!",
  tree clean, primary worktree alone, HEAD == origin. GATE j WAS RE-RUN, not
  read: compiling the same five-file fixture repo and calling
  `write_context_size_comparison_json` reproduces the handoff's file byte for
  byte — `whole_file_tokens` 215, `compiled_tokens` 164, `saved_tokens` 51,
  `saved_ratio` 0.2372093023255814 — the compiled figure equals the 164 the
  shipped CLI view prints, and the writer created its missing parent. The
  reviewer also ran TWO mutation probes the block did not order, in a disposable
  worktree at c50080e0, removed and pruned before this verdict: fabricating a
  1.0 ratio for a zero baseline gives `2 failed, 59 passed`, and clamping a
  negative saving to 0 gives `2 failed, 59 passed` — the new tests genuinely
  bite. The deviation that matters is the block's own self-contradiction over
  where the `docs/README.md` rows land, registered above as R-0280; the worker's
  reading was correct and its declaration is exactly the wanted behaviour. The
  stale claim it flagged rather than silently fixed is R-0281.
  `LAST_REVIEWED_SHA` advances f86bda87 -> c50080e0.

- Reviewer gate on R11 (2026-08-12): PASS — and this is the round that makes
  F107's DONE condition real. Range c50080e0..04154822 = eight commits touching
  the EIGHT paths the R11 block enumerated (its prose said nine; that is
  R-0282). Transport by the PRIMARY shape: the reviewer original
  `.remedy-wt/f107-r11-1.block.md` survives, its body is byte-identical to
  `.agent/authored/f107-r11-1.md` and `.agent/last_block.md`, all three sha256
  to 121401148a1ec2f1… at 314 lines, and all nine slice bodies recompute to
  their BEGIN-marker digests. `git show --numstat 815e4294 --
  .agent/live_review.md` reads `78  1` — one deletion, HDR2 being the only
  REWRITE — and the anchored greps return exactly their specified values
  (R-0282 header 1, R-0280 header 0, `^- R-0280` 1, `^- R-0281` 1, `^Done:` 7,
  `^Landed:` 0). Every gate was RE-RUN by this reviewer: 6 passed on the new
  end-to-end module, 61 on the compiler suite, 42 on the canary, `ruff check`
  "All checks passed!", and THE REGRESSION GATE HELD — `test_pingpong.py` plus
  `test_pingpong_integration.py` return 43 passed, the same 43 measured before
  C4 touched the loop every job runs through. The C4 diff was read line by line:
  three keyword-only parameters that default to today's behaviour, one
  all-or-nothing branch, a local import inside that branch, records written only
  where the caller points, and `build_repo_context` reached unchanged in every
  other case — the default path does not move. GATE j WAS RE-RUN, not read: the
  fixture repo runs twice through `run_pingpong` with `FakeProvider`, and BOTH
  runs reach `staged_review_passed` while `context_chars` falls 4613 -> 899 and
  the size record reads whole_file_tokens 1067, compiled_tokens 195,
  saved_tokens 872, saved_ratio 0.817244611059044, with `src/invoice_report.py`
  omitted for `distance`. A fixture task is solved by the fake provider on a
  context 81.7% smaller, and the omissions record explains the exclusion: that
  is the feature file's Done sentence, measured. All ten declared deviations
  re-measured accurate; the substantive one is registered as R-0283 after the
  reviewer reproduced it independently, and the two citation errors are R-0284.
  `LAST_REVIEWED_SHA` advances c50080e0 -> 04154822.

- Reviewer gate on R12 (2026-08-12): PASS, and the round's decisive claim was
  reproduced in BOTH directions rather than read. Range 04154822..d7dd12b6 = six
  commits over exactly the six paths the R12 block enumerated, `git diff
  --name-only` returning that set and nothing else. Transport by the PRIMARY
  shape: `cmp .agent/authored/f107-r12-1.md .agent/last_block.md` exits 0 and
  silent under this reviewer's own run, both files sha256 to
  edc2563b00979927cd17d8837a3887d1b17620ea0fcf5844cbb20b9f92bbac54 at 242 lines
  — the value the R12 block's BLOCK_SHA256 trailer declares — and
  `.agent/plan.md` hashes to a949117f430008cc… as slice PLAN12 specified.
  `git show --numstat e7c700fc -- .agent/live_review.md` reads `65  1`: one
  deletion, HDR3 the only REWRITE. The anchored counts hold on disk now —
  `^Done:` 8, `^Landed:` 0, `^## Steps` 1, and `^<<<` 0 in live_review.md,
  plan.md and handoff.md alike.
  THE PROBE WAS RE-RUN BY THIS REVIEWER, twice, inside the disposable worktree
  `.remedy-wt/r13probe` and nowhere else, with the same one-line mutation
  `use_compiled_context = False` at pingpong_loop.py:2662 (`git diff --numstat`
  `1  1` each time). At 04154822 the e2e module returns 3 failed, 3 passed and
  `test_compiled_run_shrinks_the_context_and_still_solves_the_task` is among the
  THREE THAT STILL PASS — R-0283 reproduced independently, not quoted. At
  d7dd12b6 the same mutation returns 4 failed, 2 passed and that same test is
  now among the failures, on the new pin, verbatim `assert
  compiled.context_chars == len(expected_compiled_text)` -> `E assert 265 ==
  899`. 265 is the fall-through pack, 899 the compiler's own rendered bytes: the
  test that stands for F107's DONE condition finally bites the wiring it names.
  The worktree was removed and pruned; `git worktree list` is the primary
  checkout alone and `git status --porcelain` is empty. Every other gate re-run
  green by this reviewer: 6 passed on the e2e module, 43 on `test_pingpong.py`
  plus `test_pingpong_integration.py` — the same 43 R11 measured, so the loop
  every job runs through did not move — 42 on the canary, `ruff check` "All
  checks passed!", `git diff --stat 04154822..HEAD -- packages apps` EMPTY, and
  each commit's insertion column under 500 (242, 177, 65, 12, 8, 112). All six
  declared deviations re-measured accurate; deviation 4 becomes R-0285 because
  the conflict it declared was the block's, not the worker's.
  `LAST_REVIEWED_SHA` advances 04154822 -> d7dd12b6.
- Reviewer gate on R13, R14 and R15 (2026-08-12): PASS on all three, gated
  together by the reviewer of a NEW session because not one of them survived
  to write a handback. Range d7dd12b6..513a8c58 = eight commits over exactly
  four `.agent/` paths and nothing else: `git diff --stat 43e05108..HEAD --
  packages apps tests docs` is EMPTY and `git diff --name-only 43e05108..HEAD`
  returns `.agent/authored/f107-r15-1.md` and `.agent/last_block.md` alone.
  Transport by the PRIMARY shape, re-run here against the surviving
  `.remedy-wt/` originals rather than read from any summary:
  `.agent/authored/f107-r13-1.md` sha256 5fd436727e378348a182b30d459753cd… at
  280 lines, `f107-r14-1.md` cfb52b3917f3fed9639ceeb32b946373… at 278,
  `f107-r15-1.md` b1c8acaca006e1aa149814bdd12337cb… at 208 — each the value its
  own original's BLOCK_SHA256 trailer declares — and `cmp
  .agent/authored/f107-r15-1.md .agent/last_block.md` exits 0 and silent.
  `git show --numstat 43e05108 -- .agent/live_review.md` reads `29  1`, the
  single deletion being the header rewrite, and every anchored count holds on
  disk under this reviewer's own run: `^> Branch:.*Next free ID: R-0288` 1,
  `^- R-0286` 1, `^- R-0287` 1, `^Done:` 9, `^Landed:` 0, `^## Steps` 1,
  `^<<<` 0. Insertions per commit 280, 223, 56, 278, 156, 29, 208 and 147 —
  each under 500.
  WHAT DID NOT LAND, stated plainly because three rounds of state commits with
  no gate behind them is exactly what a false-progress record looks like: NO
  GATE EVIDENCE EXISTS. R13 and R14 died before their gate ran. R15's gate DID
  run — both suites, to completion — but died while copying its trimmed
  evidence into the repository, leaving five of the ten mandated files and no
  `attribution.txt`. Two of the missing five cannot be reconstructed at all
  (R-0288), so this reviewer treats R15's C3 as NOT DONE rather than as
  evidence to transcribe, and R16 re-runs the gate against a rebuilt base
  worktree. The surviving `.agent/gate_f107_r15/` is untracked partial output,
  never committed and now superseded; R16 moves it out of the repository
  rather than delete it, so the dead session's raw record stays readable.
  `LAST_REVIEWED_SHA` advances d7dd12b6 -> 513a8c58.
- Reviewer gate on R16 (2026-08-12): PASS, and the F107 INTEGRATION GATE IS
  GREEN. Range 513a8c58..5c808a59 = four commits over thirteen paths, every one
  under `.agent/`: `git diff --stat 513a8c58..5c808a59 -- packages apps tests
  docs` is EMPTY. Transport re-run here rather than quoted:
  `.agent/authored/f107-r16-1.md` and `.agent/last_block.md` both sha256
  39e6cb447d679ff3777e162f9832c489a49e72a5ab02aa60b7fde14db9650963 at 369
  lines — the value the surviving original `.remedy-wt/f107-r16-1.block.md`
  declares on the trailer one line past its saved region — and `cmp` between
  them exits 0 and silent. All seven slice bodies recompute to their
  BEGIN-marker digests at their declared line counts: SLICES=7 MISMATCH=0. C3
  is byte-exact, checked by extracting both sides from the diff and comparing
  the lists: its 49 added lines equal HDR16TO plus the TO-only tails of LRF16
  and LRG16 exactly, and its single deleted line is HDR16FROM.
  THE GATE ITSELF. Branch run at d94b0c97, `python3 -m pytest -n auto -q` ->
  exit 1, 5 failed / 16533 passed / 19 skipped, 221 s. Base run at the merge
  base 2e4142c3 in a rebuilt `tmp/base-gate` worktree,
  `REMEDY_UI_NO_AUTO_BUILD=1 python3 -m pytest -n auto -q` -> exit 1, 5 failed
  / 16457 passed / 19 skipped, 155 s. This reviewer recomputed the decisive
  comparison from the RAW scratch logs instead of the trimmed evidence:
  `grep -c '^FAILED'` is 5 in both `.remedy-wt/gate-scratch/f107-r16/
  branch_full.txt` and `base_full.txt`, the two committed FAILED lists are
  byte-identical (md5 cbf4dd9c85afafaf20aba2e38f940cee each), and therefore
  branch-only 0, base-only 0, common 5. The five common ids are R-0286's
  `[reviewer]` parametrizations, failing at a merge base where no F107 commit
  exists — not charged to F107, and the reason both runs exit 1. UI parity
  holds: four identical `apps/ui/dist` aggregate content hashes
  fb68a7293502c79b8ece61d154f5752100a16da1a08a481a7a4c1d79a5a503c0 (base and
  primary, before and after) with dist mtimes newer than src, so the seven-id
  `tests/ui_server/test_live_state.py` environment class of R-0221 does not
  appear in this gate at all. The collected-test delta 16557 - 16481 = 76
  equals the 76 tests `--collect-only` counts across the three test files F107
  adds, so it is F107's own coverage and not a selection difference. Wall clock
  221 s and 155 s, both inside the ~5 min budget, so no perf pass is indicated.
  Per docs/agents/integration_gate.md step 5 the verdict is the reviewer's and
  it is PASS, the five R-0286 ids carried as a documented risk.
  WHAT DID NOT LAND: C5 (`.agent/plan.md`) and C6 (`.agent/handoff.md` and the
  push). The session died after C4. Both files still describe R12 and the
  branch stood twelve commits ahead of origin at review time — registered here
  as R-0289. R17 lands that tail and nothing else.
  `LAST_REVIEWED_SHA` advances 513a8c58 -> 5c808a59.
- Reviewer gate on R17 (2026-08-12): PASS. Range `5c808a59..54d05e37` = five
  commits over five paths, every one under `.agent/`: `git diff --stat
  5c808a59..HEAD -- packages apps tests docs README.md` is EMPTY. Insertions per
  commit 285, 214, 72, 13 and 94, each far under 500. Transport by the PRIMARY
  shape, because the reviewer's original survives on disk:
  `.remedy-wt/f107-r17-1.block.md` carries BLOCK_SHA256
  6b91d4fcc89f8c67ac4f8a51ea8b5453969dcd603117109f96c77e576511a3d6 on the
  trailer one line past its saved region, `head -n -1` over that file recomputes
  exactly that digest, and `.agent/authored/f107-r17-1.md` and
  `.agent/last_block.md` both hash to it at 285 lines with `cmp` exit 0 and
  silent. `git show --numstat 40e5bf7b -- .agent/live_review.md` is `72 1`;
  `sha256sum .agent/plan.md` is
  d40eabc5d461b094b53b462c9b0dc9215f92e36072124dadd26d5a8608ae9f29 at 29 lines.
  On the files after: `^<<<` 0 in live_review, plan and handoff, `^## Steps` 1,
  `^Done:` 10, `^Landed:` 0, `Next free ID: R-0290` 1x, `^- R-0289` 1x. Every
  gate was RE-RUN by this reviewer rather than read from the handback: the canary
  `python3 -m pytest tests/cli/test_golden_path.py -q` returns 42 passed at exit
  0, and the FULL suite `python3 -m pytest -n auto -q` returns `5 failed, 16533
  passed, 19 skipped in 131.74s` — the same five R-0286 `[reviewer]` ids and the
  same three counts R16 recorded on this branch, which re-confirms closure
  precondition 2 rather than opening a new gate. `python3 -m apps.cli.grouped
  integrity check --json` returns `"passed": true` with 5 of 5 checks,
  `untracked=0, relevant=0` and no open blocker/high findings. `git status
  --porcelain` is empty, `git worktree list` shows the primary checkout alone,
  and `git rev-list --left-right --count origin/...v2...HEAD` is `0 0`. The
  126-line handoff is a declared D15 stated-cause overage carrying its mandated
  tables, which AGENTS.md permits. `.agent/STOP`, present when R17 handed back,
  is gone: the operator cleared it and started this session, which is guardrail
  G6 working rather than failing. Three findings are registered above from this
  gate — R-0290, R-0291 and R-0292 — the first two found by auditing this
  session's own start and the roadmap's Design bullets against the disk, the
  third by reading the selector's treatment of `parse_failed`.
  `LAST_REVIEWED_SHA` advances 5c808a59 -> 54d05e37.
- Reviewer gate on R18 (2026-08-12): PASS. Range `54d05e37..6e1970c4` = seven
  commits over the ten paths the R18 Change line names and no others; `git diff
  --numstat` reads 407/0, 381/259, 113/1, 33/6 and 70/0, 3/2 and 1/1, 54/0,
  23/19 and 113/124, so every commit's insertions stand far under 500.
  Transport, shape stated because it is NOT the primary one: no reviewer
  scratch original for R18 survives — `.remedy-wt/` holds F105-era block files
  only — and the saved block carries no BEGIN-marker digest, so neither the
  cmp-against-scratchpad proof nor the §4.9 digest fallback was available to
  this reviewer. What IS proved: `.agent/authored/f107-r18-1.md` and
  `.agent/last_block.md` are byte-identical at 407 lines, both hashing to
  6d1ea116f1f33c97682e5cf26267ef28304c4b7c1bb64a520763d9f22425dd39, and this
  reviewer read the saved block against the disk item by item rather than
  trusting the handback. Two gates were RED and are accepted as declared, both
  now registered as R-0294: the block's 407 lines against the 400 cap, and gate
  C's first clause, whose string the block's own gate text writes at line 905.
  The append shapes are exact: C3 adds 113 and removes 1, and PAIR_LRF_TO's 79
  TO-only lines plus PAIR_LRG_TO's 33 plus the one-line header rewrite account
  for all 113, leaving no stray. Every remaining gate was RE-RUN here, not
  read: `test_context_compiler.py` collects 64 and passes, up from the 61 the
  R17 gate recorded, `test_context_compiler_e2e.py` and
  `tests/cli/test_job_context_cmd.py` pass 15 together, `tests/docs/` passes
  294, the canary `python3 -m pytest tests/cli/test_golden_path.py -q` returns
  42 passed in 19.66s, and `python3 -m ruff check` over the two changed Python
  files returns "All checks passed!". The vocabulary edits hold on disk: the
  old reason list is 0x and the new one 1x in the feature file, the old guide
  clause is 0x and the new one 1x, DECISION F107 D1 and D2 each occur once with
  D1's heading immediately after its anchor at `.agent/decisions.md:4248-4250`,
  and `^<<<` is 0 across all eight touched files. `git status --porcelain` is
  empty, `git worktree list` shows the primary checkout alone, `git rev-list
  --left-right --count` against the remote is `0 0`, and `gh pr list --state
  open` returns an empty list. R-0291 and R-0292 are resolved below. One new
  code finding came out of this gate rather than out of the handback: probing
  the selector's third signature path showed the R18 repair reached two of
  three, which is R-0293 above, so the registered count returns to 20 open.
  `LAST_REVIEWED_SHA` advances 54d05e37 -> 6e1970c4.
- Reviewer gate on R19 (2026-08-12): PASS. Range `6e1970c4..65723390` = six
  commits over exactly the eight paths the R19 Change line names; `git diff
  --numstat` reads 379/0, 293/321, 96/1, 14/2 and 28/0, 67/0, 10/12 and
  103/99, so every commit stands far under the 500 cap. Transport by the
  PRIMARY shape, restored after R18 could not offer it: the reviewer's own
  original survives at `.remedy-wt/f107-r19-1.block.md`, and `cmp` against
  `.agent/authored/f107-r19-1.md` is silent at exit 0, as is `cmp` of that file
  against `.agent/last_block.md`. Stronger than the counts: every authored
  payload was extracted from the reviewer's original and searched for as a
  whole string in its target — PAIR_HDR_TO, PAIR_LRF_TO, PAIR_LRG_TO and
  PAIR_DONE_TO each occur exactly 1x in `.agent/live_review.md`, PAIR_BS_TO
  exactly 1x in `docs/roadmap/features/T2_F107.md`, and `.agent/plan.md` equals
  PAYLOAD_PLAN byte for byte. Nothing was retyped and nothing drifted. The
  block was 379 lines against the 400 cap, so R-0294's first instance did not
  recur. Append shapes: C3 adds 96 and removes 1, and 35 + 35 + 25 TO-only
  lines plus the one-line header rewrite account for all 96; the worker's
  qualifier that two of those TO-only lines are blank is correct and is the
  R-0253 exception this file already records. Gates RE-RUN here rather than
  read: 80 passed across `test_context_compiler.py` (65, up from 64),
  `test_context_compiler_e2e.py` (6) and `tests/cli/test_job_context_cmd.py`
  (9), `tests/docs/` 294 passed, the canary 42 passed in 20.06s, `ruff` "All
  checks passed!", `^Done:` 12 and `^Landed:` 0, `^<<<` 0 across all six
  touched files, `^## Built State` 1 in the feature file with zero deletions in
  that commit. The red-proof was re-run INDEPENDENTLY by this reviewer in a
  disposable worktree at HEAD: removing only the phase-A `parse_failed` append
  turns the new test red with `Right contains one more item: ('unparseable',
  'signatures')`, and the worktree was removed and pruned, leaving the primary
  checkout clean and alone. This reviewer's own probe, written before the
  repair existed, now reports the `unparseable` record where it reported none —
  the fix is confirmed against evidence that predates it. The two declared
  substitutions are accepted: `remedy` is unavailable to this session's shell
  and both plan probes ran through `python3 -m apps.cli.grouped`, the same
  entry point the R17 gate used, with real output pasted; and the 119-line
  handoff is a DECISION D15 stated-cause overage carrying every mandated
  section. `git status --porcelain` empty, one worktree, `0 0` against the
  remote, `gh pr list --state open` empty. R-0293 is resolved below.
  `LAST_REVIEWED_SHA` advances 6e1970c4 -> 65723390.

Done: R-0271 — RESOLVED. `packages/orchestration/context_compiler.py` now reads
`from collections.abc import Iterable` (commit b52b1c3c, numstat `1 1`), and the
reviewer's own re-run of `python3 -m ruff check` over that module and its test
file returns exit 0 with "All checks passed!" — zero errors, where the same
command reported UP035 before the fix. Open findings 9 -> 8.

Done: R-0273 — RESOLVED. `CompiledContext` carries a fifth field `line_cap`,
`compile_task_context` sets it from the caller's cap, and
`render_compiled_context_text` renders signature bodies at `compiled.line_cap`
instead of `DEFAULT_SIGNATURE_LINE_CAP` (commit e0f0a0d1 "fix(f107): render
signatures at the compiled line cap", C5 of R7). The fix was MEASURED, not
read: on the same three-file fixture at `line_cap=3` that produced the finding,
the rendered text's estimate falls from 128 tokens to 46 against an
`estimated_tokens` of 25, so the 5.1x divergence is gone, and two mutation
probes in a disposable worktree put the module back to red (1 failed / 3
failed) — the regression test genuinely bites. The residual 21-token gap is the
one header line the renderer adds per included file, uniform at every cap and
not drift. Open findings 11 -> 10.

Done: R-0275 — RESOLVED. The R8 handoff text that carried the wrong `218/328` no
longer exists on disk (C8 of R9 rewrote the file), and the class did not recur:
this reviewer re-measured every `+/-` cell of the R9 handoff against `git show
--numstat` and all eight agree — 276/0, 253/195, 68/7, 273/0, 17/0 plus 2/1,
231/0, 12/12 and C8's own 254/94 — with the insertion column, not a line count,
in every cell. Open findings 15 -> 14.

Done: R-0276 — RESOLVED. `.agent/live_review.md` line 8 read `Next free ID:
R-0277.` at f86bda87, measured line-scoped so that the finding's own quotation of
the stale string cannot pollute the count: `grep -c '^> Branch:.*Next free ID:
R-0271'` is 0 and the R-0277 form is 1. The one carrier that owns the ID sequence
is correct again, and this round allocates past it. Open findings 14 -> 13.

Done: R-0277 — RESOLVED. The R10 block's procedure step 1 no longer says
"below": it names the trailer line of `.remedy-wt/f107-r10-1.block.md` as the
digest's home and says in the same sentence that the trailer sits one line PAST
the saved region. The worker met the gate against that artifact without a
correction of its own, and this reviewer re-derived it independently — the
original's first 311 lines hash to d0117326ae081a8d…, which is what its line 312
declares. Open findings 15 -> 14.

Done: R-0278 — RESOLVED. Every zero-gate in the R10 block was anchored to the
line it is about rather than to the whole file, and the gate that used to be
unmeetable now measures what it means: `grep -c '^> Branch:.*Next free ID:
R-0277'` is 0 and `'^> Branch:.*Next free ID: R-0280'` is 1, both re-run by this
reviewer, while `.agent/live_review.md` still legitimately contains the string
`R-0277` inside R-0277's own body. The self-counting-gate class has a written
counter-measure that a block now demonstrably follows. Open findings 14 -> 13.

Done: R-0279 — RESOLVED. `remedy job context` is documented:
`docs/guides/job-context-view-user-guide-v0.md` exists at 184 lines and the
`docs/README.md` index carries its two rows (quick-find and guides table),
landing in C6 with numstat `2  0`. `python3 -m pytest tests/docs/ -q` returns
294 passed under this reviewer's own re-run, including the link-resolution check
that made the ordering matter. Open findings 13 -> 12.

Done: R-0281 — RESOLVED. `tests/orchestration/test_context_compiler.py` no
longer calls `write_omitted_context_json` "the one writing function" (commit
b4e9d423, numstat `1 1` — one line changed and nothing else in the file), and
the reviewer's own re-run of that module returns 61 passed. The stale-absolute
claim class now has no live instance in this feature's files. Open findings
15 -> 14.

Done: R-0283 — RESOLVED. The end-to-end test that stands for F107's DONE
condition no longer passes with the compiled path disabled. Commit 0df94864
(numstat `12  0`, one test file, no production byte moved) pins the compiled
run's `context_chars` to `len(render_compiled_context_text(...))` over the same
fixture, and this reviewer's own mutation probe — `use_compiled_context = False`
in a disposable worktree — turns the module from `3 failed, 3 passed` at
04154822, where the test PASSED, to `4 failed, 2 passed` at d7dd12b6, where it
fails on `assert 265 == 899`. A bypass can no longer satisfy the feature's Done
sentence. Open findings 14 -> 13.

Done: R-0288 — RESOLVED. The parity proof R15 could not show exists on disk for
R16, and this reviewer read the files rather than the summary that describes
them. `.agent/gate_f107_r16/base_worktree.txt` records the `git worktree add -b
tmp/base-gate`, both `cp -a` copies, the `find ... -exec touch {} +` and the
three identity checks, each with its real exit code; `dist_hashes.txt` carries
the four aggregate `apps/ui/dist` content hashes — base before, base after,
primary before, primary after, all
fb68a7293502c79b8ece61d154f5752100a16da1a08a481a7a4c1d79a5a503c0 — plus the
newest-src, newest-dist and oldest-dist mtimes that prove the ordering the R13
base run lacked. Ten of the ten mandated evidence files are committed, where
R15 left five and no `attribution.txt`. The forward-looking rule the finding
states held in practice: every number in those ten files also exists in the
gitignored raw record at `.remedy-wt/gate-scratch/f107-r16/`, which is why this
reviewer could re-derive the gate's decisive comparison from `branch_full.txt`
and `base_full.txt` directly instead of trusting the trimmed copies. Open
findings 18 -> 17.

Done: R-0291 — RESOLVED. The finding asked for the operator-visible record
§4.7 requires of a spec deviation, not for the deferred code. That record is on
disk: `.agent/decisions.md:4250` carries `## DECISION F107 D1 (2026-08-12) —
two Design bullets are DEFERRED, on the record`, naming both gaps — no
production caller for `register_compiled_context_segment`, and a CLI tier 1
that is the files_hint alone — with the chosen option, the two alternatives
that were rejected and the concrete reversal condition. This reviewer read the
committed text rather than the handback's summary of it, and confirmed the
heading sits immediately after its anchor with one blank line between. The
deferral is now visible where an operator looks instead of only in a module
docstring. Open findings 20 -> 19.

Done: R-0292 — RESOLVED for the two paths it names, with the third split out as
R-0293 rather than folded in silently. `OMISSION_REASON_UNPARSEABLE` exists
beside the other four constants; the tier-2 over-cap path and the tier-3 path
both obtain the `FileSignatures` object once, estimate from its own rendered
lines, and append an `unparseable` record when `parse_failed` is set, while
tier 1 stays exempt. Three tests pin exactly that — the tier-3 file carried
empty with one record, the over-cap tier-2 file carrying both `size` and
`unparseable` and no others, and the unparseable tier-1 file carried whole with
none — and the suite this reviewer re-ran collects 64 where it collected 61.
The fifth reason reached the vocabulary test, the feature file's Design
enumeration and the user guide in the same round as the code, so no reader
meets a word the plan does not carry. Open findings 19 -> 18.

Done: R-0293 — RESOLVED. Phase A of `compile_task_context` now takes the
`FileSignatures` object once through `extract_file_signatures`, estimates from
its own rendered lines, and appends an `unparseable` record beside the existing
`budget` one when `parse_failed` is set, so the third and last signature path
stops blaming the budget for a blank the budget did not cause. Verified three
ways by this reviewer rather than once: the diff reads as specified with the
budget record unchanged; the probe that FOUND the gap, written before any fix
existed, now reports `('broken.py', 2, 'unparseable', 'signatures')` where it
reported only the budget record; and the new test, run in a disposable worktree
with only that append removed, fails with `Right contains one more item:
('unparseable', 'signatures')` — it bites the exact line it names.
`_signature_render_text` survives for `render_compiled_context_text`, unchanged.
The suite collects 65 where it collected 64, and the Edge-cases clause
"signature-skipped WITH REASON otherwise" now holds on every path that renders
signatures. Open findings 20 -> 19.
