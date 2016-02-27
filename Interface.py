import sys, os, re
from PySide import QtCore, QtGui, QtUiTools
from Tkinter import Tk
from tkFileDialog import askdirectory


class MainInterface(QtGui.QMainWindow):
    def __init__(self):
        super(MainInterface, self).__init__()

        # Construct the UI
        loader = QtUiTools.QUiLoader()
        main_ui_file = QtCore.QFile("AnimationViewer.ui")
        main_ui_file.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(main_ui_file, self)
        self.ui.setWindowTitle('Animation Viewer')
        main_ui_file.close()

        # Connect controllers
        self.ui.pushButtonBrowse.clicked.connect(lambda: self.openBrowser())

    def fillDataAndFillTable(self):
        # Find the file data
        data = self.findAnimationData()
        animations_data = data.keys()
        timeData = data.values()
        self.ui.table_animation.setRowCount(len(animations_data))

        # Print them in the table
        for i in range(len(animations_data)):
            animationName = QtGui.QTableWidgetItem(animations_data[i])
            frameRange = QtGui.QTableWidgetItem("{0}".format(timeData[i][0]))
            frameTime = QtGui.QTableWidgetItem("{0}".format(timeData[i][1]))
            secondsTime = QtGui.QTableWidgetItem("{0}".format(timeData[i][2]))
            self.ui.table_animation.setItem(i, 0, animationName)
            self.ui.table_animation.setItem(i, 1, frameRange)
            self.ui.table_animation.setItem(i, 2, frameTime)
            self.ui.table_animation.setItem(i, 3, secondsTime)

    def showTools(self):
        self.ui.show()

    def findAnimationData(self):
        maya_file_list = {}

        # Finding maya file recursively in the folder
        for root, dirs, files in os.walk(self.file_path):
            for name in files:
                # Making sure it's a .ma file and removing bad extension from the search
                if ".ma" in name and len(name.split(".", 2).pop(-1)) is 2:
                    if name not in maya_file_list and self.findAnimationLength(os.path.join(root, name)):
                        frameRange, frameData, secondsData = self.findAnimationLength(os.path.join(root, name))
                        # Only shows animation that has a length
                        if frameData > 1:
                            maya_file_list[name] = frameRange, frameData, secondsData
        return maya_file_list

    def findAnimationLength(self, file_path):
        with open(file_path, "r") as ascii_file:
            # Regex to find frame content of -min (frame) -max (frame) of ascii maya file.
            for content_lines in ascii_file.readlines():
                regex_content = re.compile("(-min)\s-{0,1}(\d*)\s(-max)\s-{0,1}(\d*)").search(content_lines)

                if regex_content and len(regex_content.group(2)) > 0 and len(regex_content.group(4)) > 0:
                    frame_start, frame_end = float(regex_content.group(2)), float(regex_content.group(4))

                    # Printing the result
                    anim_length = frame_end - frame_start
                    return "{0} - {1}".format(int(frame_start), int(frame_end)), int(anim_length), round(float(anim_length/30), 2)

    def SetProgreeBar(self):
        pass

    def openBrowser(self):
        Tk().withdraw()
        self.file_path = askdirectory()
        self.fillDataAndFillTable()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    AnimationViewer = MainInterface()
    AnimationViewer.showTools()
    sys.exit(app.exec_())
