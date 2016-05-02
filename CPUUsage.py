import sys
import psutil
from PySide import QtGui, QtCore, QtUiTools


class CPUWorker(QtCore.QObject):
    """
    Function to be threaded to send cpu usage
    """
    cpuList = QtCore.Signal(object)

    def work(self):
        """
        Return a list of CPU usage in percent
        """
        while True:
            cpuPercent = psutil.cpu_percent(interval=1, percpu=True)
            self.cpuList.emit(cpuPercent)

    def cpuCount(self):
        """
        Return a list of CPU count in processor
        """
        return psutil.cpu_count()


class MainInterface(QtGui.QWidget):
    """
    Main Ui Interface
    """
    def __init__(self):
        super(MainInterface, self).__init__()

        # === Ui Loader === #
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile("SysStatWatcher.ui")
        file.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(file, self)
        file.close()

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.ui)
        self.setLayout(layout)
        self.resize(self.ui.width(), self.ui.height())

        # === Threading worker, need to find a way to kill it when closing app. === #
        self.cpuThread = QtCore.QThread()
        self.cpuWorker = CPUWorker()
        self.cpuWorker.moveToThread(self.cpuThread)
        self.connect(self.cpuThread, QtCore.SIGNAL("started()"), self.cpuWorker, QtCore.SLOT("work()"))
        self.cpuThread.start()

        self.cpuWorker.cpuList.connect(self.updateProgressCpuBar)

        # === Populating QVBoxLayout code wise due to random number of core. === #
        self.lCore = self.createProgressBar()
        for progressBar in range(len(self.lCore)):
            self.lCore[progressBar].setValue(0)
            barLabel = QtGui.QLabel()
            barLabel.setText("CPU" + " " + str(progressBar + 1))
            self.ui.verticalLayout_CPUHolder.addWidget(barLabel)
            self.ui.verticalLayout_CPUHolder.addWidget(self.lCore[progressBar])
        self.ui.verticalLayout_CPUHolder.addStretch(1)

    def createProgressBar(self):
        """
        Populating progress bar list depending on cpu count.
        """
        lCore = []
        for core in range(self.cpuWorker.cpuCount()):
            progressBar = QtGui.QProgressBar()
            progressBar.setAlignment(QtCore.Qt.AlignCenter)
            lCore.append(progressBar)
        return lCore

    def updateProgressCpuBar(self, value):
        """
        Value taken from signal and updating progress bar
        """
        for i in range(len(self.lCore)):
            self.lCore[i].setValue(value[i])


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    tool = MainInterface()
    tool.show()
    sys.exit(app.exec_())

