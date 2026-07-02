---
bug_id: BUG-10
status: open
severity: low
scope: src/bcp/prompt_handler.py
title: "23% uncovered — error paths in prompt loading and JSON parsing not tested"
---

# BUG-10: `prompt_handler.py` — uncovered error paths

## Problem

`src/bcp/prompt_handler.py` has 77% coverage. The uncovered lines are:

- **Lines 48–56**: `load_prompt()` exception handler (`FileNotFoundError`, etc.) — loading a missing prompt template
- **Lines 74–76**: `render_prompt()` exception handler — Jinja2 rendering failures with bad variables
- **Lines 107, 110–112**: `process_prompt()` JSON decode fallback — when LLM returns malformed JSON that passes `_extract_json_from_response` but fails `json.loads()`

These are all **error recovery paths** that currently have no test coverage, meaning regressions in error handling would go undetected.

## Expected Fix

Add 3 unit tests:
1. `test_load_prompt_file_not_found` — verify graceful error when `.jinja2` file is missing
2. `test_render_prompt_bad_variables` — verify graceful error when template references undefined variable
3. `test_process_prompt_malformed_json` — verify `raw_response` fallback when JSON is syntactically invalid

All can use `FakePromptHandler`/mocked provider — no API keys needed.

## Resolution

<!-- filled in by validate-fix -->
