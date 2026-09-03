== STEP closure-prep / F109 — ROUND 18 ==

SESSION 4 of feature F109. Round 18. Rounds so far: 17 done, this is the 18th.
Soft limit is 25 rounds / 7 sessions (docs/agents/self_drive_protocol.md G7,
amend0827 rule 6); at 18 rounds and 4 sessions it is NOT reached, so no scope
report is due. No line of this block is a run of a repeated character, so there
is no run length to recover (§3 checklist item 37).

Scope rule, verbatim as every F109 order must carry it:
RESUMED SESSION ONLY, PROVEN SENDS ONLY.

## Goal

Make every closure precondition that this round can reach TRUE. Give
`docs/roadmap/features/T3_F109.md` the BUILT STATE section closure precondition 4
requires and it does not have. Book round 17's PASS — the integration gate, both
suites green with zero branch-only failures — resolve `R-0782`, and register and
repair `R-0783`, the sixth site of the stale-prose class and the last one the
sweep has found.

## Bundle, in commit order

- C0a  save this block verbatim to `.agent/authored/f109-r18.md`
- C0b  mirror it to `.agent/last_block.md`
- C1   apply PLAN18 to `.agent/plan.md`            (FIRST substantive commit)
- C2   append RECORD18 to `.agent/live_review.md`  (verdict, one resolution, new id)
- C3   apply PAIR F to `tests/orchestration/test_semantic_dedupe.py`
- C4   append BUILTSTATE to `docs/roadmap/features/T3_F109.md`
- C5   rewrite `.agent/handoff.md`

## Change set — these paths and nothing else

    .agent/authored/f109-r18.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    tests/orchestration/test_semantic_dedupe.py
    docs/roadmap/features/T3_F109.md
    .agent/handoff.md

## Constraints

1. EVERY slice below is applied BYTE FOR BYTE — no rewrap, no re-indent, no
   improvement. If a slice looks wrong, apply it anyway and declare it in the
   handback; that is how a reviewer mistake becomes visible rather than becoming
   a silent correction.
2. `.agent/live_review.md` ends WITHOUT a trailing newline and that convention is
   preserved: append exactly the two bytes `\n\n` then RECORD18, which itself
   ends without one. Never rewrite a landed entry.
3. `docs/roadmap/features/T3_F109.md` ends WITH exactly one trailing newline.
   Append exactly the one byte `\n` and then BUILTSTATE, which itself ends with
   one trailing newline — so the file gains a blank separator line and still ends
   with exactly one newline. Nothing already in that file is edited or deleted.
4. C3 changes ONE COMMENT. No executable line moves, no case is added, renamed or
   deleted, no import changes. The dedupe suite's collected count must be
   IDENTICAL before and after C3, and it is 130 at `50526376`.
5. THE HANDBACK CARRIES THE FORTSCHRITT LINE, and this block supplies it as
   authored text below rather than telling you to fetch it from somewhere you
   cannot see. That is finding `R-0418`'s standing form for self-drive: under
   docs/agents/self_drive_protocol.md there is no paste relay, so a worker never
   sees the reviewer's operator brief and any order to copy a line out of it is
   unsatisfiable by construction.
6. Nothing outside the change set is edited. If the sweep finds something else,
   DECLARE it; do not repair it.
7. Do not quote this handback commit's own insertion count anywhere; it cannot
   exist while the text stating it is written (§3 checklist item 14).
8. `python3 -m pytest` is the pytest route. Env-var assignment (`VAR=x cmd`,
   `env`, `export`) and `cp` are DENIED: copy with
   `python3 -c "import shutil; shutil.copyfile(a, b)"`. A `bash -c` wrapper
   around a Python heredoc, and a heredoc with braces adjacent to quotes, have
   both been observed DENIED — write such logic to a scratch `.py` under
   `.remedy-wt/`, run it with `python3 -B`, and delete it by exact path.
9. Never force-push, never work on main, never create or merge a PR this round.

## SLICE FORTSCHRITT — one line, applied verbatim into the handback's state block

BEGIN FORTSCHRITT
| **Fortschritt** | ~97 % (T001 ✅ · T002 ✅ · T003 ✅ · Integration Gate ✅ · Closure offen) — Schätzung |
END FORTSCHRITT

## SLICE PLAN18 — the whole of `.agent/plan.md`

BEGIN PLAN18
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

Round 18, session 4. CLOSURE PREPARATION. Give the feature file the
BUILT STATE section closure precondition 4 requires; book round 17's
PASS, which is the integration gate — branch 18937 passed and base 18799
passed, both exit 0, with ZERO branch-only failures; resolve `R-0782`;
and register and repair `R-0783`, the sixth and last site the
stale-prose sweep has found.

## Next Steps

- The self-use item closure precondition 6 requires: the queue holds no
  pending item, so `generate_and_append_if_empty` supplies one from the
  ledger, and it is planned, RUN to the normal approval gate, and its
  defects registered before the close.
- The closure sequence proper: evidence job, a FRESH review zip, the
  authored STATUS line with the README sync in the SAME commit, the PR.

## Risks

- Six findings on this branch have been one class: prose that was TRUE
  when written and was falsified by a later round. The closure
  consolidation should answer the class, not add a seventh id.
- Nothing dedupes in production: every concrete adapter returns
  `supports_resume = False`, so the mechanism is suite-only today.
  `docs/system/semantic-dedupe-v1.md` states this plainly.
- The open finding set is a SET DIFFERENCE, not a subtraction: two ids
  carry two `Done:` lines each. That is `R-0778`.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
END PLAN18

## SLICE RECORD18 — appended to `.agent/live_review.md`, three paragraphs

BEGIN RECORD18
Gate: F109 R17 — the round 17 entry. VERDICT PASS, over the range `35c0b03f..50526376`. THIS IS THE INTEGRATION GATE ROUND AND IT IS GREEN ON BOTH SIDES: the branch at `cce5f9d7` ran 18937 passed, 20 skipped, ZERO failed, exit 0 in 133.20s, and the base at `5e18a8536afa086b591b5a2e13009d68d6227432`, checked out on the throwaway branch `tmp/base-gate` because a DETACHED base worktree fails the self-dogfood guard by design, ran 18799 passed, 20 skipped, ZERO failed, exit 0 in 159.88s. `comm -13` and `comm -23` are BOTH EMPTY, so there is no branch-only failure and no base-only failure, and NO BLOCKER exists. THE REVIEWER MEASURED THE BRANCH SUITE INDEPENDENTLY at `35c0b03f` before authoring the round — 18937 passed, 20 skipped, zero failed, exit 0, 133.30s — and gave those four figures to the worker precisely so a divergence would show as divergence; the worker's reading matches all four, differing by 0.10s of wall clock. THE PARITY CLAIM WAS MEASURED AS AN EVENT AND HOLDS: every one of the four files under the base worktree's `apps/ui/dist` carries mtime 1788410854.675 both before and after the base run, and the run window is 1788410860.264 to 1788411020.379, so none is inside it; the accompanying content digest `846b7f62fa3c13a8fd3ecd7c54dfd89771af272843530a59bd318d7e006f7a51` is identical before and after but was correctly reported BESIDE the mtime reading rather than in place of it, which is what `R-0444` asks for. THE ROUND'S THREE SUBSTANTIVE DEVIATIONS ARE ALL SOUND AND TWO OF THEM CORRECT THE REVIEWER. First, the block's constraint 6 sent the running suite's log into `.remedy-wt/`, inside the measured repository, on the reviewer's over-wide reading of `R-0176`; the worker first blamed a red run on it, then MEASURED that `worktree_identity()` reads `git ls-files --others --exclude-standard` and therefore cannot see a gitignored file, and reported its own diagnosis as wrong. That is the behaviour this record exists to reward, and it narrows `R-0176` to files git can actually see. Second, the block's sandbox note implied `REMEDY_UI_NO_AUTO_BUILD` for the whole gate while integration_gate.md scopes it to the BASE run; the worker followed the canonical doc, and its env-var branch run went red at 4 failures while the plain run matched the reviewer exactly — the doc was right and the block was loose. Third, and this is the round's real discovery, `R-0736` reaches further than the block warned: after `copytree(symlinks=True)` preserved all 27 npm symlinks, the first base run still produced 126 failures, every one in `tests/ui_server/` on `ERROR: React UI not built.`, because `git worktree add` stamped all 142 files under `apps/ui/src` at checkout time while `dist` kept its copied mtime, so `_frontend_is_stale()` demanded a rebuild the env var then refused. Re-stamping `dist` RESTORES the true relationship a real base environment would have and changes no content, the digest above proving it; the discarded 126-failure run is declared with its direct evidence rather than quietly dropped. FIVE IDS WENT RED ACROSS THE TWO FLAWED RUNS and every one passes serially, so all five are the xdist-flake class and none touches F109 code. THE TREE is clean, the base worktree and `tmp/base-gate` are gone, and the branch is pushed at `50526376`.

Done: R-0782 — RESOLVED at `cce5f9d7` and verified by the reviewer at `50526376`. The `_capture_compositions` docstring in `tests/orchestration/test_semantic_dedupe.py` no longer says the dedupe report has no production consumer: it now states that the composed OBJECT never reaches `PingPongResult`, which is the helper's real reason for existing, while naming the prompt trace as carrying the manifest and, since `78d2b7b5`, the deduped NAMES that `build_trace_entry` reads off the composed prompt. The reviewer counted the string `no consumer for the report` in that file at ZERO, which is the finding's stated resolution condition, and confirmed by AST over the commit's own blobs that all 154 definition names and every definition's executable-statement count are unchanged, so the repair moved no code.

- R-0783 — Low, A COMMENT IN THE SAME SUITE STILL GIVES THE STALE REASON `R-0782` WAS REGISTERED AGAINST, ONE SCREEN AWAY FROM THE DOCSTRING THAT WAS REPAIRED. Offered by the WORKER of F109 R17 as a candidate and ASSESSED DIFFERENTLY BY THE REVIEWER, which is why it is registered rather than dropped: the worker judged the sentence "still literally true" and left it, correctly, because PAIR E authorised one docstring and widening a pair silently is worse than declaring the miss. MEASURED at `50526376`. The comment above `test_a_disabled_run_reports_no_deduped_names_on_any_composition` reads "THE COMPOSED OBJECTS ARE READ THE WAY SPEC T CASE 5 READS THEM, through that class's own capture helper, because the report never reaches ``PingPongResult``". BY THE VERY DISTINCTION `R-0782`'S REPAIR TURNS ON, that reason is now false: the composed OBJECT never reaches `PingPongResult`, but the REPORT does — as `deduped_segment_names` on each entry of `PingPongResult.prompt_traces`, since `78d2b7b5` — and `TestTheRunsOwnTraceMeasuresWhatItWithheld`, in this same file, reads the report off the result exactly that way. So the comment states a reason that the file itself contradicts two classes later. WHAT REMAINS TRUE and what the repair must keep is the helper's actual justification: the composed OBJECT is what these cases need, and only the capture helper yields it. WHY LOW: no behaviour is wrong, no gate is blind, no test is weakened, the suite is green at 130 cases and the comment misleads a reader rather than a machine. THIS IS THE SIXTH SITE OF ONE CLASS on this branch, after `R-0749`, `R-0773`, `R-0779`, `R-0780` and `R-0781`, and it is registered with that stated plainly because the class, not the site, is what the closure consolidation must answer: every one of the six was a sentence TRUE when written and falsified by a later round that did not sweep it, and five of the six were caught by the standing staleness sweep one round after the falsification. FIX: restate the comment so the OBJECT-versus-REPORT distinction survives and the false reason goes. Resolved when no comment or docstring in that file gives "the report never reaches `PingPongResult`" as a reason for anything.
END RECORD18

## PAIR F — in `tests/orchestration/test_semantic_dedupe.py`

Containment test, run mechanically before emission: TO contains FROM: false.
REWRITE, so the proof is FROM 0x and TO 1x after C3. FROM counted in the target
at `50526376`: exactly 1x.

BEGIN PAIRF_FROM
        # THE COMPOSED OBJECTS ARE READ THE WAY SPEC T CASE 5 READS THEM, through
        # that class's own capture helper, because the report never reaches
        # ``PingPongResult``. The positive half already lives there:
        # ``test_a_resumed_chain_reports_the_names_it_replaced`` runs this very
        # chain at the default flag and finds names, so this case mirrors a
        # measured run rather than an assumption.
END PAIRF_FROM

BEGIN PAIRF_TO
        # THE COMPOSED OBJECTS ARE READ THE WAY SPEC T CASE 5 READS THEM, through
        # that class's own capture helper, because the composed OBJECT is what
        # these cases assert on and only that helper yields it — the prompt trace
        # carries the deduped NAMES onto ``PingPongResult`` but never the
        # ``ComposedPrompt`` itself. The positive half already lives there:
        # ``test_a_resumed_chain_reports_the_names_it_replaced`` runs this very
        # chain at the default flag and finds names, so this case mirrors a
        # measured run rather than an assumption.
END PAIRF_TO

## SLICE BUILTSTATE — appended to `docs/roadmap/features/T3_F109.md`

BEGIN BUILTSTATE
## Built State — what F109 delivered

T001-T003 built semantic dedupe inside a RESUMED provider session only.
The prose description of the built state, for a reader rather than for
this ledger, is `docs/system/semantic-dedupe-v1.md`.

- `packages/orchestration/session_sent_index.py` — `SessionSentIndex`
  keyed by provider session id, holding the segment SHA-256 digests
  `ComposedPrompt.manifest_as_dicts()` produced. `record_call` records
  nothing for a call that carried an error and nothing for an empty
  session id, so an unproven send and a sessionless call can never enter
  the index; a malformed manifest row raises rather than shrinking it
  silently. The module is pure and imports nothing from the rest of
  `packages.orchestration`. `record_finalized_call` and
  `invalidate_on_resume_fallback` are the adapter seams, and
  `session_sent_index_from_evidence` is the restart-honesty seam (T001a,
  T001b-i).
- `packages/orchestration/pingpong_loop.py` — the loop calls both seams
  on the Builder path and again on the Reviewer path and writes
  `as_evidence_dicts()` onto `PingPongResult.session_sent_evidence`
  (T001b-ii, `7451e9c7`). `_dedupe_resumed_segments` replaces an
  already-sent segment's text with
  `[unchanged: <name>, previously provided]`, rewriting text only, so
  names and ranks survive; both `compose_*` functions reach it behind a
  `dedupe_sent_hashes` parameter that bypasses dedupe by default
  (`24352750`, `60343048`). `run_pingpong` carries
  `semantic_dedupe_enabled` and forwards it as `dedupe_enabled`, and
  `enabled` is consulted first and alone, so the kill switch is total
  (T002a-T002c, `b245e1c9`).
- `packages/orchestration/prompt_trace.py` — every `PromptTraceEntry`
  carries `deduped_segment_names`, derived from the composed prompt
  alone (T003c, `78d2b7b5`); and `measure_dedupe_savings_from_traces`
  reports what a run did not resend, reading only that record. Its
  `unmeasured_segment_names` field NAMES a deduped segment whose
  full-content size was never observed and excludes it from every total,
  so an absent measurement can never be read as a zero saving (T003d).
- Measured on the two-round resumed fixture chain at commit `d52a5371`:
  556 characters avoided against 97 spent on markers, 459 net over 2
  withheld segments, nothing unmeasurable; the same chain with the flag
  off reports zero on every field and names nothing unmeasured.
- SCOPE LIMIT, stated because it is the first thing a reader should
  know: no concrete adapter resumes in production — `ClaudeProvider`,
  `ClaudeCliProvider` and `OllamaPingPongProvider` all return
  `supports_resume = False` — so dedupe is exercised by the suite and is
  inert on every real run today. The measurement function is a library
  with no production caller.
END BUILTSTATE

## Done when — the eight gates. RUN each one and record its REAL exit code.

Every gate below runs at a commit STRICTLY EARLIER than C5, the commit that
writes the handback, so the handback can honestly quote all eight.

G1 TRANSPORT, one comparison and no chain. Run
   `cmp .remedy-wt/f109-r18.md .agent/authored/f109-r18.md` and report the exit
   code. That scratch file is the REVIEWER'S OWN original, so this comparison
   proves real transport and not merely your own self-consistency. Then report
   `sha256sum .agent/authored/f109-r18.md .agent/last_block.md` — one digest twice.

G2 THE PLAN. Extract PLAN18 by delimiter index and `cmp` it against
   `.agent/plan.md` after C1: exit 0, no output. Report `wc -l .agent/plan.md`,
   under 50 (AGENTS.md), and `grep -c '^## Goal'` and `grep -c '^## Next Steps'`,
   each 1.

G3 THE RECORD APPEND, four readings; the only slice earning full byte forensics.
   (a) ARITHMETIC. Report base size and base sha256 of `.agent/live_review.md` at
       `50526376`, the appended length S, the new size, and whether base + S
       equals it. Confirm the file still ends WITHOUT a trailing newline.
   (b) A SECOND READER THAT COUNTS NO BYTE, covering the WHOLE appended region.
       Split the entire file on blank-line boundaries into units. Let N be the
       paragraph count of RECORD18 as YOUR SCRIPT COUNTS IT from the slice — do
       not take N from this block. Assert the LAST N units equal RECORD18's N
       paragraphs IN ORDER, printing each one's opening 60 characters.
   (c) A NEGATIVE CONTROL ON THE FIRST APPENDED PARAGRAPH. Copy the file to
       `.remedy-wt/live_review_negative_control_r18.md`, flip one byte INSIDE the
       FIRST appended paragraph there, and show reader (b) REJECTS the copy while
       ACCEPTING the tracked file. Report the tracked sha256 before and after to
       show it never moved, then delete that scratch file BY ITS EXACT PATH and
       report `os.path.exists` on that exact path as False.
   (d) COUNTS, AS A SET DIFFERENCE and never a subtraction (`R-0778`). Read the
       base from `git show 35c0b03f:.agent/live_review.md`, never by rewinding the
       tracked file, and report five figures for base and five for the new state:
       registered ids, DISTINCT registered ids, `Done:` lines, DISTINCT resolved
       ids, and `len(set(registered) - set(resolved))`. Also report
       `grep -c '^Gate: F109 R17 — '` = 1, `grep -c '^Done: R-0782 — '` = 1 and
       `grep -c '^- R-0783 — '` = 1.

G4 PAIR F AND THE PROOF THAT NO CODE MOVED. Report PAIR F's FROM count in
   `tests/orchestration/test_semantic_dedupe.py` BEFORE C3 (1) and AFTER C3 (0),
   and its TO after C3 (1). Then, from `git show <sha>:<path>` blobs only, parse
   the BEFORE and AFTER blob with `ast` and report that the set of definition
   NAMES is identical and that every definition's count of executable body
   statements, with the docstring excluded, is identical. Report the dedupe
   suite's collected count before and after C3; both must read 130.

G5 THE BUILT STATE APPEND. Report the size and sha256 of
   `docs/roadmap/features/T3_F109.md` before C4 and after, the appended length,
   and whether the arithmetic closes. Confirm the file ends with EXACTLY ONE
   trailing newline, that `grep -c '^## Built State'` is 1, and that the bytes
   BEFORE the appended region are byte-identical to the whole pre-C4 file — an
   append adds and never edits.

G6 THE BUILT STATE IS TRUE, re-measured by you rather than trusted. It is a
   ledger claim about code it does not live in, so verify each and report the
   reading: (a) `supports_resume` returns literal False for `ClaudeProvider`,
   `ClaudeCliProvider` and `OllamaPingPongProvider`; (b) each of `7451e9c7`,
   `24352750`, `60343048`, `b245e1c9`, `78d2b7b5` and `d52a5371` exists via
   `git cat-file -e`; (c) the marker string `[unchanged: ` and the field
   `unmeasured_segment_names` both resolve in the modules named; (d)
   `docs/system/semantic-dedupe-v1.md` exists and its own savings table reads
   556, 97, 459 and 2 — the Built State must not disagree with the doc. Any
   reading that contradicts the slice is a finding against the REVIEWER: report
   it, apply the slice unchanged, and do not silently correct it.

G7 THE SUITES, run SERIALLY, one process finishing before the next starts. Report
   the collected count and REAL exit code of each:
   - `python3 -m pytest tests/docs/ -q`
   - `python3 -m pytest tests/orchestration/test_semantic_dedupe.py -q`
   - `python3 -m pytest tests/orchestration/test_prompt_trace.py -q`
   - `python3 -m pytest tests/cli/test_golden_path.py -q`
   `tests/docs/` is FIRST and is mandatory because this round's change set
   includes `docs/roadmap/**` (planner_reviewer_prompt.md §3, verification tier
   5). The last is the mandatory canary. NO COUNT MAY MOVE IN EITHER DIRECTION —
   the reviewer measured these at `50526376` as 295, 130, 54 and 42.

G8 THE TREE AND THE SWEEP. `git status --porcelain` EMPTY and
   `git ls-files .remedy-wt` returning nothing. Report each commit's insertion
   count from `git show --numstat` — the `+` column ONLY, per AGENTS.md DECISION
   F104 D1 — for every commit of this round EXCEPT C5, and compare cell by cell
   against your own `## Commits` table (§3 checklist item 28). Then re-read each
   file this round touched and report every sentence now stale, including any you
   did NOT repair, with the reason.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It has NO
length cap. Its STATE BLOCK carries the FORTSCHRITT slice above, applied
VERBATIM as its own line — that is constraint 5 and finding `R-0418`'s standing
form. It must also carry: the SESSION NUMBER (4) and round (18); the item-status
table with every one of C0a, C0b, C1, C2, C3, C4, C5 appearing exactly once with
`done`, `skipped` or `deviated` and a reason; a per-commit changed-files table
with the `+/-` column; ONE LINE PER GATE G1 through G8 with its real reading; the
open-finding count as a SET DIFFERENCE; a PENDING RESOLUTION note stating that
`R-0783` is repaired but NOT resolved, because only reviewer-authored text sets
`Done:`; your deviations and assumptions; and the next expected action, which is
the self-use item closure precondition 6 requires. Then
`git push -u origin feature/f109-semantic-dedupe` and report the result. Create
no PR.
