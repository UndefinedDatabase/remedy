── STEP R9 — F085 Sandbox hardening (stage 1) ────────────────

Goal:
Record the R8 PASS, register the one finding the R8 gate produced against the
reviewer's own block, and fix it. R-0495 is fixed and R-0496 is resolved; this
round adds no behaviour and touches no production module. It exists because a
verdict that is not written down did not happen (planner_reviewer_prompt.md §4
item 13) and because the separator defect is one line and should not wait behind
the seam migration. T002a is NOT started here — it is R10's work and it needs its
own block.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f085-r9.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/live_review.md` += RECORD-R8, then R0500
  C2  `tests/orchestration/test_exec_guard.py` := the SEPARATOR pair applied
  C3  `.agent/live_review.md` += the LANDED-R0500 line
  C4  `.agent/plan.md` whole file := the PLAN slice
  C5  rewrite `.agent/handoff.md` (the handback)

Base:
This round starts from `b868401f6341946337f31c4eae593ef27133dbe7`, the R8 handback
commit and the current tip of `feature/f085-sandbox-hardening`. Every range gate
below names that SHA. Stay on this branch; do not create a new one.

Slice convention:
Each authored unit below sits between a `<<<SLICE NAME>>>` marker and a
`<<<END NAME>>>` marker, each occupying a line whose ENTIRE content is that
marker. Extract each slice programmatically by those marker LINES and apply it
byte-verbatim; a `<<<` that appears mid-line inside a slice is prose and never a
marker. No marker line ever reaches a target file. The slices are PLAN,
RECORD-R8, R0500, LANDED-R0500, SEPARATOR-FROM and SEPARATOR-TO. Every slice's
bytes end with a single trailing newline, and a whole-file slice is the COMPLETE
file including it.

Round type: SPLIT. The change set reaches `tests/`, so the reviewer gates and you
execute; the single-writer rule of docs/agents/self_drive_protocol.md is
unchanged — the reviewer writes nothing, you write everything.

──────────────────────────────────────────────────────────────

Change:

1. C0a — write this ENTIRE block, byte for byte, to `.agent/authored/f085-r9.md`.
   The reviewer's original is on disk at `.remedy-wt/f085-r9.md` and its expected
   sha256 is stated in the delegation that carries this block; copy that file
   rather than retyping it (`shutil.copyfile` is fine — the gate names the byte
   property, not the tool). Verify the digest BEFORE committing. Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f085-r9.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — append to `.agent/live_review.md`, in this order, each preceded by exactly
   one blank line, byte-verbatim, nothing else in the file touched:
   a. the RECORD-R8 slice;
   b. the R0500 slice.
   The pre-C1 content must remain a byte-exact PREFIX of the post-C1 content.

4. C2 — in `tests/orchestration/test_exec_guard.py`, replace the SEPARATOR-FROM
   slice with the SEPARATOR-TO slice. This pair is a REWRITE, not an append: the
   TO does not contain the FROM, because the byte that changes is the separator
   itself. FROM occurs exactly once in the file before the edit and zero times
   after. The ONLY difference between the two texts is one added newline; nothing
   else in the file, and no other file, is touched by this commit. Do not edit
   `packages/orchestration/exec_guard.py`.

5. C3 — append to `.agent/live_review.md`, preceded by exactly one blank line, the
   LANDED-R0500 slice byte-verbatim. It is a `Landed:` line and NOT a `Done:`
   paragraph: only reviewer-authored text sets Resolved
   (docs/agents/planner_reviewer_prompt.md §4 item 4), and the reviewer replaces
   this line with the authored resolution at the next gate.

6. C4 — `.agent/plan.md` whole file := the PLAN slice. Commit alone.

7. C5 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Its
   state block repeats this Fortschritt line verbatim:
   `Fortschritt: ~35 % (F085 beansprucht · Amendment F085 D1 angewandt · T001 gebaut · R8 PASS · R-0495 und R-0496 erledigt · T002 entsperrt, offen · T003 offen) — Schätzung`
   Its "Next" section states exactly this:
   - R10 starts T002a — the builder class, five call sites, the first seam
     migration — and needs its own block; nothing of it is started here;
   - `exec_guard.py` is UNCHANGED by this round and still has NO callers, so no
     containment claim holds for the running system;
   - `_StreamPump` still returns `b""` for a stream whose pump never reached EOF,
     so partial output is LOST on an incomplete drain; the `snapshot()` refinement
     is named in the plan and is not claimed here;
   - there is NO open PR for this branch and none is opened before closure;
   - the R9 verdict is written by the NEXT round's record commit.

──────────────────────────────────────────────────────────────

Constraints:

1. AGENTS.md is the highest authority. Self-review loop before every commit; push
   after committing.
2. Every slice is applied BYTE-VERBATIM. If a slice cannot be applied as-is, stop
   and declare it — never adjust the bytes to make a gate pass.
3. The ONLY files this round may change are the ones named in the ordered bundle.
   Do NOT touch `packages/orchestration/exec_guard.py`, `.agent/f085_inventory.md`,
   `.agent/context.md`, `docs/roadmap/STATUS.md`,
   `docs/roadmap/features/T2_F085.md` or `docs/roadmap/ROADMAP.md`.
4. DO NOT START T002a THIS ROUND, and do not "improve" anything else in the test
   file while you are in it. One finding, one pair, one commit.
5. Never force-push, never rebase, never amend, never reset, never work on `main`,
   never delete a branch. Do not create a PR.
6. Re-read `.agent/STOP` from disk before the FIRST commit and again at the
   handback. If it exists at either point, finish the commit in flight, write the
   handoff and end.
7. If any gate below is red, do not repair it by editing the thing it measures.
   Record the real command, the real exit code and the real output, and hand back.

──────────────────────────────────────────────────────────────

Done when — every command run from the repository root with `pwd` confirmed,
every real exit code recorded:

G1  `git status --porcelain` is EMPTY at the handback. `git worktree list` is ONE
    line. `.agent/STOP` absent at both readings.
G2  TRANSPORT: `.remedy-wt/f085-r9.md`, the committed `.agent/authored/f085-r9.md`
    and the committed `.agent/last_block.md` are byte-EQUAL and share one sha256.
    Report that digest, the byte count and the line count.
G3  `.agent/plan.md` at HEAD is byte-equal to the PLAN slice; report its sha256 and
    line count; it contains `## Goal`, `## Next Steps` and a `\bF\d{3}\b` match, and
    is under 50 lines.
G4  `.agent/live_review.md`: the pre-C1 content is a byte-exact PREFIX of the post-C1
    content and the pre-C3 content is a byte-exact PREFIX of the post-C3 content.
    The C1 tail contains the RECORD-R8 and R0500 slices and the C3 tail contains the
    LANDED-R0500 slice, each byte-verbatim and each exactly once in the WHOLE file.
    Report `git show --numstat` for that path at C1 and at C3 and confirm both
    deletion columns are 0.
G5  Open-set recomputation at HEAD with the two regexes `^- R-\d+ — ` and
    `^Done: R-\d+ — `: report registered, resolved, duplicate ids and resolutions
    naming an unregistered id. REQUIRED: the REGISTERED set at HEAD equals the
    registered set at `b868401f` PLUS exactly `R-0500`, with nothing lost, and the
    RESOLVED set is UNCHANGED at exactly `{R-0496}` — R9 resolves nothing, because
    a `Landed:` line is not a resolution. Report both counts and the symmetric
    difference rather than predicting them, plus the max id and the next free id.
    Separately report the number of LINE-START records matching `^Landed: R-\d+`,
    which must be exactly 1 and must name R-0500.
G6  `.agent/live_review.md` still contains the substring `Steps`.
G7  `git diff --name-only b868401f..HEAD` lists exactly this set and nothing else:
    `.agent/authored/f085-r9.md`, `.agent/handoff.md`, `.agent/last_block.md`,
    `.agent/live_review.md`, `.agent/plan.md`,
    `tests/orchestration/test_exec_guard.py`. Report the real list. NO path under
    `packages/`, `docs/`, `apps/` or `scripts/` may appear.
G8  UNCHANGED GUARD, the counter-proof to constraint 3: report the sha256 of
    `packages/orchestration/exec_guard.py` at `b868401f` and at HEAD. They must be
    equal — R8 fixed that file and this round adds nothing to it.
G9  PAIR SHAPE, a REWRITE: over the WHOLE of `tests/orchestration/test_exec_guard.py`
    at HEAD the SEPARATOR-FROM text occurs 0 times and the SEPARATOR-TO text occurs
    exactly 1 time. Report both counts and the `git show --numstat` of C2 for that
    path. Report also the size difference of that file between `b868401f` and HEAD,
    which must be exactly ONE byte.
G10 SEPARATOR MEASUREMENT, the property the fix exists for. In Python, over the
    WHOLE of `tests/orchestration/test_exec_guard.py` at HEAD, report the list
    `[len(m.group(0)) for m in re.finditer(r"\n+(?=@pytest\.mark\.subprocess)", text)]`.
    Every entry must be 3 — two blank lines before every decorated test. At
    `b868401f` the last entry is 2, which is the defect; report the base list too,
    so the reading is a comparison and not an assertion.
G11 DETERMINISM: run `python3 -m pytest tests/orchestration/test_exec_guard.py -q`
    TEN times in a row and report the real exit code AND the real summary line of
    EACH of the ten runs, in order. ALL TEN must be exit 0 and all ten must read
    `7 passed`. The reviewer measured exactly that, ten times out of ten, at
    `b868401f` — before this round's whitespace-only edit, which cannot change it.
G12 `python3 -m ruff check tests/orchestration/test_exec_guard.py` → exit 0, using
    the repository's OWN configuration. Do NOT pass `--isolated`: it discards
    `pyproject.toml` and with it the lint rules this gate exists to run (R-0463).
    Note what R-0500 records: this command was ALSO exit 0 before the fix, because
    stable ruff does not evaluate the blank-line rules at all, so a green reading
    here is not evidence about the separator and G10 is what measures it.
G13 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, the canary. The
    reviewer measured `42 passed`, exit 0, at `b868401f`.
G14 PROBE, not a colour — run the eight-file structural sweep THREE times and report
    each real exit code and each real summary line:
    `python3 -m pytest tests/orchestration/test_autonomy.py tests/regression/test_named_bugs.py tests/test_path_utils.py tests/test_data_paths.py tests/test_no_interactive_guard.py tests/orchestration/test_review_subject_resolution.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py -q -rf`
    The reviewer measured `350 passed, 6 skipped`, exit 0, three times out of three
    at `b868401f`. If a run is red, report the FAILED node id verbatim from `-rf`
    and hand back — that capture is what resolves R-0499. Do not repair it and do
    not re-run until it goes green.
G15 Per-commit insertions — the `+` column of `git show --numstat` — for C0a, C0b,
    C1, C2, C3 and C4 only. None may exceed 500. C5's own count is ordered nowhere
    and the reviewer measures it at the next gate (R-0494, checklist item 14).
    `git log --format=%p b868401f..HEAD` shows one parent per commit (linear), and
    `git reflog` over this round shows only `commit:` entries — no amend, rebase,
    reset, checkout of another branch, or force-push.

Verification tier: round gate (§3 tier 1) plus the canary at G13. The docs-round
gate of tier 5 is NOT triggered: this round's change set contains no
`docs/roadmap/**` path.

Handback:
Completion report + rewrite `.agent/handoff.md`. Push with
`git push origin feature/f085-sandbox-hardening`. Do NOT open a PR.

──────────────────────────────────────────────────────────────

<<<SLICE SEPARATOR-FROM>>>
    assert survivors == [], f"orphans survived run_guarded: {survivors}"

@pytest.mark.subprocess
def test_wall_timeout_bounds_the_call_when_a_descendant_escapes_the_group():
<<<END SEPARATOR-FROM>>>

<<<SLICE SEPARATOR-TO>>>
    assert survivors == [], f"orphans survived run_guarded: {survivors}"


@pytest.mark.subprocess
def test_wall_timeout_bounds_the_call_when_a_descendant_escapes_the_group():
<<<END SEPARATOR-TO>>>

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
R9, this round: record the R8 PASS, register R-0500 and fix it — the new test's
one-blank-line separator, which stable ruff does not evaluate. No production
module is touched and no behaviour changes.

## Next Steps
1. R10 starts T002a — the builder class, five call sites, the first seam
   migration. It is UNBLOCKED: `run_guarded` now bounds its own wall time, so a
   migrated seam makes a hang easier to see rather than harder.
2. `_StreamPump` gains a lock and a `snapshot()` so PARTIAL output survives a
   bounded drain. R8 returns `b""` for a stream whose pump never reached EOF,
   which `streams_complete` reports honestly but which loses bytes.
3. T002b-d, then T003 — network posture, limitations document, README link.

## Risks
- A stream still blocked at the grace deadline leaks one pipe read end and one
  daemon thread. Closing an fd under a blocked reader risks that thread reading a
  recycled fd after a later `open()`, so the leak is the cheaper wrong.
- The address-space limit is enforced but NOT attributable from `wait4` data;
  R5's G16 probe confirmed it. Whether stage 1 can name that trip stays open.
<<<END PLAN>>>

<<<SLICE LANDED-R0500>>>
Landed: R-0500 — the new test is now separated from the one above it by two blank lines, matching every other test in the file; the edit adds exactly one newline byte and changes no code; `tests/orchestration/test_exec_guard.py`, commit C2 of R9.
<<<END LANDED-R0500>>>

<<<SLICE RECORD-R8>>>
Gate: R8 — PASS, and the round that finally makes the guard bound its own runtime. Every one of the fifteen ordered gates was re-run by the reviewer from the repository root at b868401f and every one reproduces the handback's reading. TRANSPORT, against the reviewer's OWN scratchpad original and NOT by digest fallback (§4.9): `.remedy-wt/f085-r8.md`, the committed `.agent/authored/f085-r8.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 b89466df0a7caa60971c727be97ae1ab0de7478476fc7be391a0bdb63163dfde, 27927 B, 393 lines. `.agent/plan.md` at HEAD byte-equals the PLAN slice at sha256 a0bd751ab5087eea336976f65cc2aa62f79dddf74fbecbc672d6bf92ab2db1a5, 2235 B, 39 lines, under the 50-line cap, carrying `## Goal`, `## Next Steps` and an F-id. The C1 edit is exactly the shape the block ordered: the pre-C1 blob ends with the LANDED-R0496 line, stripping that line leaves 231729 B which is a byte-exact PREFIX of the 238429 B post-C1 file, and the 6700-byte remainder equals the DONE-R0496 slice, a blank line, the RECORD-R7 slice, a blank line and the R0499 slice, byte for byte — the reviewer reconstructed that remainder from its own scratchpad slices and compared bytes, rather than reading the worker's claim. The numstat is `5 1` and the single deletion is the retired `Landed:` line. The open set moved as ordered: 113 registered / 0 resolved at d37d1a1e against 114 / 1 at HEAD, registered delta exactly {R-0499} with nothing lost, resolved exactly {R-0496} against an empty base, 0 duplicate ids, 0 resolutions naming an unregistered id, max R-0499, next free R-0500, and the LINE-START `^Landed: R-\d+` count fell from 1 to 0 — the worker's marker retired into reviewer-authored text, which is what §4 item 4 asks for. The substring `Steps` survives 23 times. The change set is exactly the seven ordered paths with nothing under `docs/`, `apps/` or `scripts/`. THE FIX ITSELF, read as a diff and not as a summary: `run_guarded`'s `finally` no longer calls `out_pump.join()` and `err_pump.join()` untimed; it computes ONE `drain_deadline` from `policy.stream_drain_grace_seconds`, joins both pumps against that shared deadline so the grace is a total and not a per-stream cost, derives `streams_complete` from `is_alive()` on both, and closes `proc.stdout`/`proc.stderr` ONLY when the drain completed — the deliberate leak of a pipe read end under a still-blocked reader being cheaper than a recycled-fd read, which the added comment states where a reader will find it. `stream_drain_grace_seconds` and `streams_complete` are documented in their own dataclass docstrings, and the `run_guarded` docstring's old absolute claim "no descendant outlives this call" is narrowed to "no descendant of THAT GROUP", with the setsid escape named and attributed to R-0495. All seven pairs read as declared: GUARD5 and GUARD6 are rewrites with FROM 0x and TO 1x, GUARD1, GUARD2, GUARD3, GUARD4 and GUARD7 are appends with TO 1x, numstat `32 5`. The new test is present exactly once and the file ends with it. THE PROPERTY IS MEASURED, NOT ASSERTED: the reviewer reproduced R-0495 before ordering the fix — an escapee sleeping 20s under `wall_timeout_seconds=1.0` made the unfixed guard return after 20.13s — and the fixed guard returned after 6.00s, the 1.0s deadline plus the 5.0s grace, with `streams_complete=False` and no surviving process. Ten consecutive runs of `python3 -m pytest tests/orchestration/test_exec_guard.py -q` at the reviewer's own hand are ten exits of 0 and ten `7 passed` summaries between 7.62s and 7.66s, and the worker's independent ten are the same. The red control is decisive and the reviewer ran it too, in a disposable worktree: replacing the bounded join with `pump.join()` turns the suite red at exactly one node, `test_wall_timeout_bounds_the_call_when_a_descendant_escapes_the_group`, on `assert result.streams_complete is False` — so the new test detects the very regression it was written for, and the gate can fail honestly. `grep -rn "exec_guard"` over packages, apps, scripts and tests still names exactly one file, the test file, so constraint 4 held and NO call site was migrated: the running system is still unprotected and no containment claim may be made from this round. Ruff is exit 0 under the repository's own configuration; the canary is `42 passed in 20.48s`, exit 0; the eight-file sweep is `350 passed, 6 skipped`, exit 0, three times out of three, so R-0499 gained no new observation. Per-commit insertions are C0a 393, C0b 268, C1 5, C2 32, C3 35 and C4 12, none over 500, and the history is seven single-parent commits 988869c6←d37d1a1e through b868401f with a reflog of `commit:` entries only. The values R8 routed nowhere are recorded HERE, measured by the reviewer at b868401f (R-0494): the handback commit b868401f inserted 45 lines and deleted 44, `.agent/handoff.md` measures 104 lines against its own DECISION D15 declaration of 104 so its self-measurement is honest, `git status --porcelain` is EMPTY, `git worktree list` is one line, and origin carries b868401f with no PR open. The round's eight declared deviations were all checked and all are accurate; deviation 5 is the honest declaration of a real defect the reviewer caused, and it is registered as R-0500 rather than held against the round. LAST_REVIEWED_SHA advances to b868401f.
<<<END RECORD-R8>>>

<<<SLICE R0500>>>
- R-0500 — Low, A BLOCK ORDERED "PRECEDED BY EXACTLY ONE BLANK LINE" FOR AN APPEND WHOSE TARGET WAS A TOP-LEVEL PYTHON DEFINITION, WHICH THE LANGUAGE SEPARATES BY TWO. Raised by the reviewer against its own R8 block at the R8 gate. Change item 5 of that block ordered the NEW-TEST slice appended "preceded by exactly one blank line", and the worker applied it exactly, so `tests/orchestration/test_exec_guard.py` now separates its last test from the one above by ONE blank line while all its other tests are separated by TWO. The worker was right not to adjust the bytes — constraint 2 forbids it — and right to declare it, which it did as deviation 5. The wording came from the `.agent/live_review.md` appends in the same block, where one blank line IS the convention, and was reused for a Python file without re-reading what the target file's own layout demands; that reuse is the defect. Lint does not catch it and cannot be relied on to: `ruff check` was exit 0 both before and after, because pycodestyle's blank-line rules E301-E306 are preview-only in stable ruff and the repository selects `["E", "F", "W", "I", "UP"]` without preview, so those rules are never EVALUATED rather than merely unreported — the same shape as R-0463, where `--isolated` made a probe blind rather than wrong. The cost is one line of churn and this finding; nothing was mismeasured and no gate passed falsely, which is why it is Low. Counter-measure, binding on the reviewer from this round on: a block that orders an APPEND into a source file states the separator the TARGET LANGUAGE requires and never a generic blank-line count carried over from a prose or state file — and where the separator itself is the thing being fixed, the gate MEASURES it directly, as G10 of the block registering this finding does, rather than resting on a linter that does not evaluate the rule. Promoting the rule into the docs/agents/planner_reviewer_prompt.md §3 pre-emission checklist is a `docs/agents/**` edit outside this feature's change set and is NOT claimed here; it is named for the paydown branch that already carries R-0403, R-0448, R-0482, R-0487, R-0490, R-0493, R-0494, R-0497 and R-0498. OPEN.
<<<END R0500>>>
