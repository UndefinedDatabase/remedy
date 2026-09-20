STEP closure part two — F276 Data-root hygiene & disk budget, ROUND 8

This block contains no horizontal rule and no run of a repeated character, so
nothing in its frame has a length a reader must recover by eye (item 37).

Goal
Book round 7's verdict and the resolution of R-1006; spend the ONE repair round
operator amendment amend0917-throughput rule 2 allows, re-running the full suite
against a `apps/ui` that is BUILT BEFORE the run starts; and consume the one
self-use item closure precondition 6 requires. That is everything the closure
sequence needs before its last round. This round does NOT flip STATUS, does not
build the evidence package, does not rotate the ledger and does not open a pull
request.

Bundle, in commit order
C1 the bookkeeping, in ONE commit: the five payload copies under
   `.agent/authored/`, the ledger append, the decisions append, the two
   prose-slip lines, the plan rewrite.
C2 the integration gate's repair run and its transcript.
C3 the self-use item: generate, plan, run, and RECORD its defects.
C4 the handoff.

Payloads on disk
Every authored text of this round is a FILE the worker reads from disk. Nothing
is retyped. Each is named with its line count and its sha256; the worker
verifies the digest BEFORE using the file and reports both readings.

P1 `.remedy-wt/f276-r8/block.md` — this block.
   lines 246; the digest is in the delegation message that names this file.
P2 `.remedy-wt/f276-r8/ledger.md`
   lines 4; sha256 6ba01f3ef232816e86c7850f6ddf4799d68273a40584ff04e8d090f5bb99cb93
P3 `.remedy-wt/f276-r8/decisions.md`
   lines 58; sha256 7f71b167601c5d198fdd31a76c77c9ec582c2e2d517f7b4bee78394e16c114ba
P4 `.remedy-wt/f276-r8/plan.md`
   lines 43; sha256 8df1095f45da9ec7c42f72948caba7b06db88987fef3087f569c9437ba693b3d
P5 `.remedy-wt/f276-r8/prose_slips.md`
   lines 2; sha256 1a9a44a01a0d05b4f875b870ac0b9d4a849ed80a8ee0a9fb35522fe7bc512b03

P2, P3 and P5 are APPEND-shaped: each is concatenated onto the end of its
target, whose current bytes end with a newline, so the result is the target's
bytes followed by the payload's bytes and nothing else. P2 and P3 each begin
with a newline, which is the blank separator their targets' existing entries use;
P5 does not, because `.agent/prose_slips.md` is one line per slip with no blank
between them. P4 is a REWRITE: `.agent/plan.md` becomes exactly P4's bytes.
Containment test, run mechanically before emission, one reading per pair:
`.agent/live_review.md` contains P2 — false; `.agent/decisions.md` contains P3 —
false; `.agent/prose_slips.md` contains P5 — false; `.agent/plan.md` contains P4
— false. All four are therefore NEW bytes and no FROM-count proof is owed.

Change set — exactly these paths, and nothing else this round
  .agent/authored/f276-r8-block.md        (new, C1)
  .agent/authored/f276-r8-ledger.md       (new, C1)
  .agent/authored/f276-r8-decisions.md    (new, C1)
  .agent/authored/f276-r8-plan.md         (new, C1)
  .agent/authored/f276-r8-prose-slips.md  (new, C1)
  .agent/live_review.md                   (C1 append)
  .agent/decisions.md                     (C1 append)
  .agent/prose_slips.md                   (C1 append)
  .agent/plan.md                          (C1 rewrite)
  .agent/authored/f276-closure-suite.txt  (C2 rewrite)
  scripts/self_use_queue.json             (C3, the generated entry only)
  .agent/selfuse_f276/                    (C3, new artefact files)
  .agent/handoff.md                       (C4)

`scripts/self_use_queue.json` is touched in C3 ONLY by the generator appending
one pending entry. Its `consumed_by` field is NOT set this round: closure
precondition 6 puts that edit in the closure commit, which is round 9's.

C1 — the bookkeeping
Copy P1 to `.agent/authored/f276-r8-block.md`, P2 to `-ledger.md`, P3 to
`-decisions.md`, P4 to `-plan.md`, P5 to `-prose-slips.md`, each with
`shutil.copyfile`, never by retyping. Append P2's bytes to
`.agent/live_review.md`; append P3's bytes to `.agent/decisions.md`; append P5's
bytes to `.agent/prose_slips.md`; write P4's bytes over `.agent/plan.md`. Commit.

What P2 books: round 7's verdict, PASS, and the reviewer-authored resolution
`Done: R-1006`. What P3 appends: DECISION F276 D9, which rules what the closure
suite's three red nodes are and how they are repaired. What P5 appends: two
dated lines, one for the reviewer's own unmeetable G2 clause of round 7 and one
for the cold-checkout race this round repairs.

C2 — the integration gate's repair run
This is the ONE repair round amend0917-throughput rule 2 allows to be spent on
this bad set, and the rule it must satisfy is that the bad set STRICTLY SHRINKS
with NO node newly bad. Its base is round 7's committed transcript, whose bad set
is exactly these three:
  tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_post_to_job_dashboard_is_405
  tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_a_near_miss_of_the_commands_path_is_405
  tests/ui_server/test_live_state.py::TestUIServerIntegration::test_put_rejected

FIRST, build the UI, because the diagnosis DECISION F276 D9 records is that the
auto-build was still racing the `-n auto` workers when those three ran:

  cd apps/ui && npm run build

Report its exit code and its last line. It writes only into `apps/ui/dist`,
which is gitignored, so it changes no tracked file; confirm that with
`git status --porcelain` and report the reading. Do NOT run `npm install`: the
reviewer measured this build as `built in 1.41s` against the `node_modules`
already in this checkout, so a build that needs the network means something
changed and is a finding, not a step to force through.

THEN, from the repository root, in the PRIMARY checkout, never a worktree, ONCE:

  python3 -m pytest -n auto -q

Capture the real exit code — do not pipe the run into `tail` or `head`, which
replaces pytest's exit code with the pager's. Rewrite
`.agent/authored/f276-closure-suite.txt` completely, keeping the same path
because closure precondition 2 reads that one file by name, and state in it:
the command, the checkout, the commit, the exit code, the pytest summary line
verbatim, the wall clock, the PREVIOUS bad set of three quoted above, this run's
OWN complete bad set one node id per line and never truncated (or
`BAD NODE IDS: none` under its own heading when the run is green), and the two
readings the shrinking rule needs stated as arithmetic: how many of the previous
three are still bad, and how many nodes are newly bad that were not bad before.
Commit that file alone.

If this run's bad set is NOT empty: repair nothing, record it, commit, and say
so plainly in the handback. Two of the three repair rounds rule 2 allows are
then still unspent and the next one is the reviewer's to author.

C3 — the self-use item
Closure precondition 6: exactly one self-use item is consumed by this close. The
queue currently holds NO pending item — `pending_self_use_items()` answers an
empty tuple — so the generator runs first, exactly as the precondition orders:

  packages.orchestration.self_use_generator.generate_and_append_if_empty()

Report what it answered. If it answers None, the track is exhausted rather than
blocked: record `self-use NONE (queue exhausted)` in the handback and stop this
commit there, which is a legitimate outcome and not a failure.

Otherwise run the item to the normal approval gate, never applied:

  packages.orchestration.self_use_runner.run_next_self_use_item(
      dest_dir=Path(".agent/selfuse_f276"), repo_path=".")

Let it resolve its own builder and reviewer roles; do NOT pass
`builder_name="fake"` or `reviewer_name="fake"`, because a self-use run under the
fake provider proves nothing about Remedy being used on Remedy. Then read the
run's own defects:

  packages.orchestration.self_use_findings.describe_self_use_run_defects(result)

Record, under `.agent/selfuse_f276/`, one file per reading, each named for what
it holds: the queue entry and the job file path; the resolved
`execution_config`, which states which provider actually ran; the returned
`JobPlan`'s state; the full transcript of the run; and `run_defects.txt` holding
EVERY string that tuple returns, one per line, verbatim and never summarised, or
the literal `EMPTY TUPLE — no defect string was returned` when it is empty. An
empty tuple means nothing to register, NOT that nothing was checked, and the
file says which of the two it is. Commit.

REGISTER NOTHING. Those strings become R-id findings only in reviewer-authored
text, and the reviewer writes them into round 9's first commit after reading
this round's report. Write no `- R-` line and no `Done:` line this round beyond
what P2 already carries.

The self-use run is a REAL job. It may create a `remedy/job-*` branch and a
worktree under `.remedy-wt/`, and a job that ends BLOCKED retains both BY
DESIGN. Do not delete either and do not treat their presence as an unclean tree;
G5 below reads them as measurements.

C4 — the handoff
Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`: the SESSION
NUMBER (this is SESSION 2 of F276), the round, the branch, the per-commit tables
with `git show --numstat` insertion counts for C1 to C3, every gate below with
its real output and exit code, the open-findings count by both readings, the
item-status table, the deviations, the self-use outcome and every defect string
verbatim, and the next expected action. One sentence of context self-assessment.
No length cap. Its own insertion count belongs in its own text, not in a gate.

Constraints
1. Apply every payload byte for byte. A payload that looks wrong is REPORTED as
   a deviation and applied anyway; it is never edited and no slice is retyped.
2. Touch no path outside the change set above. In particular: do not edit
   `docs/roadmap/STATUS.md`, `README.md`, `docs/roadmap/features/T2_F276.md`,
   `docs/agents/planner_reviewer_prompt.md`, `.agent/candidates.md`, and do not
   set `consumed_by` in `scripts/self_use_queue.json` — every one of those is
   round 9's.
3. The commit sequence is C1, C2, C3, C4, in that order, no extra commit, none
   dropped, none reordered. Report any deviation.
4. Every commit's insertion count, by `git show --numstat`, stays under 500.
   Report each of C1 to C3's; C4's own belongs in its own text.
5. No destructive verification is ordered this round, so no disposable worktree
   is created for one. The self-use run's own worktree, if it keeps one, is the
   job's and is left alone.
6. Never force-push, never rewrite history, never delete a branch, never merge,
   never open or edit a pull request, never run any `gh` command. Work only on
   `feature/f276-data-root-hygiene`.
7. Read `.agent/STOP` from disk before the first commit. If it exists, write the
   handoff and end, doing nothing else.
8. The full suite of C2 runs exactly ONCE. If it is red, it is not re-run to see
   whether it passes the second time: that reading would be worth nothing and
   the rule spends repair rounds, not retries.

Done when — five gates, each executed, each reporting its REAL output and exit
code. "Green" as a word is a finding.

G1 TRANSPORT AND STATE, at C1. One python check printing an explicit True or
   False per reading: each of the five `.agent/authored/f276-r8-*` files equals
   its payload on disk byte for byte; `.agent/live_review.md` at C1 equals its
   `9fb2ab65` bytes plus P2's bytes; `.agent/decisions.md` at C1 equals its
   `9fb2ab65` bytes plus P3's bytes; `.agent/prose_slips.md` at C1 equals its
   `9fb2ab65` bytes plus P5's bytes; `.agent/plan.md` at C1 equals P4's bytes.
   Report the number of readings and that every one is True. SEPARATELY, report
   the SAVED BLOCK's own line count and sha256 beside the line count and digest
   the delegation message gave for P1, as two readings side by side (R-0954).

G2 THE UI BUILD, at C2 and BEFORE the suite run. Report `npm run build`'s exit
   code and its last line, and `git status --porcelain` immediately afterwards,
   which must be empty because `apps/ui/dist` is gitignored. A non-empty reading
   here is a finding and stops the round.

G3 THE REPAIR RUN, at C2. Report the exit code of `python3 -m pytest -n auto -q`
   taken from the process and not from a pipe, the pytest summary line verbatim,
   and the complete bad set. Then report the two shrinking-rule readings as
   numbers: of round 7's three bad nodes, how many are still bad; and how many
   nodes are bad now that were not bad then. Rule 2 is satisfied when the first
   number is smaller than three and the second is zero.

G4 THE CANARY, after C3, in the primary checkout:

  python3 -m pytest tests/cli/test_golden_path.py -q

   Report the summary line and the exit code. It runs AFTER the self-use job on
   purpose: a real job that has just run in this checkout is exactly the state a
   canary exists to check.

G5 PUSH, TREE AND WHAT THE JOB LEFT, after C4.
   `git push origin feature/f276-data-root-hygiene`; then `git status --porcelain`
   in the primary checkout, which must be EMPTY; then `ls .agent/STOP`, which
   must be absent. Then report, as measurements and not as pass or fail:
   `git worktree list` in full, and the count of `remedy/job-*` branches by
   `git branch --list "remedy/job-*"` taken BEFORE C3 and again after C4, both
   numbers printed. A self-use job that ends BLOCKED retains its worktree and
   its branch by design, so a difference here is information for the reviewer
   and not a violation; report it, change nothing.

Handback
Rewrite `.agent/handoff.md` as C4 describes, then report. The handback names
every gate with one line of its real output, declares every deviation, carries
the item-status table with one row per bundle item and per gate, and quotes
every self-use defect string verbatim. If any gate is red, say so plainly with
the output — a red gate honestly reported ends the round cleanly.
