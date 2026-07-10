# Conventions

> Shared rules for all AI agents working on this project.
> Read this before any commit, push, or code generation.

## Git & Workflow

- **Workflow mode: solo-git** — direct commits to `main` are permitted. Pre-commit hooks (black, isort, mypy, pytest) enforce quality gates before every commit. If the project transitions to a team, switch to feature branches + PRs.
- **All commits must follow Conventional Commits:** `<type>(<scope>): <description>`
  - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, `build`.
  - Breaking changes MUST include `BREAKING CHANGE:` footer.
  - Example: `feat(api): add BPC scoring endpoint`
- **Worktrees over branches** — use `kickoff-branch` skill to create isolated worktrees for multi-step features.
- **One commit per logical change** — squash before merging (if using branches).

## Code Standards

- **Functions:** 4–20 lines. If longer, split.
- **Files:** under 300 lines. If longer, split.
- **Names must be grep-able** — unique, specific, searchable. No generic names like `data`, `utils`, `helper`.
- **Tests verify behavior through public interfaces** — test the what, not the how.
- **Boy Scout Rule** — leave files cleaner than you found them.
- **No commented-out code** — delete it. Git history has the original.
- **No console.log in production** — use structured logging.

## Python

- Python 3.10+ required (matching `bcp-agent` baseline).
- Type hints on all function signatures — enforced by `mypy --strict`.
- Use `pathlib.Path` for all filesystem operations, never raw strings.
- Prefer `| None` over `Optional[...]` (PEP 604).
- Error handling: define custom exception classes inheriting from domain base.
- Every public function has a Google-style docstring.
- Use `black` + `isort` for formatting (line-length 100, matching `bcp-agent`).

## Architecture

- **Modules over monoliths** — each module has a single responsibility.
- **Imports:** relative within module, absolute across modules.
- **Dependency injection** for testability — no singleton imports.
- **Input validation** at every adapter boundary.

## Defensive Code

This project uses the following defensive patterns:

| Pattern | When to apply |
|---------|--------------|
| Rate limit | API endpoints, external integrations |
| Retry with backoff | Network calls, database operations |
| Timeout | All I/O operations |
| Graceful degradation | Feature flags, fallback responses |

## Specs Directory

- All planning lives in `specs/`.
- `specs/PLAN.md` — implementation plan for the current task.
- `specs/RELEASE-PLAN.md` — release plan epics.
- `specs/ADRS/` — Architecture Decision Records.
- Read specs/ before writing any code.

## Running Code

| Action | Command |
|--------|---------|
| Run CLI | `python run_cli.py <story.md>` |
| Run API server | `python run_api_server.py` |
| Run MCP (stdio) | `python run_mcp.py` |
| Run MCP (HTTP) | `python run_mcp_http_server.py` |
| Test | `python -m pytest` |
| Test (with coverage) | `python -m pytest --cov=src --cov-report=term-missing` |
| Lint | `black --check . && isort --check-only .` |
| Type check | `mypy src/` |
| Stability test | `python run_stability.py <story.md> --iterations 25` |
