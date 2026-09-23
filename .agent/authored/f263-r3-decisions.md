
DECISION F263 D3 (2026-09-23, round 3) — RUFF DOES NOT LINT `.agent/authored/`: THE TRANSPORT
COPIES ARE RECORDS, AND THE FILES THEY WERE APPLIED TO ARE LINTED WHERE THEY LIVE.

CONTEXT. Finding R-1042. Measured by the reviewer at `0e2e04ef`: `.agent/authored/` holds 40
Python files, every one a byte-verbatim copy of a payload some round applied, committed before
the payload is applied and never edited afterwards (docs/agents/self_drive_protocol.md, Phase 2
step 1). `ruff check .` lints them because `pyproject.toml`'s `extend-exclude` names no `.agent`
path, so one lint defect in a payload is carried into a record that cannot be repaired, and CI's
`budgets` stage, which requires zero findings, stays red for as long as the record exists.

CHOSEN. (1) `.agent/authored` joins `extend-exclude` in `pyproject.toml`, with a comment giving
the reason. (2) Nothing else in `.agent/` changes status: no other directory there holds Python.
(3) Every applied file is still linted at its own path, and every block's own ruff gate names
the applied paths, so the exclusion removes a second reading of the same bytes and nothing else.

ALTERNATIVES. Rewrite the landed copy — rejected: the copy is the transport proof, and changing
it would make every later disk-to-disk comparison of that round false. Add a `per-file-ignores`
entry for `F401` alone — rejected: the next payload defect would be another rule. Store payload
copies under a non-Python suffix — rejected for landed rounds, which would stay red, and left
open for later rounds as a convention change.

REVERSE by deleting this paragraph and the `.agent/authored` entry with its comment from
`pyproject.toml`.
