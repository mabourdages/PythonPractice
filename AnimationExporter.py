from pyfbsdk import *
from pyfbsdk_additions import *
from PySide import QtCore, QtGui, QtUiTools, shiboken


class NativeWidgetHolder(FBWidgetHolder):
    def __init__(self):
        FBWidgetHolder.__init__(self)
        self.oFBTool = FBCreateUniqueTool("Test")

        x = FBAddRegionParam(0, FBAttachType.kFBAttachLeft, "")
        y = FBAddRegionParam(0, FBAttachType.kFBAttachTop, "")
        w = FBAddRegionParam(0, FBAttachType.kFBAttachRight, "")
        h = FBAddRegionParam(0, FBAttachType.kFBAttachBottom, "")
        self.oFBTool.AddRegion("main", "main", x, y, w, h)
        
        oGridLayout = FBGridLayout()
        oGridLayout.Add(self, 0, 0)
        self.oFBTool.SetControl("main", oGridLayout)

        ShowToolByName("Test")

    def WidgetCreate(self, wParentWidget):
        #=== Loading Ui ===#
        loader = QtUiTools.QUiLoader()
        uiFile = QtCore.QFile("TakeName.ui")
        uiFile.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(uiFile)

        self.oToolWidget = QtGui.QWidget()
        self.oLayout = QtGui.QVBoxLayout()
        self.oLayout.addWidget(self.ui)
        self.oToolWidget.setLayout(self.oLayout)

        uiFile.close()

        return shiboken.getCppPointer(self.oToolWidget)[0]


class MainInterfaceClass(NativeWidgetHolder):
    def __init__(self):
        NativeWidgetHolder.__init__(self)
        #=== Updating SceneInfo ===#
        self.updateTakeComboBox()
        self.updateTakeInfo()

        #=== Connecting Slot ===#
        self.oToolWidget.connect(self.ui.comboBox_takeName, QtCore.SIGNAL("currentIndexChanged(int)"), self.updateTakeInfo)

        FBSystem().Scene.OnTakeChange.RemoveAll()
        FBSystem().Scene.OnTakeChange.Add(self.takeCallback)

    def takeCallback(self, caller, event):
        if "kFBTakeChangeMoved" or "kFBTakeChangeOpened" or "kFBTakeChangeRenamed" in str(event.Type):
            self.updateTakeComboBox()

    def updateTakeComboBox(self):
        self.ui.comboBox_takeName.clear()
        for take in FBSystem().Scene.Takes:
            self.ui.comboBox_takeName.addItem(take.Name)

    def updateTakeInfo(self):
        sceneInfo = FBFindModelByLabelName("SceneInfo")
        oPropTakeName = sceneInfo.PropertyList.Find("TakeName")
        oPropTakeName.Data = str(self.ui.comboBox_takeName.currentText())


MainInterfaceClass()