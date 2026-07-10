"""
Pydantic models for the BCP Calculator API.
"""

from typing import Any

from pydantic import BaseModel, Field


class StoryRequest(BaseModel):
    """Request model for BCP calculation."""

    content: str = Field(..., description="User story content")
    provider: str = Field("openai", description="LLM provider to use (openai or claude)")


class JobStatus(BaseModel):
    """Response model for job status."""

    job_id: str = Field(..., description="Unique identifier for the job")
    status: str = Field(
        ..., description="Current status of the job (pending, processing, completed, failed)"
    )
    result: dict[str, Any] | None = Field(
        None, description="Results of the BCP calculation if completed"
    )
    error: str | None = Field(None, description="Error message if job failed")
