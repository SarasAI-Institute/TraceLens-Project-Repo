# Starter diagnostics

Run `python -m pytest tests -v` from `backend` after installing `requirements-dev.txt`.

Verified release baseline on Python 3.12: **20 passed, 9 failed** across 29 checks. The nine failures cover TL-1, TL-2, both TL-3 symptoms, TL-4, TL-5 and three TL-6 cases. Third-party deprecation warnings do not represent additional ticket failures.

The supplied tests deliberately expose TL-1 through TL-6. They must become green through repairs, not skips, xfails, weaker assertions or reconstructed history. The TL-5 check accepts any documented cascade/detach/reject strategy and checks for dangling references. PATCH diagnostics assert desired behavior even though the route is initially absent.

An import/dependency error, zero collected tests or a server that never starts is **not** an expected ticket failure. Record your actual baseline output before repairs. Extend the diagnostics with boundary cases, combined filtering, unknown-model cost, failed-update atomicity, deletion relationships and your feature contracts. These tests do not constitute the full assessment.

In Module 4, add meaningful storage, utility, model and endpoint tests. Run `python -m pytest tests --cov=app --cov-report=term-missing --cov-fail-under=80`, then wire the same gate plus lint into your own CI. Do not change coverage scope to hide untested application code. Preserve genuine failing-test/implementation commits.
