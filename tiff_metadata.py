import tifffile as tf


def extract_tifffile_metadata(filepath):
    try:
        with tf.TiffFile(filepath) as tif:
            print(f"Number of pages: {len(tif.pages)}")
            for i, page in enumerate(tif.pages):
                print(f"\n--- Page {i + 1} Metadata ---")
                print(f"  Shape: {page.shape}")
                print(f"  Dtype: {page.dtype}")
                if page.tags:
                    print("  Tags:")
                    for tag_name, tag_value in page.tags.items():
                        print(f"    {tag_name}: {tag_value.value}")

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__' :
    extract_tifffile_metadata('/Users/mvkazit/src/image_grid/data/WT.995.M.40X.08.26.2025_WT.995.M.CortexMotor B.08.26.2025.tif')
