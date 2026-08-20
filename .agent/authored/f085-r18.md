# F085 R18 — record the R17 PASS and promote three standing rules into the checklist

Feature T2_F085 Sandbox hardening (stage 1) · Round R18 · Branch feature/f085-sandbox-hardening
Base of this round: the R17 handback commit, `git rev-parse HEAD` at start = 88dbcefa.
Fortschritt: ~68 % (T001 gebaut · R13-R17 PASS · T002a: Builder-Site und CLI-Half fertig ·
`stream_evidence.py`, T002b-d, T003 offen) — Schätzung.

## Goal

First the record: R17 passed the reviewer's gate and that verdict is written by C1. Then the work
R-0508 and R-0510 have stayed open for since R16 — three standing rules stop being reviewer habit
and start binding on disk as checklist items 15, 16 and 17 of
`docs/agents/planner_reviewer_prompt.md` §3. C3 then resolves both findings, after the promotion
exists and not before.

Evidence already taken by the reviewer, reported so the worker does not repeat it: both pairs below
were applied to a disposable worktree at 88dbcefa, where PROMF occurs exactly once, the checklist
region then parses to a contiguous 1 through 17 with no repeat, `.agent/plan.md` lands at 40 lines,
`tests/test_agent_tooling.py` is 10 passed 1 skipped, `tests/docs/` is 295 passed and the canary is
42 passed. The state readers were run EIGHT times in that tree and read 157 passed every time.

## Bundle — in this order, none added, dropped or reordered

- C0a `docs(f085): save the R18 step block verbatim` — `.agent/authored/f085-r18.md`
- C0b `docs(f085): mirror the R18 block into last_block` — `.agent/last_block.md`
- C1 `docs(review): record the R17 PASS` — `.agent/live_review.md`
- C2 `docs(agents): promote three standing rules into the pre-emission checklist` —
  `docs/agents/planner_reviewer_prompt.md`
- C3 `docs(review): resolve R-0508 and R-0510 now that the promotion has landed` —
  `.agent/live_review.md`
- C4 `docs(f085): advance the plan to the stream-evidence round` — `.agent/plan.md`
- C5 `docs(f085): rewrite the handback for R18` — `.agent/handoff.md`

C3 is a separate commit ON PURPOSE and must not be folded into C1: a resolution claiming a promotion
that had not yet landed would assert on disk something no commit had done
(planner_reviewer_prompt.md §4.4).

## Change set — exactly these paths, nothing else

`.agent/authored/f085-r18.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
`.agent/handoff.md`, `docs/agents/planner_reviewer_prompt.md`. Nothing under `packages/`, `tests/`,
`apps/` or `scripts/`; no file under `docs/` other than the one named. `.agent/context.md` and
`.agent/decisions.md` are NOT touched. `docs/README.md` is NOT touched: this promotion adds items to
a document already registered in that index, and registration is owed for new or renamed docs only.

## Constraints

1. `cp` and the `remedy` CLI are denied here: copy with `shutil.copyfile` and prove the BYTE
   property, never the tool. Gate scratch lives under the gitignored `.remedy-wt/`.
2. Extract every slice programmatically by its one-line marker pair and apply it byte-verbatim,
   never retyped, reformatted or reworded: the review slices' quoted rule text and backticks are
   prose and land as prose.
3. Apply each FROM/TO pair by locating the FROM exactly once and replacing it with the TO; if it
   does not occur exactly once, STOP and report. Pair shapes, classified MECHANICALLY by containment
   at build time and printed here rather than judged by eye: PROMF→PROMT APPEND, PLANF→PLANT
   REWRITE. No "FROM 0x" reading is ordered for PROMF — it legitimately survives inside its own TO.
4. This round orders NO destructive check and no mutation red-proof. No gate below needs a
   disposable tree, and no worktree is added, removed or pruned.
5. Re-read `.agent/STOP` from disk before the FIRST commit and again before the LAST. If it exists
   at either point, finish the commit in flight, write the handback and end.

<<<SLICE RECORD1>>>
Gate: R17 — PASS, the round that completed T002a's CLI half. All ten ordered gates were re-run by the
reviewer over 396ad913..88dbcefa and every one reproduces the handback's reading. TRANSPORT,
disk-to-disk and not by digest fallback: the committed `.agent/authored/f085-r17.md` blob, the
committed `.agent/last_block.md` blob and both working copies are byte-EQUAL at sha256
cc496f97e15b8feb9a82368c78493c03f48f1a64c8302dca265874e4fdebb195, 19911 B, 309 lines. BOTH APPEND
COMMITS HOLD THEIR SHAPE: for C1 the pre-commit blob 6c374ca1 (286462 B) is a byte-exact PREFIX of
the post-commit file 98be125d (289062 B) and the remainder is byte-equal to blank plus RECORD1; for
C3 the pre-commit blob 98be125d is a prefix of 27c1e4ef (291333 B) and the remainder is blank plus
DONE1 plus blank plus DONE2. Each slice occurs exactly ONCE in the file at HEAD, no marker line
survives anywhere in it, and HEAD equals the C3 blob. THE ARITHMETIC: 125 / 4 / 0 at base and after
C1 alike — a record registers no id, exactly as the block predicted — against 125 / 6 / 0 at HEAD,
the open set moving 121 to 119, registered difference EMPTY, resolved difference exactly R-0507 and
R-0509, no duplicate id and no resolution naming an unregistered id; max R-0510, next free R-0511.
THE MIGRATION IS COMPLETE AND MEASURED BY AST, NOT BY TEXT: over `pingpong_provider.py` at HEAD,
`_resolve_version`, both defs of `_call`, `_call_reviewer_structured` and `_guarded_cli_run` hold
ZERO `subprocess.run/Popen/call/check_output` call nodes, and so does the WHOLE MODULE. THE GOLDENS
ARE NOT VACUOUS: the eight-file provider suite reads 341 passed at C1 in a disposable worktree at
that commit and 346 at HEAD in the primary checkout — the two numbers are NOT equal and the
difference is exactly the five goldens C2 adds. Those goldens spawn a REAL child, because `_provider`
writes the body through `textwrap.dedent` to an executable stand-in, so the indented `_ENVELOPE` is
valid Python at the child and the "HELLO" assertion could not pass against a mock. TWO INDEPENDENT
RED CONTROLS, run by the reviewer in a disposable worktree at HEAD and not inherited from the block:
reverting the mock target alone reddens ELEVEN tests in `test_structured_cli_envelope.py`, which is
the number DONE1 puts on disk, and restoring the stdlib spawn at the `_call` site reddens
`test_the_probe_and_the_runner_hold_no_subprocess_spawn`, so the two AST assertions C2 adds do bite.
The five goldens stay GREEN under that second mutation, which is correct and worth stating: they pin
BEHAVIOUR across the migration while the AST guard pins the MECHANISM, and neither substitutes for
the other. THE SEAM PRESERVES ITS CONTRACT: `_guarded_cli_run` re-raises a wall trip as
`subprocess.TimeoutExpired`, republishes a signal death in the -SIGNUM form and decodes both streams
the way `text=True` did, so the `except subprocess.TimeoutExpired` handler each call site already
carried still catches. THE PLAN PAIR: PLANF 0x and PLANT 1x at HEAD, `.agent/plan.md` at sha256
8c68c6ae324fd779094990ee19c5961b35f6df4fcdb6639ef8f085aecc65c9f2, 2704 B and 44 lines under its cap,
`## Goal` and `## Risks` byte-identical to base, `## Next Steps` parsing to 1, 2, 3, 4 with no
repeat. Scoped ruff is exit 0 on all three touched paths, the state readers are 157 passed and the
canary 42 passed. BEYOND THE ORDERED GATES the reviewer ran the two provider readers G7's file list
does not cover — `test_pingpong_cli.py` at 172 passed and `test_run_manifest.py` at 44 passed — and
grepped the repository for surviving patches of `pingpong_provider.subprocess`, of which there are
none; the seam has no reader left on the stdlib path. The change set is exactly the declared paths
with 0 outside; insertions are 309, 225, 28, 45, 25 and 8 before the handback commit, which is itself
32, none over 500; seven single-parent commits, twelve reflog entries all `commit:`-prefixed, no
amend, rebase, reset or force-push; the tree is clean and `git worktree list` is ONE line. The
handback measures 80 lines against its own declaration of 80, and its stated-cause deviation is
accurate. LAST_REVIEWED_SHA advances to 88dbcefa.
<<<END RECORD1>>>
<<<SLICE DONE1>>>
Done: R-0508 — the counter-measure is on disk. `docs/agents/planner_reviewer_prompt.md` §3 now
carries checklist item 15, "Pair shapes are classified by a containment test, never by eye", which
THIS SAME BLOCK orders into that file — so the sentence you are reading names a rule that exists
rather than one a later round is expected to write, which is exactly what item 11 requires of it.
The item states the METHOD the finding faulted: every FROM/TO pair is tested mechanically for
containment and the answer printed beside that pair, one reading per pair, never one generalised to
the rest. It names its neighbour on purpose, because item 4 already stated the RULE and the R15
block still failed while satisfying it — it ran the check for the pair it suspected and eyeballed
the others. A rule and the method that produces its input are two different checks, and only the
second was missing.
<<<END DONE1>>>
<<<SLICE DONE2>>>
Done: R-0510 — the counter-measure is on disk as checklist item 16, "No heading states a count of the
contents beneath it", ordered into `docs/agents/planner_reviewer_prompt.md` §3 by THIS SAME BLOCK.
The item carries the part of the finding that mattered: not that a heading said SIX over a body of
SEVEN, but that the R15 block DID sweep its Bundle heading and left the Change set heading behind,
so the fix reached the instance that was noticed instead of the class. It therefore ends by ordering
the sweep over EVERY heading in a block rather than the one that changed, which is the R-0417 shape
the finding named. Item 17 lands in the same commit and closes the third counter-measure this round
was held open for — the arity rule R-0509's resolution said would be promoted here — so no standing
rule of that family is left living only in reviewer habit.
<<<END DONE2>>>
<<<SLICE PROMF>>>
  Why this is on disk and not a habit: item 2 has recurred six times across
<<<END PROMF>>>
<<<SLICE PROMT>>>
  15. **Pair shapes are classified by a containment test, never by eye.** Finding
      R-0508. Before emission every FROM/TO pair is tested MECHANICALLY for whether the
      TO contains the FROM verbatim, and the answer is printed beside that pair in the
      block's constraints — one reading per pair, never one reading generalised to the
      rest. Item 4 states the RULE that an APPEND claim requires containment; this one
      governs the METHOD by which the claim is produced, which is where R-0508 landed:
      the R15 block ran the check for the single pair it suspected, wrote "Every other
      pair is a REWRITE", and was wrong about an import insertion whose TO kept its
      anchor line. An import pair that keeps its anchor is the most common
      append-shaped pair in this repository, so the eye fails exactly where it is most
      likely to be trusted. Nothing broke that round only because no gate ordered the
      unsatisfiable "FROM 0x" reading; the next block to order one pays for it.
  16. **No heading states a count of the contents beneath it.** Finding R-0510. A
      section heading that restates a number its own body defines — "exactly these SIX
      paths", "the four commits" — drifts the moment an item is added, and the heading
      is the half nobody re-reads. Write the heading without the numeral. Item 11
      forbids a hand-counted numeral about the block's own PARTS inside a convention
      paragraph; this one forbids it in a HEADING over a list the reader can count
      unaided, which is where the R-0402 / R-0404 / R-0436 family kept resurfacing
      after item 11 was written. The R15 instance is the shape to recognise: that block
      DID apply the rule to its Bundle heading, because that list had just grown, and
      left the Change set heading saying SIX over a body of SEVEN. The fix reached the
      instance that was noticed instead of the class — the R-0417 staleness shape — so
      sweep every heading in the block, not the one that changed.
  17. **A pair that changes a structure's arity spans the whole structure.** Finding
      R-0509. When a TO adds or removes an entry of a numbered list, a table, or any
      other structure whose items carry positional labels, the FROM spans that WHOLE
      structure rather than a prefix of it, so the surviving entries are renumbered by
      the pair itself. A prefix-shaped FROM leaves the old labels standing on the
      untouched tail, and the applied file then carries two items numbered 2 — which is
      what `.agent/plan.md` held for a round. Item 4 asks what SHAPE a pair is and item
      15 asks how that shape was determined; this one asks how far the FROM must REACH,
      a question about the target's structure rather than about the pair's own bytes,
      and no containment test can answer it.
  Why this is on disk and not a habit: item 2 has recurred six times across
<<<END PROMT>>>
<<<SLICE PLANF>>>
## Current Step
R17, this round: record the R16 PASS, migrate R-0507's coupled unit — `_call`,
`_call_reviewer_structured` and the envelope test's mock move as one commit — with
five behaviour-equality goldens, then resolve R-0507 and R-0509. T002a's CLI half is
complete after this round; every `ClaudeCliProvider` spawn runs under the guard.

## Next Steps
1. Promote three standing rules into docs/agents/planner_reviewer_prompt.md §3, which
   is what R-0508 and R-0510 are still open for: classify pair shapes mechanically,
   let no heading count its own contents, and span a whole structure when a pair
   changes its arity. Reviewer habit binds nothing until it is on disk.
2. `stream_evidence.py`:595 is T002a's last site and is NOT a `subprocess.run` swap:
   it streams incrementally where `run_guarded` buffers, so its shape is decided first.
3. `_StreamPump` gains a lock and a `snapshot()` so PARTIAL output survives a
   bounded drain. It still returns `b""` for a stream whose pump never reached
   EOF, which `streams_complete` reports honestly but which loses bytes.
4. T002b-d, then T003 — network posture, limitations document, README link.
<<<END PLANF>>>
<<<SLICE PLANT>>>
## Current Step
R18, this round: record the R17 PASS, promote three standing rules into
docs/agents/planner_reviewer_prompt.md §3 as checklist items 15, 16 and 17, then
resolve R-0508 and R-0510 — the two findings that stayed open for exactly that
promotion. Reviewer habit binds nothing until it is on disk.

## Next Steps
1. `stream_evidence.py`:595 is T002a's last site and is NOT a `subprocess.run` swap:
   it streams incrementally where `run_guarded` buffers, so its shape is decided first.
2. `_StreamPump` gains a lock and a `snapshot()` so PARTIAL output survives a
   bounded drain. It still returns `b""` for a stream whose pump never reached
   EOF, which `streams_complete` reports honestly but which loses bytes.
3. T002b-d, then T003 — network posture, limitations document, README link.
<<<END PLANT>>>

## Application order

C1 appends RECORD1 to `.agent/live_review.md`, preceded by exactly one blank line, appending only.
C2 applies PROMF→PROMT to `docs/agents/planner_reviewer_prompt.md`. C3 appends DONE1 then DONE2 to
`.agent/live_review.md`, each preceded by exactly one blank line. C4 applies PLANF→PLANT to
`.agent/plan.md`.

## Gates — every one is RUN and its real exit code recorded; "green" as a word is a finding

This session's Bash tool rejects `$?`, loops and command substitution BY FORM: read every exit code
as a real `subprocess.returncode` from `python3`.

G1 HYGIENE. `git status --porcelain` EMPTY before EVERY commit in the bundle; `.agent/STOP` re-read
from disk before the first and the last; `git worktree list` prints ONE line.

G2 TRANSPORT. `.agent/authored/f085-r18.md` after C0a and `.agent/last_block.md` after C0b are
byte-EQUAL: report one sha256, byte length and line count for both. C0b copies the COMMITTED C0a
blob, never the scratch file. Per docs/agents/self_drive_protocol.md §2.1 an in-session delegation
has no transport hop, so the hash-stamp ritual is replaced by exactly this byte-equality proof: there
is no reviewer scratch digest to check a receipt against, and none is ordered.

G3 APPEND SHAPE, twice. For C1 and again for C3: the pre-commit blob is a byte-exact PREFIX of the
post-commit file, HEAD equals it, and the remainder is byte-equal to blank + the ordered slices for
that commit — RECORD1 for C1, and DONE1 then DONE2 for C3. Each occurs exactly ONCE in the whole
file at HEAD, and neither commit adds a marker line. Report both numstat pairs as READINGS.

G4 ARITHMETIC over `.agent/live_review.md`, regexes `^- R-\d+ — `, `^Done: R-\d+ — `,
`^Landed: R-\d+`. Base 125 / 6 / 0, 119 open; after C1 unchanged at 125 / 6 / 0, because a record
adds no id; expected at HEAD 125 / 8 / 0, 117 open, two resolutions and NO registration. Report the
reading after C1 as well as at HEAD, both symmetric differences, duplicate-id counts, any resolution
naming an unregistered id, and the max and next-free id.

G5 THE PROMOTION. PROMF occurs exactly ONCE in `docs/agents/planner_reviewer_prompt.md` at HEAD — it
is an APPEND-shaped pair, so no "0x" reading is ordered for it and one that came out 0 would mean the
anchor had been destroyed. Each of the three item titles `Pair shapes are classified`, `No heading
states a count` and `spans the whole structure` occurs exactly once AMONG THE LINES C2'S OWN DIFF
ADDS. Then, scoped to the region between `**Pre-emission block checklist` and the PROMF line, the
numbers matched by `^  (\d+)\. \*\*` read 1 through 17 with no repeat and no gap — item 17's own rule
holding on the very commit that writes it. Report the parsed sequence.

G6 PLAN PAIR. PLANF occurs 0 times at HEAD and PLANT once. Report `.agent/plan.md` sha256, bytes and
a line count under 50, with `## Goal` and `## Risks` byte-IDENTICAL to base, and report the ordered
numbers `## Next Steps` parses to — they must have no repeat.

G7 DOC READERS. `python3 -m pytest tests/test_agent_tooling.py tests/docs/ -q` exits 0. That file is
the only one under `tests/` naming `planner_reviewer_prompt`, and `tests/docs/` owns the docs
structure this commit edits. No ruff gate is ordered and none is skipped by oversight: the change set
contains no `.py` file, so there is nothing in it for ruff to read.

G8 STATE READERS, because this round rewrites `.agent/` state: `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -q` exits 0.
CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` exits 0 with 42 passed. Report the
state-reader count as a READING rather than matching it against a number. That suite spawns wrapper
processes under flock and timeouts and is timing-sensitive: the reviewer saw one red run it could not
reproduce in eight further runs, all 157 passed. If a run comes out red, report the failing test id,
re-run `tests/regression/test_resource_safety.py` alone three times and report all four readings. A
failure that reproduces every time is a STOP; one that does not is recorded with its tally and the
round continues.

G9 COMMIT HYGIENE, three readings. `git diff --name-only 88dbcefa..HEAD` measured BEFORE C5 equals
the declared paths minus `.agent/handoff.md` — report the list; 0 paths outside it. The `+` column of
`git show --numstat` for C0a, C0b, C1, C2, C3 and C4: none exceeds 500. C5's own count is ordered
nowhere, because a commit cannot measure itself; report it in the round report instead.
`git log --format=%h %p 88dbcefa..HEAD` shows ONE parent per commit and a linear chain; `git reflog`
shows every entry prefixed `commit:`, no amend, rebase, reset or force-push.

## Done when

Every commit in the bundle exists in order, the branch is pushed, every gate has been RUN with its
exit code recorded, `git status --porcelain` is empty, and `.agent/handoff.md` is rewritten per
docs/agents/handback_template.md with an item-status table covering C0a through C5. Run `gh pr list
--state open --json number,headRefName,baseRefName,isDraft` after the final push and report its
output; create NO pull request and merge nothing. Report what the commands PRINTED — a gate whose
result you did not read is a finding. If a gate contradicts this block, report the contradiction and
STOP: never repair text to make a number come out, never widen the change set. Declare every
deviation.
