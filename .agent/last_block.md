STEP CLOSURE COMMIT + PR / ROUND 28 - F262 List commands v2 (dates, sort, filter) (FINAL ROUND ON THIS BRANCH)
FEATURE F262 - List commands v2 (dates, sort, filter) (Tier 2) - SESSION 9, ROUND 28

Goal
  Book round 27's verdict (RECORD27 - evidence bundle + review zip,
  algorithm steps 1-2 complete), then execute the closure commit itself
  (STATUS `[x]` flip + README sync + self_use_queue consumed_by edit, all
  in ONE commit per docs/roadmap/STATUS_closure_protocol.md algorithm
  step 5) and open the pull request. Do NOT merge the PR - the reviewer
  reads its checks and merges under the operator's authorization.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f262-r28.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD27 to .agent/live_review.md (append) and PLAN29 to
      .agent/plan.md (whole-file replacement)
  C2  THE CLOSURE COMMIT: apply the STATUS pair to docs/roadmap/STATUS.md,
      the three README pairs to README.md, and the QUEUE pair to
      scripts/self_use_queue.json - ALL FIVE PAIRS IN THIS ONE COMMIT
  then push, run the docs gates (G6, must be green), then `gh pr create`
  C3  rewrite .agent/handoff.md - the FINAL handback

Change set - EXACTLY these paths and nothing else
  .agent/authored/f262-r28.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md, .agent/plan.md (C1) - docs/roadmap/STATUS.md,
  README.md, scripts/self_use_queue.json (C2) - .agent/handoff.md (C3)

Constraints
  1. Every authored slice (RECORD27, PLAN29, PRBODY, every pair) is
     applied BYTE FOR BYTE: extract by its one-line BEGIN/END markers
     from the COMMITTED .agent/authored/f262-r28.md (marker lines
     EXCLUDED), by a Python script, never retyped.
  2. C1 is the first substantive commit of the round.
  3. RECORD27 appends to .agent/live_review.md as EXACTLY TWO newline
     bytes followed by the slice; PLAN29 REPLACES .agent/plan.md whole;
     neither carries a trailing newline.
  4. Read .agent/STOP before C0a, before C2 and before C3; if present,
     finish the commit in hand, write the handback, stop - and create no
     PR.
  5. Pairs are applied with str.replace(FROM, TO, 1) after confirming
     FROM occurs EXACTLY ONCE in the file. Containment readings computed
     before emission: STATUS `TO contains FROM: false`, README_COUNT
     `TO contains FROM: false`, README_TIER2 `TO contains FROM:
     false`, README_PARA `TO contains FROM: false`, QUEUE
     `TO contains FROM: false` - every one a REWRITE, so no FROM-zero
     count is ordered; re-check each and report what you measured.
  6. THE OPEN SET, §3 item 10's line-count formula: registered / Done /
     open BEFORE C1 and AFTER C1, both UNCHANGED at 356 / 77 / 279.
  7. THE CLOSURE COMMIT IS ONE COMMIT, NOT TWO (F112 R30 lesson: a split
     flip left `tests/docs/` red until a repair commit). All five pairs
     land together in C2.
  8. This round does not touch packages/, apps/ or tests/. Sandbox
     re-expressions as in every prior round (Python for cp/cmp/env/
     loops), each reported.
  9. THE PULL REQUEST, after C2 is pushed and G6 is green: extract the
     PRBODY slice to a scratch file under .remedy-wt/ (or write it via a
     heredoc if that path is refused) and run
       gh pr create --title "F262: List commands v2 (dates, sort, filter)" --base main --head feature/f262-list-commands-v2 --body-file <that file>
     Report the PR number and URL. Do NOT run `gh pr merge`.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 HYGIENE. `.agent/STOP` at each of constraint 4's reads; `git status
     --porcelain | wc -l` 0 after each of C0a, C0b, C1 and C2.
  G2 TRANSPORT. `sha256sum .agent/authored/f262-r28.md
     .agent/last_block.md` - one digest, twice.
  G3 THE RECORD APPEND (RECORD27). Base size of .agent/live_review.md
     before C1 (expect 2508240, no trailing newline); RECORD27's byte
     length (expect 4977); base + 2 + that (expect 2513219)
     versus the post-C1 length; tail equality "\n\n" + RECORD27; negative
     control in a scratch copy (one flipped byte REJECTED).
  G4 THE PLAN AT C1. `.agent/plan.md` equals PLAN29 byte for byte
     (expect 1449 bytes); `wc -l` under 50 (expect 33);
     `grep -c '^## Goal'` and `grep -c '^## Next Steps'` each 1.
  G5 THE FIVE PAIRS AT C2. For each: FROM count immediately before
     applying (must be 1), the measured `TO contains FROM` beside the
     label. After all five: STATUS.md's F262 line, README.md's
     accepted-count line and Tier 2 row, and the SU-009 `consumed_by`
     line, exactly as they read; `grep -c '^- \[x\] F262 — ' docs/roadmap/STATUS.md`
     1 and `grep -c '^- \[~\] ' docs/roadmap/STATUS.md` 0.
  G6 THE DOCS GATES, before `gh pr create`:
       python3 -m pytest tests/docs/ -q                              (expect 295)
       python3 -m pytest tests/orchestration/test_roadmap_index.py -q (expect 30)
     Both MUST be green; if either is red, STOP before creating the PR
     and report the failure.
  G7 THE FOUR STATE READERS AND THE CANARY, serially:
       python3 -m pytest tests/ui_server/ -q                          (expect 515)
       python3 -m pytest tests/orchestration/test_test_runner.py -q   (expect 52)
       python3 -m pytest tests/regression/test_resource_safety.py -q  (expect 21)
       python3 -m pytest tests/orchestration/test_integrity_gate.py -q (expect 16)
       python3 -m pytest tests/cli/test_golden_path.py -q             (expect 42)
  G8 THE TREE, THE COMMITS, THE PR. `git status --porcelain` empty
     before C3 is staged; `git diff --stat d887906b..<C2> -- packages/
     apps/ tests/` empty; per-commit `git show --numstat --format=""`
     for C0a, C0b, C1 (two paths), C2 (three paths) against this
     handback's Commits table; the PR number, URL, base/head, not a
     draft, not merged; re-run `python3 -m apps.cli.grouped integrity
     check --json` and report passed / fail_count / high_blockers_open.

SLICES. Each lies between its own one-line BEGIN and END marker; the
slice is the bytes between the BEGIN marker's newline and the newline
before the END marker, EXCLUDING that final newline.

<<<BEGIN RECORD27>>>
Gate: R27 — the F262 R27 entry, algorithm steps 1-2 of `docs/roadmap/STATUS_closure_protocol.md`: the evidence bundle and the review zip, no production code touched. VERDICT PASS over the range `0609f113..d887906b` (C0a `fca83123`, C0b `694a11e1`, C1 `a5896aa6`, handback `d887906b`), independently re-verified by the reviewer. TRANSPORT HELD IN ITS PRIMARY FORM: scratch original, committed `.agent/authored/f262-r27.md` and `.agent/last_block.md` equal byte for byte, sha256 `68536a44a4274bd438ee53e58d2adb26201577e6df2fb62ede978fc4f2b2938f`, 18010 bytes. THE LEDGER APPEND (RECORD26) HELD: 2503246 (at `694a11e1`) plus two newlines plus RECORD26 (4992 bytes) equals 2508240 (at `a5896aa6`), tail equal, the flipped-byte control rejected. THE PLAN HELD: `.agent/plan.md` equals PLAN28 (1681 bytes, 38 lines by `wc -l`). THE EVIDENCE BUNDLE HELD, REPRODUCED FROM THE PACKAGE ON DISK: evidence job `f262-closure` carries seven verification runs, each with `len(node_ids)` equal to `selected` equal to `passed` — `tests/orchestration/test_list_options.py` 11, `tests/test_command_catalog.py::TestListCommandOptions` 3, `tests/cli/test_config_cmd.py` 16, `tests/cli/test_worker_facade_cmd.py` 70, `tests/cli/test_managed_builder_execution_cli.py` 12, `tests/cli/test_queue_cmd.py` 28, `tests/docs/test_docs_consistency.py` 295 — zero failed/skipped/deselected, every `output_hash` equal to sha256 of its `stdout_summary`, the `_unsafe_text` pre-scan 0 rejected with its red control answering "a local absolute path", all eight closed-schema gate files present (final_verifier_report, fresh_evidence, artifact_contract, change_provenance, manifest_integrity, postmortem_integrity, commit_execution, runtime_integration — confirmed by the reviewer from the zip's member list), the template's computed head equal to C1, the producer's own verdict PASS_WITH_RISKS. THE REVIEW ZIP HELD, REPRODUCED BY THE REVIEWER OVER THE FILE ON DISK: `remedy-review-20260905-112903-READY_FOR_REVIEW.zip` at `/home/decodeux/Repos/remedy-history/zips/`, 22992203 bytes, sha256 `83953f280dd856277529add08212b767e5588370da937ccfad5608923a73295e`, matching the worker's reported digest exactly; its `.review_zip_manifest.json` reads `package_status` READY_FOR_REVIEW, `ready_gate_matrix.ok` true, `blocking_reasons` empty, `committed_review_subject.head_commit` `a5896aa6c7e8ebc7616fdef62f5964f6bb9772a0` (C1) and `committed_review_subject.base_commit` `7c65d9ccfb512aef1c3eea0245030647332c26ea`. THE RED CONTROL WAS OPENED, NOT TAKEN ON REPORT: the deliberately poisoned COPY of the evidence directory (one absolute-path node id appended to `vr-0001`, 11 ids becoming 12) packaged `remedy-review-20260905-112938-BLOCKED_EVIDENCE.zip` (22992497 bytes), re-opened by the reviewer, reading `package_status` BLOCKED_EVIDENCE with exactly three blocking reasons — the unconfirmable VerificationTests total, `runs[0].node_ids[11]` carrying a local absolute path, and the 12-versus-11 count mismatch — proving the validator distinguishes a poisoned bundle from the real one; the two packages were built from DIFFERENT inputs by design, and the control is not evidence about the real bundle (DECISION F262 D6 records why this pair must never be read as non-determinism). PRECONDITION 3 RE-CONFIRMED: `python3 -m apps.cli.grouped integrity check --json` unchanged from round 26. THE STRUCTURE HELD: `git status --porcelain` empty at every checkpoint including immediately before the zip build, `git ls-files .remedy-wt` empty, no tracked path matching `remedy-job-evidence`, `git diff --numstat 0609f113..a5896aa6` empty for `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and for every path under `packages/`, `apps/`, `tests/`, `docs/`, `scripts/`; every numstat cell matches the handback's Commits table (232/0, 186/155, 3/1 + 18/21), all three pre-handback commits single-parent and under 500 insertions; head equal to `origin/feature/f262-list-commands-v2`. FIVE DEVIATIONS WERE DECLARED, NONE A DEFECT ON DISK: an unrefused `cd` prefix on one read-only compound, the template's line-1 docstring left reading "F009" (not an ordered value), pre-emptive Python re-expressions with no refusal to report, the control zip left under the archive dir per constraint 8, and the block's line-wrapped `job_title` applied as one line. Open findings, canonical line-count formula: 356 registered minus 77 `Done:` lines equals 279 open, unchanged; `.agent/candidates.md` remains EMPTY. ALL SIX CLOSURE PRECONDITIONS CONTINUE TO HOLD and algorithm steps 1 and 2 are complete: `Evidence job f262-closure`, package `remedy-review-20260905-112903-READY_FOR_REVIEW.zip`, SHA-256 `83953f280dd856277529add08212b767e5588370da937ccfad5608923a73295e`, archived at `/home/decodeux/Repos/remedy-history/zips`, accepted head `a5896aa6c7e8ebc7616fdef62f5964f6bb9772a0`. The next and final round on this branch is the closure commit (STATUS line, README sync, `consumed_by=F262`) and the pull request.
<<<END RECORD27>>>

<<<BEGIN PLAN29>>>
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

Round 28, session 9 — the closure commit and the pull request. Books
round 27 (evidence job `f262-closure`, package `remedy-review-20260905-112903-READY_FOR_REVIEW.zip`, accepted HEAD
`a5896aa6`), then ONE commit flips STATUS to `[x]`, syncs the
README numerals and capability list, and sets `consumed_by=F262` on
SU-009 (docs/roadmap/STATUS_closure_protocol.md algorithm step 5); then
`gh pr create`. The merge follows under the operator's 2026-09-05
authorization once hosted CI reads green.

## Next Steps

None on this branch — F262 closes with this round's pull request. The
reviewer reads the PR checks, merges, and verifies `main`. The next
feature is claimed per Rule A5 in a fresh session.

## Risks

- README's derived numerals (accepted count, Tier 2 Done cell) move the
  moment STATUS flips; both land in the SAME commit as the flip (F112
  R30 lesson: a split closure commit went red on `tests/docs/`).
<<<END PLAN29>>>

<<<BEGIN STATUS_FROM>>>
- [~] F262 — List commands v2 (dates, sort, filter)
<<<END STATUS_FROM>>>

<<<BEGIN STATUS_TO>>>
- [x] F262 — List commands v2 (dates, sort, filter) (T001–T003 complete; accepted 2026-09-05 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f262-closure · package remedy-review-20260905-112903-READY_FOR_REVIEW.zip · SHA-256 83953f280dd856277529add08212b767e5588370da937ccfad5608923a73295e · package path /home/decodeux/Repos/remedy-history/zips · accepted HEAD a5896aa6c7e8ebc7616fdef62f5964f6bb9772a0)
<<<END STATUS_TO>>>

<<<BEGIN README_COUNT_FROM>>>
71 of 267 registered items accepted.
<<<END README_COUNT_FROM>>>

<<<BEGIN README_COUNT_TO>>>
72 of 267 registered items accepted.
<<<END README_COUNT_TO>>>

<<<BEGIN README_TIER2_FROM>>>
| 2 | Minimal Self-Build Runtime | 14 | 20 |
<<<END README_TIER2_FROM>>>

<<<BEGIN README_TIER2_TO>>>
| 2 | Minimal Self-Build Runtime | 15 | 20 |
<<<END README_TIER2_TO>>>

<<<BEGIN README_PARA_FROM>>>
F086 release capability (wheel, `remedy --version`, release gate).

Accepted in Tier 3 so far:
<<<END README_PARA_FROM>>>

<<<BEGIN README_PARA_TO>>>
F086 release capability (wheel, `remedy --version`, release gate),
F262 list commands v2 (one shared `--sort <field> [--desc] --since <when>
--until <when> --limit <n>` surface attached to every list-shaped command
by the catalog, CREATED/UPDATED dates on the rows, and newest-first
sort/filter/limit behaviour wired into 15 of the 24 in-scope commands;
the remaining nine are F267's).

Accepted in Tier 3 so far:
<<<END README_PARA_TO>>>

<<<BEGIN QUEUE_FROM>>>
"consumed_by": "",
<<<END QUEUE_FROM>>>

<<<BEGIN QUEUE_TO>>>
"consumed_by": "F262",
<<<END QUEUE_TO>>>

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
  `Gate: R27` of the F262 entries; decisions in `.agent/decisions.md`
  (DECISION F262 D1–D6).

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
  ledger-wide: 279 (pre-existing project debt, none Blocker/High;
  R-0796 is the one this feature leaves open by decision).

## Runtime actuals
- 28 delegated rounds across 9 sessions (self-drive, one branch, no
  paste relay).
- Wall clock / token / cost totals: not-measured (this workflow's ledger
  does not track them per round).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01LvvDEqLkieE84dZcwifEyU
<<<END PRBODY>>>

Handback: write .agent/handoff.md per docs/agents/handback_template.md
and AGENTS.md - Session line `SESSION 9 of feature F262 · round 28 ·
rounds so far 28` with one sentence of context self-assessment, Range
`Review of d887906b..<C2>`, one changed-files table per commit (C0a, C0b,
C1, C2; C3 grouped per the self-reference exception), an item-status
table over C0a..C3 and G1..G8, External actions (the push, `gh pr
create` with the resulting PR number), raw Verification per gate,
Authored-text proofs (grep proof that the STATUS line and the queue line
read byte-identical to their slices), Deviations, and Next: "the
reviewer reads the PR's hosted checks and merges under the operator's
2026-09-05 authorization; F262 is closed on this branch".
