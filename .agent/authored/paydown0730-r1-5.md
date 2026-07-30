   Two more, from the F051 BLOCKED_EVIDENCE attempt (both caught by
   the packaging validator — catch them at authoring time instead):
   (a) verification records must carry non-empty test node ids with
   `len(node_ids) == selected` (run `--collect-only` for real ids);
   (b) `test_files` entries are files, never directories (expand
   `tests/docs/` to the actual file paths).
