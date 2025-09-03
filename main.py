import os
import time

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import xml.etree.ElementTree as ET
import tifffile
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

MM_TO_INCHES = 1/25.4
M_TO_INCHES = 39.37
M_TO_MKM = 1.0e+6
GRID_SPACING = 100

EXT_JPG = '.jpeg'
EXT_TIF = '.tif'
EXT_XML = '.xml'

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = f"{ROOT_PATH}/data/input"
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
    DPI = 1200
    try:
        img = Image.open(image_path)
        fig, ax = plt.subplots()

        if not (imp_prop["width"]["unit"] == "m" and imp_prop["height"]["unit"]  == "m"):
            print("Error !! Unknow Units")
            exit(0)

        physical_width = imp_prop["width"]["real"] * M_TO_MKM
        physical_height = imp_prop["height"]["real"] * M_TO_MKM

        extent = [0, physical_width, 0, physical_height]
        ax.imshow(img, extent=extent, origin='lower')

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

def save_crop(img, image_path, x, y, idx):
    output_path = image_path.replace(EXT_JPG, f"_crop_{x}_{y}_{idx}{EXT_JPG}")
    print(f"Saving {output_path}")
    img.save(output_path)

def image_crop(input_file, output_file, imp_prop, x, y):

    img = Image.open(input_file)

    physical_width = imp_prop["width"]["real"] * M_TO_MKM
    pixel_per_mkm = imp_prop["width"]["pixels"]  / physical_width
    map = [[1,1,1,1], [1,1,0,0],[0,1,1,0],[1,0,0,1], [0,0,1,1]]
    # 0 - all four regions
    # 1, 2
    # 3, 4

    for i in range(0, 5):
        cropped_region = ((x - GRID_SPACING * map[i][0]) * pixel_per_mkm,
                          (y - GRID_SPACING * map[i][1]) * pixel_per_mkm,
                          (x + GRID_SPACING * map[i][2]) * pixel_per_mkm,
                          (y + GRID_SPACING * map[i][3]) * pixel_per_mkm)
        cropped_img = img.crop(cropped_region)
        save_crop(cropped_img, output_file, x, y, i)


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

    print(f"Save to {output_jpeg}")

if __name__ == '__main__' :
    print(f"Input path: {INPUT_PATH}")
    print(f"Output path : {OUTPUT_PATH}")

    input_files = get_all_files(INPUT_PATH)
    for file_name in input_files:
        image_path = f"{INPUT_PATH}/{file_name}"
        if file_name.endswith(EXT_TIF):
            if not (file_name.replace(EXT_TIF, EXT_JPG) in input_files):
                tiff_to_jpeg(image_path, f"{INPUT_PATH}/{file_name.replace(EXT_TIF, EXT_JPG)}")
                input_files.append(f"{file_name.replace(EXT_TIF, EXT_JPG)}")
                time.sleep(1)
        if file_name.endswith(EXT_JPG):
            xml_path = f"{INPUT_PATH}/{file_name.replace(EXT_JPG, EXT_XML)}"
            print(f"Reading JPEG : {image_path}")
            print(f"Reading XML : {xml_path}")
            img_props = get_image_dimensions(xml_path, image_path)
            print(img_props)
            add_grid_to_jpeg_matplotlib(image_path, f"{OUTPUT_PATH}/{file_name}", img_props)

            points = [[700, 800],[1500, 700]]
            for p in points:
                image_crop(image_path,  f"{OUTPUT_PATH}/{file_name}", img_props, p[0], p[1])
