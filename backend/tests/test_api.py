"""API tests for TraceLens

These tests verify the API endpoints work correctly.
Some of them currently FAIL — the failures point at real defects
listed in the Module 2 issue tickets. Students should expand these
tests significantly in Module 4.
"""

import pytest
from fastapi.testclient import TestClient


class TestHealth:
    """Tests for health endpoint."""

    def test_health_check(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestProjects:
    """Tests for project endpoints."""

    def test_create_project(self, client: TestClient, sample_project_data):
        response = client.post("/projects", json=sample_project_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_project_data["name"]
        assert "id" in data
        assert "created_at" in data

    def test_list_projects(self, client: TestClient, sample_project_data):
        client.post("/projects", json=sample_project_data)

        response = client.get("/projects")
        assert response.status_code == 200
        data = response.json()
        assert len(data["projects"]) == 1
        assert data["total"] == 1

    def test_get_project_not_found(self, client: TestClient):
        response = client.get("/projects/nonexistent-id")
        assert response.status_code == 404

    def test_update_project(self, client: TestClient, sample_project):
        project_id = sample_project["id"]

        updated_data = {
            "name": "Renamed Project",
            "description": "Updated description"
        }
        response = client.put(f"/projects/{project_id}", json=updated_data)
        assert response.status_code == 200
        assert response.json()["name"] == "Renamed Project"

    def test_delete_project(self, client: TestClient, sample_project):
        project_id = sample_project["id"]

        response = client.delete(f"/projects/{project_id}")
        assert response.status_code == 204

        get_response = client.get(f"/projects/{project_id}")
        assert get_response.status_code == 404

    def test_delete_project_with_traces(
        self, client: TestClient, sample_project, sample_trace_data
    ):
        """TL-5: cascade, detach or reject, but never leave a dangling reference."""
        project_id = sample_project["id"]
        created = client.post("/traces", json={**sample_trace_data, "project_id": project_id})
        assert created.status_code == 201
        trace_id = created.json()["id"]
        deleted = client.delete(f"/projects/{project_id}")
        project = client.get(f"/projects/{project_id}")
        # Inspect storage as well as HTTP: a list filter must not hide an orphan.
        from app.storage import storage
        surviving = storage.get_trace(trace_id)
        if deleted.status_code == 409:  # Documented reject-if-nonempty policy.
            assert project.status_code == 200
            assert surviving is not None and surviving.project_id == project_id
        else:
            assert deleted.status_code == 204
            assert project.status_code == 404
            assert surviving is None or surviving.project_id is None
            if surviving is not None:  # Detach must remain representable over the API.
                detail = client.get(f"/traces/{trace_id}")
                assert detail.status_code == 200
                assert detail.json()["project_id"] is None


class TestTraces:
    """Tests for trace endpoints."""

    def test_create_trace(self, client: TestClient, sample_project, sample_trace_data):
        trace_data = {**sample_trace_data, "project_id": sample_project["id"]}
        response = client.post("/traces", json=trace_data)
        assert response.status_code == 201
        data = response.json()
        assert data["model"] == trace_data["model"]
        assert "id" in data
        assert "cost_usd" in data

    def test_create_trace_unknown_project(self, client: TestClient, sample_trace_data):
        trace_data = {**sample_trace_data, "project_id": "nonexistent-id"}
        response = client.post("/traces", json=trace_data)
        assert response.status_code == 400

    def test_trace_cost_calculation(
        self, client: TestClient, sample_project, sample_trace_data
    ):
        """Cost for gpt-4o-mini: $0.15 per 1M input, $0.60 per 1M output.

        1000 prompt tokens  -> $0.00015
        500 completion tokens -> $0.00030
        Total: $0.00045

        NOTE: Ticket TL-2 — this test currently FAILS. Users report
        dashboard costs roughly 1000x higher than their provider bills.
        """
        trace_data = {**sample_trace_data, "project_id": sample_project["id"]}
        response = client.post("/traces", json=trace_data)
        cost = response.json()["cost_usd"]
        assert cost == pytest.approx(0.00045)  # Will fail until TL-2 is fixed

    def test_get_trace_not_found(self, client: TestClient):
        """Getting a non-existent trace should return 404.

        NOTE: Ticket TL-1 — this test currently FAILS.
        The API returns 500 instead of 404.
        """
        response = client.get("/traces/nonexistent-id")
        assert response.status_code == 404  # Will fail until TL-1 is fixed

    def test_delete_trace(self, client: TestClient, sample_project, sample_trace_data):
        trace_data = {**sample_trace_data, "project_id": sample_project["id"]}
        create_response = client.post("/traces", json=trace_data)
        trace_id = create_response.json()["id"]

        response = client.delete(f"/traces/{trace_id}")
        assert response.status_code == 204

    def test_list_traces_filter_by_status(
        self, client: TestClient, sample_project, sample_trace_data
    ):
        project_id = sample_project["id"]
        ok_trace = {**sample_trace_data, "project_id": project_id}
        failed_trace = {
            **sample_trace_data,
            "project_id": project_id,
            "status": "error",
            "response": None,
            "error_message": "Rate limit exceeded"
        }
        client.post("/traces", json=ok_trace)
        client.post("/traces", json=failed_trace)

        response = client.get("/traces", params={"status": "error"})
        data = response.json()
        assert len(data["traces"]) == 1
        assert data["traces"][0]["status"] == "error"

    def test_pagination_page_size(
        self, client: TestClient, sample_project, sample_trace_data
    ):
        """Requesting limit=2 must return exactly 2 traces.

        NOTE: Ticket TL-3 — this test currently FAILS.
        The API returns one more trace than requested.
        """
        project_id = sample_project["id"]
        for i in range(5):
            trace = {
                **sample_trace_data,
                "project_id": project_id,
                "prompt": f"Prompt number {i}"
            }
            client.post("/traces", json=trace)

        response = client.get("/traces", params={"limit": 2, "offset": 0})
        data = response.json()
        assert len(data["traces"]) == 2  # Will fail until TL-3 is fixed

    def test_pagination_total_is_full_count(
        self, client: TestClient, sample_project, sample_trace_data
    ):
        """'total' must be the full filtered count, not the page size.

        NOTE: Ticket TL-3 — this test currently FAILS.
        The frontend pager cannot compute page numbers without it.
        """
        project_id = sample_project["id"]
        for i in range(5):
            trace = {
                **sample_trace_data,
                "project_id": project_id,
                "prompt": f"Prompt number {i}"
            }
            client.post("/traces", json=trace)

        response = client.get("/traces", params={"limit": 2, "offset": 0})
        data = response.json()
        assert data["total"] == 5  # Will fail until TL-3 is fixed

    def test_traces_sorted_newest_first(
        self, client: TestClient, sample_project, sample_trace_data
    ):
        from datetime import datetime, timezone, timedelta
        from app.storage import storage

        project_id = sample_project["id"]
        first = {**sample_trace_data, "project_id": project_id, "prompt": "First prompt"}
        second = {**sample_trace_data, "project_id": project_id, "prompt": "Second prompt"}

        first_id = client.post("/traces", json=first).json()["id"]
        second_id = client.post("/traces", json=second).json()["id"]
        baseline = datetime(2026, 1, 1, tzinfo=timezone.utc)
        storage.get_trace(first_id).created_at = baseline
        storage.get_trace(second_id).created_at = baseline + timedelta(seconds=1)

        response = client.get("/traces")
        traces = response.json()["traces"]
        assert traces[0]["prompt"] == "Second prompt"


class TestProjectStats:
    """Tests for the project stats endpoint."""

    def test_stats_with_traces(
        self, client: TestClient, sample_project, sample_trace_data
    ):
        project_id = sample_project["id"]
        ok_trace = {**sample_trace_data, "project_id": project_id}
        failed_trace = {
            **sample_trace_data,
            "project_id": project_id,
            "status": "error",
            "response": None,
            "error_message": "Timeout"
        }
        client.post("/traces", json=ok_trace)
        client.post("/traces", json=failed_trace)

        response = client.get(f"/projects/{project_id}/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["trace_count"] == 2
        assert data["error_rate"] == pytest.approx(0.5)
        assert data["total_prompt_tokens"] == 2000

    def test_stats_empty_project(self, client: TestClient, sample_project):
        """A project with no traces must return zeroed stats, not crash.

        NOTE: Ticket TL-4 — this test currently FAILS with a 500.
        Every newly created project hits this on the dashboard.
        """
        project_id = sample_project["id"]
        response = client.get(f"/projects/{project_id}/stats")
        assert response.status_code == 200  # Will fail until TL-4 is fixed
        data = response.json()
        assert data["trace_count"] == 0
        assert data["total_cost_usd"] == 0
        assert data["error_rate"] == 0

    def test_stats_project_not_found(self, client: TestClient):
        response = client.get("/projects/nonexistent-id/stats")
        assert response.status_code == 404
