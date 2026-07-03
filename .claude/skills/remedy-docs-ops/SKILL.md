---
description: Use for Remedy documentation operations — adding, moving, renaming, or indexing docs. Enforces structure rules, cross-link repair, banner conventions, and README.md index registration.
---

# Remedy Docs Operations Skill

## Documentation Layout
```
docs/
  README.md          — master index (MUST be updated when docs change)
  system/            — 54 specs (built system descriptions)
  guides/            — 16 user guides, quickstarts, usage docs
  archive/           — 7 deprecated/future-only docs (DEPRECATED banner)
  roadmap/           — target plan (operator-only edits to ROADMAP.md)
    ROADMAP.md       — 150-feature masterplan
    00_INDEX.md      — feature file index
    CONVENTIONS.md   — shared naming register
    features/        — T{tier}_F{nnn}.md (150 files)
  ui/
    design_reference/ — visual mockups
```

## Categorization Rules
- **system/**: specs, design docs, contracts, architecture (no "user-guide" or "quickstart" in name)
- **guides/**: files with "user-guide", "quickstart", "usage" in name + do-run, do-continue, resume
- **archive/**: deprecated subsystems, future-only design notes

## When Adding a New Doc
1. Place in correct subdirectory (system/ or guides/)
2. Add entry to `docs/README.md` in correct table (file, one-line description)
3. Add to quick-find table if keyword is useful
4. Commit doc + index update together

## When Moving or Renaming a Doc
1. Use `git mv` (preserves history)
2. Fix ALL cross-references: `grep -r "old-name.md" docs/`
3. Cross-dir links use relative paths: `../system/foo.md`, `../guides/bar.md`
4. Update `docs/README.md` entry
5. Run link-fix script pattern:
   ```python
   # For each .md in docs/{system,guides,archive}:
   # Replace bare [text](filename.md) with [text](../targetdir/filename.md)
   # when filename.md lives in a different subdirectory
   ```

## Banner Conventions
- Archive docs: `> **Status: DEPRECATED** — This document describes a future plan or deprecated subsystem.`
- Overnight-superseded: `> **Status: SEMANTICS SUPERSEDED** — The overnight / time-of-day mechanics described here are explicitly deprecated by the roadmap.`
- Roadmap-replaced: `> **Status (roadmap):** Superseded by docs/roadmap/features/T?_F???.md`
- Banner goes right after the first heading, separated by blank line

## Boundary Rules (from AGENTS.md)
- `docs/` = IS (built state); `docs/roadmap/` = SHALL BE (target plan)
- On conflict: roadmap wins for planning; ist-doc stays correct + gets banner
- Agents MUST NOT edit `docs/roadmap/ROADMAP.md` unless operator explicitly requests
- Feature detail files (`docs/roadmap/features/`) change via normal PRs

## Language
- All new content in English
- Existing German docs (especially roadmap/) stay as-is unless asked to translate
