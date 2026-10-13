# F058 round 7, stop — commit the reviewer's handback from a worktree of the branch

Session 3 of F058. Round 7 stopped after its A2: another session switched the primary checkout
`/home/decodeux/Repos/remedy` to `feature/ui-external-host-links` and opened pull request 331. That
checkout is NOT yours: do not switch it, commit in it, stash in it, clean it or run anything that
writes in it. This block commits the reviewer's handback on `feature/f058-model-failover-chain`
(tip `0e3063d6a8ac72cfba8e683a168075dffda6f4ac`, equal to its origin) from a worktree of its own.

## Prepared files (`/home/decodeux/Repos/remedy/.remedy-wt/f058-r7/stop/`, read-only for you)
Check each sha256 with a Python reader before use; stop if one differs.
- `block.md` — this block (digest and line count in the prompt)
- `dry-handoff.md` for `.agent/handoff.md` — `ddada375029872083ad7b93d8818db73e8622bbfd4fccdd307ed38fa85763b95`
- `dry-operator_questions.md` for `.agent/operator_questions.md` — `b42658e7e583c47d9e322fb0c33c18ad93a292b55388ccf015e6cd8f158d4fbf`

## Steps
1. Read-only checks: `git -C /home/decodeux/Repos/remedy rev-parse feature/f058-model-failover-chain`
   and `... rev-parse origin/feature/f058-model-failover-chain` both read `0e3063d6a8ac...`;
   `git -C /home/decodeux/Repos/remedy worktree list` shows no worktree on that branch; `.agent/STOP`
   is absent. Else stop and report.
2. `git -C /home/decodeux/Repos/remedy worktree add /home/decodeux/Repos/remedy/.remedy-wt/f058-r7-stop-tree feature/f058-model-failover-chain`.
3. In that worktree (always `git -C /home/decodeux/Repos/remedy/.remedy-wt/f058-r7-stop-tree`, never
   `cd`), with one `python3` copy script under `/home/decodeux/Repos/remedy/.remedy-wt/f058-r7-stop-worker/`:
   copy `dry-handoff.md` over `.agent/handoff.md`, `dry-operator_questions.md` over
   `.agent/operator_questions.md`, and `block.md` to `.agent/authored/f058-r7-stop.md` (NEW FILE);
   prove each pair byte-equal (`True`). `git diff --cached --numstat` after `git add` of exactly
   those three paths names those three paths and no other. Read the staged diff whole (self-review,
   AGENTS.md).
4. `git -C <worktree> branch --show-current` reads `feature/f058-model-failover-chain`; commit with
   the subject `F058 R7 C2: handback after the shared checkout was taken`, ending with the
   co-author trailer naming the model you run on. Never amend.
5. `git -C <worktree> push origin feature/f058-model-failover-chain` (on an HTTP 500 wait 60 seconds
   and retry, at most three times; never force). Report the output.
6. `git -C /home/decodeux/Repos/remedy worktree remove /home/decodeux/Repos/remedy/.remedy-wt/f058-r7-stop-tree`,
   then report `git -C /home/decodeux/Repos/remedy worktree list` (no line for that path) and
   `git -C /home/decodeux/Repos/remedy branch --show-current` (still the other session's branch,
   untouched).

## Constraints
No test run, no provider call, no pull request created or merged, no other path. If anything
differs from what a step expects, stop and report it whole.
