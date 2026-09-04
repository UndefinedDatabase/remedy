STEP T002/2 - F262 List commands v2, ROUND 4
FEATURE F262 - List commands v2 (Tier 2) - SESSION 1, ROUND 4

Goal
  Ship T002 batch 2: memory.list gains `updated_at` in --json (the
  model already has the field; the json branch simply omits it) and
  both created/updated in its text output. Single file, single test
  file. No model or store changes, no behavior change beyond the
  printed/exported fields.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f262-r4.md
  C0b mirror it to .agent/last_block.md
  C1  append GATE3 to .agent/live_review.md - books round 3's PASS
      verdict (the reviewer's own, independently re-verified)
  C2  apply CODE PAIR M1 and CODE PAIR M2 to
      apps/cli/commands/memory.py, and add the two new test methods
      per the TEST SPEC below to tests/test_grouped_cli.py (one commit)
  C3  apply PLAN5 to .agent/plan.md
  C4  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f262-r4.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - apps/cli/commands/memory.py (C2) -
  tests/test_grouped_cli.py (C2) - .agent/plan.md (C3) -
  .agent/handoff.md (C4)

CODE PAIR M1 (apps/cli/commands/memory.py) - APPEND-shaped (TO contains
FROM verbatim - this is a same-place insertion, not a rewrite). FROM is
long enough to be unique to `_cmd_memory_list` specifically (it starts
at that function's own local import line, `list_memory`, which differs
from the near-identical `_cmd_memory_recall` function's `recall_memory`
import a few lines above it in the same file - the two functions'
json-dict blocks are otherwise byte-identical, which is exactly why a
shorter FROM would have matched twice).
<<<BEGIN PAIR_M1_FROM>>>
    from packages.memory.local_gateway import list_memory

    entries = list_memory(project_id=project_id, job_id=job_id)

    if json_output:
        output = [
            {
                "id": str(e.id), "key": e.key, "value": e.value,
                "summary": e.summary, "tags": e.tags,
                "approved": e.approved, "source_type": e.source_type,
                "validity": e.validity, "review_status": e.review_status,
                "scope": e.scope, "evidence_refs": e.evidence_refs,
                "created_at": e.created_at,
<<<END PAIR_M1_FROM>>>
<<<BEGIN PAIR_M1_TO>>>
    from packages.memory.local_gateway import list_memory

    entries = list_memory(project_id=project_id, job_id=job_id)

    if json_output:
        output = [
            {
                "id": str(e.id), "key": e.key, "value": e.value,
                "summary": e.summary, "tags": e.tags,
                "approved": e.approved, "source_type": e.source_type,
                "validity": e.validity, "review_status": e.review_status,
                "scope": e.scope, "evidence_refs": e.evidence_refs,
                "created_at": e.created_at,
                "updated_at": e.updated_at,
<<<END PAIR_M1_TO>>>

CODE PAIR M2 (apps/cli/commands/memory.py) - REWRITE (TO does not
contain FROM verbatim), the text-branch print line inside the SAME
function, further down.
<<<BEGIN PAIR_M2_FROM>>>
            print(f"  {e.key}: {e.value}{approved_mark}{tags_str}  (id={str(e.id)[:8]})")
<<<END PAIR_M2_FROM>>>
<<<BEGIN PAIR_M2_TO>>>
            print(f"  {e.key}: {e.value}{approved_mark}{tags_str}  (id={str(e.id)[:8]}, created={e.created_at}, updated={e.updated_at})")
<<<END PAIR_M2_TO>>>

TEST SPEC for C2 - two new test methods added to the EXISTING
`TestMemoryCLIContract` class in tests/test_grouped_cli.py (it already
holds `test_list_json_has_version_1` and the `test_store_approved_*`
pair right above it - place these two new methods directly after
`test_store_approved_false_by_default`, before `test_approved_is_store_
true_in_argparse`). Both follow the exact setup pattern those existing
methods already use (monkeypatch REMEDY_DATA_DIR, redirect sys.stdout
to a StringIO via monkeypatch.setattr, call `_cmd_memory_store` then
`_cmd_memory_list`, parse the second buffer):
  - `test_list_json_has_updated_at_key`: store one entry
    (`_cmd_memory_store("test_key", "test_value")`), list with
    `json_output=True`, assert `"updated_at" in data["entries"][0]`.
  - `test_list_text_shows_created_and_updated`: store one entry the
    same way, list with `json_output=False`, capture the text buffer,
    assert `"created="` in it and `"updated="` in it.

Constraints
  1. C1's append to .agent/live_review.md is applied BYTE FOR BYTE:
     extract GATE3 from the COMMITTED .agent/authored/f262-r4.md by its
     BEGIN/END markers (excluded) and apply with a script, never by
     retyping. GATE3 carries ZERO internal newlines and NO trailing
     newline of its own. The base file (measured by the reviewer before
     this round) is 2421305 bytes with NO trailing newline; the applied
     file must equal base + one newline byte + GATE3's own bytes,
     exactly 2424986 bytes total. Report the arithmetic and a `cmp`
     against a script-extracted copy of GATE3, both directions.
  2. PAIR M1 and PAIR M2 are extracted from the COMMITTED
     .agent/authored/f262-r4.md by marker index and applied with
     str.replace(FROM, TO, 1) via a script, never by hand-retyping.
     M1 is APPEND-shaped: report FROM count before (must be 1) and TO
     count after (must be 1) - do NOT report "FROM count after" as a
     finding of 0, since TO contains FROM verbatim and a plain substring
     search for FROM will still read 1 after the edit; that is expected
     for this pair's shape, not a defect. M2 is a REWRITE: report FROM
     count before (1), FROM count after (0), TO count after (1).
  3. The two new test methods are written by hand from the TEST SPEC
     above (not extracted from a marker slice), matching the existing
     neighboring tests' style exactly.
  4. `python3 -m py_compile apps/cli/commands/memory.py
     tests/test_grouped_cli.py` must exit 0 for both (ruff is denied
     this session - attempt it anyway and report the exact refusal or
     the real result, never assume).
  5. C2 is ONE commit covering both files.
  6. PLAN5 REPLACES .agent/plan.md whole-file, ending WITHOUT a trailing
     newline, same as every prior round.
  7. The reviewer confirmed before authoring this block that
     `_cmd_memory_recall` (a few lines above `_cmd_memory_list` in the
     same file) has an almost byte-identical json-dict block and is
     NOT touched by this round - PAIR M1's FROM was deliberately widened
     to start at `_cmd_memory_list`'s own distinguishing import line so
     it cannot accidentally match `_cmd_memory_recall`'s copy (verified:
     a naive one-line FROM matched twice in the file before this
     widening).
  8. A sentence OUTSIDE the change set that this round makes stale is
     DECLARED in the handback and NOT repaired.
  9. Read .agent/STOP from disk before the first commit and again
     before C4. If it exists, finish the commit in hand, write the
     handback, and stop.
  10. Self-review loop before every commit (git diff --stat, git diff).
      Push after C4 (git push origin feature/f262-list-commands-v2). No
      pull request, no merge.
  11. `git rev-parse HEAD` before C0a must read
      `0d85f9fcc4381d0143c35f2e40bde6079e804789` (report the full SHA);
      `git branch --show-current` must read
      `feature/f262-list-commands-v2`.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f262-r4.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND, FULL FORENSICS. Report:
       base size immediately before C1 (bytes, trailing-newline byte)
       GATE3 own byte length and internal-newline count
       base + 1 + GATE3_length, compared against the post-C1 file's real
         byte length - state match True/False
       tail slice (last GATE3_length bytes of the post-C1 file) compared
         against GATE3 - state equal True/False
       negative control: flip the first byte of a COPY of GATE3, confirm
         the flipped copy does NOT match the real tail - state
         rejected True/False
  G3 THE TWO PAIRS, READ AND COUNTED, PER CONSTRAINT 2's SHAPES. Then
     read the full diff of apps/cli/commands/memory.py and confirm
     nothing beyond the two named insertions changed - in particular,
     confirm `_cmd_memory_recall`'s block is byte-for-byte untouched.
     `python3 -m py_compile` on both touched files, reported
     individually, each exit 0.
  G4 THE TESTS, BEFORE AND AFTER. Report
     `python3 -m pytest tests/test_grouped_cli.py -q` BOTH before C2
     (base count, fully green) and after C2 (base + 2, fully green -
     the two new tests plus every pre-existing one in that file, none
     of which this round should have touched).
  G5 THE STATE READERS AND THE CANARY (this round rewrites `.agent/`
     state):
       python3 -m pytest tests/ui_server/ -q
       python3 -m pytest tests/orchestration/test_test_runner.py -q
       python3 -m pytest tests/regression/test_resource_safety.py -q
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q
       python3 -m pytest tests/cli/test_golden_path.py -q
     Report each pass count; a moved count against this session's own
     prior readings (515/52/21/16/42) is itself a finding.
  G6 THE PLAN. Extract PLAN5 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G7 THE TREE, THE COMMITS AND THE SWEEP. `git status --porcelain`
     immediately before C4 is staged -> empty. `git ls-files
     .remedy-wt` -> no output. For C0a, C0b, C1, C2 and C3 (every commit
     before the handback), report each one's insertion count from
     `git show --numstat`, the '+' column only, compared cell by cell
     against the handback's Commits table. Then the staleness sweep,
     one line per file this round touched.

Handback
  Rewrite .agent/handoff.md per docs/agents/handback_template.md. SESSION
  1, ROUND 4 of F262. Item-status table with every ordered item (C0a
  through C4, G1 through G7) exactly once, Commits table, one line per
  gate followed by its real transcript, Deviations (apply anything that
  looks wrong exactly as specified and declare it - never silently
  correct the block), Next (round 5 designs the tournament.list /
  external-builder.submission-list per-row text format, per PLAN5's
  Next Steps).

<<<BEGIN GATE3>>>
Gate: R3 — the F262 R3 entry. R3 SHIPPED T002 BATCH 1, DATES IN TEXT OUTPUT FOR FOUR LIST COMMANDS, AND THE REVIEWER RE-RAN EVERY GATE ITSELF rather than reading the handback back. TRANSPORT HELD: `.agent/authored/f262-r3.md`/`.agent/last_block.md` share one sha256 digest over 303 lines. THE LEDGER APPEND (booking R2) IS PROVEN IN FULL: base immediately before C1 was 2417095 bytes with no trailing newline, GATE2 measured at 4209 bytes with 0 internal newlines, base plus one newline plus GATE2 equals 2421305 against an actual post-C1 size of 2421305 — match True; the tail slice equals GATE2 byte for byte — equal True; a negative control flipping GATE2's first byte was correctly rejected — rejected True. THE FOUR CODE PAIRS WERE READ, NOT ONLY GATED: `apps/cli/commands/blocker.py`, `apps/cli/commands/decision.py`, `apps/cli/commands/worker_facade_cmd.py` and `apps/cli/commands/self_repair_cmd.py` each show exactly one print statement replaced by two lines (a conditional resolved/updated-bearing suffix plus the extended print), nothing else changed in any of the four files, confirmed by reading the full diff of each. Every pair's FROM occurred exactly once before its own edit and its TO exactly once after, and the containment check `FROM in TO` was False for all four, confirming REWRITE for all four. THE TWO NEW TEST FILES MATCH THE TEST SPEC SYMBOL FOR SYMBOL: `tests/cli/test_blocker_cmd.py` and `tests/cli/test_decision_cmd.py`, each with the named fixture helper, the named patch targets and two tests apiece, read in full by the reviewer against the block's own TEST SPEC section. `python3 -m py_compile` exited 0 on all six touched or added `.py` files, run individually by the reviewer. THE TESTS MOVED EXACTLY AS EXPECTED: `tests/cli/test_worker_facade_cmd.py` (68 passed) and `tests/cli/test_self_repair_cmd.py` (12 passed) were IDENTICAL before and after C2, reproduced by the reviewer; the two new files read 2 passed apiece after C2, reproduced independently. THE STATE READERS AND THE CANARY WERE UNMOVED FROM THIS SESSION'S OWN BASELINE, reproduced by the reviewer: `tests/ui_server/` 515, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `test_golden_path` 42. HYGIENE HELD: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, and every commit's insertion counts match the handback's Commits table cell for cell, each measured independently via `git show --numstat`: `a262f04100eb12dd07820c683ea8073fd06be4b3` 303 new, `be92b6577f1c67cdc6b8ab5581d0121827a52457` 227 plus 225 deleted (mirror), `f5774a49b04358e0782676464f59714c3c1742a4` 2 plus 1 deleted, `e9589f54e5508daeff06eb25837a8fb93ff20e23` 2 plus 1 deleted apiece on the four printer files plus 49 and 53 new on the two test files, and `41922f01aa656c4fd968a412cb9731de608c83a9` 21 plus 17 deleted. THE PUSH DISCHARGED — `git ls-remote origin refs/heads/feature/f262-list-commands-v2` and the local `git rev-parse HEAD` both read `0d85f9fcc4381d0143c35f2e40bde6079e804789`, and nothing was created or merged; the branch carries R1 through R3 unmerged. THE FOUR DECLARED DEVIATIONS ARE ALL TOOLING OR PRE-EXISTING STALENESS, NONE A DEFECT ON DISK: `/tmp` denied for forensic scratch, redone under `.remedy-wt/` with identical bytes and comparisons; several compound Bash invocations rejected and re-expressed singly; `wc -l`'s newline-counting convention read `.agent/plan.md` at 40 rather than its raw 41-line width, both well under the 50-line cap; `docs/roadmap/features/T2_F262.md`'s "REGISTRATION ONLY" sentence is now more stale than at R2, outside the declared change set, correctly declared and left unrepaired. THE VERDICT IS PASS.
<<<END GATE3>>>

<<<BEGIN PLAN5>>>
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 4, session 1 — T002 batch 2: memory.list gains `updated_at` in
its --json output and both created/updated in its text output.

## Next Steps

- Round 5: tournament.list and external-builder.submission-list print
  only a COUNT in text mode today - no per-row listing exists at all -
  so adding dates there means designing a first per-row text format,
  a bigger slice than a one-line edit. Design it explicitly before
  coding it.
- Then: job.list/queue.list/project.list need `--json` added before a
  date can appear there; loop.list/patch.list have no timestamp on
  their model and need a design decision (round 3's handback carries
  the full 28-command audit).
- T003 (sort/filter/limit behavior) starts once date coverage is far
  enough along to sort by.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix unless it
  blocks T003's sort behavior for them specifically.
<<<END PLAN5>>>
