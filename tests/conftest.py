# No fixtures needed — tests are standalone and self-contained.
# This file kept for pytest compatibility and future extensibility.
import pytest

def pytest_configure(config):
    # Optional: add markers or custom options
    config.addinivalue_line(
        "markers", "readme: mark tests related to README validation"
    )
    config.addinivalue_line(
        "markers", "structure: mark tests related to project structure"
    )