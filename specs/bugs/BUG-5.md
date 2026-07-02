---
bug_id: BUG-5
status: open
severity: low
scope: src/main.py
title: "2 mypy errors — implicit Optional in function parameters"
---

# BUG-5: `main.py` — implicit Optional parameters

## Problem

`mypy src/main.py` reports 2 errors on line 84 in `save_or_print_results`:

```
error: Incompatible default for parameter "output_file"
  (default has type "None", parameter has type "str")
error: Incompatible default for parameter "logger"
  (default has type "None", parameter has type "Logger")
```

PEP 484 prohibits implicit `Optional`. The parameters default to `None` but are typed as `str` and `Logger` without `| None`.

## Expected Fix

```python
def save_or_print_results(
    results: dict[str, Any],
    output_format: str,
    output_file: str | None = None,
    logger: logging.Logger | None = None,
) -> None:
```

Two lines changed: add `| None` to `output_file` and `logger` types.

## Resolution

<!-- filled in by validate-fix -->
