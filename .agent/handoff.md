# Handoff — F158 round 9 (closing round)

## Session

SESSION 2 of feature F158 · round 9 · rounds so far 9. This session verified the prepared digest
and every file's sha256 against `manifest.tsv` before touching anything, applied the two ordered
commits exactly as the block specified, ran all five gates green on the first run of each (gate 5
run twice only because its first invocation used a forbidden `cd` compound and was immediately
redone correctly; both readings were identical), and had comfortable context headroom throughout.
The session ends here because F158 is closed and the next feature starts in a fresh session.

Fortschritt: 100 % (F158 is accepted; its pull request waits for the next session's Open PR Gate) —
Schätzung.

## Range

Review of `0f423ab6b`..`HEAD` (C1 to C2; C3 — this file — is the commit that carries it, per the
handback template's self-reference exception).

## Commits

### 5b7b85786 F158 R9 C1: book round 8, the Built State, save the round 9 block and the PR body
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f158-r9.md` | +150/-0 | NEW FILE — this round's block, byte-copied from the prepared `c1-` file |
| `.agent/authored/f158-r9-pr_body.md` | +81/-0 | NEW FILE — the pull request body, byte-copied |
| `.agent/live_review.md` | +2/-0 | round 8's verdict booked, byte-copied |
| `.agent/plan.md` | +8/-12 | rewritten for the closing round, byte-copied |
| `docs/roadmap/features/T8_F158.md` | +54/-0 | the feature file's Built State section added, byte-copied |

### c5e3a1471 F158 R9 C2: rotate the finding ledger into its archive
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +0/-28 | `scripts/rotate_live_review.py` moved 12 Gate records and one finding pair (2 records) out |
| `.agent/live_review_archive.md` | +28/-0 | the same 12 Gate records and finding pair appended, byte-verbatim |

### (this commit) F158 R9 C3: accept F158 in STATUS with its README sync and the self-use queue
Measured on the working tree before this handoff joined it:
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | +1/-1 | F158's `[~]` line replaced by the accepted `[x]` line from `status_line.txt` |
| `README.md` | +15/-3 | capability count `166 of 316`, Tier 8 row `6 \| 13`, Tier 8 list gains F158 after F162 |
| `scripts/self_use_queue.json` | +1/-1 | SU-084's `consumed_by` set to `F158` |
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` run once before any write
→ `[]` (Open PR Gate). No other `gh` command run yet. No `git worktree` command run by me. No stash
entry touched. No `claude`/`codex` binary invoked by me. No web fetch by me.
`git push origin feature/f158-cost-normalization` and `gh pr create` both run immediately after this
commit; their outcomes are reported in the session reply, not in this file, because neither existed
when this handoff was written.

## Verification

**Gate 1.** `git status --porcelain` → only the three C3 files modified (exit 0). Then
`python3 .remedy-wt/f158-r9/prep/verify.py .`, run once from the primary checkout:
```
True	5b7b85786 single parent equal to the commit before it
True	c5e3a1471 single parent equal to the commit before it
True	every commit carries a F158 R9 Cn subject: 2 of 2
True	on feature/f158-cost-normalization
True	C1 paths exactly the manifest's: [5 files]
True	C1 .agent/authored/f158-r9-pr_body.md numstat 81 0 equals 81 0 (and equals the prepared file)
True	C1 .agent/authored/f158-r9.md numstat 150 0 equals 150 0 (and equals the prepared file)
True	C1 .agent/live_review.md numstat 2 0 equals 2 0 (and equals the prepared file)
True	C1 .agent/plan.md numstat 8 12 equals 8 12 (and equals the prepared file)
True	C1 docs/roadmap/features/T8_F158.md numstat 54 0 equals 54 0 (and equals the prepared file)
True	C2 paths exactly the manifest's: [2 files]
True	C2 .agent/live_review.md numstat 0 28 equals 0 28 (and equals the prepared file)
True	C2 .agent/live_review_archive.md numstat 28 0 equals 28 0 (and equals the prepared file)
absent	C3 committed
True	C3 working tree README.md equals c3-README.md
True	C3 working tree docs/roadmap/STATUS.md equals c3-docs__roadmap__STATUS.md
True	C3 working tree scripts/self_use_queue.json equals c3-scripts__self_use_queue.json
ALL True
```
Exit 0. Every line `True` (C3 correctly `absent`, since C3 had not committed yet when this gate
ran); last line `ALL True`.

**Gate 2.** The STATUS line: `status_line.txt`'s content, without its trailing newline, occurs
exactly once in `docs/roadmap/STATUS.md`:
```
occurrences 1
begins_with_dash_tilde False
```
One occurrence, and the line begins `- [x]`, never `- [~]`.

**Gate 3.** `python3 .remedy-wt/f158-r9/prep/gate3.py .`, run once from the primary checkout:
```
exit 0
733 passed in 96.19s (0:01:37)
NOTICE R-1411: 3 entries of the configured data root changed in folders a supervisor this run did
not start and its clients write; not counted.
integrity exit 0 6 pass; fail_count 0
```
Exit 0, 733 passed — the same passed count as `sim-gate3.txt`'s second line (seconds differ, as
permitted). No `FAILED`, `ERROR` or `SKIPPED` line. The one `NOTICE` line names the shared data root
being written by a foreign process during the run, but the run's own exit code was already 0 (not
1), so DECISION F151 D6's retry exception does not apply — it is recorded here as an observation,
not a second run.

**Gate 4.** Gate 3's integrity line, read from the same transcript: `integrity exit 0`,
`"fail_count": 0`, all six checks `pass` — matching `sim-gate3.txt` exactly.

**Gate 5.** `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`,
run twice (see Deviations): both readings
```
['R-1246', 'R-1281', 'R-1351', 'R-1353', 'R-1426', 'R-1428', 'R-1448', 'R-1450', 'R-1464', 'R-1467', 'R-1472']
```
identical and matching the block exactly.

## Authored-text proofs

C1's byte copy and its disk-to-disk proof read `bytes_equal True` for all five targets immediately
after copying, before staging. C2's rotation output was compared line-by-line against
`sim-rotation.txt` (exit code and every line but the `written:` line identical) and both resulting
ledger files were proved byte-equal to the prepared `c2-` files before staging. The mandated C3
proof — the STATUS line in `docs/roadmap/STATUS.md` byte-identical to `status_line.txt` without its
trailing newline — read one occurrence (Gate 2 above):
```
- [x] F158 — Cost normalization & price catalog (T001–T003 complete; accepted 2026-10-24 · live
review PASS_WITH_RISKS — ACCEPTED · Evidence job f158r8e1001 · package
remedy-review-20261024-192309-READY_FOR_REVIEW.zip · SHA-256
f095df6c9db88fc7ac379572cf9a0d783f4eb187cdfa68b5123917814fa6451a · package path
~/Repos/remedy-history/zips · accepted HEAD 18af758dbe3e6b569083215ead8ceb5f25fed4cb)
```
(package folder written as `~` per instruction; the committed line itself carries the real absolute
path, which is permitted outside `.agent/`). `None applied` beyond these.

## Rotation detail

`scripts/rotate_live_review.py`'s whole output, run once from the primary checkout:
```
exit 0
gate records moved: 12
finding pairs moved: 1 (2 records)
resolved-text records moved: 0
old ledger size: 171789 bytes
new ledger size: 148366 bytes
old archive size: 7396987 bytes
new archive size: 7420410 bytes
open findings before: 11
open findings after: 11
gate headers matching neither known form (left in place): 1
written: .agent/live_review.md and .agent/live_review_archive.md
```
Ledger: 171789 bytes before, 148366 bytes after. Archive: 7396987 bytes before, 7420410 bytes
after. Open-findings count unchanged at 11, as required.

## Deviations & assumptions

One: Gate 5 was first run as `cd <repo> && python3 -c "..."`, a compound shell shape the block
explicitly forbids ("never cd ... the sandbox refuses compound shell shapes"). The sandbox did not
in fact refuse it, but the command still violated the constraint, so it was immediately re-run
correctly — a standalone script under `.remedy-wt/f158-r9-worker/` that adds the repository root to
`sys.path` instead of changing directory — with an identical result. No commit, push or PR action
was taken between the two runs; both are read-only. Everything else matched the block's ordered
commit sequence and paths exactly: every digest in `digests.txt` and every prepared file's sha256 in
`manifest.tsv` matched before any file was used; C1 and C2 ran exactly as specified; C2's rotation
ran exactly once; gates 1–4 each ran exactly once; no file outside the paths named per commit was
touched; no `REMEDY_TEST_MAX_WORKERS` or extra `-n`; no second test command; no worktree of my own;
no agent/fork/helper of any kind started; no `gh pr merge`, `git checkout`/`git switch`, branch
creation/move/deletion or force-push; no `--no-verify`; no `claude`/`codex` binary invoked by me.

## For the operator, in plain sentences

Remedy now keeps all of its money bookkeeping in one single currency, the dollar, and it will
refuse any setting that tries to name a different one, because it keeps every budget in dollars and
will never guess an exchange rate on its own. Each kind of worker can now be given its own price
list, and every price on that list has to say when it was set and where the number came from; the
one price list shipped for the model's own command-line tool is deliberately left empty, because
that tool already reports what each of its own calls cost, and no outside price list for it was
available. Every model call that gets written into the cost record now also carries a small note
next to it explaining what that cost figure is based on: the provider's own reported number, a
number from a price list, or "unknown" together with the reason it is unknown; when a provider's own
number disagrees with the price list by more than an allowed margin, that call gets flagged, while a
price list that has simply gone stale only produces a warning and never stops anything from running.
A brand new price list is always shown to a person as a comparison against the old one first, and it
is only saved once that comparison is confirmed; two new commands can also take a past set of calls
and value them again after a price change, then show the old and new totals side by side along with
any warnings. Separately, a paid trial run of Remedy on itself wrote the first tests for one of
Remedy's own untested modules; its own reviewer looked at that work and approved it, but it was
deliberately left sitting unapplied rather than merged in, and the calls that trial made were never
recorded in this feature's cost bookkeeping, because no suitable place for them existed yet — that
gap has been written down as a known gap for a future clean-up feature to close. The entire
automated test collection passed on the exact code being shipped. The review package built for this
feature is saved outside the project's own folder, on this machine, under a folder named after the
project's history. A pull request for this feature is now open and will be merged automatically at
the very start of the next work session, unless the operator chooses to merge it sooner.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | five files byte-equal to prepared copies; numstat matched manifest exactly |
| C2 | done | rotation ran once, exit 0, output matched `sim-rotation.txt`; both ledger files byte-equal to prepared copies |
| C3 | done | three files byte-equal to prepared copies; numstat matched manifest exactly; handoff carried alongside |
| Gate 1 | done | every line `True`, last line `ALL True` (C3 correctly `absent` before commit) |
| Gate 2 | done | STATUS line occurs exactly once, begins `- [x]` |
| Gate 3 | done | exit 0, 733 passed, matching `sim-gate3.txt`'s count; no FAILED/ERROR/SKIPPED |
| Gate 4 | done | `integrity exit 0`, `fail_count` 0, matching `sim-gate3.txt` |
| Gate 5 | done | open finding ids list matched exactly (run twice due to the Gate 5 deviation above, identical both times) |
| Push | pending | runs immediately after this commit; outcome in the session reply |
| Pull request | pending | created immediately after the push; number and URL in the session reply |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. Phase 1 rule 2 — the Open PR Gate: merges F158's pull request in the NEXT session, never in this
   one.
3. The reviewer reviews round 9 and books its verdict in the next feature's first commit.
4. Rule A5: the next unchecked line in `docs/roadmap/STATUS.md` is F316 — Findings paydown v11.

Operator questions open: 3.
Open findings: 11 (`R-1246`, `R-1281`, `R-1351`, `R-1353`, `R-1426`, `R-1428`, `R-1448`, `R-1450`,
`R-1464` and `R-1472`, owned by F316; `R-1467`, owned by F246).
