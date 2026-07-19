# Plan — Steps 13361-13560 — F012 hardening round 29 (SYSTEMIC CLASS CLOSURE)

## Round 29 binding decision

Reviewed `remedy-review-20260719-134026-READY_FOR_REVIEW.zip`
(SHA `6d1a28a7...e9712`, Evidence `be06ea70dd607523`, linked prior `a3d937ec1835eb93`,
Base `8c32724`, HEAD `925c6fa`). Verdict FINDINGS. Round 28 fixed the narrow reproductions but did
not close the complete error classes. Round 29 closes each class systemically, not by example patch.

Five non-overlapping scopes, each its own commit:

1. **Exact token producer re-derivation** — one shared pure module
   `packages/orchestration/token_measurement.py::token_measurement_summary(token_status)` is the SOLE
   authority, imported by both `final_verifier.py` and the review gate. The gate computes
   `expected = token_measurement_summary(token_status)` and requires deep equality with
   `token_measurement` plus exact equality of the top-level projections
   (`token_measurement_confidence`/`token_measurement_note`/`token_actual_summary`). Deletes the
   hand-duplicated projection-field lists so no list can drift from the producer. Evidence is
   regenerated through the real producer (no hand-edited note). Scope: new module + `final_verifier`
   import alias + `_gate_semantic_problems` token block + the two dead projection constants.
2. **Complete manual-completion nested-shape safety** — one typed pre-consumption normalizer validates
   every trust-bearing collection/record field consumed by `validate_manual_completion` and its
   `_verify_*` helpers before any iteration or `.get` chain. Wrong types append a bounded
   `artifact: field is not a <kind>` error and normalize to a safe empty; nothing downstream operates
   on an unvalidated collection. Scope: `_mc` shape table + `_read_mc` + the `_verify_*` signatures.
3. **Internally-derived generated-output identity + collision safety** — the classifier filters any
   supplied generated set through an eligibility gate (repo-ROOT path; exactly
   `.review_zip_manifest.json` or the `remedy-review-…zip` output form), so an arbitrary source path a
   caller names can never be dispositioned. `build_review_zip.py` DERIVES the set from its own
   `--out`/`--manifest-rel` (not a trusted free list) and records it. `make_review_zip.sh` stops
   passing the non-existent `.sha256` sidecar and REFUSES to delete/reserve a TRACKED manifest/ZIP
   path. Scope: `_eligible_generated_output` + classifier filter + coordinator derivation + shell
   collision guard.
4. **Correct NUL-safe Git porcelain path identity** — `_dirty_files()` uses
   `git status --porcelain=v1 -z` and preserves the two status columns exactly (no record `.strip()`);
   `_dirty_line_path` takes the path from column 3 without dropping a leading status char and handles
   rename/copy `->`/`-z` origin pairs. Scope: `_dirty_files` + `_dirty_line_path` + `_has_untracked`.
5. **Hermetic stream-export E2E** — the copied-pipeline subprocess receives an intentional
   `PYTHONPATH=<repo root>` env; a regression clears any inherited path first. No shell/ZIP assertion
   weakened. Scope: the one fixture test.

6. **Truthful Round-29 documentation + operator state** — T0_F012 Round-29 section, the pinned
   consistency test, corrected Round-28 over-claims (present-tense "F012 is accepted" → "may be
   accepted only after external review confirms…"), plan/live-review.

## Constraints (unchanged)

No provider calls; no Evidence job-flow/job-run; no database; no LLM rerun; no network; no Fable; no
subagents; no Docker; no new dependency. Manual operator work only. Small local commits, never amend/
squash prior rounds. Do not push, PR, merge, or begin F017. Fresh Evidence linked `be06ea70dd607523`;
one READY_FOR_REVIEW ZIP; then stop. Preserve every accepted F012 behavior, including Round 28's
externally-verified VerificationTests corrections. F012 stays `[~]`, F017 stays `[ ]`, pending
external acceptance.
