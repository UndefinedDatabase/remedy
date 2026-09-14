── STEP T001 (documentary remainder) — F275 — ROUND 27 ──
(The rule line above and below are each exactly 56 characters, per §3 item 37.)

Goal: Make the advertisement guard see the defect class it was built for, and
repair every dead advertisement that widening exposes in PRODUCTION CODE. The
guard's scanner is blind three ways at `c370dcee`, and finding R-0847 records
the first: it pre-filters the group against `GROUPS`, so once a deletion feature
removes a group WHOLE every string still telling an operator to run one of its
commands stops matching. Round 26 found the second — the scanner matches only
`remedy <group> <sub>`, so a one-word invocation is invisible, which is how the
reviewer's own invented `remedy list` survived two rounds of a session whose
subject was dead advertisements. The reviewer's applied dry run found the third:
`_COMMAND_TAIL_CHARS` omits the BACKTICK, and a markdown page closes an inline
command with one, so 150 advertisements in `docs/` were never scanned at all.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f275-r27.md`
  C0b  mirror the COMMITTED C0a blob into `.agent/last_block.md`
  C1   `.agent/plan.md` <- PLAN27
  C2   the record: LEDGER27 into `.agent/live_review.md`, SLIPS27 into
       `.agent/prose_slips.md`
  C3   `docs/system/architecture.md` <- pairs U1 and U2
  C4   the guard and the production repairs: SPEC-GUARD, plus pairs P1..P8
  C5   the handback

Change set — exactly these paths, nothing else:
  .agent/authored/f275-r27.md          (C0a, new file)
  .agent/last_block.md                 (C0b)
  .agent/plan.md                       (C1)
  .agent/live_review.md                (C2, append)
  .agent/prose_slips.md                (C2, append)
  docs/system/architecture.md          (C3)
  tests/cli/test_advertised_commands.py (C4)
  packages/orchestration/brain_detail.py (C4)
  packages/orchestration/cockpit.py    (C4)
  packages/orchestration/trust_report.py (C4)
  .agent/handoff.md                    (C5)

Constraints:
 1. Every slice below is applied BYTE FOR BYTE. If a slice looks wrong, apply it
    anyway and DECLARE the doubt in the handback. Never repair a reviewer slice.
 2. Marker lines `<<<BEGIN ...>>>` / `<<<END ...>>>` never reach a target file.
    Extract each slice from the COMMITTED C0a blob, never from a retype.
 3. PAIR SHAPES, each from the reviewer's own mechanical containment test, one
    reading per pair — `TO contains FROM: false` for U1, U2, P1, P2, P3, P4, P5,
    P6, P7 and P8. All ten are REWRITES, so each gets the FROM 1x -> 0x and
    TO 0x -> 1x proof, measured before and after the write. No FROM-zero count is
    ordered for any append, because this block orders no append-shaped pair.
 4. C2's `Done: R-0847` paragraph describes a repair that lands at C4, one commit
    LATER. That is the §3 item 20 / R-0524 carve-out and it is legal only because
    THIS CONSTRAINT fixes the order: C4 is committed in the same round and before
    the handback, and the paragraph names this constraint rather than a SHA that
    cannot exist when the slice is written.
 5. Commit subjects carry NO leading-slash token, absolute path or secret-like
    string (AGENTS.md Commit Discipline). C3's subject names R-0843's residue;
    C4's subject names R-0847.
 6. `.agent/STOP` is re-read FROM DISK before the FIRST commit and again before
    C4. If it exists at either reading, stop and hand off.
 7. Destructive verification (G6) runs ONLY inside a disposable `git worktree`,
    never in the primary checkout, which satisfies `git status --porcelain` ==
    empty at the handback. Remove and prune the worktree before the handback.
 8. The allowlist in SPEC-GUARD is GENERATED from the worker's own measured sweep
    and never transcribed from this block. Its 43 entries are gated by digest in
    G5, so a retyped or hand-edited list cannot pass.
 9. No file outside the change set is edited, and no test is deleted, skipped or
    weakened to make a gate green.
10. Do not re-verify the deleted-module sweeps of round 26; they were measured at
    `319b8777` and hold.

──────── SPEC-GUARD — the scanner change, described not sliced ────────

Target: `tests/cli/test_advertised_commands.py`. Behaviour required, at C4:

 (a) `_COMMAND_TAIL_CHARS` gains the BACKTICK, becoming the five characters
     `<`, `{`, `"`, `'` and backtick. Its comment states WHY: a markdown page
     closes an inline command with a backtick, and omitting it hid every
     advertisement written as an inline code span from the operator-facing sweep.
 (b) A new module-level regex matches the SINGLE-token form `remedy <token>`,
     `token` being `[a-z][a-z0-9-]*`, beside the existing two-token regex.
 (c) The tail test becomes one named helper used by BOTH forms: after the match,
     left-strip spaces; accept when nothing remains, or the first character is in
     `_COMMAND_TAIL_CHARS`, or the remainder starts with `--`.
 (d) `scan_advertised_commands` DROPS `if group not in GROUPS: continue`. It
     returns a list of tuples: two-element for the two-token form, one-element
     for the single-token form. Its docstring names finding R-0847 as the reason
     the pre-filter is gone.
 (e) A new `_resolves(invocation)` decides reachability against the LIVE catalog:
     a two-element tuple must be in `{(e.group_id, e.subcommand) for e in
     CATALOG}`; a one-element tuple must be in `GROUPS`, because `remedy <group>`
     is the real group-help invocation.
 (f) `_sweep` yields, per unresolved site, a record carrying the path, the
     invocation tuple and the line number, whose allowlist KEY is
     `(path, " ".join(invocation))` and NEVER includes the line number — a
     line-keyed allowlist rots on the next edit anywhere in the file.
 (g) `KNOWN_DEAD_DOC_ADVERTISEMENTS` is a frozenset of those keys, GENERATED per
     constraint 8, sorted, with a comment stating that it is a RATCHET in the
     sense DECISION F274 D1 gave the word, why it exists, and that when it
     reaches zero it is deleted together with `_ALLOWLIST_CEILING` and the
     ratchet test. `_ALLOWLIST_CEILING` is its measured length.
 (h) The PRODUCTION sweep test is unchanged in effect and must find ZERO
     unresolved. The OPERATOR-FACING sweep test subtracts
     `KNOWN_DEAD_DOC_ADVERTISEMENTS` by key and asserts the remainder is empty.
     Both anti-blindness `seen > 100` floors stay exactly as they are.
 (i) ONE new test, `test_the_known_dead_doc_advertisement_list_only_ever_shrinks`,
     asserts BOTH ratchet halves: `len(...) <= _ALLOWLIST_CEILING`, and that no
     allowlist key is absent from the live unresolved set. Its docstring says why
     an allowlist that may not grow and may not go stale is not a suppression.
 (j) The three existing scanner unit tests are NOT edited. The reviewer measured
     that all three still pass under (a)-(f): the single-token form is filtered
     out of each by the tail rule, so their expected lists are unchanged.

WHAT THE REVIEWER ALREADY MEASURED, by APPLYING all of the above in a disposable
worktree at `c370dcee` and RUNNING it — these are the numbers G5 and G6 re-derive,
not predictions: the production sweep reads 542 seen and ZERO unresolved; the
operator-facing sweep reads 417 seen and 68 unresolved over 43 DISTINCT keys
across 7 paths; the guard file runs 6 passed; `ruff check` is clean on all four
edited Python files; and `tests/docs/ tests/cli/` with the five modules' own test
files is green at 2024 passed.

──────── The production repairs, as exact pairs ────────

Every one is a next-action string the product hands an operator, naming a flat
command the group-first restructure of Steps 38-40 replaced and nobody updated.
The reviewer probed all four replacements through the SHIPPED dispatcher at
`c370dcee`, read-only and in process: `remedy brain timeline`, `remedy dev
agent-loop` and `remedy brain constitution` each exit 2 printing THEIR OWN usage
line (`Usage: remedy brain timeline JOB_ID`), and `remedy worker list` exits 0
printing `Worker Adapters`; the dead controls `remedy timeline`, `remedy workers`
and `remedy brain no-such-sub` exit 2 printing the PARENT's usage line and never
their own. That difference is the discriminator, and `--help` is NOT it: the help
pre-scan short-circuits before the subcommand is validated, so `remedy brain
no-such-sub --help` exits 0 and a probe built on it proves nothing.

P1  packages/orchestration/cockpit.py
FROM: inspect with: remedy timeline <job_id>
TO:   inspect with: remedy brain timeline <job_id>

P2  packages/orchestration/cockpit.py
FROM: "      remedy timeline {job_id_str}\n"
TO:   "      remedy brain timeline {job_id_str}\n"

P3  packages/orchestration/trust_report.py
FROM: " (run: remedy constitution {job.id})"
TO:   " (run: remedy brain constitution {job.id})"

P4  packages/orchestration/brain_detail.py
FROM: next_actions=(f"remedy timeline {job_id_str}",),
TO:   next_actions=(f"remedy brain timeline {job_id_str}",),

P5  packages/orchestration/brain_detail.py
FROM: next_actions = [f"remedy agent-loop {job_id_str}"]
TO:   next_actions = [f"remedy dev agent-loop {job_id_str}"]

P6  packages/orchestration/brain_detail.py
FROM: "Created when remedy agent-loop was run against this job.",
TO:   "Created when remedy dev agent-loop was run against this job.",

P7  packages/orchestration/brain_detail.py
FROM: next_actions=(f"remedy constitution {job_id_str}",),
TO:   next_actions=(f"remedy brain constitution {job_id_str}",),

P8  packages/orchestration/brain_detail.py
FROM: "Inspect with `remedy workers` for all provider specs.",
TO:   "Inspect with `remedy worker list` for all provider specs.",

P6 is the one the widened guard does NOT reach — its tail is prose, so the tail
rule filters it — and it is repaired anyway because it names a dead command in a
string a reader sees. G5 does not gate it; G7's pair proof does.

──────── The architecture.md pair ────────

U1 repairs both defects round 26 declared in its own authored banner: the invented
`remedy list`, and a span narrower than the section it dates. The reviewer measured
the true span from the file's own headings at `c370dcee`: `## Group-first CLI v0`
at line 2908 is the LAST `##` heading, the file ends at line 3072, and the `###`
headings beneath it name Steps 41-43, 48, 50, 51, 52 and 53 — NOT a contiguous
range, which is why the TO enumerates rather than spans. The invented command is
removed rather than replaced: the sentence already points at the catalog file,
which is true and needs no probe.

<<<BEGIN U1 FROM>>>
> **Status (2026-09-10): HISTORICAL SNAPSHOT, finding R-0843.** This whole section
> records the CLI as it shipped at Steps 38 to 43. The group-first STRUCTURE it
> describes is still how the CLI works and is still accurate; every COUNT and every
> ENUMERATION in it is not. Measured through the shipped reader at `684b1b55`: the
> catalog holds 222 commands in 44 groups, so the twelve groups listed below are 12
> of 44; and the `action_class` list below omits `local_state_change`, which the
> catalog uses. Read `apps/cli/command_catalog.py`, or run `remedy list`, for what
> ships today. The section is dated rather than repaired sentence by sentence,
> because a hand-written mirror of the catalog drifts again after the next feature
> that adds or deletes a command.
<<<END U1 FROM>>>

<<<BEGIN U1 TO>>>
> **Status (2026-09-10): HISTORICAL SNAPSHOT, finding R-0843.** This whole section
> records the CLI as it shipped, and it reaches further than its own heading says:
> the heading names Steps 38 to 40, while the subsections beneath it carry Steps 41
> to 43, 48, 50, 51, 52 and 53, and the section runs to the end of this file. The
> group-first STRUCTURE it describes is still how the CLI works and is still
> accurate; every COUNT and every ENUMERATION in it is not. Measured through the
> shipped reader at `684b1b55`: the catalog holds 222 commands in 44 groups, so the
> twelve groups listed below are 12 of 44; and the `action_class` list below omits
> `local_state_change`, which the catalog uses. Read
> `apps/cli/command_catalog.py` for what ships today. The section is dated rather
> than repaired sentence by sentence, because a hand-written mirror of the catalog
> drifts again after the next feature that adds or deletes a command.
<<<END U1 TO>>>

U2 is the `Groups` table banner, which still says "twelve rows" while pointing at
a section banner that now enumerates its steps. Only the stale cross-reference
moves; the measurement it carries was re-verified at `c370dcee` and is unchanged.

<<<BEGIN U2 FROM>>>
> **Historical, under the banner at the top of this section.** Measured through
> the shipped reader at `06dbb1c6`, only three of the twelve rows below still
> state a command count the catalog agrees with: `readiness`, `context` and
> `file`. The table is kept as the record of what shipped at that step.
<<<END U2 FROM>>>

<<<BEGIN U2 TO>>>
> **Historical, under the banner at the top of this section.** Measured through
> the shipped reader at `06dbb1c6` and re-measured at `c370dcee`, only three of the
> rows below still state a command count the catalog agrees with: `readiness`,
> `context` and `file`. The table is kept as the record of what shipped at that
> step, and the flat commands named elsewhere in this section are dead: finding
> R-0872 carries them.
<<<END U2 TO>>>

──────── PLAN27 — the whole of `.agent/plan.md` ────────

<<<BEGIN PLAN27>>>
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 27 makes the advertisement guard see the class it was built for. Its scanner drops the
`GROUPS` pre-filter that hid every advertisement of a deleted group, gains the single-token
`remedy <something>` form, and counts a closing backtick as a command tail. Eight dead
next-action strings in production code become the live group-first commands, the
`architecture.md` banner loses the `remedy list` the reviewer invented and states the span it
really covers, and the dead advertisements the widening exposes on operator-facing pages are
pinned in a shrink-only allowlist as R-0872. R-0847 closes.

## Next Steps

1. R-0872's first half: delete the four pages that document command groups F275 deleted
   whole, and repair `core-product-spine-v0.md`, lowering the allowlist by 21.
2. R-0872's second half: the flat pre-Step-38 CLI in `architecture.md` and the one site in
   `vocabulary.md`, lowering the allowlist to zero and deleting the ratchet with it.
3. T002: the DECISION F272 D7 raising-property probe over every candidate `.id` receiver,
   giving the real site set rather than D15's upper bound, then the dated decision choosing
   the route. No production line moves in that slice.
4. T003, the classic runner, which T002's ruling is the prerequisite for.
5. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   STATUS line and the PR.

## Risks

- The open set is 88 by distinct id at this round's base `c370dcee`, computed mechanically
  from the record. This round registers one and resolves one, leaving 88. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per DECISION
  F272 D12.
- The allowlist is the first mechanism in this feature that lets a known defect sit on disk
  under a green suite. It is bounded by two assertions rather than by intent: it may not
  grow, and it may not keep an entry whose advertisement is gone.
<<<END PLAN27>>>

──────── LEDGER27 — appended to `.agent/live_review.md` ────────

Four paragraphs, blank-line separated, in this order. The header of the first was
compared mechanically against the `^Gate: F275 R` headers already in the file (§3
item 26) and follows their shape.

<<<BEGIN LEDGER27>>>
Gate: F275 R26 — the F275 round 26 entry. VERDICT PASS, written by the planner and reviewer of session 13 after reading the committed range `684b1b55`..`319b8777` and RE-RUNNING EVERY GATE INDEPENDENTLY against the committed blobs, and booked here by round 27 rather than by a round of its own, per operator amendment amend0827-process-diet rule 1, carried from the pushed `.agent/handoff.md` at `c370dcee`. The worker's report was evidence for no line of it. Seven single-parent commits C0a `a517f769`, C0b `79dd47f4`, C1 `9fb92ba0`, C2 `ae50c3b7`, C3 `d0652d43`, C4 `319b8777` and C5 `7701f035`, per-commit insertions 306, 228, 14, 14, 11 and 15 for the six before the handback, every one far under the AGENTS.md DECISION F104 D1 cap of 500. G1 covers the chain this workflow can walk and NOT the emitted bytes, per §3 item 37: the reviewer's scratch original and both committed copies are 29712 bytes at `cf0cac758b2ba9feae85af33883b5615472f97aa1b529c67302f197f37f53725` and compare BYTE-EQUAL. G2: `.agent/plan.md` at C1 is 2237 bytes byte-identical to PLAN26, 41 lines against the cap of 50, both mandated headings exactly once. G3 over both append targets: `.agent/live_review.md` 745098 to 755015 and `.agent/prose_slips.md` 209425 to 211596, each post-blob equal to pre plus ONE newline plus the slice as extracted, the joining byte READ BACK at offset len(pre) reading a newline in both, and the structural reader counting N from each slice — 4 and 3 paragraphs — and matching the last N blank-line units IN ORDER. THE OPEN SET FELL 90 TO 88 BY DISTINCT ID over 100 registrations against 12 resolutions, correct for a round that registers nothing and resolves two. G4 IS THE GATE THAT ROUND EXISTED TO PASS: over `docs/roadmap/features/T2_F267.md` the reviewer's own sweep read `24`, `fifteen` and `nine` at ZERO, the five deleted command ids at exactly one occurrence each and every one INSIDE the blockquote round 25 added, and `four` at exactly the four places the block named in advance, every one a sentence about the DECISION F262 D4 exclusions rather than a live claim — R-0869's split-sweep clause working as designed for the second round running. G5 and G6: `12 groups` at lines 2928 and 2972 and `twelve` at 2914 and 2977, all four BENEATH the `## Group-first CLI v0` heading at line 2908, with the outside set EMPTY, and each banner one blank line below its heading. G7: the shipped catalog UNCHANGED at 222 commands and 44 groups with ZERO dangling `related=` references, `tests/docs/` and `tests/cli/test_product_spine.py` green at 368 passed and the canary at 42, no `.agent/STOP`, porcelain EMPTY, ONE worktree, and `684b1b55..319b8777` an EXACT set match over the seven change-set paths. THE WORKER'S OWN END-TO-END SWEEP PRODUCED THE BEST FINDING OF THAT SESSION and the reviewer sustains both declared deviations after measuring each itself: the banner the reviewer wrote advertised `remedy list`, which no group and no catalog id has ever carried, and dated its section "Steps 38 to 43" while that section is the last `##` heading in the file and carries subsections for Steps 48, 50, 51, 52 and 53. Both are repaired by round 27 at C3, and neither changes this verdict, because every gate the block ordered was run and returned a true reading and the round's change set is exactly what it declared. NO FINDING IS RESOLVED BY THIS GATE.

Note: F275 R27 — new evidence for the OPEN finding R-0847, added rather than given an id of its own per `docs/agents/planner_reviewer_prompt.md` §3 item 30, and it is the sharper form of that finding rather than another instance of it. R-0847 records that `tests/cli/test_advertised_commands.py` cannot see an advertisement whose command GROUP has been deleted, and its measured cause was the scanner's group pre-filter. THE SCANNER IS BLIND THREE WAYS, not one, and only the first was on the record. SECOND, found by the WORKER of round 26 and re-measured by the reviewer at `c370dcee`: the scanner matches a TWO-TOKEN form, `remedy <group> <subcommand>`, so it is structurally blind to a SINGLE-TOKEN invocation `remedy <something>` no matter which groups exist. THIRD, found by the reviewer of session 14 while APPLYING the widening in a disposable worktree before authoring it: `_COMMAND_TAIL_CHARS` holds `<`, `{`, `"` and `'` and NOT the BACKTICK, while a markdown page closes an inline command with a backtick — so adding that one character to the tail set raises the advertisements the shipped scanner SEES from 641 to 791 across the same corpora, 150 of which were never scanned at all. THE INSTANCE THAT PROVES THE SECOND, and it is the reviewer's own: `docs/system/architecture.md` line 2916 instructed a reader to "run `remedy list`". Measured through the shipped dispatcher rather than by grep — `apps.cli.grouped.main(["list"])` exits 2 on `Error: Unknown command 'list'.` against a control `main(["worker"])` at exit 0 — and through the shipped catalog: no `list` group among the 44, no `list.*` id among the 222, and `git log -S` finding no commit that ever added one. So it was never a deletion residue; it was a command that never existed, written into a status banner by the reviewer of round 25 at `9cf79a08` while repairing R-0843, a finding about pages advertising commands that cannot run. A SECOND DEFECT IN THE SAME BANNER: it dated the section "Steps 38 to 43" while `## Group-first CLI v0` is the LAST `##` heading in the file, which ends at line 3072 and carries subsections naming Steps 41 to 43, 48, 50, 51, 52 and 53 — so the date was true of less than it covered, the opposite failure to the one the banner was written to fix. ALL OF IT IS REPAIRED BY ROUND 27, whose C3 rewrites the banner and whose C4 widens the scanner in all three directions. AND THE LESSON THAT OUTLIVES THE INSTANCE: a repair for a dead-advertisement finding is itself swept for dead advertisements before it lands, through the shipped dispatcher and not by eye, because the reviewer writing the fix is the reader least likely to doubt the command it recommends.

- R-0872 — Medium, FORTY-THREE DEAD ADVERTISEMENTS STAND ON OPERATOR-FACING PAGES, EVERY ONE OF THEM HIDDEN UNTIL ROUND 27 WIDENED THE SCANNER, AND THEY ARE HELD BY A RATCHET RATHER THAN REPAIRED IN THE ROUND THAT REVEALED THEM. Raised by the reviewer of session 14 at `c370dcee` by APPLYING the R-0847 widening in a disposable worktree and reading what it reported, before authoring the round that ships it. THE MEASUREMENT, taken through the widened scanner's own functions: the operator-facing corpus — `scripts/**.sh`, `docs/system/**.md`, `docs/guides/**.md` — reads 417 advertisements seen and 68 unresolved sites over 43 DISTINCT `(path, invocation)` keys across 7 paths, against 0 unresolved for the same corpus under the shipped scanner. Every one was probed: all 24 distinct single-token invocations exit 2 through `apps.cli.grouped.main`, against controls `remedy worker` and `remedy job` at exit 0 with 1025 and 2727 bytes of help, so the probe distinguishes live from dead. THE SEVEN PATHS AND WHAT EACH IS. Four are DYING PAGES documenting command groups F275 deleted whole and carrying 16 keys between them — `docs/guides/dogfood-run-user-guide.md` 6, `docs/guides/self-repair-proposal-user-guide-v0.md` 7, `docs/system/feature-planner-v0.md` 2, `docs/system/progress-ledger-v1.md` 1 — and their repair is DELETION, with the `docs/README.md` index entry and every inbound cross-link going in the same commit. One is a LIVE page needing surgery, `docs/system/core-product-spine-v0.md` at 5 keys, all naming the deleted `self-repair` group. `docs/system/architecture.md` carries 21, every one a flat pre-Step-38 command inside a section the page itself dates as a historical snapshot; `docs/system/vocabulary.md` carries the last, `remedy absorb`. WHY MEDIUM AND NOT HIGH: nothing false is claimed about what Remedy can DO, and no production code path is wrong — round 27 repaired all eight production sites and the production sweep reads ZERO unresolved at 542 seen. It is not Low because an operator reading a guide end to end is told to run six commands that cannot run, and because a page whose whole subject is a deleted capability is worse than a stale sentence. WHY IT IS NOT REPAIRED IN ROUND 27: the widening is a change to a guard and the repair is a set of page deletions, and AGENTS.md Commit Discipline forbids mixing a refactor with deletions in one commit; landing them together would also put four page deletions and a scanner rewrite in one reviewable round. THE CARRIER IS A RATCHET, in the sense DECISION F274 D1 gave the word, and it is deliberately not a suppression: `KNOWN_DEAD_DOC_ADVERTISEMENTS` names all 43 keys explicitly, `test_the_known_dead_doc_advertisement_list_only_ever_shrinks` fails if the set GROWS past `_ALLOWLIST_CEILING` and fails if it keeps an entry whose advertisement is GONE, and both halves were proved to bite by mutation at round 27's G6. A new dead advertisement anywhere in either corpus goes red immediately, because only these 43 keys are excused. THE FIX CLAUSE, binding on the next two rounds of this feature: the first deletes the four dying pages and repairs `core-product-spine-v0.md`, lowering the allowlist to 22 and `_ALLOWLIST_CEILING` with it in the same commit; the second repairs `architecture.md` and `vocabulary.md`, lowering it to ZERO, and DELETES `KNOWN_DEAD_DOC_ADVERTISEMENTS`, `_ALLOWLIST_CEILING` and the ratchet test in that same commit, because a ratchet at zero is a gate that cannot fail. This finding is not resolved while any entry remains.

Done: R-0847 — RESOLVED at F275 round 27, by the commit constraint 4 of that round's block orders, which fixes C4 as the commit landing the scanner change one commit after this paragraph is written; the reading below is the reviewer's own, taken by APPLYING the change in a disposable worktree at `c370dcee` before the round was delegated. THE FINDING'S OWN FIX CLAUSE HAD TWO HALVES AND BOTH ARE DISCHARGED. FIRST, "resolves the pair against the catalog without the group pre-filter and narrows false positives by the existing command-tail rule instead" — done exactly as written: `if group not in GROUPS: continue` is gone from `scan_advertised_commands`, resolution moves to a new `_resolves` against the live catalog, and the tail rule is what keeps prose out. The widening went further than the clause asked, because applying it exposed two further blindnesses the clause did not know about: the single-token form and the missing backtick in the tail set, both recorded in the `Note: F275 R27` entry above. SECOND, "the same round deletes the `remedy feature plan --agent --json` return at `worker_registry.py` line 710 together with the `via the feature planner` clause in `_worker_next_action`'s docstring" — DISCHARGED BY DELETION rather than by edit, and measured rather than assumed: `packages/orchestration/worker_registry.py` was removed whole at `1abe8ac2`, F275 round 20's C4, and a repo-wide `git grep` for `_worker_next_action` and for `via the feature planner` over `packages apps tests scripts docs` returns NOTHING at `c370dcee`. WHAT THE RESOLUTION IS WORTH, measured and not asserted: the PRODUCTION corpus now reads 542 advertisements seen and ZERO unresolved, under a scanner with no group pre-filter, both token forms and the backtick tail — where the shipped scanner read 0 unresolved by being blind to eight of them. All eight are repaired in the same commit, each a next-action string naming a flat command the Steps 38-40 restructure replaced: `remedy timeline` becomes `remedy brain timeline` at three sites, `remedy agent-loop` becomes `remedy dev agent-loop` at two, `remedy constitution` becomes `remedy brain constitution` at two, and `remedy workers` becomes `remedy worker list`. THE CLAUSE THIS RESOLUTION LIFTS, and the precise limit of the lift: R-0847 forbade any deletion round to cite a green `test_advertised_commands.py` as evidence that its own dead advertisements are gone. For PRODUCTION CODE that restriction is lifted — the sweep is now honest there and a green production test means what it says. For the OPERATOR-FACING corpus it is NOT lifted and must not be read as lifted: 43 known dead advertisements are excused by name in `KNOWN_DEAD_DOC_ADVERTISEMENTS`, so a green operator-facing test means "no dead advertisement OUTSIDE those 43", and the residue is registered as R-0872 with a fix clause binding the next two rounds. The blindness is gone; the backlog it was hiding is now visible, counted and ratcheted.
<<<END LEDGER27>>>

──────── SLIPS27 — appended to `.agent/prose_slips.md` ────────

Three paragraphs, blank-line separated. They are session 13's, drafted in the
handback at `c370dcee` and booked here by the round that is happening anyway.

<<<BEGIN SLIPS27>>>
2026-09-10 · F275 R25 · The round 25 block's S7 slice told a reader to "run `remedy list`" inside a status banner whose whole purpose was to stop a page advertising commands that cannot run. The reviewer wrote the recommendation from memory of what a catalog reader ought to be called, never probed it, and the round 26 block then carried the same clause into U4 without re-probing it either — so one invented command survived two rounds of a session whose subject was dead advertisements. The lesson is that any command a reviewer types into an authored slice is executed through the shipped dispatcher before emission, exactly as a numeral is re-derived, because a command name is a claim about the product and not a turn of phrase.

2026-09-10 · F275 R26 · The round 26 block's constraint 8 declared U4 an APPEND on the reasoning that it inserts a banner between a heading and the paragraph under it and therefore keeps its whole FROM. The mechanical containment test the same checklist item requires reported `TO contains FROM: false`, because the inserted banner separates the FROM's blank line from its second line, and the constraint and the gate were both corrected before emission. Nothing landed wrong. It is recorded because the eye and the test disagreed on the pair shape this repository most often gets wrong, and the eye was confident: §3 item 15's instruction to classify by test and never by eye earned its place again, in a block written by a reviewer who had just quoted it.

2026-09-10 · F275 R23-R26 · Session 13 ran four delegated rounds and every one of them shipped a block whose authored text carried a defect the WORKER found rather than the reviewer: a gate naming a digest the block did not carry, a universal about a file's separators that fourteen entries falsify, a pair whose FROM stopped one line short of the numeral it existed to remove, a banner at the wrong granularity, and a banner recommending a command that does not exist. Every round still passed on its measured gates, and the product state each one left is correct. The lesson is about rate rather than about any one slip: four rounds produced eleven dated slips, which is the signal `docs/agents/self_drive_protocol.md` G7 as amended by amend0905-throughput names as an honest reason to end a session, and session 13 ended on it rather than writing a fifth block at the same rate.
<<<END SLIPS27>>>

Done when — the gates below, G1 to G8, which is the maximum the amend0827
rule 5 gate budget allows. Each is run with
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, real exit codes and real numbers in the
handback, ONE LINE PER GATE. G1 through G7 are ordered at commits strictly before
C5, per §3 item 31.

G1 TRANSPORT (at C0b). `sha256sum` of the scratch original, of the committed
   `a-blob` `.agent/authored/f275-r27.md` and of the committed `.agent/last_block.md`
   are ONE comparison and must be equal. State that this covers the saved copy, its
   mirror and the working copy, and NOT the emitted bytes (§3 item 37).

G2 THE PLAN (at C1). `.agent/plan.md` byte-identical to the PLAN27 slice; report
   `written == slice`. Line count under the AGENTS.md cap of 50. `grep -c '^## Goal$'`
   and `grep -c '^## Next Steps$'` both 1.

G3 THE RECORD (at C2), full byte forensics, both append targets. For each of
   `.agent/live_review.md` (pre 755015 bytes) and `.agent/prose_slips.md` (pre
   211596 bytes): post == pre + ONE newline + slice, with the joining byte READ BACK
   from the committed post-blob at offset len(pre) and shown to be `\n`; plus an
   INDEPENDENT structural reader comparing the LAST N blank-line units of the whole
   post-file against the slice's N paragraphs IN ORDER, N COUNTED BY THE SCRIPT from
   the slice and never taken from this block; plus a negative control flipping one
   byte inside the FIRST appended paragraph of each file, which BOTH readers must
   REJECT while both accept the truth. Then whole-post-file counts: `^Gate: F275 R26 `
   == 1, `^Note: F275 R27 ` == 1, `^- R-0872 — ` == 1, `^Done: R-0847 — ` == 1.
   Then THE OPEN SET BY DISTINCT ID, computed mechanically as every distinct
   `^- R-\d+ — ` id minus every distinct `^Done: R-\d+ — ` id, reporting both counts
   and any resolution naming an unregistered id. It reads 88 at the base `c370dcee`
   over 100 distinct registrations against 12 distinct resolutions; this commit
   registers one and resolves one, so it must read 88 again. Report the DISTINCT
   resolution count beside the LINE count: the record carries 14 `Done:` lines for 12
   ids, because `R-0721` and `R-0725` each carry two, which is landed state this round
   does not touch.

G4 THE DOC PAIR (at C3). U1 and U2 each FROM 1 -> 0 and TO 0 -> 1, measured before
   and after the write, with the per-slice sha256 and byte length of all four texts
   as EXTRACTED from the committed block blob. Then over the whole file, TWO readings
   of the invented command and not one, because the bare substring cannot reach zero
   and a filter used as a measurement must print its own count:
     (a) the BACKTICK-DELIMITED form, the three words `remedy list` wrapped in
         backticks, must be 0. It reads 1 at `c370dcee` and U1 removes exactly it.
     (b) the RAW substring `remedy list` must be 2, NOT 0, and every hit is printed
         with its line number. It reads 3 at `c370dcee`: line 675
         `remedy list-patch-intents`, line 1897 `remedy list-projects`, and line 2916
         the clause U1 removes. The first two are flat pre-Step-38 commands that merely
         BEGIN with the same eleven characters; they are R-0872's, not this round's,
         and a gate stated as a bare zero here would be unmeetable by every possible
         round. If (b) reads anything other than 2, stop and report.
   Then `Steps 38 to 43` == 0 over the whole file. Print `^## Group-first CLI v0` with
   its line number and the file's total line count, and confirm the first `^> ` after
   that heading is separated from it by exactly one blank line.

G5 THE GUARD (at C4), through the WORKER's OWN import of the edited module, not by
   grep. Report: the production sweep's `seen` and `unresolved` — unresolved MUST be
   0 and `seen` must exceed 100; the operator-facing sweep's `seen`, its `unresolved`
   count and its DISTINCT key count; `len(KNOWN_DEAD_DOC_ADVERTISEMENTS)` and
   `_ALLOWLIST_CEILING`, which must be EQUAL. Then the allowlist DIGEST: sha256 over
   the sorted keys joined as `f"{path}\t{invocation}"` lines separated by `\n`, with
   no trailing newline, which must read
   `364eb51c60942c14da584ce3a822a555b737c36cf54b5027d13f03586dcd64c0`. Then
   `python3 -m pytest tests/cli/test_advertised_commands.py -q` at exit 0.

G6 THE RED PROOFS (after C4, inside a disposable worktree at the C4 commit, per
   constraint 7). Run the UNMUTATED control FIRST and report its exit code and count.
   Then FOUR mutations, one at a time, each reverted byte-exactly before the next,
   each reported with the mutated exit code:
     M1 restore `, or run \`remedy list\`,` into the U1 TO sentence in
        `docs/system/architecture.md` -> the operator-facing test must go RED.
     M2 restore P1's FROM in `packages/orchestration/cockpit.py` -> the production
        test must go RED.
     M3 add one entry to `KNOWN_DEAD_DOC_ADVERTISEMENTS` -> the ratchet test must go
        RED on the ceiling.
     M4 add an allowlist entry naming an advertisement that does NOT occur -> the
        ratchet test must go RED on staleness.
   Then re-run the control and prove every mutated file is restored BYTE-EXACTLY by
   comparing against bytes captured before the first mutation. A mutation that comes
   back GREEN is a finding, not a pass: report the colour, never assume it.

G7 THE PRODUCTION PAIRS (at C4). P1 through P8 each FROM 1 -> 0 and TO 0 -> 1,
   measured before and after the write. Then, through the SHIPPED dispatcher and in
   process, probe `remedy brain timeline`, `remedy dev agent-loop`,
   `remedy brain constitution` and `remedy worker list` with NO `--help`, reporting
   each exit code and its first output line; and probe the CONTROL `remedy timeline`
   the same way. The four replacements must print their own command in the usage line
   or succeed; the control must not. Then `ruff check` over the four edited Python
   files, reporting the real message.

G8 NOTHING ELSE MOVED (at C4, before C5).
   - `python3 -m pytest tests/docs/ tests/cli/ tests/test_timeline.py
     tests/test_project_constitution.py tests/test_agent_loop.py tests/test_cockpit.py
     tests/test_trust_report.py tests/test_brain_detail.py -q` — report passed/failed.
     The canary `tests/cli/test_golden_path.py` is inside `tests/cli/`; say so.
   - Through the shipped reader `apps.cli.command_catalog`: `len(_BASE_CATALOG)`,
     `len(GROUPS)` and the count of dangling `related=` references. They read 222, 44
     and 0 at `c370dcee` and must be unchanged, because this round adds and deletes
     no command.
   - `.agent/STOP` absent (from disk), `git status --porcelain` EMPTY,
     `git worktree list` exactly ONE entry, branch
     `feature/f275-one-world-completion-part-three`.
   - `git diff --name-only c370dcee..<C4>` an EXACT SET MATCH against the change set
     above minus `.agent/handoff.md`; report MISSING and EXTRA explicitly.
   - Per-commit insertions for every commit BEFORE the handback commit, each against
     the AGENTS.md DECISION F104 D1 cap of 500 (§3 item 14: the handback commit's own
     number is not reachable here and belongs to the next round's ledger entry).

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md — feature
and round, SESSION 14 of F275, branch, per-commit changed-files table with `+/-`
transcribed cell by cell from `git show --numstat` (§3 item 28), one line per gate
with real exit codes, the item-status table covering C0a..C5, U1, U2, P1..P8, G1..G8,
R-0847 and R-0872, every deviation declared, the open-findings count, and the next
expected action. It has NO length cap (amend0827 rule 3). Push the branch. Create NO
pull request: F275's closure sequence is not this round.

(The rule line below is exactly 56 characters, per §3 item 37.)
────────────────────────────────────────────────────────
