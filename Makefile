.PHONY: setup engine-install test lint type verify format clean

# Detect python command
PYTHON := python3
UV := $(shell command -v uv 2> /dev/null)

setup:
	@echo "🦄 Setting up KALDRA Unicorn Environment..."
ifndef UV
	@echo "Installing uv..."
	$(PYTHON) -m pip install uv
endif
	@echo "Syncing dependencies..."
	uv sync
	# Ensure git hooks
	uv run pre-commit install || true

engine-install:
	@echo "🔧 Installing kaldra_engine (Editable)..."
	uv pip install -e packages/engine

test:
	@echo "🧪 Running Tests..."
	uv run pytest -q

lint:
	@echo "🧹 Running Linter (Ruff)..."
	uv run ruff check .

format:
	@echo "✨ Formatting Code (Ruff)..."
	uv run ruff format .

type:
	@echo "🧠 Running Typecheck (Pyright)..."
	uv run pyright

verify:
	@echo "🛡️ Running Full Verification..."
	./scripts/verify.sh

clean:
	@echo "🗑️ Cleaning artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .ruff_cache .pytest_cache .pytype
