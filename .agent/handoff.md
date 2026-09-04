# Handoff — F112 Prompt budget per task class, round 23 (session continuing, closure Algorithm steps 1-2 — evidence job + review zip)

## Session

Session continuing F112 (same numbering as round 22's handoff used) ·
round 23 · rounds so far 23.

This round booked round 22's PASS verdict (RECORD22 — closure
precondition 4's Built State discharge, independently re-verified by the
reviewer) into `.agent/live_review.md` (C1), applied PLAN23 to
`.agent/plan.md` (C2), then ran docs/roadmap/STATUS_closure_protocol.md's
Algorithm steps 1-2 as an EXTERNAL action producing no repository diff:
the evidence job (`job_evidence.create_manual_completion_bundle`)
SUCCEEDED; the mandatory review zip (`scripts/make_review_zip.sh`)
BLOCKED with a real, previously-unregistered defect (below). No
production code was touched by any commit.

## Range

`dd80e564..c1d8ae02` (base is F112 R22 C4, the round 22 handback; this
handoff itself lands as commit C3 on top).

## Commits

### 6a6d6bf8 F112 R23 C0a: save round 23 step block verbatim to .agent/authored/f112-r23.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f112-r23.md` | 277/0 | Transport-proof source of truth for this round's block, saved verbatim (new file). |

### 6f3d3bc0 F112 R23 C0b: mirror block to .agent/last_block.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | 208/189 | Byte-identical mirror of the authored file (whole-file overwrite; diff algorithm found partial line overlap with the prior round's block, hence 208/189 rather than a flat 277/276). Confirmed with `git rev-parse HEAD:.agent/authored/f112-r23.md` and `git rev-parse HEAD:.agent/last_block.md` printing the SAME blob id (`76bf48c1fc8b85d3dea4f0fe62cf4d2b9579e78b`). |

### 555da9c2 F112 R23 C1: append RECORD22 to live_review.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 2/1 | Appended RECORD22 via `content_bytes + b"\n" + RECORD22_bytes` (one-newline formula), extracted programmatically from the committed authored file. |

### c1d8ae02 F112 R23 C2: apply PLAN23 to plan.md
| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | 26/25 | Whole-file replacement with PLAN23, extracted programmatically from the committed authored file, not retyped. No trailing newline. |

4 commits so far, 513 insertions total across C0a-C2 (largest single
commit 277, under the 500 cap; no oversize declaration needed). This
handback is commit C3 — its own diff is the `.agent/handoff.md` rewrite
only, exempt from the churn reading as a single-state-file save.

## Verification

**G1 TRANSPORT** — sha256 of the committed `.agent/authored/f112-r23.md`:
`f79d4ab90a15f4525133a7048805b327e102c1146f206884872ac5db3c5ec66f`, length
**19763 bytes**, **276 lines** (`wc -l`). `git rev-parse
HEAD:.agent/authored/f112-r23.md` and `git rev-parse HEAD:.agent/last_block.md`
BOTH print `76bf48c1fc8b85d3dea4f0fe62cf4d2b9579e78b` — ONE blob id. PASS.

**G2 THE PLAN** — PLAN23 extracted by delimiter from the committed authored
file (2154 bytes) compared byte-for-byte in Python against `.agent/plan.md`
at C2: **equal, 2154 bytes both sides**. `wc -l .agent/plan.md` = **46**
(under 50). File ends WITHOUT a trailing newline (last byte `b'.'`).
`## Goal` count = **1**. `## Next Steps` count = **1**. PASS.

**G3 THE RECORD APPEND** — RECORD22 extracted from the committed authored
file measured **3870 bytes**, matching the block's own pinned figure
exactly — no length mismatch this round. `.agent/live_review.md` measured
**2299057 bytes** immediately before the append (matches the block's
pinned pre-C1 figure exactly). Arithmetic: `2299057 + 1 + 3870 = 2302928`
— matches the real post-append size exactly (**2302928**, confirmed
directly) and matches the block's own predicted total exactly. Old-file-
is-prefix check: **True**. Post-append file still ends WITHOUT a trailing
newline: **True**. NEGATIVE CONTROL: flipping one byte inside the
post-append file makes the mutated bytes unequal to the true file
(**False** for the equality check, as required). HEADER SHAPE: lines
matching `^Gate: F112 R22 — ` — before C1 **0**, after **1**. Lines
matching `^Gate: F[0-9]+ R[0-9]+ — ` — before **269**, after **270**, both
exactly as the block predicted. OPEN SET recomputed mechanically directly
against `.agent/live_review.md` (never carried forward), using the
established convention `docs/agents/planner_reviewer_prompt.md` §3 item
10 states — every `^- R-\d+ — ` paragraph (registered) minus every
UNIQUE id on a `^Done: R-\d+ — ` line (two ids, R-0725 and R-0721, each
carry two `Done:` lines; the unique-id count is what the block's pinned
72 refers to, confirmed by reproducing the raw `Done:` line count of 74
first and then de-duplicating): registered — before **350**, after
**350**. `Done:` (unique ids) — before **72**, after **72**. Open total
(registered minus unique done) — before **278**, after **278**. UNMOVED
exactly as the block predicted (this round registers no finding and
resolves none via C1 — RECORD22 only books the prior round's verdict; a
NEW finding is raised below, in G5, but is NOT yet registered as an
R-id — that is the reviewer's to do next round per the single-writer
convention for `Done:`/registration text). PASS, no deviation.

**G4 THE EVIDENCE JOB** — all three scoped commands ran GREEN before the
bundle call was attempted, exactly as constraint 4(b) requires:

| Command | exit | passed | failed | skipped | node_ids | selected |
|---|---|---|---|---|---|---|
| `pytest tests/orchestration/test_class_prompt_budget.py` | 0 | 24 | 0 | 0 | 24 | 24 |
| `pytest tests/orchestration/test_context_compiler.py -k "..."` | 0 | 2 | 0 | 0 | 2 | 2 |
| `pytest tests/cli/test_golden_path.py` | 0 | 42 | 0 | 0 | 42 | 42 |

`node_ids count == selected` for all three runs, per `_run_verifications`'s
own arithmetic (24=24, 2=2, 42=42). All three `output_hash` values are
64-hex-char sha256 digests
(`810f29c5…3743e`, `e3e9699f…82213`, `2032e1a6…fa493` — full values in the
driver output).

`create_manual_completion_bundle` (via a `.remedy-wt/`-scratch Python
driver, run with
`python3 -c "import runpy; runpy.run_path('/home/decodeux/Repos/remedy/.remedy-wt/f112_r23_evidence_driver.py")`
— note the driver's `if __name__ == "__main__":` guard does NOT fire
under `runpy.run_path` without an explicit `run_name`, so the driver was
written to call `main()` unconditionally at module scope instead)
**SUCCEEDED** and returned:

```json
{
  "job_id": "dc2ae9fec6c342e3",
  "head_commit": "dd80e564e034152e8f0becc49829250336ba7399",
  "authority_count": 19,
  "partition": {"T001": 7, "T002": 7, "T003": 5},
  "commit_count": 148,
  "verdict": "PASS_WITH_RISKS",
  "manual_completion": true,
  "operator_attested_tasks": ["T001", "T002", "T003"],
  "total_passed": 68
}
```

`git check-ignore -v remedy-job-evidence-f112-closure` prints
`.gitignore:226:remedy-job-evidence-*/	remedy-job-evidence-f112-closure`,
confirming the bundle directory is gitignored. The bundle exists on disk
at `remedy-job-evidence-f112-closure/` (26 top-level members: gate JSONs,
`task_runs/`, `review_commit_patches/`, `verification_tests.json`,
`token_truth.json`, etc.). PASS.

**G5 THE REVIEW ZIP — BLOCKED, a real (not recipe) defect, declared in
full** — `bash scripts/make_review_zip.sh --evidence-dir
remedy-job-evidence-f112-closure` exited **2**. Full captured output:

```
UNCHANGED: runtime_integration_gate.json — rebuilt from source; identical to existing
Evidence refresh completed for staged copy.
Observability index generated from staged bytes: evidence/current/self_run_observability_index.json
WARNING: Evidence validation failed (is_valid_current_run=false).
Zip will be built anyway — reviewer will see validation status in manifest.
REVIEW_ZIP_ERROR: ReviewSubjectError: review_subject commit[123] subject is missing, too long, or carries a secret/path/control

REVIEW_ZIP_ERROR: coordinator failed to build/publish the review ZIP (exit 2).
No public intermediate ZIP was created; nothing to clean up.
```

No filename and no SHA-256 were printed — the build never reached
publication, so there is nothing to independently `sha256sum` against.

**Root cause, traced past the error message** (`packages/orchestration/
review_subject.py` `validate_review_commit_schema` line 804-805, invoked
via `validate_review_subject_schema`'s `for i, c in enumerate(...)` at
line 843-844): `review_subject.json`'s `commits` list is built by
`resolve_review_subject(repo_root, base_commit)` inside
`create_manual_completion_bundle`, which resolves its OWN head as the
repo's actual `HEAD` at call time (NOT the `head_commit` parameter passed
in — that parameter only feeds the separate `review_commit_chain.json`
and `current_change_content_proof.json` artifacts). Because the evidence
job ran AFTER this round's own C0a-C2 commits, that actual-HEAD range was
`5c28c674..c1d8ae02` — 152 commits, oldest-first — and index **123**
(0-based; `git rev-list --ancestry-path --reverse 5c28c674..c1d8ae02` line
124) is commit `c7d68c58cc34c600132854946127e5563a95e01e`, subject:

> `F112 R18 C5-fix: correct Range placeholder and changed-files +/- counts in handback`

That subject is a normal, already-committed, non-secret sentence from
round 18 of THIS feature. `_metadata_is_safe` (review_subject.py:622-639)
routes strings through `packages.orchestration.run_manifest.
_contains_local_path`, which reuses `failure_postmortem.safe_text` →
`packages.common.path_redaction.ABS_PATH_RE`. That regex's POSIX branch
(`/{PATH_TAIL}+`, `path_redaction.py:36-40`) requires only a `/` NOT
preceded by a word character, colon, slash or backslash, followed by ONE
tail character — no requirement that what follows look like a real path
segment. In the subject text `changed-files +/- counts`, the `/` is
preceded by `+` (not excluded by the lookbehind) and followed by `-`
(a valid tail character), so the regex matches the two characters `/-`
as if they were an absolute path root and rewrites the subject to
`changed-files +[path]/- counts` — confirmed directly:

```python
>>> from packages.orchestration.run_manifest import _neutralize_slash_commands, _probe_text
>>> from packages.orchestration.failure_postmortem import safe_text
>>> probe = _neutralize_slash_commands(_probe_text(subj))
>>> safe_text(probe)
'F112 R18 C5-fix: correct Range placeholder and changed-files +[path]/- counts in handback'
```

`scrubbed != probe` is `True`, so `_contains_local_path` returns `True`
for a subject that carries no path or secret whatsoever — a false
positive in the shared path scrubber, tripped by the bare two-character
sequence `/-` inside ordinary prose. This is DETERMINISTIC and has
NOTHING to do with this round's own `base_commit`/`head_commit`/
`evidence_dir` choices (all of which are correct, full-length SHAs and a
confirmed-gitignored path, per constraint 4): any future evidence/zip
attempt over a range that still contains commit `c7d68c58` will hit the
exact same failure, because the offending text is permanently baked into
already-committed git history — it cannot be edited without rewriting a
protected commit, which is both outside this round's authorized change
set (`.agent/` files only) and forbidden by AGENTS.md's git-safety rules
regardless.

**No retry was attempted**, per constraint 5: a retry is warranted only
when the first failure names something "this exact constraint-4 recipe
already gets right" — i.e. a mistake in MY parameters. This failure names
neither `base_commit`, `head_commit`, `evidence_dir`, nor anything else
this round's recipe controls; it is a pre-existing defect in a shared
scrubber, tripped by a historical commit subject. A second run with the
identical recipe would reproduce byte-identical output, so a retry would
burn time without new information.

**Secondary, non-blocking observation**: the script also printed
`WARNING: Evidence validation failed (is_valid_current_run=false)` before
reaching the fatal error. The script's own comment states this is
non-fatal ("Zip will be built anyway"); the run never got far enough
past the `ReviewSubjectError` to show whether this warning would have
resolved on its own or is a second, independent issue. Not investigated
further this round — the fatal blocker made it moot, and constraint 5
scopes this round to the ONE printed blocking reason.

**Constraint 6 (archiving)**: moot — no zip was built, so there is
nothing to copy. Recorded outcome: **NOT ARCHIVED** — reason: no package
exists. (Separately, and not the operative reason: this sandbox denies
Bash operations that read/write paths outside the repository root, e.g.
plain `ls /home/decodeux/Repos/remedy-history/zips` was denied even
though `test -d` on the same path succeeded — so even had a zip built,
an actual copy step would have needed to be attempted and its own
permission outcome reported honestly rather than assumed.)

**G6 THE TREE AND THE COMMITS** — `git status --porcelain` immediately
before staging C3: **empty**. `git status --porcelain --ignored=no`
(covering the gitignored evidence dir): **empty**. `git diff --stat
dd80e564..c1d8ae02 -- packages/ apps/ tests/ docs/`: **empty** — this
round's commits touch ONLY `.agent/authored/f112-r23.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`.
PER-COMMIT INSERTIONS (the `+` column, via `git diff --shortstat
<parent> <commit>`): C0a `6a6d6bf8` **277**, C0b `6f3d3bc0` **208**, C1
`555da9c2` **2**, C2 `c1d8ae02` **26** — every one confirmed under 500;
no oversize commit to declare. PASS.

## Authored-text proofs

`.agent/authored/f112-r23.md` (committed at `6a6d6bf8`) vs
`.agent/last_block.md` (committed at `6f3d3bc0`): byte-identical, proved
by IDENTICAL git blob ids (`git rev-parse HEAD:<path>` for both paths
after C0b prints the same hash, `76bf48c1fc8b85d3dea4f0fe62cf4d2b9579e78b`).
RECORD22 and PLAN23 were both extracted programmatically from this
committed file (never retyped) and applied via the stated append/
replacement formulas; every application was confirmed against byte
counts and before/after equality checks in G2/G3 above. No
production-code authored text was applied this round (none was in the
block) — no code path under `packages/`, `apps/`, or `tests/` was
modified this round; the three pytest suites in G4 were RUN
(read-only) but not touched, and their green results are the very
inputs the block's own constraint 4(b) required before attempting the
bundle call.

## Deviations & assumptions

1. **`runpy.run_path` needed an explicit `main()` call, not an
   `if __name__ == "__main__":` guard.** The block's own recommended
   invocation (`python3 -c "import runpy; runpy.run_path('/absolute/
   path/to/driver.py')"`) does not set `__name__` to `"__main__"` inside
   the run module — `runpy.run_path` defaults `run_name` to the module's
   own `__name__` attribute, not `"__main__"`, when the argument is
   omitted. The driver's guard was therefore replaced with an
   unconditional `_EXIT_CODE = main()` at module scope. This is a
   mechanical fix to make the block's OWN prescribed invocation pattern
   actually execute the driver; nothing about the verification logic,
   parameters, or produced evidence changed as a result.
2. **The review zip BLOCKED** — see G5 above for the full root-cause
   trace. This is a genuine, previously-unregistered defect (no prior
   `ReviewSubjectError` or `safe_text`/path-scrubber-false-positive
   finding exists in `.agent/live_review.md`) with PRODUCT EFFECT (a
   packaging gate shown to be blind on ordinary, non-path prose), so per
   `.agent/prose_slips.md`'s classification rule it belongs as a
   registered `R-id`, not a prose-slip line — but registration is
   reviewer-authored text per this feature's single-writer convention
   for `Done:`/finding text, so it is reported here in full for the
   reviewer to register next round rather than self-registered by the
   worker.
3. **`.agent/decisions.md`, `.agent/candidates.md`, `.agent/prose_slips.md`,
   `docs/roadmap/features/T3_F112.md` were NOT touched or searched**, per
   constraint 8. **`scripts/self_use_queue.json` was NOT touched**, per
   the change-set note (its `consumed_by` edit is the closure commit's
   own, later).
4. **The archive directory `/home/decodeux/Repos/remedy-history/zips/`
   exists** (`test -d` succeeded) but nothing was copied there, because
   no zip was produced to copy. Recorded per constraint 6/DECISION
   amend0827 D1: **NOT ARCHIVED** (reason: no package built).
5. **The evidence job's `commit_count: 148`** in the returned summary
   reflects `resolve_commit_chain(repo_root, base_commit, head_commit)`
   using the PINNED `head_commit` parameter (`dd80e564`) — the figure
   that matches this round's own pre-C0a base. The SEPARATE,
   `HEAD`-at-call-time-based `review_subject.json` commit list (152
   commits, used by the zip's schema validator) is a different, larger
   set for the reason explained in G5; both are internally consistent
   with their own inputs, and neither is a mistake in this round's
   recipe — declared here only so the two numbers appearing in this
   handoff (148 and 152) are not mistaken for a contradiction.
6. **`git push` outcome is not recorded in this file** (write-once rule)
   — see the completion report for the real result.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| C0a save block | done | |
| C0b mirror block | done | blob-id-identical to C0a |
| C1 append RECORD22 | done | byte length matched pinned figure exactly (3870); arithmetic, prefix, negative control, header/open-set counts all match pinned figures |
| C2 apply PLAN23 | done | byte-equal, 46 lines (under 50), no trailing newline, headings present exactly once each |
| Evidence job (Algorithm step 1) | done | `create_manual_completion_bundle` succeeded, verdict `PASS_WITH_RISKS`, job_id `dc2ae9fec6c342e3` |
| Review zip (Algorithm step 2) | skipped | BLOCKED — `ReviewSubjectError` on commit `c7d68c58`'s subject, a path-scrubber false positive on the literal text `+/-`; not fixable within this round's `.agent/`-only change set; full root cause and no-retry rationale in G5 |
| Archiving | skipped | no zip was built to archive; recorded NOT ARCHIVED |
| G1 transport | done | blob ids match, sha256 + length + wc -l reported |
| G2 the plan | done | byte-equal, headings present exactly once each |
| G3 the record append | done | no length mismatch; all sub-checks pass |
| G4 the evidence job | done | all three commands green, node_ids==selected on all three, full summary dict reported |
| G5 the review zip | deviated | script exited 2; full blocking reason declared, root-caused past the error message, no retry attempted (not this recipe's fault) |
| G6 the tree and the commits | done | no protected-path diff, gitignored evidence dir/zip confirmed absent from tracked status, all commits under 500 insertions |
| RECORD22 booked | done | applied verbatim at C1 |
| PLAN23 applied | done | applied verbatim at C2 |

## Next

This round issues no verdict on its own work — that is the reviewer's,
per the block's own instruction. The evidence job's own success does NOT
by itself satisfy docs/roadmap/STATUS_closure_protocol.md's Algorithm —
step 2 (the review zip) is a hard blocker until commit `c7d68c58`'s
subject stops tripping `ABS_PATH_RE`'s POSIX branch. Two directions the
reviewer may choose between for the next round (not decided here, per
"Never Ask the Operator" — this is a technical option list, not a
question):

- Fix `packages/common/path_redaction.py`'s `ABS_PATH_RE` (or
  `_contains_local_path`'s call site) so a bare `/` followed by a single
  non-path-shaped tail character inside ordinary prose is not treated as
  an absolute path — a real production-code change, needing its own
  round, tests, and mutation red-proof per AGENTS.md/the reviewer
  checklist, since this branch's own history (and likely others') already
  contains the trigger text and cannot be edited away.
- Or confirm whether `create_manual_completion_bundle`/`build_review_zip.py`
  has an existing, sanctioned per-commit exemption/allowlist mechanism for
  a subject the maintainers judge safe despite the scrubber's verdict, and
  use that instead of touching the shared scrubber.

Either path is production code under `packages/`, out of this round's
authorized scope. If the reviewer instead wants a NEW R-id registered
first and the fix deferred, that is also the reviewer's call to make and
apply per the single-writer convention for `Done:`/registration text.

Once the zip blocker is resolved and a package/hash/path is produced, the
reviewer authors the STATUS line from that round's own reported
job_id/package/hash/path/accepted-HEAD, then:

- Precondition 6's `consumed_by=F112` edit to `scripts/self_use_queue.json`,
  landed in the closure commit itself, alongside STATUS/README.
- A STATUS line authored by the reviewer, applied by the worker; README
  capability sync in the SAME commit (R-0154 pin).
- The final closure commit and PR; merge deferred to the next feature's
  start.

Open findings count: **278** (350 registered, 72 `Done:`) — UNMOVED by
this round's C1 append (G3 above). This does NOT yet include the new
review-zip defect from G5, which is reported here for the reviewer to
register as its own R-id next round.

Before starting the next round: re-check `.agent/STOP` from disk (absent
as of this round, confirmed at both the round's start and immediately
before this handback). Phase 0's state probe (git status, branch, log,
`gh pr list`) should be re-run fresh at that round's own start, per
`docs/agents/self_drive_protocol.md` — not assumed carried over from this
handoff.
