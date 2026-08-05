# TraceLens

**LLM Observability & Evaluation Platform**

---

## Welcome to the Team! 👋

Congratulations on joining the TraceLens engineering team! You've been brought on to take over our observability product after the previous developer left — somewhat abruptly.

### What is TraceLens?

TraceLens is a self-hosted observability platform for teams that ship LLM features. Think of it as a **"Datadog for LLM calls"** — every prompt your product sends to a model gets logged as a *trace*, and TraceLens turns those traces into answers:

- 📡 **Ingest traces** — model, prompt, response, tokens, latency, status, tags
- 📁 **Organize by project** — one project per product or feature
- 💰 **Track spend** — per-call cost computed from model pricing tables
- 📊 **Aggregate stats** — cost, latency, error rate per project
- 🔎 **Explore traces** — filter by project, model, status; search; paginate
- 🧪 **Evaluations & alerting** — you'll specify and build these yourself

### The Current Situation

The previous developer left us with a *partially working* backend, and the issue tracker has been filling up:

| Ticket | Reported symptom |
|--------|------------------|
| **TL-1** | Opening a trace that doesn't exist crashes with a 500 instead of returning 404 |
| **TL-2** | Customers say dashboard costs are **~1000× higher** than their provider bills |
| **TL-3** | The trace list pager is broken — pages overlap by one item, and `total` is wrong so page numbers can't be computed |
| **TL-4** | Viewing stats for a **freshly created project** crashes with a 500 |
| **TL-5** | Deleting a project leaves its traces behind, pointing at a project that no longer exists |
| **TL-6** | The README documents `PATCH /projects/{id}` for renaming projects — it was never implemented |

On top of that: the **documentation is minimal**, the **tests are thin** (some of them fail on purpose — they point at the tickets above), there's **no CI/CD pipeline**, and **no frontend** has been built yet.

Your job across the five modules is to transform this into a **production-ready, full-stack observability product**.

---

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+ (for Module 4)
- Git

### Run Locally

```bash
# Clone the repo
git clone <your-repo-url>
cd tracelens

# Set up backend
cd backend
pip install -r requirements.txt
python main.py
```

API runs at: http://localhost:8000

API docs at: http://localhost:8000/docs

### Seed Sample Data

With the API running, in a second terminal:

```bash
cd backend
python seed_data.py
```

### Run Tests

```bash
cd backend
pytest tests/ -v
```

Expect failures — several provided tests document the open tickets.

---

## Project Structure

```
tracelens/
├── README.md                    # You are here
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api.py              # FastAPI routes (see the tickets!)
│   │   ├── models.py           # Pydantic models
│   │   ├── storage.py          # In-memory storage
│   │   └── utils.py            # Cost calc, filters, pagination, stats
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_api.py         # Basic tests — some fail, pointing at tickets
│   │   └── conftest.py         # Test fixtures
│   ├── main.py                 # Entry point
│   ├── seed_data.py            # Populate the API with sample data
│   └── requirements.txt
│
├── frontend/                    # You'll create this in Module 4
├── specs/                       # You'll create these in Module 2
└── docs/                        # You'll create these in Module 1
```

---

## Your Mission

### 🧪 Experimentation Encouraged!
While we provide guidelines, **you are the engineer**. If you see a better way to solve a problem using AI, do it!
- Want to swap the storage layer for a real database? **Go for it.**
- Want to add authentication? **Do it.**
- Want to restructure the API? **As long as tests pass, you're clear.**

The goal is to learn how to build *better* software *faster* with AI. Don't be afraid to break things and rebuild them better.

### Module 1: Rescue the Backend
- Understand this codebase using AI
- Close tickets TL-1 through TL-5
- Implement the missing PATCH endpoint (TL-6)

### Module 2: Specify What Comes Next
- Write professional documentation
- Configure a custom AI agent for the project
- Write feature specs: **Evaluations** and **Alert Rules**

### Module 3: Make it Production-Ready
- Comprehensive tests, one spec feature built with TDD
- CI/CD pipeline and Docker

### Module 4: Build the Frontend
- The second spec feature, plus a React dashboard and trace explorer
- Deployed where someone else can reach it

### Module 5: Defend It
- A recorded defense of code *we* pick

---

## API Endpoints (Current)

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/health` | Health check | ✅ Works |
| GET | `/projects` | List projects | ✅ Works |
| GET | `/projects/{id}` | Get single project | ✅ Works |
| POST | `/projects` | Create project | ✅ Works |
| PUT | `/projects/{id}` | Full update of a project | ✅ Works |
| PATCH | `/projects/{id}` | Partial update (rename etc.) | ❌ TL-6: documented but missing |
| DELETE | `/projects/{id}` | Delete project | ⚠️ TL-5 |
| GET | `/projects/{id}/stats` | Cost / latency / error stats | ❌ TL-4 |
| GET | `/traces` | List traces with filters + pagination | ⚠️ TL-3 |
| GET | `/traces/{id}` | Get single trace | ❌ TL-1 |
| POST | `/traces` | Ingest a trace | ⚠️ TL-2 (cost) |
| DELETE | `/traces/{id}` | Delete trace | ✅ Works |

---

## Tech Stack

- **Backend**: Python 3.10+, FastAPI, Pydantic
- **Frontend**: React, Vite (Module 4)
- **Testing**: pytest, pytest-cov
- **DevOps**: Docker, GitHub Actions (Module 3)

---

Good luck, and welcome to the team! 🚀
