---
bug_id: BUG-9
status: open
severity: low
scope: run_mcp_http_server.py
title: "Duplicate `calculate_bcp` function definitions"
---

# BUG-9: `run_mcp_http_server.py` — duplicate function definitions

## Problem

`run_mcp_http_server.py` defines two `calculate_bcp` functions:

- **Line 32**: Simple version — 2 params (`story_content`, `provider`), inside `build_server()`
- **Line 108**: Extended version — 9 params with provider overrides (`api_key`, `model_name`, `flow_*`), inside `main()`

The `build_server()` function creates an MCP server with the simple version, but `main()` creates a different MCP server with the extended version. The `build_server()` function is never called from `main()` — it's dead code.

## Expected Fix

Remove the unused `build_server()` function and its inner `calculate_bcp`. The `main()` function's extended version (line 108) is the one actually used when the script runs.

## Resolution

<!-- filled in by validate-fix -->
