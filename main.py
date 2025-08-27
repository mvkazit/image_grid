import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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
        #plt.show()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
    except FileNotFoundError:
        print(f"Error: Image not found at {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__' :
    root_path = "/Users/mvkazit/ImageGrid/pythonProject1"
    input_path = f"{root_path}/images/"
    output_path = f"{root_path}/output/"

    input_files = get_all_files(input_path)
    for f_img in input_files:
        print(f"Processing : {f_img}")
        add_grid_to_jpeg_matplotlib(f"{input_path}{f_img}", f"{output_path}{f_img}")
