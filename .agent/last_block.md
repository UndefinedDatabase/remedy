--- STEP R2/F106 — T001a: Protocol + evidence fields + FakeProvider ---

Goal: book the round 1 verdict into the record, then land the FIRST slice
of T001 — the `supports_resume` capability shape on the provider Protocol,
the `resume_used`/`resume_session_ref` evidence fields on
`BuilderOutput`/`ReviewerOutput`, and the matching additive surface on
`FakeProvider` (the adapter the round-3 test file exercises most). Zero
behavior change: every new parameter is optional with a default, every new
field defaults False/"". `ClaudeProvider`/`ClaudeCliProvider` get the same
treatment next round (T001b); the new test file lands the round after that
(T001c), once all three adapters conform.

Base: `481565a8dac13f32621e536a4e8e01cdbe597e97`, the tip of
`feature/f106-session-resume` after round 1. Same branch, no new branch.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f106-r2.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN2
- C2  append slice RECORD2 (the round 1 verdict) to `.agent/live_review.md`
- C3  apply the five pairs below to
      `packages/orchestration/pingpong_provider.py`
- C4  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f106-r2.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    packages/orchestration/pingpong_provider.py
    .agent/handoff.md

No file under `apps/`, `tests/`, `docs/` or any other `packages/` module
changes this round. `ClaudeProvider`/`ClaudeCliProvider` are NOT touched —
only the Protocol, the two output dataclasses, and `FakeProvider`.

## Constraints

1. Apply every slice and pair BYTE FOR BYTE. Do not fix, rewrap or improve
   one. If a slice looks wrong, apply it as given and DECLARE the problem.
2. C0a/C0b: `shutil.copyfile` from the reviewer's scratch original at
   `.remedy-wt/f106-r2-block.md` for C0a, then from the committed
   `.agent/authored/f106-r2.md` for C0b. Never `cp`, never retype. Extract
   every slice/pair from the COMMITTED `.agent/authored/f106-r2.md`.
3. C1 is the FIRST substantive commit, ahead of C2, per AGENTS.md's Commit
   Gate and checklist item 23 (this round touches the finding ledger).
4. The record is APPEND-ONLY. C2 appends RECORD2 and revises nothing
   already in `.agent/live_review.md`.
5. NO NEW R-ID IS MINTED and NO DECISION ID IS MINTED this round. Registered
   318 and resolved 55 stay UNMOVED (measured by the reviewer at
   `481565a8`); `DECISION F\d+ D\d+ — ` stays 19. `Gate: F106 R1 — ` occurs
   0x before C2 and exactly 1x after — that is RECORD2's own header, not a
   new finding id.
6. `.agent/plan.md` stays under 50 lines (AGENTS.md).
7. Every exit code is REAL, from `subprocess.run(...).returncode` in a
   script under the gitignored `.remedy-wt/`. Never through a pipe.
8. G3's negative control is the only destructive check this round and runs
   in its own disposable worktree per that gate's own text; G6's probe is
   read-only (import + call, nothing written) and needs no worktree.
9. `remedy` the console script is DENIED in this sandbox; use
   `python3 -m apps.cli.main ...`.
10. Commit subjects: no leading-slash token, no absolute path, no
    secret-like string, no `Co-Authored-By` trailer.
11. Push after C4. Open NO pull request — T001 is not done until round 4
    (T001c) lands the test file.
12. Pair shapes, measured by the reviewer's own containment test before
    emission, reported here as the result, not the method: all FIVE pairs
    (PAIR-A, PAIR-B, FAKEPROVIDER-INIT, FAKEPROVIDER-NAME-BUILD,
    FAKEPROVIDER-REVIEW) read `TO contains FROM: false` — each inserts new
    lines INSIDE the FROM span rather than after it, so each is a REWRITE.
    Run the same containment test yourself for each of the five
    independently (item 15 — do not generalize from one to the rest) and
    report your own result beside the reviewer's; if any of yours
    disagrees, apply the pair as given and declare the discrepancy rather
    than silently reclassifying it. For every REWRITE pair: FROM occurs
    exactly 1x in `packages/orchestration/pingpong_provider.py` before C3
    and 0x after; TO occurs 0x before and exactly 1x after. Report all five
    readings.
13. After C3, the file must still be valid Python: `python3 -c "import ast;
    ast.parse(open('packages/orchestration/pingpong_provider.py').read())"`
    exits 0, and `python3 -c "from packages.orchestration.pingpong_provider
    import PingPongProvider, FakeProvider, ClaudeProvider, ClaudeCliProvider,
    BuilderOutput, ReviewerOutput"` exits 0 with no output.

## Pairs

Each pair is FROM/TO, delimited the same way as the round 1 slices: content
starts the line after `<<<BEGIN` and ends with the newline before
`<<<END`.

<<<BEGIN RECORD2
Gate: F106 R1 — THE CLAIM AND THE SHAPE INVENTORY. VERDICT PASS. The reviewer re-ran every gate independently against the real diff `811c2d7e..481565a8`, not against the worker's own report, inside a disposable review worktree removed after. G1 TRANSPORT: `.agent/authored/f106-r1.md` and `.agent/last_block.md` both 18597 bytes, byte-equal to the reviewer's own scratch original at `.remedy-wt/f106-r1-block.md`. G2 THE PLAN: `.agent/plan.md` byte-equal to slice PLAN1 (with its trailing newline included, per the marker convention), 39 lines. G3 THE RECORD APPEND: base 1809603 bytes + one separator `\n` + RECORD1 (1164 bytes) = 1810768 bytes, matching the committed file exactly; whole-reconstruction and paragraph-order readings both `True`; negative control in a disposable worktree (removed after) — one byte flipped 10 bytes into the appended region rejected by both readings, the unflipped byte accepted by both. G4 THE LEDGER: 318 registered / 55 resolved / 263 open, unchanged at C1 and at C2; `DECISION` count 19, unchanged; no id minted. G5 THE CLAIM AND DOCS PINS: `docs/roadmap/STATUS.md` PAIRSTATUS-FROM 0x / PAIRSTATUS-TO 1x, exactly one `^- \[~\] F\d{3} — ` line in the whole file, `git diff --numstat` for C3 alone reads `1 1`; `pytest tests/docs/ -q` 295 passed, `test_roadmap_index.py` 30 passed, both matching the reviewer's own base reading. G6 THE CONTEXT FILE: `.agent/context.md` byte-equal to slice CONTEXT1. G7 THE STATE READERS AND CANARY: `tests/ui_server/` 515, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, canary 42 — all matching the base exactly. G8 THE INVENTORY AND THE TREE: `.agent/f106_inventory.md` carries all seven SPEC sections; 30 distinct `file:line` citations, two spot-checked directly by the reviewer (`pingpong_loop.py:3227`/`:3284`, both real `reviewer_provider.review(` call sites; `worker_registry.py:167-169`, the three `supports_*` fields) and every one resolving via `git ls-tree HEAD`; tree clean, no untracked files, every commit's insertions under 500. ONE DECLARED DEVIATION, NOT A DEFECT: an extra commit (`44c6847c`) corrected the inventory's own citation-count tally from a partial hand-count (19) to a complete mechanical enumeration (30) after the worker's own self-audit caught the undercount — a real deviation from the block's exact 8-commit bundle shape, judged correct by the reviewer rather than routed to a repair round, since it strengthened the evidence and stayed strictly inside the round's own Change set. THE ROUND PASSES: the change set matched the block's eight named paths exactly, the tree was clean and pushed, no worktree survived.
<<<END RECORD2

<<<BEGIN PLAN2
# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 1, round 2.

## Goal
Repair rounds stop resending the world: where the provider supports resuming
a session, a repair call resumes the original session and sends only the
findings delta, with an honest automatic fallback to full context when the
session is gone, flagged in evidence. Correctness never depends on resume
working.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the F106 claim, branch, shape inventory | done | round 1 |
| T001a: Protocol + evidence fields + FakeProvider | done | this round |
| T001b: ClaudeProvider + ClaudeCliProvider, same surface | open | next round |
| T001c: `tests/orchestration/test_session_resume.py` | open | round 4, once all 3 adapters conform |
| T002 repair-path integration + delta shrink + expired fallback | open | gated on T001; F111 already accepted |
| T003 measured fixture comparison + docs | open | |

## Next Steps
1. This round adds `supports_resume`, the `resume` kwarg, and the two
   evidence fields to the Protocol and to `FakeProvider` only.
2. The next round does the identical mechanical addition to
   `ClaudeProvider` and `ClaudeCliProvider` — no new design, same shape.
3. Round 4 writes the dedicated test file once all three adapters share the
   same surface, closing T001.

## Risks
- None new this round. Carried from round 1: only `ClaudeCliProvider`
  reports a session id today; no adapter's `supports_resume` turns True
  until T002 wires real resume behavior.
<<<END PLAN2

<<<BEGIN PAIR-A-FROM
    usage_actuals: dict[str, Any] | None = None
    actual_missing_reason: str = ""
    incomplete: bool = False
    stream_cap_reached: bool = False
    stream_call_id: str = ""
    stream_artifact_refs: list[str] = field(default_factory=list)
    prepared_input: Any = None  # F012: fingerprint of the EXACT transport request


@dataclass
class ReviewFinding:
<<<END PAIR-A-FROM

<<<BEGIN PAIR-A-TO
    usage_actuals: dict[str, Any] | None = None
    actual_missing_reason: str = ""
    # F106 T001: honest resume bookkeeping — true only when this call
    # actually resumed a prior session; the ref it resumed, "" otherwise.
    resume_used: bool = False
    resume_session_ref: str = ""
    incomplete: bool = False
    stream_cap_reached: bool = False
    stream_call_id: str = ""
    stream_artifact_refs: list[str] = field(default_factory=list)
    prepared_input: Any = None  # F012: fingerprint of the EXACT transport request


@dataclass
class ReviewFinding:
<<<END PAIR-A-TO

<<<BEGIN PAIR-B-FROM
    usage_actuals: dict[str, Any] | None = None
    actual_missing_reason: str = ""
    incomplete: bool = False
    stream_cap_reached: bool = False
    stream_call_id: str = ""
    stream_artifact_refs: list[str] = field(default_factory=list)
    prepared_input: Any = None  # F012: fingerprint of the EXACT transport request


# ---------------------------------------------------------------------------
# Provider protocol
# ---------------------------------------------------------------------------

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
<<<END PAIR-B-FROM

<<<BEGIN PAIR-B-TO
    usage_actuals: dict[str, Any] | None = None
    actual_missing_reason: str = ""
    # F106 T001: honest resume bookkeeping — true only when this call
    # actually resumed a prior session; the ref it resumed, "" otherwise.
    resume_used: bool = False
    resume_session_ref: str = ""
    incomplete: bool = False
    stream_cap_reached: bool = False
    stream_call_id: str = ""
    stream_artifact_refs: list[str] = field(default_factory=list)
    prepared_input: Any = None  # F012: fingerprint of the EXACT transport request


# ---------------------------------------------------------------------------
# Provider protocol
# ---------------------------------------------------------------------------

class PingPongProvider(Protocol):
    """Protocol for Builder/Reviewer providers."""

    @property
    def name(self) -> str: ...

    @property
    def supports_resume(self) -> bool: ...

    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> BuilderOutput: ...

    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> ReviewerOutput: ...
<<<END PAIR-B-TO

<<<BEGIN FAKEPROVIDER-INIT-FROM
        malformed_review_recoverable: bool = False,
    ) -> None:
        self._builder_files = builder_files or ["docs/README.md"]
<<<END FAKEPROVIDER-INIT-FROM

<<<BEGIN FAKEPROVIDER-INIT-TO
        malformed_review_recoverable: bool = False,
        supports_resume: bool = False,
    ) -> None:
        self._builder_files = builder_files or ["docs/README.md"]
        self._supports_resume = supports_resume
<<<END FAKEPROVIDER-INIT-TO

<<<BEGIN FAKEPROVIDER-NAME-BUILD-FROM
    @property
    def name(self) -> str:
        return "fake"

    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> BuilderOutput:
<<<END FAKEPROVIDER-NAME-BUILD-FROM

<<<BEGIN FAKEPROVIDER-NAME-BUILD-TO
    @property
    def name(self) -> str:
        return "fake"

    @property
    def supports_resume(self) -> bool:
        return self._supports_resume

    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> BuilderOutput:
<<<END FAKEPROVIDER-NAME-BUILD-TO

<<<BEGIN FAKEPROVIDER-REVIEW-FROM
    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> ReviewerOutput:
        out = self._review_impl(prompt, timeout_sec=timeout_sec,
                                max_output_chars=max_output_chars)
<<<END FAKEPROVIDER-REVIEW-FROM

<<<BEGIN FAKEPROVIDER-REVIEW-TO
    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> ReviewerOutput:
        out = self._review_impl(prompt, timeout_sec=timeout_sec,
                                max_output_chars=max_output_chars)
<<<END FAKEPROVIDER-REVIEW-TO

## Done when — the gates

Run each gate and report ONE line per gate with its REAL exit code. Every
gate runs at a commit STRICTLY EARLIER than C4, which writes the handback.

G1 TRANSPORT, at C0b. Report the byte length of the committed
   `.agent/authored/f106-r2.md` and of `.agent/last_block.md`; state
   whether they are byte-equal. No expected length is stated here — the
   reviewer holds the original.

G2 THE PLAN, at C1. `.agent/plan.md` byte-equal to slice PLAN2 (sha256 of
   both), line count under 50, holds `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2. Re-measure `.agent/live_review.md`'s
   pre-commit byte length yourself (the reviewer read 1810768 at
   `481565a8`); base + `\n` + RECORD2 must equal the committed size. TWO
   readings: (a) whole reconstruction; (b) the committed file's last
   blank-line unit equals RECORD2 exactly (N=1). NEGATIVE CONTROL, in a
   disposable worktree removed after: one byte flipped inside RECORD2 is
   rejected by both readings; the unflipped byte is accepted by both.

G4 THE LEDGER, at C1 and C2. Report registered/resolved/open — the
   reviewer measured 318/55/263 at `481565a8`, unmoved is the PASS
   condition. `DECISION` count 19 at both. `Gate: F106 R1 — ` occurs 0x
   before C2 and exactly 1x after.

G5 THE CODE — PAIR SHAPE AND ORDERED APPLICATION, at C3. For EACH of the
   five pairs (PAIR-A, PAIR-B, FAKEPROVIDER-INIT, FAKEPROVIDER-NAME-BUILD,
   FAKEPROVIDER-REVIEW): run your own containment test (`TO contains
   FROM`) and report the result; then report FROM's occurrence count in
   `packages/orchestration/pingpong_provider.py` before C3 and after, and
   TO's occurrence count before and after — FROM must read 1x→0x and TO
   0x→1x for every one of the five. Then `python3 -c "import ast;
   ast.parse(open('packages/orchestration/pingpong_provider.py').read())"`
   exits 0, and the four-class import line from constraint 13 exits 0 with
   no output.

G6 ZERO BEHAVIOR CHANGE — THE PROBE, at C3. Two parts, both real, in the
   primary checkout (read-only, no worktree needed — nothing is deleted or
   broken). (a) Existing suite, unmodified by this round:
   `python3 -m pytest tests/orchestration/test_pingpong.py
   tests/orchestration/test_provider_mode.py
   tests/orchestration/test_provider_evidence_integration.py -q` — report
   the exit code and passed count; the reviewer measured these green at the
   base (before this round's edit) and expects the SAME passed count after,
   since nothing under test changed behavior. (b) A/B probe script under
   `.remedy-wt/`: construct two `FakeProvider()` instances with identical
   constructor arguments; call `.build("x")` on one and
   `.build("x", resume="some-ref")` on the other, and likewise for
   `.review("x")` / `.review("x", resume="some-ref")`; report that
   `.supports_resume` is `False` on the instance, and that every field of
   the two `BuilderOutput`/`ReviewerOutput` results is equal EXCEPT
   `prepared_input` (which legitimately differs — F012 fingerprints the
   call, not resume) — report the field-by-field comparison, not just
   "equal". `resume_used` reads `False` and `resume_session_ref` reads `""`
   on BOTH results.

G7 THE STATE READERS AND CANARY, at C4's parent (i.e. after C2, before C4
   itself — `.agent/` state was rewritten at C1/C2). Each its own real exit
   code: `python3 -m pytest tests/ui_server/ -q`,
   `python3 -m pytest tests/orchestration/test_test_runner.py -q`,
   `python3 -m pytest tests/regression/test_resource_safety.py -q`,
   `python3 -m pytest tests/orchestration/test_integrity_gate.py -q`, and
   the canary `python3 -m pytest tests/cli/test_golden_path.py -q`. The
   reviewer measured 515, 52, 21, 16, 42 at the base; report yours.

G8 THE TREE AND LINT, at C3. `python3 -m ruff check
   packages/orchestration/pingpong_provider.py` — the reviewer measured
   `All checks passed!` at the base; report your exit code and output.
   `git status --porcelain` empty, `git ls-files --others
   --exclude-standard` count 0, every commit's insertions under 500
   (`git diff --numstat`).

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: state
block, `## Commits` table with `+/-` from `git diff --numstat`, deviations,
item-status table with every bundle item and every gate exactly once, next
steps. States `SESSION 1` of F106, round 2. No length cap.
