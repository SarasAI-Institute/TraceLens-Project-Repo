"""FastAPI routes for TraceLens"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Project, ProjectCreate, ProjectUpdate, ProjectList, ProjectStats,
    Trace, TraceCreate, TraceList, HealthResponse,
    get_current_time
)
from app.storage import storage
from app.utils import (
    calculate_cost, sort_traces_by_date, paginate,
    filter_traces_by_project, filter_traces_by_model,
    filter_traces_by_status, search_traces, compute_project_stats
)
from app import __version__


app = FastAPI(
    title="TraceLens API",
    description="LLM Observability Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="healthy", version=__version__)


# ============== Project Endpoints ==============

@app.get("/projects", response_model=ProjectList)
def list_projects():
    projects = storage.get_all_projects()
    projects = sorted(projects, key=lambda p: p.created_at, reverse=True)
    return ProjectList(projects=projects, total=len(projects))


@app.get("/projects/{project_id}", response_model=Project)
def get_project(project_id: str):
    project = storage.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.post("/projects", response_model=Project, status_code=201)
def create_project(project_data: ProjectCreate):
    project = Project(**project_data.model_dump())
    return storage.create_project(project)


@app.put("/projects/{project_id}", response_model=Project)
def update_project(project_id: str, project_data: ProjectUpdate):
    existing = storage.get_project(project_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Project not found")

    updated_project = Project(
        id=existing.id,
        name=project_data.name,
        description=project_data.description,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )

    return storage.update_project(project_id, updated_project)


# NOTE: PATCH /projects/{id} for partial updates is documented in the README
# but was never implemented.


@app.delete("/projects/{project_id}", status_code=204)
def delete_project(project_id: str):
    if not storage.delete_project(project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return None


@app.get("/projects/{project_id}/stats", response_model=ProjectStats)
def get_project_stats(project_id: str):
    project = storage.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    traces = storage.get_traces_by_project(project_id)
    return compute_project_stats(project_id, traces)


# ============== Trace Endpoints ==============

@app.get("/traces", response_model=TraceList)
def list_traces(
    project_id: Optional[str] = None,
    model: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
):
    traces = storage.get_all_traces()

    if project_id:
        traces = filter_traces_by_project(traces, project_id)
    if model:
        traces = filter_traces_by_model(traces, model)
    if status:
        traces = filter_traces_by_status(traces, status)
    if search:
        traces = search_traces(traces, search)

    traces = sort_traces_by_date(traces, descending=True)
    page = paginate(traces, limit, offset)

    return TraceList(traces=page, total=len(page), limit=limit, offset=offset)


@app.get("/traces/{trace_id}", response_model=Trace)
def get_trace(trace_id: str):
    trace = storage.get_trace(trace_id)

    if trace.id:
        return trace


@app.post("/traces", response_model=Trace, status_code=201)
def create_trace(trace_data: TraceCreate):
    # Validate the project exists
    project = storage.get_project(trace_data.project_id)
    if not project:
        raise HTTPException(status_code=400, detail="Project not found")

    cost = calculate_cost(
        trace_data.model,
        trace_data.prompt_tokens,
        trace_data.completion_tokens
    )

    trace = Trace(**trace_data.model_dump(), cost_usd=cost)
    return storage.create_trace(trace)


@app.delete("/traces/{trace_id}", status_code=204)
def delete_trace(trace_id: str):
    if not storage.delete_trace(trace_id):
        raise HTTPException(status_code=404, detail="Trace not found")
    return None
