# Plan — F278 Durable writes & loud failures

Branch: feature/f278-durable-writes-loud-failures, cut from `main` at
`9817a927`, the merge commit of pull request 265 (F283's closure).

## Goal

One durable write in this repository, used everywhere, and no artifact that is
silently incomplete (`docs/roadmap/features/T2_F278.md`).

## Current Step

ROUND 1 claims F278, re-heads the review record and lands T001:
`durable_write` and `durable_write_json` in `packages/common/secure_fs.py`,
which fsync the file and the parent directory, use an unpredictable temporary
file in the destination directory, and unlink it on every failure path; with
`tests/orchestration/test_secure_fs_durable_write.py` and both red proofs.

## Next Steps

1. T002, the migration: re-derive the surviving private atomic-write helpers
   from the tree, replace each with an import of `durable_write` and delete
   it, one module per commit, keeping each call site's return-type contract.
2. T002's AST guard: no function named `_?atomic_(private_)?write` outside
   `packages/common/`, with its red proof.
3. T003, loud failures: BLE001 enabled with a frozen ignore list, the nine
   handlers in `stream_evidence.py` first, a `degradations` field on the
   stream artifact, and a reason on every remaining ignored site.
4. The closure sequence.

## Risks

`os.replace` of a directory entry and the directory fsync are POSIX
behaviour; the helper fails loudly rather than silently where either is
refused.
