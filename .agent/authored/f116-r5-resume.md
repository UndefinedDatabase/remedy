# F116 round 5 — RESUME (session 2): finish C3 and C4 of the committed block

The round 5 block is committed at `.agent/authored/f116-r5.md`; it is your specification, read it
whole. Its C1 (`f3952cac2`) and C2 (`47d00224b`) are committed locally and NOT pushed; `origin` still
reads `8effa367afddb795830c417e1141449a2af60e53`. The previous session ended in the middle of C3:
the primary checkout holds UNCOMMITTED edits to exactly C3's three paths
(`packages/orchestration/job_burn.py`, `packages/orchestration/pingpong_job.py`,
`tests/orchestration/test_job_burn.py`). The production half (D5 (1) to (3)) is drafted; the test
file has only new imports, none of the block's C3 test functions.

## What you do
1. Before any write: `git rev-parse HEAD` reads `47d00224b71ccdff0c6256d5aa7d92607506cf1b`;
   `git status --porcelain` lists exactly the three C3 paths above and nothing else; `.agent/STOP`
   is absent. If any of that differs, commit nothing and report.
2. Read the uncommitted diff (`git -C /home/decodeux/Repos/remedy diff`) against the block's C3 and
   DECISION F116 D5 (`grep -n -A8 '^## DECISION F116 D5' .agent/decisions.md`). Keep what matches,
   correct what does not, and say in the handback which drafted lines you changed and why. Do NOT
   discard the draft with `git checkout`, `git restore` or `git stash`; edit it.
3. Write every C3 test the block lists, then commit C3 with the block's subject. Split per the
   block's 500-insertion rule if needed.
4. Run gates 1 to 5 exactly as the block orders (gate 1's "C1's byte proofs" is satisfied by
   re-running `.remedy-wt/f116-r5-worker/c1_proofs.py` if it still applies to HEAD's C1, otherwise
   by `git show --numstat f3952cac2` reading four paths — say which).
5. C4 as the block orders, with these differences: the Session line reads
   `SESSION 2 of feature F116 · round 5 (resumed) · rounds so far 5`; the Session section adds one
   sentence that session 1 ended inside C3 and session 2 resumed it from the uncommitted draft; the
   `## Commits` table covers C1, C2, C3 and C4; and C4 also adds this file, byte for byte, as
   `.agent/authored/f116-r5-resume.md` (report its line count and sha256 against
   `/home/decodeux/Repos/remedy/.remedy-wt/f116-r5-resume/resume.md`).
6. Push once, as the block's THEN orders, and report gate 6 in your reply.

Every constraint of the block binds unchanged: no `cd`, helper scripts under
`/home/decodeux/Repos/remedy/.remedy-wt/f116-r5-worker/`, never `/tmp`, no mutation, no full
suite, no `-n`, one gate 2 run, the `Co-Authored-By:` trailer naming the model you run on.
