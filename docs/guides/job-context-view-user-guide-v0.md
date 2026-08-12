# Compiled task context — user guide (v0)

`remedy job context` shows what ONE task of a job would actually receive as its file
context, and what the context compiler left out and why. It is a read-only view: it
compiles the context in memory, prints it, and writes nothing — no evidence file, no
job state, no cache. Nothing is sent to a provider.

```
remedy job context <job-id> --task <task-ref> [--json]
```

`<job-id>` may be any prefix a job id resolves by, the same way the other `remedy job`
commands accept one.

## What is compiled, and what is deliberately not

The fenced scope is exactly the task's own `inputs["flight"]["files_hint"]` — the write
scope the flight plan gave that task. Remedy deliberately does NOT consult the job's
scope-fence globs (`remedy job fences`, F017) here: merging fence allow-globs into the
compiled scope is out of scope for this version, so a view that showed them would be
showing something the compiler never used. A task with no `files_hint` has an EMPTY
scope; that is a real answer the view prints, not an error.

Around that scope the compiler assigns every candidate file a tier:

| Tier | What it is | How it is rendered |
|------|------------|--------------------|
| 1 | the fenced files themselves | full text |
| 2 | files the fenced files import directly | full text (signatures if too large) |
| 3 | dependencies one hop further out | signatures only |
| 4 | everything else | omitted, with a reason |

Selection stops at two graph hops. Every candidate path appears exactly once, either
under `Included` or under `Omissions` with a reason (`distance`, `budget`, `size`,
`binary`) — so "why did the task not see file X" always has a written answer.

## How `--task` resolves

The reference is matched against the planned id first (`T001`, as written by the flight
plan), and only then as a prefix of the task's UUID. A reference that matches nothing,
an ambiguous UUID prefix, and a job with several tasks and no `--task` are all errors.
The command never guesses a task. If the job has exactly one task, `--task` may be
omitted.

## Where the candidate list comes from

The compiler does not walk the repository itself; the command produces the candidate
listing for it, in one of two branches, and the output NAMES the one that ran:

- `git ls-files` — used when the target repo is a git checkout, so the listing already
  honours `.gitignore` and the index;
- `filesystem walk` — the fallback when it is not a checkout or when git fails. It walks
  the tree and skips `.git`, `__pycache__`, `node_modules`, `.venv` and `dist`.

Both branches return a sorted, deduplicated list, so the same repository always compiles
to the same view.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | compiled and rendered |
| 1 | unknown job |
| 2 | the job has no usable `target_repo` (missing, or the path does not exist) |
| 3 | the task could not be resolved — unknown, ambiguous, or several tasks and no `--task` |

Errors go to stderr and name only what was actually found:

```
$ remedy job context 994eb8d1-5ce5-4fd8-a150-2121bf391d07 --task T999
Error: no task matches --task 'T999'
$ echo $?
3
```

## A real run

Against a five-file demo checkout whose `src/payment_gateway.py` imports
`src/retry_policy.py`, which in turn imports `src/clock_source.py`, while `README.md`
and `src/invoice_report.py` are imported by nothing:

```
$ remedy job context 994eb8d1-5ce5-4fd8-a150-2121bf391d07 --task T001
Task context for job 994eb8d1 task T001 (52c783f1)
  Fenced paths (1):
    src/payment_gateway.py
  Candidates: 5 (git ls-files)
  Budget: 164 / 24000 tokens
  Included (3):
    Tier 1:
      src/payment_gateway.py  full  73 tokens
    Tier 2:
      src/retry_policy.py  full  63 tokens
    Tier 3:
      src/clock_source.py  signatures  28 tokens
  Omissions (2):
    README.md  tier 4  distance  omitted
    src/invoice_report.py  tier 4  distance  omitted
```

Read it as: the task's own file arrives whole, the file it imports arrives whole, the
file behind that one arrives as signatures only, and the two files nothing imports do
not arrive at all. `Budget` is the estimated cost of the compiled context against the
token budget it was compiled under. It gains `(OVER BUDGET)` only after every demotion
and omission phase is exhausted and the fenced files alone still exceed the budget: the
compiler reports the overflow instead of cutting the files the task must edit.

## `--json`

`--json` prints the same values as one object, and nothing else. Fields:

| Field | Meaning |
|-------|---------|
| `job_id`, `task_id` | the full UUIDs |
| `task_label` | the planned id (`T001`), or the first 8 hex of the task UUID |
| `fenced_paths` | the task's `files_hint`, as compiled |
| `candidate_count` | how many files were offered to the compiler |
| `candidate_source` | `git ls-files` or `filesystem walk` |
| `estimated_tokens` | the compiled context's estimated cost |
| `budget_tokens` | the budget it was compiled under |
| `over_budget` | whether the estimate exceeds that budget |
| `line_cap` | the per-file line cap the signature rendering used |
| `included[]` | `path`, `tier`, `rendering` (`full` / `signatures`), `estimated_tokens` |
| `omissions[]` | `path`, `tier`, `reason`, `outcome` |

The same run as above:

```json
{
  "job_id": "994eb8d1-5ce5-4fd8-a150-2121bf391d07",
  "task_id": "52c783f1-815a-4bfb-a307-d2335de3e18e",
  "task_label": "T001",
  "fenced_paths": [
    "src/payment_gateway.py"
  ],
  "candidate_count": 5,
  "candidate_source": "git ls-files",
  "estimated_tokens": 164,
  "budget_tokens": 24000,
  "over_budget": false,
  "line_cap": 200,
  "included": [
    {
      "path": "src/payment_gateway.py",
      "tier": 1,
      "rendering": "full",
      "estimated_tokens": 73
    },
    {
      "path": "src/retry_policy.py",
      "tier": 2,
      "rendering": "full",
      "estimated_tokens": 63
    },
    {
      "path": "src/clock_source.py",
      "tier": 3,
      "rendering": "signatures",
      "estimated_tokens": 28
    }
  ],
  "omissions": [
    {
      "path": "README.md",
      "tier": 4,
      "reason": "distance",
      "outcome": "omitted"
    },
    {
      "path": "src/invoice_report.py",
      "tier": 4,
      "reason": "distance",
      "outcome": "omitted"
    }
  ]
}
```

## Related

- `remedy job fences` — the job's scope fence, which this view intentionally ignores.
- `remedy job show` — the job and its tasks.
- The compiler itself: `packages/orchestration/context_compiler.py`; the feature brief is
  [T2_F107.md](../roadmap/features/T2_F107.md).
