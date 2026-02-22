# Humidity Threshold Validation

When configuring humidity thresholds, ensure values are realistic to prevent sensor misreads or false alerts.

## Validation Rules

1. **Range Check**: Values must be between 0 and 100 (inclusive)
   - ✅ Valid: `25`, `50.5`, `0`, `100`
   - ❌ Invalid: `-1`, `101`, `150.7`

2. **Order Check**: `min_threshold ≤ max_threshold`
   - ✅ Valid: `min=30, max=70`
   - ❌ Invalid: `min=80, max=60`

3. **Type Check**: Must be numeric (int or float)
   - ❌ Invalid: `"high"`, `null`, `true`

## Example Configuration
