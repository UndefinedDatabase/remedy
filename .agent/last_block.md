── STEP R15/18 — F082 Self-benchmark ─────────────────────────────────────────
Goal:        Record the R14 verdict, register the four reviewer defects R14
             surfaced — three of them found by the worker — and build T003b's
             READ half: the `models` map a run already writes into `run.json`
             becomes a `BenchRecord` field that survives the history file.

Bundle:      C0a save this block · C0b mirror it · C1 GATE-R14 + FINDINGS-R423-426
             appended to the review record · C2 the read half in
             `capability_bench.py` and `bench_history.py` · C3 the new pins in
             `test_bench_model_context.py` · C4 plan and context re-sync · C5
             handback.

Change:      This list is a CEILING. Nothing outside it.
             - .agent/authored/f082-r15.md                     (C0a, new)
             - .agent/last_block.md                            (C0b)
             - .agent/live_review.md                           (C1 append)
             - packages/orchestration/capability_bench.py      (C2, 5 pairs)
             - packages/orchestration/bench_history.py         (C2, 2 pairs)
             - tests/orchestration/test_bench_model_context.py (C3, by contract)
             - .agent/plan.md                                  (C4 whole-file)
             - .agent/context.md                               (C4, two pairs)
             - .agent/handoff.md                               (C5)
             NOT in scope: `docs/**`, `apps/**`, `scripts/**`, every gauntlet
             module, and every PRE-EXISTING bench test file. This round adds no
             new module and no new file except C0a.

Constraints:
 1. THE READ HALF TOUCHES NO GAUNTLET MODULE. The path is already built:
    `gauntlet_runner._evidence_body` writes `models` into `run.json`,
    `bench_dry_run._recorded_bodies` reads that body back as raw JSON, and
    `capability_bench.build_bench_record` receives it as `evidence_body`.
    `gauntlet_evidence.RunEvidence` is NOT on that path and is not edited. No
    additive ruling is needed and none is invented (R-0426).
 2. `models` IS THE LAST FIELD AND IT IS DEFAULTED. Seven `BenchRecord(`
    construction sites exist — three under `packages/` and four under `tests/`,
    counted by grep before this block was written. A defaulted last field keeps
    every one of them valid UNEDITED, and that is the additivity proof gate 11
    measures on both axes.
 3. ABSENCE IS NOT AN UNOBSERVED ROLE. A body carrying no `models` key at all
    reads back as `None`. A body whose roles were unobservable reads back as a
    dict whose VALUES are `None`. These are different facts and both are pinned
    (R-0178, and R-0407 for what a false zero costs).
 4. `.agent/plan.md` stays UNDER 50 lines and keeps `## Goal` and `## Next
    Steps`. The PLAN slice was measured at 48 lines before emission (R-0423).
 5. Apply every REWRITE-PAIR slice DISK-TO-DISK out of the COMMITTED
    `.agent/authored/f082-r15.md`. No `--- BEGIN SLICE` / `--- END SLICE`
    marker line may reach any target file. No target file gains a
    trailing-whitespace line. C3 is authored by YOU from the contract below,
    not transported.
 6. Every commit follows the AGENTS.md self-review loop and the Commit Gate.
    Insertions per commit stay under 500. No commit trailer.
 7. Apply every slice VERBATIM. If a slice is wrong on arrival, apply it as
    ordered and DECLARE it — do not silently repair it (R-0419). Reporting a
    reviewer's error is the behaviour this round exists to reward.
 8. DECISION F082 D7 and D8 and every prior gate entry ARE NOT REWRITTEN. They
    are time-stamped history. R-0425 corrects D8's line number by APPENDING.

────────────────────────── AUTHORED SLICES ──────────────────────────

--- BEGIN SLICE GATE-R14 --- (append to .agent/live_review.md, C1, ONE physical line)
Gate: R14 — PASS, with four new findings, ALL of them the reviewer's, and three of the four found by the worker before the reviewer saw them. Verification tier: round gate only; R14 changed no executable line, so no full-suite claim is made and none is owed. Every one of the sixteen ordered gates was re-executed by the reviewer against the disk rather than read out of the handback, and every reported value matched. Transport is proven at PRIMARY strength: the committed `.agent/authored/f082-r14.md`, the same file on disk and `.agent/last_block.md` are all three byte-identical under python3 `read_bytes()`, sha256 `a0a0da2490a4c5b54241b309f61ee416b7e0e83d8921d93d95c11e5458f2ec18`, 22962 bytes, and the measured line count is 246 — exactly the number the block stated before emission, so R-0420's new rule held on its first run. The C1 append is a PROPERTY and not a line count: over the committed `dc376e91^` to `dc376e91` the reviewer re-derived that `post` equals `pre` followed by a newline, the gate slice, a blank line, the findings slice and a closing newline, TRUE byte-wise, with `pre` a prefix of `post`, the added region 8203 bytes and the numstat deletion column 0. Record counts at HEAD are `^Gate: R13 — PASS` 1, `^- R-0420 — ` 1, `^- R-0421 — ` 1, `^- R-0422 — ` 1, `^## DECISION F082 D8` 1, `^## DECISION F082 D7` 1, `^Landed: ` 0 and `^Done: ` 0, and the open set recomputed mechanically is FIFTY-TWO with no duplicate, max R-0422 and next free R-0423. Both context pairs were re-proved by the reviewer as R-0422's own rule demands: the composite `pre` with BOTH replacements applied EQUALS `post`, each FROM goes 1x to 0x, each TO goes 0x to 1x, and `FROM in TO` is False for both. `.agent/plan.md` byte-equals the PLAN slice as a whole file at sha256 `0934d07bc7479171b9a0930ff566e90ece525dc6343b02fd2e5f6d534b3a69b6`. The change set is six paths, every one inside the block's Change list, and the same range restricted to apps, packages, tests, scripts and docs is EMPTY, so the no-code claim is proven rather than asserted. Marker lines reaching any target: 0. Trailing-whitespace lines gained in any target: 0. Suites re-run by the reviewer at the branch head: the canary plus the three contract readers `184 passed` exit 0, and `test_bench_model_context.py` plus `test_gauntlet_runner.py` `53 passed` exit 0, so R13's work still stands. `integrity check --json` is `passed: true`, `fail_count: 0` over 5 checks with `handler_import` still `handlers=337`. Insertions per commit are 246, 148, 8, 37 and 61 with none over 500, `git status --porcelain` is empty, `git worktree list` is the single primary checkout, `.agent/STOP` is absent and `gh pr list --state open` is `[]`. The round's decisive act was again Constraint 7: the block was wrong three times, and the worker applied it as ordered and DECLARED all three rather than quietly repairing them — which is right, because a silent repair of the PLAN slice would have destroyed the byte-equality that makes transport provable, and a silent repair of the finding text would have hidden two reviewer defects that are now written down. The worker also did the reviewer's diagnostic work for it: gate 9's expected count was unreachable, and the handback names the exact cause — the findings slice quotes the very phrase the gate counts — rather than reporting a bare mismatch. No block condition was hit: no fabricated data, no false live indicator, no missing changed-files table, no unverified completion claim, no silent scope change.
--- END SLICE GATE-R14 ---

--- BEGIN SLICE FINDINGS-R423-426 --- (append to .agent/live_review.md, C1, after GATE-R14, one blank line between the gate and this slice)
- R-0423 — Medium, REVIEWER-BLOCK DEFECT, found by the worker and confirmed by the reviewer by measuring the committed file. The R14 block ordered `.agent/plan.md` "under 50 lines" in its own Constraint 4 and then supplied a PLAN slice that is FIFTY-TWO lines, to be applied as a WHOLE-FILE byte-equal replacement. The two orders cannot both be obeyed, and the worker obeyed the one that keeps transport provable — byte-equality — and declared the breach, which is the correct choice. This is R-0420's family recurring INSIDE the block that registered R-0420: the reviewer measured the block itself, as the new rule demands, and did not measure the slices the block carries. AGENTS.md's own under-fifty rule for `plan.md` is therefore broken on disk at HEAD, which is why this is Medium. Standing rule from here, binding the reviewer: every WHOLE-FILE slice is measured against the cap that binds its TARGET file before emission, and the measured number is stated in the block next to the constraint it must satisfy. Measuring the container does not measure the contents.

- R-0424 — Medium, REVIEWER-GATE DEFECT, found by the worker and confirmed by the reviewer by re-deriving the count. R14's gate 9 ordered that a phrase quoted out of DECISION F082 D8 appear in `.agent/live_review.md` exactly ONCE — the original inside D8 — and stated that a 2 means "the record was edited or the finding was rewritten". Neither happened: the reviewer verified that D8 is untouched by proving the whole file is a pure append over `dc376e91^`, with 8 insertions and 0 deletions. The real cause is that the block's OWN findings slice quotes that phrase verbatim, in double quotes, inside R-0421. Applying the block correctly therefore FORCES the count to 2, and the gate's stated expectation of 1 was unreachable from the moment the block was written. This is the R-0371 family — a gate that cannot be satisfied as written — in a new form: not self-reference and not arithmetic, but a gate that counts a string while ignoring the block's own contribution of that string. Standing rule from here, binding the reviewer: before ordering a count of any string, count that string in the BLOCK's own slices and either add that number to the expected value or gate a property the block's text cannot influence. This round applies the rule by ordering line-anchored counts only.

- R-0425 — Low, REVIEWER-FINDING DEFECT, found by the worker and confirmed by the reviewer with a repository-wide grep and by reading the file. R-0421 states that the seventh call site of `packages/orchestration/intake.py::make_structured_call_fn` is at `intake.py:324`. Line 324 is a COMMENT line inside the factory body; the real seventh call site is `intake.py:331`, inside `make_provider_call_fn`. The finding's substance is untouched and re-verified: there are SEVEN call sites, and the other six line numbers — `gauntlet_runner.py:216` and `:225`, `mission_cmd.py:227` and `:385`, `do_cmd.py:246` and `:2864` — are exact. Corrected here by APPENDING rather than by editing R-0421, because a registered finding is history. Low because the count, which is what R-0421 exists to correct, is right. Standing rule from here, binding the reviewer: a line number written into a finding is read back off the file at that line before the finding is emitted; a grep that returns a match does not tell you which of its lines you copied.

- R-0426 — Medium, REVIEWER-PLAN DEFECT, found by the reviewer while reading the code the plan describes. `.agent/plan.md` and the R14 handoff both state that T003b's read half means carrying `models` from `gauntlet_evidence.py::RunEvidence` into the bench record, "which needs its own additive ruling because that is a third gauntlet module". Every clause of that is false, and the code says so: `capability_bench.build_bench_record` receives the raw `run.json` body as its `evidence_body` argument, and `bench_dry_run._recorded_bodies` produces that body with `json.loads` straight off disk without constructing a `RunEvidence` at all. `RunEvidence` is not on the path, `capability_bench.py` is a BENCH module and not a gauntlet module, and the three `BenchRecord(` construction sites under `packages/` are all in bench modules. Had the block been written from the plan, the round would have edited a gauntlet module that needs no editing and would have manufactured a DECISION to permit it — the exact scope drift the additive design exists to prevent. Medium because a plan that names the wrong file directs the next round's work. This is R-0419's grep-every-writer rule applied to a data PATH rather than to a set of writers, so it adds no new standing rule; it is evidence that the existing one was not run here.
--- END SLICE FINDINGS-R423-426 ---

--- BEGIN SLICE CB-FIELD --- (in packages/orchestration/capability_bench.py, C2 — REWRITE pair)
    repair_rounds: int | None
    postmortem_classes: tuple[str, ...]

    def to_json(self) -> dict[str, Any]:
--- END SLICE CB-FIELD ---

--- BEGIN SLICE CB-FIELD-TO --- (C2)
    repair_rounds: int | None
    postmortem_classes: tuple[str, ...]
    #: Which model served which role in the run this row came from, straight off
    #: the evidence body's ``models`` key (F082 T003b write half, DECISION F082
    #: D7). ``None`` means the run recorded no model context AT ALL — a run from
    #: before the write half landed. A role the run could not observe is ``None``
    #: INSIDE the dict, which is a different fact and stays distinguishable here.
    #: Last field and defaulted on purpose: every existing ``BenchRecord(`` call
    #: site stays valid unedited, which is what makes this change additive.
    models: dict[str, str | None] | None = None

    def to_json(self) -> dict[str, Any]:
--- END SLICE CB-FIELD-TO ---

--- BEGIN SLICE CB-JSON --- (in packages/orchestration/capability_bench.py, C2 — REWRITE pair)
            "repair_rounds": self.repair_rounds,
            "postmortem_classes": list(self.postmortem_classes),
        }
--- END SLICE CB-JSON ---

--- BEGIN SLICE CB-JSON-TO --- (C2)
            "repair_rounds": self.repair_rounds,
            "postmortem_classes": list(self.postmortem_classes),
            "models": dict(self.models) if self.models is not None else None,
        }
--- END SLICE CB-JSON-TO ---

--- BEGIN SLICE CB-DOC --- (in packages/orchestration/capability_bench.py, C2 — REWRITE pair)
    Reads only what R2's inventory proved a gauntlet run already writes:
    ``order_id``, ``wall_seconds`` and ``tokens`` off the ``run.json`` body,
    and the ``failure_class`` of each postmortem it recorded. Everything else
    the feature file names is either supplied by the caller (``series``) or has
    no source in the harness and is therefore ``None`` (``repair_rounds``).
--- END SLICE CB-DOC ---

--- BEGIN SLICE CB-DOC-TO --- (C2)
    Reads only what a gauntlet run already writes: ``order_id``,
    ``wall_seconds`` and ``tokens`` off the ``run.json`` body (R2's inventory),
    the ``failure_class`` of each postmortem it recorded, and — since T003b's
    write half — the ``models`` map. Everything else the feature file names is
    either supplied by the caller (``series``) or has no source in the harness
    and is therefore ``None`` (``repair_rounds``).
--- END SLICE CB-DOC-TO ---

--- BEGIN SLICE CB-VARS --- (in packages/orchestration/capability_bench.py, C2 — REWRITE pair)
    tokens = evidence_body.get("tokens")
    wall = evidence_body.get("wall_seconds")
    return BenchRecord(
--- END SLICE CB-VARS ---

--- BEGIN SLICE CB-VARS-TO --- (C2)
    tokens = evidence_body.get("tokens")
    wall = evidence_body.get("wall_seconds")
    models = evidence_body.get("models")
    return BenchRecord(
--- END SLICE CB-VARS-TO ---

--- BEGIN SLICE CB-BUILD --- (in packages/orchestration/capability_bench.py, C2 — REWRITE pair)
        repair_rounds=None,
        postmortem_classes=_postmortem_classes_of(evidence_body),
    )
--- END SLICE CB-BUILD ---

--- BEGIN SLICE CB-BUILD-TO --- (C2)
        repair_rounds=None,
        postmortem_classes=_postmortem_classes_of(evidence_body),
        # A body with no ``models`` key predates T003b's write half, and that
        # absence is ``None`` rather than a dict of ``None``s: "nobody recorded
        # this" and "this role was unobservable" are different facts (R-0178).
        models=({str(k): (None if v is None else str(v)) for k, v in models.items()}
                if isinstance(models, dict) else None),
    )
--- END SLICE CB-BUILD-TO ---

--- BEGIN SLICE BH-VARS --- (in packages/orchestration/bench_history.py, C2 — REWRITE pair)
    classes = row.get("postmortem_classes")
    return BenchRecord(
--- END SLICE BH-VARS ---

--- BEGIN SLICE BH-VARS-TO --- (C2)
    classes = row.get("postmortem_classes")
    models = row.get("models")
    return BenchRecord(
--- END SLICE BH-VARS-TO ---

--- BEGIN SLICE BH-READ --- (in packages/orchestration/bench_history.py, C2 — REWRITE pair)
        postmortem_classes=tuple(str(c) for c in classes) if isinstance(classes, list) else (),
    )
--- END SLICE BH-READ ---

--- BEGIN SLICE BH-READ-TO --- (C2)
        postmortem_classes=tuple(str(c) for c in classes) if isinstance(classes, list) else (),
        # A history line written before T003b carries no ``models`` key. It
        # reads back as ``None`` and the trend keeps it that way: the file is
        # append-only and is never rewritten to add a field to old rows.
        models=({str(k): (None if v is None else str(v)) for k, v in models.items()}
                if isinstance(models, dict) else None),
    )
--- END SLICE BH-READ-TO ---

--- BEGIN SLICE CTXSCOPE --- (in .agent/context.md, C4 — REWRITE pair)
constructs `OllamaBuilder()` where no seam can observe it. Still to come,
T003b's read half — those models into the bench record — and the fake-provider
bench run end to end, inventoried at R11 before either is built.
--- END SLICE CTXSCOPE ---

--- BEGIN SLICE CTXSCOPE-TO --- (C4)
constructs `OllamaBuilder()` where no seam can observe it. T003b's READ half
landed at R15: `BenchRecord` carries a defaulted `models` field that
`build_bench_record` reads straight off the evidence body and that survives the
history file. No gauntlet module is touched and no additive ruling was needed —
`RunEvidence` is not on that path at all, and R-0426 registers the reviewer's
earlier claim that it was. Still to come, the fake-provider bench run end to
end, inventoried at R11 before it is built.
--- END SLICE CTXSCOPE-TO ---

--- BEGIN SLICE CTXSTEPS6 --- (in .agent/context.md, C4 — REWRITE pair)
served which role ✅ → R14 record the R13 verdict and register R-0420 to R-0422
→ R15 T003b the read half and the fake-provider run → R16 the integration gate
→ R17 closure. T003 split at DECISION F082 D5, its second half inventoried at
D6, unblocked at D7 and split in two at D8; each round marks the PREVIOUS one
done and never itself.
--- END SLICE CTXSTEPS6 ---

--- BEGIN SLICE CTXSTEPS6-TO --- (C4)
served which role ✅ → R14 record the R13 verdict and register R-0420 to R-0422 ✅
→ R15 record the R14 verdict, register R-0423 to R-0426 and build T003b's read
half → R16 the fake-provider run and the Q7 pin → R17 the integration gate →
R18 closure. T003 split at DECISION F082 D5, its second half inventoried at D6,
unblocked at D7 and split in two at D8, and R15 splits the read half off from
the run because they are independent deliverables; each round marks the
PREVIOUS one done and never itself.
--- END SLICE CTXSTEPS6-TO ---

--- BEGIN SLICE FORTSCHRITT --- (the Fortschritt line; the handoff repeats it VERBATIM, R-0418)
Fortschritt: ~86 % (T001 ✅ · T002 ✅ · T003a ✅ · T003b Schreib- und Lesehälfte gebaut und gegated · Fake-Provider-Lauf offen) — Schätzung
--- END SLICE FORTSCHRITT ---

--- BEGIN SLICE PLAN --- (WHOLE-FILE replacement of .agent/plan.md, C4)
# Plan — F082 Self-benchmark

Branch: feature/f082-self-benchmark, cut from main after the F077 closure PR
#200 merged. F082 is claimed `[~]` in docs/roadmap/STATUS.md. Next free finding
id: R-0427. Open findings: fifty-six — the thirty-two carried from F077, plus
R-0403 to R-0426 registered on this branch. `.agent/live_review.md` is the
source of truth for that ledger; this file mirrors it and nothing else.

## Goal
Capability becomes a measured, versioned trend instead of a feeling: a frozen
set of benchmark orders runs on demand, producing pass rate, cost, wall time and
repair rounds per order into an append-only history, and `remedy stats bench`
shows the trend with regression warnings. DONE when the bench runs green on
fixtures, history survives across runs, and a deliberately degraded fixture run
triggers the regression warning.

## Current Step
R15 records the R14 gate, registers R-0423 to R-0426, and builds T003b's READ
half: the `models` map a run already writes into `run.json` becomes a defaulted
`BenchRecord` field that survives the history file. No gauntlet module is
touched and no additive ruling is needed — R-0426 corrects the plan claim that
one was.

## Next Steps
1. R16 — the fake-provider bench run end to end, clearing R11's Q6 four
   blockers: no entry point, local-Ollama reach, a `time.monotonic()` call in
   `::run_order`, and history resolving to the real data root; plus the Q7 pin
   for "the bench never runs implicitly".
2. R17 the integration gate, R18 closure.

## Risks
- "The bench never runs implicitly" is an ACCEPTANCE criterion that NO test
  pins (R11 Q7). It holds today only by absence: `append_bench_run` and
  `dry_run_from_order_set` have no caller under `apps/`, `packages/` or
  `scripts/`. An unpinned criterion at closure is a blocker, so R16 pins it.
- The builder's model stays unobservable: making it visible means reaching into
  `orchestrator_loop.py::execute_dispatched_job`. Closure states that absence
  rather than implying three roles were recorded.
- The delivered order set is three, not the Design's five (R-0411). Closure may
  not quote five, and DECISION F082 D3 binds the recovery to a bench-owned
  fixture rather than an edit to the gauntlet's template.
- The freeze holds against a file-side edit only (R-0410). The Built State
  states that threat model rather than quoting the criterion whole.
- Reviewer defects are the dominant finding class here and four more landed at
  R14. Nine standing counter-measures now bind every block: R-0417 staleness,
  R-0418 Fortschritt, R-0419 grep-every-writer, R-0420 measure-the-block,
  R-0421 count-the-list, R-0422 composite-property, R-0423 measure-the-slice,
  R-0424 count-your-own-contribution, R-0425 read-back-the-line-number.
--- END SLICE PLAN ---

────────────────── C3 — THE NEW PINS, BY CONTRACT ──────────────────
APPEND a new numbered section to `tests/orchestration/test_bench_model_context.py`
and add whatever imports it needs — that file already owns T003b's pins and its
docstring explains why `test_x.py` ↔ `x.py` is not followed there. Create no new
file and touch no pre-existing bench test file; gate 11 measures that. Every
test function already in the file stays present and unedited. Reuse its
`an_order()` helper and drive bodies through the REAL `_evidence_body`, never a
hand-written dict, so the read half is pinned against what the write half
actually emits. Pin exactly these six properties:

 1. A body whose `models` names two roles produces a `BenchRecord` whose
    `models` equals that same map, builder included as `None`.
 2. A body built with NO model context — `_evidence_body(..., None)` — produces
    `models` equal to a dict with all three roles present and each `None`.
 3. A body with the `models` key DELETED produces `models is None`. Properties
    2 and 3 together are Constraint 3 — the two different absences.
 4. `BenchRecord.to_json()` carries `models`, keeps its keys sorted, and
    survives a `json.dumps`/`json.loads` round trip unchanged.
 5. A record appended with the REAL `bench_history.append_bench_run` and read
    back with `load_bench_history` still carries the same `models` map. A field
    that only survives `to_json` has not survived the file.
 6. A history line written by hand with NO `models` key still loads, reads back
    `models is None`, and keeps its other fields — back-compat as a property of
    the reader, not of a migration.

────────────────────────── DONE WHEN ──────────────────────────
Run every gate. Record its REAL output. "Green" as a word is a finding.
BASE is 56635794.

 1. `git status --porcelain` EMPTY at handback; `git worktree list` back to
    exactly the primary checkout. Report both verbatim.
 2. TRANSPORT AS A PROPERTY: python3 `read_bytes()` equality of
    `.agent/authored/f082-r15.md` and `.agent/last_block.md`, plus the shared
    sha256 and byte length. The reviewer measured this block at 399
    lines before emission (R-0420). Report the REAL line count and say whether
    it matches; a mismatch is the reviewer's defect to own, not yours to fix.
 3. `.agent/STOP` — report presence at round START and at handback.
 4. C1 APPEND PROOF over the COMMITTED `<C1>^` to `<C1>`: report whether `post`
    equals `pre` + newline + GATE-R14 + blank line + FINDINGS-R423-426 + a
    closing newline, BYTE-WISE — the same join R14 proved. Report the C1
    `--numstat`; its DELETION column must be 0.
 5. RECORD COUNTS in `.agent/live_review.md` at HEAD, LINE-ANCHORED only:
    `^Gate: R14 — PASS` 1 · `^- R-0423 — ` 1 · `^- R-0424 — ` 1 ·
    `^- R-0425 — ` 1 · `^- R-0426 — ` 1 · `^## DECISION F082 D8` 1 ·
    `^## DECISION F082 D7` 1 · `^Landed: ` 0 · `^Done: ` 0. Report each real
    number. No unanchored substring count is ordered this round (R-0424).
 6. OPEN SET RECOMPUTED MECHANICALLY: every `^- R-\d+ — ` paragraph minus every
    `^Done: R-\d+ — ` line. Report the count, max id, next free id and any
    duplicate. R15 registers exactly four, so the expected count is FIFTY-SIX
    and the next free id becomes R-0427 — report the real numbers regardless.
 7. C2 AS TWO PER-FILE COMPOSITES over the COMMITTED `<C2>^` to `<C2>` (R-0422:
    five pairs share `capability_bench.py` and two share `bench_history.py`, so
    a per-pair whole-file equality is unreachable and is NOT ordered). Per file
    report `pre` with ALL its replacements applied `== post`; per pair report
    FROM 1x to 0x, TO 0x to 1x and `FROM in TO`. The reviewer measured all
    seven FROMs at 1x and `FROM in TO` False; report the real values.
 8. C3 IS AN EXTENSION, NOT A REWRITE. Report the count of `^def test_` in
    `tests/orchestration/test_bench_model_context.py` at BASE and at HEAD, and
    report whether EVERY test function name present at BASE is still present at
    HEAD. Report the C3 `--numstat` for that file.
 9. `.agent/plan.md` at HEAD BYTE-EQUALS the PLAN slice as a WHOLE FILE. Report
    its sha256 and `wc -l`; it must be UNDER 50 (R-0423 — the reviewer measured
    the slice at 48 lines; report the real number), and it keeps `## Goal` and
    `## Next Steps`. Report `wc -l` for `.agent/context.md` and its contract
    readers: `## Active Branch` then a `feature/` slug · substring `Steps` · a
    roadmap F-id · `pytest` or `resource`.
10. CHANGE SET: `git diff --name-only 56635794..HEAD` — report every path,
    COUNT them, and state whether you measured before or after C5. The Change
    list is a CEILING. `git diff --name-only 56635794..HEAD -- docs/ apps/
    scripts/` MUST be EMPTY.
11. ADDITIVITY ON BOTH AXES, the claim this round's design rests on. THE TWO
    SETS: the gauntlet's SEVEN are `tests/orchestration/test_gauntlet_*.py`
    plus `tests/orchestration/test_self_run_gauntlet.py`; the pre-existing
    bench FIVE are `tests/orchestration/test_bench_dry_run.py`,
    `test_bench_history.py`, `test_bench_orders.py`, `test_capability_bench.py`
    and `tests/cli/test_stats_bench.py`. (a) NOT EDITED:
    `git diff --name-only 56635794..HEAD` restricted to either set MUST be
    EMPTY, and restricted to `packages/orchestration/` must name exactly
    `capability_bench.py` and `bench_history.py`. (b) STILL GREEN: run each set
    together — reviewer's BASE measurements `276 passed` and `61 passed`.
    Report both real numbers and both exit codes.
12. `python3 -m pytest tests/orchestration/test_bench_model_context.py -q` →
    exit 0. Reviewer's BASE measurement `8 passed`; this round adds pins, so it
    MUST rise. Report the real number; no prediction is ordered (R-0336).
13. `python3 -m pytest tests/cli/test_golden_path.py
    tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_test_runner.py -q` → exit 0. Reviewer's BASE
    measurement: 184 passed.
14. `python3 -m ruff check packages/orchestration/capability_bench.py
    packages/orchestration/bench_history.py
    tests/orchestration/test_bench_model_context.py` → exit 0. The reviewer ran
    this at BASE and it was `All checks passed!`, so a red result here is THIS
    round's doing. Repository-wide ruff is red on main and is NOT gated
    (R-0364).
15. `python3 -m apps.cli.main integrity check --json` → `passed: true`,
    `fail_count: 0`, `check_count: 5`, `handler_import` message `handlers=337`.
16. `gh pr list --state open --json number,headRefName` → report verbatim. Must
    be `[]`. Create NO pull request.
17. Report each commit's `git show --numstat <sha>` insertion total. If any
    exceeds 500, declare it with the inseparability reason BEFORE review. C5
    cannot state its own numstat; report it in the completion report.
18. STANDING STALENESS GATE (R-0417, seventh run). Re-read every sentence in
    the files this round touched that states a COUNT, a module list, a
    round-to-step map, or a completion claim, and report for each whether it
    still holds at HEAD. Repair ONLY what the ordered slices cover; report
    everything else and leave it. State how many sentences you checked. Known
    open items to re-check rather than repair: `.agent/context.md` still names
    240 as the preferred block target, which this block exceeds by design.
No mutation red-proof is ordered and none is owed: the change is additive and
the absence-versus-unobserved distinction is pinned by C3 properties 2 and 3.
The docs-round gate does NOT bind; gate 10 proves `docs/**` is untouched.
BLOCK-SIZE DECLARATION (R-0420): 399 lines, under the 400 cap (DECISION
F105 D5) and OVER the 240 preference, because seven code pairs plus the C3
contract cannot be carried in prose. C0a's insertions stay inside the 500 limit.

Handback:    Completion report + rewrite `.agent/handoff.md` per
             docs/agents/handback_template.md: feature and round, branch,
             per-commit changed-files tables, the real verification values
             above, an item-status table with every C0a–C5 item and every gate
             1–18 exactly once, open-findings count, next expected action.
             Declare every deviation with its cause. Repeat the FORTSCHRITT
             slice VERBATIM (R-0418). Push after every commit. Create NO PR.
             THE NEXT SESSION'S FIRST ACTION is self_drive_protocol.md Phase 1
             rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2's Open PR
             Gate; say so in the Next section. F082 is MID-FEATURE and no PR
             exists. The next round is R16, the fake-provider run and the Q7
             pin.
──────────────────────────────────────────────────────────────────────────────
