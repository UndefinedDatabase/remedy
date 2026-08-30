# F106 Inventory — Session resume shape measurement

Round 1 measurement, SESSION 1. Every claim below was verified against the
repository at commit `b33f5c4d` (this branch, after C4) by reading the cited
file or running the cited command myself — none is transcribed from the
block's own hypotheses without checking. Where a citation resolved exactly
as the block stated, that is recorded as CONFIRMED. Where it drifted, the
corrected citation is given instead.

## 1. The provider protocol and its concrete adapters

CONFIRMED. `packages/orchestration/pingpong_provider.py:132` is exactly:

    class PingPongProvider(Protocol):
        """Protocol for Builder/Reviewer providers."""

        @property
        def name(self) -> str: ...

        def build(
            self,
            prompt: str,
            *,
            timeout_sec: int = 120,
            max_output_chars: int = 50000,
        ) -> BuilderOutput: ...

        def review(
            self,
            prompt: str,
            *,
            timeout_sec: int = 120,
            max_output_chars: int = 50000,
        ) -> ReviewerOutput: ...

Command: `Read packages/orchestration/pingpong_provider.py` lines 100-300.

Three concrete adapters, each with its class line and `build`/`review`
signatures (all three match the Protocol's shape exactly — same keyword
params, same defaults):

- `FakeProvider` — `packages/orchestration/pingpong_provider.py:159`.
  `build` at line 194, `review` at line 221 (each delegates to
  `_review_impl` at line 235 for the actual verdict logic). Both signatures:
  `def build(self, prompt: str, *, timeout_sec: int = 120, max_output_chars: int = 50000) -> BuilderOutput`
  and the equivalent for `review` returning `ReviewerOutput`.

- `ClaudeProvider` — `packages/orchestration/pingpong_provider.py:334`.
  `build` at line 395, `review` at line 436. Same signature shape as the
  Protocol (`prompt: str, *, timeout_sec: int = 120, max_output_chars: int
  = 50000`).

- `ClaudeCliProvider` — `packages/orchestration/pingpong_provider.py:865`.
  `build` at line 1326, `review` at line 1391. Same signature shape as the
  Protocol.

Command:
`python3 -c "import re; [print(i, l.rstrip()) for i, l in enumerate(open('packages/orchestration/pingpong_provider.py'), 1) if re.match(r'^class (ClaudeProvider|ClaudeCliProvider|FakeProvider)\\b', l) or re.match(r'^    def (build|review)\\(', l)]"`
— output: `138 def build(` / `146 def review(` (Protocol) / `159 class
FakeProvider:` / `194 def build(` / `221 def review(` / `334 class
ClaudeProvider:` / `395 def build(` / `436 def review(` / `865 class
ClaudeCliProvider:` / `1326 def build(` / `1391 def review(`.

## 2. The session-id field in call evidence

CONFIRMED, with the class name added since the block cited only the field.
`packages/orchestration/token_actuals.py:37` is exactly `session_id: str`,
a field of `@dataclass class UsageActuals` (class at line 16). The
docstring line describing it, at line 26:

    session_id:      CLI session identifier ("" if not reported).

Grep `session_id` in `packages/orchestration/pingpong_provider.py` —
command `grep -n "session_id" packages/orchestration/pingpong_provider.py`
— three matches, not one:

- Line 70: a comment, `# Measured provider usage
  (input/output/cache/cost/session_id/parse_source)` — inside
  `BuilderOutput`'s field block, not executable.
- Line 702: `"session_id": actuals.session_id,` inside the MODULE-LEVEL
  helper `_usage_actuals_dict()` (defined at line 692, not a method of any
  class). This helper has exactly one call site in the file — line 1278,
  `usage = _usage_actuals_dict(env.usage_actuals, cli_ver) if
  env.usage_actuals else None` — which sits inside `ClaudeCliProvider`
  (class starts at line 865, no other `class` line appears between 865 and
  1391). So this match is reachable only through `ClaudeCliProvider`.
- Line 1179: `"session_id": actuals.session_id,` directly inside
  `ClaudeCliProvider._call` (method starts at line 1121).

`ClaudeProvider` (lines 334-863) and `FakeProvider` (lines 159-297) have
zero `session_id` references between their class line and the next class
line. The claim "only `ClaudeCliProvider` populates it" is CONFIRMED, with
the correction that the field is referenced 3 times, not counted in the
block, and one of those three is a comment.

## 3. The call-entry signature — the additive target for `resume`

Already fully quoted in section 1 (the `Protocol.build`/`Protocol.review`
signatures at `packages/orchestration/pingpong_provider.py:138` and
`:146`). Cross-reference only, per the SPEC; not repeated verbatim here.

## 4. Capability-flag precedent elsewhere in the repo

CONFIRMED. `packages/orchestration/worker_registry.py:167` is exactly
`supports_external_builder_package: bool = False`, a field of `class
WorkerSpec` (class at line 148). The two NEIGHBORING `supports_*` fields
sit immediately below it, lines 168-169:

    supports_candidate_quality: bool = False
    supports_review_loop: bool = False

Grep for `supports_[a-z_]*: bool` across `packages/` and `apps/` — command
`grep -rn "supports_[a-z_]*: bool" packages apps` — 4 distinct files, 7
matches total:

- `packages/orchestration/worker_registry.py:167,168,169` (the three
  above).
- `packages/orchestration/model_route_tournament.py:144`
  (`supports_external_package: bool = False`) and `:145`
  (`supports_candidate_quality: bool = False`).
- `packages/orchestration/repair_request_builder.py:86`
  (`supports_execution: bool = False`).
- `apps/cli/command_catalog.py:83` (`supports_json: bool = False`).

## 5. The repair loop's call sites — locate only

DRIFTED from the block's implicit assumption of one call site each.
Confirmed `packages/orchestration/pingpong_loop.py` calls
`builder_provider.build(...)` and `reviewer_provider.review(...)`, but
`review` has two call sites, not one:

- `builder_provider.build(` — one call site, line 3014 (inside a
  `lambda ts=builder_timeout: ...`).
- `reviewer_provider.review(` — two call sites, lines 3227 and 3284 (both
  inside `lambda ts=reviewer_timeout: ...`).

Command: `grep -n "builder_provider\.build(\|reviewer_provider\.review("
packages/orchestration/pingpong_loop.py`, and `grep -c` for each pattern
individually to confirm the 1-vs-2 count (`pingpong_loop.py` is 4680 lines
total).

## 6. The diff-repair / delta mechanism

CONFIRMED. `docs/roadmap/STATUS.md` line 71 (F111's line, current on this
branch) reads exactly:

    - [x] F111 — Diff-only repair (T001–T003 complete; accepted 2026-08-13 · live review PASS_WITH_RISKS — ACCEPTED · Evidence job f111-closure · package remedy-review-20260813-060242-READY_FOR_REVIEW.zip · SHA-256 c44b4a12a5715a66bf3abd55633fc86a77351b0018fab930f374e707458d79e6 · accepted HEAD a2fe520bd16773e4f1536035caeec76e880bbdde)

Command: `grep -n "F111" docs/roadmap/STATUS.md`.

`packages/orchestration/diff_repair.py` exists (8190 bytes,
`ls -la packages/orchestration/diff_repair.py`). Its module docstring's
first line, line 1:

    Repair hunk selection for diff-only repair (F111 T001).

## 7. Test conventions for provider-adapter tests

CONFIRMED, with the exact file list. Files under `tests/orchestration/`
whose name contains `provider` or `pingpong` — command `ls
tests/orchestration/ | grep -i "provider\|pingpong"` — 11 files:

    test_pingpong_cli.py
    test_pingpong_integration.py
    test_pingpong_job_hunk_ledger.py
    test_pingpong_promote.py
    test_pingpong.py
    test_provider_evidence_integration.py
    test_provider_mode.py
    test_provider_patch_material.py
    test_provider_retry.py
    test_provider_timeouts.py
    test_provider_trust.py
    test_provider_trust_verification.py

CONFIRMED ABSENT: `tests/orchestration/test_session_resume.py` does not
exist. Searched with `ls tests/orchestration/test_session_resume.py`,
which exits 2 with `No such file or directory`, and the directory listing
above independently shows no file of that name.

## Citation count and tree resolution

This file cites 19 distinct `file:line` locations (or `file` where no
single line applies to an existence check):
`packages/orchestration/pingpong_provider.py:132`,
`packages/orchestration/pingpong_provider.py:159`,
`packages/orchestration/pingpong_provider.py:194`,
`packages/orchestration/pingpong_provider.py:221`,
`packages/orchestration/pingpong_provider.py:334`,
`packages/orchestration/pingpong_provider.py:395`,
`packages/orchestration/pingpong_provider.py:436`,
`packages/orchestration/pingpong_provider.py:865`,
`packages/orchestration/pingpong_provider.py:1326`,
`packages/orchestration/pingpong_provider.py:1391`,
`packages/orchestration/pingpong_provider.py:702`,
`packages/orchestration/pingpong_provider.py:1179`,
`packages/orchestration/token_actuals.py:16`,
`packages/orchestration/token_actuals.py:37`,
`packages/orchestration/worker_registry.py:148`,
`packages/orchestration/worker_registry.py:167`,
`packages/orchestration/pingpong_loop.py:3014`,
`packages/orchestration/pingpong_loop.py:3227`,
`packages/orchestration/diff_repair.py:1`.
Every one resolves with `git ls-tree HEAD -- <path>` (the containing
file's blob is present at HEAD; the round adds no code so every cited path
predates this branch).
