STEP CLOSURE PART 2 REDONE / F260 — One world: mission, job, run — round 23 of session 8
BRANCH feature/f260-one-world, head 18787ffa at the time this block was written.
THE CORRECT REVIEW BASE IS b5cd6c20782283923f0e276d9479751e475b9359, the branch's
fork point. It is NOT f957c4c6, which round 22 was wrongly ordered to use.

Goal
  Round 22 did everything it was asked and its review package still built
  BLOCKED_EVIDENCE, because the block ordered the wrong `base_commit`. This round
  books that verdict, registers the docs gap behind it as `R-0817`, repairs the
  gap, and then REBUILDS the evidence bundle and the review zip from the correct
  base. The STATUS flip, the README sync, the `consumed_by` edit and the pull
  request stay in the round after this one, because the STATUS line cannot be
  authored until this round has measured the new job id, package name, SHA-256,
  package path and accepted head.

What went wrong in round 22, stated so you can check it rather than trust it
  `packages/orchestration/review_subject.py` builds the packaged commit chain with
  `rev-list --ancestry-path --reverse <base>..<head>`. This branch merged `main`
  IN at `7ed25b88`, so `git merge-base HEAD main` answers `f957c4c6` — main's own
  tip at that merge — and NOT the branch's fork point. Every commit this branch
  made BEFORE that merge fails to descend from `f957c4c6`, so `--ancestry-path`
  drops it while the `base..head` diff still carries its effect. The
  one-directional check in `scripts/build_review_manifest.py` then reports "the
  review subject claims committed changes no packaged commit made". The reviewer
  measured both bases at `6cebdce6` with the product's own
  `_is_source_for_alignment` predicate: from `f957c4c6` the ancestry chain is 41
  against a plain `rev-list` of 158, leaving 58 source paths unexplained; from
  `b5cd6c20` it is 160 against 160, leaving none. NOTHING IS WRONG WITH THE
  PACKAGING CODE — the validator caught a real inconsistency and refused, which is
  it working. What was missing is a line in the closure protocol's own pitfall
  list, and that is what `R-0817` registers and C3 repairs.

Bundle, in this order (one commit each)
  C0a save this block file to .agent/authored/f260-r23.md (copy, never retype)
  C0b mirror it to .agent/last_block.md (same copy route, same source file)
  C1  .agent/plan.md <- PLANF260R23 (whole rewrite). FIRST substantive commit,
      per checklist item 23.
  C2  FINDINGS PERSIST FIRST (§4 item 4). `.agent/live_review.md`: append GATE_R22
      then FIND0817, in that order, by the recipe below. `.agent/prose_slips.md`:
      append SLIP27 by its own recipe. ONE commit; write the ledger FIRST within
      it.
  C3  docs/roadmap/STATUS_closure_protocol.md: apply the single PITFALL pair.
      then push. Then, from the CLEAN TREE at that head, and committing nothing:
      the evidence job (G5) and the review zip (G6).
  C4  rewrite .agent/handoff.md, which records the zip outcome; push again.

  Create NO pull request. Do NOT touch `docs/roadmap/STATUS.md`, `README.md` or
  `scripts/self_use_queue.json` — all three belong to the NEXT round's single
  closure commit, which must carry them together (R-0154). Do NOT author a
  `Done: R-0817` line: only the reviewer sets Resolved, and it is authored at the
  next gate (§4 item 4).

Change set — EXACTLY these paths and nothing else
  .agent/authored/f260-r23.md (C0a) — .agent/last_block.md (C0b) —
  .agent/plan.md (C1) — .agent/live_review.md, .agent/prose_slips.md (C2) —
  docs/roadmap/STATUS_closure_protocol.md (C3) — .agent/handoff.md (C4)

Delivery
  This block is at `.remedy-wt/f260-r23-block.md`, gitignored scratch. C0a COPIES
  that file to .agent/authored/f260-r23.md with `shutil.copyfile`, C0b copies the
  SAME source file to .agent/last_block.md. Never retype either. Slices are
  extracted from the COMMITTED authored file after C0a, by matching lines EXACTLY
  equal to `<<<BEGIN name>>>` and `<<<END name>>>` by position, asserting exactly
  one of each, and joining the lines between them with a newline — so an extracted
  slice carries NO trailing newline of its own.

The C2 appends
  Both targets end with exactly one newline; assert that from each file's OWN
  measured terminal byte BEFORE writing, never from a number in this block.
  `.agent/live_review.md`, in ONE write: the pre-image, a newline, GATE_R22, a
  blank line, FIND0817, a newline — so the two records land in that order, each
  separated from its neighbour by one empty line, and the file still ends with
  exactly one newline.
  `.agent/prose_slips.md`, in ONE write: the pre-image, a newline, SLIP27, a
  newline.
  GATE_R22, FIND0817 and SLIP27 are each a single-line paragraph and contain no
  newline of their own.

The PITFALL pair (C3)
  Applied with `str.replace(FROM, TO, 1)` after asserting FROM occurs EXACTLY
  ONCE. The reviewer ran the containment test before emission and it printed
  `TO contains FROM: true`, so this is an APPEND-shaped pair. Per §4 item 9 the
  obligation is therefore FROM exactly 1x and each TO-ONLY added line exactly 1x
  AMONG THE LINES THAT COMMIT'S DIFF ADDS — NOT a FROM-zero count, which is
  unattainable by construction for an append and must not be reported.

Constraints
  1. Slices are applied BYTE FOR BYTE from the committed authored file by marker
     extraction in Python. If you believe a slice is wrong, apply it verbatim
     anyway and declare it in the handback.
  2. Read `.agent/STOP` from disk before C0a, before C3 and before C4. If it
     exists, finish any half-written commit, write the handback and end.
  3. NEWLINE CONVENTIONS: PLANF260R23 replaces `.agent/plan.md` whole with the
     slice plus exactly one trailing newline; the C2 appends are as described
     above; `docs/roadmap/STATUS_closure_protocol.md` still ends with exactly one
     newline after C3. Every append recipe is derived from ITS OWN target's
     measured terminal byte, with the assert executed BEFORE the write.
  4. EXACTLY ONE ID IS MINTED THIS ROUND, `R-0817`, and NO `Done:` or `Landed:`
     line is authored. The open set by DISTINCT id must go up by exactly one.
  5. THE BASE IS `b5cd6c20782283923f0e276d9479751e475b9359` AND YOU PROVE IT
     BEFORE YOU USE IT — see G5's first reading. If that proof fails, do not call
     the bundle producer: report the counts and stop.
  6. THE EVIDENCE DIRECTORY IS NEVER COMMITTED. Put it in a FRESH directory under
     the gitignored `.remedy-wt/`, not the one round 22 used. A pre-committed
     evidence dir puts evidence files into the reviewed range and the package
     builds BLOCKED_EVIDENCE.
  7. THE TREE IS CLEAN when the evidence job and the zip run. A package built from
     a dirty tree is invalid. Report `git status --porcelain` immediately before
     each.
  8. This session's shell guard refuses some command FORMS outright — shell loops,
     command substitution with parentheses, `$?` inside a compound command,
     `${PIPESTATUS[0]}`, a `$` anchor inside a `grep -c` pattern, an `=` that
     reads as an equals-expansion, and a non-ASCII character in a Python bytes
     literal. Write the Python to a file under `.remedy-wt/` and run that file
     rather than fighting the guard inline; report the Python you ran beside its
     output, quoting any refusal verbatim. `cmp` may be replaced by
     `filecmp.cmp(shallow=False)` plus sha256. The built `remedy` binary is
     denied; use `python3 -m apps.cli.grouped <...>`. Read every exit code from
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
     decides. Never close without the package. In particular: do NOT change the
     base, the evidence fields or any source file to make the package go READY.
 12. Helper scripts go under the gitignored `.remedy-wt/` and are never `git
     add`ed. Create no git worktree; nothing this round is destructive.

Done when — the gates. Real exit codes, real output, one line per gate in the
handback. EVERY gate runs at or before the zip; none is ordered after C4, so the
handback can quote all of them (checklist item 31). C4's own insertion count and
byte length are reported NOWHERE — under self-drive there is no round report, and
the reviewer measures those at the next gate.

  G1 TRANSPORT. sha256 and byte length of `.remedy-wt/f260-r23-block.md`,
     `.agent/authored/f260-r23.md` and `.agent/last_block.md` — one digest, three
     times — plus `filecmp.cmp(shallow=False)` True for source-vs-saved and
     source-vs-mirror. Measured BEFORE C0a is staged. The delegation states the
     digest; verify against it BEFORE executing anything else in this block.
  G2 THE RECORD. Three readings over `.agent/live_review.md`, which is the append
     into the record and therefore earns full byte forensics under the gate budget.
     (a) BYTE: the post-image equals the pre-image followed by a newline, GATE_R22,
         a blank line, FIND0817 and a newline; and the pre-image is a byte-exact
         PREFIX of the post-image. Report both booleans, the pre and post byte
         lengths and their delta, and that the file ends in exactly one newline.
     (b) STRUCTURAL, independently of (a): split the WHOLE file image on the regex
         for two-or-more consecutive newlines, drop units that are empty after
         stripping, and strip each surviving unit of leading and trailing
         newlines. Report the unit count before and after. N is COUNTED BY YOUR
         SCRIPT from the slices' own paragraphs and is never taken from this
         block; the last N units must equal those paragraphs IN ORDER, and you
         report which unit is which.
     (c) NEGATIVE CONTROL, in memory on a `bytes` object and never on disk: pick a
         byte offset your script first ASSERTS lies inside the FIRST appended
         paragraph — that is GATE_R22, not FIND0817 — XOR that byte with 0x20, and
         report that reader (a) REJECTS and reader (b) REJECTS; then restore it and
         report that both ACCEPT and that the restored image equals the disk image.
     Then, over `.agent/prose_slips.md`: the same prefix property and remainder
     equality for SLIP27, its byte lengths, and its unit count before and after.
     Then the ledger counts before and after: `^Gate: `, `^Gate: R22 — ` and
     `^- R-0817 — `. The last two each go from 0 to exactly 1.
     Then the OPEN SET BY DISTINCT ID before and after, computed as the number of
     DISTINCT ids matching `^- R-\d{4} — ` minus the number of DISTINCT ids
     matching `^Done: R-\d{4} — `. It must rise by exactly one, and no `Done:` or
     `Landed:` line may appear anywhere in the appended region.
  G3 THE PLAN. `.agent/plan.md` equals the PLANF260R23 slice plus exactly one
     trailing newline — report the boolean and the byte length you measured; its
     line count, which must be under the AGENTS.md cap of 50; and that it carries
     `## Goal` and `## Next Steps`.
  G4 THE PITFALL PAIR. Report the containment reading you measure yourself, in the
     words `TO contains FROM: true` or `TO contains FROM: false`, and derive the
     APPEND or REWRITE label from that output on the same line. Then: FROM count
     BEFORE, which must be 1; the boolean that the post-commit file equals the
     pre-commit file with that ONE replacement applied and nothing else; the byte
     length before and after; that the file still ends with exactly one newline;
     and — this is the append obligation, not a FROM-zero count — that every
     TO-ONLY added line occurs exactly ONCE among the lines `git show --numstat`
     and `git show` report that commit as ADDING. Report the number of added lines
     you measured. Finally, confirm the literal `(e) ` appears exactly once in the
     producer-pitfall region and that the labels `(a)`, `(b)`, `(c)` and `(d)` are
     each still present exactly once there.
  G5 THE EVIDENCE JOB — closure algorithm step 1.
     FIRST, THE BASE PROOF, before anything else and before the producer is
     called: with base `b5cd6c20782283923f0e276d9479751e475b9359` and head the
     full sha of C3, report the count of `git rev-list --ancestry-path <base>..<head>`
     and the count of `git rev-list <base>..<head>`, and the boolean that THE TWO
     ARE EQUAL. Also report that the base is an ancestor of both `main` and the
     head. If the counts differ, STOP per constraint 5 — that inequality is the
     exact defect that blocked round 22.
     THEN `git status --porcelain` empty. Then call, in Python,
     `packages.orchestration.job_evidence.create_manual_completion_bundle` with:
       evidence_dir   a FRESH directory under the gitignored `.remedy-wt/`
       repo_root      the primary checkout
       base_commit    b5cd6c20782283923f0e276d9479751e475b9359 — the full
                      40-character fork point, never abbreviated
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
     Report the returned summary dict in full, the job id, and the final verdict
     it names. Do NOT record a full-suite node-id list anywhere in the bundle.
  G6 THE REVIEW ZIP — closure algorithm step 2, MANDATORY and never skipped.
     `git status --porcelain` empty first, branch pushed. Then
     `bash scripts/make_review_zip.sh --evidence-dir <the dir from G5>`.
     Report: the full stdout; the package FILENAME; its SHA-256 as the script
     printed it AND as you recompute it from the file on disk; the package's
     ABSOLUTE directory; `PACKAGE_STATUS`; and the manifest's
     `committed_review_subject` base and head, which must span
     b5cd6c20782283923f0e276d9479751e475b9359..C3. If `PACKAGE_STATUS` is not
     READY_FOR_REVIEW, report the `validation_errors` list VERBATIM and in full,
     then stop per constraint 11.
  G7 THE PRECONDITIONS, run SERIALLY in the primary checkout. This round's change
     set includes `docs/roadmap/**`, so the docs-round gate applies.
     `python3 -m pytest tests/docs/ -q -p no:randomly` — report the count and exit
     code; the reviewer measured 303 at 18787ffa, and C3 edits a file that suite
     reads, so a change in that number is a real signal and not noise.
     `python3 -m pytest tests/cli/test_golden_path.py -q -p no:randomly` — the
     canary; the reviewer measured 42. `python3 -m apps.cli.grouped integrity
     check --json` — report `passed` and `fail_count`. Report `git status
     --porcelain` and the full list of untracked paths, saying for each whether it
     is gitignored.
  G8 STRUCTURE AND TREE. `git status --porcelain` EMPTY immediately before C4 is
     staged; `git ls-files .remedy-wt` returns nothing. Every commit
     single-parent. `git diff --numstat <parent> <commit>` reported cell by cell
     for EACH of C0a, C0b, C1, C2 and C3 — the insertions column only, which is
     the count AGENTS.md DECISION F104 D1 caps at 500, never insertions plus
     deletions — and each one's reading against that cap. Report the push result;
     that NO pull request was created; and that `docs/roadmap/STATUS.md`,
     `README.md` and `scripts/self_use_queue.json` are named NOWHERE in this
     round's diff. Also report the number of marker lines beginning with the BEGIN
     prefix or the END prefix that reached `.agent/plan.md`,
     `.agent/live_review.md`, `.agent/prose_slips.md` or
     `docs/roadmap/STATUS_closure_protocol.md`, which must be zero in each.

The handback (C4) — rewrite .agent/handoff.md whole
  No length cap (amend0827 rule 3). It is the durable carrier for everything the
  closure round needs, so it must record, in a section a later reader can find BY
  NAME: the EVIDENCE JOB ID; the PACKAGE FILENAME; its SHA-256; the package's
  ABSOLUTE DIRECTORY (DECISION amend0827 D1 — or the literal `NOT ARCHIVED` if it
  was left where it was built); the ACCEPTED HEAD, which is the full sha of C3 and
  the head the manifest recorded; and `PACKAGE_STATUS`. The next round authors the
  STATUS line from those values, so a missing one costs a round.
  Beyond that: feature, round and SESSION NUMBER — SESSION 8 of F260, round 23,
  rounds so far 23; the commit range; a `## Commits` table whose insertion and
  deletion cells are the numbers G8 printed from `git diff --numstat`, compared
  cell by cell against that tool rather than re-derived by eye (checklist item
  28); the AGENTS.md item-status table with one row per bundle item C0a through
  C4; one line per gate G1 through G8 with its real reading; the deviations; ONE
  sentence of context self-assessment (amend0905-throughput); and the next
  expected action — the reviewer's gate, then THE CLOSURE ROUND: the STATUS `[x]`
  line, the README capability sync and the `consumed_by` edit on SU-011 in ONE
  commit, then the pull request, which is NOT merged this session. State plainly
  that the ledger rotation already ran in round 22 at `6cebdce6` and is NOT
  repeated. Repeat this line verbatim in its state block:
  `~99 % (T001 komplett, T002 Run-Haelfte, Integration Gate gruen, Evidence + Zip neu gebaut, nur noch STATUS/README/PR) — Schaetzung`

<<<BEGIN PLANF260R23>>>
# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world. Rounds 1 to 22 are reviewed; round 1 FAILED and was
repaired, and 2 to 22 PASSED. DECISION F260 D8 closes this feature at the scope it
built; F272 carries the remainder and was registered in round 18, directly after
F260 in the ledger.

## Goal

SESSION 8 finishes the closure sequence. Round 22 booked round 21 and rotated the
ledger, but its review package built BLOCKED_EVIDENCE because the block ordered the
wrong review base. This round repairs the cause and rebuilds the package; the STATUS
flip is the round after it.

## Current Step

Round 23 books round 22's verdict, registers `R-0817` — the closure protocol's
producer-pitfall list never stated that `base_commit` is the branch's FORK POINT
rather than its merge base — repairs that gap in
`docs/roadmap/STATUS_closure_protocol.md`, and then, committing nothing further,
reruns the evidence job and the review zip from base `b5cd6c20`, proving before the
run that the ancestry-path chain and the plain commit list over that base are the
same length.

## Next Steps

1. THE CLOSURE ROUND: book round 23's verdict and author `Done: R-0817`; then the
   STATUS `[x]` flip and the README capability sync in ONE commit, with
   `consumed_by` set to `F260` on SU-011 in that same commit, then the handback,
   then the pull request — left UNMERGED as the operator's review window.

## Risks

- SU-011 is PENDING and must be marked consumed in the closure commit, not before.
- A failing zip build is a closure BLOCKER. It is reported raw and the reviewer
  decides; the base, the evidence fields and the sources are never adjusted to make
  a package go READY.
- The ledger rotation already ran at `6cebdce6` and is not repeated; byte baselines
  are re-measured from each target's own terminal byte.
<<<END PLANF260R23>>>
<<<BEGIN GATE_R22>>>
Gate: R22 — the F260 R22 entry, CLOSURE PART 2. VERDICT PASS ON EVERY COMMIT, WITH GATE G6 UNSATISFIED FOR A CAUSE THAT IS THE REVIEWER'S AND NOT THE WORKER'S. Range `941846d7c9afd3c633a61ebbef15b62bb283f413`..`18787ffa`, six commits, every one single-parent, in exactly the bundle's ordered sequence C0a, C0b, C1, C2, C3, C4 with nothing added, dropped or reordered; insertion counts 290, 276, 22, 2, 24 and 262, walked commit by commit with `git rev-list --reverse`, every one far under the 500 cap so no exemption was needed. `git diff --name-only` over the range lists exactly the six `.agent/` paths of the change set, and `docs/roadmap/STATUS.md`, `README.md` and `scripts/self_use_queue.json` appear nowhere in it. THE REVIEWER RE-RAN EVERY GATE ITSELF AND REPRODUCED EVERY NUMBER THE HANDBACK REPORTED. TRANSPORT: the reviewer's own scratchpad original `.remedy-wt/f260-r22-block.md`, the committed `.agent/authored/f260-r22.md` at `accbc607` and `.agent/last_block.md` at `42dd2fe8` are all 23024 bytes and all hash to `9ce6547aef8d3a56e2d77a933b75e1ceccabc0185fa3c97d585c0e164b3a25d3`, which is the digest the delegation named before the round began; per §3 item 37 that chain covers the scratch file, the saved copy and the mirror, and is not a claim about the bytes emitted into a prompt. THE RECORD, at `db505a2c`: `.agent/live_review.md` 983418 to 987791 bytes, delta 4373, equal to its pre-image plus a newline plus the GATE_R21 slice plus a newline exactly, with the pre-image a byte-exact prefix; blank-line units 444 to 445; the last unit equals the slice; `^Gate: R21 — ` 0 to exactly 1. `.agent/plan.md` at `8e6a622a` equals its slice plus one newline at 1703 bytes and 36 lines, under the 50-line cap, carrying one `## Goal` and one `## Next Steps`. THE ROTATION, at `6cebdce6` and touching exactly `.agent/live_review.md` and `.agent/live_review_archive.md`: ten gate records and one resolved finding pair moved byte-verbatim into the archive; the ledger 987791 to 939023 bytes and the archive 1731461 to 1780229; the script's own open-findings count 296 before and 296 after, EQUAL, which is the property the rotation guarantees rather than any particular number. Measured by the reviewer on the post-rotation ledger at `18787ffa`: `^Gate: ` 21, `^Gate: R21 — ` still exactly 1 — the booking survived rather than being archived, because F260 is `[~]` in `docs/roadmap/STATUS.md` and its records are therefore not movable — registrations 300 over 300 DISTINCT ids, `^Done: R-dddd — ` 4 lines over TWO distinct ids, and the OPEN SET 298 BY DISTINCT ID, unchanged across the whole round exactly as constraint 4 required. Zero marker lines reached any written file. THE EVIDENCE JOB RAN AND PASSED: job `af9cf1705d203f2d`, verdict `PASS_WITH_RISKS`, authority count 71, total passed 303, its one verification run being `tests/docs/` at exit 0 with 303 node ids equal to 303 selected. THE REVIEW ZIP BUILT BUT NOT AS ORDERED, AND THIS IS WHY THIS ENTRY IS NOT A PLAIN PASS: `remedy-review-20260906-131557-BLOCKED_EVIDENCE.zip`, sha256 `54f642007968b6e5c2743a7fa3f154243b6a84ff34694538d516d215db3c11f1` both as printed and as recomputed from disk, archived at `/home/decodeux/Repos/remedy-history/zips`, carrying the single validation error that the review subject claims committed changes no packaged commit made. THE CAUSE IS THE BLOCK'S, MEASURED BY THE REVIEWER AND NOT INFERRED FROM THE HANDBACK. The block ordered `base_commit` as `git merge-base HEAD main`, which answers `f957c4c6dede34e9ba9d3653ae01cc16157b96fc`; this branch merged `main` IN at `7ed25b88993d497463129e21ad9b008362304e90`, so that merge base is main's OWN tip at the merge and not the branch's fork point, and every commit this branch made before the merge fails to descend from it. `packages/orchestration/review_subject.py` builds the packaged chain with `rev-list --ancestry-path`, so those commits are dropped from the chain while the `base..head` diff still carries their effect, and the one-directional check in `scripts/build_review_manifest.py` correctly refuses. Measured at `6cebdce6` with the product's own `_is_source_for_alignment` predicate: from `f957c4c6` the ancestry chain is 41 commits against a plain `rev-list` of 158, the commit union covers 32 of the subject's 108 paths, and 58 source paths are unexplained; from the fork point `b5cd6c20782283923f0e276d9479751e475b9359` the chain is 160 against 160, the union is 110 of 110, and NONE is unexplained. The handback reported 57 rather than 58 from the manifest's own error string, a one-path difference the reviewer did not chase because both readings are non-empty and both go to zero at the fork point. NOTHING IS WRONG WITH THE PACKAGING CODE: the validator caught a real inconsistency and refused to certify it, which is the gate working as designed and is the opposite of a blind gate. What was missing is a line in the closure protocol's own producer-pitfall list, registered as `R-0817` in the paragraph that follows this one. THE WORKER'S CONDUCT IS THE PART OF THIS ROUND WORTH PRAISING RATHER THAN REPAIRING: constraint 11 told it that a failing zip is a closure blocker and not something to work around, and it did exactly that — recorded the raw error, committed the handback saying so, stopped, and changed no base, no evidence field and no source file to make the package go green. It then diagnosed the mechanism read-only and correctly named the merge as the reason. A round that is handed an unmeetable order and returns an honest red with a correct diagnosis is worth more than one that quietly finds a way to satisfy it. SUITES re-run by the reviewer, serially, in the primary checkout: `tests/docs/` exit 0 at 303 passed, the canary `tests/cli/test_golden_path.py` exit 0 at 42 passed, `tests/orchestration/test_live_review_rotation.py` exit 0 at 10 passed, and `python3 -m apps.cli.grouped integrity check --json` exit 0 with `"passed": true` and `"fail_count": 0`. `git status --porcelain` EMPTY and `git ls-files .remedy-wt` EMPTY at `18787ffa`. SIX ITEMS WERE DECLARED AND ALL SIX ARE UPHELD, including the worker's note that the mandated state line understated what remained once the package came back blocked — which is the round reading its own instruction against its own result, and is exactly the reflex this workflow wants.
<<<END GATE_R22>>>
<<<BEGIN FIND0817>>>
- R-0817 — Medium, THE CLOSURE PROTOCOL'S PRODUCER-PITFALL LIST NEVER STATES WHICH COMMIT `base_commit` MUST BE, AND A REVIEWER FOLLOWING THE PRECEDENT IT DOES CARRY BUILT A BLOCKED_EVIDENCE PACKAGE AT F260'S CLOSURE. `docs/roadmap/STATUS_closure_protocol.md` Algorithm step 1 lists four named producer pitfalls — the `output_hash`, the node-id equality, the `test_files` shape, the `run_id` pattern and the full-suite prohibition — and says of the base only that it must be "the full-length base_commit SHA", which is a rule about its FORMAT and none about WHICH COMMIT it is. The F260 R22 block therefore took it from `git merge-base HEAD main`. That branch had merged `main` IN at `7ed25b88993d497463129e21ad9b008362304e90`, so the merge base is main's own tip rather than the branch's fork point, and `packages/orchestration/review_subject.py` builds the packaged commit chain with `rev-list --ancestry-path`, which drops every commit that does not descend from the declared base. Measured at `6cebdce6` with the product's own `_is_source_for_alignment` predicate: the ancestry chain is 41 commits against a plain `rev-list` of 158 over the same range, the commit union explains 32 of the review subject's 108 paths, and 58 source paths are left unexplained, so `scripts/build_review_manifest.py` reports that the review subject claims committed changes no packaged commit made and the package packages BLOCKED_EVIDENCE. From the fork point `b5cd6c20782283923f0e276d9479751e475b9359` the same three readings are 160 against 160, 110 of 110, and zero unexplained. THE OPEN SET WAS SEARCHED FOR THE DEFECT BEFORE THIS ID WAS MINTED, per §3 item 30, and the two nearest neighbours are named here so a later reader can see why this is not a duplicate of either: `R-0490` is the same LIST missing the `output_hash` rule and `R-0448` is a block ordering an evidence FIELD in a rejected order, and both are about a field's value, while this is about which commit the base names — a different gap, a different fix, and neither of their fix clauses would have prevented it. The strings `ancestry` and `fork point` occur ZERO times in `.agent/live_review.md` and zero times in `.agent/live_review_archive.md`, which is the measurement that settled it. THIS IS NOT A DEFECT IN THE PACKAGING CODE and no code change is asked for: the validator caught a real inconsistency and refused, which is a gate working. RESOLVED WHEN `docs/roadmap/STATUS_closure_protocol.md` carries a producer-pitfall entry stating that `base_commit` is the branch's fork point rather than its merge base, giving the equality of `rev-list --ancestry-path <base>..<head>` and `rev-list <base>..<head>` as the mechanical check that distinguishes them. Severity Medium rather than Low because it blocks a closure outright and recurs on every future branch that merges `main` in, which is every long-running feature; and Medium rather than High because nothing wrong reaches disk, the failure is loud, and the repair is one paragraph.
<<<END FIND0817>>>
<<<BEGIN SLIP27>>>
2026-09-06 · F260 R22 (reviewer) · The round-22 block ordered the evidence bundle's `base_commit` as `git merge-base HEAD main`, which on a branch that has merged `main` IN names main's own tip rather than the branch's fork point, so the packaged ancestry chain covered 41 of the range's 158 commits and the review zip built BLOCKED_EVIDENCE with 58 source paths unexplained; the reviewer had carried the base wording forward from F259's closure, whose branch held no merge at all and whose merge base therefore coincided with its fork point, so a coincidence was generalised into a rule, and the reviewer's pre-emission dry runs measured the suites and the append arithmetic but never the base's own property — the one number in the block that no gate it ordered could have caught before the zip refused.
<<<END SLIP27>>>
<<<BEGIN PITFALL_FROM>>>
   SCOPED suites in the bundle and let the full-suite proof ride in
   the committed integration-gate evidence and the reviewer's own
   re-run. The package still covers the accepted HEAD, and nothing
   green is claimed that was not run.
<<<END PITFALL_FROM>>>
<<<BEGIN PITFALL_TO>>>
   SCOPED suites in the bundle and let the full-suite proof ride in
   the committed integration-gate evidence and the reviewer's own
   re-run. The package still covers the accepted HEAD, and nothing
   green is claimed that was not run.

   A fifth, from the F260 R22 attempt (58 unexplained source paths,
   packaged BLOCKED_EVIDENCE): (e) `base_commit` is the branch's FORK
   POINT — the first commit that `git rev-list --first-parent <head>`
   shares with `main` — and NEVER `git merge-base <head> main` once the
   branch has merged `main` IN. `packages/orchestration/review_subject.py`
   builds the packaged chain with `rev-list --ancestry-path`, so a
   merge-base taken after such a merge names main's own tip, and the
   chain then silently drops every commit the branch made BEFORE that
   merge while the `base..head` diff still carries their effect; the
   one-directional check in `build_review_manifest.py` reports "the
   review subject claims committed changes no packaged commit made" and
   the package builds BLOCKED_EVIDENCE. Measured at `6cebdce6`: the
   merge-base gave an ancestry chain of 41 against a plain `rev-list` of
   158 and left 58 source paths unexplained, while the fork point gave
   160 against 160 and left none. CHECK IT BY RUNNING BOTH — `rev-list
   --ancestry-path <base>..<head>` and `rev-list <base>..<head>` must
   return the SAME count, or the base is wrong. A branch with no merges
   makes the two bases coincide, which is why carrying an earlier
   closure's base wording forward generalises a coincidence.
<<<END PITFALL_TO>>>
