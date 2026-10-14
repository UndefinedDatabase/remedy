# F055 round 2 — amendment 1

The block did not name `tests/test_ble001_ratchet.py`, which freezes the count of excused blind
handlers, and its summary template left the unit of an unavailable whole-job figure open. Both
are the reviewer's slips. C1 to C3 stand as committed; add one commit and renumber the handback.

1. NEW C4 — `F055 R2 C4: the head reader names its exceptions, and an unavailable whole-job estimate reads without a unit`
   Paths: `packages/orchestration/do_rehearsal.py`,
   `tests/orchestration/fixtures/rehearsal/golden/rehearsal.md`,
   `tests/orchestration/test_do_rehearsal.py`, `.agent/authored/f055-r2-amend1.md` (a Python byte
   copy of this file, its sha256 reported).
   - `_rehearsal_repo_head` catches exactly `(OSError, subprocess.SubprocessError)` and carries no
     `# noqa: BLE001`; the ratchet's count stays 285.
   - The whole-job line reads `Whole job: <low>–<high> USD. Basis: <basis>.` when both bounds
     exist, and `Whole job: not available. Basis: <basis>.` otherwise.
   - The golden file is regenerated from `render_rehearsal_summary` and changes in that line
     only; `test_do_rehearsal.py` gains a test that renders a priced whole job and reads the
     `USD` form, so both forms are held.
2. The handback becomes C5 — `F055 R2 C5: handback` — with every obligation the block gave C4;
   its item-status table gains a row for this amendment's C4.
3. Gates 1 to 6 run once each after the new C4 and before C5. Gate 3 runs ONCE more, now: its
   first run, before the new C4, read `1 failed, 3507 passed, 3 skipped`, the one failure
   `tests/test_ble001_ratchet.py::test_the_count_of_excused_handlers_never_rises` at 286 excused
   handlers; the handback reports that reading too. Gate 2 also lints
   `tests/orchestration/test_do_rehearsal.py` as before.
4. `verify.py` is replaced by the version whose digest the prompt gives.
