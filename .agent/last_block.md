--- STEP R3/F106 — T001b: ClaudeProvider + ClaudeCliProvider surface ---

Goal: book the round 2 verdict, then land the SECOND slice of T001 — the
identical mechanical `supports_resume`/`resume` addition already applied to
the Protocol and `FakeProvider` in round 2, now applied to `ClaudeProvider`
and `ClaudeCliProvider`. No new design: same shape, same defaults, zero
behavior change. Once this lands all three adapters conform to the
Protocol; round 4 writes the dedicated test file, closing T001.

Base: `f05c3d6187c1fda5fec3f1148662ca07e0469482`, the tip of
`feature/f106-session-resume` after round 2. Same branch, no new branch.

## Bundle, in commit order

- C0a save this block verbatim to `.agent/authored/f106-r3.md`
- C0b mirror the same bytes into `.agent/last_block.md`
- C1  rewrite `.agent/plan.md` from slice PLAN3
- C2  append slice RECORD3 (the round 2 verdict) to `.agent/live_review.md`
- C3  apply the six pairs below to
      `packages/orchestration/pingpong_provider.py`
- C4  append slice PROSESLIP3 to `.agent/prose_slips.md`
- C5  rewrite `.agent/handoff.md` — the handback

## Change set — exactly these paths, nothing else

    .agent/authored/f106-r3.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    packages/orchestration/pingpong_provider.py
    .agent/prose_slips.md
    .agent/handoff.md

No file under `apps/`, `tests/`, `docs/` or any other `packages/` module
changes this round. `FakeProvider`, `BuilderOutput`, `ReviewerOutput` and
the Protocol are NOT touched again — only `ClaudeProvider` and
`ClaudeCliProvider`.

## Constraints

1. Apply every slice and pair BYTE FOR BYTE. If one looks wrong, apply it
   as given and DECLARE the problem.
2. C0a/C0b: `shutil.copyfile` from the reviewer's scratch original at
   `.remedy-wt/f106-r3-block.md` for C0a, then from the committed
   `.agent/authored/f106-r3.md` for C0b. Never `cp`, never retype.
3. C1 is the FIRST substantive commit, ahead of C2, per checklist item 23.
4. `.agent/live_review.md` and `.agent/prose_slips.md` are both
   APPEND-ONLY. C2 appends RECORD3, C4 appends PROSESLIP3; neither revises
   anything already on disk.
5. NO NEW R-ID IS MINTED and NO DECISION ID IS MINTED. Registered 318 and
   resolved 55 stay UNMOVED (measured at `f05c3d61`); `DECISION` stays 19.
   `Gate: F106 R2 — ` occurs 0x before C2 and exactly 1x after — that is
   RECORD3's own header. `.agent/prose_slips.md` gets ONE dated line, no id.
6. `.agent/plan.md` stays under 50 lines (AGENTS.md).
7. Every exit code is REAL, from `subprocess.run(...).returncode` in a
   script under the gitignored `.remedy-wt/`. Never through a pipe.
8. G3's negative control is the only destructive check this round and runs
   in its own disposable worktree per that gate's own text.
9. `remedy` the console script is DENIED in this sandbox; use
   `python3 -m apps.cli.main ...`.
10. Commit subjects: no leading-slash token, no absolute path, no
    secret-like string, no `Co-Authored-By` trailer.
11. Push after C5. Open NO pull request — T001 is not done until round 4
    lands the test file.
12. Pair shapes, measured by the reviewer's own containment test before
    emission: CLAUDEPROVIDER-NAME and CLICLIPROVIDER-NAME each read
    `TO contains FROM: true` (TO is FROM plus lines appended AFTER it,
    nothing inserted inside) — APPEND-shaped. THEIR TWO TO SLICES ARE
    BYTE-IDENTICAL TO EACH OTHER (both add the same three-line
    `supports_resume` property returning `False`), so a bare occurrence
    count of the appended lines is a SELF-COUNTING GATE — it would demand
    "1x" of text that legitimately appears twice. G5 below checks these
    two POSITIONALLY instead (byte offset, not count): do not substitute a
    count-based check for either. The other four pairs (CLAUDEPROVIDER-
    BUILD, CLAUDEPROVIDER-REVIEW, CLICLIPROVIDER-BUILD, CLICLIPROVIDER-
    REVIEW) each read `TO contains FROM: false` — REWRITE, so FROM 1x→0x
    and TO 0x→1x applies to each (their FROM/TO text differs between the
    two providers via the trailing `# F012` comment, so no duplication
    risk there). Run the same containment test yourself for all six
    independently (item 15 — do not generalize) and report your own
    result beside the reviewer's; on disagreement, apply the pair as given
    and declare it.
13. After C3, the file must still be valid Python: `python3 -c "import ast;
    ast.parse(open('packages/orchestration/pingpong_provider.py').read())"`
    exits 0, and the same four-class import line as round 2's constraint
    13 exits 0 with no output.

## Slices and pairs

Delimited the same way as prior rounds: content starts the line after
`<<<BEGIN` and ends with the newline before `<<<END`.

<<<BEGIN RECORD3
Gate: F106 R2 — T001a: PROTOCOL + EVIDENCE FIELDS + FAKEPROVIDER. VERDICT PASS. The reviewer re-ran every gate independently against the real diff `481565a8..f05c3d61`, inside a disposable review worktree removed after, then confirmed the primary checkout (the round's own shared working tree) landed at the same tip. G1 TRANSPORT: `.agent/authored/f106-r2.md` and `.agent/last_block.md` both 18877 bytes, byte-equal to the reviewer's own scratch original. G2 THE PLAN: `.agent/plan.md` byte-equal to slice PLAN2, 35 lines. G3 THE RECORD APPEND: base 1810768 bytes + `\n` + RECORD2 (2665 bytes) = 1813434, matching the committed file exactly; whole-reconstruction and paragraph-order readings both `True`; negative control in a disposable worktree (removed after) — one byte flipped 10 bytes into the appended region rejected by both readings, unflipped accepted by both. G4 THE LEDGER: 318 registered / 55 resolved / 263 open, unchanged at C1 and C2; `DECISION` count 19, unchanged; `Gate: F106 R1 — ` 0x before C2, 1x after. G5 THE CODE: all five pairs (PAIR-A, PAIR-B, FAKEPROVIDER-INIT, FAKEPROVIDER-NAME-BUILD, FAKEPROVIDER-REVIEW) independently re-measured `TO contains FROM: false`, FROM 1x→0x and TO 0x→1x for every one, `ast.parse` and the four-class import both exit 0. G6 ZERO BEHAVIOR CHANGE: `test_pingpong.py`+`test_provider_mode.py`+`test_provider_evidence_integration.py` 122 passed, matching base; A/B probe on `FakeProvider` — `supports_resume` False, `resume_used` False and `resume_session_ref` ""  on both `build`/`review` results with and without a `resume=` kwarg, and EVERY dataclass field equal between the two calls, `prepared_input` INCLUDED — the block's own gate text had asserted `prepared_input` would differ, which measurement showed false (booked as PROSESLIP3 this round, not an R-id: no product file was wrong, only the reviewer's own gate prose, per amend0827-process-diet rule 2). G7 THE STATE READERS AND CANARY: `tests/ui_server/` 515, `test_test_runner.py` 52, `test_resource_safety.py` 21, `test_integrity_gate.py` 16, canary 42 — all matching base exactly. G8 THE TREE AND LINT: `ruff check packages/orchestration/pingpong_provider.py` `All checks passed!`; tree clean, no untracked files; every commit's insertions under 500 (400, 350/294 note below, 15/19, 2/0, 21/0, 44/228 by `git diff --numstat` against each commit's own parent — the worker's own `git commit` terminal summaries print different, larger numbers for the two full-file `.agent/` rewrites due to git's own rewrite-detection heuristic, a presentation difference confirmed harmless, not a measurement error). THE ROUND PASSES: the change set matched the block's six named paths exactly, tree clean and pushed, no worktree survived.
<<<END RECORD3

<<<BEGIN PROSESLIP3
2026-08-30 — F106 R2's own gate G6 asserted `BuilderOutput.prepared_input`/`ReviewerOutput.prepared_input` would differ between a `resume=`-bearing call and a plain one; measurement at C3 showed every field equal including `prepared_input`, because `FakeProvider.build`/`review` do not thread `resume` into `prepare_call_input`'s options this round (correctly — T001a is additive-only). Reviewer-prose inaccuracy, nothing wrong on disk; no R-id spent (amend0827-process-diet rule 2).
<<<END PROSESLIP3

<<<BEGIN PLAN3
# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 1, round 3.

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
| T001a: Protocol + evidence fields + FakeProvider | done | round 2 |
| T001b: ClaudeProvider + ClaudeCliProvider, same surface | done | this round |
| T001c: `tests/orchestration/test_session_resume.py` | open | next round, closes T001 |
| T002 repair-path integration + delta shrink + expired fallback | open | gated on T001; F111 already accepted |
| T003 measured fixture comparison + docs | open | |

## Next Steps
1. This round applies the identical mechanical addition from round 2 to
   the two remaining adapters — no new design.
2. The next round writes `tests/orchestration/test_session_resume.py`
   covering all three adapters' `supports_resume`/`resume`/evidence-field
   shape, closing T001, then T002 (repair-path integration) can start.

## Risks
- None new. Carried forward: no adapter's `supports_resume` turns True
  until T002 wires real resume behavior.
<<<END PLAN3

<<<BEGIN CLAUDEPROVIDER-NAME-FROM
    @property
    def name(self) -> str:
        return "claude"
<<<END CLAUDEPROVIDER-NAME-FROM

<<<BEGIN CLAUDEPROVIDER-NAME-TO
    @property
    def name(self) -> str:
        return "claude"

    @property
    def supports_resume(self) -> bool:
        return False
<<<END CLAUDEPROVIDER-NAME-TO

<<<BEGIN CLAUDEPROVIDER-BUILD-FROM
    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> BuilderOutput:
        # F012: the builder prompt is sent verbatim — fingerprint the exact bytes.
<<<END CLAUDEPROVIDER-BUILD-FROM

<<<BEGIN CLAUDEPROVIDER-BUILD-TO
    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> BuilderOutput:
        # F012: the builder prompt is sent verbatim — fingerprint the exact bytes.
<<<END CLAUDEPROVIDER-BUILD-TO

<<<BEGIN CLAUDEPROVIDER-REVIEW-FROM
    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> ReviewerOutput:
        structured = _reviewer_structured_enabled()
        full_prompt = (
<<<END CLAUDEPROVIDER-REVIEW-FROM

<<<BEGIN CLAUDEPROVIDER-REVIEW-TO
    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> ReviewerOutput:
        structured = _reviewer_structured_enabled()
        full_prompt = (
<<<END CLAUDEPROVIDER-REVIEW-TO

<<<BEGIN CLICLIPROVIDER-NAME-FROM
    @property
    def name(self) -> str:
        return "claude-cli"
<<<END CLICLIPROVIDER-NAME-FROM

<<<BEGIN CLICLIPROVIDER-NAME-TO
    @property
    def name(self) -> str:
        return "claude-cli"

    @property
    def supports_resume(self) -> bool:
        return False
<<<END CLICLIPROVIDER-NAME-TO

<<<BEGIN CLICLIPROVIDER-BUILD-FROM
    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> BuilderOutput:
        # F012: the CLI sends the builder prompt verbatim (no out-of-band schema).
<<<END CLICLIPROVIDER-BUILD-FROM

<<<BEGIN CLICLIPROVIDER-BUILD-TO
    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> BuilderOutput:
        # F012: the CLI sends the builder prompt verbatim (no out-of-band schema).
<<<END CLICLIPROVIDER-BUILD-TO

<<<BEGIN CLICLIPROVIDER-REVIEW-FROM
    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> ReviewerOutput:
        structured = _reviewer_structured_enabled()
        # F012: fingerprint exactly what the transport receives — the prompt bytes plus, in
<<<END CLICLIPROVIDER-REVIEW-FROM

<<<BEGIN CLICLIPROVIDER-REVIEW-TO
    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> ReviewerOutput:
        structured = _reviewer_structured_enabled()
        # F012: fingerprint exactly what the transport receives — the prompt bytes plus, in
<<<END CLICLIPROVIDER-REVIEW-TO

## Done when — the gates

Run each gate and report ONE line with its REAL exit code. Every gate runs
at a commit STRICTLY EARLIER than C5, which writes the handback.

G1 TRANSPORT, at C0b. Report the byte length of the committed
   `.agent/authored/f106-r3.md` and `.agent/last_block.md`; state whether
   equal. No expected length stated — the reviewer holds the original.

G2 THE PLAN, at C1. `.agent/plan.md` byte-equal to slice PLAN3 (sha256 of
   both), under 50 lines, holds `## Goal` and `## Next Steps`.

G3 THE RECORD APPEND, at C2. Re-measure `.agent/live_review.md`'s
   pre-commit byte length (the reviewer read 1813434 at `f05c3d61`); base +
   `\n` + RECORD3 must equal the committed size. TWO readings: (a) whole
   reconstruction; (b) last blank-line unit equals RECORD3 (N=1). NEGATIVE
   CONTROL in a disposable worktree removed after: one byte flipped inside
   RECORD3 rejected by both readings, unflipped accepted by both.

G4 THE LEDGER, at C1 and C2. Registered/resolved/open unmoved from 318/55/
   263. `DECISION` count 19 at both. `Gate: F106 R2 — ` 0x before C2, 1x
   after. `.agent/prose_slips.md`'s byte length before C4 and after —
   report the delta equals PROSESLIP3's byte length plus one separator.

G5 THE CODE, at C3. For EACH of the six pairs: run your own containment
   test and report the result. For CLAUDEPROVIDER-NAME and
   CLICLIPROVIDER-NAME (append-shaped, and — constraint 12 — byte-identical
   to each other in their TO half, so checked POSITIONALLY, never by a bare
   occurrence count): confirm CLAUDEPROVIDER-NAME-TO's bytes appear in the
   post-commit file strictly between `class ClaudeProvider:` and
   `class ClaudeCliProvider:` (i.e. at `content.find("class ClaudeProvider:")
   < content.find(CLAUDEPROVIDER-NAME-TO) < content.find("class
   ClaudeCliProvider:")`), and CLICLIPROVIDER-NAME-TO's bytes appear AFTER
   `class ClaudeCliProvider:` with no second `class ` line between that
   class line and the match. Report both byte offsets found. For the other
   four (REWRITE-shaped): FROM 1x→0x, TO 0x→1x. Then `python3 -c "import
   ast; ast.parse(...)"` exits 0, and the four-class import exits 0 with no
   output (constraint 13).

G6 THE FULL SURFACE, at C3. Two parts. (a) Re-run the round-2 existing
   suite unmodified: `python3 -m pytest tests/orchestration/test_pingpong.py
   tests/orchestration/test_provider_mode.py
   tests/orchestration/test_provider_evidence_integration.py -q` — report
   exit code and passed count; the reviewer measured 122 at the base and
   expects the SAME after (behavior unchanged). (b) A read-only probe
   script under `.remedy-wt/`: import `ClaudeProvider` and
   `ClaudeCliProvider`, instantiate each with no arguments (no network
   call — do not call `.build`/`.review`, which would attempt a real
   provider call), and report `.supports_resume` reads `False` on both,
   and that `inspect.signature(cls.build).parameters` and
   `inspect.signature(cls.review).parameters` both include a `resume`
   parameter with default `None` for both classes.

G7 THE STATE READERS AND CANARY, after C2 (before C3's code touches
   nothing under `.agent/`, so this may run any time after C2). Each its
   own real exit code: `python3 -m pytest tests/ui_server/ -q`,
   `python3 -m pytest tests/orchestration/test_test_runner.py -q`,
   `python3 -m pytest tests/regression/test_resource_safety.py -q`,
   `python3 -m pytest tests/orchestration/test_integrity_gate.py -q`, and
   the canary `python3 -m pytest tests/cli/test_golden_path.py -q`. The
   reviewer measured 515, 52, 21, 16, 42 at the base; report yours.

G8 THE TREE AND LINT, at C3. `python3 -m ruff check
   packages/orchestration/pingpong_provider.py` — reviewer measured `All
   checks passed!` at the base; report your exit code and output. `git
   status --porcelain` empty, `git ls-files --others --exclude-standard`
   count 0, every commit's insertions under 500 (`git diff --numstat`).

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: state
block, `## Commits` table with `+/-` from `git diff --numstat`, deviations,
item-status table with every bundle item and every gate exactly once, next
steps. States `SESSION 1` of F106, round 3. No length cap.
