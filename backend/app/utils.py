"""Utility functions for TraceLens"""

from typing import List, Optional
from app.models import Trace, ProjectStats


# Pricing in USD per 1 MILLION tokens: (input_price, output_price)
# Prices roughly follow OpenRouter listings.
MODEL_PRICING = {
    "openai/gpt-4o-mini": (0.15, 0.60),
    "openai/gpt-4o": (2.50, 10.00),
    "moonshotai/kimi-k3": (0.55, 2.20),
    "z-ai/glm-5.2": (0.40, 1.60),
}

# Fallback for models we don't have listed prices for
DEFAULT_PRICING = (1.00, 3.00)


def calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Calculate the USD cost of a single LLM call.

    Pricing is stored per one million tokens.
    """
    input_price, output_price = MODEL_PRICING.get(model, DEFAULT_PRICING)
    input_cost = (prompt_tokens / 1_000) * input_price
    output_cost = (completion_tokens / 1_000) * output_price
    return round(input_cost + output_cost, 8)


def sort_traces_by_date(traces: List[Trace], descending: bool = True) -> List[Trace]:
    """Sort traces by creation date, newest first by default."""
    return sorted(traces, key=lambda t: t.created_at, reverse=descending)


def filter_traces_by_project(traces: List[Trace], project_id: str) -> List[Trace]:
    return [t for t in traces if t.project_id == project_id]


def filter_traces_by_model(traces: List[Trace], model: str) -> List[Trace]:
    return [t for t in traces if t.model == model]


def filter_traces_by_status(traces: List[Trace], status: str) -> List[Trace]:
    return [t for t in traces if t.status == status]


def search_traces(traces: List[Trace], query: str) -> List[Trace]:
    """Search traces by prompt or response content (case-insensitive)."""
    query_lower = query.lower()
    return [
        t for t in traces
        if query_lower in t.prompt.lower() or
           (t.response and query_lower in t.response.lower())
    ]


def paginate(items: List, limit: int, offset: int) -> List:
    """Return one page of items."""
    return items[offset:offset + limit + 1]


def compute_project_stats(project_id: str, traces: List[Trace]) -> ProjectStats:
    """Aggregate observability stats for a single project."""
    error_count = len([t for t in traces if t.status == "error"])

    return ProjectStats(
        project_id=project_id,
        trace_count=len(traces),
        total_cost_usd=round(sum(t.cost_usd for t in traces), 6),
        avg_latency_ms=sum(t.latency_ms for t in traces) / len(traces),
        error_rate=error_count / len(traces),
        total_prompt_tokens=sum(t.prompt_tokens for t in traces),
        total_completion_tokens=sum(t.completion_tokens for t in traces),
    )


def validate_tags(tags: List[str]) -> bool:
    """Check that a tag list is valid.

    Valid tags are non-empty, at most 32 characters, and there are
    at most 10 tags per trace.
    """
    if len(tags) > 10:
        return False
    return all(tag.strip() and len(tag) <= 32 for tag in tags)
