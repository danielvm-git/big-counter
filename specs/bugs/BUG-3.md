---
bug_id: BUG-3
status: open
severity: medium
scope: src/bcp/llm_providers.py
title: "14 mypy type errors — LangChain BaseChatModel subclass signature mismatches + missing annotations"
---

# BUG-3: `llm_providers.py` — type errors from LangChain subclass mismatches

## Problem

`mypy src/bcp/llm_providers.py` reports 14 errors. Three categories:

### A) LangChain `BaseChatModel` subclass signatures don't match supertype (10 errors)

`FlowChatModel` and `FlowBedrockChatModel` override `_llm_type`, `_generate`, and `_stream` with signatures incompatible with `langchain_core.language_models.chat_models.BaseChatModel`:

- `_generate` missing the `run_manager: CallbackManagerForLLMRun | None` parameter
- `_stream` returns `Iterator[dict]` instead of `Iterator[ChatGenerationChunk]` or `Iterator[ChatResult]`
- `_llm_type` return type shadowing

### B) Missing type annotations (3 errors)

- `message_dict` in `_convert_messages_to_bedrock_format` (line 354) — untyped dict
- `stop_sequences` in `FlowBedrockProvider.__init__` (line 480) — list without element type
- `response` variable type cascade

### C) Type narrowing issue (1 error)

- `base_url: str | None` (from `os.environ.get("FLOW_BASE_URL")`) passed to `FlowChatModel(base_url=...)` which expects `str`, not `str | None`

### D) Deprecated kwarg

- `ChatAnthropic(model=...)` on line 114 should be `ChatAnthropic(model_name=...)` (LangChain v1 API change)

## Root Cause

The code was written against an older LangChain version where `BaseChatModel` had different signatures. The LangChain v1 upgrade (in `requirements.txt`) introduced stricter type contracts.

## Expected Fix

- Add `run_manager` parameter to `_generate` and `_stream` overrides
- Fix `_stream` return types to match LangChain v1 signatures
- Add explicit type annotations on untyped variables
- Narrow `base_url` with `assert base_url is not None` or default fallback
- Change `ChatAnthropic(model=...)` → `ChatAnthropic(model_name=...)`

## Resolution

<!-- filled in by validate-fix -->
