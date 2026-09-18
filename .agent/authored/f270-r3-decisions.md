
## DECISION F270 D3 (2026-09-18, reviewer, round 3) — `job apply` gains `--commit "<message>"`, `--commit-auto` and `--push`, and the config key `apply.push_after_mission` is registered
CONTEXT: `docs/roadmap/features/T2_F270.md` Design (the flag family, author and trailers, commit
messages for humans, `--push`) and T004. Measured at `4a615385` by a research helper's prototype in
a disposable worktree, which the reviewer read: a `Mission` has a `goal` and no title;
`contract_blockers` in `packages/orchestration/mission_contract.py` lists every blocking
criterion of the whole mission that is not `met`; the per-task subject `task 2: add the contact
form` cannot pass a verb-first rule; `git add` of a path the target's `.gitignore` matches fails;
no test pins the config registry's key list or `job.apply`'s argument list. `do`'s own flags stay
refused until the next round.
CHOSEN: (1) THE FLAGS on `job apply`: `--commit "<message>"`, `--commit-auto` and D2's
`--commit-with-history` are mutually exclusive; `--push` needs one of them. A clash, a lone
`--push`, and a `--commit` message that is empty or spans more than one line are refused before
the job is read. Like D2 (1), each flag needs `--approve`; without it the command previews and
names every refusal the real run would meet. A refusal is a blocked apply and exits as one (D2
(7)). (2) CHECKOUT REFUSALS, shared with D2 and checked after the existing gates and again right
before anything is written, each one sentence, each changing nothing: a target below its
repository's top level; a detached `HEAD`; the operator's own merge, rebase, cherry-pick or revert
in progress; a dirty tree, naming the paths; for `--commit` and `--commit-auto`, a copied path the
target's `.gitignore` matches. A staging job may be committed onto a git target, because the
commit holds only the copied files; D2 still refuses it for `--commit-with-history`. (3) THE
COMMIT. After the copy, its verification and the post-test pass, ONE commit on the operator's
current branch of exactly the copied files, under the operator's own identity, configuration and
hooks; afterwards its parent must be the previous tip and it must touch no other path. A post-test
that fails leaves the files copied and uncommitted, and the record says so; a commit that fails
is recorded as blocked and its paths are unstaged, the index only — the branch is never reset.
(4) MESSAGES. `--commit`: the operator's line, unchanged, as the first line. `--commit-auto`: the
first line is the mission's goal, else the job's title, else `Apply the <n> tasks of Remedy job
<first eight characters of the job id>`, the first candidate that passes the rule — one line, at
most 72 characters, at least three words, the first word from a fixed list of imperative verbs —
cut at a word boundary by the same fitter the per-task commits use; the body lists the task
titles. Both then carry one body sentence naming the job, the contract line of D1 (3) as the last
body line, and the trailers `Remedy-Job: <job id>` and `Co-authored-by: Remedy <remedy@local>`.
The per-task commits and `--commit-auto` share the subject fitter, the contract line and the
trailer names; the verb rule binds `--commit-auto` only. (5) `--push`, after the commit or merge
and the post-test, runs `git push --porcelain <remote> <landed sha>:<upstream ref>` to the
branch's configured upstream, never with force and never to another branch, with no credential
prompt and a timeout. It is refused before anything is written when the branch has no upstream
(the sentence names `git push --set-upstream <remote> <branch>`), when the upstream is a local
branch, when the mission's contract cannot be read, and while any blocking criterion of the
job's mission is not `met` — the push is a mission-level act, so the whole mission counts, and
an `open` criterion is not green. A push that fails after the commit landed leaves the commit,
records status `applied_push_failed` with git's words, and tells the operator to push by hand.
(6) THE RECORD keeps D2's fields and adds `commit_message_mode` (`""`, `message`, `auto`,
`history`), `commit_sha`, `push`, `pushed`, `push_remote` (the remote's name, never its URL),
`push_ref` and `push_error`. (7) THE CONFIG KEY `apply.push_after_mission`: a bool, default
false, env var `REMEDY_APPLY_PUSH_AFTER_MISSION`, one-sentence help, read by one helper that also
reads the string `"false"` as false; `job apply` never reads it, and a plain `--approve` with the
key set commits and pushes nothing. `do` uses it in the next round.
ALTERNATIVES: exiting 2 for a flag clash as `do` does, rejected for consistency with D2 (7) and
so `do` can reuse the refusals through `apply_job`; committing before the post-test as D2 merges
before it, rejected because a copy can stay uncommitted at no cost while a merge cannot be half
made; counting only the job's slice for `--push`, rejected because a push publishes the whole
mission's branch. REVERSE: remove the three flags, the shared refusals' new members, the record
fields and the key, and delete this paragraph.
