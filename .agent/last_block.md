── STEP INTEGRATION-GATE/1 — F106 ─────────────────────────────────────────
Goal: Run the dedicated integration gate F106 has never had (STATUS_closure_
protocol.md precondition 2; docs/agents/integration_gate.md steps 1-5): the
full suite, TWICE — once on the branch tip, once in a disposable worktree at
the merge-base — compared and attributed. This is precondition-gathering
work for closure, not closure itself: no STATUS edit, no PR, this round.
Also books round 15's already-produced verdict (RECORD15) into the
permanent record, per amend0827-process-diet rule 1.

Bundle:
  C0a — save this step block verbatim to .agent/authored/f106-r16.md
  C0b — mirror it into .agent/last_block.md
  C1  — rewrite .agent/plan.md for round 16 (PLAN16 below)
  C2  — append RECORD15 (booking round 15's PASS) to .agent/live_review.md,
        ONE paragraph
  C3  — run the branch suite, run the base suite in a disposable worktree
        with the R-0736 parity fix applied proactively, compare, attribute
        every branch-only id, commit the evidence under
        .agent/gate_f106_r16/ (see procedure below)
  C4  — rewrite .agent/handoff.md for round 16 handback

Change: exactly .agent/gate_f106_r16/ (new directory, several files), plus
the four .agent/** paths named in C0a/C0b/C1/C2/C4. No path under packages/,
apps/, tests/, docs/ — this round measures, it does not modify the product.

Constraints:
1. C0a/C0b verbatim single-.agent-state-file saves (shutil.copyfile, never
   cp, never retyped), exempt from the 500-line cap.
2. C1 — PLAN16 is a REWRITE of .agent/plan.md, applied via shutil.copyfile
   from .remedy-wt/f106-r16-plan.md (34 lines, < 50, holds `## Goal`/
   `## Next Steps`, sha256
   7152a746c1c2ccc40fa0710c9859ed1cbef505d7f18630d852cd6593f3d00bb1, 1620
   bytes).
3. C2 — ONE paragraph appended to .agent/live_review.md, never retyped:
   RECORD15 (.remedy-wt/f106-r16-record15.txt, 4688 bytes, sha256
   c2cb7de564024c72ecbfe67435a490a476139323b4390d98aa540ee308f0cc31).
   Re-measure the file's own base length and trailing-newline state before
   appending. At this round's base the file is 1878570 bytes and does NOT
   end in a trailing newline, so the separator is "\n\n". Expected total:
   base + 2 + 4688 = base + 4690 = 1883260 bytes, sha256
   04d9753c642953998cfe6a6ccab77fa6acefab1e9091b6dcf62e8f401965fc8b.
4. C3 procedure — follow docs/agents/integration_gate.md steps 1-4 exactly;
   this constraint states the F106-specific parameters, not a substitute
   for that file.
   a. BRANCH RUN, from the repo root, primary checkout, at the current
      branch tip: `python3 -m pytest -n auto -q`. Record wall time (wrap as
      `bash -c 'time python3 -m pytest -n auto -q > <scratch>/branch_run.txt 2>&1; echo EXIT=$?'`
      or equivalent, run OUTSIDE the repo — write the log to a scratch
      path first, per integration_gate.md step 2's own reasoning applied
      here too: a log growing inside the repo mid-run risks the same class
      of false positive that step 2 documents for the base run). Extract
      `grep '^FAILED' <log> | sort > branch_failed.txt`.
   b. BASE RUN — merge-base is `811c2d7e96b4719b8c76e6fc59ec6d926847a026`
      (re-verify with `git merge-base feature/f106-session-resume main`
      before creating the worktree; do not trust this number blindly).
      Create it ON A THROWAWAY BRANCH:
      `git worktree add -b tmp/base-gate-r16 <scratch-path> 811c2d7e96b4719b8c76e6fc59ec6d926847a026`
      (a detached HEAD fails the self-dogfood branch guard by design —
      DECISION D3, integration_gate.md step 2). Apply the R-0736 parity fix
      PROACTIVELY, before the first base run attempt (F040 R17 / F258 R7
      precedent — do not wait to rediscover the 114-failure signature):
      `shutil.copytree` the primary checkout's `apps/ui/node_modules` and
      `apps/ui/dist` into the worktree with `symlinks=True` EXPLICITLY (a
      default `symlinks=False` dereferences npm's bin shims — finding
      R-0591), THEN `os.utime` every file under the worktree's copied
      `apps/ui/dist/` to a timestamp strictly AFTER the max mtime under the
      worktree's own `apps/ui/src/` (content untouched, sha256 unchanged —
      record both max-mtime readings, before and after the `os.utime`
      call, as the EVENT proof R-0736's fix requires, not merely the
      outcome). Set `REMEDY_UI_NO_AUTO_BUILD=1` for this run (in-process,
      e.g. `os.environ['REMEDY_UI_NO_AUTO_BUILD']='1'` before invoking
      pytest, or `env` if your shell allows it — NOT `VAR=x cmd` form,
      which this sandbox has denied before). Run the IDENTICAL suite
      command with the subprocess's own `cwd` set to the worktree root (no
      path argument to pytest — a path argument run from the primary
      checkout's cwd resolves the wrong installed package for CLI
      subprocess tests, an unrelated artifact F040 R17 hit and diagnosed).
      Record wall time the same way as the branch run; extract
      `branch_failed.txt`'s sibling `base_failed.txt` the same way.
   c. COMPARE: `comm -13 base_failed.txt branch_failed.txt` >
      `branch_only.txt` (failures only on the branch); `comm -23
      base_failed.txt branch_failed.txt` > `base_only.txt` (failures the
      base has that the branch does not — expected empty if the parity fix
      worked; if non-empty, attribute EVERY id to the environment class by
      direct evidence — the R-0736 signature specifically, `React UI not
      built.` in captured output — or count it as a genuine base failure
      per integration_gate.md step 3's unconditional-attribution rule).
   d. ATTRIBUTE every id in `branch_only.txt` (integration_gate.md step 4):
      serial re-run of the exact node id (`pytest <node_id> -q`, no
      `-n auto`). serial-pass ⇒ xdist-flake class, record it, not a
      blocker. serial-fail ⇒ reproduce it at the base (serially, same
      worktree) before concluding it is feature-coupled. A reproducible
      branch-only failure that does NOT reproduce at the base and is
      coupled to F106's own code (packages/orchestration/pingpong_loop.py,
      pingpong_provider.py, diff_repair.py, call_identity.py, or their
      tests) is a BLOCKER: STOP before C4, do not write a handoff claiming
      the gate passed, and report the failure in full instead — that
      becomes the next round's REPAIR target, never something this round
      papers over or a later round silently absorbs.
   e. Write `.agent/gate_f106_r16/attribution.md` — a prose account of the
      comparison result and every attribution made (mirror the shape of
      `.agent/gate_f040_r17/attribution.md`, a real committed precedent in
      this repository's own history at `c94dec74`; read it before writing
      yours). Commit `.agent/gate_f106_r16/{branch_run.txt, base_run.txt,
      branch_failed.txt, base_failed.txt, branch_only.txt, base_only.txt,
      attribution.md}` — the raw logs verbatim, never summarized or
      truncated (a `.txt` extension, never `.log` — `.gitignore` drops
      `*.log` silently and the review-zip guard rejects any `\.log$`
      member, R-0169).
   f. Remove the worktree and its throwaway branch after: `git worktree
      remove <scratch-path>` then `git branch -D tmp/base-gate-r16`; prove
      it with `git worktree list` (primary checkout only) and `git branch
      --list 'tmp/*'` (empty) in your completion report.
5. C3's commit is a SINGLE oversize exception, declared here in advance per
   AGENTS.md's insertion-cap exception clause: the raw pytest output for
   ~18000+ collected tests plus the attribution prose is one indivisible
   measurement (accepted precedent: F040 R17's own `.agent/gate_f040_r17/`
   commit, 596 insertions, `c94dec74`) — state the real insertion count in
   your completion report rather than splitting the evidence dir across
   commits, which would corrupt the record it exists to preserve.
6. C4 — .agent/handoff.md rewrite per AGENTS.md's handoff contract: state,
   SESSION 5, branch, commit SHAs, a changed-files table, this round's real
   G1-G8 results (numbers, never "green"), open-findings count (unchanged —
   no new R-id this round unless a genuine blocker was found in C3.d, in
   which case that finding IS registered here as a new R-id, in ITS OWN
   commit before C4, per §4 item 4's "findings persist FIRST" rule — if
   this happens, name the extra commit and its R-id explicitly in your
   completion report), and next expected action: IF the gate is clean
   (empty branch_only.txt after attribution, or every id classified as
   flake/environment, none feature-coupled), F106's closure precondition 2
   is MET and the next round is the feature file's Built State section
   (precondition 4) plus resolving the feature file's own job/mission-
   resume scope note against Task slicing. IF C3.d found a genuine
   feature-coupled blocker, say so plainly and name it as the next round's
   repair target instead.

Done when (run every command yourself; record REAL exit codes, wall times
and FAILED counts, never the word "green"):
G1 TRANSPORT — .agent/authored/f106-r16.md and .agent/last_block.md both
   sha256-equal to this block as saved (single digest comparison).
G2 THE PLAN — .agent/plan.md sha256
   7152a746c1c2ccc40fa0710c9859ed1cbef505d7f18630d852cd6593f3d00bb1, 34
   lines (`wc -l`), holds `## Goal` and `## Next Steps`.
G3 LIVE_REVIEW APPEND — .agent/live_review.md is 1883260 bytes, sha256
   04d9753c642953998cfe6a6ccab77fa6acefab1e9091b6dcf62e8f401965fc8b; its
   last `\n\n`-delimited unit is byte-equal to RECORD15
   (.remedy-wt/f106-r16-record15.txt); negative control — flip one byte
   inside that last unit in a SCRATCH copy and confirm the flipped copy no
   longer byte-equals RECORD15 (never mutate the tracked file itself).
G4 THE LEDGER — `grep -cE '^- R-[0-9]{4} — '`,
   `grep -cE '^Done: R-[0-9]{4} — '` and
   `grep -cE '^DECISION F[0-9]+ D[0-9]+ — '` over .agent/live_review.md
   read 320, 59 and 20 respectively, IDENTICAL before (base) and after
   (HEAD) this round's C2 — UNLESS C3.d found a genuine feature-coupled
   blocker, in which case the registered count is exactly one higher and
   the new id is named.
G5 THE BRANCH RUN — real exit code, real `passed`/`skipped`/`FAILED`
   counts and real wall time, all read from the committed
   `.agent/gate_f106_r16/branch_run.txt`, not from memory or a summary.
G6 THE BASE RUN — same, from `.agent/gate_f106_r16/base_run.txt`, PLUS the
   mtime-window proof (max `apps/ui/src/` mtime and `apps/ui/dist/`
   mtime, before and after the `os.utime` call) confirmed present in
   `.agent/gate_f106_r16/attribution.md`.
G7 THE COMPARISON AND ATTRIBUTION — `.agent/gate_f106_r16/branch_only.txt`
   and `base_only.txt` both re-derived from `.agent/gate_f106_r16/
   branch_failed.txt` and `base_failed.txt` via `comm -13`/`comm -23`
   yourself (never trust the committed files without recomputing); every
   line of `branch_only.txt` has an explicit classification in
   `attribution.md` (flake / base-reproduces / feature-coupled-blocker);
   zero feature-coupled blockers survive into this round's own verdict —
   if one exists, this gate is RED and the round's own conclusion says so.
G8 THE TREE — `git status --porcelain` empty; `git worktree list` shows
   only the primary checkout; `git branch --list 'tmp/*'` empty; C3's
   insertion count stated and matched against the declared oversize
   exception (constraint 5); every OTHER commit's insertions under 500;
   the canary (`pytest tests/cli/test_golden_path.py -q`) REAL exit 0;
   HEAD pushed and equal to `origin/feature/f106-session-resume`.

Handback: completion report + rewrite .agent/handoff.md (C4 above). State
the real numbers for every gate above, not the word "green". Name every
deviation, however small. If C3 finds no blocker, say so as plainly as you
would report one — a clean gate is not a lesser finding.
─────────────────────────────────────────────────────────────────────────
