# TraceLens baseline contract

This is the **target behavior after Module 2**, not a claim that the starter already implements it. Swagger describes the current code and therefore initially lacks PATCH. Later feature contracts belong in your own specs. Use the fixed local fixtures; no provider integration is required.

## Projects and traces

Project: generated ID, required name (1-100 characters), optional description (up to 500), UTC creation/update timestamps. A trace references an existing project and records model, nonempty prompt, optional response, nonnegative prompt/completion token counts and latency in milliseconds, success/error status, optional error message, and up to ten non-blank tags of at most 32 characters each. Ingestion requires a project even if your deletion strategy later detaches traces. Whitespace-only project names are not separately rejected by the baseline schema; specify any stricter validation consistently if you add it.

| Method | Route | Success and relevant failures |
|---|---|---|
| GET | `/health` | 200 with healthy status and version. |
| GET | `/projects` | 200 `{projects, total}`, newest creation first. |
| POST | `/projects` | 201 with stored project; invalid input 422. |
| GET | `/projects/{id}` | 200 project; missing 404. |
| PUT | `/projects/{id}` | 200 full editable-field replacement, name required; preserve ID/created_at, refresh updated_at; missing 404, invalid 422. Omitted description becomes null. |
| PATCH | `/projects/{id}` | TL-6: 200 partial update; details below. |
| DELETE | `/projects/{id}` | 204 empty body; missing 404; nonempty project may return 409 under a documented reject strategy. |
| GET | `/projects/{id}/stats` | 200 aggregate object; missing project 404; existing empty project returns zeros. |
| GET | `/traces` | 200 `{traces, total, limit, offset}`; invalid query 422. |
| POST | `/traces` | 201 trace with computed cost; unknown project 400, invalid payload/tags 422. |
| GET | `/traces/{id}` | 200 trace; missing 404 (TL-1). |
| DELETE | `/traces/{id}` | 204 empty body; missing 404. |

Errors use FastAPI's `detail` field; validation details may be a list, application errors a string. Clients must handle both. No authentication is implemented in the starter. Data is process-local and lost on restart/reload; persistence is optional, not a hidden requirement.

## TL-2: cost and TL-4: statistics

Rates in `backend/app/utils.py` are **USD per one million tokens**, stored as input/output pairs. Unknown model IDs use the documented default pair. For the fixture `openai/gpt-4o-mini`, 1,000 input tokens and 500 output tokens must cost **$0.00045**. Keep a hand calculation and test more than one model/zero-token case. Store cost rounded to eight decimal places.

Stats include project_id, trace_count, total_cost_usd (sum rounded to six decimals), avg_latency_ms (arithmetic mean), error_rate (fraction 0-1), total_prompt_tokens and total_completion_tokens. With no traces, every numeric value is zero; the project ID remains present.

## TL-3: filtering and pagination

Filters `project_id`, `model` and `status` combine with AND. Status is `success` or `error`. Search is case-insensitive across prompt OR response and combines with the filters. Sort newest creation first before slicing. `limit` defaults to 20 and accepts 1-100; `offset` defaults to 0 and must be nonnegative. Return at most `limit` items, fewer on the last page and none past the end. `total` always counts all filtered matches, independent of the requested page. Preserve stable ordering for equal timestamps. No matches is an empty list and total zero.

## TL-5: deletion policy - choose and document one

- **Cascade:** delete the project and all its traces, return 204.
- **Detach:** delete the project, keep its traces with `project_id: null`, return 204. Adapt stored/response models so detached traces remain readable; ingestion must still require a valid project.
- **Reject:** return 409 and leave project and traces unchanged while traces exist. Allow deletion of an empty project.

Document the choice in README, the system model and API reference; test it. Merely hiding orphaned traces from a list is not a repair. In later specs, define how evaluations and alert rules follow project/trace deletion. The frontend must visibly respect your chosen policy.

## TL-6: PATCH

Only `name` and `description` are editable. Omitted fields retain their values. A supplied name must meet the existing name constraints and cannot be null; description may be null to clear it. Preserve ID and created_at, refresh updated_at on accepted requests, and store the update. An empty object is accepted and refreshes updated_at. A valid request to a missing ID returns 404. Invalid editable values return 422 and must not partially change the stored project. Document your handling of unknown fields consistently with your models; they must never allow identity/timestamp fields to be changed by a caller.

## Scope boundaries

Do not rename/remove these public routes to work around a defect. Refactor internals without changing observable behavior. Optional architecture changes must preserve these guarantees and keep the required tests/evidence meaningful. The two feature specs define their own route shapes and validations before implementation.
