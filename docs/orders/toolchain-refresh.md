# Job: Refresh the pinned toolchain

Remedy's continuous integration installs an exact, hash-checked set of tools from
`constraints.txt`. Pinning stops a tool from changing under the test suite without warning, and
this order is how the pins move on purpose. Remedy's self-use track may turn this file into a
job no more than once every fourteen days. The job ends with a pull request for a person to
review. Nothing in it merges anything.

## Task 1 — Find the pinned tools that have a newer release

Run `remedy doctor toolchain`. For each tool it lists, compare the pinned version with the
newest version the package index knows. A tool whose newest version reads "unknown" could not be
checked; say so and leave its pin alone. Also compare the two Python versions the matrix in
`.github/workflows/ci.yml` runs with the oldest Python that `pyproject.toml` promises to support
and with the newest stable Python that GitHub's hosted runners offer.

Acceptance:
- The task's output lists every tool whose pin can move, with its pinned and its newest version.
- The task's output says whether either Python version in the CI matrix should move, and why.

## Task 2 — Read the release notes of every tool that moves

A model does not know from its training what changed in a release newer than that training.
Before anything is raised, fetch the release notes or the changelog of every tool Task 1 found,
for each version between its pin and its newest release, from the project's own pages. Put what
they say about removed features, changed defaults and new warnings into this job's context.

Acceptance:
- Every tool Task 1 found has its release notes quoted or summarized, with the address they were read from.

## Task 3 — Raise the pins and regenerate the constraints file

Raise the bounds in `pyproject.toml` only where a new major version is wanted, and keep the
`ruff==` pin in the `dev` extra equal to the version `constraints.txt` will pin. Then
regenerate `constraints.txt` with the command its own header records, changing only the
`--exclude-newer` date to today. Never edit `constraints.txt` by hand. When Task 1 found that
a Python version should move, change the matrix in `.github/workflows/ci.yml` in the same step.

Files:
- pyproject.toml
- constraints.txt
- .github/workflows/ci.yml

Acceptance:
- `constraints.txt` is exactly what its header command produces.
- `python3 -m pytest tests/orchestration/test_toolchain_pins.py tests/orchestration/test_ci_workflow.py -q` passes.

## Task 4 — Repair what the new versions break, and run the whole suite once

Install the new pins in a fresh virtual environment the way `.github/workflows/ci.yml` does,
then run the whole test suite once with `python3 -m pytest -n auto -q`. Repair each failure the
new versions cause, using what Task 2 found. Never delete a test, weaken an assertion or raise
a ceiling to make a failure go away.

Acceptance:
- One whole-suite run on the new pins exits 0, and its summary line is in the task's output.

## Task 5 — Open a pull request, only when the suite is green

When Task 4's run exited 0, open a pull request with the changes and the release-note summary
from Task 2 in its description. When it did not, open nothing and report what is still failing.
Do not merge the pull request: a person reviews and merges it.

Acceptance:
- A pull request exists only if Task 4's whole-suite run exited 0.
- Nothing was merged by this job.
