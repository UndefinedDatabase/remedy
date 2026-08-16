# Handback — F083 R28 (CLOSURE)

## Range
Review of 74063862..HEAD on feature/f083-ci-self-check. Ordered sequence C0a, C0b, C1, C2, C3 followed exactly; C3 is the last commit.

## Commits
### fb8a703a docs(f083): save the R28 closure block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f083-r28.md | 317/0 | C0a — block copied byte-for-byte (`shutil.copyfile`; `cp` is denied here) |
### ae303b0f chore(agent): mirror the R28 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | 275/242 | C0b — mirror of the COMMITTED authored copy |
### 6bcc4d39 docs(review): record the R27 PASS verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | C1 — RECORD-R27 appended at EOF, deletion column 0 |
### 83f3eb31 docs(f083): advance the plan to the closure round
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | 13/16 | C2 — PLAN slice, whole file. **ACCEPTED HEAD 83f3eb31f5020bc5201a23b06e23e7558ee01b4e** |
### C3 (this commit) docs(f083): close F083 in the roadmap ledger
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | 1/1 | STATUSLINE pair, `[~]`→`[x]` with package, SHA-256 and accepted HEAD |
| README.md | 2/2 | READMECOUNT 49→50 and READMETIER 11→12, same commit as STATUS (R-0154) |
| .agent/candidates.md | 15/4 | CANDIDATES slice, whole file — carrier is EMPTY for F083 |
| .agent/handoff.md | — | this file (R-0149 self-reference) |

## External actions
- `git push -u origin feature/f083-ci-self-check` → 74063862..83f3eb31, OK (before the zip build, per the canonical sequence).
- The push of C3 and `gh pr create` run AFTER this commit, so their outcomes — PR number and URL — cannot exist in this file and ride in the ROUND REPORT, the same item-14 routing R-0489 established. No `gh pr merge` is run in this session.
- No worktree added or removed — `git worktree list` is ONE line throughout.

## Verification
- pwd `/home/decodeux/Repos/remedy`. `git rev-parse HEAD` before C0a = 74063862…, equals the ordered base. `git status --porcelain` EMPTY before C0a and before the zip build; the post-C3 reading cannot exist in this file and rides in the round report. `.agent/STOP` absent at round start and at handback.
- TRANSPORT: `.remedy-wt/f083-r28.md`, committed `.agent/authored/f083-r28.md` and committed `.agent/last_block.md` all sha256 822f27dee592af55b29761c3bddab530ee64735850bdbcfb3171f957b283387f, 23611 B, 317 lines — byte-EQUAL.
- C1: pre (315460 B) PREFIXES post (320295 B); tail byte-EQUALS the RECORD-R27 slice; numstat `2 0`. live_review BEGIN-marker LINE count 0 at base and 0 at HEAD.
- C2: `.agent/plan.md` byte-equals PLAN, sha256 21bc00f89b2fe12fab8e76e85ff7f3ca6b583930af2362f1ebdbca80a5ba677a, 38 lines (<50), `## Goal` and `## Next Steps` present, 0 unchecked-box lines.
- EVIDENCE JOB `f083-closure`: verdict PASS_WITH_RISKS, authority_count 20, partition T001 7/T002 7/T003 6, commit_count 189, total_passed 121, head 83f3eb31…. Dir `remedy-job-evidence-f083-closure/` (gitignored line 226) — `git status --porcelain` STILL EMPTY after.
- VERIFICATION RECORD, from a real run of the seven scoped files (`python3 -m pytest <7 files> -q` → 121 passed, exit 0): selected 121 == len(node_ids) 121; test_files = those seven files, sorted True; run_id `vr-0001` matches `^vr-\d{4,}$`; output_hash 9def1a8d… 64 hex.
- REVIEW ZIP: `bash scripts/make_review_zip.sh --evidence-dir remedy-job-evidence-f083-closure`, exit 0 → **remedy-review-20260816-082019-READY_FOR_REVIEW.zip**, SHA-256 **162bacf6265e79651b098c524b5060de44d58e9d89e9ec4d645c158950b78986**. Manifest `committed_review_subject.head_commit` = 83f3eb31f5020bc5201a23b06e23e7558ee01b4e = the C2 head. First attempt: see Deviations.
- STATUS LINE: `<<` occurs 0x in the file; replacing the three measured values back with their tokens reproduces STATUSLINE-TO BYTE-FOR-BYTE (True). `^- \[~\] F083` 0x, `^- \[x\] F083` 1x, `^- \[x\] F\d{3} — ` 50 lines.
- README: READMECOUNT FROM 1 before / 0 after, TO 1 after; READMETIER FROM 1 before / 0 after, TO 1 after; composite `pre.replace(F1,T1).replace(F2,T2) == post` True.
- `python3 -m pytest tests/docs/ -q` → 295 passed, exit 0. `python3 -m pytest tests/cli/test_golden_path.py -q` → 42 passed, exit 0. `remedy integrity check --json` → exit 0, passed True, fail_count 0; handler_import, live_review_verdict, plan_consistency, relevant_untracked and high_blockers_open all pass.
- OPEN SET at HEAD: 117 registered, 13 resolved, 0 landed, **104 open**; max R-0489, next free R-0490; 0 duplicate ids, 0 resolutions naming an unregistered id; R-0482 and R-0487 still open.
- Per-commit insertions C0a 317, C0b 275, C1 2, C2 13 — none over 500. C3's own count goes in the round report (checklist item 14). History linear, 4 single-parent commits in the range when read (C3 not yet made); reflog shows only `commit:` entries; no amend, rebase, reset or force-push.

## Authored-text proofs
Every slice extracted programmatically from the COMMITTED `.agent/authored/f083-r28.md` by its markers and applied byte-verbatim: RECORD-R27 (tail equality), PLAN (whole-file byte equality), CANDIDATES (whole file), and the pairs STATUSLINE, READMECOUNT, READMETIER (single-occurrence replacements, counted before and after). STATUSLINE is verbatim except the three ordered placeholders, proven by the round-trip above. No transport marker reached any target file.

## Deviations & assumptions
1. **The FIRST zip attempt packaged BLOCKED_EVIDENCE and was fixed, not closed over.** `remedy-review-20260816-081828-BLOCKED_EVIDENCE.zip` (SHA-256 cce65acad2e2278d4b9748f637512f5c14cd9c0fd8824cab8cb0dfdf910ef798), single manifest error verbatim: `verification_tests.json runs[0] output_hash does not match sha256(stdout_summary)`. Cause: I hashed the full pytest stdout while recording only its last line as `stdout_summary`; the packaging validator in `scripts/build_review_manifest.py` requires `output_hash == sha256(stdout_summary)`. Fix: record the whole 181-char stdout as `stdout_summary` and hash exactly that; rebuild the evidence job and the zip from the SAME clean tree at the SAME head. Nothing committed changed between the attempts. Read as protocol step 2's "fix or go `[!]`" branch; the block's constraint 7 (end the round) was read as covering a build this round could not repair without a commit, which this was not. The reviewer may rule otherwise — the raw error and both packages are recorded here.
2. `cp` is denied in this session, so C0a copied through `shutil.copyfile`; the PROPERTY the gate names (byte equality + shared sha256 of the committed blobs) was measured, not the tool. `/tmp` is denied, so scratch lives in the gitignored `.remedy-wt/`.
3. This file is within the 60-line cap but over the template's ≤800-token guidance; the cause is mandated content — five per-commit tables plus the closure values. No section dropped, no padding, no transcript.
4. The ordered commit sequence C0a, C0b, C1, C2, C3 was followed EXACTLY — no extra commit, none dropped, no reordering. Nothing follows C3.

## Next
The PR is NOT merged in this session. It merges at the NEXT feature's start via the AGENTS.md Open PR Gate; the gap is the operator's manual-review window. Window 1 reviews this closure round.
