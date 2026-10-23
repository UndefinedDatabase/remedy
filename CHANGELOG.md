# Changelog

All notable changes to Remedy are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and Remedy follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file is DATA the release gate reads: `packages/orchestration/release_gate.py`
refuses any release whose version has no section here, or whose section is empty.
Bumping the version in `pyproject.toml` without adding a section below therefore
fails the gate rather than shipping an unexplained release.

## [Unreleased]

### Fixed
- 2026-10-22, fix1022-review-findings, the orchestrator's review of F310 to F074; the public API and
  the client interface move to 1.28:
  - R-1422: a backup that serves with one call while the primary is held down is booked under its
    own provider and model, never the primary's.
  - R-1423: `budget.used.minutes` of a running job in `remedy client now` and `remedy client insight`
    is measured to now, not to its last safe point (contract 1.28).
  - R-1424: an `extend` without an answer on a deadline stop is refused `missing_argument` with the
    sentence that names the deadline answer.
  - R-1425: the mypy errors of the ten modules F310 to F074 added are repaired without a change of
    behaviour (440 to 410); the rest of the growth stays open for F314.

## [0.1.0] - 2026-08-20

### Added
- Remedy installs like a normal tool: a `pip install` of the wheel puts the
  `remedy` CLI on PATH with the built UI assets bundled (T2_F086 T001).
- `remedy --version` reports the distribution version, the revision embedded at
  build time, the Python version and the platform. A checkout with no embedded
  revision reports `dev` rather than inventing a sha (T2_F086 T002).
- A release gate that refuses on red CI, on a tag that does not match the
  distribution version, on a missing or empty changelog section, and on a wheel
  over its size budget (T2_F086 T003).
