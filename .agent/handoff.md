# Handback — F315 "The loop runs through the adapter," round 1

## Session

SESSION 1 of feature F315 · round 1 · rounds so far 1. Context self-assessment: this session
claimed the feature fresh off the merge of pull request 384 and only ran the inventory slice
(T001), so it carries no backlog from an earlier session of this feature.

**Fortschritt:** ~15 % (T001 inventory landed · T002 and T003 open) — Schätzung.

## Range

Review of `4747f2c67`..`831400281`.

## Commits

### c0d30f6d2 F315 R1 C1: claim F315, re-head the ledger, DECISION F315 D1, the slice list
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f315-r1.md` | +119/-0 | NEW FILE; byte copy of this round's block, `block.md` |
| `.agent/context.md` | +12/-15 | re-headed from the amend1023 context to F315's scope |
| `.agent/decisions.md` | +10/-0 | DECISION F315 D1: the seam is an inventory question, not an assumption |
| `.agent/live_review.md` | +19/-21 | re-headed from F151 to F315; Findings carried forward byte-identical |
| `.agent/plan.md` | +14/-9 | rewritten for F315's goal and current step |
| `docs/roadmap/STATUS.md` | +1/-1 | F315 `[ ]` to `[~]` |
| `docs/roadmap/features/T8_F315.md` | +14/-0 | the slice list (T001–T003) DECISION F315 D1 orders |

All seven paths are byte copies of the reviewer's prepared `c1-*` files; gate 1's `verify.py`
confirms each equality (see Verification).

### 831400281 F315 R1 C2: T001, the inventory of the claude-cli call path and its seams
| Path | +/- | Reason |
|---|---|---|
| `.agent/f315_inventory.md` | +365/-0 | NEW FILE; T001's committed findings pass, read at `4747f2c67`: what `ClaudeCliProvider` builds/maps/owns, the adapter's faces against it, every construction site, the candidate seams against the import guard, the goldens that must stay green, the structure-ledger rows it touches, and a proposal for DECISION F315 D2 |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 branch | done | `feature/f315-loop-through-adapter` from `main` at `4747f2c67` |
| C1 records commit | done | `c0d30f6d2`, seven paths, byte-equal to prepared files |
| C2 inventory commit | done | `831400281`, `.agent/f315_inventory.md`, 365 lines |
| Gate 1 | done | `verify.py` exit 0, every line `True`, `ALL True` |
| Gate 2 | done | selection + every `tests/test_*.py`, exit 0, `3767 passed, 2 skipped` |
| Gate 3 | done | `integrity check --json`, `fail_count` 0 |
| Gate 4 | done | open finding ids: `11` |
| C3 handback | done | this file |
| Push | done | see External actions |

## External actions

- `git push -u origin feature/f315-loop-through-adapter` — pushed after this handback's own
  commit, carrying `c0d30f6d2`, `831400281` and the handback commit; branch now tracks
  `origin/feature/f315-loop-through-adapter`.
- No pull request opened (the block orders none).
- No worktree created or removed; one scratch directory was used,
  `.remedy-wt/f315-r1-worker/`, holding only python helper scripts and gate output, never written
  under `.remedy-wt/f315-r1/` (the reviewer's prepared tree, left untouched).

## Verification

Gate order per the block: run once each, after C2 and before C3.

1. `git -C <repository root> status --porcelain` → empty.
   `python3 .remedy-wt/f315-r1/prep/verify.py .` → exit 0. Every line `True`, including:
   `C1 paths exactly [...]: [...]` (match), all seven `C1 <path> equals c1-<name>` lines `True`,
   `C2 .agent/f315_inventory.md holds no machine path` `True`, `C2 .agent/f315_inventory.md has
   365 lines, under 400` `True`, `C3` → `absent` (as the block states C3 prints before the
   handback commit exists), `the saved block equals block.md` `True`, final line `ALL True`.
2. `python3 .remedy-wt/f315-r1/prep/run_selection.py . .remedy-wt/f315-r1-worker/selection-output.txt`
   → exit 0. `paths 82`, `3767 passed, 2 skipped in 30.10s`. No `FAILED`, no `ERROR`, no
   `process(es) behind` anywhere in the output file. The two skips, reported as the block asks:
   `tests/test_agent_tooling.py:43` (D12 quarantine, pre-existing, unrelated to this round) and
   `tests/test_install_smoke.py:175` (opt-in, needs network).
3. `python3 -m apps.cli.main integrity check --json` → exit 0,
   `{"check_count": 6, ..., "fail_count": 0, "ok": true, "passed": true, ...}`, every one of the
   six named checks `"status": "pass"`.
4. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
   → exit 0, printed `11`, matching the block's required value.

## Authored-text proofs

`.agent/authored/f315-r1.md` (this round's committed copy of the block) against
`.remedy-wt/f315-r1/prep/block.md`: `wc -l` 119 on both; sha256
`f689bbb5643a30bbfced278e007d0257091a0f7b344edf0ecf72175198e7b748` on both. Byte-identical.

Before using any prepared file, `.remedy-wt/f315-r1/prep/digests.txt` was checked against its own
stated sha256 (`ad46b17b87abcfda9ab2f2e0a2a1d6456e65d94e95d58a5cd867bae970753c86`, matched), then
every one of its eleven listed entries was recomputed and matched (`ALL_OK`), before any prepared
file was copied or read for C1 or C2.

## Deviations & assumptions

- T001 is this round's own investigation, not a byte copy: the inventory file
  `.agent/f315_inventory.md` is original text the worker wrote from reading the code. To cover the
  large read (eleven source files, two test trees and the structure ledger) without crowding this
  session's own context, a read-only research pass was delegated to a forked copy of this same
  session to gather candidate facts with their `path:line` citations in parallel. Every load-bearing
  citation that pass returned was re-verified directly by this worker against the files on disk
  before the inventory was written and committed — several files were re-read in full
  (`claude_cli_reference.py`, `adapter_contract.py`, `role_provider_factory.py`, the import guard,
  the structure ledger) and one imprecise citation from the research pass (the exact function that
  calls `run_job` inside `remedy do`'s walk) was corrected to the verified line numbers before it
  reached the committed file. The synthesis, the wording, and the proposal in §7 are the worker's
  own, written after that verification, not transcribed from the research pass.
- `LAST_REVIEWED_SHA` in the Range line above is taken as `4747f2c67`, the merge commit this
  round's branch was cut from, since no round of F315 has been reviewed yet.
- No other deviation from the block's ordered commit sequence (C0, C1, C2, gates 1–4, C3, push);
  nothing was added, dropped or reordered.

## Next

1. Phase 1 rule 1: if `.agent/STOP` exists, the next session finishes whatever commit is in hand,
   writes the handoff, pushes, and stops, before anything else.
2. Phase 1 rule 2: the next session runs the Open PR Gate before opening any new branch.
3. Round 1's verdict gets booked into the next round's first commit, once a reviewer has read this
   handback.
4. T002: thread the builder and reviewer calls through the adapter, under DECISION F315 D2 (the
   seam this inventory's proposal names, to be settled as a decision before T002's code is
   written).

Operator questions open: 0. Open findings (gate 4): 11, all owned by a different, earlier feature,
none of them F315's.

For the person reading this and not the next worker: this round only investigated. It read how the
assistant "claude-cli" is called today and wrote down, in one new file, exactly which pieces of
code build its commands, which pieces read its answers, and which places in the program could let
a newer wrapper stand in for it without breaking anything that already works. No program behavior
changed. The next round will use that write-up to decide, in writing, exactly where that wrapper
is plugged in, before any of that plumbing is actually rewired.
