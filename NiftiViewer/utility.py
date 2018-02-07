import nibabel as nib
import numpy as np
import xml.etree.ElementTree as ET
from matplotlib.colors import LinearSegmentedColormap
nib.Nifti1Header.quaternion_threshold = - np.finfo(np.float32).eps * 10 # lowers threshold to read NIFTI


def importNIFTI_MICCAI(filename):
    """Imports data from the MICCAI dataset saved in NIFTI files

    Data in the MICCAI dataset is organized as follows:
    X = Right -> Left
    Y = Top -> Bottom
    Z = Back -> Front

    Args:
        filename (string): filename and path to the NIFTI file

    Returns:
        data (3D numpy): the 3d volume of the image
        hdr_data: header of the NIFTI file
    """
    img_mri = nib.load(filename)
    data = img_mri.get_data()
    hdr_data = img_mri.header
    return data, hdr_data

def importLabelDescr(filepath):
    """Import the labels from the xml file included with the MICCAI competition

    The xml file contains three fields for each entry
    - Name: name of the brain region
    - Number: label id
    - RGBColor: the associated color for plotting

    Args:
        filepath: location of the xml file

    Returns:
        label_descr: decription of the labels
        mycmap: custom color map for the labels
    """
    # Get to the root of the xml file.
    root = ET.parse('data\\1000_3_glm_LabelMap.xml').getroot()

    label_descr = {}
    # The colormap function in python needs an explicit 0 and 1 limits.
    colors = [(0, [0, 0, 0])]
    for child in root:
        id = int(child[1].text) / 255
        color = child[2].text.split(" ")
        color = [int(x) / 255 for x in color]
        colors.append((id, color))
        # The description of the labels, [[id, name, color], ...]
        label_descr[str(child[1].text)] = (int(child[1].text), child[0].text, color)
        print(child[0].text + '  ' + child[1].text + '  (' + child[2].text + ')')
    colors.append((1, (1, 1, 1)))

    # Sort the color list
    colors = sorted(colors, key=lambda x: x[0])
    # Create the colormap
    mycmap = LinearSegmentedColormap.from_list('my_colormap', colors)

    return label_descr, mycmap