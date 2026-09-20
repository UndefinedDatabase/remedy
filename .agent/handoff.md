# Handoff — F276 Data-root hygiene & disk budget · Round 13

## Session

SESSION 3 of feature F276 · round 13 · rounds so far 13

Context self-assessment: the worker read AGENTS.md in full, verified the step
block's bytes before using it — 320 lines, sha256
`9a908e2a61bb0907210aa2fc2e329461c9638bfecde8149d84fc33ba9a961f3c`, both
readings identical to the digest and line count the delegation message named
(R-0954) — then read `docs/agents/handback_template.md` and
`docs/roadmap/STATUS_closure_protocol.md`, found no `.agent/STOP` on disk,
verified all seven payloads under `.remedy-wt/f276-r13/` (P2-P8) byte-for-byte
against their stated line counts and digests, applied C1, C2 and C3, ran G1
(transport/state forensics), G2 (repair confinement and green suites) and G3
(the mutation red-proof, in a disposable worktree already added and removed),
and is writing this handoff (C4) before running the integrity check, the
evidence job and the review package — G4, G5 and G6 — all three of which the
block's own Bundle places AFTER C4 with the tree clean and nothing further
committed, so this file cannot and does not carry their outputs; those go to
the round report instead, exactly as the block orders for the package's own
name and hash.

## Range

Review of b8ecbb7a..HEAD.

## Commits

### 628ce362 f276-r13: book round 12 verdict, register R-1010 (C1)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/authored/f276-r13-block.md | 320/0 | shutil.copyfile of P1 (this block) |
| .agent/authored/f276-r13-ledger.md | 4/0 | shutil.copyfile of P2 |
| .agent/authored/f276-r13-plan.md | 49/0 | shutil.copyfile of P3 |
| .agent/authored/f276-r13-prose-slips.md | 1/0 | shutil.copyfile of P4 |
| .agent/authored/f276-r13-ledger-done.md | 2/0 | shutil.copyfile of P7 (applied at C3) |
| .agent/live_review.md | 4/0 | append P2: round 12 PASS verdict + R-1010 registration |
| .agent/plan.md | 18/18 | rewrite with P3 |
| .agent/prose_slips.md | 1/0 | append P4: round-11 numstat-reading lesson |

Insertions by `git show --numstat` sum to 399. Well under the 500-line cap;
no exception is spent this round (constraint 4 — the AGENTS.md oversize
exception is already spent by `c6a519d1` and unavailable here).

### ba4dd38f f276-r13: widen parse_safe_diff_paths to read hunkless diff entries (C2)
| Path | +/- | Reason |
|------|-----|--------|
| packages/orchestration/repair_attest.py | 54/0 | rewrite with P5 — the R-1010 repair |
| tests/orchestration/test_repair_attest.py | 78/0 | rewrite with P6 — the red proof |

Insertions by `git show --numstat` sum to 132. Confined to exactly these two
paths (G2's `git show --numstat` reading, reported in full below).

### ba518b42 f276-r13: book Done R-1010, resolved by this round's C2 (C3)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/live_review.md | 2/0 | append P7: `Done: R-1010` resolution |

### This handoff (C4, self-reference, R-0149 pattern)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewritten | a handoff cannot table the commit that writes it |

## External actions

- `git worktree add .remedy-wt/f276-r13-mutation ba4dd38f` — G3's disposable
  mutation worktree, added at C2. Outcome: control run 9 passed, exit 0
  (GREEN); mutation applied (`git checkout b8ecbb7a --
  packages/orchestration/repair_attest.py`, that one path only); mutated run
  5 failed / 4 passed, exit 1 (RED), with two nodes of
  `TestHunklessDiffEntriesAreVisible` staying green as discriminators.
  Removed with `git worktree remove .remedy-wt/f276-r13-mutation --force`
  as G3's last action. `git worktree list` afterward showed the primary
  checkout and the two job worktrees only — full transcript in the round
  report.
- `git push origin feature/f276-data-root-hygiene` — after C4, per G6.
  Outcome reported in the round report (postdates this file by
  construction).
- No `gh` command was run this round. No pull request was opened, edited or
  merged. No branch was created or deleted. No history was rewritten. No
  force-push.
- The two job worktrees under `.remedy-wt/` (`job-468c8e62a2cc4fac`,
  `job-c1dba9c3d7874968`) belong to earlier jobs and were left alone per
  constraint 5. `.remedy-wt/` scratch (this round's and earlier rounds'
  payload directories) was left intact; no `git clean -x` was run.

## Verification

**R-0954 — THE SAVED BLOCK'S OWN BYTES, two readings side by side.**
```
delegation message stated for P1 : lines 320  sha256 9a908e2a61bb0907210aa2fc2e329461c9638bfecde8149d84fc33ba9a961f3c
worker's own reading on disk     : lines 320  sha256 9a908e2a61bb0907210aa2fc2e329461c9638bfecde8149d84fc33ba9a961f3c
EQUAL on both readings: True
```

**ALL SEVEN PAYLOADS (P2-P8), verified byte-for-byte before use.**
```
wc -l   file                          sha256sum
  4     ledger.md                     77774dbee01fc24d35869ee7c96d0d30cfc0de65d058d19ebc474057b76a0c41
 49     plan.md                       7adab1f8aab9a688cb6758c2d63c0070c2652c7ef2b84017d1a363dc6024609c
  1     prose_slips.md                7beaa26d2add5c290e94ee9fd91f081a5a23ed8527dee1e93339a45025770e7e
156     repair_attest.py              7811676fd35f45d1885cbc2739cf7c9d73001ef919ccd17be657bbedee85750d
279     test_repair_attest.py         29b69d42eb2bf94d54a369826da23c756b8876c08861ed31bbed9dd4ae089418
  2     ledger_done.md                017e406ae83eb4390cdbe086d57930a344aae0ecebc0a2f3fe054a5ea7f98669
147     create_f276_evidence.py       37e1660e41ed8beb8b89247b77b2140f8d56ca232598bb56a6faa578cc14d378
```
Every line count and digest matches the block's P2-P8 statement exactly
(P1's is the R-0954 pair above).

**G1 — TRANSPORT AND STATE. Command: on-disk python checks using `git show`.**
```
G1(a) — five authored copies, each == its payload byte for byte: True x5
G1(a) files measured: 5

G1(b) — .agent/live_review.md record append, full byte forensics:
  AT C1 (628ce362), against b8ecbb7a bytes + P2 bytes:
    reading (a) byte equality:                                   True
    reading (b) structural, last 2 paragraph-units == P2's 2:     True (N=2, counted from P2)
    negative control (byte flip in first appended paragraph)
      rejected by BOTH readings:                                  True
  AT C3 (ba518b42), against C1 (628ce362) bytes + P7 bytes:
    reading (a) byte equality:                                   True
    reading (b) structural, last 1 paragraph-unit == P7's 1:      True (N=1, counted from P7)
    negative control (byte flip in first appended paragraph)
      rejected by BOTH readings:                                  True

G1(c) — byte equality only:
  .agent/prose_slips.md at C1 == b8ecbb7a bytes + P4 bytes:       True
  .agent/plan.md at C1 == P3 bytes:                                True
  packages/orchestration/repair_attest.py at C2 (git show) == P5:  True
  tests/orchestration/test_repair_attest.py at C2 (git show) == P6: True

TOTAL READINGS TAKEN: 15
ALL TRUE: True
```

**G2 — THE REPAIR IS CONFINED AND GREEN, at C2 (ba4dd38f).**
```
$ git show --numstat ba4dd38f
54  0  packages/orchestration/repair_attest.py
78  0  tests/orchestration/test_repair_attest.py
(exactly two paths, no third)

$ python3 -m pytest -q tests/orchestration/test_repair_attest.py
9 passed in 84.78s   exit 0

$ python3 -m pytest -q tests/orchestration/test_diff_parser.py \
    tests/orchestration/test_round13_evidence_alignment.py \
    tests/orchestration/test_review_package_status.py \
    tests/orchestration/test_review_authoritative_e2e.py \
    tests/orchestration/test_development_artifact_boundary.py \
    tests/cli/test_golden_path.py
153 passed in 138.93s   exit 0

$ python3 -m ruff check packages/orchestration/repair_attest.py tests/orchestration/test_repair_attest.py
All checks passed!   exit 0
```
All three numbers (9, 153, "All checks passed!") match the reviewer's
measurement stated in the block exactly; no deviation to report.

**G3 — THE MUTATION RED-PROOF, disposable worktree `.remedy-wt/f276-r13-mutation` added at ba4dd38f, no `__pycache__` present to purge, run with `python3 -B`.**
```
(i) CONTROL — python3 -B -m pytest -q tests/orchestration/test_repair_attest.py
    9 passed in 0.27s   exit 0   (GREEN)

(ii) MUTATION — git checkout b8ecbb7a -- packages/orchestration/repair_attest.py
    git status --porcelain in the worktree: " M packages/orchestration/repair_attest.py" only

(iii) MUTATED RUN — python3 -B -m pytest -v tests/orchestration/test_repair_attest.py
    5 failed, 4 passed in 0.30s   exit 1   (RED)

FAILED node ids:
  tests/orchestration/test_repair_attest.py::TestHunklessDiffEntriesAreVisible::test_an_added_empty_file_is_named_by_its_header
  tests/orchestration/test_repair_attest.py::TestHunklessDiffEntriesAreVisible::test_a_pure_rename_is_named_by_its_destination
  tests/orchestration/test_repair_attest.py::TestHunklessDiffEntriesAreVisible::test_an_added_empty_file_whose_path_holds_a_space_is_read_whole
  tests/orchestration/test_repair_attest.py::TestHunklessDiffEntriesAreVisible::test_a_mixed_diff_names_every_path_that_exists_at_head
  tests/orchestration/test_repair_attest.py::TestHunklessDiffEntriesAreVisible::test_the_writers_own_round_trip_holds_for_an_added_empty_file

PASSING discriminator nodes (of TestHunklessDiffEntriesAreVisible, under the
mutation): test_a_deleted_file_is_still_absent_whether_or_not_it_had_hunks,
test_an_ordinary_modified_file_reads_exactly_as_before — at least one node
of the class stays green, satisfying the ordered property.

Worktree removed: git worktree remove .remedy-wt/f276-r13-mutation --force
git worktree list afterward:
  /home/decodeux/Repos/remedy                                  ba518b42 [feature/f276-data-root-hygiene]
  /home/decodeux/Repos/remedy/.remedy-wt/job-468c8e62a2cc4fac  1b9ae606 [remedy/job-468c8e62a2cc4fac]
  /home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968  fd23710f [remedy/job-c1dba9c3d7874968]
```
The reviewer's measurement (9 nodes, 5 failed / 4 passed under mutation) is
reproduced exactly.

**G4, G5, G6 — necessarily postdate this file.** The block's own Bundle
places the integrity check, the evidence job and the review package "AFTER
C4 and with the tree clean, and committing nothing," so none of the three
can be run before this file exists; all are reported in full, with real
output and exit codes, in the round report to the reviewer.

## Authored-text proofs

Five files copied via `shutil.copyfile`, each verified byte-identical to its
source payload immediately after copy (see G1(a) above): `.agent/authored/
f276-r13-block.md`, `-ledger.md`, `-plan.md`, `-prose-slips.md`,
`-ledger-done.md`. P5 and P6 get no `.agent/authored/` copy by the block's
own reasoned departure (§ "P5 AND P6 GET NO COPY"); their saved-copy proof
is G1(c)'s `git show <C2>:<path>` equality above instead. The record-append
fidelity for `.agent/live_review.md` at both C1 and C3 is proven in G1(b)
above by two independent readings plus a negative control at each commit;
the byte-equality readings for `.agent/prose_slips.md` and `.agent/plan.md`
are in G1(c).

## Open findings

By distinct id: 20 open at C1 (628ce362), immediately after R-1010's
registration — the full set carried from round 12 (19) plus R-1010 itself;
19 open at C3 (ba518b42), after R-1010's resolution — R-1010 is confirmed
NOT among the open set at C3. Both readings taken mechanically from
`.agent/live_review.md` at each commit (`- R-id` registrations minus
`Done: R-id` resolutions). The open set at C3: R-0499, R-0622, R-0662,
R-0819, R-0820, R-0829, R-0866, R-0880, R-0892, R-0950, R-0984, R-0998,
R-0999, R-1000, R-1004, R-1005, R-1007, R-1008, R-1009 — unchanged from
round 12 except for R-1010's net removal.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 the bookkeeping (5 payload copies + 2 appends + 1 rewrite) | done | commit 628ce362 |
| C2 the repair | done | commit ba4dd38f |
| C3 the resolution | done | commit ba518b42 |
| C4 the handoff | done | this file |
| G1 transport and state | done | 15 readings, all True |
| G2 the repair is confined and green | done | numstat confined; 9/153/All checks passed, all exit 0 |
| G3 the mutation red-proof | done | control GREEN (9 passed), mutated RED (5 failed/4 passed), worktree removed |
| G4 the integrity check | pending | runs after C4 per the block's Bundle; reported in the round report |
| G5 the evidence job and the base | pending | runs after C4 per the block's Bundle; reported in the round report |
| G6 the package, push and tree | pending | runs after C4 per the block's Bundle; reported in the round report |
| STATUS line, README edit, `consumed_by`, pull request | not done | explicitly out of scope for this round per the block's Goal — belongs to the closure round after this one |

## Deviations & assumptions

1. **G1(b)'s N differs between C1 and C3** — N=2 at C1 (P2 carries two
   paragraphs: the round-12 verdict and the R-1010 registration) and N=1 at
   C3 (P7 carries one paragraph: the `Done:` resolution). Both are counted
   mechanically from each payload as the block orders, not asserted from
   this block's prose.
2. **G2's and G3's readings were taken and reported in this handoff rather
   than deferred to the round report**, unlike G4/G5/G6 which the block's
   Bundle explicitly places after C4. G1, G2 and G3 all concern commits
   already made by C3 (C1 and C2), so nothing prevents running and
   recording them before C4 exists; doing so keeps the handoff's "every
   gate below with its real output and exit code" instruction as true as
   it can be at the moment this file is written, while G4-G6 remain
   physically impossible to report here for the same reason round 12's
   handoff declared.
3. **No `__pycache__` was found to purge** in the freshly-added G3
   worktree — declared rather than silently skipped, since constraint 5
   orders the purge unconditionally.
4. **Open-findings count is reported by both readings (20 at C1, 19 at
   C3)** as the block's C4 instruction orders, rather than a single count
   — declared here for clarity since round 12's handoff reported only one
   number (nothing having changed that round).

ANY DEPARTURE FROM THE BLOCK'S ORDERED COMMIT SEQUENCE BELONGS HERE: there
was none. The sequence executed is exactly C1, C2, C3, C4, in that order,
with no extra commit and none dropped or reordered. Whether anything after
C4 leaves a tracked file modified — which constraint 3 would make a
finding — is checked and reported in the round report's G6 reading.

## Next

Run, without committing anything: the integrity check (`python3 -m
apps.cli.main integrity check --json`), the evidence job (`python3
.remedy-wt/f276-r13/create_f276_evidence.py`), and the review package
(`bash scripts/make_review_zip.sh --evidence-dir
.remedy-wt/f276_evidence_closure`) from the clean tree at this commit. Push
the branch. Report every gate's real output, the package's filename,
SHA-256 and archived path to the reviewer, and write those four readings to
`.remedy-wt/f276-r13/package.txt`. The reviewer then authors the STATUS
line and DECISION F276 D11's closure round applies it, the README
paragraph and counters, `consumed_by`, the final `.agent/` state and the
pull request.
