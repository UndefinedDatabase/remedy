STEP REPAIR OF THE RED DOCS GATE + PR / ROUND 29 - F262 List commands v2 (dates, sort, filter) (FINAL ROUND ON THIS BRANCH)
FEATURE F262 - List commands v2 (dates, sort, filter) (Tier 2) - SESSION 9, ROUND 29

Goal
  Book round 28's verdict (RECORD28: FAIL on the docs gate, everything else
  held), register FINDING R-0797 (the reviewer's own README slice named F267
  inside an "Accepted" block), repair it with ONE README pair that names no
  feature id, re-run the docs gate to green, and open the pull request. Do
  NOT merge - the reviewer reads the checks and merges under the operator's
  authorization.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f262-r29.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD28 then FINDING to .agent/live_review.md (two appends, in
      that order, each as EXACTLY TWO newline bytes then the slice), and
      PLAN30 to .agent/plan.md (whole-file replacement)
  C2  apply the PARA pair to README.md; then append to .agent/live_review.md
      (EXACTLY TWO newline bytes then the text) ONE line of your own words
      beginning `Landed: R-0797 — ` that names the repairing commit's short
      sha, the pair applied and the docs-gate count you measured (this is
      the worker's `Landed:` marker per docs/agents/planner_reviewer_prompt.md
      §4 item 4 - never write `Done:`). ONE commit for both edits.
  then push, run G5 (must be green), then `gh pr create` (constraint 8)
  C3  rewrite .agent/handoff.md - the FINAL handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f262-r29.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md, .agent/plan.md (C1) - README.md,
  .agent/live_review.md (C2) - .agent/handoff.md (C3)

Constraints
  1. Every authored slice (RECORD28, FINDING, PLAN30, PARA pair, PRBODY) is
     applied BYTE FOR BYTE from the COMMITTED .agent/authored/f262-r29.md by
     marker extraction in Python, never retyped.
  2. C1 is the first substantive commit of the round.
  3. RECORD28, FINDING and PLAN30 carry no trailing newline; the two C1
     appends are ordered RECORD28 first, FINDING second.
  4. Read .agent/STOP before C0a, before C2 and before C3; if present,
     finish the commit in hand, write the handback, stop, create no PR.
  5. The PARA pair is applied with str.replace(FROM, TO, 1) after confirming
     FROM occurs EXACTLY ONCE in README.md. `TO contains FROM: false`
     (REWRITE) - re-check and report. After applying, `grep -c "F267"
     README.md` must read 0 (report it).
  6. THE OPEN SET, §3 item 10's line-count formula: BEFORE C1 356 / 77 /
     279; AFTER C1 357 / 77 / 280 (FINDING registers one id); the C2
     `Landed:` line changes neither count. Report all three readings.
  7. This round does not touch packages/, apps/, tests/, docs/,
     scripts/. STATUS.md and scripts/self_use_queue.json are NOT touched
     (they landed at `423bc28d`). Sandbox re-expressions in Python, each
     reported; never `cd`.
  8. THE PULL REQUEST, after C2 is pushed and G5 is green: write the PRBODY
     slice to a scratch file and run
       gh pr create --title "F262: List commands v2 (dates, sort, filter)" --base main --head feature/f262-list-commands-v2 --body-file <file>
     Report the PR number and URL. Never `gh pr merge`.

Done when - the gates. Real exit codes, real output.
  G1 HYGIENE. `.agent/STOP` at each of constraint 4's reads; `git status
     --porcelain | wc -l` 0 after C0a, C0b, C1, C2.
  G2 TRANSPORT. `sha256sum .agent/authored/f262-r29.md .agent/last_block.md`
     - one digest, twice.
  G3 THE RECORD APPENDS AT C1. Base size before C1 (expect 2513219, no
     trailing newline); RECORD28 length (expect 4060); FINDING length
     (expect 2545); base + 2 + RECORD28 + 2 + FINDING (expect
     2519828) versus the post-C1 length; the post-C1 tail equals
     "\n\n" + RECORD28 + "\n\n" + FINDING; negative control in a scratch
     copy flips one byte inside RECORD28 (the FIRST appended paragraph) and
     the reader REJECTS it. After C2: the file ends with "\n\n" + your
     `Landed: R-0797 — ` line and `grep -c '^Landed: R-0797' .agent/live_review.md`
     reads 1; `grep -c '^Done: R-0797' .agent/live_review.md` reads 0.
  G4 THE PLAN AT C1. `.agent/plan.md` equals PLAN30 byte for byte (expect
     1375 bytes); `wc -l` under 50 (expect 33); `grep -c '^## Goal'`
     and `grep -c '^## Next Steps'` each 1.
  G5 THE DOCS GATES after C2, before `gh pr create`:
       python3 -m pytest tests/docs/ -q                              (expect 295)
       python3 -m pytest tests/orchestration/test_roadmap_index.py -q (expect 30)
     Both MUST be green; if either is red, STOP before creating the PR
     and report the failure.
  G6 THE STATE READERS AND THE CANARY, serially: tests/ui_server/ (515),
     tests/orchestration/test_test_runner.py (52),
     tests/regression/test_resource_safety.py (21),
     tests/orchestration/test_integrity_gate.py (16),
     tests/cli/test_golden_path.py (42).
  G7 STRUCTURE AND THE PR. `git status --porcelain` empty before C3 is
     staged; `git diff --stat 893ae3c9..<C2> -- packages/ apps/ tests/
     docs/ scripts/` empty; per-commit `git show --numstat --format=""`
     for C0a, C0b, C1 (two paths), C2 (two paths) against the handback's
     Commits table; `python3 -m apps.cli.grouped integrity check --json`
     passed / fail_count / high_blockers_open; the PR number, URL,
     base/head, not a draft, not merged; the push result.

SLICES. Each lies between its own one-line BEGIN and END marker; the
slice is the bytes between the BEGIN marker's newline and the newline
before the END marker, EXCLUDING that final newline.

<<<BEGIN RECORD28>>>
Gate: R28 — the F262 R28 entry, the closure commit and the pull request. VERDICT FAIL ON ONE GATE, EVERYTHING ELSE HELD, over the range `d887906b..893ae3c9` (C0a `71635dd5`, C0b `9364ff12`, C1 `7dbcde4c`, C2 `423bc28d`, handback `893ae3c9`), independently re-verified by the reviewer. TRANSPORT HELD IN ITS PRIMARY FORM: scratch original, committed `.agent/authored/f262-r28.md` and `.agent/last_block.md` equal byte for byte, sha256 `9005edf35c4330d3e7e06407810c3414bd8291e09ade30b8c25b554deee32d55`, 18922 bytes. THE LEDGER APPEND (RECORD27) HELD: 2508240 (at `9364ff12`) plus two newlines plus RECORD27 (4977 bytes) equals 2513219 (at `7dbcde4c`), tail equal, the flipped-byte control rejected. THE PLAN HELD: `.agent/plan.md` equals PLAN29 (1449 bytes, 33 lines by `wc -l`). THE CLOSURE COMMIT LANDED AS ONE COMMIT (`423bc28d`), all five pairs applied byte for byte with every FROM occurring once: `docs/roadmap/STATUS.md` line 24 now reads `- [x] F262 — List commands v2 (dates, sort, filter) (T001–T003 complete; accepted 2026-09-05 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f262-closure · package remedy-review-20260905-112903-READY_FOR_REVIEW.zip · SHA-256 83953f280dd856277529add08212b767e5588370da937ccfad5608923a73295e · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD a5896aa6c7e8ebc7616fdef62f5964f6bb9772a0)` and no `[~]` line remains; `README.md` reads `72 of 267 registered items accepted.` and `| 2 | Minimal Self-Build Runtime | 15 | 20 |`; `scripts/self_use_queue.json` carries `"consumed_by": "F262"` on SU-009 and parses. THE STATE READERS AND THE CANARY HELD (515 / 52 / 21 / 16 / 42), `test_roadmap_index.py` 30, the integrity check unchanged (`passed` true, `fail_count` 0, no open Blocker/High). THE DOCS GATE WENT RED, AND THE WORKER CORRECTLY STOPPED BEFORE `gh pr create`: `python3 -m pytest tests/docs/ -q` read 1 failed, 294 passed — `TestPrimaryDocsAreHonest::test_the_readme_reports_the_accepted_foundation_and_no_later_feature`, `AssertionError: README claims F267 accepted; STATUS does not` — reproduced by the reviewer at `893ae3c9`. THE CAUSE IS THE REVIEWER'S OWN AUTHORED SLICE, not the application: README_PARA_TO's last line, `the remaining nine are F267's).`, sits inside the `Accepted in Tier 2 so far:` block, and that test reads every `F\d{3}` token in an Accepted block as a claim of acceptance while F267 is `[ ]`. The reviewer read that test before authoring (it is quoted in the round-24 authoring notes) and still put a registered-but-unaccepted id inside the block it guards — the §3 checklist item 34 class (a file's guards read, then not applied to the bytes written into it), landing as WRONG STATE ON DISK under `README.md` with `tests/docs/` red at the committed head `423bc28d`, so it takes an id: FINDING R-0797 (Low), registered in this round's own C1 immediately below this entry, fix authored in the same block. NO PULL REQUEST EXISTS (`gh pr list` empty at `893ae3c9`), nothing merged. Rule A4's rendering is disturbed by construction — a README repair must now follow the STATUS flip — and that is declared here rather than repaired by history rewrite (guardrail G2). THE STRUCTURE OTHERWISE HELD: `git status --porcelain` empty, `git diff --stat d887906b..423bc28d -- packages/ apps/ tests/` empty, numstat cells matching the handback's table (275/0, 228/185, 3/1 + 13/18, 1/1 + 8/3 + 1/1), all commits single-parent and under 500 insertions, head equal to `origin/feature/f262-list-commands-v2`. FOUR DEVIATIONS WERE DECLARED (the ordered PR skipped on the red gate; PLAN29's now-stale Next Steps left untouched because the change set bound C3; unrefused `cd` prefixes, a `for` loop and `${PIPESTATUS[0]}`; the handback's Next differing from the block's ordered sentence) — all correct behaviour. Open findings before this round's registrations: 356 registered minus 77 `Done:` lines equals 279 open; after R-0797 below, 357 minus 77 equals 280. The repair is this round: one README pair, the docs gate re-run, then the pull request.
<<<END RECORD28>>>

<<<BEGIN FINDING>>>
- R-0797 — Low, THE F262 CLOSURE COMMIT PUT A REGISTERED-BUT-UNACCEPTED FEATURE ID INSIDE README.md's `Accepted in Tier 2 so far:` BLOCK, AND `tests/docs/` IS RED AT THE COMMITTED TIP `423bc28d`. Measured by the reviewer at `893ae3c9`: `python3 -m pytest tests/docs/ -q` reads 1 failed, 294 passed; the failing id is `tests/docs/test_docs_consistency.py::TestPrimaryDocsAreHonest::test_the_readme_reports_the_accepted_foundation_and_no_later_feature`, `AssertionError: README claims F267 accepted; STATUS does not`. The offending bytes are the reviewer-authored README_PARA_TO slice of `.agent/authored/f262-r28.md`, applied byte for byte at `423bc28d`: its closing line `the remaining nine are F267's).` lands at `README.md` line 67 inside the block the test scans with `Accepted[^\n]*:\n((?:[^\n]+\n)+)` and `\bF(\d{3})\b`, and `F267` is `- [ ]` at `docs/roadmap/STATUS.md` line 99. ROOT CAUSE: §3 checklist item 34 — the reviewer read that very test while planning the round-24 registration (its one-directional pin was noted in the authoring notes) and then wrote a slice that violates it, because the check was applied to the pin's DIRECTION and not to the TOKENS the slice would put inside the guarded block. Product effect: the root README's accepted list makes a false claim on disk and the docs suite is red at a committed head, the F112 R30 shape this feature's own round-28 constraint 7 warned against for the numerals and did not warn against for the prose. FIX (authored in the round-29 block that registers this finding): one REWRITE pair over `README.md` replacing the two-line tail `sort/filter/limit behaviour wired into 15 of the 24 in-scope commands;\nthe remaining nine are F267's).` with wording that names no `F\d{3}` token (`the remaining nine belong to the follow-up feature registered right\nafter F086's line in docs/roadmap/STATUS.md).` is REJECTED because it still names F086 — acceptable, F086 is `[x]` — but the chosen wording names no id at all: `the remaining nine belong to the follow-up feature the STATUS ledger\nregisters next).`), then `tests/docs/` re-run to 295 passed at the repairing commit; the reviewer resolves this finding only after reproducing that count. Searched before minting per §3 item 30: `grep -n "Accepted in Tier\|README claims" .agent/live_review.md` finds `R-0570` (the README list pinned in ONE direction only — a different defect: an INCOMPLETE list passing, where this is a FALSE entry failing) and no open finding describing a false accepted claim, so a new id is taken.
<<<END FINDING>>>

<<<BEGIN PLAN30>>>
# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md, scoped by DECISION F262 D4; the nine
remaining wirings are F267's per DECISION F262 D5).

## Current Step

Round 29, session 9 — the repair of round 28's red docs gate and the
pull request. Books RECORD28 (FAIL on G6, all else held), registers
FINDING R-0797 (the reviewer's README slice named F267 inside an
"Accepted" block), applies one README pair that names no feature id,
re-runs `tests/docs/` to 295, then `gh pr create`. The STATUS `[x]`
line, README numerals and `consumed_by=F262` landed at `423bc28d` and
are untouched.

## Next Steps

None on this branch — F262 closes with this round's pull request. The
reviewer reads the PR checks, merges under the operator's 2026-09-05
authorization, and verifies `main`. R-0797 stays `Landed:` until the
next feature's first round books its `Done:`.

## Risks

- A README repair after the STATUS flip is the F112 R30 shape; it is
  declared, not hidden, and the flip commit itself is not rewritten.
<<<END PLAN30>>>

<<<BEGIN PARA_FROM>>>
sort/filter/limit behaviour wired into 15 of the 24 in-scope commands;
the remaining nine are F267's).
<<<END PARA_FROM>>>

<<<BEGIN PARA_TO>>>
sort/filter/limit behaviour wired into 15 of the 24 in-scope commands;
the remaining nine belong to the follow-up feature the STATUS ledger
registers next).
<<<END PARA_TO>>>

<<<BEGIN PRBODY>>>
## Summary
- Every list-shaped CLI command now carries one shared option surface —
  `--sort <field> [--desc] --since <when> --until <when> --limit <n>` —
  attached mechanically by the command catalog
  (`apps/cli/command_catalog.py`: `_is_list_command`, `_with_list_options`),
  so a new list command gets the flags by construction.
- Rows carry CREATED/UPDATED dates (or the store's own equivalent) in text
  and `--json`; `packages/orchestration/list_options.py`
  (`apply_list_options`, `parse_time_bound`, `ListOptionError`) implements
  newest-first default sort, `--since`/`--until` filtering (ISO-8601 or
  `2d`/`12h`), `--limit`, and a non-zero exit naming the valid fields on an
  unknown `--sort`.
- Wired into 15 commands: job.list, queue.list, loop.list, project.list,
  patch.list, worker.list, tournament.list, memory.list, blocker.list,
  decision.list, external-builder.submission-list, review.list,
  propose.list, config.list, execution.list — each with regression tests.

## Key decisions
- DECISION F262 D4 scopes Acceptance to 24 of the catalog's 28 list-shaped
  commands (three static registries and one name-browsed policy catalog
  excluded permanently).
- DECISION F262 D5 (operator ruling 2026-09-05, Option B): the nine
  remaining wirings, the catalog-driven handler test and the ten-second-demo
  smoke test split into the newly registered feature F267
  (`docs/roadmap/features/T2_F267.md`); F262 closes at the D4 scope.
  FINDING R-0796 stays open as documented Medium risk, owned by F267.
- DECISION F262 D6 records why the operator-ordered "non-deterministic
  packaging" finding was NOT registered (the F114 BLOCKED zip was a
  deliberate red control).
- D1–D3: CREATED-date sourcing for patch/loop rows; queue.list keeps
  priority order and loop.list keeps config-declaration order as defaults.

## How to review
- `docs/roadmap/features/T2_F262.md` Built State names every shipped
  symbol and test file; `T2_F267.md` carries the split-off scope.
- Full round-by-round record: `.agent/live_review.md`, `Gate: R1` through
  `Gate: R28` of the F262 entries; decisions in `.agent/decisions.md`
  (DECISION F262 D1–D6).
- Round 29 is a one-pair README repair after the closure commit: the
  closure commit's capability paragraph named F267 inside an "Accepted"
  block, which `tests/docs/` correctly rejected (FINDING R-0797, `Landed:`
  on this branch, booked `Done:` by the next feature's first round).

## Verification
- Integration gate (round 25): full suite clean at the merge-base with
  `main` — 19676 passed / 23 skipped / 0 failed on branch, 19601 / 23 / 0
  at base, both failure sets empty, UI parity held as an event.
- Closure evidence bundle (round 27, job `f262-closure`): seven scoped
  suites green — `test_list_options.py` 11, `TestListCommandOptions` 3,
  `test_config_cmd.py` 16, `test_worker_facade_cmd.py` 70,
  `test_managed_builder_execution_cli.py` 12, `test_queue_cmd.py` 28,
  `tests/docs/` 295 — all eight closed-schema gates present; review zip
  `remedy-review-20260905-112903-READY_FOR_REVIEW.zip` `PACKAGE_STATUS=READY_FOR_REVIEW` (SHA-256 `83953f280dd856277529add08212b767e5588370da937ccfad5608923a73295e`), red control
  confirmed `BLOCKED_EVIDENCE`.
- `integrity check --json` (module route): `passed: true`, `fail_count: 0`,
  no open Blocker/High findings. Self-use precondition: SU-009 generated,
  run to the approval gate (blocked, the correct outcome), defects added as
  evidence to open `R-0784`.
- Latest live-review verdict: PASS_WITH_RISKS — ACCEPTED. Open findings
  ledger-wide: 280 (pre-existing project debt, none Blocker/High; R-0796
  is left open by decision, R-0797 is repaired on this branch and awaits
  its `Done:` booking).

## Runtime actuals
- 29 delegated rounds across 9 sessions (self-drive, one branch, no
  paste relay).
- Wall clock / token / cost totals: not-measured (this workflow's ledger
  does not track them per round).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01LvvDEqLkieE84dZcwifEyU
<<<END PRBODY>>>

Handback: write .agent/handoff.md per docs/agents/handback_template.md
and AGENTS.md - Session line `SESSION 9 of feature F262 · round 29 ·
rounds so far 29` with one sentence of context self-assessment, Range
`Review of 893ae3c9..<C2>`, one changed-files table per commit (C0a, C0b,
C1, C2; C3 grouped per the self-reference exception), an item-status table
over C0a..C3 and G1..G7, External actions (the push, `gh pr create` with
the PR number), raw Verification per gate, Authored-text proofs,
Deviations, and Next: "the reviewer reads the PR's hosted checks and
merges under the operator's 2026-09-05 authorization; F262 is closed on
this branch; R-0797's `Done:` is booked by the next feature's first round".
