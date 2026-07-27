- Exception: a diff over 500 lines is acceptable only when (a) the worker
  declares it in the handback WITH the inseparability reason before
  review, and (b) it is the only such commit in its feature. An
  undeclared oversize commit, or a second one in the same feature, is a
  finding (Medium). "Accepted, not a precedent" may appear at most once
  per feature — by construction.
