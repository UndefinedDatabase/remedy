── STEP R5 — F085 Sandbox hardening (stage 1) ────────────────

Goal:
Record the R4 PASS, register R-0494, then build T001: a new module
`packages/orchestration/exec_guard.py` carrying the stage-1 execution mechanics —
POSIX rlimits, the guard's OWN wall-timeout supervision, output-size caps and a
classified outcome — plus its unit tests with the four runaway fixtures. This is
the FIRST production-code round of this feature and therefore a SPLIT round under
docs/agents/planner_reviewer_prompt.md §3 Round-types.

Bundle (ordered, one commit each; no extra commit, none dropped, no reordering):
  C0a save this block verbatim as `.agent/authored/f085-r5.md`
  C0b mirror the COMMITTED C0a file into `.agent/last_block.md`
  C1  `.agent/live_review.md` += the RECORD-R4 slice, then the R0494 slice
  C2  `.agent/plan.md` whole file := the PLAN slice
  C3  NEW FILE `packages/orchestration/exec_guard.py`
  C4  NEW FILE `tests/orchestration/test_exec_guard.py`
  C5  rewrite `.agent/handoff.md` (the handback)

Base:
This round starts from `382ed7fa2055d38bc6ff94164c8cb993f28ce9fb`, the R4
handback commit and the current tip of `feature/f085-sandbox-hardening`. Every
range gate below names that SHA. Stay on this branch; do not create a new one.

Slice convention:
Each authored unit below sits between a one-line `<<<SLICE NAME>>>` marker and a
one-line `<<<END NAME>>>` marker. Extract each slice programmatically by its
markers and apply it byte-verbatim. No marker line ever reaches a target file.
The slices are PLAN, RECORD-R4 and R0494. Every slice's bytes end with a single
trailing newline, and a whole-file slice is the COMPLETE file including it.

Authorship of the production code, stated because it decides who may certify it:
the reviewer authors NO byte of `exec_guard.py` or of its test file. Change items
5 and 6 below give a CONTRACT — names, semantics, invariants — and YOU write the
implementation. A round in which the reviewer both wrote and gated the production
code is void under docs/agents/self_drive_protocol.md, so a request to "apply"
those two files verbatim would be the defect, not the fix.

──────────────────────────────────────────────────────────────

Change:

1. C0a — write this ENTIRE block, byte for byte, to
   `.agent/authored/f085-r5.md`. The reviewer's original is on disk at
   `.remedy-wt/f085-r5.md` and its expected sha256 is stated in the delegation
   that carries this block; copy that file rather than retyping it
   (`shutil.copyfile` is fine — the gate names the byte property, not the tool).
   Verify the digest BEFORE committing. Commit alone.

2. C0b — copy the COMMITTED `.agent/authored/f085-r5.md` over
   `.agent/last_block.md`, whole file. Commit alone.

3. C1 — append to `.agent/live_review.md`, in this order, each preceded by
   exactly one blank line, both byte-verbatim, nothing else in the file touched:
   a. the RECORD-R4 slice;
   b. the R0494 slice.
   The pre-C1 content must remain a byte-exact PREFIX of the post-C1 content.
   This is the FIRST commit of the round on purpose: findings persist before any
   fix (planner_reviewer_prompt.md §4 item 4).

4. C2 — `.agent/plan.md` whole file := the PLAN slice. Commit alone.

5. C3 — create `packages/orchestration/exec_guard.py`. It has NO callers this
   round: migrating the 24 in-scope seams is T002 and no part of it happens here.
   The contract:

   `ExecGuardPolicy`, a frozen dataclass, fields and meaning:
   - `cpu_seconds: int | None` — RLIMIT_CPU soft limit; None means not set.
   - `cpu_grace_seconds: int` — default 2. The hard limit is
     `cpu_seconds + cpu_grace_seconds`. WHY, and this is measured rather than
     preferred: with soft == hard the kernel delivers SIGKILL, which is
     byte-identical in `wait4` status to the SIGKILL this guard itself sends on a
     wall-timeout, and the two causes become indistinguishable. With a grace band
     the kernel delivers SIGXCPU first and the trip is attributable.
   - `address_space_bytes: int | None` — RLIMIT_AS soft and hard.
   - `open_files: int | None` — RLIMIT_NOFILE soft and hard.
   - `core_file_bytes: int` — default 0; RLIMIT_CORE, cores off.
   - `wall_timeout_seconds: float | None` — the guard's OWN deadline. None means
     no wall timeout, which is the runtime class's policy per the feature file's
     amendment F085 D1 table.
   - `output_cap_bytes: int | None` — per stream, not combined.
   - `cwd: str | None` — passed to the child.
   - `env: dict[str, str] | None` — passed through UNCHANGED this round.
     Environment scrubbing and the allowlist are T002; do not implement them here
     and do not claim them anywhere in the module.

   `ExecGuardResult`, a frozen dataclass: `returncode: int | None`,
   `term_signal: str | None` (the signal NAME, e.g. `"SIGXCPU"`, or None if the
   child exited normally), `stdout: bytes`, `stderr: bytes`,
   `stdout_truncated: bool`, `stderr_truncated: bool`, `stdout_bytes_seen: int`,
   `stderr_bytes_seen: int` (the totals the child actually produced, which stay
   correct after truncation), `wall_seconds: float`, `cpu_seconds_used: float`
   (from the child's own `rusage`), `classification: str`,
   `tripped_limit: str | None`, `limits_enforced: tuple[str, ...]` and
   `limits_unsupported: tuple[str, ...]`.

   `run_guarded(cmd: Sequence[str], policy: ExecGuardPolicy) -> ExecGuardResult`.
   Implementation invariants:
   - `subprocess.Popen`, argv list only, never `shell=True`.
   - `start_new_session=True`, so the child leads its own process group and the
     wall-timeout kill reaches the whole group rather than the leader alone.
   - `preexec_fn` sets the rlimits and nothing else. A limit the platform does
     not support is recorded in `limits_unsupported` and never silently dropped
     (the feature file's A9 edge case: no silent claims).
   - The wall timeout is this guard's own supervision of the child. It is NEVER
     a forwarded `timeout=` keyword — six of the seven timeout-less in-scope
     sites are `Popen`, which takes no such keyword, and amendment F085 D1
     records that as a design constraint.
   - Output caps are enforced while reading, never by truncating a buffer that
     was already allowed to grow without bound. Past the cap the guard stops
     STORING and keeps COUNTING, so `*_bytes_seen` remains true.
   - The child is reaped with `os.wait4` so its `rusage` belongs to that child
     and to no other. No orphan may survive `run_guarded` on any path.
   - No `except Exception: pass` anywhere (a repo-wide guard forbids it).

   Classification, and each rule must be decidable from evidence the guard
   actually holds:
   - the guard's own deadline fired and the guard sent the kill →
     `classification="resource_limit"`, `tripped_limit="wall_timeout"`;
   - else the child died on SIGXCPU → `"resource_limit"`, `"cpu_seconds"`;
   - else the guard's reader hit `output_cap_bytes` on either stream →
     `"resource_limit"`, `"output_bytes"`;
   - else `returncode == 0` → `"ok"`, `tripped_limit=None`;
   - else `"failed"`, `tripped_limit=None`.

   The address-space limit is ENFORCED and deliberately NOT classified. The
   module docstring says so in its own words and states the measured reason: a
   child that exceeds RLIMIT_AS raises `MemoryError` and exits 1 with no signal,
   and its `ru_maxrss` stays BELOW the limit because the refused mapping never
   became resident — so nothing in `wait4` attributes that death to the limit
   rather than to any other exit-1 failure. Claiming `address_space` from that
   evidence would be an overclaim, and the Orchestrator brief rejects overclaiming
   wording in code comments too. Whether stage 1 can attribute it at all is R6's
   question and G16 below is the evidence for it.

6. C4 — create `tests/orchestration/test_exec_guard.py`, every test marked
   `@pytest.mark.subprocess` (the marker is registered in `pyproject.toml`).
   Cover exactly these, and keep every limit small so the file stays fast:
   a. WELL-BEHAVED: a command that prints to stdout and stderr and exits 0 under
      a policy with limits set. `returncode`, `stdout` and `stderr` equal what
      the same argv produces without the guard; `classification == "ok"`;
      `tripped_limit is None`; neither stream truncated.
   b. CPU: a busy loop under `cpu_seconds=1`. The child dies,
      `term_signal == "SIGXCPU"`, `classification == "resource_limit"`,
      `tripped_limit == "cpu_seconds"`.
   c. WALL: a command that sleeps far longer than the deadline, under
      `wall_timeout_seconds` of at most 2.0 and NO cpu limit that could fire
      first. `classification == "resource_limit"`,
      `tripped_limit == "wall_timeout"`, and `wall_seconds` is well under the
      child's own sleep — assert an upper bound, never an exact duration.
   d. OUTPUT: a command that writes far more than `output_cap_bytes`.
      `classification == "resource_limit"`, `tripped_limit == "output_bytes"`,
      `stdout_truncated is True`, `len(result.stdout) <= output_cap_bytes`, and
      `stdout_bytes_seen` greater than the cap.
   e. MEMORY, enforcement only: the SAME argv run twice — once under an
      `address_space_bytes` far below what it allocates, once under a generous
      one. The tight run has `returncode != 0` and `b"MemoryError"` in stderr;
      the generous run has `returncode == 0`. Assert NOTHING about
      `tripped_limit` here: this test proves the limit is enforced, and the
      module's docstring already says attribution is not claimed.
   f. NO ORPHANS: after the runaway cases, no child process survives. Use a
      unique argv marker string and `pgrep -af <marker>`, the pattern
      `tests/regression/test_resource_safety.py` already uses, filtering out the
      `pgrep` line itself.

7. C5 — rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Its
   state block repeats this Fortschritt line verbatim:
   `Fortschritt: ~25 % (F085 beansprucht · Seam-Inventar abgenommen · Amendment F085 D1 angewandt · T001 gebaut, ungenutzt · T002/T003 offen) — Schätzung`
   Its "Next" section states exactly this:
   - R6 is the next round: the seam migration begins with T002a (builder, 5
     sites), and it too is a SPLIT round;
   - `exec_guard.py` has NO callers yet, so nothing in Remedy is guarded by it
     and no containment claim may be made for the running system;
   - there is NO open PR for this branch and none is opened before closure;
   - the R5 verdict is written by the NEXT round's record commit.

──────────────────────────────────────────────────────────────

Constraints:

1. AGENTS.md is the highest authority. Self-review loop before every commit;
   push after committing.
2. Every SLICE is applied BYTE-VERBATIM. If a slice cannot be applied as-is,
   stop and declare it — never adjust the bytes to make a gate pass. The two new
   Python files are yours to write and this rule does not apply to them.
3. The ONLY files this round may change are the ones named in the ordered
   bundle. No existing production module, no existing test file, NOT
   `.agent/f085_inventory.md`, NOT `docs/roadmap/STATUS.md`, NOT
   `docs/roadmap/features/T2_F085.md`, and NOT `docs/roadmap/ROADMAP.md`.
4. Do not migrate any seam, do not import `exec_guard` from anywhere, and do not
   edit any of the 24 in-scope call sites. That is T002 and this round would hide
   it inside a much larger diff.
5. Never force-push, never rebase, never amend, never reset, never work on
   `main`, never delete a branch. Do not create a PR.
6. Re-read `.agent/STOP` from disk before the FIRST commit and again at the
   handback. If it exists at either point, finish the commit in flight, write the
   handoff and end.
7. If any gate below is red, do not repair it by editing the thing it measures.
   Record the real command, the real exit code and the real output, and hand
   back. A red gate ends the round honestly. This applies with full force to G16:
   report what the memory fixture really did, whatever that is.
8. Destructive or exploratory verification runs only inside a disposable
   `git worktree`, never in the primary checkout, which must satisfy
   `git status --porcelain` == empty at the handback.

──────────────────────────────────────────────────────────────

Done when — every command run from the repository root with `pwd` confirmed,
every real exit code recorded:

G1  `git status --porcelain` is EMPTY at the handback. `git worktree list` is
    ONE line. `.agent/STOP` absent at both readings.
G2  TRANSPORT: `.remedy-wt/f085-r5.md`, the committed `.agent/authored/f085-r5.md`
    and the committed `.agent/last_block.md` are byte-EQUAL and share one sha256.
    Report that digest, the byte count and the line count.
G3  `.agent/plan.md` at HEAD is byte-equal to the PLAN slice; report its sha256
    and line count; it contains `## Goal`, `## Next Steps` and a `\bF\d{3}\b`
    match, and is under 50 lines.
G4  `.agent/live_review.md`: the pre-C1 content is a byte-exact PREFIX of the
    post-C1 content, and the appended tail contains the RECORD-R4 slice and the
    R0494 slice, each byte-verbatim and each exactly once. Report
    `git show --numstat` for that path at C1 and confirm its deletion column is 0.
G5  Open-set recomputation at HEAD with the two regexes `^- R-\d+ — ` and
    `^Done: R-\d+ — `: report registered, resolved, duplicate ids and resolutions
    naming an unregistered id. REQUIRED: the set of OPEN ids at HEAD EQUALS the
    set open at `382ed7fa` PLUS exactly `R-0494`, and R5 resolves nothing. Report
    both counts and the symmetric difference rather than predicting them, plus the
    max id and the next free id. Separately report the number of LINE-START
    records matching `^Landed: R-\d+` — report the number you measure.
G6  `.agent/live_review.md` still contains the substring `Steps`.
G7  `git diff --name-only 382ed7fa..HEAD` lists exactly this set and nothing
    else: `.agent/authored/f085-r5.md`, `.agent/handoff.md`,
    `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
    `packages/orchestration/exec_guard.py`,
    `tests/orchestration/test_exec_guard.py`. Report the real list and flag any
    difference rather than editing to match. No path under `docs/`, `apps/` or
    `scripts/` may appear.
G8  NO CALLERS: `grep -rn "exec_guard" packages/ apps/ scripts/ tests/` returns
    matches in `packages/orchestration/exec_guard.py` and
    `tests/orchestration/test_exec_guard.py` ONLY. Report the real file list. Any
    third file means T002 started inside this round.
G9  `python3 -m ruff check packages/orchestration/exec_guard.py tests/orchestration/test_exec_guard.py`
    → exit 0. Run it EXACTLY so, from the repository root, with the repository's
    own `pyproject.toml` — never `--isolated`, which discards the `select` line
    that enables the isort rules at all. Reviewer's note, so you do not widen it:
    the broader scope `packages/orchestration/ tests/orchestration/` is ALREADY
    RED at base with 13 pre-existing errors in unrelated files, so it is
    deliberately not ordered; the reviewer red-controlled the scoped command
    inside a disposable worktree and it does fail on a broken file.
G10 `python3 -m pytest tests/orchestration/test_autonomy.py tests/regression/test_named_bugs.py tests/test_path_utils.py tests/test_data_paths.py tests/test_no_interactive_guard.py tests/orchestration/test_review_subject_resolution.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py -q`
    → exit 0. These are the whole-directory sweeps that a NEW
    `packages/orchestration/*.py` falls under: no `shell=True`, no `0.0.0.0`, no
    `except Exception: pass`, no local `_section`, no interactive construct, no
    inline `REMEDY_DATA_DIR` read, no `REMEDY_REVIEW_BASE` mention. The reviewer
    measured `350 passed, 6 skipped`, exit 0, at `382ed7fa`.
G11 `python3 -m pytest tests/orchestration/test_exec_guard.py -q` → exit 0.
    Report the passed count and the reported wall time.
G12 NO ORPHANS: immediately after G11, `pgrep -af <your marker>` prints nothing
    but its own excluded line. Report the exact command and its real output.
G13 `python3 -m pytest tests/cli/test_golden_path.py -q` → exit 0, the canary.
    The reviewer measured `42 passed`, exit 0, at `382ed7fa`.
G14 Per-commit insertions — the `+` column of `git show --numstat` — for C0a,
    C0b, C1, C2, C3 and C4 only. None may exceed 500. C5's own count is NOT
    ordered anywhere: it cannot exist while C5's text is being written, and this
    round does not route it to a round report either. The reviewer measures it at
    the next gate, which is the counter-measure R-0494 registers.
G15 `git log --format=%p 382ed7fa..HEAD` shows one parent per commit (linear).
    `git reflog` over this round shows only `commit:` entries — no amend, rebase,
    reset, checkout of another branch, or force-push.
G16 MEMORY PROBE, evidence for R6 and not a pass/fail gate: for the tight run of
    test (e), report the child's `returncode`, its `term_signal` (or that there
    was none), the last line of its stderr, and its `ru_maxrss` beside the
    `address_space_bytes` you set. Report what you measured even if it
    contradicts the reviewer's stated reason in Change item 5 — that
    contradiction would be the most valuable thing this round produces.
G17 NO OVERCLAIM: neither new file, and no line of the handback, states or
    implies that any existing Remedy subprocess is now guarded, limited or
    sandboxed. Nothing calls `run_guarded` yet. Confirm you checked this and name
    where you checked.

Verification tier: this is a round gate (planner_reviewer_prompt.md §3 tier 1)
plus the canary at G13. The docs-round gate of tier 5 is NOT triggered: this
round's change set contains no `docs/roadmap/**` path.

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
R5, this round: record the R4 PASS, register R-0494, then build T001 — the new
module `packages/orchestration/exec_guard.py` with rlimit, wall-timeout and
output-cap mechanics, plus `tests/orchestration/test_exec_guard.py` with the four
runaway fixtures. The module gets NO callers this round.

## Next Steps
1. T002a — builder class, 5 sites, the first seam migration, with
   behaviour-equality goldens for well-behaved commands.
2. T002b-d — test (12 sites), DoD (2) and runtime (5, no wall timeout) classes,
   one ordered sub-slice each, plus environment scrubbing with the allowlist test
   that carries R-0202.
3. T003 — network posture, per-class policy table, the limitations document and
   its README link.

## Risks
- The address-space limit is enforced but NOT attributable from `wait4` data:
  the child raises `MemoryError`, exits 1 with no signal, and its `ru_maxrss`
  stays below the limit. R6 rules on whether stage 1 can name that trip at all.
- 24 in-scope call sites in 18 modules and 22 enclosing functions is a far wider
  migration than the feature file assumed. None of T002's sub-slices may widen
  into the git, packaging or other classes.
<<<END PLAN>>>

<<<SLICE RECORD-R4>>>
Gate: R4 — PASS. All sixteen ordered gates reproduce at the reviewer's own hand, from the repository root at 382ed7fa, and every measured value equals the one the handback reports. TRANSPORT, against the reviewer's OWN scratchpad original and NOT by digest fallback (§4.9): `.remedy-wt/f085-r4.md`, the committed `.agent/authored/f085-r4.md` and the committed `.agent/last_block.md` are byte-EQUAL at sha256 c755c49d28f58c0d9f97ce0e0f95daa75e9291eeb3b6fce10153291b96727b42, 23993 B, 318 lines. `.agent/plan.md` at HEAD byte-equals the PLAN slice at sha256 a1a17001365fd83c0de0168d8c7d5c6057ead885121c54917fbc54322c1be673, 41 lines, 2266 B, carrying `## Goal`, `## Next Steps` and an F-id, under the 50-line cap. The C2 append is honest: the pre-C2 blob of 202948 B is a byte-exact PREFIX of the 208910 B post-C2 file, the RECORD-R3 and R0493 slices each occur exactly once in the whole file and both inside the 5962-byte, four-line appended tail, and the numstat is `4 0` with a zero deletion column. The open set moves by exactly one: 107 open at fb346e8c, 108 at HEAD, the symmetric difference of the HEAD open set against the base open set plus R-0493 is EMPTY, with 0 duplicate ids, 0 resolutions naming an unregistered id and 0 line-start `^Landed: R-` records; max R-0493, next free R-0494. `.agent/f085_inventory.md` is byte-identical at base and at HEAD at sha256 fed207f9f8fb5a2de6a52a5366e1f3332eab1ae60c3a666cbddf4771f6c166bd, so R4 did not revise what R2 closed. The amendment landed exactly as authored: in `docs/roadmap/features/T2_F085.md` FROM1 and FROM2 each occur 0 times and TO1, TO2 and the AMENDMENT each exactly once, the file ends with the AMENDMENT, `<<<` occurs 0 times, and lines 1 and 2 are byte-identical to lines 1 and 2 at fb346e8c, which is what keeps `tests/orchestration/test_roadmap_index.py` parsing it. Its arithmetic reproduces against the inventory it cites: the inventory's own per-class counts are builder 5, test 12, dod 2, runtime 5, git 24, packaging 11 and other 14, of which six `other` rows are the grep lines that are not call sites at all, so the amendment's `8 real` is exact and 5+12+2+5+24+11+8 equals the 67 real sites it claims. The change set is exactly the six ordered paths with nothing under `packages/`, `apps/`, `tests/` or `scripts/`; the history is six single-parent commits and the reflog over the round is six `commit:` entries with no amend, rebase, reset or force-push. Re-run by the reviewer in the PRIMARY checkout: `tests/docs/` 295 passed exit 0, `test_roadmap_index.py` 30 passed exit 0 — the R-0493 counter-measure doing its work on the very round that registered it — the four state-file readers 157 passed exit 0, and the canary 42 passed exit 0. The values R4's own gates routed to its round report, which no later session can read, are recorded HERE instead, measured by the reviewer at 382ed7fa: C4 inserted 48 lines, so the per-commit series is 318, 213, 16, 4, 68, 48 and none exceeds 500; the post-C4 change set is the same six paths; `git status --porcelain` is EMPTY and `git worktree list` is one line; the push landed, with `origin/feature/f085-sandbox-hardening` at 382ed7fa; and the handback measures 95 lines and 8467 B against its own DECISION D15 declaration of 95 lines, so its self-measurement is honest. That routing is the R-0494 class, registered next and answered by G14 of the R5 block.
<<<END RECORD-R4>>>

<<<SLICE R0494>>>
- R-0494 — Low, UNDER SELF-DRIVE A GATE READING ROUTED TO THE "ROUND REPORT" IS WRITTEN TO A CHANNEL THAT DIES WITH THE SESSION, SO THE NEXT SESSION INHERITS A GATE IT CANNOT READ. Raised by the reviewer at the R4 gate. docs/agents/planner_reviewer_prompt.md §3 pre-emission checklist item 14 rules that a per-commit gate may not order a value the handback commit cannot hold — its own insertion count — and directs that value to the ROUND REPORT instead, which is correct for the two-window relay where the operator sees that report. docs/agents/self_drive_protocol.md removes the second window and rules the opposite way about channels: "The handoff is the only return channel, and a session with no handoff did not happen." R4 followed item 14 exactly, so its G1 post-C4 readings, its G9 post-C4 change set, its G14 C4 insertion count and its push outcome were all directed into the worker's final message; the session then ended at the handback, and every one of those readings ceased to exist. Measured rather than assumed: none of the four appears in `.agent/handoff.md` at 382ed7fa, which states for each only that it "is in the round report". Nothing false was recorded and nothing was lost in substance, because a self-drive reviewer has execution and re-measured all four at 382ed7fa — they are in the RECORD-R4 paragraph above — which is exactly why this is Low and not higher. The cost is structural: a gate whose reading lives only in an ephemeral channel is unauditable by any later reader, and under G7 session limits an ending session is the NORMAL case rather than the exception, so the channel dies routinely. This is the R-0438 silently-vacuous-gate family reached from a third direction — R-0438's gate named a path that did not exist, R-0493's named a path that exists and does not cover the change, and this one names a value that is produced and then written where nothing can read it. Counter-measure, binding on the reviewer from this round on and APPLIED IN THE SAME BLOCK THAT REGISTERS THIS FINDING, as gate G14: under self-drive the handback commit's own numbers are ordered nowhere, and the reviewer measures them at the next gate and records them in that round's record paragraph in `.agent/live_review.md`, which is on disk and therefore auditable. Amending checklist item 14 itself to carry the self-drive branch is a `docs/agents/**` edit outside this feature's change set and is NOT claimed here; it is named as work for the paydown branch that already carries R-0403, R-0448, R-0482, R-0487, R-0490 and R-0493. OPEN.
<<<END R0494>>>
