import os
from PIL import Image
import tifffile
import imagecodecs
import numpy as np


def tiff_to_jpeg(input_tiff, output_jpeg):
    tiff_data = tifffile.imread(input_tiff)
    print(f"Read {input_tiff}")
    if tiff_data.ndim == 3 and tiff_data.shape[2] == 4: # RGBA
        tiff_data = tiff_data[:, :, :3] # Drop alpha channel
        mode = 'RGB'
    elif tiff_data.ndim == 3 and tiff_data.shape[2] == 3: # RGB
        mode = 'RGB'
    elif tiff_data.ndim == 2: # Grayscale
        mode = 'L'
    else:
        raise ValueError("Unsupported TIFF image format for conversion to JPEG.")

    pil_image = Image.fromarray(tiff_data, mode=mode)

    pil_image.save(output_jpeg, quality=90)

    print(f"Save to {output_jpeg}.")

if __name__ == '__main__' :
    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
    INPUT_PATH = f"{ROOT_PATH}/data/input_1"
    tiff_to_jpeg(
        f"{INPUT_PATH}/WT.995.M.40X.08.26.2025_WT.995.M.CortexMotor B.08.26.2025.tif",
    f"{INPUT_PATH}/WT.995.M.40X.08.26.2025_WT.995.M.CortexMotor B.08.26.2025.jpeg")