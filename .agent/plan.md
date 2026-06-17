# Plan — Steps 2616-2655: Simple Worker Onboarding + Mission Command Facade v0

## Goal
Make existing safe core easier to use. Worker add/doctor/disable facades +
mission run/report facades. Low-level commands stay available.

## Steps
- [x] Step 2616: Mainline gate + R-0151/R-0152 fix
- [x] Step 2617: UX audit
- [x] Step 2618-2619: Facade principles + alias registry
- [x] Step 2620-2622: worker doctor/add/disable
- [x] Step 2623: worker readiness — skipped, doctor covers it
- [x] Step 2624-2626: mission run/report/status facades (status skipped — report covers it)
- [x] Step 2627-2628: Fix self-repair command text + status values (R-0151/R-0152)
- [x] Step 2629-2630: Quickstart output + advanced field
- [x] Step 2631-2632: Catalog + contract
- [x] Step 2633-2634: CLI handlers + help text
- [x] Step 2635-2637: Docs
- [x] Step 2638-2644: Tests (27 facade + 6835 full suite) + lint + full suite
- [ ] Step 2645: Final handoff

## Hard rules
No auto-apply/approve/provider execution/shell=True/secret storage/raw leaks.
Facade only — calls existing safe rails.
