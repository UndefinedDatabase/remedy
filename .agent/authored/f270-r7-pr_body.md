## F270 — History apply: one commit per task, merge on demand

Closes F270 (Tier 2) at PASS_WITH_RISKS. Accepted head `3e9897ac`, evidence job `f270r6e1001`, review package `remedy-review-20260919-002024-READY_FOR_REVIEW.zip` (SHA-256 `e058bfd3…46a2`).

### What it builds
- **One commit per applied task (T001).** Each applied task of a git-target job becomes one commit on the job's `remedy/job-<job id>` branch, authored `Remedy <remedy@local>`, with no hook or signing, and a refusal of any non-Remedy branch. The message is `task <n>: <title>` plus a contract line and the `Remedy-Job` and `Remedy-Task` trailers. A commit made by an interrupted run is adopted, not repeated (D1).
- **`job apply --approve --commit-with-history` (T002, T003).** After every existing apply gate, this merges the verified job-branch tip onto your current branch with `--no-ff`, as you and under your hooks. It refuses a dirty tree, a detached HEAD, a merge in progress, a staging job, a branch that is not the reviewed work, and a conflict; each refusal changes nothing (D2).
- **`--commit "<message>"`, `--commit-auto`, `--push` (T004).**
  - The two commit flags land one commit of exactly the copied files, after the post-test.
  - `--push` pushes the landed commit once, never forced, to the configured upstream. It refuses without an upstream, or while a blocking criterion is `unmet`; `open` ones are named (D3, D4).
  - `remedy do` passes the flags through, chains its jobs under a commit flag, and pushes the mission once.
  - `apply.push_after_mission` makes such a run push without `--push` (D4).
- Without one of these flags, Remedy commits nothing on your branch.

### Findings
- Raised and resolved here: R-0975 and R-0976.
- Found here and owned by F273: R-0974, R-0977 and R-0978.
- The closure suite read 1 failed and 18060 passed. The one failure, `test_study_run_dispatch_e2e`, passes when run alone and is load-bound (R-0978).

### Operator question
Q6 in `.agent/operator_questions.md`: a push waits only for a *failed* blocking criterion. This recommendation is already executed and reversible.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
