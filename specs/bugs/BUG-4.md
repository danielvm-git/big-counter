---
bug_id: BUG-4
status: open
severity: medium
scope: src/bcp/bcp_calculator.py
title: "10 mypy type errors — untyped `response` variable cascade + `step['name']` typed as `object`"
---

# BUG-4: `bcp_calculator.py` — type errors from untyped variable cascade

## Problem

`mypy src/bcp/bcp_calculator.py` reports 10 errors, nearly all cascading from two root causes:

### Root cause 1: `response = {}` has no type annotation (line 109)

`response` is initialized as `{}` (inferred as `dict[<nothing>, <nothing>]`), then later assigned `list[dict]` and used in operations like `response.get("Static", 0) / 5`. mypy infers `object` for all downstream uses, producing:
- `"object" has no attribute "replace"`
- `Unsupported operand types for / ("object" and "int")`
- `Unsupported target for indexed assignment ("object")`

### Root cause 2: `step["name"]` inferred as `object` (line 103)

The `steps` list uses untyped dicts, so `step["name"]` is `object`, not `str`. This causes `Argument 2 to "StepLogger" has incompatible type "object"; expected "str"`.

Both cascades would be fixed by a single type annotation on `self.steps` and the `response` variable.

## Expected Fix

```python
# Line 109 — add type annotation
response: dict[str, Any] | list[dict[str, Any]] = {}

# Steps list — add TypedDict or explicit annotation
from typing import TypedDict
class StepDef(TypedDict):
    name: str
    prompt_file: str
    required: bool
```

## Resolution

<!-- filled in by validate-fix -->
