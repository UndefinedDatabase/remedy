── STEP R7 — F085 Sandbox hardening (stage 1) ────────────────

Goal:
Record the R6 PASS, register the one finding the R6 gate produced against the
reviewer's own block, and fix R-0496 so that `tests/orchestration/test_exec_guard.py`
stops being a coin flip. R-0495 is NOT touched this round: its fix rewrites the
stream-pump and the wall-timeout return path and needs a block of its own, which
is R8. Findings persist FIRST, in their own commit, before any repair
(docs/agents/planner_reviewer_prompt.md §4 item 4).

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f085-r7.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/live_review.md` += RECORD-R6, then R0498
  C2  `tests/orchestration/test_exec_guard.py` := the CPU-ASSERT pair applied
  C3  `.agent/live_review.md` += the LANDED-R0496 line
  C4  `.agent/plan.md` whole file := the PLAN slice
  C5  rewrite `.agent/handoff.md` (the handback)

Base:
This round starts from `ca5ff4f1756b38e7c176579abc753c0dcff06a22`, the R6 handback
commit and the current tip of `feature/f085-sandbox-hardening`. Every range gate
below names that SHA. Stay on this branch; do not create a new one.

Slice convention:
Each authored unit below sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each slice programmatically by its
markers and apply it byte-verbatim. No marker line ever reaches a target file.
The slices are PLAN, RECORD-R6, R0498, LANDED-R0496, CPU-ASSERT-FROM and
CPU-ASSERT-TO. Every slice's bytes end with a single trailing newline, and a
whole-file slice is the COMPLETE file including it.

Round type: SPLIT. The change set reaches `tests/`, so the reviewer gates and you
execute; the single-writer rule of docs/agents/self_drive_protocol.md is
unchanged — the reviewer writes nothing, you write everything.

──────────────────────────────────────────────────────────────

Change:

1. C0a — write this ENTIRE block, byte for byte, to `.agent/authored/f085-r7.md`.
   The reviewer's original is on disk at `.remedy-wt/f085-r7.md` and its expected
   sha256 is stated in the delegation that carries this block; copy that file
   rather than retyping it (`shutil.copyfile` is fine — the gate names the byte
   property, not the tool). Verify the digest BEFORE committing. Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f085-r7.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — append to `.agent/live_review.md`, in this order, each preceded by exactly
   one blank line, byte-verbatim, nothing else in the file touched:
   a. the RECORD-R6 slice;
   b. the R0498 slice.
   The pre-C1 content must remain a byte-exact PREFIX of the post-C1 content.

4. C2 — in `tests/orchestration/test_exec_guard.py`, replace the CPU-ASSERT-FROM
   slice with the CPU-ASSERT-TO slice. This pair is a REWRITE, not an append: the
   TO does not contain the FROM, because the whole point is that the compared
   value changes. FROM occurs exactly once in the file before the edit and zero
   times after; nothing else in the file, and no other file, is touched by this
   commit. Do not edit `packages/orchestration/exec_guard.py`.

5. C3 — append to `.agent/live_review.md`, preceded by exactly one blank line, the
   LANDED-R0496 slice byte-verbatim. It is a `Landed:` line and NOT a `Done:`
   paragraph: only reviewer-authored text sets Resolved
   (docs/agents/planner_reviewer_prompt.md §4 item 4), and the reviewer replaces
   this line with the authored resolution at the next gate.

6. C4 — `.agent/plan.md` whole file := the PLAN slice. Commit alone.

7. C5 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Its
   state block repeats this Fortschritt line verbatim:
   `Fortschritt: ~30 % (F085 beansprucht · Amendment F085 D1 angewandt · T001 gebaut · R6 PASS · R-0496 gefixt, R-0495 offen und T002 blockiert · T003 offen) — Schätzung`
   Its "Next" section states exactly this:
   - R8 is a REPAIR round and fixes R-0495, the wall timeout that does not bound
     `run_guarded`'s own return; it is the last thing blocking T002a;
   - `tests/orchestration/test_exec_guard.py` is GREEN and DETERMINISTIC as of this
     round, measured over ten runs, and R-0495 is a defect the suite does not yet
     cover — a green suite is not evidence that the guard bounds runtime;
   - `exec_guard.py` still has NO callers, so no containment claim holds for the
     running system;
   - there is NO open PR for this branch and none is opened before closure;
   - the R7 verdict is written by the NEXT round's record commit.

──────────────────────────────────────────────────────────────

Constraints:

1. AGENTS.md is the highest authority. Self-review loop before every commit; push
   after committing.
2. Every slice is applied BYTE-VERBATIM. If a slice cannot be applied as-is, stop
   and declare it — never adjust the bytes to make a gate pass.
3. The ONLY files this round may change are the ones named in the ordered bundle.
   Do NOT touch `packages/orchestration/exec_guard.py`, `.agent/f085_inventory.md`,
   `docs/roadmap/STATUS.md`, `docs/roadmap/features/T2_F085.md` or
   `docs/roadmap/ROADMAP.md`.
4. DO NOT FIX R-0495 THIS ROUND, and do not "improve" anything else in the test
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
G2  TRANSPORT: `.remedy-wt/f085-r7.md`, the committed `.agent/authored/f085-r7.md`
    and the committed `.agent/last_block.md` are byte-EQUAL and share one sha256.
    Report that digest, the byte count and the line count.
G3  `.agent/plan.md` at HEAD is byte-equal to the PLAN slice; report its sha256 and
    line count; it contains `## Goal`, `## Next Steps` and a `\bF\d{3}\b` match, and
    is under 50 lines.
G4  `.agent/live_review.md`: the pre-C1 content is a byte-exact PREFIX of the post-C1
    content and the pre-C3 content is a byte-exact PREFIX of the post-C3 content.
    The C1 tail contains the RECORD-R6 and R0498 slices and the C3 tail contains the
    LANDED-R0496 slice, each byte-verbatim and each exactly once in the WHOLE file.
    Report `git show --numstat` for that path at C1 and at C3 and confirm both
    deletion columns are 0.
G5  Open-set recomputation at HEAD with the two regexes `^- R-\d+ — ` and
    `^Done: R-\d+ — `: report registered, resolved, duplicate ids and resolutions
    naming an unregistered id. REQUIRED: the set of OPEN ids at HEAD EQUALS the set
    open at `ca5ff4f1` PLUS exactly `R-0498`, and R7 resolves nothing — a `Landed:`
    line is not a resolution. Report both counts and the symmetric difference rather
    than predicting them, plus the max id and the next free id. Separately report the
    number of LINE-START records matching `^Landed: R-\d+`, which must be exactly 1
    and must name R-0496.
G6  `.agent/live_review.md` still contains the substring `Steps`.
G7  `git diff --name-only ca5ff4f1..HEAD` lists exactly this set and nothing else:
    `.agent/authored/f085-r7.md`, `.agent/handoff.md`, `.agent/last_block.md`,
    `.agent/live_review.md`, `.agent/plan.md`,
    `tests/orchestration/test_exec_guard.py`. Report the real list. NO path under
    `packages/`, `docs/`, `apps/` or `scripts/` may appear.
G8  UNCHANGED GUARD, the counter-proof to constraint 4: report the sha256 of
    `packages/orchestration/exec_guard.py` at `ca5ff4f1` and at HEAD. They must be
    equal — R-0495 is R8's work and no part of it lands here.
G9  PAIR SHAPE, a REWRITE: over the WHOLE of `tests/orchestration/test_exec_guard.py`
    at HEAD, the CPU-ASSERT-FROM text occurs 0 times and the line
    `    assert result.cpu_seconds_used >= 0.5` occurs exactly 1 time. Report both
    counts. Also report the `git show --numstat` of C2 for that path.
G10 DETERMINISM, and read this one carefully: run
    `python3 -m pytest tests/orchestration/test_exec_guard.py -q` TEN times in a row
    and report the real exit code AND the real summary line of EACH of the ten runs,
    in order. ALL TEN must be exit 0. One green run is not what this gate asks for:
    at `ca5ff4f1` this same command is a coin flip — the reviewer measured 8 red and
    4 green over twelve runs — and ten consecutive greens is the evidence that the
    coin flip is gone. If any run is red, report every reading and hand back without
    repairing anything. (This gate is the counter-measure of R-0498, applied in the
    block that registers it.)
G11 `python3 -m ruff check tests/orchestration/test_exec_guard.py` → exit 0, using
    the repository's OWN configuration. Do NOT pass `--isolated`: it discards
    `pyproject.toml` and with it the lint rules this gate exists to run (R-0463).
G12 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, the canary. The
    reviewer measured `42 passed`, exit 0, at `ca5ff4f1`.
G13 PROBE, not a colour — run the eight-file structural sweep THREE times and report
    each real exit code and each real summary line:
    `python3 -m pytest tests/orchestration/test_autonomy.py tests/regression/test_named_bugs.py tests/test_path_utils.py tests/test_data_paths.py tests/test_no_interactive_guard.py tests/orchestration/test_review_subject_resolution.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py -q -rf`
    The reviewer measured `350 passed, 6 skipped`, exit 0, seven times out of seven
    at `ca5ff4f1`, and on a scratch worktree carrying a LARGER draft change saw one
    unreproduced red in 22 runs whose node id was not captured. So: if a run is red,
    report the FAILED node id verbatim from `-rf` and hand back. Do not repair it and
    do not re-run until it goes green.
G14 Per-commit insertions — the `+` column of `git show --numstat` — for C0a, C0b,
    C1, C2, C3 and C4 only. None may exceed 500. C5's own count is ordered nowhere
    and the reviewer measures it at the next gate (R-0494, checklist item 14).
G15 `git log --format=%p ca5ff4f1..HEAD` shows one parent per commit (linear).
    `git reflog` over this round shows only `commit:` entries — no amend, rebase,
    reset, checkout of another branch, or force-push.

Verification tier: round gate (§3 tier 1) plus the canary at G12. The docs-round
gate of tier 5 is NOT triggered: this round's change set contains no
`docs/roadmap/**` path.

Handback:
Completion report + rewrite `.agent/handoff.md`. Push with
`git push origin feature/f085-sandbox-hardening`. Do NOT open a PR.

──────────────────────────────────────────────────────────────

<<<SLICE CPU-ASSERT-FROM>>>
    assert result.cpu_seconds_used >= 1.0
<<<END CPU-ASSERT-FROM>>>

<<<SLICE CPU-ASSERT-TO>>>
    # Tolerance strictly BELOW the limit, never ON it (R-0496): `ru_utime +
    # ru_stime` is the kernel's own CPU accounting, which is granular and rounds
    # against RLIMIT_CPU rather than exactly to it, so a value a few hundred
    # microseconds under an integer limit is the normal outcome. The property
    # this test is named for is the SIGXCPU trip asserted above; the number only
    # has to show the child really burned the CPU it was limited on.
    assert result.cpu_seconds_used >= 0.5
<<<END CPU-ASSERT-TO>>>

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
R7, this round: record the R6 PASS, register R-0498, and fix R-0496 — the
boundary assertion that made the T001 suite a coin flip. R-0495 is untouched
here; it gets its own round because its fix rewrites the stream pumps.

## Next Steps
1. R8 repairs R-0495: the wall timeout must bound `run_guarded`'s own return and
   not only the process group it can reach, and the result must say whether the
   streams were complete. The docstring's "no descendant outlives this call"
   narrows to the group the kill actually reaches.
2. T002a — builder class, 5 sites, the first seam migration. BLOCKED until R-0495
   is fixed: migrating a seam onto a guard whose timeout does not bound wall time
   would make hangs harder to see, not easier.
3. T002b-d, then T003 — network posture, limitations document, README link.

## Risks
- R-0495 is the feature's central promise failing in its central case. Until it
  is fixed, no round may describe `exec_guard` as bounding runtime, and a green
  T001 suite is not evidence to the contrary: no test covers R-0495 yet.
- The address-space limit is enforced but NOT attributable from `wait4` data;
  R5's G16 probe confirmed it. Whether stage 1 can name that trip stays open.
<<<END PLAN>>>

<<<SLICE LANDED-R0496>>>
Landed: R-0496 — the marginal assertion now compares `cpu_seconds_used` against 0.5 instead of against the 1.0 RLIMIT_CPU limit it sat exactly on, with the kernel-accounting reason in a comment above it; `tests/orchestration/test_exec_guard.py`, commit C2 of R7.
<<<END LANDED-R0496>>>

<<<SLICE RECORD-R6>>>
Gate: R6 — PASS. Every ordered gate was re-run by the reviewer from the repository root at ca5ff4f1, and every one reproduces the handback's reading, with the round's single declared deviation CONFIRMED rather than refuted. TRANSPORT, against the reviewer's OWN scratchpad original and NOT by digest fallback (§4.9): `.remedy-wt/f085-r6.md`, the committed `.agent/authored/f085-r6.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 fc4752a4ac333290e30d11145beaf519b9b6eb46d3b01099f95869fff5956d03, 22488 B, 213 lines. `.agent/plan.md` at HEAD byte-equals the PLAN slice at sha256 8b4398f8616dcdb71cf72d254e22c09937f87052350e22bd2721cb69ab1ef5ad, 2136 B, 38 lines, under the 50-line cap, carrying `## Goal`, `## Next Steps` and an F-id. The C1 append is honest: the pre-C1 blob of 214867 B is a byte-exact PREFIX of the 225757 B post-C1 file, the RECORD-R5, R0495, R0496 and R0497 slices each occur exactly once in the whole file and each exactly once inside the 10890-byte, eight-line appended tail, the numstat is `8 0` with a zero deletion column, and the file is byte-identical from C1 through HEAD. The open set moved by exactly three: 109 registered / 0 resolved / 109 open at 16506c0b against 112 / 0 / 112 at HEAD, symmetric difference of HEAD-open against base-open plus R-0495, R-0496 and R-0497 EMPTY, 0 duplicate ids, 0 resolutions naming an unregistered id, 0 line-start `^Landed: R-` records, max R-0497 and next free R-0498. The substring `Steps` survives 19 times. The change set is exactly the five ordered `.agent/**` paths with nothing under `packages/`, `tests/`, `docs/`, `apps/` or `scripts/`, and G8's counter-proof holds: `packages/orchestration/exec_guard.py` at sha256 d9c77caec4ed9136868cef080bd2e2ae18c4216851507dc943d778d5c575114e, 12241 B, and `tests/orchestration/test_exec_guard.py` at sha256 9301bc652ecf555b983e0cf85dc7c5da52071ef20de741b9cd3f1476188bad53, 6211 B, are byte-identical at 16506c0b and at HEAD, so constraint 4 held and nothing was repaired under cover of a record round. The history is five single-parent commits, bb22b2dd←16506c0b then 4cc753b6, 07255ccd, 93fcf6ff and ca5ff4f1, and the reflog over the round carries `commit:` entries only. The canary is `42 passed in 20.46s`, exit 0. THE DEVIATION, CONFIRMED: G9 ordered a COLOUR — it passed only when the command FAILED — and the worker reported that the colour does not reproduce, 3 red and 4 green over seven runs. At the reviewer's own hand the same command at HEAD is red on 8 runs and green on 4 out of TWELVE, `1 failed, 5 passed` against `6 passed`, always at `test_cpu_limit_kills_a_busy_loop_and_names_the_limit`. The worker's reading is therefore corroborated and the gate as written was unmeetable rather than unmet. The worker recorded the real commands, exit codes and summary lines, edited nothing the gate measures — G8 is the byte proof — and declared the deviation, which is exactly what constraint 7 asks of it; the defect is the reviewer's own and is registered as R-0498. The values R6 routed nowhere are recorded HERE, measured by the reviewer at ca5ff4f1, which is the R-0494 counter-measure working as designed: the handback commit ca5ff4f1 inserted 41 lines and deleted 60, the per-commit insertions before it are C0a 213, C0b 106, C1 8 and C2 14 with none over 500, the post-C5 change set is the same five paths, `git status --porcelain` is EMPTY, `git worktree list` is one line, the push landed with origin at ca5ff4f1, and `.agent/handoff.md` measures 87 lines against its own DECISION D15 declaration of 87, so its self-measurement is honest. LAST_REVIEWED_SHA advances to ca5ff4f1.
<<<END RECORD-R6>>>

<<<SLICE R0498>>>
- R-0498 — Low, A REVIEWER GATE ORDERED AN EXPECTED COLOUR FOR A COMMAND THE REVIEWER HAD SEEN ONLY FIVE TIMES, AND THAT COMMAND IS A COIN FLIP RATHER THAN RELIABLY RED. Raised by the reviewer against its own R6 block at the R6 gate. G9 of that block ordered `python3 -m pytest tests/orchestration/test_exec_guard.py -q`, declared that the gate PASSES when the command FAILS, and rested that order on five consecutive red runs measured at 16506c0b. The worker got 3 red and 4 green over seven runs and declared the deviation; the reviewer then measured 8 red and 4 green over twelve runs at ca5ff4f1. Five consecutive observations of one colour are not evidence of determinism — for an even coin five identical outcomes arrive once in sixteen attempts, which is ordinary rather than remarkable — so the sample never supported the order built on it, and the flakiness was a property of the test the whole time rather than something that changed between rounds. The cost was one declared deviation on a round that did everything else right, and the worse branch was reachable: had the worker's seven runs happened to come out all red, an unmeetable gate would have been recorded as satisfied and the coin flip would have stayed invisible until it fell the other way at a less convenient moment. This is the reviewer-arithmetic family of R-0327 and R-0336 reaching the same place from a third direction — R-0327 ordered a count the reviewer computed by hand, R-0497 ordered a value the code could not produce, and this one orders a colour that a non-deterministic command cannot honestly promise. Counter-measure, binding on the reviewer from this round on and APPLIED IN THE SAME BLOCK THAT REGISTERS THIS FINDING, as gate G10: a gate that names an expected COLOUR for a command whose determinism has not been established orders that command run at least TEN times with every exit code and summary line reported, and either requires the colour on all ten or is rewritten as a probe that reports what it saw. Promoting the rule into the docs/agents/planner_reviewer_prompt.md §3 pre-emission checklist is a `docs/agents/**` edit outside this feature's change set and is NOT claimed here; it is named for the paydown branch that already carries R-0403, R-0448, R-0482, R-0487, R-0490, R-0493, R-0494 and R-0497. OPEN.
<<<END R0498>>>
