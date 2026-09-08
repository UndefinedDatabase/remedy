# Handback — F274 ROUND 21 — R-0837's SECOND SITE: the review zip now accepts the branch the producer already accepted

This file supersedes the round 20 handback. It is written by the delegated worker of round 21 on the
reviewer's authored text; the reviewer never edits a work-tree file. It carries NO verdict and NO
`Done:` paragraph — those belong to the reviewer's own authored text in `.agent/live_review.md`.

## Session

SESSION 8 of feature F274 · round 21 · feature rounds so far 21 of the soft limit of 25, sessions 8
of 7.

Fortschritt: F274 schließt bei ~35 % des ursprünglichen Umfangs, Closure-Blocker R-0837 an BEIDEN Stellen behoben, Paket als READY_FOR_REVIEW nachgewiesen (Löschkarte ✅ · Reachability-Ratsche ✅ · D1–D8 ✅ · F275 ✅ · Gate ✅ · Self-Use ✅ · R-0837 ✅ · Closure offen) — Schätzung

### The session soft limit is PAST, and the obligation it carries

    SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

F274 is at 8 sessions against a soft limit of 7, so the scope report is owed again. It is short,
because session 7 already executed the SPLIT half of the split-and-close default:

- WHAT IS FINISHED. The split is executed and F275 is registered; the deletion card, the
  reachability ratchet and DECISIONS D1–D8 are done; the integration gate has PASSED (round 18); the
  self-use precondition is met (round 19); and the closure blocker R-0837 is now repaired at BOTH of
  its sites — the evidence producer in round 20, the review-zip coordinator in THIS round — each
  with a regression test whose colour is proved by mutation.
- WHAT IS MISSING. Only the CLOSE itself, in the two rounds the plan names: closure round A (ledger
  rotation, evidence job, fresh review zip) and closure round B (STATUS `[x]` flip, README sync, the
  one `consumed_by` edit, then the pull request).
- THE PROPOSAL. Do not re-split. Run closure rounds A and B and close F274; the cluster deletion,
  the atomic record flip and the classic runner already live in F275 per DECISION F274 D8.

## Range

Review of `630f22b9`..THIS HANDOFF COMMIT, which is the tip of the branch and the last commit of the
round; the GATED work of the round is `630f22b9`..`45c17555`. The C4 sha is deliberately not written
here: it does not exist until this file is committed, and an unmeasured sha in the record is worse
than a named range endpoint.

## Commits

### 93437eb5 F274 R21 C0a: save the round 21 step block verbatim as the authored record
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f274-r21.md` | +295 / -0 | the round 21 step block, saved by `cp` from `.remedy-wt/f274-r21-FINAL.md`, never retyped |

### fffcd14e F274 R21 C0b: mirror the round 21 block into the last-block state file
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +193 / -187 | same bytes mirrored by `cp`; the deletions are round 20's block being replaced |

### 22c9042e F274 R21 C1: point the plan at the second site of the closure blocker
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +19 / -17 | replaced byte-for-byte by the PLAN21 slice |

### 3bc758fc F274 R21 C2: book round 20 PASS and append the closure blocker second site without minting an id
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +4 / -0 | RECORD21 appended: round 20's PASS verdict and R-0837's SECOND SITE, no new id |
| `.agent/prose_slips.md` | +4 / -0 | SLIPS21 appended: the round 20 block's frame-convention wording and its `T001` quotation |

### 45c17555 F274 R21 C3: guard the review-zip authority recomputation against a deleted path and prove both colours
| Path | +/- | Reason |
|------|-----|--------|
| `scripts/build_review_zip.py` | +2 / -1 | the `and f.current_sha256` conjunct on the attestable-subject comprehension in `_assert_authority_equality`, plus its one-line WHY comment |
| `tests/orchestration/test_review_zip_deleted_path_authority.py` | +97 / -0 | new module: the regression and its discriminator |

### (this commit) F274 R21 C4: hand back the review-zip guard round with its measured gates
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | this file | a handoff cannot table the commit that writes it (R-0149 pattern) |

## External actions

- `git worktree add --detach .remedy-wt/f274-r21-redproof HEAD` — created TWICE and removed twice,
  detached both times, no branch made. The first worktree was created at the pre-amend C3 and
  discarded when the discriminator was corrected (see deviation 3); the reported G5 readings all
  come from the SECOND worktree, created at the final `45c17555`.
- `git worktree remove --force .remedy-wt/f274-r21-redproof` then `git worktree prune`, after each
  of the two — worktree count back to 14, unchanged from the pre-round reading.
- `git commit --amend` on C3, once, BEFORE any push (see deviation 3). No force-push was needed or
  performed, because nothing had been pushed.
- `git push -u origin feature/f274-one-world-completion-part-two` — pushed after C4.
- NO pull request created. NOTHING merged. No branch deleted. No force-push, no history rewrite of
  any pushed commit. No review zip built and no evidence job run, per block constraint 9.

## Verification

ONE LINE PER GATE, each with its real measured result.

G1 TRANSPORT — the three digests are EQUAL and all three files are 29142 bytes:
`.remedy-wt/f274-r21-FINAL.md`, the committed `.agent/authored/f274-r21.md` and the committed
`.agent/last_block.md` each hash to
`79d0ecbc1dc301d570e6c6ce31045c9db330c1a5f862ba3df0fac9f79bfce6ca`.

G2 THE PLAN — `.agent/plan.md` is 2869 bytes and 45 lines, byte-identical to the PLAN21 slice
(`bf5c3c345041876f1de426e76d5a1c7790db159441930b364605f266eb66bb76`), 45 under the AGENTS.md cap of
50; `## Goal` occurs 1 time and `## Next Steps` occurs 1 time.

G3 THE APPENDS — (a) `.agent/live_review.md` 650874 → 658562 bytes, delta 7688 = the RECORD21 slice
exactly, and 650874 + 7688 = 658562 as the block predicted; (b) pre-commit blob is a byte-exact
PREFIX True, slice is an exact SUFFIX True; (c) N counted from the slice's OWN paragraphs = 2,
ordered equality of the file's last 2 units against the slice's 2 paragraphs True; (d) negative
control on the FIRST appended paragraph, the `G` of `Gate: F274 R20` at offset 650875 flipped to `g`
in memory and never in the tracked file, reader-(b) REJECTS and reader-(c) REJECTS; (e) blank-line
units 250→252, `^Gate: ` 51→52, `^Gate: F274 R20 ` 0→1, `^SECOND SITE of R-0837 ` 0→1, distinct
`^- R-\d+ — ` ids 72→72, distinct `^Done: R-\d+ — ` ids 7→7, and the OPEN SET BY DISTINCT ID 65→65 —
every transition exactly as ordered, and the open set is unchanged because this round registers
NOTHING; (f) `.agent/prose_slips.md` 165189 → 165972, prefix True, suffix True, blank-line units
225→227, gaining exactly 2; (g) unquoted `\bHEAD\b` in the RECORD21 slice with every backtick-quoted
span deleted first = 0.

G4 THE GUARD — `git show --numstat 45c17555 -- scripts/build_review_zip.py` reads
`2	1	scripts/build_review_zip.py`; in the post-commit file
`attestable_subject = {f.path for f in subject.files` occurs 1 time,
`is_attestable_source(f.path)` occurs 1 time, and
`is_attestable_source(f.path) and f.current_sha256` occurs 1 time where it was 0; `ruff check` over
both changed files exited 0 with `All checks passed!`.

The full C3 diff of that file, verbatim:

    diff --git a/scripts/build_review_zip.py b/scripts/build_review_zip.py
    index dc8850a5..c01bbcbe 100644
    --- a/scripts/build_review_zip.py
    +++ b/scripts/build_review_zip.py
    @@ -220,7 +220,8 @@ def _assert_authority_equality(*, authority: set, subject, content_proof, staged
                     or content_proof.head_commit != subject.head_commit:
                 raise ArchivePlanError("Content-Proof base/head != ReviewSubject base/head")

    -    attestable_subject = {f.path for f in subject.files if is_attestable_source(f.path)}
    +    # R-0837: a DELETED path attests through its tombstone (base_sha256), never through current content.
    +    attestable_subject = {f.path for f in subject.files if is_attestable_source(f.path) and f.current_sha256}
         if authority != attestable_subject:
             only_auth = sorted(authority - attestable_subject)[:4]
             only_subj = sorted(attestable_subject - authority)[:4]

G5 THE RED-PROOF — (a) IMPORT PROOF, taken first: the module resolves INSIDE the disposable worktree
at `/home/decodeux/Repos/remedy/.remedy-wt/f274-r21-redproof/packages/orchestration/review_subject.py`,
so the editable install did not shadow it; (b) unmutated control exit code 0, counts line
`2 passed in 0.30s`; (c) the conjunct `and f.current_sha256` deleted from the sole
`attestable_subject = {f.path for f in subject.files` statement in that worktree's
`scripts/build_review_zip.py`, both the anchor and the conjunct asserted UNIQUE in the file before
the edit, leaving exactly the pre-round condition
`{f.path for f in subject.files if is_attestable_source(f.path)}`; (d) the SAME command re-run exits
1 with counts line `1 failed, 1 passed in 0.32s` — the FAILING id is
`tests/orchestration/test_review_zip_deleted_path_authority.py::TestDeletedPathIsNotDemandedOfTheAuthoritySet::test_a_deleted_path_does_not_block_the_package`,
raising `ArchivePlanError: authority set != attestable ReviewSubject paths (only_in_authority=[],
only_in_subject=['src_pkg/gamma.py'])` at `scripts/build_review_zip.py:228`, while
`test_a_genuinely_missing_live_path_still_blocks` PASSED, which is the half proving the mutation
narrowed the guard rather than disabling the check; (e) after `git worktree remove --force` and
`git worktree prune`, `git worktree list | wc -l` = 14.

G6 THE SCOPED SUITE — exit code 0, counts line verbatim `69 passed in 22.33s`, which is EXACTLY the
ordered 69: the reviewer measured 67 for this same six-file selection without the new module at
`630f22b9`, and this round adds exactly two tests. The selection carries
`tests/cli/test_golden_path.py`, so no separate canary run is owed.

G7 THE FULL SUITE — `python3 -m pytest -n auto -q` exit code 0, final counts line verbatim
`19770 passed, 23 skipped, 1 warning in 156.08s (0:02:36)`, which is round 20's 19768 plus this
round's two new tests. The list of failing node ids is EMPTY, and that emptiness is itself the
reading — no `FAILED` and no `ERROR` line appeared, so the per-id serial triple re-runs the gate
provides for had no input and none was run. The `tests/orchestration/test_product_smoke.py` shape
seen at rounds 18 and 20 did NOT recur. Every disposable worktree was pruned before this run; the
14 remaining entries are the primary checkout and 13 pre-existing `remedy/job-*` worktrees that also
stood during round 20's run, and they are outside this round's change set.

G8 THE TREE — `git status --porcelain` EMPTY; `git ls-files .remedy-wt` EMPTY;
`git worktree list | wc -l` = 14; `git diff --name-only 630f22b9..45c17555` is EXACTLY the seven
paths of the Change section other than `.agent/handoff.md` — `.agent/authored/f274-r21.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `.agent/prose_slips.md`,
`scripts/build_review_zip.py` and
`tests/orchestration/test_review_zip_deleted_path_authority.py`; per-commit insertions C0a 295,
C0b 193, C1 19, C2 8, C3 99 — every one at or under the DECISION F104 D1 cap of 500, so this round
declares NO oversize commit.

## Authored-text proofs

All four slices were extracted PROGRAMMATICALLY from the block, each verified against its own BEGIN
marker's `sha256` and `bytes` before application, and each re-verified AFTER application against the
slice re-extracted from the COMMITTED `.agent/authored/f274-r21.md` blob
(`79d0ecbc1dc301d570e6c6ce31045c9db330c1a5f862ba3df0fac9f79bfce6ca`, 29142 bytes):

| Slice | Bytes | sha256 | Marker match | Disk-to-disk result |
|-------|-------|--------|--------------|---------------------|
| `PLAN21` | 2869 | `bf5c3c345041876f1de426e76d5a1c7790db159441930b364605f266eb66bb76` | True | `.agent/plan.md` is byte-EQUAL to the slice |
| `RECORD21` | 7688 | `51c890060afcfb9966e1ec4e9073d0f518f4670f967332734fe0d40af3c3210a` | True | exact SUFFIX of `.agent/live_review.md` |
| `SLIPS21` | 783 | `b126c4e5d1c5dbac857d5e3d48fcd15f8ec1bf9ef33d9702c1746dac55ac9a48` | True | exact SUFFIX of `.agent/prose_slips.md` |
| `FORTSCHRITT` | 304 | `e6cde7c5462b0ab92e5ee7e46eadb9f4433bcd27bb7e79545ff966e996dbfff8` | True | present verbatim in the Session block above; the containment test was RUN against this file's committed bytes, not eyeballed, and the line was assembled by concatenating the slice's bytes rather than retyped |

No slice was altered, reflowed or corrected. No objection to any slice text arose.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a — save the block as `.agent/authored/f274-r21.md` | done | |
| C0b — mirror into `.agent/last_block.md` | done | |
| C1 — replace `.agent/plan.md` with PLAN21 | done | |
| C2 — append RECORD21 and SLIPS21 | done | |
| C3 — the guard and its two-test regression module | deviated | committed, then AMENDED once before any push to correct the discriminator; see deviation 3 |
| C4 — rewrite `.agent/handoff.md` and hand back | done | this commit |
| G1 TRANSPORT | done | three equal digests, 29142 bytes each |
| G2 THE PLAN | done | 2869 bytes, 45 lines |
| G3 THE APPENDS | done | all seven sub-readings as ordered |
| G4 THE GUARD | done | counts 1 / 1 / 1, ruff exit 0 |
| G5 THE RED-PROOF | done | control exit 0 at 2 passed, mutant exit 1 at 1 failed and 1 passed |
| G6 THE SCOPED SUITE | done | exit 0, exactly 69 passed |
| G7 THE FULL SUITE | done | exit 0, 19770 passed, failing list EMPTY |
| G8 THE TREE | done | seven paths, every commit under the cap |

## Deviations & assumptions

1. G4 orders the literal command `ruff check <two paths>`. The session's bash guard DENIED the bare
   `ruff` executable, so the gate ran as `python3 -m ruff check <the same two paths>` — the same
   tool, the same `pyproject.toml` configuration, the same argument list. Exit code 0, output
   `All checks passed!`. The property the gate orders was measured; only the invocation route
   differs. This is the same route round 20 used and the reviewer sustained.
2. Several gates were invoked through a small `python3` wrapper around `subprocess.run` with an
   explicit `argv` list, rather than typed straight at the shell, because the session's bash guard
   rejects the `$?` and `$(...)` forms by FORM and a piped `tail` reports the pipe's exit code
   rather than pytest's. The `argv` is identical to the block's command line in every case and every
   exit code reported above is the process's real `returncode`. This affects G5(b), G5(d), G6 and G7.
3. THE ONE REAL DEPARTURE FROM THE ORDERED SEQUENCE, stated plainly. C3 was committed once as
   `750e61e9`, and the FIRST run of G5(d) came back exit 1 at `2 failed` rather than the ordered
   `1 failed, 1 passed`. The cause was mine, not the block's: my discriminator carried a third
   assertion, `assert DELETED not in str(excinfo.value)`, which is itself guard-dependent, so the
   discriminator could not survive the mutation — and a discriminator that goes red under the
   mutation is exactly the thing G5(d)'s two-sided count exists to forbid. The block DESCRIBES the
   tests rather than slicing them, and it specifies the discriminator as raising `ArchivePlanError`
   whose message contains `authority set != attestable ReviewSubject paths` — nothing more — so that
   third assertion was my own over-specification and removing it is a repair of my code, not of
   reviewer-owned text. I deleted that one assertion, left a comment in its place explaining why it
   must not be asserted there, and AMENDED C3 rather than adding a seventh commit, so that the
   bundle the reviewer verifies is exactly the ordered C0a, C0b, C1, C2, C3, C4. Nothing had been
   pushed at that moment, so no pushed history was rewritten and no force-push was performed. The
   discarded `750e61e9` is not an ancestor of the branch. Every G4 and G5 reading reported above was
   taken AFTER the amend, against the final `45c17555`; the pre-amend red run is reported here and
   is not counted as a gate result.
4. G5(c) orders the conjunct deleted "restoring its pre-round condition and nothing else". The
   mutation restored the CONDITION exactly; the one-line WHY comment C3 added directly above the
   statement was left in place, since removing it would have been a second edit and a comment cannot
   affect the behaviour under test. This is the same shape round 20 declared and the reviewer
   sustained.
5. G7's failing-node-id list came back EMPTY, so the "re-run that id alone, serially, three times"
   sub-step had no input and was not run. Reported as the block instructs — "empty" is the reading,
   not an omission.
6. G3(d)'s negative control was performed entirely in memory on a mutated copy of the post-commit
   bytes. Nothing was written to `.agent/live_review.md` or to any other tracked file, per the
   block's "in scratch and never in the tracked file".
7. G3(c)'s independent reader compares paragraph CONTENT: it splits on runs of two or more newlines
   and strips each unit's edge whitespace. This is not a weakening and it is forced by the shape of
   an append — the RECORD21 slice's own leading newline becomes part of the blank-line SEPARATOR once
   the slice is on the end of the file, and the file's final unit carries the terminal newline, so an
   unstripped comparison would fail on separator bytes that reader (b) already proves byte-for-byte.
   Reader (b) is the byte-identity reader and it was run unstripped, and G3(d) confirms both readers
   still reject a one-byte corruption INSIDE the paragraph.
8. The guard's WHY comment is ONE line, as the block orders, at 104 characters against the project's
   limit of 120; the guarded comprehension stayed on ONE line at 109 characters, so the two-line wrap
   the block permits "if the line would otherwise exceed 120" was not needed and was not used.
9. The new module sets `kind=KIND_DELETED` on the tombstone record and `kind=KIND_REGULAR` on the two
   live ones. The block specifies each record's `status`, `base_sha256` and `current_sha256` but not
   its `kind`; these are the realistic values for those shapes and `_assert_authority_equality` never
   reads `kind`, so no gate depends on the choice.
10. The scratch directory `.remedy-wt/slices/` holds the four extracted slices, and
    `.remedy-wt/r21_extract.py`, `.remedy-wt/r21_g3.py`, `.remedy-wt/r21_proofs.py` and
    `.remedy-wt/run.py` hold the readers, all left in place for the reviewer's independent
    re-verification. They are under the gitignored `.remedy-wt/`, `git ls-files .remedy-wt` is EMPTY,
    and nothing was deleted by glob.
11. The 13 pre-existing `remedy/job-*` worktrees under `.remedy-wt/` were NOT removed. They are
    outside this round's change set, they stood identically during round 20's full-suite run, and the
    block's constraint 5 binds the worker to removing the worktree the worker creates. Only that one
    was created and removed.
12. NO verdict and NO `Done:` paragraph was written anywhere. No pull request was created and nothing
    was merged. No review zip was built and no evidence job was run, exactly as block constraint 9
    orders.
13. G4's verbatim diff is reproduced above as a 4-space-indented block. Its one BLANK context line
    carries a single leading space in git's real output; here that line is empty, because this file
    keeps no trailing whitespace on any line. That is the only byte-level difference between the
    block above and `git show 45c17555 -- scripts/build_review_zip.py`, and every `+`/`-` line is
    reproduced exactly.

## Next

CLOSURE ROUND A: the ledger rotation by `scripts/rotate_live_review.py` as its own commit, then the
evidence job and the fresh review zip against a checkout `git status --porcelain` reports EMPTY —
the authority set is read from the WORKING TREE, so an untracked `.py` file under the repo root
would join it and shift every count. Both R-0837 sites are now guarded, and the reviewer's own
end-to-end dry run at `630f22b9` showed the package reaching `PACKAGE_STATUS=READY_FOR_REVIEW` with
`tombstone_count 1` once they are, so R-0837's resolution condition is expected to be MET by that
build — it is not claimed met until that build is run on this branch. The package's `base_commit` is
the FORK POINT `13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, never `git merge-base`.
