"""Verify all test files use package-qualified bcp imports."""

import ast
from pathlib import Path


def test_no_bare_bcp_imports_in_tests():
    """No test file should use bare imports from bcp modules.

    BUG-1: bare `from llm_providers import` instead of `from bcp.llm_providers import`
    caused ModuleNotFoundError because bcp modules live under src/bcp/, not at top-level.
    """
    tests_dir = Path(__file__).parent.parent
    bcp_internals = {
        "bcp_calculator",
        "llm_providers",
        "logger",
        "prompt_handler",
    }

    violations: list[str] = []

    for py_file in tests_dir.rglob("*.py"):
        if py_file.name == "__init__.py" or py_file == Path(__file__):
            continue
        tree = ast.parse(py_file.read_text(), filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module in bcp_internals and node.level == 0:
                    # level == 0 means absolute import without leading dots
                    # bcp_internals should be imported as `from bcp.<module> import`
                    violations.append(
                        f"{py_file.relative_to(tests_dir.parent)}: "
                        f"bare `from {node.module} import` "
                        f"→ should be `from bcp.{node.module} import`"
                    )

    assert not violations, f"Found {len(violations)} bare import(s) of bcp modules:\n" + "\n".join(
        violations
    )
