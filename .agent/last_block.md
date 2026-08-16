# F083 R25 — session-closing persistence round

SPLIT round, and deliberately a SMALL one: it writes down a verdict that already
exists and nothing else. It changes `.agent/` only — no file under `docs/`,
`packages/`, `apps/`, `scripts/` or `tests/` is touched.

Why this round exists rather than folding into the next one: R24's verdict is PASS
and lives only in the reviewer's round report, which dies with the session. The
next round is the integration gate, a full-suite round that does not fit in the
remaining session budget (self-drive protocol G7). A verdict that waits for a
round nobody has started is a verdict that can be lost, so it is persisted now and
the session ends behind it.

Base: `git rev-parse HEAD` MUST print 94ceafa2 before the first commit. If it does
not, stop and report — every gate below is measured against that base.

## Slice convention

Every slice is delimited by its own `--- BEGIN SLICE <NAME> ---` and
`--- END SLICE <NAME> ---` markers, which are TRANSPORT ONLY and NEVER reach a
target file. A slice's content begins on the line AFTER its BEGIN marker and ends
on the line BEFORE its END marker, newline included. The slices carried here are
named RECORD-R24 and PLAN. Neither has a FROM: line: RECORD-R24 is an EOF-APPEND
and PLAN is a whole-file replacement. Extract both programmatically from the
COMMITTED `.agent/authored/f083-r25.md` by their markers — never by retyping.

--- BEGIN SLICE RECORD-R24 --- (EOF-APPEND to .agent/live_review.md, C1)

Gate: R24 — PASS. Every one of the round's sixteen ordered gates reproduces at the reviewer's own hand, from the repository root at 94ceafa2, and every measured value equals the one the handback reports. TRANSPORT, against the reviewer's OWN original bytes and NOT by digest fallback (§4.9): the committed `.agent/authored/f083-r24.md` is byte-IDENTICAL to the reviewer's emitted file and `.agent/last_block.md` is byte-identical to both, all three at sha256 cb9ab43ea41ae179 over 21312 bytes and 232 lines, under the 400-line cap. C1 is a pure append and was proved so: `.agent/live_review.md` goes 293293 B to 300239 B, the former prefixes the latter, the 6946-byte tail byte-EQUALS the RECORD-R23 slice extracted from the committed authored file by its markers, `git show --numstat` is `6 0` so no committed text was edited, and the file's count of transport BEGIN-markers is unchanged at four between base and HEAD. The D6FIX pair is a REWRITE as declared and was checked that way, scoped to `docs/system/ci-self-check-v1.md` alone: the FROM occurred exactly 1x before the replacement and exactly 0x after, the TO exactly 1x after, and the document's marker count and its count of bare FROM:/TO: label lines are both 0. `.agent/plan.md` byte-equals its PLAN slice at sha256 e1f4becafde7b177, 2303 bytes, 39 lines under the 50-line cap, `## Goal` and `## Next Steps` present, 0 unchecked-box lines. THE MEMBERSHIP GATE REPRODUCES ON BOTH FILES, which is the whole point of the repair: collecting each stage's own selection out of `CI_STAGES` gives `standard` 1 node id containing `test_typescript_compiles` and 7 containing `test_apps_ui_probe`, and gives `fast`, `ui`, `smoke`, `budgets` and `excluded` 0 and 0 each, every collection at exit 0 — so the corrected paragraph's "the `standard` stage and no other" is measured rather than asserted, and `tests/runtimes/test_apps_ui_probe.py` does carry the `pytest.mark.skipif` on a missing `apps/ui/node_modules/.bin/vite` that the paragraph now cites. The remaining gates reproduce: the range gate prints nothing for `packages/ apps/ scripts/ tests/`; ruff is `Found 26 errors.` at exit 1, so the ratchet held; `tests/docs/` is 295 passed; the three stage- and workflow-guard files are 25 passed; the verification set with the canary is 78 passed, every one at exit 0; both relative links in the document resolve; the open set recomputes to 116 registered, 11 resolved, 0 landed, 105 open, max R-0488, next free R-0489, no duplicate id and no unregistered resolution; the change set is exactly the six paths the handback lists; per-commit insertions are 232, 102, 6, 13, 14 and 48, none near 500; and the history is six single-parent commits chained to 24bc77c5 with no amend, rebase or reset. All five declared deviations are honest and none is a defect. Two deserve naming. Running gate 8 before C2 rather than after is the worker declining to commit a correction it had not yet verified, under a gate whose own STOP clause says a disagreeing reading means the document is right; the reading is invariant across the round because it reads only `packages/` and `tests/`, and the reviewer re-took it at HEAD and got the same twelve numbers. And gate 13 reporting 25 where the R23 record says 20 is not a regression but a change of scope the worker correctly identified and re-measured both ways: R23 ordered two guard files, this block ordered three, `test_ci_workflow.py` contributes the other 5, and re-running the two-file form at HEAD still returns exactly 20. The C0b numstat note is likewise correct — `git commit`'s rename-detected summary and `git show --numstat` disagree on a whole-file state rewrite, both readings sit far under the cap, and that commit is an exempt single `.agent/**` state-file rewrite in any case.

Done: R-0488 — resolved, and the replacement text was measured before it was written rather than after. C2 of R24 rewrote the D6 section so that it names the `standard` stage rather than a count of tests: it states that the toolchain is a precondition of `standard` and of no other stage, that two of the files `standard` selects need the install and both skip without it, that `test_typescript_compiles` carries `integration` and shells out to the compiler while the Vite probes in `tests/runtimes/test_apps_ui_probe.py` carry `subprocess` and skip on a missing `apps/ui/node_modules/.bin/vite`, and that the `ui` stage needs nothing installed at all. The reviewer re-ran the collection itself at 94ceafa2 across every stage — `standard` 1 and 7, every other stage 0 and 0 — so each of those claims is now pinned to a measurement, and the paragraph no longer carries a numeral about tests that a later marker change could silently falsify. The string "ONE TEST" occurs nowhere in the document. R-0486's correction, which this finding sat on top of, is unaffected and stays resolved.
--- END SLICE RECORD-R24 ---
--- BEGIN SLICE PLAN --- (WHOLE FILE, replaces .agent/plan.md, C2)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0489. `.agent/live_review.md` is the source of
truth for the open set; this file repeats no count of it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R24 is closed PASS and R25 recorded it. R-0488 is resolved: the D6 section now
names the `standard` stage instead of counting tests, and every claim in it is
pinned to a stage collection. T001, T002 and T003 are COMPLETE and no
documentation claim in this feature is unverified against a measurement. R25
carries no work of its own — it exists so the R24 verdict was written down before
the session ended rather than waiting on the integration-gate round.

## Next Steps
1. The integration-gate round: the full suite exactly once, per
   docs/agents/integration_gate.md. Budget it as a round of its own — a branch run
   plus a base run in a throwaway worktree, roughly 23 minutes of suite each, and
   the base worktree needs `apps/ui/node_modules` parity or per-id attribution.
2. Then closure per docs/roadmap/STATUS_closure_protocol.md — evidence job plus a
   FRESH review zip, both mandatory, then the authored STATUS line and the PR.

## Risks
- Hosted wall time is still unmeasured, and the first hosted run is that
  measurement. `standard` needs 935.14 s at its slowest local sample against a
  2100 s budget, and it is also the stage carrying the toolchain-dependent tests.
- The lint ceiling is a RATCHET. Raising it to make a round green converts the
  one honest lint signal in this repository into decoration.
- R-0482 (a live `NameError` on a guard's refusal path) and R-0487
  (`docs/README.md` is never link-checked) are both frozen here and belong to a
  paydown branch: each is a code- or test-content fix this feature may not make.
--- END SLICE PLAN ---

## Change — exactly these paths, nothing beyond them

**C0a** saves this block verbatim to `.agent/authored/f083-r25.md`. **C0b** mirrors
the COMMITTED copy over `.agent/last_block.md`.

**C1** applies RECORD-R24 as an EOF-append to `.agent/live_review.md`, the only
file in that commit.

**C2** applies PLAN. **C3** rewrites `.agent/handoff.md`.

The ordered sequence is exactly C0a, C0b, C1, C2, C3 — five commits, no gaps and no
spare numbers.

## Constraints

1. Never work on `main`; never force-push; never amend, rebase or reset. No PR is
   created and none is merged.
2. `.agent/live_review.md` is APPENDED to once, at C1. No committed text in it is
   edited; write no resolution or `Landed:` line of your own.
3. No marker line reaches a target file. Both slices are extracted from the
   COMMITTED `.agent/authored/f083-r25.md` by their markers.
4. NOTHING outside `.agent/` is modified. In particular
   `docs/system/ci-self-check-v1.md` is finished and is NOT touched again. Gate 7
   proves it.
5. The 26 ruff errors are NOT fixed and the lint ceiling is NOT raised.
6. If any gate is red, stop at that gate, record its real output verbatim, and hand
   back. Do not widen the change set to route around it.
7. Your handback's Deviations section states explicitly whether the ordered commit
   sequence was followed, per the rule in `docs/agents/handback_template.md`.
8. This is the session's LAST round. Your handoff is the only thing the next
   session reads, so its Next section must name, in order: read `.agent/STOP` from
   disk, run the Open PR Gate, then the integration-gate round per
   docs/agents/integration_gate.md.

## Done when — every command run from /home/decodeux/Repos/remedy, each its own
## unpiped process, each exit code read from that process

1. `pwd` printed FIRST. `git status --porcelain` EMPTY before the first commit and
   before C3. `git worktree list` ONE line at round start and at handback.
   `.agent/STOP` ABSENT at both.
2. `git rev-parse HEAD` at round start EQUALS 94ceafa2.
3. `.agent/authored/f083-r25.md` and `.agent/last_block.md` byte-equal as COMMITTED
   blobs; report their sha256, byte count and line count.
4. `.agent/live_review.md` at C1: the pre content PREFIXES the post content, the
   tail byte-EQUALS the RECORD-R24 slice as extracted from the committed authored
   file by its markers, and `git show --numstat` has deletion column 0. Also report
   the file's count of transport BEGIN-marker lines at base and at HEAD; they must
   be equal.
5. `.agent/plan.md` byte-equals the PLAN slice; report its sha256, line count
   (under 50), that `## Goal` and `## Next Steps` are present, and its count of
   unchecked-box lines.
6. The string `ONE TEST` occurs exactly 0 times in
   `docs/system/ci-self-check-v1.md`. Report the count. Scope it to that path: the
   RECORD-R24 text quotes the retired phrase on purpose.
7. `git diff --name-only 94ceafa2..HEAD -- docs/ packages/ apps/ scripts/ tests/`
   prints NOTHING. Report that it printed nothing.
8. `python3 -m ruff check .` — report the `Found N errors.` line and the exit code.
   Expected 26 errors at exit 1, unchanged. Take this reading AT C2 and name the
   commit; C2 and not C3, because C3 writes the handback that carries the reading.
9. `python3 -m pytest tests/regression/test_resource_safety.py
   tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q` —
   the verification set and the canary, which read `.agent/` state live and are
   therefore the gates that matter for a state-only round. Report the passed count
   and exit code.
10. `python3 -m pytest tests/docs/ -q` — report the passed count and exit code.
11. The open set, recomputed from `.agent/live_review.md` at HEAD: count every
    `^- R-\d+ — ` paragraph, every `^Done: R-\d+ — ` line and every
    `^Landed: R-\d+ — ` line, report registered, resolved, landed and open, the
    maximum id, the next free id, and that no id repeats and no resolution names an
    unregistered id. R-0488 must appear as resolved and R-0482 and R-0487 must
    appear as still open.
12. The change set: `git diff --name-only 94ceafa2..HEAD` lists exactly
    `.agent/authored/f083-r25.md`, `.agent/handoff.md`, `.agent/last_block.md`,
    `.agent/live_review.md` and `.agent/plan.md`. Report the list and that nothing
    else is in it.
13. Per-commit insertions from `git show --numstat`, reported per commit, none
    exceeding 500; and the history is linear with no amend, rebase or reset.

## Handback

Completion report plus a rewritten `.agent/handoff.md` per
`docs/agents/handback_template.md`: feature and round, branch, the commit table,
the item-status table with every ordered item above appearing exactly once, the
real verification results, the open-findings count, and the next expected action
per constraint 8.

Fortschritt: 93 % (F083 beansprucht · R1 bis R7, R9 bis R21, R23 und R24 PASS, R8 und R22 FAIL — beide in der Folgerunde repariert · T001, T002 und T003 fertig: Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht, die gemessenen Stage-Budgets, die gehostete Workflow-Datei als dünner Wrapper mit ihren Guards, und die Doku samt Laufzeit-Budget-Tabelle, deren Aussagen jetzt alle gegen eine Collection gemessen sind · D4 schliesst eine eigene Determinismus-Stage aus, D5 friert die 26 ruff-Fehler ein, D6 macht den lokalen tsc-Compiler tragend · offen sind im Feature selbst nur noch das Integration Gate und die Closure; R-0482 und R-0487 sind bewusst auf einen eigenen Paydown-Branch geroutet · gehostete Laufzeit ist weiterhin NICHT gemessen) — Rundenzahl gemessen, Prozentwert geschätzt
