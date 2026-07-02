---
bug_id: BUG-2
status: open
severity: low
scope: tests
title: "tests/test_sdk.py — requires live API credentials (not self-contained)"
---

# BUG-2: `tests/test_sdk.py` — requires live API credentials

## Problem

`pytest tests/test_sdk.py` fails at runtime because `test_sdk_direct()` creates a real `BCPCalculator` with `provider_name="flow-openai"`, which calls the live Flow API without credentials:

```
RuntimeError: Error calling Flow API
```

**Expected:** Test either runs self-contained (no external API calls) or cleanly skips when credentials are absent.
**Actual:** Crashes with opaque `RuntimeError`.
**Reproduction:** `python -m pytest tests/test_sdk.py` from project root (no `.env` file needed to trigger — the test hardcodes flow-openai).

## Root Cause Analysis

The failure chain:
```
test_sdk_direct()
  → BCPCalculator(logger, provider_name="flow-openai")  # hardcoded on line 54
    → PromptHandler(logger, "flow-openai")
      → get_provider("flow-openai", logger)
        → FlowProvider()
          → _get_flow_token()
            → HTTP POST to FLOW_BASE_URL/auth-engine-api/v1/api-key/token
              → crashes: no FLOW_CLIENT_ID/FLOW_CLIENT_SECRET
```

The test is a **live integration test** dressed as a unit test — no mocks, no dependency injection, no skip guard. Contrast with `tests/unit/test_bcp_calculator.py` which injects a `FakePromptHandler` to stay self-contained.

**Risk level:** Low — affects only test infrastructure, no production impact.
**Security impact:** NONE — no security exploit path identified.

## TDD Fix Plan

1. **RED**: Verify the test currently fails with `RuntimeError`
   **GREEN**: Refactor `test_sdk_direct()` to inject a `FakePromptHandler`, making it self-contained (no API calls):
   ```python
   from tests.unit.test_bcp_calculator import FakePromptHandler
   # ... inject fake with mocked responses ...
   ```
   **verify**: `python -m pytest tests/test_sdk.py -v`

2. **REFACTOR**: Extract `FakePromptHandler` to `tests/conftest.py` as a shared fixture so both unit tests and SDK tests can use it without cross-importing.

## Acceptance Criteria

- [ ] `python -m pytest tests/test_sdk.py -v` passes without `.env` file
- [ ] All 14 existing unit tests in `tests/unit/` still pass
- [ ] Test still verifies BCP calculation logic (just mocked, not live)
- [ ] No hardcoded provider name in test body

## Resolution

**Fixed:** 2026-07-02
**Root cause confirmed:** `test_sdk_direct()` created a real `BCPCalculator` with hardcoded `provider_name="flow-openai"`, triggering a live Flow API call without credentials. No mock or skip guard.
**Fix applied:** Injected `FakePromptHandler` (shared test double from `conftest.py`) into `BCPCalculator`, replacing the live provider. Extracted `FakePromptHandler` from `tests/unit/test_bcp_calculator.py` to `tests/conftest.py` so all test files can share it. Added proper assertions: verifies `total_bcp`, `breakdown`, and exact score calculation. Removed unused imports (`requests`, `subprocess`, `time`, `dotenv`).
**Hardening added:** `FakePromptHandler` now lives in shared `conftest.py`, preventing future tests from accidentally using live providers.
**Evidence:** 15/15 tests pass, zero warnings (`python -m pytest tests/ -v`)
**Commit:** `fix(tests): make test_sdk.py self-contained with FakePromptHandler`
