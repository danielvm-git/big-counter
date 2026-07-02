---
bug_id: BUG-8
status: open
severity: low
scope: tests/compare_providers.py
title: "Script-style comparison tool at tests/ root — not pytest; requires live API keys"
---

# BUG-8: `tests/compare_providers.py` — script, not pytest test

## Problem

`tests/compare_providers.py` is a **standalone comparison tool** with `def main()` and `if __name__ == "__main__": main()`. It:

- Runs BCP calculations across multiple providers (openai, claude, flow-openai, flow-bedrock)
- Requires `.env` with all provider API keys
- Writes comparison results to JSON/CSV/Excel
- Uses `argparse` flags (`--stories-dir`, `--output-dir`, `--log-level`, `--format`)

Same pattern as BUG-7 — lives in `tests/` but is a utility tool, not a test.

## Expected Fix

Move to `scripts/compare_providers.py`. The `run_comparison.py` entry point at root already wraps it — just needs the target file relocated.

## Resolution

<!-- filled in by validate-fix -->
