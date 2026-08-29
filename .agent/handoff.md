# Handback — F033 · SESSION 7 · round 27 · THE INTEGRATION GATE

> Written by the WORKER at the close of the round-27 delegation. The reviewer
> holds the pre-emission original of the step block and runs the other half of
> the transport comparison itself.

## Session

SESSION 7 of feature F033 · round 27 · rounds so far 27.

SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE.

Both triggers of the amend0827 rule 6 soft limit remain reached: this is the
SEVENTH session and the TWENTY-SEVENTH round. The scope report is carried
forward with one line of its arithmetic moved — item 2 of "what is missing" is
delivered by this round.

### Scope report — required by operator amendment amend0827 rule 6

WHAT IS FINISHED. The feature's Goal & Done is met on every clause the feature
file states: stable content-hash ids and their stability property (T001); the
command, its validation, the all-or-nothing subset apply, the hunk ledger and
the write door (T002); partial-state truth on all three surfaces — viewer, task
node and report line (T003, R-0738); and the rejection-to-repair loop end to
end. THE FEATURE'S FUNCTIONAL SCOPE CLOSED AT ROUND 24 and this round did not
touch it. Round 26 added the `docs/` operator guide.

NEWLY FINISHED THIS ROUND: the integration gate of docs/agents/integration_gate.md
is RUN. Both suites are executed, compared and attributed id by id. THIS ROUND
CHANGED NO FILE UNDER `packages/`, `apps/`, `tests/` OR `docs/` — the measured
path set over `7adee149`..C3 is eleven paths, every one of them under `.agent/`.

WHAT IS MISSING, and none of it is feature work:
  1. ~~the `docs/` operator guide~~ — DELIVERED at round 26.
  2. ~~the integration-gate round~~ — DELIVERED by this round, with the two
     qualifications stated under "Verification" below: the branch suite is NOT
     all-green (2 failures, both SHARED with the merge base and both attributed
     to the UI-build environment class), and G8's insertion clause does not hold
     on one commit.
  3. The closure sequence and its pull request, which by precedent on this
     branch is two rounds.
  4. R-0745 (Low, OPEN) — the write door's import guard reads DIRECT imports
     only, and the door's transitive closure reaches `subprocess` through
     `evidence_index`.

THE PROPOSAL, unchanged and still a proposal only: split R-0745 onto its own
STATUS line and let F033 close on the Acceptance it has met, carrying R-0745 as
the documented Low risk the closure protocol's precondition 1 admits. NEITHER
READING IS EXECUTED ON A WORKER'S OR REVIEWER'S OWN AUTHORITY.

## Range

Review of `7adee149`..`e313c0c0` on branch `feature/f033-hunk-approval-v2`,
pushed. Eight commits, C0a through C4; the range is named to C3 because C4 is
the commit that writes this file and cannot name its own SHA (R-0149 pattern).

## Commits

### baf2bf52 docs(f033): save the round 27 step block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f033-r27.md | +281/-0 | C0a — the block saved verbatim, copied with `shutil.copyfile`, never retyped |

### 365bddf2 docs(f033): mirror the round 27 block into last_block
| Path | +/- | Reason |
|------|-----|--------|
| .agent/last_block.md | +204/-360 | C0b — the same bytes mirrored, copied from the saved file |

### e9543cd2 docs(f033): retarget the plan at the integration gate round
| Path | +/- | Reason |
|------|-----|--------|
| .agent/plan.md | +16/-19 | C1 — full rewrite from slice PLAN27 |

### 0e0314dc docs(f033): book the round 26 pass and resolve R-0749
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | +4/-0 | C2 — slice RECORD27 appended: the R26 `Gate:` paragraph and the `Done: R-0749` resolution. No id registered; exactly one resolved |

### b04bde68 test(f033): commit the round 27 branch run evidence
| Path | +/- | Reason |
|------|-----|--------|
| .agent/gate_f033_r27/branch_run.txt | +390/-0 | C3a — the branch run's full output, copied in only after the run exited (P1) |

### 9cee95b6 test(f033): commit the round 27 failure lists, parity and attribution
| Path | +/- | Reason |
|------|-----|--------|
| .agent/gate_f033_r27/branch_failed.txt | +2/-0 | C3b — the branch run's sorted `^FAILED` lines |
| .agent/gate_f033_r27/base_failed.txt | +114/-0 | C3b — the base run's sorted `^FAILED` lines |
| .agent/gate_f033_r27/parity.txt | +27/-0 | C3b — the P3 copy record and the P4 mtime-window reading |
| .agent/gate_f033_r27/comparison.txt | +118/-0 | C3b — both `comm` sets |
| .agent/gate_f033_r27/attribution.txt | +178/-0 | C3b — the per-id A/B attribution; created because G7 produced ids to attribute |

### e313c0c0 test(f033): commit the round 27 base run log in full
| Path | +/- | Reason |
|------|-----|--------|
| .agent/gate_f033_r27/base_run.txt | +7561/-0 | C3c — the base run's full output. DECLARED OVERSIZE; see deviation 3 |

### C4 — the handback (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewrite | C4 — this file; a handback cannot table the commit that writes it |

## External actions

- `git worktree add -b tmp/base-gate .remedy-wt/base-gate bd8d9529` — REAL exit 0,
  "Preparing worktree (new branch 'tmp/base-gate')", HEAD `bd8d952942d8ec1d243d787ccfe16e0ad04360d2`.
- `git worktree remove --force .remedy-wt/base-gate` — REAL exit 0.
- `git worktree prune` — REAL exit 0.
- `git branch -D tmp/base-gate` — REAL exit 0, "Deleted branch tmp/base-gate (was bd8d9529)".
- `git push` on `feature/f033-hunk-approval-v2` after C4. NO PR created, none
  edited, none merged — the closure sequence owns the pull request.
- No `gh` command run.

## Verification

Every exit code below is REAL, taken from `subprocess.run(...).returncode`
inside a script under the gitignored `.remedy-wt/`, never through a pipe
(constraint 9). SIX GATES ARE GREEN. G5 AND G6 CARRY A NON-ZERO PYTEST EXIT BY
DESIGN — that is the measurement, not a gate failure — AND G8 IS RED ON ONE
CLAUSE.

G1 TRANSPORT — REAL exit 0.
    committed `.agent/authored/f033-r27.md` : 22358 bytes, 281 lines,
      sha256 5b81aa42a97c5592e104c09c1b1a6c11ff2c260fc9a2e2cb2703c202521bbcf9
    committed `.agent/last_block.md`        : 22358 bytes, 281 lines, same sha256
    the two committed files are BYTE-EQUAL: True
    The digest EQUALS the one the reviewer stated for its pre-emission original.
    Both hops used `shutil.copyfile`; nothing was retyped.

G2 THE PLAN, at C1 — REAL exit 0.
    byte length 2211 · line count 42 · under 50 lines True
    byte-EQUAL to slice PLAN27 True (both sha256 8767405295593552c827d39c4f32deaffdb985cc80f97cfa3f71f70b3af5ca12)
    holds `## Goal` True · holds substring `Steps` True

G3 THE RECORD APPEND, at C2 — REAL exit 0.
    MEASURED base 1618414 + 1 + RECORD27 6988 = 1625403 = committed. RECONSTRUCTS True.
      (re-measured by this worker at the commit it appended at; it matches the
       1618414 the block stated, but the reading is this worker's own)
    pre-commit blob is byte PREFIX True · slice is exact SUFFIX True
    separator byte is a newline True
    N COUNTED by the script: 2. File blank-line units: 731.
    LAST 2 units EQUAL the slice's paragraphs IN ORDER True
      unit -2, 4472 bytes, `Gate: F033 R26 — THE OPERATOR GUIDE, ITS INDEX ROWS, A…`
      unit -1, 2514 bytes, `Done: R-0749 — BOTH INSTANCES ARE LANDED AND THE WIDEN…`
    NEGATIVE CONTROL: the FIRST appended paragraph spans 1618415..1622887; flip
      offset 1620651, inside that span True; byte b'r' flipped to b's'.
      reader PREFIX/SUFFIX accepts unflipped True / rejects flipped True
      reader PARAGRAPHS  accepts unflipped True / rejects flipped True

G4 THE LEDGER, at `7adee149` and at C2 — REAL exit 0.
    | rev | `^- R-\d+ — ` | distinct | `^Done: R-\d+ — ` | distinct | `^Landed: ` | `^Landed: R-0749 — ` | `^Gate: F033 R26 — ` | open |
    |-----|---------------|----------|-------------------|----------|-------------|----------------------|----------------------|------|
    | 7adee149 | 310 | 310 | 54 | 52 | 22 | 2 | 0 | 258 |
    | 0e0314dc | 310 | 310 | 55 | 53 | 22 | 2 | 1 | 257 |
    ADDED resolved ids `['R-0749']` — exactly the ordered id, and only it.
    ADDED registered ids `[]`; REMOVED registered `[]`; REMOVED resolved `[]`.
    Every ordered numeral reproduced, including `^Landed: R-0749 — ` still
    exactly 2 with both lines left standing beside the new `Done:` paragraph.

G5 THE BRANCH RUN — pytest REAL exit code 1.
    Command: `python3 -m pytest -n auto -q`, cwd `/home/decodeux/Repos/remedy`.
    REAL EXIT CODE (subprocess.run.returncode) = 1
    COUNTS: 2 failed, 18445 passed, 20 skipped.
    WALL CLOCK 188.3 s wall / 187.66 s pytest-reported. UNDER five minutes, so
    there is no perf note to raise.
    RAW TAIL:
        =========================== short test summary info ============================
        FAILED tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_unresolvable_job_id_matches_the_get_door
        FAILED tests/ui_server/test_live_state.py::TestUIServerIntegration::test_dashboard_no_raw_leaks
        2 failed, 18445 passed, 20 skipped in 187.66s (0:03:07)
    `branch_failed.txt` holds 2 lines.
    THE BRANCH SUITE IS THEREFORE NOT ALL-GREEN. Both failures are attributed
    under G7 below; both are SHARED with the merge base, so neither is a
    branch-only failure and neither is a blocker. NO "FULL SUITE GREEN" CLAIM IS
    MADE BY THIS HANDBACK; what is claimed is "full suite RUN, compared and
    attributed", with 2 environment-class failures standing on both sides.

G6 THE BASE RUN AND ITS PARITY — pytest REAL exit code 1; parity HOLDS.
    Worktree: `git worktree add -b tmp/base-gate .remedy-wt/base-gate bd8d9529`,
    REAL exit 0. Worktree HEAD `bd8d952942d8ec1d243d787ccfe16e0ad04360d2`,
    equal to the merge base True. Branch `tmp/base-gate`, NOT detached
    (constraint 6).
    THE COPY CALL AS WRITTEN: `shutil.copytree(src, dst, symlinks=True)` — for
    `apps/ui/node_modules` and again for `apps/ui/dist`. The keyword was passed
    explicitly, not defaulted.
    SYMLINKS: `apps/ui/node_modules` holds 27 symlinks at any depth in the
    source; 27 SURVIVED AS SYMLINKS in the copy. (The block stated 23 within
    three levels; this worker counted at every depth and reports its own number.
    `apps/ui/dist` holds 0 symlinks and 0 survived.) Neither destination is
    itself a symlink.
    `REMEDY_UI_NO_AUTO_BUILD` set to `'1'` in the runner's own `os.environ` and
    passed as `env=` (P2) — never as a shell prefix.
    Command: `python3 -m pytest -n auto -q`, cwd the worktree — identical to G5.
    REAL EXIT CODE (subprocess.run.returncode) = 1
    COUNTS: 114 failed, 18072 passed, 20 skipped.
    WALL CLOCK 151.8 s wall / 151.21 s pytest-reported. Under five minutes.
    THE P4 EVENT READING:
        run wall-clock window start 1788009268.624 end 1788009420.420 (151.8 s)
        `apps/ui/dist` files BEFORE 4, AFTER 4
        mtimes falling INSIDE the run window: 0
        files that APPEARED 0 · VANISHED 0 · mtimes CHANGED 0
    PARITY CLAIM = HOLDS, measured by the EVENT and not by a content hash.
    (A hash reading is reported separately under G7 and does not stand alone.)

G7 COMPARE AND ATTRIBUTE — REAL exit 0. Both halves discharged, neither
    conditioned on the other and neither conditioned on the parity claim.
    `comm -13 base_failed.txt branch_failed.txt` = BRANCH-ONLY, count 0.
    `comm -23 base_failed.txt branch_failed.txt` = the branch FIXED, count 112.
    Both written to `comparison.txt`. The sets are not both empty, so
    `attribution.txt` WAS created, as the change set's condition provides.
    ACCOUNTING, so no id of either run is left over:
        branch run FAILED lines 2   = branch-only 0   + shared 2
        base   run FAILED lines 114 = base-only  112  + shared 2

    (i) BRANCH-ONLY: the set is EMPTY. There is no id to re-run serially and no
        candidate for the BLOCKER class. The two failures of the branch run also
        failed at the merge base, so they are SHARED rather than branch-only.

    (ii) EVERY ONE OF THE 112 BASE-ONLY IDS IS ATTRIBUTED, by a measured A/B in
        the SAME worktree at the SAME commit with ONLY the artifact changed —
        not by scraping text.
        THE ARTIFACT NAMED, and it is the same one for all 112: the base
        worktree has no `apps/ui/dist` build that is FRESH relative to its own
        `apps/ui/src`. Measured:
            PRIMARY  dist/index.html mtime 1788009103.917 sha256 6f53e73d3842…
                     newest apps/ui/src mtime 1787993872.580
                     `_frontend_is_stale()` = False
            BASE WT  dist/index.html mtime 1788009103.917 sha256 6f53e73d3842…
                     newest apps/ui/src mtime 1788009266.881
                     `_frontend_is_stale()` = True
            dist/index.html BYTE-IDENTICAL in both trees = True
        So what the base worktree lacks is not the BYTES of the build — those
        were copied in and match — but a build whose mtime is not older than its
        own checked-out sources. `git worktree add` stamps the checkout with the
        worktree's creation time, which is newer than the build's preserved
        mtime. `ui_server._frontend_is_stale()` answers True there, and with
        `REMEDY_UI_NO_AUTO_BUILD=1` `_auto_build_frontend` returns None at its
        first line, so `_load_frontend` prints "ERROR: React UI not built." and
        calls `sys.exit(1)`, killing the server thread.
        A. ARTIFACT STALE (dist mtimes restored to exactly the copytree state):
           REAL exit 1, 112 failed in 567.16 s. ids FAILED = 112 of 112.
           "ERROR: React UI not built." appears 112 times.
           "[remedy-ui] auto-build" appears 0 times — P2 suppression confirmed.
        B. ARTIFACT FRESH (`os.utime` on the 4 dist files; nothing else touched,
           dist/index.html sha256 UNCHANGED by the touch):
           REAL exit 0, 112 passed in 15.24 s. ids PASSED = 112 of 112.
           "ERROR: React UI not built." appears 0 times.
        ids whose A/B is FAILED-then-PASSED = 112 of 112. UNATTRIBUTED = 0.
        The full per-id table is `.agent/gate_f033_r27/attribution.txt`.
        CORROBORATION from the base run's own output: "Failed: Server did not
        start in time" 114 occurrences, "ERROR: React UI not built." 114,
        "[remedy-ui] auto-build" 0, and every one of the 114 base failures is
        under `tests/ui_server/`.

    (iii) THE SHARED PAIR, attributed too although it falls in NEITHER comm set
        and G7 therefore does not demand it. These two are the whole reason the
        branch run's REAL exit is 1, so any "full suite" reading depends on them:
          `tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_unresolvable_job_id_matches_the_get_door`
            branch stderr: "[remedy-ui] auto-build (source changed)…" then
            "[remedy-ui] build failed: Command '['npm', 'run', 'build']' returned
            non-zero exit status 1." → "Server did not start in time".
          `tests/ui_server/test_live_state.py::TestUIServerIntegration::test_dashboard_no_raw_leaks`
            branch stderr: "[remedy-ui] auto-build (dist missing)…" →
            "ERROR: React UI not built." → "Server did not start in time".
        SAME ARTIFACT CLASS, measured on the branch side: at branch-run start the
        primary checkout's `apps/ui/dist` was STALE relative to `apps/ui/src`, so
        the auto-build fired under xdist. `npm run build` failed for the workers
        that reached the door first; a later attempt succeeded and rewrote
        `dist/index.html` at mtime 1788009103.917, which lies INSIDE the branch
        run's window 1788009029.235..1788009217.499 (True) — which is also why
        `_frontend_is_stale()` reads False in the primary checkout now. The
        second id's "dist missing" is that rewrite observed mid-flight.
        The branch run was NOT given `REMEDY_UI_NO_AUTO_BUILD=1`, correctly:
        docs/agents/integration_gate.md sets it for the BASE run only.

G8 CLEANUP AND STRUCTURE, at C3 — REAL exit 1. FIVE CLAUSES HOLD, ONE DOES NOT.
    `git worktree list` -> `/home/decodeux/Repos/remedy  e313c0c0 [feature/f033-hunk-approval-v2]`
      — the primary checkout ALONE. True.
    `git branch --list tmp/base-gate` -> `''`, EMPTY True.
    `git status --porcelain` -> `''`, EMPTY True.
    `git ls-files --others --exclude-standard` -> 0 paths total; paths naming
      `remedy-wt` = 0. This is the evidence P1 asks for: a log growing under the
      gitignored `.remedy-wt/` is invisible to the run manifest's untracked
      input, which is R-0176's substance.
    PER-COMMIT INSERTIONS, C0a through C3, every commit single-parent:
        baf2bf52 281 · 365bddf2 204 · e9543cd2 16 · 0e0314dc 4 ·
        b04bde68 390 · 9cee95b6 439 · e313c0c0 7561
      EVERY COMMIT UNDER 500 = **False**. Exactly one commit is over:
      `e313c0c0`, 7561 insertions, the base run log. See deviation 3. NOTHING
      WAS TRUNCATED TO MAKE THIS CLAUSE HOLD, and the real number is reported
      rather than a word.
    PATH SET over `7adee149`..C3 EQUALS the change set minus `.agent/handoff.md`
      in BOTH directions: `measured - declared` [] and `declared - measured` [].
      Eleven paths, all under `.agent/`, the conditional `attribution.txt`
      included because G7 produced ids to attribute.

## Authored-text proofs

Both slices were EXTRACTED from the committed `.agent/authored/f033-r27.md` by
script — neither was retyped at any point. Extraction asserted exactly one
`<<<BEGIN` and one `<<<END` marker per name.

| Slice | bytes | lines | sha256 (head) | disk-to-disk result |
|-------|-------|-------|---------------|---------------------|
| PLAN27 | 2211 | 42 | 87674052955935… | `.agent/plan.md` byte-EQUAL, G2 |
| RECORD27 | 6988 | 3 (2 paragraphs) | 0d3b8b0b0c148c… | exact SUFFIX of `.agent/live_review.md` at C2, G3 |

Transport comparison for the block itself: `.remedy-wt/f033-r27-block.md`,
`.agent/authored/f033-r27.md` and `.agent/last_block.md` are all 22358 bytes
over 281 lines at sha256
`5b81aa42a97c5592e104c09c1b1a6c11ff2c260fc9a2e2cb2703c202521bbcf9`, byte-equal
to each other and to the digest the reviewer stated. Reading `.remedy-wt/` was
NOT denied to this worker, so the report-and-stop fallback was not used.

## Deviations & assumptions

1. C3 WAS SPLIT INTO THREE COMMITS. The block's Bundle names C3 as one commit
   that "commit[s] the evidence files"; this worker committed them as `b04bde68`
   (branch_run.txt, 390), `9cee95b6` (the five small files, 439) and `e313c0c0`
   (base_run.txt, 7561). REASON: AGENTS.md Commit Discipline says "If a diff
   exceeds 500 lines, stop and split before committing", and the seven evidence
   files total 8390 insertions. Splitting this way makes six of the seven files
   land in commits that MEET the 500 cap and isolates the overage to the one
   file that cannot be split at all. A departure from the ordered commit
   sequence belongs here even when it is correct (R-0485), which is why it is
   stated first. Nothing was added or dropped — only regrouped.
2. THE ORDERED SEQUENCE IS OTHERWISE UNCHANGED. C0a, C0b, C1, C2, then C3 as
   above, then C4. Eight single-parent commits, nothing reordered.
3. ONE COMMIT EXCEEDS THE 500-INSERTION CAP, DECLARED HERE BEFORE REVIEW WITH
   ITS INSEPARABILITY REASON, AND THE FEATURE'S ALLOWANCE FOR ONE IS ALREADY
   SPENT. `e313c0c0` adds `.agent/gate_f033_r27/base_run.txt` at 7561
   insertions. INSEPARABILITY: it is a single file — the base run's full pytest
   output — and a file cannot be added by two commits. Its size is a consequence
   of 114 environment-class failures each carrying a full traceback, not of
   scope. It was NOT truncated: the block's G6 orders `base_run.txt` written,
   the round's whole purpose is the evidence, and trimming a run log to fit a
   line cap is exactly the "weaken it to make the check green" move the brief
   forbids. THE PART THE REVIEWER MUST RULE ON: AGENTS.md admits a declared
   oversize commit only when "it is the only such commit in its feature", and it
   is NOT — this worker measured every commit on the branch and found
   `5f0273d8` "docs(f033): put the round 16 verdict on disk" at 647 insertions
   already standing. By the letter of AGENTS.md this is therefore a SECOND
   oversize commit and a Medium finding. It is declared rather than avoided
   because the alternative was destroying evidence. No ceiling was raised and no
   rule was reinterpreted by this worker.
4. G8 IS RED AND WAS NOT REPAIRED. Its insertion clause does not hold, for the
   reason in deviation 3. Per the brief this worker did not repair it on its own
   initiative; it is reported with its REAL exit code 1 and its real numbers.
   The other five G8 clauses hold.
5. G5 AND G6 CARRY PYTEST EXIT CODE 1. This is the measurement the gate exists
   to take, not a gate failure: the branch run has 2 failures and the base run
   114. Both are fully attributed under G7. This handback makes NO unqualified
   "full suite green" claim; it claims the suite was RUN on both sides, compared
   and attributed, with an EMPTY branch-only set.
6. THE SYMLINK COUNT THIS WORKER REPORTS IS 27, NOT THE BLOCK'S 23. The block
   measured 23 "within three levels"; this worker walked
   `apps/ui/node_modules` to any depth and counted 27, of which 27 survived as
   symlinks. The two readings do not contradict each other — they are different
   reaches — and the ordered property (survival under `symlinks=True`) holds on
   this worker's own wider count.
7. THE FIRST ATTRIBUTION SCRIPT WAS DISCARDED AND REWRITTEN. Its per-id evidence
   came from scraping pytest's failure headers out of `base_run.txt`; pytest
   truncates long headers, so it matched only 47 of 112 and its verdict regex
   also mishandled a node id containing a space (`…[has space]`). It reported 65
   ids "UNATTRIBUTED" and one id "not passing" — BOTH ARTEFACTS OF THE SCRIPT,
   not of the product, since that same run's own summary was "112 passed" at
   REAL exit 0. Rather than report a false gap, this worker replaced the text
   scrape with the measured A/B now in `attribution.txt`. Disclosed because it
   happened; only the A/B result is reported above. The discarded script was
   removed by exact path.
8. THE A/B TOUCHED THE BASE WORKTREE AFTER THE BASE RUN AND AFTER `parity.txt`
   WAS WRITTEN. `os.utime` was applied to the 4 files under the worktree's
   `apps/ui/dist` — inside the throwaway worktree only, which is where
   constraint 7 confines environment-mutating work, and only once the P4 window
   was closed and recorded. The primary checkout was never mutated. The parity
   reading in `parity.txt` predates and is unaffected by it.
9. A DEFECT OUTSIDE THE CHANGE SET, DECLARED AND NOT TOUCHED. The UI auto-build
   is racy under xdist: when `apps/ui/dist` is stale at run start, several
   workers reach `_load_frontend` at once, `npm run build` fails for the first
   to arrive, and those tests fail with "Server did not start in time" while the
   rest pass after a later build succeeds. That is exactly the branch run's 2
   failures, and it also means a full-suite run REWRITES `apps/ui/dist`
   mid-flight — measured: dist/index.html mtime 1788009103.917 lies inside the
   branch run window 1788009029.235..1788009217.499. It is a real
   test-infrastructure hazard against a green full suite, it is NOT feature
   code, and this round changed no file under `packages/`, `apps/`, `tests/` or
   `docs/`. Reported for the reviewer to register or dismiss; no id was minted
   by this worker and nothing was repaired.
10. `comm` WAS RUN WITH `LC_ALL=C` PASSED THROUGH `env=` IN PYTHON. The two
    `*_failed.txt` files are sorted by Python's byte ordering, so `comm` was
    given byte collation to match. Not a shell prefix — the sandbox forbids
    that (constraint 9) — and the exit code was still taken from
    `subprocess.run(...).returncode`.
11. Scratch scripts and run logs lived under the gitignored `.remedy-wt/` and
    were run as `python3 -B <path>`. All were removed BY EXACT PATH, never by
    glob; `git status --porcelain` is empty and
    `git ls-files --others --exclude-standard` returns 0 paths.

## Next

The reviewer books the round-27 verdict and rules on the two open questions this
gate raises, neither of which a worker may settle: (a) whether `e313c0c0`, the
second oversize commit in this feature, is accepted with its inseparability
reason or whether the base run log must be recorded some other way, and (b)
whether the 2 shared `tests/ui_server/` failures — environment-class, present on
BOTH sides, branch-only set EMPTY — are compatible with the closure's "full
suite" language, or whether the auto-build race of deviation 9 must be fixed
first in a round of its own. The branch-only set being empty means no BLOCKER
was found in feature code. After that: the closure sequence per
docs/roadmap/STATUS_closure_protocol.md and its pull request, which is NOT
merged in this session.
