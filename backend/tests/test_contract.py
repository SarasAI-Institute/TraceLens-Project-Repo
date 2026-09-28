"""Public starter diagnostics, not an exhaustive assessment suite."""
import pytest
from datetime import datetime, timezone
from app.storage import storage


def test_patch_partial_update(client, sample_project):
    """TL-6: change only supplied fields and preserve identity/creation time."""
    pid = sample_project["id"]
    baseline = datetime(2020, 1, 1, tzinfo=timezone.utc)
    storage.get_project(pid).updated_at = baseline
    response = client.patch(f"/projects/{pid}", json={"name": "Renamed"})
    assert response.status_code == 200
    actual = response.json()
    assert actual["name"] == "Renamed"
    assert actual["description"] == sample_project["description"]
    assert actual["id"] == pid
    assert actual["created_at"] == sample_project["created_at"]
    assert datetime.fromisoformat(actual["updated_at"].replace("Z", "+00:00")) > baseline
    assert client.get(f"/projects/{pid}").json() == actual


def test_patch_missing_project(client):
    assert client.patch("/projects/missing", json={"name": "New"}).status_code == 404


def test_patch_clear_description(client, sample_project):
    pid = sample_project["id"]
    response = client.patch(f"/projects/{pid}", json={"description": None})
    assert response.status_code == 200
    assert response.json()["description"] is None
    assert response.json()["name"] == sample_project["name"]


@pytest.mark.parametrize("params", [{"limit": 0}, {"limit": 101}, {"offset": -1}, {"status": "unknown"}])
def test_invalid_list_parameters(client, params):
    assert client.get("/traces", params=params).status_code == 422


@pytest.mark.parametrize("tags", [[" "], ["x" * 33], ["x"] * 11])
def test_invalid_tags(client, sample_project, sample_trace_data, tags):
    payload = {**sample_trace_data, "project_id": sample_project["id"], "tags": tags}
    assert client.post("/traces", json=payload).status_code == 422
    assert storage.get_all_traces() == []
