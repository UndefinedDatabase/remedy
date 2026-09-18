
## DECISION F270 D4 (2026-09-18, reviewer, round 4) — `do` takes the commit and push flags, chains its jobs under them, pushes once per mission; a push is held by a RED blocking criterion, amending D3 (5)
CONTEXT: `docs/roadmap/features/T2_F270.md` Design: the flag family is "passed through by `do`";
every `--commit…` flag implies `--apply`; push is a mission-level act, `do` pushes once at the end
of the mission, not per job; `apply.push_after_mission` makes unattended runs push as `--push`
would; a push happens "only when no blocking contract criterion is red". DECISION F268 D12 left
a `do` walk of several jobs running the first and leaving the rest waiting, because a plain apply
does not commit and a job's worktree is cut from `HEAD`, and it names F270's `--commit` family as
what lets the jobs chain. Measured at `8e9c2fad` by a research helper's prototype in a disposable
worktree, which the reviewer read: `_DO_FLAGS_NOT_YET_AVAILABLE` in `apps/cli/commands/do_cmd.py`
holds exactly these four flags; chaining under a commit flag is 46 lines of
`packages/orchestration/do_sequence.py` and changes no F268 test; and — by DECISION F269 D6 —
`do`'s jobs serve no milestone, so the planner's per-milestone blocking criteria of a `do` mission
are never evaluated and stay `open`, which under D3 (5) would refuse every real `do --push`.
CHOSEN: (1) FLAGS. `do` accepts `--commit "<message>"`, `--commit-auto`, `--commit-with-history`
and `--push` with `job apply`'s rules (D3 (1)): one commit flag at most, `--push` only with one, a
`--commit` message non-empty and one line; each commit flag implies `--apply`; with `--plan-only`
any of them is refused. These refusals, and the checkout refusals of D3 (2), and with a push the
upstream refusals of D3 (5), are asked BEFORE any step runs and exit 2 with "Nothing was run.", so
a long run is never spent on a push that cannot happen. The four flags leave
`_DO_FLAGS_NOT_YET_AVAILABLE`, which goes with its refusal function once empty. (2) CHAINING.
Under a commit flag no job of the walk waits: each job is run, applied and committed (or merged)
before the next job's worktree is cut, so each sees the work before it; without a commit flag F268
D12 stands unchanged. A walk that stops at a job commits what it had applied, pushes nothing, and
says so. (3) MESSAGES in a walk of more than one job: `--commit` gives each job's commit the
operator's line followed by ` (job <k> of <n>)`; `--commit-auto` takes each job's title first,
then the mission's goal, then the fixed sentence, under D3 (4)'s rule; `--commit-with-history`
merges each job's branch in turn. (4) ONE PUSH. The apply step never passes `--push` to
`apply_job`; after the walk's last job `do` asks the upstream and contract refusals again and
pushes the last landed commit once, never forced, through the same push function `job apply`
uses. A refused or failed push leaves every commit where it landed and exits 1. (5) THE KEY.
`apply.push_after_mission`, read with the repository's configuration, makes a `do` run with a
commit flag push exactly as `--push` would; with the key set and no commit flag, `do` commits and
pushes nothing and prints one sentence saying so on stderr, so `--json` stays clean. (6) RED, for
`do` and for `job apply` alike, amending D3 (5): a push is refused while any blocking criterion of
the mission is `unmet` — the spec's "red"; a blocking criterion still `open`, which no gate has
evaluated yet, does not hold the push but is named in the push's output and record as not yet
evaluated. For a single-job `do` and for `job apply`, a red contract refuses before anything is
applied; in a chained walk, where the contract is final only after the last job, the commits land
and the push is refused. (7) `do --json` gains `landed` (each landed commit with its job) and
`push` (remote, ref, pushed, error, and the open blocking criteria named). `docs/guides/do-run-v1.md`
states the flags, that Remedy never commits on the operator's branch by itself, and the new keys.
ALTERNATIVES: keeping D3 (5)'s `open`-blocks rule, rejected because by F269 D6 it refuses every
real `do --push` and so turns the feature's push acceptance into a fixture-only property; one
job per `do` under a commit flag, rejected because F268 D12 hands the chaining to exactly this
flag family and a mission-level push over one of several jobs would publish a partial mission;
pushing per job, rejected by the feature file. REVERSE: restore the four flags to
`_DO_FLAGS_NOT_YET_AVAILABLE` with its refusal, remove the chaining and the mission push, restore
D3 (5)'s `open`-blocks rule, and delete this paragraph.
