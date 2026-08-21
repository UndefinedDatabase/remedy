── STEP R16 — F255 Teacher role ───────────────────────────────
Goal:        FINISH T004. Rule the teacher's model seam, build it, and wire it to
             `remedy teach ask` in the SAME round, so the seam has a caller the
             round it is born. R13 left `record_teacher_question` with no caller
             and this plan has carried that as a live risk ever since; shipping a
             second uncalled seam would compound it rather than pay it down.

Bundle:      C0a save this block · C0b mirror it · C1 the plan, FIRST · C2 record
             the R15 verdict · C3 the three rulings · C4 the feature amendment ·
             C5 the seam and its tests · C6 the CLI, the catalog and the pin ·
             C7 the behavioural proofs · C8 the handback, then push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r16.md`
             C0b `.agent/last_block.md`
             C1  `.agent/plan.md`
             C2  `.agent/live_review.md`
             C3  `.agent/decisions.md`
             C4  `docs/roadmap/features/T5_F255.md`
             C5  `packages/orchestration/teacher_model.py` (NEW) and
                 `tests/orchestration/test_teacher_model.py` (NEW)
             C6  `apps/cli/commands/teach_cmd.py`, `apps/cli/command_catalog.py`
                 and `tests/cli/test_teach_cmd.py`
             C7  `tests/cli/test_teach_cmd.py`
             C8  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. These paths are
             PRESENT at the base `2e5b8299` and must stay untouched:
             `packages/orchestration/teacher_spend.py`,
             `packages/orchestration/teacher_qa.py`,
             `packages/orchestration/token_ledger.py`,
             `packages/orchestration/role_config.py`,
             `packages/providers/ollama_planner/provider.py`.

             WHAT C5 BUILDS — `packages/orchestration/teacher_model.py`, the model
             half of Stage 2, ruled by DECISION F255 D8 in slice DECISIONS255.
             Public API, and nothing wider:
             * `TEACHER_TRANSPORTS: tuple[str, ...]` — the provider names the
               teacher can actually call. It holds `ollama` and nothing else,
               because that is the only transport this round builds.
             * `TeacherTransportUnavailable(RuntimeError)` — raised by a transport
               whose dependency is absent or whose call failed.
             * `TeacherReply` — frozen dataclass: `text: str`, `usage:
               TeacherUsage` (reused from `teacher_spend`, never redefined).
             * `TeacherAnswer` — frozen dataclass: `text: str`, `model: str`,
               `refused: bool`, `call_id: str | None`, `billed: bool`.
             * `resolve_teacher_transport(config_file=None) -> tuple[str, str] |
               None` — resolves through `resolve_role_config("teacher",
               config_file=config_file)` and returns `(provider, model)` when the
               provider is in `TEACHER_TRANSPORTS`, else `None`.
             * `ollama_teacher_call(prompt, *, model) -> TeacherReply` — one
               `ollama.Client(host).chat` with a free-text reply and NO schema,
               because a tutor answer is prose. The host comes from the existing
               `ollama.host` config with the same default
               `packages/providers/ollama_planner/provider.py` uses. A missing
               `ollama` package or any call failure raises
               `TeacherTransportUnavailable`. Usage is read from the reply where
               the provider reports it and left as NULL where it does not — never
               defaulted to zero, matching `teacher_spend`'s own rule.
             * `ask_teacher(question, *, events=(), code=None, code_path=None,
               level=DEFAULT_LEVEL, call=None, job_id=None, project_id=None,
               ledger_path=None) -> TeacherAnswer` — the orchestration, in this
               order: build the context with `build_teacher_context`; resolve the
               transport; on `None` return a REFUSAL built by `no_model_refusal`
               naming the resolved provider and model, with `refused=True`,
               `call_id=None`, `billed=False`, and NO ledger row; otherwise render
               with `render_prompt` and call `call` — which defaults to
               `ollama_teacher_call` — and on `TeacherTransportUnavailable` return
               the same shape of refusal, again with NO ledger row; on success
               record exactly ONE row through
               `teacher_spend.record_teacher_question` and return its `call_id`
               with `billed` set from that call's own durability flag.
             A REFUSAL IS NEVER BILLED. There was no model call to pay for, and a
             row recording one would be the fabrication `token_ledger` refuses.
             `call` is the seam: every test injects a fake and NO test opens a
             socket. The module reads no file and writes none of its own.

             WHAT C6 BUILDS — the CLI surface. `_cmd_teach_ask` in
             `apps/cli/commands/teach_cmd.py` takes the question, optional
             `--job-id`, `--level`, `--project` and `--json`; resolves the ledger
             target through `packages.orchestration.project_scope.resolve_scope`
             exactly as `apps/cli/commands/stats_ledger_cmd.py` does; loads run
             events through `load_run_events` when a job id is given and passes
             `()` when it is not; calls `ask_teacher`; and prints the answer, the
             model, the grounding sources it may speak from, and — when the answer
             was not billed — one plain line saying the spend row was not
             recorded. A refusal prints the refusal text and exits 0, because a
             teacher that could fail a run would not be passive. The catalog gains
             ONE `CommandEntry` with `command_id="teach.ask"`, `group_id="teach"`,
             `subcommand="ask"`, `action_class="write_metadata"` per DECISION F255
             D10, `supports_json=True`, and `related=("teach.narrate",)`.
             THE PIN THIS BREAKS, NAMED SO NOBODY DISCOVERS IT AT RUN TIME:
             `tests/cli/test_teach_cmd.py::TestTeachCatalogDeclaration::
             test_the_handler_table_covers_every_declared_teach_command` asserts
             `declared == {"teach.narrate"} == set(COMMAND_HANDLERS)` and goes RED
             the moment `teach.ask` is declared. It is EXTENDED IN THE SAME COMMIT
             as the entry it guards — the T001 precedent — and it keeps asserting
             equality of the two sets rather than being weakened to a subset.
             THAT PIN IS THE ONLY ONE, AND THAT IS A MEASUREMENT RATHER THAN A
             GREP. In a disposable worktree at `2e5b8299` the reviewer added this
             catalog entry and a stub handler and ran
             `tests/test_command_catalog.py`, `tests/cli/test_teach_cmd.py`,
             `tests/test_grouped_cli.py`, `tests/ui_server/test_dashboard_contract.py`,
             `tests/cli/test_golden_path.py`,
             `tests/test_cli_execution_loop_closure.py` and
             `tests/test_test_categories.py`: unmodified they are exit 0 at 701
             passed and 1 skipped, and with the entry added exit 1 at 1 failed and
             701 passed, the single failure being that pin. The worktree was
             removed and `git worktree list` reports the primary checkout alone.

             WHAT C7 BUILDS — the behavioural proofs, in
             `tests/cli/test_teach_cmd.py`, all with an injected fake `call`:
             * READ-ONLY EXCEPT THE LEDGER, BY NAME. `_hash_tree` over the data
               root before and after an ask, with the ledger file and its sqlite
               sidecars EXCLUDED BY AN EXPLICIT NAME FILTER, is unchanged; a
               second assertion states that the excluded set is exactly the paths
               whose name starts with `ledger.sqlite`. Excluding by name is the
               point: a silent exclusion would hide any other write.
             * EXACTLY ONE ROW. After one ask, the ledger holds exactly one row,
               its `role` is `teacher`, its `task_id` is NULL, and
               `query_cost(by="role")` reports a `teacher` bucket distinct from
               the mission roles.
             * A REFUSAL BILLS NOTHING. With a provider outside
               `TEACHER_TRANSPORTS`, the command refuses, names Stage 1, exits 0,
               and the ledger holds ZERO rows.
             * A FAILING TRANSPORT REFUSES. A fake `call` raising
               `TeacherTransportUnavailable` produces a refusal and zero rows.

Constraints:
1. NO SLICE IS EDITED. Every text between the SLICE and END markers is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f255-r16.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r16.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL;
   the reviewer stated the expected digest when it delegated, and that digest
   cannot appear in this file because this file is what it digests.
3. THE PLAN COMES FIRST. Findings R-0377, R-0491 and R-0548 are OPEN and all rule
   that the `.agent/plan.md` update is the FIRST substantive commit of a round
   with substance to record. Only C0a and C0b may precede it.
4. THE THREE APPENDS ARE BLANK-SEPARATED (R-0578): RECORDR15 at C2, DECISIONS255
   at C3 and AMEND255 at C4 are each appended preceded by exactly one blank line.
   This round registers NO finding and resolves NONE: registered stays 183,
   resolved stays 3.
5. RECORDR15 IS SINGLE-PARAGRAPH — the reviewer measured it for an interior blank
   line and found none — so the LAST-UNIT paragraph reading G5 orders is exact for
   it. DECISIONS255 and AMEND255 are MULTI-paragraph, so NO last-unit paragraph
   reading is ordered or owed for either, and none may be reported as if it were:
   the prefix-and-remainder reading is their whole proof (R-0606).
6. THIS ROUND CONTAINS NO FROM/TO PAIR. Every authored text is an APPEND at end of
   file or a full replacement, so no containment reading and no FROM-zero count is
   owed (§4.9, R-0207). The code C5, C6 and C7 build is written by you to the
   specification above; it is NOT authored text and carries no transport proof.
7. THE CODE IS YOURS, THE BEHAVIOUR IS NOT NEGOTIABLE. Write the modules in this
   repository's idiom — the one-line WHY comment above each definition, a module
   docstring naming the feature and the deliberate absences, `from __future__
   import annotations`. Every property the Change section states is a property a
   test must hold you to.
8. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH.
9. NO TEST OPENS A SOCKET AND NO TEST REQUIRES A RUNNING OLLAMA. Every test that
   reaches `ask_teacher` injects `call`. One test asserts the DEFAULT is
   `ollama_teacher_call` by identity, without calling it.
10. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
    handback instead.
11. `git status --porcelain` is EMPTY after every commit. No worktree is created,
    and the primary checkout is never mutated to take a reading — use
    `git show <sha>:<path>`.
12. YOU DO NOT WAIT ON ANY CI RUN, you report no run's conclusion, and you create
    NO pull request: on this project the PR is created by the closure round.

<<<SLICE PLAN255R16
# Plan — F255 Teacher role

Branch: feature/f255-teacher-role, cut from `main` at b35d350b, the merge commit
of pull request #207. No pull request is open for this branch; on this project
the PR is created by the closure round.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
A fourth configured role, `teacher`, that narrates a running mission and answers
operator questions about the operator's own code, and never influences the run.
DONE when passive narration keyed to an enumerated set of ledger events (Stage 1,
deterministic templates, zero tokens) and on-demand Q&A (Stage 2, through the
teacher role's own model) both work, the three grounding sources are never mixed
silently, teacher spend is reported as its own role in the F103 ledger, and the
read-only invariant is proven behaviourally.

## Current Step
R16 FINISHES T004. It rules the teacher's model seam, builds it as
`packages/orchestration/teacher_model.py`, and wires it to `remedy teach ask` in
the SAME round, so the seam has a caller the round it is born — the debt R13 left
and this plan has carried as a risk since.

## Next Steps
1. The INTEGRATION GATE round follows T004 — the full suite, per
   docs/agents/integration_gate.md — because T002, T003 and T004 all touch the
   CLI catalog, which the parser and the help renderer both read.
2. The CLOSURE round follows, per docs/roadmap/STATUS_closure_protocol.md:
   evidence job, fresh review zip, the STATUS line, and the pull request.

## Risks
- THE REFUSAL CONDITION IS NOT "NO MODEL CONFIGURED". `resolve_role_config`
  returns a provider-aware DEFAULT model for every role, so that state is
  unreachable and a test driving it would prove nothing. Stage 2 refuses on NO
  USABLE TRANSPORT instead (DECISION F255 D9).
- `remedy teach ask` WRITES ONE LEDGER ROW, so its read-only proof must exclude
  that file BY NAME (DECISION F255 D10) rather than by silence, or it proves the
  opposite of what it claims.
- R-0607 STAYS OPEN. Only a docs round promoting its rule into the
  docs/agents/planner_reviewer_prompt.md §3 checklist closes it; R16 obeys the
  rule without closing the finding.
<<<END PLAN255R16
<<<SLICE RECORDR15
Gate: R16 — the R15 entry. R15 PASSED with NO finding registered against it: the round did exactly what its block ordered, and every value the handback reported reproduced under the reviewer's own independent measurement rather than being read back from it. R15 was a RECORD round that built nothing, and every gate its block ordered was RE-EXECUTED by the reviewer over `501c08a7..2e5b8299`; every number here is the reviewer's own. THE TRANSPORT HELD IN THE PRIMARY FORM: `.remedy-wt/f255-r15.md`, the committed `.agent/authored/f255-r15.md` at `b720b658` and the committed `.agent/last_block.md` at `ef1b49c2` are byte-EQUAL at sha256 c3b44d7b5613839d85662f7f542799d302b98d9953d868b3063dd3db07c95d3e over 19845 B and 207 lines, the digest stated at delegation. THREE SLICES, a count taken from the reviewer's own ordered extraction of the committed blob and agreeing with the worker's independent count, newline convention NEWLINE-INCLUDED: PLAN255R15 sha256 cb38694ce328a6bb2ffcf30427f400f266952cef50840185a2b2783c648f6ba3 over 2511 B and 43 lines; FIND0607 sha256 26c586d9e6d510ce4b0d19ea1fe97aaebae2f34a53bf2fd17f2bd6bfccea6196 over 1601 B and 1 line; RECORDR14 sha256 55092fad559a9aaed28b451743c8845c6c25f67a60f69caf01ec3932295a7151 over 4703 B and 1 line. THE PLAN LANDED FIRST: `.agent/plan.md` at `f65d0833` byte-equals PLAN255R15 over 2511 B and 43 lines, under the 50-line cap, carrying `## Goal` once, `## Next Steps` once and the F-id F255, and `git log --reverse 501c08a7..2e5b8299` opens b720b658, ef1b49c2, f65d0833, so it is the first commit after the two block-save commits. THE FINDING PERSISTED BEFORE THE VERDICT, which is what §4.4 asks: the `.agent/live_review.md` blob at `501c08a7` is a byte-exact prefix of the blob at `4e3d7a73` whose 1602 B remainder equals one newline followed by FIND0607, the byte after that newline being `-`; and THAT blob is a byte-exact prefix of the blob at `9807f67f` whose 4704 B remainder equals one newline followed by RECORDR14, the byte after that newline being `G`. The independent blank-line paragraph split agrees at both commits: 204 units at `4e3d7a73` whose last unit IS FIND0607, and 205 units at `9807f67f` whose last unit IS RECORDR14, each matching under both newline conventions. THE SETS MOVED BY EXACTLY ONE REGISTRATION AND NOTHING ELSE: 182 registered / 3 resolved / 179 open / 0 line-anchored `Landed:` at `501c08a7`, then 183 / 3 / 180 / 0 at BOTH `4e3d7a73` and `9807f67f`, the second commit adding a `Gate:` paragraph, which is neither kind of line. `R-0607` occurs 0x at `501c08a7`; `Gate: R15 — the R14 entry.` occurs 1x at `9807f67f`, sits last among the fifteen lines beginning `Gate: R`, and all fifteen header keys are distinct — counted LINE-ANCHORED, since the bare prefix `Gate: R15` occurs 3x at `501c08a7` inside the BODY of finding R-0394 as ordinary prose and 0x line-anchored there (R-0584). THE RANGE AND THE HISTORY HOLD: five paths over six single-parent commits, all five under `.agent/`; per-commit insertions 207, 83, 9, 2, 2 and 27, every one under the 500 cap; every `+/-` cell of the handback's `## Commits` table is byte-identical to `git diff --numstat`; all four paths the block named untouched — `packages/orchestration/teacher_spend.py`, `tests/orchestration/test_teacher_spend.py`, `packages/orchestration/token_ledger.py` and `.agent/decisions.md` — are PRESENT at `501c08a7` and ABSENT from the range; and zero lines beginning with the slice or end marker prefixes appear in any written file. R-0607'S OWN RULE WAS OBEYED BY THE VERY BLOCK THAT REGISTERED IT: G8 ordered the state-reader four and the canary, and the reviewer re-ran both SERIALLY in the primary checkout at `2e5b8299` — exit 0 at 160 passed and exit 0 at 42 passed — which is a stronger reading than the handback's, taken at `9807f67f` and one commit short of the branch tip. C4'S OWN REFLOG ENTRY IS MEASURED HERE, which is what R-0494 asks of the next gate: at `2e5b8299` the round has made 6 commits and its reflog entries whose operation prefix reads exactly `commit` number 6, the two being EQUAL, with 0 whose prefix contains amend, reset, rebase or cherry. THE PUSH LANDED: `origin/feature/f255-teacher-role` resolves to `2e5b8299`, the commit the branch holds. THE HANDBACK ITSELF MEASURES CLEAN: 67 lines at `2e5b8299`, inside the 100-line allowance its six-commit table earns, no trailing whitespace on any line, and all seven mandated headings in the order docs/agents/handback_template.md gives them. R-0607 STAYS OPEN: only a docs round that promotes its rule into the docs/agents/planner_reviewer_prompt.md §3 pre-emission checklist closes it, and R16 is not that round — R16 obeys the rule and says so rather than claiming it away.
<<<END RECORDR15
<<<SLICE DECISIONS255
## DECISION F255 D8 — the teacher gets its OWN model transport, because no generic one exists (2026-08-21)

CONTEXT. T004 requires Stage 2 to answer through the teacher role's own model,
and the reviewer measured the provider surface at `2e5b8299` before assuming one
was available. `packages/providers/` holds `claude_agent`, `docker_runtime`,
`mempalace`, `ollama_builder` and `ollama_planner`; every one is role-specific.
The closest thing to a general call is `OllamaPlanner.raw_call`, and it is not
general in either direction: it takes a REQUIRED `schema` and passes it as
`format=`, and it resolves its model, host, temperature and num_predict from the
PLANNER's configuration surface. A teacher answer is prose, not a schema, and
borrowing the planner's configuration would make `teacher.model` decorative.

CHOSEN. Build one narrow transport owned by the teacher, in
`packages/orchestration/teacher_model.py`, behind an INJECTABLE seam: a `call`
parameter defaulting to `ollama_teacher_call`. The transport sends one free-text
chat with no schema, resolves its model through `resolve_role_config("teacher")`
and its host through the existing `ollama.host` config. `TEACHER_TRANSPORTS`
names the providers the teacher can call and holds `ollama` alone, because that
is the only one this round builds. Every test injects the seam, so the suite
never opens a socket and never needs a running Ollama.

ALTERNATIVES CONSIDERED and rejected. Calling `OllamaPlanner.raw_call` with a
permissive schema — rejected because it bills the teacher's question to the
planner's configuration and puts the planner's system prompt in front of a tutor
answer. Adding a generic completion provider under `packages/providers/` —
rejected as a strictly larger change than F255 needs, and one that would outlive
this feature's review; a future feature that needs it can lift this transport.
Refusing all Q&A until such a provider exists — rejected because it would leave
T004's acceptance unreachable and the seam R13 built still uncalled.

CONSEQUENCE. `teacher.model` becomes load-bearing for the first time. A provider
outside `TEACHER_TRANSPORTS` is refused honestly rather than mis-called, which is
the behaviour DECISION F255 D9 defines.

Reverse this decision by deleting this section, deleting
`packages/orchestration/teacher_model.py` and its test, and removing the
`teach.ask` handler and catalog entry.

## DECISION F255 D9 — Stage 2 refuses on NO USABLE TRANSPORT, not on "no model configured" (2026-08-21)

CONTEXT. The feature file's Edge cases say "With no model configured, Stage 2
refuses with an honest message and Stage 1 keeps working". Read against
`packages/orchestration/role_config.py` at `2e5b8299`, that state cannot occur:
`resolve_role_config` fills an unset model from `default_model_for_provider`, and
`DEFAULT_PROVIDER` is `ollama`, so EVERY role resolves to a model whether or not
anyone configured one. A test driving "no model configured" would therefore
assert a branch no configuration reaches — the vacuous gate this project keeps
paying for.

CHOSEN. Keep the honest refusal and re-point its CONDITION at something real.
Stage 2 refuses when the resolved provider is not in `TEACHER_TRANSPORTS`, when
that transport's dependency is absent, or when the call fails — and every refusal
names the provider and the model it refused for, so the operator can act on it.
`teacher_qa.no_model_refusal` keeps its job and its wording unchanged; only what
triggers it is corrected. Stage 1 keeps working, because Stage 1 is offline by
construction, and the refusal says so.

ALTERNATIVES CONSIDERED and rejected. Adding a sentinel "unconfigured" model so
the spec's literal words become reachable — rejected because it invents a state
to satisfy a sentence, and every other role would inherit it. Refusing whenever
`teacher.model` is absent from the config file — rejected because it would refuse
the default configuration that works, which is the opposite of honest.

CONSEQUENCE. A REFUSAL IS NEVER BILLED: no model was called, so no ledger row is
written, and a row claiming one would be the fabrication `token_ledger` refuses.
The feature file records this supersession beside its earlier three.

Reverse this decision by deleting this section and restoring the Edge-cases
sentence as the implemented condition.

## DECISION F255 D10 — `teach.ask` declares write_metadata, and its read-only proof names the ledger (2026-08-21)

CONTEXT. The Scope block lists "Hard invariants: ActionClass read_only", and
`teach.narrate` earns that declaration with the behavioural proof DECISION F255
D4 required. But DECISION F255 D3 requires Stage 2 to record teacher spend and
DECISION F255 D7 shapes that row, so `teach ask` writes
`<data_root>/projects/<project_id>/ledger.sqlite` and its sqlite sidecars. A
`read_only` declaration on that command would be false, and DECISION F255 D4
exists precisely because a declaration proves nothing while a false one misleads
the permission layer that reads the catalog.

CHOSEN. `teach.ask` declares `action_class="write_metadata"`, the class the
catalog already uses for commands that write Remedy's own records and not the
user's repository. `teach.narrate` keeps `read_only` unchanged. The invariant the
Scope actually means — never influencing the RUN — is proven for ask the same
behavioural way it was proven for narrate, with the ledger file and its sidecars
EXCLUDED BY EXPLICIT NAME and the exclusion itself asserted, so any other write
still fails the test.

ALTERNATIVES CONSIDERED and rejected. Declaring `read_only` and arguing the
ledger is not part of the run — rejected because the catalog's classes describe
what a command WRITES, not what it means to write, and a permission layer cannot
read intent. Moving the ledger write out of the command into a later batch —
rejected because it would separate the cost from the question that incurred it
and reintroduce the uncalled seam this round exists to close.

CONSEQUENCE. The teacher group now holds one `read_only` command and one
`write_metadata` command, and F255's read-only claim is stated where it is true
rather than everywhere.

Reverse this decision by deleting this section and changing the `teach.ask`
entry's `action_class` back to `read_only`.
<<<END DECISIONS255
<<<SLICE AMEND255
## Amendment status (F255 R16, 2026-08-21)

Two more phrases were measured against the code at `2e5b8299` and found to name
ground that does not exist, and one design choice is recorded here because the
Scope assumes a provider this repository does not have. Each is SUPERSEDED by a
ruling in `.agent/decisions.md`, and the superseding text is stated here so that
this file and those rulings never disagree on disk.

- "With no model configured, Stage 2 refuses" (Edge cases) — SUPERSEDED by
  DECISION F255 D9. `resolve_role_config` fills an unset model from the
  provider's default, so no configuration reaches the state that sentence names.
  Stage 2 refuses when the resolved provider has NO TEACHER TRANSPORT, when that
  transport's dependency is absent, or when the call fails, each refusal naming
  the provider and model it refused for. A refusal is never billed.
- "Hard invariants: ActionClass read_only" (Scope) — SUPERSEDED by DECISION F255
  D10 for `remedy teach ask` ALONE, which writes exactly one token-ledger row
  that DECISION F255 D3 requires and DECISION F255 D7 shapes, and therefore
  declares `write_metadata`. `remedy teach narrate` keeps `read_only` and the
  proof it earned at T003. The invariant the Scope means — never influencing the
  RUN — is unchanged, and for ask it is proven by the byte-equality of every file
  under the data root EXCEPT the ledger, excluded by name.
- Stage 2's model seam is `packages/orchestration/teacher_model.py`, ruled by
  DECISION F255 D8: no generic text-completion provider exists here —
  `OllamaPlanner.raw_call` requires a schema and reads the PLANNER's own
  configuration — so the teacher owns a narrow transport behind an injectable
  seam rather than borrowing another role's.
<<<END AMEND255

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit and at the handback; `git worktree list` reports the
   primary checkout alone.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r16.md`, of `.agent/authored/f255-r16.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Extract each slice from the COMMITTED
   `.agent/authored/f255-r16.md` by its markers and report each slice's name,
   sha256, byte count and line count, naming the newline convention (R-0600).
   Report the number of slices as a COUNT YOU TOOK FROM THAT LISTING; this block
   states no numeral of its own for it (R-0604, checklist item 11).
G4 THE PLAN, FIRST. `.agent/plan.md` at C1 byte-equals PLAN255R16; report its
   sha256, byte and line counts, that the line count is under 50, and that
   `## Goal`, `## Next Steps` and a roadmap F-id all occur in it. Report also
   that C1 is the FIRST commit of this round other than C0a and C0b, from
   `git log --reverse 2e5b8299..<C1>`.
G5 THE R15 VERDICT RECORDED. Over `.agent/live_review.md`: the base blob at
   `2e5b8299` is a byte-exact PREFIX of the C2 blob; report the remainder's
   sha256, byte and line counts; that it equals one newline followed by
   RECORDR15; and that the byte after that leading newline is not a newline.
   Then a SECOND, INDEPENDENT blank-line paragraph split of the C2 blob whose
   LAST unit is RECORDR15, giving that unit's sha256 under BOTH newline
   conventions with the byte count of each. Constraint 5 records the measurement
   that makes the LAST-UNIT reading exact here; re-measure it rather than
   trusting it. Run a negative control: one character of the expected remainder
   mutated, rejected by BOTH readings.
G6 THE RULINGS AND THE AMENDMENT. For C3 over `.agent/decisions.md` and for C4
   over `docs/roadmap/features/T5_F255.md`, report the same prefix, remainder,
   equality and separator readings — the C3 remainder equal to one newline
   followed by DECISIONS255, the C4 remainder equal to one newline followed by
   AMEND255. NO paragraph reading is ordered for either: both slices are
   multi-paragraph (constraint 5). Report additionally that each of the three
   strings `## DECISION F255 D8`, `## DECISION F255 D9` and `## DECISION F255
   D10` occurs 0x in `.agent/decisions.md` at `2e5b8299` and 1x at C3, counted
   LINE-ANCHORED.
G7 THE SETS AND THE KEYS. Report registered / resolved / open / line-anchored
   `Landed:` over `.agent/live_review.md` at `2e5b8299` and at C2, the registered
   count being lines matching `^- R-\d+ — ` and the resolved count lines matching
   `^Done: R-\d+ — `: the reviewer measured 183 / 3 / 180 / 0 at `2e5b8299`, and
   C2 owes the SAME four numbers because a `Gate:` paragraph adds neither kind of
   line. Report that `Gate: R16 — the R15 entry.` occurs 0x at `2e5b8299` and 1x
   at C2, that it is the LAST line beginning `Gate: R`, and that every such
   header key is distinct. COUNT HEADERS LINE-ANCHORED, never as substrings
   (R-0584).
G8 THE SEAM. At C5 run
     `python3 -m pytest tests/orchestration/test_teacher_model.py -q -rf`
   and report the exact command, exit code and tail; it must be exit 0. Report
   also `python3 -m ruff check packages/orchestration/teacher_model.py
   tests/orchestration/test_teacher_model.py` at C5 with its exit code; the
   reviewer measured ruff 0.15.17 exit 0 over the six existing files this round
   touches at `2e5b8299`, so exit 0 is the standard these NEW files are held to.
   State that no test in this file opens a socket, and name the test that asserts
   the default `call` IS `ollama_teacher_call` by identity.
G9 THE CLI, THE CATALOG AND THE PIN. At C6 run
     `python3 -m pytest tests/cli/test_teach_cmd.py tests/test_command_catalog.py -q -rf`
   and report the exact command, exit code and tail; exit 0. Report that
   `get_command("teach.ask").action_class` is `write_metadata`, that
   `get_commands_for_group("teach")` and `set(COMMAND_HANDLERS)` are EQUAL as
   sets, and that the pin
   `test_the_handler_table_covers_every_declared_teach_command` still asserts an
   EQUALITY of those two sets rather than a subset. The reviewer measured that
   pin as `declared == {"teach.narrate"} == set(COMMAND_HANDLERS)` at
   `2e5b8299`, so it goes red unless C6 extends it in the same commit.
G10 THE BEHAVIOURAL PROOFS. At C7 run
     `python3 -m pytest tests/cli/test_teach_cmd.py -q -rf`
   and report the exact command, exit code and tail; exit 0. Report the NAME of
   each of the four tests the Change section's C7 list requires, and for the
   read-only one state the exclusion filter it applies, verbatim.
G11 THE DOCS GATE. This round's change set includes `docs/roadmap/**`, so at C7
   run, serially and in the PRIMARY checkout:
     `python3 -m pytest tests/docs/ -q -rf`
     `python3 -m pytest tests/orchestration/test_roadmap_index.py -q -rf`
   and report each command, exit code and tail. The reviewer measured exit 0 at
   295 passed and exit 0 at 30 passed at `2e5b8299`.
G12 THE CANARY AND THE STATE READERS, UNCONDITIONALLY — this is R-0607's own rule
   obeyed, and it binds whether or not the round looks harmless. This round
   rewrites `.agent/` state, so both gate. Run them serially in the PRIMARY
   checkout, never two pytest processes at once, and report the exact command,
   exit code and tail of each:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
   The reviewer measured exit 0 at 160 passed and exit 0 at 42 passed at
   `2e5b8299` in the primary checkout.
G13 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only 2e5b8299..<C7>`
   and state that it equals the Change list minus `.agent/handoff.md`, which C8
   itself adds, with no path on either side alone. Report that each path the
   Change section names untouched is PRESENT at the base and ABSENT from the
   range; that every commit in the range has one parent; and each commit's
   insertion column from `git diff --numstat` for C0a through C7, every one under
   500, with the same `+/-` cells appearing byte-identically in the handback's
   `## Commits` table (checklist item 28). C8's own cell and the complete change
   set belong to the round report, because a handback cannot table the commit
   that writes it (R-0149).
   THE REFLOG IS TWO MEASURED CLAIMS, NOT ONE UNIVERSAL (R-0601), AND NEITHER IS
   A TOTAL (R-0605): report the count of this round's reflog entries whose
   OPERATION PREFIX — the text before the first colon of
   `git reflog --format=%gs` — reads exactly `commit`, WITH the commit it was
   taken at and the number of commits the round has made AT THAT MOMENT, and
   state that the two are equal. State no total: C8 is unwritten as this is
   composed, so the reviewer measures its entry at the next gate (R-0494). Report
   also the count whose prefix contains `amend`, `reset`, `rebase` or `cherry`,
   which must be 0.
G14 NO MARKER LEAKED, AND THE PUSH. Report the count of LINES beginning with the
   SLICE or END marker prefixes in `.agent/plan.md` at C1, `.agent/live_review.md`
   at C2, `.agent/decisions.md` at C3, `docs/roadmap/features/T5_F255.md` at C4
   and `.agent/handoff.md` at C8 — every count 0. Then, after C8, `git push` and
   report its real output. Do NOT create a pull request and do NOT wait on the CI
   run the push starts (constraint 12).

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the item-status
             table for the C0a..C8 bundle, the `## Commits` table G13 pins, and
             one LINE per gate rather than its transcript (R-0582). Its `## Next`
             section names the next session's FIRST action as Phase 1 rule 1, the
             `.agent/STOP` re-read, and its SECOND as the INTEGRATION GATE round
             per docs/agents/integration_gate.md, which follows T004. It states
             that R15 PASSED and that its verdict is now ON DISK at C2, that this
             round registered no finding and resolved none, that R-0607 remains
             OPEN and is closed only by a docs round promoting its rule into the
             §3 checklist, and that R16 ITSELF IS THE ROUND WHOSE VERDICT IS NOT
             ON DISK, so it awaits review. It states that no pull request is open.
             Transcripts go in the round report. The handback carries this
             Fortschritt line verbatim (R-0418):
             Fortschritt: ~88 % (T001, T002 and T003 COMPLETE · T004 COMPLETE at
             this round — the model seam is built, ruled and CALLED by
             `remedy teach ask`, and teacher spend lands as its own ledger role ·
             integration gate and closure remain) — Schätzung
──────────────────────────────────────────────────────────────
