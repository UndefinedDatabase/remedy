# Live Review — F115 Prompt breakdown & cost report

> Round-by-round review record for F115, reset at the feature claim. The F111
> record is preserved in git history at its closure commit 98a49b5c. Finding
> IDs continue monotonically across features and are never renumbered.

## Steps
R1 claim, state reset and shape inventory → T001 manifest-alongside-actuals
persistence with backfill tolerance → T002 aggregation queries, the pure
renderer and its goldens → T003 CLI, period comparison and json schema →
integration gate → closure.

## Findings

- R-0320 — Low — carried forward from the F111 closure-candidates file under
  the disk-vehicle rule (docs/roadmap/STATUS_closure_protocol.md,
  "Closure-candidate findings"). A stop reason no code can ever emit:
  `STOP_REASONS` in `packages/orchestration/builder_bridge.py` declares
  `stale_diff_context`, and a repo-wide grep over every `.py` file finds that
  string in exactly one place — the frozenset itself. Nothing raises it,
  nothing tests it, nothing reads it. It predates the F111 branch (it is
  present at the merge base 4e0b762e), so it was not an F111 defect and was
  deliberately not fixed there. It is not fixed in F115 either: AGENTS.md bars
  mixing an unrelated fix into a feature branch, and F115 opens the token
  ledger and the report renderer, not the builder bridge. The remedy — wire it
  to the condition it names, or delete it — is a one-commit change that
  belongs to whichever feature next has a legitimate reason to open
  `builder_bridge.py`. Recording it here keeps it findable after
  `.agent/candidates.md` is emptied, which is the whole point of the
  carry-forward rule. OPEN.

- R-0321 — Low — `.agent/f115_inventory.md` says "only four of the eight
  `build_trace_entry` call sites pass `composed_prompt`". The count of
  non-test call sites is SEVEN, not eight: `intake.py:135`,
  `flight_plan.py:181`, `orchestrator_loop.py:920`, `mission_compiler.py:280`,
  `pingpong_loop.py:2824`, `pingpong_loop.py:3010` and
  `apps/cli/commands/job.py:236`. The inventory's own enumeration names four
  that pass and three that do not, which is seven, so the number contradicts
  the list directly above it. Every individual citation is correct and the
  round's conclusion is unaffected — this is an arithmetic slip in prose, not
  a bad reading of the source, and it is registered rather than waved through
  because a wrong total in an inventory is exactly the kind of number a later
  round quotes without re-counting. Fix: change "eight" to "seven" in that
  sentence and nothing else. OPEN.

- R-0322 — Medium — the suite is RED at this branch's merge base. Five ids in
  `tests/orchestration/test_role_conventions.py` fail, every one a
  `[reviewer]` parametrization, each raising `PromptSegmentError: prompt
  segment 'reviewer_conventions' is over its token cap: 954 tokens estimated,
  cap 800` before any assertion in the test runs. Measured by the reviewer at
  the R2 gate: `5 failed, 21 passed in 0.14s`. It is NOT an F115 defect —
  `docs/agents/reviewer_conventions.md` was last touched at a85e82f5 on
  2026-08-12, before this branch existed, and
  `git diff --name-only 0d6c97aa..HEAD` over that path and over
  `prompt_facts.py` is empty. It is the same class F111 recorded as R-0286 and
  attributed at its integration gate in both trees. It is registered here
  rather than inherited silently because F115's own integration gate will meet
  it, and a gate that has to rediscover a known red spends a round proving
  something already known. It is deliberately NOT fixed on this branch:
  AGENTS.md bars mixing an unrelated fix into a feature branch. The fix
  belongs to a round that legitimately opens the conventions document or the
  cap. OPEN.

Done: R-0321 — RESOLVED at the R4 gate. Verified against the disk, not the report: `grep -c 'four of the eight' .agent/f115_inventory.md` prints 0 and `grep -c 'four of the seven'` prints 1, the enumeration below that sentence still names four wired call sites and three unwired, and `git show --numstat 8412f20c` shows the C3 commit of R3 changed exactly one line of that file. The R3 round as a whole is PASS: gates (a)-(g) were re-run by the reviewer and every value matched the handback, and the R3 diff touched only `.agent/**` and `docs/agents/planner_reviewer_prompt.md`, as its block declared.

- R-0323 — Low — reviewer gate arithmetic, self-registered. The R4 block's gate
  (f) demanded that `git diff --name-only 0d6c97aa..HEAD` list SEVENTEEN paths
  — "the fifteen of R1-R3 plus this round's two new ones
  (`.agent/authored/f115-r4-1.md`, `tests/orchestration/test_prompt_trace.py`)".
  `tests/orchestration/test_prompt_trace.py` was ALREADY one of those fifteen:
  R2 added the builder behaviour test and its wiring guard to that same file,
  and `git diff --name-only 0d6c97aa..8601e276` lists it. Only one path was new
  in R4, so the reachable total was SIXTEEN and the ordered seventeen was
  unmeetable by construction. The worker measured 16, reported it, changed
  nothing to meet the number, and declared the deviation — the correct
  behaviour, and the round cost one declared deviation to prove a reviewer
  slip. Same class as R-0282 (F107 R11, "exactly these nine paths" over a list
  of eight) and R-0321 (F115 R1, "four of the eight" over a list of seven);
  three instances now, all of them a count stated in prose that the reviewer
  never re-derived from the list beside it. The standing counter-measure is
  already on disk as checklist item 8
  (`docs/agents/planner_reviewer_prompt.md`, added at 43763bf4) — it says to
  compute a gate's expected value from the source that PRODUCES it. A path
  count's source is the previous round's own `git diff --name-only` output,
  which the reviewer had already run in that same session and did not re-read.
  No fix is possible on disk: the block is committed verbatim by design and
  R4's verdict already stands as PASS. It is registered so the pattern is
  countable rather than forgotten. OPEN.

- R-0324 — Low — reviewer spec arithmetic, self-registered, caught before the
  round it would have broken. DECISION F115 D2 (R5) fixed the planner segment
  ranks as "the job prompt at TASK rank, the recalled memory section at
  JOB_CONTEXT rank". Composition sorts by rank ASCENDING
  (`compose_prompt_segments`, `prompt_segments.py:182-188`) and JOB_CONTEXT is 3
  against TASK's 4, so that assignment composes the MEMORY SECTION FIRST, while
  the code it must reproduce concatenates the other way round —
  `prompt = f"{prompt}\n\n{memory_section}"`, `llm_planner.py:107-109`. D2's own
  byte-identity gate, the one it calls the round's first gate, was therefore
  unmeetable by construction — reading the rank names as semantic labels rather
  than as the sort key they are is what produced the slip. Corrected before
  emission as DECISION F115 D3, by checklist item 8
  (`docs/agents/planner_reviewer_prompt.md`) — compute a gate's expected value
  from the code that PRODUCES it. Fourth of the reviewer-arithmetic class after
  R-0282, R-0321 and R-0323, and the first caught before a worker paid. OPEN.

- R-0325 — Low — the R6 authored import block left `tests/test_llm_planner.py`
  ruff-dirty. TEXT-G placed `from packages.orchestration.prompt_segments import
  (...)` ABOVE the existing `planner_models` import, so the block is no longer
  alphabetically sorted and `python3 -m ruff check tests/test_llm_planner.py`
  reports `I001` (un-sorted import block) at line 7 — measured by the reviewer
  at the R6 gate, against a file that printed `All checks passed!` one commit
  earlier. `I` is an enabled rule class (`pyproject.toml:50`), so this is a real
  regression this branch introduced, not a pre-existing style debt; it is Low
  because no suite test and no CI workflow runs ruff (the repository has no
  `.github/workflows/`), so nothing turns red today. The worker was right to
  report it rather than edit an authored slice to fix it. Fix: move the
  `prompt_segments` import below `planner_models`. OPEN.

- R-0326 — Low — the R6 authored docstring carries a live escape sequence. The
  `compose_planner_prompt` docstring is a normal (non-raw) string containing the
  characters backslash-n twice, so Python turns them into two real newlines and
  the rendered `__doc__` breaks its own sentence mid-clause — the text meant to
  NAME the delimiter instead BECOMES it. The source file reads correctly and
  ruff stays silent (backslash-n is a valid escape, so no W605), which is why
  the R6 gate did not catch it; `help(compose_planner_prompt)` is where it
  shows. Reviewer-authoring defect, same class as R-0325: the authored bytes
  were correct as bytes and wrong as Python. Fix: name the delimiter in words
  instead of spelling it. OPEN.

Done: R-0325 — RESOLVED at the R7 gate. Verified against the disk, not the report: `python3 -m ruff check tests/test_llm_planner.py` prints `All checks passed!` with exit 0 at f20f172a, and `git show dd7feebd` shows the fix is exactly one moved line — the `planner_models` import now sits ABOVE the `prompt_segments` block, one insertion and one deletion in that file and no other file touched. `python3 -m pytest tests/test_llm_planner.py -q` prints `38 passed`, the R6 baseline unmoved, so the reorder changed no behaviour. The four-file ruff sweep the block also ordered prints `All checks passed!` with exit 0.

Done: R-0326 — RESOLVED at the R7 gate. Verified against the RENDERED docstring rather than the source line, because the source line was never the defect: `compose_planner_prompt.__doc__` now contains no backslash-n sequence at all and its sentence reads intact, naming `PROMPT_SEGMENT_DELIMITER` as "the same blank-line separator this module concatenated by hand". `git show cbe38b90` confines the change to that docstring, four insertions and three deletions in `packages/orchestration/llm_planner.py`. The R7 round as a whole is PASS: the reviewer re-ran gates (a) through (i) and every value matched the handback — cmp exit 0 with sha256 c6ab0e7d25c42144af766401daf7a90309dae3736c6c0ba8285a0a6b9942ea00 over both copies, the five live-review counts 1/1/7/1/1, ruff clean over all four files, `38 passed`, the inventory's 1/6/6, canary `42 passed`, `wc -l .agent/plan.md` = 38, an empty `git status --porcelain`, and 24 changed paths with no `.remedy-wt/**` among them. The R7 diff touched only the eight paths its block declared, and the C5 inventory's load-bearing claims were spot-checked against source: thirteen `calls` columns with exactly three NOT NULL and no DEFAULT clause, `grep -rn "ALTER TABLE" --include=*.py .` zero matches, `grep -rn "unattributed" --include=*.py .` zero matches.

- R-0327 — Low — reviewer gate arithmetic, fifth of its class. R8's gate (e)
  demanded `grep -c` of the literal `        2: (` with EIGHT leading spaces.
  `_MIGRATIONS` is a dict whose KEYS sit at FOUR spaces — `1: (` at
  `token_ledger.py:170` is the shape the reviewer had already read in that same
  session — and the block's own TEXT-E, authored by the reviewer, places `2: (`
  at four spaces too. Real values: the eight-space pattern counts 0, the
  four-space one counts 1, at `token_ledger.py:207`. The eight-space indent
  belongs to the STATEMENT lines INSIDE the tuple, not to the key that opens it.
  The worker measured both, reported the real numbers and changed nothing to
  meet the ordered one — the correct behaviour, and it cost the round nothing
  because the gate asked for real values. Nothing on disk is wrong, so there is
  no fix; it is registered so the class stays countable. After R-0282, R-0321,
  R-0323 and R-0324. The standing counter-measure is already on disk as
  checklist item 8 (`docs/agents/planner_reviewer_prompt.md`): compute a gate's
  expected value from the code that PRODUCES it. Here that code was the block's
  OWN authored replacement text, four lines below the gate that miscounted it —
  the shortest distance any instance of this class has yet had. OPEN.

- R-0328 — Low — the R8 red-proof under-predicted its own blast radius. Gate (g)
  stated "Tests 1, 2 and 3 assert the table exists, so they MUST fail". The real
  result, with migration step 2 deleted in a disposable worktree, was `8 failed,
  78 passed`: all FOUR new tests — the fourth,
  `test_a_pre_f115_call_owns_no_segment_rows`, on `sqlite3.OperationalError: no
  such table: call_segments`, because its assertion SELECTs from that very table
  and the same block authored that assertion — plus four pre-existing
  `TestOpenLedger` tests that pin the version constant against the last
  migration step. The ordered COLOUR was right and the round went red exactly as
  required; what was wrong was the COUNT. An under-counted red-proof invites a
  worker either to doubt a correct result or to trim the mutation until the
  prediction fits, and neither is a thing a gate should tempt anyone into.
  Checklist item 5 governs a red-proof's REACHABILITY; this is its arithmetic
  sibling and the first recorded instance. No on-disk fix: the round's evidence
  is correct and more complete than the gate that asked for it. A welcome
  by-product of the over-shoot: `test_schema_version_matches_the_last_migration_step`
  already pins `SCHEMA_VERSION` to the highest `_MIGRATIONS` key, so a version
  bump without its step, or a step without its bump, cannot pass today. OPEN.

- R-0329 — Low — a manifest value of the wrong TYPE becomes a measured zero in
  the sums T002 is about to build, which is the exact outcome the helper's own
  docstring says it prevents. `_call_segment_row` (`token_ledger.py:1247-1276`)
  checks only that the five `_MANIFEST_KEYS` are PRESENT and then takes their
  values VERBATIM, so a trace line carrying `"chars": "not-a-number"` yields a
  `CallSegmentRow` whose `chars` is that string. SQLite then accepts it:
  `chars INTEGER NOT NULL` is an AFFINITY, not a constraint, so a string that
  does not look like a number is stored AS TEXT and the NOT NULL is satisfied.
  Measured by the reviewer at the R9 gate against a scratch in-memory database:
  `typeof(chars)` prints `text`, and `SUM(chars)` over that row plus one real
  row of 10 prints `10.0`. Both halves of that result matter. The bad row
  contributed 0, which is precisely the "unpublished figure must never become a
  measured zero (P6)" the docstring four lines above the defect forbids; and
  the sum came back a FLOAT, which would move the bytes of any markdown golden
  that renders the same figure as an integer everywhere else — so R11's goldens
  would be pinned to a shape one malformed input can change. It is NOT
  reachable from Remedy's own composer, which publishes real ints through
  `manifest_as_dicts()`; it is registered anyway because the reader's entire
  contract is that it survives ARBITRARY file content, and "our producer is
  well behaved" is not the guarantee that contract makes. Fixed in R10 rather
  than deferred: R10 is the slice that starts SUMming those two columns and is
  therefore the round with a legitimate reason to open that helper, so fixing
  it here mixes nothing that does not already belong to the change. The R9
  round as a whole is PASS. The reviewer re-ran gates (a) through (i) and every
  value matched the handback: cmp exit 0 with sha256
  c5c5bc40c103ce743a81156078a727231460fe321be65e87613e2dc0265244b6 over both
  copies, the five live-review counts 1/1/9/3/1, the six `token_ledger.py`
  counts 1/1/1/4/2/3, ruff `All checks passed!` and the import exit 0, zero
  changed lines assigning a `BackfillResult` counter and zero inside its class
  body, `92 passed` and `41 passed`, canary `42 passed`, `wc -l .agent/plan.md`
  38, an empty porcelain, 28 changed paths with no `.remedy-wt/**` among them,
  and 0/0 against origin. The red-proof was RE-RUN INDEPENDENTLY by the
  reviewer in its own disposable worktree rather than accepted from the report:
  mutating `segment_rows_from_trace_file` to `return []` reproduced `5 failed,
  87 passed` and the same five test ids the handback names, and the worktree
  was removed and pruned with `git worktree list` left showing one line. OPEN.

Done: R-0329 — RESOLVED at the R10 gate. Verified against the code and a live probe, not the report: `_MANIFEST_KEY_TYPES` now names the type each of the five manifest keys must ALREADY be, `_MANIFEST_KEYS` is derived from it so the key order still has one spelling, and `_call_segment_row` skips a dict whose value is of the wrong type by the same rule that skips a missing key — bool excluded from int explicitly. The reviewer re-ran the round's own probe class: reverting the guard to the presence-only check makes `test_a_wrongly_typed_manifest_value_is_skipped_like_a_missing_key` fail and nothing else, so the test genuinely catches the regression rather than passing alongside it. The R10 round as a whole is PASS: gates (a) through (i) were re-run by the reviewer and every value matched the handback — cmp exit 0 with sha256 93a5a6347496a811cb9887d64f9d2312c42824537df592cd1ad6a846fc5f8731 over both copies, `wc -lc` 322 20573, the live-review counts 1/10/3/1, the seven token_ledger counts 4/4/1/1/1/4/3, ruff `All checks passed!` and the import exit 0, `99 passed` and `41 passed` (140 in one run), canary `42 passed`, `wc -l .agent/plan.md` 41, 29 changed paths with no `.remedy-wt/**` among them, and 0/0 against origin. Both declared deviations are accepted: the C3 fixture swap keeps the bad bytes on disk while sparing a shared helper, and the C4 placement puts the two dataclasses where this module already keeps every result type, which is better than the block ordered. `git status --porcelain` is NOT empty — it carries `?? .agent/STOP`, the operator signal that ended the session — and that is the one gate value the round could not meet, correctly reported rather than routed around.

- R-0330 — Low — `query_segment_shares` promises more than it delivers in the
  first line of its own docstring. It says "READ-ONLY, never raises", flat,
  while `query_cost` — the function it is modelled on, twenty lines above it in
  the same module — scopes the identical claim precisely: "READ-ONLY, and never
  raises on absence". The narrower wording is the true one. Both functions
  resolve their target through `_resolve_ledger_path`, which raises
  `ValueError("a ledger target needs either project_id or path")` when given
  neither `project_id` nor `path`. Measured by the reviewer at the R10 gate:
  calling each with no arguments raises that exact `ValueError` from both, so
  the two docstrings describe the same behaviour and only one of them describes
  it correctly. The behaviour is right and no caller is misled today, which is
  why this is Low and not a defect of the round: what is wrong is a promise a
  reader can check and find false, in a module whose entire style is that a
  claim is measured before it is written. Fix: scope the sentence the way
  `query_cost` already scopes it — "never raises on absence" — and change
  nothing else. It belongs to R11, which opens this region for the renderer
  anyway. OPEN.

Done: R-0330 — RESOLVED at the R11 gate. Verified against the disk and the behaviour, not the report: `grep -c 'READ-ONLY, never raises\.' packages/orchestration/token_ledger.py` prints 0, and the scoped sentence counts 2 — `query_cost`'s own at :1004 and `query_segment_shares`'s at :1098. Two is the CORRECT value, not a miscount: the fix makes the two docstrings agree, it does not make one of them unique. `git show --numstat a74e0668` changes exactly one line of one file. The claim is now true of the behaviour it describes — both functions still raise `ValueError` from `_resolve_ledger_path` when given neither `project_id` nor `path`, and neither raises on a ledger that is merely absent. The R11 round as a whole is PASS. The reviewer re-ran every gate itself: cmp exit 0 with sha256 431da8edba356a9521f58fec5be40f182cd7223addac54f1895a7799034dba74 over both copies, `wc -lc` 449 20234, ruff `All checks passed!`, the import exit 0, `10 passed` and `99 passed` and canary `42 passed` (151 in one run), `wc -l .agent/plan.md` 46, an empty porcelain, and 0/0 against origin. The authored C3 slice was compared DISK TO DISK against the applied file — 315 lines each, byte-identical — rather than against a reviewer retype, which is the R-0147 class this project has paid for before. Both mutation probes were RE-RUN INDEPENDENTLY in the reviewer's own disposable worktree rather than accepted from the handback: neutering `_same_question` fails exactly `test_a_mismatched_pair_is_refused_by_both_renderers` and nothing else, and changing `_figure`'s None branch to `return "0"` fails exactly `test_an_unmeasured_figure_prints_the_word_and_never_a_zero`; the worktree was removed and pruned with `git worktree list` left showing one line. The worker's fixture-design note was CHECKED rather than believed, and it is correct: rendering the DEFAULT pair under the second mutation still prints the word, from the "PARTLY UNMEASURED" sentence, so the fully-measured total in that one test is what makes the probe discriminating instead of decorative. That is a worker catch the block did not order, and it improved the round.

- R-0331 — Low — reviewer block self-contradiction, self-registered. The R11
  block's "Change:" clause named SEVEN paths and said "nothing else", while its
  own "Constraints:" clause ordered a `Landed: R-0330` line into an EIGHTH,
  `.agent/live_review.md`. The two halves of one block disagreed about that
  block's own change set. The worker resolved it the right way: it wrote the
  line the constraint demanded and listed all eight paths in its handback,
  rather than dropping a mandated write to satisfy a file list. Sixth of the
  reviewer-arithmetic class after R-0282, R-0321, R-0323, R-0324 and R-0327,
  and the first whose two contradicting halves sat inside the SAME block — the
  earlier five were numbers the reviewer never re-derived from a list beside
  them, this one is a list the reviewer never re-derived from its own
  instructions four lines below. The standing checklist
  (`docs/agents/planner_reviewer_prompt.md`) sends the reviewer to the block's
  bytes, to the code it points at, to the file it writes into and to the tests
  that guard that file; it does not yet send the reviewer to the block's own
  other clause. No on-disk fix is possible — the block is committed verbatim by
  design and R11's verdict stands as PASS. Registered so the class stays
  countable rather than forgotten. OPEN.

- R-0332 — Low — `_same_question` guards the filters but not the ledger, so the
  one thing it exists to prevent can still happen. `cost_report.py` refuses a
  pair whose `since` or `job_id` disagree, on the stated ground that publishing
  the breakdown of one period beside the total of another silently answers a
  question nobody asked. Two reports drawn from DIFFERENT LEDGERS with
  identical filters pass that check unexamined, and the result is the same
  defect in a better disguise: a share table from one project rendered under
  another project's total, with no filter mismatch anywhere to betray it. Both
  dataclasses already carry `ledger_path` and `ledger_exists`, so the evidence
  needed to catch it was in hand and simply not read. It is Low because no
  caller exists yet — nothing outside the tests renders a report until T003
  wires the CLI — and that is also precisely why it should close before that
  caller is written rather than after. Reviewer-authoring defect: the guard was
  authored in the R11 block, so this is the R11 slice's own gap, found at its
  own gate. Fixed in R12, which opens that module for the goldens anyway. OPEN.
