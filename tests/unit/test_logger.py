"""Tests for structured JSON logger and StepLogger."""

import json
import logging

import pytest

from bcp.logger import JsonFormatter, StepLogger, setup_logger


class TestJsonFormatter:
    def test_basic_entry(self):
        fmt = JsonFormatter()
        record = logging.LogRecord(
            name="bcp",
            level=logging.INFO,
            pathname="x.py",
            lineno=1,
            msg="hello",
            args=(),
            exc_info=None,
        )
        entry = json.loads(fmt.format(record))
        assert entry["level"] == "info"
        assert entry["message"] == "hello"
        assert entry["logger"] == "bcp"
        assert "timestamp" in entry

    def test_extra_fields_merged(self):
        fmt = JsonFormatter()
        record = logging.LogRecord(
            name="bcp",
            level=logging.WARNING,
            pathname="x.py",
            lineno=1,
            msg="slow request",
            args=(),
            exc_info=None,
        )
        record.__dict__["extra_fields"] = {"requestId": "abc123", "duration_ms": 450}
        entry = json.loads(fmt.format(record))
        assert entry["requestId"] == "abc123"
        assert entry["duration_ms"] == 450
        assert entry["level"] == "warning"

    def test_error_includes_exception(self):
        fmt = JsonFormatter()
        try:
            raise ValueError("boom")
        except ValueError:
            import sys

            record = logging.LogRecord(
                name="bcp",
                level=logging.ERROR,
                pathname="x.py",
                lineno=1,
                msg="failed",
                args=(),
                exc_info=sys.exc_info(),
            )
        entry = json.loads(fmt.format(record))
        assert entry["error"] == "boom"


class TestSetupLogger:
    def test_plain_text_default(self):
        logger = setup_logger(logging.DEBUG, json_format=False)
        logger.info("test message")
        # Handler is present
        assert len(logger.handlers) == 1

    def test_json_format(self):
        logger = setup_logger(logging.DEBUG, json_format=True)
        assert len(logger.handlers) == 1


class TestStepLogger:
    @pytest.fixture
    def logger(self):
        return setup_logger(logging.DEBUG)

    def test_info_includes_step(self, logger):
        step = StepLogger(logger, "Break Elements")
        step.info("processing")
        # Not asserting log output (side-effect only), just that it doesn't crash

    def test_error_includes_step(self, logger):
        step = StepLogger(logger, "Business Rules")
        step.error("LLM call failed")

    def test_debug_and_warning(self, logger):
        step = StepLogger(logger, "Boundaries")
        step.debug("variables: test")
        step.warning("low confidence")
        step.critical("fatal error")
