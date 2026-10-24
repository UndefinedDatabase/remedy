# Handoff — F152 round 9 (the closure's evidence round)

## Session

SESSION 1 of feature F152 · round 9 · rounds so far 9. This session verified every prepared digest
before touching a file, applied the two byte copies exactly, ran the staging reclaim (empty
reading), the evidence job and the review package each once, and found every gate green with no
deviation of consequence.

Fortschritt: ~95 % (everything but the closing round is done) — Schätzung.

## Range

Review of `74251df64`..`ab327e93f` (C1 to C2; C3 — this file — is the commit that carries it, per
the handback template's self-reference exception).

## Commits

### e1b509009 F152 R9 C1: book round 8, R-1463 resolved, the plan, the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f152-r9.md` | +125/-0 | NEW FILE — this round's block, the authored-text proof, byte-copied from the prepared `c1-` file |
| `.agent/live_review.md` | +4/-0 | round 8's PASS verdict booked as a Gate entry; R-1463 resolved as a `Done:` paragraph |
| `.agent/plan.md` | +6/-9 | rewritten: Current Step/Next Steps to round 9 |

### ab327e93f F152 R9 C2: the evidence script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f152-r9-create_f152_evidence.py` | +313/-0 | NEW FILE — the evidence script, byte-copied from the prepared `c2-` file |

### (this commit) F152 R9 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`, checked before any
write. No pull request created, edited or merged. No `git worktree` command run by me. No stash
entry touched. No `claude` binary invoked by me; no provider call this round.
`git push origin feature/f152-worker-config-isolation` ran once, immediately after C2, and
succeeded on the first attempt (no HTTP 500, no retry needed):
```
To github.com:UndefinedDatabase/remedy.git
   74251df64..ab327e93f  feature/f152-worker-config-isolation -> feature/f152-worker-config-isolation
```
A second push runs once, immediately after this commit.

## Verification

**Gate 1.** After C2: `git status --porcelain` → empty (exit 0). Then
`python3 .remedy-wt/f152-r9/prep/verify.py .` (the repository root):

```
True	e1b509009 single parent
True	e1b509009 subject carries a F152 R9 Cn tag: F152 R9 C1: book round 8, R-1463 resolved, the plan, the block
True	e1b509009 adds no machine path
True	ab327e93f single parent
True	ab327e93f subject carries a F152 R9 Cn tag: F152 R9 C2: the evidence script
True	ab327e93f adds no machine path
True	on feature/f152-worker-config-isolation
True	C1 paths ['.agent/authored/f152-r9.md', '.agent/live_review.md', '.agent/plan.md']
True	C1 .agent/authored/f152-r9.md equals c1-.agent__authored__f152-r9.md
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C2 paths ['.agent/authored/f152-r9-create_f152_evidence.py']
True	C2 .agent/authored/f152-r9-create_f152_evidence.py equals c2-.agent__authored__f152-r9-create_f152_evidence.py
absent	C3
True	the saved block equals block.md
ALL True
```

Every line `True` (C3 correctly `absent` before this commit exists); the last line `ALL True`.

**Gate 2.** A2's and A3's readings, exit codes read from the launcher's `.exit` files — see
"Evidence and package" below for the quoted decisive lines.
`.remedy-wt/f152-r9-worker/evidence.exit` → `exit 0 wall 1903.0`.
`.remedy-wt/f152-r9-worker/zip.exit` → `exit 0 wall 17.6`.

**Gate 3.** After A3, before C3:
`python3 -m apps.cli.main integrity check --json`, run once:

```
{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```

`fail_count` 0, all six checks `pass`.

`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`:

```
['R-1246', 'R-1281', 'R-1351', 'R-1353', 'R-1426', 'R-1428', 'R-1448', 'R-1450']
```

Exactly the eight ids the block names.

`git status --porcelain` → empty.

## Evidence and package

Evidence job `f152r9e1001`. A2's decisive lines, from `.remedy-wt/f152-r9-worker/evidence.log`
(the launcher's own tool output):

```
head ab327e93f84f62018230713a4a8e46927e03567b
ancestry-path count 34
plain count 34
collected node ids 12941, deselected 253
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 0, {'passed': 12935, 'failed': 0, 'skipped': 6}, output_hash f9a67f22b1182d922d983fe4f167cc6c73f76535617caa44696d9d8ced620b43, duration 1874.34s
validate_verification_tests problems [] passed 12935
is_valid_current_run True
validation_errors []
```
`head` equals C2's full sha; both ancestry counts equal 34, matching the block's expectation; 12941
collected node ids with 253 deselected, matching the reviewer's own collect-only precheck at
`74251df64`; the red control found 0 unsafe real ids and correctly flagged the planted id as a
local absolute path; pytest exited 0 with 0 failed and a positive duration; the manifest validator
found no problems and the bundle `is_valid_current_run True` with no `validation_errors`. The
launcher's exit line: `exit 0 wall 1903.0`.

Package build, from `.remedy-wt/f152-r9-worker/zip.log` (the launcher's own tool output) and an
independent Python check against the built file:

```
{"member_count": 2118, "authoritative_count": 24, "symlink_count": 0, "tombstone_count": 0, "final_path": "~/Repos/remedy-history/zips/remedy-review-20261024-111421-READY_FOR_REVIEW.zip", "final_sha256": "47ab419b8fe89aa50ff6106679c1089930649a4a1bebccfe6af6e6324dd30319", "publication_capability": "SUPPORTED", "package_status": "READY_FOR_REVIEW", "evidence_authoritative": true, "review_subject_alignment": "PASS", "manifest_sha256": "fd48244d7b3b058437760a5358799777776768b469ea32568dd78cd444909791"}
PACKAGE_STATUS=READY_FOR_REVIEW
REVIEW_SUBJECT_ALIGNMENT=PASS
EVIDENCE_AUTHORITATIVE=true
```
No second attempt was needed — the sandbox wrote its default directory on the first start.
Package: `remedy-review-20261024-111421-READY_FOR_REVIEW.zip`.
SHA-256 (independently computed over the file): `47ab419b8fe89aa50ff6106679c1089930649a4a1bebccfe6af6e6324dd30319`.
Directory: `~/Repos/remedy-history/zips`.
`committed_review_subject` inside `.review_zip_manifest.json`, read independently: base
`ef2b85f83e986f7ad566ba5613e2bcfbf0dabc1b`, head `ab327e93f84f62018230713a4a8e46927e03567b` (C2's
full sha, as the block requires). `zipfile.is_zipfile` → `True`; `testzip()` → `None`.

## Staging reclaim

`python3 -m apps.cli.main data reclaim --orphans` (preview, run once): "Would free 0 B in 0 paths —
nothing deleted; re-run with --apply". Every data class the report lists is marked `(durable)` with
a reason ("reclaim addresses ephemeral classes only"); none is refused as a candidate because none
is a candidate. The preview listed no candidate, so the `--apply` run was skipped per the block, and
the empty reading above is the one recorded.

## Authored-text proofs

C1's byte copy (`.remedy-wt/f152-r9-worker/c1_copy.py`) read `True` for all three targets
immediately after copying: `.agent/authored/f152-r9.md`, `.agent/live_review.md`, `.agent/plan.md`.
`block.md`'s own line count and sha256 — `125` lines,
`259af2928014e9b2e6a9963284f68142b33401cf5f07e7aba938e0f3775f6bf4` — were independently computed
directly against the prepared `block.md`, matching the digest given in the prompt and in
`digests.txt`. C2's byte copy (`.remedy-wt/f152-r9-worker/c2_copy.py`) read `True` for
`.agent/authored/f152-r9-create_f152_evidence.py`. Gate 1's `verify.py` run independently
re-confirmed every `C1 ... equals c1-...` and `C2 ... equals c2-...` line `True`, and `the saved
block equals block.md` `True`.

## Deviations & assumptions

1. The zip launcher's own JSON line quotes `final_path` as this machine's absolute path; the
   commit-msg hook's agent-state guard correctly refused it under `.agent/`, so this file quotes
   that one field with the home folder written as `~` (the same substitution the block's A3 section
   itself asks for elsewhere) instead of the tool's literal bytes. Every other field of that line,
   and the independently-computed SHA-256 and directory beside it, are unchanged.

No other departure from the block's ordered commit sequence: no split, no correction commit, no
file touched outside the paths named per commit, no second test command beyond A2's one scoped
evidence pytest, no `REMEDY_TEST_MAX_WORKERS`, no `-n` of my own, no `claude` binary invoked by me,
no worktree of my own, no mutation beyond the two ordered byte copies, and `--apply` correctly
skipped because the reclaim preview listed no candidate.

## For the operator, in plain sentences

This round collected and checked this feature's evidence, and the checks came back clean: every
test the evidence job ran passed, and the bundle it produced was found internally consistent. The
review package was built successfully and is sitting on disk, ready for a human reviewer to open.
Separately, the paid trial run from two rounds ago wrote the first tests for one of Remedy's own
modules that had none; a reviewer checked that work and approved it, but it has deliberately not
been applied to the project yet — it is parked on its own branch. That same trial run was also the
first time the underlying model's command-line tool ran for real without the operator's own personal
account settings attached to it.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | three files byte-equal to the prepared snapshots; block.md 125 lines, sha256 matched |
| C2 | done | `.agent/authored/f152-r9-create_f152_evidence.py` byte-equal to the prepared snapshot |
| A1 | done | preview "Would free 0 B in 0 paths"; apply correctly skipped (no candidate) |
| A2 | done | evidence job `f152r9e1001`, exit 0, all decisive lines matched the block's expectations |
| A3 | done | package `READY_FOR_REVIEW`, alignment `PASS`, evidence authoritative, both python checks True |
| C3 | done | this handback |
| Gate 1 | done | every line `True`, last line `ALL True` |
| Gate 2 | done | A2 exit 0 wall 1903.0; A3 exit 0 wall 17.6 |
| Gate 3 | done | `fail_count` 0, all six checks pass; exactly the eight open ids; status clean |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2: the Open PR Gate — no pull request is open for this branch yet.
3. The reviewer reviews round 9 and books its verdict in the next round's first commit.
4. The closing round: the Built State, the rotation, SU-082's `consumed_by`, the STATUS flip with
   the README sync, and the pull request, left unmerged.

Operator questions open: 3.
Open findings: R-1246, R-1281, R-1351, R-1353, R-1426, R-1428, R-1448, R-1450.
