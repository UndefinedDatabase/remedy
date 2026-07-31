# ---------------------------------------------------------------------------
# Branch / main safety (Step 1433) — read the repo HEAD file only, no
# subprocess. Worktree-safe since the R-0159 fix: accepts both `.git` forms.
# ---------------------------------------------------------------------------


def _git_head_file() -> Path | None:
    """HEAD location for both repo forms: `.git` directory (normal
    checkout) or `.git` gitfile pointer (linked worktree, R-0159)."""
    dot_git = Path(".git")
    if dot_git.is_dir():
        return dot_git / "HEAD"
    if dot_git.is_file():
        try:
            text = dot_git.read_text(encoding="utf-8",
                                     errors="replace").strip()
        except OSError:
            return None
        if text.startswith("gitdir: "):
            gitdir = Path(text[len("gitdir: "):].strip())
            if not gitdir.is_absolute():
                gitdir = dot_git.parent / gitdir
            return gitdir / "HEAD"
    return None


def current_branch() -> str:
    """Return the current git branch from the repo's HEAD file, or ""
    if unknown/detached. No subprocess, no git invocation. Accepts a
    `.git` directory and a linked worktree's gitfile pointer (R-0159)."""
    try:
        head = _git_head_file()
        if head is None or not head.exists():
            return ""
        text = head.read_text(encoding="utf-8", errors="replace").strip()
        if text.startswith("ref: refs/heads/"):
            return text[len("ref: refs/heads/"):].strip()
        return ""  # detached HEAD → unknown
    except OSError:
        return ""
