import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class PlantConfig:
    """Configuration for a plant's environment."""
    name: str
    humidity_threshold_min: float
    humidity_threshold_max: float
    
    def __post_init__(self):
        # Validate humidity thresholds are within valid range (0-100%)
        if not (0 <= self.humidity_threshold_min <= 100):
            raise ValueError(
                f"humidity_threshold_min must be between 0 and 100, got {self.humidity_threshold_min}"
            )
        if not (0 <= self.humidity_threshold_max <= 100):
            raise ValueError(
                f"humidity_threshold_max must be between 0 and 100, got {self.humidity_threshold_max}"
            )
        if self.humidity_threshold_min > self.humidity_threshold_max:
            raise ValueError(
                f"humidity_threshold_min ({self.humidity_threshold_min}) cannot be greater than "
                f"humidity_threshold_max ({self.humidity_threshold_max})"
            )


def load_config(config_path: str) -> list[PlantConfig]:
    """
    Load plant configuration from a YAML file.
    
    This function now includes humidity threshold validation to prevent
    invalid values (negative numbers or >100%) from being accepted.
    """
    try:
        import yaml
    except ImportError:
        raise ImportError("PyYAML is required to load configuration files")
    
    with open(config_path, 'r') as f:
        config_data = yaml.safe_load(f)
    
    if not config_data or 'plants' not in config_data:
        raise ValueError("Configuration file must contain a 'plants' section")
    
    plant_configs = []
    for plant_data in config_data['plants']:
        # Extract humidity thresholds with defaults if not specified
        humidity_min = plant_data.get('humidity_threshold_min', 30.0)
        humidity_max = plant_data.get('humidity_threshold_max', 70.0)
        
        # Validate humidity thresholds
        if not isinstance(humidity_min, (int, float)):
            raise ValueError(
                f"humidity_threshold_min must be a number for plant '{plant_data.get('name', 'unknown')}', "
                f"got {type(humidity_min).__name__}"
            )
        if not isinstance(humidity_max, (int, float)):
            raise ValueError(
                f"humidity_threshold_max must be a number for plant '{plant_data.get('name', 'unknown')}', "
                f"got {type(humidity_max).__name__}"
            )
        
        # Create config with validation
        plant_config = PlantConfig(
            name=plant_data.get('name', 'unnamed'),
            humidity_threshold_min=float(humidity_min),
            humidity_threshold_max=float(humidity_max)
        )
        plant_configs.append(plant_config)
    
    return plant_configs