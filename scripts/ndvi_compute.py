import rasterio
import numpy as np

red_path = r"LC08_L2SP_027039_20250731_20250807_02_T1_SR_B4.TIF"   # Red
nir_path = r"LC08_L2SP_027039_20250731_20250807_02_T1_SR_B5.TIF"   # NIR

with rasterio.open(red_path) as red_src:
    red = red_src.read(1).astype("float32")
    profile = red_src.profile
    
with rasterio.open(nir_path) as nir_src:
    nir = nir_src.read(1).astype("float32")

# Avoid division by zero
ndvi = (nir - red) / (nir + red + 1e-6)

# Save NDVI raster
profile.update(dtype=rasterio.float32)

out_path = "NDVI.tif"
with rasterio.open(out_path, "w", **profile) as dst:
    dst.write(ndvi.astype(np.float32), 1)

print("Saved:", out_path)
