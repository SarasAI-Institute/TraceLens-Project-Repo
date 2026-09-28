# TraceLens - optional capstone starter

**AIE 500 | 10x Coding with AI | Modules 2-6**

Choose **TraceLens instead of PromptLab** if you want a more challenging domain. You build an LLM observability and evaluation application: projects contain traces of model calls, with token counts, cost, latency and errors. The course videos demonstrate PromptLab; there are no TraceLens walkthrough videos. Apply the same methods to this codebase independently.

Both tracks assess the **same 22 criteria and three competencies**, with the same mastery rules. TraceLens changes the defects, features and user journeys, not the grading threshold. Module 1's ungraded TokenScope activity remains common to both tracks. Choose one capstone before Module 2 and keep it through the final defense.

## Start here

1. Create your own copy following [STUDENT_WORKFLOW.md](STUDENT_WORKFLOW.md).
2. Run the backend and its diagnostic tests below.
3. Read [Module 2](milestones/module-02.md), [CONTRACT.md](CONTRACT.md) and the [rubric PDFs](rubrics/README.md) before making repairs.
4. Keep authentic prompts, checks and commits in [EVIDENCE.md](EVIDENCE.md) as you work.

Use one repository across the course. **No weekly capstone upload is required.** Prepare evidence at each milestone; submit the final repository, evidence and recording through the course channel. [ASSESSMENT.md](ASSESSMENT.md) defines review and defense requirements. [COMPETENCY_MAP.md](COMPETENCY_MAP.md) compares the two tracks.

## Local setup

Use Python **3.12**, Git and your local editor. Use the course's Codex or Claude workflow with your own account. No Codespaces, dev container, Continue configuration, shared API key or model-provider account is required to run TraceLens. Node.js is needed only when you build React in Module 5; use a supported LTS version compatible with your chosen Vite release and record it. Docker is introduced in Module 4.

From the root of your own cloned repository:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements-dev.txt
cd backend
python main.py
```

On Windows PowerShell, create the environment with `py -3.12 -m venv .venv`, then activate it with `.\.venv\Scripts\Activate.ps1`. If your shell disallows activation, run `.\.venv\Scripts\python.exe` directly from the root with `-m pip install -r backend/requirements-dev.txt`; then run `..\.venv\Scripts\python.exe main.py` from `backend`.

Open http://127.0.0.1:8000/health and http://127.0.0.1:8000/docs. The server reloads when Python files change. Stop it with Ctrl+C. Run it from `backend` so `app` imports resolve.

Defaults require no environment file. `.env.example` lists `HOST`, `PORT` and `ALLOWED_ORIGINS`; it is a reference and is **not automatically loaded**. Export values in your shell before starting if needed (PowerShell: `$env:PORT="8001"`; macOS/Linux: `export PORT=8001`). Local frontend origins on port 5173 are allowed by default. Container work must bind the API to `0.0.0.0` and document port/origin configuration.

## Add synthetic data

In another terminal, activate the same environment and run from the root:

```sh
cd backend
python seed_data.py
```

The helper creates three projects and synthetic traces without calling an LLM. It checks every API write and reports errors rather than claiming a failed insert succeeded. Use `--base-url http://127.0.0.1:8001` for another API port and `--seed 42` for repeatable sample values. IDs/timestamps remain fresh. Each run **adds** records. Storage is in memory: stopping or reloading the API clears all data. Use synthetic data only; this unauthenticated starter is for local learning.

Model names and USD-per-million rates are fixed teaching fixtures, not live provider prices. Incorrect computed costs are part of TL-2 below.

## Run the starter diagnostics

From the root, with the environment active:

```sh
cd backend
python -m pytest tests -v
```

**The initial suite is intentionally red.** It exposes the open tickets below, including the missing PATCH route. Repair the application; do not delete, skip or weaken checks to make it green. These public diagnostics are not a complete grading suite. Add meaningful regression and feature tests as you work; collecting zero tests is not success. [Test notes](backend/tests/README.md) distinguish setup failures from expected defect failures.

## Inherited issue tracker - Module 2

| Ticket | Required repaired behavior |
|---|---|
| TL-1 | A missing trace returns 404 rather than crashing. |
| TL-2 | Costs use the fixed per-million-token rates and agree with a hand calculation. |
| TL-3 | A page contains at most `limit` traces; `total` is the full filtered count before pagination. |
| TL-4 | An existing project with no traces returns zeroed stats. |
| TL-5 | Project deletion cannot leave dangling trace references: document and test cascade, detach or reject. |
| TL-6 | Implement partial `PATCH /projects/{id}` with preserved omitted fields, timestamp update and missing-ID handling. |

See [CONTRACT.md](CONTRACT.md) for expected behavior and edge cases. The starter deliberately omits the repairs, new features, full documentation, AI instruction file, CI, containers and React application that you will create.

## Course milestones

| Module | Build and evidence | Criteria |
|---|---|---|
| [2 - Brownfield challenge](milestones/module-02.md) | Understand the system; close TL-1 through TL-6; verify AI changes. | C1.1-C1.6 |
| [3 - Documentation and specs](milestones/module-03.md) | Document the repaired backend; specify evaluations and alert rules; demonstrate agent instructions. | C2.1-C2.3 |
| [4 - Production-ready backend](milestones/module-04.md) | Build one feature test-first; tests, refactor, CI gate and containers. | C2.4-C2.8; finalize C2.1/C2.2 |
| [5 - Full-stack application](milestones/module-05.md) | Build the other feature test-first and a specified React UI; reproducible deployment. | C3.1-C3.5 |
| [6 - Delivery and defense](milestones/module-06.md) | Explain your own final code and decisions; no additional feature. | C3.6-C3.8 |

Both **Evaluation Scores** and **Alert Rules** are required. Either can come first; evaluations are a useful first choice. Requirements and open design decisions live in [specs/evaluations.md](specs/evaluations.md) and [specs/alert-rules.md](specs/alert-rules.md). Write your own implementable specs before coding.

## Repository layout

- `backend/app/`: inherited API, models, in-memory storage and utilities.
- `backend/tests/`: public diagnostic starting point; expand it.
- `backend/seed_data.py`: synthetic data helper.
- `specs/`: learner-authored specifications, starting from the briefs provided.
- `docs/`: your system model, API reference and supporting evidence.
- `frontend/`: create the React application in Module 5.
- `milestones/`, `rubrics/`, `ASSESSMENT.md`: course tasks and assessment expectations.
- `EVIDENCE.md`: your continuing evidence record.

Keep route contracts stable while refactoring. Extensions such as persistence, authentication, live model ingestion or charts are optional and carry no extra credit. Finish the required work first; extras cannot compensate for an unmet criterion.
