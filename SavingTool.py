import sys, datetime
from PySide import QtCore, QtGui, QtXml
from SavingToolUi import Ui_MainWindow

currentDate = datetime.datetime.now()
qCurrentDate = QtCore.QDate(currentDate)


class MainInterface(QtGui.QMainWindow):
    def __init__(self):
        super(MainInterface, self).__init__()

        # Construct the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect controller
        self.ui.amountWanted.setText("{0}".format(0))

        self.ui.calendarWidget.setMinimumDate(currentDate + datetime.timedelta(days=14))
        self.ui.calendarWidget.clicked.connect(self.calculate)

        self.ui.amountWanted.returnPressed.connect(self.calculate)

    def returnDaysTo(self):
        # Return the number of das between current and selection
        upcomingDate = self.ui.calendarWidget.selectedDate()
        return qCurrentDate.daysTo(upcomingDate)

    def calculate(self):
        # Def to calculate the amount needed by 2 weeks interval
        userInput = self.ui.amountWanted
        try:
            if float(userInput.text()):
                savingNeeded = float(userInput.text()) / (self.returnDaysTo() / 14)
                self.ui.amountResult.setText(str(round(savingNeeded, 2))+"$")
        except ValueError:
            userInput.setText("0")

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    SavingTool = MainInterface()
    SavingTool.show()
    sys.exit(app.exec_())
