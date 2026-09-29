STEP F041 R2 — THE FILE ROUTE: a screenshot's bytes and the whole README behind headers that never run them, R-1105's repair, and the upper-case scheme case

GOAL
Round 1 passed at `e1dc49dd`. Book it, register R-1105 and record DECISION F041 D2 in one commit,
then land D2 against the reviewer's tests: `read_artifact_file` in
`packages/orchestration/artifact_preview.py`, the structural route
`/api/jobs/<id>/artifacts/file` in `packages/orchestration/ui_server.py` with its response
headers, and R-1105's repair of `_serve_static`.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE TESTS ARE THE REVIEWER'S AND THE CODE IS YOURS:
tests.diff is the acceptance and you write the production code against it and S1 to S3 below. You
never edit a payload test; if one looks wrong to you, STOP and report it. Read DECISION F041 D2
and R-1105 in records.diff before you write code, and read whole, before you edit them:
`packages/orchestration/artifact_preview.py`, and in `packages/orchestration/ui_server.py` the
`do_GET` method, `_build_artifacts_json`, `_send_json` and `_serve_static`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f041-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f041-r2/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f041-r2-dry/`, `.remedy-wt/f041-r2-sim/`, `.remedy-wt/f041-r1-scratch/`
                                  The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f041-r2-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Set environment variables for a child process inside a Python script (`subprocess.run(...,
env=...)`), never on a command line. Never run npm or npx. Before every commit, run
`git diff --cached --stat` and confirm the index holds exactly that commit's paths.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f041-artifact-preview`, and `git log --oneline -1` must read `e1dc49dd7`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f041-r2/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f041-r2-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 39 | 12108 | 9d86132434a77f544e32b21adedd4f10b5af6dbad00bdd2cbf7c1255872b6fa5 |
| tests.diff | 231 | 11226 | 80730dd9ac114ab797a3bedb9f1dc8e4636abf1096b77cde28e48ad0b341bd28 |
| plan.md | 29 | 970 | 777c82411db01589eac3f140f0a20b871f4b48b105d83e0d736c630b967d45cc |

`plan.md` is a REWRITE of `.agent/plan.md`. Every `.diff` goes on with `git apply`; the reviewer
generated them with `git diff HEAD` from a tree at `e1dc49dd7`. `records.diff` appends round 1's
gate entry and R-1105 to `.agent/live_review.md`, DECISION F041 D2 to `.agent/decisions.md`, and
one dated line to `.agent/prose_slips.md`. `tests.diff` edits
`tests/orchestration/test_artifact_markdown.py`, `tests/orchestration/test_artifact_preview.py`,
`tests/ui_server/test_artifacts_route.py` and `tests/ui_server/test_command_channel.py`.

THE SPECIFICATION — the tests are the acceptance; these clauses fix what they leave open.
S1 `packages/orchestration/artifact_preview.py` gains, after `artifacts_view`:
   `FILE_MAX_BYTES = 10_485_760`; `README_CONTENT_TYPE = "text/plain; charset=utf-8"`; a frozen
   dataclass `ArtifactFile` of `status: int`, `content_type: str`, `body: bytes`, `error: str`;
   and `read_artifact_file(job_id, root, relative, data_root=None) -> ArtifactFile`, with a
   docstring naming F041 T001 and DECISION F041 D2. It answers 400 with
   `"invalid artifact request"` unless `root` is in `ARTIFACT_ROOTS` and EITHER `relative` is
   `README_NAME` (served as `README_CONTENT_TYPE`) OR `root` is the evidence root and `relative`
   is exactly `captures/<name>` for a single path segment `<name>` whose lowercased suffix is in
   `IMAGE_CONTENT_TYPES` (served as that type) — "exactly" means `relative` equals
   `f"{CAPTURES_DIRNAME}/{PurePosixPath(relative).name}"`, so no `.`, `..`, empty or extra
   segment passes. Then the root is found with `artifact_root` and the name with
   `resolve_artifact_path`; either None answers 404 `"artifact not found"`. A file whose size is
   over `FILE_MAX_BYTES` answers 413 `"artifact too large"`; an `OSError` reading it answers 404.
   Otherwise 200 with the bytes and an empty error. Every refusal has an empty `content_type` and
   an empty `body`.
S2 `packages/orchestration/ui_server.py`: a module-level `_read_artifact_file(job, root,
   relative)` directly after `_build_artifacts_json`, importing `read_artifact_file` inside its
   body and returning `read_artifact_file(str(job.job_id), root, relative)`; in `do_GET`, directly
   before its final `self._send_json(*_safe_error(404, "not found"))`, a structural route for
   `len(parts) == 6` with `parts[4] == "artifacts"` and `parts[5] == "file"` that loads the job
   with `_load_job` (answering its error), reads the `root` and `path` query values (empty when
   absent), and answers a refusal with `self._send_json(*_safe_error(status, error))` and a 200 with
   `self._send_artifact_bytes(content_type, body)`, under a comment naming DECISION F041 D2 and
   `_walkable_paths`; and in `_RemedyHandler`, directly before `_MIME_TYPES`, a class tuple
   `ARTIFACT_RESPONSE_HEADERS` of `("X-Content-Type-Options", "nosniff")`,
   `("Content-Security-Policy", "default-src 'none'; sandbox")` and `("Cache-Control",
   "no-store")`, and a method `_send_artifact_bytes(self, content_type, body)` that sends 200,
   `Content-Type`, `Content-Length` and those headers, then the body.
S3 R-1105: in `_serve_static`, the containment test becomes
   `if not target.is_relative_to(dist.resolve()):` under a one-line comment naming R-1105.
   Nothing else in `_serve_static` changes.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5 and C6, in this order.

C1a — `.agent/authored/f041-r2-block.md` := this block and `.agent/authored/f041-r2-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F041 R2 C1a: copy round 2 block and plan payload into .agent/authored/`
  Its insertions are this block's line count plus 29.
C1b — `.agent/authored/f041-r2-records.diff` := records.diff and
  `.agent/authored/f041-r2-tests.diff` := tests.diff.
  Subject: `F041 R2 C1b: copy round 2 records and tests diffs into .agent/authored/`
  Expected insertions: 270.
C2 — THE RECORDS, the findings first: `git apply` records.diff, then rewrite `.agent/plan.md` :=
  plan.md.
  Subject: `F041 R2 C2: book round 1, register R-1105, record D2`
  Expected by `git show --numstat` (insertions and deletions): 10/0 .agent/decisions.md, 4/0 .agent/live_review.md, 9/14 .agent/plan.md, 1/0 .agent/prose_slips.md.
C3 — THE CODE: S1 to S3.
  Subject: `F041 R2 C3: serve an artifact's bytes behind no-run headers and fix R-1105`
C4 — THE TESTS: `git apply` tests.diff.
  Subject: `F041 R2 C4: add the reviewer's file route, header and containment tests`
  Expected by `git show --numstat`: 3/0 tests/orchestration/test_artifact_markdown.py, 70/0 tests/orchestration/test_artifact_preview.py, 94/1 tests/ui_server/test_artifacts_route.py, 1/0 tests/ui_server/test_command_channel.py.
C5 — THE TOOL: your mutation tool (G4) saved as `.agent/authored/f041-r2-mutations.py`.
  Subject: `F041 R2 C5: add the round 2 mutation tool`
C6 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F041 R2 C6: rewrite handoff for round 2`
  Then `git push`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading. If one would not,
   split it at a file boundary, keep the order above, and say so.
3. The round's whole tracked path set is: the `.agent/authored/f041-r2-*` copies and tool, the
   paths records.diff and tests.diff edit, `.agent/plan.md`,
   `packages/orchestration/artifact_preview.py`, `packages/orchestration/ui_server.py`, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only e1dc49dd7` at the
   branch tip after C6. Do NOT touch `apps/ui/`, `.agent/context.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md` or `README.md`.
4. Every test tests.diff carries passes against your code unedited, at C4.
5. You write no `Done:` line and no `Landed:` line: the reviewer authors R-1105's resolution at
   the next gate.
6. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. An EXISTING test that goes red is never edited to pass.
7. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`, and no reset of a pushed commit.
8. Leave every worktree already listed at your step 4, its branch, and every existing stash
   alone. The worktree G4 adds goes under `.remedy-wt/`, is removed as that gate's last action,
   and `git worktree list | wc -l` is reported afterwards.
9. DO NOT run the full suite (amend0917 rule 1). Run no self-use job and no command that calls a
   provider.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G4 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f041-r2-*` payload copy byte for
 byte with its source, read back with `git show <commit>:<path>` from the commit that added it.

G2 THE RECORDS AND THE TESTS — the sha256 of each file below, read with `git show <commit>:<path>`
 at the commit named, equals the reviewer's reading from its simulation tree:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/decisions.md | C2 | 2455145 | c9aac5a1c21717634f3a27aa8d8d0e070b8fb8ccff5bd629b0bf73727c01ad0d |
 | .agent/live_review.md | C2 | 298288 | 74e64663de3580a93af28dd0407cb9fd0da6e8ac15df417c2aa1ae00b2b68f9c |
 | .agent/plan.md | C2 | 970 | 777c82411db01589eac3f140f0a20b871f4b48b105d83e0d736c630b967d45cc |
 | .agent/prose_slips.md | C2 | 376997 | 7062b8ca9e665ec060b9e271dc13f8f734f2f8b74d2d42b27b2578595cee6ace |
 | tests/orchestration/test_artifact_markdown.py | C4 | 13014 | 705f576bbb1a42cb5807ba01f28d8f70f70a357691e86148a1a00086fe4e5825 |
 | tests/orchestration/test_artifact_preview.py | C4 | 9865 | df7ea8ed899bb6dbc8a3db797c9901e54571b982e72c9db36f96ac57028fa211 |
 | tests/ui_server/test_artifacts_route.py | C4 | 9277 | 1b10b44b902e9d80717f42ee2e2322205f81bd2c64cadbf64317c873bda445a0 |
 | tests/ui_server/test_command_channel.py | C4 | 103129 | 9a01b127bda1f16d1f9b4310fc7ddb6f8988520a1a6d876f2cca2b0993171d77 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show`, at `e1dc49dd7` and at
 C2 (the reviewer read `[]` and `['R-1105']`).

G3 THE CODE AND THE TESTS — `python3 -m ruff check packages/orchestration/artifact_preview.py
 packages/orchestration/ui_server.py tests/orchestration/test_artifact_markdown.py
 tests/orchestration/test_artifact_preview.py tests/ui_server/test_artifacts_route.py
 tests/ui_server/test_command_channel.py .agent/authored/f041-r2-mutations.py` at C5, with its
 real exit code. Report the diff of `packages/orchestration/ui_server.py` at C3, whole. Then, in
 the primary checkout at C5, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_artifact_markdown.py tests/orchestration/test_artifact_preview.py tests/ui_server/test_artifacts_route.py tests/ui_server/test_command_channel.py tests/ui_server/test_live_state.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran it serially in its simulation tree, which carries C2, the tests and its own
 version of S1 to S3 but no `.agent/authored/f041-r2-*` copy, and read `738 passed, 1 skipped` at
 real exit code 0, the skip being `SKIPPED [1] tests/test_agent_tooling.py:43`, the D12
 quarantine. Report your count, every `SKIPPED` line, and the node counts of
 `tests/orchestration/test_artifact_markdown.py`, `tests/orchestration/test_artifact_preview.py`
 and `tests/ui_server/test_artifacts_route.py` by `--collect-only -q` (the reviewer's read 108,
 39 and 14). Then `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G4 THE RED PROOFS — your tool `.agent/authored/f041-r2-mutations.py` takes a worktree path, and
 for each mutation below edits the named production file INSIDE that worktree (asserting its FROM
 text occurs exactly once there), runs `python3 -B -m pytest -q -p no:cacheprovider <the test file
 named>` with the worktree as the working directory and its root first on `PYTHONPATH` (through
 `subprocess.run(..., env=...)`), restores the bytes, and prints one line per mutation: its label,
 the exit code and the failed count. It runs an unmutated control of each test file the
 mutations name first and last, reports `restored byte-identical: True` after each restore, and
 ends with `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  n1 `_serve_static` tests containment by the old string prefix again (test_artifacts_route.py);
  n2 the `nosniff` header is no longer sent (same file);
  n3 the policy loses `sandbox` (same file);
  n4 `read_artifact_file` no longer demands the name be exactly `captures/<name>`
     (test_artifact_preview.py);
  n5 the size cap is never applied (same file);
  n6 an image may be served from the workspace root (same file);
  n7 the README is served as `text/html; charset=utf-8` (test_artifacts_route.py).
 Run it: `git worktree add --detach .remedy-wt/f041-r2-mut <C5>`, then
 `python3 -B .agent/authored/f041-r2-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f041-r2-mut`
 and report its whole output. EVERY mutation must exit non-zero; one that stays green is reported
 as green and you STOP, because the tests are the reviewer's. Then
 `git worktree remove --force .remedy-wt/f041-r2-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G5 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C6, C5, C4, C3, C2, C1b, C1a and `e1dc49dd7` in that
 order; `git worktree list | wc -l`, which must equal your step 4 reading; the push's real
 outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must
 be EMPTY. These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 and C5), every gate's
real output and exit code, the authored-text proofs, the item-status table AGENTS.md requires (one
row per commit and per gate), the deviations, and the next expected action. Your Session section
reads SESSION 1 of feature F041, round 2, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2, then T002 (the preview commands, their intent and its consumer). State the open-findings
count, 1 (R-1105, repaired this round and awaiting its resolution), and the operator-questions
count, 1.
