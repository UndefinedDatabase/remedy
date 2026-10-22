# Handback — F307 round 23: book round 22 with R-1331; R-1328, a job's dirty start shown; R-1325's rules held

## Session

SESSION 6 of feature F307 · round 23 · rounds so far 23

Context self-assessment: this worker verified every prepared digest before any write, applied C1 by a byte-proof script, applied C2 and C3 by `git apply` from the reviewer's cut patches with no hand-retyping, read each staged diff in full against its patch before committing, and ran each gate once; context is ample and nothing was lost.

Fortschritt: ~90 % (T001 to T006, T008 to T011, T013 to T016, R-1280, R-1290, R-1292, R-1297, R-1298, R-1301, R-1414 to R-1417 landed, R-1281's writer part landed, R-1325, R-1327 and R-1328 under review · the rest open) — Schätzung

## Range

Review of `5bffe07e0`..`HEAD` on `feature/f307-findings-paydown-v9`.

## Commits

### 38bddcc6c F307 R23 C1: book round 22 with R-1331, DECISION F307 D23, the plan
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f307-r23.md` | 85/0 | NEW FILE, this round's block, byte copy (85 lines, sha256 `0f4af5c2ac66de5a0b03fd52df353ffc80157a6bef04f34bdb6be09a658a724e`, equal to `block.md`) |
| `.agent/decisions.md` | 12/0 | prepared slice appended (DECISION F307 D23) |
| `.agent/live_review.md` | 4/0 | prepared slice appended (round 22's Gate verdict PASS, R-1331 RESOLVED) |
| `.agent/plan.md` | 6/6 | replaced with the prepared file |

107 insertions, 6 deletions over 4 files (`git show --shortstat`).

### 972b9a723 F307 R23 C2: the story counts and the digest names the dirty paths a job started from (R-1328)
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/client_interface_digest.py` | 2/1 | `DIGEST_KEY_TREE` comment updated; `dirty_start` key tree (`captured`, `preserved`) added under the job entry |
| `apps/cli/client_interface_story.py` | 3/1 | `CLIENT_STORY_ANSWER_KEYS` gains `dirty_start`; `CLIENT_STORY_KEY_TREE` maps it to the word tree |
| `docs/guides/do-run-v1.md` | 3/1 | paragraph added: the story counts the dirty paths a job started from, the digest names them |
| `docs/system/api-release-matrix-v1.json` | 4/1 | 1.27 `added` entry for the new story/digest key; `dirty_start` added to the key-version tables |
| `docs/system/machine-client-contract-v1.md` | 10/4 | `dirty_start` phrase, answer keys, and key trees updated at four sites |
| `docs/system/public-http-api-v1.md` | 7/2 | `dirty_start` (since 1.27) documented in the story section and the route table row |
| `packages/orchestration/client_digest.py` | 8/0 | `_job_dirty_start` added; `dirty_start` key added to `_job_entry`'s dict |
| `packages/orchestration/client_story.py` | 12/0 | `_dirty_start` added; `dirty_start` key added to `build_client_story`'s dict |
| `packages/orchestration/client_story_words.py` | 3/1 | `dirty_start` phrase registered in `STORY_PHRASES`; checked in `story_problems` |
| `packages/orchestration/dirty_baseline.py` | 14/0 | `job_dirty_start` added — reads `captured`/`preserved` paths from the job's start baseline record |
| `packages/orchestration/public_api_routes.py` | 2/1 | route description text updated to mention `dirty_start` |
| `tests/cli/test_client_interface.py` | 2/2 | `UNRESOLVED_ANSWER_SITES` story key set gains `dirty_start` |
| `tests/orchestration/test_client_story_words.py` | 11/0 | new test for the `dirty_start` phrase's shape in `story_problems` |
| `tests/orchestration/test_dirty_baseline.py` | 25/1 | new test for `job_dirty_start`, the story and the digest naming the dirty paths of a job started from a dirty tree; clean-start assertion added |

106 insertions, 15 deletions over 14 files (`git show --shortstat`); applied from `c2.patch`, not hand-retyped.

### 998eb494b F307 R23 C3: the lane matrix holds the rules of a plain word that names a file (R-1325)
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_do_lane_matrix.py` | 5/1 | `MATRIX_VERSION` raised to 2 with a comment; three rows added: the changelog resolved by its word, a plain word two documents share (full lane), a plain word naming a source file (full lane) |

5 insertions, 1 deletion over 1 file (`git show --shortstat`); applied from `c3.patch`, not hand-retyped.

### (this commit) F307 R23 C4: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | HEAD and `origin/feature/f307-findings-paydown-v9` both `5bffe07e01ba64304d693fba83092d499bab6441`, tree clean, no pull run, no `.agent/STOP` |
| C1 | done | commit `38bddcc6c`, 107 insertions, byte proofs all held |
| C2 | done | commit `972b9a723`, 106 insertions, applied from `c2.patch` |
| C3 | done | commit `998eb494b`, 5 insertions, applied from `c3.patch` |
| C4 | done | this handback commit |
| Gate 1 | done | `git status --porcelain` empty |
| Gate 2 | done | `ruff over 11 files: exit 0`, `All checks passed!` |
| Gate 3 | done | `paths 109`, `exit 0`, `4563 passed, 2 skipped in 114.42s` |
| Gate 4 | done | `fail_count` 0, all six checks pass |
| Gate 5 | done | `13` |
| Gate 6 | done | `git diff --stat 54e78c7b9 HEAD -- packages apps scripts tests docs` empty |
| Push | pending | runs after this commit; reported in the session reply |

## External actions

None before this commit; the push follows it and is reported in the session reply. `.remedy-wt/f307-r23-worker/` (created this round) holds the digest-verification script, the C1 byte-proof script, the integrity-check script, the three commit-message files and the selection output.

## Verification

1. Digests, before any write: `digests.txt` sha256 `339e1c0d68531a72362f7f4ea35dfdb04de2f43e3ebdc8f3e776e3f3f3464fad` and `block.md` sha256 `0f4af5c2ac66de5a0b03fd52df353ffc80157a6bef04f34bdb6be09a658a724e` (85 lines) both equal the delivering prompt; the eight other listed entries (`c1-.agent__plan.md`, `c1-decisions-append.txt`, `c1-live_review-append.txt`, `c2.patch`, `c3.patch`, `ruff_touched.py`, `run_selection.py`, `selection.txt`) matched (by a python3 script, since `digests.txt` is tab-separated).
2. C0: branch `feature/f307-findings-paydown-v9`; HEAD equals `origin/feature/f307-findings-paydown-v9` at `5bffe07e01ba64304d693fba83092d499bab6441`; tree clean.
3. Gate 1: `git -C <root> status --porcelain` — empty (read after C3, before C4).
4. Gate 2: `python3 .remedy-wt/f307-r23/prep/ruff_touched.py <root>` — 11 touched files listed, `ruff over 11 files: exit 0`, `All checks passed!`.
5. Gate 3: `python3 .remedy-wt/f307-r23/prep/run_selection.py <root> .remedy-wt/f307-r23-worker/selection-output.txt` — `paths 109`, `exit 0`, `4563 passed, 2 skipped in 114.42s (0:01:54)`. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine, F252), `tests/test_install_smoke.py:175` (opt-in, `REMEDY_INSTALL_SMOKE=1`). No FAILED, ERROR or "process(es) behind" line.
6. Gate 4: `python3 -m apps.cli.main integrity check --json` via a python3 script with `cwd=<root>` — exit 0, `fail_count` 0; `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open` all pass.
7. Gate 5: `python3 .remedy-wt/f307-r10/open_count.py <root>` — `13`.
8. Gate 6: `git -C <root> diff --stat 54e78c7b9 HEAD -- packages apps scripts tests docs` — empty output, confirming the committed product bytes equal the reviewer's dry run.

## Authored-text proofs

`.agent/authored/f307-r23.md` equals `block.md`: 85 lines, sha256 `0f4af5c2ac66de5a0b03fd52df353ffc80157a6bef04f34bdb6be09a658a724e` on both sides. The `.agent/live_review.md` and `.agent/decisions.md` appends (each equal to pre-image plus slice) and the `.agent/plan.md` replacement were each proved byte for byte by one script right after writing, in the same run that applied them. C2 and C3 were the reviewer's cut patches (`c2.patch`, `c3.patch`) applied with `git apply --check` then `git apply`, never retyped; each staged diff was read in full before its commit and matched its patch hunk for hunk.

## Deviations & assumptions

None. The commit sequence landed exactly as ordered (C1 to C4), each touching only its named paths. No mutation red-proof, no full suite outside the selection, `REMEDY_TEST_MAX_WORKERS` never set, `.data` never read, no amend, rebase, force-push or `--no-verify`, no PR; each gate ran once and never concurrently.

## For the operator, in plain sentences

When a person starts a job while some files are still uncommitted, the job's overview now says how many of them it took as its starting point and how many it left alone, and a program reading Remedy's overview gets their names.

## Next

1. Phase 1 rule 1: check `.agent/STOP`.
2. Rule 2: the Open PR Gate.
3. Review round 23's handback and book its verdict, with R-1325, R-1327 and R-1328, in the next round's first commit.
4. R-1326, the `[roles]` table.

Operator questions open: 0. Open findings count gate 5 printed: 13.
