import xml.etree.ElementTree as ET

def read_dimensions_from_prop(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    dimensions = root.find('Image/ImageDescription/Dimensions')
    prop = [x .attrib for x in dimensions]

    return prop


if __name__ == '__main__' :
    dimensions = read_dimensions_from_prop('/Users/mvkazit/src/image_grid/data/WT.995.M.40X.08.26.2025_WT.995.M.Hippocampus A.08.26.2025.xml')
    print(dimensions)