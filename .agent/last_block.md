# F083 R26 — the integration gate

SPLIT round. It writes down the R25 verdict, then runs the integration gate per
`docs/agents/integration_gate.md`: the full suite once on this branch and once at
the merge base in a throwaway worktree, the two FAILED lists compared, and every
id in either direction attributed by direct evidence. It changes `.agent/` only —
no file under `docs/`, `packages/`, `apps/`, `scripts/` or `tests/` is touched.

Base: `git rev-parse HEAD` MUST print 6a413eb7 before the first commit. If it does
not, stop and report — every gate below is measured against that base. The merge
base is f3fd96d7, which is main's tip.

## Slice convention

Every slice is delimited by its own `--- BEGIN SLICE <NAME> ---` and
`--- END SLICE <NAME> ---` markers, which are TRANSPORT ONLY and NEVER reach a
target file. A slice's content begins on the line AFTER its BEGIN marker and ends
on the line BEFORE its END marker, newline included. The slices carried here are
named RECORD-R25 and PLAN. Neither has a FROM: line: RECORD-R25 is an EOF-APPEND
and PLAN is a whole-file replacement. Extract both programmatically from the
COMMITTED `.agent/authored/f083-r26.md` by their markers — never by retyping.

Shell note, so a guard does not eat a gate: this session rejects `$( )`, `${...}`
and shell loops by form. Route anything of that shape through `python3 - <<'PY'`
and read every exit code from the process object, never from `$?`.

--- BEGIN SLICE RECORD-R25 --- (EOF-APPEND to .agent/live_review.md, C1)

Gate: R25 — PASS. Every one of the round's thirteen ordered gates reproduces at the reviewer's own hand, from the repository root at 6a413eb7, and every measured value equals the one the handback reports. TRANSPORT, by DIGEST FALLBACK and declared as such (§4.9): the R25 block was authored by a previous session, so no reviewer-side original survives to compare against, and the proof actually available is that the committed `.agent/authored/f083-r25.md` and `.agent/last_block.md` are byte-IDENTICAL to each other and that both carry the sha256 the R25 handback had recorded before either file was read this session — 21dbf26eeaec7c0aee97ea5e216c23286c71631f0cddaae88e13ab39847724cd over 14465 bytes and 161 lines, under the 400-line cap. C1 is a pure append and was proved so: `.agent/live_review.md` goes 300239 B to 305119 B, the former prefixes the latter, the 4880-byte tail byte-EQUALS the RECORD-R24 slice extracted from the committed authored file by its markers, `git show --numstat` is `4 0` so no committed text was edited, and the file's count of transport marker LINES is 0 at base and 0 at HEAD while the bare substring count is 4 at both. `.agent/plan.md` byte-EQUALS its PLAN slice at sha256 ff88ab851c0cb6d86430a947ddb5c0c67158e0e9136d5a1636eb4a3611c50751 over 2304 bytes and 39 lines, under the 50-line cap, with `## Goal` and `## Next Steps` present, 0 unchecked-box lines and 0 marker lines. No marker line reached any target file. The remaining gates reproduce: `ONE TEST` occurs 0 times in `docs/system/ci-self-check-v1.md`; the range gate over `docs/ packages/ apps/ scripts/ tests/` prints nothing at exit 0; ruff is `Found 26 errors.` with `[*] 25 fixable` at exit 1, so the ratchet held and the ceiling was not raised; the verification set with the canary is `78 passed in 31.27s` at exit 0; `tests/docs/` is `295 passed in 0.25s` at exit 0; the open set recomputes to 116 registered, 12 resolved, 0 landed and 104 open, max id R-0488 and next free R-0489, with 0 duplicate ids and 0 resolutions naming an unregistered id, R-0488 resolved and R-0482 and R-0487 both still open; the change set is exactly the five `.agent/` paths the handback lists and nothing else; per-commit insertions are 161, 79, 4, 9 and 45, none near 500; and the history is five single-parent commits chained to 94ceafa2, with a reflog showing only `commit:` entries and no amend, rebase or reset. The ordered sequence C0a, C0b, C1, C2, C3 was followed exactly — five commits, none added, none dropped, none reordered. The open set moves 105 to 104 across the round, entirely because the RECORD-R24 text that C1 appended carries a `Done: R-0488` line; R25 registered no finding of its own and resolved none of its own, which is what a persistence round should do. Both declared deviations are honest and neither is a defect. The C0b reading discrepancy reproduces exactly as declared — `git commit`'s rename-detected summary says 161 insertions and 232 deletions while `git show --numstat` gives 79 and 150 — gate 13 uses numstat as the block ordered, both readings sit far under the cap, and that commit is an exempt single `.agent/**` state-file rewrite under the AGENTS.md counting rule in any case. The stated-cause overage is honest under DECISION D15: the handback measures 70 lines against the 60-line cap, the cause named is mandated content — five per-commit tables and a thirteen-row item-status table — and no mandated section was dropped to chase the cap.
--- END SLICE RECORD-R25 ---
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
R25 is closed PASS and R26 recorded it. R26 is the integration-gate round per
docs/agents/integration_gate.md: the full suite once on the branch, once at the
merge base f3fd96d7 in a throwaway worktree, the two FAILED lists compared, and
every id in either direction attributed by direct evidence. Its measured values
live in `.agent/gate_f083_r26/`, not in this file. T001, T002 and T003 are
COMPLETE and every documentation claim in this feature is pinned to a
measurement.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md — the evidence job and a
   FRESH review zip, both mandatory, then the authored STATUS line and the PR.
   The closure run is the second and last full-suite run this feature gets.

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

**C0a** saves this block verbatim to `.agent/authored/f083-r26.md`. **C0b**
mirrors the COMMITTED copy over `.agent/last_block.md`.

**C1** applies RECORD-R25 as an EOF-append to `.agent/live_review.md`, the only
file in that commit.

**C2** adds the gate evidence directory `.agent/gate_f083_r26/`, whose members are
named in gate 12 and nothing else.

**C3** applies PLAN. **C4** rewrites `.agent/handoff.md`.

The ordered sequence is exactly C0a, C0b, C1, C2, C3, C4 — six commits, no gaps
and no spare numbers.

## Constraints

1. Never work on `main`; never force-push; never amend, rebase or reset. No PR is
   created and none is merged. The only branch this round creates is the
   throwaway `tmp/base-gate` of gate 6, and gate 11 deletes it again.
2. `.agent/live_review.md` is APPENDED to once, at C1. No committed text in it is
   edited; write no resolution and no `Landed:` line of your own.
3. No marker line reaches a target file. Both slices are extracted from the
   COMMITTED `.agent/authored/f083-r26.md` by their markers.
4. NOTHING outside `.agent/` is modified. Gate 17 proves it. In particular no
   test, no source file and no configuration is edited to change a suite result —
   if the suite is red, that is the gate's finding, not a thing to fix here.
5. The 26 ruff errors are NOT fixed and the lint ceiling is NOT raised.
6. Every destructive or mutating check runs ONLY inside the disposable base
   worktree. The primary checkout is never mutated, and `git status --porcelain`
   is empty at every point gate 1 names.
7. Raw full-suite logs are written OUTSIDE the tracked tree, under
   `.remedy-wt/.cache/gate_r26/`, and are NEVER committed: a log growing inside
   the tracked tree changes the worktree digest mid-run and turns the
   manifest-identity ids red as false positives (R-0176). Committed gate evidence
   never carries a `.log` suffix (R-0169).
8. Report every exit code and every summary line as MEASURED. This block predicts
   no suite exit code, no pass count and no collected count, and a reported
   "green" that was not read off a process is a finding. The gate's verdict is
   the COMPARISON of the two runs, not the colour of either one.
9. BLOCKER STOP: if gate 10 attributes a reproducible branch-only failure to F083
   code, stop at gate 10, do NOT apply PLAN, do NOT create C3, record the real
   output verbatim and hand back. The repair is its own reviewer-gated round.
10. If any other gate is red, stop at that gate, record its real output verbatim,
    and hand back. Do not widen the change set to route around it.
11. Your handback's Deviations section states explicitly whether the ordered
    commit sequence was followed, per `docs/agents/handback_template.md`.

## Done when — every command run as its own unpiped process, each exit code read
## from that process, the working directory named for every one of them

1. `pwd` printed FIRST. `git status --porcelain` EMPTY before the first commit,
   before the branch run of gate 5, before C2 and before C4. `git worktree list`
   ONE line at round start and at handback. `.agent/STOP` ABSENT at both.
2. `git rev-parse HEAD` at round start EQUALS 6a413eb7, and
   `git merge-base main HEAD` EQUALS f3fd96d7. Report both.
3. `.agent/authored/f083-r26.md` and `.agent/last_block.md` byte-equal as
   COMMITTED blobs; report their sha256, byte count and line count.
4. `.agent/live_review.md` at C1: the pre content PREFIXES the post content, the
   tail byte-EQUALS the RECORD-R25 slice as extracted from the committed authored
   file by its markers, and `git show --numstat` has deletion column 0. Also
   report the file's count of transport BEGIN-marker LINES at base and at HEAD;
   they must be equal.
5. BRANCH RUN, at C1 with a clean tree, from /home/decodeux/Repos/remedy:
   `python3 -m pytest -n auto -q`, output to
   `.remedy-wt/.cache/gate_r26/branch_run.txt`. Report the commit SHA it ran at,
   the exact final summary line, the exit code and the wall seconds.
6. BASE WORKTREE, created after gate 5 has finished.
   `git worktree add -b tmp/base-gate .remedy-wt/base-gate f3fd96d7` — on a
   BRANCH, never a detached HEAD, because the self-dogfood guard refuses
   detachment by design (DECISION D3). Then restore parity: place the primary
   checkout's `apps/ui/node_modules` and `apps/ui/dist` into that worktree by
   COPY, never by symlink — report the count of symbolic links directly at each
   of those two paths, which must be 0. Then restore FRESHNESS: make every file
   under the copied `apps/ui/dist` newer than every file under that worktree's
   `apps/ui/src`, and report the newest mtime found under each of the two
   directories and that dist's is the later. This is not decoration: at F082 R21
   a content-correct but STALE copied `dist` made the UI server refuse to start
   and cost that gate eight base-only failures needing per-id attribution.
7. `apps/ui/dist` digest, BEFORE and AFTER the base run: a composite sha256 over
   the sorted `<relpath> <sha256-of-file>` lines of every file under the base
   worktree's `apps/ui/dist`. Report both digests, the file count, and whether
   they are equal. `REMEDY_UI_NO_AUTO_BUILD=1` is set for the base run but is NOT
   trusted on its own — a spawned build path has ignored it before (R-0169). A
   changed digest does not fail the round; it VOIDS the parity claim and forces
   per-id attribution under gate 10.
8. BASE RUN, from `.remedy-wt/base-gate`, with `REMEDY_UI_NO_AUTO_BUILD=1` set:
   `python3 -m pytest -n auto -q`, output to
   `.remedy-wt/.cache/gate_r26/base_run.txt`. Report the commit SHA it ran at,
   the exact final summary line, the exit code and the wall seconds.
9. COMPARE. Build `branch_failed.txt` and `base_failed.txt` as the sorted
   `^FAILED` lines of the respective raw logs. Then
   `comm -13 base_failed.txt branch_failed.txt` is the branch-only set and
   `comm -23 base_failed.txt branch_failed.txt` is the base-only set. Report BOTH
   lists in full and the count of each. An empty list is reported as empty, with
   its byte count.
10. ATTRIBUTION, for EVERY id in EITHER list, per
    `docs/agents/integration_gate.md` step 4. A branch-only id is re-run serially
    by its exact node id: serial-pass is the xdist-flake class, recorded and not a
    blocker; serial-fail is reproduced at the base worktree before the feature is
    blamed; a reproducible branch-only failure coupled to F083 code is a BLOCKER
    and constraint 9 applies. A base-only id is attributed to the environment
    class by naming the MISSING ARTIFACT for that id with direct evidence from
    the base run's own log and the base worktree's own code. An id left
    unattributed blocks the verdict. If both lists are empty, say so explicitly
    and say that nothing needs attributing. If more than ten branch-only ids land
    in the flake class, say so in the handback in those words — the reviewer owes
    the operator a flake-debt line when that happens.
11. WORKTREE REMOVAL, before C2. Remove the base worktree, prune, and delete the
    `tmp/base-gate` branch. Report that `git worktree list` prints ONE line and
    that `git branch --list tmp/base-gate` prints nothing.
12. EVIDENCE at C2. `.agent/gate_f083_r26/` contains exactly
    `branch_run_tail.txt`, `base_run_tail.txt`, `branch_failed.txt`,
    `base_failed.txt`, `comm_branch_only_failures.txt`,
    `comm_base_only_failures.txt`, `attribution.txt`, `dist_hashes.txt` and
    `full_log_provenance.txt`. Report the directory listing, that every member
    ends in `.txt`, and that `git ls-files` matching `\.log$` over the whole
    repository returns nothing. `full_log_provenance.txt` carries, for each raw
    log left in `.remedy-wt/`, its path, line count, byte count and sha256 — the
    raw logs themselves are not committed.
13. `python3 -m pytest tests/cli/test_golden_path.py -q` — the canary, run from
    the repository root at HEAD. Report the passed count and the exit code.
14. `python3 -m ruff check .` — report the `Found N errors.` line and the exit
    code. Take this reading AT C3 and name the commit; C3 and not C4, because C4
    writes the handback that carries the reading.
15. The open set, recomputed from `.agent/live_review.md` at HEAD: count every
    `^- R-\d+ — ` paragraph, every `^Done: R-\d+ — ` line and every
    `^Landed: R-\d+ — ` line; report registered, resolved, landed and open, the
    maximum id, the next free id, and that no id repeats and no resolution names
    an unregistered id.
16. `.agent/plan.md` byte-equals the PLAN slice; report its sha256, line count
    (under 50), that `## Goal` and `## Next Steps` are present, and its count of
    unchecked-box lines.
17. `git diff --name-only 6a413eb7..HEAD -- docs/ packages/ apps/ scripts/ tests/`
    prints NOTHING. Report that it printed nothing.
18. The change set: `git diff --name-only 6a413eb7..HEAD` lists exactly
    `.agent/authored/f083-r26.md`, `.agent/handoff.md`, `.agent/last_block.md`,
    `.agent/live_review.md`, `.agent/plan.md` and the members of
    `.agent/gate_f083_r26/`. Report the list and that nothing else is in it.
19. Per-commit insertions from `git show --numstat`, reported per commit, none
    exceeding 500; and the history is linear with no amend, rebase or reset.

## Handback

Completion report plus a rewritten `.agent/handoff.md` per
`docs/agents/handback_template.md`: feature and round, branch, the commit table,
the item-status table with every ordered item above appearing exactly once, the
real verification results, the open-findings count, and the next expected action.
The handoff's Next section names, in order: read `.agent/STOP` from disk, run the
AGENTS.md Open PR Gate, then the closure round per
`docs/roadmap/STATUS_closure_protocol.md`.

Fortschritt: 95 % (F083 beansprucht · R1 bis R7, R9 bis R21, R23 bis R25 PASS, R8 und R22 FAIL — beide in der Folgerunde repariert · T001, T002 und T003 fertig: Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht, die gemessenen Stage-Budgets, die gehostete Workflow-Datei als dünner Wrapper mit ihren Guards, und die Doku samt Laufzeit-Budget-Tabelle, deren Aussagen alle gegen eine Collection gemessen sind · D4 schliesst eine eigene Determinismus-Stage aus, D5 friert die 26 ruff-Fehler ein, D6 macht den lokalen tsc-Compiler tragend · diese Runde ist das Integration Gate, danach bleibt nur die Closure; R-0482 und R-0487 sind bewusst auf einen eigenen Paydown-Branch geroutet · gehostete Laufzeit ist weiterhin NICHT gemessen) — Rundenzahl gemessen, Prozentwert geschätzt
