
## DECISION F273 D8 (2026-09-19, reviewer, round 8) — the README lists and routed docs are pinned both ways, the review manifest says what it counted and who governs, the manual bundle's job report carries content, and a run prices and counts its own calls
CONTEXT: T013 (R-0570, R-0665, R-0752, R-0769), T011 (R-0666, R-0667, R-0668), R-0986 and the
R-0987 this round registers each needed a choice between routes their own texts allow, taken in the
round that lands the patch (amend0917-throughput rule 3). Measured by research helpers and
re-measured by the reviewer's dry run at `ec4e2e86`: the README's Tier 1, Tier 2 and Tier 5
accepted lists were 9, 10 and 1 ids short of `docs/roadmap/STATUS.md`, and F106 had a second entry
under Tier 5; 77 tracked docs named an `assumption_log` no tracked path contains; 14 feature files
named `tests/ui_contract/`, the 13 of R-0752 and T013's own description in `T2_F273.md`; the
review manifest's alignment counted the packaging's own untracked `.review_zip_manifest.json`; the
manual completion bundle wrote `job_report.json` as zero bytes while `artifact_contract_gate.py`
requires it and `fresh_evidence_gate.py` reads its `job_id`; and `run_job` priced a job only from
the ledger, only under a cost limit, and counted live tokens as zero.
CHOSEN: (1) R-0570 and R-0769. Every accepted STATUS id is an entry of the README list for its own
tier, entered by its STATUS title with no invented prose, and the misplaced Tier 5 F106 paragraph
is deleted rather than merged; two tests pin both directions, placement and uniqueness, reading
each list to the next heading. (2) R-0665. `docs/ui/design_reference/assumption_log.md` is created,
scoped to visual deviations from the design reference, and registered in `docs/README.md` and the
design reference's own README; rewording the 77 files is rejected because `docs/roadmap/ROADMAP.md`
names the log and may not be edited. A test holds the file and its index row while any doc names
it. (3) R-0752. The 13 files are substituted, T013's own description is reworded so it names the
plural path's singular form without spelling it, and a test forbids the singular path under
`docs/roadmap/features/`. (4) R-0666. The alignment counts the review subject's own dirty set, and a
new `dirty_files` list names every file its count counted. (5) R-0667. A top-level
`commit_execution_arbitration` key beside `ready_gate_matrix` carries the commit gate's verdict, the
matrix's `ok` and the rule: the ready gate governs package status, and `NEEDS_HUMAN_APPROVAL` means
the package is ready for a human who still approves any commit. `scripts/build_review_zip.py`
rebuilds the key where it rebuilds the matrix; that line has no red-proof, because the builder
already wrote an equal value from the same bytes. (6) R-0668. The job report is populated, not
dropped, because two gates read it; it carries only facts the manifest and `tasks.json` beside it
already carry. (7) R-0986, THE RULING. `run_job` keeps its own tally of the job's cost side: one row
per provider attempt the task-run evidence lists, fake ones included, each read by the ledger's own
`token_truth._strict_cost` on `total_cost_usd`, seeded from the persisted version-2 record. That is
the ledger's count taken earlier, not a second counting basis (R-0224, DECISION F104 D5). At each
safe point and at persist the money is whichever of the latest ledger read and this tally covers
more rows, taken whole and never added or mixed. A consequence taken on purpose: a `max_cost_usd`
limit now sees the current run's spend and can stop it before any mirror, which is what F104's
comment says the limit is for. (8) R-0987. The live counter reads the dict's `input_tokens` and
`output_tokens` as `int(ua.get(k, 0) or 0)`, the one definition `_aggregate_usage_actuals` uses,
cache tokens outside the total.
ALTERNATIVES: rewording 77 docs for R-0665, rejected above; stopping the job report write,
rejected because two gates read it; mirroring into the ledger before each persist for R-0986,
rejected because it exports the whole evidence at every save and needs a registered project;
adding the ledger and the tally, rejected as double counting.
REVERSE: restore `README.md`, `docs/README.md`, `docs/ui/design_reference/README.md`, the 14
feature files, `scripts/build_review_manifest.py`, `scripts/build_review_zip.py`,
`packages/orchestration/job_evidence.py` and `packages/orchestration/pingpong_job.py` from
`ec4e2e86`, delete `docs/ui/design_reference/assumption_log.md`, drop the tests this round added or
changed, and delete this paragraph.
