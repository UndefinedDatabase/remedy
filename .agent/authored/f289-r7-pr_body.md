## What

F289 — Self-use sources completion. The self-use generator, which gives a feature's closure one
item of Remedy's own maintenance to run, had two honest `None` sources after the finding ledger and
the standing order. Both are built now.

- **Tier 2, the documentation-staleness catalog** (`packages/orchestration/doc_staleness.py`):
  twelve checks compare what the README, the docs index, the guides and the command catalog claim
  with what ships — guides listed in both index tables, the `remedy.toml` guide's CLI table against
  the `config` group, index command lines, guide links and link fragments, `REMEDY_` names, config
  keys, TOML example keys, the index's category column, source paths, dotted command ids, and the
  config keys the catalog's own texts name. Each check reads documents under a root against an
  injectable `ShippedTruth`, so each is proven red on a stale fixture. The first claim no queue entry
  targets becomes a one-task job that edits the document, never the code.
- **Tier 3, `doctor core` as data** (`apps/cli/commands/worker_facade_cmd.py`):
  `doctor_core_report()` returns a `DoctorCoreReport` of structured `DoctorWarning`s, and the command
  prints from it with its text and JSON output byte-identical. A warning is actionable when a tracked
  file of this repository is its repair — today a dead built-in model, repaired in
  `packages/orchestration/model_aliases.py` — and the first untargeted one becomes a one-task job.
- **R-1073**: the diff parser's timing test asserts a machine-independent scale ratio instead of an
  absolute 0.5 s ceiling that a slower hosted runner crossed twice.

## Why

A closure's self-use run needs work when the ledger is empty; F027's closure ended "queue
exhausted". F289's own closure is the proof: its item came from Tier 2 and was repaired by Remedy.

## Key decisions (in `.agent/decisions.md`)

- F289 D1 — the report beside its command, structured warnings, what "actionable" means, Tier 3.
- F289 D2 — the twelve checks, the injectable truth, Tier 2's job that repairs the document.
- F289 D3 — the proof: three closures on an empty ledger, the first item run to completion.

## How to review

Start with `packages/orchestration/doc_staleness.py`, then `_doc_staleness_tier` and
`_doctor_warning_tier` in `packages/orchestration/self_use_generator.py`, then `doctor_core_report`
in `apps/cli/commands/worker_facade_cmd.py`. The Built State of `docs/roadmap/features/T5_F289.md`
names the test for each acceptance line; each round's mutation tool is
`.agent/authored/f289-r<n>-mutations.py`, and `.agent/authored/f289-r1-parity.py` proves the
command's output unchanged.

## Verification

- The one full suite on the tree that ships: `19754 passed, 20 skipped` at exit 0, no bad node
  (`.agent/authored/f289-closure-suite.txt`).
- `TestThreeConsecutiveItemsOnAnEmptyLedger`: three closures on an empty ledger produce three
  distinct items, and the first runs through the real `run_job` to `completed` inside the default
  6.00 USD budget.
- The closure's self-use item `SU-033`, from Tier 2: job `da4583bff80a47f1` on `claude-cli` added the
  missing Quick-Find row to `docs/README.md` in 2 calls for 0.56 USD, its reviewer passed it, and the
  one line landed verbatim.
- Evidence job `f289r6e1001` against the fork point `d0239fa3`: 634 selected tests passed at exit 0.
- Review package `remedy-review-20260926-225640-READY_FOR_REVIEW.zip`, SHA-256
  `7044a4959459a9144a0b3030453ed74944ab4edad8125fd67c2eb2e6cc488a62`, READY_FOR_REVIEW.

## Findings and notes

Latest verdict PASS; accepted PASS. F289 registered R-1073 and R-1074 and resolved both. No finding
is open. One stale claim stays on the real tree for the next closure's self-use run: the
`remedy.toml` guide does not document `remedy config show`. The self-use job left the branch
`remedy/job-da4583bff80a47f1`, which the operator may delete.

## Runtime actuals

Seven rounds in one session, from the branch's first commit at 19:23 to the accepted head at 22:52
on 2026-09-26; reviewer and workers ran as Claude Opus 5.5; the self-use run cost 0.56 USD; other
tokens not measured.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
