# Module 4 - Production-Ready Backend

C2 - Specification-Driven Development & Automated Quality Engineering. **C2.4-C2.8; finalize C2.1/C2.2 | Completes C2.**

Implement the first specified feature test-first, then prove test quality, safe refactoring, CI gates and container behavior.

This is the optional TraceLens capstone track. Follow PromptLab's demonstrated methods independently; no TraceLens walkthrough is required. Continue your own repository rather than restarting from another starter.

## Work and evidence

1. Commit genuine failing tests before each first-feature increment; retain the red, green and refactor history.

2. Reach meaningful pytest-cov coverage of at least 80%; test endpoint success/failures, storage, utilities and validation.

3. Document a named refactor, before/after hashes and a green suite on both sides with unchanged public behavior.

4. Create push/PR lint/test/coverage CI. Keep actual success, deliberate failure and recovery evidence, plus required merge-check proof.

5. Build/run a backend Docker image and Compose development environment with hot reload; synchronize both specs and current documentation.

## Task detail

Implement one of your Module 3 specifications. Evaluations are recommended first, but alerts first is equally valid. For each meaningful increment, commit a test that actually fails for missing behavior, then its implementation. Preserve this order; do not squash or reconstruct evidence.

Use `python -m pytest tests --cov=app --cov-report=term-missing --cov-fail-under=80` from backend. Keep application coverage scope honest and add meaningful assertions for arithmetic, filtering, pagination, empty cases, storage and model validation. Test documented failures where defined; do not invent a failing health-check scenario just to satisfy a count.

Refactor only after the suite is green. In docs/refactor-note.md name the smell, commit hashes and green results before/after; preserve behavior and interfaces.

Create .github/workflows/ci.yml that installs committed dependencies, runs lint, tests and the 80% coverage gate on push and pull requests. Save real run URLs/logs in docs/ci-gate-evidence.md. Deliberately break a test on a branch to demonstrate failure, then restore it and show recovery. Configure and separately demonstrate a required merge check in your own repository; a workflow file alone is not merge protection.

Create backend/Dockerfile and docker-compose.yml (or compose.yaml). Build from committed files, serve the API, and demonstrate development hot reload. Explain startup, ports, origins, environment and reset behavior. Do not claim image-build success proves runtime success. Update the implemented feature's docs; keep the second feature explicitly planned for Module 5.

## Milestone review

Use the [Module 4 rubric](../rubrics/TraceLens_Module_4_Project_Rubric.pdf) and [full criterion text](../rubrics/CRITERIA.md). Update [EVIDENCE.md](../EVIDENCE.md), commit your real results and mark a milestone as described in [STUDENT_WORKFLOW.md](../STUDENT_WORKFLOW.md). No weekly capstone upload is required; all evidence feeds the final review. Tags are bookmarks, not passing grades.

Both tracks use the same Met/Not Yet standard, 80% coverage threshold and defense rules. Optional extensions carry no bonus credit. [ASSESSMENT.md](../ASSESSMENT.md) explains policy and MUST PASS returns.
