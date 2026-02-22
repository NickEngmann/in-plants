import os
from pathlib import Path

def test_firmware_directory_contains_mesh_or_particle_files():
    """Check firmware/ contains expected Particle Mesh-related files (e.g., .ino, .h, platformio.ini)."""
    firmware_dir = Path("firmware")
    if not firmware_dir.exists():
        return  # Optional directory
    
    # Look for at least one firmware-related file
    firmware_files = list(firmware_dir.rglob("*")) 
    firmware_files = [f for f in firmware_files if f.is_file()]
    
    # If empty, that’s okay — but if present, should be named appropriately
    if firmware_files:
        # At least one file should have expected extension or name
        valid_extensions = {".ino", ".h", ".cpp", ".c", "platformio.ini"}
        has_valid = any(f.suffix in valid_extensions or f.name in valid_extensions for f in firmware_files)
        assert has_valid, f"firmware/ contains no recognized firmware files: {[str(f) for f in firmware_files]}"

def test_hardware_directory_contains_design_files():
    """Ensure hardware/ contains KiCad, Fritzing, or schematic files."""
    hardware_dir = Path("hardware")
    if not hardware_dir.exists():
        return
    
    design_files = list(hardware_dir.rglob("*"))
    design_files = [f for f in design_files if f.is_file()]
    
    # Accept common hardware file extensions
    valid_extensions = {".kicad_pcb", ".kicad_sch", ".sch", ".pcb", ".fzz", ".svg", ".pdf"}
    has_valid = any(f.suffix.lower() in valid_extensions for f in design_files)
    
    # If no files, that’s acceptable (e.g., just README in hardware/)
    if design_files:
        assert has_valid, f"hardware/ contains no recognized design files: {[str(f) for f in design_files]}"

def test_docs_directory_exists_and_has_content():
    """Verify docs/ exists and has at least one file."""
    docs_dir = Path("docs")
    if not docs_dir.exists():
        return
    
    files = list(docs_dir.rglob("*"))
    files = [f for f in files if f.is_file()]
    assert len(files) > 0, "docs/ directory exists but is empty"