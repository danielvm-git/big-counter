---
bug_id: BUG-7
status: open
severity: low
scope: tests/test_bcp_calculator.py
title: "Script-style test at tests/ root — not pytest; requires live API keys"
---

# BUG-7: `tests/test_bcp_calculator.py` — script, not pytest test

## Problem

`tests/test_bcp_calculator.py` is structured as a **standalone script** with `def main()` and `if __name__ == "__main__": main()`, not as pytest test functions. It also:

- Creates a real `BCPCalculator(logger)` without injecting a `FakePromptHandler`
- Requires live LLM API keys in `.env`
- Writes output to `tests/output/` directory
- Uses `argparse` for an `--executions` flag (multi-run stability test)

When run via `pytest`, it gets collected as 0 tests (no `def test_*` functions) and then callers get confused.

## Expected Fix

Either:
- **A)** Move to `scripts/stability_test.py` (it's a utility script, not a unit test)
- **B)** Refactor into pytest tests using `FakePromptHandler` (like `tests/unit/test_bcp_calculator.py`)

Option A is minimal — just rename and move. The functionality (multi-run stability testing) is valuable for Phase 5 of our PLAN.md.

## Resolution

**Fixed:** 2026-07-02
**Root cause confirmed:** Script-style stability testing utility lived at `tests/test_bcp_calculator.py`, misleading pytest (collects 0 tests) and requiring live API keys.
**Fix applied:** Moved to `scripts/stability_test.py` — clear separation from test suite.
**Hardening added:** None needed — file relocation is self-documenting.
**Evidence:** `pytest tests/` collects 17 tests (no script interference).
**Commit:** `refactor(tests): move stability test script from tests/ to scripts/`
