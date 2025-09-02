import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image, ExifTags

Image.MAX_IMAGE_PIXELS = None

METER_TO_INCH = 39.3701

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = f"{ROOT_PATH}/data/input"
OUTPUT_PATH = f"{ROOT_PATH}/data/output"

def get_all_files(input_path):
    try:
        files = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]
        return files
    except Exception as e:
        print(f"Can't get list of files : {e}")
    return []

def add_grid_to_jpeg_matplotlib(image_path, output_path):
    try:
        img = mpimg.imread(image_path)
        plt.imshow(img)
        plt.axis("on")
        plt.grid(color="red", linestyle="--", linewidth=0.5)
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
    except Exception as e:
        print(f"An error occurred: {e}")

def print_meta_data(imp_file):
    try:
        img = Image.open(imp_file)

        if img.getexif():
            exif = {ExifTags.TAGS[k]: v for k, v in img.getexif().items() if k in ExifTags.TAGS}
        print(exif)
    except Exception as e:
        print(f"An error occurred: {e}")

'''
import cv2
import tifffile

# Example function
def rescale_image(path, output_path, scale_factor):
    img = tifffile.imread(path)
    new_size = (int(img.shape[1] * scale_factor), int(img.shape[0] * scale_factor))
    resized = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
    tifffile.imwrite(output_path, resized)

# Example usage
rescale_image("image_025um.tif", "image_rescaled.tif", 0.25)
'''

if __name__ == '__main__' :
    print(f"Input path: {INPUT_PATH}")
    print(f"Output path : {OUTPUT_PATH}")

    input_files = get_all_files(INPUT_PATH)
    for f_img in input_files:
        image_path = f"{INPUT_PATH}/{f_img}"
        print(f"Processing : {f_img}")
       #  print_meta_data(image_path)
        add_grid_to_jpeg_matplotlib(image_path, f"{OUTPUT_PATH}/{f_img}")
