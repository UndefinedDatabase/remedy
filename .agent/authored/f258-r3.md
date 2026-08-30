# STEP R3/F258 — T001 PART 2: THE GENERATOR MODULE (TIER 1 REAL, TIERS 2-3 HONEST PLACEHOLDERS)

Goal: build `packages/orchestration/self_use_generator.py`, the ONE writer the
self-use queue gains — it searches, in the priority order the feature file
names, for a source to turn into a new pending queue item, and appends it ONLY
when the queue is empty. Tier 1 (the finding ledger) is real and tested this
round. Tiers 2 and 3 are honest, documented `None` placeholders, per DECISION
F258 D2 below — not yet wired to a real source, same shape as F040's
honestly-empty `ownership` field. This round also books the two verdicts the
reviewer owes the ledger from rounds 1 and 2, which amend0827 rule 1 defers to
"the first commit of the next round that is happening anyway" — this one.

Base: `549895fe`, round 2's handback commit and the tip of
`feature/f258-self-use-v2`. Stay on that branch. Open no pull request.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f258-r3.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN3
- C2  append slice RECORD3 to `.agent/live_review.md`
- C3  copy `.remedy-wt/f258-r3-genmodule.py` verbatim to `packages/orchestration/self_use_generator.py`
- C4  copy `.remedy-wt/f258-r3-gentests.py` verbatim to `tests/orchestration/test_self_use_generator.py`
- C5  apply pair PAIR-BOUNDARY to `tests/orchestration/test_development_artifact_boundary.py`
- C6  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f258-r3.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    packages/orchestration/self_use_generator.py
    tests/orchestration/test_self_use_generator.py
    tests/orchestration/test_development_artifact_boundary.py
    .agent/handoff.md

`.agent/context.md` is NOT touched — nothing in it changed. No file under
`apps/` changes. `scripts/self_use_queue.json` is NOT touched this round —
the generator is built and tested against FIXTURE queues only; nothing calls
it against the real shipped queue, so the real queue stays exactly as round 2
left it (five would be wrong: it stays FOUR items).

## Constraints

1. C3 and C4 are COPIES, never a retype: `shutil.copyfile` from
   `.remedy-wt/f258-r3-genmodule.py` and `.remedy-wt/f258-r3-gentests.py`
   respectively — the reviewer's own code, already written and tested against
   this exact repository before this block was authored. Do not "improve" a
   docstring, a comment, or a variable name; if either file looks wrong,
   apply it as given and declare the problem in the handback's deviations.
   Apply PLAN3, RECORD3 and PAIR-BOUNDARY the same never-retype discipline —
   PLAN3 and RECORD3 by copying their exact slice bytes, PAIR-BOUNDARY by the
   FROM/TO replace method constraint 5 describes.
2. C0a is a COPY, never a retype: the block is at
   `.remedy-wt/f258-r3-block.md`. Use `shutil.copyfile` for C0a and again for
   C0b. Its sha256 is stated in gate G1; verify BEFORE saving. This block is
   DELIBERATELY SMALL relative to the code it orders: GENMODULE and GENTESTS
   are shipped as separate scratch files (constraint 1) precisely so this
   commit and this block stay under the 500-line cap without needing round
   2's oversize-commit exception a second time in the same feature, which
   AGENTS.md's own wording permits only once.
3. C1 is the FIRST substantive commit, ahead of C2, per AGENTS.md's Commit
   Gate.
4. `.agent/live_review.md` is APPEND-ONLY. C2 appends RECORD3 and revises
   NOTHING already there — RECORD3 carries THREE paragraphs (the round 1
   verdict, the round 2 verdict, and DECISION F258 D2), all as ONE slice
   appended in ONE commit.
5. PAIR-BOUNDARY is applied with the same method round 2 established: assert
   `text.count(FROM) == 1`, then `text.replace(FROM, TO, 1)`, then write
   back. Report before/after occurrence counts.
6. `.agent/plan.md` stays under 50 lines.
7. Every exit code you report is REAL, from `subprocess.run(...).returncode`
   in a script under the gitignored `.remedy-wt/`, never through a pipe.
8. The mutation red-proof (G5) runs ONLY inside a disposable `git worktree`:
   purge every `__pycache__` under `packages/orchestration/` and
   `tests/orchestration/` inside it and run with `python3 -B`. The primary
   checkout is `git status --porcelain` empty at every reading.
9. `packages/orchestration/self_use_generator.py` is a NEW module under
   `packages/orchestration/`, swept by repo-wide guards that name no path:
   the `REMEDY_DATA_DIR` single-reader invariant (`tests/test_data_paths.py`),
   the path-utils single-implementation invariant
   (`tests/test_path_utils.py`), the bare-`except: pass` ban, and the
   development-artifact boundary (`tests/orchestration/test_development_artifact_boundary.py`
   — this is WHY C5 exists: the reviewer ran this exact guard against this
   exact module before authoring this block and it failed until the module
   was added to `_ALLOWED_LEGACY`, for the same reason `self_dogfood.py` and
   `integrity_gate.py` are already there — this module reads Remedy's OWN
   development ledger to feed Remedy's OWN self-maintenance, never an
   end-user job's runtime path).
10. The `remedy` console script is DENIED in this sandbox; use
    `python3 -m apps.cli.grouped ...` if needed and say so.
11. Commit subjects carry no leading-slash token, no absolute path, no
    secret-like string, and no `Co-Authored-By` trailer.
12. Push after C6. No pull request, no merge, no force-push.
13. NO NEW R-ID IS MINTED. Exactly one new `^DECISION F258 D\d+ — ` id is
    minted: `D2`. `R-0570` stays OPEN. No `Gate: F258 R3` line is added this
    round — a round does not record a verdict on itself; ROUND 4 books this
    one, per amend0827 rule 1, the same way this round books rounds 1 and 2.

## Slices

PLAN3 and RECORD3, each between its own BEGIN/END marker line. The markers
are NOT part of the unit; the unit starts on the line after BEGIN and ends
with the newline before END. GENMODULE and GENTESTS are NOT inlined here —
they are the two scratch files C3/C4 copy from (constraint 1); read them
directly from disk rather than looking for a slice marker that does not
exist in this block.

<<<BEGIN PLAN3
# Plan — F258 Self-use track v2

Branch: feature/f258-self-use-v2, cut from `main` at `18ae7129`, the merge
commit of pull request 225. SESSION 1, round 3.

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
| T001 part 2 — the generator module, tier 1 | done | this round |
| T001 part 3 — wiring the closure protocol doc | open | next round |
| T002 consumed means executed | open | |
| T003 findings flow back | open | |

## Next Steps
1. This round builds `packages/orchestration/self_use_generator.py`: Tier 1
   (the finding ledger) is real and tested; Tiers 2-3 are honest `None`
   placeholders per DECISION F258 D2. Nothing calls it yet — the real queue
   is untouched.
2. The round after it wires `generate_and_append_if_empty` into
   `docs/roadmap/STATUS_closure_protocol.md` precondition 6's own text, so a
   future closure round reads "call the generator" rather than "curate by
   hand" — still a session/human action, since nothing in this protocol runs
   unattended, but the function now exists to call.
3. T002 depends on a generated item actually being run, not just appended;
   T003 wires existing finding-ledger machinery once T002 exists.

## Risks
- R-0570 (Low) stays OPEN, routed away, unrelated to this branch.
- Tiers 2 and 3 are placeholders, not gaps hidden from the record: DECISION
  F258 D2 names exactly what each needs before it can be real.
<<<END PLAN3

<<<BEGIN RECORD3
Gate: F258 R1 — THE CLAIM, THE F040 CANDIDATE DISCHARGE, AND THE SEAM INVENTORY. VERDICT PASS. THE REVIEWER RE-RAN THE ROUND'S OWN VERIFICATION INDEPENDENTLY RATHER THAN TAKING THE HANDBACK'S NUMBERS, reading the diff `18ae7129..d3913f60` in full. THE TRANSPORT: `.remedy-wt/f258-r1-block.md`, `.agent/authored/f258-r1.md` and `.agent/last_block.md` sha256-equal at `4285092d765124f143b48f3ec791eaa7eac8cf4e266c4c31fcfc72e424c5f11c`, 20439 bytes, all three. THE PLAN: byte-equal to PLAN1 at sha256 `86dad5fe0fa993cb96ca60b9a195562849ef20579837b7cbf12393ef7fc49265`, 44 lines. THE RECORD APPEND: base 1751668 bytes trailing-newline-terminated; `base + "\n" + RECORD1` (1375 bytes) equals the committed 1753044-byte file exactly; the last of 771 blank-line units equals RECORD1 exactly. NEGATIVE CONTROL, inside a disposable worktree removed after: one byte flipped inside RECORD1 made both readings reject the flipped file; the unflipped file was accepted by both. THE LEDGER, recomputed by difference between the commit before C2 and C2: registered/resolved ADDED `[]`/`[]` (317/55 distinct both sides), `DECISION F258 D` ADDED `[]`, `Done: R-0570` stays 0. THE CANDIDATES FILE: byte-equal to CAND1 at sha256 `454ac5f45f58bb1662523e77a95b902704b3d2662bec80a2c30d53f0172579ed`, 695 bytes, the stale marker `· F040 · 2026-08-30` occurring 0 times. THE STATUS PAIR: PAIRSTATUS-FROM 0 occurrences, PAIRSTATUS-TO exactly 1, one `^- \[~\] F\d{3} — ` line in the whole file. `python3 -m pytest tests/docs/ -q` and `test_roadmap_index.py` both REAL exit 0, 295 and 30 passed. THE STATE READERS AND CANARY, all REAL exit 0: `tests/ui_server/` 515, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, canary 42. THE INVENTORY: `.agent/f258_inventory.md` carries all six SPEC-ordered headings plus one additive "Absences, summarized" section; 60 `file:line` citations over 10 distinct paths, every one independently confirmed to resolve via `git ls-tree HEAD`; every claim spot-checked against the cited source (the queue schema constants, the `_ITEM_KEYS` equality check, the `SelfUseQueueEntry` dataclass fields) read EXACTLY as cited. THE ROUND PASSES: the change set matches the block's fixed nine paths exactly, no file under `packages/`, `apps/` or `tests/` changed, the tree was clean and pushed, no `tmp/*` branch or extra worktree survived. No new finding is raised by this review.

Gate: F258 R2 — THE QUEUE SCHEMA MOVES TO V2 (THE PROVENANCE FIELD). VERDICT PASS. THE REVIEWER RE-RAN THE ROUND'S OWN VERIFICATION INDEPENDENTLY, reading the diff `d3913f60..549895fe` in full, having ALSO dry-run the entire block against the real repository BEFORE delegating it — every pair checked for a unique FROM match, the resulting Python and JSON parsed, and the real test suite run — so this verdict rests on a proof the reviewer built twice, once before and once after. THE TRANSPORT: sha256 `cb57357a7e568dba4b8b5df2f25099a9af98552535c2d2fec8ae8be4d3c036fa`, 33555 bytes, all three copies equal. THE PLAN: byte-equal to PLAN2, sha256 `3d065c0ecc484b69b999d7a1916285b9a6af84c9e16900f49958daf5bad59dd1`, 40 lines. THE RECORD APPEND: base 1753044 bytes; `base + "\n" + RECORD2` (3569 bytes) equals the committed 1756614-byte file exactly; the last of 772 units equals RECORD2 exactly. NEGATIVE CONTROL, inside a disposable worktree removed after: a byte flip was rejected by both readings, the original accepted by both. THE LEDGER: `DECISION F258 D` ADDED exactly `['D1']`, registered/resolved unchanged at 317/55, `Done: R-0570` stays 0. THE TWENTY-FIVE PAIRS (six in `self_use_queue.py`, six in `test_self_use_queue.py`, three in `test_self_use_job.py`, six in `scripts/self_use_queue.json`, three in `self-use-track-v1.md`, one in `T5_F257.md`): every FROM occurs 0 times and every TO occurs exactly 1 time post-commit, independently re-measured. `scripts/self_use_queue.json` parses, `schema_version` 2, all four items carry six keys including a non-blank `provenance`. `python3 -m pytest tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_job.py -q`: REAL exit 0, 41 passed (23+18, five new tests, one renamed). THE MUTATION RED-PROOF, independently reproduced by the reviewer in the reviewer's OWN disposable worktree, `__pycache__` purged, `python3 -B`: reverting PAIRQ5 alone gives REAL exit 1, exactly ONE failure, `test_blank_provenance_raises` (`DID NOT RAISE SelfUseQueueError`) — the other two tests the worker's own report also correctly predicted would stay green did stay green; restoring gives REAL exit 0, 41 passed again. `tests/docs/` and `test_roadmap_index.py` both REAL exit 0, 295 and 30 passed. THE STATE READERS AND CANARY, all REAL exit 0, matching round 1's own base exactly: 515, 52, 21, 16, 42. THE TREE: clean, single worktree, per-commit insertions 682/624/18/2/9/42/3/10/11/9/298 from `git log --numstat`, matching the handback exactly. ONE DECLARED EXCEPTION IS ACCEPTED, NOT A PRECEDENT: C0a (`.agent/authored/f258-r2.md`, 682 insertions) exceeds AGENTS.md's 500-line cap and is NOT covered by the named `.agent/**` exemption (which lists only `last_block.md`, `handoff.md`, `live_review.md`, `plan.md`, `context.md` — not `authored/*.md`). The worker declared it in the handback with the inseparability reason (the WHOLE 682-line block must land in one commit for G1's transport proof to compare like-for-like) before this review, and it is the ONLY such non-exempt oversize commit across F258's two rounds so far — round 1's equivalent commit was 365 lines, under the cap. Both conditions of AGENTS.md's oversize-commit exception are met. C0b (624 insertions, `last_block.md`) needed no declaration: it IS in the named exemption. THE ROUND PASSES: the change set matches the block's fixed eleven paths exactly, the tree was clean and pushed, no `tmp/*` branch or extra worktree survived. No new finding is raised by this review.

DECISION F258 D2 — THE GENERATOR'S THREE TIERS: ONE REAL, TWO HONEST PLACEHOLDERS; A GENERIC TITLE OVER A PARSED ONE; NO SAFETY PROBE THROUGH `parse_job_file`. THE PROBLEM: `docs/roadmap/features/T5_F258.md` T001 names three sources in priority order — the finding ledger, a documentation-staleness catalog, and an actionable `remedy doctor core` warning — and this round has to decide how much of that to build now versus defer, and how to render a ledger finding into a job without inventing content the finding's own text does not state. CHOSEN, four parts. (1) TIER 1 IS REAL: the oldest OPEN (no `Done:` line) Low or Medium finding in `.agent/live_review.md`, chosen by lowest numeric id — measured by the reviewer at `549895fe`: 149 such findings exist today (`R-0418` oldest), so this tier will fire in practice for a very long time; High and Critical are never picked, because a generator making a judgement call about a high-severity finding is exactly the kind of guess this project's "never invent" discipline forbids. (2) TIERS 2 AND 3 ARE HONEST `None` PLACEHOLDERS, not stubs hidden from the record: a documentation-staleness catalog needs its own curation (mirroring DECISION F040 D3's empty `ownership` list until F035 existed), and `remedy doctor core`'s handler (`apps/cli/commands/worker_facade_cmd.py:412`, `_cmd_doctor_core`) is an argparse function that prints, not an importable function returning structured warnings — refactoring that seam is its own future round, not squeezed into this one. (3) THE RENDERED JOB's TITLE IS GENERIC ("Address ledger finding R-XXXX"), NOT PARSED FROM THE FINDING'S OWN HEADLINE, and the finding's FULL PARAGRAPH is quoted verbatim as both `why` and the job's Task 1 body — measured by the reviewer across all 149 open Low/Medium findings: their ALL-CAPS headline conventions are NOT uniform (some are one long capitalized sentence, e.g. `R-0570`; others are a short capitalized phrase followed by ordinary prose, e.g. `R-0418`'s "REVIEWER-BLOCK DEFECT, found by the worker..."), so any regex attempting to extract "the headline" would occasionally produce a truncated or wrong title — robustness was chosen over polish, and the full paragraph in `why`/Task-1 carries every fact a human would need regardless of what the title says. (4) SAFETY IS CHECKED BY REGEX, NOT BY CALLING `parse_job_file`: the reviewer discovered, while drafting this module, that `parse_job_file` (`packages/orchestration/pingpong_job.py:731`) calls `_persist_job` as a side effect — using it to "probe" whether a rendered job_markdown parses safely would silently write a phantom job record to `REMEDY_DATA_DIR` on every generation, which a pure search function must never do. The module instead checks the ledger paragraph directly for a line shaped like `## ` or `Acceptance:` (case-insensitive) and RAISES rather than generates if one is found — measured against all 149 candidates: zero are unsafe today, but the check is structural, not a today-only assumption. ALTERNATIVES CONSIDERED: (a) parse the headline with a best-effort regex and accept an occasional truncation — rejected, an occasionally-wrong title is worse than a boring-but-always-correct one, per the same reasoning DECISION F040 D5 used to reject a deep link with no reader; (b) build a minimal doc-staleness catalog now with one or two entries — rejected as scope creep this round did not need, since Tier 1 already satisfies the Acceptance bar ("a feature close on an empty queue still consumes one generated item") on its own; (c) call `parse_job_file` and catch/ignore the persistence side effect — rejected, a side effect a caller must remember to ignore is a defect waiting for the caller who forgets. HOW TO REVERSE: Tiers 2/3 becoming real is purely additive — replacing a `None`-returning function body with a real one changes no signature and no caller. The title convention can change independently of everything else, since `why` and the job body never depend on what the title says. WHAT IT COSTS TO BE WRONG HERE: if the generic title reads poorly next to the human-curated titles already in the queue, only the one f-string in `_ledger_tier` changes; every other decision in this record stands independently of it.
<<<END RECORD3

## PAIR-BOUNDARY — `tests/orchestration/test_development_artifact_boundary.py`

<<<BEGIN PAIRBOUNDARY-FROM
    "packages/orchestration/fresh_evidence_gate.py",
}
<<<END PAIRBOUNDARY-FROM
<<<BEGIN PAIRBOUNDARY-TO
    "packages/orchestration/fresh_evidence_gate.py",
    # F258's self-use generator reads the SAME development ledger to pick its
    # next self-maintenance item — it is Remedy's own dogfooding machinery,
    # the same category as self_dogfood.py and integrity_gate.py above, never
    # a runtime dependency of an end-user's job.
    "packages/orchestration/self_use_generator.py",
}
<<<END PAIRBOUNDARY-TO

## Done when — the gates

Run each gate and report ONE line per gate in the handback with its REAL exit
code. Every gate below runs at a commit STRICTLY EARLIER than C6, which writes
the handback.

G1 TRANSPORT, at C0b. sha256 over THREE files — `.remedy-wt/f258-r3-block.md`,
   the committed `.agent/authored/f258-r3.md`, and the committed
   `.agent/last_block.md` — report the one digest and byte length, state all
   three equal.

G2 THE PLAN, at C1. `.agent/plan.md` BYTE-EQUAL to PLAN3 (report both sha256),
   under 50 lines, holds `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2. Re-measure `.agent/live_review.md`'s byte length
   yourself immediately before C2. TWO readings: (a) WHOLE RECONSTRUCTION —
   base + `\n` + RECORD3 equals the committed file exactly; (b) PARAGRAPH
   ORDER — the committed file's last THREE `\n\n`-delimited units equal
   RECORD3's three paragraphs (the two Gate paragraphs and the DECISION) IN
   ORDER — RECORD3 is N=3, not N=1, unlike every prior round's record slice
   on this branch, because it carries two verdicts and one decision as three
   separate dense paragraphs. NEGATIVE CONTROL inside a disposable worktree:
   flip one printable byte inside the DECISION paragraph (the third/last) and
   show both readings reject the flip and accept the original; remove the
   worktree after.

G4 THE LEDGER, at C1 and at C2. Distinct `^- R-\d+ — ` and `^Done: R-\d+` ids,
   ADDED/REMOVED both empty. Distinct `^DECISION F258 D\d+ — ` ids before and
   after: `['D1']` then `['D1', 'D2']` — ADDED is exactly `['D2']`. Distinct
   `^Gate: F258 R\d+ — ` lines before and after: `[]` then
   `['Gate: F258 R1', 'Gate: F258 R2']` (report the two full line-openings you
   find, not just the count). `^Done: R-0570` stays 0.

G5 THE GENERATOR MODULE AND ITS TESTS, at C4. `packages/orchestration/self_use_generator.py`
   BYTE-EQUAL to the scratch original `.remedy-wt/f258-r3-genmodule.py`
   (report both sha256, both byte lengths).
   `tests/orchestration/test_self_use_generator.py` BYTE-EQUAL to the scratch
   original `.remedy-wt/f258-r3-gentests.py` (report both sha256, both byte
   lengths). Then, at C4, in the PRIMARY
   checkout: `python3 -m pytest tests/orchestration/test_self_use_generator.py
   tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_job.py -q`,
   REAL exit 0, report the count (the reviewer measured 61 — 20+23+18 — when
   drafting this module against this exact repository state; report yours
   and confirm it matches or explain any difference). THEN the mutation
   red-proof, in a disposable git worktree branched from C4, `__pycache__`
   purged, `python3 -B`: comment out (or otherwise disable) the ONE `if`
   statement in `_ledger_tier` that raises `SelfUseGenerationError` for an
   unsafe paragraph (the block right after `found = ...`), and re-run
   `tests/orchestration/test_self_use_generator.py` alone — report REAL exit
   code and the FAILED test names; you expect BOTH
   `TestLedgerTierSafety::test_a_paragraph_shaped_like_a_heading_raises_rather_than_generating`
   and `TestLedgerTierSafety::test_a_paragraph_containing_an_acceptance_marker_raises`
   to go RED (each asserts `pytest.raises(SelfUseGenerationError)`, and with
   the check disabled the call returns a value instead of raising), while
   every OTHER test in the file stays GREEN. If your own run shows a
   DIFFERENT failure set, STOP and declare it as a deviation rather than
   silently reporting your own number as expected. Then restore the disabled
   check and re-run once more: REAL exit 0, all passing again. Remove the
   worktree after; `git worktree list` shows the primary checkout alone.

G6 THE BOUNDARY PAIR AND THE REPO-WIDE GUARDS, at C5. PAIR-BOUNDARY: FROM
   occurs 0 times, TO occurs exactly 1 time, post-commit. Then, at C5, in the
   PRIMARY checkout, each its own REAL exit code:
   `python3 -m pytest tests/test_data_paths.py -q`,
   `python3 -m pytest tests/orchestration/test_development_artifact_boundary.py -q`,
   and `python3 -m pytest tests/test_path_utils.py -q`. The reviewer measured
   these against the drafted module (before this round existed as a commit),
   run separately: `test_data_paths.py` 23 passed, then
   `test_development_artifact_boundary.py` 18 passed, then
   `test_path_utils.py` 28 passed — every one REAL exit 0 in that order. The
   MIDDLE one failed with exactly ONE violation (this new module, flagged by
   name) BEFORE PAIR-BOUNDARY's equivalent edit was applied by hand in that
   draft check; after it, all three passed clean. Report YOUR three numbers
   in the same order and confirm all three are green.

G7 THE STATE READERS AND THE CANARY, at C6. Each its own REAL exit code:
   `python3 -m pytest tests/ui_server/ -q`,
   `python3 -m pytest tests/orchestration/test_test_runner.py -q`,
   `python3 -m pytest tests/regression/test_resource_safety.py -q`,
   `python3 -m pytest tests/orchestration/test_integrity_gate.py -q`, and the
   canary `python3 -m pytest tests/cli/test_golden_path.py -q`. The reviewer
   measured these at the base at 515, 52, 21, 16 and 42 passed; report YOURS.

G8 THE TREE, at C6. `git status --porcelain` EMPTY, `git ls-files --others
   --exclude-standard` count 0, `git worktree list` shows the primary
   checkout alone, and the per-commit insertion counts for C0a through C5
   from `git diff --numstat`, every one under 500. The scratch originals are
   270 (`f258-r3-genmodule.py`) and 310 (`f258-r3-gentests.py`) lines, and
   this block itself is 279 lines — all comfortably under the cap, which is
   WHY C3/C4 copy from separate scratch files rather than inlining their
   content in this block (constraint 2): round 2 needed AGENTS.md's
   oversize-commit exception once already, and that exception is spent for
   this feature. Report YOUR measured numbers; do not assume they match
   exactly if your own copy differs in any way from what is declared here.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries
the state block, the `## Commits` table with `+/-` from `git diff --numstat`,
the deviations, the item-status table with every bundle item and every gate
appearing exactly once, and the next steps. It states `SESSION 1` of F258 and
round 3. It has NO length cap. Name `DECISION F258 D2` as the one id minted
this round, `R-0570` as OPEN and routed away, and both `Gate: F258 R1` and
`Gate: F258 R2` as newly booked into the ledger this round (not this round's
own verdict — that is round 4's to book).
