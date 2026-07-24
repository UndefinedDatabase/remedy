# Agent Operating Rules

> Source of truth for automated agents working in this repository.
> This file defines mandatory behavior, workflow constraints, documentation boundaries, and runtime state rules.

## Audience

These rules bind the WORKER — any agent that writes, commits, or merges
in this repository. The read-only planner/reviewer role (Window 1 of
docs/agents/split_workflow.md) is governed by
docs/agents/planner_reviewer_prompt.md; it writes nothing and therefore
most sections below do not apply to it. On safety and scope discipline,
this file binds every agent.

## 🔒 Mandatory Agent Rules

These rules apply to any automated agent (Claude, AI assistants, scripts) working in this repository.

------------------------------------------------------------------------

## Priority

- This file has the highest priority for agent behavior.
- Rules in this file MUST NOT be weakened, ignored, or reinterpreted.
- If other files conflict with this file, `AGENTS.md` wins.

If anything is ambiguous:

- preserve safety
- preserve scope discipline
- prefer smaller changes
- prefer repository state over session memory

------------------------------------------------------------------------

### Core Workflow

- Never work directly on `main`.
- Never commit directly to `main`.
- Always use a `feature/*` branch.
- Keep commits small and logically scoped.
- Never mix unrelated features or fixes in the same branch.

------------------------------------------------------------------------

### Open PR Gate

Before creating a new feature branch or starting a new unrelated task, the agent MUST check for open pull requests.

Run:

    gh pr list --state open --json number,headRefName,baseRefName,isDraft

Rules:

- If there are no open PRs, continue normally.
- If there is exactly one open PR from a `feature/*` branch into `main` and it is not a draft, merge it before continuing.
- If there are multiple open PRs, stop and report them. Do not merge automatically.
- If the PR is a draft, stop and report it. Do not merge.
- If the PR does not target `main`, stop and report it.
- If the PR does not originate from `feature/*`, stop and report it.

Merge command:

    gh pr merge <number> --merge --delete-branch

After merging:

    git checkout main
    git pull --ff-only

The agent MUST NOT create a new branch while a mergeable, non-draft `feature/*` PR into `main` is open.

If the PR cannot be merged (conflicts, failing checks, missing approvals, or policy restrictions):

1. stop
2. report the blocker
3. do not proceed with new work

------------------------------------------------------------------------

### Branching

When asked to implement a feature, fix, refactor, or documentation change:

1. Check the current branch.
2. If already on a matching `feature/*` branch, continue there.
3. Otherwise create a new feature branch.

Branch naming format:

    feature/<short-kebab-description>

------------------------------------------------------------------------

### Creating a Feature Branch

Before running these commands, the Open PR Gate MUST pass.

    git status
    git checkout main
    git pull
    git checkout -b feature/<name>

------------------------------------------------------------------------

### Starting a New Feature While Already on a Feature Branch

If a new unrelated task is requested:

1. Finish the current logical unit of work.
2. Commit remaining changes.
3. Push the branch.
4. Run the Open PR Gate.
5. Switch to `main`.
6. Pull latest changes.
7. Create a new feature branch.

Never implement multiple unrelated tasks in the same branch.

### PR Scope Drift Prevention

When a new step range (e.g. Steps 48-50) is requested and an open PR already exists for an earlier step range (e.g. Steps 35-37) on the current branch:

1. **Preferred**: Merge the existing PR first (via Open PR Gate), then create a new branch for the new step range.
2. **If merge is blocked** (conflicts, pending review, etc.): Create a new branch from the current branch tip, do the new work there, and create a separate PR.
3. **Last resort only** (user explicitly requests continuing on the same branch): Update the existing PR title and description to cover all included step ranges immediately after the first commit of new work.

Never let a PR title/description fall out of sync with the actual commits on the branch. A PR whose title says "Steps 35-37" but contains Steps 35-50 is a review hazard.

------------------------------------------------------------------------

### Mandatory Self-Review Loop (Before Every Commit)

Run:

    git diff --stat
    git diff

Check for:

- obvious bugs
- unintended edits
- debug leftovers
- broken imports
- formatting noise
- unrelated changes
- deviations from the request
- scope drift

Additionally verify:

- what exactly this change does
- what could break
- whether it matches the plan

If issues are found:

1. fix them
2. re-run diff
3. repeat until clean

Only then commit.

------------------------------------------------------------------------

### File Editing Safety Rules

Before modifying any file:

1. Read the entire file.
2. Understand structure and context.

After editing:

1. Re-read the entire file.
2. Verify syntax correctness.
3. Verify logical consistency.
4. Fix any issues.

Files must remain:

- syntactically correct
- consistent with architecture
- free of obvious bugs

------------------------------------------------------------------------

### Commit Discipline

- Commit after every logical step.
- Use clear commit messages.
- Avoid large or mixed commits.
- Target one step per commit. Do not bundle multiple unrelated steps.
- If a diff exceeds 500 lines, stop and split before committing.
- Never mix refactoring with new features in the same commit.
- Commit subjects never contain leading-slash tokens ('/foo'), absolute
  paths, or secret-like strings — the evidence-packaging metadata scanner
  rejects such subjects and blocks closure. Write 'add review-remedy
  slash command', never 'add /review-remedy command'. (Learned 2026-07-23:
  one such subject blocked the F081 closure for several rounds.)

If changes become too large:

- stop
- split changes
- re-plan

------------------------------------------------------------------------

### Push Discipline

After committing:

    git push -u origin <branch>

------------------------------------------------------------------------

### Task Completion Protocol

When a logical unit of work is fully complete:

1. Update `.agent/plan.md` to reflect the current completion state
2. Commit all relevant changes, including plan updates if needed
3. Push to remote promptly
4. If the branch is in a reviewable state and no PR exists, create a PR

Do not treat local-only committed work as finished.

Work is considered review-ready only when:
- `.agent/plan.md` reflects the current state
- relevant changes are committed
- the branch is pushed
- a PR exists if the branch is ready for review

Before every commit:

1. Verify that `.agent/plan.md` reflects the current state
2. If not, update it before committing
3. Ensure the current step is accurate

A step is considered complete only when:
- the implementation matches the intended change
- no obvious issues remain in the diff
- `.agent/plan.md` is updated
- the next step is clearly defined or the task is finished

------------------------------------------------------------------------

### If Blocked

If the agent cannot complete the current task:

1. Do not pretend the task is finished
2. Update `.agent/plan.md` with the exact blocker
3. Clearly state what remains unfinished
4. Commit and push only the valid completed portion, if appropriate
5. Create or update a PR only if the current branch is still reviewable

------------------------------------------------------------------------

### Reading PR Review Comments

When addressing review comments, always read all three sources with pagination:

    gh api --paginate repos/<owner>/<repo>/issues/<n>/comments
    gh api --paginate repos/<owner>/<repo>/pulls/<n>/comments
    gh api --paginate repos/<owner>/<repo>/pulls/<n>/reviews

For each review, also fetch its attached comments (catches PENDING draft comments):

    gh api --paginate repos/<owner>/<repo>/pulls/<n>/reviews/<review_id>/comments

Do not assume there are no comments until all four sources have been checked.

Before making any code changes for review feedback, the agent MUST:

1. group related comments
2. detect overlaps, duplicates, and conflicts
3. identify comments that can be solved by one coherent change
4. validate each comment against the current code, architecture, and intent of the change
5. identify comments that are outdated, incorrect, low-value, or should not be applied
6. define the smallest coherent implementation plan

The agent MUST NOT implement review comments one-by-one by default.

The grouped review handling plan MUST be reflected in `.agent/plan.md` before code changes begin.

If a review comment is intentionally not applied, the reason MUST be recorded in `.agent/decisions.md` or in PR discussion context, as appropriate.

------------------------------------------------------------------------

### Pull Request Workflow

When work reaches a reviewable state:

1. Ensure all changes are committed.
2. Push the branch.
3. Check for existing PR.
4. If none exists:

    gh pr create

The PR must include:

- what changed
- why it changed
- key decisions
- how to review/test

Rules:

- Do not create duplicate PRs.
- Do not merge without instruction.
- Prefer small PRs.
- Keep diffs mobile-friendly.

------------------------------------------------------------------------

## 🧠 Runtime State Management

The agent MUST NOT rely on session memory.

All working state MUST be externalized.

### plan.md

Location:

    .agent/plan.md

Must contain:

- Goal
- Current Step
- Next Steps
- Review Strategy (when handling PR feedback)
- Risks (optional)

Rules:

- keep it short (<50 lines)
- rewrite, do not append
- remove completed items

### context.md

Location:

    .agent/context.md

Purpose:

- scope boundaries
- active assumptions
- current constraints
- current branch context

Rules:

- update when scope changes
- update when assumptions change
- update when constraints change
- keep it task-specific and minimal
- do not copy durable project knowledge into this file

### decisions.md

Location:

    .agent/decisions.md

Purpose:

- important decisions made during the current task
- rationale for non-obvious implementation choices
- temporary decisions that may later move to `docs/`

Rules:

- update when a meaningful implementation or scope decision is made
- do not use it as a full activity log
- keep entries concise
- move durable architectural knowledge to `docs/`

### handoff.md

Location:

    .agent/handoff.md

Purpose: the fast-resume snapshot for the planner/reviewer. Rewritten
(never appended) by the worker at every handback; only the latest state;
≤60 lines; git history is the archive. Contents: feature + round, branch,
last commit SHAs, changed-files table, verification results (real,
trimmed), open findings count, next expected action.

- Every artifact-build attempt (evidence bundle, review zip)
  appears in the handoff with its status, including failed
  attempts with blocking reasons.

### Documentation Updates

The agent MUST update `docs/` when:

- a feature introduces new behavior that is not yet documented
- an existing behavior is changed
- architectural decisions affect long-term understanding
- setup or usage instructions change

Rules:

- keep documentation concise and accurate
- do not duplicate code
- do not include temporary or task-specific content
- prefer updating existing files over creating new ones
- register new or renamed docs in the index `docs/README.md` (category, one-line
  description, status marker)

------------------------------------------------------------------------

## 🔁 State Update Triggers

The agent MUST update `.agent/plan.md`:

1. after creating a plan
2. after changing a plan
3. after completing a step
4. when the current step changes
5. when a blocker is encountered

The agent MUST update `.agent/context.md`:
1. when scope changes
2. when assumptions change
3. when constraints change
4. when the active branch context becomes relevant to the task

The agent MUST rewrite `.agent/handoff.md` at every handback to Window 1.

The agent MUST update `.agent/decisions.md`:
1. when a meaningful technical decision is made
2. when a non-obvious tradeoff is chosen
3. when a decision affects later implementation steps
4. when a review comment is intentionally rejected, deferred, or merged into a broader fix

Note: "before every commit" is handled by the Commit Gate.

------------------------------------------------------------------------

## 🚫 Commit Gate

Before committing:

1. Verify `.agent/plan.md` matches the current work
2. Ensure the current step is accurate
3. Ensure the diff is focused and reviewable
4. Ensure the diff matches the intended plan
5. Verify that review comments in scope were handled coherently rather than one-by-one
6. Verify that any skipped, rejected, or deferred review comments are documented appropriately
7. Verify whether `.agent/context.md` or `.agent/decisions.md` need updates
8. Verify whether relevant documentation in `docs/` needs to be updated

If any of these fail:

- DO NOT COMMIT

------------------------------------------------------------------------

## 🔄 Session Resume

On new session or after reboot:

1. Read `AGENTS.md`
2. Read `.agent/plan.md`
3. Identify relevant files via the index `docs/README.md` (quick-find table);
   for roadmap work also read `docs/roadmap/ROADMAP.md` Teil A and the active
   `docs/roadmap/features/T?_F???.md`
4. Read only the relevant documentation
5. Run:

    git log --oneline -n 5
    git diff main...HEAD

6. Reconstruct context
7. Continue from current step

If plan is missing:

- recreate it before proceeding

------------------------------------------------------------------------

## 🎯 Scope Control

- Only work within current task scope.
- Do not introduce unrelated changes.
- No "while I'm here" edits.

The agent MUST NOT introduce changes that are not reflected in `.agent/plan.md`.

If new work appears:

1. Update the plan first
2. Then implement the change

Or:

- defer it
- or create new branch

------------------------------------------------------------------------

## 📏 Change Size Limits

- Keep commits small
- Keep PRs small
- Avoid mixed diffs

If diff becomes large:

- stop
- split
- continue in smaller steps

------------------------------------------------------------------------

## 🧩 Documentation Structure

Use four layers:

AGENTS.md → rules  
docs/ → long-term knowledge about the BUILT system (index: `docs/README.md`)  
docs/roadmap/ → the TARGET plan (ROADMAP.md + 250 feature detail files)  
.agent/ → current task state (plan, live review, context, decisions)  

`docs/roadmap/STATUS.md` IS the roadmap execution ledger. There is no separate
`.agent/ROADMAP_LEDGER.md`: a second ledger would only be a second source of truth.

Do NOT mix them.

Boundary rules:

- `docs/` describes what IS; `docs/roadmap/` describes what SHALL BE. On conflict,
  `docs/roadmap/ROADMAP.md` wins for planning; the ist-doc still correctly describes
  the built state and gets a `> **Status (…)**` banner pointing to the roadmap.
- Agents MUST NOT edit `docs/roadmap/ROADMAP.md` unless the operator explicitly
  requests it. Feature detail files (`docs/roadmap/features/`) change via normal PRs.
- When looking for any document, start at `docs/README.md` (categorized index with
  a quick-find table). When adding an ist-doc, add it to that index in the same PR.

------------------------------------------------------------------------

## 🔒 Safety Rule

The non-human content policy MUST NOT be weakened.

------------------------------------------------------------------------

## 🧠 Operating Principle

- Session is disposable
- Repo is durable
- plan.md is the bridge