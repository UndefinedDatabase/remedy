# Handback — F305 round 5: the closing round — book round 4, the Built State, the rotation, the STATUS flip with the README sync, and the pull request

## Session

SESSION 1 of feature F305 · round 5 · rounds so far 5

Context self-assessment: the session verified the block's own line count and sha256 and all
fifteen Bundle-listed prepared files' digests before any write, byte-copied and re-hashed every C1
and C3 target against its prepared source, confirmed the exact path set and numstat before each
commit, ran the rotation and every gate exactly once with real output captured, and closed every
gate green on the first pass; context remains comfortable at handback.

Fortschritt: 100 % (F305 is accepted; its pull request waits for the next session's Open PR Gate) — Schätzung

## Range

Review of `915925988`..HEAD.

## Commits

### e2c182719 F305 R5 C1: book round 4, the Built State, save the round 5 block, the STATUS line and the PR body

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f305-r5.md` | +120/-0 | NEW FILE, byte copy of `block.md` (120 lines, sha256 `f5790a6bd3ed6d8cf1cea1a61df45a677ae966d03d8af4fc028cab43c803e4cb`, matching both values the session was given) |
| `.agent/authored/f305-r5-status_line.txt` | +1/-0 | NEW FILE, byte copy of `prep/src-status_line.txt` |
| `.agent/authored/f305-r5-pr_body.md` | +53/-0 | NEW FILE, byte copy of `prep/src-pr_body.md` |
| `.agent/live_review.md` | +2/-0 | base plus `prep/append-live_review.txt`: the `Gate: F305 R4` entry appended |
| `.agent/plan.md` | +9/-9 | rewritten in full for F305 round 5, byte copy of `prep/src-plan.md` |
| `docs/roadmap/features/T13_F305.md` | +29/-0 | Built State section appended, byte copy of `prep/sim-T13_F305.md` |

### adbe1407b F305 R5 C2: rotate the finding ledger into its archive

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +0/-32 | `scripts/rotate_live_review.py` run once from the primary checkout; moved 14 gate records and 1 finding pair (2 records) into the archive |
| `.agent/live_review_archive.md` | +33/-0 | same rotation run; receives the moved records |

### this commit F305 R5 C3: accept F305 in STATUS with its README sync and the self-use queue

| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | +1/-1 | F305's line flipped `[~]` → `[x]` with its closure annotation, byte copy of `prep/sim-STATUS.md` |
| `README.md` | +10/-3 | accepted count 138→139, Tier 13 accepted row 1→2, F305 added to the Tier 13 accepted list, byte copy of `prep/sim-README.md` |
| `scripts/self_use_queue.json` | +1/-1 | self-use entry `SU-057`'s `consumed_by` set to `F305`, byte copy of `prep/sim-self_use_queue.json` |
| `.agent/handoff.md` | this commit | this file (self-reference rule, `docs/agents/handback_template.md`) |

## External actions

`git -C /home/decodeux/Repos/remedy push origin feature/f305-multi-repo-chain-band` after this
commit, then
`gh pr create --repo UndefinedDatabase/remedy --base main --head feature/f305-multi-repo-chain-band --title "F305 — Multi-repo missions: the cockpit's chain band" --body-file .agent/authored/f305-r5-pr_body.md`
— both outcomes reported in the final reply only, not here, because the handoff is written before
either command runs and cannot name a pull request number that does not yet exist. No pull request
merged this round (the block forbids it). No `git worktree add`/`remove` performed; the worker's
own scratch directory `.remedy-wt/f305-r5-worker/` (gitignored) held the digest, copy, rotation and
gate scripts.

## Verification

**Preconditions (before C1):** `git rev-parse HEAD` read `9159259880fb091082924c8b0953d9cf03afc683`,
equal to `origin/feature/f305-multi-repo-chain-band`; `git status --porcelain` empty; `.agent/STOP`
absent; `git branch --show-current` read `feature/f305-multi-repo-chain-band`.

**Block digest (before any write):** `wc -l block.md` read `120`, its sha256 read
`f5790a6bd3ed6d8cf1cea1a61df45a677ae966d03d8af4fc028cab43c803e4cb` — both equal to the values the
prompt delivered.

**Bundle digests (before any write):** all fifteen digest-bearing prepared files
(`src-status_line.txt`, `src-pr_body.md`, `sim-C1-live_review.md`, `src-plan.md`,
`sim-T13_F305.md`, `sim-C2-live_review.md`, `sim-C2-live_review_archive.md`, `sim-rotation.txt`,
`sim-STATUS.md`, `sim-README.md`, `sim-self_use_queue.json`, `append-live_review.txt`, `verify.py`,
`run_selection.py`, `selection.txt`) were hashed and matched the block's stated digests exactly
before use (a Python sha256 reader, all fifteen `OK`).

**C1:** byte-copied `block.md`, `src-status_line.txt` and `src-pr_body.md` to their new-file
destinations; byte-copied `src-plan.md` over `.agent/plan.md` in full; appended
`append-live_review.txt`'s bytes to `.agent/live_review.md`; byte-copied `sim-T13_F305.md` over
`docs/roadmap/features/T13_F305.md` in full. Every resulting file's sha256 matched the Bundle's
stated digest exactly. `git status --porcelain` then `git diff --numstat` (working tree, before
staging) read exactly the six C1 pairs and no other path:
```
2	0	.agent/live_review.md
9	9	.agent/plan.md
29	0	docs/roadmap/features/T13_F305.md
```
plus the three new files, each untracked. `git add` of the six paths, then
`git diff --cached --numstat` read:
```
53	0	.agent/authored/f305-r5-pr_body.md
1	0	.agent/authored/f305-r5-status_line.txt
120	0	.agent/authored/f305-r5.md
2	0	.agent/live_review.md
9	9	.agent/plan.md
29	0	docs/roadmap/features/T13_F305.md
```
`git branch --show-current` read `feature/f305-multi-repo-chain-band` immediately before the
commit. Commit `e2c182719`, `git show --numstat` matched the table above exactly.

**C2:** before the run, `.agent/live_review.md` read 149287 bytes and
`.agent/live_review_archive.md` read 6645394 bytes, matching the sim's stated "old" sizes exactly.
`python3 scripts/rotate_live_review.py` ran once from the primary checkout (`cwd=/home/decodeux/Repos/remedy`),
its exit code and whole stdout captured in the same launching script:
```
exit 0
gate records moved: 14
finding pairs moved: 1 (2 records)
resolved-text records moved: 0
old ledger size: 149287 bytes
new ledger size: 124594 bytes
old archive size: 6645394 bytes
new archive size: 6670088 bytes
open findings before: 4
open findings after: 4
gate headers matching neither known form (left in place): 1
written: /home/decodeux/Repos/remedy/.agent/live_review.md and /home/decodeux/Repos/remedy/.agent/live_review_archive.md
```
Equal to `sim-rotation.txt` from its second line onward, apart from the last line naming the
primary checkout's own paths instead of the simulation's. `.agent/live_review.md` and
`.agent/live_review_archive.md` were then read byte-for-byte against their C2 Bundle files
(`sim-C2-live_review.md`, `sim-C2-live_review_archive.md`): both equal, and both sha256 matched the
Bundle's stated digests exactly. `git status --porcelain` showed exactly these two paths modified,
no other path. `git diff --numstat` read:
```
0	32	.agent/live_review.md
33	0	.agent/live_review_archive.md
```
Commit `adbe1407b`, `git show --numstat` matched exactly.

**C3 file copy:** byte-copied `sim-STATUS.md` over `docs/roadmap/STATUS.md`, `sim-README.md` over
`README.md` and `sim-self_use_queue.json` over `scripts/self_use_queue.json`. Every resulting
file's sha256 matched the Bundle's stated digest exactly. `git status --porcelain` showed exactly
these three paths modified, no other path. `git diff --numstat` read:
```
10	3	README.md
1	1	docs/roadmap/STATUS.md
1	1	scripts/self_use_queue.json
```

**Gate 1 (status + verify.py):** `git -C /home/decodeux/Repos/remedy status --porcelain` →
```
 M README.md
 M docs/roadmap/STATUS.md
 M scripts/self_use_queue.json
```
exactly the three C3 files, no other path. Then
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f305-r5/prep/verify.py /home/decodeux/Repos/remedy` →
```
equal at C1 .agent/authored/f305-r5.md True
equal at C1 .agent/authored/f305-r5-status_line.txt True
equal at C1 .agent/authored/f305-r5-pr_body.md True
equal at C1 .agent/live_review.md True
equal at C1 .agent/plan.md True
equal at C1 docs/roadmap/features/T13_F305.md True
C1 ledger is base plus slice True
equal at C2 .agent/live_review.md True
equal at C2 .agent/live_review_archive.md True
equal in the working tree docs/roadmap/STATUS.md True
equal in the working tree README.md True
equal in the working tree scripts/self_use_queue.json True
ALL True
```
Every line `True`, last line `ALL True`.

**Gate 2 (status line occurrence):** a Python reading of
`.agent/authored/f305-r5-status_line.txt` without its trailing newline against
`docs/roadmap/STATUS.md`: `occurrences: 1`; `tilde lines count: 0` (no line of that file starts
`- [~]`).

**Gate 3 (selection):**
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f305-r5/prep/run_selection.py /home/decodeux/Repos/remedy` →
```
563 passed in 28.60s
exit 0
```
Exit 0, no FAILED or ERROR line, `563 passed` matching the simulation's reading exactly.

**Gate 4 (integrity):** `python3 -m apps.cli.main integrity check --json` →
```json
{"check_count": 6, "checks": [{"message": "handlers=184", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Exit 0, all six checks `pass`, `fail_count` 0.

**Gate 5 (open findings list):**
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1235', 'R-1246', 'R-1251', 'R-1252']`, matching exactly.

No mutation run, no test beyond gate 3's one selection run (this round forbids more). No
`REMEDY_TEST_MAX_WORKERS` set, no extra `-n` passed. No `npm`/`npx` run. No pull request opened,
edited or merged before this commit. No provider call made this round.

## Authored-text proofs

1. `block.md` → `.agent/authored/f305-r5.md` (C1): byte-equal, confirmed by the copy script's own
   printed sha256 and again by gate 1's `verify.py`.
2. `prep/src-status_line.txt` → `.agent/authored/f305-r5-status_line.txt` (C1): byte-equal,
   confirmed the same way.
3. `prep/src-pr_body.md` → `.agent/authored/f305-r5-pr_body.md` (C1): byte-equal, confirmed the
   same way; this is the exact file the pull request's `--body-file` will cite.
4. The base `.agent/live_review.md` + `prep/append-live_review.txt` → `.agent/live_review.md` (C1):
   built by direct append, confirmed byte-equal to `prep/sim-C1-live_review.md` before staging and
   again by gate 1's `verify.py`.
5. `prep/src-plan.md` → `.agent/plan.md` (C1): byte-equal, confirmed the same way.
6. `prep/sim-T13_F305.md` → `docs/roadmap/features/T13_F305.md` (C1): byte-equal, confirmed the
   same way; the first 65 lines unchanged, 29 lines of Built State appended.
7. The rotation's own output (C2): byte-equal to `prep/sim-C2-live_review.md` and
   `prep/sim-C2-live_review_archive.md`, confirmed by direct comparison and gate 1's `verify.py`.
8. `prep/sim-STATUS.md` → `docs/roadmap/STATUS.md` (C3): byte-equal, confirmed by the copy
   script's own printed sha256.
9. `prep/sim-README.md` → `README.md` (C3): byte-equal, confirmed the same way.
10. `prep/sim-self_use_queue.json` → `scripts/self_use_queue.json` (C3): byte-equal, confirmed the
    same way.

## Deviations & assumptions

None. Every commit matched the block's ordered sequence (C1, C2, C3) with no extra commit, no
dropped commit and no reordering. No file was written outside each commit's named path set. The
rotation ran exactly once, from the primary checkout, with its exit code and whole output captured
in the launching script rather than a shell redirection (the sandbox refused a shell `&&`/redirect
chain for this step). `.agent/STOP` did not appear during the round; no merge, branch
create/switch beyond the one feature branch, or force-push was performed; no pull request was
opened or merged before this commit; no mutation was run; exactly one test command ran this round
(gate 3's selection); `REMEDY_TEST_MAX_WORKERS` was never set and no extra `-n` was passed;
`npm`/`npx` were never run.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): absent throughout this round; the next session checks it first.
2. The Open PR Gate, which merges F305's pull request in the next session.
3. The next feature's first commit books round 5's verdict.
4. Rule A5, the next unchecked line in `docs/roadmap/STATUS.md`.

Operator questions open: 1.
Open findings: 4 (R-1235, R-1246, R-1251 and R-1252, Low, owned by F306).

## For the operator, in plain sentences

This feature is finished. It gives a person a Missions button in the cockpit's right panel that
opens one card for each repository's mission; opening a card shows its newest orders, each with
how many model calls and tokens its jobs used and one small chip per job in every repository the
order reached, and clicking a chip opens that job in its own project's view. A test proves this
works in a real browser. The whole test collection passed once on the exact code that ships. A
review package was built and saved. A pull request is open and will be merged automatically at the
start of the next working session unless the operator merges it sooner. Four small problems stay
written down for the next clean-up feature to pick up. One question still waits for the operator's
answer, and the session's reversible choice for it already stands in the meantime.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | round 4 booked (VERDICT PASS), the Built State appended, the round 5 block and the STATUS line and PR body saved, `.agent/plan.md` rewritten for round 5; all byte proofs `True` |
| C2 | done | the ledger rotated once; both resulting files byte-equal to the Bundle's C2 files |
| C3 | done | STATUS flipped `[x]`, README synced, self-use `SU-057` consumed_by set to `F305`, handback written in the same commit |
| Push | done | reported in the final reply |
| Pull request | done | reported in the final reply |
| Gate 1 | passed | every line `True`, `ALL True` |
| Gate 2 | passed | occurrence count 1, no `- [~]` line |
| Gate 3 | passed | exit 0, `563 passed`, no FAILED/ERROR line |
| Gate 4 | passed | `fail_count` 0, six checks `pass` |
| Gate 5 | passed | open findings list matched exactly |
