── STEP R21/22 — F082 Self-benchmark — record the R20 verdict, then the integration gate ─

Goal:
  Persist the R20 gate on disk and run the feature's integration gate. R20 was
  REVIEWED and PASSED: the reviewer re-ran every one of the fourteen ordered
  gates against the committed tree and every value reproduced. This round writes
  that verdict into the record, registers the three text defects R20 exposed —
  two the reviewer's own and one the handback's — repairs the stale D10 citation
  R20 declared and could not touch, and then runs the full suite on the branch
  and at the merge base per docs/agents/integration_gate.md. It changes no code
  and no test.

Bundle, in commit order:
  C0a  copy the reviewer's scratchpad original to `.agent/authored/f082-r21.md`
  C0b  mirror it byte-identically into `.agent/last_block.md`
  C1   `.agent/live_review.md` — GATE-R20 + R-0440 + R-0441 + R-0442, appended
       at EOF in ONE commit. Findings persist FIRST
       (planner_reviewer_prompt §4.4), before anything else this round touches.
  C2   `.agent/context.md` — the two rewrite pairs
  C3   `.agent/gate_f082_r21/` — the integration-gate evidence, all new files
  C4   `.agent/plan.md` — the PLAN slice, whole file
  C5   rewrite `.agent/handoff.md`

D11 RULED that R21 is the integration gate. Recording the R20 verdict in this
round's C1 does NOT contradict it: §4.4 binds every round to persist findings
first, and every round on this branch records the PREVIOUS round's verdict. D11
split the R19 verdict out of an integration-gate round that would ALSO have had
to author new capability; C1 here appends text that is already written.

BASE: 98d53826. Re-derive `git rev-parse HEAD` before the first commit and
report whether it equals 98d53826 (R-0428). If it does NOT, stop and hand off.

TRANSPORT (new shape this round, planner_reviewer_prompt §4.9 primary proof):
the reviewer's scratchpad original of THIS block is on disk at
`.remedy-wt/.cache/r21/f082-r21.md`, which `.gitignore` drops (line 235,
`.remedy-wt/`). C0a is a byte COPY of that file — do not retype it, do not
reflow it, do not strip anything. Gate 2 compares all three files as bytes read
in Python, so scratchpad-to-authored identity is PROVEN rather than assumed.

SLICE CONVENTION (R-0437): every FROM and TO body below is the lines between its
markers INCLUDING the trailing newline of its last line, and every shape is
declared UNDER THAT CONVENTION. The block's authored units are, listed: one EOF
append (GATE-R20-BLOCK, carrying the gate and all three findings as one body);
two REWRITE pairs in `.agent/context.md` (CTX-D10, CTXSTEPS-R21), each with FROM
and TO disjoint; and one whole-file replacement (PLAN). No numeral is stated for
that list — the list IS the statement (R-0402, R-0441). The integration-gate
evidence in C3 is MEASURED, never authored, and is not a slice.

Constraints:
  1. Change set: `.agent/authored/f082-r21.md`, `.agent/last_block.md`,
     `.agent/live_review.md`, `.agent/context.md`, `.agent/gate_f082_r21/**`,
     `.agent/plan.md`, `.agent/handoff.md`. Nothing else. `packages/`, `apps/`,
     `scripts/`, `docs/` and `tests/` all stay EMPTY in the range diff — this
     round touches no code and no test, and gate 14 measures that as a
     restriction.
  2. Apply every slice BYTE-VERBATIM, including one you believe is wrong. A
     defect in my text is a declared deviation, never a silent repair.
  3. C1 lands BEFORE C2 and BEFORE the suite runs. If the session dies mid-run,
     the findings must already be on disk.
  4. The base worktree is the ONLY worktree this round adds, it lives under
     `.remedy-wt/`, and it is removed, pruned and its throwaway branch deleted
     before the handback. `git worktree list` is one line at round start and one
     line again at handback.
  5. Create NO pull request. F082's PR is created at closure, now R22.
  6. Raw full-suite logs are written OUTSIDE the tracked tree, under
     `.remedy-wt/.cache/gate_r21/`, and are NEVER committed: a log growing
     inside the tracked tree changes the worktree digest mid-run and turns the
     manifest-identity ids red as false positives (R-0176). No committed
     evidence file carries a `.log` suffix (R-0169). Only the trimmed `*.txt`
     evidence named in C3 is committed, plus a provenance file hashing the raw
     logs.

--- BEGIN SLICE GATE-R20-BLOCK --- (APPEND to .agent/live_review.md, C1, with exactly one blank line between the file's current last line and the first line of this slice)
Gate: R20 — PASS. Verification tier: round gate plus the canary; no full-suite claim is made or implied. The reviewer re-executed all fourteen ordered gates against the committed tree and every value reproduced, none accepted from the handback. TRANSPORT: `.agent/authored/f082-r20.md` and `.agent/last_block.md` are both sha256 33364f1caf2f0101e08b91abd3f7b20f1808045584f7c55d8e751465ae8bda80, 21788 bytes, 219 lines, and the two byte strings are EQUAL; the block declared 219 and measured 219. BASE: the parent of the C0a commit is 418ee8380bfe457f6152f25ca8d372dceeba9e63, which is the ordered base. C1's append is proven as a PREFIX PROPERTY and not by counting: `post.startswith(pre)` is True, `post[len(pre):]` equals one newline plus the GATE-R19-BLOCK body byte-for-byte, the delta is 8316 bytes over an 8315-byte slice, and the file's numstat is `32 0` — the deletion column is 0. C2's two pairs and C3's one pair each measure FROM-in-pre 1, FROM-in-post 0, TO-in-post 1, `FROM in TO` False, and both composites — `pre.replace(F1,T1).replace(F2,T2) == post` and `pre.replace(F,T) == post` — are True; the two FROMs reproduce from the committed `.agent/authored/f082-r19.md` LR-LANDED slice body, sha256 3ce7b462a8db3abcbc15775793903c90a1e7bc7d654e3386a0348b55d88f7469. All eight line-anchored counts hit their ordered values exactly. The OPEN SET recomputed at HEAD is 69 registered, 2 resolved, 67 open, max id R-0439, next free R-0440, 4 `Landed:` lines remaining, no duplicate registered id and no duplicate Done id — the block EXPECTED 69 and 2 and MEASURED 69 and 2. `.agent/plan.md` byte-equals the PLAN slice as a whole file at sha256 982bf7edd2ec7e804c19c56bc188972e14cc260a66bab00a27a8485caac9857f, 41 lines, both required headings present. The contract readers `pytest tests/test_test_runner.py tests/regression/test_resource_safety.py tests/ui_server -q` gave 324 passed, exit 0, and the canary `pytest tests/cli/test_golden_path.py -q` gave 42 passed, exit 0 — both re-run by the reviewer. Gate 11 was the same round's repair of R-0438, so the finding registered there was closed by the block that registered it. Insertions per commit measured 219 · 165 · 32 · 2 · 3 · 17 · 147, none over 500. The change set is six files, all under `.agent/`, and the same range restricted to `packages/`, `apps/`, `scripts/`, `docs/` and `tests/` is EMPTY at 0 files. ONE reported number needed reconciling and is NOT a defect: the handback gives the two C2 FROM lines as 476 and 177 characters where the reviewer measures 478 and 179 BYTES, and the difference is exactly the one em dash each line carries — both readings are true of the same bytes. All THREE deviations the handback declared reproduce exactly as declared, and all three are defects of the reviewer's own text or of the handback's, none of the work; they are registered below. This is the fourth consecutive round in which the WORKER found the reviewer's block defects and declared them before the reviewer read the diff.

- R-0440 — Low, A RESOLUTION THAT QUOTES A FILE'S WORDING WHICH ITS OWN ROUND THEN REWRITES. Found by the WORKER and declared as R20 deviation 1. C2's `Done: R-0436` text asserts that `.agent/plan.md` "now reads ... R-0417 through R-0437". C4 of the SAME round replaced plan.md as a whole file, and the replacement reads R-0417 through R-0439. Measured at HEAD: plan.md contains "R-0417 through R-0437" 0 times and "R-0417 through R-0439" 1 time, while the `Done: R-0436` line contains "R-0417 through R-0437" 1 time. The resolution was stale the moment C4 landed, in the round that wrote it. Low, because the resolution's SUBSTANCE — that the counter-measure list is stated as a RANGE and deliberately without a count — is exactly what plan.md still does, so the finding is genuinely resolved and only its quotation is dead. What makes it worth an id is that no ordering of the commits could have saved it: putting C4 first would have made the quotation true at write time and false at the NEXT plan rewrite instead, because the range's endpoint moves every round by design. The defect is quoting a moving value at all. Standing rule from here, binding the reviewer: a `Done:` text names the PROPERTY a repair established — "stated as a range, without a count" — and never quotes the target file's current sentence, because a resolution outlives every wording it could quote. Where a quotation is genuinely needed, it is pinned to a commit SHA rather than to "now reads".

- R-0441 — Low, A NUMERAL THAT CONTRADICTS THE ENUMERATION IT CLAIMS TO HAVE BEEN COUNTED FROM. Found by the WORKER and declared as R20 deviation 3. The R20 block's slice-convention paragraph says "Two EOF appends (GATE-R19-BLOCK, which carries the gate, both findings and the decision as one body)" — a numeral of two whose own parenthetical enumerates one — and then "Four named units, counted by listing them" over a block the reviewer measures at 6 `--- BEGIN SLICE` markers resolving to 5 logical units: 1 APPEND, 3 REWRITE pairs and 1 WHOLE FILE. Both numerals are wrong, and the second is wrong while explicitly claiming to have been derived by listing. Low, because no gate depended on either numeral and nothing downstream was mismeasured. It is registered because of what it does to R-0402's standing rule: that rule says count the enumeration or state NO numeral, and the phrase "counted by listing them" had been adopted as the rule's own compliance marker — so the marker became the lie. Standing rule from here, binding the reviewer: the phrase "counted by listing them", and every phrase like it, is BANNED. A block states the enumeration and, if it states a numeral at all, that numeral is produced by counting the emitted bytes mechanically in the same pre-emission pass that measures the block's line count — never from the author's recollection of what was written, and never certified by an assertion that counting happened.

- R-0442 — Low, A HANDBACK COUNT WHOSE RANGE WAS NEVER STATED, TRUE UNDER ONE READING AND FALSE UNDER ANOTHER. Found by the REVIEWER while reproducing R20 deviation 2. The R20 handback states "context.md names D10 1x and D11 1x". Measured at HEAD: the bare token `D10` as a word occurs 2 times and `D11` as a word 2 times, while the full citation "DECISION F082 D10" occurs 1 time and "DECISION F082 D11" 1 time. The handback's numbers are true under the full-citation reading and false under the bare-token reading, and the sentence says nowhere which string it counted. The substance holds: the stale citation the deviation reports is real and is repaired by this round's CTX-D10 pair, and the second `D10` occurrence is the historical line "R18 ... rule at D10", which is correct and must NOT be touched. Low for that reason. It is registered because R-0439, written in the very block this handback answers, established that a count is undefined without saying what it ranges over — and the next document produced under that rule broke it. R-0439 bound the reviewer's gates only. Standing rule from here, binding the WORKER's handback as well as the reviewer's gates: every count in a handback states the exact string or pattern counted and the file it was counted in, quoted, so a reader can re-run it. A bare token and its full citation form are two different counts and are never reported as one.
--- END SLICE GATE-R20-BLOCK ---

--- BEGIN SLICE CTX-D10 --- (in .agent/context.md, C2 — REWRITE pair, FROM and TO disjoint)
properties that assert what the rows SAY — and is the round that measures the
Goal's three DONE conditions together (DECISION F082 D10).
--- BEGIN SLICE CTX-D10-TO --- (C2)
properties that assert what the rows SAY — and is the round that first measured
the Goal's three DONE conditions together. R20 recorded that PASS, and the round
map now runs to R21 the integration gate and R22 closure (DECISION F082 D11).
--- END SLICE CTX-D10-TO ---

--- BEGIN SLICE CTXSTEPS-R21 --- (in .agent/context.md, C2 — REWRITE pair, FROM and TO disjoint)
R-0431 to R-0434 ✅ → R19 the acceptance proof for R-0435 ✅ → R20 record the R19
verdict, register R-0438 and R-0439 and rule at D11 → R21 the integration gate
→ R22 closure, per DECISION F082 D11.
--- BEGIN SLICE CTXSTEPS-R21-TO --- (C2)
R-0431 to R-0434 ✅ → R19 the acceptance proof for R-0435 ✅ → R20 record the R19
verdict, register R-0438 and R-0439 and rule at D11 ✅ → R21 the integration
gate → R22 closure, per DECISION F082 D11.
--- END SLICE CTXSTEPS-R21-TO ---

--- BEGIN SLICE PLAN --- (WHOLE FILE replacement of .agent/plan.md, C4)
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0443. Open findings: seventy — the thirty-two carried from F077, plus
R-0403 to R-0442 registered on this branch, less R-0435 and R-0436 resolved at
R20. `.agent/live_review.md` is the source of truth; this file mirrors it.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R21 records the R20 PASS verdict, registers R-0440 to R-0442 — three text
defects, two the reviewer's and one the handback's — repairs the stale D10
citation in `.agent/context.md`, and runs the integration gate per
docs/agents/integration_gate.md: the full suite on the branch and at the merge
base 668d40f7, the comm compare, and per-id attribution for every branch-only
failure. It changes no code and no test.

## Next Steps
1. R22 closure: evidence job, FRESH review zip, the STATUS line, Built State,
   closure candidates, the PR.

## Risks
- The integration gate is the first full-suite run on this branch. A
  reproducible branch-only failure coupled to F082 code is a BLOCKER and its
  repair is its own reviewer-gated round, not a fix inside this one.
- All three DONE conditions are MEASURED by the suite, not argued, but they
  were measured under DOUBLES and never under a live provider; closure says so.
- The delivered order set is three, not the Design's five (R-0411), the freeze
  holds against a file-side edit only (R-0410), and the builder's model stays
  unobservable — closure states all three absences.
- `wall_s` is clock-derived and every row's `cost` is `None` under doubles, so
  pass rate is the only trend a real run can prove.
- Reviewer and handback text defects remain the dominant finding class: the
  standing counter-measures binding every block are R-0417 through R-0442,
  stated as a range and deliberately WITHOUT a count (R-0436).
--- END SLICE PLAN ---

C3 — THE INTEGRATION GATE, docs/agents/integration_gate.md, run in this order:

 a. BRANCH RUN from the repo root. `mkdir -p .remedy-wt/.cache/gate_r21`, then
    `python3 -m pytest -n auto -q` with stdout+stderr redirected to
    `.remedy-wt/.cache/gate_r21/branch_run.txt`. Record the real exit code and
    the wall time. Then
    `grep '^FAILED' .remedy-wt/.cache/gate_r21/branch_run.txt | sort >
    .remedy-wt/.cache/gate_r21/branch_failed.txt`.
 b. BASE RUN at the merge base 668d40f7, which is also main's tip today —
    re-derive `git merge-base main HEAD` and report it. Create the worktree ON A
    THROWAWAY BRANCH, never detached, because the self-dogfood branch guard
    refuses a detached HEAD by design (DECISION D3):
    `git worktree add -b tmp/base-gate .remedy-wt/base-gate 668d40f7`.
    Restore environment parity by COPYING — never symlinking, the UI auto-build
    writes THROUGH a symlink into the primary checkout (F053 R3) —
    `apps/ui/node_modules` and `apps/ui/dist` from the primary checkout into the
    base worktree. Set `REMEDY_UI_NO_AUTO_BUILD=1` for the base run but do NOT
    trust it alone (R-0169): compute a composite digest over the base
    worktree's `apps/ui/dist` BEFORE and AFTER the run and report both. A
    changed digest voids the parity claim and forces per-id attribution instead.
    Same pytest command, log to `.remedy-wt/.cache/gate_r21/base_run.txt`, same
    records, `base_failed.txt` the same way.
 c. COMPARE. `comm -13 base_failed.txt branch_failed.txt` = branch-only
    failures. `comm -23 base_failed.txt branch_failed.txt` = failures present at
    base only. Report BOTH lists in full and both counts.
 d. ATTRIBUTION for EVERY branch-only id: serial re-run of the exact node id.
    serial-pass => xdist-flake class, recorded, not a blocker. serial-fail =>
    reproduce at the merge base before blaming the feature. A reproducible
    branch-only failure coupled to F082 code is a BLOCKER: STOP, write the
    handoff naming the exact ids, and end — the fix is its own gated round.
    EVERY base-only id must also be attributed to the environment class by
    direct evidence naming the missing artifact per id; an unattributed
    base-only id counts as a genuine base failure and blocks the gate verdict.
 e. TEARDOWN. `git worktree remove .remedy-wt/base-gate`, `git worktree prune`,
    `git branch -D tmp/base-gate`. Prove with `git worktree list` (one line) and
    `git branch --list 'tmp/*'` (empty).
 f. COMMIT as C3 exactly these files under `.agent/gate_f082_r21/`, following
    the F077 R16 naming precedent in `.agent/gate_f077_r16/`:
    `branch_run_tail.txt` and `base_run_tail.txt` (each: the command, the SHA,
    the exit code, the wall time, the summary line and the last 40 lines of the
    raw log), `branch_failed.txt`, `base_failed.txt`,
    `comm_branch_only_failures.txt`, `comm_base_only_failures.txt`,
    `attribution.txt`, `dist_hashes.txt` (method + the before and after
    readings), and `full_log_provenance.txt` (for each raw log: path, `wc -l`,
    bytes, sha256, and why it is not committed). If C3's insertions would exceed
    500, split it into C3a (the two run tails and the two failed lists) and C3b
    (the rest) and say so in the handback; do not drop a file to fit.

Done when — run every gate and record its REAL value; a gate you cannot run is
reported as not run, never as green:

 1. `git status --porcelain` EMPTY before the first commit and after the last.
    `.agent/STOP` ABSENT at round start and again at handback (R-0347).
 2. TRANSPORT, bytes read in Python rather than through a shell utility: report
    sha256, byte count and line count of `.remedy-wt/.cache/r21/f082-r21.md`,
    `.agent/authored/f082-r21.md` and `.agent/last_block.md`, and whether all
    three byte strings are EQUAL. Report whether the measured line count equals
    the count this block declares in its footer.
 3. BASE: `git rev-parse HEAD` before the first commit; report it and whether it
    equals 98d53826.
 4. C1 is an APPEND and is proven as a PREFIX PROPERTY, not by counting lines:
    over `<C1>^..<C1>`, report that `pre` is a prefix of `post` and that
    `post[len(pre):]` equals `b"\n" + GATE-R20-BLOCK` byte-for-byte. Report the
    numstat for the file and confirm its deletion column is 0.
 5. C2, both pairs: report for each the FROM count in `pre`, the FROM count in
    `post`, the TO count in `post`, and `FROM in TO`. Then the COMPOSITE: `pre`
    with both replacements applied equals `post`, byte-wise.
 6. Line-anchored counts, each reported with the exact pattern and the file it
    was counted in (R-0442). In `.agent/live_review.md` at HEAD: `^- R-0440 — `
    1x, `^- R-0441 — ` 1x, `^- R-0442 — ` 1x, `^Gate: R20 ` 1x. In
    `.agent/context.md` at HEAD: the literal `DECISION F082 D10` 0x, the literal
    `DECISION F082 D11` 2x, and the whole-word `D10` 1x — that one remaining
    occurrence is the historical "R18 ... rule at D10" line and is CORRECT.
 7. INTEGRATION GATE, branch run: report the exact command, the exit code, the
    wall time, the final summary line verbatim, and the number of `^FAILED`
    lines in `branch_failed.txt`. The target is the whole repository and the
    reviewer measured its collect count at emission as 17007 (R-0438: a gate
    naming a test target states what that target is expected to collect, because
    a path that exists but collects nothing fails silently). Report the count the
    run actually collects; a materially different number is itself a finding, not
    something to reconcile.
 8. INTEGRATION GATE, base run: the merge base you derived, the same four
    values, the number of `^FAILED` lines in `base_failed.txt`, and the
    `apps/ui/dist` digest BEFORE and AFTER with whether they are equal.
 9. COMPARE and ATTRIBUTION: the branch-only count and its full list, the
    base-only count and its full list, and for EVERY id in either list the
    classification and the direct evidence for it. State explicitly whether any
    id is an unattributed base-only failure or a reproducible branch-only
    failure coupled to F082 code — either one blocks the gate verdict.
10. TEARDOWN proof: `git worktree list` output and `git branch --list 'tmp/*'`
    output, both verbatim.
11. `.agent/plan.md` at HEAD byte-equals the PLAN slice as a WHOLE FILE; report
    sha256 and line count (must be under 50), and that `## Goal` and
    `## Next Steps` are both present.
12. OPEN SET recomputed mechanically at HEAD: count `^- R-\d+ — ` paragraphs,
    count `^Done: R-\d+ — ` lines, report both, their difference, the max id,
    the next free id, and the count of remaining `^Landed: ` lines. Report any
    duplicate id. The expected shape after this round is 72 registered and 2
    resolved; report what you MEASURE, and if it differs say so rather than
    reconciling it.
13. CHANGE SET, measured BEFORE C5: `git diff --name-only 98d53826..HEAD`.
    Report the full list and its count. Restricted to `packages/`, `apps/`,
    `scripts/`, `docs/` and `tests/` it must be EMPTY — this round's claim to
    change nothing executable, measured as a restriction rather than asserted.
14. Insertions (`+` column only) per commit — report each; none over 500, with
    the C3 split rule above if needed.
15. STALENESS GATE, standing since R-0417. READ — do not grep — every
    claim-bearing sentence in `.agent/context.md` and `.agent/plan.md` at HEAD.
    Report the number READ, the number that HOLD, and name separately those that
    do NOT hold and those this round's gates never measured. Repair nothing
    outside Constraint 1; report it for R22.
16. `gh pr list --state open --json number,headRefName` — report it. Create NO
    PR.

The canary is SUBSUMED by gate 7: `tests/cli/test_golden_path.py` runs inside
the full branch suite. Say so in the handback rather than running it twice, and
report the golden-path file's own result from the branch run.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
feature and round, branch, per-commit changed-files tables, every gate value
above, the item-status table covering every C-item and every gate, open findings
with max and next free id, and the next expected action. THE NEXT SESSION'S
FIRST ACTION is self_drive_protocol.md Phase 1 rule 1, re-read `.agent/STOP`
from disk, BEFORE rule 2's Open PR Gate. Repeat this line verbatim as the
Fortschritt line:

Fortschritt: ~98 % (T001 ✅ · T002 ✅ · T003a ✅ · T003b ✅ · alle drei DONE-Bedingungen gemessen · R-0435 und R-0436 aufgelöst · R20-Verdikt auf Platte · Integrationsgate läuft · nur noch Closure R22 offen) — Schätzung

If any gate is RED, or anything here contradicts what you find on disk: finish
the commit you are in, write the handoff naming the exact blocker, and end. Do
not widen scope to route around it (G8).

BLOCK SIZE, measured on these final bytes: 280 lines (cap 400, DECISION F105 D5).
──────────────────────────────────────────────────────────────────────────────
