   A third, from the F052 BLOCKED_EVIDENCE attempt (caught by the
   packaging validator, fixed at authoring time): (c) the
   VerificationTests `run_id` must match `^vr-\d{4,}$`
   (`build_review_manifest._VT_RUN_ID_RE`) — a rejected
   VerificationTests document yields `vt_passed = None`, which
   fails the final-verifier confirmation.
