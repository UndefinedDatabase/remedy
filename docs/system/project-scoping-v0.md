# Project Scoping (F148)

> Every job belongs to exactly one project. Listings default to the current
> project; `--all-projects` shows everything.

## Job model

`Job.project_id: str | None` — set at creation time via the CLI's project
resolution. `None` means legacy (pre-F148).

## Scope resolution

CLI commands that list jobs resolve a `ProjectScope` via:

1. `--all-projects` flag → show everything
2. `--project <slug-or-id>` → that specific project
3. `REMEDY_PROJECT` env var → that specific project
4. cwd autodetection → project owning the current repo
5. fallback → all projects (no project resolvable)

## Legacy rule

Jobs with `project_id=None` are visible only when:
- `--all-projects` is active, OR
- exactly one project exists on the machine

## Commands affected

| Command | Scope support |
|---------|--------------|
| `job list` | `--project`, `--all-projects` |
| `status` | auto-scoped to cwd project |
| `project adopt` | bulk-adopt unscoped jobs |

## Display labels

Under `--all-projects`, jobs show suffixes:
- `(unscoped)` — `project_id` is `None`
- `(project: <id>)` — belongs to a different project

## Creation guard

`remedy job create` and `remedy do run` require a resolvable project
(exit 3 with fix-it hint if none found). Library functions keep
permissive `project_id=None` for test harnesses.
