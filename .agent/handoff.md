# Handback — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 23 · The closure sequence's evidence half: the bundle, the package, and the one finding the self-use run owes

## Session

SESSION 5 of feature F283 · round 23 · rounds so far 23

This round booked round 22's PASS, registered R-1035 from the self-use run's own
defect reader (closure precondition 6), built the feature's evidence bundle
against the fork point `d0d40e89` (evidence job `f283r23e1001`), and built the
fresh review package: `remedy-review-20260922-215357-READY_FOR_REVIEW.zip`,
`PACKAGE_STATUS=READY_FOR_REVIEW`. Nothing closes this round — no ledger
rotation, no STATUS/README edit, no PR.

Context self-assessment: a comfortable majority of the working budget remained
at the point this handoff was written; the round's two slow steps (the scoped
pytest run under the evidence job, and the review-zip build) both ran once and
to completion.

## Range

Review of `15145f71`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 173 | 173 | True |
| sha256 | `f810a9e6ebb487780e0a2491ada0a2eaaaaeff8c85fee8b812537027b4fdb065` | `f810a9e6ebb487780e0a2491ada0a2eaaaaeff8c85fee8b812537027b4fdb065` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `15145f71`, matching the delegation message.
- `git stash list`, first line before C1: `stash@{0}: WIP on (no branch):
  365051fa F277 R17 C3: rewrite handoff for round 17 with the rebuilt package
  readings` (pre-existing project debt, untouched this round).
- `git worktree list`, before C1: primary checkout + `.remedy-wt/job-129b3ad7206d4f8d`
  (round 22's self-use leftover, per its own constraint 7 — not this round's to
  remove).
- `git branch --list 'remedy/job-*' | wc -l`, before C1: **38**.

Payload readings against the PAYLOADS table (lines = newline count):

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| ledger.md | 4/4 | 6089/6089 | True |
| plan.md | 34/34 | 1507/1507 | True |

## Commits

### 91f15a19 F283 R23 C1: copy round 23 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r23-block.md | +173/-0 | byte-for-byte copy of this round's step block (`shutil.copyfile`) |
| .agent/authored/f283-r23-ledger.md | +4/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r23-plan.md | +34/-0 | byte-for-byte copy of plan.md |

Measured insertions (`git show --numstat`): **211** (173+4+34).

### 9e40d5fe F283 R23 C2: book round 22's PASS and register R-1035
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | append ledger.md payload: round 22's `Gate:` entry and R-1035's Medium finding (the closure's self-use run's own defect strings) |
| .agent/plan.md | +13/-13 | rewrite to plan.md payload, byte-identical |

Measured insertions: **17** (4+13); 13 deletions from the plan.md rewrite. This
commit's sha is this closure's **ACCEPTED HEAD**: `9e40d5fe2133ab343fbe3ef64ed584cbcb141062`.

### (this commit) F283 R23 C3: rewrite handoff for round 23 with the evidence and package readings
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback
cannot table the commit that writes it.

## External actions

- **A1 — the evidence job** (algorithm step 1, no commit — the evidence dir is
  gitignored under `.remedy-wt/`). Ran
  `.remedy-wt/f283-r23-scratch/create_f283_evidence.py`, adapted from
  `.remedy-wt/f273-r24/create_f273_evidence.py` per the block's naming: base
  `d0d40e89b6aa9afcebd639df7a7c16a260059537`, head `9e40d5fe2133ab343fbe3ef64ed584cbcb141062`
  (C2), `job_id=f283r23e1001`, `job_title="F283 round 23 evidence job"`,
  `step_range=T001-T002`, `review_feature_id=f283`, five sorted `TEST_FILES`.
  Node ids collected via `--collect-only`: 523, matching `selected`. Real
  pytest run: 523 passed, 0 failed, 0 skipped, exit 0. `output_hash`
  (sha256 of the real pytest stdout):
  `e0965c184108b26226689a2422359239479a1929a5d0de3449db990ff680dc88`.
  Bundle built at `.remedy-wt/f283-r23-evidence/` via
  `create_manual_completion_bundle`; `validate_evidence_candidate` answered
  `is_valid_current_run=True`, `validation_errors=[]`.
- Before paying for the package build: `build_review_manifest.validate_verification_tests`
  over the produced `verification_tests.json` answered `(problems=[], passed=523)`
  — an EMPTY problem list.
- **RED CONTROL** (in memory only, never on the real bundle): the real
  `node_ids` list validates clean (`problems=[]`, `passed=523`); a copy with
  ONE planted id carrying an absolute path
  (`/home/decodeux/Repos/remedy/tests/cli/test_exit_codes.py::test_planted`)
  is REJECTED by the same validator with two problems: `"...node_ids[523]
  carries a local absolute path"` and `"...node_ids count (524) != selected
  (523)"`. Both readings recorded — a check that cannot fail proves nothing
  when it passes, and this one visibly can.
- `git push origin feature/f283-machine-contracts-part-two` after C2 (A2's
  precondition that the branch be pushed before the package build) —
  `15145f71..9e40d5fe feature/f283-machine-contracts-part-two ->
  feature/f283-machine-contracts-part-two`.
- **A2 — the review package** (algorithm step 2, no commit). Built with
  `bash scripts/make_review_zip.sh --evidence-dir .remedy-wt/f283-r23-evidence`
  from the clean, pushed tree at C2. Outcome:
  `PACKAGE_STATUS=READY_FOR_REVIEW`, `EVIDENCE_AUTHORITATIVE=true`,
  `REVIEW_SUBJECT_ALIGNMENT=PASS`, package
  `remedy-review-20260922-215357-READY_FOR_REVIEW.zip`, SHA-256
  `ec82c6f501f9f387fcc12632e2a16129ef8969ed4792ddc460de24562847246a`,
  5173 members. The script's own `REMEDY_REVIEW_DIR` default placed it
  directly at `/home/decodeux/Repos/remedy-history/zips/remedy-review-20260922-215357-READY_FOR_REVIEW.zip`
  — built there, never moved after, so the archived directory is
  `/home/decodeux/Repos/remedy-history/zips`, not the literal `NOT ARCHIVED`.
- `git push origin feature/f283-machine-contracts-part-two` after this
  commit — real outcome reported in the session reply, since it ships this
  very file.
- `gh pr list --state open ...` after the push — real outcome reported in
  the session reply.
- **NOTHING IS MERGED, NOTHING IS CLOSED.** No `gh pr merge`, no
  `gh pr create`, no checkout of `main`, no STATUS edit, no README edit, no
  `consumed_by` edit, no ledger rotation.
- `git stash` was **not** used at any point this round.
- No file under `.remedy-wt/f283-r23-payloads/` was written to, and no file
  the reviewer placed under `.remedy-wt/f283-r23-scratch/` before this round
  (`build_payloads.py`, `gate_src.txt`, `plan.txt`, `r1035.txt`) was edited.

## Verification

### G1 — TRANSPORT

Payload readings (table above): **both files equal on lines/bytes/sha256**.

Two `.agent/authored/f283-r23-*` blobs plus the block copy, each read back
from the committed tree with `git show 91f15a19:<path>` and compared
byte-for-byte with its source:

| copy | equal to source | bytes |
|---|---|---|
| f283-r23-block.md | True | 11834 both |
| f283-r23-ledger.md | True | 6089 both |
| f283-r23-plan.md | True | 1507 both |

**All three readings True.**

### G2 — THE BOOKING (at C2, `9e40d5fe`)

**(a) Append arithmetic**, by strict byte concatenation, pre-file read at
`15145f71`:

| file | pre | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 559905 | 6089 | 565994 | True |

Matches the block's stated composition exactly (565994).

**(b) Line-anchored on the committed ledger**: `^Gate: F283 R22 — ` = **1**,
`^- R-1035 — ` = **1**. Open set by distinct id, via `open_finding_ids` from
`scripts/rotate_live_review.py` (imported and called directly):

| rev | OPEN by distinct id |
|---|---|
| `15145f71` | **25** |
| C2 (`9e40d5fe`) | **26** |

Added: `['R-1035']`. Removed: `[]`. Matches the block's stated 25 → 26, ADDED
`R-1035`, REMOVED none, exactly.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**: sha256-equal to
the payload (`e4677998024b8c3550780c75e0e068b786860220cbe1505cacd000c99a801242`
both). Line count: **34**, under the AGENTS.md 50-line rule.

### G3 — THE BUNDLE (at A1)

Ancestry-count equality at HEAD (`9e40d5fe`) over the fork point
`d0d40e89`: `git rev-list --count --ancestry-path d0d40e89..HEAD` = **161**;
`git rev-list --count d0d40e89..HEAD` = **161**. Equal — base is correct
(pitfall (e) does not apply).

Evidence job id: **`f283r23e1001`**.

Gate set written by the bundle — all **eight** closed-schema gates present
under `.remedy-wt/f283-r23-evidence/`: `final_verifier_report.json`,
`fresh_evidence_gate.json`, `artifact_contract_gate.json`,
`change_provenance_gate.json`, `manifest_integrity.json`,
`postmortem_integrity.json`, `commit_execution_gate.json`,
`runtime_integration_gate.json`.

`validate_verification_tests(verification_tests.json)` → `(problems=[],
passed=523)` — **EMPTY problem list**.

`validate_evidence_candidate(evidence_dir)` → `is_valid_current_run=True`,
`validation_errors=[]`.

Verification run: `run_id=vr-1035` (matches `^vr-\d{4,}$`), `selected=523`,
`len(node_ids)=523` (equal), `test_files` sorted — exactly the five named in
the block — `output_hash=e0965c184108b26226689a2422359239479a1929a5d0de3449db990ff680dc88`.

Unsafe-text red control: real list `problems=[]` (accepted); planted list
(one node id carrying an absolute path) `problems=['...node_ids[523] carries
a local absolute path', '...node_ids count (524) != selected (523)']`
(rejected). Both readings recorded above under External actions.

### G4 — THE PACKAGE (at A2)

`PACKAGE_STATUS=READY_FOR_REVIEW`. `EVIDENCE_AUTHORITATIVE=true` (also
confirmed nested at `current_evidence.evidence_freshness.evidence_authoritative`
= `true` inside the packaged `.review_zip_manifest.json`). Package filename
`remedy-review-20260922-215357-READY_FOR_REVIEW.zip`, SHA-256
`ec82c6f501f9f387fcc12632e2a16129ef8969ed4792ddc460de24562847246a` (as
reported by the packaging script's own final summary; the file lives outside
this session's allowed directory tree, so it is not independently re-hashed
here).

`committed_review_subject` read from the packaged `.review_zip_manifest.json`:
`base_commit=d0d40e89b6aa9afcebd639df7a7c16a260059537`, `base_is_ancestor=true`,
`commit_count=161`, `head_commit=9e40d5fe2133ab343fbe3ef64ed584cbcb141062` —
**equal to C2's sha**, the accepted HEAD.

Zip's own import check: `zipfile.is_zipfile(path)=True`,
`ZipFile.testzip()=None` (no corrupt member across all 5173 entries).

Archived directory: `/home/decodeux/Repos/remedy-history/zips` (built there
directly by the script's own default `REMEDY_REVIEW_DIR`; never moved after
— not the literal `NOT ARCHIVED`).

### G5 — THE TREE

`python3 -c` calling `run_integrity_checks` from
`packages.orchestration.integrity_gate`: `passed=True`, `fail_count=0`, all
five checks (`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `high_blockers_open`) read `PASS`.

`git status --porcelain` (before this commit): empty.

`git worktree list`: primary checkout + `.remedy-wt/job-129b3ad7206d4f8d`
(round 22's self-use leftover, unchanged — constraint 6 forbids deleting it).

`git branch --list 'remedy/job-*' | wc -l`: **38**, unchanged from
pre-flight — this round created no new job branch.

## Authored-text proofs

- The block copy and two payload copies at C1, compared with the block's
  originals under `.remedy-wt/f283-r23-payloads/` and
  `.remedy-wt/f283-r23-block.md`: **three readings, all True** (G1).
- The one APPEND payload against its committed file: strict byte
  concatenation True for `.agent/live_review.md` (ledger.md,
  559905+6089=565994, G2a).
- The one REWRITE payload against its committed file: `.agent/plan.md`'s
  committed sha256 equals the payload's sha256 (G2c).
- No payload was edited or retyped. The block copy and two payload copies at
  C1 were made with `shutil.copyfile`; the live_review.md append by reading
  the payload's bytes and writing pre+payload back to disk; the plan.md
  rewrite by `shutil.copyfile`, then verified sha256-equal.
- The evidence job's own producer text (gate JSON, `final_verifier_report`,
  `verification_tests.json`) is machine-generated by
  `create_manual_completion_bundle` from measured facts (real pytest output,
  real git history) — there is no reviewer-authored diff to compare it
  against; its correctness is established by the validators (G3) instead.

## Deviations & assumptions

None. The block's three commits (C1, C2, C3) and two actions (A1, A2) landed
in the ordered sequence, with no extra, dropped or reordered commit.

1. **Constraint 1** (no payload edited or retyped): held — `shutil.copyfile`
   for C1's two payload copies and the block copy; byte-read-then-write for
   C2's one append; `shutil.copyfile` + sha256 verification for the plan.md
   rewrite.
2. **Constraint 2** (every commit under 500 insertions by `git show
   --numstat`): held — 211, 17; this handoff commit exempt as a single
   `.agent/**` state file.
3. **Constraint 3** (the round's tracked path set is EXACTLY the enumerated
   set): held — `git diff --name-only 15145f71 HEAD` before this commit
   reads exactly `.agent/authored/f283-r23-block.md`,
   `.agent/authored/f283-r23-ledger.md`, `.agent/authored/f283-r23-plan.md`,
   `.agent/live_review.md`, `.agent/plan.md` — five paths, all inside the
   block's enumeration (the `.agent/authored/f283-r23-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/plan.md` and `.agent/handoff.md`); adding
   `.agent/handoff.md` from this commit makes six, still the exact set.
4. **Constraint 4** (a non-READY package is a blocker to report, not work
   around): not invoked — the package built `READY_FOR_REVIEW` on the first
   attempt.
5. **Constraint 5** (nothing merged, nothing closed): held — no
   `gh pr merge`, no `gh pr create`, no checkout of `main`, no STATUS/README
   edit, no `consumed_by` edit, no ledger rotation.
6. **Constraint 6** (delete nothing not created this round): held —
   `remedy/job-129b3ad7206d4f8d` and its worktree, and all pre-existing
   stash entries, left exactly as found; `remedy/job-*` count unchanged at 38.
7. `git stash` was never used this round.

One clarifying note, not a deviation: the block asks the round to "report the
ABSOLUTE DIRECTORY the package now lives in, or the literal `NOT ARCHIVED`."
No `REMEDY_REVIEW_DIR` override was ordered or set, so
`scripts/make_review_zip.sh` used its own default, which writes the final zip
directly to `/home/decodeux/Repos/remedy-history/zips` — the same directory
every prior accepted `STATUS.md` line in this project's history names as
`package path`. The package was therefore never "moved"; it was built
straight into that directory, which is the reading reported above.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `15145f71`; block 173 lines / matching sha256 |
| C1 copy block + 2 payloads | done | 211 insertions |
| C2 book round 22 PASS, register R-1035 | done | 17 insertions, 13 deletions; open set 25→26, added R-1035, removed none |
| A1 the evidence job | done | job `f283r23e1001`; 523/523 node ids; 523 passed, exit 0; all 8 closed-schema gates present; `validate_evidence_candidate` clean |
| A1 pre-package validation | done | `validate_verification_tests` empty problem list before paying for the build |
| A1 red control | done | real list accepted, planted absolute-path id rejected on two grounds |
| A2 the review package | done | `READY_FOR_REVIEW`, `EVIDENCE_AUTHORITATIVE=true`, head equals C2's sha |
| C3 the handback | done | this commit |
| G1 payload transport + authored copies | done | 2/2 payload readings equal; 3/3 authored copies byte-identical |
| G2(a) live_review.md append | done | 559905+6089=565994 |
| G2(b) line-anchored gate lines + open set by distinct id | done | 1 each of the 2 named lines; 25→26, added R-1035, removed none |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 34 lines, under 50 |
| G3 the bundle | done | ancestry counts 161=161; 8/8 gates; empty validator problem lists; run_id/selected/node_ids/test_files/output_hash all match; red control both readings correct |
| G4 the package | done | `READY_FOR_REVIEW`, `EVIDENCE_AUTHORITATIVE=true`, head=C2 sha, zip import check clean, archived at `/home/decodeux/Repos/remedy-history/zips` |
| G5 the tree | done | integrity `passed=True fail_count=0`; git status clean; worktree list unchanged |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile` / bytes read+write only |
| Constraint 2 every commit under 500 insertions | done | 211, 17; this handoff exempt as single `.agent/**` state file |
| Constraint 3 tracked path set is exactly the enumeration | done | 5 paths before this commit (6 after), exact match |
| Constraint 4 non-READY package is a blocker to report | done (n/a) | package came back READY_FOR_REVIEW on first build |
| Constraint 5 nothing merged, nothing closed | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no STATUS/README/consumed_by edit, no rotation |
| Constraint 6 delete nothing not created this round | done | round-22 branch/worktree left alone; `remedy/job-*` count unchanged at 38 |
| `git stash` used | done (n/a) | never used this round |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk. While it exists, write
   nothing and end.
2. The review of round 23 — C1 through C3, A1 and A2, all gates re-derived.
3. Then the closure sequence's last round, as `.agent/plan.md` lists it: the
   ledger rotation as its own commit, then the STATUS line, the README
   capability paragraph, the README accepted count with its Next clause and
   the README tier row in ONE commit with the self-use entry's
   `consumed_by`, then the pull request, which the session that opens it
   never merges.

Open findings count: **26**. Operator-questions count: **0**.
