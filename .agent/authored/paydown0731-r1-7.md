# ---------------------------------------------------------------------------
# current_branch() repo forms (R-0159) — .git directory vs worktree gitfile
# ---------------------------------------------------------------------------


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                   text=True, check=True)


class TestCurrentBranchRepoForms:
    """R-0159: a linked worktree's `.git` is a gitfile pointer, not a
    directory — current_branch() must resolve HEAD in both forms."""

    @pytest.fixture()
    def repo(self, tmp_path) -> Path:
        r = tmp_path / "repo"
        r.mkdir()
        _git(r, "init", "-q")
        _git(r, "config", "user.email", "t@e.com")
        _git(r, "config", "user.name", "T")
        _git(r, "config", "commit.gpgsign", "false")
        (r / "a.txt").write_text("v1\n")
        _git(r, "add", "-A")
        _git(r, "commit", "-qm", "init")
        _git(r, "checkout", "-qb", "feature/primary")
        return r

    def test_git_directory_form(self, repo, monkeypatch):
        monkeypatch.chdir(repo)
        assert SE.current_branch() == "feature/primary"

    def test_worktree_gitfile_form(self, repo, monkeypatch):
        wt = repo.parent / "wt"
        _git(repo, "worktree", "add", "-q", "-b", "feature/linked",
             str(wt))
        monkeypatch.chdir(wt)
        assert (wt / ".git").is_file()  # the R-0159 precondition
        assert SE.current_branch() == "feature/linked"

    def test_detached_head_unknown(self, repo, monkeypatch):
        _git(repo, "checkout", "-q", "--detach")
        monkeypatch.chdir(repo)
        assert SE.current_branch() == ""

    def test_no_repo_unknown(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        assert SE.current_branch() == ""
