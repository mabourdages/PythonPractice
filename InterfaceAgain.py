import sys, time
from PySide import QtCore, QtGui, QtUiTools
from TableViewUI import Ui_Form


class LoadingBarDelegate(QtGui.QItemDelegate):
    """
    Example of a progress bar delegate
    """
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        value = int(index.data())
        self.progressBar = QtGui.QStyleOptionProgressBarV2()
        self.progressBar.maximum = 100
        self.progressBar.textVisible = True
        self.progressBar.progress = value
        self.progressBar.rect = option.rect
        self.progressBar.text = str(value) + "%"
        self.progressBar.textAlignment = QtCore.Qt.AlignCenter

        QtGui.QApplication.style().drawControl(QtGui.QStyle.CE_ProgressBar, self.progressBar, painter)

    def createEditor(self, parent, option, index):
        editor = QtGui.QProgressBar(parent)
        return editor


class SpinBoxDelegate(QtGui.QItemDelegate):
    """
    Example of a spin box delegate
    """
    def createEditor(self, parent, option, index):
        editor = QtGui.QSpinBox(parent)
        editor.setMinimum(0)
        editor.setMaximum(100)
        return editor

    def setEditorData(self, spinBox, index):
        value = index.model().data(index, QtCore.Qt.EditRole)

        spinBox.setValue(value)

    def setModelData(self, spinBox, model, index):
        spinBox.interpretText()
        value = spinBox.value()

        model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class ComboBoxDelegate(QtGui.QItemDelegate):
    """
    Example of a combo box delegate
    """
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        editor = QtGui.QComboBox(parent)
        li = ["0", "1", "2", "3", "4"]
        editor.addItems(li)

        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        editor.setCurrentIndex(editor.findText(str(value)))

    def setModelData(self, editor, model, index):
        value = editor.currentText()

        model.setData(index, value, QtCore.Qt.EditRole)

    def paint(self, painter, option, index):
        self.parent().openPersistentEditor(index)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, table):
        super(TableModel, self).__init__()
        self.__spinBoxValue = {}
        self.__comboBoxValue = {}
        self.percent = 0
        self.table = table

        for row in range(self.rowCount()):
            self.__spinBoxValue[row] = 0
            self.__comboBoxValue[row] = 0

        self.worker = Worker()
        self.worker.upgradeProgess.connect(self.updateProgress)

    def updateProgress(self, value):
        self.percent = value
        self.table.viewport().update()

    def stopThread(self):
        self.worker.quit()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return 4

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 3

    def data(self, index, role=QtCore.Qt.DisplayRole):
        row = index.row()
        column = index.column()

        if role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole:
            if column == 0:
                return self.__spinBoxValue[row]
            if column == 1:
                return self.__comboBoxValue[row]
            if column == 2:
                return self.percent

    def setData(self, index, value, role):
        row = index.row()
        column = index.column()

        if column == 0:
            self.__spinBoxValue[row] = value
            return self.__spinBoxValue[row]
        if column == 1:
            self.__comboBoxValue[row] = int(value)
            return self.__comboBoxValue[row]

    def flags(self, index):
        if index.column() == 2:
            return QtCore.Qt.NoItemFlags
        else:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, col, orientation, role):
        self.header = ["Spin Box", "Column Box", "Progress Bar"]
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]


class Worker(QtCore.QThread):
    """
    Thread to process loading bar progress
    """
    upgradeProgess = QtCore.Signal(int)
    isThreadStopped = False

    def __init__(self):
        super(Worker, self).__init__()
        self.start()

    def run(self):
        for i in range(101):
            self.upgradeProgess.emit(i)
            time.sleep(0.5)


class MainInterface(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile("TableView.ui")
        file.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(file, self)
        self.close()

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.ui)
        self.setLayout(layout)
        self.resize(self.ui.width(), self.ui.height())

        self.model = TableModel(self.ui.tableView)
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        self.spinBoxDelegate = SpinBoxDelegate()
        self.ui.tableView.setItemDelegateForColumn(0, self.spinBoxDelegate)

        self.comboBoxDelegate = ComboBoxDelegate(self.ui.tableView)
        self.ui.tableView.setItemDelegateForColumn(1, self.comboBoxDelegate)

        self.loadingBarDelegate = LoadingBarDelegate(self.ui.tableView)
        self.ui.tableView.setItemDelegateForColumn(2, self.loadingBarDelegate)

    def closeEvent(self, event):
        self.model.worker.terminate()
        event.accept()

if __name__ == "__main__":
    currentTime = time.time()
    a = QtGui.QApplication(sys.argv)
    t = MainInterface()
    t.show()
    sys.exit(a.exec_())
