STEP F036 R2 — T002'S FIRST HALF: the model-written tour through the summary role, the no-new-claims check, the honest first stop and the labelled fallback

GOAL
Round 1 passed. Book its verdict and record DECISION F036 D3, then add generation to
`packages/orchestration/result_tour.py`: one source text of the job's records, a prompt built from
it and the allowed anchors, a structured call through an injected call function, a check that
drops every model-written stop stating what the records do not hold, the mechanical tour's first
stop always kept first, and the mechanical tour as the labelled fallback. Add `tour_call_fn()`
for the `summary` role and inventory that call site. The module stays unwired: no file is written,
nothing calls it, and no report, command, event name or browser code changes this round.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code and its tests yourself against S1 to S7 below. Only the `.agent/` records travel as
payloads. Read DECISION F036 D3 in the booking diff before you write code: it is the design this
specification implements. Before you write anything, read whole:
`packages/orchestration/result_tour.py` as round 1 left it; `generate_artifact_summary`,
`_fallback_summary` and `summary_call_fn` in `packages/orchestration/artifact_summary.py`;
`run_structured_call` and `StructuredOutcome` in `packages/orchestration/structured_outputs.py`;
`make_structured_call_fn` in `packages/orchestration/intake.py`; `classify`, `FailureSignals`
and `FailureClass` in `packages/orchestration/failure_postmortem.py`; `ROLE_CONFIG_CALL_SITES` in
`packages/orchestration/model_routing.py`; `TestTheCallSiteInventoryIsChecked` in
`tests/orchestration/test_model_routing.py`; `_no_live_ollama_reach` in `tests/conftest.py`; the
`TaskEntry` fields `title`, `status` and `acceptance` in `packages/orchestration/pingpong_job.py`;
and how `tests/orchestration/test_artifact_summaries.py` stubs a call function.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f036-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f036-r2/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f036-r1-dry/`, `.remedy-wt/f036-r1-sim/`, `.remedy-wt/f036-r2-dry/`,
  `.remedy-wt/f036-r2-sim/`       The reviewer's trees; do not touch them.
  `.remedy-wt/f036-r1-src/`, `.remedy-wt/f036-r2-src/`, `.remedy-wt/f036-review/`  The
                                  reviewer's scripts; do not touch them.
  `.remedy-wt/f036-r2-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Set `REMEDY_DATA_DIR` inside tests with `monkeypatch.setenv`, never on a command line.
Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f036-guided-result-tour`, and `git log --oneline -1` must read `44965328`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f036-r2/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f036-r2-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| booking.diff | 73 | 12245 | 4f1d09fd1bcb931e4c7bbcc170d79562566c368533cd483c5f8b2f70188b533f |
| plan.md | 29 | 992 | ff10018e44efab6b5599bff119a22a5059ecb1cfff25fc380f35cb7373bd5474 |

`plan.md` is a REWRITE of `.agent/plan.md`. `booking.diff` goes on with `git apply`; the reviewer
generated it with `git diff HEAD` from a tree at `44965328`. It appends round 1's gate entry to
`.agent/live_review.md` and DECISION F036 D3 to `.agent/decisions.md`.

THE SPECIFICATION. No `except Exception` anywhere, and no new `# noqa: BLE001`. Every addition
goes into `packages/orchestration/result_tour.py`, which still writes no file and reads no clock.
S1 CONSTANTS AND SCHEMA. `GENERATED_TOUR_SCHEMA_V = "generated_tour_v1"`,
   `TOUR_GENERATOR_SUMMARY_ROLE = "summary-role"`, `TOUR_NO_SOUND_STOPS = "no_sound_stops"`, and
   `TOUR_CLAIM_DENYLIST`, a tuple of lower-case words holding at least `seamless`, `seamlessly`,
   `robust`, `flawless`, `perfect`, `perfectly`, `guaranteed`, `bulletproof`, `effortless`,
   `blazing`, `world-class`, `best-in-class`, `state-of-the-art`, `cutting-edge`,
   `production-ready` and `enterprise-grade`. Pydantic models `GeneratedTourAnchor` (`kind`,
   `ref`), `GeneratedTourStop` (`title`, `body`, `anchor`) and `GeneratedTourContent` (`stops`,
   a list of stops) with `SCHEMA_V: ClassVar[str] = GENERATED_TOUR_SCHEMA_V`, and no length or
   value constraint of their own: the resolver judges the stops.
S2 THE SOURCE TEXT. `tour_source_text(job, sources, context) -> str`, one fact per line, in this
   order: `state: <state or NOT_RECORDED>`; `terminal status: …`, `stop reason: …` and
   `mission: …`, each only when non-empty; for every task of `job.tasks`,
   `task <task_id>: <title>; status <status>`, followed by `; acceptance: <acceptance>` when that
   is non-empty; for every diff file, `changed file <path> (+<added> −<deleted>)`; for every
   evidence file, `evidence file <name>`; for every run command, `command <command>`; and, when
   `sources.dod_released is not None`, `Definition of Done: <the body of stop (d)>` followed by
   `check <check_id> (<kind>): <status>` for each check. The minus sign is the module's U+2212.
S3 NO NEW CLAIMS. `tour_claim_problems(stop, source_text) -> list[str]` reads the stop's title
   and body together and answers one readable line per breach: a number — a run of digits between
   word boundaries — that is not such a number of the source text; a span between backticks that
   the source text does not contain; a path — a token holding "/" between word characters, or a
   word, a dot and a letter-only extension of one to five letters — that the source text does
   not contain, read after the backtick spans are removed; and a word of `TOUR_CLAIM_DENYLIST`
   found in the lower-cased text as a whole word, hyphens included. `[]` for a clean stop.
S4 THE PROMPT. `build_tour_prompt(source_text, context) -> str` holds the source text verbatim,
   then one line per allowed anchor, `<kind> <ref>`, for every task id, diff path, evidence file
   and run command of the context, then the rules: at most `MAX_TOUR_STOPS - 1` stops, a title of
   at most `TOUR_TITLE_MAX_CHARS` characters on one line, a body of at most
   `TOUR_BODY_MAX_CHARS`, every anchor copied from the list, and every sentence restating the
   records above and adding no claim.
S5 THE GENERATION. `PROVIDER_CALL_ERRORS` is a tuple built once at import: `OSError`,
   `RuntimeError`, `ValueError` and `ImportError`, plus `ollama.RequestError` and
   `ollama.ResponseError` when `ollama` imports and `httpx.HTTPError` when `httpx` imports.
   `generate_result_tour(job, call_fn=None, *, on_call=None) -> dict` reads the context and
   `build_report_sources(job)` once, then:
   (a) `call_fn is None` → the mechanical tour exactly as `build_fallback_tour` answers it.
   (b) Otherwise `run_structured_call(GeneratedTourContent, build_tour_prompt(...), call_fn,
       on_call=on_call, allow_parse_retry=True)`. An exception of `PROVIDER_CALL_ERRORS` → the
       mechanical tour with generator `fallback:<classify(FailureSignals(exception=exc))
       .failure_class.value>`. An outcome that is not ok → the mechanical tour with generator
       `fallback:<the class classify gives for FailureSignals(error_class=outcome.error_class,
       error_text=outcome.hint)>`.
   (c) An ok outcome: each model stop as a plain dict; a stop with any `tour_claim_problems`
       line is dropped with them joined by "; " as its reason, keeping its title; the rest go to
       `resolve_tour_stops` behind the mechanical tour's FIRST stop, `fallback_tour_stops(...)[0]`.
       When fewer than two stops are kept, the answer is the mechanical tour with generator
       `fallback:no_sound_stops`. Otherwise the kept stops with generator `summary-role`.
   In every case the answer has the shape of S7 of round 1, `tour_problems` of it is `[]`, and
   `dropped` lists every drop of every stage in the order it happened: claim drops, then the
   resolver's, then, on a fallback after (c), the mechanical tour's own.
S6 THE CALL FUNCTION. `tour_call_fn()` answers
   `make_structured_call_fn(GeneratedTourContent, model=resolve_role_config("summary").model)`,
   `None` when that factory answers `None`. `ROLE_CONFIG_CALL_SITES` in
   `packages/orchestration/model_routing.py` gains `("packages/orchestration/result_tour.py",
   "summary")` directly after the `pingpong_job.py` entry, and
   `test_most_call_sites_still_pass_no_role_literal` in `tests/orchestration/test_model_routing.py`
   changes `== 9` to `== 10` and `== 4` to `== 5`, its comment naming ten sites, five literal
   roles and F036 T002's `summary`. Nothing else in either file changes.
S7 UNCHANGED. Round 1's functions keep their behaviour, and `ALLOWED_UNWIRED` keeps the module.

THE TESTS — appended to `tests/orchestration/test_result_tour.py`, with the round-1 fixtures and
a call function stubbed as `def fake(prompt, attempt): return <json text>`. At least, one test
each: no call function gives exactly `build_fallback_tour`'s answer; a model answer of three stops
that restate the records gives generator `summary-role` and the mechanical first stop followed by
those three; a model stop stating a number the records lack, one quoting a backtick span they lack,
one naming a path they lack, and one saying "Seamlessly" are each dropped with a reason naming the
number, the span, the path and the word; a model stop anchored to an unknown task is dropped by the
resolver; nine sound model stops keep eight stops in all and drop the rest past the ceiling; a
model answer whose every stop is dropped gives `fallback:no_sound_stops` with those drops listed;
a call function raising `RuntimeError`, one raising `OSError` and one answering unparseable text
each give a generator starting `fallback:` and never raise; the unparseable one is called twice
and `on_call` fires once per call; the prompt holds the source text, every allowed anchor line and
the numeral 7; the source text lists a task's acceptance and each changed file with its counts;
`tour_call_fn` asks `resolve_role_config` for `summary` and hands `GeneratedTourContent` to
`make_structured_call_fn` (spy both with `monkeypatch`), and answers `None` under the suite's
refused Ollama; and `tour_problems` of every answer above is `[]`.

BUNDLE — the commits are C1, C2, C3, C4, C5 and C6, in this order.

C1 — copy this block and the payloads
  `.agent/authored/f036-r2-block.md` := this block, `.agent/authored/f036-r2-booking.diff` :=
  booking.diff and `.agent/authored/f036-r2-plan.md` := plan.md, by `shutil.copyfile`.
  Subject: `F036 R2 C1: copy round 2 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 102. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C2 — THE BOOKING, the round's first substantive commit: `git apply` booking.diff, then rewrite
  `.agent/plan.md` := plan.md.
  Subject: `F036 R2 C2: book round 1, record DECISION F036 D3`
  Expected by `git show --numstat`: 55/0 decisions.md, 2/0 live_review.md, 6/6 plan.md.

C3 — THE CODE AND THE INVENTORY: `packages/orchestration/result_tour.py`,
  `packages/orchestration/model_routing.py` and `tests/orchestration/test_model_routing.py`.
  Subject: `F036 R2 C3: generate the result tour through the summary role, no new claims`

C4 — THE TESTS: `tests/orchestration/test_result_tour.py`.
  Subject: `F036 R2 C4: test the generated tour, its claim check and its fallbacks`

C5 — THE TOOL: your mutation tool (G5) saved as `.agent/authored/f036-r2-mutations.py`.
  Subject: `F036 R2 C5: add the round 2 mutation tool`

C6 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F036 R2 C6: rewrite handoff for round 2`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; split a commit that
   would reach it into parts with their own subjects (C3a and C3b, C4a and C4b), and say so.
3. The round's whole tracked path set is: the `.agent/authored/f036-r2-*` copies and tool,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/result_tour.py`, `packages/orchestration/model_routing.py`,
   `tests/orchestration/test_model_routing.py`, `tests/orchestration/test_result_tour.py`, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 44965328` at the
   branch tip after C6. Do NOT touch anything under `apps/`, any other file under `packages/`,
   `tests/test_no_orphan_modules.py`, `tests/orchestration/import_reachability_allowlist.txt`,
   `tests/conftest.py`, `.agent/context.md`, `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `README.md` or anything under `docs/`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C6, and the correction is declared. An
   EXISTING test that goes red is never edited to pass, except the two numerals S6 orders; report
   it and stop.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that gate's last action, and `git worktree list | wc -l` is
   reported afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F036's belongs to its closure. No test may reach a live model: every call function in the
   tests is a stub, and the suite's refused Ollama stays in force.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f036-r2-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f036-r2/block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE BOOKING — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree. Report each path beside the hash you read:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2356984 | 3a67422486ec1d0f94283e7dc21be73553ca8017503f2dd83e900055180e3cca |
 | .agent/live_review.md | 313639 | 293c27fdc0d483cfcc5f2b5e610dff576df4c0b50c1da3b7d18cf3a4d6b39212 |
 | .agent/plan.md | 992 | ff10018e44efab6b5599bff119a22a5059ecb1cfff25fc380f35cb7373bd5474 |
 Also: `open_finding_ids` from `scripts/rotate_live_review.py` over the ledger's TEXT at C2,
 which the reviewer read empty; the ledger's last non-empty line at C2 begins
 `Gate: F036 R1 — `; and `git diff --name-only <C1> <C2>` names exactly the paths above.

G3 THE CODE — `python3 -m ruff check packages/orchestration/result_tour.py
 packages/orchestration/model_routing.py tests/orchestration/test_model_routing.py
 tests/orchestration/test_result_tour.py` at C4, with its real exit code. Then report, quoted
 from `git show <C3>`, the whole of `tour_claim_problems`, `PROVIDER_CALL_ERRORS` and its
 builder, and `generate_result_tour`.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_result_tour.py tests/orchestration/test_model_routing.py tests/orchestration/test_orchestrator_model_routing.py tests/orchestration/test_role_config.py tests/orchestration/test_call_modes_agree.py tests/orchestration/test_artifact_summaries.py tests/orchestration/test_structured_outputs.py tests/orchestration/test_intake.py tests/orchestration/test_failure_postmortem.py tests/orchestration/test_run_report.py tests/orchestration/test_job_digest.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_subprocess_timeouts.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/orchestration/test_development_artifact_boundary.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection, serially, in the primary checkout at `44965328` before any
 change, and read `1616 passed, 4 skipped` at real exit code 0, with the 13 round-1 nodes of
 `tests/orchestration/test_result_tour.py` among them. The skips are three in
 `tests/orchestration/test_model_routing.py` covered by a violating fixture and the F252
 quarantine in `tests/test_agent_tooling.py`, and they stay skipped. Report every `SKIPPED` line,
 the node count of `tests/orchestration/test_result_tour.py` by `--collect-only -q`, and account
 for any difference from 1616 plus that count less 13. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — your tool `.agent/authored/f036-r2-mutations.py` takes a worktree path, and
 for each mutation below edits `packages/orchestration/result_tour.py` INSIDE that worktree
 (asserting its FROM text occurs exactly once), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/orchestration/test_result_tour.py` from the worktree's root with that root first on
 `sys.path` after purging its `__pycache__` directories, restores the bytes, and prints one line
 per mutation: its label, the exit code, the failed count and the failing node ids. It runs an
 unmutated control first and last and ends with `restored byte-identical: True` and a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  m1 the claim check ignores numbers;
  m2 the claim check ignores backtick spans;
  m3 the claim check ignores paths;
  m4 the denylist is matched case-sensitively, before lower-casing;
  m5 a generated tour does not put the mechanical first stop first;
  m6 `PROVIDER_CALL_ERRORS` holds no `RuntimeError`;
  m7 a generated tour keeps even one stop, with no fallback for fewer than two;
  m8 a not-ok outcome is labelled `summary-role`;
  m9 `tour_call_fn` binds `GeneratedSummaryContent` from `artifact_summary` instead;
  m10 the structured call is made with `allow_parse_retry=False`.
 Run it: `git worktree add --detach .remedy-wt/f036-r2-mut <C5>`, then
 `python3 -B .agent/authored/f036-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f036-r2-mut`
 and report its whole output. EVERY mutation must be red with at least one failing node; a
 mutation that stays green is reported as green, never papered over, and you then add the test
 that catches it in C4 before C6 and re-run the tool. Then
 `git worktree remove --force .remedy-wt/f036-r2-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C6, C5, C4, C3, C2, C1 and `44965328` in that order
 (more lines if constraint 2 split a commit); `git worktree list | wc -l`, which must equal your
 step 4 reading; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3, C4 and C5 — report what
you measure), every gate's real output and exit code, the authored-text proofs, the item-status
table AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F036, round 2, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2, then T002's second half — `tour.json` stored and versioned at the job terminal, the
command line's tour, and the fixture goldens. State the open-findings count, 0, and the
operator-questions count, 1.
