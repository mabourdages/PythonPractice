import os, sys, re
from PySide.QtCore import QFile
from PySide.QtGui import QApplication
from PySide.QtUiTools import QUiLoader
from PySide import QtGui
from pysideuic import compileUi

temp_path = r"C:\ProjectPersonnel\trunk\towergame\GameAssets\Assets\Character\Hero\Animation"


def find_maya_files(temp_path):
    for root, folders, files in os.walk(temp_path):
        for file in files:
            if re.compile("\w\.ma*$").search(file):
                print file


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Test")

        loader = QUiLoader()
        ui_file = QFile(r"C:\Users\Marc\Documents\PycharmProjects\PythonPractice\AnimationViewer.ui")
        ui_file.open(QFile.ReadOnly)
        mainWindow = loader.load(ui_file, self)
        ui_file.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    animation_viewer = MainWindow()
    animation_viewer.show()

    sys.exit(app.exec_())

