---
bug_id: BUG-1
status: open
severity: medium
scope: tests
title: "tests/test_providers.py — broken module import path"
---

# BUG-1: `tests/test_providers.py` — broken module import path

## Problem

`pytest tests/test_providers.py` cannot even collect tests — crashes at module import with:

```
ModuleNotFoundError: No module named 'llm_providers'
```

**Expected:** `pytest` collects and runs the provider tests.
**Actual:** Import error prevents test discovery entirely.
**Reproduction:** `python -m pytest tests/test_providers.py` from project root.

## Root Cause Analysis

The project uses `setup.py` with `package_dir={"": "src"}`, placing all modules under the `bcp` namespace. The `tests/conftest.py` correctly adds `src/` to `sys.path`, making `bcp.llm_providers` importable. However, `tests/test_providers.py` uses **bare imports** that bypass the namespace:

```python
# Line 10-11 — BROKEN (no bcp. prefix)
from llm_providers import get_provider
from logger import setup_logger
```

Python resolves `llm_providers` as a top-level module, which doesn't exist — it lives at `src/bcp/llm_providers.py`. The `conftest.py` only adds `src/` to the path; it doesn't flatten the `bcp/` directory. Same root cause on the `logger` import.

**Risk level:** Low — affects only test infrastructure, no production impact.
**Security impact:** NONE — no security exploit path identified.

## TDD Fix Plan

1. **RED**: Verify the test file currently fails to import
   **GREEN**: Change lines 10–11 from bare imports to package-qualified imports:
   ```python
   from bcp.llm_providers import get_provider
   from bcp.logger import setup_logger
   ```
   **verify**: `python -m pytest tests/test_providers.py --co`

2. **RED**: (implicit) Verify no other test file has the same pattern
   **GREEN**: Confirm no other bare imports exist
   **verify**: `grep -rn "from llm_providers import\|from logger import" tests/`

## Acceptance Criteria

- [ ] `python -m pytest tests/test_providers.py --co` succeeds (collects tests without ImportError)
- [ ] All 13 existing unit tests in `tests/unit/` still pass
- [ ] No other test files have bare `from llm_providers` or `from logger` imports
- [ ] Change is exactly 2 lines, no side effects

## Resolution

**Fixed:** 2026-07-02
**Root cause confirmed:** Bare imports (`from llm_providers import`) instead of package-qualified (`from bcp.llm_providers import`). Project uses `package_dir={"": "src"}` so modules live under `bcp` namespace.
**Fix applied:** Changed lines 10–11 in `tests/test_providers.py` from bare imports to `from bcp.llm_providers import get_provider` and `from bcp.logger import setup_logger`.
**Hardening added:** `tests/unit/test_guard_bare_imports.py` — AST-based test that scans all test files for bare imports of `bcp` internal modules and fails if found.
**Evidence:** 14/14 tests pass (`python -m pytest tests/unit/ -v`)
**Commit:** `fix(tests): qualify bare imports in test_providers.py with bcp namespace`
