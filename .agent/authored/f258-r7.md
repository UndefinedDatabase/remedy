── STEP INTEGRATION-GATE/3 — F258 Self-use track v2 ────────────────────────
Goal: Book round 6's reviewer verdict into the ledger, then run the
dedicated integration-gate round (planner_reviewer_prompt.md §3 tier 3) —
the full suite runs TWICE, branch and base, before F258 can close.

Bundle:
1. Book `Gate: F258 R6` into `.agent/live_review.md` (round 6's own verdict
   was already written by the reviewer into `.agent/handoff.md` last round;
   this round is the "first commit of the next round" amend0827 rule 1
   names to persist it into the ledger).
2. Run the canonical integration-gate procedure in
   `docs/agents/integration_gate.md` in full — branch run, base run
   (disposable worktree on a throwaway branch at the merge-base, node
   parity restored, compared, both worktree and throwaway branch removed
   after), attribution of any base-only failure, and write the evidence
   files listed below under `.agent/gate_f258_r7/`.
3. All three of F258's T-slices (T001, T002, T003) are already built and
   independently reviewer-verified (rounds 5 and 6). This round adds
   nothing to `packages/`, `apps/` or `tests/` — it only measures and
   records.

Change: exactly these paths, nothing else —
  .agent/authored/f258-r7.md (new)
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/gate_f258_r7/branch_run.txt (new)
  .agent/gate_f258_r7/base_run.txt (new)
  .agent/gate_f258_r7/branch_failed.txt (new)
  .agent/gate_f258_r7/base_failed.txt (new)
  .agent/gate_f258_r7/comparison.txt (new)
  .agent/gate_f258_r7/parity.txt (new)
  .agent/handoff.md

Constraints:
1. If anything below looks wrong, apply it as given and DECLARE the
   problem in the handoff rather than silently fixing it — the reviewer
   corrects it at the next gate. This constraint does NOT excuse a real
   test failure you observe — if either run shows a failure, record it
   exactly as it happened; do not retry until it disappears.
2. `.agent/authored/f258-r7.md` (C0a) is a byte-exact save of THIS ENTIRE
   BLOCK (from `── STEP INTEGRATION-GATE/3` down to the closing line of
   dashes at the very end) — copy it with a plain file write from what you
   were given, not a retype, and mirror it into `.agent/last_block.md`
   (C0b).
3. RECORD7 (below) is copied byte-for-byte with `shutil.copyfile` from the
   scratch original named — never retyped.
4. THE KNOWN PARITY GOTCHA (finding R-0736, OPEN, not yet fixed in
   `docs/agents/integration_gate.md`'s own text): that doc's step 3 tells
   you to COPY `apps/ui/node_modules` and `apps/ui/dist` into the base
   worktree, but `shutil.copytree` PRESERVES source mtimes while
   `git worktree add` stamps every checked-out file with the checkout
   time — so the copied `dist` is byte-correct but mtime-STALE, which
   makes `ui_server._frontend_is_stale()` return True and every
   `tests/ui_server/` test in the base run fails with
   'ERROR: React UI not built.' (roughly 114 ids, all under
   `tests/ui_server/`, on this repository's current test count). FIX IT
   BEFORE the base run, not after discovering the failure class: after
   `shutil.copytree(..., symlinks=True)` on `apps/ui/dist` (symlinks=True
   is also required for `node_modules`, or npm's bin shims get
   dereferenced — finding R-0591), advance every file under the copied
   `apps/ui/dist`'s mtime past the worktree's own checkout time with
   `os.utime(path, (now, now))`, where `now = time.time()`. Record every
   `apps/ui/dist` file's mtime immediately before and immediately after
   the base run itself (not just before/after the copy) and confirm none
   falls inside the run's own wall-clock window — that is what
   `parity.txt` reports, proving the parity claim by the EVENT (nothing
   rewrote `dist` mid-run) and not merely by content-hash equality (which
   cannot distinguish "no rebuild" from "an identical rebuild"). See
   `.agent/gate_f257_r6/parity.txt` and `.agent/gate_f257_r6/comparison.txt`
   for the exact worked precedent this constraint describes (that gate hit
   the staleness class on ITS first base run, fixed it, and reran; you are
   told the fix up front so you do not have to rediscover it).
5. Model every evidence file's SHAPE on the precedent under
   `.agent/gate_f257_r6/` (same six file names, same sections). Do not
   invent a different shape.
6. Every disposable worktree (base run, and any other scratch) is removed
   and its throwaway branch deleted before the round's own gates are
   declared met; `git worktree list` in the primary checkout shows only
   the primary checkout at every commit.
7. Never force-push. Never touch `main`. Push at the end. No pull request
   this round — closure readiness is the reviewer's own decision at the
   next round.

Authored artifacts (all under `.remedy-wt/f258-r7/`, all already on disk in
this checkout — this path is part of THIS SAME checkout, no paste relay
this session):

  PLAN7 — `.remedy-wt/f258-r7/plan7.md`
    sha256 8bff7f63194c5c4d0701f8570f554e6a0d0d4985b3c91a3ac5b055584f0badb1
    1702 bytes, 38 lines, ends with a single `\n`.
    Rewrite `.agent/plan.md` from this file (shutil.copyfile).

  RECORD7 — `.remedy-wt/f258-r7/record7.txt`
    sha256 16228e064c990fa60c3413cf293dfc7379e15983b5870a405e7f98f864bda418
    3909 bytes, one paragraph, ends with a single `\n`.
    Append to `.agent/live_review.md`: read the CURRENT file, confirm it is
    1779093 bytes and ends with exactly one `\n` (not `\n\n`) — if either
    reading differs, STOP and declare it rather than appending — then write
    `base + b"\n" + record7_bytes`.

Done when (every gate below runs for real, exit codes captured, at most
eight gates per amend0827 rule 5):

G1 TRANSPORT. `.agent/authored/f258-r7.md` and `.agent/last_block.md` are
   byte-equal to each other and to the scratch original
   `.remedy-wt/f258-r7/block.md` (sha256, all three).

G2 THE PLAN. Committed `.agent/plan.md` sha256 equals
   8bff7f63194c5c4d0701f8570f554e6a0d0d4985b3c91a3ac5b055584f0badb1, 1702
   bytes, 38 lines, carries `## Goal` and `## Next Steps`, ends with `\n`.

G3 THE RECORD APPEND. Re-measure `.agent/live_review.md` immediately before
   C2 (do not trust the number above if the file has changed): confirm
   `base_bytes + 1 + len(record7_bytes) == committed_bytes`; confirm the
   committed file's last `\n\n`-delimited unit equals RECORD7's own bytes
   (RECORD7 is a single paragraph, so this is the N=1 case); confirm the
   committed file ends with exactly one `\n`. Run a negative control in
   your own disposable worktree: flip one printable byte inside a copy of
   RECORD7 and confirm the reconstruction reading rejects it while
   accepting the true original.

G4 THE LEDGER. Before C2 and after C2, count `^- R-\d+ — ` distinct ids
   (expect 317 both times, ADDED `[]`), `^Done: R-\d+` distinct ids (expect
   55 both times, ADDED `[]`), `DECISION F258 D\d+` distinct ids (expect
   `['D1','D2']` both times, ADDED `[]`), and `^Gate: F258 R\d+` lines
   (expect `['F258 R1',...,'F258 R5']` before, `[...,'F258 R6']` after —
   ADDED exactly `['F258 R6']`).

G5 THE BRANCH RUN, at the primary checkout, HEAD before this round's own
   commits (i.e. at `be848035`). `python3 -m pytest -n auto -q`. REAL exit
   code, full raw tail, wall time, `FAILED` list (expect EMPTY — the
   reviewer's own prior run at this exact commit measured 18677 passed, 20
   skipped, 0 failed, ~126s; your own run is the one that counts, report
   whatever it actually shows).

G6 THE BASE RUN, in a disposable worktree on a throwaway branch at the
   merge-base `18ae71293cde9b1157aca35d3d02c3a8f4265813` (verify with
   `git merge-base HEAD main` first), with constraint 4's parity fix
   applied BEFORE running. `python3 -m pytest -n auto -q`. REAL exit code,
   full raw tail, wall time, `FAILED` list (the reviewer's own prior run
   with the same fix measured 18642 passed, 20 skipped, 0 failed, ~201s;
   report whatever your own run actually shows). Remove the worktree and
   delete the throwaway branch after.

G7 THE COMPARISON. Compute `set(branch_failed) - set(base_failed)`
   (branch-only) and `set(base_failed) - set(branch_failed)` (base-only) IN
   PYTHON (this session's command guard rejects `comm` pipelines by form —
   order the property, not the tool). Attribute every base-only id by
   direct evidence per `docs/agents/integration_gate.md` step 3 (never
   leave one unattributed); attribute every branch-only id with one serial
   re-run per step 4. If both sets are empty, say so plainly and cite the
   two RUN TOTALS lines as the whole proof — no attribution section is
   owed for an empty set.

G8 THE TREE. `git status --porcelain` empty at the end; `git worktree
   list` shows only the primary checkout; no `tmp/*` branch survives
   (`git branch --list 'tmp/*'` empty); every commit's `git diff --numstat`
   insertion total under 500.

Handback: completion report + rewrite `.agent/handoff.md` per
docs/agents/handback_template.md and self_drive_protocol.md's "Ending a
session" section — feature and round (SESSION 2 of F258, round 7), branch,
commit SHAs, the changed-files table, every gate's REAL result (one line
per gate, per checklist item 31, run each at a commit strictly before the
handoff commit), open-findings count (unchanged: 317 registered / 55
resolved / 262 open unless the comparison surfaces a genuine new defect —
if it does, STOP, declare it, and do not proceed to write it up as a
finding yourself; that is the reviewer's own act), the DECISION F258 id
list (unchanged `['D1','D2']`), and next expected action: the reviewer's
own verdict on this round decides whether F258's closure sequence
(docs/roadmap/STATUS_closure_protocol.md) can begin. Push
`feature/f258-self-use-v2` at the end (no force push). No PR is opened
this round.
──────────────────────────────────────────────────────────────
