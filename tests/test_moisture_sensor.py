"""Test moisture sensor calculations from inplants-argon.ino and inplants-xenon.ino."""
import pytest


def moisture_percentage_from_analog(analog_value):
    """Re-implementation of the moisture percentage calculation from the Arduino code.
    
    Formula: moisture_percentage = (100 - ( (moisture_analog/4095.00) * 100 ))
    This converts a 12-bit ADC reading (0-4095) to moisture percentage.
    Higher analog values = lower moisture (dry soil), lower analog values = higher moisture (wet soil).
    """
    return 100 - ((analog_value / 4095.00) * 100)


class TestMoisturePercentageCalculation:
    """Tests for the moisture percentage calculation algorithm."""
    
    def test_dry_soil(self):
        """Dry soil should give low moisture percentage (high analog reading near 4095)."""
        # Near maximum analog value = dry soil
        assert moisture_percentage_from_analog(4095) == 0.0
        assert moisture_percentage_from_analog(3500) < 15.0
    
    def test_wet_soil(self):
        """Wet soil should give high moisture percentage (low analog reading near 0)."""
        # Near zero analog value = wet soil
        assert moisture_percentage_from_analog(0) == 100.0
        assert moisture_percentage_from_analog(500) > 87.0
    
    def test_medium_moisture(self):
        """Medium moisture should give medium percentage."""
        # Around midpoint
        assert 50 < moisture_percentage_from_analog(2000) < 52
    
    def test_specific_values(self):
        """Test specific calculated values."""
        # 50% moisture should be around 2048 analog value
        assert abs(moisture_percentage_from_analog(2048) - 49.9878) < 0.01
        
        # 75% moisture should be around 1024 analog value
        assert abs(moisture_percentage_from_analog(1024) - 74.9939) < 0.01
        
        # 25% moisture should be around 3072 analog value
        assert abs(moisture_percentage_from_analog(3072) - 24.9756) < 0.01
    
    def test_boundary_conditions(self):
        """Test edge cases and boundary conditions."""
        # Maximum analog value (12-bit max)
        assert moisture_percentage_from_analog(4095) == 0.0
        
        # Zero analog value
        assert moisture_percentage_from_analog(0) == 100.0
        
        # Negative values should give >100% (theoretical, not physically meaningful)
        assert moisture_percentage_from_analog(-100) > 100.0
        
        # Values above 4095 should give negative percentage (theoretical)
        assert moisture_percentage_from_analog(5000) < 0.0


class TestMoistureSensorIntegration:
    """Integration tests simulating real-world scenarios."""
    
    def test_normal_plant_reading(self):
        """Simulate a typical plant reading in optimal range."""
        # Typical optimal reading might be around 2000-2500 analog
        optimal_analog = 2200
        moisture = moisture_percentage_from_analog(optimal_analog)
        assert 46 < moisture < 51
    
    def test_drought_condition(self):
        """Simulate drought condition (very dry soil)."""
        # Dry soil reading
        dry_analog = 3500
        moisture = moisture_percentage_from_analog(dry_analog)
        assert 0 <= moisture <= 15
    
    def test_overwatered_condition(self):
        """Simulate overwatered condition (very wet soil)."""
        # Wet soil reading
        wet_analog = 500
        moisture = moisture_percentage_from_analog(wet_analog)
        assert 87 <= moisture <= 100
    
    def test_threshold_detection(self):
        """Test detection of threshold values for watering alerts."""
        # Threshold at 30% moisture
        threshold_analog = 2866.5  # 30% = 100 - (analog/4095*100) => analog = 2866.5
        moisture = moisture_percentage_from_analog(threshold_analog)
        assert abs(moisture - 30.0) < 0.1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
