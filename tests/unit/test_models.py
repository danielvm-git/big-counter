"""Tests for API Pydantic models."""

import pytest
from pydantic import ValidationError

from src.api.models import JobStatus, StoryRequest


class TestStoryRequest:
    def test_valid_request(self):
        req = StoryRequest(content="As a user, I want to log in")
        assert req.content == "As a user, I want to log in"
        assert req.provider == "openai"  # default

    def test_missing_content_raises(self):
        with pytest.raises(ValidationError):
            StoryRequest()

    def test_explicit_provider(self):
        req = StoryRequest(content="test", provider="claude")
        assert req.provider == "claude"


class TestJobStatus:
    def test_completed_job(self):
        job = JobStatus(
            job_id="abc-123",
            status="completed",
            result={"total_bcp": 12, "story_name": "Login"},
        )
        assert job.job_id == "abc-123"
        assert job.result["total_bcp"] == 12
        assert job.error is None

    def test_failed_job(self):
        job = JobStatus(
            job_id="xyz-456",
            status="failed",
            error="API rate limit exceeded",
        )
        assert job.error == "API rate limit exceeded"
        assert job.result is None

    def test_pending_job_no_result(self):
        job = JobStatus(job_id="pend-1", status="pending")
        assert job.result is None
        assert job.error is None
