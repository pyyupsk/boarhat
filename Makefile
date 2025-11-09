.PHONY: help install dev lint format typecheck check test clean

# Colors for echo -e
BLUE := \\033[0;34m
GREEN := \\033[0;32m
YELLOW := \\033[0;33m
RED := \\033[0;31m
NC := \\033[0m

help: ## Show this help message
	@echo -e "$(BLUE)Available commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[0;32m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	@echo -e "$(BLUE)Installing dependencies...$(NC)"
	@uv sync

dev: ## Install dev dependencies
	@echo -e "$(BLUE)Installing dev dependencies...$(NC)"
	@uv sync --all-extras

lint: ## Run linter (ruff check)
	@echo -e "$(BLUE)Running linter...$(NC)"
	@uv run ruff check src/

lint-fix: ## Run linter with auto-fix
	@echo -e "$(BLUE)Running linter with auto-fix...$(NC)"
	@uv run ruff check --fix src/

format: ## Format code with ruff
	@echo -e "$(BLUE)Formatting code...$(NC)"
	@uv run ruff format src/

format-check: ## Check code formatting
	@echo -e "$(BLUE)Checking code formatting...$(NC)"
	@uv run ruff format --check src/

typecheck: ## Run type checker (mypy)
	@echo -e "$(BLUE)Running type checker...$(NC)"
	@uv run mypy src/ || echo -e "$(YELLOW)⚠ Type check warnings (non-blocking)$(NC)"

check: lint format-check ## Run all checks (lint, format)
	@echo -e "$(GREEN)✓ All checks passed!$(NC)"

check-strict: lint format-check typecheck ## Run all checks including strict typecheck
	@echo -e "$(GREEN)✓ All strict checks passed!$(NC)"

fix: lint-fix format ## Fix linting and formatting issues
	@echo -e "$(GREEN)✓ Code fixed!$(NC)"

test: ## Run tests (placeholder)
	@echo "$(YELLOW)⚠ No tests configured yet$(NC)"

clean: ## Clean cache files
	@echo "$(BLUE)Cleaning cache files...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@echo "$(GREEN)✓ Cache cleaned!$(NC)"
