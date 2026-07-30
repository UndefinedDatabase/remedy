    def test_the_readme_accepted_count_equals_the_status_count(self):
        """R-0156: pin the README accepted-COUNT to the STATUS ledger.

        The id cross-check above verifies every README-listed feature
        IS accepted, but the prose line "N of 252 registered items
        accepted" could carry any N (negative control: a faked count
        stayed green through all of tests/docs). Parse both counts
        and pin them equal.
        """
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        status = STATUS.read_text(encoding="utf-8")
        m = re.search(r"^(\d+) of (\d+) registered items accepted\.",
                      readme, re.MULTILINE)
        assert m, "README must state 'N of M registered items accepted.'"
        assert int(m.group(2)) == TOTAL_FEATURES
        accepted = len(re.findall(r"^- \[x\] F\d{3} — ", status,
                                  re.MULTILINE))
        assert int(m.group(1)) == accepted, (
            f"README claims {m.group(1)} accepted; STATUS.md has "
            f"{accepted}")
