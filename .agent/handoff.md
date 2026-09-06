# Handoff — F260 One world · round 22 · CLOSURE PART 2 · EVIDENCE BUILT, ZIP BLOCKED

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE
(the banner announces the REPORT, not a stop — amend0905-throughput)

**CLOSURE BLOCKER: the review zip built but reached `PACKAGE_STATUS=BLOCKED_EVIDENCE`,
not `READY_FOR_REVIEW`.** Per constraint 11 and gate G6 the raw error is recorded
below, this handback is committed saying so, and the round STOPS there. Nothing was
worked around. THE REVIEWER DECIDES whether closure part 3 may proceed.

## Session

SESSION 8 of feature F260 · round 22 · rounds so far 22

`.agent/STOP` was read from disk with `os.path.exists` before C0a (**False**),
before C3 (**False**) and before this handback (**False**).

Context self-assessment (amend0905-throughput): context is comfortable — this round
is five small `.agent/` commits plus two tool runs — and was never the constraint;
what ends the round is the blocked package, not the margin.

F260 IS AT ITS 7-SESSION SOFT LIMIT. **DECISION F260 D8** (2026-09-06, round 17) is
the standing authority for closing this feature at the scope it built, with F272
carrying the remainder; that decision is unchanged by this round.

`~99 % (T001 komplett, T002 Run-Haelfte, Integration Gate gruen, Evidence + Zip gebaut, nur noch STATUS/README/PR) — Schaetzung`

## CLOSURE PART 3 INPUTS — the measured values part 3 needs

Named here so a later reader finds them BY NAME. Part 3 authors the STATUS line
from exactly these.

| Name | Value |
|---|---|
| EVIDENCE JOB ID | `af9cf1705d203f2d` |
| PACKAGE FILENAME | `remedy-review-20260906-131557-BLOCKED_EVIDENCE.zip` |
| PACKAGE SHA-256 (as the script printed it) | `54f642007968b6e5c2743a7fa3f154243b6a84ff34694538d516d215db3c11f1` |
| PACKAGE SHA-256 (recomputed from the file on disk) | `54f642007968b6e5c2743a7fa3f154243b6a84ff34694538d516d215db3c11f1` — **equal** |
| PACKAGE ABSOLUTE DIRECTORY | `/home/decodeux/Repos/remedy-history/zips` |
| ACCEPTED HEAD | `6cebdce6176fee0e1cfdbe64be9cc772a3ffae5e` (full sha of C3; the head the manifest recorded) |
| PACKAGE_STATUS | `BLOCKED_EVIDENCE` — **not** `READY_FOR_REVIEW` |

The two SHA-256 readings are byte-equal, so the package on disk is the package the
script reported. The manifest's `committed_review_subject` records base
`f957c4c6dede34e9ba9d3653ae01cc16157b96fc` and head
`6cebdce6176fee0e1cfdbe64be9cc772a3ffae5e`, `base_is_ancestor` **true**,
`commit_count` **41**, `file_count` **108** — it spans the ordered range.

## THE BLOCKER — raw

`scripts/make_review_zip.sh` exited **0** and produced a zip, but the manifest
carries `package_status: "BLOCKED_EVIDENCE"`, `evidence_authoritative: false`,
`packaging_warnings: ["evidence is not authoritative"]` and
`current_evidence.evidence_freshness.evidence_validity.is_valid_current_run: false`.
The script's own stdout warning, verbatim:

    WARNING: Evidence validation failed (is_valid_current_run=false).
    Zip will be built anyway — reviewer will see validation status in manifest.

There is EXACTLY ONE entry in `current_evidence.validation.validation_errors`,
quoted verbatim (the path list is the entry's own, unabridged):

    the review subject claims committed changes no packaged commit made: ['apps/cli/commands/do_cmd.py', 'apps/cli/commands/job_stop_cmd.py', 'apps/cli/commands/project.py', 'apps/cli/commands/teach_cmd.py', 'packages/orchestration/cockpit.py', 'packages/orchestration/data_paths.py', 'packages/orchestration/job_evidence.py', 'packages/orchestration/patch_apply.py', 'packages/orchestration/patch_revert.py', 'packages/orchestration/pingpong_evidence.py', 'packages/orchestration/pingpong_job.py', 'packages/orchestration/pingpong_loop.py', 'packages/orchestration/pingpong_promote.py', 'packages/orchestration/prompt_trace.py', 'packages/orchestration/repair_attest.py', 'packages/orchestration/run_log.py', 'packages/orchestration/safe_points.py', 'packages/orchestration/storage.py', 'packages/orchestration/timeline.py', 'packages/orchestration/trust_report.py', 'packages/orchestration/worker_queue.py', 'packages/orchestration/worktree_resume.py', 'tests/cli/test_patch_cmd.py', 'tests/cli/test_propose_cli.py', 'tests/cli/test_task_input.py', 'tests/cli/test_teach_cmd.py', 'tests/orchestration/test_evidence_bundle.py', 'tests/orchestration/test_failure_postmortem.py', 'tests/orchestration/test_failure_wiring.py', 'tests/orchestration/test_job_budgets.py', 'tests/orchestration/test_job_evidence.py', 'tests/orchestration/test_job_promote_consistency.py', 'tests/orchestration/test_job_stop_integration.py', 'tests/orchestration/test_job_worktree_handoff.py', 'tests/orchestration/test_job_worktree_integration.py', 'tests/orchestration/test_job_worktree_integrity.py', 'tests/orchestration/test_manual_completion_bundle.py', 'tests/orchestration/test_mint_call_sites.py', 'tests/orchestration/test_persisted_call_episode_membership.py', 'tests/orchestration/test_persisted_call_ownership.py', 'tests/orchestration/test_persisted_run_call_schema.py', 'tests/orchestration/test_pingpong_cli.py', 'tests/orchestration/test_pingpong_integration.py', 'tests/orchestration/test_pingpong_promote.py', 'tests/orchestration/test_repair_loop.py', 'tests/orchestration/test_run_manifest_ledger_semantics.py', 'tests/orchestration/test_run_manifest_task_lifecycle_binding.py', 'tests/orchestration/test_run_manifest_zero_call_expectations.py', 'tests/orchestration/test_stream_export_e2e.py', 'tests/orchestration/test_worktree_isolation.py', 'tests/orchestration/test_worktree_lifecycle.py', 'tests/orchestration/test_worktree_persistence.py', 'tests/orchestration/test_worktree_resume_cli.py', 'tests/orchestration/test_worktree_safety.py', 'tests/test_data_paths.py', 'tests/test_run_log.py', 'tests/test_test_runner.py', 'tests/test_timeline.py']

That is **57** paths.

### What I measured about it — diagnosis only, NOTHING was changed

I did not re-run the build with different inputs, did not re-pick a base, and did
not touch the evidence. The following are read-only measurements offered so the
reviewer can rule quickly.

- The check is `scripts/build_review_manifest.py` line 1017-1021. It subtracts the
  UNION of `changed_files` over the packaged commit chain from the review subject's
  committed source files, and errors on any remainder.
- The packaged chain has **41** commits, matching
  `git rev-list --ancestry-path f957c4c6..6cebdce6` = **41**.
- But `git rev-list f957c4c6..6cebdce6` = **158** commits, and the range contains
  **one merge commit**: `7ed25b88 Merge remote-tracking branch 'origin/main' into
  feature/f260-one-world`.
- Over ALL 158 commits the union of changed files is **108** paths and the
  `git diff --name-only f957c4c6 6cebdce6` file set is also **108** paths, and the
  set difference `diff − union` is **0**. The subject is fully explained by the
  branch's real history.
- `git merge-base main HEAD` and `git merge-base origin/main HEAD` BOTH resolve to
  `f957c4c6dede34e9ba9d3653ae01cc16157b96fc`, so the base the block declared is the
  true merge base and was not mis-stated.
- So the 57 "unexplained" files are the ones this branch changed BEFORE
  `origin/main` was merged into it. Those commits are not on the ancestry path FROM
  `f957c4c6` (they do not descend from it), so `--ancestry-path` drops them while
  the base..HEAD diff keeps their effect. The validator's one-directional check then
  reads honest history as a gap.
- `change_provenance_gate.json` inside the bundle is **PASS** with `uncovered_files`
  empty, `hash_mismatches` empty and `content_hash_verified` true;
  `ready_gate_matrix.ok` is **true**; `token_truth_authority.status` is
  `VERIFIED_EQUAL`; `review_subject_alignment` is **PASS**;
  `final_verifier_reproducible` is **true**. The single failing reading is the one
  above.

I make no claim about what the fix is. It is plainly a closure blocker and it is
the reviewer's to rule on.

## Range

Base `941846d7c9afd3c633a61ebbef15b62bb283f413` (the head the block names)
..`HEAD`. FIVE commits plus this handback, ALL single-parent, in EXACTLY the
bundle's ordered sequence C0a → C0b → C1 → C2 → C3 → C4, with nothing added,
dropped or reordered.

## Commits

Every `+/-` cell below is the number `git diff --numstat <parent> <commit>`
printed, compared cell by cell against that tool rather than re-derived by eye.

### accbc607f71737d7fdbdfc47af11acae9a2b1c46 — f260 r22: save the round 22 step block to the authored record
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f260-r22.md | +290 / -0 | C0a — `shutil.copyfile` from `.remedy-wt/f260-r22-block.md`; digest verified against the delegation's value BEFORE anything else was executed |

### 42dd2fe88586d616082427235c37a2370e7f1500 — f260 r22: mirror the round 22 step block to the last block slot
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +276 / -218 | C0b — the SAME source file, the same `shutil.copyfile` route |

### 8e6a622a16eb845fe81728bd59e5966c0729cbde — f260 r22: point the plan at closure part 2, the evidence half
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +22 / -23 | C1 — whole-file replacement by the PLANF260R22 slice plus exactly one trailing newline; 1703 bytes, 36 lines |

### db505a2c00ca84276cbcd3ea025cca2c77e3baae — f260 r22: book the round 21 reviewer verdict into the ledger
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2 / -0 | C2 — the GATE_R21 record appended by the recipe derived from this file's OWN measured terminal byte; 983418 → 987791 bytes |

### 6cebdce6176fee0e1cfdbe64be9cc772a3ffae5e — f260 r22: rotate the closed-feature ledger records into the archive
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +0 / -24 | C3 — `python3 scripts/rotate_live_review.py`, its own commit |
| .agent/live_review_archive.md | +24 / -0 | C3 — the same run's append side |

Insertion counts C0a..C3: **290, 276, 22, 2, 24**. Every one is far under the
500-insertion cap of AGENTS.md DECISION F104 D1 (the `+` column only, never
insertions plus deletions), so no `.agent/**` state-write exemption had to be
claimed for any of them — including C3, whose rotation diff is 24 insertions.

## The rotation transcript

`python3 scripts/rotate_live_review.py --dry-run` — returncode **0**, stdout in
full:

    gate records moved: 10
    finding pairs moved: 1 (2 records)
    old ledger size: 987791 bytes
    new ledger size: 939023 bytes
    old archive size: 1731461 bytes
    new archive size: 1780229 bytes
    open findings before: 296
    open findings after: 296
    dry run; nothing written

`python3 scripts/rotate_live_review.py` — returncode **0**, stdout in full:

    gate records moved: 10
    finding pairs moved: 1 (2 records)
    old ledger size: 987791 bytes
    new ledger size: 939023 bytes
    old archive size: 1731461 bytes
    new archive size: 1780229 bytes
    open findings before: 296
    open findings after: 296
    written: /home/decodeux/Repos/remedy/.agent/live_review.md and /home/decodeux/Repos/remedy/.agent/live_review_archive.md

## External actions

- `git push -u origin feature/f260-one-world` after C3 (returncode **0**,
  `941846d7..6cebdce6`), and a second push after C4.
- `python3 scripts/rotate_live_review.py` and `bash scripts/make_review_zip.sh`.
- NO pull request was created, NOTHING was merged, there was no force-push, no
  branch deletion and no commit on `main`. I created NO git worktree.

## Verification — one line per gate, REAL exit codes

Every code below was read from `subprocess.run(...).returncode` or from the tool's
own reported status; none is a word standing in for a run.

| Gate | Exit | Evidence |
|---|---|---|
| G1 TRANSPORT | 0 | `.remedy-wt/f260-r22-block.md`, `.agent/authored/f260-r22.md` and `.agent/last_block.md` are all **23024 bytes** and all sha256 `9ce6547aef8d3a56e2d77a933b75e1ceccabc0185fa3c97d585c0e164b3a25d3` — one digest, three times, EQUAL to the value the delegation stated, verified BEFORE anything else in the block ran. `filecmp.cmp(shallow=False)` **True** for source-vs-saved and **True** for source-vs-mirror. Measured BEFORE C0a was staged |
| G2 THE RECORD (a) BYTE | 0 | `post == pre + b"\n" + GATE_R21 + b"\n"` **True**; `post.startswith(pre)` **True** (pre is a byte-exact PREFIX). Pre **983418** → post **987791** bytes, delta **4373** = 4371 + 2. The pre-image's terminal byte was asserted to be exactly ONE newline BEFORE the write; post ends in exactly one newline **True** |
| G2 THE RECORD (b) STRUCTURAL | 0 | Independent of (a). Whole file split on `\n{2,}`, units empty after stripping dropped, each survivor stripped of leading/trailing newlines: raw **444 → 445**, kept **444 → 445**. N = **1**, COUNTED BY THE SCRIPT from the slice's own paragraphs. Last N kept units equal the slice's paragraphs IN ORDER **True** |
| G2 THE RECORD (c) NEGATIVE CONTROL | 0 | In memory on a `bytes` object, never on disk. Offset **983424**, which the script first ASSERTED lies inside the FIRST appended paragraph (span `[983419, 987790)`); byte `' '` XOR 0x20. Reader (a) **REJECTS**, reader (b) **REJECTS**. Restored: (a) **ACCEPTS**, (b) **ACCEPTS**, and the restored image equals the disk image **True** |
| G2 THE COUNTS | 0 | Over the whole file: `^Gate: ` **30 → 31**; `^Gate: R21 — ` **0 → exactly 1** |
| G3 THE PLAN | 0 | `.agent/plan.md` equals the PLANF260R22 slice plus exactly one trailing newline **True**; **1703 bytes**; **36 lines**, under the AGENTS.md cap of 50 **True**; carries `## Goal` **True** and `## Next Steps` **True** |
| G4 THE ROTATION | 0 | Dry run and real run both returncode **0**; both transcripts quoted IN FULL above. `.agent/live_review.md` **987791 → 939023** bytes; `.agent/live_review_archive.md` **1731461 → 1780229** bytes. Open findings AS THE SCRIPT PRINTS THEM: **296 before, 296 after — THE TWO ARE EQUAL**. `^Gate: ` remaining in the ledger **21**; now in the archive **354** (from 344, +10). `git show --numstat 6cebdce6` names EXACTLY `.agent/live_review.md` and `.agent/live_review_archive.md` and no other path. `^Gate: R21 — ` still counts **exactly 1 IN THE LEDGER** after the rotation, and the record there is the F260 one (`Gate: R21 — the F260 R21 entry, …`), so the booking SURVIVED rather than being archived — F260 is `[~]` in STATUS at this commit, so its records are not movable |
| G5 THE EVIDENCE JOB | 0 | `git status --porcelain` **EMPTY** first. `create_manual_completion_bundle` returned: `job_id af9cf1705d203f2d`, `head_commit 6cebdce6176fee0e1cfdbe64be9cc772a3ffae5e`, `authority_count 71`, `partition {T001:24, T002:24, T003:23}`, `commit_count 41`, **`verdict PASS_WITH_RISKS`**, `manual_completion true`, `operator_attested_tasks [T001,T002,T003]`, `total_passed 303`. The one verification run: `python3 -m pytest tests/docs/ -q` exit **0**, passed **303**, failed 0, skipped 0, deselected 0, `selected` **303**; `node_ids` from a real `--collect-only` of the SAME selection, length **303 = selected**; `test_files` SORTED as `['tests/docs/test_docs_consistency.py', 'tests/docs/test_vocabulary.py']`; no node id holds an absolute path or a `..` traversal; `stdout_summary` **< 4000** chars; `output_hash` = sha256 of exactly that string = `54ee3d3888b1c4ccead127b3538b2fe188504221b685cfbd99bdd680e539a486`; `run_id` `vr-1788693345`. Evidence dir OUTSIDE the review subject, under gitignored `.remedy-wt/` |
| G6 THE REVIEW ZIP | 0 (script) — **GATE NOT SATISFIED** | `git status --porcelain` **EMPTY** and the branch pushed first. `bash scripts/make_review_zip.sh --evidence-dir …` returncode **0**. Filename `remedy-review-20260906-131557-BLOCKED_EVIDENCE.zip`; sha256 as printed AND as recomputed from disk both `54f642007968b6e5c2743a7fa3f154243b6a84ff34694538d516d215db3c11f1`; absolute directory `/home/decodeux/Repos/remedy-history/zips`; **`PACKAGE_STATUS=BLOCKED_EVIDENCE`**; manifest `committed_review_subject` base `f957c4c6dede34e9ba9d3653ae01cc16157b96fc` → head `6cebdce6176fee0e1cfdbe64be9cc772a3ffae5e`, spanning the ordered range. It did NOT reach `READY_FOR_REVIEW`, so per G6 and constraint 11 the raw error is recorded above and the round STOPS |
| G7 integrity check | 0 | `python3 -m apps.cli.grouped integrity check --json` → `"passed": true`, `"fail_count": 0`, `check_count 5` |
| G7 tests/docs | 0 | `python3 -m pytest tests/docs/ -q -p no:randomly` → **303 passed in 0.49s** — the 303 the reviewer measured at `941846d7` |
| G7 test_golden_path | 0 | `python3 -m pytest tests/cli/test_golden_path.py -q -p no:randomly` → **42 passed in 21.16s** — the 42 the reviewer measured |
| G7 rotation suite | 0 | `python3 -m pytest tests/orchestration/test_live_review_rotation.py -q -p no:randomly` → **10 passed in 0.23s** — the 10 the reviewer measured, and this round ran that script for real. All four G7 commands were run SERIALLY in the primary checkout |
| G7 TREE | 0 | `git status --porcelain` **EMPTY**. `git ls-files --others --exclude-standard` returns **0** paths, so there is no untracked path that is not gitignored — every untracked path in this tree IS gitignored, including the block scratch, the helper scripts, the evidence directory and the zip staging (`.gitignore:235 .remedy-wt/`, `:223 remedy-review-*`, `:226 remedy-job-evidence-*`) |
| G8 STRUCTURE | 0 | `git status --porcelain` **EMPTY** immediately before C4 was staged; `git ls-files .remedy-wt` returns **nothing**. Every commit single-parent: C0a `accbc607` 1, C0b `42dd2fe8` 1, C1 `8e6a622a` 1, C2 `db505a2c` 1, C3 `6cebdce6` 1. Insertions **290 / 276 / 22 / 2 / 24**, every one UNDER 500. `git diff --name-only 941846d7 6cebdce6` lists exactly the five `.agent/` paths of the change set; `docs/roadmap/STATUS.md` **not named**, `README.md` **not named**, `scripts/self_use_queue.json` **not named**. Marker lines: `.agent/plan.md` BEGIN-prefix **0** END-prefix **0**; `.agent/live_review.md` BEGIN-prefix **0** END-prefix **0** |

## Authored-text proofs

- **Transport is a COPY chain, never a retype.** Both writes went through
  `shutil.copyfile` from the SAME source file, and the digest
  `9ce6547aef8d3a56e2d77a933b75e1ceccabc0185fa3c97d585c0e164b3a25d3` at 23024 bytes
  was checked against the delegation's stated value BEFORE the block was executed at
  all.
- **Both slices were extracted from the COMMITTED authored copy** after C0a, never
  from the delegation message and never retyped. The extractor matches lines EXACTLY
  equal to `<<<BEGIN name>>>` / `<<<END name>>>` BY POSITION, asserts exactly one of
  each and that BEGIN precedes END, and joins the lines between them with a newline,
  so an extracted slice carries no trailing newline of its own.
- **Slice sizes**: PLANF260R22 **1702 B / 36 lines**; GATE_R21 **4371 B / 1 line /
  1 paragraph**, containing **0** newlines of its own.
- **Blank-line unit definition**, stated so the reviewer can reproduce it rather
  than match a phrase: the WHOLE file image split on the regex `\n{2,}`, units that
  are empty after stripping dropped, each surviving unit stripped of leading and
  trailing newlines. Under that definition `.agent/live_review.md` reads
  **444 → 445**.
- **The append recipe was derived from the target's OWN measured terminal byte**,
  with both asserts (`endswith(b"\n")` and `not endswith(b"\n\n")`) executed BEFORE
  the write, as constraint 3 orders. No number from the block was used for it.
- **Constraint 4 upheld — NO id was minted and no `Done:` or `Landed:` line was
  authored.** Census over `.agent/live_review.md` immediately BEFORE C2 (from
  `git show 8e6a622a:.agent/live_review.md`) and immediately AFTER: registrations
  **301** over **301 distinct ids**, `^Done: R-dddd — ` **5** lines over **3
  distinct ids**, **OPEN SET 298 BY DISTINCT ID** — identical on both sides. After
  the C3 rotation the ledger reads 300 distinct registrations and 2 distinct `Done:`
  ids, so the open set is **still 298**: the rotation moved one resolved PAIR, which
  is exactly why the count is preserved.

## Deviations & assumptions

**1 — THE ZIP DID NOT REACH `READY_FOR_REVIEW`, AND I STOPPED THERE.** This is the
round's headline and it is a genuine closure blocker, not a nuisance. I recorded the
raw error verbatim, committed this handback saying so, and did NOT attempt any
workaround — no alternate base, no re-run with different inputs, no edit to the
evidence, no `--force`-style flag. The read-only diagnosis above is offered as
evidence for the reviewer's ruling, not as a proposed fix.

**2 — THE MANDATED VERBATIM STATE LINE SAYS `Evidence + Zip gebaut`, AND THAT IS
LITERALLY TRUE BUT READS AS MORE THAN IT IS.** The block orders that line repeated
verbatim in the state block and constraint 1 says to apply a slice verbatim even if
I believe it is wrong, so I wrote it exactly as given. Declaring the tension: the
zip WAS built and is on disk, but its `PACKAGE_STATUS` is `BLOCKED_EVIDENCE`, so
"nur noch STATUS/README/PR" understates what remains. The blocker section above is
the accurate statement and this note is here so the two are never read apart.

**3 — THE BUNDLE UPDATES `.agent/plan.md` AT C1, SO C0a AND C0b WERE COMMITTED WITH
A PLAN NAMING ROUND 21.** AGENTS.md's Commit Gate asks that the plan reflect the
current work before EVERY commit; the block's ordered bundle puts the two transport
commits before the plan rewrite, and its own text says only the two block-save
commits may precede C1. I executed the bundle order as written rather than
reordering it, and declare the gap — the same shape every prior round on this branch
used. The plan named the F260 closure sequence throughout.

**4 — NOTHING OUTSIDE THE CHANGE SET WAS WRITTEN.** `docs/roadmap/STATUS.md`,
`README.md` and `scripts/self_use_queue.json` are untouched (G8). No pull request
was created. The evidence directory and the zip live under gitignored paths outside
the review subject and were never `git add`ed.

**5 — SANDBOX SUBSTITUTIONS, AS CONSTRAINT 8 PRESCRIBES.** The session's shell guard
refused two command FORMS outright, each with the message
`Permission to use Bash has been denied`: a compound command containing `$?`, and an
inline `python3 -c` whose source contained a `for … in …` line, which the guard reads
as a shell loop by FORM. Both were re-expressed — the first as a Python probe, the
second as a script file under `.remedy-wt/` run as `python3 <file>` — and the Python
I ran is beside its output in this handback. `cmp` was replaced by
`filecmp.cmp(shallow=False)` plus sha256; the built `remedy` binary was never
invoked, `python3 -m apps.cli.grouped` was used instead; every exit code was read
from `subprocess.run(...).returncode`. Helper scripts (`r22_c0.py`, `r22_slice.py`,
`r22_c2.py`, `r22_g5.py`, `r22_g8.py`, `r22_diag.py`, `r22_diag2.py`) live under the
gitignored `.remedy-wt/` and NONE was `git add`ed — `git ls-files .remedy-wt` is
EMPTY.

**6 — CONSTRAINT 10 AND THE C4 REPORTING RULE.** C4 is ONE commit. Its own insertion
count and byte length are reported NOWHERE in this file, per the block's Done-when
preamble; the reviewer measures those at the next gate.

**NO SLICE LOOKED WRONG THIS ROUND.** Both slices were applied byte for byte and
neither raised a doubt. The one text I would have written differently is the
mandated verbatim state line, declared as deviation 2.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a `.agent/authored/f260-r22.md` | done | |
| C0b `.agent/last_block.md` | done | |
| C1 `.agent/plan.md` | done | |
| C2 `.agent/live_review.md` | done | GATE_R21 appended, one commit, one path |
| C3 `.agent/live_review.md` + `.agent/live_review_archive.md` | done | the rotation, its own commit, exactly two paths; the script did NOT refuse, so constraint 5's stop clause never engaged |
| C4 `.agent/handoff.md` | done | this file |
| G1 TRANSPORT | done | exit 0 |
| G2 THE RECORD | done | exit 0 on all four readings, including the in-memory negative control on the FIRST appended paragraph |
| G3 THE PLAN | done | exit 0 |
| G4 THE ROTATION | done | exit 0; both transcripts quoted in full; open-findings count equal before and after |
| G5 THE EVIDENCE JOB | done | exit 0; job `af9cf1705d203f2d`, verdict `PASS_WITH_RISKS` |
| G6 THE REVIEW ZIP | **deviated** | the script exited 0 and produced a package, but `PACKAGE_STATUS=BLOCKED_EVIDENCE`, so the gate's required `READY_FOR_REVIEW` was NOT reached; raw error recorded, round stopped per constraint 11 |
| G7 THE PRECONDITIONS | done | exit 0 on all four, run serially: integrity, 303, 42, 10 |
| G8 STRUCTURE AND TREE | done | exit 0; five single-parent commits, every insertion count under 500, zero marker lines, the three forbidden paths named nowhere |

## Open findings

**298 OPEN BY DISTINCT ID**, unchanged by this round, which is correct: this round
mints no id and resolves none. Measured before C2 and after C2 with the same script
and the same number both times; measured again after the C3 rotation, where the
ledger now holds 300 distinct registrations and 2 distinct `Done:` ids because one
resolved PAIR moved to the archive as a pair — 300 − 2 = **298**.

Round 21's PASS is now ON THE RECORD as the `Gate: R21` entry in
`.agent/live_review.md`, booked by C2 in the first ledger commit of this round, and
it survived the rotation.

## Next

1. **The reviewer's independent gate on round 22** — including a ruling on the
   `BLOCKED_EVIDENCE` package, which is the one thing this round could not resolve
   on its own authority.
2. **CLOSURE PART 3, only if the reviewer clears the package**: the STATUS `[x]`
   line, the README capability sync and the `consumed_by = F260` edit on `SU-011`
   in ONE commit (R-0154, the README/STATUS agreement pin), then the handback, then
   the pull request — which is NOT merged this session and stands as the operator's
   review window.

F260 is at its 7-session soft limit and **DECISION F260 D8**'s split-and-close is
the authority for closing at the built scope, with F272 carrying the remainder.
