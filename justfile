# Sync project environment
sync:
    uv sync --frozen --all-packages --all-groups

# Setup project environment
setup: sync
    uv tool install pre-commit
    pre-commit uninstall
    pre-commit install --install-hooks

# Build project packages
build:
    uv build --all-packages --wheel

# Test project packages
test *flags:
    uv run --group test pytest -v {{flags}} {{justfile_directory()}}/packages/plat-common
    uv run --group test pytest -v {{flags}} {{justfile_directory()}}/packages/plat-image

# Lint project packages
lint:
    uv run --group dev mypy .

format:
    uv run --group dev ruff format
