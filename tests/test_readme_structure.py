import os
import re
from pathlib import Path

# Expected sections in README (common for IoT/hardware projects)
REQUIRED_SECTIONS = [
    r"#\s+.*",  # Title (any H1)
    r"##\s+Overview",
    r"##\s+Hardware",
    r"##\s+Setup",
    r"##\s+Testing",
    r"##\s+Project Structure",
]

def test_readme_exists():
    readme_path = Path("README.md")
    assert readme_path.exists(), "README.md must exist at project root"

def test_readme_has_required_sections():
    readme_path = Path("README.md")
    content = readme_path.read_text(encoding="utf-8")
    
    for pattern in REQUIRED_SECTIONS:
        assert re.search(pattern, content, re.IGNORECASE), \
            f"README.md missing required section matching: {pattern}"

def test_readme_contains_humidity_formula_or_description():
    """Ensure README describes humidity measurement logic (even if pseudo-code)."""
    readme_path = Path("README.md")
    content = readme_path.read_text(encoding="utf-8")
    
    # Look for keywords indicating humidity logic: formula, calculation, sensor, raw, calibrated
    humidity_keywords = [
        r"humidity",
        r"sensor.*value",
        r"raw.*reading",
        r"calibrat",
        r"mapping",
        r"\d+\s*-\s*\d+",
        r"percent",
        r"%"
    ]
    
    found_any = any(re.search(kw, content, re.IGNORECASE) for kw in humidity_keywords)
    assert found_any, "README.md should describe humidity measurement logic or formula"

def test_project_structure_has_expected_directories():
    """Verify key directories exist per typical IoT project layout."""
    expected_dirs = ["docs", "hardware", "firmware"]
    for d in expected_dirs:
        assert Path(d).is_dir(), f"Expected directory '{d}' not found"

def test_readme_does_not_assume_hardware_execution():
    """Ensure README doesn’t claim to run code requiring hardware (e.g., 'pio run --target upload')."""
    readme_path = Path("README.md")
    content = readme_path.read_text(encoding="utf-8")
    
    # Disallow commands that require physical device
    forbidden_patterns = [
        r"pio\s+run\s+--target\s+upload",
        r"particle\s+flash",
        r"dfu-util",
        r"esptool\.py"
    ]
    
    for pattern in forbidden_patterns:
        assert not re.search(pattern, content), \
            f"README.md should not include hardware-deploy commands: {pattern}"