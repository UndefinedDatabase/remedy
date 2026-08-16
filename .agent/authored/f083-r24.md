# F083 R24 — repair: the D6 section undercounts what needs the UI toolchain

SPLIT round: it changes `docs/` and `.agent/` only — no file under `packages/`,
`apps/`, `scripts/` or `tests/` is touched. It records the R23 verdict (PASS),
resolves R-0486, and registers and repairs one Medium finding, R-0488, against
text the REVIEWER authored in R23 and the worker was required to apply verbatim.

Base: `git rev-parse HEAD` MUST print 24bc77c5 before the first commit. If it does
not, stop and report — every gate below is measured against that base.

## What this round fixes

R23 correctly moved the TypeScript compile check out of the `ui` stage and into
`standard`, which was R-0486 and is resolved. The replacement sentence the
reviewer authored then overcounted its own precision: it says the UI toolchain is
"a precondition of ONE TEST". It is not. Measured by collecting each stage out of
`CI_STAGES`:

    standard selects test_typescript_compiles : 1 node id
    standard selects test_apps_ui_probe       : 7 node ids

`tests/runtimes/test_apps_ui_probe.py` carries `pytestmark = [pytest.mark.subprocess,
pytest.mark.slow]`, so `standard` selects it too, and it is guarded by
`pytest.mark.skipif` on a missing `apps/ui/node_modules/.bin/vite` — a second file,
seven more node ids, the same dependency and the same skip behaviour. So the
toolchain is a precondition of the `standard` STAGE, across two files, not of one
test.

The load-bearing half of R23's correction is untouched and stays true: the check is
in `standard`, the `ui` stage needs nothing installed, and the workflow installs
unconditionally. Only the quantifier is wrong, and only the one paragraph moves.

## Slice convention

Every slice is delimited by its own `--- BEGIN SLICE <NAME> ---` and
`--- END SLICE <NAME> ---` markers, which are TRANSPORT ONLY and NEVER reach a
target file. A slice's content begins on the line AFTER its BEGIN marker and ends
on the line BEFORE its END marker, newline included. The slices carried here are
named RECORD-R23, D6FIX and PLAN. A slice with no FROM: line is an EOF-APPEND.
D6FIX is a FROM/TO pair and it is a REWRITE — its TO edits the lines of its FROM
rather than containing them (§4.9), so its proof obligation is FROM exactly 0x and
TO exactly 1x in the target file AFTER the edit. Extract every slice
programmatically from the COMMITTED `.agent/authored/f083-r24.md` by its markers —
never by retyping.

--- BEGIN SLICE RECORD-R23 --- (EOF-APPEND to .agent/live_review.md, C1)

Gate: R23 — PASS. Every one of the round's sixteen ordered gates reproduces at the reviewer's own hand, from the repository root at 24bc77c5, and every measured value equals the one the handback reports. TRANSPORT, against the reviewer's OWN original bytes and NOT by digest fallback (§4.9), because the authored block survived on disk this round: the committed `.agent/authored/f083-r24.md`'s predecessor `.agent/authored/f083-r23.md` is byte-IDENTICAL to the reviewer's emitted file, and `.agent/last_block.md` is byte-identical to both, all three at sha256 c194ee19da65f7d3 over 27100 bytes and 263 lines, under the 400-line cap. C1 is a pure append and was proved so: `.agent/live_review.md` goes 282756 B to 293293 B, the former prefixes the latter, the 10537-byte tail byte-EQUALS the RECORD-R22 slice extracted from the committed authored file by its markers, `git show --numstat` is `8 0` so no committed text was edited, and the file's count of transport BEGIN-markers is unchanged at four between base and HEAD. The D6SEC, UIROW and STDROW pairs are REWRITES as declared and were checked that way, each scoped to `docs/system/ci-self-check-v1.md` alone: every FROM occurred exactly 1x before its replacement and exactly 0x after, every TO exactly 1x after, and the document's marker count and its count of bare FROM:/TO: label lines are both 0. `.agent/plan.md` byte-equals its PLAN slice at sha256 b846a529a780417c, 2401 bytes, 40 lines under the 50-line cap, `## Goal` and `## Next Steps` present, 0 unchecked-box lines. THE NEW GATE DID THE WORK IT WAS ADDED FOR, which is the point of the round: collecting each stage's own selection out of `CI_STAGES` puts `test_typescript_compiles` in `standard` with exactly 1 node id and in `fast`, `ui`, `smoke`, `budgets` and `excluded` with 0 each, every collection at exit 0, and the `ui` selection's seven files contain no `node_modules`, `npx`, `tsc` or `npm ` at all — so the correction was verified against a collection rather than against a sentence, and R-0486 is resolved on measured ground. The remaining gates reproduce: the range gate prints nothing for `packages/ apps/ scripts/ tests/`; ruff is `Found 26 errors.` at exit 1, so the ratchet held; `tests/docs/` is 295 passed; the stage-table guards are 20 passed; the verification set with the canary is 78 passed, every one at exit 0; both relative links in the document resolve; the open set recomputes to 115 registered, 10 resolved, 0 landed, 105 open, max R-0487, next free R-0488, no duplicate id and no unregistered resolution; the change set is exactly the six paths the handback lists; per-commit insertions are 263, 182, 8, 12, 14 and 47, none near 500; and the history is six single-parent commits chained to 07d6577a with no amend, rebase or reset. Both declared deviations are honest and neither is a defect: running gate 8 before C2 rather than after is the worker correctly refusing to commit a correction it had not yet verified — constraint 7 of the block told it that a disagreeing reading meant the document was right — and the reading is invariant across the round because it reads only `packages/` and `tests/`, neither of which this round touches; the reviewer re-took it at HEAD and got the same six numbers. THE ROUND IS NOT FAULTLESS, but the fault is the reviewer's and not the worker's, and it is registered below as R-0488 rather than charged against this verdict: the replacement paragraph the reviewer authored for the D6 section calls the toolchain "a precondition of ONE TEST", and `standard` also selects seven Vite-probe node ids that need the same install. A worker ordered to apply an authored slice byte for byte cannot fix its content, and this one applied it exactly as required; charging that to the round would punish the behaviour the transport rules exist to produce.

Done: R-0486 — resolved, and verified against a collection rather than against prose. C2 of R23 applied three REWRITE pairs to `docs/system/ci-self-check-v1.md`: the stage table's `ui` row no longer claims the TypeScript check and now records that no test in that selection shells out to the node toolchain, the `standard` row now names the check and its `integration` marker, and the D6 section no longer calls the toolchain a precondition of the `ui` stage. The reviewer re-ran the membership gate itself at 24bc77c5 — `standard` 1 node id, `fast`, `ui`, `smoke`, `budgets` and `excluded` 0 each — so the document now agrees with the code on the point it previously contradicted. The markers were not touched, as T2_F083's Do-not-touch list requires, and R-0480's committed prose, which carried the original error, was correctly left alone as resolved history. What R23 did NOT get right is a quantifier in its own replacement text, registered separately as R-0488; that is a new defect in new text, not a failure of this resolution.

- R-0488 — Medium, THE D6 SECTION NOW UNDERCOUNTS WHAT NEEDS THE UI TOOLCHAIN, AND THE SENTENCE IS THE REVIEWER'S OWN. R23's replacement paragraph in `docs/system/ci-self-check-v1.md` reads "The UI toolchain is a precondition of ONE TEST, and that test is not in the `ui` stage". Measured by collecting each stage out of `CI_STAGES`, `standard` selects `test_typescript_compiles` at 1 node id AND `tests/runtimes/test_apps_ui_probe.py` at 7 node ids; that file carries `pytestmark = [pytest.mark.subprocess, pytest.mark.slow]`, which `standard`'s expression matches, and it is guarded by `pytest.mark.skipif` on a missing `apps/ui/node_modules/.bin/vite` with the reason "INTEGRATION BLOCKER: apps/ui dependencies are not installed". Eight node ids across two files depend on the install, not one. Medium and not Low: this is the same class as R-0486 and in the same paragraph — a countable claim about built behaviour in a `docs/` page, stated with a numeral that the code contradicts — and a reader deciding whether the hosted `npm ci` step is worth its minute is being shown one eighth of the reason it exists. Not High: the sentence errs toward understating the dependency, so nothing built on it is unsafe, and R23's load-bearing correction is unaffected — the check really is in `standard`, the `ui` stage really needs nothing installed, and the workflow really does install unconditionally. AUTHORSHIP IS RECORDED BECAUSE IT DETERMINES WHERE THE FIX BELONGS: the sentence was authored by the reviewer and applied verbatim by a worker that constraint 3 forbade from altering it, so this is a defect in reviewer text, not in worker execution, and R23's verdict stays PASS. The lesson generalises past this paragraph and is why the finding is registered rather than quietly patched: a reviewer correcting a counting error is exactly when a new counting error gets written, because the corrected sentence is drafted with the old wrong fact still in mind. Fixed at C2 of this round by one REWRITE pair, and gated by the same collection that measured it.
--- END SLICE RECORD-R23 ---
--- BEGIN SLICE D6FIX --- (FROM/TO pair, REWRITE, docs/system/ci-self-check-v1.md, C2)
FROM:
The hosted workflow runs `npm ci --prefix apps/ui` BEFORE `remedy ci run`. The UI
toolchain is a precondition of ONE TEST, and that test is not in the `ui` stage:
`test_typescript_compiles` in `tests/ui_server/test_dashboard_contract.py` carries
the `integration` marker, so `standard` selects it and `ui` does not. Without the
install it skips hosted, exactly as it skips on a local checkout that never ran
it, and F083's Acceptance line would be met by a skip instead of by a real
compile. The install is a workflow step rather than stage logic so the stage table
stays data and keeps naming no toolchain — which is also why the workflow installs
the toolchain unconditionally rather than per stage: the table is the only thing
that knows which stage selects that test, and the workflow deliberately reads no
part of it.
TO:
The hosted workflow runs `npm ci --prefix apps/ui` BEFORE `remedy ci run`. The UI
toolchain is a precondition of the `standard` stage and of no other stage: two of
the files `standard` selects need the installed toolchain, and both skip without
it. `test_typescript_compiles` in `tests/ui_server/test_dashboard_contract.py`
carries the `integration` marker and shells out to the TypeScript compiler; the
Vite probes in `tests/runtimes/test_apps_ui_probe.py` carry `subprocess` and skip
on a missing `apps/ui/node_modules/.bin/vite`. The `ui` stage needs nothing
installed at all. Without the install those checks skip hosted, exactly as they
skip on a local checkout that never ran it, and F083's Acceptance line would be
met by a skip instead of by a real compile. The install is a workflow step rather
than stage logic so the stage table stays data and keeps naming no toolchain —
which is also why the workflow installs the toolchain unconditionally rather than
per stage: the table is the only thing that knows which stage selects those tests,
and the workflow deliberately reads no part of it.
--- END SLICE D6FIX ---
--- BEGIN SLICE PLAN --- (WHOLE FILE, replaces .agent/plan.md, C3)
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
R23 is closed PASS and R24 recorded it. R-0486 is resolved: the CI note now puts
the TypeScript compile check in `standard`, the stage that selects it. R24
registered R-0488 — the replacement paragraph called the toolchain a precondition
of ONE test when `standard` selects eight toolchain-dependent node ids across two
files — and repaired it in the same round. T003 stays COMPLETE. No documentation
claim in this feature is now unverified against a collection.

## Next Steps
1. The integration-gate round: the full suite exactly once, per
   docs/agents/integration_gate.md. It is also the round that records R24's
   verdict and resolves R-0488. Budget it as a full round of its own: a branch run
   plus a base run in a throwaway worktree, roughly 23 minutes of suite each.
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

**C0a** saves this block verbatim to `.agent/authored/f083-r24.md`. **C0b** mirrors
the COMMITTED copy over `.agent/last_block.md`.

**C1** applies RECORD-R23 as an EOF-append to `.agent/live_review.md`, the only
file in that commit.

**C2** applies D6FIX to `docs/system/ci-self-check-v1.md`, the only file in that
commit.

**C3** applies PLAN. **C4** rewrites `.agent/handoff.md`.

The ordered sequence is exactly C0a, C0b, C1, C2, C3, C4 — six commits, no gaps
and no spare numbers.

## Constraints

1. Never work on `main`; never force-push; never amend, rebase or reset. No PR is
   created and none is merged.
2. `.agent/live_review.md` is APPENDED to once, at C1. No committed text in it is
   edited; write no resolution or `Landed:` line of your own.
3. No marker line and no `FROM:`/`TO:` label reaches a target file. Every slice is
   extracted from the COMMITTED `.agent/authored/f083-r24.md` by its markers.
4. Nothing under `packages/`, `apps/`, `scripts/` or `tests/` is modified at all,
   and NO pytest marker is added, removed or changed anywhere. Gate 7 proves it.
5. The 26 ruff errors are NOT fixed and the lint ceiling is NOT raised.
6. Every disposable worktree is removed and pruned before the handback.
7. If any gate is red, stop at that gate, record its real output verbatim, and hand
   back. Do not widen the change set to route around it.
8. Your handback's Deviations section states explicitly whether the ordered commit
   sequence was followed, per the rule in `docs/agents/handback_template.md`.

## Done when — every command run from /home/decodeux/Repos/remedy, each its own
## unpiped process, each exit code read from that process

1. `pwd` printed FIRST. `git status --porcelain` EMPTY before the first commit and
   before C4. `git worktree list` ONE line at round start and at handback.
   `.agent/STOP` ABSENT at both.
2. `git rev-parse HEAD` at round start EQUALS 24bc77c5.
3. `.agent/authored/f083-r24.md` and `.agent/last_block.md` byte-equal as COMMITTED
   blobs; report their sha256, byte count and line count.
4. `.agent/live_review.md` at C1: the pre content PREFIXES the post content, the
   tail byte-EQUALS the RECORD-R23 slice as extracted from the committed authored
   file by its markers, and `git show --numstat` has deletion column 0. Also report
   the file's count of transport BEGIN-marker lines at base and at HEAD; they must
   be equal, which is the proof none leaked.
5. D6FIX pair proof at C2, scoped to `docs/system/ci-self-check-v1.md` and to that
   file ALONE: the FROM occurred exactly 1x before the replacement and occurs
   exactly 0x after it, and the TO occurs exactly 1x after it. Report all three
   counts, plus the document's count of marker lines and of lines equal to `FROM:`
   or `TO:` — both must be 0. Scope every count to that single path: the RECORD-R23
   text quotes the retired sentence on purpose, so a repository-wide count is
   unmeetable by construction.
6. `.agent/plan.md` byte-equals the PLAN slice; report its sha256, line count
   (under 50), that `## Goal` and `## Next Steps` are present, and its count of
   unchecked-box lines.
7. `git diff --name-only 24bc77c5..HEAD -- packages/ apps/ scripts/ tests/` prints
   NOTHING. Report that it printed nothing.
8. THE MEMBERSHIP GATE, measured by collection and not by prose, and this time
   covering BOTH dependent files. From the repository root, import `CI_STAGES` from
   `packages.orchestration.ci_stages`, and for EVERY stage run
   `python3 -m pytest -m <that stage's marker_expression> --collect-only -q`
   followed by that stage's `test_paths`, reading both out of `CI_STAGES` and
   retyping neither. Report, per stage, how many collected node ids contain
   `test_typescript_compiles` and how many contain `test_apps_ui_probe`.
   `standard` must report 1 and 7; every other stage must report 0 and 0. Then
   confirm, by reading the file, that `tests/runtimes/test_apps_ui_probe.py`
   carries a `pytest.mark.skipif` naming `apps/ui/node_modules/.bin/vite`, and
   quote that reason string. If any reading disagrees, STOP: the document is then
   right and this block is wrong, and that is a finding against the reviewer, not a
   licence to edit the code.
9. `python3 -m pytest tests/docs/ -q` — the docs-round gate. Report the passed
   count and exit code. Take this reading AT C2 and name the commit.
10. Every relative markdown link in `docs/system/ci-self-check-v1.md` resolves on
    disk. Report the list of targets checked and that none was missing.
11. `python3 -m ruff check .` — report the `Found N errors.` line and the exit code.
    Expected 26 errors at exit 1, unchanged. Take this reading AT C3 and name the
    commit; C3 and not C4, because C4 writes the handback that carries the reading.
12. `python3 -m pytest tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q` —
    the verification set and the canary. Report the passed count and exit code.
13. `python3 -m pytest tests/orchestration/test_ci_stages.py
    tests/orchestration/test_ci_stage_selection.py
    tests/orchestration/test_ci_workflow.py -q` — the stage table's guards and the
    hosted-workflow guards. Report the passed count and exit code.
14. The open set, recomputed from `.agent/live_review.md` at HEAD: count every
    `^- R-\d+ — ` paragraph, every `^Done: R-\d+ — ` line and every
    `^Landed: R-\d+ — ` line, report registered, resolved, landed and open, the
    maximum id, the next free id, and that no id repeats and no resolution names an
    unregistered id.
15. The change set: `git diff --name-only 24bc77c5..HEAD` lists exactly
    `.agent/authored/f083-r24.md`, `.agent/handoff.md`, `.agent/last_block.md`,
    `.agent/live_review.md`, `.agent/plan.md` and
    `docs/system/ci-self-check-v1.md`. Report the list and that nothing else is in
    it.
16. Per-commit insertions from `git show --numstat`, reported per commit, none
    exceeding 500; and the history is linear with no amend, rebase or reset.

## Handback

Completion report plus a rewritten `.agent/handoff.md` per
`docs/agents/handback_template.md`: feature and round, branch, the commit table,
the item-status table with every ordered item above appearing exactly once, the
real verification results, the open-findings count, and the next expected action —
which is the integration-gate round per `docs/agents/integration_gate.md`.

Fortschritt: 92 % (F083 beansprucht · R1 bis R7, R9 bis R21 und R23 PASS, R8 und R22 FAIL — R8 auf einem roten ruff-Gate, R22 auf einer falschen Stage-Zuordnung in der neuen Doku, beide in der Folgerunde repariert · T001, T002 und T003 fertig: Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht, die gemessenen Stage-Budgets, die gehostete Workflow-Datei als dünner Wrapper mit ihren Guards, und die Doku samt Laufzeit-Budget-Tabelle · D4 schliesst eine eigene Determinismus-Stage aus, D5 friert die 26 ruff-Fehler ein, D6 macht den lokalen tsc-Compiler tragend · offen sind im Feature selbst nur noch das Integration Gate und die Closure; R-0482 und R-0487 sind bewusst auf einen eigenen Paydown-Branch geroutet, weil Code- und Testinhalte hier tabu sind · gehostete Laufzeit ist weiterhin NICHT gemessen) — Rundenzahl gemessen, Prozentwert geschätzt
