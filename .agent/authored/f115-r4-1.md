── STEP R4/n — F115 Prompt breakdown & cost report · Round 4 ─────────
Goal:        Wire the REVIEWER call site through `compose_reviewer_prompt` so its
             prompt-trace entries carry a real segment manifest, pin that
             behaviour and the wiring with tests, and resolve R-0321 with the
             reviewer-authored `Done:` text the R3 gate owes it.
Bundle:      C1a save this block · C1b mirror it · C2 resolve R-0321 ·
             C3 wire the reviewer call site · C4 pin it with two tests ·
             C5 plan + handback
Change:      EXACTLY these paths:
               .remedy-wt/f115-r4-1.md               (source, gitignored, NOT committed)
               .agent/authored/f115-r4-1.md          (new, C1a)
               .agent/last_block.md                  (rewrite, C1b)
               .agent/live_review.md                 (C2: one pair)
               packages/orchestration/pingpong_loop.py (C3: three pairs)
               tests/orchestration/test_prompt_trace.py (C4: one pair)
               .agent/plan.md                        (C5: full replace)
               .agent/handoff.md                     (C5: rewrite)
             NO other source file. Do NOT touch the PLANNER call site
             (`apps/cli/commands/job.py:236`) — it composes through
             `llm_planner` / `make_structured_planner`, not through a local
             compose call, and it is a round of its own.
Constraints:
  - TEXT-A … TEXT-E are AUTHORED text. Apply them byte for byte. Do not reword,
    rewrap or re-punctuate. No placeholder slots: substitute nothing.
  - The sent bytes must not change. `_build_reviewer_prompt` already returns
    `compose_reviewer_prompt(...).text` (`pingpong_loop.py:1415-1431`), so
    composing at the call site and taking `.text` is byte-identical by
    construction. Gate (d) proves it against the existing goldens. If any
    golden moves, STOP and hand back — do NOT adjust a golden.
  - Do NOT fix R-0320 or R-0322. Both are inherited, neither is an F115
    defect, and AGENTS.md bars mixing an unrelated fix into a feature branch.
  - Never force-push. Never commit on main. Push after EVERY commit (R-0289).
  - Do NOT create a pull request this round.
  - The red-proof in gate (f) runs ONLY inside a disposable `git worktree`
    (AGENTS.md / self-drive G5). The primary checkout is clean at handback.
Done when: every command has been RUN for real and its TRUE output recorded. A
           guessed, expected or remembered value is a finding.
  a. `cmp .agent/authored/f115-r4-1.md .agent/last_block.md` exits 0; record
     `sha256sum` of both and `wc -lc` of the authored file.
  b. After C2: `grep -c '^Done: R-0321' .agent/live_review.md` prints 1,
     `grep -c '^Landed:' .agent/live_review.md` prints 0, and
     `grep -c '^- R-0' .agent/live_review.md` prints 3 (unchanged).
  c. After C3, all four counts over `packages/orchestration/pingpong_loop.py`:
     `grep -c 'reviewer_composed = compose_reviewer_prompt('` prints 1 ·
     `grep -c 'reviewer_prompt = reviewer_composed.text'` prints 1 ·
     `grep -c 'composed_prompt=reviewer_composed,'` prints 1 ·
     `grep -c 'reviewer_prompt = _build_reviewer_prompt'` prints 0.
  d. After C3, the sent bytes are unchanged — run
     `python3 -m pytest tests/orchestration/test_reviewer_prompt_golden.py
     tests/orchestration/test_reviewer_prompt_scope.py
     tests/orchestration/test_prompt_cache_prefix.py -q`.
     Measured baseline at this branch head: `48 passed`. Record the real tail
     and exit code; anything other than 48 passed is a STOP.
  e. After C4: `python3 -m pytest tests/orchestration/test_prompt_trace.py -q`.
     Measured baseline before this round: `44 passed`. C4 adds exactly two
     tests, so the expected value is `46 passed`. Record the real tail.
  f. RED-PROOF, in a disposable worktree ONLY:
       git worktree add .remedy-wt/f115r4 HEAD
     In that worktree delete the single line `composed_prompt=reviewer_composed,`
     from `packages/orchestration/pingpong_loop.py`, then run, FROM THE WORKTREE
     ROOT, `python3 -m pytest tests/orchestration/test_prompt_trace.py -q -k
     "reviewer_composition or reviewer_call_site"`. Report the real tail and
     WHICH of the two ids failed. EXPECTED: `test_the_reviewer_call_site_hands_
     its_composition_down` FAILS and
     `test_the_reviewer_composition_traces_a_real_segment_manifest` PASSES —
     the behaviour test never imports the call site, which is exactly why the
     wiring guard exists. If the wiring guard stays GREEN, the guard is dead
     and that is a finding: report it, do not repair it. Then
     `git worktree remove .remedy-wt/f115r4 --force` and
     `git worktree prune`; record `git worktree list` afterwards.
  g. Regression scope for the touched module: `python3 -m pytest
     tests/orchestration/test_pingpong_cli.py
     tests/orchestration/test_repair_loop.py -q`. Measured baseline at this
     branch head: `303 passed`. Record the real tail and exit code.
  h. Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` (baseline
     `42 passed`) and `python3 -m pytest tests/docs/ -q` (baseline
     `294 passed`). Record both tails.
  i. `wc -l .agent/plan.md` prints a number BELOW 50 — record the real number.
  j. `git status --porcelain` empty; `git diff --name-only 0d6c97aa..HEAD`
     lists the fifteen paths of R1-R3 plus this round's two new ones
     (`.agent/authored/f115-r4-1.md`, `tests/orchestration/test_prompt_trace.py`)
     — seventeen in total, nothing else. `.remedy-wt/**` must NOT appear;
     `packages/orchestration/pingpong_loop.py` is already in the fifteen.
     `git rev-list --left-right --count origin/feature/f115-prompt-cost-report...HEAD`
     prints 0 and 0 after the final push.
Handback:  completion report + rewrite `.agent/handoff.md`. Item-status table
           (C1a, C1b, C2, C3, C4, C5 — each exactly once), commit table with
           real SHAs and insertions, changed-files table, every result a-j as a
           REAL value. Repeat the Fortschritt line verbatim. Over 60 lines ⇒
           carry a "Deviations, declared" line naming the count and the
           mandated content that caused it (AGENTS.md DECISION D15).
──────────────────────────────────────────────────────────────────────

PROCEDURE

C1a `chore(f115): save the R4 step block verbatim` — copy the reviewer's
    scratchpad original `.remedy-wt/f115-r4-1.md` to
    `.agent/authored/f115-r4-1.md`. Copy the FILE; do not retype it.
C1b `chore(f115): mirror the R4 block into last_block` — copy that same file to
    `.agent/last_block.md`. Run gate (a).

C2 `chore(f115): resolve R-0321 with the reviewer verdict`
    Apply the TEXT-A pair to `.agent/live_review.md`. REWRITE, line-anchored:
    the FROM is the single whole line beginning `Landed: R-0321` — match it by
    that anchor and replace the entire line, so no long line has to be retyped.
    Run gate (b).

C3 `feat(f115): give the reviewer trace entry its segment manifest`
    Apply TEXT-B, TEXT-C and TEXT-D to
    `packages/orchestration/pingpong_loop.py`, in that order. Run gates (c)
    and (d).

C4 `test(f115): pin the reviewer trace manifest and its wiring`
    Apply the TEXT-E pair to `tests/orchestration/test_prompt_trace.py`.
    APPEND-shaped: its TO opens with the FROM line verbatim, so the two new
    methods land at the END of `class TestSegmentManifest` and the module-level
    separator that follows keeps its place. Run gates (e), (f), (g).

C5 `chore(f115): refresh the plan and write the R4 handoff`
    `.agent/plan.md` ← TEXT-F in full, then rewrite `.agent/handoff.md`.
    Run gates (h), (i), (j).

TEXT-A — REWRITE pair for .agent/live_review.md
  FROM (the single whole line whose anchor is `^Landed: R-0321`):
Landed: R-0321 — …
  TO (1 line):
Done: R-0321 — RESOLVED at the R4 gate. Verified against the disk, not the report: `grep -c 'four of the eight' .agent/f115_inventory.md` prints 0 and `grep -c 'four of the seven'` prints 1, the enumeration below that sentence still names four wired call sites and three unwired, and `git show --numstat 8412f20c` shows the C3 commit of R3 changed exactly one line of that file. The R3 round as a whole is PASS: gates (a)-(g) were re-run by the reviewer and every value matched the handback, and the R3 diff touched only `.agent/**` and `docs/agents/planner_reviewer_prompt.md`, as its block declared.

TEXT-B — REWRITE pair for packages/orchestration/pingpong_loop.py
  FROM (1 line, occurs exactly once):
            reviewer_prompt = _build_reviewer_prompt(
  TO (4 lines):
            # F115 D1: compose instead of calling `_build_reviewer_prompt`, so the
            # trace entries below carry a real segment manifest. The sent bytes are
            # unchanged — `_build_reviewer_prompt` returns this same `.text`.
            reviewer_composed = compose_reviewer_prompt(

TEXT-C — APPEND-shaped pair for packages/orchestration/pingpong_loop.py
  FROM (2 lines, occurs exactly once):
            # Track reviewer prompt size
            result.reviewer_prompt_chars += len(reviewer_prompt)
  TO (begins with the composed-text line and ENDS with that same FROM verbatim):
            reviewer_prompt = reviewer_composed.text

            # Track reviewer prompt size
            result.reviewer_prompt_chars += len(reviewer_prompt)

TEXT-D — REWRITE pair for packages/orchestration/pingpong_loop.py
  FROM (2 lines, occurs exactly once):
                        configured_model=reviewer_model,
                        schema_v=_reviewer_schema_v(),
  TO (3 lines):
                        configured_model=reviewer_model,
                        composed_prompt=reviewer_composed,
                        schema_v=_reviewer_schema_v(),

TEXT-E — APPEND-shaped pair for tests/orchestration/test_prompt_trace.py
  FROM (1 line, occurs exactly once):
        assert "composed_prompt=builder_composed," in site
  TO (begins with that same FROM line verbatim):
        assert "composed_prompt=builder_composed," in site

    def test_the_reviewer_composition_traces_a_real_segment_manifest(self, monkeypatch):
        """F115 D1 behaviour, reviewer half: the manifest covers the composed BASE.

        The reviewer's traced text is `_reviewer_effective_prompt(...)`, which in
        structured mode appends the native-schema tail the registry deliberately
        does NOT cover (DECISION F105 D3). So `segment_manifest_chars` records the
        composed base and stays strictly BELOW `prompt_chars`, and that gap IS the
        coverage gap — recorded instead of implied. Structured mode is forced on
        here so the assertion cannot depend on the ambient environment.
        """
        from packages.orchestration.prompt_segments import PROMPT_SEGMENT_DELIMITER
        from packages.orchestration.pingpong_loop import (
            _reviewer_effective_prompt,
            compose_reviewer_prompt,
        )

        monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
        composed = compose_reviewer_prompt(
            "implement feature X",
            "builder did the thing",
            diff_summary="M  a.py",
            test_result="2 passed",
            files_changed=["a.py"],
            task_excerpt="detailed task body",
            task_sha256="abc",
            task_tokens_estimated=7,
            scope_contract="scope contract text",
        )
        entry = build_trace_entry(
            prompt_text=_reviewer_effective_prompt(composed.text),
            role="reviewer",
            composed_prompt=composed,
        )
        assert entry.segment_manifest != []
        assert [row["name"] for row in entry.segment_manifest] == [
            "reviewer_system",
            "reviewer_scope_contract",
            "reviewer_goal",
            "reviewer_task_input",
            "reviewer_builder_summary",
            "reviewer_files_changed",
            "reviewer_staged_diff",
            "reviewer_test_result",
        ]
        for row in entry.segment_manifest:
            assert set(row) == {"name", "rank", "sha256", "chars", "tokens_estimated"}
            assert len(row["sha256"]) == 64
            assert row["chars"] > 0
        rows = entry.segment_manifest
        boundaries = len(rows) - 1
        assert entry.segment_manifest_chars == len(composed.text)
        assert entry.segment_manifest_chars == sum(
            int(row["chars"]) for row in rows
        ) + boundaries * len(PROMPT_SEGMENT_DELIMITER)
        assert entry.segment_manifest_chars < entry.prompt_chars

    def test_the_reviewer_call_site_hands_its_composition_down(self):
        """F115 D1 wiring guard: an unwired reviewer trace entry fails HERE.

        The behaviour test above passes even when this call site is unwired,
        because it never touches `pingpong_loop` — which is why this guard
        exists. Index [2] is the reviewer's `build_trace_entry` append; [1] is
        the builder's, guarded by the test above it.
        """
        import packages.orchestration.pingpong_loop as pingpong_loop

        source = inspect.getsource(pingpong_loop)
        assert source.count("reviewer_composed = compose_reviewer_prompt(") == 1
        assert "reviewer_prompt = reviewer_composed.text" in source
        site = source.split("result.prompt_traces.append(build_trace_entry(")[2]
        site = site.split("))")[0]
        assert 'role="reviewer",' in site
        assert "prompt_text=prompt_text," in site
        assert "composed_prompt=reviewer_composed," in site

TEXT-F — the complete new .agent/plan.md

# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged at the Open PR Gate. Last reviewed SHA: 8601e276 (R3 PASS).
Next free finding ID: R-0323. Open findings: 2 — R-0320 (Low, carried
from F111), R-0322 (Medium, inherited suite red, not an F115 defect).
R-0321 was resolved at the R4 gate.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
R4 done — the REVIEWER call site now composes through
`compose_reviewer_prompt` and hands the composition to its trace entry,
so reviewer traces carry a real segment manifest. The manifest covers
the composed BASE; the native-schema tail stays uncovered by design
(F105 D3), which `segment_manifest_chars < prompt_chars` records.

## Next Steps
1. The PLANNER call site (`apps/cli/commands/job.py:236`). It does NOT
   compose locally — the prompt arrives through `llm_planner` and
   `make_structured_planner` as `effective_prompt`, so the composition
   has to be threaded down from where it is built. Inspect that path
   before ordering the wiring.
2. T001 proper — persist the manifest, or a reference to it, alongside
   the ledger row, additively, with backfill tolerance: old rows render
   as "unattributed", never guessed.
3. T002 — aggregation queries plus the pure renderer, with goldens;
   follow `gauntlet_matrix.py` and `tests/cli/test_stats_cost.py:49-128`.
4. T003 — CLI, prior-period comparison, json schema; then the
   integration gate and closure.

## Risks
- The per-role breakdown has one bucket until `role` stops being
  hardcoded, and per-task-class has no source at all. Both are recorded
  in the feature file; F115 must report "no data", never a fake bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.

Fortschritt: 30 % (R1 ✅ · T001a ✅ · Reviewer-Site ✅ · Planner-Site · T001 · T002 · T003 offen) — Schätzung
