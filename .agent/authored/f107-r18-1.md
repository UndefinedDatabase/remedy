── STEP R18/20 — F107 Context compiler v2 ─────────────
Goal:        Persist three new findings and the R17 gate, repair R-0292 (an
             unparseable non-tier-1 file is included with empty signatures and
             no omissions record, contradicting the feature file's own
             Edge-cases clause), and record the two Design deferrals as an
             operator-visible DECISION.
Bundle:      C1 save block · C2 mirror · C3 findings and gate persist FIRST ·
             C4 the R-0292 repair plus its tests · C5 the reason-vocabulary
             docs · C6 DECISION F107 D1 and D2 · C7 plan and handoff.
Change:      `.agent/authored/f107-r18-1.md` (new) · `.agent/last_block.md` ·
             `.agent/live_review.md` · `packages/orchestration/context_compiler.py` ·
             `tests/orchestration/test_context_compiler.py` ·
             `docs/guides/job-context-view-user-guide-v0.md` ·
             `docs/roadmap/features/T2_F107.md` (ONE line) ·
             `.agent/decisions.md` (append) · `.agent/plan.md` ·
             `.agent/handoff.md`. Ten paths, nothing else. No `apps/`, no
             `pingpong_loop.py`, no README.md, no STATUS.md.
Constraints: AGENTS.md in full. Insertions per commit under 500. Commit
             subjects carry no leading-slash tokens and no absolute paths.
             Push after every commit. Do NOT add the fifth reason anywhere the
             block does not name. Do NOT touch `docs/roadmap/ROADMAP.md`.
Done when:   gates A-K below are executed and their REAL results recorded.
Handback:    completion report + rewrite `.agent/handoff.md` (<= 60 lines, or a
             "Deviations, declared" line naming the real count and the mandated
             content that caused it, per AGENTS.md DECISION D15).

C1 — save this block verbatim to `.agent/authored/f107-r18-1.md`. Record
`wc -l` and `sha256sum`. Commit alone, then push:
  chore(f107): save the R18 step block verbatim

C2 — `cp .agent/authored/f107-r18-1.md .agent/last_block.md`, then
`cmp .agent/authored/f107-r18-1.md .agent/last_block.md` (silent, exit 0).
Commit alone, then push:
  chore(f107): mirror the R18 block into last block

C3 — FINDINGS PERSIST FIRST (planner_reviewer_prompt.md §4.4)
PAIR_HDR is a REWRITE. In `.agent/live_review.md` replace the one line:
<<<BEGIN PAIR_HDR_FROM>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0290.
<<<END PAIR_HDR_FROM>>>
<<<BEGIN PAIR_HDR_TO>>>
> Branch: feature/f107-context-compiler-v2. Next free ID: R-0293.
<<<END PAIR_HDR_TO>>>

PAIR_LRF is an APPEND: the TO's first line IS the FROM, which is the last line
of the R-0289 entry. Everything after that first line is new text inserted
directly beneath it, still inside the `## Findings` list.
<<<BEGIN PAIR_LRF_FROM>>>
  loss it will later have to report. OPEN.
<<<END PAIR_LRF_FROM>>>
<<<BEGIN PAIR_LRF_TO>>>
  loss it will later have to report. OPEN.
- R-0290 (Medium, F107 R18, reviewer-side protocol defect, found by this
  session against itself): docs/agents/self_drive_protocol.md Phase 0 lists six
  probe commands — `git status --porcelain`, `git branch --show-current`,
  `git log --oneline -n 8`, `gh pr list`, `remedy plan status` and `remedy plan
  next` — and NOT ONE of them can see a feature branch that is not checked out.
  This session ran the probe exactly as written while standing on `main` after
  merging PR #192, read the F105-era `.agent/` state that `main` carries,
  selected F107 by Rule A5 because `main`'s STATUS.md says `- [ ] F107`, and
  authored a complete R1 claim block for a feature that was already 102 commits
  deep on this branch — integration gate green at R16, seventeen findings
  registered, its own `.agent/candidates.md` emptied by its own R1. The
  delegated worker refused to write anything and reported the collision with
  `git for-each-ref` evidence, so the round cost zero commits. The
  single-writer rule is the only reason this is a near-miss rather than a
  rewind: the authored payloads replaced `.agent/live_review.md` WHOLESALE at
  "Next free ID: R-0271" while the file on disk stood at R-0290. Two
  compounding causes, both worth naming. (1) `.agent/` read on `main` is
  LAST-MERGE state, never latest-worker state, whenever a feature's work sits
  on an unmerged branch — the file the protocol calls "the only return channel"
  is invisible from the branch the probe stands on. (2) The closure protocol
  defers each feature's PR to the NEXT feature's start, so a
  completed-but-unclosed feature has BY DESIGN no open PR, and `gh pr list` —
  the one probe command that could have surfaced it — returns empty exactly
  when the risk is highest. Fix, forward-looking: Phase 0 gains `git branch -a
  --list 'feature/*'` plus `git log --oneline -1` and `git show
  <branch>:.agent/handoff.md | head -20` for every feature branch ahead of
  `main`, and Phase 1 gains a rule that such a branch whose own STATUS line
  reads `[~]` is a PENDING FEATURE that outranks Rule A5 selection. Registered
  NOT fixed here: editing the self-drive protocol is outside F107's change set,
  the same boundary R-0287 respects. OPEN.
- R-0291 (Medium, F107 R18): two bullets of the feature file's Design are UNMET
  on disk and no DECISION records the deviation, so the roadmap promises
  behaviour the code deliberately does not have. (a)
  `docs/roadmap/features/T2_F107.md` Design says "The compiled context becomes
  a registry segment with its manifest hash in evidence".
  `register_compiled_context_segment`
  (`packages/orchestration/context_compiler.py:984`) exists and is unit-tested,
  but `grep -rn 'register_compiled_context_segment' --include=*.py` returns only
  its definition, its docstring line and five lines of
  `tests/orchestration/test_context_compiler.py` — no production caller. The one
  production path that compiles a context during a run,
  `packages/orchestration/pingpong_loop.py:2682-2683`, calls
  `render_compiled_context_text` and sets `categories =
  [COMPILED_CONTEXT_SEGMENT_NAME]`: a context string and a label, not a
  `PromptSegment`, with no registry, no rank and no manifest. The module says so
  itself at `context_compiler.py:66-68` — "The segment manifest is not written
  into evidence here… wiring the manifest and the size comparison into run
  evidence is a later round" — so the deferral is honest in the code and
  invisible everywhere an operator would look. (b) The same Design section
  defines tier 1 as the files_hint AND the fence allow scope, while the only
  tier-1 producer, `apps/cli/commands/job_context_cmd.py:242`, passes
  `_task_files_hint(task)` alone, documented at that file's lines 8-13 and in
  the user guide. Neither gap is a defect of the code that exists — both are
  deliberate, both are documented at the source, and neither touches the
  feature's DONE sentence, which is about selection, shrink and the omissions
  record. What is missing is the operator-visible record that
  planner_reviewer_prompt.md §4.7 requires for a spec deviation. DECISION F107
  D1 lands in this round and states both deferrals; the reviewer resolves this
  finding at the R18 gate, once that text is verified on disk. OPEN.
- R-0292 (Medium, F107 R18, F107's own code against F107's own spec): an
  unparseable file that is NOT tier 1 is included with an EMPTY signature
  rendering and no omissions record, so the record does not explain why the
  model saw nothing for it. The feature file's Edge-cases section rules
  "Unparseable files: included-whole if tier 1 (better safe), signature-skipped
  WITH REASON otherwise". On disk the tier-3 loop
  (`packages/orchestration/context_compiler.py:820-831`) reads the file, calls
  `_signature_render_text` and appends the result to `chosen` without ever
  consulting `FileSignatures.parse_failed`; `_signature_render_text` (`:701-704`)
  returns `"\n".join(...lines)`, which is `""` when parsing failed, so the file
  lands in `included` claiming a `"signatures"` rendering with a near-zero token
  estimate while contributing no content at all. The same blind spot sits in the
  tier-2 over-cap path (`:807-818`): it records `"size"` / `"signatures"` but not
  that the signatures came back empty. `parse_failed` is computed by the
  extractor and then discarded by the selector. No test covers an unparseable
  non-tier-1 file — the selector suite at
  `tests/orchestration/test_context_compiler.py:574-842` never creates one.
  Fixed in THIS round rather than deferred: this is F107's own module
  contradicting F107's own Edge-cases clause, so AGENTS.md Scope Control does
  not bar the repair.
<<<END PAIR_LRF_TO>>>

PAIR_LRG is an APPEND: the TO's first line IS the FROM, the last line of the
R16 gate entry. The new gate entry goes directly beneath it.
<<<BEGIN PAIR_LRG_FROM>>>
  `LAST_REVIEWED_SHA` advances 513a8c58 -> 5c808a59.
<<<END PAIR_LRG_FROM>>>
<<<BEGIN PAIR_LRG_TO>>>
  `LAST_REVIEWED_SHA` advances 513a8c58 -> 5c808a59.
- Reviewer gate on R17 (2026-08-12): PASS. Range `5c808a59..54d05e37` = five
  commits over five paths, every one under `.agent/`: `git diff --stat
  5c808a59..HEAD -- packages apps tests docs README.md` is EMPTY. Insertions per
  commit 285, 214, 72, 13 and 94, each far under 500. Transport by the PRIMARY
  shape, because the reviewer's original survives on disk:
  `.remedy-wt/f107-r17-1.block.md` carries BLOCK_SHA256
  6b91d4fcc89f8c67ac4f8a51ea8b5453969dcd603117109f96c77e576511a3d6 on the
  trailer one line past its saved region, `head -n -1` over that file recomputes
  exactly that digest, and `.agent/authored/f107-r17-1.md` and
  `.agent/last_block.md` both hash to it at 285 lines with `cmp` exit 0 and
  silent. `git show --numstat 40e5bf7b -- .agent/live_review.md` is `72 1`;
  `sha256sum .agent/plan.md` is
  d40eabc5d461b094b53b462c9b0dc9215f92e36072124dadd26d5a8608ae9f29 at 29 lines.
  On the files after: `^<<<` 0 in live_review, plan and handoff, `^## Steps` 1,
  `^Done:` 10, `^Landed:` 0, `Next free ID: R-0290` 1x, `^- R-0289` 1x. Every
  gate was RE-RUN by this reviewer rather than read from the handback: the canary
  `python3 -m pytest tests/cli/test_golden_path.py -q` returns 42 passed at exit
  0, and the FULL suite `python3 -m pytest -n auto -q` returns `5 failed, 16533
  passed, 19 skipped in 131.74s` — the same five R-0286 `[reviewer]` ids and the
  same three counts R16 recorded on this branch, which re-confirms closure
  precondition 2 rather than opening a new gate. `python3 -m apps.cli.grouped
  integrity check --json` returns `"passed": true` with 5 of 5 checks,
  `untracked=0, relevant=0` and no open blocker/high findings. `git status
  --porcelain` is empty, `git worktree list` shows the primary checkout alone,
  and `git rev-list --left-right --count origin/...v2...HEAD` is `0 0`. The
  126-line handoff is a declared D15 stated-cause overage carrying its mandated
  tables, which AGENTS.md permits. `.agent/STOP`, present when R17 handed back,
  is gone: the operator cleared it and started this session, which is guardrail
  G6 working rather than failing. Three findings are registered above from this
  gate — R-0290, R-0291 and R-0292 — the first two found by auditing this
  session's own start and the roadmap's Design bullets against the disk, the
  third by reading the selector's treatment of `parse_failed`.
  `LAST_REVIEWED_SHA` advances 5c808a59 -> 54d05e37.
<<<END PAIR_LRG_TO>>>

Commit, then push:
  chore(f107): register R-0290 to R-0292 and the R17 gate

C4 — the R-0292 repair, in `packages/orchestration/context_compiler.py` and
`tests/orchestration/test_context_compiler.py`. You write this code; the
specification is exact and the behaviour is what the tests must pin.

1. Add a fifth reason constant beside the existing four (which are at lines
   615-618), spelled exactly:
       OMISSION_REASON_UNPARSEABLE = "unparseable"
   Give it the same one-line WHY comment style the neighbouring constants use.
2. The selector must stop discarding `FileSignatures.parse_failed`. In BOTH
   non-tier-1 signature paths — the tier-2 over-cap path (currently lines
   ~807-818) and the tier-3 path (currently lines ~820-831) — obtain the
   `FileSignatures` object once (via `extract_file_signatures`), render the text
   from its `.lines`, and when `parse_failed` is True append
       OmissionRecord(rel_path, <that tier>, OMISSION_REASON_UNPARSEABLE, _OUTCOME_SIGNATURES)
   The file STILL goes into `chosen` with its `"signatures"` rendering — this
   adds a record, it does not drop the file. A tier-2 file that is BOTH over the
   inline cap AND unparseable gets BOTH records: the existing `"size"` record
   and the new `"unparseable"` one. Tier 1 is untouched: an unparseable tier-1
   file is still included whole with no record.
3. Keep the estimate and the rendering reading from the SAME `FileSignatures`
   object, so the "estimates are taken from the rendered text, never from the
   file" property that `_signature_render_text` documents still holds. If that
   makes `_signature_render_text` redundant at these two call sites, you may
   call the extractor directly there; do not delete the helper if anything else
   uses it, and do not change its behaviour.
4. If the module docstring enumerates the omission reasons, add the fifth there
   too. Change nothing else in that docstring.
5. Add exactly three tests to `tests/orchestration/test_context_compiler.py`,
   named for what they pin, in the style of the surrounding selector tests:
   (a) a tier-3 file that decodes as UTF-8 but does NOT parse as Python is in
       `compiled.included` with rendering `"signatures"` and an empty rendered
       text, AND `compiled.omissions` contains exactly one record for it with
       reason `"unparseable"` and outcome `"signatures"`;
   (b) a tier-2 file that is over the inline size cap AND unparseable carries
       BOTH records — one `"size"`, one `"unparseable"` — and no others;
   (c) an unparseable TIER-1 file is included whole and produces NO omission
       record at all.
   Use the existing fixture idioms in that file; do not invent a new helper if
   one already fits.
6. Do NOT touch `test_selector_defaults_and_reason_vocabulary_are_the_documented_values`
   except to add one line asserting `OMISSION_REASON_UNPARSEABLE == "unparseable"`.
   Every other assertion in that test stays exactly as it is.

Run, and record the real output:
  python3 -m pytest tests/orchestration/test_context_compiler.py -q
  python3 -m pytest tests/orchestration/test_context_compiler_e2e.py -q
  python3 -m ruff check packages/orchestration/context_compiler.py
Commit, then push:
  fix(f107): record an omission when a non-tier-1 file cannot be parsed

C5 — the reason vocabulary in the docs. Two REWRITE pairs, both short and both
unique in their file. In `docs/roadmap/features/T2_F107.md` replace the one line:
<<<BEGIN PAIR_FEAT_FROM>>>
  reason: budget|distance|binary|size}.
<<<END PAIR_FEAT_FROM>>>
<<<BEGIN PAIR_FEAT_TO>>>
  reason: budget|distance|binary|size|unparseable}.
<<<END PAIR_FEAT_TO>>>

In `docs/guides/job-context-view-user-guide-v0.md` make exactly two substring
replacements, each of which occurs exactly once in that file. Do NOT retype the
surrounding sentence — replace only these substrings, leaving every other byte
of those lines, including their quotation marks, untouched:
  (i)  replace   appears exactly once, either
       with      is accounted for: it appears
  (ii) replace   `binary`)
       with      `binary`, `unparseable`) — and a file demoted rather than
                 dropped appears under both
Replacement (ii) may be re-wrapped across lines to respect the file's wrap
width; it is prose, not an appliable hash-stamped text, and only these two
substitutions may change.
Commit, then push:
  docs(f107): name the unparseable omission reason in the guide and feature file

C6 — the DECISION. PAIR_DEC is an APPEND whose anchor is the current LAST
non-empty line of `.agent/decisions.md`; that anchor must remain exactly 1x and
must immediately precede the payload. The payload's first line is blank.
<<<BEGIN PAIR_DEC_ANCHOR>>>
conflict resolution.
<<<END PAIR_DEC_ANCHOR>>>
<<<BEGIN PAIR_DEC_TO_APPEND>>>

## DECISION F107 D1 (2026-08-12) — two Design bullets are DEFERRED, on the record

Context: finding R-0291. The feature file's Design promises that the compiled
context "becomes a registry segment with its manifest hash in evidence", and
defines tier 1 as the files_hint AND the fence allow scope. Neither holds on
disk. `register_compiled_context_segment` exists and is unit-tested but has no
production caller; the run path in `pingpong_loop.py` passes a rendered context
string and a category label, not a registered segment, and writes no manifest
into evidence. The CLI's tier 1 is the files_hint alone. Both gaps are
deliberate and documented at the source — `context_compiler.py:66-68` states
the deferral outright — but a deferral recorded only in a module docstring is
invisible to the operator, and §4.7 requires a spec deviation to be loud,
persisted and reversible.

Chosen: DEFER both, close F107 on its DONE sentence, and record the deferral
here and in the feature file's Built State. F107's DONE sentence is about
selection, shrink and the omissions record — all three are built, tested and
reviewed. Wiring the manifest into run evidence belongs with the evidence
schema, and merging fence allow-globs into tier 1 belongs with F017's fence
semantics; each is a round of its own with its own gate.

Alternatives considered: (a) wire both inside F107 — rejected, it widens a
feature already at seventeen rounds and drags F017 semantics into a context
feature; (b) amend the Design bullets to match the code — rejected, that edits
the target plan to fit what was built, which is exactly backwards, and the
capability is wanted, only later.

Reverse this decision by wiring `register_compiled_context_segment` into the
run path with its manifest recorded in evidence, and by merging the fence allow
scope into the CLI's tier-1 seed; the Design bullets then need no change,
because they already describe the intended end state.

## DECISION F107 D2 (2026-08-12) — the omission vocabulary gains a fifth reason

Context: finding R-0292. The Design enumerates the omission reasons as
`budget|distance|binary|size`. None of the four honestly describes a file that
decodes cleanly but cannot be parsed: it is not binary, not distant, not over a
size cap and not budget-demoted, yet its signature rendering is empty and the
record must say why.

Chosen: add `unparseable` as a fifth reason and amend the Design enumeration in
the same round as the code, so the plan and the disk never disagree. The word
appears in the feature file, the user guide and the module, and is pinned by
the vocabulary test that already guards the other four.

Alternatives considered: (a) reuse `binary` — rejected as dishonest, the file
decodes fine; (b) drop the file entirely instead of recording it — rejected, an
unparseable file's path and existence are still context the model can use, and
dropping it would lose more than it explains.

Reverse this decision by removing the constant and its three tests; the
Edge-cases clause "signature-skipped with reason" would then have no carrier
again, which is the state R-0292 recorded.
<<<END PAIR_DEC_TO_APPEND>>>
Commit, then push:
  chore(f107): record DECISION F107 D1 and D2

C7 — plan and handoff. Replace `.agent/plan.md` ENTIRELY with:
<<<BEGIN PAYLOAD_PLAN>>>
# Plan — F107 Context compiler v2

Branch: feature/f107-context-compiler-v2, cut from main at 2e4142c3.
Next free finding ID: R-0293. R17 reviewed PASS at 54d05e37.

## Goal
The context compiler selects fenced-path files, their direct import neighbors,
and only SIGNATURES of distant dependencies, under a total context token budget
with tier demotion — and writes an omissions record naming everything it left
out and why. DONE when a fixture repo's task context shrinks measurably versus
whole-files with the fixture task still solvable by the fake provider, and the
omissions record explains every exclusion
(docs/roadmap/features/T2_F107.md).

## Current Step
R18 — the pre-closure repair round. Three findings registered (R-0290 the
self-drive Phase 0 branch blind spot, R-0291 two deferred Design bullets,
R-0292 the unparseable non-tier-1 file), R-0292 repaired in F107's own module
with three new tests, the fifth omission reason `unparseable` carried into the
guide and the feature file, and DECISIONS F107 D1 and D2 recorded. T001-T004
are complete and reviewed; the integration gate ran at R16 and is GREEN, with
its evidence committed under `.agent/gate_f107_r16/`.

## Next Steps
1. R19 — the feature file's `## Built State` section, which closure
   precondition 4 requires and which does not exist yet, plus the R18 gate.
2. R20 — closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a
   FRESH review zip, the reviewer-authored STATUS line, the README capability
   sync in the same commit, then the PR. The five pre-existing `[reviewer]`
   failures (R-0286) are carried as a documented risk, so the closure verdict is
   PASS_WITH_RISKS.
3. The closure PR is never merged in the session that creates it; it merges at
   the next feature's start via the AGENTS.md Open PR Gate.
<<<END PAYLOAD_PLAN>>>

Then rewrite `.agent/handoff.md` (you author it) with: feature and round,
branch, the commit SHAs of C1-C6, a changed-files table, the item-status table
for C1-C7, the REAL results of gates A-K, the open-findings count, and the next
expected action. The state block repeats the operator brief's Fortschritt line
verbatim:
  Fortschritt: ~93 % (T001-T004 ✅ · Integration Gate ✅ · R18 Repair im Review · Built State + Closure offen) — Schätzung
Commit, then push:
  chore(f107): rewrite the plan and handoff for R18

GATES — run every one, record the real output and the real exit code
A transport: `wc -l .agent/authored/f107-r18-1.md`, its `sha256sum`, and `cmp`
  against `.agent/last_block.md` (silent, exit 0).
B block cap: the gate-A line count against the cap of 400 (DECISION F105 D5).
C pairs: after C3, in `.agent/live_review.md`: `Next free ID: R-0290` 0x,
  `Next free ID: R-0293` 1x, `^- R-0290` 1x, `^- R-0291` 1x, `^- R-0292` 1x,
  `Reviewer gate on R17` 1x. Both PAIR_LRF and PAIR_LRG are APPEND-shaped, so
  prove them as such: the FROM line stays exactly 1x, and every TO-ONLY line
  occurs exactly 1x AMONG THE LINES C3's OWN DIFF ADDS. Report added/removed
  from `git show --numstat <C3> -- .agent/live_review.md` and the count of
  added lines belonging to neither TO body (must be 0).
D feature file: `grep -c -F 'budget|distance|binary|size}.'
  docs/roadmap/features/T2_F107.md` is 0 and `grep -c -F
  'budget|distance|binary|size|unparseable}.'` is 1; `git show --numstat <C5> --
  docs/roadmap/features/T2_F107.md` is exactly `1 1`.
E guide: `grep -c -F 'appears exactly once, either'` is 0, `grep -c -F
  'is accounted for: it appears'` is 1, and `grep -c 'unparseable'` is at least
  1 in `docs/guides/job-context-view-user-guide-v0.md`.
F decisions: `grep -c -F 'conflict resolution.' .agent/decisions.md` is 1,
  `grep -c '^## DECISION F107 D1' .agent/decisions.md` is 1, `^## DECISION F107
  D2` is 1, and the payload's first non-blank line directly follows the anchor.
G marker leak: `grep -c '^<<<'` is 0 in `.agent/live_review.md`,
  `.agent/plan.md`, `.agent/handoff.md`, `.agent/decisions.md`,
  `docs/roadmap/features/T2_F107.md`,
  `docs/guides/job-context-view-user-guide-v0.md`,
  `packages/orchestration/context_compiler.py` and
  `tests/orchestration/test_context_compiler.py` (`grep -c` exits 1 on absence
  — that exit 1 is the pass).
H scoped suites: `python3 -m pytest tests/orchestration/test_context_compiler.py
  -q`, `python3 -m pytest tests/orchestration/test_context_compiler_e2e.py -q`,
  `python3 -m pytest tests/cli/test_job_context_cmd.py -q` and `python3 -m
  pytest tests/docs/ -q` — exit code and pass count for each. Report the
  test-count change in `test_context_compiler.py` (it was 61 collected before
  this round; three tests are added, so state the new number).
I canary: `python3 -m pytest tests/cli/test_golden_path.py -q`.
J lint: `python3 -m ruff check packages/orchestration/context_compiler.py
  tests/orchestration/test_context_compiler.py`.
K tree, push and scope: `git status --porcelain` empty, `git worktree list` the
  primary checkout alone, `git rev-list --left-right --count
  origin/feature/f107-context-compiler-v2...HEAD` is `0 0` after the last push,
  `git diff --name-only 54d05e37..HEAD` lists exactly the ten paths the Change
  line names, insertions per commit each under 500, and `gh pr list --state
  open` still returns an empty list.
── END OF BLOCK ─────────────
