from PySide import QtCore, QtGui


class SpinBoxDelegate(QtGui.QItemDelegate):
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


class TableViewModel(QtCore.QAbstractTableModel):
    def rowCount(self, index, parent=QtCore.QModelIndex()):
        return 4

    def columnCount(self, index, parent=QtCore.QModelIndex()):
        return 4

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return 10

    def flags(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    model = TableViewModel()
    tableView = QtGui.QTableView()
    tableView.setModel(model)

    tableView = QtGui.QTableView()
    tableView.setModel(model)

    delegate = SpinBoxDelegate()
    tableView.setItemDelegateForColumn(0, delegate)

    tableView.setWindowTitle("Spin Box Delegate")
    tableView.show()
    sys.exit(app.exec_())