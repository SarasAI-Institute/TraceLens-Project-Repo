"""Pydantic models for TraceLens"""

from datetime import datetime, timezone
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, ConfigDict
from uuid import uuid4


def generate_id() -> str:
    return str(uuid4())


def get_current_time() -> datetime:
    return datetime.now(timezone.utc)


# ============== Project Models ==============

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class Project(ProjectBase):
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    model_config = ConfigDict(from_attributes=True)


# ============== Trace Models ==============

class TraceBase(BaseModel):
    project_id: str
    model: str = Field(..., min_length=1, max_length=100)
    prompt: str = Field(..., min_length=1)
    response: Optional[str] = None
    prompt_tokens: int = Field(..., ge=0)
    completion_tokens: int = Field(..., ge=0)
    latency_ms: int = Field(..., ge=0)
    status: Literal["success", "error"] = "success"
    error_message: Optional[str] = Field(None, max_length=1000)
    tags: List[str] = Field(default_factory=list)


class TraceCreate(TraceBase):
    pass


class Trace(TraceBase):
    id: str = Field(default_factory=generate_id)
    cost_usd: float = 0.0
    created_at: datetime = Field(default_factory=get_current_time)

    model_config = ConfigDict(from_attributes=True)


# ============== Stats Models ==============

class ProjectStats(BaseModel):
    project_id: str
    trace_count: int
    total_cost_usd: float
    avg_latency_ms: float
    error_rate: float
    total_prompt_tokens: int
    total_completion_tokens: int


# ============== Response Models ==============

class TraceList(BaseModel):
    traces: List[Trace]
    total: int
    limit: int
    offset: int


class ProjectList(BaseModel):
    projects: List[Project]
    total: int


class HealthResponse(BaseModel):
    status: str
    version: str
