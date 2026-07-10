"""
Logger module for BCP Calculator

This module provides logging functionality for the BCP Calculator application.
Supports both plain-text (CLI) and structured JSON formats.
"""

import json
import logging
import sys
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    """Structured JSON log formatter — machine-readable output.

    Produces one JSON object per line with level, timestamp, message,
    and any extra fields passed via the `extra` dict in log calls.
    """

    def format(self, record: logging.LogRecord) -> str:
        entry: dict[str, object] = {
            "level": record.levelname.lower(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": record.getMessage(),
            "logger": record.name,
        }
        # Merge extra context fields (never include args tuple)
        if record.__dict__.get("extra_fields"):
            entry.update(record.__dict__["extra_fields"])
        if record.exc_info and record.exc_info[1]:
            entry["error"] = str(record.exc_info[1])
        return json.dumps(entry, default=str)


def setup_logger(
    log_level: int = logging.INFO,
    json_format: bool = False,
) -> logging.Logger:
    """
    Set up and configure the logger.

    Args:
        log_level: The logging level to use (default: INFO)
        json_format: If True, emit structured JSON lines (default: False, plain text)

    Returns:
        A configured logger instance
    """
    logger = logging.getLogger("bcp_calculator")
    logger.setLevel(log_level)

    # Avoid duplicate handlers on repeated calls
    if logger.handlers:
        return logger

    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(log_level)

    if json_format:
        formatter: logging.Formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


class StepLogger:
    """
    Logger wrapper for tracking steps in the BCP calculation process.
    """

    def __init__(self, logger: logging.Logger, step_name: str):
        """
        Initialize a step logger.

        Args:
            logger: The parent logger
            step_name: The name of the step being logged
        """
        self.logger = logger
        self.step_name = step_name

    def _context(self) -> dict[str, str]:
        return {"step": self.step_name}

    def info(self, message: str) -> None:
        """Log an info message with step context."""
        self.logger.info(f"[{self.step_name}] {message}", extra={"extra_fields": self._context()})

    def debug(self, message: str) -> None:
        """Log a debug message with step context."""
        self.logger.debug(f"[{self.step_name}] {message}", extra={"extra_fields": self._context()})

    def warning(self, message: str) -> None:
        """Log a warning message with step context."""
        self.logger.warning(
            f"[{self.step_name}] {message}", extra={"extra_fields": self._context()}
        )

    def error(self, message: str) -> None:
        """Log an error message with step context."""
        self.logger.error(f"[{self.step_name}] {message}", extra={"extra_fields": self._context()})

    def critical(self, message: str) -> None:
        """Log a critical message with step context."""
        self.logger.critical(
            f"[{self.step_name}] {message}", extra={"extra_fields": self._context()}
        )
