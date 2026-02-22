import pytest
import tempfile
import os
from config import PlantConfig, load_config


class TestHumidityThresholdValidation:
    """Tests for humidity threshold validation in configuration schema."""
    
    def test_valid_humidity_thresholds(self):
        """Test that valid humidity thresholds (0-100) are accepted."""
        config = PlantConfig(
            name="Test Plant",
            humidity_threshold_min=30.0,
            humidity_threshold_max=70.0
        )
        assert config.humidity_threshold_min == 30.0
        assert config.humidity_threshold_max == 70.0
    
    def test_boundary_values_zero(self):
        """Test that 0% humidity threshold is accepted."""
        config = PlantConfig(
            name="Test Plant",
            humidity_threshold_min=0.0,
            humidity_threshold_max=50.0
        )
        assert config.humidity_threshold_min == 0.0
    
    def test_boundary_values_hundred(self):
        """Test that 100% humidity threshold is accepted."""
        config = PlantConfig(
            name="Test Plant",
            humidity_threshold_min=50.0,
            humidity_threshold_max=100.0
        )
        assert config.humidity_threshold_max == 100.0
    
    def test_negative_humidity_min_raises_error(self):
        """Test that negative humidity threshold raises ValueError."""
        with pytest.raises(ValueError, match="humidity_threshold_min must be between 0 and 100"):
            PlantConfig(
                name="Test Plant",
                humidity_threshold_min=-5.0,
                humidity_threshold_max=70.0
            )
    
    def test_negative_humidity_max_raises_error(self):
        """Test that negative humidity threshold raises ValueError."""
        with pytest.raises(ValueError, match="humidity_threshold_max must be between 0 and 100"):
            PlantConfig(
                name="Test Plant",
                humidity_threshold_min=30.0,
                humidity_threshold_max=-10.0
            )
    
    def test_humidity_over_100_min_raises_error(self):
        """Test that humidity >100% raises ValueError."""
        with pytest.raises(ValueError, match="humidity_threshold_min must be between 0 and 100"):
            PlantConfig(
                name="Test Plant",
                humidity_threshold_min=105.0,
                humidity_threshold_max=70.0
            )
    
    def test_humidity_over_100_max_raises_error(self):
        """Test that humidity >100% raises ValueError."""
        with pytest.raises(ValueError, match="humidity_threshold_max must be between 0 and 100"):
            PlantConfig(
                name="Test Plant",
                humidity_threshold_min=30.0,
                humidity_threshold_max=120.0
            )
    
    def test_min_greater_than_max_raises_error(self):
        """Test that min > max raises ValueError."""
        with pytest.raises(ValueError, match="humidity_threshold_min.*cannot be greater than.*humidity_threshold_max"):
            PlantConfig(
                name="Test Plant",
                humidity_threshold_min=80.0,
                humidity_threshold_max=60.0
            )
    
    def test_integer_humidity_values_accepted(self):
        """Test that integer humidity values are accepted."""
        config = PlantConfig(
            name="Test Plant",
            humidity_threshold_min=40,
            humidity_threshold_max=80
        )
        assert config.humidity_threshold_min == 40.0
        assert config.humidity_threshold_max == 80.0
    
    def test_load_config_with_valid_humidity_thresholds(self):
        """Test loading config file with valid humidity thresholds."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
plants:
  - name: Fern
    humidity_threshold_min: 40
    humidity_threshold_max: 80
""")
            temp_path = f.name
        
        try:
            configs = load_config(temp_path)
            assert len(configs) == 1
            assert configs[0].humidity_threshold_min == 40.0
            assert configs[0].humidity_threshold_max == 80.0
        finally:
            os.unlink(temp_path)
    
    def test_load_config_with_negative_humidity_raises_error(self):
        """Test that loading config with negative humidity raises ValueError."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
plants:
  - name: Cactus
    humidity_threshold_min: -10
    humidity_threshold_max: 50
""")
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError, match="humidity_threshold_min must be between 0 and 100"):
                load_config(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_load_config_with_humidity_over_100_raises_error(self):
        """Test that loading config with humidity >100 raises ValueError."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
plants:
  - name: Orchid
    humidity_threshold_min: 30
    humidity_threshold_max: 150
""")
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError, match="humidity_threshold_max must be between 0 and 100"):
                load_config(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_load_config_with_min_greater_than_max_raises_error(self):
        """Test that loading config with min > max raises ValueError."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
plants:
  - name: Bromeliad
    humidity_threshold_min: 70
    humidity_threshold_max: 50
""")
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError, match="humidity_threshold_min.*cannot be greater than"):
                load_config(temp_path)
        finally:
            os.unlink(temp_path)