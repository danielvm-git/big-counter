# BCP Agent — Gemini CLI

Read CONVENTIONS.md before any GitHub or git operation.

## Project
MCP agent that counts Business Complexity Points (BCP) across all 13 dimensions (BCP Plus methodology).
Stack: Python 3.10+ / LangChain

## Commands
| Action | Command |
|--------|---------|
| Run CLI | `python run_cli.py <story.md>` |
| Run API | `python run_api_server.py` |
| Run MCP | `python run_mcp.py` |
| Test | `python -m pytest` |
| Coverage | `python -m pytest --cov=src --cov-report=term-missing` |
| Lint | `black --check . && isort --check-only .` |
| Type check | `mypy src/` |
| Stability | `python run_stability.py <story.md> --iterations 25` |

## Architecture
MCP Server receives requests via the Model Context Protocol, delegates to the BPC Calculator for core domain logic, and returns results. Input Adapters feed data from external sources (Jira, GitHub Issues, etc.) into the pipeline.

## Conventions
- Follow bigpowers principles and conventions
- Functions: 4–20 lines. Files: under 300 lines.
- Names must be grep-able (unique, specific).
- Tests verify behavior through public interfaces.
- Boy Scout Rule: leave files cleaner than you found them.

## Never
- Never push directly to main/master
- Never refactor, rename, or reorganize code outside the task scope
- All commits must follow Conventional Commits
- Never skip tests or type checking

## Agent Rules
- **Workflow Mandate:** You MUST use the bigpowers skills (e.g. `plan-work`, `develop-tdd`, `orchestrate-project`) to perform tasks. DO NOT write code directly in response to a user prompt like "build this feature".
- Read specs/ before writing code.
- All planning and specifications MUST be written to `specs/` (e.g. `specs/PLAN.md`) before any code is generated.
- Write the minimum code that solves the stated problem. Nothing extra.
- Never refactor, rename, or reorganize code outside the task scope.
- Run tests after every change. Show evidence before declaring done.
- One clarifying question beats a wrong assumption baked into 200 lines.
