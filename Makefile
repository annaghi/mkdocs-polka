.PHONY: help
.PHONY: build serve compile
.PHONY: install reset upgrade clean
.PHONY: fix

.DEFAULT_GOAL := help

help:
	@echo "Available commands:"
	@echo ""
	@echo "Development:"
	@echo "  build           - Build MkDocs site"
	@echo "  serve           - Start MkDocs dev server"
	@echo "  compile         - Compile Rust extension"
	@echo ""
	@echo "Quality:"
	@echo "  fix             - Auto-format and fix linting"
	@echo ""
	@echo "Setup:"
	@echo "  install         - Install complete development environment"
	@echo "  reset           - Clean and reinitialize environment"
	@echo "  clean           - Clean build artifacts"
	@echo "  upgrade         - Full upgrade cycle (clean + upgrade + reinstall)"



build: compile
	@echo "Building MkDocs site..."
	uv run mkdocs build --strict

serve:
	@echo "Starting MkDocs development server..."
	POLKA_DEBUG=1 uv run mkdocs serve

compile:
	@echo "Compiling Rust extension..."
	uv run maturin develop

fix:
	@echo "Running pre-commit with auto-fix..."
	uv run prek run --all-files

clean:
	@echo "Cleaning build artifacts and caches..."
	rm -rf .venv
	rm -rf .ruff_cache
	rm -rf target
	rm -rf site
	rm -rf dist
	rm uv.lock
	rm Cargo.lock
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.dll" -not -path "./.venv/*" -exec rm -f {} + 2>/dev/null || true
	find . -type f -name "*.so" -not -path "./.venv/*" -exec rm -f {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -exec rm -f {} + 2>/dev/null || true
	find . -type f -name "*.pyo" -exec rm -f {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean complete!"

install:
	@echo "Creating virtual environment..."
	uv venv
	@echo "Syncing dependencies..."
	uv sync --all-groups
	@echo "Installing pre-commit hooks..."
	uv run prek install
	@echo "Building Rust extension..."
	uv run maturin develop
	@echo "Install complete!"

reset: clean install
	@echo "Environment reset complete!"

upgrade: clean py-upgrade prek-upgrade install
	@echo "Upgrading Python dependencies..."
	uv sync --upgrade --all-groups
	@echo "Upgrading pre-commit hooks..."
	uv run prek auto-update
	@echo "Upgrade complete!"
