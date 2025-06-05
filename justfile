# Sync project environment
sync:
    uv sync --frozen --all-packages

# Setup project environment
setup: sync
    uv tool install pre-commit
    pre-commit uninstall
    pre-commit install --install-hooks

# Build project packages
build:
    uv build --all-packages --wheel
