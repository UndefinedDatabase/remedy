STEP CLOSURE PART 2 / F260 — One world: mission, job, run — round 22 of session 8
BRANCH feature/f260-one-world, head 941846d7c9afd3c633a61ebbef15b62bb283f413 at
the time this block was written.
MERGE BASE f957c4c6dede34e9ba9d3653ae01cc16157b96fc.

Goal
  The evidence half of the closure sequence. Book round 21's PASS, which operator
  amendment amend0827-process-diet rule 1 left standing in the pushed
  `.agent/handoff.md` rather than in the ledger; rotate the ledger; then build the
  evidence bundle and the FRESH review zip from a clean tree. The STATUS `[x]`
  flip, the README capability sync, the `consumed_by` edit and the pull request
  are part 3, because the STATUS line cannot be authored until this round has
  measured the evidence job id, the package name, its SHA-256, the package's
  absolute directory and the accepted head.

Why this round books a verdict and registers nothing else
  Round 21 PASSED with no finding. The reviewer of round 22 re-measured every
  number in the GATE_R21 slice against this worktree before writing it, rather
  than copying the handback's, and every one reproduced: the six commits and their
  insertion counts, the transport digest, the three byte transitions, the repair's
  before-and-after, the 35-item checklist with gaps at 19 and 32, and the whole
  census including the open set of 298 by distinct id. NO NEW ID IS MINTED THIS
  ROUND and no `Done:` line is authored, so the open set must not move.

Bundle, in this order (one commit each)
  C0a save this block file to .agent/authored/f260-r22.md (copy, never retype)
  C0b mirror it to .agent/last_block.md (same copy route, same source file)
  C1  .agent/plan.md <- PLANF260R22 (whole rewrite). This is the round's FIRST
      substantive commit, per checklist item 23: a round that touches the finding
      ledger advances the plan first, and only the two block-save commits may
      precede it.
  C2  THE BOOKING (§4 item 4, findings persist first). `.agent/live_review.md`:
      append GATE_R21 by the recipe below. One commit, one path.
  C3  THE LEDGER ROTATION, its own commit, paths `.agent/live_review.md` and
      `.agent/live_review_archive.md` ONLY:
      `python3 scripts/rotate_live_review.py`. Run `--dry-run` FIRST and report
      its output, then the real run and report that too.
      Then push. Then, from the CLEAN TREE at that head, and committing nothing:
      the evidence job (G5) and the review zip (G6).
  C4  rewrite .agent/handoff.md, which records the zip outcome; push again.

  Create NO pull request. Do NOT touch `docs/roadmap/STATUS.md`, `README.md` or
  `scripts/self_use_queue.json` — all three belong to part 3's single closure
  commit, which must carry them together (R-0154, the README/STATUS agreement
  pin).

Change set — EXACTLY these paths and nothing else
  .agent/authored/f260-r22.md (C0a) — .agent/last_block.md (C0b) —
  .agent/plan.md (C1) — .agent/live_review.md (C2) —
  .agent/live_review.md, .agent/live_review_archive.md (C3) —
  .agent/handoff.md (C4)

Delivery
  This block is at `.remedy-wt/f260-r22-block.md`, gitignored scratch. C0a COPIES
  that file to .agent/authored/f260-r22.md with `shutil.copyfile`, C0b copies the
  SAME source file to .agent/last_block.md. Never retype either. Slices are
  extracted from the COMMITTED authored file after C0a, by matching lines EXACTLY
  equal to `<<<BEGIN name>>>` and `<<<END name>>>` by position, asserting exactly
  one of each, and joining the lines between them with a newline — so an extracted
  slice carries NO trailing newline of its own.

The C2 append
  `.agent/live_review.md` ends with exactly one newline; assert that from the
  file's own measured terminal byte BEFORE writing, never from a number in this
  block. Then append, in ONE write, the pre-image followed by a newline, the
  GATE_R21 slice, and a newline — so the file gains one blank line, then the
  record, and still ends with exactly one newline. GATE_R21 is a single-line
  paragraph and contains no newline of its own.

Constraints
  1. Slices are applied BYTE FOR BYTE from the committed authored file by marker
     extraction in Python. If you believe a slice is wrong, apply it verbatim
     anyway and declare it in the handback.
  2. Read `.agent/STOP` from disk before C0a, before C3 and before C4. If it
     exists, finish any half-written commit, write the handback and end.
  3. NEWLINE CONVENTIONS: PLANF260R22 replaces `.agent/plan.md` whole with the
     slice plus exactly one trailing newline; the C2 append is exactly as
     described above. Every append recipe is derived from ITS OWN target's
     measured terminal byte, with the assert executed BEFORE the write.
  4. NO ID IS MINTED AND NO `Done:` OR `Landed:` LINE IS AUTHORED. The open set
     must read the same after C2 as before it.
  5. THE ROTATION IS ITS OWN COMMIT AND TOUCHES TWO PATHS. If the script refuses,
     STOP the rotation: commit nothing for C3, report the refusal text verbatim,
     and continue to the evidence job and the zip — a refused rotation is
     reported, never forced.
  6. THE EVIDENCE DIRECTORY IS NEVER COMMITTED. Put it OUTSIDE the review subject,
     under the gitignored `.remedy-wt/`. A pre-committed evidence dir puts
     evidence files into the reviewed range and the package builds
     BLOCKED_EVIDENCE.
  7. THE TREE IS CLEAN when the evidence job and the zip run. A package built from
     a dirty tree is invalid. Report `git status --porcelain` immediately before
     each.
  8. This session's shell guard refuses some command FORMS outright — shell loops,
     command substitution with parentheses, `$?` inside a compound command,
     `${PIPESTATUS[0]}`, a `$` anchor inside a `grep -c` pattern, and a non-ASCII
     character in a Python bytes literal. Re-express in Python and report the
     Python you ran beside its output, quoting any refusal verbatim. `cmp` may be
     replaced by `filecmp.cmp(shallow=False)` plus sha256. The built `remedy`
     binary is denied; use `python3 -m apps.cli.grouped <...>` where a remedy
     subcommand is needed. Read every exit code from
     `subprocess.run(...).returncode`, never from a word.
  9. Commit subjects are `f260: <what>`. No leading-slash token, no absolute path,
     no secret-like string — the evidence metadata scanner rejects such subjects
     and would block this very closure. End every commit message with the trailer
     `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.
 10. AGENTS.md binds you in full. Never `--force`, never a history rewrite, never
     `gh pr merge`, never a branch deletion, never a commit on `main`. C4 is ONE
     commit.
 11. A FAILING ZIP BUILD IS A CLOSURE BLOCKER, not something to work around.
     Record the raw error, commit the handback saying so, and stop; the reviewer
     decides. Never close without the package.
 12. Helper scripts go under the gitignored `.remedy-wt/` and are never `git
     add`ed. Create no git worktree; nothing this round is destructive.

Done when — the gates. Real exit codes, real output, one line per gate in the
handback. EVERY gate runs at or before the zip; none is ordered after C4, so the
handback can quote all of them (checklist item 31). C4's own insertion count and
byte length are reported NOWHERE — under self-drive there is no round report, and
the reviewer measures those at the next gate.

  G1 TRANSPORT. sha256 and byte length of `.remedy-wt/f260-r22-block.md`,
     `.agent/authored/f260-r22.md` and `.agent/last_block.md` — one digest, three
     times — plus `filecmp.cmp(shallow=False)` True for source-vs-saved and
     source-vs-mirror. Measured BEFORE C0a is staged. The delegation states the
     digest; verify against it BEFORE executing anything else in this block.
  G2 THE RECORD. Three readings over `.agent/live_review.md`, which is the append
     into the record and therefore earns full byte forensics under the gate budget.
     (a) BYTE: the post-image equals the pre-image followed by a newline, the
         GATE_R21 slice and a newline; and the pre-image is a byte-exact PREFIX of
         the post-image. Report both booleans, the pre and post byte lengths and
         their delta, and that the file ends in exactly one newline.
     (b) STRUCTURAL, independently of (a): split the WHOLE file image on the regex
         for two-or-more consecutive newlines, drop units that are empty after
         stripping, and strip each surviving unit of leading and trailing
         newlines. Report the unit count before and after. N is COUNTED BY YOUR
         SCRIPT from the slice's own paragraphs and is never taken from this
         block; the last N units must equal the slice's paragraphs IN ORDER.
     (c) NEGATIVE CONTROL, in memory on a `bytes` object and never on disk: pick a
         byte offset your script first ASSERTS lies inside the FIRST appended
         paragraph, XOR that byte with 0x20, and report that reader (a) REJECTS
         and reader (b) REJECTS; then restore it and report that both ACCEPT and
         that the restored image equals the disk image.
     Then the counts, over the whole file, before and after: `^Gate: ` and
     `^Gate: R21 — `. The second goes from 0 to exactly 1.
  G3 THE PLAN. `.agent/plan.md` equals the PLANF260R22 slice plus exactly one
     trailing newline — report the boolean and the byte length you measured; its
     line count, which must be under the AGENTS.md cap of 50; and that it carries
     `## Goal` and `## Next Steps`. A `.agent/` prose file earns a byte-equality
     check and nothing heavier, per the gate budget.
  G4 THE ROTATION. Report the `--dry-run` output in full, then the real run's
     output in full. Then: the byte size of `.agent/live_review.md` and
     `.agent/live_review_archive.md` before and after; the open-findings count
     before and after AS THE SCRIPT PRINTS THEM, and say plainly whether the two
     are equal — that equality is the property, not any particular number; the
     `^Gate: ` count remaining in the ledger and the count now in the archive; and
     `git show --numstat <C3>`, which must name exactly the two paths above.
     Finally, confirm `^Gate: R21 — ` still counts exactly 1 IN THE LEDGER after
     the rotation. F260 is `[~]` in `docs/roadmap/STATUS.md` at this commit, so
     its records are not movable, and this reading is what proves the booking
     survived the rotation rather than being archived by it.
  G5 THE EVIDENCE JOB — closure algorithm step 1. `git status --porcelain` empty
     first. Then call, in Python,
     `packages.orchestration.job_evidence.create_manual_completion_bundle` with:
       evidence_dir   a fresh directory under the gitignored `.remedy-wt/`
       repo_root      the primary checkout
       base_commit    f957c4c6dede34e9ba9d3653ae01cc16157b96fc — the full
                      40-character merge base, never abbreviated
       head_commit    the full sha of C3, measured
       job_id         16 lowercase hex characters from `secrets.token_hex(8)`
       job_title      `F260 one world mission job run`
       step_range     `T001-T002`
       prior_job_ids  the empty list
       review_feature_id  `f260`
       timestamp / generated_at   ISO-8601 UTC
       verification_runs  ONE run, built from a REAL run of
         `python3 -m pytest tests/docs/ -q` at C3, with these fields and no
         others: `run_id` matching the pattern `vr-` followed by four or more
         digits; `command` the exact command string; `exit_code`; `passed`;
         `failed`; `skipped`; `deselected`; `selected` EQUAL to
         passed+failed+skipped; `node_ids` from a real `--collect-only` of the
         SAME selection, whose length must EQUAL `selected`; `test_files` the
         actual FILE paths, SORTED, never a directory; `stdout_summary` the run's
         own stdout, under 4000 characters; `output_hash` the sha256 hex of
         EXACTLY that `stdout_summary` string; `head_sha`; `duration_seconds`.
     The reviewer measured at 941846d7: `tests/docs/` collects 303 node ids, none
     of them holding an absolute path or a parent-directory traversal, and the two
     test files sort as `tests/docs/test_docs_consistency.py` then
     `tests/docs/test_vocabulary.py`. Report the returned summary dict in full,
     the job id, and the final verdict it names. Do NOT record a full-suite
     node-id list anywhere in the bundle: the equality of `node_ids` length and
     `selected` forbids filtering, and the metadata scan correctly rejects the
     redaction-torture parametrizations whose ids embed fake secrets by design.
     The full-suite proof rides in the committed round-19 integration-gate
     evidence and in the reviewer's own re-run.
  G6 THE REVIEW ZIP — closure algorithm step 2, MANDATORY and never skipped.
     `git status --porcelain` empty first, branch pushed. Then
     `bash scripts/make_review_zip.sh --evidence-dir <the dir from G5>`.
     Report: the full stdout; the package FILENAME; its SHA-256 as the script
     printed it AND as you recompute it from the file on disk; the package's
     ABSOLUTE directory; `PACKAGE_STATUS`; and the manifest's
     `committed_review_subject` base and head, which must span
     f957c4c6dede34e9ba9d3653ae01cc16157b96fc..C3. If the build does not reach
     READY_FOR_REVIEW, report the raw error verbatim and stop per constraint 11.
  G7 THE PRECONDITIONS THIS ROUND CAN ANSWER, run SERIALLY in the primary
     checkout. `python3 -m apps.cli.grouped integrity check --json` — report
     `passed` and `fail_count`. `python3 -m pytest tests/docs/ -q -p no:randomly`
     and `python3 -m pytest tests/cli/test_golden_path.py -q -p no:randomly` —
     report both counts and exit codes; the reviewer measured 303 and 42 at
     941846d7. `python3 -m pytest tests/orchestration/test_live_review_rotation.py
     -q -p no:randomly` — report the count and exit code, because this round runs
     that script for real; the reviewer measured 10 at 941846d7. Report `git
     status --porcelain` and the full list of untracked paths, saying for each
     whether it is gitignored.
  G8 STRUCTURE AND TREE. `git status --porcelain` EMPTY immediately before C4 is
     staged; `git ls-files .remedy-wt` returns nothing. Every commit
     single-parent. `git diff --numstat <parent> <commit>` reported cell by cell
     for EACH of C0a, C0b, C1, C2 and C3 — the insertions column only, which is
     the count AGENTS.md DECISION F104 D1 caps at 500, never insertions plus
     deletions — and each one's reading against that cap, with C3 declared under
     the same decision's `.agent/**` state-write exemption if the rotation's diff
     exceeds it. Report the push result; that NO pull request was created; and
     that `docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json`
     are named NOWHERE in this round's diff. Also report the number of marker
     lines beginning with the BEGIN prefix or the END prefix that reached
     `.agent/plan.md` or `.agent/live_review.md`, which must be zero in each.

The handback (C4) — rewrite .agent/handoff.md whole
  No length cap (amend0827 rule 3). It is the durable carrier for everything part
  3 needs, so it must record, in a section a later reader can find BY NAME: the
  EVIDENCE JOB ID; the PACKAGE FILENAME; its SHA-256; the package's ABSOLUTE
  DIRECTORY (DECISION amend0827 D1 — or the literal `NOT ARCHIVED` if it was left
  where it was built); the ACCEPTED HEAD, which is the full sha of C3 and the head
  the manifest recorded; and `PACKAGE_STATUS`. Part 3 authors the STATUS line from
  those values, so a missing one costs a round.
  Beyond that: feature, round and SESSION NUMBER — SESSION 8 of F260, round 22,
  rounds so far 22; the commit range; a `## Commits` table whose insertion and
  deletion cells are the numbers G8 printed from `git diff --numstat`, compared
  cell by cell against that tool rather than re-derived by eye (checklist item
  28); the AGENTS.md item-status table with one row per bundle item C0a through
  C4; one line per gate G1 through G8 with its real reading; the rotation
  transcript; the deviations; ONE sentence of context self-assessment
  (amend0905-throughput); and the next expected action — the reviewer's gate, then
  CLOSURE PART 3: the STATUS `[x]` line, the README capability sync and the
  `consumed_by` edit in ONE commit, then the pull request, which is NOT merged
  this session. State plainly that F260 is at its 7-session soft limit and that
  DECISION F260 D8's split-and-close is the authority for closing at the built
  scope. Repeat this line verbatim in its state block:
  `~99 % (T001 komplett, T002 Run-Haelfte, Integration Gate gruen, Evidence + Zip gebaut, nur noch STATUS/README/PR) — Schaetzung`

<<<BEGIN PLANF260R22>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world. Rounds 1 to 21 are reviewed; round 1 FAILED and was
repaired, and 2 to 21 PASSED. DECISION F260 D8 closes this feature at the scope it
built; F272 carries the remainder and was registered in round 18, directly after
F260 in the ledger.

## Goal

SESSION 8 finishes the closure sequence. This round is CLOSURE PART 2, the evidence
half: book round 21's verdict, rotate the ledger, then build the evidence bundle and
the FRESH review zip from a clean tree. The STATUS flip is the part after it.

## Current Step

Round 22 books round 21's PASS into `.agent/live_review.md` as the `Gate: R21`
record, rotates the ledger into `.agent/live_review_archive.md` as its own commit,
and then — committing nothing further — runs the evidence job and builds the review
zip. The handback carries the evidence job id, the package filename, its SHA-256,
the package's absolute directory and the accepted head, because the STATUS line
cannot be authored until those values are measured.

## Next Steps

1. CLOSURE PART 3: the STATUS `[x]` flip and the README capability sync in ONE
   commit, with `consumed_by` set to `F260` on SU-011 in that same commit, then the
   handback, then the pull request — left UNMERGED as the operator's review window.

## Risks

- SU-011 is PENDING and must be marked consumed in the closure commit, not before.
  Nothing else may set it.
- A failing zip build is a closure BLOCKER, not a nuisance: it is reported raw and
  the reviewer decides.
- The rotation re-bases every byte baseline, so the block after it measures its own
  terminal bytes rather than reusing any number from this session.
<<<END PLANF260R22>>>
<<<BEGIN GATE_R21>>>
Gate: R21 — the F260 R21 entry, THE ROUND 20 BOOKINGS AND ONE REPAIR. VERDICT PASS. Range `addca04a05034afa32e50e8e243f17a6ab8cb5df`..`e9a15db100ca497399ea02c0eb536f55f02ac4ce`, six commits, every one single-parent, in exactly the bundle's ordered sequence C0a, C0b, C1, C2, C3, C4 with nothing added, dropped or reordered; insertion counts 232, 156, 19, 6, 2 and 216, walked commit by commit with `git rev-list --reverse` rather than generalised, every one far under the 500 cap and the two largest exempt under AGENTS.md DECISION F104 D1 as single `.agent/**` state writes. The verdict itself was appended to `.agent/handoff.md` at `941846d7c9afd3c633a61ebbef15b62bb283f413` under operator amendment amend0827-process-diet rule 1, which makes a pushed handback a durable carrier, and this entry is that verdict booked into the record by the first ledger commit of round 22 — the closure sequence being the one place a bookkeeping commit is permitted. THE REVIEWER OF ROUND 22 RE-MEASURED EVERY NUMBER IN THIS ENTRY ITSELF rather than copying the handback's. TRANSPORT: `.agent/authored/f260-r21.md` at `4324ddc9` and `.agent/last_block.md` at `f5e70d84` are both 22504 bytes and both hash to `ae2ef0118ef7627a69db02044452e4c96adf2d641c7260dcb5bc813a48da1984`; per §3 item 37 that chain covers the saved copy and its mirror, and is not a claim about the bytes emitted into a prompt. THE RECORD, at `1e3c7c9a`: `.agent/live_review.md` 974830 to 983418 bytes and `.agent/prose_slips.md` 125380 to 126730 bytes, each equal to its pre-image plus its own append recipe exactly and each with the pre-image a byte-exact prefix; `.agent/plan.md` at `00e39d7a` equals its slice plus one newline at 1869 bytes and 37 lines, under the 50-line cap. THE REPAIR, which is why round 21 existed: `docs/agents/planner_reviewer_prompt.md` went 92539 to 92529 bytes under the single FIXPAIR, and the garbled phrase round 20's CONS2 slice landed — `former item 32-neighbour`, wrong twice over because item 19 sat between 18 and 20 and 32 is the number F259 retired — occurs ZERO times in that file at `2d3cdad8`. The consolidation it sat inside is undisturbed: counted mechanically on the committed file inside the region bounded by the two anchor lines that were each asserted unique, the checklist holds 35 items with gaps at exactly 19 and 32 and no duplicate, the same reading before and after the repair. THE OPEN SET DID NOT MOVE, which is the point of registering a recurrence rather than an id; measured over `.agent/live_review.md` at `941846d7c9afd3c633a61ebbef15b62bb283f413`, before this entry was appended: `^Gate: ` 30 with `^Gate: R20 — ` at exactly 1, registrations 301 over 301 DISTINCT ids, `^Done: R-dddd — ` 5 lines over THREE distinct ids (`R-0721`, `R-0725`, `R-0814`), OPEN SET 298 BY DISTINCT ID, `^Recurrence: R-0784` at 2 — F259's closure and this one — and the highest registered id still `R-0816`, which is the proof that no new id was minted for the self-use run's two defect strings. SUITES re-run by the reviewer, serially, in the primary checkout: `tests/docs/` exit 0 at 303 passed, the canary `tests/cli/test_golden_path.py` exit 0 at 42 passed, and `python3 -m apps.cli.grouped integrity check --json` exit 0 with `"passed": true` and `"fail_count": 0`. `git status --porcelain` EMPTY and `git ls-files .remedy-wt` EMPTY at `941846d7c9afd3c633a61ebbef15b62bb283f413`. FIVE ITEMS WERE DECLARED AND ALL FIVE ARE UPHELD, and two of them are the round correcting its own instruments rather than the evidence, which is the right direction in both cases: the worker's first checklist counter read 39 items with a duplicate set because its region bounds also caught the verification-tier list, so it fixed the READER and re-anchored the region on two lines it asserted unique; and it stated its blank-line splitter's exact definition so the reviewer could reproduce it rather than match a phrase. SESSION 7 ENDED AT THIS ROUND, and the reason is on the record rather than implied: operator amendment amend0905-throughput names the reviewer noticing its own authoring errors accumulating as an honest end condition and defines that signal as a run of `.agent/prose_slips.md` lines in one session, and session 7 wrote six — SLIP21 through SLIP26 — of which SLIP26 is the one that LANDED IN A COMMITTED DOCS FILE and cost round 21 to repair it.
<<<END GATE_R21>>>
