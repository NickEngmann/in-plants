# Humidity Threshold Validation Guide

When configuring humidity thresholds for your sensor setup, always validate inputs to prevent invalid values.

## Requirements for Threshold Values

- **Valid range**: 0% to 100% (inclusive)
- **Type**: Numeric (int or float)
- **Relationship**: `min_threshold ≤ max_threshold`

## Common Mistakes to Avoid

| Invalid Value | Why It’s Invalid |
|---------------|------------------|
| `-5` | Humidity cannot be negative |
| `101.2` | Humidity >100% is physically impossible |
| `min=80, max=60` | Minimum > maximum causes logic errors |

## Recommended Workflow

1. Open `config.yaml`
2. Set thresholds within [0, 100]
3. Verify `min ≤ max`
4. Save and test with known humidity levels

> 💡 Tip: Use a hygrometer to calibrate real-world values before finalizing thresholds.