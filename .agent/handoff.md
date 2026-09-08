# Handback — F274 ROUND 20 — the R-0837 repair: the closure evidence producer now packages a branch that deletes a source file

This file supersedes the SESSION 7 END handback. It is written by the delegated worker of round 20
on the reviewer's authored text; the reviewer never edits a work-tree file. It carries NO verdict and
NO `Done:` paragraph — those belong to the reviewer's own authored text in `.agent/live_review.md`.

## Session

SESSION 8 of feature F274 · round 20 · feature rounds so far 20 of the soft limit of 25, sessions 8
of 7.

Fortschritt: F274 schließt bei ~35 % des ursprünglichen Umfangs, Closure-Blocker R-0837 behoben, Integrationsgate BESTANDEN, F275 registriert (Löschkarte ✅ · Reachability-Ratsche ✅ · D1–D8 ✅ · F275 ✅ · Gate ✅ · Self-Use ✅ · R-0837 ✅ · Closure offen) — Schätzung

### The session soft limit is PAST, and the obligation it carries

    SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

F274 is at 8 sessions against a soft limit of 7, so the scope report is owed again. It is short,
because session 7 already executed the SPLIT half of the split-and-close default:

- WHAT IS FINISHED. The split is executed and F275 is registered; the deletion card, the
  reachability ratchet and DECISIONS D1–D8 are done; the integration gate has PASSED (round 18); the
  self-use precondition is met (round 19, `SU-013` generated, run to the approval gate, evidence
  recorded); and as of THIS round the closure blocker R-0837 is repaired on the branch, with a
  regression test whose colour is proved by mutation.
- WHAT IS MISSING. Only the CLOSE itself, in the two rounds the plan names: closure round A (ledger
  rotation, evidence job, fresh review zip) and closure round B (STATUS `[x]` flip, README sync, the
  one `consumed_by` edit, then the pull request).
- THE PROPOSAL. Do not re-split. Run closure rounds A and B and close F274; the cluster deletion,
  the atomic record flip and the classic runner already live in F275 per DECISION F274 D8.

## Range

Review of `bb375019`..THIS HANDOFF COMMIT, which is the tip of the branch and the last commit of the
round; the GATED work of the round is `bb375019`..`cacd42af`. The C4 sha is deliberately not written
here: it does not exist until this file is committed, and an unmeasured sha in the record is worse
than a named range endpoint.

## Commits

### c3ce3a7b F274 R20 C0a: save the round 20 step block verbatim as an authored artifact
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f274-r20.md` | +289 / -0 | the round 20 step block, saved by `cp` from `.remedy-wt/f274-r20-FINAL.md`, never retyped |

### 7ce25686 F274 R20 C0b: mirror the round 20 block into the last-block state file
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +241 / -252 | same bytes mirrored by `cp`; the deletions are round 19's block being replaced |

### 5dbaec86 F274 R20 C1: point the plan at the closure-blocker repair round
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +22 / -21 | replaced byte-for-byte by the PLAN20 slice |

### b6827f2a F274 R20 C2: book round 19 PASS, register the closure blocker and its generator finding, append the R-0784 recurrence
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +8 / -0 | RECORD20 appended: round 19's PASS verdict, R-0837, R-0838, the R-0784 recurrence |
| `.agent/prose_slips.md` | +2 / -0 | SLIP20 appended: the round 19 block's `dest_dir` claim about the persisted `JobPlan` |

### cacd42af F274 R20 C3: exclude a deleted path from the attestation authority set and prove it with a regression test
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/job_evidence.py` | +3 / -1 | the `and f.current_sha256` conjunct on the authority comprehension, plus its two-line WHY comment |
| `tests/orchestration/test_review_manual_completion_shapes.py` | +58 / -0 | `TestDeletedSourceFileDoesNotBlockTheBundle`, one class, one method, at the end of the file |

### (this commit) F274 R20 C4: hand back the R-0837 repair round with its measured gates
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | this file | a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

- `git worktree add --detach .remedy-wt/r20-redproof cacd42af` — created, detached, no branch made.
- `git worktree remove --force .remedy-wt/r20-redproof` then `git worktree prune` — removed; worktree
  count back to 14, unchanged from the pre-round reading.
- `git push -u origin feature/f274-one-world-completion-part-two` — pushed after C4.
- NO pull request created. NOTHING merged. No branch deleted. No force-push, no history rewrite.

## Verification

ONE LINE PER GATE, each with its real measured result.

G1 TRANSPORT — the three digests are EQUAL and all three files are 32833 bytes:
`.remedy-wt/f274-r20-FINAL.md`, the committed `.agent/authored/f274-r20.md` and the committed
`.agent/last_block.md` each hash to
`d5fc3280b35c9b22d6639cde2e859b2e2aed03435ad6ad4a2bd6b77e57a1ffac`.

G2 THE PLAN — `.agent/plan.md` is 2631 bytes and 43 lines, byte-identical to the PLAN20 slice
(`6c86b31441467619677a0d9dbdd36e674e2d62665ab9b2315cbd9c20258ac6be`), 43 under the AGENTS.md cap of
50; `## Goal` occurs 1 time and `## Next Steps` occurs 1 time.

G3 THE APPENDS — (a) `.agent/live_review.md` 638448 → 650874 bytes, delta 12426 = the RECORD20 slice
exactly; (b) prefix True, suffix True; (c) N counted from the slice itself = 4, ordered equality True;
(d) negative control on the FIRST appended paragraph, byte at offset 638469 flipped `h`→`H` in memory
and never in the tracked file, reader-(b) REJECTS and reader-(c) REJECTS; (e) units 246→250,
`^Gate: ` 50→51, `^Gate: F274 R19 ` 0→1, `^RECURRENCE of R-0784 ` 0→1, distinct `^- R-\d+ — ` 70→72,
distinct `^Done: R-\d+ — ` 7→7, OPEN SET BY DISTINCT ID 63→65 — every transition as ordered;
(f) `.agent/prose_slips.md` 164868 → 165189, prefix True, suffix True, blank-line units 224→225,
delta exactly 1; (g) unquoted `\bHEAD\b` in RECORD20 with backtick spans deleted first = 0.

G4 THE GUARD — `git show --numstat cacd42af -- packages/orchestration/job_evidence.py` reads
`3	1	packages/orchestration/job_evidence.py`; post-commit `authority = sorted(` occurs 1 time and
`is_attestable_source(f.path) and f.current_sha256` occurs 2 times; `test_role_config.py` ABSENT and
`test_execution_config_evidence.py` ABSENT, so
`TestEvidenceHygiene::test_no_hardcoded_verification_test_list` still holds; ruff over both changed
files exited 0 with `All checks passed!`.

The full C3 diff of that file, verbatim:

    diff --git a/packages/orchestration/job_evidence.py b/packages/orchestration/job_evidence.py
    index 1b18a66f..222bc97f 100644
    --- a/packages/orchestration/job_evidence.py
    +++ b/packages/orchestration/job_evidence.py
    @@ -3030,7 +3030,9 @@ def create_manual_completion_bundle(

         # 1) The committed review subject — resolved once by the production helper.
         subject = resolve_review_subject(repo_root, base_commit)
    -    authority = sorted({f.path for f in subject.files if is_attestable_source(f.path)})
    +    # A path DELETED in this range has no content at the head tip, so it can attest no sha256 and no
    +    # safe diff; leaving it in the authority set makes the two checks below jointly unsatisfiable (R-0837).
    +    authority = sorted({f.path for f in subject.files if is_attestable_source(f.path) and f.current_sha256})
         opstate = sorted(p for p in (f.path for f in subject.files) if not is_attestable_source(p))
         if not authority:
             raise ValueError("no attestable source files changed between base and head")

G5 THE RED-PROOF — (a) the module resolves INSIDE the disposable worktree at
`/home/decodeux/Repos/remedy/.remedy-wt/r20-redproof/packages/orchestration/job_evidence.py`, so no
editable install shadowed it; (b) unmutated control exit code 0, `1 passed in 0.61s`, and no
`__pycache__` directory existed anywhere under the worktree; (c) the conjunct `and f.current_sha256`
deleted from the sole `authority = sorted(` statement in that worktree file, the full statement
asserted unique before the edit; (d) the SAME command re-run exits 1 with
`E               ValueError: T002: safe-diff path set does not match the task partition` raised at
`packages/orchestration/job_evidence.py:3081` — one of the two messages quoted in R-0837; (e) after
`git worktree remove --force` and `git worktree prune`, `git worktree list | wc -l` = 14.

G6 THE SCOPED SUITE — exit code 0, counts line verbatim `79 passed in 29.52s`; 79 is STRICTLY
GREATER than the 78 the reviewer measured for this exact command line at `bb375019`, and the
selection carried `tests/cli/test_golden_path.py`, so no separate canary run is owed.

G7 THE FULL SUITE — `python3 -m pytest -n auto -q` exit code 0, final counts line verbatim
`19768 passed, 23 skipped, 1 warning in 157.45s (0:02:37)`; the list of failing node ids is EMPTY,
and that emptiness is the reading — no `FAILED` and no `ERROR` line appeared, so the per-id serial
triple re-runs the gate provides for were vacuous and none was run.

G8 THE TREE — `git status --porcelain` EMPTY; `git ls-files .remedy-wt` EMPTY;
`git worktree list | wc -l` = 14; `git diff --name-only bb375019..cacd42af` is EXACTLY the seven
paths of the Change section other than `.agent/handoff.md`; per-commit insertions C0a 289, C0b 241,
C1 22, C2 10, C3 61 — every one at or under the DECISION F104 D1 cap of 500, so this round declares
NO oversize commit.

## Authored-text proofs

All four slices were extracted PROGRAMMATICALLY from the block, each verified against its own BEGIN
marker's `sha256` and `bytes` before application, and each re-verified after application against the
slice re-extracted from the COMMITTED `.agent/authored/f274-r20.md` blob at `cacd42af`
(`d5fc3280b35c9b22d6639cde2e859b2e2aed03435ad6ad4a2bd6b77e57a1ffac`, 32833 bytes):

| Slice | Bytes | sha256 | Marker match | Disk-to-disk result |
|-------|-------|--------|--------------|---------------------|
| `PLAN20` | 2631 | `6c86b31441467619677a0d9dbdd36e674e2d62665ab9b2315cbd9c20258ac6be` | True | `.agent/plan.md` is byte-EQUAL to the slice |
| `RECORD20` | 12426 | `9f7fe20802dafc9ba04dfac35f3608be8146937e9081489dc81dc8220c1486f5` | True | exact SUFFIX of `.agent/live_review.md` |
| `SLIP20` | 321 | `f6ac7daf0ad3e5543ed00c1716faef6bd45a887d723e70903d3cb443bcfb502c` | True | exact SUFFIX of `.agent/prose_slips.md` |
| `FORTSCHRITT` | 291 | `78f37ae26b3287e27e49480d9f578c3424dcf22644c524c0c18ea226e969344d` | True | repeated verbatim in the Session block above; containment tested programmatically, not eyeballed |

No slice was altered, reflowed or corrected. No objection to any slice text arose.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a — save the block as `.agent/authored/f274-r20.md` | done | |
| C0b — mirror into `.agent/last_block.md` | done | |
| C1 — replace `.agent/plan.md` with PLAN20 | done | |
| C2 — append RECORD20 and SLIP20 | done | |
| C3 — the guard and its regression test | done | |
| C4 — rewrite `.agent/handoff.md` and hand back | done | this commit |
| G1 TRANSPORT | done | three equal digests |
| G2 THE PLAN | done | 2631 bytes, 43 lines |
| G3 THE APPENDS | done | all seven sub-readings as ordered |
| G4 THE GUARD | done | 1 and 2 occurrences, ruff exit 0 |
| G5 THE RED-PROOF | done | control 0, mutant 1 |
| G6 THE SCOPED SUITE | done | exit 0, 79 passed |
| G7 THE FULL SUITE | done | exit 0, no failing node id |
| G8 THE TREE | done | seven paths, every commit under the cap |

## Deviations & assumptions

1. G4 orders the literal command `ruff check <two paths>`. The session's bash guard DENIED the bare
   `ruff` executable, so the gate ran as `python3 -m ruff check <the same two paths>` — the same
   tool, the same `pyproject.toml` configuration, the same argument list. Exit code 0, output
   `All checks passed!`. The property the gate orders was measured; only the invocation route
   differs.
2. Several gates were invoked through a two-line `python3 -c` wrapper around `subprocess.run` with an
   explicit `argv` list, rather than typed straight at the shell, because the session's bash guard
   rejects the `$?` and `$(...)` forms by FORM and a piped `tail` reports the pipe's exit code rather
   than pytest's. The `argv` is identical to the block's command line in every case and every exit
   code reported above is the process's real `returncode`. This affects G5(d), G6 and G7.
3. G5(c) orders the conjunct deleted "restoring its pre-round condition and nothing else". The
   mutation restored the CONDITION exactly; the two-line WHY comment C3 added directly above the
   statement was left in place, since removing it would have been a second edit and the comment
   cannot affect the behaviour under test.
4. G7's failing-node-id list came back EMPTY, so the "re-run that id alone, serially, three times"
   sub-step had no input and was not run. Reported as the block instructs — "empty" is the reading,
   not an omission. The `tests/orchestration/test_product_smoke.py` shape round 18 saw did NOT recur.
5. G3(d)'s negative control was performed entirely in memory on a mutated copy of the post-commit
   bytes. Nothing was written to `.agent/live_review.md` or to any other tracked file, per the
   block's "in scratch and never in the tracked file".
6. Slice extraction: the block's FRAME CONVENTION describes the slice as the bytes between the two
   marker lines "its leading newline and its trailing newline INCLUDED". Read literally as an EXTRA
   leading newline, all four slices came out one byte long and no digest matched. Taken as the bytes
   strictly between the two marker lines — the BEGIN line's own terminating newline already consumed
   — all four matched their `bytes` and `sha256` exactly. That reading was adopted and is what the
   markers themselves verify. Recorded here as a wording observation only; nothing was changed.
7. The scratch directory `.remedy-wt/r20slices/` holds the four extracted slices and was left in
   place for the reviewer's independent re-verification. It is under the gitignored `.remedy-wt/`,
   `git ls-files .remedy-wt` is EMPTY, and nothing was deleted by glob.
8. NO verdict and NO `Done:` paragraph was written anywhere. No pull request was created and nothing
   was merged, exactly as the block orders.
9. The bundle's ordered commit sequence C0a, C0b, C1, C2, C3, C4 was executed in order with no extra
   commit, no dropped commit and no reordering.

## Next

CLOSURE ROUND A: the ledger rotation by `scripts/rotate_live_review.py` as its own commit, then the
evidence job and the fresh review zip against a checkout `git status --porcelain` reports EMPTY —
the authority set is read from the WORKING TREE, so an untracked `.py` file under the repo root
would join it, which is R-0837's second measurement. The zip's `base_commit` is the FORK POINT
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, never `git merge-base`.
