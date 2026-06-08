---
description: Work on Proof Chain truth and file provenance
---
Work on Remedy Proof Chain/file provenance.

Checklist:
- `verified` requires linked approval + apply + proof + passed/not-required linked test.
- Generic sole-change tests require parsed test time >= parsed apply time.
- Multi-change generic tests do not verify, even under `--path` filtering.
- `file why` must not show unlinked/global tests as proof.
- `file why` and `change proof --path` must agree on `proof_status`.
- Use `scripts/remedy_pytest.sh` for tests.
