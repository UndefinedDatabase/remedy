── STEP T001 (documentary remainder) — F275 — ROUND 28 ──
(The rule line above and the one at the end are each exactly 56 characters, per §3 item 37.)

Goal: Delete the pages that document capabilities F275 has already deleted, and
lower the R-0872 ratchet by the advertisements those pages carried. Five tracked
pages under `docs/` are about mechanisms whose modules are gone: the feature
planner, the progress ledger, the dogfood run loop, the self-repair proposal
guide and the run-replay-to-self-repair-proposal design. Four of them were found
by round 27's widened advertisement sweep; the FIFTH carries no `remedy <x>`
string at all and was found only by reading the CAPABILITY, which is the limit of
an advertisement sweep and the reason this round also registers R-0873.

Every one of the five has its inheritance already ruled, so this round decides
nothing and cites what is on the record: DECISION F260 D3 in `.agent/decisions.md`
routes `self_repair_proposal.py` to F017's approval gate, `progress_ledger.py` to
`job show --full` and `job evidence`, and `dogfood_run.py` to NONE, deliberately;
DECISION F274 D6 routes `feature_planner.py` to NONE. AGENTS.md Scope Control
("Replacing is deleting… there is no attic") is what makes deletion the repair.

Bundle, in commit order:
  C0a  save this block verbatim to `.agent/authored/f275-r28.md`
  C0b  mirror the COMMITTED C0a blob into `.agent/last_block.md`
  C1   `.agent/plan.md` <- PLAN28
  C2   the record: LEDGER28 into `.agent/live_review.md`, SLIPS28 into
       `.agent/prose_slips.md`
  C3   delete the five pages, drop their rows from the docs index, and remove the
       SIXTEEN allowlist entries those pages carried, ceiling 43 -> 27
  C4   the spine page's dead section, and the FIVE allowlist entries it carried,
       ceiling 27 -> 22
  C5   the handback

Change set — exactly these paths, nothing else:
  .agent/authored/f275-r28.md               (C0a, new file)
  .agent/last_block.md                      (C0b)
  .agent/plan.md                            (C1)
  .agent/live_review.md                     (C2, append)
  .agent/prose_slips.md                     (C2, append)
  docs/system/feature-planner-v0.md         (C3, DELETED)
  docs/system/progress-ledger-v1.md         (C3, DELETED)
  docs/guides/dogfood-run-user-guide.md     (C3, DELETED)
  docs/guides/self-repair-proposal-user-guide-v0.md      (C3, DELETED)
  docs/system/run-replay-to-self-repair-proposal-v0.md   (C3, DELETED)
  docs/README.md                            (C3)
  tests/cli/test_advertised_commands.py     (C3 and C4)
  docs/system/core-product-spine-v0.md      (C4)
  .agent/handoff.md                         (C5)

Constraints:
 1. Every slice below is applied BYTE FOR BYTE. If a slice looks wrong, apply it
    anyway and DECLARE the doubt in the handback. Never repair a reviewer slice.
 2. Marker lines `<<<BEGIN ...>>>` / `<<<END ...>>>` never reach a target file.
    Extract each slice from the COMMITTED C0a blob, never from a retype.
 3. THIS BLOCK CARRIES NO FROM/TO PAIR. S1 and S2 are both DELETIONS: text is
    removed and nothing replaces it. So the containment test §3 item 15 requires
    for a pair does not apply to either, no APPEND-or-REWRITE label is claimed for
    either, and NO "TO 0x -> 1x" count is ordered anywhere in this round — such a
    count would be unattainable by construction and inviting it is how a fabricated
    number gets into the record. The proof for a deletion is one-sided and is
    stated as such: each removed unit occurs EXACTLY ONCE before the write and
    ZERO times after it, measured both times. The allowlist entries C3 and C4
    remove are deletions of the same kind and are proved the same way.
 4. THE RATCHET MAY NOT GO STALE AT ANY COMMIT. `test_the_known_dead_doc_
    advertisement_list_only_ever_shrinks` fails on an allowlist entry whose
    advertisement no longer occurs, so each commit that removes advertisements
    removes their allowlist entries and lowers `_ALLOWLIST_CEILING` IN THE SAME
    COMMIT. That is why C3 and C4 both touch the guard file, and it is the ratchet
    doing its job rather than a change set that drifted.
 5. Deletions use `git rm`. No page is emptied, stubbed, redirected or replaced by
    a tombstone: AGENTS.md Scope Control forbids an attic and git is the archive.
 6. `.agent/STOP` is re-read FROM DISK before the FIRST commit and again before C3.
 7. Commit subjects carry NO leading-slash token, absolute path or secret-like
    string. C3's and C4's subjects name R-0872.
 8. No file outside the change set is edited, and no test is deleted, skipped or
    weakened to make a gate green. In particular `tests/cli/test_product_spine.py`
    pins that `core-product-spine-v0.md` EXISTS — C4 edits that page, never deletes
    it.
 9. `docs/README.md` is edited by dropping WHOLE ROWS. The reviewer measured that
    the five pages own SIX index rows, because `dogfood-run-user-guide.md` is
    listed twice: once in the quick-find table and once in the guides table.
10. Do not re-verify round 27's production sweep or its red proofs; both were
    measured at `d3e35f0f` and hold.

──────── WHAT THE REVIEWER ALREADY MEASURED, by APPLYING all of it ────────

All of the following was applied in a disposable worktree at `d3e35f0f` and RUN.
These are the numbers the gates re-derive, not predictions.

The five pages are 60, 77, 97, 91 and 111 lines. `docs/README.md` falls from 204
to 198 lines, losing exactly six rows. `core-product-spine-v0.md` loses one
`## What self-repair proposals are` section and one command-taxonomy row, after
which the page holds ZERO occurrences of the string `self-repair`. The
operator-facing sweep falls from 417 seen / 68 unresolved / 43 distinct keys
to 387 / 38 / 22, and the 22 that remain are 21 in `docs/system/architecture.md`
and 1 in `docs/system/vocabulary.md` — TWO paths, which is the whole of R-0872's
second half. The production sweep is UNCHANGED at 542 seen and ZERO unresolved.
`tests/docs/`, `tests/cli/test_advertised_commands.py` and
`tests/cli/test_product_spine.py` are green together at 374 passed, and the wider
`tests/docs/ tests/cli/` is green at 1649 passed.

The inbound-link sweep, run over `docs/ tests/ scripts/ packages/ apps/`: the five
pages are named ONLY by their own `docs/README.md` rows and by the allowlist
entries C3 removes. Nothing else links to any of them, so no cross-link repair is
owed and none is ordered.

──────── S1 — the docs index rows to drop ────────

Drop these SIX whole lines from `docs/README.md`. Each occurs exactly once; the
reviewer measured each count at `d3e35f0f`. Match on the full line, not on a
substring, and do not renumber or reflow the tables around them.

<<<BEGIN S1 ROWS>>>
| dogfood | [dogfood-run-user-guide.md](guides/dogfood-run-user-guide.md) | guide |
| [feature-planner-v0.md](system/feature-planner-v0.md) | Feature planning and decomposition |
| [progress-ledger-v1.md](system/progress-ledger-v1.md) | Progress ledger for tracking feature/task state |
| [run-replay-to-self-repair-proposal-v0.md](system/run-replay-to-self-repair-proposal-v0.md) | Replay analysis to self-repair proposal pipeline |
| [dogfood-run-user-guide.md](guides/dogfood-run-user-guide.md) | Running dogfood jobs *(overnight superseded)* |
| [self-repair-proposal-user-guide-v0.md](guides/self-repair-proposal-user-guide-v0.md) | Self-repair proposal workflow |
<<<END S1 ROWS>>>

All six rows above were read from `docs/README.md` at `d3e35f0f` and each occurs
exactly once as a whole line; the reviewer measured every count. Report the six
lines you actually removed in the handback, so the removal is proved against the
file rather than against this block.

──────── S2 — the spine page's dead section ────────

S2 is a DELETION: this FROM is removed and nothing replaces it. It occurs exactly
once in `docs/system/core-product-spine-v0.md`. Remove the trailing blank line
with it, so the heading that follows keeps exactly one blank line above it.

<<<BEGIN S2 FROM>>>
## What self-repair proposals are

Self-repair proposals are structured suggestions for improvements that
Remedy generates based on its own evidence. They are metadata records, not
executed actions.

An operator can:
- List proposals: `remedy self-repair proposal-list --json`
- Approve a proposal: `remedy self-repair proposal-approve <id> --json`
- Deny a proposal: `remedy self-repair proposal-deny <id> --json`
- Edit a proposal: `remedy self-repair proposal-edit <id> --json`
- Convert to worker prompt: `remedy self-repair worker-prompt <id> --json`

Converting to a worker prompt creates a safe, bounded prompt for the operator
to give to a worker. The proposal itself never executes anything.

<<<END S2 FROM>>>

Also at C4, remove this single command-taxonomy row, which occurs exactly once:

<<<BEGIN S2 ROW>>>
| `self-repair *` | Self-repair proposals | Development-time |
<<<END S2 ROW>>>

──────── The allowlist entries to remove ────────

At C3 remove the SIXTEEN entries whose path is one of the five deleted pages —
six for `dogfood-run-user-guide.md`, seven for
`self-repair-proposal-user-guide-v0.md`, two for `feature-planner-v0.md`, one for
`progress-ledger-v1.md`, and none for `run-replay-to-self-repair-proposal-v0.md`,
which carried no advertisement. Set `_ALLOWLIST_CEILING = 27` in the same commit.

At C4 remove the FIVE entries whose path is `docs/system/core-product-spine-v0.md`
and set `_ALLOWLIST_CEILING = 22` in the same commit.

Do not retype the surviving entries and do not reorder them: remove whole lines
and leave every other line byte-identical. G5 gates the survivors by digest.

──────── PLAN28 — the whole of `.agent/plan.md` ────────

<<<BEGIN PLAN28>>>
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 28 deletes the five pages that document capabilities F275 already deleted — the feature
planner, the progress ledger, the dogfood run loop, and the two self-repair proposal pages —
drops their six rows from the docs index, and cuts the dead self-repair section out of the
core product spine. The R-0872 ratchet falls from 43 to 22 in two steps, one per commit, and
what remains is exactly the flat pre-Step-38 CLI in `architecture.md` plus one site in
`vocabulary.md`. R-0873 registers the wider residue an advertisement sweep cannot see.

## Next Steps

1. R-0872's second half: the flat pre-Step-38 CLI in `architecture.md` and the one site in
   `vocabulary.md`, lowering the allowlist to zero and deleting the ratchet with it, which
   resolves R-0872.
2. R-0873: read the capability sweep's ranked list and rule, page by page, which pages die
   and which are dated as historical. `docs/archive/` is archival by design and is expected
   to survive the ruling.
3. T002: the DECISION F272 D7 raising-property probe over every candidate `.id` receiver,
   giving the real site set rather than D15's upper bound, then the dated decision choosing
   the route. No production line moves in that slice.
4. T003, the classic runner, which T002's ruling is the prerequisite for.
5. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   STATUS line and the PR.

## Risks

- The open set is 88 by distinct id at this round's base `d3e35f0f`, computed mechanically
  from the record. This round registers one and resolves none, leaving 89. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per DECISION
  F272 D12.
- R-0873 is measured but not scoped: 18 pages name a deleted module's concept, and several
  are `docs/archive/` pages that SHOULD keep describing an abandoned future. The finding
  records the measurement and defers the ruling rather than implying every hit is a defect.
<<<END PLAN28>>>

──────── LEDGER28 — appended to `.agent/live_review.md` ────────

Two paragraphs, blank-line separated. The first header was compared mechanically
against the `^Gate: F275 R` headers already in the file (§3 item 26).

<<<BEGIN LEDGER28>>>
Gate: F275 R27 — the F275 round 27 entry. VERDICT PASS, written by the planner and reviewer of session 14 after reading the committed range `c370dcee`..`d3e35f0f` and RE-RUNNING EVERY GATE INDEPENDENTLY against the committed blobs, and booked here by round 28 rather than by a round of its own, per operator amendment amend0827-process-diet rule 1. The worker's report was evidence for no line of it. EIGHT single-parent commits C0a `4ba30f28`, C0b `c2a5dca7`, C1 `8fe426b3`, C2 `f4390b10`, C3 `088e7e7d`, C4 `3225d876`, C4b `6335babf` and C5 `d3e35f0f`, per-commit insertions 421, 390, 21, 14, 16, 191, 5 and 235, every one under the AGENTS.md DECISION F104 D1 cap of 500. G1 is the PRIMARY §4 item 9 proof and not the digest fallback: the reviewer's own scratch original and both committed copies are 39740 bytes at `08809a29128b5f02856eb00f26cc40499d51f9df3c0ca53dfdd427b369ea2078` and compare BYTE-EQUAL; under self-drive the block travelled as a FILE the worker read at a path, so this chain reaches further than §3 item 37's usual reading, and it still claims nothing about bytes retyped into a prompt, because none were. G2: `.agent/plan.md` byte-identical to PLAN27 at 2476 bytes, 44 lines against the cap of 50, both mandated headings exactly once. G3 over both append targets: `.agent/live_review.md` 755015 to 767596 and `.agent/prose_slips.md` 211596 to 213983, each post-blob equal to pre plus ONE newline plus the slice as extracted, the joining byte READ BACK at offset len(pre) reading a newline in both, the structural reader counting N from each slice — 4 and 3 paragraphs — and matching the last N blank-line units IN ORDER, and both negative controls flipped INSIDE THE FIRST appended paragraph and REJECTED by BOTH readers. `^Gate: F275 R26 `, `^Note: F275 R27 `, `^- R-0872 — ` and `^Done: R-0847 — ` each exactly 1. THE OPEN SET HELD AT 88 BY DISTINCT ID over 101 registrations against 13 resolutions, which is correct for a round that registers one and resolves one. G4: U1 and U2 each FROM 1 to 0 and TO 0 to 1; the BACKTICK-delimited `remedy list` 1 to 0; the RAW substring 3 to 2, the survivors being `remedy list-patch-intents` at line 675 and `remedy list-projects` at line 1897, both flat pre-Step-38 commands that merely begin with the same characters and both R-0872's; `Steps 38 to 43` 1 to 0. G5 THROUGH THE REVIEWER'S OWN IMPORT of the edited guard: the PRODUCTION sweep reads 542 seen and ZERO unresolved, the operator-facing sweep 417 seen, 68 unresolved and 43 distinct keys over 7 paths, `len(KNOWN_DEAD_DOC_ADVERTISEMENTS)` and `_ALLOWLIST_CEILING` both 43, and the allowlist digest is `364eb51c60942c14da584ce3a822a555b737c36cf54b5027d13f03586dcd64c0` as ordered. G6 IS THE GATE THAT MATTERS AND IT WAS RE-RUN IN THE REVIEWER'S OWN DISPOSABLE WORKTREE: the unmutated control is 6 passed, and reinstating the invented `remedy list` in the repaired banner, reinstating a dead advertisement in production code, growing the allowlist and swapping in a non-occurring entry all go RED, with the control green again afterwards and all three mutated files restored byte-exactly. G7: all eight production pairs FROM 1 to 0 and TO 0 to 1, and through the shipped dispatcher `remedy brain timeline`, `remedy dev agent-loop` and `remedy brain constitution` each exit 2 printing THEIR OWN usage line while `remedy worker list` exits 0 printing `Worker Adapters`, against dead controls `remedy timeline`, `remedy workers` and `remedy constitution` which exit 2 printing the PARENT's usage line and never their own; `ruff check` reads `All checks passed!`. G8: 2024 passed at exit 0 with the canary inside `tests/cli/`, the shipped catalog unchanged at 222 commands, 44 groups and ZERO dangling `related=` references, no `.agent/STOP`, porcelain EMPTY, ONE worktree, and `c370dcee..6335babf` an EXACT set match over the ten change-set paths with MISSING and EXTRA both empty. THE WORKER FOUND TWO DEFECTS IN THE REVIEWER'S OWN BLOCK AND BOTH ARE SUSTAINED, and each is why this round is worth more than its diff. FIRST, SPEC-GUARD (g) said `_ALLOWLIST_CEILING` "is its measured length", which the worker implemented as `len(KNOWN_DEAD_DOC_ADVERTISEMENTS)` — a ceiling that moves with what it bounds, so the ratchet assertion could never fail. The worker saw it while PREPARING the red proof rather than while running it, pinned the literal 43 in an extra commit C4b, and declined to amend C4 because guardrail G2 forbids a history rewrite without qualification. That is a gate-that-cannot-fail authored by the reviewer and caught by the worker. SECOND, G6's M4 as ordered could not prove what it named: with the ceiling at 43, ADDING any entry trips the ceiling assertion before staleness is ever reached, and the reviewer re-measured this rather than accepting it — M4 fires `assert 44 <= 43` at line 298, while the worker's added M4b, which SWAPS an entry so the count stays 43, fires `assert not [('docs/system/architecture.md', 'no-such-flat-cmd')]` at line 305. Both ratchet halves are therefore proved to bite, by the worker's repair and not by the reviewer's order. NO FINDING IS RESOLVED BY THIS GATE; R-0847 was resolved by round 27's own C2 and R-0872 registered there.

- R-0873 — Medium, AN ADVERTISEMENT SWEEP CANNOT SEE A PAGE THAT DOCUMENTS A DELETED CAPABILITY WITHOUT SPELLING ONE OF ITS COMMANDS, AND EIGHTEEN PAGES STILL NAME A DELETED MODULE'S CONCEPT. Raised by the reviewer of session 14 while preparing round 28, after noticing that `docs/system/run-replay-to-self-repair-proposal-v0.md` — a page whose entire subject is the self-repair proposal mechanism deleted at `e9944c64`, F275 round 10's C3 — appears in NO advertisement sweep, because it never writes a `remedy <group> <sub>` or `remedy <token>` string. THE STRUCTURAL POINT, and it is the reason this is not folded into R-0872: R-0872 and its ratchet count ADVERTISEMENTS, which is a property of a page's COMMAND STRINGS, while this finding is about a page's SUBJECT, and no widening of a command scanner can reach it. A page can be perfectly free of dead commands and still be entirely about a mechanism that no longer exists. THE MEASUREMENT, taken at `d3e35f0f` by walking `git log --diff-filter=D` over `a5bf8949..HEAD` for every production `.py` F275 deleted — 89 paths reducing to 43 distinct module stems, of which 41 are distinctive rather than English-generic — and sweeping the 99 tracked non-roadmap pages under `docs/` for each stem in its underscored, spaced and hyphenated forms: EIGHTEEN pages hit. Ranked by hit count the worst are `docs/README.md` at 130, `docs/system/self-dogfood-execution-v0.md` at 38, `docs/system/core-product-spine-v0.md` at 36, `docs/system/vocabulary.md` at 35, `docs/system/orchestrator-brain-v0.md` at 23, and `docs/system/development-artifact-boundary-v0.md` and `docs/system/mission-run-loop-morning-report-v0.md` at 21 each. WHY MEDIUM: no production code path is wrong and nothing false is claimed about what Remedy can DO today; the damage is that a reader arriving at one of these pages from the index is told how a mechanism works that has no code behind it. WHAT THIS FINDING DELIBERATELY DOES NOT CLAIM, because the measurement does not support it: that all eighteen are defects. FIVE of the hits are `docs/archive/` pages, which exist to describe abandoned futures and SHOULD go on naming them; several others are live pages carrying a single incidental mention rather than a dead subject; and two stems, `provider` and `progress`, were excluded as English-generic and are reported as excluded rather than silently dropped, so the 41 swept stems are named as a subset and not as the whole. A hit is a CANDIDATE, and the ruling is per page. THE FIX CLAUSE, binding on the round that finishes R-0872: read the ranked list page by page and rule each one — DELETE where the page's subject is a deleted mechanism, DATE with a historical-snapshot banner where the page records what shipped, and LEAVE where the mention is incidental — recording the ruling for the pages that are neither deleted nor dated, so a later reader does not re-derive the same list. Round 28 discharges the five clearest cases ahead of that ruling and this finding carries the rest. It is not resolved while any page whose SUBJECT is a deleted mechanism still stands.
<<<END LEDGER28>>>

──────── SLIPS28 — appended to `.agent/prose_slips.md` ────────

<<<BEGIN SLIPS28>>>
2026-09-10 · F275 R27 · The round 27 block's SPEC-GUARD (g) described `_ALLOWLIST_CEILING` as "its measured length", and the worker reasonably implemented that as `len(KNOWN_DEAD_DOC_ADVERTISEMENTS)` — which makes the ratchet's own assertion unfailable, because the bound moves with the thing it bounds. The worker caught it while preparing the red proof, pinned the literal and declared it. The lesson is that a spec for a GUARD states the property the guard must still be able to FAIL on, not just the value it must hold: "measured length" reads as a derivation, and a derivation is exactly what a ceiling may not be.

2026-09-10 · F275 R27 · The same block's G6 ordered a mutation, M4, to prove the ratchet rejects a STALE allowlist entry, and ordered it as "add an entry naming an advertisement that does not occur". Adding anything raises the count past the ceiling, so the ceiling assertion fires first and the staleness assertion is never reached — the mutation could not distinguish the property it was written for. The worker declared this, added a SWAP mutation that keeps the count constant, and the reviewer re-measured both by reading which assertion line fired rather than by trusting the exit code. The lesson is the one this repository keeps relearning under a new face: a control must isolate the single property it names, and two assertions in one test need two mutations that differ in exactly one of them.
<<<END SLIPS28>>>

Done when — the gates below, G1 to G7, inside the amend0827 rule 5 budget of
eight. Each is run with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, with real exit
codes and real numbers in the handback, ONE LINE PER GATE. G1 to G6 are ordered
at commits strictly before C5, per §3 item 31.

G1 TRANSPORT (at C0b). `sha256sum` of the scratch original at
   `.remedy-wt/f275-r28-block.md`, of the committed `.agent/authored/f275-r28.md`
   and of the committed `.agent/last_block.md` are ONE comparison and must be
   equal. State that this covers the scratch original, the saved copy and the
   mirror, and that the block travelled as a FILE rather than as retyped bytes.

G2 THE PLAN (at C1). `.agent/plan.md` byte-identical to PLAN28; report
   `written == slice`. Line count under the AGENTS.md cap of 50.
   `grep -c '^## Goal$'` and `grep -c '^## Next Steps$'` both 1.

G3 THE RECORD (at C2), full byte forensics, both append targets. For each of
   `.agent/live_review.md` (pre 767596 bytes) and `.agent/prose_slips.md` (pre
   213983 bytes): post == pre + ONE newline + slice, with the joining byte READ
   BACK from the committed post-blob at offset len(pre) and shown to be a newline;
   plus an INDEPENDENT structural reader comparing the LAST N blank-line units of
   the whole post-file against the slice's N paragraphs IN ORDER, N COUNTED BY THE
   SCRIPT from the slice and never taken from this block; plus a negative control
   flipping one byte inside the FIRST appended paragraph of each file, which BOTH
   readers must REJECT while both accept the truth. Then `^Gate: F275 R27 ` == 1
   and `^- R-0873 — ` == 1 over the whole post-file. Then THE OPEN SET BY DISTINCT
   ID, every distinct `^- R-\d+ — ` id minus every distinct `^Done: R-\d+ — ` id,
   reporting both counts and any resolution naming an unregistered id. It reads 88
   at the base `d3e35f0f` over 101 registrations against 13 resolutions; this
   commit registers one and resolves none, so it must read 89.

G4 THE DELETIONS (at C3). `git ls-tree` at C3 for each of the five paths must find
   NOTHING, and each must have existed at `d3e35f0f` — report both readings per
   path, because an absence proves nothing without the presence before it. Then a
   repo-wide sweep, over `docs tests scripts packages apps`, for each of the five
   BASENAMES: the only surviving mentions permitted are inside
   `.agent/` and inside this round's own block; print every hit with its path and
   line, and if any hit falls outside those, STOP and report. Then `docs/README.md`
   line count 204 -> 198 with the six removed rows printed verbatim.

G5 THE RATCHET, at C3 and again at C4, through the WORKER's OWN import of the
   edited module, not by grep. At C3: `len(KNOWN_DEAD_DOC_ADVERTISEMENTS)` == 27,
   `_ALLOWLIST_CEILING` == 27, the two EQUAL, and zero stale entries. At C4: both
   == 22, and the allowlist digest — sha256 over the sorted keys joined as
   `f"{path}\t{invocation}"` lines separated by newlines, no trailing newline —
   must read `7a6b5f4fa5b0ff693acff44b3c181f0b36df05b098d61c08641fb575c96d41d2`.
   Also at C4 report the operator-facing sweep's `seen`, `unresolved` and DISTINCT
   key count, which must read 387, 38 and 22 over exactly TWO paths, and the
   PRODUCTION sweep, which must be UNCHANGED at 542 seen and ZERO unresolved.

G6 THE SPINE PAGE AND THE SUITE (at C4). The S2 section 1 -> 0 and the S2 row
   1 -> 0, each measured before and after the write, one-sided per constraint 3;
   then `self-repair` == 0 over the whole page, and the page still EXISTS. Then
   `python3 -m pytest tests/docs/ tests/cli/ -q` run SERIALLY — report passed and
   failed; the canary `tests/cli/test_golden_path.py` is inside `tests/cli/`, say
   so. A red suite here is a STOP, not a gate to force.

G7 NOTHING ELSE MOVED (at C4, before C5).
   - Through the shipped reader `apps.cli.command_catalog`: `len(_BASE_CATALOG)`,
     `len(GROUPS)` and the count of dangling `related=` references. They read 222,
     44 and 0 at `d3e35f0f` and must be unchanged, because this round adds and
     deletes no command.
   - `.agent/STOP` absent (from disk), `git status --porcelain` EMPTY,
     `git worktree list` exactly ONE entry, branch
     `feature/f275-one-world-completion-part-three`.
   - `git diff --name-only d3e35f0f..<C4>` an EXACT SET MATCH against the change
     set above minus `.agent/handoff.md`; report MISSING and EXTRA explicitly.
   - Per-commit insertions for every commit BEFORE the handback commit, each
     against the DECISION F104 D1 cap of 500. Deletions carry no insertions, so C3
     is expected to be small; report what you measure rather than what is expected.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md — feature
and round, SESSION 14 of F275, branch, per-commit changed-files table with `+/-`
transcribed cell by cell from `git show --numstat` (§3 item 28), one line per gate
with real exit codes, the item-status table covering C0a..C5, S1, S2, G1..G7,
R-0872 and R-0873, every deviation declared, the open-findings count, and the next
expected action. It has NO length cap. Push the branch. Create NO pull request.

────────────────────────────────────────────────────────
