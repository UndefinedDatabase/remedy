
DECISION F278 D4 (2026-09-23, round 5) — T003's SHAPE: NARROW WHAT CAN BE NARROWED, RECORD WHAT
IS LOST, EXCUSE THE REST BY NAME, AND TURN THE RULE ON ONLY WHEN THE COUNT IS ZERO.

CONTEXT. Measured at `924f7dd6` with `ruff check --select BLE001` over `packages/`, `apps/` and
`scripts/`: 268 unmarked blind-exception handlers in 55 files, and 35 already carrying
`# noqa: BLE001`, three of those with no reason. `stream_evidence.py` holds 11 of the 268, not the
nine T2_F278.md counted on 2026-09-08. DECISION amend0911-feedback D7 rules that `ruff check .`
reports ZERO findings and that there is no lint baseline and no lint ceiling; the CI `budgets`
stage fails on any finding.

CHOSEN. (1) STREAM EVIDENCE FIRST, this round. A handler whose call raises one known exception for
an expected reason is NARROWED to it — `OSError` for signalling or closing a process that is
already gone, `subprocess.TimeoutExpired` for a wait — so anything unexpected propagates. A step
whose failure makes the evidence incomplete is RECORDED: `StreamCaptureResult` gains
`degradations`, a list of `{"step", "error_type"}` entries, in `to_dict` and as `stream_degraded`
events in `run_events.jsonl`, continuing its `seq`. The exception's message is not kept, because an
OS error can carry an absolute path into packaged evidence. The one handler around an arbitrary
callback keeps `except Exception` with a noqa reason. (2) THE REST, module group by module group,
in the rounds that follow: each handler is read and either narrowed or marked
`# noqa: BLE001 — <reason>`, the reason saying why swallowing or converting is correct there.
Marking before the rule is on changes no behaviour and no lint result. (3) THE RULE GOES ON LAST.
`BLE001` joins `select` in `pyproject.toml` only in the commit whose tree has zero unmarked sites,
so `ruff check .` never reports a finding and D7 holds at every commit. (4) THE RATCHET lands with
it: a test that counts every `noqa: BLE001` under `packages/`, `apps/` and `scripts/`, requires a
reason after a dash on each, and fails if the count exceeds the number measured in that commit. It
is a ceiling on EXCUSED handlers, not a lint baseline: ruff's own finding count stays zero, which
is the only count D7 speaks about.

ALTERNATIVES. Turn the rule on now with a per-file ignore list — rejected: a per-file ignore
silences every future handler in those files too, which is the opposite of a ratchet. Turn it on
with 268 findings — rejected by D7. A generic reason pasted onto every site — rejected: a reason
nobody checked is a label, and T2_F278.md asks for the reason.

REVERSE by deleting this paragraph; `stream_evidence.py`'s change reverses from git history at
`924f7dd6`.
