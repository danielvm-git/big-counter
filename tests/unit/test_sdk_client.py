"""Tests for SDK client — mocked BCPCalculator to avoid live API dependencies."""

import json
import logging
from pathlib import Path

import pytest

from bcp.logger import setup_logger
from src.sdk.client import BCPClient


class FakeCalculator:
    """Test double that returns pre-canned BCP results without LLM calls."""

    def __init__(self, logger, provider_name="openai", prompt_handler=None):
        self.logger = logger
        self.provider_name = provider_name

    def calculate_bcp(self, story_content):
        return {
            "story_name": story_content.strip().split("\n")[0],
            "total_bcp": 5,
            "breakdown": {"Business Rules": 2, "UI Elements": 3},
        }


@pytest.fixture
def client(monkeypatch):
    """BCPClient with FakeCalculator — no API keys needed."""
    monkeypatch.setattr("src.sdk.client.BCPCalculator", FakeCalculator)
    return BCPClient(provider="openai")


class TestCalculate:
    def test_calculate_returns_result(self, client):
        result = client.calculate("Test Story\nAs a user, I want X")
        assert result["total_bcp"] == 5
        assert result["story_name"] == "Test Story"

    def test_calculate_file(self, client, tmp_path):
        story_file = tmp_path / "story.md"
        story_file.write_text("Password Reset\nAs a user...")
        result = client.calculate_file(str(story_file))
        assert result["total_bcp"] == 5

    def test_calculate_file_not_found(self, client):
        with pytest.raises(FileNotFoundError):
            client.calculate_file("/nonexistent/story.md")

    def test_batch_calculate(self, client, tmp_path):
        (tmp_path / "story_a.md").write_text("Story A\nbody")
        (tmp_path / "story_b.md").write_text("Story B\nbody")

        results = client.batch_calculate(str(tmp_path))
        assert "story_a.md" in results
        assert "story_b.md" in results
        assert results["story_a.md"]["total_bcp"] == 5

    def test_batch_output_file(self, client, tmp_path):
        (tmp_path / "story_x.md").write_text("Story X\nbody")
        output = tmp_path / "results.json"
        client.batch_calculate(str(tmp_path), output_path=str(output))
        assert output.exists()
        data = json.loads(output.read_text())
        assert "story_x.md" in data

    def test_batch_non_directory_raises(self, client, tmp_path):
        not_a_dir = tmp_path / "file.txt"
        not_a_dir.write_text("not a dir")
        with pytest.raises(NotADirectoryError):
            client.batch_calculate(str(not_a_dir))

    def test_compare_providers(self, client):
        results = client.compare_providers("Test Story\nbody", providers=["openai", "claude"])
        assert "openai" in results
        assert "claude" in results
        assert results["openai"]["total_bcp"] == 5
        assert results["claude"]["total_bcp"] == 5
