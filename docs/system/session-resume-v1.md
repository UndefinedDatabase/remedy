# Session Resume v1

> Built state of F106 (`docs/roadmap/features/T3_F106.md`, Tier 3). A repair
> round stops resending the world: where the provider supports resuming a
> session, the round resumes it and sends only the findings delta, with an
> honest automatic fallback to full context whenever the session is gone or
> the shrink produces nothing. Correctness never depends on resume working.

## Capability surface (T001)

Every concrete provider adapter in `packages/orchestration/pingpong_provider.py`
exposes a `supports_resume: bool` property and accepts an additive
`resume: str | None = None` keyword on both `build` and `review`. `FakeProvider`
takes it as a constructor override (`supports_resume=True`, test-only);
`ClaudeCliProvider` reads `True` since F287 (DECISION F287 D4); `ClaudeProvider`
and `OllamaPingPongProvider` read `False` and say why in a
`resume_unsupported_reason` property. `BuilderOutput`/`ReviewerOutput` default
`resume_used`/`resume_session_ref` to `False`/`""`; passing `resume=` to an
adapter that does not support it changes nothing observable.

## Repair-round resume threading (T002a, T002b-i)

A repair round's PRIMARY Builder call and PRIMARY Reviewer call each resume
the prior round's own session, gated on the SAME three-way check: the round
is a repair, the provider honestly advertises `supports_resume`, and a prior
session id was actually captured (`usage_actuals["session_id"]` on the PRIOR
round's own output). Every other path — the initial round, an unsupported
provider, no prior session id — passes `resume=None`, an honest no-op, never
guessed. The reviewer's bounded parse-retry call (a separate call within the
same round, for recovering from malformed JSON) is NOT threaded: it always
sends full context.

## Fallback-once (T002c)

A resume attempt that errors falls back ONCE, same round, to `resume=None` —
recorded on `BuilderOutput.resume_fallback` / `ReviewerOutput.resume_fallback`,
gated strictly on a resume having actually been attempted, so a plain call
failure with no resume in play is unaffected. Fallback is a normal, evidenced
event, never a task failure by itself.

## Delta-prompt shrink (T002b-ii, DECISION F106 D1(b))

When a round is actually resuming AND there is a repair diff to shrink,
`compose_builder_prompt`/`compose_reviewer_prompt` (`packages/orchestration/pingpong_loop.py`)
take a `resume_hunks_text` parameter that replaces the diff-shaped segment —
`builder_staged_diff` on the Builder side, `reviewer_focused_diff` /
`reviewer_staged_diff` (whichever of the Reviewer's two mutually exclusive
branches would otherwise fire) on the Reviewer side — with the SAME segment
name and rank each branch already uses; only the text filling it changes. An
empty render (nothing survived selection) falls through to the unconditional
full-diff path, so the shrink is additive and honest by construction.

The render itself reuses `packages/orchestration/diff_repair.py`'s
`select_repair_hunks`/`render_repair_hunks` — the same module
[diff-only-repair-v1.md](diff-only-repair-v1.md) built for F111 — but for a
DIFFERENT purpose: shrinking the PROMPT sent to an already-resumed session,
never applying a patch. DECISION F111 D1 (`pingpong_loop.py` has no
diff-apply seam; its Builder is an agentic CLI that edits staging itself) is
untouched — this feature never routes through `diff_repair_response.py` or
`diff_repair_apply.py`, only through the pure hunk-selection half of the
module. The Builder side caps the selection at `_REPAIR_DIFF_CAP` (20000
chars); the Reviewer side at `_REVIEWER_DIFF_CAP` (30000 chars) — the SAME
caps each branch's own full-diff path already used.

## Measured reduction (T003)

`tests/orchestration/test_session_resume.py::TestT003MeasuredTokenReduction`
runs the same two-round repair fixture twice — once with a
`supports_resume=True` `FakeProvider`, once with `supports_resume=False` —
against the identical 3-file demo repo, and compares
`PreparedCallInput.prompt_len_bytes` (`packages/orchestration/call_identity.py`)
on round 2's Builder and Reviewer outputs: the exact UTF-8 byte count of the
prompt actually sent, already recorded via `prepared_input` on every call — no
new measurement surface. Measured at commit `177dada423ea1c3b1e440c9a29e44f9ffbd2918f` (`pytest
tests/orchestration/test_session_resume.py -k T003MeasuredTokenReduction -s`):

| Call | Resumed (bytes) | Full context (bytes) | Reduction |
|------|-----------------:|----------------------:|----------:|
| Builder round 2  | 1331 | 1384 | 53 bytes (~3.8%) |
| Reviewer round 2 | 2208 | 2270 | 62 bytes (~2.7%) |

Both reductions are small in absolute terms on this tiny fixture — the
mechanism scopes the sent diff to the changed regions rather than
re-sending every file's full diff, and the saving scales with how much of
the world a real repair round would otherwise resend, not with this
fixture's own size. The comparison exists to prove the DIRECTION is real and
measured, per the feature's own acceptance criterion, not to claim a
production magnitude.

## Resume across a relaunch (R-1055, F285 T003)

A park or a stop returns the interrupted task to `pending`, and its relaunch
starts a new run. Every round's `builder` and `reviewer` blocks in a run's
`result.json` now carry `session_id` (the session the call reported),
`resume_used`, `resume_session_ref` and `resume_fallback`. When `run_job`
reaches a task whose `final_status` is `stopped` and whose `run_id` still
names the parked run, it reads that record with `parked_session_refs` in
`packages/orchestration/pingpong_loop.py` and passes the result to
`run_pingpong` as `resume_sessions`. Round 1's call of each role then resumes
the parked session when its provider supports resume, with the fallback-once
rule unchanged, and the new run's record names the parked run as
`resumed_from_run_id`. The prompt of that call stays full-context: the parked
session never saw the new run's staging, so no prompt shrink is gated on it.
`tests/orchestration/test_relaunch_session_resume.py` parks a job mid-build
and relaunches it through `run_job`.

## Which providers resume (F287)

`claude-cli` is the one production provider that resumes. Its builder and
reviewer calls pass the CLI's `--resume <session>` option, in a repair round
and in round 1 of a relaunch; the session reference is checked against a plain
session-id shape before it reaches the child's argument list, and a refused
resume answers `resume_refused:`, which is never transport-retried, so the
fallback-once rule above runs on the first failure (DECISIONS F287 D2 to D4).

The `claude` CLI keeps a session under the directory it ran in. A job on a git
target runs in its own worktree, and its relaunch runs in that same worktree,
so the parked session is found. A job on a target that is not a git repository
(copy mode) gets a new staging directory for every run, so its relaunch's
resume is always refused and falls back once to a fresh session at full
context; that costs one short child process and no tokens (DECISION F287 D5).

The Anthropic API provider (`claude`) and the Ollama provider (`ollama`) keep
no conversation between calls and never resume. When a relaunch offers one of
them a parked session, the run proceeds with a fresh session and its
`result.json` names the role and the reason under `resume_declined`, for
example `{"builder": "an Ollama chat call keeps no conversation between
calls"}`; a run that was offered nothing records an empty object there
(DECISION F287 D7).

## What this does NOT do

- Only `claude-cli` resumes in production; the Anthropic API and Ollama
  providers start every call fresh.
- The reviewer's bounded parse-retry call never resumes.
- New-file creation, deletion, and any diff-APPLY path stay entirely outside
  this feature — see [diff-only-repair-v1.md](diff-only-repair-v1.md) for
  the (separate) apply-side mechanism `pingpong_loop.py` deliberately does
  not use.

## Related

- `docs/roadmap/features/T3_F106.md` — the target spec and its decisions.
- `docs/roadmap/features/T3_F287.md` — the provider session continuity the
  "Which providers resume" section describes.
- [diff-only-repair-v1.md](diff-only-repair-v1.md) — the module this
  feature's hunk selection is shared with, and the apply-side path it does
  NOT route through.
