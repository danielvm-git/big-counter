"""
BCP Calculator Test Script

This script demonstrates three different ways to use the BCP Calculator:
1. Direct SDK usage
2. CLI usage via subprocess
3. API usage via HTTP requests
"""

import json
import logging
import os
from pathlib import Path

from bcp.bcp_calculator import BCPCalculator
from bcp.logger import setup_logger

# Define a test story
TEST_STORY = """
As a user, I want to reset my password so that I can regain access to my account.

Acceptance Criteria:
1. User can request a password reset via email
2. User receives a reset link that expires in 24 hours
3. User can set a new password that meets security requirements
"""


def test_sdk_direct():
    """Test that BCPCalculator returns valid BCP results when given mocked LLM responses."""
    from tests.conftest import FakePromptHandler

    logger = setup_logger(logging.DEBUG)

    responses = {
        "step3_flow_bcp_break_elements.jinja2": {
            "Integrations (Boundaries)": [
                {"Boundary": "Email Service", "Size": "S"},
            ],
            "User View": "Password reset page",
            "Acceptance Criteria": ["User can request reset"],
            "Test Plan": {"GIVEN": "locked out", "WHEN": "reset", "THEN": "access"},
            "Business Narrative": "Allow password resets",
            "Requirements and Business Rules": "Password must meet policy",
        },
        "step4_flow_bcp_boundaries.jinja2": [
            {"Boundary": "Email Service", "Size": "S"},
        ],
        "step5_flow_bcp_interface_elements.jinja2": {
            "Static": 3,
            "Dynamic": 2,
        },
        "step6_flow_bcp_business_rule.jinja2": [
            {"Rule": "Password policy", "Score": 2},
        ],
    }

    calculator = BCPCalculator(
        logger=logger,
        prompt_handler=FakePromptHandler(responses),
    )

    result = calculator.calculate_bcp(TEST_STORY)

    assert "total_bcp" in result
    assert "breakdown" in result
    assert "story_name" in result
    # Boundaries: S=2, UI: ceil(3/5)*3 + ceil(2/5)*5 = 3+5=8, Business: 2 → total 12
    assert result["total_bcp"] == 12


def main():
    """Run all tests."""
    # Test SDK directly
    sdk_result = test_sdk_direct()

    print(f"SDK Total BCP: {sdk_result['total_bcp']}")


if __name__ == "__main__":
    main()
