── STEP T003 / F275 — ROUND 45 — repair the guard the reviewer wrote wrong ──

Goal:
  THE BRANCH TIP IS RED ON ONE TEST AND THE FAULT IS THE REVIEWER'S. The guard round 44
  landed, `tests/test_model_construction_keywords.py`, sweeps every TRACKED `*.py` file for
  a keyword the model does not declare — and its own premise test writes
  `Task(description="d", type="write_readme")`. Once the file is tracked it therefore
  reports ITSELF, and it did: the single offender at the tip is that file's own line 113.
  That is planner_reviewer_prompt.md §3 item 2 exactly, a zero-gate counting a string the
  same block writes into the file the gate reads, and the reviewer's own red proof could not
  see it because the guard was UNTRACKED in the dry-run worktree, where `git ls-files` does
  not look. This round repairs it, books the round 44 FAIL verdict, and records the
  authoring lesson. It mints no id and resolves none.

  THE ROUND 44 WORKER DID NOTHING WRONG. Constraint 1 of that block forbade editing a slice
  "even where you believe it wrong — declare it instead", and it applied the defective slice
  byte for byte, measured both states, proved the sweep still reaches the mutated line by a
  reading the block did not order, and declared the ordered colour proof VOID rather than
  reporting it as a pass. That is the round rescuing the reviewer.

Bundle:
  C0a  save this block verbatim as `.agent/authored/f275-r45.md`
  C0b  mirror that file into `.agent/last_block.md`
  C1   the plan — slice PLAN45, whole-file replacement
  C2   the record — slices RECORD45 and SLIPS45, two appends
  C3   the repair — the single pair PAIR45
  C4   the handback

Change: exactly these paths and nothing else.
  .agent/authored/f275-r45.md                      (new, C0a)
  .agent/last_block.md                             (C0b)
  .agent/plan.md                                   (C1)
  .agent/live_review.md                            (C2)
  .agent/prose_slips.md                            (C2)
  tests/test_model_construction_keywords.py        (C3)
  .agent/handoff.md                                (C4)

WHY THE REPAIR TAKES THIS FORM AND NOT AN EXEMPTION. The obvious fix is to have the sweep
skip its own file. It is rejected, and the reason is recorded because it is the kind of
choice a later reader reverses: an exemption makes the sweep PARTIAL, and the next reader who
meets a real offender in an exempt file can widen the exemption instead of fixing the
offender. The repair instead changes the PREMISE TEST to pass its keywords as a `**{...}`
SPLAT. The sweep's subject is a LITERAL keyword argument in source — that is the defect
class, because a reader sees `type=` and believes it lands — and a splat carries no
`keyword.arg` at all, which is why the existing sweep already skips one. So the premise still
demonstrates the real runtime drop and the sweep stays total. The repair also ADDS a test
asserting that this file is itself among the files the sweep reads, so the exemption cannot
arrive later by accident.

THE PAIR, measured mechanically before emission against the committed blob at `123a0c3f`.
  `TO contains FROM: False` — so PAIR45 is a REWRITE, and the FROM-zero count applies.
  FROM  358 bytes, 7 lines, sha256 `63606f1390a4f857a9e5e8f3a97f03bf2c3cf175e0b56d119a6d7387ba5be94e`
  TO   1437 bytes, 26 lines, sha256 `0af6c552bc7894f8c70ee1c0105bf433cc3f2fb65433dca22c92873fa5e9d6ac`
  FROM occurs exactly 1x in the committed file and must read 0x after the rewrite; TO must
  read exactly 1x after it. The file goes from 4419 bytes and 115 lines to 5498 bytes and
  134 lines, at sha256
  `e0b29143eb63dba5723570a02cf694c40a242fe8dbad13d1351621db18ed0016`.

Constraints:
  1. EVERY SLICE IS APPLIED BYTE FOR BYTE. Extract each one MECHANICALLY by its
     `BEGIN-`/`END-` marker lines from the COMMITTED `.agent/authored/f275-r45.md`, read
     with `git cat-file blob`, and apply it by file write or byte concatenation in Python.
     Never retype a slice, never reflow one, and never edit one even where you believe it
     wrong — declare it instead. A marker line is never part of a slice's content.
  2. AN EOF-APPEND IS PURE CONCATENATION. Each append slice's content already begins with
     the blank line that separates it from what precedes it, so the operation is exactly
     `old_bytes + slice_bytes` with nothing inserted between them. Both targets named in C2
     end with a newline at C1; do not add one.
  3. COUNT BYTES IN BYTES. Where you report a length, report `len(<bytes>)` and not
     `len(<str>)`: this file's docstrings hold an em dash, so the two differ by 6 here, and
     the round 44 pre-emission check reported 4413 for a file that is 4419 bytes for exactly
     that reason. The digests in this block are over BYTES.
  4. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4 and nothing is reordered, merged or
     added. C1 precedes C2 because the plan must be current before the round touches the
     finding ledger (planner_reviewer_prompt.md §3 item 23).
  5. THIS ROUND MINTS NO ID AND RESOLVES NONE. The open set is 87 by distinct id at this
     base and 87 at C3; the next free id is R-0876 and it stays free. `R-0875` keeps its
     `Landed:` line and gains NO `Done:` paragraph — the reviewer authors that at the next
     gate, once this round's own gates have shown the repair works, which is the scheduling
     §3 item 31 requires.
  6. THE CHANGE SET IS EXACTLY THE SEVEN PATHS the Change list names. No path under
     `packages/`, `apps/`, `docs/` or `scripts/` moves, and no test file other than the
     guard is touched.
  7. NEVER `cd` INTO A WORKTREE, for any purpose. Address a worktree's files by ABSOLUTE
     path, run commands there with `subprocess.run([...], cwd=<abs worktree>)`, run
     `git status --porcelain` in the PRIMARY checkout in the same command sequence as any
     mutation, and revert with a sha256 re-read. Remove and prune before the handback.
  8. RUN `python3 -m pytest`, never bare `pytest`. The `remedy` console script is
     sandbox-blocked; if a CLI reading is needed use `python3 -m apps.cli.grouped`.
  9. THIS BLOCK IS CAPPED AT 490 LINES TOTAL AND 400 LINES OF PROSE, where PROSE is TOTAL
     minus the summed content lines of every slice and the marker lines count as prose
     (DECISION F085 D6 and D5). Measure BOTH from the committed blob, report both, and say
     plainly if either is exceeded. Do not fix an overage — declare it.
 10. READ `.agent/STOP` FROM DISK before the first commit and again before C3.

Done when: six gates. Run each as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and record the real
exit code and real numbers — one line per gate. Every reading is taken at a commit EARLIER
than C4.

  G1  TRANSPORT, at C0b. `.agent/authored/f275-r45.md` and `.agent/last_block.md` have the
      SAME sha256 and byte count, and the mirror was written from
      `git cat-file blob <C0a>:.agent/authored/f275-r45.md`. Report both digests. This covers
      the two committed artefacts and claims nothing about the bytes emitted into your prompt
      (planner_reviewer_prompt.md §3 item 37).
  G2  THE PLAN, at C1. `.agent/plan.md` is BYTE-EQUAL to PLAN45 as extracted; report bytes,
      sha256, line count against the AGENTS.md cap of 50, and `^## Goal$` and
      `^## Next Steps$` each exactly 1.
  G3  THE RECORD, at C2, for both appends, against COMMITTED blobs only — pre at C1, post at
      C2, read with `git show <rev>:<path>`.
      (a) Reader A: the post blob EQUALS the pre blob followed by the slice. Report pre,
          slice and post bytes and whether the reconstruction is identical.
      (b) Reader B: count N as the blank-line-separated paragraphs IN THE SLICE — count it,
          do not take a number from this block — and compare the LAST N paragraphs of the
          post blob against the slice's N IN ORDER, WITH LEADING AND TRAILING WHITESPACE
          STRIPPED, for the reason constraint 2 creates and round 42 measured.
      (c) One negative control per append: flip ONE byte inside the FIRST appended paragraph
          and confirm BOTH readers REJECT it. Report four outcomes per append.
      (d) `^Gate: F275 R44 ` reads 0 at C1 and exactly 1 at C2. `^Done: R-0875 ` reads 0 at
          C2 — this round resolves nothing. `^Landed: R-0875 ` reads exactly 1 at C2, the
          line round 44 wrote, unchanged.
  G4  THE OPEN SET, at C3. By DISTINCT ID: distinct `^- R-\d+ — ` minus distinct
      `^Done: R-\d+ — `, read from `git show <rev>:.agent/live_review.md` into memory and
      never by writing over the tracked file. Report at the base `123a0c3f` and at C3, plus
      the ids registered and resolved this round. Expect 87 and 87, both lists empty.
  G5  THE REPAIR IS THE AUTHORED BYTES AND IT IS GREEN, at C3.
      (a) The pair: report FROM's count in the committed BASE blob (it must read 1) and in
          the committed C3 blob (it must read 0), and TO's count in the C3 blob (exactly 1).
          Report the C3 blob's byte count, line count and sha256 and compare all three
          against the figures this block states.
      (b) `python3 -m pytest tests/test_model_construction_keywords.py -q` and report the
          figure. The reviewer read `6 passed` at exit 0 in a worktree with this repair
          applied, against `1 failed, 4 passed` at exit 1 without it.
      (c) `python3 -m pytest tests/cli/test_golden_path.py -q` — the canary.
      (d) `python3 -m ruff check tests/test_model_construction_keywords.py`.
      (e) The sweep's own reach, through the SHIPPED function rather than by grep: in one
          `python3 -c`, import the guard module, call `_undeclared_keyword_sites()` and print
          its length, and print whether this file's own repository-relative path is in
          `_tracked_python_files()`. The first must be 0 and the second True.
  G6  THE REPAIR STILL BITES, AND SO DOES THE EXEMPTION GUARD — TWO RED PROOFS, at C3, in a
      DISPOSABLE worktree detached at C3 under constraint 7, `__pycache__` purged before
      every run, every run under `python3 -B`, the selection scoped to
      `tests/test_model_construction_keywords.py`. Print the imported module's file path
      before believing any result. Run the UNMUTATED control FIRST, then each mutation, then
      the control again after every revert. For each mutation report the anchor's count
      before it is applied (it must read 1), the real exit code, and WHICH NODE IDS FAILED,
      read from the `FAILED ` lines where the node id is the token after the FIRST space and
      never inferred from the exit code. DO NOT REPORT A PREDICTED COUNT.
        M1  put ONE deleted keyword back: `type="write_readme"` into the `Task(...)` call in
            `tests/ui_server/test_command_channel.py`. This proves the sweep still catches a
            real offender after the repair.
        M2  introduce the EXEMPTION the repair rejected: make `_tracked_python_files()` drop
            this file's own path from what it returns. This proves the new self-coverage test
            catches the hole, and it must turn a DIFFERENT node id red from M1 — report both
            ids so the two are visibly distinct.
      Report each revert's sha256 against the pristine digest, and state that the file equals
      its pristine digest after the last revert.
  G7  NOTHING ELSE MOVED, at C3. `.agent/STOP` read FROM DISK is ABSENT.
      `git status --porcelain` is EMPTY. `git worktree list` reads exactly ONE entry.
      `git diff --name-only 123a0c3f..<C3>` is an EXACT SET MATCH against the Change list
      minus `.agent/handoff.md`: report the MISSING and EXTRA sets, both of which must be
      empty. Report ZERO paths under `packages/`, `apps/`, `docs/` or `scripts/`. Report each
      commit's INSERTION count for C0a, C0b, C1, C2 and C3 against the AGENTS.md DECISION
      F104 D1 cap of 500; C4's own numbers are not ordered here, because its text cannot
      count itself.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md with its mandated
sections — the state block carrying the SESSION NUMBER, the range, a per-commit
changed-files table with a reason per path, external actions, one line per gate with its REAL
exit code and real numbers, the item-status table, the open-findings count, and your
deviations. This is SESSION 18 of F275 and round 45; F275 stands at 45 rounds against the
operator's soft limit of 60 rounds and 20 sessions (amend0908-f275-finish rule 1), so no
scope report is owed. Add the one sentence of context self-assessment amend0905-throughput
requires. State the measured TOTAL and PROSE counts constraint 9 orders. Then push the
branch. Create no pull request, merge nothing, force-push nothing, rewrite no history.

--- BEGIN SLICE PLAN45 ---
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 45 repairs a RED BRANCH TIP the reviewer caused. The guard round 44 landed for R-0875
sweeps every tracked `*.py` file for a keyword its model does not declare, and its own
premise test wrote one literally, so once tracked the guard reported itself — §3 item 2, a
zero-gate counting a string the same block writes into the file the gate reads. The premise
now passes its keywords as a `**{...}` splat, which the sweep skips for the right reason, and
a new test pins that this file is itself swept so no per-file exemption can arrive later.
The round 44 FAIL verdict is booked here. No id is minted and none resolved.

## Next Steps

1. Author `Done: R-0875` at the next gate, once round 45's own gates have shown the repair
   works — the scheduling §3 item 31 requires, and the reason the `Landed:` line still
   stands.
2. THE FLIP. Its target API exists (round 42), its record shapes are measured (round 43), its
   construction mapping is ruled (DECISION F275 D25) and its tree is clean (round 44). The
   dry run measured it at 284 files and 4856 insertions, declared before review as the one
   oversize commit AGENTS.md permits per feature. It also registers
   `Task.acceptance_checks`'s structured form as a finding naming the feature that owns
   acceptance criteria, per amend0908-f275-finish rule 4.
3. The resolver collapse DECISION F260 D5 places in T003, with the classic store, which is
   the same commit range by that decision's own terms. Then the closure sequence: the
   integration gate, the evidence job, a fresh review zip, the ledger rotation, the STATUS
   line and the PR.

## Risks

- A guard added in the same commit as the cleanup it guards must be red-proved as a TRACKED
  file. Round 44's was proved untracked, where `git ls-files` cannot see it, and that is the
  whole of this round's cause.
- The open set is 87 by distinct id at this round's base `123a0c3f`. Four are High — R-0803,
  R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
--- END SLICE PLAN45 ---

--- BEGIN SLICE RECORD45 ---

Gate: F275 R44 — the F275 round 44 entry. VERDICT FAIL, and the fault is the REVIEWER'S, not the round's. Written by the planner and reviewer of session 18 after reading the committed range `c0e9dd10`..`be83dc4c` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs. THE DEFECT: the guard the block ordered as slice GUARD44, `tests/test_model_construction_keywords.py`, sweeps every TRACKED `*.py` file for a keyword its model does not declare, and its own premise test wrote `Task(description="d", type="write_readme")` literally — so once the file is tracked the guard reports ITSELF, and the reviewer confirmed at the tip that the single offender is that file's own line 113, at `1 failed, 4 passed` and exit 1. That is planner_reviewer_prompt.md §3 item 2 exactly: a zero-gate counting a string the same block writes into the file the gate reads. The reviewer's own red proof could not have caught it, and the reason is the lesson: the guard was written into the dry-run worktree as an UNTRACKED file, and `git ls-files` does not list untracked files, so the sweep never read itself. A round PASS requires the scoped commands green, so this round cannot have one; the repair is round 45 and the round 44 WORK IS KEPT, because the cleanup itself is correct. THE WORKER DID NOTHING WRONG AND SEVERAL THINGS WELL. Constraint 1 forbade editing a slice even where it looked wrong, so it applied the defective bytes verbatim at sha256 `03b5a334…` and DECLARED the consequence as its first line rather than burying it. It measured both states — the same file untracked over a cleaned tree reads `5 passed` at exit 0 and tracked reads `1 failed, 4 passed` at exit 1 — which is the measurement that identifies the cause. It declared the ordered colour proof VOID rather than reporting it as a pass, on the correct ground that a control which is already red discriminates nothing, and then took a reading the block never ordered, over the same node set in the same function: the offender LIST grows 1 to 2 and back to 1 under the mutation, which proves the sweep does reach the mutated line even though no colour could show it. THE REST OF THE ROUND IS CORRECT AND THE REVIEWER RE-DERIVED ALL OF IT. G1 is again the PRIMARY cmp-against-scratchpad proof and not the §4.9 digest fallback: the reviewer's scratch original survived, was hashed BEFORE delegation at `d919cf772594bffc2185692ac234a0e6f3240f1506eab43122d7e79ad2ebb50b`, and is byte-identical to both committed copies at 32143 bytes as ONE shared blob. G2: `.agent/plan.md` byte-identical to PLAN44 at 2863 bytes, 47 lines against the cap of 50. G3 over FOUR appends chained across two commits, every reader A identical on the reviewer's own reconstruction: `.agent/live_review.md` 867326 to 874062 at C2 and 874062 to 874338 at C3, `.agent/decisions.md` 1067057 to 1070820. G4: the open set rises from 86 to 87 BY DISTINCT ID, over 104 registrations against 17 resolutions, with `R-0875` registered, a `Landed:` line written and no `Done:` paragraph — which is exactly what an unreviewed fix should look like. G5: THE CLEANUP IS RIGHT AND THE REVIEWER'S FIGURE REPRODUCES EXACTLY — 35 keywords deleted and 5 repointed onto `user_prompt`, zero remaining in the 24 cleaned files, zero production files touched, and the 24 files read `1083 passed, 10 skipped` at exit 0 when the reviewer ran them itself, the same figure the block stated. The `ruff` claim is SUSTAINED on the reviewer's own measurement: the two `I001` findings are at `tests/orchestration/test_checkpoints.py:414` and `tests/ui_contracts/test_graph_architecture.py:6`, and reading the BASE bytes through `ruff check --stdin-filename` — so nothing was written into the primary checkout, per §3 item 29 — shows both present at the base, so the round added no lint debt and the new guard file is itself clean. G7: 30 paths, every one the Change list allows, ZERO under `packages/`, `apps/`, `docs/` or `scripts/`, porcelain EMPTY, ONE worktree, and insertions 386, 306, 21, 16 and 137, so F275's one declared-oversize allowance is still unspent at 45 rounds. THE TEN DEVIATIONS ARE ALL SUSTAINED. Two are worth naming beyond the first: the worker measured the `ruff` findings' pre-existence in an extra disposable worktree rather than arguing it, and it left two now-unused local names in place because S1 said to leave the rest untouched, which is the correct reading of a narrow order even where a wider one would have been tidier. NO FINDING IS REGISTERED BY THIS GATE AND NONE IS RESOLVED; R-0875's resolution waits for round 45's gates, per §3 item 31.
--- END SLICE RECORD45 ---

--- BEGIN SLICE SLIPS45 ---

2026-09-10 · F275 R45 · TWO REVIEWER SLIPS FROM THE ROUND 44 BLOCK, both mine and neither an id beyond R-0875's own repair. FIRST, the GUARD44 slice violated §3 item 2 — the guard's zero-assertion counts a string the same slice writes into the file the guard reads — and the red proof that should have caught it could not, because the guard was written into the dry-run worktree UNTRACKED and `git ls-files` does not list untracked files, so the sweep never read itself. THE RULE THAT FOLLOWS: a guard whose subject is the tracked file set is red-proved only after `git add`, and the control must be taken in that state. SECOND, that block's pre-emission check reported the GUARD44 slice as "4413 bytes" where the committed file is 4419: the check measured `len()` over a `str` while the file's docstring holds an em dash, and the digests agreed only because they were taken over `.encode()`. Both are caught here, and the irony is recorded rather than smoothed over — DECISION F275 D25, written in that same round, rules that `ast` columns are BYTE offsets and that a character-based reading of them is the defect.
--- END SLICE SLIPS45 ---

--- BEGIN SLICE PAIR45_FROM ---
    def test_an_undeclared_keyword_really_is_dropped_rather_than_rejected(self) -> None:
        """The premise, pinned: this is why the defect is invisible at runtime."""
        from packages.core.models import Task

        task = Task(description="d", type="write_readme")
        assert not hasattr(task, "type")
        assert task.model_extra is None
--- END SLICE PAIR45_FROM ---

--- BEGIN SLICE PAIR45_TO ---
    def test_an_undeclared_keyword_really_is_dropped_rather_than_rejected(self) -> None:
        """The premise, pinned: this is why the defect is invisible at runtime.

        The keywords are passed as a SPLAT, not written literally, and that is
        load-bearing rather than stylistic: the sweep above reads every tracked file
        including this one, so a literal ``type=`` here would make the guard report
        itself — which is exactly what it did when this file first landed. A splat
        carries no ``keyword.arg``, so the sweep skips it for the same reason it should:
        its subject is the literal keyword a reader sees and believes, and a splat is a
        different thing. The runtime behaviour demonstrated is identical.
        """
        from packages.core.models import Task

        task = Task(**{"description": "d", "type": "write_readme"})
        assert not hasattr(task, "type")
        assert task.model_extra is None

    def test_the_sweep_reads_this_file_too(self) -> None:
        """No file is exempt from the sweep, including this one.

        Pinned because the obvious repair for the self-report above would have been a
        per-file exemption, and an exemption is a hole a later reader can widen instead of
        fixing the offender it hides.
        """
        own_path = str(Path(__file__).resolve().relative_to(REPO_ROOT))
        assert own_path in _tracked_python_files()
--- END SLICE PAIR45_TO ---
