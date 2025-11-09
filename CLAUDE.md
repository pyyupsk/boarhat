# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**boarhat** is a Python project managed with **uv** (Astral's fast Python package manager). The project uses Python >=3.10.

## Project Structure

```text
boarhat/
├── src/
│   └── main.py       # Main entry point
├── pyproject.toml    # Project configuration and dependencies
└── .venv/            # Virtual environment (auto-managed by uv)
```

## Essential Commands

All commands use `uv` - never use pip or manual venv activation.

### Running the Project

```bash
uv run python src/main.py
```

### Dependency Management

```bash
uv add <package>          # Add a dependency
uv add --dev <package>    # Add a dev dependency (e.g., pytest, ruff)
uv remove <package>       # Remove a dependency
uv sync                   # Install/sync all dependencies
uv lock                   # Update lockfile
```

### Development Workflow

When adding new features or modules:

- Place Python modules in `src/`
- Run code with `uv run python src/<module>.py`
- For scripts, consider adding to `[tool.uv.scripts]` in pyproject.toml

### Python Version

The project requires Python >=3.10. To use a specific version:

```bash
uv python install 3.12    # Install specific version
```

Then update `pyproject.toml` if needed:

```toml
[tool.uv]
python = "3.12"
```

## Notes for Claude Code

- Always use `uv run` to execute Python code in the project context
- Add dependencies via `uv add` to ensure they're tracked in pyproject.toml
- The project is in early stages - suggest appropriate project structure improvements as features are added
- When tests are added, use a testing framework like pytest (install via `uv add --dev pytest`)
- For code quality tools, recommend ruff (install via `uv add --dev ruff`)
