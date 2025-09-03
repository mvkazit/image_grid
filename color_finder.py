import cv2
import numpy as np

IMAGE = "/Users/mvkazit/src/image_grid/data/output/WT.995.M.40X.08.26.2025_WT.995.M.CortexMotor B.08.26.2025_crop_1500_700_2.jpeg"

def calc_pct(image_path, lower_hsv, upper_hsv):
    img = cv2.imread(image_path)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, np.array(lower_hsv), np.array(upper_hsv))
    target_color_pxl = np.sum(mask == 255)
    total_pxl = img.shape[0] * img.shape[1]
    pct = 100 * ( target_color_pxl/total_pxl)
    return pct

if __name__ == '__main__' :
    # https://www.selecolor.com/en/hsv-color-picker/
    green_pct = calc_pct(IMAGE, (35, 50, 50), (85, 255, 255))
    print(f"Green {green_pct:.3f} %")

    blue_pct = calc_pct(IMAGE, (90, 50, 50), (130, 255, 255))
    print(f"Blue {blue_pct:.3f} %")

    orange_pct = calc_pct(IMAGE, (5, 100, 100), (20, 255, 255))
    print(f"Orange {orange_pct:.3f} %")
