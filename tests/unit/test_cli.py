"""Tests for CLI entry point — formatters, file reading, argument parsing."""

import logging

import pytest

from bcp.logger import setup_logger
from src.main import format_results_json, format_results_text, read_story_file


class TestFormatResultsJson:
    def test_full_results(self):
        results = {
            "story_name": "Login",
            "total_bcp": 8,
            "breakdown": {"Business Rules": 3, "UI Elements": 5},
            "steps": {
                "Business Rules Complexity": {
                    "assessment": "moderate",
                    "score": 3,
                    "classification": "Medium",
                    "raw_response": "",
                },
                "UI Elements Complexity": {"total": 5},
                "Story Maturity Complexity": {"score": 4},
                "Story INVEST Maturity": {"score": 3},
            },
        }
        output = format_results_json(results)
        assert '"total_bcp": 8' in output
        assert '"story_name": "Login"' in output
        assert '"maturity": 4' in output
        assert '"invest": 3' in output

    def test_empty_steps(self):
        results = {
            "story_name": "Minimal",
            "total_bcp": 0,
            "breakdown": {},
            "steps": {},
        }
        output = format_results_json(results)
        assert '"maturity": 0' in output
        assert '"invest": 0' in output


class TestFormatResultsText:
    def test_contains_sections(self):
        results = {
            "story_name": "Test",
            "total_bcp": 10,
            "breakdown": {"Business Rules": 5, "UI Elements": 5},
            "steps": {
                "Business Rules Complexity": "details here",
                "UI Elements Complexity": "more details",
            },
        }
        output = format_results_text(results)
        assert "=== Business Rules Complexity ===" in output
        assert "=== FINAL BUSINESS COMPLEXITY POINTS ===" in output
        assert "=== BCP BREAKDOWN ===" in output
        assert "Total BCP: 10" in output
        assert "Business Rules: 5" in output


class TestReadStoryFile:
    def test_reads_existing_file(self, tmp_path):
        story = tmp_path / "story.md"
        story.write_text("# Login\nAs a user...")
        logger = setup_logger(logging.DEBUG)
        content = read_story_file(str(story), logger)
        assert content == "# Login\nAs a user..."

    def test_missing_file_exits(self, tmp_path):
        logger = setup_logger(logging.DEBUG)
        with pytest.raises(SystemExit):
            read_story_file(str(tmp_path / "nope.md"), logger)


class TestSaveOrPrintResults:
    def test_saves_to_file(self, tmp_path):
        from src.main import save_or_print_results

        results = {
            "story_name": "Test",
            "total_bcp": 5,
            "breakdown": {"Business Rules": 5},
            "steps": {},
        }
        output_file = tmp_path / "output.json"
        logger = setup_logger(logging.DEBUG)
        save_or_print_results(results, "json", str(output_file), logger)
        assert output_file.exists()
        assert "Test" in output_file.read_text()

    def test_calculate_bcp_error_exits(self, monkeypatch):
        from src import main as main_module

        def failing_calc(logger, provider_name="openai", prompt_handler=None):
            raise RuntimeError("LLM down")

        monkeypatch.setattr(main_module, "BCPCalculator", failing_calc)
        logger = setup_logger(logging.DEBUG)
        with pytest.raises(SystemExit):
            main_module.calculate_bcp_for_story("story", "openai", logger)
