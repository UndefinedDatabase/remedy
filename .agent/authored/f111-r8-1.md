── STEP R8/4 — F111 Diff-only repair — T002a: the diff response record ───────
Goal:        Persist the R7 gate and finding R-0307, fix the stale
             live_review header, and build the RESPONSE-SIDE half of T002:
             the versioned diff-repair response record, its validation with
             a declared-files cross-check, and a non-raising fence pre-check
             that rejects an out-of-fence path BEFORE the applicator runs.
             The apply/fallback half of T002 is R9 and is NOT in this round.
Bundle:      C1 block save; C2 last_block mirror; C3 gate+finding append;
             C4 header fix + Landed line; C5 structured_patch helpers;
             C6 diff_repair_response module + tests; C7 plan + handoff.
             Commit AND push at every item.
Change:      EXACTLY these paths and nothing else:
             .agent/authored/f111-r8-1.md (new), .agent/last_block.md,
             .agent/live_review.md, .agent/plan.md, .agent/handoff.md,
             packages/orchestration/structured_patch.py,
             packages/orchestration/diff_repair_response.py (new),
             tests/orchestration/test_diff_repair_response.py (new).
Constraints: AGENTS.md in full. Apply every authored slice by READING ITS
             SCRATCH FILE (`cat` / `cp`) — never retype, never reflow.
             Do NOT touch `.agent/candidates.md` or `.agent/decisions.md`.
             Do NOT touch `packages/orchestration/diff_repair.py`,
             `review_scope.py`, `source_apply.py`, `builder_bridge.py`,
             `repair_context.py` or `pingpong_loop.py`.
             Write no `Done:` line: only reviewer-authored text sets
             Resolved (docs/agents/planner_reviewer_prompt.md §4.4). The
             ONE `Landed:` line C4 orders is the worker's correct marker.

PROCEDURE (in order; commit AND push at every numbered item):

0. Preconditions: `git status --porcelain` empty; branch is
   feature/f111-diff-only-repair; `git log -1 --format=%h` is 023e8d9d.
   Any mismatch => STOP and hand back.
   `mkdir -p .remedy-wt/f111r8`.

1. C1 — Save this ENTIRE step block (from the `── STEP R8/4` line through
   the final `Handback:` line, byte for byte) to
   `.remedy-wt/f111r8/BLOCK`, then `cp .remedy-wt/f111r8/BLOCK
   .agent/authored/f111-r8-1.md`; `cmp` the two — must be silent.
   Commit: chore(f111): save the R8 step block verbatim   -> push

2. C2 — `cp .agent/authored/f111-r8-1.md .agent/last_block.md`; `cmp`
   silent.
   Commit: chore(f111): mirror the R8 block into last block   -> push

3. C3 — GATE AND FINDING FIRST. Write the slice delimited below by
   `<<<LRG_BEGIN` and `<<<LRG_END` (those two marker lines are NOT part of
   the slice) to `.remedy-wt/f111r8/LRG`, then
   `cat .remedy-wt/f111r8/LRG >> .agent/live_review.md`.
   PURE APPEND: `git show --numstat <C3> -- .agent/live_review.md` must
   read `36 0`. A nonzero delete column means a rewrite: STOP and hand back.
   Commit: chore(f111): record the R7 gate and finding R-0307   -> push

<<<LRG_BEGIN

### R7 — PASS (2026-08-13)
Reviewed by the main session of the next self-drive session over
b1e5cc7e..023e8d9d, a state-only round. Section 4.13 does not apply here: a
new session CAN gate the round that closed the previous one, and this entry is
that gate. Every command was re-run by the reviewer, never read off the
handback. Transport: PRIMARY cmp proof, no digest fallback —
`.remedy-wt/f111r7/BLOCK` and `.agent/authored/f111-r7-1.md` are
byte-identical, that file and `.agent/last_block.md` are byte-identical,
`sha256sum .remedy-wt/f111r7/LRG` reproduces the stated digest ending
d49c182, and a `str.count` of that slice against `.agent/live_review.md`
prints 1. Append purity by numstat: `50 0` for the findings commit and `2 2`
for the plan pair. Markers on the final file: 31 `- R-0`, 4 `Done:`, 0
`Landed:` (exit 1, the pass), 1 `### R6 — PASS`. Plan: the retired id 0x
(exit 1, the pass), `Next free finding ID: R-0307` 1x, `Open findings: 27`
1x, 46 lines. Handoff: 76 lines carrying the DECISION D15 stated-cause line
that names 76, and 1 `^Fortschritt: ` line. Tests: `python3 -m pytest
tests/orchestration/test_test_runner.py -q -k 'plan_md or context_md'` exit 0,
3 passed 48 deselected; `python3 -m pytest tests/cli/test_golden_path.py
tests/orchestration/test_diff_repair.py -q` exit 0, 72 passed — the 42 canary
plus the 30 T001 tests, unchanged, as a round that touches no code requires.
Hygiene: `git status --porcelain` empty, `git worktree list` one entry,
per-commit insertions 109/71/50/2/45 each under 500, `git rev-list
--left-right --count origin/feature/f111-diff-only-repair...HEAD` prints
`0 0`. Scope: exactly the five ordered paths; no production, test or docs
file was touched.

- R-0307 (Low, F111 R7, stale live-looking header): the header of
  `.agent/live_review.md` names a next-free finding id that the body has long
  overtaken — the findings below it run past it by four — so the file's own
  header contradicts its body, and a reader who trusts it would reuse ids
  already allocated. It was true when the file was reset and nothing updates
  it, which is the R-0228 class: a line that positively CLAIMS a live value it
  does not track. The fix is not to refresh the number, because the next round
  would stale it again, but to stop the header carrying a counter at all —
  `.agent/plan.md` already holds it and is rewritten every round. OPEN.
<<<LRG_END

4. C4 — TWO edits to `.agent/live_review.md`, nothing else in that file.
   (i) REWRITE pair. The FROM string occurs EXACTLY 1x in the file today
       (verified at authoring time by `grep -c`), on line 8.
       FROM (one line):
> Branch: feature/f111-diff-only-repair. Next free ID: R-0298.
       TO (two lines):
> Branch: feature/f111-diff-only-repair. The next free finding ID is not
> tracked in this header: `.agent/plan.md` holds it and is rewritten each round.
   (ii) APPEND at the very end of the file: one blank line, then exactly:
Landed: R-0307 — the live_review header no longer carries a finding-id counter, commit <C4 short sha>.
   Replace `<C4 short sha>` with this commit's own short sha only if you can
   do so without amending; otherwise write `commit C4 of R8` and say so in
   the handback.
   `git show --numstat <C4> -- .agent/live_review.md` must read `4 1`.
   Commit: chore(f111): stop the live review header tracking finding ids -> push

5. C5 — `packages/orchestration/structured_patch.py`. Two ADDITIVE public
   helpers plus the two call-site swaps that make them the single reading.
   Behaviour must be IDENTICAL; the pin is stated in gate (f).
   (i) Add a module-level constant directly above `def
       parse_structured_patch`, hoisting the regex that function already
       uses inline:
       `_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*\n(\{[\s\S]*?\})\s*\n```")`
       and change that function's first statement to use
       `_JSON_FENCE_RE.search(raw_output)`. Nothing else in the function.
   (ii) Add a public `extract_json_object(raw_output: str) -> str | None`
        returning the first JSON object's TEXT: the fenced block if
        `_JSON_FENCE_RE` matches, else — when the stripped text starts with
        `{` — `_extract_first_json_object(stripped) or stripped`, else None.
        It returns TEXT, not a parsed value, so each caller decides what
        schema that object must satisfy. One-line WHY comment directly above
        the definition, per AGENTS.md Code Discoverability.
   (iii) Add a public `unsafe_path_issues(paths: Iterable[str]) -> list[str]`
         holding EXACTLY the three path-safety checks `validate_structured_patch`
         performs today — absolute path, `..` traversal, and the
         `.env/.pem/.key/.p12` suffix set — with the SAME message strings,
         and make `validate_structured_patch` call it instead of looping
         itself. The messages are part of the contract: do not reword them.
   (iv) Extend the `Public API::` docstring block at the top of the file with
        the two new names.
   Commit: feat(f111): expose the json object and path safety helpers -> push

6. C6 — NEW `packages/orchestration/diff_repair_response.py` plus NEW
   `tests/orchestration/test_diff_repair_response.py`, in ONE commit (the
   repo's convention for this feature: commit 83aec443 landed source and
   tests together).
   The module is the RESPONSE side of diff-only repair. Its module docstring
   states, in prose you write: that the record is
   `{"format": "unified_diff", "version": 1, "diff": "...", "files": [...]}`;
   that the declared `files` list is cross-checked against the paths the diff
   itself touches BEFORE anything reaches the applicator; that this module
   holds NO unified-diff parser, because paths come from
   `review_scope.parse_diff_line_ranges`, the repository's single reading of
   hunk headers; that it holds NO fence policy, because the decision is
   `scope_fences.check_change_set` against the effective spec, called in its
   NON-RAISING form so an out-of-fence path is a validation rejection rather
   than an exception thrown out of the applicator; and — as a deliberate
   absence, AGENTS.md Code Discoverability — that Remedy deliberately does
   not convert a response to a `StructuredPatch` in this half, because a
   `files` list longer than one entry has no correct conversion until the
   per-path diff split is designed (R9 owns it). Then a `Public API::` block.
   Every public definition carries the one-line WHY comment directly above it.

   Public surface, exactly:
     DIFF_REPAIR_RESPONSE_FORMAT = "unified_diff"
     DIFF_REPAIR_RESPONSE_VERSION = 1
     @dataclass(frozen=True) DiffRepairResponse:
         diff: str ; files: tuple[str, ...] ;
         format: str = DIFF_REPAIR_RESPONSE_FORMAT ;
         version: int = DIFF_REPAIR_RESPONSE_VERSION
     @dataclass(frozen=True) DiffFencePrecheck:
         allowed: bool ; denied_paths: tuple[str, ...] ;
         reasons: tuple[tuple[str, str], ...]   # (path, reason), sorted
     parse_diff_repair_response(raw_output: str)
         -> tuple[DiffRepairResponse | None, str]
     validate_diff_repair_response(response: DiffRepairResponse) -> list[str]
     precheck_diff_repair_fences(repo_root: Path, response: DiffRepairResponse,
                                 *, job_fences: dict | None = None)
         -> DiffFencePrecheck

   parse_diff_repair_response: locate the object with
   `structured_patch.extract_json_object` (C5) — this module MUST NOT
   contain a second JSON-wrapper reading. Return `(None, reason)` with these
   exact reason strings, checked in this order:
     "no_json_object"            nothing to decode
     "invalid_json"              json.loads raised
     "not_an_object"             decoded value is not a dict
     "missing_field:format" / ":version" / ":diff" / ":files"
     "wrong_format:<value>"      format is not DIFF_REPAIR_RESPONSE_FORMAT
     "unsupported_version:<value>"  version is not DIFF_REPAIR_RESPONSE_VERSION
     "files_not_a_list"          files is not a list or tuple
   On success return `(DiffRepairResponse(...), "")` with `files` a tuple of
   `str(...)` entries and `diff` `str(...)`.

   validate_diff_repair_response returns a list of issue strings, empty when
   valid, and MUST reuse `structured_patch.unsafe_path_issues` for path
   safety rather than restating those rules. Issues:
     "empty diff" when diff is empty or whitespace only
     "empty files list" when files is empty
     every string `unsafe_path_issues(response.files)` returns
     f"declared path not touched by the diff: {path}" for each declared path
       absent from the diff's touched paths
     f"diff touches undeclared path: {path}" for each touched path absent
       from the declared list
   Touched paths come from `parse_diff_line_ranges(response.diff)` keys.
   Both cross-check lists are emitted in sorted order so the same input
   always yields the same issue list.

   precheck_diff_repair_fences: `resolve_fence_spec_effective(repo_root,
   job_fences=job_fences)`, build one `TouchedPath(path=p,
   operation="modify", role="target")` per declared file, call
   `check_change_set(repo_root, effective.spec, touched)`, and map its
   result into `DiffFencePrecheck` — `denied_paths` and `reasons` taken from
   `result.violations`, which `check_change_set` already returns sorted.
   It raises nothing.

   The test file covers AT LEAST these cases, each a separate test:
     parse: fenced ```json block; bare object; bare object with trailing
       prose; prose only -> "no_json_object"; broken json inside a fence ->
       "invalid_json"; each of the four missing fields ->
       "missing_field:<name>"; format "file_ops" -> "wrong_format:file_ops";
       version 2 -> "unsupported_version:2"; files as a string ->
       "files_not_a_list".
     validate: a response whose declared list equals the diff's touched paths
       -> []; a diff touching a path not declared -> exactly the
       "diff touches undeclared path" issue; a declared path the diff never
       touches -> exactly the "declared path not touched" issue; empty diff;
       empty files list; an absolute declared path, a `..` declared path and
       a `.env` declared path -> the messages `unsafe_path_issues` produces
       (assert on the message text, so a future reword of those strings
       fails here rather than silently).
     precheck: under `tmp_path` as repo_root with default fences, a normal
       path such as `src/app.py` -> allowed True and empty denied_paths;
       `remedy.toml`, which `scope_fences.BUILTIN_DENY` denies and no allow
       glob can override -> allowed False with that path in denied_paths and
       a non-empty reason; with `job_fences={"allow": ["src/**"], "deny": []}`
       a path outside that allow glob -> allowed False.
   Use `tmp_path` for every filesystem need; create no file outside it.
   Commit: feat(f111): add the versioned diff repair response record -> push

7. C7 — `.agent/plan.md` FULL REPLACEMENT with the slice delimited below by
   `<<<PLAN_BEGIN` and `<<<PLAN_END` (marker lines excluded). Write it to
   `.remedy-wt/f111r8/PLAN` first, then `cp .remedy-wt/f111r8/PLAN
   .agent/plan.md`; `cmp` silent. It is 48 lines — do not reflow it.
   Then rewrite `.agent/handoff.md` in YOUR OWN text. COUNT THE LINES
   BEFORE COMMITTING (`wc -l`): 60 or fewer, or carry a DECISION D15
   "Deviations, declared" line naming the REAL measured count and the
   mandated content that caused it. It must contain: feature and round
   (F111 R8); the branch; a per-commit SHA table for C1-C7 with insertions;
   a changed-files table; the real gate results below with commands and real
   exit codes; open findings 28 with next free id R-0308; an item-status
   table over C1-C7 whose Status cells carry the SAME status you declare in
   the handback — `done`, `skipped` with reason, or `deviated` with reason,
   never a bare `done` over a deviation you reported elsewhere (finding
   R-0306); this line verbatim, on its own line (finding R-0304):
Fortschritt: ~50 % (T001 ✅ · T002 halb: Response-Record ✅, Apply+Fallback offen · T003 offen) — Schätzung
   and a NEXT SESSION block stating, in this order: that the branch is
   UNMERGED and has NO PR by design; that the next action is R9, the apply
   half of T002; and that NOTHING imports `diff_repair.py` or
   `diff_repair_response.py` yet — both are seams and T003 wires them.
   plan.md and handoff.md land in ONE commit.
   Commit: chore(f111): rewrite the plan and handoff for R8   -> push

<<<PLAN_BEGIN
# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged. Last reviewed SHA: 023e8d9d (R7 PASS). Next free finding
ID: R-0308. Open findings: 28, none above Medium.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
T002 is HALF built and has NO CALL SITE. The response record landed
this round in `packages/orchestration/diff_repair_response.py`: the
versioned `{format, version, diff, files}` shape, its parse, a
validation that cross-checks the declared `files` list against the
paths the diff really touches, and `precheck_diff_repair_fences`,
the non-raising fence decision that rejects an out-of-fence path
BEFORE the applicator is called. `structured_patch.py` gained the
two helpers this reuses, `extract_json_object` and
`unsafe_path_issues`, so neither the JSON-wrapper reading nor the
path-safety rules exist twice. Nothing imports the new module: T001
and T002 are both seams, and T003 wires both.

## Next Steps
1. R9 — the apply half of T002: convert a validated response to a
   `StructuredPatch`, apply strictly through `apply_structured_patch`,
   and on ANY hunk conflict discard the attempt whole, record
   `fallback_reason`, and report mode `full_fallback` with the
   touched files byte-identical to their pre-attempt state.
2. T003 — wire `changed_line_ranges_from_patch` and the response
   channel into `run_builder_bridge_loop`, emit mode and token
   evidence per repair round, add the fixture token comparison.
3. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- `review_scope._parse_diff` and `source_apply._apply_hunks` already
  exist and must be reused, never duplicated. `parse_diff_line_ranges`
  is the ONLY sanctioned reading of hunk headers outside
  `review_scope` itself.
- A `files` list with more than one entry has no correct conversion
  yet: giving each path the whole diff text would apply every hunk to
  every file. R9 owns it.
<<<PLAN_END

Done when (record command + real exit code + counted value; never the word
"green"):
  a. `cmp .remedy-wt/f111r8/BLOCK .agent/authored/f111-r8-1.md` silent;
     `cmp .agent/authored/f111-r8-1.md .agent/last_block.md` silent;
     `cmp .remedy-wt/f111r8/PLAN .agent/plan.md` silent.
  b. `git show --numstat <C3> -- .agent/live_review.md` -> `36 0`
     `git show --numstat <C4> -- .agent/live_review.md` -> `4 1`
  c. on the final `.agent/live_review.md`:
     `grep -c '^- R-0'` -> 32 ; `grep -c '^Done:'` -> 4
     `grep -c '^Landed:'` -> 1 ; `grep -c '^### R7 — PASS'` -> 1
     python3 -c "import pathlib;print(pathlib.Path('.agent/live_review.md').read_text().count(pathlib.Path('.remedy-wt/f111r8/LRG').read_text()))"
     -> exit 0, printed count 1
  d. the header edit landed: `sed -n '8,9p' .agent/live_review.md` written to
     `.remedy-wt/f111r8/HDR_ACTUAL`, and `cmp` against a
     `.remedy-wt/f111r8/HDR` holding the two TO lines -> silent.
  e. on `.agent/plan.md`: `wc -l` -> 48 ; `grep -c '^## Goal'` -> 1 ;
     `grep -c '^## Next Steps'` -> 1 ; `grep -c 'R-0308'` -> 1.
     `wc -l < .agent/handoff.md` -> the real number, 60 or fewer unless the
     D15 line declares it; `grep -c '^Fortschritt: ' .agent/handoff.md` -> 1
  f. behaviour pin for C5: `python3 -m pytest
     tests/orchestration/test_source_apply.py
     tests/orchestration/test_source_apply_transaction.py
     tests/orchestration/test_fence_e2e.py -q` -> exit 0, 174 passed, the
     SAME count this reviewer measured at HEAD before the round.
  g. `python3 -m pytest tests/orchestration/test_diff_repair_response.py -q`
     -> exit 0, report the real count.
     `python3 -m pytest tests/orchestration/test_diff_repair.py -q` -> exit 0,
     30 passed, unchanged: this round does not touch that module.
     `python3 -m pytest tests/cli/test_golden_path.py -q` -> exit 0, 42
     passed (canary). Do NOT run tests/ui_server/test_dashboard_contract.py
     (R-0221: it runs a real npm build).
  h. `python3 -m pytest tests/test_path_utils.py tests/test_data_paths.py -q`
     -> exit 0, report the real count. These two files rglob every
     `packages/**/*.py`, so the NEW module is inside their reach; they are
     the guard that it introduces no second copy of the path regex, no
     `_MAX_PATH_COMPONENT_LENGTH`, and no direct `REMEDY_DATA_DIR` read.
  i. red-proof, inside a DISPOSABLE `git worktree` at HEAD and nowhere else:
     in that worktree only, make `validate_diff_repair_response` skip the
     "diff touches undeclared path" branch entirely, run
     `python3 -m pytest tests/orchestration/test_diff_repair_response.py -q`
     and record the real exit code and the failing test ids; then remove and
     prune the worktree. If the mutation does NOT go red, say so plainly —
     that is a true report about an unreachable branch, not a failure.
  j. `git status --porcelain` -> empty; `git worktree list` -> one entry;
     per-commit insertions each < 500;
     `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
     -> `0 0` after the final push.
Handback:    completion report (per-commit table, changed-files table,
             item-status table over C1-C7 with real statuses, raw gate
             results a-j with real exit codes) and `.agent/handoff.md`
             rewritten as C7. Do not merge, do not open a PR.
