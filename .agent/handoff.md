# Handback — F086 R23

## Range

Review of `43e7f1e0..HEAD`.

## Commits

| Commit | Short SHA | Path | +/- | Reason |
|---|---|---|---|---|
| C0a | 67224395 | `.agent/authored/f086-r23.md` | +334/-0 | the R23 block saved byte-verbatim |
| C0b | 17e60f3a | `.agent/last_block.md` | +285/-287 | mirror of the committed C0a, read back from git |
| C1 | c24aa05e | `.agent/plan.md` | +14/-14 | whole file := PLAN23 |
| C2 | 181ade7e | `.agent/live_review.md` | +4/-0 | append: blank, RECORD21, blank, DONE0588 |
| C3 | f5d556f6 | `.agent/gate_f086_r23/**` | +243/-0 | 12 new `.txt` files, the integration gate's derived evidence |
| C4, C5 | this commit, then its successor | `.agent/handoff.md` | see round report | this handback, then VERDICT appended verbatim; a handoff cannot table the commit that writes it (R-0149) |

## External actions

`git worktree add -b tmp/base-gate-r23 .remedy-wt/base-r23 76661dc1` -> exit 0; then `git worktree remove --force`, `git branch -D tmp/base-gate-r23` ("Deleted branch tmp/base-gate-r23 (was 76661dc1)") and `git worktree prune`, after which `git worktree list` reads one line and `git branch --list 'tmp/*'` reads none. `gh pr list --state open --json number,headRefName,baseRefName,isDraft` -> `[]`. Nothing created, nothing merged. One push of this branch after C5.

## Verification

G1 HYGIENE: `.agent/STOP` absent, read from disk before C0a and again now; branch `feature/f086-release-capability`; `git status --porcelain` EMPTY at every commit and at the handback; `git worktree list` reads ONE line at the start of the round and ONE now, two only between the base worktree's add and its remove.
G2 TRANSPORT: `.remedy-wt/f086-r23.md`, the committed `.agent/authored/f086-r23.md` and the committed `.agent/last_block.md` are all three byte-EQUAL at sha256 886e7b86b10ac302f6f4299ead87433440399aea4a073cb90c52e42bf02fc52d, 25631 bytes, 334 lines.
G3 PLAN: `.agent/plan.md` at c24aa05e byte-equal to PLAN23 extracted from the committed C0a, sha256 63533396d445866a0aab7f30d44b79f7b6caae5d9d683f116a123e4b02b6de68, 44 lines (under the AGENTS.md 50), containing `## Goal`, `## Next Steps` and `F086`.
G4 LEDGER APPEND: the pre-C2 blob is a byte-exact PREFIX of the post-C2 blob; the remainder is byte-equal to a blank line, RECORD21, a blank line, DONE0588, at sha256 93d27a26788e3e7fd0aec74f7aff9dde171c2c4bc5de0369475be23d8f0c90a7 over 4 lines.
G5 LEDGER SETS: two independent extractions AGREE at each end — 171 registered / 3 resolved / 0 duplicates / 0 unregistered resolutions / 0 `Landed:` / 168 open at `43e7f1e0`, and 171 / 4 / 0 / 0 / 0 / 167 at C2; the registered SETS are equal, the resolved symmetric difference is exactly `['R-0588']`; CONTROL `f0b27118..7b84524c` reads `[]` registered while its resolved set gains exactly `R-0584`.
G6 ITEM-20 SCAN: over the lines C2 ADDS, backtick-quoted spans deleted first, `\bHEAD\b` reads 0; RED CONTROL, same two-step extractor over the lines `fd166295` adds to the same file, reads 3.
G7 ITEM-26 HEADERS: 19 at `43e7f1e0`, 20 at C2; the duplicate SET is UNCHANGED and is exactly `Gate: R19 — the R18 entry.`, which constraint 3 forbids repairing; `Gate: R23 — the R22 entry.` occurs 1x, is the LAST such header, and the text after it begins `R22 `.
G8 BRANCH RUN: `python3 -m pytest -n auto -q` in the PRIMARY checkout at 181ade7e — EXIT_CODE 0, WALL_SECONDS 149.0, summary `17192 passed, 20 skipped in 148.46s (0:02:28)`, FAILED_COUNT 0.
G9 BASE RUN AND PARITY: worktree on branch `tmp/base-gate-r23` at `76661dc1` (`git merge-base main HEAD`, identical to main and origin/main), `apps/ui/node_modules` and `apps/ui/dist` copied with `shutil.copytree`, `REMEDY_UI_NO_AUTO_BUILD=1` set through a copied `os.environ` — EXIT_CODE 1, WALL_SECONDS 135.3, summary `23 failed, 17110 passed, 19 skipped in 134.81s (0:02:14)`. All FOUR parity readings HELD: `apps/ui/dist` sha256 c14681f28e79a0c908642a03ceeda315b5d5150f079860fe20fcfbc9d3a26873 and `dist/index.html` mtime_ns 1787239643036148044, identical before and after the run in the base worktree AND in the primary checkout.
G10 COMPARISON AND ATTRIBUTION: `comm -13` reads 0 lines — EMPTY BY CONSTRUCTION, the branch set being empty, so no serial re-run exists to perform and constraint 10 finds no BLOCKER; `comm -23` reads 23 lines and EVERY ONE is attributed in `attribution.txt` by DEMONSTRATION rather than hypothesis — 7 to npm bin shims dereferenced by the copy, 16 to `apps/ui/dist` stale by construction against freshly checked-out sources — each class then PASSING at `76661dc1` once its artefact was repaired in the throwaway worktree.
G11 LOG PROVENANCE: `full_log_provenance.txt` lists all 13 raw files under `.remedy-wt/.cache/gate_r23/` with line count and sha256, records that only derived `.txt` evidence is committed, and states that the worktree and `tmp/base-gate-r23` were removed after every reading was taken.
G12 CANARY, in the PRIMARY checkout after both gate runs ended: `python3 -m pytest tests/cli/test_golden_path.py -q` — exit 0, `42 passed in 20.52s`.
G13 NO MARKER LEAKED: 0 LINES beginning `<<<SLICE ` or `<<<END ` in `.agent/plan.md`, in `.agent/live_review.md` and in each of the 12 files under `.agent/gate_f086_r23/` at C4; the `.agent/handoff.md` reading can only be taken after C5 and is in the round report.
G14 CHANGE SET AND HISTORY: the printed path set equals the Change list other than `.agent/handoff.md`, with no path on either side alone; all six paths the Change section FORBIDS are PRESENT at `43e7f1e0` by `git ls-tree` and none is touched; the range is linear with every commit at exactly one parent and every round `git reflog` entry `commit:`; insertions before C4 are 334, 285, 14, 4 and 243, none over 500.
G15 THE HANDBACK, BOTH HALVES: (a) `wc -l` of `.agent/handoff.md` at C4 reads 56, within constraint 9's bound of 56 and G15(a)'s 57; (b) at C5 it reads (a) plus VERDICT's 44 — see the Deviations line on the block's two disagreeing numerals. All seven mandated headings of docs/agents/handback_template.md are present in the template's order and none is dropped; the prefix-and-remainder equality against VERDICT is measurable only after C5 and is in the round report.
G16 OPEN PR GATE, re-read at the handback: `gh pr list --state open --json number,headRefName,baseRefName,isDraft` printed `[]`. Nothing created, nothing merged.

## Authored-text proofs

PLAN23, RECORD21, DONE0588 and VERDICT were all EXTRACTED programmatically from the committed `.agent/authored/f086-r23.md`, never retyped. Disk-to-disk: `.agent/plan.md` at C1 equals PLAN23 exactly (G3); C2's remainder equals blank+RECORD21+blank+DONE0588 exactly (G4); C5's remainder equals VERDICT exactly, reported in the round report because it is measurable only after C5.
The block itself: the scratchpad, the committed authored copy and the committed last-block mirror are byte-EQUAL (G2). No marker line reached any target file (G13).

## Deviations & assumptions

THE BLOCK'S TWO CLAUSES ON VERDICT'S LENGTH DISAGREE: constraint 9 states the slice is 44 lines and that C5 is "C4's length plus 44", while G15(b) orders "(a) plus 43". Measured on the committed C0a the slice is 44 lines, so G15(b)'s numeral is unmeetable. Per constraint 1 the slice was applied byte-verbatim and the defect is declared here, not repaired.
G9'S MANDATED RESTORE METHOD CAUSED 7 OF THE 23 BASE-ONLY FAILURES: `shutil.copytree` defaults to `symlinks=False`, which dereferenced the 23 npm bin shims under `apps/ui/node_modules/.bin`, so `.bin/vite` and `.bin/vitest` resolved their own dist imports from `.bin/` and died with ERR_MODULE_NOT_FOUND. The base run was executed exactly as ordered; the consequence is attributed rather than hidden.
TWO RE-RUNS THE BLOCK DID NOT ORDER were then added INSIDE the throwaway worktree, after the base run and after its parity readings, to attribute those 23 ids by demonstration: a symlink-PRESERVING recopy of `apps/ui/node_modules` (7 ids pass), then an `os.utime` of the copied `apps/ui/dist` past the freshly checked-out source mtimes with the dist digest unchanged and no rebuild (16 ids pass). Neither touched the primary checkout, whose dist digest and mtime were re-read after each and never moved.
G10 CONDITIONS BASE-ONLY ATTRIBUTION ON THE PARITY CLAIM GOING VOID; parity HELD and 23 base-only ids existed anyway, so that condition would have left them unattributed. docs/agents/integration_gate.md step 3 rules an unattributed `comm -23` id a genuine base failure, so every one was attributed regardless.
OTHERWISE NONE: the ordered sequence C0a, C0b, C1, C2, C3, C4, C5 ran in order, with no extra commit, none dropped and no reordering; constraint 3 was honoured; the compact form of constraint 9 is used — ONE commits table, ONE line per gate, the transcript in the round report; and no verdict was authored by the worker anywhere.

## Next

The reviewer reviews `43e7f1e0..HEAD` and records R23's verdict in `.agent/live_review.md` as `Gate: R24 — the R23 entry.`; the next substantive work is closure.
