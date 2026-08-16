── STEP R4 — F085 Sandbox hardening (stage 1) ────────────────

Goal:
Record the R3 PASS, register R-0493, then apply amendment F085 D1 to
`docs/roadmap/features/T2_F085.md`: correct the falsified "small number of
helpers" premise, re-slice T002 per command class, and rule the stage-1 command
classes and their policies. This is a RECORD + AMENDMENT round: no production
code, no test file, no new inventory work.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f085-r4.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/plan.md` whole file := the PLAN slice
  C2  `.agent/live_review.md` += the RECORD-R3 slice, then the R0493 slice
  C3  `docs/roadmap/features/T2_F085.md` := two replacements + the AMENDMENT
  C4  rewrite `.agent/handoff.md` (the handback)

Base:
This round starts from `fb346e8c1783b397f83f44bb1d7a317435c505f1`, the R3
handback commit and the current tip of `feature/f085-sandbox-hardening`. Every
range gate below names that SHA. Stay on this branch; do not create a new one.

Slice convention:
Each authored unit below sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each slice programmatically by its
markers and apply it byte-verbatim. No marker line ever reaches a target file.
The slices are PLAN, RECORD-R3, R0493, FROM1, TO1, FROM2, TO2 and AMENDMENT.
Every
slice's bytes end with a single trailing newline, and a whole-file slice is the
COMPLETE file including it.

Pair shapes, declared at authoring time (§4.9): FROM1→TO1 is a REWRITE — TO1
does not contain FROM1, it re-wraps the paragraph and keeps only its final
clause. FROM2→TO2 is a REWRITE with disjoint bodies. The AMENDMENT is not a
pair at all: it is an append to the end of the file.

──────────────────────────────────────────────────────────────

Change:

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f085-r4.md`. The reviewer's original is on disk at
   `.remedy-wt/f085-r4.md` and its expected sha256 is stated in the delegation
   that carries this block; copy that file rather than retyping it
   (`shutil.copyfile` is fine — the gate names the byte property, not the tool).
   Verify the digest BEFORE committing. Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f085-r4.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — `.agent/plan.md` whole file := the PLAN slice. Commit alone.

4. C2 — append to `.agent/live_review.md`, in this order, each preceded by
   exactly one blank line, both byte-verbatim, nothing else in the file touched:
   a. the RECORD-R3 slice;
   b. the R0493 slice.
   The pre-C2 content must remain a byte-exact PREFIX of the post-C2 content.

5. C3 — `docs/roadmap/features/T2_F085.md`, all three edits in ONE commit,
   in this order:
   a. replace the single occurrence of FROM1 with TO1;
   b. replace the single occurrence of FROM2 with TO2;
   c. append the AMENDMENT slice to the END of the file, preceded by exactly
      one blank line, so the file ends with the AMENDMENT's own trailing
      newline and nothing after it.
   Lines 1 and 2 of that file are parser-bound and must come out byte-unchanged.

6. C4 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Its
   state block repeats this Fortschritt line verbatim:
   `Fortschritt: ~10 % (F085 beansprucht · Seam-Inventar abgenommen · Amendment F085 D1 angewandt · T001/T002/T003 offen) — Schätzung`
   Its "Next" section states exactly this:
   - the next round is T001 — `exec_guard.py` mechanics plus the four runaway
     fixtures — and it is the first round of this feature to touch production
     code, so it is a SPLIT round under §3 Round-types;
   - there is NO open PR for this branch and none is opened before closure;
   - the R4 verdict is written by the NEXT round's record commit, not by this
     handback.

──────────────────────────────────────────────────────────────

Constraints:

1. AGENTS.md is the highest authority. Self-review loop before every commit;
   push after committing.
2. Every slice is applied BYTE-VERBATIM. If a slice cannot be applied as-is,
   stop and declare it — never adjust the bytes to make a gate pass.
3. The ONLY files this round may change are the six in the ordered bundle. No
   production code, no test file, NOT `.agent/f085_inventory.md`, NOT
   `docs/roadmap/STATUS.md`, and NOT `docs/roadmap/ROADMAP.md`, which AGENTS.md
   forbids editing without an explicit operator request.
4. Never force-push, never rebase, never amend, never reset, never work on
   `main`, never delete a branch. Do not create a PR.
5. Re-read `.agent/STOP` from disk before the FIRST commit and again at the
   handback. If it exists at either point, finish the commit in flight, write
   the handoff and end.
6. If any gate below is red, do not repair it by editing the thing it measures.
   Record the real command, the real exit code and the real output, and hand
   back. A red gate ends the round honestly.
7. `docs/roadmap/features/T2_F085.md` line 1 (the title line) and line 2 (the
   `**Tier 2 · Depends on: … · Blocks/used by: …**` line) are parsed by
   `tests/orchestration/test_roadmap_index.py`. Do not touch either.

──────────────────────────────────────────────────────────────

Done when — every command run from the repository root with `pwd` confirmed,
every real exit code recorded:

G1  `git status --porcelain` is EMPTY at the handback. `git worktree list` is
    ONE line. `.agent/STOP` absent at both readings.
G2  TRANSPORT: `.remedy-wt/f085-r4.md`, the committed `.agent/authored/f085-r4.md`
    and the committed `.agent/last_block.md` are byte-EQUAL and share one
    sha256. Report that digest, the byte count and the line count.
G3  `.agent/plan.md` at HEAD is byte-equal to the PLAN slice; report its sha256
    and line count; it contains `## Goal`, `## Next Steps` and a `\bF\d{3}\b`
    match, and is under 50 lines.
G4  `.agent/live_review.md`: the pre-C2 content is a byte-exact PREFIX of the
    post-C2 content, and the appended tail contains the RECORD-R3 slice and the
    R0493 slice, each byte-verbatim and each exactly once. Report
    `git show --numstat` for that path at C2 and confirm its deletion column
    is 0.
G5  Open-set recomputation at HEAD with the two regexes `^- R-\d+ — ` and
    `^Done: R-\d+ — `: report registered, resolved, duplicate ids and
    resolutions naming an unregistered id. REQUIRED: the set of OPEN ids at HEAD
    EQUALS the set open at `fb346e8c` PLUS exactly `R-0493`, and R4 resolves
    nothing. Report both counts and the symmetric difference rather than
    predicting them, plus the max id and the next free id. Separately report the number of
    LINE-START records matching `^Landed: R-\d+` — report the number you
    measure, do not predict it.
G6  `.agent/live_review.md` still contains the substring `Steps`.
G7  `.agent/f085_inventory.md` is BYTE-IDENTICAL to its content at `fb346e8c`.
    Report the sha256 at both commits; they must be equal.
G8  `docs/roadmap/features/T2_F085.md` after C3: FROM1 occurs 0 times and TO1
    exactly once; FROM2 occurs 0 times and TO2 exactly once; the AMENDMENT slice
    occurs exactly once and the file ENDS with it; `<<<` occurs 0 times in the
    whole file; and lines 1 and 2 are byte-identical to lines 1 and 2 at
    `fb346e8c`. Report each of these readings.
G9  `git diff --name-only fb346e8c..HEAD` lists exactly this set and nothing
    else: `.agent/authored/f085-r4.md`, `.agent/handoff.md`,
    `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
    `docs/roadmap/features/T2_F085.md`. Report the real list and flag any
    difference rather than editing to match. No path under `packages/`, `apps/`,
    `tests/` or `scripts/` may appear.
G10 `python3 -m pytest tests/docs/ -q` → exit 0. The reviewer measured
    `295 passed`, exit 0, at `fb346e8c` before ordering this gate.
G11 `python3 -m pytest tests/orchestration/test_roadmap_index.py -q` → exit 0.
    The reviewer measured `30 passed`, exit 0, at `fb346e8c`.
G12 `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q`
    → exit 0. Run in the PRIMARY checkout, not a worktree: the reviewer measured
    `157 passed`, exit 0, at `fb346e8c`, and the same command in a fresh
    worktree is red on `TestVitestFrontendTestFoundation::test_vitest_passes`
    because `apps/ui/node_modules` is gitignored and absent there — the known
    R-0480 mechanism, not a base red.
G13 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, the canary.
    The reviewer measured `42 passed`, exit 0, at `fb346e8c`.
G14 Per-commit insertions — the `+` column of `git show --numstat` — for C0a,
    C0b, C1, C2 and C3 only. None may exceed 500. C4's own insertion count
    cannot exist while C4's text is being written, so it is reported in your
    FINAL MESSAGE, the round report, and not in this file.
G15 `git log --format=%p fb346e8c..HEAD` shows one parent per commit (linear).
    `git reflog` over this round shows only `commit:` entries — no amend,
    rebase, reset, checkout of another branch, or force-push.
G16 STALENESS, a property gate and deliberately NOT a token count: the R3 PASS
    is on disk in `.agent/live_review.md` at HEAD as the RECORD-R3 paragraph,
    which G4 already measures, and the handback you write must not repeat R3's
    now-superseded statement that this branch's final round had been reached or
    that the R3 verdict lives only in the handoff. Both were true only while R3
    was planned as the last round; R4 falsified them. State in the handback that
    you checked for that statement and that it is absent. No string count is
    ordered here on purpose: a handback has to be free to describe this gate,
    and a gate that forbids a token its own report must name is the recurring
    defect DECISION F105 D8 exists to stop.

Handback:
Completion report + rewrite `.agent/handoff.md`. Push with
`git push origin feature/f085-sandbox-hardening`. Do NOT open a PR.

──────────────────────────────────────────────────────────────

<<<SLICE PLAN>>>
# Plan — F085 Sandbox hardening (stage 1)

Branch: feature/f085-sandbox-hardening, cut from origin/main at a5a70621 after
the F083 closure PR #202 and the amendment PR #203 merged.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
Builder-spawned commands stop relying on prompted discipline: every builder,
test and DoD subprocess gets POSIX resource limits, a per-command wall timeout,
output-size caps, a cwd pinned inside the worktree, an environment allowlist and
a default-deny network posture — with a document that says EXACTLY what stage 1
does and does not prevent. DONE when the limits provably kill a runaway fixture
(cpu, memory, oversized output, endless sleep) and classify it `resource_limit`
with the tripped limit named, an off-scope write attempt fails, well-behaved
commands behave identically under the guard, a secret-like parent env var never
reaches a child, and the limitations document exists and is linked from the
README.

## Current Step
R4, this round: record the R3 PASS, then apply amendment F085 D1 to
`docs/roadmap/features/T2_F085.md` — correct the falsified premise, re-slice
T002 per class, and rule the stage-1 command classes and their policies. No
production code and no test file is touched.

## Next Steps
1. T001 — `exec_guard.py` with rlimit, wall-timeout and output-cap mechanics
   plus the runaway fixtures (cpu, memory, output, sleep), each killed and each
   classified `resource_limit`. The wall timeout is the guard's OWN supervision:
   six of the seven timeout-less in-scope sites are `Popen`, which takes no
   `timeout=` keyword.
2. T002a-d — seam migration, one order per class, with behaviour-equality
   goldens and the environment-allowlist test.

## Risks
- 24 in-scope call sites in 18 modules and 22 enclosing functions is a far wider
  migration than the feature file assumed. T002 is four ordered sub-slices and
  none of them may widen into git, packaging or other.
- R-0202 has one reader and exactly two seams that drop the variable
  (`managed_builder_execution.py`:1160, `test_execution_service.py`:323). Naming
  them is not fixing them, and no round may fix them outside T002.
<<<END PLAN>>>

<<<SLICE RECORD-R3>>>
Gate: R3 — PASS. All twelve ordered gates reproduce at the reviewer's own hand, from the repository root at fb346e8c, and every measured value equals the one the handback reports. TRANSPORT, against the reviewer's OWN scratchpad original and NOT by digest fallback (§4.9): `.remedy-wt/f085-r3.md`, the committed `.agent/authored/f085-r3.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 77fb0d0ec4256a6d5145f58118eac49090c11df05827cba4e21d5d74206b19ee, 16976 B, 186 lines. `.agent/plan.md` at HEAD byte-equals the PLAN slice at sha256 05b3082b6f971b944d52dc84663d45bb366046abba1dcd99f94823f585be0479, 36 lines, 1970 B, carrying `## Goal`, `## Next Steps` and an F-id, under the 50-line cap. The C2 append is honest: the pre-C2 blob of 196461 B is a byte-exact PREFIX of the 202948 B post-C2 file, the RECORD-R2 and R0492 slices each occur exactly once in the whole file and both inside the 6487-byte, four-line appended tail, the numstat is `4 0` with a zero deletion column, and no transport marker reached a target file: measured at fb346e8c, before this paragraph existed, neither `.agent/plan.md` nor `.agent/live_review.md` contained a single slice-marker sequence. The open set moves by exactly one: 106 open at 2d492d49, 107 at HEAD, the symmetric difference of the HEAD open set against the base open set plus R-0492 is EMPTY, with 0 duplicate ids and 0 resolutions naming an unregistered id; max R-0492, next free R-0493. `.agent/f085_inventory.md` is byte-identical at base and at HEAD at sha256 fed207f9f8fb5a2de6a52a5366e1f3332eab1ae60c3a666cbddf4771f6c166bd, so R3 did not revise what R2 closed. The change set is exactly the five ordered `.agent/` paths with nothing under `packages/`, `apps/`, `tests/`, `scripts/` or `docs/`; the history is five single-parent commits and the reflog over the round is five `commit:` entries with no amend, rebase, reset or force-push; per-commit insertions are C0a 186, C0b 75, C1 12, C2 4 and C3 40 — the handback commit's own count, which could not exist while its text was being written and is recorded here instead — none over 500. Re-run by the reviewer in the PRIMARY checkout: the four state-file readers `157 passed` exit 0, the canary `42 passed` exit 0. The handback's self-measurement is honest: it declares 87 lines under DECISION D15 and it measures 87. One reading is stated rather than corrected, because the gate never defined it: G5's `Landed:` figure of 14 is a raw SUBSTRING count over the whole file, while the number of actual `^Landed: R-` RECORDS is 0 — all fourteen occurrences sit in prose inside five paragraphs that discuss the convention, so no unreviewed fix is hiding in the record. That is the R-0492 class read back against the very block that registered it, and it is answered by construction rather than by a second finding: R4's G5 orders the line-start regex, which is exactly the counter-measure R-0492 binds the reviewer to from R4 on. TERMINATOR CORRECTION, recorded because the disk must not keep a claim the session has falsified: the R3 block and the R3 handback both state that the R3 verdict lives only in the handoff, the round report and the PR under §4 item 13, because R3 was authored as this branch's last round. The session continued into R4, so R3 is NOT the last round of the branch, item 13 does not apply to it, and THIS paragraph is its on-disk gate entry. Item 13 still governs whichever round does end the branch.
<<<END RECORD-R3>>>

<<<SLICE R0493>>>
- R-0493 — Low, THE MANDATED DOCS-ROUND GATE IS VACUOUS FOR A FEATURE-FILE EDIT, SO A ROUND THAT AMENDS `docs/roadmap/features/**` IS GATED BY A COMMAND THAT CANNOT FAIL ON ITS OWN CHANGE. Raised by the reviewer at the R3 gate while assembling R4's gate list. docs/agents/planner_reviewer_prompt.md §3, verification tier 5, requires any round whose change set includes `docs/roadmap/**` to gate with `python3 -m pytest tests/docs/ -q`. Measured rather than assumed: `tests/docs/test_docs_consistency.py` reads `PRIMARY_DOCS` — `README.md`, `AGENTS.md`, `docs/README.md`, `docs/roadmap/STATUS.md` and `docs/roadmap/ROADMAP.md` — plus F012-specific assertions and the feature-detail FILENAME pattern, and asserts nothing whatever about the BODY of a feature detail file. Proven by a red control inside a disposable `git worktree` at fb346e8c, never in the primary checkout: with line 2 of `docs/roadmap/features/T2_F085.md` replaced by a malformed dependency line, `python3 -m pytest tests/docs/ -q` stayed GREEN at `295 passed`, while `python3 -m pytest tests/orchestration/test_roadmap_index.py -q` went RED at `11 failed, 19 passed`. The rule is right for its founding case — R-0151, where a STATUS.md ledger-count change broke the feature-ledger pins — and vacuous for the case it now most often meets, since AGENTS.md forbids editing `ROADMAP.md` without an explicit operator request and STATUS.md edits belong to closure, which leaves the feature detail file as the ordinary `docs/roadmap/**` change. Low, because nothing false was recorded and no round has yet passed on the strength of this gate alone; the cost is a round that believes itself gated and is not. That is the silently-vacuous-gate class of R-0438 reached by a different route: R-0438's gate named a path that did not exist, while this one names a path that exists and does not cover the change. Counter-measure, binding on the reviewer from this round on and APPLIED IN THE SAME BLOCK THAT REGISTERS THIS FINDING, as gate G11: a round whose change set touches `docs/roadmap/features/**` gates `python3 -m pytest tests/orchestration/test_roadmap_index.py -q` IN ADDITION to the mandated `tests/docs/` command, because that suite is the only one in the repository that parses those files. Promoting the rule into §3 tier 5 itself is a `docs/agents/**` edit outside this feature's change set and is NOT claimed here; it is named as work for the paydown branch that already carries R-0403, R-0448, R-0482, R-0487 and R-0490. OPEN.
<<<END R0493>>>

<<<SLICE FROM1>>>
All subprocess execution already flows through a small number of helpers
(test runner, DoD runners, provider transport, runtime harness) —
inventory them; stage 1 wraps THOSE seams with a common execution guard
rather than scattering limits. Fences already stop the APPLICATOR from
<<<END FROM1>>>

<<<SLICE TO1>>>
Subprocess execution does NOT flow through a small number of helpers. The R2
inventory (`.agent/f085_inventory.md`, AST-derived) measured 67 real call sites
in 33 files and 56 enclosing functions. The four classes this feature names —
provider transport (builder), test, DoD and runtime harness — hold 24 of those
sites across 18 modules and 22 enclosing functions, so stage 1 wraps 24 CALL
SITES with a common execution guard rather than four helpers; the amendment
section at the end of this file carries the ruling and the counts. Fences
already stop the APPLICATOR from
<<<END TO1>>>

<<<SLICE FROM2>>>
- **T002** seam migration (each subprocess helper adopts the guard, one
  order per seam, behavior-equality tests for well-behaved commands) +
  environment scrubbing with an allowlist test.
<<<END FROM2>>>

<<<SLICE TO2>>>
- **T002** seam migration, re-sliced against the measured shape (amendment
  F085 D1): one order per CLASS rather than per helper — **T002a** builder
  (5 sites), **T002b** test (12 sites), **T002c** DoD (2 sites), **T002d**
  runtime (5 sites, the differing policy). Behaviour-equality goldens for
  well-behaved commands in every sub-slice + environment scrubbing with an
  allowlist test. The git (24), packaging (11) and other (8 real) sites are
  NOT migrated in stage 1.
<<<END TO2>>>

<<<SLICE AMENDMENT>>>
## Amendment F085 D1 (2026-08-16) — measured seam shape, stage-1 classes

Ruled by the reviewer at the R2 gate under docs/agents/planner_reviewer_prompt.md
§4 item 7, applied here at R4. Reverse it by deleting this section and restoring
the two paragraphs it replaced (`git log -p` on this file). It changes SCOPE,
never the Goal & Done above.

### What the measurement found
`.agent/f085_inventory.md` tabled the 73 lines its defining grep prints, of
which 67 are real `subprocess.*` calls in 33 files and 56 enclosing functions.
The "small number of helpers" premise is FALSIFIED as written. Its SCOPE was
right and its SHAPE was wrong: the four named helpers do correspond to the four
classes worth guarding, but those classes hold 24 of the 67 sites spread over 18
modules and 22 enclosing functions — the 12 `test` sites alone live in 10
different modules. Measured gaps inside those 24: 7 pass no `timeout`, 1 passes
no `cwd`, 15 pass no `env`. Six of the seven timeout-less sites are `Popen`,
which accepts no `timeout=` keyword at construction, so the stage-1 wall timeout
MUST be the guard's own supervision of the child and can never be a forwarded
keyword. That is a design constraint, not a preference.

### Stage-1 command classes and their policies
A site's class is the PURPOSE its enclosing helper serves, not the binary it
happens to exec — the inventory's own rule, applied unchanged here.

| Class | Sites | Stage 1 | rlimits | wall timeout | output cap | cwd pinned | env allowlist | network |
|---|---|---|---|---|---|---|---|---|
| builder | 5 | yes | yes | yes | yes | yes | yes | default-deny |
| test | 12 | yes | yes | yes | yes | yes | yes | default-deny |
| dod | 2 | yes | yes | yes | yes | yes | yes | default-deny |
| runtime | 5 | yes | yes | NO | yes | yes | yes | allowed |
| git | 24 | no | — | — | — | — | — | — |
| packaging | 11 | no | — | — | — | — | — | — |
| other | 8 real | no | — | — | — | — | — | — |

The runtime class differs because its children are long-lived servers: a wall
timeout would kill the very harness the class exists to serve, and that harness
needs its port. It still takes rlimits, an output cap, a pinned cwd and the
environment allowlist.

git, packaging and other are OUT of stage 1. Their argv is authored by Remedy
itself rather than supplied by a project, so they are not the
prompted-discipline problem this feature names. That is a SCOPE ruling and NOT a
safety claim: several of those sites pass no `timeout` and can hang. The
limitations document (T003) says so explicitly; no round fixes them here.

### What this does not change
T001 and T003 keep their content. "Do not touch" is unchanged. The carried
finding R-0202 stays with T002 and is now a two-site question: of the 16 sites
that pass `env=`, only `managed_builder_execution.py`:1160 (via
`_build_sanitized_env`) and `test_execution_service.py`:323 (via
`_build_safe_env`) drop `REMEDY_UI_NO_AUTO_BUILD`; the other 14 build their
environment from `os.environ` and forward it unchanged.
<<<END AMENDMENT>>>
