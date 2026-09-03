# Semantic Dedupe v1

> Built state of F109 (`docs/roadmap/features/T3_F109.md`, Tier 3). Inside a
> RESUMED provider session, a prompt segment whose exact content has already
> provably reached that session is replaced by a one-line marker instead of
> being sent again; everywhere else the full content is composed unchanged.
> The scope rule of the whole feature binds every mechanism below:
> RESUMED SESSION ONLY, PROVEN SENDS ONLY.

## The sent-hash index (T001)

`packages/orchestration/session_sent_index.py` holds `SessionSentIndex`: per
provider session id, the set of segment SHA-256 digests PROVABLY delivered. The
digests are the ones `ComposedPrompt.manifest_as_dicts()` already produces — no
second hashing scheme — and the module is PURE: no file, no network, no
provider, no import from the rest of `packages.orchestration`. "Proven" is the
load-bearing word: `record_call` records nothing when the call carried an error,
because a failed call did not reach the session, and nothing when the session id
is empty after stripping, because an empty key would become one bucket every
sessionless call shares. Neither case is an error and both are silent; a
malformed manifest row, by contrast, RAISES `SessionSentIndexError` rather than
degrading quietly into a smaller index.

`record_finalized_call` and `invalidate_on_resume_fallback` are the two adapter
seams. `pingpong_loop.py` calls both on the Builder path and again on the
Reviewer path (landed at `7451e9c7`), and writes `as_evidence_dicts()` onto
`result.session_sent_evidence`, so `session_sent_index_from_evidence` rebuilds
after a restart exactly what the evidence proves and never more.

## The composition hook and the marker (T002)

`_dedupe_resumed_segments` in `packages/orchestration/pingpong_loop.py` is the
transform. It rewrites `text` and nothing else, so segment NAMES and RANKS
survive by construction, and it returns the INPUT order rather than a rank sort —
`compose_prompt_segments` sorts afterwards, and re-ordering here would move
segments the cache discipline requires to stay put. The digest it compares comes
from the shipped producer one segment at a time, never from a local `hashlib`
call, so the decision asks the same producer that made the index's entries.

The marker reads `[unchanged: <segment name>, previously provided]`. The name
stays inside it deliberately: the model must still be able to refer to a segment
it is no longer shown, so the marker withholds the content without withholding
the means of asking for it back.

Both `compose_builder_prompt` and `compose_reviewer_prompt` take a
`dedupe_sent_hashes` parameter that BYPASSES dedupe by default (`60343048`), so
the transform runs only for a caller supplying a real set; a non-resuming call
passes `None`, which is the scope rule and not a gap. A segment shorter than
`DEDUPE_MIN_SEGMENT_CHARS` (200, compared with `>=`) is never replaced, because
a marker has a length of its own — 48 and 49 characters for the two names
measured below — so replacing a small segment can cost more than it saves.

## The kill switch (T002c)

`run_pingpong` carries `semantic_dedupe_enabled` and forwards it to both primary
compositions as `dedupe_enabled` (`b245e1c9`). In `should_dedupe_segment` and in
`_dedupe_resumed_segments` alike, `enabled` is consulted FIRST and ALONE: false
returns the segments untouched and consults nothing else, so the switch is
provably and totally off rather than mostly off.

## What the record shows, and what it measures (T003c, T003d)

Every `PromptTraceEntry` carries `deduped_segment_names`, derived from the
composed prompt alone rather than passed in beside it, so the evidence shows
exactly which segments the model did NOT receive again.

`measure_dedupe_savings_from_traces` in `packages/orchestration/prompt_trace.py`
reads a run's own trace entries and reports what that run did not resend. Every
number it returns is MEASURED from recorded evidence. It is deliberately NOT
`estimate_token_savings` in `packages/orchestration/token_economy.py`: that
function compares two ESTIMATES and says so, and one name over both concepts
would make a measured number indistinguishable from a guess.
`unmeasured_segment_names` is the load-bearing field — a segment reported as
deduped whose full-content size never appeared in the entries handed over is
NAMED there and excluded from every total, so "nothing was saved" and "the
saving is not measurable from what you gave me" can never read alike.

Measured at commit `d52a5371` on the two-round resumed fixture chain of
`tests/orchestration/test_semantic_dedupe.py::TestTheRunsOwnTraceMeasuresWhatItWithheld`,
whose second case re-runs the identical chain with `semantic_dedupe_enabled=False`
as the discriminator:

| Reading | Dedupe on | Dedupe off |
|---|---:|---:|
| Segments withheld | 2 (`builder_system`, `reviewer_system`) | 0 |
| Characters avoided | 556 | 0 |
| Characters spent on markers | 97 | 0 |
| Net characters saved | 459 | 0 |
| Names that could not be measured | none | none |

The two markers cost 97 characters against 556 of withheld content. As with
F106's measured reduction, this comparison proves the DIRECTION is real and
measured on a small fixture; it is not a claim about production magnitude, and
the saving scales with how much of the world a real resumed round would
otherwise resend rather than with this fixture's own size.

## What this does NOT do

- **Nothing dedupes in production today.** Dedupe fires only inside a resumed
  session, and every concrete adapter in
  `packages/orchestration/pingpong_provider.py` returns
  `supports_resume = False` — `ClaudeProvider`, `ClaudeCliProvider` and
  `OllamaPingPongProvider` alike. Only `FakeProvider`'s test-only constructor
  override ever returns `True`, so the mechanism is exercised by the suite and
  is inert on every real run.
- A dedupe never crosses session ids: each session's hashes live in their own
  set, and an empty session id is never used as a key.
- A resume fallback forgets the resumed session entirely — once it has fallen
  back to full context, nothing about what the model holds is proven.
- The measurement function is a LIBRARY. The T003 fixture above is its only
  caller; `run_pingpong` does not call it and no report renders it yet. A run's
  savings stay recomputable from the traces the run already wrote.
- Cross-session caching, provider-side cache mechanics and prompt CONTENT are
  out of scope — the feature file's own "Do not touch".

## Related

- `docs/roadmap/features/T3_F109.md` — the target spec and its acceptance list.
- [session-resume-v1.md](session-resume-v1.md) — the resume machinery this
  feature's scope rule depends on, and the reason nothing dedupes in production.
- [cache-optimal-prompt-ordering-v1.md](cache-optimal-prompt-ordering-v1.md) —
  the ranked segment composition that dedupe rewrites one segment of.
