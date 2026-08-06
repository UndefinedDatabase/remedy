# Roadmap Mirror & the `plan` CLI Group

> How Remedy READS its own roadmap. Built for F080 (T001–T003).
> The roadmap itself — the target plan — lives in
> [docs/roadmap/](../roadmap/ROADMAP.md); this page describes the
> machinery that mirrors it, which is built and in use.

## The one-way mirror rule

Three human-owned markdown files are the truth:

| File | What it holds |
|---|---|
| [docs/roadmap/ROADMAP.md](../roadmap/ROADMAP.md) | the plan, the grammar (Part C), the milestones (Part G) |
| `docs/roadmap/features/T<tier>_F<id>.md` | one detail file per feature |
| [docs/roadmap/STATUS.md](../roadmap/STATUS.md) | the execution-order ledger |

`packages/orchestration/roadmap_index.py` mirrors them into a generated
JSON index under the data root (`REMEDY_DATA_DIR`), at
`<data_root>/roadmap/index.json`.

The mirror runs **one way only**, and the rule has teeth:

- the index is **regenerated on every read path** — there is no refresh
  verb, no cache to invalidate and no staleness state to manage;
- the index is **never committed** — a generated artifact in git would
  become a second source of truth the moment the two disagreed;
- nothing in this machinery writes markdown, and nothing **ever** checks
  a checkbox. STATUS.md stays human-owned (ROADMAP.md Part A, rule A4):
  Remedy reads it and may PROPOSE a diff in a job's changes, but the
  merge is the human act.

## Grammar is the only hard failure

The feature files' header conventions are the parse anchors:

```
# T1_F080 — Machine-readable roadmap mirror & STATUS.md
**Tier 1 · Depends on: F070 · Blocks/used by: F248**
```

and STATUS.md's line grammar is the one in ROADMAP.md Part C:
`- [<glyph>] F<id> — <title>`, with `[ ]` todo, `[~]` in progress,
`[x]` done, `[!]` blocked.

A violation raises `RoadmapGrammarError`, which carries **every**
violation found in one pass, each rendered as `<file>:<line>: <what>` so
a fix round is mechanical:

```
docs/roadmap/features/T0_F002.md:1: missing title line: expected '# T<tier>_F<id> — <title>'
docs/roadmap/STATUS.md:9: unknown status glyph '?' — expected one of [' ', '!', 'x', '~']
```

Violation classes: missing or mismatched title line, malformed or
unclosed dependency line, tier disagreement between the two, duplicate
feature id, unknown status glyph, a STATUS list item that is not a
checkbox line, and a feature listed twice in STATUS.

**Consistency findings are not failures.** Three classes are REPORTED
and never fatal — a STATUS entry whose feature file is missing
(`status_without_file`), a feature file absent from STATUS
(`file_without_status`, i.e. not scheduled), and a dependency reference
to an unknown id (`unknown_dependency`). They ride in the index and show
up in `remedy plan status`.

## `remedy plan status` / `remedy plan next`

Both verbs are read-only. They **propose and never start**: no job, no
run, no markdown write — the only thing they write is the generated
index under the data root.

```bash
remedy plan status [--repo <path>] [--json]
remedy plan next   [--repo <path>] [--json]
```

Both follow STATUS **Rule A5**: an in-progress `[~]` line is the active
feature and is reported as such; otherwise the first `[ ]` line is next.

`plan status` — the active feature, its blockers with their states, the
milestone it serves, the roadmap size, the consistency report, and where
the mirror was written:

```
Active: F080 — Machine-readable roadmap mirror & STATUS.md  [in_progress]
  File: docs/roadmap/features/T1_F080.md
  Milestone: M2 — It builds itself (Tier 1)
  Blockers:
    F070 — Orchestrator loop inside Remedy  [done]
Next unchecked: F103 — Token ledger (SQLite)
Roadmap: 255 features · 255 scheduled in STATUS
Consistency: no findings
Mirror: <data_root>/roadmap/index.json (generated, never committed)
```

`plan next` — the proposal alone, with the file to read and the STATUS
line it came from:

```
F080 — Machine-readable roadmap mirror & STATUS.md
File: docs/roadmap/features/T1_F080.md
State: in progress (Rule A5: the active line) · docs/roadmap/STATUS.md:48
Proposal only — nothing was started.
```

Exit codes: `0` normal, `2` roadmap grammar violations (the list goes to
stderr).

## From a feature file to a prepared mission

`packages/orchestration/feature_mission_adapter.py` turns a detail file
into a mission draft the existing machinery understands:

| Feature-file section | Becomes |
|---|---|
| "How it fits" / "Context" / "Goal & Done" | mission context input (`JobIntake`) |
| "Task slicing" | plan seed (`FlightPlan` tasks + milestone draft) |
| "Acceptance" | DoD compiler input (acceptance lines) |
| "Do not touch" | fences (deny globs + prose notes) |

Every seeded part records the heading and line it came from, so any
element of the draft traces back to the sentence that produced it.

The adapter **prepares and never executes**: the result carries
`approval_required=True` / `started=False`, no job or run is created,
and persisting the draft to
`<data_root>/roadmap/missions/<feature_id>.json` is a separate explicit
call. Approval stays on the standard human path. A file that breaks the
roadmap grammar is refused — the adapter compiles only a roadmap the
parser trusts.

## Where the code lives

| Path | Role |
|---|---|
| `packages/orchestration/roadmap_index.py` | parser, grammar validation, consistency checks, index writer |
| `packages/orchestration/feature_mission_adapter.py` | feature file → prepared mission draft |
| `apps/cli/commands/plan_cmd.py` | the two CLI verbs |
| `tests/orchestration/test_roadmap_index.py` | this repo as fixture + one fixture per violation class |
| `tests/orchestration/test_feature_mission_adapter.py` | mapping, real-file end to end, no side effects |
| `tests/cli/test_plan_cli.py` | CLI surface + the no-side-effects assertions |

Related: [orchestrator-loop.md](orchestrator-loop.md) for what consumes
a mission, [proof-chain.md](proof-chain.md) for how the resulting work
is proven.
