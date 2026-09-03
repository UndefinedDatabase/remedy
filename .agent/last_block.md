== STEP self-use / F109 — ROUND 19 ==

SESSION 4 of feature F109. Round 19. Rounds so far: 18 done, this is the 19th.
Soft limit is 25 rounds / 7 sessions (docs/agents/self_drive_protocol.md G7,
amend0827 rule 6); at 19 rounds and 4 sessions it is NOT reached, so no scope
report is due. No line of this block is a run of a repeated character, so there
is no run length to recover (§3 checklist item 37).

Scope rule, verbatim as every F109 order must carry it:
RESUMED SESSION ONLY, PROVEN SENDS ONLY.

## Goal

Discharge closure precondition 6 (docs/roadmap/STATUS_closure_protocol.md): the
self-use queue holds NO pending item, so the generator supplies one from the
ledger, and it is PLANNED and RUN to the normal approval gate like any other job
— never promoted. Report every defect the run exposes, so the reviewer can author
them as findings for the closure round. Also book round 18's PASS and resolve
`R-0783`.

## Bundle, in commit order

- C0a  save this block verbatim to `.agent/authored/f109-r19.md`
- C0b  mirror it to `.agent/last_block.md`
- C1   apply PLAN19 to `.agent/plan.md`            (FIRST substantive commit)
- C2   append RECORD19 to `.agent/live_review.md`  (verdict, one resolution)
- C3   the self-use item: generate, plan, RUN, and land its evidence
- C4   rewrite `.agent/handoff.md`

## Change set — these paths and nothing else

    .agent/authored/f109-r19.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    scripts/self_use_queue.json
    .agent/selfuse_f109/             (new directory; `run.txt` and the job file)
    .agent/handoff.md

## Constraints

1. EVERY authored slice below is applied BYTE FOR BYTE. C3 is NOT a slice — it is
   a procedure whose output is whatever the shipped code produces. You never
   hand-write the queue entry or the job file; the shipped functions write them.
2. `.agent/live_review.md` ends WITHOUT a trailing newline and that convention is
   preserved: append exactly the two bytes `\n\n` then RECORD19, which itself ends
   without one. Never rewrite a landed entry.
3. `consumed_by` STAYS EMPTY on the generated item this round. Closure
   precondition 6 sets it to `F109` in the CLOSURE commit, which is not this
   round. Do not set it early.
4. The four items already in `scripts/self_use_queue.json` are NOT edited. After
   C3 the file holds exactly one MORE item than before and the four prior ones
   are byte-identical.
5. THE RUN IS A REAL RUN. `packages.orchestration.role_config.resolve_role_config`
   answers provider `ollama`, model `muse-glimmer:latest`, for both roles, so
   `run_next_self_use_item` will NOT refuse for want of a real provider. Do NOT
   pass `builder_name="fake"` or `reviewer_name="fake"` — the docstring reserves
   those for tests, and a faked run does not discharge the precondition. Keep the
   default budgets (`max_provider_calls=6`, `max_cost_usd=0.50`, `max_tasks=1`).
6. IF THE RUN CANNOT HAPPEN — ollama unreachable, the model absent, the budget
   exhausted, `SelfUseRunError` raised — that is a REPORTABLE OUTCOME, not
   something to route around. Record the exact exception text and the full
   traceback in `.agent/selfuse_f109/run.txt`, say so plainly in the handback, and
   STOP the round there with C3 committed as far as it got. A blocked precondition
   truthfully reported is a success; a faked run is a closure-corrupting lie.
7. Nothing outside the change set is edited. If the sweep finds something else,
   DECLARE it; do not repair it.
8. `python3 -m pytest` is the pytest route. Env-var assignment (`VAR=x cmd`,
   `env`, `export`) and `cp` are DENIED: copy with
   `python3 -c "import shutil; shutil.copyfile(a, b)"`. A `bash -c` wrapper around
   a Python heredoc, and a heredoc with braces adjacent to quotes, have both been
   observed DENIED — write such logic to a scratch `.py` under `.remedy-wt/`, run
   it with `python3 -B`, and delete it by exact path. A local-model run can be
   SLOW: give it a generous timeout and never report a tool-level timeout as a run
   result.
9. Never force-push, never work on main, never create or merge a PR this round.

## SLICE FORTSCHRITT — one line, applied verbatim into the handback's state block

BEGIN FORTSCHRITT
| **Fortschritt** | ~98 % (T001-T003 ✅ · Integration Gate ✅ · Self-Use läuft · Closure offen) — Schätzung |
END FORTSCHRITT

## SLICE PLAN19 — the whole of `.agent/plan.md`

BEGIN PLAN19
# Plan — F109 Semantic dedupe

Branch: feature/f109-semantic-dedupe, cut from `main` at
`5e18a8536afa086b591b5a2e13009d68d6227432` (pull request 231 merged).

## Goal

Within a RESUMED session only, stop resending context the model has
already provably received: segments whose hash already went to that exact
session are replaced by short reference markers. Everywhere else full
content wins, because only a resumed session guarantees the model still
holds the prior content. The scope rule of the whole feature is "resumed
session only, proven sends only".

## Current Step

Round 19, session 4. CLOSURE PRECONDITION 6, the self-use item: the queue
holds no pending item, so the generator supplies one from the ledger and
it is planned and RUN to the normal approval gate under the product's own
provider — never promoted, never faked. Its defects are reported in the
handback for the reviewer to author as findings. Also book round 18's
PASS and resolve `R-0783`.

## Next Steps

- The closure sequence (docs/roadmap/STATUS_closure_protocol.md):
  register the self-use defects, the evidence job, a FRESH review zip,
  the authored STATUS line with the README sync in the SAME commit, the
  `consumed_by` edit, and the PR. That round also runs the single
  consolidation pass on the checklist of
  docs/agents/planner_reviewer_prompt.md section 3.

## Risks

- The self-use run uses a local model. If it cannot run, the precondition
  is BLOCKED and reported, never faked.
- SEVEN findings on this branch have been one class: prose TRUE when
  written and falsified by a later round. The consolidation should answer
  the class, not add an eighth id.
- Nothing dedupes in production: every concrete adapter returns
  `supports_resume = False`, so the mechanism is suite-only today.
- The open finding set is a SET DIFFERENCE, not a subtraction: two ids
  carry two `Done:` lines each. That is `R-0778`.
END PLAN19

## SLICE RECORD19 — appended to `.agent/live_review.md`, two paragraphs

BEGIN RECORD19
Gate: F109 R18 — the round 18 entry. VERDICT PASS, over the range `50526376..cb19e916`. THE TRANSPORT PROOF IS AGAIN A REAL ONE — `cmp` of `.remedy-wt/f109-r18.md`, the reviewer's own original, against `.agent/authored/f109-r18.md` exited 0 — and EVERY SLICE WAS VERIFIED BYTE-IDENTICAL by the reviewer independently: `.agent/plan.md` equals PLAN18, RECORD18's three paragraphs are the tail of this record, PAIR F reads FROM 0x and TO 1x, and BUILTSTATE is the exact tail of `docs/roadmap/features/T3_F109.md`, which now carries exactly one `## Built State` heading and exactly one trailing newline. THE FEATURE FILE THEREFORE SATISFIES CLOSURE PRECONDITION 4, which it did not before this round: it had no Built State section at all. THE SUITES were re-run by the reviewer at 295, 130, 54 and 42, totalling 521 at exit 0, and NO COUNT MOVED IN EITHER DIRECTION, which is what the round's own constraint demanded of a comment-only repair. THE HANDBACK CARRIES THE FORTSCHRITT LINE VERBATIM, confirmed by the reviewer as a substring of `.agent/handoff.md`; that is finding `R-0418`'s standing form for self-drive, where no paste relay exists and a worker cannot see the operator brief, and this is the first round of this feature to satisfy it — the reviewer's earlier blocks simply omitted the line, which met `R-0418`'s letter by not ordering it and missed the obligation planner_reviewer_prompt.md §3 states. A CORRECTION THE REVIEWER OWES THIS RECORD, appended here rather than by rewriting the landed text, which item 20 forbids: the R-0783 paragraph committed at `18f0c9c6` calls that finding "THE SIXTH SITE OF ONE CLASS" and lists `R-0749`, `R-0773`, `R-0779`, `R-0780` and `R-0781` before it, omitting `R-0782`, which is a member of exactly that class by its own registration text. THE TRUE COUNT IS SEVEN. The worker of round 18 spotted the discrepancy and reported it rather than editing either text, which is correct. Nothing on disk under `packages/`, `apps/`, `tests/` or `docs/` is wrong because of it and the argument the numeral served — that the closure consolidation must answer the CLASS rather than mint another id — is unaffected at six or seven, so this is a dated correction and a `.agent/prose_slips.md` line at the consolidation, not a new id and not a correction round. TWO FURTHER REVIEWER LOOSENESSES the round declared and the reviewer accepts: G6(c) asked for the marker string `[unchanged: ` to "resolve in the modules named" when it lives in `session_sent_index.py` and reaches the loop only through the imported `dedupe_marker_for_segment`, so a literal grep in `pingpong_loop.py` reads 0 while the Built State sentence stays true; and G3(d) named `35c0b03f` as its base while G3(a) named `50526376`, so the ledger delta it reports spans two rounds — the figures 342 to 344 registered and 66 to 69 `Done:` lines are correct for that wider range, and the reviewer re-derived them independently, but the base should have been the round's own. THE OPEN SET IS 277 by set difference over 344 distinct registered ids and 67 distinct resolved ones. THE TREE is clean and the branch is pushed at `cb19e916`.

Done: R-0783 — RESOLVED at `b89456a6` and verified by the reviewer at `cb19e916`. The comment above `test_a_disabled_run_reports_no_deduped_names_on_any_composition` in `tests/orchestration/test_semantic_dedupe.py` no longer gives "the report never reaches ``PingPongResult``" as its reason. It now says the composed OBJECT is what those cases assert on and only the capture helper yields it, while stating plainly that the prompt trace carries the deduped NAMES onto `PingPongResult` but never the `ComposedPrompt` itself — which is the distinction `R-0782`'s repair established one round earlier, now applied consistently across both sites. The reviewer counted the string `the report never reaches` in that file at ZERO, which is the finding's stated resolution condition, and confirmed by AST over the commit's own blobs that every definition name and every executable-statement count is unchanged, so the repair moved no code and the suite still collects 130.
END RECORD19

## C3 — the self-use procedure, in this order

This is the only part of the round that is a PROCEDURE rather than a slice. Do
each step, capture its REAL output, and write everything you capture into
`.agent/selfuse_f109/run.txt` — commands, return values, status, provider, and
any traceback in full.

1. BEFORE. Record `pending_self_use_items()` (expect 0 pending of 4 items) and
   `next_self_use_item()` (expect `None`), which is WHY the generator runs at all.
2. GENERATE. Call
   `packages.orchestration.self_use_generator.generate_and_append_if_empty()` and
   record the entry it returns. The reviewer's own read-only probe of
   `generate_self_use_item()` at `cb19e916` answered `SU-005`, titled
   "Address ledger finding R-0418", provenance
   `generated (self-use-generator tier 1, ledger scan, R-0418)`. Report what YOURS
   returns; a different id or subject is a real difference worth declaring, not a
   discrepancy to smooth over.
3. RUN. Call
   `packages.orchestration.self_use_runner.run_next_self_use_item(dest_dir=Path(".remedy-wt/selfuse-f109-run"), repo_path=".")`
   with the DEFAULT budgets and NO `builder_name`/`reviewer_name` override, per
   constraint 5. It answers `(entry, job_file_path, plan)`. Record the plan's
   `status`, its `error` if any, and the provider its `execution_config` says
   actually ran.
4. DEFECTS. Call
   `packages.orchestration.self_use_findings.describe_self_use_run_defects(plan)`
   and record EVERY string it returns, verbatim and in order, each on its own
   clearly delimited line. An EMPTY TUPLE means nothing to register — record it
   as the empty result it is, never as "no defects were checked".
5. LAND THE EVIDENCE. Copy the rendered job file into `.agent/selfuse_f109/` under
   its own item id (the precedent is `.agent/selfuse_f257/`, which holds `run.txt`
   and `SU-001.md`), and commit `run.txt` beside it. The run's working directory
   under `.remedy-wt/` is scratch and is NOT committed; delete it by exact path
   after copying what you need.

## Done when — the eight gates. RUN each one and record its REAL exit code.

Every gate below runs at a commit STRICTLY EARLIER than C4, the commit that
writes the handback, so the handback can honestly quote all eight.

G1 TRANSPORT, one comparison and no chain. Run
   `cmp .remedy-wt/f109-r19.md .agent/authored/f109-r19.md` and report the exit
   code. That scratch file is the REVIEWER'S OWN original, so this proves real
   transport, not your own self-consistency. Then report
   `sha256sum .agent/authored/f109-r19.md .agent/last_block.md` — one digest twice.

G2 THE PLAN. Extract PLAN19 by delimiter index and `cmp` it against
   `.agent/plan.md` after C1: exit 0, no output. Report `wc -l .agent/plan.md`,
   under 50 (AGENTS.md), and `grep -c '^## Goal'` and `grep -c '^## Next Steps'`,
   each 1.

G3 THE RECORD APPEND, four readings.
   (a) ARITHMETIC. Report base size and base sha256 of `.agent/live_review.md` at
       `cb19e916`, the appended length S, the new size, and whether base + S
       equals it. Confirm the file still ends WITHOUT a trailing newline.
   (b) A SECOND READER THAT COUNTS NO BYTE, covering the WHOLE appended region.
       Split the entire file on blank-line boundaries into units. Let N be the
       paragraph count of RECORD19 as YOUR SCRIPT COUNTS IT from the slice — do
       not take N from this block. Assert the LAST N units equal RECORD19's N
       paragraphs IN ORDER, printing each one's opening 60 characters.
   (c) A NEGATIVE CONTROL ON THE FIRST APPENDED PARAGRAPH. Copy the file to
       `.remedy-wt/live_review_negative_control_r19.md`, flip one byte INSIDE the
       FIRST appended paragraph there, and show reader (b) REJECTS the copy while
       ACCEPTING the tracked file. Report the tracked sha256 before and after,
       then delete that scratch file BY ITS EXACT PATH and report
       `os.path.exists` on that exact path as False.
   (d) COUNTS, AS A SET DIFFERENCE and never a subtraction (`R-0778`). Read the
       base from `git show cb19e916:.agent/live_review.md` — THE ROUND'S OWN BASE,
       not an earlier one — and report five figures for base and five for the new
       state: registered ids, DISTINCT registered ids, `Done:` lines, DISTINCT
       resolved ids, and `len(set(registered) - set(resolved))`. Also report
       `grep -c '^Gate: F109 R18 — '` = 1 and `grep -c '^Done: R-0783 — '` = 1.

G4 THE QUEUE GREW BY EXACTLY ONE, AND ONLY AT THE END. Report the item count of
   `scripts/self_use_queue.json` before and after C3 (expect 4 then 5), that the
   FIRST FOUR items are byte-identical to their pre-C3 selves when re-serialised
   in order, that the new item's `consumed_by` is the EMPTY string, that its
   `provenance` is non-blank, and that its id matches `^SU-\d{3}$`. Report
   `schema_version`, which must still read 2.

G5 THE RUN REALLY RAN, AND NOT UNDER THE FAKE PROVIDER. From the captured output
   report: the `JobPlan.status`, its `error` if any, and the provider named in its
   `execution_config`. That provider must NOT be `fake`. If the run raised
   instead, report the exception type and message verbatim — constraint 6 makes
   that a valid outcome for this gate, and the gate is then RED-BUT-HONEST rather
   than passed.

G6 THE DEFECTS ARE RECORDED VERBATIM. Report the exact tuple
   `describe_self_use_run_defects(plan)` returned — its length and every string in
   order — and show that each one appears in `.agent/selfuse_f109/run.txt`. This
   is the gate the CLOSURE round reads: the reviewer authors findings from these
   strings, so a paraphrase here becomes a wrong finding there.

G7 THE SUITES, run SERIALLY, one process finishing before the next starts. Report
   the collected count and REAL exit code of each:
   - `python3 -m pytest tests/orchestration/test_self_use_queue.py -q`
   - `python3 -m pytest tests/orchestration/test_self_use_generator.py -q`
   - `python3 -m pytest tests/orchestration/test_self_use_runner.py -q`
   - `python3 -m pytest tests/orchestration/test_self_use_job.py -q`
   - `python3 -m pytest tests/cli/test_golden_path.py -q`
   The first four are the suites that READ the queue file this round appends to,
   which is why they are named; the last is the mandatory canary. None may go red.
   The reviewer checked their guards at `cb19e916`: they assert at least one item,
   `schema_version == 2`, unique ids matching `^SU-\d{3}$`, and a non-blank
   provenance on every item — there is NO count-equality guard, so a fifth item is
   safe by construction.

G8 THE TREE AND THE SWEEP. `git status --porcelain` EMPTY and
   `git ls-files .remedy-wt` returning nothing. Confirm
   `.remedy-wt/selfuse-f109-run` is gone by exact path. Report each commit's
   insertion count from `git show --numstat` — the `+` column ONLY, per AGENTS.md
   DECISION F104 D1 — for every commit of this round EXCEPT C4, and compare cell
   by cell against your own `## Commits` table (§3 checklist item 28). Then
   re-read each file this round touched and report every sentence now stale,
   including any you did NOT repair, with the reason.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It has NO
length cap. Its STATE BLOCK carries the FORTSCHRITT slice above, applied VERBATIM
as its own line. It must also carry: the SESSION NUMBER (4) and round (19); the
item-status table with every one of C0a, C0b, C1, C2, C3, C4 appearing exactly
once with `done`, `skipped` or `deviated` and a reason; a per-commit changed-files
table with the `+/-` column; ONE LINE PER GATE G1 through G8 with its real
reading; THE SELF-USE OUTCOME in one unmissable sentence — item id, run status,
provider, and the number of defects reported; the FULL verbatim defect list a
second time in its own section, because the closure round authors findings from
it; the open-finding count as a SET DIFFERENCE; your deviations and assumptions;
and the next expected action, which is the closure sequence. Then
`git push -u origin feature/f109-semantic-dedupe` and report the result. Create
no PR.
