# F083 R23 — repair: the CI note names the wrong stage for the TypeScript check

SPLIT round: it changes `docs/` and `.agent/` only — no file under `packages/`,
`apps/`, `scripts/` or `tests/` is touched. It records the R22 verdict (FAIL),
resolves R-0485, and registers two Medium findings: R-0486, repaired here, and
R-0487, which is a TEST-CONTENT defect and is therefore registered and routed
rather than fixed — T2_F083's Do-not-touch list puts test contents out of scope,
and this round obeys that list instead of widening to route around it.

Base: `git rev-parse HEAD` MUST print 07d6577a before the first commit. If it does
not, stop and report — every gate below is measured against that base.

## What this round fixes

R22's new ist-doc `docs/system/ci-self-check-v1.md` says the TypeScript compile
check belongs to the `ui` stage. It does not. The reviewer measured this by
collecting every stage's own selection out of `CI_STAGES`:

    test_typescript_compiles  ->  standard: 1 hit, ui: 0 hits,
                                  fast / smoke / budgets / excluded: 0 hits

`tests/ui_server/test_dashboard_contract.py::TestJobSummaryCommandContract::test_typescript_compiles`
is selected by `-m integration` and is NOT selected by `-m ui_contract`, so the
`standard` stage runs it. Further: of the seven files the `ui` selection collects,
NONE mentions `node_modules`, `npx`, `tsc` or `npm `. The `ui` stage does not touch
the node toolchain at all.

The doc states the wrong thing twice — in the stage table's `ui` row and in the
whole D6 section — and it inherited the error from the already-resolved R-0480
prose, which asserted the same membership. THE MARKERS ARE NOT TOUCHED: marker
semantics are on T2_F083's Do-not-touch list, so the document moves to the code,
never the code to the document. Only the three text pairs below change.

While red-controlling the docs gate for this block the reviewer found a second
defect, registered as R-0487 and NOT fixed here: `docs/README.md` is never
link-checked. `TestPrimaryDocLinksResolve` parametrizes on `p.name`, so the repo
root `README.md` and `docs/README.md` share the id `README.md`, and the body's
`next(p for p in PRIMARY_DOCS if p.name == doc)` resolves both to the root file.
Proved by paired control in a disposable worktree: breaking a link in the ROOT
README fails BOTH `[README.md0]` and `[README.md1]`, while breaking one in
`docs/README.md` leaves all 295 green. Fixing it means editing a test's content,
which this feature may not do. All 163 relative links in `docs/README.md` do
currently resolve, checked directly — the hole is latent, not live.

## Slice convention

Every slice is delimited by its own `--- BEGIN SLICE <NAME> ---` and
`--- END SLICE <NAME> ---` markers, which are TRANSPORT ONLY and NEVER reach a
target file. A slice's content begins on the line AFTER its BEGIN marker and ends
on the line BEFORE its END marker, newline included. The slices carried here are
named RECORD-R22, UIROW, STDROW, D6SEC and PLAN. A slice with no FROM: line is an
EOF-APPEND. UIROW, STDROW and D6SEC are FROM/TO pairs and all three are REWRITES —
each TO edits the lines of its FROM rather than containing them (§4.9), so the
proof obligation for each is FROM exactly 0x and TO exactly 1x in the target file
AFTER the edit. Extract every slice programmatically from the COMMITTED
`.agent/authored/f083-r23.md` by its markers — never by retyping.

--- BEGIN SLICE RECORD-R22 --- (EOF-APPEND to .agent/live_review.md, C1)

Gate: R22 — FAIL. Every one of the round's nineteen ordered gates reproduces at the reviewer's own hand, from the repository root at 07d6577a, and every measured value equals the one the handback reports — the round FAILS on a property no gate in its block covered, which is stated first so the record is not read as a transport failure. TRANSPORT, by digest over the committed files (§4.9 digest fallback, this being a self-drive session in which the reviewer holds no scratch copy): `.agent/authored/f083-r22.md` and `.agent/last_block.md` are byte-equal at sha256 35e46857c733612a over 24644 bytes and 288 lines, under the 400-line block cap. C1 is a pure append and was proved so rather than believed: `.agent/live_review.md` goes 275871 B to 282756 B, the former prefixes the latter, the 6885-byte tail byte-EQUALS the RECORD-R21 slice extracted from the committed authored file by its markers, `git show --numstat` is `4 0` so no committed text was edited, and the file's count of transport BEGIN-markers is unchanged at four between base and HEAD, so none leaked. All three FROM/TO pairs are APPEND-SHAPED as declared and were checked that way: each TO contains its FROM verbatim, each FROM occurred exactly 1x in its target before its commit, TEMPLATE's five TO-ONLY lines each occur exactly 1x among the six lines C2 adds, QUICKFIND's and SYSTABLE's one TO-ONLY line each occur exactly 1x among the two lines C4 adds, and no marker line and no FROM:/TO: label reached any target. `.agent/plan.md` byte-equals its PLAN slice at sha256 056a6756b92341b9, 2087 bytes, 37 lines under the 50-line cap, `## Goal` and `## Next Steps` present, 0 unchecked-box lines. The gates all reproduce: the range gate prints nothing for `packages/ apps/ scripts/ tests/`; ruff is `Found 26 errors.` at exit 1 at HEAD, so the ratchet held; `tests/docs/` is 295 passed; the R21 workflow guards are 5 passed; the five CI suites are 46 passed; the verification set with the canary is 78 passed, every one at exit 0; both relative links in the new document resolve; the open set recomputes mechanically to 113 registered, 9 resolved, 0 landed, 104 open, max R-0485, no duplicate id and no unregistered resolution; the change set is exactly the eight paths the handback lists; per-commit insertions are 288, 211, 4, 6, 115, 2, 15 and 79, none near 500; and the history is eight single-parent commits chained to 8336140e with no amend, rebase or reset. The item 9 deviation is correct and is not a finding: a ruff reading cannot be inside the file being written before that text exists (R-0149), and the reviewer's own re-run at the committed C6 returns the same 26 errors at exit 1, which is what the deviation predicted. THE BUDGET TABLE IS RIGHT AND WAS RE-DERIVED RATHER THAN READ: every measured maximum in the document matches both `.agent/f083_inventory.md`'s published samples and `MEASURED_MAX_WALL_S` in `tests/orchestration/test_ci_stages.py` — fast 397.45 from `## Q10`, standard 935.14 from `## Q11`, ui 8.09 and smoke 11.07 from `## Q10`, budgets 1.32 from `## Q12` — all five budgets equal their stage's `timeout_sec` when the numbers are parsed OUT of the document text, the five sum to 3900 s against the workflow's own `timeout-minutes: 90`, the five maxima sum to 1353.07 s, and `ceil(2 * measured_max / 300) * 300` reproduces every one of them. The machine facts hold too: `os.cpu_count()` is 24 and pytest is 9.0.3. WHAT FAILS THE ROUND is a claim about built behaviour that no ordered gate asked about, in the document that IS this round's deliverable, registered below as R-0486: the stage table's `ui` row and the entire D6 section attribute the TypeScript compile check to the `ui` stage, and the code says `standard`. The reviewer measured stage membership by collecting each stage's own selection out of `CI_STAGES` — `standard` selects `test_typescript_compiles`, `ui` does not, and no other stage does either — and further found that of the seven files the `ui` selection collects, not one mentions `node_modules`, `npx`, `tsc` or `npm `, so the D6 section's subject is wrong and not merely its wording. The gate that would have caught it did not exist: the block ordered the stage list "taken from `CI_STAGES`" and gated the budget table against the code, but nothing gated the Why-it-exists column against a collection, so the worker's added clause travelled unchecked. That gate is ordered in the repair round, which is the only durable half of this verdict. ONE REVIEWER IMPRECISION IS RECORDED AND IS NOT A FINDING AGAINST THE WORKER, because it is the reviewer's own text and it cost the round nothing: the R22 block justified landing C3 before C4 with the claim that "`tests/docs/` asserts that every relative link in `docs/README.md` resolves". It does not, and the commit order it produced was harmless and good practice anyway. Red-controlling that claim for the repair block is what surfaced R-0487, registered below: the link guard parametrizes on `p.name`, the repo root `README.md` and `docs/README.md` collide on that id, and both cases resolve to the root file, so the index every new document must be registered in has never been link-checked at all.

Done: R-0485 — resolved as designed, by rule rather than by rewriting R21. C2 of R22 added to `docs/agents/handback_template.md` the requirement that any departure from the block's ordered commit sequence appears in the Deviations section even when the commit table already shows it, and the reviewer verified the pair on disk: the FROM occurred exactly 1x before the commit, all five TO-ONLY lines occur exactly 1x each among the six lines the commit adds, and no marker or label leaked into the file. R22's own handback then applied the new rule to itself in the same round it landed — its Deviations section carries the explicit line "No departure from the ordered commit sequence", naming the eight commits in order — which is the strongest available evidence that the rule is usable and not merely present. R21's commits were correctly left alone.

- R-0486 — Medium, THE NEW CI NOTE ATTRIBUTES THE TYPESCRIPT COMPILE CHECK TO THE `ui` STAGE, AND THE CODE PUTS IT IN `standard`. Measured, not read: collecting each stage's own selection out of `CI_STAGES` puts `tests/ui_server/test_dashboard_contract.py::TestJobSummaryCommandContract::test_typescript_compiles` in `standard` with 1 hit and in `ui` with 0, and `fast`, `smoke`, `budgets` and `excluded` with 0 each; `-m integration` selects the id and `-m ui_contract` does not. `docs/system/ci-self-check-v1.md` states the opposite twice. The stage table's `ui` row reads "Python-verifiable frontend and UI contracts, including the TypeScript check", a clause the worker added beyond the `CiStage.description` the block told it to take the column from. The whole "The UI toolchain is a precondition (DECISION F083 D6)" section then builds on that error: "The UI toolchain is a precondition of the `ui` stage, not a part of it: without that install the stage's TypeScript check skips hosted". The `ui` stage has no such dependency — of the seven files its selection collects, not one mentions `node_modules`, `npx`, `tsc` or `npm `. Medium and deliberately not Low: this is a document in `docs/`, which AGENTS.md defines as the description of what IS, and the misattribution is not cosmetic. It moves the compile out of the stage whose budget is 300 s against an 8.09 s measured maximum and into the one the document itself flags as the stage to watch on a slower hosted runner, so a reader reasoning about hosted timeout risk from this page reasons about the wrong stage and the wrong budget. Not High: nothing executable is wrong, CI behaviour is unaffected, and the hosted install still precedes the whole run, so the compile does get its toolchain. The error was INHERITED rather than invented — R-0480's prose asserted the same membership ("`test_typescript_compiles` carries the `ui_contract` marker, so it is selected by the `ui` stage") and that finding is already resolved, so its text is committed history and is NOT rewritten here; the correction lands where a reader looks for built behaviour, which is the document. The markers are not touched either: marker semantics are on T2_F083's Do-not-touch list, so the fix moves the document to the code and never the code to the document. Fixed at C2 of this round by three FROM/TO pairs, and gated by a collection that reports which stage selects the id rather than by any sentence about it.

- R-0487 — Medium, `docs/README.md` HAS NEVER BEEN LINK-CHECKED, AND THE GUARD THAT IS SUPPOSED TO CHECK IT REPORTS GREEN TWICE FOR THE WRONG FILE. `TestPrimaryDocLinksResolve` in `tests/docs/test_docs_consistency.py` parametrizes over `[p.name for p in PRIMARY_DOCS]`, and `PRIMARY_DOCS` holds both the repository root `README.md` and `docs/README.md`, so two entries share the parametrize id `README.md`. The test body then recovers the path with `next(p for p in PRIMARY_DOCS if p.name == doc)`, and `next` returns the FIRST match for both cases — the root file. The root README is therefore link-checked twice and `docs/README.md` never. Proved by paired control inside a disposable worktree at 07d6577a, not by reading: breaking one relative link in the ROOT `README.md` fails both `test_every_relative_markdown_link_exists[README.md0]` and `[README.md1]` at `2 failed, 293 passed`, while breaking one in `docs/README.md` leaves the suite at `295 passed` with nothing red. The worktree was removed and pruned. Medium and not Low: AGENTS.md makes registering every new or renamed doc in `docs/README.md` mandatory, R22's own C4 did exactly that, and the index carries 163 relative links that nothing verifies — a guard that cannot fail is the "green as a word" class this repository treats as a block condition, and here it announces itself green twice. Not High: measured directly, all 163 of those links resolve today, so the hole is latent rather than live, and no shipped artifact is wrong. NOT FIXED IN THIS FEATURE, deliberately: the repair is an edit to a test's CONTENT, which T2_F083's Do-not-touch list forbids, and `.agent/context.md` already rules that a change needing a test's content edited is a finding and not a fix. It is routed to a paydown branch of its own, alongside R-0482. The obvious repair, for whoever takes it: parametrize on a path relative to the repo root rather than on `p.name`, so the two ids stop colliding, and keep the `next(...)` lookup keyed on that same unique value. OPEN.
--- END SLICE RECORD-R22 ---
--- BEGIN SLICE UIROW --- (FROM/TO pair, REWRITE, docs/system/ci-self-check-v1.md, C2)
FROM:
| `ui` | `ui_contract and not real_ollama` | Python-verifiable frontend and UI contracts, including the TypeScript check. |
TO:
| `ui` | `ui_contract and not real_ollama` | Python-verifiable frontend and UI contracts. No test in this selection shells out to the node toolchain. |
--- END SLICE UIROW ---
--- BEGIN SLICE STDROW --- (FROM/TO pair, REWRITE, docs/system/ci-self-check-v1.md, C2)
FROM:
| `standard` | `(integration or subprocess) and not real_ollama` | Integration and subprocess tests on the fake provider. The determinism suite lives here rather than in a stage of its own (DECISION F083 D4). |
TO:
| `standard` | `(integration or subprocess) and not real_ollama` | Integration and subprocess tests on the fake provider. The determinism suite lives here rather than in a stage of its own (DECISION F083 D4), and so does the TypeScript compile check, which carries the `integration` marker. |
--- END SLICE STDROW ---
--- BEGIN SLICE D6SEC --- (FROM/TO pair, REWRITE, docs/system/ci-self-check-v1.md, C2)
FROM:
## The UI toolchain is a precondition (DECISION F083 D6)

The hosted workflow runs `npm ci --prefix apps/ui` BEFORE `remedy ci run`. The UI
toolchain is a precondition of the `ui` stage, not a part of it: without that
install the stage's TypeScript check skips hosted, exactly as it skips on a local
checkout that never ran it, and F083's Acceptance line would be met by a skip
instead of by a real compile. The install is a workflow step rather than stage
logic so the stage table stays data and keeps naming no toolchain.
TO:
## The UI toolchain is a precondition (DECISION F083 D6)

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
--- END SLICE D6SEC ---
--- BEGIN SLICE PLAN --- (WHOLE FILE, replaces .agent/plan.md, C3)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0488. `.agent/live_review.md` is the source of
truth for the open set; this file repeats no count of it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R22 is closed FAIL and R23 recorded it. R22's commits are all correct and none is
rewritten; what failed was a claim in its new ist-doc that no gate covered — the
TypeScript compile check was attributed to the `ui` stage, and the code puts it in
`standard`. R23 registered that as R-0486 and repaired the document in the same
round, gated by a stage collection rather than by prose. R23 also registered
R-0487 — `docs/README.md` is never link-checked, a test-content defect this
feature may not fix — and routed it out. R-0485 is resolved. T003 stays COMPLETE.

## Next Steps
1. The integration-gate round: the full suite exactly once, per
   docs/agents/integration_gate.md. It is also the round that records R23's
   verdict and resolves R-0486. R-0487 stays open and is not resolved here.
2. Then closure per docs/roadmap/STATUS_closure_protocol.md — evidence job plus a
   FRESH review zip, both mandatory, then the authored STATUS line and the PR.

## Risks
- Hosted wall time is still unmeasured, and the first hosted run is that
  measurement. `standard` needs 935.14 s at its slowest local sample against a
  2100 s budget, and it is also the stage carrying the npm-dependent compile.
- The lint ceiling is a RATCHET. Raising it to make a round green converts the
  one honest lint signal in this repository into decoration.
- R-0482 is a live `NameError` on a guard's refusal path, frozen under that
  ceiling rather than fixed, and belongs to a branch of its own. R-0487, the
  `docs/README.md` link guard that checks the wrong file, belongs to that same
  paydown branch: both are test- or guard-content fixes this feature may not make.
--- END SLICE PLAN ---

## Change — exactly these paths, nothing beyond them

**C0a** saves this block verbatim to `.agent/authored/f083-r23.md`. **C0b** mirrors
the COMMITTED copy over `.agent/last_block.md`.

**C1** applies RECORD-R22 as an EOF-append to `.agent/live_review.md`, the only
file in that commit.

**C2** applies UIROW, STDROW and D6SEC, all three to
`docs/system/ci-self-check-v1.md`, in ONE commit — they are one correction and
splitting them would leave the document self-contradictory between commits. It is
the only file in that commit.

**C3** applies PLAN. **C4** rewrites `.agent/handoff.md`.

The ordered sequence is exactly C0a, C0b, C1, C2, C3, C4 — six commits, no gaps
and no spare numbers. This round changes no file under `docs/roadmap/`, so there
is no feature-file commit to make and none is reserved for one.

## Constraints

1. Never work on `main`; never force-push; never amend, rebase or reset. No PR is
   created and none is merged.
2. `.agent/live_review.md` is APPENDED to once, at C1. No committed text in it is
   edited — in particular R-0480's paragraph, which carries the inherited error, is
   left exactly as it stands: it is resolved history, and R-0486 says so.
3. No marker line and no `FROM:`/`TO:` label reaches a target file. Every slice is
   extracted from the COMMITTED `.agent/authored/f083-r23.md` by its markers.
4. Nothing under `packages/`, `apps/`, `scripts/` or `tests/` is modified at all,
   and NO pytest marker is added, removed or changed anywhere. Gate 7 proves it.
5. The 26 ruff errors are NOT fixed and the lint ceiling is NOT raised.
6. Every disposable worktree is removed and pruned before the handback.
7. If any gate is red, stop at that gate, record its real output verbatim, and hand
   back. Do not widen the change set to route around it.
8. Your handback's Deviations section states explicitly whether the ordered commit
   sequence was followed, per the rule R22 added to
   `docs/agents/handback_template.md`.

## Done when — every command run from /home/decodeux/Repos/remedy, each its own
## unpiped process, each exit code read from that process

1. `pwd` printed FIRST. `git status --porcelain` EMPTY before the first commit and
   before C4. `git worktree list` ONE line at round start and at handback.
   `.agent/STOP` ABSENT at both.
2. `git rev-parse HEAD` at round start EQUALS 07d6577a.
3. `.agent/authored/f083-r23.md` and `.agent/last_block.md` byte-equal; report
   their sha256, byte count and line count.
4. `.agent/live_review.md` at C1: the pre content PREFIXES the post content, the
   tail byte-EQUALS the RECORD-R22 slice as extracted from the committed authored
   file by its markers, and `git show --numstat` has deletion column 0. Also report
   the count of `--- BEGIN SLICE` in the file at base and at HEAD; they must be
   equal, which is the proof no transport marker leaked.
5. UIROW, STDROW and D6SEC pair proofs at C2, separately, each scoped to
   `docs/system/ci-self-check-v1.md` and to that file ALONE: after C2 each FROM
   occurs exactly 0x in that file and each TO exactly 1x. Report all six counts.
   Scope every one of these counts to that single path — the RECORD-R22 text quotes
   the retired sentences on purpose, so a repository-wide count is unmeetable by
   construction.
6. `.agent/plan.md` byte-equals the PLAN slice; report its sha256, line count
   (under 50), that `## Goal` and `## Next Steps` are present, and its count of
   unchecked-box lines.
7. `git diff --name-only 07d6577a..HEAD -- packages/ apps/ scripts/ tests/` prints
   NOTHING. Report that it printed nothing.
8. THE GATE R22 LACKED — stage membership, measured by collection and not by
   prose. From the repository root, import `CI_STAGES` from
   `packages.orchestration.ci_stages`, and for EVERY stage run
   `python3 -m pytest -m <that stage's marker_expression> --collect-only -q`
   followed by that stage's `test_paths`, reading both out of `CI_STAGES` and
   retyping neither. Report, per stage, how many collected node ids contain
   `test_typescript_compiles`. `standard` must report 1 and every other stage must
   report 0. Then, for the `ui` stage only, list the distinct FILES its collection
   yields and report how many of them contain any of `node_modules`, `npx`, `tsc`
   or `npm ` — the answer must be 0 files. If either reading disagrees, STOP: the
   document is then right and this block is wrong, and that is a finding against
   the reviewer, not a licence to edit the code.
9. `python3 -m pytest tests/docs/ -q` — the docs-round gate. Report the passed
   count and exit code. Take this reading AT C2, the commit that changes the
   document, and name the commit you took it at.
10. Every relative markdown link in `docs/system/ci-self-check-v1.md` resolves on
    disk. Report the list of targets checked and that none was missing.
11. `python3 -m ruff check .` — report the `Found N errors.` line and the exit code.
    Expected 26 errors at exit 1, unchanged. Take this reading AT C3 and name the
    commit. C3 and not C4 deliberately: C4 is the commit that writes the handback
    carrying this reading, so a reading "at C4" cannot exist when the text is
    written (R-0149) and R22 had to spend a declared deviation saying so. No commit
    in this round touches a Python file, so C3 is the last commit at which the
    reading is both takeable and current.
12. `python3 -m pytest tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q` —
    the verification set and the canary. Report the passed count and exit code.
13. `python3 -m pytest tests/orchestration/test_ci_stages.py
    tests/orchestration/test_ci_stage_selection.py -q` — the stage table's own
    guards, still green after a round that changed only its documentation. Report
    the passed count and exit code.
14. The open set, recomputed from `.agent/live_review.md` at HEAD: count every
    `^- R-\d+ — ` paragraph, every `^Done: R-\d+ — ` line and every
    `^Landed: R-\d+ — ` line, report registered, resolved, landed and open, the
    maximum id, the next free id, and that no id repeats and no resolution names an
    unregistered id.
15. The change set: `git diff --name-only 07d6577a..HEAD` lists exactly
    `.agent/authored/f083-r23.md`, `.agent/handoff.md`, `.agent/last_block.md`,
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

Fortschritt: 90 % (F083 beansprucht · R1 bis R7, R9 bis R21 PASS, R8 und R22 FAIL — R8 auf einem roten ruff-Gate, R22 auf einer falschen Stage-Zuordnung in der neuen Doku, beide in der Folgerunde repariert · T001, T002 und T003 fertig: Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht, die gemessenen Stage-Budgets, die gehostete Workflow-Datei als dünner Wrapper mit ihren Guards, und die Doku samt Laufzeit-Budget-Tabelle · D4 schliesst eine eigene Determinismus-Stage aus, D5 friert die 26 ruff-Fehler ein, D6 macht den lokalen tsc-Compiler tragend · offen sind im Feature selbst nur noch das Integration Gate und die Closure; R-0487 (docs/README.md wird nie auf tote Links geprüft) ist neu registriert und bewusst auf einen eigenen Paydown-Branch geroutet, weil Testinhalte hier tabu sind · gehostete Laufzeit ist weiterhin NICHT gemessen) — Rundenzahl gemessen, Prozentwert geschätzt
