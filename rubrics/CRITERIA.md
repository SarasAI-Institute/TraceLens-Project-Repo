# TraceLens Criterion Set v1.1

Current course Modules 2-6. This is the canonical text reproduced in the module PDFs. It adapts the supplied TraceLens v1.0 rubric to the published PromptLab course workflow; changes are recorded in [ALIGNMENT.md](../ALIGNMENT.md). The Syllabus governs policy; [ASSESSMENT.md](../ASSESSMENT.md) summarizes final review.

All 22 criteria must be Met, with no averaging. MUST PASS: C1.4, C2.4, C2.7, C3.3, C3.6. C2.1/C2.2 are provisional in Module 3, finalized in Module 4 and maintained thereafter. No weekly capstone upload is required.

## C1.1 — Your system model is accurate

**Evidence:** docs/SYSTEM_MODEL.md

**Met:** Correctly identifies every route the app exposes, the request-to-storage-and-back data flow, the project/trace relationship, where and how per-call cost is computed, how the storage layer works, and every external dependency. Nothing in the document contradicts the code.

**Common mistakes:**

– Describing what the AI said the code does rather than what it does.
– Missing a module or dependency.
– Listing file names without explaining behaviour.

## C1.2 — You justify your context strategy

**Evidence:** docs/SYSTEM_MODEL.md, context strategy section

**Met:** States, for each stage of exploration, whether you used whole-repo or file-level context, with a reason based on the size or coupling of the code.

**Common mistakes:**

– Not stating which approach you used.
– A reason that doesn't match your prompt log.
– Whole-repo context throughout with no rationale.

## C1.3 — Your prompt log shows real iteration

**Evidence:** docs/prompt-log.md

**Met:** At least two iterations where you narrowed context, added a constraint, or restructured a prompt because the output wasn't good enough — with your reasoning recorded.

**Common mistakes:**

– One successful prompt and nothing else.
– Prompts listed with no outputs or reasoning.
– Rewording without changing context or constraints.

## C1.4 — Every ticket is closed - MUST PASS

**Evidence:** Repository; pytest tests/ -v output

**Met:** All 5 defects fixed — TL-1: 404 on a missing trace; TL-2: cost correct per million tokens, verified against a hand calculation; TL-3: pages contain at most limit items (short last pages and empty pages past the end are valid) and total is the full filtered count; TL-4: a project with no traces returns zeroed stats instead of a 500; TL-5: orphaned traces handled with your chosen strategy recorded — and TL-6: PATCH /projects/{id} implemented with partial updates, timestamp update and 404 handling. All provided tests pass and nothing that worked before is broken.

**Common mistakes:**

– A ticket still open.
– Changing the test's expected cost instead of fixing the unit conversion.
– Hiding the stats crash behind a try/except instead of handling the empty case.
– Fixing the page size but leaving total wrong, or the reverse.
– PATCH implemented but requiring all fields.
– A fix that breaks something that worked before.

## C1.5 — You caught the AI being wrong

**Evidence:** docs/ai-verification-note.md, traceable to docs/prompt-log.md

**Met:** At least one specific case of wrong AI output: what it produced, why it was wrong, how you spotted it, what you did instead. The case appears in your prompt log.

**Common mistakes:**

– General comments about AI limitations with no actual example.
– An example that's just a syntax error your editor would have caught.
– An example not traceable to the log.

## C1.6 — Your documentation is accurate

**Evidence:** Docstrings on functions you modified; README run instructions

**Met:** Every function you modified or added has a Google-style docstring whose Args, Returns and Raises match the implementation. README run steps work on a clean clone.

**Common mistakes:**

– Docstrings listing parameters that don't exist or omitting ones that do.
– README steps that fail on a fresh machine.
– Docstrings restating the function name as a sentence.

## C2.1 — Your specs are specific enough - Provisional until Module 4

**Evidence:** specs/evaluations.md, specs/alert-rules.md

**Met:** Each spec has overview and goals, user stories with acceptance criteria, data model changes, API endpoints with request and response shapes, and specified error conditions and edge cases. Every endpoint has at least one acceptance criterion you could write a test from directly.

**Common mistakes:**

– Requirements that name a feature without describing behaviour.
– Specifying the happy path and leaving errors unstated.
– Criteria you can't test, like “handles input correctly”.

## C2.2 — Your docs match your code - Provisional until Module 4

**Evidence:** README.md, docstrings in models.py / api.py / storage.py / utils.py, docs/API_REFERENCE.md

**Met:** Docstrings on every function and class across all four source modules, with parameters, returns and exceptions matching the implementation. API reference documents every endpoint that exists — including PATCH and your Module 4 feature — with request examples, sample responses and error formats. README setup steps work on a clean clone.

**Common mistakes:**

– API reference describing an earlier draft of the spec.
– Docs not updated after Module 4's feature work.
– Setup steps missing an environment variable or dependency.
– Docstrings that restate the function name.

## C2.3 — Your agent instructions do something

**Evidence:** AGENTS.md or CLAUDE.md; docs/agent-effect-note.md

**Met:** The file states standards specific to TraceLens — its patterns, naming, error handling, testing expectations. The note shows one concrete before-and-after case where generated output changed because of it.

**Common mistakes:**

– Generic best-practice advice that would suit any project.
– No evidence it affected any output.
– Standards in the file that your own code contradicts.

## C2.4 — Your tests came first - MUST PASS

**Evidence:** Commit history for your Module 4 feature

**Met:** For each part of the feature, a commit containing a failing test precedes the commit containing its implementation. The Red-Green-Refactor rhythm is visible.

**Common mistakes:**

– All tests in one commit after the code.
– Squashed history, so ordering can't be seen.
– Tests committed first that assert nothing capable of failing.

## C2.5 — Spec, tests and code line up

**Evidence:** tests/, coverage report, specs/

**Met:** Coverage at least 80% measured with pytest-cov across application code. Every implemented endpoint in your specs and API reference has meaningful passing success tests and documented failure-case tests where a failure is defined. Storage, utilities (including cost, pagination and stats) and model validation are covered. Planned second-feature endpoints are tested when implemented in Module 5.

**Common mistakes:**

– Endpoints built but not tested, or tested but not specified.
– Coverage reached by tests that run code without asserting anything.
– Failure cases specified but never tested.

## C2.6 — Your refactor changed nothing visible

**Evidence:** docs/refactor-note.md, before/after commits

**Met:** A named code smell removed, the two commit hashes given, suite green on both sides, public interface and observable behaviour unchanged.

**Common mistakes:**

– Not naming the smell, or fixing something other than the one named.
– Changing behaviour at the same time.
– Editing tests to accommodate the refactor instead of using them to check it.

## C2.7 — Your pipeline actually gates - MUST PASS

**Evidence:** .github/workflows/ci.yml, run logs, docs/ci-gate-evidence.md

**Met:** Triggers on push and pull request, runs linting and tests with coverage, fails the build below 80%, passes on a clean clone, and demonstrably fails when a test is deliberately broken. Keep recovery evidence after restoring the test. Prove the required merge check separately in your repository settings.

**Common mistakes:**

– A workflow file with no successful run recorded.
– A pipeline that runs tests but doesn't fail the build when they fail.
– Passing locally but failing on a clean clone because config was never committed.

## C2.8 — Your container builds and runs

**Evidence:** backend/Dockerfile, docker-compose.yml, build output

**Met:** The image builds from committed files with no manual steps. The container serves the API. docker-compose up --build brings up a working local environment, and the README explains Docker usage. Demonstrate local hot reload through the Compose development configuration.

**Common mistakes:**

– An image that builds but a container that exits or serves nothing.
– A Dockerfile depending on files not in the repository.
– A build needing undocumented manual steps.

## C3.1 — Your structure follows your spec

**Evidence:** specs/frontend.md, frontend/src/

**Met:** The frontend specification is committed before implementation. Every component in your frontend spec exists as its own module, and you can state the organizing principle of your folder structure in one sentence. Backend and frontend concerns stay separate.

**Common mistakes:**

– Vite template directories left in unused.
– Specified components missing or merged with no explanation.
– Concerns tangled across modules.

## C3.2 — Your backend increment was built test-first

**Evidence:** Commit history for your Module 5 feature; test run against deployed config

**Met:** The second spec feature, and any endpoints your frontend needs, show a failing test before implementation in commit history. The suite passes against your deployed configuration, not just locally.

**Common mistakes:**

– Tests added once the feature was finished.
– A suite that passes locally but not against the deployed config.
– Tests that exercise FastAPI rather than your own logic.

## C3.3 — Your app runs end to end - MUST PASS

**Evidence:** Deployed app or documented container run; frontend/, backend/

**Met:** The deployed application completes its core journeys: dashboard showing real per-project stats, create a project, rename it, delete it with confirmation and your orphaned-trace strategy visibly applied, browse traces filtered by project, model and status, search, paginate with correct page counts, open a trace's detail, and use both evaluations and alert rules end to end. The frontend consumes your real API. Loading and empty states present, and API failures produce visible user-facing messages.

**Common mistakes:**

– A frontend running on mocked or hard-coded data.
– A core journey breaking partway through.
– A pager that still shows the wrong number of pages.
– API errors producing a blank screen or nothing at all.

## C3.4 — Someone else could deploy it

**Evidence:** docs/deployment.md, committed configuration

**Met:** A second person can deploy or run TraceLens using only what's committed. Every step, environment variable and secrets-handling approach is documented.

**Common mistakes:**

– Deployment relying on something you configured by hand and never wrote down.
– Instructions missing environment variables.
– Only a running instance, with no reproducible path to it.

## C3.5 — You worked inside the time budget

**Evidence:** Commit timestamps for the Module 5 backend increment

**Met:** Record genuine commits from scaffolding the Module 5 backend increment to its first passing new endpoint, plus the advance plan and blockers. The original four-hour figure is unvalidated: timing-based Not Yet requires pilot calibration, a published budget and a criterion-version update. Pending calibration is not automatic Met. The interval does not cover the entire application.

**Common mistakes:**

– Going over with no blocker documented.
– Committing everything in one batch, so timestamps prove nothing.
– Committing unfinished work to hit the time and finishing later.

## C3.6 — You can explain the code we pick - MUST PASS

**Evidence:** Recorded defense, responding to the issued prompt set

**Met:** For the instructor-selected backend function and React component at your final commit, explain what each does, why it is structured that way, and what would break if a specified part were removed. Use actual code and substantive reasoning, not a substitute selection.

**Common mistakes:**

– Reading the code aloud or paraphrasing your own comments.
– Steering toward code you know better.
– Not being able to say what a function you submitted is for.

## C3.7 — You can trace a request

**Evidence:** Recorded defense

**Met:** You follow one user action from the frontend event, through the API call, the backend handler and the storage layer, and back to what renders — naming the actual components in your repository.

**Common mistakes:**

– Stopping at the API boundary.
– Describing layers in general architectural terms rather than in your app.
– Not being able to find where the request is handled in your own repo.

## C3.8 — You evaluate AI honestly

**Evidence:** Recorded defense and written follow-up

**Met:** At least one time you overrode or rejected AI output and why, and one specific incident in this build where AI was wrong or unhelpful and what it cost you. Both traceable to your prompt log, commits or verification note.

**Common mistakes:**

– General commentary about AI's strengths and weaknesses.
– Saying you never disagreed with it.
– Incidents not traceable to this project's history.
