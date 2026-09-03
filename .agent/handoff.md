# Handback — F109 Semantic dedupe, round 17 — THE INTEGRATION GATE

## Session

SESSION 4 of feature F109 · round 17 · rounds so far 17

Soft limit is 25 rounds / 7 sessions (self_drive_protocol.md G7, amend0827 rule
6). At 17 rounds and 4 sessions it is NOT reached, so no scope report is due.
`.agent/STOP` was read from disk at the start of the round and does not exist;
it was re-checked before the handback and still does not exist.

## THE INTEGRATION GATE RESULT — the one sentence

**The branch ran 18937 passed / 20 skipped / 0 failed at exit 0, the merge base
ran 18799 passed / 20 skipped / 0 failed at exit 0, the branch-only failure set
is EMPTY (0 ids) and the base-only set is EMPTY (0 ids), so NO BLOCKER was
found.**

## Range

Review of `35c0b03f..HEAD` (HEAD is the commit this file is written in).

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C0a `a5a0141f` | done | block copied verbatim with `shutil.copyfile`; G1 `cmp` exit 0 against the reviewer's own `.remedy-wt/f109-r17.md` |
| C0b `eb3420da` | done | mirrored to `.agent/last_block.md`; one sha256 for all three copies |
| C1 `bd224463` | done | PLAN17 extracted by delimiter index from the COMMITTED authored copy and applied; G2 `cmp` exit 0, 43 lines |
| C2 `ee285c44` | done | RECORD17 appended as the two bytes `\n\n` + slice; G3 (a)(b)(c)(d) all pass |
| C3 `cce5f9d7` | done | PAIR E applied byte for byte; FROM 1→0, TO 0→1, 130 cases collected before and after |
| C4 `9fdfaab1` | done | 9 evidence files under `.agent/gate_f109_r17/`, all `.txt`, written only after both suites exited |
| C5 (this commit) | done | handback rewritten per handback_template.md, then pushed |

No item was skipped and none deviated. The block's ordered commit sequence was
followed exactly — no extra commit, no dropped commit, no reordering. The
DEVIATIONS section below records three method deviations INSIDE C4's gate work;
none of them changed the commit sequence.

## Commits

### a5a0141f F109 R17 C0a: save the round 17 block verbatim under agent authored

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f109-r17.md` | +289 / -0 | the reviewer's round 17 block, byte-for-byte |

### eb3420da F109 R17 C0b: mirror the round 17 block to last_block

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +197 / -235 | mirror of the saved block; single-state-file rewrite |

### bd224463 F109 R17 C1: the plan names round 17 as the integration gate

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | +14 / -14 | PLAN17 applied whole; Current Step is now the gate, Risks gains the blocker rule |

### ee285c44 F109 R17 C2: book round 16 PASS, resolve R-0780 and R-0781, register R-0782

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | +9 / -1 | RECORD17's four paragraphs appended; the `-1` is the no-trailing-newline last line being extended, not a rewrite |

### cce5f9d7 F109 R17 C3: repair R-0782 - the capture helper names the consumer that exists

| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_semantic_dedupe.py` | +8 / -5 | PAIR E, one docstring in `_capture_compositions`; no executable line moved |

### 9fdfaab1 F109 R17 C4: the integration gate evidence - both suites green, no branch-only failure

| Path | +/- | Reason |
|------|-----|--------|
| 9 files under `.agent/gate_f109_r17/` | +182 / -0 | `attribution.txt` +77, `gate_summary.txt` +63, `parity_mtime.txt` +18, `branch_run_tail.txt` +12, `base_run_tail.txt` +12, and the four comparison files `branch_failed.txt`, `base_failed.txt`, `branch_only.txt`, `fixed_by_branch.txt` at 0 lines each — the empty set committed as a reading |

### C5 (this commit) F109 R17 C5: handback for round 17

| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewrite | a handoff cannot table the commit that writes it (R-0149 pattern) |

Insertion counts, `+` column ONLY per AGENTS.md DECISION F104 D1, read from
`git show --numstat` and compared cell by cell with the table above: 289, 197,
14, 9, 8, 182. Every commit is under the 500-line cap; no oversize commit was
declared and none exists.

## External actions

| Command | Outcome |
|---|---|
| `git worktree add -b tmp/base-gate .remedy-wt/base-gate 5e18a8536afa086b591b5a2e13009d68d6227432` | created; "HEAD is now at 5e18a853 Merge pull request #231 …" |
| `git worktree remove --force .remedy-wt/base-gate` | removed, no output |
| `git worktree prune` | no output |
| `git branch -D tmp/base-gate` | "Deleted branch tmp/base-gate (was 5e18a853)" |
| `git worktree list` | 5 lines: the primary checkout plus the four PRE-EXISTING `remedy/job-*` worktrees; `base-gate` absent |
| `git branch --list 'tmp/*'` | no output, exit 0 |
| `ls .remedy-wt/base-gate` | "No such file or directory" |
| `git push -u origin feature/f109-semantic-dedupe` | see Push below |

No PR was created, none was merged, nothing was force-pushed, and `main` was
never checked out.

## Verification — the eight gates, real commands and real exit codes

### G1 TRANSPORT — PASS

    cmp .remedy-wt/f109-r17.md .agent/authored/f109-r17.md
    REAL_EXIT=0

    sha256sum .agent/authored/f109-r17.md .agent/last_block.md .remedy-wt/f109-r17.md
    61f5632a9c6f58749486ad49573d3ba205dfeaba167533a668373f62bc650161  .agent/authored/f109-r17.md
    61f5632a9c6f58749486ad49573d3ba205dfeaba167533a668373f62bc650161  .agent/last_block.md
    61f5632a9c6f58749486ad49573d3ba205dfeaba167533a668373f62bc650161  .remedy-wt/f109-r17.md

One digest three times. The left side of the `cmp` is the reviewer's OWN
scratch original, so this is real transport and not self-consistency.

### G2 THE PLAN — PASS

    cmp .remedy-wt/r17_plan17.txt .agent/plan.md      G2_CMP_EXIT=0   (no output)
    wc -l .agent/plan.md                              43              (< 50, AGENTS.md)
    grep -c '^## Goal' .agent/plan.md                 1
    grep -c '^## Next Steps' .agent/plan.md           1

PLAN17 was extracted by delimiter index from the COMMITTED authored copy;
`BEGIN PLAN17` / `END PLAN17` never reached the file.

### G3 THE RECORD APPEND — PASS, all four readings

(a) ARITHMETIC

    blob at 35c0b03f == file on disk : True
    base_size                        : 2112853
    base_sha256                      : 27f9d1b9bfbb530fabaf895bf473469632af2ee14bd56e14196ba06f1c9e83bc
    base ends with a newline         : False
    appended length S                : 6693   (the two bytes \n\n + RECORD17)
    new_size                         : 2119546
    base + S == new_size             : True
    new_sha256                       : f934a2a18754767ab3428c1db06b86d83ced20c058b2a70532685ca504e9222d
    new ends with a newline          : False

(b) A SECOND READER THAT COUNTS NO BYTE, over the WHOLE appended region

    N, counted by the script from the slice itself : 4
    total blank-line units in the tracked file     : 886
    reader accepts the tracked file                : True

    unit 1/4 opening60: 'Gate: F109 R16 — the round 16 entry. VERDICT PASS, over the '
    unit 2/4 opening60: 'Done: R-0780 — RESOLVED at `9dab6cae` and verified by the re'
    unit 3/4 opening60: 'Done: R-0781 — RESOLVED at `ca4879b4` and verified by the re'
    unit 4/4 opening60: "- R-0782 — Low, A TEST HELPER'S DOCSTRING STILL SAYS THE DED"

    The four RECORD17 paragraphs print the same four openings, in order.

(c) NEGATIVE CONTROL on the FIRST appended paragraph

    tracked sha256 BEFORE : f934a2a18754767ab3428c1db06b86d83ced20c058b2a70532685ca504e9222d
    copied to .remedy-wt/live_review_negative_control_r17.md
    flipped byte at offset 2112895: b'E' -> b'e'   (inside paragraph 1)
    reader (b) ACCEPTS the mutated control : False   <- rejects, as required
    reader (b) ACCEPTS the tracked file    : True    <- still accepts
    tracked sha256 AFTER  : f934a2a18754767ab3428c1db06b86d83ced20c058b2a70532685ca504e9222d
    tracked sha256 unchanged : True
    os.remove(.remedy-wt/live_review_negative_control_r17.md)
    os.path.exists(that exact path) : False

(d) COUNTS AS A SET DIFFERENCE, never a subtraction (`R-0778`)

Base read with `git show cf210f6f:.agent/live_review.md`, never by rewinding
the tracked file. (`cf210f6f` blob == `35c0b03f` blob: **False** — round 16 did
append there, so the base below is the round-16 base, exactly as ordered.)

    | figure | base cf210f6f | new, after C2 |
    |---|---|---|
    | registered id lines | 341 | 343 |
    | DISTINCT registered ids | 341 | 343 |
    | `Done:` lines | 66 | 68 |
    | DISTINCT resolved ids | 64 | 66 |
    | `len(set(registered) - set(resolved))` | 277 | 277 |

    grep -c '^Gate: F109 R16 — '  = 1
    grep -c '^Done: R-0780 — '    = 1
    grep -c '^Done: R-0781 — '    = 1
    grep -c '^- R-0782 — '        = 1

The open set stays 277 because this round resolved two ids and registered one.
The two ids carrying more than one `Done:` line are `R-0721` and `R-0725` —
the exact reason `R-0778` demands a set difference; 343 − 68 would read 275
and be wrong.

### G4 PAIR E AND THE PROOF THAT NO CODE MOVED — PASS

    containment, TO contains FROM : False   (so this is a REWRITE)
    FROM count BEFORE C3 : 1        TO count BEFORE C3 : 0
    FROM count AFTER  C3 : 0        TO count AFTER  C3 : 1

    dedupe suite collected BEFORE C3 : 130 tests collected in 0.15s, exit 0
    dedupe suite collected AFTER  C3 : 130 tests collected in 0.25s, exit 0

AST comparison from `git show <sha>:<path>` blobs ONLY, `ee285c44` vs
`cce5f9d7`, docstring excluded from every body:

    definition count BEFORE : 154   AFTER : 154
    definition NAME sets identical : True
    statement maps identical       : True
    line count BEFORE : 2311   AFTER : 2314

No executable line moved; the only change is inside one docstring.

### G5 THE INTEGRATION GATE — BRANCH RUN — PASS (exit 0)

    integration_gate.md step 1, at C3's tree (cce5f9d7)
    pytest.main(["-n", "auto", "-q"]) from /home/decodeux/Repos/remedy
    (shell ENV assignment is denied here, so pytest runs as a library; NO env
    var is set for the branch run — step 1 asks for a plain run)

    raw tail : 18937 passed, 20 skipped in 133.20s (0:02:13)
    FAILED list : EMPTY — `grep '^FAILED' <log>` returned nothing
    PYTEST_EXIT_CODE = 0
    wall : 133.20s reported by pytest, 133.48s measured around the call

Against the reviewer's four figures at `35c0b03f` (18937 passed, 20 skipped, 0
failed, exit 0, 133.30s): passed MATCHES, skipped MATCHES, failed MATCHES,
exit MATCHES, wall differs by 0.10s. No divergence to declare.
`.agent/gate_f109_r17/branch_failed.txt` is committed at 0 lines — the empty
set written down, not skipped.

### G6 THE INTEGRATION GATE — BASE RUN AND COMPARISON — PASS (exit 0)

Base worktree on a BRANCH, never detached (DECISION D3):

    git worktree add -b tmp/base-gate .remedy-wt/base-gate 5e18a8536afa086b591b5a2e13009d68d6227432
    git merge-base main feature/f109-semantic-dedupe -> 5e18a8536afa086b591b5a2e13009d68d6227432  (confirmed)

Parity restored BEFORE the run:

    shutil.copytree(apps/ui/node_modules, ..., symlinks=True)
        44839 entries, 27 of them symlinks PRESERVED
    shutil.copytree(apps/ui/dist, ..., symlinks=True)
        5 entries, 0 symlinks
    git -C .remedy-wt/base-gate status --porcelain -> EMPTY (both are gitignored)

    base run: REMEDY_UI_NO_AUTO_BUILD set IN-PROCESS, then
              pytest.main(["-n","auto","-q"]) from .remedy-wt/base-gate
    raw tail : 18799 passed, 20 skipped in 159.88s (0:02:39)
    FAILED list : EMPTY — `grep '^FAILED'` exit 1
    PYTEST_EXIT_CODE = 0
    wall : 159.88s reported, 160.11s measured around the call

MTIME PARITY, MEASURED AS AN EVENT (R-0444), not as an outcome:

    run window : 1788410860.264 .. 1788411020.379
                 (2026-09-03 06:47:40 .. 06:50:20)
    4 files under the base worktree's apps/ui/dist, each read before and after:
      assets/diffHighlightGrammars-o9XqnLhb.js  before=1788410854.675 after=1788410854.675 in_window=False
      assets/index-Bh0mkYBD.js                  before=1788410854.675 after=1788410854.675 in_window=False
      assets/index-D_qZGOuo.css                 before=1788410854.675 after=1788410854.675 in_window=False
      index.html                                before=1788410854.675 after=1788410854.675 in_window=False
    accompanying content digest, before and after, identical:
      846b7f62fa3c13a8fd3ecd7c54dfd89771af272843530a59bd318d7e006f7a51

**THE PARITY CLAIM HOLDS.** No mtime falls inside the run window, so
`apps/ui/dist` was not rebuilt during the base run. The digest accompanies that
reading; it does not stand in for it.

COMPARISON (integration_gate.md step 3):

    grep '^FAILED' branch log | sort > branch_failed.txt        0 lines
    grep '^FAILED' base   log | sort > base_failed.txt          0 lines
    comm -13 base_failed.txt branch_failed.txt > branch_only.txt      0 lines
    comm -23 base_failed.txt branch_failed.txt > fixed_by_branch.txt  0 lines

Because the base-only set is EMPTY, there is no `comm -23` id to attribute and
no unattributed id can block the verdict. Test-count delta: 18937 − 18799 =
138 cases added by this branch, of which the dedupe suite alone collects 130.

### G7 THE INTEGRATION GATE — ATTRIBUTION — PASS, empty set recorded

**The branch-only set is EMPTY**, so integration_gate.md step 4 has no id to
classify. `.agent/gate_f109_r17/attribution.txt` states that empty result and
the four commands that produced it, so the emptiness is a written reading.

That file additionally carries an APPENDIX I chose to write rather than drop:
two EARLIER branch invocations of this round, whose METHOD was flawed, did go
red, and it would be dishonest to leave that unrecorded. Invocation 1 (1
failed) and invocation 2 (4 failed) between them produced five distinct ids —
three in `tests/orchestration/test_product_smoke.py`, two in
`tests/cli/test_job_rerun_workspace_identity.py`. All five were re-run
SERIALLY at `cce5f9d7`:

    python3 -m pytest <the five node ids> -p no:xdist -q
    5 passed in 3.35s
    REAL_EXIT=0

serial-pass ⇒ XDIST-FLAKE class (F135/F052) — recorded, not a blocker. Direct
evidence per class: the three smoke ids died on
`OSError: [Errno 98] Address already in use` binding port 5273, all on worker
gw5 (two parallel workers contending for one port; `ss -ltnp` and
`pgrep -af good_app.py` afterwards showed no listener and no surviving
process); the two workspace-identity ids died on a `remedy_worktree_digest`
mismatch whose builder folds in the outcome of four `git` subprocesses, each
contributing a FAILED marker to the hash on timeout, and those calls are
load-coupled under 16 xdist workers. Neither class touches F109 code.

**NO BLOCKER WAS FOUND. No reproducible branch-only failure coupled to F109
code exists.**

### G8 THE TREE AND THE SWEEP — PASS

    git status --porcelain        -> EMPTY
    git ls-files .remedy-wt       -> nothing
    git worktree list             -> primary + 4 PRE-EXISTING remedy/job-* worktrees;
                                     .remedy-wt/base-gate is ABSENT
    git branch --list 'tmp/*'     -> no output, exit 0
    ls .remedy-wt/base-gate       -> No such file or directory

Insertion counts from `git show --numstat`, `+` column only, compared cell by
cell with the `## Commits` table above — every cell agrees:

    a5a0141f  .agent/authored/f109-r17.md                 +289  -0     TOTAL 289
    eb3420da  .agent/last_block.md                        +197  -235   TOTAL 197
    bd224463  .agent/plan.md                              +14   -14    TOTAL 14
    ee285c44  .agent/live_review.md                       +9    -1     TOTAL 9
    cce5f9d7  tests/orchestration/test_semantic_dedupe.py +8    -5     TOTAL 8
    9fdfaab1  9 files under .agent/gate_f109_r17/         +182  -0     TOTAL 182

THE STALENESS SWEEP, over every file this round touched:

- `.agent/plan.md` — no stale sentence. Its risk bullet "every concrete adapter
  returns `supports_resume = False` … `docs/system/semantic-dedupe-v1.md`
  states this plainly" was re-measured against that doc: lines 99-105 say
  exactly that, naming `ClaudeProvider`, `ClaudeCliProvider` and
  `OllamaPingPongProvider`. The blocker bullet it gained is a standing rule,
  not a claim about this run, and remains true although no blocker was found.
- `.agent/live_review.md` — no stale sentence. The `R-0782` entry's factual
  claims were re-measured independently, not accepted: `build_trace_entry` in
  `packages/orchestration/prompt_trace.py` line 172 really does read
  `list(composed_prompt.deduped_names)`, and
  `git log -S deduped_segment_names -- packages/orchestration/prompt_trace.py`
  names `78d2b7b5` as the commit that introduced it, so the repaired docstring's
  attribution of the consumer to that commit is correct.
- `tests/orchestration/test_semantic_dedupe.py` — the repaired docstring is
  true as written. `grep` for "no consumer", "lacks a production",
  "no production caller" and "not consumed" over the whole file now returns
  nothing, so `R-0782`'s stated resolution condition is met.
- `.agent/gate_f109_r17/*` — written this round from this round's readings.
- `.agent/authored/f109-r17.md` and `.agent/last_block.md` — verbatim copies of
  the reviewer's block; nothing in them may be edited by the worker.

ONE SENTENCE FOUND STALE-ADJACENT AND DELIBERATELY NOT REPAIRED, declared here
per constraint 7 rather than fixed: `tests/orchestration/test_semantic_dedupe.py`
line 1837, inside `test_a_disabled_run_reports_no_deduped_names_on_any_composition`,
carries the COMMENT "because the report never reaches ``PingPongResult``". That
sentence is still literally TRUE — the `ComposedPrompt` object does not reach
`PingPongResult` — but it is the same shape of wording that `R-0782` was
registered against, and a reader who has just read the repaired docstring may
find the two uneven. It is a comment, not a docstring, so it does not touch
`R-0782`'s resolution condition, and PAIR E authorized exactly one docstring.
I did not touch it. The reviewer may want it as a candidate, not a finding.

## Authored-text proofs

| Slice | Target | Proof |
|---|---|---|
| whole block | `.agent/authored/f109-r17.md` | `cmp` against the reviewer's own `.remedy-wt/f109-r17.md`, exit 0; one sha256 for all three copies |
| PLAN17 | `.agent/plan.md` | extracted by delimiter index, `cmp` exit 0, whole file |
| RECORD17 | `.agent/live_review.md` | G3 (a) exact byte arithmetic, (b) a byte-free paragraph reader over the whole appended region, (c) a negative control that the reader rejects |
| PAIRE_FROM / PAIRE_TO | `tests/orchestration/test_semantic_dedupe.py` | FROM 1→0, TO 0→1; AST proof that no executable statement moved |

Every slice was applied BYTE FOR BYTE by delimiter index. Nothing was rewrapped,
re-indented or improved, and no slice looked wrong.

## Deviations & assumptions

None of the following changed the block's ordered commit sequence: every
deviation is inside the METHOD of C4's gate work.

1. **THE BLOCK'S CONSTRAINT 6 IS UNSAFE AS WRITTEN, AND I DECLARE IT RATHER
   THAN ONLY WORKING AROUND IT.** Constraint 6 says to write a running suite's
   log to `.remedy-wt/`. `.remedy-wt/` is INSIDE the repo the suite measures. My
   first branch invocation followed it literally and went red with one failure
   in `tests/cli/test_job_rerun_workspace_identity.py`, which is the R-0176
   signature the constraint exists to prevent. I then read the digest builder
   rather than guessing: `worktree_identity()` in
   `packages/orchestration/run_manifest.py` line 500 enumerates untracked
   entries with `git ls-files --others --exclude-standard`, so a GITIGNORED file
   cannot enter the digest and `.remedy-wt/` was NOT in fact the cause — the
   first reading I reached for was wrong and I am recording that it was wrong.
   Regardless, I changed the method to the strictly safer one: the transcript is
   buffered IN MEMORY and written to disk only after `pytest.main` returns, which
   is what integration_gate.md step 2 actually asks for ("copied into the
   `.agent/gate_*` evidence dir only after the run exits"). All reported runs use
   the in-memory method.
2. **I DID NOT SET `REMEDY_UI_NO_AUTO_BUILD` ON THE BRANCH RUN.** The block's
   sandbox-delta section describes setting it in-process for "the gate"; the
   canonical procedure sets it for the BASE run only (integration_gate.md step 3)
   and orders a plain `python3 -m pytest -n auto -q` for the branch (step 1). My
   second branch invocation set it anyway and went red with 4 failures; the
   third, plain, matched the reviewer's own reading exactly. The gate doc is
   canonical, so the branch run reported above is the plain one. The env var is
   set for the base run, as ordered.
3. **PARITY RESTORATION NEEDED A THIRD STEP THE BLOCK DID NOT NAME, AND THE
   FIRST BASE RUN IS REPORTED AS A DISCARDED READING.** After copying
   `node_modules` and `dist` with `symlinks=True`, the first base run produced
   **126 failures, all in `tests/ui_server/`**, every one dying on
   `Failed: Server did not start in time` with `ERROR: React UI not built.` on
   stderr. This is the R-0736 trap the block warned about, reaching further than
   the block expected: `git worktree add` stamps the checkout with the CURRENT
   time while `copytree` PRESERVES source mtimes, so `_frontend_is_stale()` in
   `ui_server.py` line 3071 saw source as newer than the build and demanded a
   rebuild that `REMEDY_UI_NO_AUTO_BUILD=1` then refused. Measured directly in
   the base worktree, not inferred:

       dist/index.html mtime       : 1788057215.854  (2026-08-30 04:33:35)
       newest apps/ui/src mtime    : 1788410595.645  (2026-09-03 06:43:15)
       source files under src      : 142
       source files NEWER than dist: 142
       _frontend_is_stale() would be: True

   I restored real parity by re-stamping every file under the base worktree's
   `apps/ui/dist` to the current time (content untouched — the digest is
   identical before and after) and re-measured:

       source files NEWER than dist: 0
       _frontend_is_stale() would be: False

   and re-ran the whole base suite, which is the run reported in G6: 18799
   passed, 0 failed, exit 0. THE DISCARDED FIRST BASE RUN IS DECLARED HERE
   rather than quietly dropped: it was 126 failed / 18673 passed, and its 126
   ids are attributed by direct evidence to ONE environment class — a base
   worktree whose UI build is older than its own checkout — not to the branch.
   The re-stamp happened BEFORE the reported run, so the R-0444 event reading in
   G6 is untouched by it: the before-mtimes were re-recorded after the re-stamp
   and no mtime falls inside that run's window.
4. **FOUR PRE-EXISTING `remedy/job-*` WORKTREES UNDER `.remedy-wt/` WERE LEFT
   ALONE.** They were present at round start (`git worktree list` before any
   work) and are outside the change set. `git worktree list` at the end shows
   them; only `.remedy-wt/base-gate` was created and removed by this round.
5. **`.remedy-wt/f109-r17.md`, THE REVIEWER'S OWN ORIGINAL, WAS NOT DELETED.**
   It is the left side of G1's `cmp` and the reviewer may want to re-run that
   comparison. Every scratch file I created was deleted by its EXACT path; none
   by glob.
6. **NO `Done:` OR `Landed:` LINE WAS WRITTEN FOR `R-0782`.** The block does not
   order one, and round 16 set the precedent that the worker repairs and the
   reviewer books the resolution. The repair is on disk at `cce5f9d7`.

Assumptions: none beyond the above. `.agent/context.md` and
`.agent/decisions.md` needed no update — no scope, assumption, constraint or
non-obvious technical tradeoff changed that is not already recorded here and in
`.agent/live_review.md`.

## Open findings

Recomputed as a SET DIFFERENCE, never a subtraction (`R-0778`), after C2:

    registered id lines      343
    DISTINCT registered ids  343
    'Done:' lines            68
    DISTINCT resolved ids    66
    OPEN = |registered - resolved|  =  277

`R-0721` and `R-0725` each carry two `Done:` lines, which is why 343 − 68 = 275
would be the wrong reading.

`R-0782` is registered and REPAIRED on disk at `cce5f9d7` but not yet booked
resolved; its resolution line is the reviewer's to write next round.

## Next

The single expected next action: the reviewer re-runs these eight gates over
`35c0b03f..HEAD`, issues the round 17 verdict and the INTEGRATION GATE verdict
(only the reviewer may issue it — integration_gate.md step 5), books `R-0782`'s
resolution, and then opens the closure sequence of
`docs/roadmap/STATUS_closure_protocol.md`: the evidence job, a FRESH review zip,
the authored STATUS line and the PR. Phase 1 rule 1 first — re-read
`.agent/STOP` from disk before anything else.
