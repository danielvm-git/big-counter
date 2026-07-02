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

<!-- filled in by validate-fix -->
