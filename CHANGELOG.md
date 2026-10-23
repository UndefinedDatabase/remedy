# Changelog

All notable changes to Remedy are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and Remedy follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file is DATA the release gate reads: `packages/orchestration/release_gate.py`
refuses any release whose version has no section here, or whose section is empty.
Bumping the version in `pyproject.toml` without adding a section below therefore
fails the gate rather than shipping an unexplained release.

## [Unreleased]

### Added
- 2026-10-23, amend1023-universe-trust; the public API and the client interface move to 1.29:
  - The client property `host_tools`, granted and revoked only on this machine's command line
    (`remedy client grant-host-tools`, `revoke-host-tools`, `show`): a client holding it may name
    `claude-cli` as builder and reviewer and choose the planner over HTTP; the call ledger marks
    every call naming `claude-cli` with `host_tools=true`.
  - `GET /api/v1/orders/{order}/story` (`remedy client order-story`): an order's missions,
    milestones and jobs in closed words, with who gave it; the order poll's jobs carry
    `mission_id` and `blocking_criterion`.
  - Small orders stay small: `shape: single-job` in an order's header, or an order naming exactly
    one file, is one job without milestones; a planned criterion demanding a file nobody named is
    removed and named in the story's `scope_findings`; an order saying "no new documentation
    files" gets that criterion, and a new file outside the named ones leaves the result.

### Changed
- 2026-10-23, amend1023-universe-trust: F133's format-error rate also reads the post-mortems under
  the task's run directory; the worker list names its adapters honestly and `remedy worker show
  --json` carries the capabilities; the conformance kit fails a class whose source it cannot read
  and reads the module functions a class calls; the contract page is
  `docs/system/worker-adapter-contract-v2.md`.

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
