import sys
from PySide import QtCore, QtGui, QtUiTools


class ListModel(QtCore.QAbstractListModel):
    def __init__(self, data):
        super(ListModel, self).__init__()
        self.__data = data

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__data)

    def data(self, index, role):
        row = index.row()
        if role == QtCore.Qt.DisplayRole:
            return self.__data[row]

    def setData(self, index, value, role):
        row = index.row()
        self.__data[row] = str(value)
        return True

    def flags(self, role):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled

    def insertRows(self, position, row, item, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, len(self.__data), len(self.__data) + 1)
        self.__data.append(item)
        self.endInsertRows()
        return True

    def removeRows(self, position, row, item, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, len(self.__data), len(self.__data) + 1)
        self.__data.remove(item)
        self.endRemoveRows()
        return True


class MainInterface(QtGui.QWidget):
    def __init__(self):
        super(MainInterface, self).__init__()
        self.listData = []

        self.ui = QtUiTools.QUiLoader().load("TakeListView.ui")

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.ui)
        self.setLayout(layout)
        self.resize(self.ui.width(), self.ui.height())

        self.listModel = ListModel(self.listData)
        self.ui.listView.setModel(self.listModel)

    def contextMenuEvent(self, event):
        self.menu = QtGui.QMenu(self)

        addItemMenu = QtGui.QAction("Add", self)
        addItemMenu.triggered.connect(self.addItem)
        self.menu.addAction(addItemMenu)

        printListMenu = QtGui.QAction("Print", self)
        printListMenu.triggered.connect(self.printList)
        self.menu.addAction(printListMenu)

        removeListMenu = QtGui.QAction("Delete", self)
        removeListMenu.triggered.connect(self.removeItem)
        self.menu.addAction(removeListMenu)

        self.menu.popup(QtGui.QCursor.pos())

    def addItem(self):
        self.listModel.insertRow(0)
        print self.listData

    def removeItem(self):
        self.listModel.removeRow(0)

    def printList(self):
        print self.listData


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    tool = MainInterface()
    tool.show()
    sys.exit(app.exec_())

