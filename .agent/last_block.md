== STEP T003-docs / F109 — ROUND 15 ==

SESSION 4 of feature F109. Round 15. Rounds so far: 14 done, this is the 15th.
Soft limit is 25 rounds / 7 sessions (docs/agents/self_drive_protocol.md G7,
amend0827 rule 6); at 15 rounds and 4 sessions it is NOT reached, so no scope
report is due. No line of this block is a run of a repeated character, so there
is no run length to recover (§3 checklist item 37).

Scope rule, verbatim as every F109 order must carry it:
RESUMED SESSION ONLY, PROVEN SENDS ONLY.

## Goal

Ship the T003 DOCS: one new built-state document describing what F109 actually
built, registered in the docs index in the SAME commit. Book round 14's PASS,
resolve R-0779, and REGISTER R-0780 — two "deliberate absence" bullets in
`session_sent_index.py` that still tell a reader the ping-pong loop invokes
nothing, three wiring commits after it did. Its repair is round 16's, so this
round registers it and does not touch that file.

## Bundle, in commit order

- C0a  save this block verbatim to `.agent/authored/f109-r15.md`
- C0b  mirror it to `.agent/last_block.md`
- C1   apply PLAN15 to `.agent/plan.md`            (FIRST substantive commit)
- C2   append RECORD15 to `.agent/live_review.md`  (verdict, resolution, new id)
- C3   create `docs/system/semantic-dedupe-v1.md` from DOC, AND apply
        PAIR IDX1 and PAIR IDX2 to `docs/README.md` — ONE commit, both paths
- C4   rewrite `.agent/handoff.md`

## Change set — these paths and nothing else

    .agent/authored/f109-r15.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    docs/system/semantic-dedupe-v1.md
    docs/README.md
    .agent/handoff.md

## Constraints

1. EVERY slice below is applied BYTE FOR BYTE — no rewrap, no re-indent, no
   improvement. If a slice looks wrong, apply it anyway and declare it in the
   handback; that is how a reviewer mistake becomes visible rather than becoming
   a silent correction.
2. `.agent/live_review.md` ends WITHOUT a trailing newline and that convention is
   preserved: append exactly the two bytes `\n\n` then RECORD15, which itself
   ends without one. Never rewrite a landed entry.
3. `docs/system/semantic-dedupe-v1.md` is NEW: create it with the DOC text
   exactly, ending with exactly one trailing newline.
4. C3 lands the doc AND both index rows in ONE commit. A doc registered in a
   later commit is the docs-index drift AGENTS.md forbids.
5. Nothing outside the change set is edited. If the G8 sweep finds something
   else, DECLARE it; do not repair it.
6. `python3 -m pytest` is the pytest route; bare `remedy` may be denied, and
   `python3 -m apps.cli.main <cmd>` is the substitute. Env-var assignment
   (`VAR=x cmd`, `env`, `export`) and `cp` are DENIED by the sandbox: copy with
   `python3 -c "import shutil; shutil.copyfile(a, b)"`, and capture real exit
   codes with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`.
7. Do not quote this handback commit's own insertion count anywhere; it cannot
   exist while the text stating it is written (§3 checklist item 14).
8. Never force-push, never work on main, never create or merge a PR this round.

## SLICE PLAN15 — the whole of `.agent/plan.md`

BEGIN PLAN15
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

Round 15, session 4. The T003 DOCS: `docs/system/semantic-dedupe-v1.md`
describes the built state — the sent-hash index, the composition hook,
the kill switch, the trace record and the measured savings — and is
registered in `docs/README.md` in the same commit. Also book round 14's
PASS and resolve `R-0779`, and REGISTER `R-0780`: two deliberate absence
bullets in `session_sent_index.py` still tell a reader the loop invokes
nothing, three wiring commits after it did. This round does not touch
that file.

## Next Steps

- Repair `R-0780` in `packages/orchestration/session_sent_index.py`.
- The integration gate (docs/agents/integration_gate.md).
- The closure sequence (docs/roadmap/STATUS_closure_protocol.md), which
  also runs the single consolidation pass on the checklist of
  docs/agents/planner_reviewer_prompt.md section 3.

## Risks

- Nothing dedupes in production: every concrete adapter returns
  `supports_resume = False`, so the mechanism is suite-only today. The
  doc states this plainly rather than leaving it to be discovered.
- The measurement function is a library, consumed by the T003 fixture
  and by no production caller. The doc states that too.
- The open finding set is a SET DIFFERENCE, not a subtraction: two ids
  carry two `Done:` lines each. That is `R-0778`.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
END PLAN15

## SLICE RECORD15 — appended to `.agent/live_review.md`, three paragraphs

BEGIN RECORD15
Gate: F109 R14 — the round 14 entry. VERDICT PASS, over the range `5fe32449..d52a5371`. THE REVIEWER RE-RAN ALL FIFTEEN SUITES RATHER THAN READING THE HANDBACK, in two serial processes: 676 passed for the first eight and 268 for the remaining seven, 944 in total at exit 0, and every per-suite figure the handback stated is reproduced — `test_semantic_dedupe.py` at 130 and `test_prompt_trace.py` at 54, up from 128 and 49 by exactly the seven cases SPEC H ordered, with the other thirteen identical to their base. THE PRODUCTION DIFF WAS READ IN FULL: `git log --numstat` gives C4 as 104 insertions and ZERO deletions on `packages/orchestration/prompt_trace.py`, so the insert-only shape G4(a) demanded is confirmed from the tool rather than from the report, and every commit is under the 500-insertion cap of AGENTS.md DECISION F104 D1. THE LEDGER was recomputed mechanically as a SET DIFFERENCE per `R-0778` and never as a subtraction: 340 registered ids, all distinct; 65 `Done:` lines over 63 distinct resolved ids; open set 277 — matching the handback exactly. TWO INDEPENDENT RED-PROOFS OF THE REVIEWER'S OWN CHOOSING, neither of them one the worker ran, were executed in a disposable worktree detached at `d52a5371` with `__pycache__` purged and `python3 -B`: dropping the ROLE from both the write and the read key of `latest_full_chars` went RED at 1 failed with `assert () == ('builder_context',)`, and inflating `occurrences += 1` to `+= 2` went RED at 3 failed with `assert 2 == 1`, while the unmutated control was exit 0 at 135 passed BOTH before the mutations and after the restore. So the per-role scoping the docstring claims and the exact occurrence count are each PINNED by a case, and the suite is load-bearing rather than merely green. THE ROUND'S EIGHT DECLARED DEVIATIONS WERE READ AND ALL ARE SOUND; deviation 1 is the notable one and the worker was RIGHT to widen SPEC G's honesty branch to `if full is None or spent is None:`, because the reviewer's literal `marker_chars.get(name, 0)` would have claimed a marker cost zero characters and OVER-reported the saving — the exact dishonesty the branch exists to prevent. That is a reviewer error the round repaired, and it belongs in `.agent/prose_slips.md` at the closure consolidation rather than earning an id under amend0827 rule 2. THE TRANSPORT CHAIN THIS VERDICT COVERS is the saved copy, its mirror and the working copy — `sha256sum` gives one digest, `d391081163058c104207886d8beb09eac0a42eec24cc8321d395f2523487e558`, for `.agent/authored/f109-r14.md` and `.agent/last_block.md` — and it is NOT a claim about the emitted bytes, which this workflow cannot measure (§3 checklist item 37). THE TREE is clean and no worktree but the primary checkout and the four pre-existing `remedy/job-*` worktrees remains.

Done: R-0779 — RESOLVED at `79edbcbf` and verified by the reviewer at `d52a5371`. The module docstring of `tests/orchestration/test_semantic_dedupe.py` now opens "Tests for F109 semantic dedupe — the per-session sent-hash index (T001a), the composition hook and its markers (T002), the config kill switch (T002c) and the trace's record of what was not resent (T003c)", so it names no slice the file does not cover; and the real-loop sentence now reads "the later classes deliberately drive the real ping-pong loop against ``FakeProvider`` in a tmp_path, beginning at F109 T001b-ii and continuing through every slice that followed it", which states NO numeral and no "final class". Both halves of the finding's own resolution condition are therefore met, measured on disk and not taken from the handback. The file's remaining positional claim about `_real_manifest_rows` — the worker declared it under G8 and correctly declined to repair it, SPEC F having given two literal pairs and neither reaching that sentence — is NOT part of this resolution and stays declared.

- R-0780 — Low, THE SENT-INDEX MODULE STILL DOCUMENTS ITS OWN WIRING AS ABSENT, THREE WIRING COMMITS AFTER IT LANDED, IN THE ONE PLACE A READER IS TOLD TO LOOK. Raised by the REVIEWER at the F109 R14 gate while reading `packages/orchestration/session_sent_index.py` end to end for the T003 documentation round, and registered rather than slipped because the wrong state is on disk under `packages/` — the amend0827 rule 2 test. MEASURED at `d52a5371`. That module's docstring carries a section headed "Scope boundary — deliberate absences (a reader searching here should find this rather than conclude the wiring was forgotten)", which is exactly the construct AGENTS.md's Code Discoverability Conventions require, and TWO of its three bullets are now FALSE. The second says of `invalidate_on_resume_fallback` that "What is still absent is only the CALL SITES — nothing in ``pingpong_loop.py`` invokes it yet, and wiring those seams is T001b-ii", while `grep -n` puts real calls at `pingpong_loop.py:3469` and `:3818` and `git log -S` dates both to `7451e9c7`, the commit whose own subject is "wire the sent-hash index into the ping-pong loop". The third says of `should_dedupe_segment` and `dedupe_marker_for_segment` that "What is still absent is the COMPOSITION HOOK that calls them — no prompt is rewritten here, and nothing in ``pingpong_loop.py`` invokes either function yet — together with the config plumbing that supplies ``enabled``", while `_dedupe_resumed_segments` calls both at `pingpong_loop.py:936` and `:939` since `24352750`, both `compose_*` functions call that hook since `60343048`, and the config plumbing landed at `b245e1c9`. THE FIRST BULLET WAS EXAMINED AND IS LEFT ALONE DELIBERATELY, so a later reader does not think it was missed: its claim is scoped by the word "here" to this module, and this module genuinely still neither persists the index nor reads it back, even though `pingpong_loop.py` now writes `as_evidence_dicts()` onto `result.session_sent_evidence`. WHY LOW: no behaviour is wrong, no gate is blind, no test is weakened and every suite is green; the damage is confined to prose. WHY IT IS NOT MERELY A SLIP: an absence note is load-bearing documentation by AGENTS.md's own rule, so a reader who searches for "is the composition hook wired?" lands precisely here and is told NO when the answer is YES — a stale absence note is worse than no note, because it converts a search into a confident wrong answer. This is the same CLASS as the open finding `R-0593`, which records two such notes in `packages/orchestration/release_gate.py` and `pyproject.toml`; those are different files under a different feature, so this is a sibling instance and not a duplicate of it under the checklist's item 30 test, and it is the fourth staleness instance on this branch after `R-0749`, `R-0773` and `R-0779`. FIX: restate both bullets to say the call sites exist and name the commits that made them exist. Resolved when no bullet of that section says any part of this module's wiring is absent from `pingpong_loop.py`.
END RECORD15

## DOC — the whole of the NEW file `docs/system/semantic-dedupe-v1.md`

BEGIN DOC
# Semantic Dedupe v1

> Built state of F109 (`docs/roadmap/features/T3_F109.md`, Tier 3). Inside a
> RESUMED provider session, a prompt segment whose exact content has already
> provably reached that session is replaced by a one-line marker instead of
> being sent again; everywhere else the full content is composed unchanged.
> The scope rule of the whole feature binds every mechanism below:
> RESUMED SESSION ONLY, PROVEN SENDS ONLY.

## The sent-hash index (T001)

`packages/orchestration/session_sent_index.py` holds `SessionSentIndex`: per
provider session id, the set of segment SHA-256 digests PROVABLY delivered. The
digests are the ones `ComposedPrompt.manifest_as_dicts()` already produces — no
second hashing scheme — and the module is PURE: no file, no network, no
provider, no import from the rest of `packages.orchestration`. "Proven" is the
load-bearing word: `record_call` records nothing when the call carried an error,
because a failed call did not reach the session, and nothing when the session id
is empty after stripping, because an empty key would become one bucket every
sessionless call shares. Neither case is an error and both are silent; a
malformed manifest row, by contrast, RAISES `SessionSentIndexError` rather than
degrading quietly into a smaller index.

`record_finalized_call` and `invalidate_on_resume_fallback` are the two adapter
seams. `pingpong_loop.py` calls both on the Builder path and again on the
Reviewer path (landed at `7451e9c7`), and writes `as_evidence_dicts()` onto
`result.session_sent_evidence`, so `session_sent_index_from_evidence` rebuilds
after a restart exactly what the evidence proves and never more.

## The composition hook and the marker (T002)

`_dedupe_resumed_segments` in `packages/orchestration/pingpong_loop.py` is the
transform. It rewrites `text` and nothing else, so segment NAMES and RANKS
survive by construction, and it returns the INPUT order rather than a rank sort —
`compose_prompt_segments` sorts afterwards, and re-ordering here would move
segments the cache discipline requires to stay put. The digest it compares comes
from the shipped producer one segment at a time, never from a local `hashlib`
call, so the decision asks the same producer that made the index's entries.

The marker reads `[unchanged: <segment name>, previously provided]`. The name
stays inside it deliberately: the model must still be able to refer to a segment
it is no longer shown, so the marker withholds the content without withholding
the means of asking for it back.

Both `compose_builder_prompt` and `compose_reviewer_prompt` take a
`dedupe_sent_hashes` parameter that BYPASSES dedupe by default (`60343048`), so
the transform runs only for a caller supplying a real set; a non-resuming call
passes `None`, which is the scope rule and not a gap. A segment shorter than
`DEDUPE_MIN_SEGMENT_CHARS` (200, compared with `>=`) is never replaced, because
a marker has a length of its own — 48 and 49 characters for the two names
measured below — so replacing a small segment can cost more than it saves.

## The kill switch (T002c)

`run_pingpong` carries `semantic_dedupe_enabled` and forwards it to both primary
compositions as `dedupe_enabled` (`b245e1c9`). In `should_dedupe_segment` and in
`_dedupe_resumed_segments` alike, `enabled` is consulted FIRST and ALONE: false
returns the segments untouched and consults nothing else, so the switch is
provably and totally off rather than mostly off.

## What the record shows, and what it measures (T003c, T003d)

Every `PromptTraceEntry` carries `deduped_segment_names`, derived from the
composed prompt alone rather than passed in beside it, so the evidence shows
exactly which segments the model did NOT receive again.

`measure_dedupe_savings_from_traces` in `packages/orchestration/prompt_trace.py`
reads a run's own trace entries and reports what that run did not resend. Every
number it returns is MEASURED from recorded evidence. It is deliberately NOT
`estimate_token_savings` in `packages/orchestration/token_economy.py`: that
function compares two ESTIMATES and says so, and one name over both concepts
would make a measured number indistinguishable from a guess.
`unmeasured_segment_names` is the load-bearing field — a segment reported as
deduped whose full-content size never appeared in the entries handed over is
NAMED there and excluded from every total, so "nothing was saved" and "the
saving is not measurable from what you gave me" can never read alike.

Measured at commit `d52a5371` on the two-round resumed fixture chain of
`tests/orchestration/test_semantic_dedupe.py::TestTheRunsOwnTraceMeasuresWhatItWithheld`,
whose second case re-runs the identical chain with `semantic_dedupe_enabled=False`
as the discriminator:

| Reading | Dedupe on | Dedupe off |
|---|---:|---:|
| Segments withheld | 2 (`builder_system`, `reviewer_system`) | 0 |
| Characters avoided | 556 | 0 |
| Characters spent on markers | 97 | 0 |
| Net characters saved | 459 | 0 |
| Names that could not be measured | none | none |

The two markers cost 97 characters against 556 of withheld content. As with
F106's measured reduction, this comparison proves the DIRECTION is real and
measured on a small fixture; it is not a claim about production magnitude, and
the saving scales with how much of the world a real resumed round would
otherwise resend rather than with this fixture's own size.

## What this does NOT do

- **Nothing dedupes in production today.** Dedupe fires only inside a resumed
  session, and every concrete adapter in
  `packages/orchestration/pingpong_provider.py` returns
  `supports_resume = False` — `ClaudeProvider`, `ClaudeCliProvider` and
  `OllamaPingPongProvider` alike. Only `FakeProvider`'s test-only constructor
  override ever returns `True`, so the mechanism is exercised by the suite and
  is inert on every real run.
- A dedupe never crosses session ids: each session's hashes live in their own
  set, and an empty session id is never used as a key.
- A resume fallback forgets the resumed session entirely — once it has fallen
  back to full context, nothing about what the model holds is proven.
- The measurement function is a LIBRARY. The T003 fixture above is its only
  caller; `run_pingpong` does not call it and no report renders it yet. A run's
  savings stay recomputable from the traces the run already wrote.
- Cross-session caching, provider-side cache mechanics and prompt CONTENT are
  out of scope — the feature file's own "Do not touch".

## Related

- `docs/roadmap/features/T3_F109.md` — the target spec and its acceptance list.
- [session-resume-v1.md](session-resume-v1.md) — the resume machinery this
  feature's scope rule depends on, and the reason nothing dedupes in production.
- [cache-optimal-prompt-ordering-v1.md](cache-optimal-prompt-ordering-v1.md) —
  the ranked segment composition that dedupe rewrites one segment of.
END DOC

## PAIR IDX1 — the quick-find table of `docs/README.md`

Containment test, run mechanically before emission: TO contains FROM: false.
The new row goes BETWEEN the two FROM lines, so the TO does not contain the FROM
contiguously and this is a REWRITE, not an append. FROM 0x and TO 1x after C4 is
therefore attainable and IS the proof. FROM counted at `d52a5371`: exactly 1x.

BEGIN IDX1_FROM
| self-dogfood | [self-dogfood-execution-v0.md](system/self-dogfood-execution-v0.md) | system |
| session resume | [session-resume-v1.md](system/session-resume-v1.md) | system |
END IDX1_FROM

BEGIN IDX1_TO
| self-dogfood | [self-dogfood-execution-v0.md](system/self-dogfood-execution-v0.md) | system |
| semantic dedupe | [semantic-dedupe-v1.md](system/semantic-dedupe-v1.md) | system |
| session resume | [session-resume-v1.md](system/session-resume-v1.md) | system |
END IDX1_TO

## PAIR IDX2 — the system-docs table of `docs/README.md`

Containment test, run mechanically before emission: TO contains FROM: false.
REWRITE for the same reason as IDX1, and the same FROM 0x / TO 1x proof applies.
FROM counted at `d52a5371`: exactly 1x.

BEGIN IDX2_FROM
| [self-use-track-v1.md](system/self-use-track-v1.md) | Self-use track: the curated queue, the job-file format, one item consumed per feature close |
| [session-resume-v1.md](system/session-resume-v1.md) | Provider session resume + delta-prompt shrink: capability surface, resume threading, fallback-once, and the measured reduction |
END IDX2_FROM

BEGIN IDX2_TO
| [self-use-track-v1.md](system/self-use-track-v1.md) | Self-use track: the curated queue, the job-file format, one item consumed per feature close |
| [semantic-dedupe-v1.md](system/semantic-dedupe-v1.md) | Semantic dedupe inside a resumed session: the sent-hash index, the marker hook, the kill switch, and the measured savings |
| [session-resume-v1.md](system/session-resume-v1.md) | Provider session resume + delta-prompt shrink: capability surface, resume threading, fallback-once, and the measured reduction |
END IDX2_TO

## Done when — the eight gates. RUN each one and record its REAL exit code.

Every gate below runs at a commit STRICTLY EARLIER than C4, the commit that
writes the handback, so the handback can honestly quote all eight.

G1 TRANSPORT, one comparison and no chain. Run
   `cmp .remedy-wt/f109-r15.md .agent/authored/f109-r15.md` and report the exit
   code. That scratch file is the REVIEWER'S OWN original, so this comparison
   proves real transport and not merely your own self-consistency. Then report
   `sha256sum .agent/authored/f109-r15.md .agent/last_block.md` — one digest
   twice.

G2 THE PLAN. Extract PLAN15 by delimiter index (the lines strictly between
   `BEGIN PLAN15` and `END PLAN15`) and `cmp` it against `.agent/plan.md` after
   C1: exit 0, no output. Report `wc -l .agent/plan.md`, which must be under 50
   (AGENTS.md), and `grep -c '^## Goal'` and `grep -c '^## Next Steps'`, each 1.

G3 THE RECORD APPEND, three readings, and this is the only slice that earns full
   byte forensics this round.
   (a) ARITHMETIC. Report the base size and base sha256 of `.agent/live_review.md`
       at `d52a5371`, the length S of the appended bytes, the new size, and
       whether base + S equals the new size. Confirm the file still ends WITHOUT
       a trailing newline.
   (b) A SECOND READER THAT COUNTS NO BYTE, covering the WHOLE appended region.
       Split the entire file on blank-line boundaries into units. Let N be the
       paragraph count of RECORD15 as YOUR SCRIPT COUNTS IT from the slice — do
       not take N from this block. Assert the LAST N units equal RECORD15's N
       paragraphs IN ORDER, printing each one's opening 60 characters.
   (c) A NEGATIVE CONTROL ON THE FIRST APPENDED PARAGRAPH. Copy the file to
       `.remedy-wt/live_review_negative_control_r15.md`, flip one byte INSIDE
       the FIRST appended paragraph there, and show reader (b) REJECTS the copy
       while ACCEPTING the tracked file. Report the tracked sha256 before and
       after to show it never moved, then delete that scratch file BY ITS EXACT
       PATH and report `os.path.exists` on that exact path as False.
   (d) COUNTS, AS A SET DIFFERENCE and never a subtraction (`R-0778`). Read the
       base from `git show 5fe32449:.agent/live_review.md`, never by rewinding
       the tracked file, and report five figures for base and five for the new
       state: registered ids, DISTINCT registered ids, `Done:` lines, DISTINCT
       resolved ids, and `len(set(registered) - set(resolved))`. Also report
       `grep -c '^Gate: F109 R14 — '` = 1, `grep -c '^Done: R-0779 — '` = 1 and
       `grep -c '^- R-0780 — '` = 1.

G4 THE INDEX PAIRS, both of which are REWRITES by the containment test recorded
   beside each. For PAIR IDX1 and PAIR IDX2 in `docs/README.md`, report the count
   of each FROM BEFORE C3 (each must be 1) and AFTER C3 (each must be 0), and the
   count of each TO after C3 (each 1).

G5 THE DOC IS REAL AND REGISTERED. After C3 report: the doc exists and its
   `wc -l`; `git show --numstat <C3>` naming BOTH new paths, proving ONE commit;
   `grep -c 'semantic-dedupe-v1.md' docs/README.md` = 2; and that EVERY relative
   markdown link in the new doc resolves on disk, listing each target and
   whether it exists — the reading
   `tests/docs/test_docs_consistency.py::test_every_relative_markdown_link_exists`
   will make, so make it yourself first.

G6 THE SUITES, run SERIALLY, one process finishing before the next starts. Report
   the collected count and REAL exit code of each:
   - `python3 -m pytest tests/docs/ -q`
   - `python3 -m pytest tests/orchestration/test_semantic_dedupe.py -q`
   - `python3 -m pytest tests/orchestration/test_prompt_trace.py -q`
   - `python3 -m pytest tests/orchestration/test_session_resume.py -q`
   - `python3 -m pytest tests/orchestration/test_pingpong.py -q`
   - `python3 -m pytest tests/orchestration/test_pingpong_cli.py -q`
   - `python3 -m pytest tests/cli/test_golden_path.py -q`
   The last is the mandatory canary; `tests/docs/` is listed because this round
   touches `docs/`. NOTHING may go red and no count may FALL — the reviewer
   measured the six that are not `tests/docs/` at `d52a5371` as 130, 54, 27, 34,
   173 and 42.

G7 THE DOC'S FACTUAL CLAIMS, RE-MEASURED BY YOU rather than trusted. The doc
   asserts things about code it does not live in, so verify each and report the
   reading: (a) `supports_resume` returns False for `ClaudeProvider`,
   `ClaudeCliProvider` and `OllamaPingPongProvider` in `pingpong_provider.py`,
   and `FakeProvider` alone takes it as a constructor override; (b) each of the
   commits `7451e9c7`, `60343048` and `b245e1c9` exists (`git cat-file -e`);
   (c) `DEDUPE_MIN_SEGMENT_CHARS` is 200 and the comparison in
   `should_dedupe_segment` is `>=`; (d) `estimate_token_savings` exists in
   `packages/orchestration/token_economy.py`; (e) the two marker strings for
   `builder_system` and `reviewer_system` are 48 and 49 characters, summing to
   the 97 the table states. Any reading that disagrees with the DOC is a finding
   against the REVIEWER: report it, apply the slice unchanged, and do not
   silently correct the doc.

G8 THE TREE AND THE SWEEP. `git status --porcelain` must be EMPTY and
   `git ls-files .remedy-wt` must return nothing. Report each commit's insertion
   count from `git show --numstat` — the `+` column ONLY, per AGENTS.md DECISION
   F104 D1 — for every commit of this round EXCEPT C4, and compare those figures
   cell by cell against your own `## Commits` table, which must carry the same
   numbers (§3 checklist item 28). Then RE-READ each file this round touched, end
   to end, and report every sentence that is now stale — including any you did
   NOT repair, with the reason. Repair nothing outside the change set.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It has NO
length cap. It must carry: the SESSION NUMBER (4) and round (15); the item-status
table with every one of C0a, C0b, C1, C2, C3, C4 appearing exactly once with
`done`, `skipped` or `deviated` and a reason; a per-commit changed-files table
with the `+/-` column; ONE LINE PER GATE G1 through G8 with its real reading; the
open-finding count as a SET DIFFERENCE; your deviations and assumptions; and the
next expected action. Then `git push -u origin feature/f109-semantic-dedupe` and
report the result. Create no PR.
