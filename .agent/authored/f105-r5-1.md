── STEP T002 repair — F105 ───────────────────────────────────
Goal:        Close R-0229 and R-0230, each with a red-proof, and record
             DECISION F105 D2. No new feature work.
Bundle:      C1 save this block · C2 persist both findings and the R4 record ·
             C3 fix R-0229 · C4 fix R-0230 · C5 decision, plan, context,
             handoff, push.
Change:      Exactly these paths:
             - .agent/authored/f105-r5-1.md   (new, this block verbatim)
             - .agent/last_block.md           (rewrite, same bytes)
             - .agent/live_review.md          (pairs A and B, then two Landed lines)
             - tests/orchestration/test_role_conventions.py  (C3, C4)
             - packages/orchestration/role_conventions.py    (C4, one line)
             - .agent/decisions.md            (pair C, append)
             - .agent/context.md              (pair D)
             - .agent/plan.md                 (rewrite, authored below)
             - .agent/handoff.md              (rewrite, yours per template)
Constraints: docs/agents/worker_conventions.md and docs/agents/reviewer_conventions.md
             are NOT touched — not one byte. No docs/, no docs/roadmap/, no
             AGENTS.md, no apps/. No builder migrated. The cap literal 800 stays
             out of both the module and the test file. A worker marks a landed
             fix `Landed: R-XXXX — <one line>` and NEVER writes a `Done:`
             paragraph (docs/agents/planner_reviewer_prompt.md §4.4).

C1 — save this block
  Write these bytes to BOTH .agent/authored/f105-r5-1.md (new) and
  .agent/last_block.md (replacing its contents). Run
  `cmp .agent/authored/f105-r5-1.md .agent/last_block.md`, record the exit code.
  Commit those two files alone.
  Subject: chore(f105): save the R5 repair block verbatim

C2 — persist the findings and the R4 record FIRST
  Apply pairs A and B to .agent/live_review.md in one commit, before any fix.
  Both are APPEND-SHAPED: each TO contains its FROM verbatim as its first line.
  Slice both texts out of .agent/authored/f105-r5-1.md on disk — never retype.
  Confirm each FROM occurs exactly once before its write, and that the file
  carries no trailing whitespace afterwards. Do not attempt a per-line
  uniqueness count: prose legitimately repeats short lines, and a count the text
  itself defeats is not a proof (the R4 D2 lesson).
  Subject: chore(f105): persist R-0229 and R-0230 and the R4 record

  PAIR A FROM (one line, exact):
  evidence at the integration gate rather than chased. OPEN.

  PAIR A TO:
  evidence at the integration gate rather than chased. OPEN.

- R-0229 (Medium, F105 R4): the segment-name mapping is unpinned, because the
  test that looks like its guard reads the mapping it is meant to prove.
  `tests/orchestration/test_role_conventions.py::TestRoleConventionsRegistration::test_registered_segment_carries_the_documented_name_and_rank`
  asserts `segment.name == CONVENTIONS_SEGMENT_NAMES[role]`, which holds for any
  mapping, correct or swapped. Proven in a disposable worktree at 65d3c7b9:
  exchanging the two values of `CONVENTIONS_SEGMENT_NAMES` between WORKER and
  REVIEWER leaves all 21 tests GREEN. This is not cosmetic — the segment name is
  what the T001 manifest records, so a swapped mapping would label the worker's
  conventions `reviewer_conventions` in every audit row, and the T003 per-builder
  goldens would inherit the mislabel. The module docstring itself says the names
  "appear in the segment manifest, so renaming one rewrites audit history": that
  is precisely the property no test guarded. The sibling mapping is fine —
  exchanging the two values of `CONVENTIONS_DOC_RELATIVE_PATHS` turns 3 tests RED
  through the role-specific rule anchors. Fix: assert the expected literal per
  role, for both mappings, and red-proof the swap. OPEN.
- R-0230 (Low, F105 R4): `packages/orchestration/role_conventions.py`
  `role_conventions_text` promises `RoleConventionsError` for a document that is
  "missing or unreadable", and the round's spec said the same, but only `OSError`
  is caught. A document that is not valid UTF-8 raises `UnicodeDecodeError`,
  which escapes the conventions layer — so `except PromptSegmentError`, the
  single catch this module's error hierarchy exists to enable, does not cover it.
  Fix: catch `(OSError, UnicodeDecodeError)` and pin it with a test. OPEN.

  PAIR B FROM (three lines, exact):
  `tests/orchestration/test_role_conventions.py`. No conventions RULE is
  re-authored, not one byte of either document changes, and no builder is
  migrated.

  PAIR B TO:
  `tests/orchestration/test_role_conventions.py`. No conventions RULE is
  re-authored, not one byte of either document changes, and no builder is
  migrated.
- Reviewer gate on R4 (2026-08-09): FINDINGS. Range `1a054862..65d3c7b9` read as
  a real diff — the eight declared paths and nothing else; no `docs/`, no
  `apps/`, no `AGENTS.md`, so neither conventions document changed a byte. Gates
  re-run by the reviewer from the repo root: `cmp` of the authored block against
  `.agent/last_block.md` exit 0, `test_role_conventions.py` 21 passed,
  `test_prompt_segments.py` 22 passed, `test_token_economy.py` 37 passed, the
  `.agent` contract tests 4 passed, `tests/docs/` 294 passed, the canary 42
  passed, integrity 5 of 5, tree clean, HEAD equal to origin. FOUR mutation
  red-proofs ran in a disposable worktree at 65d3c7b9, removed and pruned before
  the verdict: stripping the verbatim read turns 2 tests RED, dropping the token
  cap turns 1 RED, exchanging the document paths turns 3 RED — and exchanging the
  segment NAMES turns none, which is R-0229. `LAST_REVIEWED_SHA` does NOT advance
  and stays 1a054862.
- R5: the repair round for R-0229 and R-0230, plus DECISION F105 D2 on step-block
  size. No feature work; the discoverability block moves to R6.

C3 — fix R-0229
  In tests/orchestration/test_role_conventions.py, inside
  `TestRoleConventionsMappings`, add two parametrized tests that assert the
  EXPECTED LITERAL per role instead of reading the mapping under test:

    @pytest.mark.parametrize(
        "role, expected_name",
        [
            (ConventionsRole.WORKER, "worker_conventions"),
            (ConventionsRole.REVIEWER, "reviewer_conventions"),
        ],
    )
    def test_segment_name_mapping_holds_the_expected_literal(self, role, expected_name):
        assert CONVENTIONS_SEGMENT_NAMES[role] == expected_name
        _, segment = _register(role)
        assert segment.name == expected_name

    @pytest.mark.parametrize(
        "role, expected_relative",
        [
            (ConventionsRole.WORKER, "docs/agents/worker_conventions.md"),
            (ConventionsRole.REVIEWER, "docs/agents/reviewer_conventions.md"),
        ],
    )
    def test_document_path_mapping_holds_the_expected_literal(self, role, expected_relative):
        assert CONVENTIONS_DOC_RELATIVE_PATHS[role] == expected_relative

  Add a one-line WHY comment above the first of the two saying that these assert
  literals BECAUSE a test that reads the mapping it pins can never fail.
  Then RED-PROOF the fix, and do it only inside a disposable worktree:
    git worktree add .remedy-wt/f105-r5-redproof HEAD --detach
  In that worktree, exchange the two values of `CONVENTIONS_SEGMENT_NAMES`
  between WORKER and REVIEWER, run
  `python3 -m pytest tests/orchestration/test_role_conventions.py -q`, and record
  the real failure count and the failing test names. Then restore the file there,
  and remove the worktree with `git worktree remove --force .remedy-wt/f105-r5-redproof`
  followed by `git worktree prune`. NEVER mutate the primary checkout. Do not
  commit anything from the worktree. If a `cd` into the worktree makes a later
  relative path fail, use absolute paths — do not improvise around it.
  In the same commit, add under R-0229 in .agent/live_review.md the single line
  `  Landed: R-0229 — literal-per-role mapping assertions added; the swap now
  turns 2 tests RED.` and nothing else. Do not write a `Done:` paragraph.
  Subject: chore(f105): pin the conventions mapping to expected literals

C4 — fix R-0230
  In packages/orchestration/role_conventions.py change the one except clause of
  `role_conventions_text` from `except OSError as exc:` to
  `except (OSError, UnicodeDecodeError) as exc:`. Change nothing else in that
  file. Add to `TestRoleConventionsFailures` in the test file:

    def test_non_utf8_document_raises_role_conventions_error(self, tmp_path):
        repo_root = _write_repo_root(tmp_path)
        target = repo_root / CONVENTIONS_DOC_RELATIVE_PATHS[ConventionsRole.WORKER]
        target.write_bytes(b"\xff\xfe not utf-8")
        with pytest.raises(RoleConventionsError) as excinfo:
            role_conventions_text(ConventionsRole.WORKER, repo_root=repo_root)
        assert CONVENTIONS_DOC_RELATIVE_PATHS[ConventionsRole.WORKER] in str(excinfo.value)

  Red-proof it the cheap way: before applying the module change, run that one new
  test and record that it fails with `UnicodeDecodeError`; then apply the change
  and record it passing. Doing that in the primary checkout is acceptable ONLY
  because the test is added first and the module edit is the fix itself — no
  deliberate breakage is introduced. Record both transcripts.
  In the same commit, add under R-0230 in .agent/live_review.md the single line
  `  Landed: R-0230 — the decode error is caught with the OS error; pinned by a
  non-UTF-8 document test.` and nothing else.
  Subject: fix(f105): treat an undecodable conventions document as a load error

C5 — decision, state, handoff, push
  Apply pair C to .agent/decisions.md. It is APPEND-SHAPED against the file's
  final line. Then rewrite .agent/plan.md to the authored text below VERBATIM,
  apply pair D to .agent/context.md (REWRITE-shaped: FROM 0x and TO 1x after),
  and rewrite .agent/handoff.md yourself per docs/agents/handback_template.md
  and the AGENTS.md handoff rules — feature and round, branch, per-commit
  changed-files tables, the real verification table with real exit codes and
  real trimmed output, the authored-text proofs, both red-proof transcripts,
  deviations, the item-status table over C1-C5, open findings, next expected
  action. Carry a "Deviations, declared" line if it must exceed 60 lines. Then
  `git push -u origin feature/f105-cache-optimal-prompt-ordering` and report the
  result. Do NOT create a PR.
  Subject: chore(f105): hand back R5

  PAIR C FROM (one line, exact — the current final line of .agent/decisions.md):
Reverse this decision by deleting the doc and its two `docs/README.md` rows.

  PAIR C TO:
Reverse this decision by deleting the doc and its two `docs/README.md` rows.

## DECISION F105 D2 — step blocks are capped at 240 lines (2026-08-09)

Context: F105 R4's commit `ea48ea89` carried 523 insertions, 23 over the AGENTS.md
cap. The cause was not the work: C1 mandates writing the step block to BOTH
`.agent/authored/<round>.md` and `.agent/last_block.md`, so a block of N lines costs
2N insertions in one inseparable commit. The R4 block was 263 lines. It was declared
with its inseparability reason and verified to be the only oversize commit in F105
(previous maximum 486, `5d7b9fce`), so it is accepted under the AGENTS.md exception —
which by construction may be used at most ONCE per feature. F105's allowance is now
spent, and a second oversize commit on this branch would be a Medium finding.

D2 — every F105 step block from R5 on is at most 240 authored lines, so block plus
`last_block.md` clears 500 insertions with room to spare. The cause and the fix both
sit with the reviewer's authoring, not with the worker: when a round needs more
authored content than that, it is split into two rounds instead of one long block.
R5 and R6 are exactly that split — the repair and the discoverability block, which
together would have overrun the cap.

Alternative considered: exempt the C1 pair from the counting rule the way AGENTS.md
exempts a SINGLE `.agent/**` state-file rewrite. Rejected — the exemption exists
because a one-file verbatim save is indivisible, while block LENGTH is a free choice
of the author, and an exemption would remove the only pressure keeping blocks short.

Reverse this decision by deleting this entry.

  AUTHORED .agent/plan.md (verbatim, whole file):
# Plan — F105 Cache-optimal prompt ordering

Branch: feature/f105-cache-optimal-prompt-ordering, cut from main at cfda4245
after PR #188 (the F104 closure) merged at the Open PR Gate. Build mode:
one-session self-drive, one delegated worker per round. Next finding ID: R-0231.

## Goal
Prompt assembly stops being ad hoc. Every prompt composes from REGISTERED
SEGMENTS ordered by stability — system and conventions first, task and steering
last — every call records a segment manifest (name, rank, hash) into evidence,
and `remedy stats cache` shows the cache-read share per role from actuals. Prompt
CONTENT does not change; only its composition.

## Current Step
R5 — the repair round for the two R4 findings. R-0229 replaces the
self-referential segment-name assertion with literal-per-role assertions on both
conventions mappings, red-proved by exchanging the two names in a disposable
worktree. R-0230 makes an undecodable document fail as a `RoleConventionsError`
like a missing one. DECISION F105 D2 caps step blocks at 240 lines so the C1
save pair stops overrunning the AGENTS.md commit cap. R1, R2 and R3 are
reviewer-gated PASS; R4 gated FINDINGS, so `LAST_REVIEWED_SHA` stays 1a054862.
NO PR exists for this branch; one is created at CLOSURE, not now.
`.agent/candidates.md` is empty.

## Next Steps
- R6 — T002 part 2, the operator addition of 2026-07-30: a distilled
  write-discoverable-code block, sourced from the AGENTS.md "Code
  Discoverability Conventions" section, added to BOTH conventions documents as a
  reviewed diff of those documents, staying under the cap the R4 loader
  enforces.
- R7 — the session-terminator round: record the R5 and R6 gates and write the
  session-end handoff. This session's declared cap is four rounds, R4 through R7,
  so T003 starts in the NEXT session.
- Then T003: migrate the prompt builders, ONE builder per round, each with its
  content-equality golden, and wire the segment manifest into call evidence.
- Then T004, the `remedy stats cache` view over actuals, then the integration
  gate, then closure (the PR is created there).

## Risks
- Roughly twenty assembly sites in three idioms (template `.format`, a `parts`
  join, f-string concatenation). Migration must not change content — goldens
  land before behaviour moves.
- No tokenizer here: the conventions cap rides the chars/4 estimator in
  `packages/orchestration/token_economy.py`, so it is an ESTIMATE, documented as
  one rather than presented as a count. The headroom is real but small — the
  worker document estimates 505 tokens and the reviewer document 515 against a
  cap of 800 — so the R6 block must be distilled, not pasted.
- R-0221 stays open and will cost the F105 integration gate the same phantom
  base-only failures it cost F103 and F104.

  PAIR D FROM (.agent/context.md, exact):
R1 claim, candidate sweep and state reset → R2 T001 the segment registry,
compose and the manifest → R3 the session terminator of the previous session →
R4 T002 the conventions loaders and their goldens → R5 the distilled
discoverability block added to both conventions documents → R6+ T003 one builder
per round, each with a content-equality golden → T004 the cache stats view →
integration gate → closure.

  PAIR D TO:
R1 claim, candidate sweep and state reset → R2 T001 the segment registry,
compose and the manifest → R3 the session terminator of the previous session →
R4 T002 the conventions loaders and their goldens → R5 the repair of R-0229 and
R-0230 → R6 the distilled discoverability block added to both conventions
documents → R7 the session terminator → T003 one builder per round, each with a
content-equality golden → T004 the cache stats view → integration gate →
closure.

Done when:   Every command below was run by you from the repo root and its REAL
             exit code and REAL trimmed output appear in the handoff.
             A. cmp .agent/authored/f105-r5-1.md .agent/last_block.md
             B. python3 -m pytest tests/orchestration/test_role_conventions.py -q
                (expect 26 passed: 21 + 4 mapping-literal + 1 non-UTF-8)
             C. python3 -m pytest tests/orchestration/test_prompt_segments.py -q
             D. python3 -m pytest tests/orchestration/test_test_runner.py -q -k "live_review or context_md or plan_md"
             E. python3 -m pytest tests/docs/ -q
             F. python3 -m pytest tests/cli/test_golden_path.py -q (canary)
             G. git status --porcelain (must be EMPTY)
             H. git worktree list (must show the primary checkout alone)
             I. remedy integrity check --json through the python3 -c form over
                apps.cli.grouped:main — report "passed" and "fail_count"
             J. the C3 red-proof transcript: with the two segment names exchanged
                in the disposable worktree, the failure count and the failing
                test names
             K. the C4 red-proof transcript: the new non-UTF-8 test failing with
                UnicodeDecodeError before the module change, passing after
Handback:    completion report + rewrite .agent/handoff.md
──────────────────────────────────────────────────────────────
