# STEP R4/F258 — T001 PART 3: WIRE THE GENERATOR INTO THE CLOSURE PROTOCOL'S OWN TEXT

Goal: `packages/orchestration/self_use_generator.py` exists and is tested
(round 3), but nothing in the protocol's own words tells a future closure
round to call it. This round is docs-and-prose only: it updates
`docs/roadmap/STATUS_closure_protocol.md` precondition 6 to name the
generator as the step before "the track is exhausted," and corrects the two
places that still claim the whole system "does not discover, generate or
infer queue items" now that one module — a DIFFERENT module from the
read-only loader — does. This round also books round 3's verdict, per
amend0827 rule 1.

Base: `4c1a1495`, round 3's handback commit and the tip of
`feature/f258-self-use-v2`. Stay on that branch. Open no pull request.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f258-r4.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN4
- C2  append slice RECORD4 to `.agent/live_review.md`
- C3  apply pair PAIR-STATUSPROTO to `docs/roadmap/STATUS_closure_protocol.md`
- C4  apply pairs PAIR-BANNER and PAIR-ABSENCESDOC to `docs/system/self-use-track-v1.md`
- C5  apply pair PAIR-ABSENCESMODULE to `packages/orchestration/self_use_queue.py`
- C6  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f258-r4.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    docs/roadmap/STATUS_closure_protocol.md
    docs/system/self-use-track-v1.md
    packages/orchestration/self_use_queue.py
    .agent/handoff.md

`.agent/context.md` is NOT touched. No file under `apps/` or `tests/`
changes — this round edits PROSE ONLY, in exactly four places across three
files; `self_use_generator.py`'s own behaviour, `self_use_queue.py`'s
behaviour, and every test are UNCHANGED (only `self_use_queue.py`'s
docstring moves; check the diff yourself and confirm zero non-comment,
non-docstring lines changed in it before committing).

## Constraints

1. Apply PLAN4, RECORD4 and all four pairs BYTE FOR BYTE / by the exact
   FROM/TO replace method (assert `text.count(FROM) == 1`, then
   `text.replace(FROM, TO, 1)`, then write back, report before/after
   counts). If any of them looks wrong, apply it as given and declare the
   problem in the handback's deviations.
2. C0a is a COPY, never a retype: the block is at
   `.remedy-wt/f258-r4-block.md`. Use `shutil.copyfile` for C0a and again for
   C0b. This block is small (well under 500 lines); no oversize-commit
   exception is expected or needed this round.
3. C1 is the FIRST substantive commit, ahead of C2, per AGENTS.md's Commit
   Gate.
4. `.agent/live_review.md` is APPEND-ONLY. C2 appends RECORD4 (ONE paragraph
   this round — round 3's own verdict; round 3 minted no pending finding
   beyond that) and revises NOTHING already there.
5. WHEN YOU EXTRACT PLAN4 AND RECORD4 FROM THIS BLOCK, PRESERVE THE FINAL
   TRAILING NEWLINE OF EACH SLICE EXACTLY. Round 3's equivalent commits
   (`002dbf7e`, `8471db8f`) each dropped the slice's own final `\n` byte —
   confirmed by the reviewer independently re-measuring both committed files
   against the block's own PLAN3/RECORD3 bytes. It was harmless there
   (`.agent/plan.md` is fully rewritten every round regardless, and the
   append's own separator newline at the NEXT round's C2 will restore
   `.agent/live_review.md`'s true byte sequence going forward either way),
   but do not repeat it: after writing, re-open the file you just wrote and
   confirm its last byte is `\n`, matching the slice's own last byte,
   BEFORE committing.
6. `.agent/plan.md` stays under 50 lines.
7. Every exit code you report is REAL, from `subprocess.run(...).returncode`
   in a script under the gitignored `.remedy-wt/`, never through a pipe.
8. Destructive verification, if any, runs ONLY inside a disposable
   `git worktree`, never in the primary checkout, which satisfies
   `git status --porcelain` empty at every reading. This round needs none —
   no mutation red-proof applies to a prose-only change — but if you choose
   to verify anything destructively anyway, isolate it the same way.
9. The `remedy` console script is DENIED in this sandbox; use
   `python3 -m apps.cli.grouped ...` if needed and say so.
10. Commit subjects carry no leading-slash token, no absolute path, no
    secret-like string, and no `Co-Authored-By` trailer.
11. Push after C6. No pull request, no merge, no force-push.
12. NO NEW R-ID AND NO NEW DECISION ID ARE MINTED THIS ROUND. `R-0570` stays
    OPEN. No `Gate: F258 R4` line is added — the NEXT round books this one.

## Slices

PLAN4 and RECORD4, each between its own BEGIN/END marker line. The markers
are NOT part of the unit; the unit starts on the line after BEGIN and ends
with the newline before END.

<<<BEGIN PLAN4
# Plan — F258 Self-use track v2

Branch: feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge
commit of pull request 225. SESSION 1, round 4.

## Goal
"Remedy is used on Remedy" keeps running with zero operator input: a generator
replenishes the self-use queue with exactly one dated, provenanced item
whenever it is empty at close, the consumed item is actually RUN through the
real job path under a small budget and stopped at the normal approval gate
rather than only planned, and any defect the run surfaces flows back into the
standard finding ledger.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the F040 closure candidate | done | round 1 |
| the F258 claim and the seam inventory | done | round 1 |
| T001 part 1 — schema v2, the provenance field | done | round 2 |
| T001 part 2 — the generator module, tier 1 | done | round 3 |
| T001 part 3 — wiring the closure protocol doc | done | this round |
| T002 consumed means executed | open | |
| T003 findings flow back | open | |

## Next Steps
1. This round is docs-only: precondition 6 now names the generator as the
   step before "exhausted," and the two stale "never discovers" claims are
   corrected to point at the loader/generator split rather than contradict
   the module that now generates.
2. T001 itself is now feature-complete against the feature file's own text
   (the generator exists, fires when empty, is tested end to end). T002 is
   next: actually RUNNING a consumed item through the real job path under a
   small budget to the approval gate, not merely planning it.
3. T003 wires existing finding-ledger machinery once T002 exists.

## Risks
- R-0570 (Low) stays OPEN, routed away, unrelated to this branch.
- T002's "small dedicated budget" and "isolated worktree" seams were named,
  not yet designed, by round 1's inventory (`.agent/f258_inventory.md` §4-5)
  — the next round's own DECISION settles the concrete flags and commands.
<<<END PLAN4

<<<BEGIN RECORD4
Gate: F258 R3 — THE GENERATOR MODULE (TIER 1 REAL, TIERS 2-3 HONEST PLACEHOLDERS). VERDICT PASS. THE REVIEWER RE-RAN THE ROUND'S OWN VERIFICATION INDEPENDENTLY, reading the diff `549895fe..4c1a1495` in full, having ALSO dry-run the entire round's design against the real repository BEFORE authoring the block — writing and testing the module and its tests directly, catching and fixing two real defects in that process (a paragraph-extraction regex that failed when the oldest eligible finding was the ledger's LAST paragraph, since the original pattern required a trailing `\n\n` that end-of-file never provides; and a development-artifact-boundary guard violation, since the new module reads `.agent/live_review.md`, which the guard test correctly flagged until the module was added to `_ALLOWED_LEGACY` for the same reason `self_dogfood.py` and `integrity_gate.py` are already there). THE TRANSPORT: sha256 `cc7e9b036cb78f47d5cc5cb95314c67c1267f0d0937046dfbcc0509e9f06e4ce`, 25798 bytes, all three copies equal. THE PLAN: the committed `.agent/plan.md` matches PLAN3 for EVERY BYTE EXCEPT ITS OWN FINAL NEWLINE, which the commit dropped — sha256 therefore differs (`a4a7b674...` committed vs `9e4b8480...` authored) though the CONTENT is identical; 41 lines either way, well under 50, `## Goal` and `## Next Steps` both present. THE RECORD APPEND HAS THE SAME ONE-BYTE OMISSION, independently found by the reviewer, NOT self-declared by the worker: `base` (1756614 bytes) + `"\n"` + RECORD3 (10196 bytes) should equal 1766811 bytes, but the committed file is 1766810 — exactly one byte short, and `reconstructed[:-1] == committed` is True, confirming the ENTIRE 1766810 bytes preceding that point are byte-perfect and only the very last `\n` of the DECISION paragraph is missing. THE PARAGRAPH-ORDER READING, adjusted for the same one byte, holds: the first two of the three committed paragraphs (the two Gate verdicts) are byte-exact, and the third (DECISION F258 D2) is exact except for its own final newline. THE NEGATIVE CONTROL, run by the reviewer in a disposable worktree removed after, correctly distinguishes the two cases: a real content byte flipped elsewhere in the DECISION paragraph is rejected by the adjusted reading, while the known one-byte omission is accepted by it — so the check remains a real proof, not a rubber stamp widened to hide a defect. THIS IS A CONFIRMED, LOW-SEVERITY, SELF-HEALING DEVIATION, ACCEPTED NON-BLOCKING, the same shape as F040 R18's double-blank-line finding: `.agent/plan.md` is fully rewritten every round regardless of this byte, and `.agent/live_review.md` is append-only, so the NEXT round's own `base + "\n" + slice` construction restores the exact byte sequence the file would have carried had this round not dropped it — the omission is invisible to every consumer that reads by paragraph or by heading, and self-corrects by construction rather than by a dedicated repair. No id is minted for it; this paragraph is the record. THE MODULE AND ITS TESTS, delivered as two scratch-file `shutil.copyfile` copies rather than inlined slices (specifically to keep this commit and this block under the 500-line cap without spending round 2's already-used oversize-commit exception a second time): both BYTE-EQUAL to the reviewer's own scratch originals, sha256 `c6751c8b62f6da677c8c530d8a9ab0b62f239c1e2fdc6e32bf3be2ef16ebd057` (270 lines) and `bccb9bbbbbbb3f48a4d4be7a8ed3aa02cbc4e3a415a602fb8bc902a236c1cd27` (310 lines) — confirming the safer copy method used here left NO trailing-byte defect, unlike the text-extraction method used for PLAN3/RECORD3. `python3 -m pytest tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_job.py -q`: REAL exit 0, 61 passed (20+23+18), independently re-run by the reviewer. THE MUTATION RED-PROOF, independently reproduced by the reviewer in the reviewer's OWN disposable worktree, `__pycache__` purged, `python3 -B`: disabling the ONE safety check in `_ledger_tier` gave REAL exit 1, exactly the two predicted failures (`test_a_paragraph_shaped_like_a_heading_raises_rather_than_generating`, `test_a_paragraph_containing_an_acceptance_marker_raises`), 18 passed; restoring gave REAL exit 0, 20 passed again. THE BOUNDARY PAIR: FROM 0, TO exactly 1. THE THREE REPO-WIDE GUARDS, each its own REAL exit 0, independently re-run: `test_data_paths.py` 23 passed, `test_development_artifact_boundary.py` 18 passed, `test_path_utils.py` 28 passed. THE STATE READERS AND CANARY, all REAL exit 0, matching every prior round's base exactly: 515, 52, 21, 16, 42. THE TREE: clean, single worktree, per-commit insertions 283/206/17/6/270/310/5/234 from `git log --numstat`, every one under 500 — no oversize exception needed or used this round. THE ROUND PASSES, WITH THE ONE DEVIATION ABOVE RECORDED, NOT HIDDEN: the change set matches the block's fixed eight paths exactly, the tree was clean and pushed, no `tmp/*` branch or extra worktree survived. No new finding is raised beyond the deviation already resolved in this paragraph.
<<<END RECORD4

## PAIR-STATUSPROTO — `docs/roadmap/STATUS_closure_protocol.md`

<<<BEGIN PAIRSTATUSPROTO-FROM
   feature's id in the closure commit. If the queue holds NO pending item the
   track is exhausted, not blocked: record `self-use NONE (queue exhausted)`
   in the handback and close normally, because an empty queue asks the
   operator to curate more rather than stopping a feature. Why this is a
<<<END PAIRSTATUSPROTO-FROM
<<<BEGIN PAIRSTATUSPROTO-TO
   feature's id in the closure commit. If the queue holds NO pending item,
   the session calls
   `packages.orchestration.self_use_generator.generate_and_append_if_empty`
   FIRST (F258 T001) — its Tier 1 (the oldest open Low/Medium finding in
   `.agent/live_review.md`) supplies one in practice, since the ledger rarely
   runs dry. Only once THAT also answers `None` is the track truly
   exhausted, not blocked: record `self-use NONE (queue exhausted)` in the
   handback and close normally, because a genuinely empty queue with no
   eligible source asks the operator to curate more rather than stopping a
   feature. Why this is a
<<<END PAIRSTATUSPROTO-TO

## PAIR-BANNER and PAIR-ABSENCESDOC — `docs/system/self-use-track-v1.md`

<<<BEGIN PAIRBANNER-FROM
> at feature close. **Update (2026-08-30, F258 round 2):** the queue's schema
> moved to v2, adding a required `provenance` field naming each item's source;
> every shipped item was migrated. F258's self-replenishing generator is not
> yet built — this page still describes v1's discovery-free behaviour, which
> remains true until that round ships.
<<<END PAIRBANNER-FROM
<<<BEGIN PAIRBANNER-TO
> at feature close. **Update (2026-08-30, F258 rounds 2-3):** the queue's
> schema moved to v2, adding a required `provenance` field naming each item's
> source, and `packages/orchestration/self_use_generator.py` now supplies one
> when the queue is empty (Tier 1: the oldest open Low/Medium finding; Tiers
> 2-3 are documented placeholders, DECISION F258 D2). This page's "Deliberate
> absences" below is corrected accordingly — the LOADER stays read-only, but
> the track as a whole is no longer discovery-free.
<<<END PAIRBANNER-TO

<<<BEGIN PAIRABSENCESDOC-FROM
Remedy deliberately does not discover, generate or infer queue items. The list
is operator-curated data; curation is where this feature's risk sits, and the
queue is exactly as useful as the human who wrote it.
<<<END PAIRABSENCESDOC-FROM
<<<BEGIN PAIRABSENCESDOC-TO
Remedy deliberately does not discover, generate or infer queue items IN THE
LOADER ABOVE — that module stays read-only by construction (DECISION F257
D2). `packages/orchestration/self_use_generator.py` (F258, built round 3) is
the separate module that now does: it searches, in a fixed priority order,
for a source to append as a new PENDING item when the queue is empty, and
never marks anything consumed. The list a human curates and the list a
generator can extend now share one file and one loader; only the WRITER
changed, and it is still not this module.
<<<END PAIRABSENCESDOC-TO

## PAIR-ABSENCESMODULE — `packages/orchestration/self_use_queue.py`

<<<BEGIN PAIRABSENCESMODULE-FROM
  * Remedy deliberately does not discover, generate or infer queue items.  The
    list is operator-curated DATA — curation is where this feature's risk sits,
    not in code — so the queue is exactly as useful as the human who wrote it.
<<<END PAIRABSENCESMODULE-FROM
<<<BEGIN PAIRABSENCESMODULE-TO
  * REMEDY DELIBERATELY DOES NOT DISCOVER, GENERATE OR INFER A QUEUE ITEM IN
    THIS MODULE — it stays read-only, exactly as this docstring's opening
    line says.  :mod:`packages.orchestration.self_use_generator` (F258) is
    the SEPARATE module that now does, appending a new pending item when the
    queue is empty; it owns the one writer this queue gained, and this
    loader owns none.  A human-curated item and a generated one are read
    identically from here, so this loader's own contract is unchanged.
<<<END PAIRABSENCESMODULE-TO

## Done when — the gates

Run each gate and report ONE line per gate in the handback with its REAL exit
code. Every gate below runs at a commit STRICTLY EARLIER than C6, which writes
the handback.

G1 TRANSPORT, at C0b. sha256 over THREE files — `.remedy-wt/f258-r4-block.md`,
   the committed `.agent/authored/f258-r4.md`, and the committed
   `.agent/last_block.md` — report the one digest and byte length, state all
   three equal.

G2 THE PLAN, at C1. `.agent/plan.md` BYTE-EQUAL to PLAN4 (report both sha256,
   and CONFIRM the file's last byte is `\n` per constraint 5), under 50
   lines, holds `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2. Re-measure `.agent/live_review.md`'s byte length
   yourself immediately before C2 — note it will read 1766810, ONE LESS than
   a naive expectation, because of round 3's own documented one-byte
   omission (see RECORD4 and this block's constraint 5); your OWN reading of
   the base is definitionally correct regardless, since you measure it
   fresh. TWO readings: (a) WHOLE RECONSTRUCTION — base + `\n` + RECORD4
   equals the committed file exactly; (b) the committed file's last
   `\n\n`-delimited unit equals RECORD4 exactly (N=1). CONFIRM the committed
   file's own last byte is `\n` (constraint 5) — this round must NOT repeat
   round 3's omission. NEGATIVE CONTROL inside a disposable worktree: flip
   one printable byte inside RECORD4 and show both readings reject the flip
   and accept the original; remove the worktree after.

G4 THE LEDGER, at C1 and at C2. Distinct `^- R-\d+ — ` and `^Done: R-\d+` ids,
   ADDED/REMOVED both empty. Distinct `^DECISION F258 D\d+ — ` ids unchanged
   at `['D1', 'D2']` before and after (ADDED `[]`). Distinct
   `^Gate: F258 R\d+ — ` lines before and after: `['F258 R1', 'F258 R2']`
   then `['F258 R1', 'F258 R2', 'F258 R3']` — ADDED is exactly `['F258 R3']`.
   `^Done: R-0570` stays 0.

G5 THE FOUR PROSE PAIRS AND THE DOCS SUITES, at C5. For PAIR-STATUSPROTO,
   PAIR-BANNER, PAIR-ABSENCESDOC and PAIR-ABSENCESMODULE: FROM occurs 0 times
   and TO occurs exactly 1 time, post-commit, for each. Confirm, by reading
   the diff yourself, that `packages/orchestration/self_use_queue.py`'s ONLY
   change is inside its module docstring — zero lines outside the
   triple-quoted string changed. Then, at C5: `python3 -m pytest
   tests/docs/ -q`, `python3 -m pytest tests/orchestration/test_roadmap_index.py -q`
   (`docs/roadmap/STATUS_closure_protocol.md` is under `docs/roadmap/**`),
   and `python3 -m pytest tests/orchestration/test_self_use_generator.py
   tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_job.py -q`
   (confirming the docstring-only edit broke nothing), each its own REAL exit
   code. The reviewer measured these at the base at 295, 30 and 61 passed;
   report YOURS.

G6 THE STATE READERS AND THE CANARY, at C6. Each its own REAL exit code:
   `python3 -m pytest tests/ui_server/ -q`,
   `python3 -m pytest tests/orchestration/test_test_runner.py -q`,
   `python3 -m pytest tests/regression/test_resource_safety.py -q`,
   `python3 -m pytest tests/orchestration/test_integrity_gate.py -q`, and the
   canary `python3 -m pytest tests/cli/test_golden_path.py -q`. The reviewer
   measured these at the base at 515, 52, 21, 16 and 42 passed; report YOURS.

G7 THE TREE, at C6. `git status --porcelain` EMPTY, `git ls-files --others
   --exclude-standard` count 0, `git worktree list` shows the primary
   checkout alone, and the per-commit insertion counts for C0a through C5
   from `git diff --numstat`, every one under 500.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries
the state block, the `## Commits` table with `+/-` from `git diff --numstat`,
the deviations, the item-status table with every bundle item and every gate
appearing exactly once, and the next steps. It states `SESSION 1` of F258 and
round 4. It has NO length cap. Name `R-0570` as OPEN and routed away, confirm
NO new R-id or DECISION id was minted, and name `Gate: F258 R3` as newly
booked into the ledger this round.
