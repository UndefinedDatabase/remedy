# Handoff — F287 session 3, round 17: the closing round — round 16 booked, the ledger rotated,
# F287 accepted in STATUS with its README sync and the self-use queue's `consumed_by`, the pull
# request opened

## Session

SESSION 3 of feature F287 · round 17 · rounds so far 17

Context self-assessment, quoted: "the reviewer's context is comfortable; the session ends here
because F287 is closed and the next feature starts in a fresh session."

## Range

Review of `332af0e68`..HEAD (HEAD is this commit, C3 below).

## Commits

### 33b124749 F287 R17 C1: book round 16, save the round 17 block, the STATUS line and the PR body

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f287-r17-pr_body.md` | 103/0 (new) | byte copy of the reviewer's prepared PR body |
| `.agent/authored/f287-r17-status_line.txt` | 1/0 (new) | byte copy of the reviewer's prepared STATUS line |
| `.agent/authored/f287-r17.md` | 127/0 (new) | byte copy of `block.md` |
| `.agent/live_review.md` | 2/0 | append: books the F287 R16 gate entry (VERDICT PASS) |
| `.agent/plan.md` | 6/7 | rewrite to round 17's current step, replaced with `dry-plan.md` |

### 8aa6ef25d F287 R17 C2: rotate the finding ledger into its archive

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 0/80 | `python3 scripts/rotate_live_review.py`: 31 gate records, 4 finding pairs (8 records) and 1 resolved-text record moved out |
| `.agent/live_review_archive.md` | 80/0 | the same records appended, byte-verbatim |

### F287 R17 C3: accept F287 in STATUS with its README sync and the self-use queue (self-reference exception — the handoff is committed by this same commit)

Measured before the handoff joined it (`git diff --cached --numstat`):

| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | 1/1 | F287's `[~]` line becomes the `[x]` STATUS line (`status_line.txt`, verbatim) |
| `README.md` | 12/2 | `128 of 297`; Tier 3 row `7 \| 28`; F287's paragraph follows F114's under "Accepted in Tier 3 so far" |
| `scripts/self_use_queue.json` | 1/1 | `SU-046`'s `consumed_by` set to `F287` (precondition 6) |
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |

## External actions

- `git push origin feature/f287-provider-session-continuity` after C3 (with the handoff): outcome
  reported in the worker's final reply (write-once rule; not known when this file is written).
- `gh pr create --base main --head feature/f287-provider-session-continuity --title "F287 —
  Provider session continuity across relaunch" --body-file
  /home/decodeux/Repos/remedy/.agent/authored/f287-r17-pr_body.md`: outcome (number and URL)
  reported in the worker's final reply only — it does not exist while this file is written.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft`: reported in the
  worker's final reply.
- No merge, no `git checkout` or `git switch`, no branch created, moved or deleted, no
  force-push, no pull, no worktree add/remove.

## Verification

0. Before any write: both reviewer digests (`block.md`, `digests.txt`) verified by a
   worker-written Python sha256 script (`.remedy-wt/f287-r17-worker/verify_digests.py`): both
   matched the prompt's sha256 lines exactly (`block.md` 127 lines / 9985 bytes; `digests.txt`
   sha256 `a60e1665f9092362adbfc41955b090c39512879ae089bf0aba2bb6885488c907`), then every one of the
   nine digest-bearing lines in `digests.txt` (`status_line.txt`, `pr_body.md`, `dry-plan.md`,
   `sim-C1-live_review.md`, `sim-C2-live_review.md`, `sim-C2-live_review_archive.md`,
   `sim-STATUS.md`, `sim-README.md`, `sim-self_use_queue.json`) matched its listed sha256, line
   count and byte count (9/9 OK, `.remedy-wt/f287-r17-worker/verify_all_digests.py`). `HEAD` read
   `332af0e68`, equal to `origin/feature/f287-provider-session-continuity`, and `git status
   --porcelain` was empty before any write. `git branch --show-current` read
   `feature/f287-provider-session-continuity` before C1.
1. C1 copy step (`.remedy-wt/f287-r17-worker/c1_apply.py`): `.agent/authored/f287-r17.md` read
   byte_eq=True against `block.md` (sha256
   `f464444be81ea52a9db59423e649c7a6928a3a23c6a83c368ead985003cd45a3` on both sides; 127 lines,
   9985 bytes). `.agent/authored/f287-r17-status_line.txt` read byte_eq=True against
   `status_line.txt` (sha256 `042fb5ef8b66d999530e61d509876198c69d2b3a555647b56734b754b6ff186a`;
   1 line, 563 bytes). `.agent/authored/f287-r17-pr_body.md` read byte_eq=True against `pr_body.md`
   (sha256 `c25b5620cd695262f0b0b8e778d68705da8dd37c6feb275fb640f7cade9e0228`; 103 lines, 6336
   bytes). `.agent/live_review.md` read byte_eq=True against `sim-C1-live_review.md` (sha256
   `2dbbed6c4bc19e0824993de850777d73aa9146103f843b123ebafd6ff1a2a67f`; 283 lines, 223862 bytes).
   `.agent/plan.md` read byte_eq=True against `dry-plan.md` (sha256
   `d4346cdf62e577fbea9cffbebdb01c2ce8315158a04b4d2dcdd14012094c1632`; 24 lines, 1328 bytes).
   `git diff --cached --numstat` (`.remedy-wt/f287-r17-worker/c1_stage.py`) read exactly the five
   cells `digests.txt` lists: `103 0 .agent/authored/f287-r17-pr_body.md`, `1 0
   .agent/authored/f287-r17-status_line.txt`, `127 0 .agent/authored/f287-r17.md`, `2 0
   .agent/live_review.md`, `6 7 .agent/plan.md`. The full cached diff was read before committing
   (self-review): the plan rewrite advanced the current step to round 17 exactly as prepared, and
   the `live_review.md` diff is a pure two-line append (round 16's gate entry, VERDICT PASS); no
   unrelated edit found. Committed as `33b124749621d28e96973d560de534bd2d75a84c`.
2. **C2 — the ledger rotation** (`.remedy-wt/f287-r17-worker/c2_rotate.py`, `python3
   scripts/rotate_live_review.py`, exit 0). Whole output:
   ```
   gate records moved: 31
   finding pairs moved: 4 (8 records)
   resolved-text records moved: 1
   old ledger size: 223862 bytes
   new ledger size: 157310 bytes
   old archive size: 6029259 bytes
   new archive size: 6095811 bytes
   open findings before: 9
   open findings after: 9
   written: /home/decodeux/Repos/remedy/.agent/live_review.md and
     /home/decodeux/Repos/remedy/.agent/live_review_archive.md
   ```
   Matches the block's expected reading exactly. Re-verified
   (`.remedy-wt/f287-r17-worker/c2_verify.py`): `.agent/live_review.md` byte_eq=True against
   `sim-C2-live_review.md` (sha256
   `1e5deeb1f163aa2a3eb9952e979ce9a501d4bb587a61e339b28e00b77c1c4621`; 203 lines, 157310 bytes).
   `.agent/live_review_archive.md` byte_eq=True against `sim-C2-live_review_archive.md` (sha256
   `9a029e29d6b09c34b52836fa7140b6132f3e6cf70d037fac5118490e0497f72b`; 7155 lines, 6095811 bytes).
   `git status --porcelain` showed only the two ledger files modified. `git diff --cached
   --numstat` (`.remedy-wt/f287-r17-worker/c2_stage.py`) read exactly the two cells `digests.txt`
   lists: `0 80 .agent/live_review.md`, `80 0 .agent/live_review_archive.md`. Committed as
   `8aa6ef25da84564b7f49552a641f1d4076c7696f`.
3. **C3 copy step** (`.remedy-wt/f287-r17-worker/c3_copy.py`): `docs/roadmap/STATUS.md` read
   byte_eq=True against `sim-STATUS.md` (sha256
   `aafe5d08893b04a5613c371e1dc225f5a215cb3fd837a92a0a2219162acb3b91`; 480 lines, 66047 bytes).
   `README.md` read byte_eq=True against `sim-README.md` (sha256
   `2238034839a51297fcbdae9bb6d8b1bd5bd22eb656cbb5ef854c5e8e511c3a7f`; 807 lines, 54479 bytes).
   `scripts/self_use_queue.json` read byte_eq=True against `sim-self_use_queue.json` (sha256
   `95a2e31eac5416e797709424cac2f3848a91918f6f0fb460c7d84ed285898618`; 374 lines, 161500 bytes).
   `git diff --numstat` (unstaged) read exactly the three cells `digests.txt` lists: `12 2
   README.md`, `1 1 docs/roadmap/STATUS.md`, `1 1 scripts/self_use_queue.json`. The full diff was
   read before staging (self-review): the STATUS line flip is exactly the `[~]` → `[x]` line
   swap with no other line touched; the README diff is exactly the `127 of 297` → `128 of 297`
   count, the Tier 3 row `6 \| 28` → `7 \| 28`, and F287's new paragraph inserted directly after
   F114's and before "Accepted in Tier 4 so far:"; the queue diff is exactly `SU-046`'s
   `consumed_by` from `""` to `"F287"`. No unrelated edit found.
4. **Gate 1** (`.remedy-wt/f287-r17-worker/gate1.py`): `git status --porcelain` read exactly three
   modified paths (`README.md`, `docs/roadmap/STATUS.md`, `scripts/self_use_queue.json`) after
   C3's copy step and before staging. Every file copied this round re-checked byte-equal against
   its prepared file (9/9 True): the three `.agent/authored/f287-r17*` files, `.agent/live_review.md`
   and `.agent/live_review_archive.md` (against their post-rotation sim files),
   `.agent/plan.md` (against `dry-plan.md`), and the three C3 files. `ALL BYTE COMPARISONS EQUAL:
   True`. PASS.
5. **Gate 2** (`.remedy-wt/f287-r17-worker/gate2.py`): the content of `status_line.txt` without
   its trailing newline occurs exactly once (`count=1`) in `docs/roadmap/STATUS.md`, and no line
   of it begins `- [~]`. PASS.
6. **Gate 3** (`.remedy-wt/f287-r17-worker/gate3.py`, run once):
   `python3 -m pytest -q -rfEs tests/docs/ tests/cli/test_advertised_commands.py
   tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
   tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py
   tests/cli/test_golden_path.py` — exit 0, `555 passed in 61.92s`, no FAILED, ERROR or SKIPPED
   line. PASS.
7. **Gate 4** (`.remedy-wt/f287-r17-worker/gate4.py`, `python3 -m apps.cli.main integrity check
   --json`, exit 0): `{"check_count": 6, "checks": [{"message": "handlers=175", "name":
   "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name":
   "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False",
   "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name":
   "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or
   archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open
   blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0,
   "ok": true, "passed": true, "schema_version": 1, "version": 1}`; six of six checks `pass`,
   `fail_count: 0`. PASS.
8. **Gate 5** (`.remedy-wt/f287-r17-worker/gate5.py`, `python3 -c "import
   scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`):
   `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162']` —
   exact match to the block's ordered list. PASS.
9. **Gate 6** (after the push and the pull request): reported in the worker's final reply (not
   known when this file is written).

## Authored-text proofs

- `block.md` → `.agent/authored/f287-r17.md`: 127 / 127 lines, sha256
  `f464444be81ea52a9db59423e649c7a6928a3a23c6a83c368ead985003cd45a3` / same.
- `pr_body.md` → `.agent/authored/f287-r17-pr_body.md`: 103 / 103 lines, sha256
  `c25b5620cd695262f0b0b8e778d68705da8dd37c6feb275fb640f7cade9e0228` / same.
- `status_line.txt` → `.agent/authored/f287-r17-status_line.txt`: 1 / 1 line, sha256
  `042fb5ef8b66d999530e61d509876198c69d2b3a555647b56734b754b6ff186a` / same. The same bytes, minus
  their one trailing newline, occur exactly once inside `docs/roadmap/STATUS.md` (gate 2 above) —
  the STATUS line is byte-identical to the authored file with its trailing newline (count 1)
  stripped.
- `dry-plan.md` → `.agent/plan.md`: byte-equal, `True`.
- `sim-STATUS.md` → `docs/roadmap/STATUS.md`: byte-equal, `True`.
- `sim-README.md` → `README.md`: byte-equal, `True`.
- `sim-self_use_queue.json` → `scripts/self_use_queue.json`: byte-equal, `True`.
- `sim-C2-live_review.md` / `sim-C2-live_review_archive.md` → the post-rotation
  `.agent/live_review.md` / `.agent/live_review_archive.md`: byte-equal, `True` / `True`.

## Deviations & assumptions

1. **Commit attribution trailer.** The block's Constraints order "Every commit ends with a
   `Co-Authored-By:` trailer naming the model you run on" — this worker runs on Claude Sonnet 5,
   and a standing harness attribution instruction names `Co-Authored-By: Claude Sonnet 5
   <noreply@anthropic.com>` for commits this session makes. `33b124749` and `8aa6ef25d` both
   carry that trailer; this handback's own closing commit will too. Not a deviation — the block
   names "the model you run on", not a fixed string.
2. From the block's ordered commit/action sequence: none — C1 landed exactly as ordered (five
   files, five numstat cells matching `digests.txt`), C2 ran the rotation script once and its
   output matched the block's expected reading exactly, before committing exactly the two ledger
   files, C3's three files were copied and byte-verified before gates 1-5 ran (in that order,
   all green) and before this handoff was written. No extra commit, none dropped, no reordering.
3. Helper scripts under `.remedy-wt/f287-r17-worker/` (gitignored, left untracked) did the digest
   checks, the HEAD/branch checks, the C1 copy/stage/commit, the rotation run and its
   re-verification, the C3 copy/stage, and gates 1 through 5; none touched any path outside the
   one named per commit, and none touched `.remedy-wt/f287-r17/` (the reviewer's prepared files,
   read-only throughout, re-verified unmodified by never writing to that directory).
4. No `cd` command of any kind was run this round, compound or standalone, no-op or otherwise —
   every command used `git -C /home/decodeux/Repos/remedy` or an absolute-path Python script with
   `cwd="/home/decodeux/Repos/remedy"`.
5. `.agent/STOP` was not present at any point in the round (checked before C1 and again before
   writing this handback).
6. No mutation red-proof and no full suite ran. Gate 3 is the round's one test selection and the
   round's one pytest invocation; no two test commands ran at the same time; `REMEDY_TEST_MAX_WORKERS`
   was not set and `-n` was not passed.
7. The tracked path set this round is exactly the three `.agent/authored/f287-r17*` files,
   `.agent/live_review.md`, `.agent/plan.md` (C1); `.agent/live_review.md` and
   `.agent/live_review_archive.md` (C2); `docs/roadmap/STATUS.md`, `README.md`,
   `scripts/self_use_queue.json` and `.agent/handoff.md` (C3) — matching the block's Constraints
   path set exactly.
8. No other departure.

ANY DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE BELONGS HERE: none beyond item 1 above
(a continuity note, not an actual deviation).

## For the operator, in plain sentences

The feature that lets a paused or stopped task continue its earlier conversation with the Claude
command-line tool, instead of paying again for what that conversation already knew, is finished
and accepted. A pull request is open for it and will be merged at the start of the next session
unless the operator merges it earlier. Nine smaller problems — one found during this feature and
eight carried from earlier ones — are written down for the next clean-up feature. Nothing waits
for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback
   and stop. (Not present as of this handback.)
2. Then the Open PR Gate, which merges F287's pull request in the NEXT session and never in this
   one.
3. Then the booking of round 17's verdict, in the next feature's first commit.
4. Then Rule A5: the next unchecked line in `docs/roadmap/STATUS.md` is F116.

Operator questions open: 0.
Open findings: 9 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158 and
R-1162, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 16, save the round 17 block, the STATUS line and the PR body | done | `33b124749` |
| C2: rotate the finding ledger into its archive | done | `8aa6ef25d`; output matched the block's expected reading exactly |
| Gates 1-5 | done | all PASS, before the handoff was written |
| C3: copy the three files, accept F287 in STATUS with its README sync and the self-use queue | done | this commit |
| Handoff rewrite | done | this file |
| Push | pending | run right after this commit, reported in the worker's final reply |
| Pull request create | pending | run right after the push, reported in the worker's final reply |
| Gate 6 | pending | run after the pull request, reported in the worker's final reply |
