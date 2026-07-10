# Contributing

## Development setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install
```

## Pre-commit checks

Before committing, pre-commit runs automatically:

- `ruff check .` — linting + import ordering
- `ruff format .` — code formatting
- `mypy src/` — static type checking
- `pytest tests/unit/ -q` — unit tests

Run manually with:

```bash
pre-commit run --all-files
```

## Running tests

```bash
pytest                               # all tests
pytest --cov --cov-report=term-missing  # with coverage
```

## Conventions

See [CONVENTIONS.md](CONVENTIONS.md) for the full coding standards.
