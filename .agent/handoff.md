# Handback — F315 "The loop runs through the adapter," round 6 (closing round)

## Session

SESSION 1 of feature F315 · round 6 · rounds so far 6. Context self-assessment: this session
continued directly from round 5's handback, booked round 5's verdict and gave the feature file its
Built State, rotated the finding ledger, accepted F315 in STATUS with the README sync and SU-079's
`consumed_by`, ran the gates, and is about to push and open the pull request. The session ends here
because F315 is closed and the next feature starts in a fresh session.

**Fortschritt:** 100 % (F315 is accepted; its pull request waits for the next session's Open PR
Gate) — Schätzung.

## Range

Review of `66661cef1`..HEAD.

## Commits

### 1004b79a8 F315 R6 C1: book round 5, the Built State, save the round 6 block and the PR body
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f315-r6.md` | +141/-0 | NEW FILE; byte copy of this round's block, `block.md` |
| `.agent/authored/f315-r6-pr_body.md` | +69/-0 | NEW FILE; byte copy of the reviewer-authored pull request body |
| `.agent/live_review.md` | +2/-0 | books round 5's verdict |
| `docs/roadmap/features/T8_F315.md` | +38/-0 | the feature file's Built State |
| `.agent/plan.md` | +5/-6 | rewritten for round 6, the closing round |

All five paths are byte copies of the reviewer's prepared `c1-*` files; gate 1's `verify.py`
confirms each equality (see Verification).

### e0e949e9a F315 R6 C2: rotate the finding ledger into its archive
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +0/-22 | `scripts/rotate_live_review.py` moved 11 gate records out, byte-verbatim |
| `.agent/live_review_archive.md` | +22/-0 | the same 11 gate records appended to the append-only archive |

Byte copies of the reviewer's prepared `c2-*` files; gate 1's `verify.py` confirms the equality;
the rotation's own run (not a copy) is reported under Verification §2 below.

### this commit — F315 R6 C3: accept F315 in STATUS with its README sync and the self-use queue
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | +1/-1 | F315's `[~]` line becomes `[x]` with the accepted-HEAD line, byte-identical to `status_line.txt` |
| `README.md` | +8/-2 | `161 of 315`, Tier 8 row `2 \| 13`, Tier 8 list gains F315's entry after F151's |
| `scripts/self_use_queue.json` | +1/-1 | SU-079's `consumed_by` becomes `F315` |
| `.agent/handoff.md` | n/a (self-reference; R-0149 pattern) | this handback, rewritten per `docs/agents/handback_template.md` |

All three C3 files are byte copies of the reviewer's prepared `c3-*` files; gate 1's `verify.py`
confirmed each equality against the working tree before this commit existed (printing `absent` for
"C3 committed", as the block states).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `1004b79a8`, five paths, byte-equal to prepared files, numstat exactly the manifest's |
| C2 | done | `e0e949e9a`, two paths, byte-equal to prepared files, rotation output matched `sim-rotation.txt` |
| C3 | done | this commit, three paths plus the handoff, byte-equal to prepared files |
| Push | done | see External actions |
| Pull request | done | see External actions |
| Gate 1 (`verify.py`) | done | every line `True`, `C3 committed` read `absent` before this commit, last line `ALL True` |
| Gate 2 (STATUS line) | done | `status_line.txt` content occurs exactly once in `docs/roadmap/STATUS.md`; no line begins `- [~]` |
| Gate 3 (pytest selection) | done | exit 0, `827 passed in 47.99s` (same passed count as `sim-gate3.txt`'s `827`, seconds differ as permitted), no FAILED/ERROR/SKIPPED line |
| Gate 4 (integrity) | done | `integrity exit 0`, `"fail_count": 0`, matching `sim-gate3.txt` |
| Gate 5 (open finding ids) | done | exactly the twelve required ids, in the required order |

## External actions

- `git push origin feature/f315-loop-through-adapter` — carrying `1004b79a8`, `e0e949e9a` and this
  handback's commit; see the reply for the push's own result.
- `gh pr create --repo UndefinedDatabase/remedy --base main --head feature/f315-loop-through-adapter --title "F315 — The loop runs through the adapter" --body-file .agent/authored/f315-r6-pr_body.md` —
  see the reply for the resulting PR number and URL.
- `gh pr list --repo UndefinedDatabase/remedy --state open --json number,headRefName,baseRefName,isDraft`
  — see the reply for the reading; expected exactly the one PR just opened, not a draft, into `main`.
- No merge performed or requested. No worktree created or removed by this session. One scratch
  directory was used, `.remedy-wt/f315-r6-worker/`, holding only Python helper scripts (digest
  checks, byte copies, the rotation wrapper, gate readings); `.remedy-wt/f315-r6/` (the reviewer's
  prepared tree) was only read, never written.

## Verification

Gate order per the block, run after C3's three files were in place and before this handoff.

1. `git status --porcelain` → only the three C3 files modified (`README.md`,
   `docs/roadmap/STATUS.md`, `scripts/self_use_queue.json`).
   `python3 .remedy-wt/f315-r6/prep/verify.py .` → every line `True`: both prior commits'
   single-parent checks, the new-subject check (`2 of 2`), the branch check, each commit's
   exact-path-set check and every per-path byte-equality check against the prepared `c1-*`/`c2-*`
   files, `C3 committed` → `absent` (as the block states, before this commit exists) followed by
   three `True` working-tree equality lines, final line `ALL True`.

2. Gate 2: `status_line.txt`'s content (without its trailing newline) occurs exactly once in
   `docs/roadmap/STATUS.md`, and no line of it begins `- [~]` — confirmed by direct count.

   The rotation (C2), run once with `scripts/rotate_live_review.py`, cwd the repository root:
   ```
   exit 0
   gate records moved: 11
   finding pairs moved: 0 (0 records)
   resolved-text records moved: 0
   old ledger size: 157212 bytes
   new ledger size: 140397 bytes
   old archive size: 7269917 bytes
   new archive size: 7286732 bytes
   open findings before: 12
   open findings after: 12
   gate headers matching neither known form (left in place): 1
   written: ~/Repos/remedy/.agent/live_review.md and
     ~/Repos/remedy/.agent/live_review_archive.md
   ```
   Exit code (`0`) equalled `sim-rotation.txt`'s first line; every output line but the `written:`
   line equalled `sim-rotation.txt`'s lines after its first line and before its `written:` line (the
   `written:` line differs only in naming the primary checkout instead of the reviewer's disposable
   dry worktree, which the block's wording anticipates). Both ledger files were then confirmed
   byte-equal to `c2-.agent__live_review.md` and `c2-.agent__live_review_archive.md`.

3. Gate 3: `python3 .remedy-wt/f315-r6/prep/gate3.py .`, run once:
   ```
   exit 0
   827 passed in 47.99s
   NOTICE R-1411: 3 entries of the configured data root ~/Repos/remedy/.data changed
     in the folders a supervisor this run did not start and its clients write; not counted
   integrity exit 0 6 pass; fail_count: 0
   ```
   Exit 0; passed count `827` equalled `sim-gate3.txt`'s second line's `827` (seconds differ, which
   the block permits); no FAILED, ERROR or SKIPPED line. The DECISION F151 D6 exception (exit 1 with
   a matching passed count and a NOTICE line) did not apply here — this run exited 0 cleanly; the
   NOTICE is gate3.py's unconditional data-root notice and named no failure.

4. Gate 4, read from the same gate-3 run above: `integrity exit 0`, `"fail_count": 0`, matching
   `sim-gate3.txt`.

5. Gate 5:
   `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   from the repository root →
   `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418', 'R-1421', 'R-1425', 'R-1426',
   'R-1427', 'R-1428', 'R-1442']` — exactly the required twelve, in the required order.

## Authored-text proofs

- `.agent/authored/f315-r6.md` against `.remedy-wt/f315-r6/prep/c1-.agent__authored__f315-r6.md`
  (= `block.md`): sha256 `f5417e9bfebe9c0f0f2a88f919530bb2d5943bfa4635e7e0d41d325cb9a9b3dc` on both.
  Byte-identical.
- `.agent/authored/f315-r6-pr_body.md` against
  `.remedy-wt/f315-r6/prep/c1-.agent__authored__f315-r6-pr_body.md`: sha256
  `07b4e03535f5c4dfb604d6728d64c5fffc48a099ed030fd34d9ab81fcf3065c1` on both. Byte-identical.
- `.agent/live_review.md` (C1 state) against `.remedy-wt/f315-r6/prep/c1-.agent__live_review.md`:
  sha256 `bfd9ee963a76595bbed9d1068126031e8b1df8243413b1cb7491ed64fea34c9a` on both. Byte-identical.
- `docs/roadmap/features/T8_F315.md` against
  `.remedy-wt/f315-r6/prep/c1-docs__roadmap__features__T8_F315.md`: sha256
  `c4b6e846caacc2f5ccdad7db52c10bdac0ca4bb09145327bc96170e8c0915313` on both. Byte-identical.
- `.agent/plan.md` against `.remedy-wt/f315-r6/prep/c1-.agent__plan.md`: sha256
  `a8ca2488a9e0433b66d2734ad33b2a6fbbe92b9833622cd982b5e919966219a4` on both. Byte-identical.
- `.agent/live_review.md` (C2 state) against `.remedy-wt/f315-r6/prep/c2-.agent__live_review.md`:
  sha256 `397c51a0652ed5648b7d8d2d8485629b6689fcbf65c6b664bdefaf9bdfbeb45d` on both. Byte-identical.
- `.agent/live_review_archive.md` against
  `.remedy-wt/f315-r6/prep/c2-.agent__live_review_archive.md`: sha256
  `f15b4a51fb365d0f20ef3dfbafbacad70e319bdf3e0c9f72244998328456d0bf` on both. Byte-identical.
- `docs/roadmap/STATUS.md` against `.remedy-wt/f315-r6/prep/c3-docs__roadmap__STATUS.md`: sha256
  `260e25c9c5af8d296dafda1931f070a977aa46d68a6c971165341f65799c92b1` on both. Byte-identical. The
  STATUS line itself is byte-identical to the prep folder's `status_line.txt` without its trailing
  newline (count 1), per gate 2 above.
- `README.md` against `.remedy-wt/f315-r6/prep/c3-README.md`: sha256
  `4c0687b37f24078f4bb7ef766ce27172f59b33116577fc05fbd03183f8dc42b1` on both. Byte-identical.
- `scripts/self_use_queue.json` against `.remedy-wt/f315-r6/prep/c3-scripts__self_use_queue.json`:
  sha256 `d1d667d5f1694d7f16a6c37c59e0a2f41a48607ddcd338ba84e707f8e7eef07b` on both. Byte-identical.

Before using any prepared file, `.remedy-wt/f315-r6/prep/digests.txt` was checked against its own
stated sha256 (`4471d9caa62cc799a5aa740511c0e64b1c3152e8d1aee8c62c99171c56771580`, matched), then
every one of its seven listed entries was recomputed and matched, then every one of
`manifest.tsv`'s ten listed prepared files was recomputed and matched, before any prepared file was
copied, run or read for C1, C2 or C3.

## Deviations & assumptions

None. C1, C2 and C3 landed in the block's order with no added, dropped or reordered commit; every
`c1-*`/`c2-*`/`c3-*` prepared byte was copied verbatim and proved equal by a direct byte comparison
before being staged, and every gate ran exactly once with no retry needed (gate 3 exited 0 on its
first and only run, so the DECISION F151 D6 one-more-run exception never triggered).

## For the operator, in plain sentences

The jobs Remedy runs now take every command they send to the Claude command line from that model's
adapter, the piece written last time so that other vendors' models can plug in the same way, and
read the usage of most calls through it too. The order of retries, timeouts and model switching
stays in Remedy's own loop, and the recorded stream of a call and the reason a call failed stay in
Remedy's own records. No existing test of the Claude command line had to change what it checks. The
paid run on itself went through the new path and stopped at its approval gate, because its reviewer
found the change it was asked for impossible, which is noted for the next clean-up feature. The
whole test collection passed on the code that ships and used a little less computer time than last
time. The review package is named
`remedy-review-20261023-225932-READY_FOR_REVIEW.zip`, in the folder
`~/Repos/remedy-history/zips`. A pull request is open and will be merged at the start
of the next session unless the operator merges it earlier.

## Next

1. Phase 1 rule 1: if `.agent/STOP` exists, the next session finishes whatever commit is in hand,
   writes the handoff, pushes, and stops, before anything else.
2. The Open PR Gate, which merges F315's pull request in the NEXT session and never in this one.
3. The booking of round 6's verdict in the next feature's first commit.
4. Rule A5: the next unchecked line in `docs/roadmap/STATUS.md`.

Operator questions open: 0. Open findings: 12 (R-1246, R-1281, R-1326, R-1351, R-1353, R-1418,
R-1421, R-1425, R-1426, R-1427, R-1428 and R-1442, owned by F314).
