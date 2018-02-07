import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from NiftiViewer.utility import importNIFTI_MICCAI, importLabelDescr
from NiftiViewer.viewNIFTI import ViewNIFTI

# Import the data and the labels
data, hdr_data = importNIFTI_MICCAI('data\\1000_3.nii')
label, hdr_label = importNIFTI_MICCAI('data\\1000_3_glm.nii')

print(data.shape)
print(label.shape)

# Label descriptors
label_descr, mycmap = importLabelDescr('data\\1000_3_glm_LabelMap.xml')

print(label[96, 127, 93])
print(label_descr[str(label[96, 127, 93])][1])

# Open viewer
ViewNIFTI('c', data, label, label_descr, mycmap)