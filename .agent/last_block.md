STEP T003 PART 5 (DOCS) / ROUND 10 - F114 Cost preview per command
FEATURE F114 - Cost preview per command (Tier 3) - SESSION 3, ROUND 10

Goal
  Book round 9's PASS verdict into the ledger (RECORD9) and add T003's
  docs item: a new user guide, docs/guides/cost-preview-user-guide-v0.md,
  documenting job.run's cost-preview behavior end to end - the estimate
  line, the mandatory basis label, the cost_preview.confirm_above_usd
  config key, --yes, --unattended, and the non-tty exit-2-with-hint path
  - and register it in docs/README.md (Quick-Find Table + Guides
  section). No production code or test file changes this round.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f114-r10.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD9 to .agent/live_review.md (append) and PLAN10 to
      .agent/plan.md (whole-file replacement)
  C2  write docs/guides/cost-preview-user-guide-v0.md per GUIDE (new
      file), and apply QUICKFIND PAIR and GUIDESROW PAIR to
      docs/README.md
  C3  rewrite .agent/handoff.md - the handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f114-r10.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - .agent/plan.md (C1) -
  docs/guides/cost-preview-user-guide-v0.md (new, C2) -
  docs/README.md (C2) - .agent/handoff.md (C3)

Constraints
  1. Every authored slice is applied BYTE FOR BYTE: extract it by
     delimiter index from the COMMITTED .agent/authored/f114-r10.md -
     marker lines EXCLUDED - and write it with a script, never by
     retyping. If a slice looks wrong, apply it as written and DECLARE it
     in the handback.
  2. C1 is the first substantive commit of the round.
  3. RECORD9 appends to .agent/live_review.md as EXACTLY ONE newline byte
     followed by the slice (the file's own current convention, same as
     every prior round's own G2 measurement). PLAN10 REPLACES
     .agent/plan.md whole.
  4. NEWLINE CONVENTION, STATED EXPLICITLY: RECORD9 and PLAN10 carry NO
     trailing newline of their own. GUIDE is a real markdown file whose
     OWN trailing newline is its true last byte - a byte-exact structural
     suffix of the file, not marker-line formatting (same class as round
     9's own TESTMODULE).
  5. GUIDE IS A WHOLE-FILE WRITE: write its exact bytes with the Write
     tool (a "copyfile", never a text-extraction-and-reflow) and verify
     by extracting GUIDE from the committed authored file and `cmp`
     against the written file.
  6. BOTH docs/README.md pairs are APPEND-shaped: TO contains FROM
     verbatim in each (containment already verified at authoring time:
     true for both). Apply each via str.replace(FROM, TO, 1); before C2
     confirm each FROM occurs exactly 1x in docs/README.md; after C2
     confirm "TO contains FROM: true" holds for both, matching this
     constraint.
  7. This round does NOT touch packages/, apps/, or tests/ - no
     production code or test file changes; rounds 8/9's wiring and tests
     are untouched.
  8. A sentence OUTSIDE the change set that this round makes stale is
     DECLARED in the handback and NOT repaired. Rounds 2 and 3's own
     .agent/context.md declarations (lines 29 and 36) stand; do not
     repeat them.
  9. Read .agent/STOP from disk before the first commit and again
     before C3. If it exists, finish the commit in hand, write the
     handback, and stop.
  10. Self-review loop before every commit (git diff --stat, git diff).
      Push after C3. No pull request, no merge this round - a docs-only
      addition does not by itself trigger the Open PR Gate; that waits
      for the remaining T003 acceptance items (marking further expensive
      commands, the integration gate).
  11. No git worktree is needed this round (no production code changed,
      so no mutation red-proof applies) - do not create one.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b:
       sha256sum .agent/authored/f114-r10.md .agent/last_block.md
     One digest, twice. Report both lines verbatim.
  G2 THE LEDGER APPEND. Base size of .agent/live_review.md immediately
     BEFORE C1 (measure it yourself): report its byte length and whether
     it ends with a trailing newline. RECORD9 has ZERO internal
     newlines - report its own byte length. Report: base + 1 +
     len(RECORD9) and whether that equals the post-C1 file's byte length
     (expected 2382446, from a base of 2379181 and a RECORD9 of 3264
     bytes - recompute both independently). Then the SECOND reader:
     report whether the post-C1 file's bytes from `base` to the end
     equal exactly "\n" + RECORD9. Then a NEGATIVE CONTROL in a scratch
     copy ONLY (never the tracked file): flip one byte inside RECORD9's
     own text and report the second reader REJECTS it.
  G3 THE PLAN. Extract PLAN10 from the COMMITTED authored file, then:
       cmp <extracted> .agent/plan.md            -> exit 0
       wc -l .agent/plan.md                      -> report; expect 40, must be under 50
       grep -c '^## Goal' .agent/plan.md         -> 1
       grep -c '^## Next Steps' .agent/plan.md   -> 1
  G4 THE NEW FILE. Extract GUIDE from the COMMITTED authored file and
     `cmp` against docs/guides/cost-preview-user-guide-v0.md -> exit 0.
     Report the file's byte length (expected 3666 - recompute
     independently).
  G5 THE README PAIRS. For EACH of QUICKFIND PAIR and GUIDESROW PAIR:
     report the FROM count in docs/README.md immediately BEFORE C2 (must
     be 1), apply it, then report "TO contains FROM: true" (matching
     constraint 6). Then `git show --numstat <C2 sha> -- docs/README.md`
     and report the +/- cells verbatim (no predicted value - just
     report what the tool prints).
  G6 THE SUITES, EACH AS ITS OWN INVOCATION, RUN SERIALLY, IN THE PRIMARY
     CHECKOUT:
       python3 -m pytest tests/docs/ -q
       python3 -m pytest tests/ui_server/ -q
       python3 -m pytest tests/orchestration/test_test_runner.py -q
       python3 -m pytest tests/regression/test_resource_safety.py -q
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q
       python3 -m pytest tests/cli/test_golden_path.py -q
     Report each count. tests/docs/ is expected to read 295, UNCHANGED
     from rounds 8 and 9: the new guide file is not itself a member of
     PRIMARY_DOCS in tests/docs/test_docs_consistency.py, so its links
     are checked as part of the EXISTING parametrized case for
     docs/README.md rather than as a new case - no new test is added by
     this round. The other five counts are also expected unchanged from
     round 9 (515, 52, 21, 16, 42 respectively), since no code this
     round touches anything they exercise - recompute all six for real,
     do not assume.
  G7 THE TREE, THE COMMITS AND THE SWEEP.
       git status --porcelain                    -> empty, immediately before C3 staged
       git ls-files .remedy-wt                   -> empty (nothing under .remedy-wt/ is ever committed)
     Per-commit insertion/deletion cross-check (`git show --numstat`)
     against this handback's own Commits table for C0a, C0b, C1 (both
     paths) and C2 (three paths: the new guide, docs/README.md) - report
     every cell and confirm it matches the table. C3's own numbers go to
     neither the table nor a round report, per the template's
     self-reference exception.
     Staleness sweep: one entry per file this round touched (NOT stale /
     stale + why), plus a statement that no NEW stale sentence was found
     outside the change set this round.

SLICES. Each slice lies between its own one-line BEGIN and END marker.
There are five: RECORD9, PLAN10, GUIDE, QUICKFIND PAIR FROM/TO and
GUIDESROW PAIR FROM/TO.

<<<BEGIN RECORD9>>>
Gate: F114 R9 — the round 9 entry, adds tests/cli/test_cost_preview.py (T003 continued): five acceptance tests exercising the REAL confirm_cost_preview end to end through job.run, no production code changed. VERDICT PASS, over the range `64de02a69288b65265766c548c8a86f0cbd6bfd5..c18a416c68d6d2edabab9fba34f08cb7005e8f34` (commits C0a `a871cd4fff331ee071429c1ea187f893fcc93baf`, C0b `cab855b8cc85047fbe0294d8b9311160779651e8`, C1 `947a14743a9d2805ca721e14890171b00501fc03`, C2 `c18a416c68d6d2edabab9fba34f08cb7005e8f34` — four real content commits — plus handback commit `91e4ad641da9668f43959043075fc7c2056f2e9b`), independently re-verified by the reviewer in a fresh session. TRANSPORT HELD: `sha256sum .agent/authored/f114-r9.md .agent/last_block.md` both print `ce56e9ec686400c21b009c758a3309a813cd5f5705e768450332d530c56ab4a7`, reproduced directly. G2 THE LEDGER APPEND HELD: base 2375218 bytes (no trailing newline), RECORD8 3962 bytes, base + 1 + 3962 = 2379181, matching the post-C1 file's measured length exactly; the second reader's tail slice equalled `\n` + RECORD8 byte for byte, and a one-byte-flipped negative control was correctly rejected — all reproduced independently. G3 THE PLAN HELD BYTE-EXACT: PLAN9 extracted from the committed authored file `cmp`s exit 0 against `.agent/plan.md` (46 lines, under 50; `## Goal`/`## Next Steps` each exactly once), reproduced independently. G4 THE NEW FILE HELD: `tests/cli/test_cost_preview.py` `cmp`s exit 0 against the extracted TESTMODULE slice (2965 bytes), reproduced independently; `python3 -m py_compile` exit 0, reproduced. G6 THE RED-PROOF HELD, REPRODUCED INDEPENDENTLY IN A SEPARATE DISPOSABLE WORKTREE: inverting `apps/cli/commands/job.py`'s existing `if not confirm_cost_preview(` to `if confirm_cost_preview(` at HEAD produced the identical two failing tests the worker reported (`test_yes_flag_proceeds_through_the_real_gate_without_a_tty`, `test_unattended_proceeds_through_the_real_gate_without_a_tty`) plus three still passing; reverted, 5 passed again; worktree removed after. G7 THE SUITES, REPRODUCED INDEPENDENTLY BY THE REVIEWER at this round's own HEAD, all twelve counts identical to the worker's own reading: `test_cost_preview.py` 5, `test_long_run_executor.py` 76, `test_escalation.py` 68, `test_no_interactive_guard.py` 6, `test_command_catalog.py`+`test_command_catalog.py` (cli) 45, `tests/docs/` 295, `test_roadmap_index.py` 30, `tests/ui_server/` 515, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, `test_golden_path.py` (canary) 42 — nothing moved outside this round's own declared changes. G8 HELD: `git status --porcelain` empty, `git ls-files .remedy-wt` empty, no leftover scratch worktree, all four pre-handback commits' numstat +/- cells matched the handback's own Commits table cell for cell, reproduced independently. ZERO DEVIATIONS WERE DECLARED by the worker and the reviewer found none either. No finding is registered; nothing is wrong on disk. This is the first round whose acceptance tests exercise confirm_cost_preview through job.run end to end rather than through a mock. Branch `feature/f114-cost-preview-per-command` is pushed and matches `origin` head-for-head; `git status --porcelain` reads empty now.
<<<END RECORD9>>>

<<<BEGIN PLAN10>>>
# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 10 adds T003's docs item: a new user guide,
`docs/guides/cost-preview-user-guide-v0.md`, documenting `job.run`'s
cost-preview behavior end to end - the estimate line, the basis label,
the `cost_preview.confirm_above_usd` config key, `--yes`, `--unattended`,
and the non-tty exit-2-with-hint path - and registers it in
`docs/README.md` (Quick-Find Table + Guides section). No production
code or test changes this round.

## Next Steps

- T003 continuation: consider marking other "rerunning subtrees" /
  "long explanations" commands `is_expensive` - only `job.run` so far.
- Real cost bands for `job.run` still do not exist - a future round
  needs real task-class data to replace the unavailable estimate.
- Acceptance fixtures continue; the integration gate, then the closure
  sequence (PR, Open PR Gate). No PR exists yet.
- Session note: round 10, session 3 - 1 delegated round this session so
  far, at the 4-5 default.

## Risks

- Docs-only round: no gate over packages/apps/ this round beyond the
  standing .agent-state readers and the docs link-check suite.
- The guide documents behavior round 8/9 already gated; a future
  behavior change to cost_preview.py or cost_preview_confirm.py must
  update this guide in the same round (named here so it is not missed).
<<<END PLAN10>>>

<<<BEGIN GUIDE>>>
# Cost preview per command — user guide (v0)

Some commands can spend real money before they finish. `remedy job run` is the
first one Remedy wires to a cost preview (F114): before an expensive run
starts, it prints an estimate and, in attended mode, asks for confirmation
above a configured threshold. For the numbers Remedy prints AFTER a run, see
[cost-report-user-guide-v0.md](cost-report-user-guide-v0.md); this guide is
about the estimate shown BEFORE.

## What you see

```
$ remedy job run abc12345
estimated $0.0120-$0.0480 (basis: class defaults (low/medium token bands) x price_basis_usd_per_1k_tokens=0.003)
Continue running 'job.run'? [y/N]
```

The line always carries a `basis:` label — never a bare number — because a
number with no stated source cannot be checked. When the estimate cannot be
computed at all (an unrecognised task class, or no price basis configured),
the line says so instead of guessing:

```
estimated cost unavailable (basis: estimate_unavailable)
Continue running 'job.run'? [y/N]
```

An unavailable estimate is treated as expensive — A9 of
[T3_F114.md](../roadmap/features/T3_F114.md) is "unknown is treated as
expensive, never guessed" — so it always asks for confirmation, the same as a
real estimate above the threshold. Below the threshold, nothing prints a
question at all; cheap runs never interrupt.

## Skipping the prompt

- `--yes` skips the confirmation and proceeds, printing an audited line so the
  skip is visible in evidence:
  ```
  $ remedy job run abc12345 --yes
  estimated cost unavailable (basis: estimate_unavailable) - proceeding without prompt (--yes)
  ```
- `--unattended` (the loop's unattended mode, F051) skips it the same way —
  neither flag bypasses budget limits or the escalation log, only the
  cost-preview prompt itself.
- With neither flag, on a pipe (no terminal attached to stdin) the command
  never hangs waiting for an answer nobody can give. It exits immediately:
  ```
  $ echo | remedy job run abc12345
  Error: estimated cost unavailable (basis: estimate_unavailable). stdin is not a terminal, so there is nobody to confirm. Pass --yes to run 'job.run' without a prompt.
  $ echo $?
  2
  ```

## The confirmation threshold

`cost_preview.confirm_above_usd` sets the USD figure the estimate's high end
must exceed before a confirmation is required at all. Configure it like any
other Remedy setting:

- environment variable `REMEDY_COST_PREVIEW_CONFIRM_ABOVE_USD`
- `remedy.toml`:
  ```toml
  [remedy.cost_preview]
  confirm_above_usd = 0.5
  ```
- default: `0.5` (F114 Design: "around half a dollar")

A malformed or non-positive configured value falls back to the default rather
than blocking every command — this threshold is a UX setting, not a budget
limit, so a bad config value degrades safely instead of refusing every run.

## What is wired so far

Only `remedy job run` carries a cost preview today; it is the command the
catalog marks `is_expensive`. Real cost bands for `job.run` do not exist yet
either — its estimate is always `estimate_unavailable` until a future round
supplies real task-class data, which is why every example above shows the
unavailable case. Marking further commands `is_expensive` and giving `job.run`
a real band are both separate, later work.

## Related

- [T3_F114.md](../roadmap/features/T3_F114.md) — the feature brief (goal,
  design, acceptance).
- [token-economy-user-guide-v0.md](token-economy-user-guide-v0.md) — the
  budget estimates this preview's arithmetic shares with.
- [cost-report-user-guide-v0.md](cost-report-user-guide-v0.md) — the actuals
  report, for what a run really cost after it finished.
<<<END GUIDE>>>

<<<BEGIN QUICKFIND PAIR FROM>>>
| cost report | [cost-report-user-guide-v0.md](guides/cost-report-user-guide-v0.md) | guide |
<<<END QUICKFIND PAIR FROM>>>

<<<BEGIN QUICKFIND PAIR TO>>>
| cost preview | [cost-preview-user-guide-v0.md](guides/cost-preview-user-guide-v0.md) | guide |
| cost report | [cost-report-user-guide-v0.md](guides/cost-report-user-guide-v0.md) | guide |
<<<END QUICKFIND PAIR TO>>>

<<<BEGIN GUIDESROW PAIR FROM>>>
| [cost-report-user-guide-v0.md](guides/cost-report-user-guide-v0.md) | Reading `remedy stats report` |
<<<END GUIDESROW PAIR FROM>>>

<<<BEGIN GUIDESROW PAIR TO>>>
| [cost-preview-user-guide-v0.md](guides/cost-preview-user-guide-v0.md) | Cost preview before an expensive command runs (`remedy job run`) |
| [cost-report-user-guide-v0.md](guides/cost-report-user-guide-v0.md) | Reading `remedy stats report` |
<<<END GUIDESROW PAIR TO>>>
