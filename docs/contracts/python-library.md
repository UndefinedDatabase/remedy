# Contract template — python-library

The floor of the contract for an order that builds a Python library. Every criterion below is part
of such a mission's contract, and the planner adds its own criteria on top; it never drops one of
these. The format is DECISION F269 D1's, and `remedy do --contract python-library` forces this
template.

## Proposed when the order mentions

- library
- python library
- python package
- sdk

## Criteria

- blocking: Every function and class the order names is importable from the package, and a test calls each one.
- blocking: The package installs, and a test imports it.
- blocking: The test suite passes.
- advisory: Every public function and class has a docstring.
- blocking: No file is added that nothing references.
  check: {"kind": "custom_cmd", "spec": {"argv": ["python3", "-m", "packages.orchestration.contract_hygiene", "unreferenced"]}, "description": "contract hygiene: unreferenced"}
- blocking: Code that is replaced is deleted in the same task, never left beside its replacement.
  check: {"kind": "custom_cmd", "spec": {"argv": ["python3", "-m", "packages.orchestration.contract_hygiene", "replaced"]}, "description": "contract hygiene: replaced"}
- blocking: No stub, placeholder or TODO body survives the job.
  check: {"kind": "custom_cmd", "spec": {"argv": ["python3", "-m", "packages.orchestration.contract_hygiene", "stubs"]}, "description": "contract hygiene: stubs"}

## Fixture order

Build a Python library that parses and formats ISO 8601 durations.
