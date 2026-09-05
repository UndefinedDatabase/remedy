STEP CLOSURE PART 2 / F259 — Vocabulary & concept model v1 — round 9 of session 1
BRANCH feature/f259-vocabulary, head 32808b5d at the time this block was written.
MERGE BASE 25961794.

Goal
  The evidence half of the closure sequence. Book the round-8 verdict and the
  three ledger obligations closure precondition 6 and §4 item 4 create; repair
  the one real defect round 8 left on disk; rotate the ledger; build the evidence
  bundle and the FRESH review zip from a clean tree. The STATUS `[x]` flip, the
  README capability sync, the `consumed_by` edit and the pull request are part 3,
  because the STATUS line cannot be authored until this round has measured the
  evidence job id, the package name, its SHA-256 and the accepted HEAD.

Why each ledger entry is what it is
  R-0813 IS A NEW ID because round 8's consolidation left a real contradiction on
  disk under `docs/`: the frozen paragraph of
  `docs/agents/planner_reviewer_prompt.md` §3 now says both "The list stood at 37
  items on 2026-08-27, which is the number the next consolidation measures
  against" and "The next consolidation measures against 36." Both sentences claim
  to name what the NEXT consolidation measures against. The reviewer searched the
  open set for the defect before minting, per §3 item 30, and no open finding
  describes it — it did not exist until round 8 created it.
  THE SELF-USE DEFECTS TAKE NO NEW ID. Closure precondition 6 requires every
  string `describe_self_use_run_defects` returns to be registered before the
  close, and round 8's run returned two. `R-0784` is OPEN and is exactly this
  defect: its own text records the same two strings from an earlier run and
  states that they are one defect seen twice — the job-level and task-level views
  of one gate failure — and therefore take ONE id. §3 item 30 forbids a second id
  for a defect the open set already holds, so this round appends a `Recurrence:`
  paragraph to that id rather than minting `R-0814`.
  `Done: R-0418` IS OWED AND IS PAID HERE. SU-010's own acceptance reads: "R-0418
  is repaired with a red-to-green proof, or the reviewer records in
  `.agent/live_review.md` why it cannot be — either way the ledger gains a
  `Done: R-0418` line." R-0418 is a rule about REVIEWER block-authoring practice
  under self-drive, so it has no code to turn red; the reviewer measured
  compliance instead, across all seven of this feature's build rounds.

Bundle, in this order (one commit each)
  C0a save the block file to .agent/authored/f259-r9.md (copy, never retype)
  C0b mirror it to .agent/last_block.md
  C1  .agent/plan.md ← PLANF259R9 (whole rewrite)
  C2  FINDINGS PERSIST FIRST (§4 item 4). `.agent/live_review.md`: append, in
      this order and separated as described below, GATE_R8, FIND0813, REC0784 and
      DONE0418. `.agent/prose_slips.md`: append SLIP9. One commit.
  C3  docs/agents/planner_reviewer_prompt.md: the FROZENFIX pair — the repair of
      R-0813.
  C4  THE LEDGER ROTATION, its own commit, paths `.agent/live_review.md` and
      `.agent/live_review_archive.md` ONLY: `python3 scripts/rotate_live_review.py`.
      Run `--dry-run` first and report its output, then the real run.
  then push. Then, from the CLEAN TREE at that head, and committing nothing:
      the evidence job (G5) and the review zip (G6).
  C5  rewrite .agent/handoff.md, which records the zip outcome; push again.

  Create NO pull request. Do NOT touch `docs/roadmap/STATUS.md`, `README.md` or
  `scripts/self_use_queue.json` — all three belong to part 3's single closure
  commit, which must carry them together (R-0154).

Change set — EXACTLY these paths and nothing else
  .agent/authored/f259-r9.md (C0a) — .agent/last_block.md (C0b) —
  .agent/plan.md (C1) — .agent/live_review.md, .agent/prose_slips.md (C2) —
  docs/agents/planner_reviewer_prompt.md (C3) —
  .agent/live_review.md, .agent/live_review_archive.md (C4) —
  .agent/handoff.md (C5)

Delivery
  The block is at `.remedy-wt/f259-r9-block.md`, gitignored scratch. C0a COPIES
  it to .agent/authored/f259-r9.md, C0b to .agent/last_block.md. Slices are
  extracted from the COMMITTED authored file by marker extraction in Python.

The C2 appends
  `.agent/live_review.md` ends with a newline. Append, in ONE write:
      "\n" + GATE_R8 + "\n\n" + FIND0813 + "\n\n" + REC0784 + "\n\n" + DONE0418 + "\n"
  so the four paragraphs land in that order, each separated from its neighbour by
  one empty line, and the file still ends with exactly one newline.
  `.agent/prose_slips.md` does NOT end with a newline. Append `"\n\n" + SLIP9`
  and add NO trailing newline.

The FROZENFIX pair (C3)
  Applied with `str.replace(FROM, TO, 1)` after confirming FROM occurs EXACTLY
  ONCE. The reviewer ran the containment test before emission and it printed
  `TO contains FROM: false`, so it is a REWRITE and the obligation is FROM 0x and
  TO 1x afterwards. It changes exactly one clause of one sentence; gate G3
  requires the per-item digest sweep to show that NO checklist item's text
  changed, because the frozen paragraph is not inside any item.

Constraints
  1. Slices are applied BYTE FOR BYTE from the committed authored file by marker
     extraction in Python. Apply a slice you believe wrong verbatim and declare
     it in the handback.
  2. Read `.agent/STOP` from disk before C0a, before C4 and before C5.
  3. NEWLINE CONVENTIONS: PLANF259R9 replaces `.agent/plan.md` whole with exactly
     one trailing newline; the C2 appends are as described above;
     `docs/agents/planner_reviewer_prompt.md` still ends with exactly one newline.
  4. THE ROTATION IS ITS OWN COMMIT AND TOUCHES TWO PATHS. If the script refuses,
     STOP the rotation: commit nothing for C4, report the refusal text verbatim,
     and continue to the evidence job and the zip — a refused rotation is
     reported, never forced.
  5. THE EVIDENCE DIRECTORY IS NEVER COMMITTED. Put it OUTSIDE the review
     subject, under the gitignored `.remedy-wt/`. A pre-committed evidence dir
     puts evidence files into the base..HEAD review subject and the package
     builds BLOCKED_EVIDENCE.
  6. THE TREE IS CLEAN when the evidence job and the zip run. A package built
     from a dirty tree is invalid. Report `git status --porcelain` immediately
     before each.
  7. This session's shell guard refuses some command FORMS outright — shell
     loops, `$(...)` substitution, `$?` in a compound command, `${PIPESTATUS[0]}`,
     a `$` anchor inside a `grep -c` pattern, brace-with-quote literals in a
     heredoc, and a non-ASCII character in a Python bytes literal. Re-express in
     Python and report the Python you ran beside its output, with any refusal
     quoted verbatim. `ruff check` and the built `remedy` CLI are denied; use
     `python3 -m apps.cli.grouped <...>` where a remedy subcommand is needed.
  8. Commit subjects are `f259: <what>`. No leading-slash token, no absolute
     path, no secret-like string. End every commit message with the trailer
     `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.
  9. AGENTS.md binds you in full. Never `--force`, never a history rewrite, never
     `gh pr merge`, never a branch deletion. C5 is ONE commit.
 10. A FAILING ZIP BUILD IS A CLOSURE BLOCKER, not something to work around.
     Record the raw error, commit the handback saying so, and stop; the reviewer
     decides. Never close without the package.

Done when — the gates. Real exit codes, real output, one line per gate in the
handback. Every gate runs at or before the zip; none is ordered after C5.

  G1 TRANSPORT. `sha256sum .remedy-wt/f259-r9-block.md .agent/authored/f259-r9.md .agent/last_block.md`
     — one digest, three times.
  G2 THE C2 APPENDS. `.agent/live_review.md`: the pre-append bytes are a
     byte-exact PREFIX of the post-append bytes and the remainder equals exactly
     the concatenation named above — report both booleans and the byte lengths.
     Then report the counts, each of which must go from 0 to 1:
     `^Gate: R8 — `, `^- R-0813 — `, `^Recurrence: R-0784`, `^Done: R-0418`.
     `.agent/prose_slips.md`: same prefix property, remainder exactly
     `"\n\n" + SLIP9`, still no trailing newline.
  G3 THE FROZENFIX. FROM count 1 before and 0 after; TO count 1 after; the
     printed containment reading; and the boolean that the post-commit file
     equals the pre-commit file with that one replacement and nothing else. Then
     the per-item digest sweep: report the checklist item count (expect 36,
     numbers 1..31 and 33..37) and the number of items whose block digest
     changed, which must be ZERO — the frozen paragraph sits outside every item.
     Confirm the paragraph now contains the string `measures against 36` exactly
     once and `the number the next consolidation measures against` zero times.
  G4 THE ROTATION. Report the `--dry-run` output in full, then the real run's
     output in full, then: `wc -c` of `.agent/live_review.md` and
     `.agent/live_review_archive.md` before and after; the open-findings count
     before and after, computed as the number of `^- R-\d{4} — ` lines minus the
     number of `^Done: R-\d{4} — ` lines IN THE LEDGER, which the script
     guarantees identical across the rotation — report both numbers and say
     plainly whether they are equal; the count of `^Gate: ` records remaining in
     the ledger and the count now in the archive; and `git show --numstat <C4>`,
     which must name exactly those two paths.
  G5 THE EVIDENCE JOB — closure algorithm step 1. `git status --porcelain` empty
     first. Then call, in Python,
     `packages.orchestration.job_evidence.create_manual_completion_bundle` with:
       evidence_dir   a fresh directory under the gitignored `.remedy-wt/`
       repo_root      the primary checkout
       base_commit    25961794 (the full 40-character sha, not abbreviated)
       head_commit    the full sha of C4, measured
       job_id         16 lowercase hex characters from `secrets.token_hex(8)`
       job_title      `F259 vocabulary and concept model v1`
       step_range     `T001-T004`
       prior_job_ids  the empty list
       review_feature_id  `f259`
       timestamp / generated_at   ISO-8601 UTC
       verification_runs  ONE run, schema 1.1.0 shaped, built from a REAL run of
         `python3 -m pytest tests/docs/ -q` at C4, with these fields and no
         others: `run_id` matching `^vr-\d{4,}$`; `command` the exact command
         string; `exit_code`; `passed`; `failed`; `skipped`; `deselected`;
         `selected` EQUAL to passed+failed+skipped; `node_ids` from a real
         `--collect-only` of the same selection, whose length must EQUAL
         `selected`; `test_files` the actual FILE paths, SORTED, never a
         directory; `stdout_summary` the run's own stdout, under 4000
         characters; `output_hash` the sha256 hex of EXACTLY that
         `stdout_summary` string; `head_sha`; `duration_seconds`.
     The reviewer measured at 32808b5d: `tests/docs/` collects 303 node ids, all
     free of absolute paths and traversal, and the two test files sort as
     `tests/docs/test_docs_consistency.py` then `tests/docs/test_vocabulary.py`.
     Report the returned summary dict in full, the job id, and the final verdict
     it names. Do NOT record a full-suite node-id list anywhere in the bundle:
     the full-suite proof rides in the committed `.agent/gate_f259_r7/` evidence
     and the reviewer's own re-run.
  G6 THE REVIEW ZIP — closure algorithm step 2, MANDATORY. `git status --porcelain`
     empty first, branch pushed. Then
     `bash scripts/make_review_zip.sh --evidence-dir <the dir from G5>`.
     Report: the full stdout, the package FILENAME, its SHA-256 as the script
     printed it AND as you recompute it from the file on disk, the package's
     absolute directory, `PACKAGE_STATUS`, and the manifest's
     `committed_review_subject` base and head — which must span 25961794..C4.
     If the build does not reach READY_FOR_REVIEW, report the raw error verbatim
     and stop per constraint 10.
  G7 THE PRECONDITIONS THIS ROUND CAN ANSWER.
     `python3 -m apps.cli.grouped integrity check --json` — report `passed` and
     `fail_count`. `python3 -m pytest tests/docs/ -q` and
     `python3 -m pytest tests/cli/test_golden_path.py -q` — report both counts
     and exit codes; the reviewer measured 303 and 42 at 32808b5d.
     `python3 -m pytest tests/orchestration/test_live_review_rotation.py -q` —
     report the count and exit code, because this round runs that script for
     real. Also report `git status --porcelain` and the full list of untracked
     paths with whether each is gitignored.
  G8 THE PLAN AND THE STRUCTURE. `wc -l .agent/plan.md` under 50; one `## Goal`
     and one `## Next Steps`; `filecmp.cmp(..., shallow=False)` True against the
     slice plus one newline. Then `git status --porcelain` empty immediately
     before C5 is staged; `git ls-files .remedy-wt` returns nothing; every commit
     single-parent; `git diff --numstat <parent> <commit>` for EACH commit C0a
     through C4 reported cell by cell; each commit's insertion count against the
     500 cap, with C4 declared under the AGENTS.md DECISION F104 D1 exemption if
     the rotation's diff exceeds it — it is the verbatim rewrite of a single
     `.agent/**` state file pair; the push result; and confirmation that no pull
     request was created and that STATUS.md, README.md and
     `scripts/self_use_queue.json` are named nowhere in this round's diff.

The handback (C5) — rewrite .agent/handoff.md whole
  No length cap. It is the durable carrier for everything part 3 needs, so it
  must record, in a section a later reader can find by name: the EVIDENCE JOB ID;
  the PACKAGE FILENAME; its SHA-256; the package's ABSOLUTE DIRECTORY (DECISION
  amend0827 D1 — or the literal `NOT ARCHIVED` if it was left where it was
  built); the ACCEPTED HEAD, which is the full sha of C4 and the head the
  manifest recorded; and `PACKAGE_STATUS`. Part 3 authors the STATUS line from
  those five values, so a missing one costs a round. Beyond that: feature, round
  and SESSION NUMBER — still SESSION 1 of F259, round 9, rounds so far 9; the
  commit range; a `## Commits` table with the `+/-` numbers G8 printed; the
  AGENTS.md item-status table, one row per bundle item C0a through C5; one line
  per gate G1 through G8 with its real reading; the rotation transcript; the
  deviations; ONE sentence of context self-assessment; and the next expected
  action — the reviewer's gate, then CLOSURE PART 3: the STATUS `[x]` line, the
  README capability sync and the `consumed_by` edit in ONE commit, then the pull
  request, which is NOT merged this session. Repeat this line verbatim in its
  state block:
  `~99 % (T001–T004 ✅ · Integration Gate ✅ · Evidence + Zip gebaut · nur noch STATUS/README/PR) — Schätzung`

<<<BEGIN PLANF259R9>>>
# Plan — F259 Vocabulary & concept model v1

Branch: feature/f259-vocabulary, cut from `main` at 25961794. Rounds 1 to 8
PASSED the reviewer's gate. Round 7 was the integration gate: the full suite is
green on the branch and at the merge base, with zero branch-only and zero
base-only failures. Round 8 was closure part 1.

## Goal

`docs/system/vocabulary.md` is the BINDING vocabulary page: the DECISION
amend0905-vocab D1 table, the do-not-confuse table, the Mermaid concept diagram,
the per-word meaning table, and D2–D10 plus F259 D1/D2 as dated DECISION
paragraphs. `tests/docs/test_vocabulary.py` pins it in planned mode against the
shipped `apps/cli/command_catalog.py`; the same diagram stands in `README.md`,
byte-equal and pinned; the page is registered in `docs/README.md`. No other
code: F259 decides words, F260 and F261 spend them.

## Current Step

Round 9 is CLOSURE PART 2, the evidence half: the round-8 verdict is booked
together with the three ledger obligations the closure creates — a new finding
for the contradiction round 8's own consolidation left in the frozen paragraph,
a recurrence under the existing R-0784 rather than a second id for the self-use
run's two defect strings, and the `Done: R-0418` that SU-010's acceptance owes;
then that contradiction is repaired, the ledger is rotated, and the evidence
bundle and the FRESH review zip are built from a clean tree.

## Next Steps

- CLOSURE PART 3: the reviewer authors the STATUS `[x]` line from this round's
  measured evidence job id, package name, SHA-256, package path and accepted
  HEAD; the worker applies it with the README capability sync and the self-use
  `consumed_by` edit in ONE commit, which is the last on the branch; then the
  pull request, which is NOT merged this session but at the next feature's Open
  PR Gate.

## Risks

- A failing zip build is a closure BLOCKER, not a nuisance: it is reported raw
  and the feature does not close until it is fixed.
- The rotation rewrites the ledger. It verifies every moved record by sha256
  before and after and refuses on mismatch; a refusal stops the rotation and is
  reported, never forced.
<<<END PLANF259R9>>>

<<<BEGIN GATE_R8>>>
Gate: R8 — the F259 R8 entry, CLOSURE PART 1. VERDICT PASS. Range e10cbc30..32808b5d, eight commits, all single-parent, pushed, no pull request; largest commit 400 insertions. The change set is exactly the ordered paths and the reviewer confirmed with `git diff --name-only` that `docs/roadmap/STATUS.md` and `README.md` are named nowhere in it, which matters because the STATUS flip and the README capability sync must land in ONE commit with each other (R-0154) and that commit is part 3's. TRANSPORT: one digest `481692ac503da0cc3a803fe8bf68bb414525f421aa15021571b6a310c236334b` across `.remedy-wt/f259-r8-block.md`, `.agent/authored/f259-r8.md` and `.agent/last_block.md`, equal to the reviewer's own pre-emission digest; a COPY chain per §3 item 37. EVERY EDIT PROVED BY RECONSTRUCTION FROM THE COMMITTED BLOBS: `.agent/live_review.md` equals its parent plus exactly `"\n" + GATE_R7 + "\n"` (843 886 to 848 281 bytes); `.agent/prose_slips.md` equals its parent plus exactly `"\n\n" + SLIP8`, still ending with no newline (82 415 to 83 964); `docs/roadmap/features/T2_F259.md` equals its parent with the REGBANNER pair applied plus exactly `"\n" + BUILTSTATE + "\n"` (9 401 to 12 386), carries a `## Built State` heading and no longer contains the string `REGISTRATION ONLY`, and its single mermaid block is untouched — closure precondition 4 is met. THE ONE MANDATED CONSOLIDATION OF THE §3 CHECKLIST WAS PERFORMED AND THE REVIEWER RE-MEASURED IT INDEPENDENTLY FROM THE COMMITTED BLOBS: before, 37 items numbered 1 to 37; after, 36 items numbered 1 to 31 and 33 to 37; item 32's block hashed `695759114c327d494d21e548170eeefd74e9263db04881dd9baa8de814d8000b` before deletion, matching the value the block stated; and the per-item digest sweep shows EXACTLY ONE surviving item changed — item 16, which absorbed item 32 — with item 31 byte-IDENTICAL, which is the trap the block warned about, since deleting the block without its terminating newline would have left a stray blank line inside item 31. The list came out SHORTER, which operator amendment amend0827-process-diet rule 4 requires, and the survivors were deliberately NOT renumbered because this record cross-references those items by number from dated entries that cannot be corrected. THE SELF-USE TRACK WAS EXERCISED FOR REAL, closure precondition 6: `next_self_use_item()` answered `None` over nine consumed entries, `generate_and_append_if_empty()` appended `SU-010` (`Address ledger finding R-0418`, provenance `generated (self-use-generator tier 1, ledger scan, R-0418)`), and the runner ran it for 107.8 seconds to the approval gate and no further under `max_provider_calls=6`, `max_cost_usd=0.5`, `max_tasks=1`, producing job `1cbb6972bf7c4ffc` with status `blocked`, T001 `repair_exhausted`, reviewer verdict `fail`. Nothing was approved and nothing applied. `describe_self_use_run_defects` returned a tuple of LENGTH TWO, reported verbatim, and `consumed_by` is still the empty string — that edit belongs to the closure commit. SUITES, re-run by the reviewer: `tests/docs/` 303, `tests/test_agent_tooling.py` 10 passed and 1 skipped, `tests/orchestration/test_roadmap_index.py` 30. `python3 -m apps.cli.grouped integrity check --json` reports `passed true`, `fail_count 0` and `relevant_untracked untracked=0, relevant=0` — closure precondition 3 — though the reviewer notes for honesty that this gate's `high_blockers_open` check reports "no open blocker/high findings" while the ledger holds High findings R-0803 and R-0806, a blind spot in the gate rather than a statement about the record. TWO THINGS THE WORKER FOUND AND THE REVIEWER ACTED ON. First, the block's prose said the deletion "leaves item 31's own trailing blank line", and item 31 has no trailing blank line — the blank belonged to item 32; the instruction was nevertheless correct and the digest sweep proves it, so this is a reviewer prose slip and is recorded in `.agent/prose_slips.md` by the same commit that appends this entry. Second, and this one is a real defect on disk under `docs/`: the FROZEN pair left the paragraph asserting both that 37 "is the number the next consolidation measures against" and that "The next consolidation measures against 36", which is registered as `R-0813` immediately below and repaired by this round's own C3.
<<<END GATE_R8>>>

<<<BEGIN FIND0813>>>
- R-0813 — Low, THE CONSOLIDATION ROUND LEFT THE FROZEN PARAGRAPH NAMING TWO DIFFERENT FIGURES FOR WHAT "THE NEXT CONSOLIDATION" MEASURES AGAINST. Found by the WORKER of F259 R8, who applied the authored slice verbatim as constraint 1 required and declared the contradiction instead of silently repairing it, and confirmed by the reviewer at `32808b5d` by reading the paragraph on disk. The rule-4 paragraph of `docs/agents/planner_reviewer_prompt.md` §3 now contains, nine lines apart, `The list stood at 37 items on 2026-08-27, which is the number the next consolidation measures against.` and `The next consolidation measures against 36.` Both sentences state what the NEXT consolidation measures against and they give different numbers; the first was written on 2026-08-27 about the consolidation that F259 has now performed, and became stale the moment that consolidation landed. PRODUCT EFFECT, which is why this spends an id rather than a `.agent/prose_slips.md` line under operator amendment amend0827-process-diet rule 2: the wrong state is on disk under `docs/`, in the document that governs every reviewer's pre-emission discipline, and a later consolidation reading the stale sentence would measure against 37 and could therefore GROW the list to 37 while believing it had obeyed the same-length-or-shorter rule. Low rather than Medium because both figures are individually true of something, the corrected sentence stands beside the stale one rather than replacing it, and the next consolidation is a whole feature away. ROOT CAUSE, stated so the class is visible: the reviewer authored an APPEND to a paragraph without re-reading the paragraph's EXISTING sentences for claims the appended text would contradict — §3 item 6 binds a zero-gate to the target's existing content and item 34 binds an order to the file it is written into, and neither was applied to the PROSE of the very paragraph being extended. Searched before minting per §3 item 30: `grep` over the open set for `frozen`, `consolidat` and `checklist` finds `R-0387`, `R-0411`, `R-0461` and `R-0604`, none of which describes a stale numeral in this paragraph, and the defect did not exist before F259 R8 created it. FIX, applied by this round's own C3 as a single REWRITE pair: the 2026-08-27 sentence is re-worded to name itself as the figure the FIRST consolidation measured against, leaving exactly one sentence in the paragraph that says what the next one measures against. Resolved when `docs/agents/planner_reviewer_prompt.md` contains `measures against 36` exactly once and `the number the next consolidation measures against` zero times, and the per-item digest sweep shows no checklist item changed.
<<<END FIND0813>>>

<<<BEGIN REC0784>>>
Recurrence: R-0784 — the same defect, at F259's closure. Closure precondition 6 requires every string `packages.orchestration.self_use_findings.describe_self_use_run_defects` returns for the closing run to be registered before the close, and F259 R8's run of `SU-010` returned two: `job 1cbb6972bf7c4ffc (blocked): task_T001_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail` and `T001 (blocked): completion_gate_failed: final_status=repair_exhausted; reviewer_verdict=fail`. These are the SAME defect `R-0784` already holds open — the job-level and task-level views of one gate failure, in a self-use run that exhausted its repair rounds — differing from the entry above only in the job id and the queue item. NO NEW ID IS MINTED, per §3 item 30: the reviewer searched the open set for the DEFECT before writing, found `R-0784` describing it in as many words, and `R-0784`'s own text already rules that the two strings are one defect and take one id. Registering `R-0814` here would give one defect two things to resolve, two things to carry forward and two chances to fix it half-way, which is precisely what that item forbids. The evidence is added to the open finding instead, which is this paragraph. WHAT IS NEW AND WORTH RECORDING: this is the SIXTH consecutive closure whose self-use item was generated from the same ledger source. The generator's tier 1 takes the OLDEST open Low or Medium finding, that finding has been `R-0418` since F110, and each closure has therefore run a job whose task was to repair a rule about REVIEWER AUTHORING PRACTICE — work no builder can do, which is why every one of those runs ended `repair_exhausted`. F259 breaks that loop from the other end: it pays `R-0418` off by demonstrated compliance rather than by another failing run, as the `Done: R-0418` paragraph below records, so the generator's tier 1 will offer a DIFFERENT finding at the next closure. Whether the runner should refuse a task whose subject is a reviewer-practice rule remains open under `R-0784`.
<<<END REC0784>>>

<<<BEGIN DONE0418>>>
Done: R-0418 — RESOLVED by demonstrated compliance, which is the branch its own acceptance offers for a finding that has no code to turn red. R-0418 is a rule about REVIEWER BLOCK-AUTHORING PRACTICE under docs/agents/self_drive_protocol.md: its fix clause states that in self-drive, where the worker is a delegated subagent that never sees the reviewer's operator brief, every block requiring the handoff to carry the Fortschritt line must CONTAIN that line as authored text or must not order it — because an instruction to repeat something from a brief the worker cannot read is unsatisfiable by construction, the R-0371 class. The acceptance carried on the self-use queue item that has re-raised this finding at every closure since F110 reads: "R-0418 is repaired with a red-to-green proof, or the reviewer records in `.agent/live_review.md` why it cannot be — either way the ledger gains a `Done: R-0418` line." WHY NO RED-TO-GREEN PROOF EXISTS, recorded as that acceptance asks: the subject is a rule binding the author of a paste block, not a code path, so there is no branch to mutate and no test that could go red; the five self-use runs that tried — SU-005 through SU-010, one per closure — each ended `repair_exhausted` for exactly that reason, and a sixth would too. WHAT WAS MEASURED INSTEAD, by the reviewer at `32808b5d`: every one of F259's seven build-round blocks, as COMMITTED under `.agent/authored/`, contains the Fortschritt line as authored literal text rather than ordering the worker to fetch it — `f259-r1.md` through `f259-r7.md`, seven files, seven matches of a backtick-quoted line ending `— Schätzung`, and every one of the seven handbacks carries the corresponding line. The rule is therefore not merely stated but followed for a full feature, by the role it binds, under the workflow that created the defect. This resolution does NOT claim the rule can no longer be broken; it claims the finding has been discharged in the only currency it accepts. The neighbouring question — whether the self-use RUNNER should refuse a task whose subject is a reviewer-practice rule instead of burning two repair rounds on it — stays open under `R-0784`, which the recurrence paragraph above names.
<<<END DONE0418>>>

<<<BEGIN SLIP9>>>
2026-09-06 · F259 R8 (reviewer) · The round-8 block's consolidation instruction said the item-32 deletion "leaves item 31's own trailing blank line followed directly by item 33", and item 31 has NO trailing blank line — the blank line the sentence attributes to item 31 was the last line of item 32's own block. The instruction itself was correct and the round's per-item digest sweep proves item 31 byte-identical; only the reviewer's account of WHOSE bytes those were is wrong, which the worker measured and declared. THE LESSON: when a block explains what a deletion will leave behind, the explanation is a claim about the target's existing bytes and is measured like any other — §3 item 34 reaches it, and the same probe that produced the block's digest could have produced the adjacency reading for free. Reviewer-authored prose inaccuracy in an `.agent/` block; nothing on disk under `packages/`, `apps/`, `tests/` or `docs/` is wrong as a result, and the separate defect that round DID leave under `docs/` is registered as `R-0813` rather than recorded here; no R-id spent for this one (amend0827-process-diet rule 2).
<<<END SLIP9>>>

<<<BEGIN FROZENFIX_FROM>>>
  move, growing the list is forbidden. The list stood at 37 items on
  2026-08-27, which is the number the next consolidation measures against.
<<<END FROZENFIX_FROM>>>

<<<BEGIN FROZENFIX_TO>>>
  move, growing the list is forbidden. The list stood at 37 items on
  2026-08-27, which is the figure the FIRST consolidation measured against.
<<<END FROZENFIX_TO>>>
