STEP T001-close / F275 — ROUND 25 — THE D3 SEQUENCE CLOSES: RETIRE THE SCAFFOLDING, REPAIR THE PLANS IT LEFT WRONG

Goal: close the DECISION F260 D3 sequence DECISION F275 D13 opened and D14 (c)
extended. Retire the four cluster scaffolding artefacts that became gates which
cannot fail the moment the module list emptied; repair the unstarted feature whose
plan names five commands this feature deleted; banner the historical `Groups` table
that has been quietly wrong for most of its rows; and sweep the three residues rounds
23 and 24 left in files their own change sets had named.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f275-r25.md`
  C0b  mirror the COMMITTED C0a blob into `.agent/last_block.md`
  C1   `.agent/plan.md` <- PLAN25
  C2   the record: LEDGER25 appended to `.agent/live_review.md`, SLIPS25 appended to
       `.agent/prose_slips.md`
  C3   DEC25 appended to `.agent/decisions.md` — DECISION F275 D15
  C4   retire the cluster scaffolding: `git rm` the four paths named below. The
       commit message NAMES R-0868.
  C5   the residues rounds 23 and 24 left: pairs S8, S9 and S10. The commit message
       NAMES R-0870.
  C6   the plans: pairs S1 to S6 into the F267 feature file, and pair S7 into
       `docs/system/architecture.md`. The commit message NAMES R-0858 and R-0843.
  C7   the handback

Change set — EXACTLY these paths, nothing else:
  .agent/authored/f275-r25.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  .agent/decisions.md
  .agent/f275_deletion_order.md                          (DELETED)
  tests/orchestration/cluster_deletion_map.txt           (DELETED)
  tests/orchestration/test_cluster_deletion_map.py       (DELETED)
  tests/orchestration/test_cluster_deletion_order.py     (DELETED)
  apps/cli/command_catalog.py
  docs/system/mission-run-loop-morning-report-v0.md
  docs/roadmap/features/T2_F267.md
  docs/system/architecture.md
  .agent/handoff.md

Constraints:
 1. Every slice between a BEGIN and END marker is applied BYTE FOR BYTE. Do not
    reflow, re-wrap, re-indent or "fix" anything inside one. If a slice looks wrong,
    apply it anyway and declare it in the handback.
 2. Marker lines are never written into any target file.
 3. THE APPEND CONVENTION for `.agent/live_review.md`, `.agent/prose_slips.md` and
    `.agent/decisions.md`, verified by the reviewer against all three at `06dbb1c6`:
    each file ends with exactly ONE newline byte. An append writes
    `pre + b"\n" + slice`, where the slice itself ends with one newline. The ledger's
    length at this base is 732715 bytes — the round 24 handback's own arithmetic
    re-baselines here, not on any earlier figure.
 4. WITHIN a slice bound for `.agent/live_review.md` or `.agent/prose_slips.md`,
    records are separated from each other by a BLANK line.
 5. C2 is the FIRST substantive commit of this round, before C3 through C6.
 6. THREE COMMIT MESSAGES CARRY AN ID, and this is ordered rather than left to
    judgement because R-0859's fix clause asked for exactly that last round and the
    block that ordered the work forgot to order the message: C4 names R-0868, C5 names
    R-0870, C6 names R-0858 and R-0843. Commit subjects carry no leading-slash token
    and no absolute path, per AGENTS.md Commit Discipline.
 7. S10's FROM contains a comment line whose trailing rule is a run of exactly
    FIFTY-SEVEN U+2500 BOX DRAWINGS LIGHT HORIZONTAL characters, and its leading rule
    is a run of exactly TWO. The lengths are stated because a run of one repeated
    character is the one thing a reader cannot recover by eye. Transport is a byte
    copy, so nothing retypes it.
 8. PAIR SHAPES, each classified by a containment test the reviewer RAN at `06dbb1c6`,
    one reading per pair, output recorded. S1 to S7 and S9: TO contains FROM false ->
    REWRITE, FROM 1x in its target, TO 0x in the target before the edit. S8 AND S10 ARE
    DIFFERENT AND ARE THE TWO TO READ TWICE: TO contains FROM false and FROM 1x for
    both, but each TO ALREADY occurs 1x in its target before the edit, because each is a
    span deletion whose TO is a substring of its own FROM — S8's TO is the FROM's second
    line and S10's TO is the FROM's prefix. So NEITHER gets a "TO 1x" gate, which would
    be satisfied before the edit and is therefore no gate at all (§3 item 6). G6 gates
    them on what actually changes: for S8 the removed bullet going to zero and the file's
    remaining `self-repair` lines enumerated; for S10 the vacant banner line going to
    zero and the anchor line staying at one.
 9. NO module, command or catalog ENTRY is deleted in this round. C4 deletes four
    scaffolding files and S10 deletes a comment; `len(_BASE_CATALOG)` and
    `len(GROUPS)` are unchanged, and G6 measures that.
10. Destructive verification runs ONLY inside a disposable `git worktree`, never in
    the primary checkout. Remove and prune it before the handback.
11. Read `.agent/STOP` from disk before the first commit. If it exists, write the
    handback and stop.
12. DO NOT RUN THE SUITE WHILE THE FOUR DELETIONS ARE UNCOMMITTED, and if you do, read
    the red correctly rather than chasing it. The reviewer measured this at `06dbb1c6`
    in a disposable worktree:
    `tests/orchestration/test_evidence_index.py::TestPorcelainParsing::test_every_enumerated_path_exists_in_this_repo`
    walks `dirty_source_test_files`, which reads `git status --porcelain`, and asserts
    every enumerated path exists — so an UNCOMMITTED deletion makes it fail on the path
    it just removed, and the same run is green the moment C4 commits. That is the
    producer's blindness to deletion, which is R-0839's subject, not a defect this
    round introduces. G8 runs after C6 for exactly this reason. The same worktree also
    reddens `TestVitestFrontendTestFoundation::test_vitest_passes` with
    `ERR_MODULE_NOT_FOUND`, because `apps/ui/node_modules` is gitignored and a fresh
    worktree carries no runner — which is why G8 runs in the PRIMARY checkout.

Done when — G1 to G8 below have all been RUN, with their real exit codes recorded,
and the handback carries ONE line per gate. Every gate runs at or before C6.

G1 TRANSPORT. `sha256` of the committed `.agent/authored/f275-r25.md` blob at C0a
equals the digest the delegation names, and the committed `.agent/last_block.md` blob
at C0b equals the same digest. Report both. Per §3 item 37 this covers those two
committed artefacts and the reviewer's scratch original, and claims nothing about the
bytes that travelled into your prompt.

G2 THE PLAN. `.agent/plan.md` at C1 is byte-identical to PLAN25. Report its byte length
and line count, under the AGENTS.md cap of 50, and confirm `^## Goal$` and
`^## Next Steps$` each occur exactly once.

G3 THE RECORD, at C2, for `.agent/live_review.md` and `.agent/prose_slips.md`
separately. Reading (a), bytes: the committed post-blob equals the pre-blob, then one
newline, then the slice exactly as extracted; READ THE JOINING BYTE BACK from the post
blob at offset len(pre) and report it. Reading (b), structure: count N as the number of
blank-line-separated paragraphs IN THE SLICE with your own script — never from this
block — and compare the LAST N blank-line units of the whole post-file against those N
paragraphs IN ORDER. Negative control: flip one byte inside the FIRST appended
paragraph and confirm BOTH readers reject it while both accept the truth. Then report
over the whole post-file: `^Gate: F275 R24 ` exactly 1, `^Note: F275 R25 ` exactly 2,
`^Done: R-0859 — ` exactly 1, `^Done: R-0871 — ` exactly 1, and `^Done: R-0864 — `
still exactly 1. Finally report THE OPEN SET BY DISTINCT ID, every distinct id in a
`^- R-\d+ — ` paragraph minus every distinct id in a `^Done: R-\d+ — ` line. The
reviewer computed it at `06dbb1c6` as 92, over 100 distinct registrations against 8
distinct resolutions. It must read 90 at C2, because this commit registers nothing and
resolves two.

G4 THE DECISION, at C3, over `.agent/decisions.md`. The same two readings and the same
negative control as G3. Then report `^## DECISION F275 D15 ` as occurring exactly once
in the whole file.

G5 THE RETIREMENT, at C4. `git ls-tree` at C4 resolves NONE of
`.agent/f275_deletion_order.md`, `tests/orchestration/cluster_deletion_map.txt`,
`tests/orchestration/test_cluster_deletion_map.py` and
`tests/orchestration/test_cluster_deletion_order.py`, and all four resolved at the
parent. Then, over every tracked file outside `.agent/` and `.data/`, report a HARD
ZERO for the bare tokens `cluster_deletion_map`, `cluster_deletion_order` and
`f275_deletion_order`. The reviewer measured at `06dbb1c6` that the only references
outside the four files themselves are in `docs/roadmap/features/T2_F274.md` and
`docs/roadmap/features/T2_F275.md`, which are HISTORY PROSE under
`docs/roadmap/features/` and stay — so report those separately as the RAW list, per
R-0869's split-sweep clause, and drive only the tracked-file-outside-`docs/roadmap/`
half to zero. Finally: `python3 -m pytest tests/orchestration/ -q` real exit code and
real counts, and the collected-test count at C4 against the parent, whose difference
must be exactly the SIX tests those two files contributed.

G6 THE RESIDUES AND THE CATALOG, at C5. For S9 the FROM reads 0x and the TO reads 1x in
`docs/system/mission-run-loop-morning-report-v0.md`. For S8, per constraint 8, the FROM
reads 0x and the line `- Is there a proposed self-repair prompt?` reads 0x; there is no
TO count. Then over that ONE file PRINT EVERY LINE matching `self-repair` or
`self repair`, case-insensitively, with its line number, and report the total: the
reviewer measured that after both pairs exactly three remain, all inside the "How
Self-Repair Proposals fit" section round 24 rewrote to say the mechanism is gone. Report
what YOU measure; a line outside that section is the defect this gate exists to find.
For S10: the FROM reads 0x in `apps/cli/command_catalog.py`, the line
beginning `    # ── dogfood ` reads 0x, and `        related=("snapshot.inspect",),`
STILL reads exactly 1x. Then, through the SHIPPED reader by importing
`apps.cli.command_catalog`: `len(_BASE_CATALOG)` is 222, `len(GROUPS)` is 44, and
resolving every `related=` tuple against the live id set gives ZERO dangling
references — all three UNCHANGED from `06dbb1c6`. And
`python3 -m ruff check apps/cli/command_catalog.py`.

G7 THE PLANS, at C6. For each of S1 to S7 the FROM reads 0x and the TO reads 1x in its
target. Then over `docs/roadmap/features/T2_F267.md`, for each of the five deleted ids
`repair.item-list`, `builder.session-list`, `execution.approval-list`,
`external-builder.package-list` and `self-repair.proposal-list`: print every hit with
its line number, print the line range of the blockquote S2 introduces, and report the
count of hits OUTSIDE that blockquote, which must be ZERO. A flat zero over the whole
file is NOT ordered and would be a gate that cannot pass, because the blockquote names
all five ids on purpose — that is R-0869's split-sweep clause applied to a page. Report
the four surviving ids `test.list`,
`mission.list`, `change.list` and `event.list` as each occurring at least once. Then
`python3 -m pytest tests/docs/ -q`, which is the docs-round gate this change set's
`docs/roadmap/**` path makes mandatory.

G8 THE SUITE AND HYGIENE, at C6, from the PRIMARY checkout.
  python3 -m pytest tests/orchestration/ tests/cli/test_product_spine.py tests/test_command_catalog.py tests/docs/ -q
  python3 -m pytest tests/cli/test_golden_path.py -q
Report both real exit codes and real counts. The full suite is NOT part of this round's
gate. Then: `.agent/STOP` does not exist; `git status --porcelain` is EMPTY;
`git worktree list` holds exactly ONE entry; the branch is
`feature/f275-one-world-completion-part-three`; `git diff --name-status 06dbb1c6..C6`
names EXACTLY the change-set paths above other than `.agent/handoff.md`, with the four
retired paths carrying status `D`, reported as an exact set match with MISSING and
EXTRA both printed even when empty; and each commit's insertion count from
`git show --numstat`, for every commit before the handback commit, against the
AGENTS.md DECISION F104 D1 cap of 500.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md — the state
block with the SESSION NUMBER, the per-commit changed-files table with `+/-` cells
transcribed from `git show --numstat` and compared cell by cell against it, one line
per gate with its real exit code, every declared deviation, the item status table, and
the next expected action. There is no length cap. Then push.

<<<BEGIN PLAN25>>>
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 25 closes the DECISION F260 D3 sequence. It retires the four cluster scaffolding
artefacts that became gates which cannot fail once the module list emptied, repairs the
unstarted F267 plan that names five commands this feature deleted, banners the historical
`Groups` table in `docs/system/architecture.md` instead of maintaining a hand-written
mirror of the catalog, and sweeps the three residues rounds 23 and 24 left behind in files
their own change sets had already named.

## Next Steps

1. T002: the DECISION F272 D7 raising-property probe over every candidate `.id` receiver,
   giving the real site set rather than D15's upper bound, then the dated decision choosing
   the route. No production line moves in that slice.
2. T003, the classic runner, which T002's ruling is the prerequisite for.
3. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   STATUS line and the PR.

## Risks

- The open set is 92 by distinct id at this round's base `06dbb1c6`, computed mechanically
  from the record. This round registers nothing and resolves two, leaving 90. Four are High
  — R-0803, R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per DECISION
  F272 D12.
- Retiring the two ratchets removes six passing tests. DECISION F275 D15 rules it and states
  what still holds the tree honest once they are gone: the import-reachability ratchet,
  which F274 D1 ruled a ratchet and which this round does not touch.
- T002 is the slice that has been deferred by three features. It needs a fresh session's
  full context and is the reason this one should not start it late.
<<<END PLAN25>>>

<<<BEGIN LEDGER25>>>
Gate: F275 R24 — the F275 round 24 entry. VERDICT PASS, written by the planner and reviewer of session 13 after reading the committed range `ea5f8128`..`06dbb1c6` and RE-RUNNING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was not evidence for any line here. Booked by round 25's C2 from the pushed handback, under amend0827-process-diet rule 1. EIGHT single-parent commits C0a `379e98de`, C0b `dc307a9e`, C1 `d7d20e60`, C2 `0d68d754`, C3 `98539f94`, C4 `90a72e8d`, C5 `b11bd5fb` and C6 `06dbb1c6`, per-commit insertions 480, 417, 16, 18, 52, 24 and 26 for the seven before the handback, every one under the AGENTS.md DECISION F104 D1 cap of 500. G1 TRANSPORT covers the chain this workflow can walk and NOT the emitted bytes, per §3 item 37: the reviewer's scratch original, the committed `.agent/authored/f275-r24.md` and the committed `.agent/last_block.md` are all 41171 bytes at `2bd1b0c6436c263222f76a0c927aef9b7690cf5fae4b88544c1f112a7b58f9ff` and compare BYTE-EQUAL. G2: `.agent/plan.md` at C1 is 2181 bytes byte-identical to PLAN24, 40 lines against the cap of 50. G3 AND G4 HELD OVER THREE APPENDS, each re-run by the reviewer: `.agent/live_review.md` 718208 to 732715, `.agent/prose_slips.md` 205219 to 207261 and `.agent/decisions.md` 1005161 to 1009356, every post-blob equal to its pre-blob then ONE newline then the slice exactly as extracted, with the joining byte READ BACK at offset len(pre) and reading `b'\n'` in all three. The structural reader counted N from each slice — 6, 3 and 5 paragraphs — and matched the last N blank-line units of each whole post-file IN ORDER. The reviewer ran its OWN negative control on the FIRST appended paragraph of the DECISION slice this time rather than the ledger slice, so the two rounds between them exercise both files: the byte reader rejects it, the structural reader rejects it, both accept the truth, and the later paragraphs are provably untouched. `^Gate: F275 R23 `, `^- R-0871 — `, `^Done: R-0864 — `, `^Done: R-0862 — ` and `^Landed: R-0862 ` each read exactly 1, `^Note: F275 R24 ` reads exactly 3, and `^## DECISION F275 D14 ` reads exactly 1. THE OPEN SET HELD AT 92 BY DISTINCT ID, over 100 registrations against 8 resolutions, which is correct for a round registering one id and resolving one. G5 THE CATALOG, read by IMPORTING the shipped reader rather than by grepping source: commands 222 and groups 44 both UNCHANGED, `mission.run`'s options exactly `run_id`, `--iterations`, `--no-llm`, `--project` and `--json` with all three dead options ABSENT, `related` exactly `("mission.report", "mission.ledger")`, the description carrying neither `dogfood` nor `run id`, and DANGLING `related=` REFERENCES AT ZERO where the reviewer measured TWO at the base. Ruff clean over both touched Python files. G6 THE RED PROOF BIT, and the reviewer takes the worker's method as sound because it reported the import probe that makes it evidence: in a disposable worktree with `__pycache__` purged and `python3 -B`, the unmutated control is exit 0 at 26 passed, adding one bogus id to `mission.run`'s `related` tuple — bytes the worker verified UNIQUE in that file, per §3 item 25 — gives exit 1 with EXACTLY ONE failure, `TestCatalogIntegrity::test_every_related_reference_resolves_to_a_live_command`, and the revert returns exit 0 at 26 passed with the worktree porcelain EMPTY. The guard R-0859 asked for exists and bites. G7: over the operator page, all six spaced `remedy dogfood` forms and `--job-id` read ZERO, and `remedy self proposal-list` still reads ZERO, which `tests/cli/test_product_spine.py` pins. G8: 633 passed at exit 0 across the five named files and the canary 42 passed, both re-run by the reviewer in the primary checkout; no `.agent/STOP`, porcelain EMPTY, ONE worktree, the branch correct, `ea5f8128..b11bd5fb` naming EXACTLY the nine change-set paths with MISSING and EXTRA both empty, and every one of the nine `+/-` cells of the handback's `## Commits` table agreeing with `git show --numstat` for its commit. THE THREE DECLARED DEVIATIONS ARE SUSTAINED and none is a worker error: G1's reference digest lives in the delegation rather than in the block, which the round 23 slip already recorded; S-shaped banner narrowing of one column, measured against a file whose 52 banners already span 72 to 83 columns; and LEDGER24 writing a `Done:` and a registration with no `Landed:` line, applied verbatim and flagged. THE THREE FINDINGS THE WORKER RAISED THAT THE BLOCK DID NOT NAME ARE ALL REAL, the reviewer measured each at `06dbb1c6`, and two of them are folded into R-0870 by the `Note: F275 R25` entry below while the third — that a block re-baselining its append arithmetic on 717936 would be one append behind, because round 23's C4 took the ledger to 718208 — is a prose slip and is corrected in constraint 3 of the round 25 block, which states 732715.

Note: F275 R25 — new evidence for the OPEN finding R-0870, added rather than given an id of its own per `docs/agents/planner_reviewer_prompt.md` §3 item 30, and recorded because it is the class recurring in the round that WIDENED the clause meant to stop it. R-0870 records prose falsified by a deletion that no gate can see. THESE ARE THE FIFTH AND SIXTH INSTANCES, both measured by the reviewer at `06dbb1c6` while gating round 24, and both are in files that round's OWN change set named. FIRST, `docs/system/mission-run-loop-morning-report-v0.md` now says of self-repair proposals "They do not, any more" at line 65, while line 60 still asks "Is there a proposed self-repair prompt?" among the questions the morning report answers and line 77 still lists "Applying approved self-repair proposals" among the steps that require operator action — so one page contradicts itself within seventeen lines, and the pair that repaired the section did not reach the two bullets outside it. SECOND, `apps/cli/command_catalog.py` carries a section banner reading `# ── dogfood ──` with NO entries beneath it, the readerless-banner half of the class, in a file the same round edited twice. The worker found both, declined to widen an exact change set to reach them, and flagged them, which is the correct handling. WHY NEITHER IS A NEW ID: R-0870 is OPEN, both are Low for the reason its other instances are — nothing executes either line — and its widened fix clause, which orders a pair authored against the WHOLE enclosing unit, is precisely what would have caught them. WHAT THIS ADDS TO THAT CLAUSE, and it is the sharper half: the enclosing unit of a page-level claim is THE PAGE, not the section, so a sweep for the CONCEPT in the page's own words — "self-repair", "dogfood", "overnight" — runs beside the sweep for identifiers. Both are repaired by this round's C5, which constraint 5 and the bundle order after this commit.

Note: F275 R25 — new evidence for the OPEN finding R-0839, added rather than given an id of its own per `docs/agents/planner_reviewer_prompt.md` §3 item 30, because it is the same producer and the same blindness. R-0839 records that the closure bundle's content proof carries no tombstone for a deleted path, so the one document the packager calls the authority source cannot tell "deleted" from "never in scope". THIS IS THAT BLINDNESS REACHING A TEST rather than a package, measured by the reviewer at `06dbb1c6` in a disposable worktree while dry-running the round 25 change set: `tests/orchestration/test_evidence_index.py::TestPorcelainParsing::test_every_enumerated_path_exists_in_this_repo` walks `dirty_source_test_files`, which reads `git status --porcelain`, and asserts that every path it enumerates exists on disk. A working tree holding an UNCOMMITTED deletion therefore fails that test on the very path it has just removed — the reading was `enumerated a nonexistent path: .agent/f275_deletion_order.md` — and the same run is green once the deletion is committed, which the reviewer confirmed by committing in that worktree and re-running to 33 passed. NOTHING IS WRONG ON DISK and no round has ever been broken by it, because every round of this workflow commits before it gates. What it costs is a false red for anyone who runs the suite mid-edit on a deletion, which is precisely the moment a worker most wants to run it, and the failure message points at the deletion rather than at the enumerator. WHAT WOULD RESOLVE IT is R-0839's own fix: the producer distinguishing a deleted path from a missing one — a porcelain `D` status is already in the bytes it parses — after which the guard can assert existence for the paths that should exist and a tombstone for the rest. This round does not widen into `packages/orchestration/evidence_index.py` to do it; constraint 12 of the round 25 block states the expectation instead, so the worker reads the red correctly rather than chasing it.

Done: R-0859 — Resolved by F275 round 24's C4 `90a72e8d`, verified by the reviewer of session 13 by re-running the measurement itself through the SHIPPED reader rather than reading the worker's report. The finding recorded that `apps/cli/command_catalog.py` carried `related=` cross-references to commands that no longer exist and that no guard in the repository could see them. BOTH DANGLING REFERENCES ARE GONE: `mission.run` no longer names the deleted `dogfood.run-loop` and `repo.status` now names `readiness.job` in place of `readiness.show`, a command id that has not existed for many features. THE GUARD NOW EXISTS AND BITES: `tests/test_command_catalog.py::TestCatalogIntegrity::test_every_related_reference_resolves_to_a_live_command` resolves every tuple against the live `CATALOG` id set, and its colour was measured in a disposable worktree at C4 — control exit 0 at 26 passed, one bogus id giving exit 1 with EXACTLY that one test failing, revert exit 0 at 26 passed. Resolving every tuple at `06dbb1c6` gives ZERO dangling references where the reviewer measured TWO at `ea5f8128`. ONE CLAUSE OF THE FIX WAS NOT HONOURED AND IS RECORDED RATHER THAN GLOSSED: the clause asked that the round "names this id in its own commit message", and C4's subject names the work without naming R-0859. The block that ordered the work did not order the message, which is the reviewer's omission and not the worker's; it is a prose slip below, and it is not repaired, because repairing it would mean rewriting a pushed commit and `docs/agents/self_drive_protocol.md` G2 forbids that outright. The substance the clause exists to secure — the repair, the guard and the colour — landed in full, and this paragraph is the pointer a reader searching for R-0859 will find in place of the commit subject.

Done: R-0871 — Resolved by F275 round 24's C4 `90a72e8d` and C5 `b11bd5fb`, verified by the reviewer of session 13 through the shipped catalog reader and by reading the committed page. The finding recorded that `remedy mission run` advertised a second mode it no longer had and three options no code path read, every one of them accepted silently. THE CATALOG ENTRY NOW MATCHES THE HANDLER: `get_command("mission.run")` gives options exactly `--iterations`, `--no-llm`, `--project` and `--json`, with `--job-id`, `--max-steps` and `--max-seconds` ABSENT, so the parser now refuses what `_cmd_mission_run` cannot honour instead of accepting it in silence; the description names the F070 loop alone and carries neither `dogfood` nor `run id`; and the section comment above it no longer calls the entry a facade over a deleted command. THE OPERATOR PAGE WAS REPAIRED IN THE SAME ROUND, which matters because the page is where a user would have found the flags after `--help` stopped offering them: its Quick start no longer recommends `remedy mission report <run_id> --job-id <job_id>`, an invocation that could not parse against the shipped entry, and its stop-condition list no longer promises per-step and wall-clock caps that nothing enforced. DECISION F275 D14 (a) records why the three options were REMOVED rather than WIRED, and states the user-visible consequence plainly: an operator who was passing `--max-steps` now gets an argparse error where they previously got silence, which is the safer direction because the flag never did anything. The fix clause R-0871 carries — that an option is read by its handler in the same commit or is not declared — binds forward and is not discharged by this resolution.
<<<END LEDGER25>>>

<<<BEGIN SLIPS25>>>
2026-09-10 · F275 R24 · R-0859's fix clause asked that the round repairing the dangling `related=` references "names this id in its own commit message", and the round 24 block ordered the repair, the guard and the colour without ordering anything about the commit subject — so C4 `90a72e8d` names the work and not the id, and the clause landed part-met on a round that did everything else it asked. Nothing is wrong on disk and the commit is pushed, so G2 forbids repairing it. The lesson is that a fix clause specifying a property of a COMMIT — its message, its position, its atomicity — is transcribed into the block's own constraints, because a block orders commits and a clause read only for its code half quietly drops the other one.

2026-09-10 · F275 R24 · The round 24 block's LEDGER24 slice reported round 23's ledger append as "702413 to 717936", which is C2's true post-length, while round 23's C4 appended the `Landed: R-0870` line and left the file at 718208 — so the figure is right about the commit it names and wrong as a baseline, and a later block re-deriving its append arithmetic from it would be one append behind. The worker measured it and said so. The lesson is that a byte length quoted for a round is labelled with the COMMIT it was taken at whenever a later block might read it as the file's current size, and that a round appending to the same file twice has two lengths rather than one.

2026-09-10 · F275 R24 · The round 24 block's Q7 pair rewrote the "How Self-Repair Proposals fit" section to say the mechanism is gone, and left two bullets outside that section — one in the morning-report question list and one in the manual-steps list — still promising it, seventeen lines apart on the same page. The block had been written in the same round whose LEDGER24 widened R-0870's fix clause to demand a pair authored against the WHOLE enclosing unit. The lesson is the one the widened clause states and this block did not apply to itself: for a claim about a PAGE the enclosing unit is the page, so the sweep runs over the page's own vocabulary before the pair is written, not after the worker reports what it found.
<<<END SLIPS25>>>

<<<BEGIN DEC25>>>
## DECISION F275 D15 (2026-09-10, F275 round 25) — the cluster deletion map, its two ratchets and the deletion order file are RETIRED, and what still holds the tree honest is named

CONTEXT. F274 built `tests/orchestration/cluster_deletion_map.txt` with the ratchet
`tests/orchestration/test_cluster_deletion_map.py` holding it against the live import
graph in both directions, and F275 round 5 added `.agent/f275_deletion_order.md` with
`tests/orchestration/test_cluster_deletion_order.py` holding that against the same
graph. Both existed to bound and sequence a deletion. Round 22 deleted the last
component; `CLUSTER_MODULES` is the empty tuple, the map holds no edge lines and the
order file holds no component lines. R-0868 measured the consequence: with an empty
subject both ratchets pass for every possible state of the repository, which is the
gate-that-cannot-fail shape this record spends ids on.

CHOSEN: all four artefacts are deleted, in one commit, and the six tests they
contribute go with them. R-0868's clause offered the alternative explicitly — retire
them together, or record a dated decision saying why an empty ratchet is kept — and
this is the first half taken.

WHY, and this is the part a later reader needs. A ratchet whose subject is empty is
not a cheap safety net, it is a false one: it reports green in the same voice it used
when it was measuring something, and the next reader has no way to tell the two apart
without opening it. Keeping it would also leave `.agent/f275_deletion_order.md` as a
state file that outlives its feature, which the `.agent/` contract in AGENTS.md does
not contemplate. Git is the archive, exactly as AGENTS.md Scope Control says for a
replaced mechanism, and the map's own history is where the twenty-four modules and
their forty-two edges are recorded.

WHAT STILL HOLDS THE TREE HONEST, named because deleting a guard without naming its
successor is how a gap gets made. `tests/orchestration/test_import_reachability.py`
with its allowlist SURVIVES and is untouched by this round; DECISION F274 D1 ruled it
a RATCHET rather than a one-shot gate, and it is the guard that fails if any deleted
module is reimported or any new module becomes unreachable. The catalog's own
integrity tests, including the referential-closure test F275 round 24 added, hold the
command surface. Neither of those has an empty subject.

ALTERNATIVES CONSIDERED. (i) Keep the two ratchets with a dated comment explaining the
empty subject — rejected because the comment would be read by whoever opens the file
and the GREEN would be read by everyone else, and the second audience is larger. (ii)
Repoint the map's ratchet at some other module set so it keeps measuring something —
rejected because inventing a subject for a guard is how a guard stops meaning what its
name says, and no such set was asked for by any feature.

HOW TO REVERSE: restore the four paths from git history at `06dbb1c6`, which is this
round's base and the last commit at which all four exist.
<<<END DEC25>>>

S1 — docs/roadmap/features/T2_F267.md — REWRITE — the title's numeral
<<<BEGIN S1 FROM>>>
# T2_F267 — List commands v2 completion — sort/filter/limit for the remaining nine commands
<<<END S1 FROM>>>
<<<BEGIN S1 TO>>>
# T2_F267 — List commands v2 completion — sort/filter/limit for the remaining list commands
<<<END S1 TO>>>

S2 — docs/roadmap/features/T2_F267.md — REWRITE — the scope list and its numerals
<<<BEGIN S2 FROM>>>
The nine list-shaped commands F262 left parsing the shared flags but ignoring
them honour `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
exactly as the fifteen F262 wired do, with newest-first as the default, and
two tests F262 never built prove the whole catalog rather than a sample:

- test.list · repair.item-list · builder.session-list ·
  execution.approval-list · mission.list · change.list · event.list ·
  external-builder.package-list · self-repair.proposal-list

DONE when every one of the nine exits non-zero on `--sort bogus` naming its
<<<END S2 FROM>>>
<<<BEGIN S2 TO>>>
The list-shaped commands F262 left parsing the shared flags but ignoring
them honour `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
exactly as the ones F262 wired do, with newest-first as the default, and
two tests F262 never built prove the whole catalog rather than a sample:

- test.list · mission.list · change.list · event.list

> **Scope narrowed by F275 on 2026-09-10, finding R-0858.** This list held five
> more ids — `repair.item-list`, `builder.session-list`,
> `execution.approval-list`, `external-builder.package-list` and
> `self-repair.proposal-list` — and F275 deleted every one of them with the
> prototype cluster it removed. The numerals that counted them are deleted
> rather than re-synchronised, per `docs/agents/planner_reviewer_prompt.md` §3
> item 16. The session that claims this feature re-derives the in-scope set
> from `apps/cli/command_catalog.py` through the shipped reader, never from
> this file.

DONE when every one of them exits non-zero on `--sort bogus` naming its
<<<END S2 TO>>>

S3 — docs/roadmap/features/T2_F267.md — REWRITE — the F262 measurement, dated as history
<<<BEGIN S3 FROM>>>
F262's round 23 (FINDING R-0796 in `.agent/live_review.md`) measured the
catalog mechanically: 28 list-shaped commands, 15 wired to
`packages/orchestration/list_options.apply_list_options`, 13 not. DECISION F262
D4 excluded four of the 13 permanently — `builder.adapter-list`,
`execution.template-list`, `worker.registry-list` (no date on their row shape)
and `approval.policy-list` (browsed by name/state, not recency) — and kept the
nine above IN scope because each has a genuine date field and is exactly the
class T003 exists to fix. They did not fit F262's remaining round budget, and
the operator ruled (DECISION F262 D5) to close F262 at the 24-of-28 scope and
finish the nine here rather than run F262 past its soft limits.
<<<END S3 FROM>>>
<<<BEGIN S3 TO>>>
F262's round 23 (FINDING R-0796 in `.agent/live_review.md`) measured the
catalog mechanically: 28 list-shaped commands, 15 wired to
`packages/orchestration/list_options.apply_list_options`, 13 not. DECISION F262
D4 excluded four of the 13 permanently — `builder.adapter-list`,
`execution.template-list`, `worker.registry-list` (no date on their row shape)
and `approval.policy-list` (browsed by name/state, not recency) — and kept the
rest IN scope because each has a genuine date field and is exactly the
class T003 exists to fix. They did not fit F262's remaining round budget, and
the operator ruled (DECISION F262 D5) to close F262 at that scope and
finish the remainder here rather than run F262 past its soft limits.

Every count in the paragraph above is F262's, taken on 2026-09-05, and is kept
as the record of the decision it explains. It is no longer a description of the
catalog: F275 deleted all four D4 exclusions along with five of the commands
that paragraph kept in scope, and the catalog fell from 339 commands to 222 in
the same feature. Read `apps/cli/command_catalog.py` for what ships.
<<<END S3 TO>>>

S4 — docs/roadmap/features/T2_F267.md — REWRITE — the T001 heading's numeral
<<<BEGIN S4 FROM>>>
## T001 — The nine wirings
<<<END S4 FROM>>>
<<<BEGIN S4 TO>>>
## T001 — The wirings
<<<END S4 TO>>>

S5 — docs/roadmap/features/T2_F267.md — REWRITE — the T002 exclusion sentence
<<<BEGIN S5 FROM>>>
T001) cannot. The four D4 exclusions are named in the test by id and reason.
<<<END S5 FROM>>>
<<<BEGIN S5 TO>>>
T001) cannot. The D4 exclusions are named in the test by id and reason, for as
many of them as still exist — F275 deleted all four, so the session that builds
this test re-measures the exclusion set before writing it down.
<<<END S5 TO>>>

S6 — docs/roadmap/features/T2_F267.md — REWRITE — the Acceptance numerals
<<<BEGIN S6 FROM>>>
- Each of the nine: `--sort bogus` exits non-zero and names the valid fields;
  `--limit 1` returns one row; `--since`/`--until` filter by the row's date.
- The catalog-driven handler test covers all 24 in-scope commands.
- The ten-second demo passes as a test.
<<<END S6 FROM>>>
<<<BEGIN S6 TO>>>
- Each command in scope: `--sort bogus` exits non-zero and names the valid
  fields; `--limit 1` returns one row; `--since`/`--until` filter by the date.
- The catalog-driven handler test covers every in-scope command, where the
  in-scope set is derived from the catalog at the time the test is written.
- The ten-second demo passes as a test.
<<<END S6 TO>>>

S7 — docs/system/architecture.md — REWRITE — banner the historical Groups table
<<<BEGIN S7 FROM>>>
### Groups

| Group     | Commands | Description |
|-----------|----------|-------------|
<<<END S7 FROM>>>
<<<BEGIN S7 TO>>>
### Groups

> **Status (2026-09-10): HISTORICAL SNAPSHOT, finding R-0843.** The table below
> records the groups the grouped CLI shipped with at the step that introduced
> it. Measured through the shipped reader at `06dbb1c6`: the catalog holds 222
> commands in 44 groups, and only three of the twelve rows below still state a
> command count the catalog agrees with. It is kept as the record of that step
> rather than repaired row by row, because a hand-written mirror of the catalog
> drifts by construction and would need repairing again after every feature
> that adds or deletes a command. Read `apps/cli/command_catalog.py`, or run
> `remedy list`, for what ships today.

| Group     | Commands | Description |
|-----------|----------|-------------|
<<<END S7 TO>>>

S8 — docs/system/mission-run-loop-morning-report-v0.md — REWRITE — the report question list
<<<BEGIN S8 FROM>>>
- Is there a proposed self-repair prompt?
- What should I do next?
<<<END S8 FROM>>>
<<<BEGIN S8 TO>>>
- What should I do next?
<<<END S8 TO>>>

S9 — docs/system/mission-run-loop-morning-report-v0.md — REWRITE — the manual-steps list
<<<BEGIN S9 FROM>>>
- Starting the loop (`remedy mission run`)
- Reviewing builder output
- Applying approved self-repair proposals
- Merging PRs
<<<END S9 FROM>>>
<<<BEGIN S9 TO>>>
- Starting the loop (`remedy mission run`)
- Reviewing builder output
- Merging PRs
<<<END S9 TO>>>

S10 — apps/cli/command_catalog.py — REWRITE, and see constraints 7 and 8 — the vacant banner
<<<BEGIN S10 FROM>>>
        related=("snapshot.inspect",),
    ),

    # ── dogfood ─────────────────────────────────────────────────────────

<<<END S10 FROM>>>
<<<BEGIN S10 TO>>>
        related=("snapshot.inspect",),
    ),

<<<END S10 TO>>>
