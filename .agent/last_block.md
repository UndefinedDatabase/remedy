STEP T002/3 - F262 List commands v2, ROUND 5
FEATURE F262 - List commands v2 (Tier 2) - SESSION 2, ROUND 5

Goal
  Ship T002 batch 3: `tournament.list` and `external-builder.submission-
  list` currently print ONLY A COUNT in text mode (no per-row listing
  exists at all) and their --json omits any date field. This round
  designs and ships a first per-row TEXT format for both, plus adds
  each record's own single date field to --json: `created_at` for
  tournament reports (the field the TournamentReport dataclass already
  carries), `received_at` for external-builder submissions (the field
  the ExternalBuilderCandidateSubmission dataclass already carries —
  NOT `created_at`, which that dataclass does not have). Neither record
  has a second/updated timestamp concept, so neither per-row line shows
  an "updated=" field — this matches blocker.list's existing precedent
  (apps/cli/commands/blocker.py: only `created=` plus a conditional
  `resolved=` when present, never a fabricated second field). Two
  production files, two test files. No model or store changes.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f262-r5.md
  C0b mirror it to .agent/last_block.md
  C1  append GATE4 to .agent/live_review.md - books round 4's PASS
      verdict (the reviewer's own, independently re-verified)
  C2  apply CODE PAIR T1 and CODE PAIR T2 to
      apps/cli/commands/tournament_cmd.py; apply CODE PAIR E1 and CODE
      PAIR E2 to apps/cli/commands/external_builder_cmd.py; add the
      TEST SPEC tests below to tests/cli/test_tournament_cli.py and
      tests/cli/test_external_builder_cli.py (one commit, four files)
  C3  apply PLAN6 to .agent/plan.md
  C4  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f262-r5.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - apps/cli/commands/tournament_cmd.py (C2)
  - apps/cli/commands/external_builder_cmd.py (C2) -
  tests/cli/test_tournament_cli.py (C2) -
  tests/cli/test_external_builder_cli.py (C2) - .agent/plan.md (C3) -
  .agent/handoff.md (C4)

CODE PAIR T1 (apps/cli/commands/tournament_cmd.py) - REWRITE (TO does
NOT contain FROM verbatim: the closing `}` of the dict-comprehension's
last field must move). FROM is the json dict comprehension's last
field line inside `_cmd_tournament_list`, unique in the file.
<<<BEGIN PAIR_T1_FROM>>>
                        "confidence": r.get("confidence")} for r in reps]}
<<<END PAIR_T1_FROM>>>
<<<BEGIN PAIR_T1_TO>>>
                        "confidence": r.get("confidence"),
                        "created_at": r.get("created_at", "")} for r in reps]}
<<<END PAIR_T1_TO>>>

CODE PAIR T2 (apps/cli/commands/tournament_cmd.py) - APPEND-shaped (TO
contains FROM verbatim as its first line - a same-place insertion,
not a rewrite). FROM is the existing count-only print line in the same
function, unique in the file.
<<<BEGIN PAIR_T2_FROM>>>
    print(f"Tournament reports for {str(args.job_id)[:8]}: {len(reps)}")
<<<END PAIR_T2_FROM>>>
<<<BEGIN PAIR_T2_TO>>>
    print(f"Tournament reports for {str(args.job_id)[:8]}: {len(reps)}")
    for r in reps:
        winner = r.get("winner_competitor_id") or "(none)"
        print(f"  {r.get('tournament_id')}: {r.get('status')}  winner={winner}"
              f"  confidence={r.get('confidence')}  (created={r.get('created_at', '')})")
<<<END PAIR_T2_TO>>>

CODE PAIR E1 (apps/cli/commands/external_builder_cmd.py) - REWRITE
(same shape as T1: the closing `}` of the dict-comprehension's last
field must move). FROM is the json dict comprehension's last field
line inside `_cmd_external_builder_submission_list`, unique in the
file.
<<<BEGIN PAIR_E1_FROM>>>
                            "intent_id": s.get("intent_id", "")} for s in subs]}
<<<END PAIR_E1_FROM>>>
<<<BEGIN PAIR_E1_TO>>>
                            "intent_id": s.get("intent_id", ""),
                            "received_at": s.get("received_at", "")} for s in subs]}
<<<END PAIR_E1_TO>>>

CODE PAIR E2 (apps/cli/commands/external_builder_cmd.py) - APPEND-
shaped (same shape as T2). FROM is the existing count-only print line
in the same function, unique in the file.
<<<BEGIN PAIR_E2_FROM>>>
    print(f"External builder submissions for {str(args.job_id)[:8]}: {len(subs)}")
<<<END PAIR_E2_FROM>>>
<<<BEGIN PAIR_E2_TO>>>
    print(f"External builder submissions for {str(args.job_id)[:8]}: {len(subs)}")
    for s in subs:
        print(f"  {s.get('submission_id')}: {s.get('state')}  source={s.get('source_label')}"
              f"  (received={s.get('received_at', '')})")
<<<END PAIR_E2_TO>>>

TEST SPEC for C2 - four new test functions written BY HAND (not
marker-extracted) from this spec, matching each file's existing
module-level test-function style exactly (they are plain functions
using the `env` fixture and `run_grouped_cli`, not a test class).

  In tests/cli/test_tournament_cli.py, append at the END of the file
  (after `test_json_purity`), two new functions:
  - `test_list_json_has_created_at(env)`: call
    `run_grouped_cli(["tournament", "report", "job-6", "--json"], env)`
    to create one report; call
    `run_grouped_cli(["tournament", "list", "job-6", "--json"], env)`;
    parse stdout as JSON into `d`; assert
    `d["reports"][0]["created_at"]` is truthy.
  - `test_list_text_shows_per_row(env)`: call `tournament report job-7
    --json`, capture its `tournament_id` from the parsed JSON as `tid`;
    call `run_grouped_cli(["tournament", "list", "job-7"], env)` (no
    --json); assert `r.returncode == 0`; assert `tid in r.stdout`;
    assert `"created=" in r.stdout`.

  In tests/cli/test_external_builder_cli.py, append at the END of the
  file (after `test_package_missing_job`), two new functions, each
  following `test_submit_candidate_json`'s existing setup pattern
  (`_job(env)`, `package-create`, write `_SAFE_CAND` to
  `env / "resp.md"`, `submit` with `--source-label claude --json`):
  - `test_submission_list_json_has_received_at(env)`: after
    submitting, call `run_grouped_cli(["external-builder",
    "submission-list", job_id, "--json"], env)`; parse stdout as JSON
    into `d`; assert `d["submissions"][0]["received_at"]` is truthy.
  - `test_submission_list_text_shows_per_row(env)`: after submitting,
    capture the submit response's `submission_id` as `sid`; call
    `run_grouped_cli(["external-builder", "submission-list", job_id],
    env)` (no --json); assert `r.returncode == 0`; assert `sid in
    r.stdout`; assert `"received=" in r.stdout`.

Constraints
  1. C1's append to .agent/live_review.md is applied BYTE FOR BYTE:
     extract GATE4 from the COMMITTED .agent/authored/f262-r5.md by its
     BEGIN/END markers (excluded) and apply with a script, never by
     retyping. GATE4 carries ZERO internal newlines and NO trailing
     newline of its own. The base file (measured by the reviewer before
     this round) is 2424986 bytes with NO trailing newline, last byte
     `.`; the applied file must equal base + one newline byte + GATE4's
     own bytes. Report the arithmetic and a `cmp`-equivalent byte
     comparison against a script-extracted copy of GATE4, both
     directions, plus a negative control (flip GATE4's first byte in a
     scratch copy, confirm it does NOT match the real tail).
  2. All four PAIRs are extracted from the COMMITTED
     .agent/authored/f262-r5.md by marker index and applied with
     str.replace(FROM, TO, 1) via a script, never by hand-retyping.
     Before editing, confirm each FROM occurs EXACTLY ONCE in its
     target file (report the count; if it is not exactly 1, STOP and
     report rather than editing). T1 and E1 are REWRITEs: report FROM
     count before (1), FROM count after (0), TO count after (1). T2 and
     E2 are APPEND-shaped: report FROM count before (1), TO count after
     (1) - do NOT report "FROM count after" as evidence of a defect if
     it also reads 1, since TO contains FROM verbatim by design; that
     is the expected shape for these two pairs, not an error.
  3. The four new test functions are written by hand from the TEST
     SPEC above (not extracted from a marker slice), matching each
     file's existing neighboring functions' style exactly - including
     the module's existing `env` fixture and `run_grouped_cli` import,
     already present in both files; no new imports needed.
  4. `python3 -m py_compile apps/cli/commands/tournament_cmd.py
     apps/cli/commands/external_builder_cmd.py
     tests/cli/test_tournament_cli.py
     tests/cli/test_external_builder_cli.py` must exit 0 for all four
     (ruff is denied this session per prior rounds - attempt it anyway
     and report the exact refusal or the real result, never assume).
  5. C2 is ONE commit covering all four files.
  6. PLAN6 REPLACES .agent/plan.md whole-file, ending WITHOUT a
     trailing newline, same as every prior round.
  7. Before writing PAIR T1/T2, confirm no OTHER function in
     tournament_cmd.py contains a matching FROM string (the file has
     four handlers total: report, show, list, integrity - only `list`
     prints a bare count or ends a dict on `"confidence"`). Before
     writing PAIR E1/E2, confirm the same for external_builder_cmd.py
     (eight handlers total - only `submission-list` matches either
     FROM). Report each count explicitly, not just "looks fine".
  8. A sentence OUTSIDE the change set that earlier rounds already
     found stale (docs/roadmap/features/T2_F262.md line 5,
     "REGISTRATION ONLY") remains outside this round's change set too -
     re-declare it in the handback, do not repair it.
  9. Read .agent/STOP from disk before the first commit and again
     before C4. If it exists, finish the commit in hand, write the
     handback, and stop.
  10. Self-review loop before every commit (git diff --stat, git diff).
      Push after C4 (git push origin feature/f262-list-commands-v2). No
      pull request, no merge.
  11. `git rev-parse HEAD` before C0a must read
      `f4765b49b0b8859a6cecfd3cf7bc8c171bf6becb` (report the full SHA);
      `git branch --show-current` must read
      `feature/f262-list-commands-v2`.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f262-r5.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND, FULL FORENSICS. Report:
       base size immediately before C1 (bytes, trailing-newline byte)
       GATE4 own byte length and internal-newline count
       base + 1 + GATE4_length, compared against the post-C1 file's
         real byte length - state match True/False
       tail slice (last GATE4_length bytes of the post-C1 file)
         compared against GATE4 - state equal True/False
       negative control: flip the first byte of a COPY of GATE4,
         confirm the flipped copy does NOT match the real tail - state
         rejected True/False
  G3 THE FOUR PAIRS, READ AND COUNTED, PER CONSTRAINT 2's SHAPES. Then
     read the FULL diff of apps/cli/commands/tournament_cmd.py and
     apps/cli/commands/external_builder_cmd.py and confirm nothing
     beyond the two named insertions changed in EACH file (all other
     handlers in both files byte-for-byte untouched). `python3 -m
     py_compile` on all four touched/added .py files, reported
     individually, each exit 0.
  G4 THE TESTS, BEFORE AND AFTER. Report
       python3 -m pytest tests/cli/test_tournament_cli.py -q
       python3 -m pytest tests/cli/test_external_builder_cli.py -q
     BOTH before C2 (baseline: 6 passed, 7 passed respectively) and
     after C2 (8 passed, 9 passed respectively - each base + 2, fully
     green, nothing else in either file touched).
  G5 THE STATE READERS AND THE CANARY (this round rewrites `.agent/`
     state):
       python3 -m pytest tests/ui_server/ -q
       python3 -m pytest tests/orchestration/test_test_runner.py -q
       python3 -m pytest tests/regression/test_resource_safety.py -q
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q
       python3 -m pytest tests/cli/test_golden_path.py -q
     Report each pass count; a moved count against this session's own
     prior readings (515/52/21/16/42) is itself a finding.
  G6 THE PLAN. Extract PLAN6 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G7 THE TREE, THE COMMITS AND THE SWEEP. `git status --porcelain`
     immediately before C4 is staged -> empty. `git ls-files
     .remedy-wt` -> no output. For C0a, C0b, C1, C2 and C3 (every
     commit before the handback), report each one's insertion count
     from `git show --numstat`, the '+' column only, compared cell by
     cell against the handback's Commits table. Then the staleness
     sweep, one line per file this round touched, plus the constraint-8
     check.

Handback
  Rewrite .agent/handoff.md per docs/agents/handback_template.md.
  SESSION 2, ROUND 5 of F262. Item-status table with every ordered item
  (C0a through C4, G1 through G7) exactly once, Commits table, one line
  per gate followed by its real transcript, Deviations (apply anything
  that looks wrong exactly as specified and declare it - never silently
  correct the block), Next (round 6: job.list/queue.list/project.list
  need --json added before a date can appear there; loop.list/
  patch.list have no timestamp on their own model and need a design
  decision - round 3's handback carries the full 28-command audit -
  per PLAN6's Next Steps).

<<<BEGIN GATE4>>>
Gate: R4 — the F262 R4 entry. R4 SHIPPED T002 BATCH 2, memory.list gains `updated_at` in --json and both created/updated in its text output, AND THE REVIEWER RE-RAN EVERY GATE ITSELF rather than reading the handback back. TRANSPORT HELD: `.agent/authored/f262-r4.md`/`.agent/last_block.md` share one sha256 digest, `420f487092908823e0e1b43459f8860cd777ad884f2a95841049c09a1756e1df`, over 246 lines. THE LEDGER APPEND (booking R3) IS PROVEN IN FULL: base immediately before C1 was 2421305 bytes with no trailing newline, GATE3 measured at 3680 bytes with 0 internal newlines, base plus one newline plus GATE3 equals 2424986 against an actual post-C1 size of 2424986 — match True; the tail slice equals GATE3 byte for byte — equal True. THE TWO PAIRS WERE READ, NOT ONLY GATED: `apps/cli/commands/memory.py`'s diff is exactly PAIR M1 (append-shaped: adds `"updated_at": e.updated_at,` after `"created_at": e.created_at,` in `_cmd_memory_list`'s json dict) and PAIR M2 (rewrite: extends the text-branch print with `created=`/`updated=`), nothing else changed in the file, confirmed by reading the full diff; `_cmd_memory_recall`'s near-identical json-dict block a few lines above remained byte-for-byte untouched. `python3 -m py_compile` exited 0 on both touched files, run individually by the reviewer. THE TWO NEW TESTS MATCH THE TEST SPEC: `test_list_json_has_updated_at_key` and `test_list_text_shows_created_and_updated`, added to the existing `TestMemoryCLIContract` class, read in full against the block's own TEST SPEC. THE TESTS MOVED EXACTLY AS EXPECTED: `tests/test_grouped_cli.py` read 511 passing before C2 and 513 after, reproduced by the reviewer independently. THE STATE READERS AND THE CANARY WERE UNMOVED FROM THIS SESSION'S OWN BASELINE, reproduced by the reviewer: `tests/ui_server/` 515, `test_test_runner` 52, `test_resource_safety` 21, `test_integrity_gate` 16, `test_golden_path` 42. HYGIENE HELD: `git status --porcelain` empty at HEAD `f4765b49b0b8859a6cecfd3cf7bc8c171bf6becb`, and every commit's insertion counts match the handback's Commits table cell for cell, each measured independently via `git show --numstat`: `831747fd00cf204b51a4c620a63031085ff7b106` 246 new, `dfe89e7e43ba11fd56c1e0431abbe1b10bdcb1c4` 158 plus 215 deleted (mirror), `2e1f7323eba0fbaca39482b7fb2f9cc0c0895e14` 2 plus 1 deleted, `66d84b2e0b802baa4f45033aaade47fea773bf62` 2 plus 1 deleted on `memory.py` plus 25 new on the test file, and `a07c6cd2492c3dceea58d145f75df6746abbe81d` 18 plus 21 deleted. THE PLAN HELD BYTE-EXACT: PLAN5 extracted from the committed authored file (1536 bytes, last byte `.`) compares equal to `.agent/plan.md`. THE PUSH DISCHARGED — `git ls-remote origin refs/heads/feature/f262-list-commands-v2` and the local `git rev-parse HEAD` both read `f4765b49b0b8859a6cecfd3cf7bc8c171bf6becb`, and nothing was created or merged; the branch carries R1 through R4 unmerged. `gh pr list --state open` printed `[]`. THE FOUR DECLARED DEVIATIONS ARE ALL TOOLING, NONE A DEFECT ON DISK, RE-CONFIRMED BY THE REVIEWER: `git commit`'s own printed rewrite-detected stat line disagreed with `git show --numstat` for the two whole-file rewrites (C0b, C3), the same substitution already declared in round 1's own ledger entry; GATE3's Python `str`-mode character count (3670) differed from its real byte length (3680) over several em-dash characters, caught before any file was touched and redone in raw bytes; several compound Bash one-liners were rejected by the sandbox and re-expressed singly; `docs/roadmap/features/T2_F262.md` line 5's "REGISTRATION ONLY" sentence remains stale since round 2, outside this round's declared change set, correctly declared and left unrepaired again. THE VERDICT IS PASS.
<<<END GATE4>>>

<<<BEGIN PLAN6>>>
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 5, session 2 — T002 batch 3: tournament.list and external-
builder.submission-list gain a first per-row text format (neither had
one before - text mode printed only a count) plus their own single
date field in --json (`created_at` for tournament reports,
`received_at` for submissions - neither record has a second/updated
timestamp, so neither row shows one).

## Next Steps

- Round 6: job.list/queue.list/project.list need `--json` added before
  a date can appear there; loop.list/patch.list have no timestamp on
  their own model and need a design decision (round 3's handback
  carries the full 28-command audit).
- T003 (sort/filter/limit behavior) starts once date coverage is far
  enough along to sort by.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix unless it
  blocks T003's sort behavior for them specifically.
<<<END PLAN6>>>