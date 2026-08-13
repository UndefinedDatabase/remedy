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

Done: R-0332 — RESOLVED at the R12 gate. Verified against the code and a live probe, not the report: `_same_question` now compares `(ledger_path, ledger_exists)` as well as `(since, job_id)`, and the reviewer re-ran the probe class itself — deleting the whole ledger guard in a disposable worktree fails exactly `test_a_pair_from_two_different_ledgers_is_refused_by_both_renderers` and nothing else, so the test catches the regression rather than passing alongside it. The docstring now states WHY the None/None case is not a hole: `merge_cost_reports` deliberately clears `ledger_path` for a cross-project total, so two merged reports compare equal to each other and to nothing else. The R12 round as a whole is PASS. The reviewer re-ran every gate itself: cmp exit 0 with sha256 a3106079f0a10af038120b60380b35c46ceac247c8e66dbb90de15fde38560ca over both copies, `wc -lc` 276 19049, the live-review counts 0/5/13/1, ruff `All checks passed!` and the import exit 0, `15 passed` and `99 passed` and canary `42 passed` (156 in one run), `wc -l .agent/plan.md` 43, an empty porcelain, 0/0 against origin, and 35 changed paths with no `.remedy-wt/**` among them. Determinism was re-established independently rather than accepted: the fifteen tests were re-run under two separate `--basetemp` roots and passed both times, so the golden bytes do not depend on where the fixture ledger was built. A THIRD probe, of the reviewer's own choosing and not ordered by the block, settled the question a golden pair actually has to answer — whether it binds the ledger or only the renderer: inserting `report.rows = []` into `query_segment_shares` turns BOTH goldens red, so the pair tests the query-to-renderer seam end to end and is not a snapshot of the formatter alone. One ordered-but-absent detail, deliberately NOT registered as a finding: the block offered a `Landed: R-0332` marker if the fix outran its review, and none was written. The marker exists so a session dying between a fix and its gate leaves an unambiguous disk state, and here the reviewer-authored R-0332 entry already said "Fixed in R12" in the same file, so the marker would have restated a fact the record already carried. The worker's one unordered edit is likewise correct and was declared: C4 made the test module's docstring claim "this module reads no ledger" false, and scoping that sentence to the property tests was better than preserving a false claim to keep a diff narrow.

- R-0333 — Low — reviewer red-proof arithmetic, self-registered, second of the
  over-prediction sibling class after R-0328. R12's gate (j) ordered the
  `_share_percent` mutation with the words "Both golden byte-comparisons MUST
  fail." Only the markdown one can. `cost_report_json` renders no percentage at
  all — the share cell is a markdown-only presentation computed over raw ints,
  and the json carries `tokens_estimated` unformatted — so `_share_percent` is
  unreachable from the json path and its golden cannot move when the format
  string does. Measured by the reviewer at the R12 gate: `grep -c '%'` over
  `tests/orchestration/fixtures/cost_report/golden/cost_report.json` prints 0,
  and the re-run mutation gives `2 failed, 13 passed` —
  `test_the_share_column_uses_the_attributed_total_as_its_denominator` and
  `test_the_golden_markdown_matches_the_fixture_ledger`, not the json golden.
  The worker measured both, reported the real numbers, declared the deviation
  and adjusted nothing to reach the ordered count — the correct behaviour, and
  the round paid one declared deviation for a reviewer's arithmetic again.
  Checklist item 5 governs a red-proof's REACHABILITY and item 8 the VALUE a
  gate asserts; this class is the blast RADIUS, and the standing counter-measure
  is the one item 5 already names — order the PROBE, not the colour, whenever
  the mutated branch's reach is not obvious. Here it was not obvious for a
  reason worth recording: the two goldens are rendered from ONE pair of reports
  by two functions that do not share a formatting path, so "the golden pair"
  reads as one artifact and behaves as two. Seventh instance of the
  reviewer-arithmetic family overall, after R-0282, R-0321, R-0323, R-0324,
  R-0327, R-0328 and R-0331. No on-disk fix: the block is committed verbatim by
  design and R12's verdict stands as PASS. OPEN.

Done: R-0333 — REGISTERED, not resolved, and it stays OPEN by construction: the block that carried the wrong prediction is committed verbatim by design, so there is nothing on disk to correct. Recorded here only to close the R13 round that registered it. The R13 round as a whole is PASS. The reviewer re-ran every gate itself: cmp exit 0 with sha256 7e9a5b81683e7eb6a09a1199f8c4b332f0ec04f146acee9b67f4b2d867c716a1 over both copies, `wc -lc` 106 9465, the live-review counts 6 / 14 / 1 / 0 for `^Done:`, `^- R-0`, `^## Steps` and `^Landed:`, `git show --numstat 9d2b638d -- .agent/live_review.md` reporting 28 insertions and ZERO deletions — which is the append-only property measured rather than asserted — `wc -l .agent/plan.md` 42, canary `42 passed`, `15 passed` unmoved by a state-only round, `99 passed`, an empty porcelain, 0/0 against origin, and 36 changed paths with no `.remedy-wt/**` among them. The declared handoff overage (80 lines against the 60-line cap) is ACCEPTED under AGENTS.md DECISION D15: the cause is mandated content, the file names its own real line count, and no section was dropped to meet the cap.

- R-0334 — Low — reviewer block self-contradiction, second instance, recurring
  in the VERY NEXT block after its class was registered. R-0331 recorded that
  the R11 block's "Change:" clause disagreed with its own "Constraints:"
  clause. The R13 delegation then told its worker "Commit 1 saves those bytes
  verbatim to `.agent/authored/f115-r13-1.md`; commit 2 mirrors the identical
  bytes" while the same block's Constraints clause said "C2 is its own commit
  and comes first". Two clauses of one instruction ordered two different commit
  sequences. The worker resolved it correctly and by the governing rule rather
  than by proximity: it landed the findings commit first
  (`9d2b638d`, before `4b149bfd` and `ab1b7e9b`), which is what
  docs/agents/planner_reviewer_prompt.md §4 item 4 requires — findings persist
  FIRST so nothing is lost if a session dies — and the block-save ordinals were
  the throwaway half. What makes this worth its own id rather than a tally mark
  under R-0331 is the interval: the class was registered, its lesson written
  out at length, and it recurred in the next block the same reviewer authored,
  in the same session. That is evidence the counter-measure is missing rather
  than merely unapplied. The gap is nameable: the standing pre-emission
  checklist sends the reviewer to the block's own bytes (items 1-4), to the
  code it points at (item 5), to the file it writes into (item 6), to the tests
  guarding that file (item 7) and to the code producing a gated value (item 8) —
  five different places, and not one of them is the block's own OTHER clause.
  Both instances are the same shape: a clause written early and a clause
  written late, never read against each other. The remedy a later round should
  weigh is a ninth checklist item — read the Change clause, the Constraints
  clause and the ordering statements against one another as a final pass — and
  it belongs to whichever round next has a legitimate reason to open
  `docs/agents/planner_reviewer_prompt.md`, since AGENTS.md bars mixing an
  unrelated doc change into a feature branch. Registered here so the pair is
  countable and the counter-measure is findable when that round comes. Eighth
  of the reviewer-arithmetic and self-contradiction family after R-0282,
  R-0321, R-0323, R-0324, R-0327, R-0328, R-0331 and R-0333. No on-disk fix.
  OPEN.

Done: R-0334 — REGISTERED, not resolved, and it stays OPEN by construction: the block that carried the contradiction is committed verbatim by design, so there is nothing on disk to correct. Recorded here to close the R14 round that registered it. The R14 round as a whole is PASS, and this gate was written by a NEW session's reviewer that re-ran every value itself rather than reading them out of the handoff: `cmp .agent/authored/f115-r14-1.md .agent/last_block.md` exit 0 with sha256 460cbfd6ec9814ea577aa907f02b0e8bc6fbf1463270985b62456508bba6c5ad over both copies, `wc -lc .agent/last_block.md` 112 8551, the live-review counts 7 / 15 / 1 / 0 for `^Done:`, `^- R-0`, `^## Steps` and `^Landed:`, `git show --numstat 24e6fb62` reporting 35 insertions and ZERO deletions, `git log --oneline 954d0ea2..HEAD` listing `24e6fb62` as the OLDEST of the four so the findings commit did land first, `git diff --name-only 954d0ea2..HEAD` naming five paths all under `.agent/`, `wc -l .agent/plan.md` 42, canary `pytest tests/cli/test_golden_path.py -q` 42 passed, `pytest tests/orchestration/test_cost_report.py -q` 15 passed, an empty `git status --porcelain`, 0 0 against origin, and 37 changed paths since 0d6c97aa with no `remedy-wt` among them. The declared handoff overage — 85 lines against the 60-line cap — is ACCEPTED under AGENTS.md DECISION D15: the cause is mandated content, the file names its own real line count, and no section was dropped.

- R-0335 — Low — the R14 handoff claimed the §4 item-13 branch terminator for a round that ended a SESSION, not a branch. Item 13 excuses the missing on-disk gate entry of the LAST round of a BRANCH, because the round that would record that verdict is the round being recorded. R14 ended neither the branch nor the feature: no PR exists, T003 was unstarted, and the handoff's own "Resume here" section says the next session continues on THIS SAME branch. The consequence is not cosmetic. `.agent/live_review.md` is append-only and durable; `.agent/handoff.md` is REWRITTEN at every handback. R14's verdict lived only in the file that the very next handback overwrites, so a session that resumed and handed back would have erased the only record that R14 was ever reviewed — the exact loss the findings-first rule of §4 item 4 exists to prevent, arriving through the one door item 13 holds open. The fix is the paragraph above: this round's findings-first commit writes the R14 gate entry where it belongs, and the entry states that its values were re-measured rather than copied. The rule to carry forward: item 13's terminator is claimable only when the round really is the last of the BRANCH — a PR exists, or is created in that same round — and a session that merely runs out of budget records its verdict in `.agent/live_review.md` like any other round. Ninth of the reviewer-arithmetic and self-contradiction family after R-0282, R-0321, R-0323, R-0324, R-0327, R-0328, R-0331, R-0333 and R-0334. No source fix. OPEN.

Done: R-0335 — RESOLVED at the R15 gate, and resolved in the only way it could be: the R14 verdict it said was missing from disk now IS on disk, written by R15's findings-first commit `f77554bf` and re-measured rather than copied out of the handoff. The R15 round as a whole is PASS. The reviewer re-ran every gate itself: `cmp .agent/authored/f115-r15-1.md .agent/last_block.md` exit 0 — the reviewer's sandbox allows `cmp` even though the worker's refused it, so the worker's sha256-plus-byte-compare substitute was corroborated by the primary proof rather than merely accepted — with sha256 `e3a1ea5706f77fccdb2953ab1db9c35a32cf493c598a6981cb4bc02d05d5d39b` over both copies, `wc -lc` 251 18389, the live-review counts 8 / 16 / 1 / 0, `git show --numstat f77554bf` 4 insertions and ZERO deletions, C1 the oldest commit of `5c7f5159..HEAD`, ruff `All checks passed!` over all four files, 119 passed against a 119 baseline of 114 plus five new tests, 83 passed over the canary and the untouched CLI cost tests, `wc -l .agent/plan.md` 43, an empty porcelain, 0 0 against origin, and 38 changed paths with no `remedy-wt` among them. The three authored slices were compared DISK TO DISK against the committed `.agent/authored/f115-r15-1.md` rather than against a reviewer retype — 43 of 43 plan lines, 39 decision lines, 3 live-review lines, all byte-identical — which is the R-0147 class this project has paid for before. Both declared deviations are ACCEPTED: refreshing the two `Public API::` signature lines and the test-module docstring was right, because leaving them would have left a false claim on disk beside a changed signature, and the gate (d) json number was the reviewer's error and not the worker's, registered below. A THIRD probe of the reviewer's own choosing, which the block did not order, settled the question the ordered probes could not: deleting the `until` clause only proves the filter is WIRED, while flipping `ts_utc < ?` to `ts_utc <= ?` proves it is HALF-OPEN, which is the whole content of DECISION F115 D5. That mutation fails exactly `test_a_call_at_exactly_until_is_out_while_one_at_exactly_since_is_in`, `test_the_merge_carries_the_period_end_of_its_inputs` and `test_until_narrows_the_shares_exactly_as_it_narrows_the_cost` and nothing else, so the three new tests bind the boundary reading and not merely the presence of a parameter. The probe ran in a disposable worktree under `.remedy-wt/`, which was removed and pruned; `git worktree list` shows one line.

- R-0336 — Low — reviewer gate arithmetic, tenth of its class, self-registered. R15's gate (d) predicted that the golden `cost_report.json` would move by `2 1`: one changed `report_version` line plus one added `"until"` line. The real diff is `3 2`. The prediction is not merely off, it is arithmetically unreachable, and the reason is a fact about the format rather than about the change: `json.dumps(sort_keys=True)` placed the new `"until"` key AFTER `"timezone"`, which is the last key of the `filters` object, so the `"timezone": "UTC"` line had to gain a trailing comma. Git counts that as one deletion plus one addition on top of the added line. The worker was right, did not stop the round on it, said plainly that the prediction forgot the comma, and proved by reading the diff that no figure, bucket or segment row had moved — which is exactly the judgement gate (d)'s STOP clause exists to invite rather than to suppress. What makes this its own id rather than a tally mark under R-0327 is that it is a NEW subclass. The standing pre-emission checklist's item 8 sends the reviewer to the code that PRODUCES a gated value, and the reviewer did go there: `sort_keys=True` was read, and the alphabetical position of `until` after `timezone` was derived correctly. What went unread is the SERIALISER'S PUNCTUATION — that a key appended after the last one perturbs the line before it. Item 8 covers the value; nothing covers the FORMAT the value is embedded in. The counter-measure is already applied in the next block rather than deferred: R16's gate (d) orders NO line-count prediction at all and replaces it with a structural proof — load both goldens and assert that every DATA key is equal, so the gate constrains what actually matters (that no figure moved) instead of a line count the reviewer keeps mis-deriving. That is the general repair for this family: when a gate's value depends on a formatter, gate the SEMANTICS and report the arithmetic, never predict the arithmetic. Tenth of the reviewer-arithmetic and self-contradiction family after R-0282, R-0321, R-0323, R-0324, R-0327, R-0328, R-0331, R-0333, R-0334 and R-0335. No source fix. OPEN.

Done: R-0336 — REGISTERED, not resolved, and it stays OPEN by construction: the block that carried the wrong prediction is committed verbatim by design, so there is nothing on disk to correct. Its counter-measure, however, was applied immediately rather than deferred, and it worked: R16's gate (d) predicted no line count at all and ordered a structural proof instead, the worker returned real numstats of `14 1` and `4 0` together with a key-by-key comparison, and the reviewer re-ran that comparison independently — `buckets`, `segments`, `total`, `label`, `filters`, `ledger_exists` and `note` all equal, added keys exactly `['comparison']`, removed none, changed exactly `['report_version']` 2 to 3. No figure, bucket or segment row moved. The R16 round as a whole is PASS. The reviewer re-ran every gate itself: `cmp .agent/authored/f115-r16-1.md .agent/last_block.md` exit 0 — again the reviewer's sandbox allows `cmp` where the worker's refuses it, so the worker's sha256-plus-byte-compare substitute was corroborated by the primary proof rather than accepted — with sha256 `24984348f53494604bcbf924b9b91238a9d0c53b33faadf53f71d724ce7b009b` over both copies, `wc -lc` 298 23248, the live-review counts 9 / 17 / 1 / 0, `git show --numstat aa1a6cfb` 4 insertions and ZERO deletions, C1 the oldest commit of `6752841a..HEAD`, ruff `All checks passed!` over all four files, 134 passed against a 119 baseline, 83 passed over the canary and the untouched CLI cost tests, `wc -l .agent/plan.md` 43, an empty porcelain, 0 0 against origin, and 39 changed paths with no `remedy-wt` among them. Both authored slices were compared DISK TO DISK against the committed `.agent/authored/f115-r16-1.md` — 43 of 43 plan lines and 44 decision lines, byte-identical. The C5 deviation is ACCEPTED and is an improvement the block did not ask for: a comparison that does not name its own baseline is a number the reader cannot check against anything, so the `Previous period: since=… until=… · N call(s).` provenance line belongs there. A PROBE of the reviewer's own choosing settled what the two ordered probes could not. P1 removed the subtraction, which only proves the window is displaced; neither probe touched the load-bearing claim of DECISION F115 D6 — that the prior window's `until` is the caller's own `since` STRING and never a re-serialisation of it. Replacing `until=since` with `until=parsed_since.isoformat()` in a disposable worktree fails exactly `TestPriorReportPeriod::test_the_prior_window_of_a_bare_date_pair` and `TestPriorReportPeriod::test_the_prior_until_is_the_original_since_string_byte_for_byte`, and nothing else, so the byte-reuse rule is pinned by a test named for it rather than merely described in a docstring. The worktree was removed and pruned; `git worktree list` shows one line. One inaccuracy is recorded here WITHOUT being registered as a finding, because it moved no evidence: the R16 handback attributed the json golden's single deleted line to a trailing comma gained by the `buckets` array, when the diff shows that line unchanged and the deletion is simply the `report_version` line being rewritten. The number reported was correct, the structural proof was correct and independently reproduced, and the wrong aside sits in a handback sentence rather than in a gate value — registering it would cost a round more than the error costs the record.

- R-0337 — Low — a mutation probe whose IMPORT PATH is not proven is not a probe. R17's ordered probe mutated `apps/cli/commands/stats_ledger_cmd.py` inside a disposable worktree, but the worker's sandbox refused `cd`, so pytest was invoked from the PRIMARY checkout against the worktree's test path. That arrangement does not establish which copy of `apps/` was imported: the repo root carries a `conftest.py` and lands on `sys.path`, so the unmutated primary module was a live candidate, and a probe that silently exercises unmutated code reports GREEN and is read as "the test does not catch this" when the truth is "the test was never run against the mutation". Here the conclusion happened to be sound — the run went RED, and only mutated code can turn a passing test red, so the mutated copy demonstrably was the one imported — and the reviewer re-ran the probe from INSIDE the worktree and reproduced exactly `TestPriorPeriodComparison::test_a_job_filter_narrows_the_prior_query_too` and nothing else. The finding is the METHOD, not this result. A red outcome is self-proving; a GREEN one under the same arrangement would have proved nothing at all, and green is the outcome a probe most needs to be able to trust, because green is what retires a suspicion. The counter-measure is cheap and does not need `cd`: the probe asserts its own provenance by printing the imported module's `__file__` and confirming the path lies under the worktree, before reading anything into the colour. G5 was NOT breached — the mutation stayed inside the worktree and the primary checkout's `git status --porcelain` was empty throughout — so this is a proof-strength finding and not a safety one. First of its class. No source fix. OPEN.

Done: R-0337 — REGISTERED, not resolved, and it stays OPEN by construction: it names a method to apply in future rounds, and there is nothing on disk to correct. Recorded here to close the R17 round that registered it. The R17 round as a whole is PASS. The reviewer re-ran every gate itself rather than reading the handback: `cmp .agent/authored/f115-r17-1.md .agent/last_block.md` exit 0 with sha256 `86e36a908de1a25dd126a96849407636fb952d8e39e4a87407ea0ab4502c70a9` over both copies, `wc -lc` 228 17476, the live-review counts 10 / 17 / 1 / 0, `git show --numstat 7899fdb0` 2 insertions and ZERO deletions with C1 the oldest commit of `aa7ad8df..HEAD`, ruff `All checks passed!` over all three touched files, 93 passed across `test_stats_report.py`, `test_stats_cost.py` and the canary — 10 plus 41 plus 42, so the new command's tests are additive and neither the CLI cost view nor the canary moved — 505 passed across the catalog and grouped-CLI contract tests against a 505 baseline, `wc -l .agent/plan.md` 41, an empty porcelain, 0 0 against origin, and 43 changed paths with no `remedy-wt` among them. The change set is exactly the eight paths the block declared. Both authored slices were compared DISK TO DISK against the committed `.agent/authored/f115-r17-1.md` — 41 of 41 plan lines and the single live-review paragraph, byte-identical. Both declared deviations are ACCEPTED: the module docstring said "Three commands" and never named `stats cache`, so adding a fifth under a false count would have left a wrong claim on disk beside new code, and the four registration tests are the only honest way to meet a gate that ordered the wiring proven "the way the suite does" while the `remedy` binary itself is refused by this sandbox. The catalog entry states the absence of `--all-projects` in its DESCRIPTION rather than only in a comment, which is what `remedy stats --help` prints, and that is the AGENTS.md rule about documenting a deliberate absence where a reader will search for it.

- R-0338 — Medium — the R18 guide states a false attribution, and the reviewer wrote it. `docs/guides/cost-report-user-guide-v0.md` tells a reader that the per-role limit is already visible in the existing CLI: "The existing `remedy stats cost` view already prints that limit in its own output." It does not. `_ROLE_LIMIT_NOTE` (`apps/cli/commands/stats_ledger_cmd.py:373`) has exactly two use sites, `_cache_payload:436` and `_render_cache_human:489`, and both belong to `remedy stats cache`; `_render_cost_human` (lines 236-304) never mentions role at all, and `grep -c role packages/orchestration/cost_report.py` is 1 — a comment about a NULL group column, not the note. So the sentence sends a reader to a command that will not show them the thing it promises, and it also hides the sharper fact: `remedy stats report` itself never prints the limit, which is why the guide has to state it in prose. The true sentence is `remedy stats cache --by role`. This is a reviewer-authoring defect of the R-0325/R-0326 class — authored text applied verbatim by a worker who was explicitly told to stop on a false claim — but it is Medium rather than Low because unlike those two it LANDED, on a user-facing page, and a doc that misdirects a reader is worse than a doc that omits. The worker's own claim-verification pass did check the note: it reported "`_ROLE_LIMIT_NOTE` at :373, printed at line 489 when `report.by == 'role'`" — true line, wrong owner, because it read the line and not the function the line sits in. That is the standing gate-scope blind spot in miniature: existence was verified, attribution was not, and only the reviewer's own probe closed the gap. The counter-measure for the next block of this class: when authored prose names a COMMAND as the source of an output string, the gate must resolve the string to its enclosing function and name that function, never just grep the constant. Fix in the next round: replace the sentence with the `stats cache` reading and say plainly that `stats report` does not print the note. OPEN.

Gate: R18 — PASS WITH RISKS (.agent/review_protocol.md, verdict table: only Medium/Low open, documented as a known risk). This entry is written by the session that reviewed the round rather than by the next one, because `.agent/STOP` appeared during R18's final gate run and R-0335 forbids leaving a reviewed round's verdict in a file the next handback overwrites. The reviewer re-ran every gate itself rather than reading the handback. `cmp .agent/authored/f115-r18-1.md .agent/last_block.md` exit 0 with sha256 `2a93345b696dffc6768ac45ab5bcbb7287b6b0e154ca203bfd1cbb9efad17940` over both copies and `wc -lc` 350 19149. The guide's fenced example is BYTE-IDENTICAL to `tests/orchestration/fixtures/cost_report/golden/cost_report.md` — 30 lines each, sha256 `ba48c81cda785847647e01de1dff12dd9bae5a6abf5eac426b272ad057da138d` over both — and SLICE A of the block equals the committed guide byte for byte, so the doc was applied and not retyped. The ordered `diff <(awk ...)` was refused by the worker's sandbox for process substitution; the worker replicated the same state machine in python and the reviewer reproduced the comparison a third way, in-process, without writing a file. The catalog entry's args are `['--since', '--until', '--job', '--by', '--label', '--project', '--json']` with `--all-projects` absent, matching the guide's flag list exactly; the export is named `CATALOG`, not `COMMAND_CATALOG` as the block's gate (d) guessed, and the worker found and reported the real name instead of reporting a failure. The golden json's top-level keys are the ten the guide lists in the spelling it lists them, `report_version` 3 and `unmeasured_notation` `'null'`. `COST_DEFAULT_LABEL = "(unlabelled)"` at `cost_report.py:64`, as the guide states. `grep -c cost-report-user-guide-v0.md docs/README.md` is 2 and C4's numstat is `2 0`, so both index rows are append-shaped with nothing else in that file touched. `tests/docs/ -q` 294 passed against a 294 baseline; canary 42 passed against 42; and `test_cost_report.py` plus `test_stats_report.py` 32 passed — the run that matters most here, because it is what binds the golden to the live renderer and therefore makes the guide's example a real rendering rather than a plausible one. `wc -l .agent/plan.md` 42, `0 0` against origin, no `remedy-wt` path in the change set, `git worktree list` one line. The change set is exactly the six paths the block declared, and `.agent/live_review.md` is correctly absent from it: R17's `Done: R-0337` was already on disk at `0fa1e40a`, so R18 owed no findings-first commit and the block said so in advance rather than leaving the absence to be read as a miss. `git status --porcelain` is NOT empty — it carries exactly `?? .agent/STOP`, the operator signal that ended the session — and that is the one gate value the round could not meet, correctly reported rather than routed around, exactly as at the R10 gate. Two facts belong in this entry beyond the values. First, the worker checked the guide's substantive claims against source BEFORE committing and reported the check; that pass is why only one claim was wrong, and it is worth more than the round it cost nothing. Second, the one it missed is R-0338 above, found by a reviewer probe the block did not order: resolving `_ROLE_LIMIT_NOTE`'s use sites to their enclosing functions rather than to their line numbers. The round is PASS WITH RISKS and not FAIL because no block condition of §4 item 5 is met — no fabricated data, no unverified completion claim, no silent scope change, and the defect originates in reviewer-authored text rather than in the worker's execution of it.
