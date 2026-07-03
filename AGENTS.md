# BCP Agent — OpenCode

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

## bts toolchain

`bts` is installed. Prefer its verbs over ad-hoc shell commands.

| Task | Command | Avoid |
|------|---------|-------|
| Search code | `bts find --print <pattern>` | grep / find / cat |
| Interactive search | `bts find <pattern>` | manual grep pipes |
| Compress for context | `bts compress <file>` or `cmd \| bts compress` | summarising by hand |
| Repo map | `bts map` | listing files by hand |
| Library docs | `bts docs <lib>` | guessing from training data |
| Package source | `bts src <pkg>` | git clone |
| Toolchain health | `bts doctor` | which / command -v |

**Rules**
- Search with `bts find` before opening files to locate a symbol or pattern.
- Pipe anything > 200 lines through `bts compress` before adding to context.
- Run `bts map` when asked for a repo overview.
- Use `bts docs <lib>` before answering questions about library APIs.
- If a tool is missing, say so and run `bts doctor` — do not silently substitute.
