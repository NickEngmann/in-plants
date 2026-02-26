"""Auto-generated conftest.py -- stubs for Arduino/embedded C testing.

Strategy: Arduino .ino/.cpp files can't be imported in Python, so we test by
re-implementing the core algorithms (state machines, math, protocol encoding,
parsers) in Python and verifying them with pytest. The conftest provides mock
serial and common helper dependencies.
"""
import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Add repo root to path so test files can import source modules
sys.path.insert(0, '')

# Mock common Arduino Python helper dependencies
for mod_name in ['serial', 'serial.tools', 'serial.tools.list_ports',
                 'pyserial', 'pyfirmata', 'pyfirmata2']:
    sys.modules[mod_name] = MagicMock()


class ArduinoConstants:
    """Provides Arduino-style constants for Python re-implementations."""
    HIGH = 1
    LOW = 0
    INPUT = 0
    OUTPUT = 1
    INPUT_PULLUP = 2
    A0, A1, A2, A3, A4, A5 = range(14, 20)

    @staticmethod
    def map_value(x, in_min, in_max, out_min, out_max):
        """Arduino map() function."""
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    @staticmethod
    def constrain(x, a, b):
        """Arduino constrain() function."""
        return max(a, min(x, b))


@pytest.fixture
def arduino():
    """Provides Arduino-like constants and helpers for testing re-implemented logic."""
    return ArduinoConstants()
