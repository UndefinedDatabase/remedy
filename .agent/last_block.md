Round f052-r3: persist the R2 gate verdict, register R-0158 + R-0159,
fix R-0158 in docs/agents/integration_gate.md, resolve it. Closure is
NOT part of this round — it follows as its own round. Save this block
to .agent/last_block.md first (OUTCOME: pending → executed at
handback). Verify each authored text's sha256 BEFORE use (wrapped
lines: rejoin with a single space, re-hash; persistent mismatch =
STOP).

STEP 1 — COMMIT A (persist FIRST: verdict + registrations)
Save the five authored texts below to .agent/authored/<name>.md.
In .agent/live_review.md:
- replace the R2 Steps bullet ("- R2: ... In progress.") with the
  BODY of f052-r3-1.md;
- replace the line "- Next free ID: R-0158." with the BODY of
  f052-r3-2.md (registers R-0158 + R-0159, sets next free R-0160);
- append the BODY of f052-r3-3.md to the "## Verdicts" section,
  directly after the R1 PASS entry.
cmp proof per applied region. Commit .agent/live_review.md,
.agent/authored/f052-r3-*.md, .agent/last_block.md as:
chore(f052): persist R2 verdict (integration gate PASS) + register
R-0158/R-0159
Push.

STEP 2 — COMMIT B (R-0158 fix)
In docs/agents/integration_gate.md, replace the ENTIRE paragraph that
runs from the line containing "Environment-coupled base failures
(R-0155 amendment, operator" through the line ending "gate verdict."
(inclusive) with the BODY of f052-r3-4.md. Proofs:
grep -c "path corrected per R-0158" 0→1;
grep -c 'the ROOT `node_modules`, `apps/ui/dist`' 1→0.
Commit:
docs(agents): integration gate — parity path correction + .git-dir
class (R-0158)
Record this commit's short sha as SHA_R0158. Push.

STEP 3 — COMMIT C (resolution)
Substitute <SHA_R0158> in a COPY of f052-r3-5.md (grep -c 1→0; the
original authored file stays untouched). Replace the ENTIRE
"- Open: R-0158 ..." bullet in .agent/live_review.md with the
substituted BODY. cmp proof. Commit:
chore(f052): resolve R-0158 in the ledger
Push.

STEP 4 — GATES + HANDBACK
python3 -m pytest tests/docs/ -q                    (expect 293)
python3 -m pytest tests/cli/test_golden_path.py -q  (expect 42)
Raw tails + exit codes. Rewrite .agent/handoff.md per the template:
range d410ce5..HEAD, per-commit tables, sha256sum output of the five
authored files, cmp proofs, gate transcripts, deviations. Flip
OUTCOME to executed. Commit: chore(f052): handback R3. Push.
No PR yet; never merge. R-0159 stays Open as a documented Low risk.

--- BEGIN f052-r3-1 sha256=6895916ba53c8eea285e38c7abbc33f1147df6357d11e03f4ceeb06c7acf39d5 ---
- R2: persist R1 verdict + DECISION D1 + feature-file amendment +
  Built State + integration gate per docs/agents/integration_gate.md
  (R-0155 amendment in force). Done.
- R3: persist R2 verdict; register R-0158 + R-0159; fix R-0158
  (integration_gate.md path correction); closure stays its own
  round. In progress.
--- END f052-r3-1 ---

--- BEGIN f052-r3-2 sha256=8140e4314ef5c606fe9e5ae557a32337bb6b84e11ffa11f570c623437f3b668f ---
- Open: R-0158 (process, Low, in the reviewer's own text): the
  R-0155 amendment in docs/agents/integration_gate.md names the
  ROOT `node_modules` as a parity target, but that path holds only
  a `.vite` cache (0 packages, 20K); the real dependency tree is
  `apps/ui/node_modules` (205 entries, 305M) — raw base error
  "Cannot find package 'vitest'". The first live gate application
  proved it (pre-parity 10 base failures → 2 after copying the
  right tree). Fix: path correction this round.
- Open: R-0159 (process, Low): the 2 ids in
  tests/cli/test_self_dogfood_execution_cli.py cannot pass in ANY
  linked worktree — self_dogfood_execution.current_branch() reads
  Path(".git")/"HEAD", and a worktree's .git is a regular FILE, so
  the guard answers main_branch_unsafe/blocked. They land in
  comm -23 on every gate run. Fix: read the real HEAD (e.g. via
  git rev-parse) — its own reviewer-gated micro-round; documented
  Low risk until then.
- Next free ID: R-0160.
--- END f052-r3-2 ---

--- BEGIN f052-r3-3 sha256=a48b560a7cac4429738b1114f77506042df829cc1afa307fca4cad21c7d4c8d4 ---
- R2: PASS — INTEGRATION GATE PASS (reviewer, 2026-07-30). Range
  21638c6..d410ce5. All 4 authored texts cmp 0 disk-to-disk; Built
  State verified strictly factual against the r1 diff; amendment
  placed at the end of How it fits. Gate: reviewer's own full run
  at d410ce5 — 14486 passed, 0 failed, 19 skipped, 2:11 — makes the
  branch-only failure set empty by construction; the worker's
  branch run matches (14486/0/19, 2:01). comm -13 = 0. comm -23 =
  2, attributed by direct evidence and REPRODUCED by the reviewer
  (worktree .git is a regular file → dogfood guard unsafe → 2
  failed; primary checkout 6/6 green). Parity per the R-0155
  amendment caught the amendment's own wrong path (ROOT
  node_modules holds only .vite; the real tree is
  apps/ui/node_modules) → R-0158 registered. New suite baseline
  14486/0/19 (+51 = 50 self-healing + 1 count pin). Wall clock
  under budget, no perf pass. LAST_REVIEWED_SHA = d410ce5.
--- END f052-r3-3 ---

--- BEGIN f052-r3-4 sha256=0b4fe00e52a49baa5f770b5730e9cd5315210c74800c3019cc5120f79e3be661 ---
   Environment-coupled base failures (R-0155 amendment, operator
   approved 2026-07-30; path corrected per R-0158): the throwaway
   base worktree lacks artifacts the suite needs — build outputs
   (`apps/ui/node_modules`, `apps/ui/dist`; the ROOT `node_modules`
   holds only a `.vite` cache) and a real `.git` DIRECTORY (a
   linked worktree's `.git` is a file, which the self-dogfood guard
   reads as unsafe — R-0159). Affected ids fail at base and land in
   `comm -23` on every gate run — where a GENUINE base failure in
   those same files would be masked. Therefore: either restore
   parity before the base run (share or copy the primary checkout's
   `apps/ui/node_modules` and `apps/ui/dist` into the base
   worktree, or run the same install/build there), or attribute
   EVERY `comm -23` id to the environment class by direct evidence
   (the missing artifact named per id). Ids whose missing artifact
   CANNOT be restored in a worktree (the `.git`-directory class)
   are attributed with that named cause. An unattributed `comm -23`
   id counts as a genuine base failure and blocks the gate verdict.
--- END f052-r3-4 ---

--- BEGIN f052-r3-5 sha256=04d8fd85e39a33cda1f5de64521eeb7451b906e527f77e197c9c97b3cfdd799e ---
- Resolved: R-0158 (process, Low) 2026-07-30: integration_gate.md
  now names `apps/ui/node_modules` (+ `apps/ui/dist`) as the parity
  targets, notes the ROOT `node_modules` is only a `.vite` cache,
  and folds the non-restorable `.git`-directory class (R-0159) into
  the attribution rule.
  Done: R-0158 (commit <SHA_R0158> — the doc diff is the evidence).
--- END f052-r3-5 ---

OUTCOME: pending
