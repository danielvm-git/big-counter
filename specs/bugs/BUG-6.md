---
bug_id: BUG-6
status: open
severity: low
scope: src/api/server.py
title: "1 mypy error — `jobs` dict missing type annotation"
---

# BUG-6: `api/server.py` — `jobs` dict missing type annotation

## Problem

`mypy src/api/server.py` reports on line 15:

```
error: Need type annotation for "jobs"
  (hint: "jobs: dict[<type>, <type>] = ...")
```

The module-level `jobs = {}` mutates across requests (background task storage) but has no type annotation, making mypy unable to verify the `job_id`/`status`/`result`/`error` key usage.

## Expected Fix

```python
from typing import Any

jobs: dict[str, dict[str, Any]] = {}
```

One line added.

## Resolution

**Fixed:** 2026-07-02
**Root cause confirmed:** Module-level `jobs = {}` missing type annotation.
**Fix applied:** `jobs: dict[str, dict[str, Any]] = {}`.
**Hardening added:** None needed — type checker now enforces key/value types.
**Evidence:** 0 mypy errors in `src/api/server.py`; 14/14 tests pass.
**Commit:** `fix(types): add type annotation for jobs dict in api server`
