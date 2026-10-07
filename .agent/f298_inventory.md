# F298 claim inventory — what a machine client meets at `77493e0f9`

Measured by the reviewer of F298's first session on 2026-10-07, on `main` at `77493e0f9`, with
the script `.agent/authored/f298-r1-measure.py` (run as `python3 -B <script> <primary checkout>
<scratch folder>`): scratch git repositories `a` (with a local bare upstream), `b` and `c`, a folder
`plain` that is no repository, and a scratch data root set through `REMEDY_DATA_DIR`. Every command
ran as `python3 -m apps.cli.main ...` with the fake builder and reviewer, `--no-llm`, `--no-ui` and
`--yes`, and an order file whose header carries `max-cost-usd: 1` and whose text reads "Add a line
saying hello to README.md". DECISION F298 D1 turns these readings into the slice order.

The scratch folder lies inside the primary checkout, so the `plain` probe runs with
`GIT_CEILING_DIRECTORIES` set to the scratch folder. A first attempt without it let git climb to
the primary checkout: the order registered that checkout as a project on the scratch data root and
ran a fake job against it, stopping before apply. No file of the checkout changed; the job's local
branch `remedy/job-b14f7592d5234480` was left behind. That attempt is itself a reading for T002:
a client standing in any folder below a repository changes that repository.

## Where an order runs (T002)
- In `plain`: exit 1, `error` `step_failed`; the init step fails with "is not a git repository —
  run `git init` first".
- In `b`, a `--plan-only` order registers `b` as project `b`.
- In `a`, an order file whose header names `project: b`: exit 0; the init step reads "project b
  (...) selected by --project"; the job's record holds project b's id and `repo_path` `a`, and the
  `next` lines name `remedy job apply <job> --repo <a> --approve`. The `project` key chooses where
  records are filed, never where the work happens.

## A blocked apply (T003)
- A full fake run in `a` answers `unmet_blocking_criteria` `["C001"]`.
- `remedy job apply <job> --approve --commit-with-history --push --json`: exit 0, `"ok": true`,
  `"status": "blocked"`, `error` absent, `blocked_reason` "push_refused: The mission's blocking
  contract criteria C001 are unmet, so nothing is pushed." Neither `a`'s HEAD nor its upstream
  moved, and `a`'s working tree stayed clean. The answer carries 49 keys, among them
  `commit_sha`, `target_branch`, `pushed`, `push_error` and `blocked_reasons`.

## Declining, and an abandoned mission (T003)
- The command catalog holds no `decline` subcommand; its one `reject` subcommand is not a job's.
- After `remedy mission abandon <mission> --json` (exit 0), the mission's completed job still reads
  `waits_for_apply` true and stands in `awaiting_apply`.

## Two jobs, and one order file twice (T004)
- `--force-mission`: exit 0, `job_ids` two, `waiting_job_ids` the second; the last `next` line
  reads "commit job <first>'s applied output in <a>, then: remedy job run <second> ...", a
  sentence for a person.
- Two `--plan-only` starts of one order file: both exit 0 and make two distinct missions.

## What a client can read (T001, T005, T006)
- Digest top-level keys: `awaiting_apply`, `decisions`, `degraded`, `jobs`, `projects`, `read_at`,
  `skipped_files`, `supervisor`, `version`. A digest job: `cost`, `evidence`, `job_id`,
  `mission_id`, `project_id`, `state`, `title`, `waits_for_apply`. A digest project:
  `cost_today`, `missions`, `project_id`, `slug`. The page names none of `title`, `slug`,
  `cost_today`, `supervisor`, `read_at`, `degraded` or `skipped_files`.
- A digest job's `cost` is `basis` and `value_usd` only, no token and no call.
- `final_job_review.json` of the completed job reads `verdict` `PASS` with no acceptance criteria
  in it, while the mission's `C001` is unmet; the job record's `test_passed` and `test_command` are
  null, and the record has no key naming tokens or calls.
- Read in `packages/orchestration/pingpong_job.py`: the job's `total_tokens` adds input and output
  tokens, cache tokens excluded. The fake provider reports no tokens, so this is read, not
  measured.
- The order header's keys are `project`, `contract`, `max-cost-usd` and `constraint`: one cap,
  in USD.

## Templates and registering (T002, T007)
- Contract templates: `api-service`, `cli-tool`, `python-library`, `website`. An order file
  naming `contract: small-change` exits 2 with `unsupported_contract_template`.
- `remedy init --json` in a clean repository `c`: exit 0, and `git status` then lists
  `.remedy/config.toml` and `remedy.toml` as untracked.

## The digest's size (T007)
- Scratch root: 7 jobs, 3 awaiting an apply, `client` object 7,249 bytes.
- The same root with 1,000 copies of the completed job's record added: 1,007 jobs, 1,003 awaiting
  an apply, 514,249 bytes, about 507 bytes for each added job, `degraded` false.
- The operator's own data root, read with `remedy status --json`: 11,652 jobs (8,058 planned,
  2,020 blocked, 1,122 completed, 450 stopped, one pending, one running), 1,122 awaiting an apply,
  13,480 open decisions, and a `client` object of 8,622,726 bytes.
