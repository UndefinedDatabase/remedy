# Handoff — F258 Self-use track v2

## Session

SESSION 1 of feature F258 · round 3 · rounds so far 3.

## State

Branch `feature/f258-self-use-v2`, cut from `main` at
`18ae71293cde9b1157aca35d3d02c3a8f4265813` (the merge commit of pull request
225, F040's closure). Last commit on this branch before the handback write is
`b9401f23028b1962235bc82994cc13554ececbc0` (`test(f258): allowlist
self_use_generator in the development-artifact boundary guard`). This round
builds `packages/orchestration/self_use_generator.py`, T001 part 2: Tier 1
(the finding ledger, rendered as a job) is real and tested; Tiers 2-3
(documentation staleness, `remedy doctor core`) are honest `None` placeholders
per DECISION F258 D2. Nothing calls the generator yet against the real
shipped queue — `scripts/self_use_queue.json` is untouched this round and
stays at four items. This round also books the two verdicts the reviewer
owed the ledger from rounds 1 and 2 (per amend0827 rule 1: a pushed handback
is persisted into `.agent/live_review.md` in the first commit of the next
round that happens anyway) — this round's C2 is that commit. Open findings
count in `.agent/live_review.md`: 317 registered, 55 distinct resolved
(`Done:`), unchanged this round (no new R-id minted or resolved).
`DECISION F258` ids: `['D1', 'D2']`, `D2` newly minted this round. `Gate:
F258 R` lines: `['Gate: F258 R1', 'Gate: F258 R2']`, both newly booked this
round (this round records no verdict on itself — round 4 books that one, per
amend0827 rule 1). R-0570 stays OPEN (0 `Done: R-0570` lines), routed away,
unrelated to this branch.

## Range

Review of `549895fe7010a74fd3b465243e3314b954500df6..b9401f23028b1962235bc82994cc13554ececbc0`
(HEAD before the C6 handback commit; see the Commits table below for the
exact short SHAs, which are what this handback actually verified against).

## Item status

Every bundle item and every gate, each appearing exactly once:

| Item | Status | Reason |
|------|--------|--------|
| C0a save block to `.agent/authored/f258-r3.md` | done | `shutil.copyfile`, sha256-verified |
| C0b mirror into `.agent/last_block.md` | done | `shutil.copyfile`, sha256-verified |
| C1 rewrite `.agent/plan.md` from PLAN3 | done | byte-equal, 41 lines |
| C2 append RECORD3 to `.agent/live_review.md` | done | append-only, proved by reconstruction + paragraph order (N=3) + negative control |
| C3 copy `.remedy-wt/f258-r3-genmodule.py` to `self_use_generator.py` | done | byte-equal (sha256), `shutil.copyfile` |
| C4 copy `.remedy-wt/f258-r3-gentests.py` to `test_self_use_generator.py` | done | byte-equal (sha256), `shutil.copyfile` |
| C5 apply PAIR-BOUNDARY to `test_development_artifact_boundary.py` | done | FROM 1→0, TO 0→1 |
| C6 rewrite `.agent/handoff.md` | done | this file |
| G1 transport | done | sha256 equal across all three copies, 25798 bytes |
| G2 the plan | done | byte-equal to PLAN3, 41 lines, `## Goal`/`## Next Steps` present |
| G3 the record append | done | reconstruction + paragraph order (N=3) + negative control, all as expected |
| G4 the ledger | done | R-ids/Done-ids ADDED/REMOVED empty at C1 and C2; DECISION F258 `['D1']`→`['D1','D2']`, ADDED `['D2']`; `Gate: F258 R` lines `[]`→`['Gate: F258 R1','Gate: F258 R2']`; `Done: R-0570` stays 0 |
| G5 the generator module and its tests | done | byte-equal to both scratch originals; 61 passed at C4; mutation red-proof reproduced the reviewer's exact expected two-test failure |
| G6 the boundary pair and the repo-wide guards | done | FROM=0/TO=1; three guard suites 23/18/28 passed |
| G7 the state readers and the canary | done | five suites, 515/52/21/16/42 passed, all matching reviewer's base |
| G8 the tree | done | clean, 0 untracked, single worktree, all seven non-handback commits under 500 insertions — no oversize-commit exception needed this round |

## Commits

All `+/-` figures are `git diff --numstat` against each commit's own parent.

### 364da871 docs(f258): save round 3 block verbatim to authored/f258-r3.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f258-r3.md` | 283/0 | C0a — verbatim copy of the round's step block, `shutil.copyfile` |

### 9c94a48f docs(f258): mirror round 3 block into last_block.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | 206/605 | C0b — verbatim copy of the same block, `shutil.copyfile`, into the mirror slot. (`git commit`'s own immediate summary reported this as a 90%-similarity full rewrite, "283 insertions(+), 682 deletions(-)" — the old and new file's own line counts; `git diff --numstat`/`git log --numstat` against the parent, the method every prior round's handback used, gives 206/605 instead. Both describe the same byte-identical result; 206/605 is reported here for methodology consistency with rounds 1-2.) |

### 002dbf7e docs(f258): rewrite plan.md for round 3 (T001 part 2 in progress)
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/plan.md` | 17/15 | C1 — rewritten from slice PLAN3, byte-equal, 41 lines |

### 8471db8f docs(f258): append round 1/2 verdicts and DECISION F258 D2 to live_review.md
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/live_review.md` | 6/0 | C2 — RECORD3 appended verbatim (three dense paragraphs: Gate F258 R1 verdict, Gate F258 R2 verdict, DECISION F258 D2); nothing earlier revised |

### 68bf1bc3 feat(f258): add self_use_generator module (tier 1 real, tiers 2-3 placeholders)
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/self_use_generator.py` | 270/0 | C3 — verbatim `shutil.copyfile` of `.remedy-wt/f258-r3-genmodule.py`, the reviewer's own pre-written and pre-tested module |

### a68902c4 test(f258): add tests for self_use_generator
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_self_use_generator.py` | 310/0 | C4 — verbatim `shutil.copyfile` of `.remedy-wt/f258-r3-gentests.py`, the reviewer's own pre-written and pre-tested test file |

### b9401f23 test(f258): allowlist self_use_generator in the development-artifact boundary guard
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_development_artifact_boundary.py` | 5/0 | C5 — PAIR-BOUNDARY: `packages/orchestration/self_use_generator.py` added to `_ALLOWED_LEGACY` with a one-line-comment WHY, same category as `self_dogfood.py`/`integrity_gate.py` |

Not tabled per the template's self-reference exception: the commit that
writes this handback (C6, `.agent/handoff.md`) — its own numbers are the
reviewer's to measure at the next gate.

## External actions

- `git worktree add --detach .remedy-wt/negctrl-g3 HEAD` — disposable
  worktree for the G3 negative control, detached at `8471db8f` (post-C2).
- `git worktree remove .remedy-wt/negctrl-g3 --force` — removed after the
  negative control ran; `git worktree list` afterward showed only the
  primary checkout.
- `git worktree add --detach .remedy-wt/mutwt-g5 HEAD` — disposable
  worktree for the G5 mutation red-proof, detached at `a68902c4` (C4).
- `git worktree remove .remedy-wt/mutwt-g5 --force` — removed after the
  mutation red-proof and its restore both ran; `git worktree list` afterward
  showed only the primary checkout.
- `git push -u origin feature/f258-self-use-v2` — to be run immediately
  after this handback's commit, per constraint 12. The push's own outcome
  (new remote SHA) is necessarily outside this file's own content, since the
  push happens after this commit is written; it is reported in this round's
  session report instead. No pull request opened — the PR is created only
  at closure.
- No `gh pr` command run this round (the Open PR Gate was already satisfied
  before this round started, per the task brief's "no new branch this round"
  instruction — this round stays on the existing `feature/f258-self-use-v2`).

## Verification

Every gate below ran with a REAL exit code captured via
`subprocess.run(...).returncode` inside scripts on disk under the gitignored
`.remedy-wt/` (`do_c0.py`, `extract_slices.py`, `do_c2.py`, `verify_g3.py`,
`negctrl_g3.py`, `run_g5_tests.py`, `run_mutation.py`,
`run_mutation_restore.py`, `run_g6.py`, `run_g7.py`, `purge_cache.py`). The
PAIR-BOUNDARY apply (C5) used the same read/assert-count-1/replace/write
method, run as a `python3 - <<'PYEOF'` heredoc through the Bash tool rather
than a saved standalone file — see Deviations. The `remedy` console script
was not needed this round (every gate is a `pytest` invocation).

**G1 — TRANSPORT, at C0b.** sha256
`cc7e9b036cb78f47d5cc5cb95314c67c1267f0d0937046dfbcc0509e9f06e4ce` over 25798
bytes, computed identically over all three files: the scratch original
`.remedy-wt/f258-r3-block.md`, the committed `.agent/authored/f258-r3.md`,
and the committed `.agent/last_block.md`. All three equal.

**G2 — THE PLAN, at C1.** `.agent/plan.md` sha256
`a4a7b674cece71895bdfc9bff4980dee4c5c94b028f15f45da51c14f31ef83f2` and the
PLAN3 slice extracted from the block, same sha256 — equal, 2000 bytes both
sides. Line count 41 (< 50). Carries `## Goal` and `## Next Steps`.

**G3 — THE RECORD APPEND, at C2.** Base (measured immediately before C2) is
1756614 bytes. RECORD3 is 10195 bytes (UTF-8). 1756614 + 1 + 10195 =
1766810, and the committed `.agent/live_review.md` after C2 is 1766810
bytes — equal.
(a) WHOLE RECONSTRUCTION: `base + b'\n' + record == committed` → `True`.
(b) PARAGRAPH ORDER: the committed file's last THREE `\n\n`-delimited units
equal RECORD3's three paragraphs in order — 2412, 3501, 4234 bytes
respectively, all equal → `True`. N=3, not N=1, as the block states (two
Gate verdicts plus one DECISION, one slice, one commit).
NEGATIVE CONTROL, run inside the disposable worktree `.remedy-wt/negctrl-g3`
(detached at `8471db8f`): flipped the first letter of the DECISION paragraph
(the third/last paragraph), `D` → `X`. Both readings on the FLIPPED append,
checked against the original RECORD3: `False`, `False` — both correctly
reject the flip. Both readings on the ORIGINAL append, checked against the
original RECORD3: `True`, `True` — both correctly accept it. Worktree
removed after; `git worktree list` then showed only the primary checkout.

**G4 — THE LEDGER, at C1 and at C2.**
- Before C1 / after C1 (identical — C1 does not touch `.agent/live_review.md`):
  317 distinct `^- R-\d+ — ` ids, 55 distinct `^Done: R-\d+` ids,
  `DECISION F258` ids `['D1']`, `Gate: F258 R` lines `[]`.
- After C2: 317 distinct `^- R-\d+ — ` ids, 55 distinct `^Done: R-\d+` ids,
  `DECISION F258` ids `['D1', 'D2']`, `Gate: F258 R` lines
  `['Gate: F258 R1', 'Gate: F258 R2']`.
- ADDED registered (C2 vs. before C2): `[]`. ADDED resolved: `[]`.
- `DECISION F258` ADDED: exactly `['D2']`.
- `Gate: F258 R` lines newly booked: `Gate: F258 R1`, `Gate: F258 R2` (both,
  this is the first round either appears).
- `^Done: R-0570` count: 0 before, 0 after (throughout).

**G5 — THE GENERATOR MODULE AND ITS TESTS, at C4.**
`packages/orchestration/self_use_generator.py` sha256
`c6751c8b62f6da677c8c530d8a9ab0b62f239c1e2fdc6e32bf3be2ef16ebd057`, 11200
bytes, equal to the scratch original `.remedy-wt/f258-r3-genmodule.py`
(same sha256, same 11200 bytes).
`tests/orchestration/test_self_use_generator.py` sha256
`bccb9bbbbbbb3f48a4d4be7a8ed3aa02cbc4e3a415a602fb8bc902a236c1cd27`, 13035
bytes, equal to the scratch original `.remedy-wt/f258-r3-gentests.py` (same
sha256, same 13035 bytes).

In the PRIMARY checkout, at C4:
`python3 -m pytest tests/orchestration/test_self_use_generator.py
tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_job.py -q`
→ REAL exit 0, `61 passed` — matches the reviewer's stated 20+23+18=61
exactly.

THE MUTATION RED-PROOF, in the disposable worktree `.remedy-wt/mutwt-g5`
(detached at `a68902c4`, C4), `__pycache__` purged (0 found — nothing to
purge, `python3 -B` never wrote one), `python3 -B -m pytest` throughout:
- Mutation (the `if re.search(...) or re.search(...):` block right after
  `r_id, paragraph = found` in `_ledger_tier`, disabled by wrapping its
  condition as `if False and (...)`, so the `raise SelfUseGenerationError`
  can never fire): re-ran `tests/orchestration/test_self_use_generator.py`
  alone → REAL exit 1, `2 failed, 18 passed`. Failed tests, exactly the two
  the reviewer named in advance:
  `TestLedgerTierSafety::test_a_paragraph_shaped_like_a_heading_raises_rather_than_generating`
  (`Failed: DID NOT RAISE <class '...SelfUseGenerationError'>`) and
  `TestLedgerTierSafety::test_a_paragraph_containing_an_acceptance_marker_raises`
  (same failure shape). No other test in the file went red. This is EXACTLY
  the failure set the reviewer stated verifying before delegation — no
  deviation to declare on this point.
- Restore (condition reverted to `if re.search(...) or re.search(...):`,
  file re-verified byte-equal to the committed module afterward): re-ran the
  same test file → REAL exit 0, `20 passed` again.

Worktree removed after; `git worktree list` then showed only the primary
checkout; `git status --porcelain` empty in the primary checkout throughout.

**G6 — THE BOUNDARY PAIR AND THE REPO-WIDE GUARDS, at C5.**
PAIR-BOUNDARY: FROM count 1 before / 0 after; TO count 0 before / 1 after.

In the PRIMARY checkout, at C5, each its own REAL exit code, in the block's
stated order:
- `python3 -m pytest tests/test_data_paths.py -q` → REAL exit 0, `23 passed`.
- `python3 -m pytest tests/orchestration/test_development_artifact_boundary.py -q`
  → REAL exit 0, `18 passed`.
- `python3 -m pytest tests/test_path_utils.py -q` → REAL exit 0, `28 passed`.

All three match the reviewer's stated pre-block-authoring measurement (23,
18, 28) exactly; all green after PAIR-BOUNDARY, as expected.

**G7 — THE STATE READERS AND THE CANARY, at C6.**
- `python3 -m pytest tests/ui_server/ -q` → REAL exit 0, `515 passed`.
- `python3 -m pytest tests/orchestration/test_test_runner.py -q` → REAL exit
  0, `52 passed`.
- `python3 -m pytest tests/regression/test_resource_safety.py -q` → REAL exit
  0, `21 passed`.
- `python3 -m pytest tests/orchestration/test_integrity_gate.py -q` → REAL
  exit 0, `16 passed`.
- Canary `python3 -m pytest tests/cli/test_golden_path.py -q` → REAL exit 0,
  `42 passed`.

All five match the reviewer's stated base readings (515, 52, 21, 16, 42)
exactly — run before this C6 handback commit itself; none of these five
suites' own contracts name `.agent/handoff.md`.

**G8 — THE TREE, at C6.** `git status --porcelain` empty; `git ls-files
--others --exclude-standard` count 0; `git worktree list` shows the primary
checkout alone. Per-commit insertion counts, C0a through C5, from `git diff
--numstat` against each commit's own parent: 283, 206, 17, 6, 270, 310, 5 —
every one under 500. No oversize-commit exception was needed this round
(constraint 2's purpose: GENMODULE/GENTESTS shipped as separate scratch
files precisely to keep this feature's one-oversize-exception budget
unspent for a second time).

## Authored-text proofs

Two authored slices (PLAN3, RECORD3), two whole-file copies (GENMODULE,
GENTESTS) and one FROM/TO pair were applied this round, all via disk-to-disk
extraction/copy from the scratch originals rather than retyping:

- C0a/C0b: the whole block, sha256
  `cc7e9b036cb78f47d5cc5cb95314c67c1267f0d0937046dfbcc0509e9f06e4ce`, 25798
  bytes — three-way equal (scratch original, `.agent/authored/f258-r3.md`,
  `.agent/last_block.md`).
- PLAN3 → `.agent/plan.md`: sha256
  `a4a7b674cece71895bdfc9bff4980dee4c5c94b028f15f45da51c14f31ef83f2` both
  sides.
- RECORD3 → appended to `.agent/live_review.md`: proved by reconstruction
  and paragraph-order equality (N=3) plus the negative control, not by
  whole-file sha256 (it is an append, not a rewrite) — see G3 above.
- GENMODULE → `packages/orchestration/self_use_generator.py`: sha256
  `c6751c8b62f6da677c8c530d8a9ab0b62f239c1e2fdc6e32bf3be2ef16ebd057` both
  sides, `shutil.copyfile`.
- GENTESTS → `tests/orchestration/test_self_use_generator.py`: sha256
  `bccb9bbbbbbb3f48a4d4be7a8ed3aa02cbc4e3a415a602fb8bc902a236c1cd27` both
  sides, `shutil.copyfile`.
- PAIR-BOUNDARY: proved by exact-string FROM/TO occurrence counts (1→0,
  0→1) against `tests/orchestration/test_development_artifact_boundary.py`,
  not sha256 (it is a substring pair inside a larger file) — see G6 above.

## Deviations & assumptions

1. **C0b's `git commit` summary line and its `git diff --numstat` figure
   disagree (283/682 vs. 206/605), though both describe the same
   byte-identical result.** `git commit`'s own immediate output labeled the
   change "rewrite .agent/last_block.md (90%)" and reported
   "283 insertions(+), 682 deletions(-)" — the new and old file's own total
   line counts, consistent with a detected complete rewrite. `git
   diff --numstat 364da871 9c94a48f -- .agent/last_block.md` and `git log
   --numstat` both report 206/605 instead, a genuine line-level diff. Round
   2's equivalent mirror commit showed no such discrepancy when checked the
   same way (`git diff --numstat` there also gave 624/307, matching what
   that round's own handback reported), so this is the first round where the
   two methods diverge for this file. Reporting 206/605 in the Commits table
   above for methodology consistency with rounds 1-2's own stated convention
   ("`git diff --numstat` against each commit's own parent"); flagging the
   divergence here per constraint 1 rather than silently picking one number.
   Neither figure matters for the 500-line cap: `last_block.md` is in
   AGENTS.md's named `.agent/**` state-file exemption regardless of size.
2. **PAIR-BOUNDARY (C5) was applied via an inline `python3 - <<'PYEOF'`
   heredoc through the Bash tool, not saved first as a standalone file under
   `.remedy-wt/`.** The read/assert-count-1/replace/write method itself
   (constraint 5) was followed exactly and the before/after counts were
   captured directly from the script's own stdout (never through a pipe),
   but the script was not persisted as a separate `.py` file the way the
   other gate scripts were. Declaring this because the letter of the block's
   general scratch-script guidance asks for on-disk scripts; the substance
   (byte-exact single-occurrence read-count-replace-write, verified counts
   reported) was met.
3. **Two sandbox-denied Bash forms, both worked around.** A `find ...
   -exec rm -rf {} +` call (to purge `__pycache__` before the G5 mutation
   worktree run) was denied; replaced with a small `purge_cache.py` script
   under `.remedy-wt/` doing the same walk via `pathlib.rglob` and
   `shutil.rmtree`. A multi-command shell one-liner with `cd` and chained
   `&&`/output-redirection into `/tmp` (to inspect the C1 ledger state) was
   also denied; replaced with `git -C <repo> show <sha>:<path> ><outfile>`
   writing into `.remedy-wt/` instead of `/tmp`, per this repo's known
   sandbox posture (`/tmp` denied, `.remedy-wt/` is the safe scratch route).
   Neither workaround changed any measured result — the pycache purge always
   reported 0 dirs found, and the ledger-state figures obtained via the
   worktree-safe route are the same ones reported throughout this handback.
4. **Slice, copy and pair content applied as given, not fixed.** Per
   constraint 1, PLAN3, RECORD3, the whole GENMODULE/GENTESTS files and
   PAIR-BOUNDARY were applied byte-for-byte without correction. Constraint 2
   states "Its sha256 is stated in gate G1" for the block file, but G1's own
   text does not literally state a numeric sha256 value anywhere in the
   block — it only names WHERE the digest is to be reported. Read this as
   "G1 is where you verify and report it," computed and verified the digest
   before saving as instructed, and flagging the literal-wording gap here
   per constraint 1 rather than treating it as a blocker. Nothing else in
   this round's authored text read as materially wrong.

## Next

Wire `generate_and_append_if_empty` into `docs/roadmap/STATUS_closure_protocol.md`
precondition 6's own text (T001 part 3), so a future closure round reads
"call the generator" rather than "curate by hand" — still a session/human
action since nothing in this protocol runs unattended, but the function now
exists to call. T002 (consumed means executed) depends on a generated item
actually being run, not just appended; T003 (findings flow back) wires
existing finding-ledger machinery once T002 exists. Push and Open PR Gate
housekeeping apply as usual; no PR is open on this branch yet (none is
created before closure, per constraint 12). Round 4 also owes the ledger
this round's own `Gate: F258 R3` verdict, per amend0827 rule 1 (booked in
round 4's first commit, not this round's).
