── STEP T-GATE/1 — F111 Diff-only repair · Round 21 ──────────────────
Goal:        Prove this branch against the WHOLE repository: full suite on the
             branch, full suite at the merge base, every branch-only failure
             attributed by evidence rather than assumed.
Bundle:      C1a save this block · C1b mirror it · C2 register R-0319 ·
             C3 record the R20 gate, resolve R-0318, fix the R19 tense ·
             C4 the integration gate + its evidence · C5 plan + handoff
Change:      EXACTLY these paths, nothing else:
               .agent/authored/f111-r21-1.md   (new, C1a)
               .agent/last_block.md            (rewrite, C1b)
               .agent/live_review.md           (C2 append, C3 append + 2 pairs)
               .agent/gate_f111_r21/*.txt      (new evidence, C4)
               .agent/plan.md                  (full rewrite, C5)
               .agent/handoff.md               (full rewrite, C5)
             NO source file, NO test, NO doc changes this round.
Constraints:
  - TEXT-A, TEXT-B, TEXT-C and TEXT-D are AUTHORED text. Apply them byte for
    byte. Do not reword, rewrap or re-punctuate. If an authored text looks
    wrong, apply it anyway and report it as a declared deviation.
  - Do NOT write a `Done:` paragraph of your own. For R-0319 you append exactly
    ONE line at column 0 after TEXT-B, in the shape
    `Landed: R-0319 — <one line: what changed, which commit>`.
  - C1 is SPLIT into two commits on purpose: the authored file alone (C1a), then
    `.agent/last_block.md` alone (C1b). Combined they would exceed the
    AGENTS.md 500-insertion cap; split, each is a single-state-file save.
  - G5 isolation: the base suite runs ONLY inside a disposable `git worktree`.
    The primary checkout must satisfy `git status --porcelain` == empty at the
    handback. Scratch and the base worktree live under `.remedy-wt/`, which is
    gitignored (line 235 of .gitignore) — never `/tmp` (writes there are denied
    on this machine) and never an untracked path inside the tracked tree.
  - Evidence files are `.txt`, never `.log`: `.gitignore` drops `*.log` and the
    review-zip guard rejects any `\.log$` member (R-0169).
  - Every suite writes its output to a file under `.remedy-wt/` AS IT RUNS and
    its exit code to a file too, so no number in the evidence exists only in a
    terminal (R-0288). Copy them into `.agent/gate_f111_r21/` only AFTER the run
    has exited (R-0176: a log growing inside the repo mid-run breaks the
    manifest-identity ids).
  - `git worktree add -b tmp/base-gate …` — the base worktree runs on a
    throwaway BRANCH, never a detached HEAD: the self-dogfood guard refuses a
    detached HEAD by design (DECISION D3). Deleting that one throwaway branch at
    cleanup is ordered by docs/agents/integration_gate.md step 2 and is the only
    branch deletion permitted in this round.
Done when: every command has been RUN for real and its TRUE output recorded. A
           guessed, expected or remembered value is a finding. If the gate finds
           a reproducible branch-only failure coupled to feature code, STOP at
           that point, do not attempt a fix, and hand back — the fix is its own
           reviewer-gated round (integration_gate.md step 4).
  a. `cmp .agent/authored/f111-r21-1.md .agent/last_block.md` exits 0; record
     `sha256sum` of both and `wc -lc` of the authored file.
  b. In `.agent/live_review.md` after C3: `grep -c '^Done:'` prints 12,
     `grep -c '^Landed:'` prints 1 (yours for R-0319; R-0318's was replaced),
     `grep -c '^### R20 — PASS'` prints 1, `grep -c '^- R-0'` prints 44.
  c. The R19 gate entry no longer claims the present tense:
     `grep -c 'are byte-identical'` over `.agent/live_review.md` prints 0, and
     `grep -c 'WERE byte-identical'` prints 1.
  d. BRANCH run: `python3 -m pytest -n auto -q`. Record raw tail, exit code,
     wall time, and `grep '^FAILED' | sort > branch_failed.txt`.
  e. BASE run at merge base 4e0b762e in the throwaway worktree, same command,
     with UI parity restored per integration_gate.md step 3 (COPY
     `apps/ui/node_modules` and `apps/ui/dist` — `cp -a`, never a symlink) and
     `REMEDY_UI_NO_AUTO_BUILD=1` set but NOT trusted alone: hash the aggregate
     CONTENT of `apps/ui/dist` in BOTH the base worktree and the primary
     checkout, before and after the base run, and record all four values. A
     changed hash voids the parity claim and forces per-id attribution.
  f. `comm -13 base_failed.txt branch_failed.txt` = branch-only failures;
     `comm -23` = failures the branch FIXED. Report both. Every `comm -23` id
     must be attributed to the environment class by direct evidence or it counts
     as a genuine base failure and blocks the verdict.
  g. Attribution for EVERY branch-only id: serial re-run of the exact node id.
     serial-pass ⇒ xdist-flake class, recorded, not a blocker. serial-fail ⇒
     reproduce at the merge base before blaming the feature. A reproducible
     branch-only failure coupled to F111 code ⇒ BLOCKER, stop and hand back.
  h. COLLECTED-TEST DELTA, measured and not assumed. Run
     `python3 -m pytest --collect-only -q` in both trees, sort the node-id
     lists, and `comm` them. Every branch-only node id must live in an F111
     test file (`tests/orchestration/test_diff_repair*.py`,
     `test_builder_repair_loop.py`, `test_review_scope.py`,
     `test_source_apply_transaction.py`). An added id anywhere else is a finding.
     Record the counts and the file breakdown.
  i. Expected at BASE, per finding R-0286: five failures, every `[reviewer]`
     parametrization in `tests/orchestration/test_role_conventions.py`, because
     `docs/agents/reviewer_conventions.md` estimates 954 tokens against an
     800-token cap. Confirm the count and the ids by reading them out of
     `base_failed.txt` — do NOT assume them. If base shows a different set, say
     so plainly; that is information, not a problem to hide.
  j. Cleanup, with proof: `git worktree remove --force`, `git worktree prune`,
     `git branch -D tmp/base-gate`, then `git worktree list`,
     `git branch --list 'tmp/*'` (expect empty), `git status --porcelain`
     (expect empty), and a test that `.remedy-wt/base-gate` is gone.
  k. `wc -l .agent/plan.md` prints a number BELOW 50 — record the real number.
     Do not pad or trim the authored text to hit any particular count.
  l. `python3 -m pytest tests/cli/test_golden_path.py -q` — the canary.
  m. `git status --porcelain` empty, `git diff --name-only 1e90e89f..HEAD`
     lists only the ordered paths, and
     `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
     prints 0 and 0 after the final push.
Handback:  completion report + rewrite `.agent/handoff.md`. Item-status table
           (C1a, C1b, C2, C3, C4, C5 — each exactly once), commit table with
           real SHAs and insertions, changed-files table, and every result a-m
           as a REAL value. Repeat the Fortschritt line verbatim. Over 60 lines
           ⇒ carry a "Deviations, declared" line naming the count and the
           mandated content that caused it (AGENTS.md DECISION D15).
──────────────────────────────────────────────────────────────────────

PROCEDURE

C1a — `chore(f111): save the R21 step block verbatim`
  Save the block bytes to `.agent/authored/f111-r21-1.md`.
C1b — `chore(f111): mirror the R21 block into last_block`
  Copy that file to `.agent/last_block.md`. Run gate (a).

C2 — `chore(f111): register R-0319`
  Apply the TEXT-A pair to `.agent/live_review.md`. APPEND-shaped: the TO
  contains the two FROM lines verbatim, followed by the new finding bullet.
  This commit exists on its own so the finding survives a dead session
  (docs/agents/planner_reviewer_prompt.md §4.4).

C3 — `chore(f111): record the R20 gate and resolve R-0318`
  Three edits to `.agent/live_review.md`, in this order:
    1. TEXT-B pair — REWRITE: the single `Landed: R-0318 …` line at the end of
       the file is replaced by the authored `Done: R-0318 …` line.
    2. Append the TEXT-B gate entry after it, then your own single
       `Landed: R-0319 — …` line at the very end.
    3. TEXT-C pair — REWRITE inside the `### R19 — PASS` entry: two lines out,
       four lines in. This is the R-0319 fix.
  Run gates (b) and (c).

C4 — `chore(f111): record the F111 integration gate`
  Follow `docs/agents/integration_gate.md` end to end. Write
  `.agent/gate_f111_r21/` with these files, mirroring the F107 R16 gate in
  `.agent/gate_f107_r16/` which is a good worked example of the format:
    branch_run.txt · branch_failed.txt · base_run.txt · base_failed.txt ·
    base_worktree.txt · comm_branch_only_failures.txt ·
    comm_base_only_failures.txt · dist_hashes.txt · collect_delta.txt ·
    attribution.txt · worktree_cleanup.txt
  `attribution.txt` opens with the procedure pointer, the merge base, the branch
  HEAD, the headline numbers for both runs with their real log lines, then the
  collected-test delta, the UI parity proof, and one paragraph per branch-only
  id. Run gates (d) through (j).

C5 — `chore(f111): refresh the plan and write the R21 handoff`
  Replace `.agent/plan.md` with TEXT-D in full. Rewrite `.agent/handoff.md`.
  Run gates (k), (l), (m), then push.

TEXT-A — one APPEND pair for .agent/live_review.md

  FROM (2 lines, occurs exactly once, two leading spaces on each):
  the next round that touches `builder_bridge.py` for another reason; do not
  open a round for it alone. OPEN.
  TO (the same 2 lines, then a blank line, then the new bullet):
  the next round that touches `builder_bridge.py` for another reason; do not
  open a round for it alone. OPEN.

- R-0319 (Low, F111 R20 gate, a dated record written in the present tense): the
  `### R19 — PASS` entry states that `.agent/authored/f111-r19-1.md` and
  `.agent/last_block.md` "are byte-identical". That was true when the value was
  measured, at the start of the R20 session, and false as soon as R20's own C1b
  overwrote `last_block.md` with the R20 block — which the same round then did,
  as every round does. A gate entry records a moment, so its transport sentence
  has to read as one; this one invites a later reader to re-run the `cmp`, find
  a mismatch, and doubt a proof that was sound. The reviewer authored the tense,
  so the fault is the reviewer's and not the R20 worker's, who applied the
  ordered bytes verbatim and flagged the drift in the handback — exactly the
  behaviour this workflow exists to produce. Fix direction: state the past tense
  and say why the file has moved on. OPEN.

TEXT-B — the Done line, then the gate entry

  PAIR (REWRITE): the FROM is the single last line of the file, the TO is one
  line. FROM (1 line):
Landed: R-0318 — the diff-metadata comment in `packages/orchestration/builder_bridge.py` now enumerates all four keys including `full_file_chars`, in commit d81b0b69.
  TO (1 line):
Done: R-0318 — the diff-metadata comment now enumerates all four keys the dict actually returns. Verified at the R20 gate by the reviewer's own reading of the full `git diff ed7eaeef..d81b0b69 -- packages/orchestration/builder_bridge.py`: three comment lines replace two, no identifier, signature or behaviour moved, the stale three-key parenthesis counts 0 and the four-key one counts 1, `ruff check` prints "All checks passed!", and the 14 repair-loop tests are unmoved. RESOLVED.

  Then append, after that line:

### R20 — PASS (2026-08-13)

Reviewed by the main session over ed7eaeef..1e90e89f, seven commits. Every gate
was re-run by the reviewer on this machine; nothing was read off the handback.
Transport: `.agent/authored/f111-r20-1.md` and `.agent/last_block.md` WERE
byte-identical at this gate under `cmp`, 17746 bytes, 329 lines, sha256
9c7497d0e5a849ee2a30de9fc063db37c38b20da45422e1bc14c22db21d43560, with no line
carrying trailing whitespace.

The ist-doc was proved by EXTRACTION, not by retype: slicing the
`<<<BEGIN TEXT-A …>>>` region out of the COMMITTED authored file and comparing
it byte for byte against `docs/system/diff-only-repair-v1.md` prints MATCH. That
doc is 108 lines, carries no trailing whitespace, and is registered twice in
`docs/README.md` — the quick-find row and the system-list row, each in its
alphabetical place.

Scope: exactly the eight ordered paths. The single production commit, d81b0b69,
changes three comment lines and nothing else; the reviewer read that diff in
full rather than its summary. Markers at gate time: eleven resolution
paragraphs, one unreviewed-fix marker, 43 registered findings, one R19 gate
heading. Tests re-run by the reviewer: 350 passed, exit 0 — `tests/docs/` 294,
`test_builder_repair_loop.py` 14 (unmoved from R18), the golden-path canary 42 —
and `ruff check` on the touched module prints "All checks passed!". `git status
--porcelain` empty, one worktree, 0 ahead and 0 behind the remote.

Four deviations were declared and all four are upheld. (1) C1 was split in two
because one commit measured 623 insertions against the AGENTS.md cap of 500. The
worker cited DECISION F105 D5 and applied it; AGENTS.md outranking the block's
"one commit per item" line is the correct reading, and this block orders the
split up front. (2) The block's length gate demanded 44 lines of
`.agent/plan.md` and the authored text was 43. The worker applied the bytes and
reported the true count rather than padding a file to make a reviewer's
arithmetic come out — the right call, the fault is the reviewer's miscount, and
the file was under its 50-line cap throughout. The countermeasure is in this
block: a length gate now asks for the real number under the cap instead of a
number counted by hand. (3) is registered above as R-0319, the reviewer's own
defect. (4) The 100-line handoff carries its DECISION D15 stated-cause line
naming the seven-commit table and the a-l verification block, with no section
dropped.

TEXT-C — one REWRITE pair for .agent/live_review.md (the R-0319 fix)

  FROM (2 lines, occurs exactly once):
`.agent/authored/f111-r19-1.md` and `.agent/last_block.md` are byte-identical
under `cmp`, 11951 bytes, 198 lines, sha256
  TO (4 lines):
`.agent/authored/f111-r19-1.md` and `.agent/last_block.md` WERE byte-identical
at the R19 gate — `last_block.md` carries whichever round's block is newest, so
this sentence records a moment and is not a claim about the file today — under
`cmp`, 11951 bytes, 198 lines, sha256

TEXT-D — the complete new .agent/plan.md

# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: 1e90e89f (R20 PASS).
Next free finding ID: R-0320. Open findings: 32 — 44 registered minus
12 resolved. None is High.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
T001, T002 and T003 are complete and gated, and the ist-doc
`docs/system/diff-only-repair-v1.md` is registered in docs/README.md.
R21 ran the integration gate: the full suite on the branch against the
full suite at the merge base, with every branch-only failure attributed
by evidence in `.agent/gate_f111_r21/`.

## Next Steps
1. Closure per docs/roadmap/STATUS_closure_protocol.md: the evidence
   job, a FRESH review zip (a zip failure is a closure blocker), the
   reviewer-authored STATUS line committed LAST on the branch, then
   the PR — which is NOT merged in that session.
2. Nothing else. Any new work is a new feature and a new branch.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286), so the gate compares base against branch and never reads
  a red branch run as a branch defect on its own.
- The saving is measured in CHARACTERS, not tokens (DECISION F111
  D9). Any doc, STATUS line or PR body calling them tokens turns an
  honest measurement into a fabricated one.
- All-or-nothing rests entirely on source_apply's durable snapshot;
  `apply_diff_repair` adds no rollback of its own, and R-0316's fix
  means a failed rollback is now reported rather than hidden.
- 32 findings stay open at closure, none above Medium, each carried
  as an accepted risk exactly as F107 carried its own.

Fortschritt: ~98 % (T001 ✅ · T002 ✅ · T003 ✅ · Doku ✅ ·
Integration Gate ✅ · Closure offen) — Schätzung
