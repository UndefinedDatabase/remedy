# F312 round 2 — amendment 1 (the reviewer's ruling on the stop after C3)

The stop after C3 was right, and the reviewer rules on it. The red test
`tests/cli/test_plan_approval.py::TestTaskPlanLabel::test_llm_plan_holding_an_inspection_task_is_rejected`
pins DECISION F268 D6, the one validator refusing an inspection-only plan with no job saved. Its
order, `test mission`, names no file and draws no fence, so it is an open order, and DECISION
F312 D3 deliberately gives an open order a second attempt and then a question. F268 D6's rule still
holds for the two kinds that are refused at once, and that is what this test keeps pinning.

1. In C4, beside the new file, that test's call `_shape_order(repo, "test mission")` becomes
   `_shape_order(repo, "Write notes.md about the repository")`, and its docstring becomes
   `"""DECISION F268 D6: the one validator runs on the LLM plan too, for an order that names a file (an open order is planned twice and then asks, DECISION F312 D3)."""`.
   Nothing else in it changes: its `pytest.raises(..., match="is inspection")` and its
   `assert list_job_plans() == []` stay byte-identical. Confirm before the commit that the new order
   is of the kind `names_files`.
2. Do not amend, rebase or rewrite any commit from here on, pushed or not; a fix a later check
   asks for is a stop and a report. C2 and C3 stay as they are now.
3. C6's paths are `.agent/handoff.md` and `.agent/authored/f312-r2-amend1.md` (NEW FILE), a
   Python byte copy of this file; the handback reports its line count and sha256. The handback's
   deviations name the two amended local commits of C2 and C3 and the line of `_cmd_do_order`
   C2 joined, and `## Next` adds, after "book round 2's verdict", "and the DECISION F312 D3
   addendum naming the test amendment 1 changed".
4. Then continue the block from C4 exactly as it stands: C4, C5, the six gates, C6, the push.
