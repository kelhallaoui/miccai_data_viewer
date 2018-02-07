import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib.widgets import Button, TextBox

class gui(object):
    def __init__(self, frame):
        self.frame = frame

        self.textX = frame.slice[0]
        self.textY = frame.slice[1]
        self.textZ = frame.slice[2]

        self.coor = self.frame.slice
        self.view_dir = self.frame.slice_direction

        x = 1

    def next(self, event):
        self.coor[self.view_dir] += 1
        self.coor[self.view_dir] = self.coor[self.view_dir] % self.frame.volume[self.view_dir]
        self.updatePlots()

    def prev(self, event):
        self.coor[self.view_dir] -= 1
        self.coor[self.view_dir] = self.coor[self.view_dir] % self.frame.volume[self.view_dir]
        self.updatePlots()

    def submitSlice(self, text):
        print(text)
        self.coor[self.view_dir] = int(text)
        self.coor[self.view_dir] = self.coor[self.view_dir] % self.frame.volume[self.view_dir]
        self.updatePlots()

    def submitX(self, text):
        self.textX = int(text)

    def submitY(self, text):
        self.textY = int(text)

    def submitZ(self, text):
        self.textZ = int(text)

    def btn_setPoint(self, event):
        print(str(self.textX) + ' ' + str(self.textY) + ' ' + str(self.textZ))

        self.coor[0] = self.textX % self.frame.volume[0]
        self.coor[1] = self.textY % self.frame.volume[1]
        self.coor[2] = self.textZ % self.frame.volume[2]
        self.updatePlots()
        self.setPoint()

    def setPoint(self):
        overlay = np.zeros((self.frame.volume[0], self.frame.volume[1], self.frame.volume[2], 4))
        # Set the color channels
        overlay[self.textX - 2:self.textX + 2, self.textY - 2:self.textY + 2, self.textZ - 2:self.textZ + 2, 0] = 1
        overlay[self.textX - 2:self.textX + 2, self.textY - 2:self.textY + 2, self.textZ - 2:self.textZ + 2, 1] = 1
        overlay[self.textX - 2:self.textX + 2, self.textY - 2:self.textY + 2, self.textZ - 2:self.textZ + 2, 2] = 0
        # Set the transparency channel
        overlay[self.textX-2:self.textX+2, self.textY-2:self.textY+2, self.textZ-2:self.textZ+2, 3] = 0.8
        self.frame.ax_mri.imshow(    np.squeeze(overlay[:, :, self.coor[self.view_dir], :])    )

        temp_label = self.frame.label[self.textX, self.textY, self.textZ]
        temp_descr = self.frame.label_descr[str(temp_label)][1]
        self.frame.text_boxLabel.set_val(temp_descr)

        plt.draw()

    def updatePlots(self):

        if self.view_dir == 0:
            self.frame.ax_mri.imshow(np.transpose(self.frame.data[self.coor[self.view_dir], :, :]), cmap='Greys_r')
            self.frame.ax_mri.set_title('Sagital slice ' + str(self.coor[self.view_dir]))

            self.frame.ax_lab.imshow(np.transpose(self.frame.label[self.coor[self.view_dir], :, :]), cmap=self.frame.cmap)
            self.frame.ax_lab.set_title('Sagital slice ' + str(self.coor[self.view_dir]))

        elif self.view_dir == 1:
            self.frame.ax_mri.imshow(np.transpose(self.frame.data[:, self.coor[self.view_dir], :]), cmap='Greys_r')
            self.frame.ax_mri.set_title('Axial slice ' + str(self.coor[self.view_dir]))

            self.frame.ax_lab.imshow(np.transpose(self.frame.label[:, self.coor[self.view_dir], :]), cmap=self.frame.cmap)
            self.frame.ax_lab.set_title('Axial slice ' + str(self.coor[self.view_dir]))

        elif self.view_dir == 2:
            self.frame.ax_mri.imshow(np.transpose(self.frame.data[:, :, self.coor[self.view_dir]]), cmap='Greys_r')
            self.frame.ax_mri.set_title('Coronal slice ' + str(self.coor[self.view_dir]))

            self.frame.ax_lab.imshow(np.transpose(self.frame.label[:, :, self.coor[self.view_dir]]), cmap=self.frame.cmap)
            self.frame.ax_lab.set_title('Coronal slice ' + str(self.coor[self.view_dir]))

        plt.draw()



class ViewNIFTI(object):

    def __init__(self, slice_dir, data, label, label_descr, cmap):
        # Set option for the slice that will be shown
        if slice_dir == 's':
            self.slice_direction = 0
        elif slice_dir == 'a':
            self.slice_direction = 1
        elif slice_dir == 'c':
            self.slice_direction = 2

        # Register the data, labels, and colormap
        self.volume = data.shape
        self.data = data
        self.label = label
        self.label_descr = label_descr
        self.cmap = cmap

        # Get the initial starting points as the middle of the brain
        self.slice = [data.shape[0] // 2, data.shape[1] // 2, data.shape[2] // 2]

        # Initialize the figure as two axes
        self.fig_mri, (self.ax_mri, self.ax_lab) = plt.subplots(1, 2)
        plt.subplots_adjust(bottom=0.3)

        # Initialize the GUI
        callback = gui(self)
        # Plot the initial brain
        callback.updatePlots()

        axprev = plt.axes([0.7, 0.15, 0.1, 0.075])
        axnext = plt.axes([0.81, 0.15, 0.1, 0.075])
        bnext = Button(axnext, 'Next')
        bnext.on_clicked(callback.next)
        bprev = Button(axprev, 'Previous')
        bprev.on_clicked(callback.prev)

        axbox = plt.axes([0.1, 0.15, 0.3, 0.075])
        text_box = TextBox(axbox, 'Slice', initial=str(self.slice[0]))
        text_box.on_submit(callback.submitSlice)

        axboxX = plt.axes([0.1, 0.05, 0.07, 0.075])
        text_boxX = TextBox(axboxX, 'X ', initial=str(self.slice[0]))
        text_boxX.on_submit(callback.submitX)
        axboxY = plt.axes([0.2, 0.05, 0.07, 0.075])
        text_boxY = TextBox(axboxY, 'Y ', initial=str(self.slice[1]))
        text_boxY.on_submit(callback.submitY)
        axboxZ = plt.axes([0.3, 0.05, 0.07, 0.075])
        text_boxZ = TextBox(axboxZ, 'Z ', initial=str(self.slice[2]))
        text_boxZ.on_submit(callback.submitZ)

        axPoint = plt.axes([0.4, 0.05, 0.11, 0.075])
        bPoint = Button(axPoint, 'Set Point')
        bPoint.on_clicked(callback.btn_setPoint)

        temp_label = label[data.shape[0] // 2, data.shape[1] // 2, data.shape[2] // 2]
        temp_descr = self.label_descr[str(temp_label)][1]
        axLabel = plt.axes([0.7, 0.05, 0.21, 0.075])
        self.text_boxLabel = TextBox(axLabel, 'Label: ', temp_descr)

        plt.show()
