import logging

import pytest
from fastapi.testclient import TestClient

from bcp.logger import setup_logger
from src.api.server import app, jobs, process_bcp_calculation


@pytest.fixture(autouse=True)
def clear_jobs():
    jobs.clear()
    yield
    jobs.clear()


def test_root():
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "BCP Calculator API"


def test_calculate_and_status(monkeypatch):
    client = TestClient(app)

    # Stub calculation to be deterministic and fast
    def fake_process(job_id: str, story_content: str, provider: str):
        jobs[job_id] = {
            "status": "completed",
            "result": {"story_name": "X", "total_bcp": 1, "breakdown": {}},
        }

    monkeypatch.setattr("src.api.server.process_bcp_calculation", fake_process)

    resp = client.post("/calculate", json={"content": "A", "provider": "openai"})
    assert resp.status_code == 200
    job_id = resp.json()["job_id"]

    # Immediately check status
    status = client.get(f"/status/{job_id}")
    assert status.status_code == 200
    data = status.json()
    assert data["status"] == "completed"
    assert data["result"]["total_bcp"] == 1


def test_background_task_success(monkeypatch, clear_jobs):
    """Test process_bcp_calculation directly with a mocked calculator."""
    from tests.conftest import FakePromptHandler

    class FakeCalc:
        def __init__(self, logger, provider_name="openai", prompt_handler=None):
            pass

        def calculate_bcp(self, story_content):
            return {"total_bcp": 7, "breakdown": {}}

    monkeypatch.setattr("src.api.server.BCPCalculator", FakeCalc)

    jobs["job-1"] = {"status": "pending", "result": None}
    process_bcp_calculation("job-1", "story content", "openai")
    assert jobs["job-1"]["status"] == "completed"
    assert jobs["job-1"]["result"]["total_bcp"] == 7


def test_background_task_failure(monkeypatch, clear_jobs):
    """Test that errors in BCP calculation are caught and recorded."""

    class FailingCalc:
        def __init__(self, logger, provider_name="openai", prompt_handler=None):
            pass

        def calculate_bcp(self, story_content):
            raise RuntimeError("LLM timeout")

    monkeypatch.setattr("src.api.server.BCPCalculator", FailingCalc)

    jobs["job-2"] = {"status": "pending", "result": None}
    process_bcp_calculation("job-2", "story", "openai")
    assert jobs["job-2"]["status"] == "failed"
    assert "LLM timeout" in jobs["job-2"]["error"]
