Target: tests/docs/test_docs_consistency.py
Operation: replace FROM with TO. FROM occurs exactly 1x (verify first).
Shape: APPEND — the TO contains the FROM verbatim. Proof obligation is
FROM 1x plus the TO-only method 1x. Do NOT claim FROM 0x.
This pin and the AGENTS.md / docs/README.md count fixes land in the SAME
commit (planner_reviewer_prompt.md §3, R-0151).

FROM
<<<FROM
    def test_no_doc_still_claims_150_feature_files(self):
        offenders = [
            str(p.relative_to(REPO)) for p in PRIMARY_DOCS
            if p.is_file() and re.search(r"150[- ]feature|150 feature detail",
                                         p.read_text(encoding="utf-8"))
        ]
        assert offenders == [], offenders
FROM>>>

TO
<<<TO
    def test_no_doc_still_claims_150_feature_files(self):
        offenders = [
            str(p.relative_to(REPO)) for p in PRIMARY_DOCS
            if p.is_file() and re.search(r"150[- ]feature|150 feature detail",
                                         p.read_text(encoding="utf-8"))
        ]
        assert offenders == [], offenders

    def test_no_doc_understates_the_feature_count(self):
        """R-0209: AGENTS.md and the docs index described a 250-file roadmap.

        The ledger has been TOTAL_FEATURES long since F251-F255 were
        registered, and the 150 pin above did not cover the successor
        claim, which is why it survived. Pinned by document rather than
        by regex over PRIMARY_DOCS on purpose: README.md's "250 features
        + registered items" is a different and still-true statement,
        and a blanket pattern would force a false repair on it.
        """
        for rel in ("AGENTS.md", "docs/README.md"):
            text = (REPO / rel).read_text(encoding="utf-8")
            assert "250 feature detail files" not in text, rel
            assert "250-feature" not in text, rel
TO>>>
