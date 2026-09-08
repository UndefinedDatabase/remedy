# Handback — F274 ROUND 22 — CLOSURE ROUND A: the ledger is rotated, the evidence bundle is built and the review zip is READY_FOR_REVIEW

This file supersedes the round 21 handback. It is written by the delegated worker of round 22 on the
reviewer's authored text; the reviewer never edits a work-tree file. It carries NO verdict and NO
`Done:` paragraph — those belong to the reviewer's own authored text in `.agent/live_review.md`, and
`Done: R-0837` in particular can only be authored in closure round B, because its resolution
condition demands the READY_FOR_REVIEW package THIS round has just produced.

## Session

SESSION 8 of feature F274 · round 22 · feature rounds so far 22 of the soft limit of 25, sessions 8
of 7.

Fortschritt: F274 im Abschluss — R-0837 an beiden Stellen behoben, Ledger rotiert, Evidenzjob und Review-Zip als READY_FOR_REVIEW gebaut (Löschkarte ✅ · Reachability-Ratsche ✅ · D1–D8 ✅ · F275 ✅ · Gate ✅ · Self-Use ✅ · R-0837 ✅ · Paket ✅ · STATUS-Flip offen) — Schätzung

### The session soft limit is PAST, and the obligation it carries

    SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

F274 is at 8 sessions against a soft limit of 7, so the scope report is owed again. It is shorter
than round 21's, because this round moved the only two items that were left:

- WHAT IS FINISHED. Everything round 21 listed, plus the two artifacts F274 cannot close without:
  the ledger rotation is committed as its own commit, the feature-scoped evidence bundle is built by
  the canonical producer at a `PASS_WITH_RISKS` verdict, and a FRESH review zip reached
  `PACKAGE_STATUS=READY_FOR_REVIEW` over the accepted head.
- WHAT IS MISSING. Only closure round B: the round 22 verdict booking and the authored
  `Done: R-0837`, then the single closure commit (STATUS `[x]`, README capability sync, the one
  `consumed_by` edit setting `SU-013` to `f274`), then the pull request — which is NOT merged this
  session.
- THE PROPOSAL. Unchanged: do not re-split, run closure round B and close F274. F275 already carries
  the cluster deletion, the atomic record flip and the classic runner per DECISION F274 D8.

## CLOSURE ROUND B — THE FIVE VALUES ITS STATUS LINE IS AUTHORED FROM

This round is the only actor that knows them, and `.agent/handoff.md` is rewritten at every handback,
so closure round B must copy them into the durable STATUS line before this file is overwritten:

    Evidence job   a19161d4ff0df836
    package        remedy-review-20260908-083448-READY_FOR_REVIEW.zip
    SHA-256        a96911ffe68f7ab371bd23a5ebcb8f3844f9934c6ec1a3f87c7f0dfe1ded8103
    package path   /home/decodeux/Repos/remedy-history/zips
    accepted HEAD  5d329d2009108073dd91546ab9da0dc30cef73c7

`accepted HEAD` is C3, the ledger-rotation commit: nothing tracked was committed between it and the
package, which is exactly why the manifest's `committed_review_subject.head_commit` names it. The
`package path` segment is DECISION amend0827 D1's, and the package is NOT archived elsewhere and NOT
deleted — it is the operator's review window, left where the script built it.

## Range

Review of `6b5387ae`..THIS HANDOFF COMMIT, which is the tip of the branch and the last commit of the
round; the GATED work of the round is `6b5387ae`..`5d329d20`. The C4 sha is deliberately not written
here: it does not exist until this file is committed, and an unmeasured sha in the record is worse
than a named range endpoint.

## Commits

### 777e57e6 F274 R22 C0a: save the round 22 closure step block verbatim as the authored record
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f274-r22.md` | +290 / -0 | the round 22 step block, saved by `cp` from `.remedy-wt/f274-r22-FINAL.md`, never retyped |

### 2cc739aa F274 R22 C0b: mirror the round 22 closure block into the last-block state file
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +223 / -228 | same bytes mirrored by `cp`; the deletions are round 21's block being replaced |

### 2bcbc711 F274 R22 C1: point the plan at closure round A
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +26 / -22 | replaced byte-for-byte by the PLAN22 slice |

### 31073828 F274 R22 C2: book round 21 PASS in the record
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +2 / -0 | RECORD22 appended: round 21's PASS verdict, one paragraph, no id minted |

### 5d329d20 F274 R22 C3: rotate the closed records out of the live ledger into the append-only archive
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +0 / -88 | 32 `Gate:` records of `[x]` features and 5 resolved finding pairs moved out by `scripts/rotate_live_review.py` |
| `.agent/live_review_archive.md` | +88 / -0 | the same 88 lines appended byte-verbatim; the pre-rotation archive is a byte-exact prefix of the post-rotation one |

### C4 (this commit) F274 R22 C4: hand back closure round A with its measured gates
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | this handback; a handoff cannot table the commit that writes it (R-0149 pattern) |

Range change set, `git diff --name-only 6b5387ae 5d329d20` — exactly the five tracked paths of the
block's Change section other than `.agent/handoff.md`, and nothing else:

    .agent/authored/f274-r22.md
    .agent/last_block.md
    .agent/live_review.md
    .agent/live_review_archive.md
    .agent/plan.md

No file under `docs/`, `packages/`, `apps/`, `tests/` or `scripts/` was edited. `docs/roadmap/STATUS.md`,
`README.md` and `scripts/self_use_queue.json` were NOT touched — all three belong to closure round B.

## External actions

- `git push -u origin feature/f274-one-world-completion-part-two` after C3 → exit 0,
  `6b5387ae..5d329d20`. A second push follows this commit.
- `git worktree remove --force <path>` for all THIRTEEN disposable worktrees under `.remedy-wt/`,
  then `git worktree prune` → every call exit 0. Required by the block's constraint 6, because the
  authority set is read from the working tree. NO BRANCH WAS DELETED: `git branch --list
  'remedy/job-*'` still returns 15. `git worktree list` went from 14 lines to 1.
- `bash scripts/make_review_zip.sh --evidence-dir …` → exit 0, package written to
  `/home/decodeux/Repos/remedy-history/zips`. The package is NOT deleted.
- No PR created, none edited, none merged. No `gh` command was run.

## Verification — eight gates, each RUN, each with its real exit code and real output

### G1 TRANSPORT, at C0b — PASS

    sha256sum .remedy-wt/f274-r22-FINAL.md .agent/authored/f274-r22.md .agent/last_block.md
    exit 0
    30bb0397abbe8ebc057aacb126cffecf731f1f7abf6a277ee469c48bc63bb616  .remedy-wt/f274-r22-FINAL.md
    30bb0397abbe8ebc057aacb126cffecf731f1f7abf6a277ee469c48bc63bb616  .agent/authored/f274-r22.md
    30bb0397abbe8ebc057aacb126cffecf731f1f7abf6a277ee469c48bc63bb616  .agent/last_block.md
    bytes: 24470 / 24470 / 24470

The two committed digests are taken from the COMMITTED BLOBS (`git cat-file blob HEAD:<path> |
sha256sum`), not from the work tree. THE THREE DIGESTS ARE EQUAL. The chain proved is
scratch-original → saved copy → mirror; nothing is claimed about the emitted bytes (§3 item 37).
All three slices were extracted programmatically and verified against their OWN `BEGIN` markers
before application: PLAN22 3043 bytes `85fbbe04…`, RECORD22 4521 bytes `cb0d2110…`, FORTSCHRITT 303
bytes `ff2a85b8…` — declared and measured equal in every case.

### G2 THE PLAN, at C1 — PASS

    wc -c .agent/plan.md → 3043
    wc -l .agent/plan.md → 49          (under the AGENTS.md cap of 50)
    sha256 of the committed blob = 85fbbe0421ec6033ecef952538ffc7fbf46e4409139b691638f23751895f0594
    sha256 of the PLAN22 slice   = 85fbbe0421ec6033ecef952538ffc7fbf46e4409139b691638f23751895f0594
    `^## Goal$` occurrences       1
    `^## Next Steps$` occurrences 1

### G3 THE RECORD APPEND, at C2 — PASS, all six parts

(a) BYTES. before 658562 at `6b5387ae` + slice 4521 = after 663083. Measured after: 663083.

(b) EXACT APPEND. pre-commit blob is a byte-exact PREFIX: `True`. Slice is a byte-exact SUFFIX:
`True`.

(c) ORDERED EQUALITY by an independent reader. The post-commit file was split on blank lines, the
SLICE's own paragraphs were counted into N rather than taking N from the block: **N = 1**. The
file's last N units compared against the slice's N paragraphs IN ORDER: `True`.

(d) NEGATIVE CONTROL on the FIRST appended paragraph. One byte inside it was flipped IN SCRATCH ONLY
(slice offset 6, `' '` → `'\x00'`, inside `Gate: F274 R21 …`). Reader 1 (suffix) accepts: `False`.
Reader 2 (ordered equality) accepts: `False`. BOTH READERS REJECT IT. The tracked file was never
touched — its sha256 after the control is still `e9e15e71a5f03d308fb61fc00f3aa4ffb97e8dcc7c002af01c066c39ce044b83`,
identical to the committed blob.

(e) COUNTS over the post-commit file, every one landing on the block's predicted value:

    | reading                      | before | after | ordered |
    |------------------------------|--------|-------|---------|
    | blank-line units             | 252    | 253   | 252→253 |
    | `^Gate: `                    | 52     | 53    | 52→53   |
    | `^Gate: F274 R21 `           | 0      | 1     | 0→1     |
    | distinct `^- R-\d+ — ` ids   | 72     | 72    | 72→72   |
    | distinct `^Done: R-\d+ — `   | 7      | 7     | 7→7     |
    | OPEN SET BY DISTINCT ID      | 65     | 65    | 65→65   |

(f) Unquoted `\bHEAD\b` in the RECORD22 slice with every backtick-quoted span deleted first: **0**.

### G4 THE ROTATION, at C3 — PASS

Run by the SCRIPT only, never by hand, from the primary checkout:

    python3 -B scripts/rotate_live_review.py
    exit 0
    gate records moved: 32
    finding pairs moved: 5 (10 records)
    old ledger size: 663083 bytes
    new ledger size: 496375 bytes
    old archive size: 2535031 bytes
    new archive size: 2701739 bytes
    open findings before: 63
    open findings after: 63
    written: /home/decodeux/Repos/remedy/.agent/live_review.md and /home/decodeux/Repos/remedy/.agent/live_review_archive.md

Every predicted value landed exactly: 32 gate records, 5 finding pairs, 663083→496375, 2535031→2701739,
and the script's own open-findings count IDENTICAL before and after.

THE TWO COUNTERS, reported and deliberately NOT reconciled, per the block's own instruction: the
script says 63 before and 63 after; the record's own distinct-id reading (`^- R-\d+ — ` ids minus
`^Done: R-\d+ — ` ids) says 65 before and 65 after. The property either counter has to supply is that
it is IDENTICAL ACROSS THE ROTATION, and both are. Nothing is opened about the difference of 2.

Independently of the script:

- post-rotation OPEN SET BY DISTINCT ID: **65** (registrations 67, resolutions 2 — the rotation moved
  5 registration/resolution PAIRS, so both totals fell by 5 and the open set did not move).
- `R-0837` still present as a registration: `True`, still in the open set: `True`.
- `R-0784` still present as a registration: `True`, still in the open set: `True`.
  A rotation that archived an OPEN finding would be a defect; this is how it would have shown.
- archive append-only: pre-rotation bytes (2535031) are a byte-exact PREFIX of post-rotation bytes
  (2701739): `True`.

`git show --numstat 5d329d20`:

    0	88	.agent/live_review.md
    88	0	.agent/live_review_archive.md

Path set is EXACTLY the two files. Insertions 88, at most 500 — so this rotation needs NO oversize
exception, and F272 D18's one-per-feature allowance is left unspent. A ledger record is one long
line here, which is why F272's own rotation was 1612 insertions and this one is 88; the figure was
measured, not inherited.

### G5 THE EVIDENCE JOB, at C3, in the primary checkout — PASS

THE BASE FIRST, with the full 40-character FORK POINT and never `git merge-base`:

    base 13dfaabd93d7b6452a1d23ca698e29ed47ecf035   (length 40)
    head 5d329d2009108073dd91546ab9da0dc30cef73c7   (C3)
    git rev-list --ancestry-path 13dfaabd..5d329d20 | count → 174   exit 0
    git rev-list                 13dfaabd..5d329d20 | count → 174   exit 0
    THE TWO ARE EQUAL → True
    git merge-base --is-ancestor <base> origin/main → exit 0 (base IS an ancestor of origin/main)
    git status --porcelain → EMPTY

For the record, `git merge-base 5d329d20 origin/main` would have named `d0d8b24da2a080ebcff85e63e73a547e6a8066e6`
— main's own tip, because this branch merged `main` in at `f85200e4`. That is the base that packaged
F260's round 22 as BLOCKED_EVIDENCE; it was measured and NOT used.

THE VERIFICATION RECORD, from a REAL run at C3 and a REAL `--collect-only` over the SAME selection:

    python3 -B -m pytest tests/docs/ -q -p no:randomly
    exit 0
    303 passed in 0.49s
    python3 -B -m pytest tests/docs/ -q -p no:randomly --collect-only
    exit 0 — 303 node ids (every output line containing `::`)

ONE entry, exactly the fourteen named fields and no others:

    run_id            vr-0001         matches ^vr-\d{4,}$ → True
    command           python3 -B -m pytest tests/docs/ -q -p no:randomly
    exit_code         0
    passed            303
    failed            0
    skipped           0
    deselected        0
    selected          303             == passed+failed+skipped → True
    len(node_ids)     303             == selected → True
    test_files        ['tests/docs/test_docs_consistency.py', 'tests/docs/test_vocabulary.py']
                                      both are FILES on disk, sorted, never a directory → True
    stdout_summary    420 characters  (< 4000 → True)
    output_hash       54ee3d3888b1c4ccead127b3538b2fe188504221b685cfbd99bdd680e539a486
                                      = sha256 of EXACTLY that stdout_summary string
    head_sha          5d329d2009108073dd91546ab9da0dc30cef73c7
    duration_seconds  0.714

PRE-SCAN BEFORE CALLING THE PRODUCER, with `_unsafe_text` loaded from
`scripts/build_review_manifest.py` — the one in `scripts/`, NOT under `packages.orchestration`
(module file printed and confirmed): 303 node ids + 2 test_files scanned, **flagged: 0**.

No full-suite node-id list was recorded anywhere: `len(node_ids) == selected` forbids filtering and
the packaging metadata scan rejects the redaction-torture ids by design.

THE PRODUCER, `packages.orchestration.job_evidence.create_manual_completion_bundle`:

    evidence_dir       /home/decodeux/Repos/remedy/.remedy-wt/f274-r22-evidence-a19161d4ff0df836
                       (fresh, under the gitignored .remedy-wt/, 232 files, 5.3M, NEVER committed)
    repo_root          /home/decodeux/Repos/remedy
    base_commit        13dfaabd93d7b6452a1d23ca698e29ed47ecf035
    head_commit        5d329d2009108073dd91546ab9da0dc30cef73c7
    job_id             a19161d4ff0df836   (16 lowercase hex from secrets.token_hex(8))
    job_title          F274 one world completion part two closure evidence
    step_range         T001-T003
    prior_job_ids      []
    review_feature_id  f274
    timestamp = generated_at = 2026-09-08T06:34:30+00:00

Returned summary dict, IN FULL:

    {
      "authority_count": 60,
      "commit_count": 174,
      "head_commit": "5d329d2009108073dd91546ab9da0dc30cef73c7",
      "job_id": "a19161d4ff0df836",
      "manual_completion": true,
      "operator_attested_tasks": ["T001", "T002", "T003"],
      "partition": {"T001": 20, "T002": 20, "T003": 20},
      "total_passed": 303,
      "verdict": "PASS_WITH_RISKS"
    }

Job id `a19161d4ff0df836`; the verdict it names is `PASS_WITH_RISKS`. The bundle's own
`verification_tests.json` was read back afterwards: `schema_version 1.1.0`, `runs[0].selected 303`,
`node_ids 303`, `passed 303`, `exit_code 0`, and `output_hash 54ee3d38…` — the producer's normalizer
recomputes that hash after scrubbing and truncating, and its recomputation AGREED with the supplied
value, because the summary is 420 characters and carries no path to scrub.

### G6 THE REVIEW ZIP — PASS, `READY_FOR_REVIEW`

`git status --porcelain` EMPTY and `git rev-parse HEAD origin/feature/f274-one-world-completion-part-two`
both `5d329d20…` (branch pushed) BEFORE the build.

    bash scripts/make_review_zip.sh --evidence-dir /home/decodeux/Repos/remedy/.remedy-wt/f274-r22-evidence-a19161d4ff0df836
    exit 0
    UNCHANGED: runtime_integration_gate.json — rebuilt from source; identical to existing
    Evidence refresh completed for staged copy.
    Observability index generated from staged bytes: evidence/current/self_run_observability_index.json
    {"member_count": 4135, "authoritative_count": 60, "symlink_count": 0, "tombstone_count": 1,
     "final_path": "/home/decodeux/Repos/remedy-history/zips/remedy-review-20260908-083448-READY_FOR_REVIEW.zip",
     "final_sha256": "a96911ffe68f7ab371bd23a5ebcb8f3844f9934c6ec1a3f87c7f0dfe1ded8103",
     "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW",
     "evidence_authoritative": true, "review_subject_alignment": "PASS",
     "manifest_sha256": "55695fc69b6bcba7ae941005d5f1d9c3e8eb99efdc1b96211511c1eb0b757c3a"}

    REVIEW_PACKAGE_CREATED=true
    PACKAGE_STATUS=READY_FOR_REVIEW
    PACKAGING_CWD=/home/decodeux/Repos/remedy
    EVIDENCE_DIR=/home/decodeux/Repos/remedy/.remedy-wt/f274-r22-evidence-a19161d4ff0df836
    REVIEW_SUBJECT_ALIGNMENT=PASS
    EVIDENCE_AUTHORITATIVE=true
    REVIEW_PACKAGE_DIR=/home/decodeux/Repos/remedy-history/zips
    ZIP_PATH=/home/decodeux/Repos/remedy-history/zips/remedy-review-20260908-083448-READY_FOR_REVIEW.zip
    Included files: 4135
    Branch: feature/f274-one-world-completion-part-two
    Commit: 5d329d2009108073dd91546ab9da0dc30cef73c7

Required values:

    PACKAGE_STATUS            READY_FOR_REVIEW     (required; met)
    REVIEW_SUBJECT_ALIGNMENT  PASS                 (required; met)
    EVIDENCE_AUTHORITATIVE    true                 (required; met)
    package FILENAME          remedy-review-20260908-083448-READY_FOR_REVIEW.zip
    package ABSOLUTE dir      /home/decodeux/Repos/remedy-history/zips
    size                      24948653 bytes (24M)
    member_count              4135
    authoritative_count       60
    tombstone_count           1                    (required ≥ 1; met)
    validation_errors         none — the status is READY_FOR_REVIEW, so none were emitted

SHA-256, printed by the script and RECOMPUTED from the file on disk:

    script-printed  a96911ffe68f7ab371bd23a5ebcb8f3844f9934c6ec1a3f87c7f0dfe1ded8103
    recomputed      a96911ffe68f7ab371bd23a5ebcb8f3844f9934c6ec1a3f87c7f0dfe1ded8103
    AGREE           True

Manifest `committed_review_subject`, read back OUT OF THE ZIP (`.review_zip_manifest.json`):

    base_commit      13dfaabd93d7b6452a1d23ca698e29ed47ecf035   (the fork point)
    head_commit      5d329d2009108073dd91546ab9da0dc30cef73c7   (C3, the accepted HEAD)
    base_is_ancestor True    commit_count 174    file_count 109

It spans the fork point to C3, exactly as required. The package was NOT deleted and NOT moved.

THE TOMBSTONE, and the aside beside it. The `tombstone_count 1` the script reports comes from the
packaged `evidence/current/review_archive_plan.json`, whose `tombstones` list holds exactly one
entry: `{"path": "apps/cli/commands/feature_cmd.py", "base_sha256": "db4fbfed…"}` — the source file
this branch deletes, and precisely the deletion R-0837 was about. TWO OTHER artifacts in the SAME
package carry a tombstone reading of zero and are reported here rather than left for someone to
discover: `evidence/current/current_change_content_proof.json` has `"tombstone_count": 0` with
`"tombstones": {}` (the producer writes those two fields as constants), and the zip manifest's
`committed_review_subject.tombstones` is `[]`. The gate's own reading is the packaging summary's,
which is 1; the other two are not claimed to say anything they do not.

### G7 THE PRECONDITIONS, at C3, in the primary checkout, run SERIALLY — PASS, with R-0648 named

    python3 -B -m pytest tests/docs/ -q -p no:randomly
    exit 0 — 303 passed in 0.59s

    python3 -B -m pytest tests/cli/test_golden_path.py -q -p no:randomly
    exit 0 — 42 passed in 20.82s

Both land on the counts the reviewer measured at `6b5387ae`: 303 and 42.

    packages.orchestration.integrity_gate.run_integrity_checks()
    result type   IntegrityGateResult
    .passed       True          (an ATTRIBUTE, not a dict key)
    .fail_count   0             (an ATTRIBUTE, not a dict key)
    checks total  5

The check named `high_blockers_open`, walked out of `.checks` and quoted VERBATIM:

    name    : high_blockers_open
    status  : IntegrityStatus.PASS
    message : 'no open blocker/high findings'

THAT MESSAGE IS FALSE, and DECISION F272 D17 requires this close to say so out loud and to rest on
the named list rather than on the check. Measured independently over the post-rotation ledger, with
severity read as the FIRST token after the em dash, the OPEN High findings are FIVE:

    R-0803  the test suite writes into the operator's real data root
    R-0804  the cockpit's brain endpoint crashes for a ping-pong job
    R-0806  a real Sonnet run blocked and no command shows a reviewer finding
    R-0807  the token ledger recorded one call for a run that made at least six
    R-0837  the canonical closure evidence producer cannot package a deleted source file

    open High count : 5

Four of them — R-0803, R-0804, R-0806, R-0807 — are F273's rather than this feature's, per DECISION
F272 D12. R-0837 is FIXED at both sites but NOT YET RESOLVED, because only reviewer-authored `Done:`
text resolves anything and its resolution condition demands the package this round has just built.
That the check reports PASS while five High findings are open IS finding R-0648, which is itself
open and Medium.

### G8 THE TREE, at C3 — PASS

    git status --porcelain              → EMPTY
    git ls-files .remedy-wt             → EMPTY (0 lines; the directory is gitignored)
    git worktree list | wc -l           → 1     (was 14; the 13 disposable ones were removed before G5)
    git diff --name-only 6b5387ae 5d329d20 → exactly the five tracked paths listed under Commits

Per-commit INSERTIONS, each at most 500 per AGENTS.md DECISION F104 D1:

    | commit    | insertions | cap  |
    |-----------|------------|------|
    | 777e57e6  | 290        | ≤500 |
    | 2cc739aa  | 223        | ≤500 |
    | 2bcbc711  | 26         | ≤500 |
    | 31073828  | 2          | ≤500 |
    | 5d329d20  | 88         | ≤500 |

No oversize commit was made and none is declared. C4's own numbers belong to the next round's ledger
entry.

## Open findings

**65 open by distinct id** over the post-rotation `.agent/live_review.md` (67 distinct
`^- R-\d+ — ` registrations minus 2 distinct `^Done: R-\d+ — ` resolutions), unchanged across both
this round's append and the rotation. The rotation script's own counter reads **63** before and 63
after; the two counters have differed by exactly 2 for several features and neither moved, which is
the property that matters. Five of the 65 are High and are named under G7.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C0a — save the block as `.agent/authored/f274-r22.md` | done | `cp` from the scratch original; digest equal |
| C0b — mirror into `.agent/last_block.md` | done | `cp`; all three digests equal |
| C1 — replace `.agent/plan.md` with PLAN22 | done | byte-identical, 3043 bytes, 49 lines |
| C2 — append RECORD22 to `.agent/live_review.md` | done | 658562→663083, prefix/suffix/ordered all true |
| C3 — the ledger rotation, its own commit | done | script only, exit 0, 88/88, two paths |
| G1 transport | done | three digests equal at `30bb0397…` |
| G2 the plan | done | 3043 bytes, 49 lines, both headings present |
| G3 the record append | done | all six parts, including the negative control |
| G4 the rotation | done | every predicted figure landed; archive prefix true |
| G5 the evidence job | done | base 174 == 174; producer `PASS_WITH_RISKS`; job `a19161d4ff0df836` |
| G6 the review zip | done | `PACKAGE_STATUS=READY_FOR_REVIEW`; SHA-256 recomputed and agreeing |
| G7 the preconditions | done | 303 and 42, exit 0 each; gate `.passed True`, `.fail_count 0`; R-0648 named |
| G8 the tree | done | porcelain empty, five paths, every commit under the cap |
| C4 — rewrite the handback and push | done | this file |

Nothing was skipped and nothing was deviated from the ordered commit sequence.

## Authored-text proofs

Three reviewer-authored texts were applied this round, each extracted PROGRAMMATICALLY from the
committed `.agent/authored/f274-r22.md` — the slice being the bytes strictly between its `BEGIN` and
`END` lines — and each verified against its OWN `BEGIN` marker before it was applied:

| slice       | declared bytes | measured | declared sha256 | measured equal |
|-------------|----------------|----------|-----------------|----------------|
| PLAN22      | 3043           | 3043     | `85fbbe04…f0594` | yes |
| RECORD22    | 4521           | 4521     | `cb0d2110…6dc1c2` | yes |
| FORTSCHRITT | 303            | 303      | `ff2a85b8…828d17` | yes |

Disk-to-disk after application: `.agent/plan.md` sha256 equals the PLAN22 slice's; the RECORD22 slice
is a byte-exact SUFFIX of `.agent/live_review.md` as committed at C2, with ordered paragraph equality
proved by a second, independent reader. The FORTSCHRITT line is reproduced verbatim in the Session
section above.

## Deviations & assumptions

1. **Exit codes captured through an explicit-argv `subprocess.run` wrapper**
   (`.remedy-wt/r22_run.py`), because the session's bash guard rejects `$?` by FORM. Established
   deviation, unchanged from earlier rounds. Every exit code reported above is the wrapper's real
   `returncode`, never an inference from output.
2. **Thirteen disposable worktrees were removed before G5**, with `git worktree remove --force`
   followed by `git worktree prune`. This is ordered by the block's constraint 6, but it is a
   destructive external action and is declared as such. NO BRANCH WAS DELETED — all 15
   `remedy/job-*` branches still exist; `git worktree remove` detaches the checkout only. The
   `--force` flag was used because several of those checkouts held modified files from earlier
   mutation red-proofs. G8's `git worktree list | wc -l` therefore reads 1 where round 21 read 14,
   and the change is intended, not drift.
3. **The G3(d) negative control flipped a space to a NUL byte** (`0x20 ^ 0x20`) at slice offset 6,
   inside the first appended paragraph. NUL is a legal UTF-8 byte and both readers rejected the
   corrupted variant on content, not on a decode error. The flip existed only in a scratch buffer;
   the tracked file's sha256 was re-measured afterwards and is unchanged.
4. **G7's independent High-finding list was measured twice, and the FIRST reading was wrong.**
   Matching `\bHigh\b` anywhere in a registration's description returned 11 ids, because several
   Medium findings use the word "High" in their prose. Anchoring severity to the FIRST token after
   the em dash returns 5 — R-0803, R-0804, R-0806, R-0807, R-0837 — which is the list the block
   names and the list reported above. The wrong reading is stated here so the reviewer can see which
   definition the number rests on.
5. **The producer recomputes `output_hash`.** `manual_attestation._vt_run_v11` scrubs paths, truncates
   `stdout_summary` to its last 2000 characters and ALWAYS recomputes `output_hash`, discarding any
   caller-supplied value (R-0792/R-0793). The supplied summary is 420 characters and carries no path,
   so the recomputation agreed byte for byte with the value computed as the block ordered. Nothing
   diverged; the mechanism is declared because a longer summary WOULD have diverged.
6. **The tombstone reading is not uniform across the package.** Reported in full under G6: the
   packaging summary says 1 (from `review_archive_plan.json`, naming
   `apps/cli/commands/feature_cmd.py`), while the evidence bundle's content proof says 0 and the zip
   manifest's `committed_review_subject.tombstones` is `[]`. The gate is met on the packaging
   summary's reading. No finding is raised and nothing was changed to make the three agree.
7. **Scratch scripts live under `.remedy-wt/`** (`r22_extract.py`, `r22_g3.py`, `r22_g5.py`,
   `r22_g7.py`, `r22_run.py`, and the extracted slice files). That directory is gitignored, so
   `git status --porcelain` stayed EMPTY at the moment the evidence job and the zip ran, and
   `git ls-files .remedy-wt` is empty. Nothing was deleted by glob; the evidence directory and the
   package both remain on disk at their exact paths.

No departure from the block's ordered commit sequence occurred: C0a, C0b, C1, C2, C3, then the
untracked G5/G6 artifacts, then C4. No commit was amended, added, dropped or reordered.

## Next

Closure round B: book round 22's verdict and author `Done: R-0837` in `.agent/live_review.md`, then
the single closure commit — the STATUS `[x]` line authored from the five values in the block near the
top of this file, the README capability sync, and the one `consumed_by` edit setting `SU-013` to
`f274` — then open the pull request, which is NOT merged this session.
