STEP T001-T004 closure part one — F276 Data-root hygiene & disk budget, ROUND 7

This block contains no horizontal rule and no run of a repeated character, so
nothing in its frame has a length a reader must recover by eye (item 37).

Goal
Book round 6's verdict, register and repair R-1006, write the feature file's
Built State paragraph, and run this feature's ONE full suite — the integration
gate of operator amendment amend0917-throughput rule 1 — committing its
transcript. This is the first half of the closure sequence; the second half
(integrity check, self-use item, evidence job, review package, ledger rotation,
finding re-assignment, checklist consolidation, STATUS flip, pull request) is
round 8 and is NOT started here.

Bundle, in commit order
C1 the bookkeeping, in ONE commit (amend0917 rule 4): the four payload copies
   under `.agent/authored/`, the ledger append, the decisions append, the plan
   rewrite.
C2 the R-1006 repair: the `remedy job budget` limits listing gains the disk
   floor, with its guard; plus the one `Landed:` line.
C3 the feature file's Built State paragraph.
C4 the integration gate's transcript.
C5 the handoff.

Payloads on disk
Every authored text of this round is a FILE the worker reads from disk. Nothing
is retyped. Each is named with its byte count, its line count and its sha256;
the worker verifies the digest BEFORE using the file and reports both readings.

P1 `.remedy-wt/f276-r7/block.md` — this block.
   lines 240; the digest is in the delegation message that names this file.
P2 `.remedy-wt/f276-r7/ledger.md`
   lines 4; sha256 d3fa155ba5d3fc26ea1f51c87f20266d3cf81ec3a1f4caeedc998f1d64e925a4
P3 `.remedy-wt/f276-r7/decisions.md`
   lines 49; sha256 f14f0e7cf3914e01d995cc9b39ae80acaa2d176b134da7bb8cb28516a699e051
P4 `.remedy-wt/f276-r7/plan.md`
   lines 42; sha256 c0372c7a3d9428282ddb88af8174ba7ca23f3bdac5f7f1462cde1c71bf4afecc
P5 `.remedy-wt/f276-r7/f276-r7.diff`
   lines 172; sha256 6631ca57984917ed22a73934bc9402fbafdd9a51b50e3125e565f85bce4b26e5

P2, P3 and P4 are prose slices. P2 and P3 are APPEND-shaped: each begins with a
newline and is concatenated onto the end of its target, whose current bytes end
with a newline, so the result is the target's bytes followed by the payload's
bytes and nothing else. P4 is a REWRITE: `.agent/plan.md` becomes exactly P4's
bytes. Containment test, run mechanically before emission, one reading per pair:
`.agent/live_review.md` contains P2 — false; `.agent/decisions.md` contains P3 —
false; `.agent/plan.md` contains P4 — false. All three are therefore NEW bytes
and no FROM-count proof is owed on any of them.

P5 is the CODE and DOCS slice, a unified diff against `b9e55410` produced by the
reviewer's own dry run and applied with `git apply`, never retyped. It is applied
in TWO disjoint slices, each its own commit:
  C2 `git apply --include=apps/cli/commands/job.py
      --include=tests/orchestration/test_job_budgets.py .remedy-wt/f276-r7/f276-r7.diff`
  C3 `git apply --include=docs/roadmap/features/T2_F276.md .remedy-wt/f276-r7/f276-r7.diff`
Run `git apply --check` with the same arguments before each. `git apply --stat`
of the whole file reads three files; the two slices partition those three paths
and neither touches a path the other does.

Change set — exactly these paths, and nothing else this round
  .agent/authored/f276-r7-block.md        (new, C1)
  .agent/authored/f276-r7-ledger.md       (new, C1)
  .agent/authored/f276-r7-decisions.md    (new, C1)
  .agent/authored/f276-r7-plan.md         (new, C1)
  .agent/live_review.md                   (C1 append, C2 one Landed line)
  .agent/decisions.md                     (C1 append)
  .agent/plan.md                          (C1 rewrite)
  apps/cli/commands/job.py                (C2, from P5)
  tests/orchestration/test_job_budgets.py (C2, from P5)
  docs/roadmap/features/T2_F276.md        (C3, from P5)
  .agent/authored/f276-closure-suite.txt  (new, C4)
  .agent/handoff.md                       (C5)

C1 — the bookkeeping
Copy P1 to `.agent/authored/f276-r7-block.md`, P2 to `-ledger.md`, P3 to
`-decisions.md`, P4 to `-plan.md`, each with `shutil.copyfile`, never by
retyping. Append P2's bytes to `.agent/live_review.md`; append P3's bytes to
`.agent/decisions.md`; write P4's bytes over `.agent/plan.md`. Commit.

What P2 books: round 6's verdict, PASS, re-derived by this session's reviewer
over `caa9d073`..`b9e55410`, and the registration of R-1006. What P3 appends:
DECISION F276 D8, which rules where the disk floor is listed in the budget
rendering and that its guard is written over the model rather than over the one
missing name. What P4 rewrites: the plan, to this round.

C2 — the R-1006 repair
Apply P5's C2 slice. It adds to `apps/cli/commands/job.py::_cmd_job_budget`, in
the labelled-limits block and directly after the `deadline` branch, an
`if _budgets.min_free_disk_bytes is not None` line printing
`min_free_disk_bytes`, with the comment stating why it is listed last; and to
`tests/orchestration/test_job_budgets.py`, appended at the end, the class
`TestEveryConfiguredLimitIsNamedInTheTextOutput` with two nodes — one
configuring every field of `JobBudgets` and asserting every field NAME appears
in the text output, one pinning the floor's own printed value.

In the SAME commit, append one line to the end of `.agent/live_review.md`,
separated from the text above it by one blank line, reading exactly:

Landed: R-1006 — the `remedy job budget` limits listing now names `min_free_disk_bytes`, guarded over `JobBudgets.model_fields`; landed at this round's C2.

Write no other line about R-1006 and no `Done:` paragraph anywhere: only
reviewer-authored text sets a finding Resolved, and the resolution of R-1006 is
booked by round 8's own first commit. A worker-authored `Done:` paragraph is
itself a finding, however honestly it is hedged.

C3 — the Built State
Apply P5's C3 slice. It appends a `## Built State (F276, 2026-09-20)` section to
`docs/roadmap/features/T2_F276.md`, naming what each of T001 to T004 built, the
three lines this feature adds to
`tests/orchestration/import_reachability_allowlist.txt` (closure precondition 7),
and the findings this feature raised and what became of each. Nothing above that
section is touched. Commit. This commit MUST follow C2, because the Built State
says R-1006 was repaired in this round and that sentence is true only once C2
exists — this is the ordering constraint the R-1006 registration in P2 names.

C4 — the integration gate
This is the ONE full suite run of feature F276 (operator amendment
amend0917-throughput, 2026-09-17, rule 1). Run it ONCE, in the PRIMARY checkout,
never a worktree, after C3 and before the handback:

  python3 -m pytest -n auto -q

Write the transcript to `.agent/authored/f276-closure-suite.txt`: the exit code,
the pytest summary line verbatim, the wall-clock duration, and the FULL list of
bad node ids — every failure and every error, one per line, never truncated. If
the run is fully green, write the summary line and the words
`BAD NODE IDS: none` under its own heading, so the file states a measured set
either way. Commit that file alone.

Do NOT repair anything in this round if the suite is red. Record it, commit the
transcript, and say so in the handback; the repair rounds and their shrinking
rule are amend0917 rule 2's and belong to the next round, which the reviewer
authors after reading the transcript.

C5 — the handoff
Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`: the SESSION
NUMBER (this is SESSION 2 of F276), the round, the branch, the per-commit tables
with `git show --numstat` insertion counts for C1 to C4, every gate below with
its real output and exit code, the open-findings count by both readings, the
item-status table, the deviations, and the next expected action. It carries one
sentence of context self-assessment. It has no length cap. Its own insertion
count belongs in the handback's own text, not in any gate.

Constraints
1. Apply every payload byte for byte. A payload that looks wrong is REPORTED in
   the handback as a deviation and applied anyway; it is never edited, and no
   slice of it is retyped.
2. Touch no path outside the change set above. In particular: do not edit
   `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` or
   `.agent/candidates.md` — those belong to round 8's closure commit.
3. The commit sequence is C1, C2, C3, C4, C5, in that order, with no extra
   commit, none dropped and none reordered. Report any deviation.
4. Every commit's insertion count, by `git show --numstat`, stays under 500.
   Report each of C1 to C4's count; C5's own count belongs in its own text.
5. Destructive verification — G5 — runs ONLY inside a disposable git worktree
   under `.remedy-wt/`, never in the primary checkout, which satisfies
   `git status --porcelain` empty at the handback. Remove that worktree as G5's
   last action and report `git worktree list` afterwards.
6. Never force-push, never rewrite history, never delete a branch, never merge,
   never open or edit a pull request, never run any `gh` command. Work only on
   `feature/f276-data-root-hygiene`.
7. Read `.agent/STOP` from disk before the first commit. If it exists, write the
   handoff and end, doing nothing else.
8. No test may call a real model provider, and nothing may read or write the
   operator's `.data` directory. The full suite of C4 is the repository's own
   suite, unchanged, and is the only long-running command this round orders.

Done when — six gates, each executed, each reporting its REAL output and exit
code. "Green" as a word is a finding.

G1 TRANSPORT AND STATE, at C1. One python check printing an explicit True or
   False per reading, and the readings are: each of the four
   `.agent/authored/f276-r7-*` files equals its payload on disk, byte for byte;
   `.agent/live_review.md` at C1 equals its `b9e55410` bytes plus P2's bytes;
   `.agent/decisions.md` at C1 equals its `b9e55410` bytes plus P3's bytes;
   `.agent/plan.md` at C1 equals P4's bytes. Report the number of readings and
   that every one is True. SEPARATELY, and in the same gate, report the SAVED
   BLOCK's own line count and sha256 beside the line count and digest the
   delegation message gave for P1, as two readings side by side (R-0954).

G2 CODE AND DOCS TRANSPORT, at C3. `git rev-parse` the three blobs and report
   them; each must read EXACTLY:
     apps/cli/commands/job.py
       d3c2f9e24e5be1f9615099056330ecc29884a669
     tests/orchestration/test_job_budgets.py
       5f1e6e06ed1015895904079b3628f90fd46f8708
     docs/roadmap/features/T2_F276.md
       ec3ebeba3b9dbd8e13ce8ae99fb07a2143792388
   These are the objects of the reviewer's own dry run, so equality proves the
   committed files are byte-identical to the tree the reviewer tested and
   red-proved before authoring. Also report `git diff --name-only <C1> <C3>`:
   it must name exactly those three paths and no other, and report its length.

G3 THE TARGETED SUITE, after C3, in the primary checkout, serial, no `-n`:

  python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_job_budgets.py tests/orchestration/test_predictive_budget.py tests/orchestration/test_f018_authority_integration.py tests/orchestration/test_disk_floor.py tests/docs tests/cli/test_golden_path.py

   Report the summary line and the exit code. Expect 0 failed and exit 0. This
   is the round gate and the docs gate and the canary in one command: the three
   files nearest the production module C2 edits, the file T004 shipped, the docs
   suite that `docs/roadmap/**` obliges, and the golden path.

G4 RUFF, after C3:

  python3 -m ruff check apps/cli/commands/job.py tests/orchestration/test_job_budgets.py

   Report the output and the exit code. Expect `All checks passed!` and exit 0.

G5 THE R-1006 RED PROOF, in ONE disposable worktree under `.remedy-wt/` created
   detached at C3 and removed as this gate's last action. Print the resolved
   path of the imported `apps.cli.commands.job` first, to prove it resolves
   inside the worktree and not through an editable install. Purge `__pycache__`
   and run with `python3 -B`. Run, from the worktree root:

  python3 -B -m pytest -q --no-header -rf -p no:cacheprovider tests/orchestration/test_job_budgets.py::TestEveryConfiguredLimitIsNamedInTheTextOutput

   FIRST the UNMUTATED control; report its exit code and summary. THEN count, in
   `apps/cli/commands/job.py` in that worktree, the occurrences of the exact two
   lines C2 added — the `if _budgets.min_free_disk_bytes is not None:` line and
   the `print` line directly beneath it, taken together including the newline
   between them and the newline after. The count must be 1; report it. Delete
   exactly those bytes, re-run, and report the exit code and every failing node
   id. Then restore the file from its saved pre-mutation bytes and report that
   its sha256 is identical to the pre-mutation reading. Report a mutation that
   stays GREEN as green: that is a true reading about a test that does not bite,
   and it is worth more than a colour that was expected. Finally remove the
   worktree and report `git worktree list`.

G6 PUSH AND CLEAN TREE, after C5. `git push origin feature/f276-data-root-hygiene`,
   then `git status --porcelain` in the primary checkout — expect empty output —
   and `ls .agent/STOP` — expect it absent. Report all three. The integration
   gate's own transcript is C4's committed file and is quoted in the handback's
   Verification section by its summary line and its bad-node-id count.

Handback
Rewrite `.agent/handoff.md` as C5 describes, then report. The handback names
every gate with one line of its real output, declares every deviation, and
carries the item-status table with one row per bundle item and per gate. If any
gate is red, say so plainly with the output — a red gate honestly reported ends
the round cleanly and is not a failure of the worker.
