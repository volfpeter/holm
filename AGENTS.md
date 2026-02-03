## General

Unless explicitly requested:

- **Do NOT** commit
- **Do NOT** write tests
- **Do NOT** run code or applications

**NEVER push code**

**Never install anything**

**ASK** questions if something is unclear or ambiguous

Always aim for **simplicity**, **clarity**, be challenging to achieve this if needed

## Commands

- `uv run poe check` - Run format, lint, and mypy checks
- `uv run poe format` - Check formatting with ruff
- `uv run poe format-fix` - Fix formatting
- `uv run poe lint` - Run ruff linter
- `uv run poe lint-fix` - Fix ruff issues
- `uv run poe mypy` - Run mypy type checking
- `uv run poe test` - Run all tests
- `uv run poe test tests/<test_file>` - Run specific test file

## Code style

- Line length: 108 characters
- Use `from __future__ import annotations` at top when necessary
- Import order: `__future__`, stdlib, third-party, local
- Use `collections.abc` for instead of `typing` where possible
- Dataclasses: `@dataclass(frozen=True, kw_only=True, slots=True)`
- Private functions/attributes: leading underscore
- No comments unless explicitly requested
- Type hints required (`mypy` strict mode)
- Use `TypeAlias` for type aliases
- Tests: use `pytest.mark.parametrize`
- FastAPI patterns for dependencies and error handling

## Coding

- Study related code before making changes to fully **understand the context**
- Try to **remove all unavoidable complexity** from the task before you start coding, **ask challenging questions if needed**
- Do everything to **simplify** solutions and remove all unnecessary complexity from the produced code
- Write clean, modular, readable code
- Prefer composition, dependency injection
- Look for general, powerful, clear abstractions
- Remember the **Zen of Python**
