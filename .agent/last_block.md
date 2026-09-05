STEP INTEGRATION GATE / ROUND 25 - F262 List commands v2 (dates, sort, filter)
FEATURE F262 - List commands v2 (dates, sort, filter) (Tier 2) - SESSION 9, ROUND 25

Goal
  Book round 24's PASS verdict into the ledger (RECORD24) and run the
  INTEGRATION GATE (docs/agents/integration_gate.md steps 1-5) before
  F262's closure: a branch run, a base run at the merge-base with UI
  parity restored in a disposable worktree on a throwaway branch, every
  branch-only failure attributed, every base-only failure attributed,
  evidence saved under .agent/gate_f262_r25/. The worker measures; only
  the reviewer issues the gate verdict at the next round.

Bundle, in this order
  C0a save this block verbatim to .agent/authored/f262-r25.md
  C0b mirror it to .agent/last_block.md
  C1  apply RECORD24 to .agent/live_review.md (append) and PLAN26 to
      .agent/plan.md (whole-file replacement)
  C2  run the integration gate (docs/agents/integration_gate.md steps
      1-5) per constraints 5-12 below; save all nine evidence files
      under .agent/gate_f262_r25/
  C3  rewrite .agent/handoff.md - the handback; then push

Change set - EXACTLY these paths and nothing else
  .agent/authored/f262-r25.md (new, C0a) - .agent/last_block.md (C0b) -
  .agent/live_review.md (C1) - .agent/plan.md (C1) -
  .agent/gate_f262_r25/*.txt (nine new files, C2) - .agent/handoff.md (C3)

Constraints
  1. Every authored slice (RECORD24, PLAN26) is applied BYTE FOR BYTE:
     extract it by its one-line BEGIN/END markers from the COMMITTED
     .agent/authored/f262-r25.md (marker lines EXCLUDED) and write it
     with a Python script, never by retyping. If a slice looks wrong,
     apply it as written and DECLARE it in the handback.
  2. C1 is the first substantive commit of the round.
  3. RECORD24 appends to .agent/live_review.md as EXACTLY TWO newline
     bytes followed by the slice (this branch's convention). PLAN26
     REPLACES .agent/plan.md whole. Neither carries a trailing newline.
  4. Read .agent/STOP from disk before C0a, before C2 and before C3. If
     it exists, finish the commit in hand, write the handback, stop.
  5. C2 executes docs/agents/integration_gate.md steps 1-5 EXACTLY, with
     these round-specific parameters:
       - base commit: confirm with `git merge-base main HEAD` (expected
         7c65d9ccfb512aef1c3eea0245030647332c26ea - PR 235's merge into
         main, matching .agent/plan.md's stated cut point); if the
         measured merge-base differs, STOP and declare the discrepancy
         rather than proceeding on an assumption.
       - base worktree: create ON A THROWAWAY BRANCH, never detached
         (the self-dogfood branch guard refuses a detached HEAD by
         design - DECISION D3, F053 R2):
           git worktree add -b tmp/f262-r25-base .remedy-wt/f262-r25-base <base-sha>
         If naming a path under .remedy-wt/ in a bash command is refused,
         perform the same `git worktree add` through Python
         `subprocess.run([...])` and say so.
       - evidence directory: .agent/gate_f262_r25/, with exactly these
         nine files, `.txt` extension only (never `.log`): gate_summary.txt,
         branch_run_tail.txt, base_run_tail.txt, branch_failed.txt,
         base_failed.txt, branch_only.txt, fixed_by_branch.txt,
         attribution.txt, parity_mtime.txt. Match the SHAPE of the most
         recent precedent, .agent/gate_f114_r11/gate_summary.txt (STEP 1
         through STEP 5, CLEANUP, GATE OUTCOME sections), for
         gate_summary.txt's own structure.
  6. UI PARITY (integration_gate.md step 3, before the base run): copy
     the PRIMARY checkout's apps/ui/node_modules and apps/ui/dist into
     the base worktree with shutil.copytree(..., symlinks=True) (never a
     plain copy, never a whole-directory symlink - copytree's default
     symlinks=False would dereference the npm bin shims, R-0591); set
     REMEDY_UI_NO_AUTO_BUILD=1 for the base run IN-PROCESS (a dict
     passed as env= to subprocess.run - shell env assignment is denied
     here); re-stamp every file under the base worktree's apps/ui/dist to
     the current time after the copy (git worktree add stamps newer than
     copytree preserves - R-0736) and re-measure that
     packages.orchestration.ui_server._frontend_is_stale() reads False
     inside the base worktree (a subprocess with cwd pinned there);
     record every dist file's mtime immediately before and after the base
     run in parity_mtime.txt - PARITY VOIDS if any mtime falls inside the
     run window; a content-hash reading may accompany that but never
     replace it (R-0444).
  7. Run logs are captured OUTSIDE the repo worktree while each suite
     runs (Python subprocess capture, written to a path outside the repo
     tree or under the gitignored .remedy-wt/) and copied into
     .agent/gate_f262_r25/ only after each run exits (R-0176).
  8. Both suite runs are `python3 -m pytest -n auto -q` invoked via
     subprocess.run with cwd pinned to the respective checkout (never
     `cd`). Record raw tail, full FAILED list, exit code, wall time.
     If `comm` is unavailable for piped forms (R-0590), compute
     branch_only.txt and fixed_by_branch.txt as Python set differences
     and state which method was used in gate_summary.txt.
  9. ATTRIBUTION (integration_gate.md step 4), for EVERY id in
     branch_only.txt: a serial re-run of the exact node id with xdist
     disabled (plain `python3 -m pytest <node-id>`, no `-n auto`).
       - serial-pass => XDIST-FLAKE class (F135/F052): record it in
         attribution.txt, not a blocker.
       - serial-fail => reproduce at the base worktree before blaming
         the feature.
       - a reproducible branch-only failure coupled to F262's own
         changed files is a BLOCKER. Check coupling against
         `git diff --name-only <base-sha>..HEAD -- packages/ apps/`
         (the real changed-file list). On a genuine BLOCKER: STOP this
         round right there - do not attempt a repair, do NOT clean up
         the worktree yet if evidence still needs it, write the handback
         naming exactly which id(s), the full evidence, and that a
         separate reviewer-gated repair round is needed before closure.
         Say plainly that it is a STOP handback, not a normal one.
  10. ATTRIBUTION, for every id in fixed_by_branch.txt (base-only
      failures): attribute EVERY one by direct evidence too (the missing
      artifact or the failing assertion named per id) - an unattributed
      base-only id counts as a genuine base failure and is named as such
      in gate_summary.txt, never assumed away.
  11. gate_summary.txt's closing section is MEASURED, not a verdict:
      follow .agent/gate_f114_r11/gate_summary.txt's "GATE OUTCOME
      (measured, not a verdict)" shape - counts and classification, and
      end it stating that the verdict belongs to the reviewer. Do not
      write the word "PASS" as your own conclusion anywhere in this
      round's files.
  12. CLEANUP (only if no BLOCKER halted the round): remove the base
      worktree by its exact path (`git worktree remove --force
      .remedy-wt/f262-r25-base`, via subprocess if the bash form is
      refused), `git worktree prune`, delete the tmp branch (`git branch
      -D tmp/f262-r25-base`) - confirm with `git worktree list` and
      `git branch --list 'tmp/*'` showing neither, before C3. The
      pre-existing `remedy/job-*` worktrees under .remedy-wt/ are NOT
      yours: leave them untouched.
  13. This round does NOT modify anything under packages/, apps/, tests/
      or docs/ - the gate reads and measures, it does not repair.
  14. Self-review loop before every commit. Push after C3
      (`git push -u origin feature/f262-list-commands-v2`). No pull
      request, no merge this round.

Done when - the gates. Run each, record the REAL exit code and the REAL
output.

  G1 TRANSPORT. After C0b: `sha256sum .agent/authored/f262-r25.md
     .agent/last_block.md` - one digest, twice; report both lines.
  G2 THE LEDGER APPEND (RECORD24). Base size of .agent/live_review.md
     immediately BEFORE C1 (expect 2494695, no trailing newline);
     RECORD24's own byte length (expect 4203, zero internal
     newlines); base + 2 + that length (expect 2498900) versus the
     post-C1 length. Second reader: post-C1 bytes from `base` to end
     equal exactly "\n\n" + RECORD24. Negative control in a scratch COPY:
     flip one byte inside RECORD24's text, confirm the reader REJECTS it.
  G3 THE PLAN. .agent/plan.md equals PLAN26 byte for byte (report both
     lengths and the boolean; expect 2015); `wc -l` under 50
     (expect 42, one less than its logical line count);
     `grep -c '^## Goal'` and `grep -c '^## Next Steps'` each 1.
  G4 THE GATE EVIDENCE. `ls .agent/gate_f262_r25/` names exactly the
     nine files constraint 5 lists, nothing else; report each file's
     byte length; print gate_summary.txt in full inside the handback.
  G5 THE CLEANUP AND THE TREE (skip only on constraint 9's BLOCKER path,
     saying so explicitly): `git worktree list` shows no f262-r25-base
     entry; `git branch --list 'tmp/*'` empty; `git status --porcelain`
     empty immediately before C3 is staged; `git ls-files .remedy-wt`
     empty; `.agent/STOP` absent at each of constraint 4's reads.
  G6 THE COMMITS AND THE SWEEP. Per-commit `git show --numstat
     --format=""` for C0a, C0b, C1 (two paths) and C2 (nine paths)
     against this handback's own Commits table, cell for cell; each
     single-parent and under 500 insertions; `git diff --stat
     92cc869b..<C2> -- packages/ apps/ tests/ docs/` empty; the push result.

SLICES. Each lies between its own one-line BEGIN and END marker; the
slice is the bytes between the BEGIN marker's newline and the newline
before the END marker, EXCLUDING that final newline.

<<<BEGIN RECORD24>>>
Gate: R24 — the F262 R24 entry. R24 RECORDED THE OPERATOR'S RULING AND REGISTERED F267, NO CODE BY DESIGN: it booked GATE23 and one reviewer numeral slip, appended DECISION F262 D5 (operator ruling of 2026-09-05, Option B — F262 closes at D4's 24-of-28 scope, the nine remaining wirings plus the catalog-driven handler test and the Acceptance smoke test split into F267, amend0827 rule 6's operator gate discharged for F262) and DECISION F262 D6 (the operator-ordered "non-deterministic packaging" finding examined against both F114 zips on disk and DECLINED — the BLOCKED package was round 17's deliberate red control built from a poisoned copy, not the same evidence), registered F267 with ledger atomicity in ONE commit (`docs/roadmap/features/T2_F267.md` new, the `- [ ] F267` STATUS line at the end of the canonical Tier 2 block after F086, `TOTAL_FEATURES = 267` with its comment, README `71 of 267` and Tier 2 total 20), brought `docs/roadmap/features/T2_F262.md` current (banner, `Blocks/used by: F267`, the D5 amendment, a Built State section — closure precondition 4) and pointed `.agent/context.md`'s Scope at the D4/D5 split — AND THE REVIEWER RE-RAN EVERY GATE ITSELF, independently. VERDICT PASS over the range `6991059c..92cc869b` (C0a `1f99a958`, C0b `7b50bc97`, C1 `7390ae7e`, C2 `be835908`, C3 `ff95b0f4`, C4 `9c5a1af2`, handback `92cc869b`). TRANSPORT HELD IN ITS PRIMARY FORM: the worker obtained the block by `shutil.copyfile` from the reviewer's scratch original, and the reviewer compared that original, the committed `.agent/authored/f262-r24.md` and `.agent/last_block.md` byte for byte — all three equal, sha256 `a2740b98bb2a0cc296b8ccbd67202004c510f77b2bb469eab26916b778eee5e8`, 35837 bytes. THE RECORD APPENDS HELD, reproduced by byte reads of the tracked blobs: `.agent/live_review.md` 2491115 (at `7b50bc97`) plus two newlines plus RECORD23 (3578 bytes) equals 2494695 (at `7390ae7e`), tail equal to the slice; `.agent/prose_slips.md` 73583 plus two newlines plus the slip (965 bytes) equals 74550, tail equal; `.agent/decisions.md` 809282 (at `7390ae7e`) plus one newline plus the D5+D6 slice (8760 bytes) equals 818043 (at `be835908`), tail equal. THE WHOLE FILES HELD: `.agent/plan.md` equals PLAN25 (2039 bytes), `docs/roadmap/features/T2_F267.md` equals F267FILE (4772 bytes), `docs/roadmap/features/T2_F262.md` equals the reviewer's assembled target (6829 bytes: 4232 at `6991059c`, banner pair +84, append 2513). THE PAIRS HELD: every FROM occurred once, every `TO contains FROM` read false as labelled; `git diff 6991059c..9c5a1af2` for `README.md`, `docs/roadmap/STATUS.md`, `tests/docs/test_docs_consistency.py` and `.agent/context.md` was READ in full and shows exactly the six pairs. THE SUITES HELD, reproduced serially by the reviewer at `92cc869b`: `tests/docs/` 295, `tests/orchestration/test_roadmap_index.py` 30, `tests/ui_server/` 515, `tests/orchestration/test_test_runner.py` 52, `tests/regression/test_resource_safety.py` 21, `tests/orchestration/test_integrity_gate.py` 16, `tests/cli/test_golden_path.py` 42 (canary); `ruff check tests/docs/test_docs_consistency.py` "All checks passed!". THE STRUCTURE HELD: every numstat cell matches the handback's Commits table (454/0, 421/105, 3/1 + 28/30 + 3/1, 23/1, 2/2 + 1/0 + 84/0 + 5/2, 3/1 + 40/2), all six pre-handback commits single-parent and under 500 insertions, `packages/` and `apps/` untouched, `tests/` touched only at the pin, `git status --porcelain` empty, `git ls-files .remedy-wt` empty, `.agent/STOP` absent, branch head equal to `origin/feature/f262-list-commands-v2`. NO DEVIATION WAS DECLARED and the reviewer found none (a shell `for` loop and `${PIPESTATUS[0]}` ran unrefused in the worker's sandbox — noted, not a defect). Open findings, canonical line-count formula: 356 registered minus 77 `Done:` lines equals 279 open, unchanged; `.agent/candidates.md` remains EMPTY. Closure preconditions after this round: 4 (Built State) SATISFIED; 1 holds (every round PASS); 2 (integration gate) NOT YET RUN — next round; 3 (`integrity check --json`) and 6 (self-use item) NOT YET RUN; 5 holds (clean, pushed). The next round is the integration gate at merge-base `7c65d9cc`.
<<<END RECORD24>>>

<<<BEGIN PLAN26>>>
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

Round 25, session 9 — the INTEGRATION GATE (docs/agents/integration_gate.md
steps 1-5) before closure: branch run vs. a base run at the merge-base
`7c65d9cc` (PR 235's merge into main), UI parity restored in a
disposable worktree on a throwaway branch, every branch-only and
base-only failure attributed, evidence under `.agent/gate_f262_r25/`.
The worker measures; the reviewer issues the gate verdict next round.

## Next Steps

- If the gate is clean: closure preconditions 3 and 6 (`integrity check
  --json` via the `apps.cli.grouped` module route; the self-use queue is
  exhausted, so `generate_and_append_if_empty`, then run the item to the
  approval gate and register what `describe_self_use_run_defects`
  returns), then closure algorithm steps 1-2 (evidence job
  `f262-closure`, fresh review zip with red control), then the closure
  commit (STATUS `[x]`, README sync, `consumed_by=F262`) and the PR.
- A reproducible branch-only failure coupled to F262 code is a BLOCKER
  and gets its own reviewer-gated repair round before closure.
- Merge under the operator's 2026-09-05 authorization once hosted CI
  reads green (checks read as their own command first).

## Risks

- The gate is where xdist-flake noise (F135/F052 class) surfaces; every
  branch-only id gets a serial re-run and a stated attribution.
- UI parity in the base worktree must be restored exactly (copytree
  symlinks=True, dist re-stamp — R-0591, R-0736) or false base-only
  failures mask real ones.
<<<END PLAN26>>>

Handback: write .agent/handoff.md per docs/agents/handback_template.md
and AGENTS.md - Session line `SESSION 9 of feature F262 · round 25 ·
rounds so far 25` with one sentence of context self-assessment, Range
`Review of 92cc869b..<C2>`, one changed-files table per commit (C0a, C0b,
C1, C2; C3 grouped per the self-reference exception), an item-status
table over C0a..C3 and G1..G6, External actions (worktree add/remove,
the push), raw Verification per gate including the full gate_summary.txt,
Authored-text proofs, Deviations (every re-expression, any departure
from the commit order), and Next: "the reviewer issues the integration
gate verdict; if clean, closure preconditions 3 and 6 follow".
