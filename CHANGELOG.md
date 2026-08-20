# Changelog

All notable changes to Remedy are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and Remedy follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file is DATA the release gate reads: `packages/orchestration/release_gate.py`
refuses any release whose version has no section here, or whose section is empty.
Bumping the version in `pyproject.toml` without adding a section below therefore
fails the gate rather than shipping an unexplained release.

## [Unreleased]

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
