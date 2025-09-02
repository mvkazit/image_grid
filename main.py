import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.ticker as ticker
import xml.etree.ElementTree as ET
from PIL import Image
import numpy as np

Image.MAX_IMAGE_PIXELS = None

MM_TO_INCHES = 1/25.4
M_TO_INCHES = 39.37
M_TO_MKM = 1.0e+6

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = f"{ROOT_PATH}/data/input_1"
OUTPUT_PATH = f"{ROOT_PATH}/data/output"

def convert_to_inches(value, from_units="m"):
    if from_units == "mm":
        return value * MM_TO_INCHES
    if from_units == "m":
        return value * M_TO_INCHES

def get_all_files(input_path):
    try:
        files = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]
        return files
    except Exception as e:
        print(f"Can't get list of files : {e}")
    return []

def add_grid_to_jpeg_matplotlib(image_path, output_path, imp_prop):
    GRID_SPACING = 100
    DPI = 1200
    try:
        img = Image.open(image_path)
        img_array = np.array(img)
        fig, ax = plt.subplots()

        physical_width = imp_prop["width"]["real"] * M_TO_MKM
        physical_height = imp_prop["height"]["real"] * M_TO_MKM

        extent = [0, physical_width, 0, physical_height]
        ax.imshow(img_array, extent=extent, origin='lower')

        major_tick = ticker.MultipleLocator(base=GRID_SPACING)
        ax.xaxis.set_major_locator(major_tick)
        ax.set_xlabel('mkm')
        ax.tick_params(axis='x', labelrotation=90, labelsize=7)

        ax.yaxis.set_major_locator(major_tick)
        ax.tick_params(axis='y',  labelsize=7)
        ax.set_ylabel('mkm')
        ax.invert_yaxis()

        ax.set_title('10 mkm Grid Overlay')
        ax.grid(which='major', linestyle='--', color='red', alpha=0.6)

        #plt.show()

        plt.savefig(output_path, dpi=DPI, bbox_inches="tight")
    except Exception as e:
        print(f"Can't build grid: {e}")

def get_image_dimensions(xml_path, image_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        dimensions = root.find('Image/ImageDescription/Dimensions')
        prop = [x .attrib for x in dimensions]

        img = Image.open(image_path)
        width_real = max(prop[0]['Length'], prop[1]['Length'])
        height_real = min(prop[0]['Length'], prop[1]['Length'])
        if img.width < img.height:
            width_real, height_real = height_real, width_real

        return {
            "width" : {
                "real" : float(width_real),
                "unit" : prop[0 if width_real == prop[0]['Length'] else 1]["Unit"],
                "pixels" : img.width
            },
            "height" : {
                "real" : float(height_real),
                "unit" : prop[0 if height_real == prop[0]['Length'] else 1]["Unit"],
                "pixels": img.height
            }
        }
    except Exception as e:
        print(f"Failed to read XML file: {e}")

def image_crop(image_path, output_path, imp_prop, left, upper, right, lower):
    img = Image.open(image_path)

    physical_width = imp_prop["width"]["real"] * M_TO_MKM
    pixel_per_mkm = imp_prop["width"]["pixels"]  / physical_width

    cropped_region = (left*pixel_per_mkm, upper*pixel_per_mkm, right*pixel_per_mkm, lower*pixel_per_mkm)
    cropped_img = img.crop(cropped_region)
    cropped_img.save(output_path)

if __name__ == '__main__' :
    print(f"Input path: {INPUT_PATH}")
    print(f"Output path : {OUTPUT_PATH}")

    input_files = get_all_files(INPUT_PATH)
    for file_name in input_files:
        if file_name.endswith((".jpeg", ".jpg")) :
            image_path = f"{INPUT_PATH}/{file_name}"
            xml_path = f"{INPUT_PATH}/{file_name.replace('.jpeg', '.xml')}"
            print(f"Reading JPEG : {image_path}")
            print(f"Reading XML : {xml_path}")
            img_props = get_image_dimensions(xml_path, image_path)
            print(img_props)
            add_grid_to_jpeg_matplotlib(image_path, f"{OUTPUT_PATH}/{file_name}", img_props)
            # getting sub image - (200, 1700) to (800, 1400)
            image_crop(image_path, f"{OUTPUT_PATH}/crop_{file_name}", img_props, 1000, 500, 1700, 800)
