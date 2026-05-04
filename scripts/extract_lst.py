import rasterio
import numpy as np

# Update this filename if needed
input_file = "LC08_L2SP_027039_20250731_20250807_02_T1_ST_B10.TIF"
output_file = "Austin_LST_Celsius.tif"

print("Loading thermal band...")

with rasterio.open(input_file) as src:
    thermal_data = src.read(1).astype(float)
    profile = src.profile

# Pixels with 0 = no data
thermal_data[thermal_data == 0] = np.nan

# USGS L2 ST_B10 is already scaled to Kelvin with scale factor
scale_factor = 0.00341802
add_offset = 149.0

print("Converting from scaled values to Kelvin...")
temp_kelvin = thermal_data * scale_factor + add_offset

# Convert to Celsius
print("Converting Kelvin → Celsius...")
temp_celsius = temp_kelvin - 273.15

# Update profile for output
profile.update(dtype=rasterio.float32)

# Write output file
with rasterio.open(output_file, "w", **profile) as dst:
    dst.write(temp_celsius.astype(rasterio.float32), 1)

print("DONE! Saved:", output_file)

