import os
import sys

import pytest

# Ensure repository root and 'src' directory are on sys.path for package imports during tests
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TESTS_DIR)
SRC_DIR = os.path.join(REPO_ROOT, "src")
for p in (REPO_ROOT, SRC_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)


class FakePromptHandler:
    """Test double for PromptHandler — returns pre-canned responses, no LLM calls.

    Use in any test that creates a BCPCalculator to avoid live API dependencies.
    """

    def __init__(self, responses: dict | None = None):
        self._responses = responses or {}
        self.calls: list[tuple[str, dict]] = []

    def process_prompt(self, prompt_file: str, variables: dict) -> dict | list:
        self.calls.append((prompt_file, variables))
        return self._responses.get(prompt_file, {})
