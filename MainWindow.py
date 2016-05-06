import sys, sip, copy
from PyQt5.QtWidgets import (QApplication, QWidget, QDesktopWidget, QDialog, QTabWidget, QButtonGroup,
                             QLabel, QCheckBox, QPushButton, QMainWindow, QMenuBar, QComboBox,
                             QLineEdit, QTextEdit, QGridLayout, QFileDialog, QAction, qApp, QHBoxLayout, QVBoxLayout)

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import (QColor, QPainter, QFont)
from PyQt5.QtWidgets import (QWidget, QPushButton, QRadioButton,
                             QFrame, QApplication, QSizePolicy)
from PyQt5.QtSvg import QSvgGenerator
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import gui
from settings import *
from biochemistry import *
from inputreader import *
from filters import *
from functools import partial
from run_vmd import *
from Canvas import *
from Plotters import *

class MainWindow(QMainWindow, gui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.contacts = []
        self.setupUi(self)

        self.setWindowTitle("pyContact")
        self.mergeSlider.valueChanged.connect(self.mergeValueChanged)

        # painter contains both labels and frame boxes for drawing
        self.painter = Canvas()
        self.scrollArea.setWidget(self.painter)
        self.actionOpen.triggered.connect(self.pushOpen)
        self.actionExport.triggered.connect(self.pushExport)
        self.actionRun_VMD_contact_search.triggered.connect(self.pushRunVMDContactSearch)

        # settings and filters
        self.settingsView = SettingsTabWidget()
        self.settingsView.applySettingsButton.clicked.connect(self.updateSettings)
        self.settingsView.applyFilterButton.clicked.connect(self.updateFilters)

        #alpha slider for color
        self.alphaSlider.setValue(50)
        self.alphaSlider.valueChanged.connect(self.alphaValueChanged)

        self.statisticsButton.clicked.connect(self.showStatistics)

        self.updateSettings()
        self.updateFilters()
        self.openPreferencesButton.clicked.connect(self.openPrefs)

        #button group for weight functions
        self.functionButtonGroup = QButtonGroup()
        self.currentFunctionType = FunctionType.sigmoid
        self.functionButtonGroup.buttonClicked[int].connect(self.showFunctionSettings)
        self.functionButtonGroup.addButton(self.settingsView.sigmoidRadioButton, 0)
        self.functionButtonGroup.addButton(self.settingsView.rectRadioButton, 1)
        self.functionButtonGroup.addButton(self.settingsView.linRadioButton, 2)
        self.setupFunctionBox()
        self.showFunctionSettings(FunctionType.sigmoid)

    def setupFunctionBox(self):
        # sig
        self.sigX0Label = QLabel("x0: ", self.settingsView)
        self.sigX0Field = QLineEdit("1", self.settingsView)
        self.settingsView.functionGridLayout.addWidget(self.sigX0Label, 1, 0)
        self.settingsView.functionGridLayout.addWidget(self.sigX0Field, 1, 1)

        self.sigLLabel = QLabel("L: ", self.settingsView)
        self.sigLField = QLineEdit("1", self.settingsView)
        self.settingsView.functionGridLayout.addWidget(self.sigLLabel, 1, 2)
        self.settingsView.functionGridLayout.addWidget(self.sigLField, 1, 3)

        self.sigKLabel = QLabel("k: ", self.settingsView)
        self.sigKField = QLineEdit("1", self.settingsView)
        self.settingsView.functionGridLayout.addWidget(self.sigKLabel, 2, 0)
        self.settingsView.functionGridLayout.addWidget(self.sigKField, 2, 1)

        self.sigY0Label = QLabel("y0: ", self.settingsView)
        self.sigY0Field = QLineEdit("0", self.settingsView)
        self.settingsView.functionGridLayout.addWidget(self.sigY0Label, 2, 2)
        self.settingsView.functionGridLayout.addWidget(self.sigY0Field, 2, 3)

        # rect
        self.rectX0Label = QLabel("x0: ", self.settingsView)
        self.rectX0Field = QLineEdit("1", self.settingsView)
        self.settingsView.functionGridLayout.addWidget(self.rectX0Label, 1, 0)
        self.settingsView.functionGridLayout.addWidget(self.rectX0Field, 1, 1)

        self.rectX1Label = QLabel("x1: ", self.settingsView)
        self.rectX1Field = QLineEdit("2", self.settingsView)
        self.settingsView.functionGridLayout.addWidget(self.rectX1Label, 1, 2)
        self.settingsView.functionGridLayout.addWidget(self.rectX1Field, 1, 3)

        self.rectHLabel = QLabel("h: ", self.settingsView)
        self.rectHField = QLineEdit("1", self.settingsView)
        self.settingsView.functionGridLayout.addWidget(self.rectHLabel, 2, 0)
        self.settingsView.functionGridLayout.addWidget(self.rectHField, 2, 1)

        self.rectY0Label = QLabel("y0: ", self.settingsView)
        self.rectY0Field = QLineEdit("0", self.settingsView)
        self.settingsView.functionGridLayout.addWidget(self.rectY0Label, 2, 2)
        self.settingsView.functionGridLayout.addWidget(self.rectY0Field, 2, 3)

        # lin
        self.linY0Label = QLabel("y0: ", self.settingsView)
        self.linY0Field = QLineEdit("0", self.settingsView)
        self.settingsView.functionGridLayout.addWidget(self.linY0Label, 1, 0)
        self.settingsView.functionGridLayout.addWidget(self.linY0Field, 1, 1)

        self.linY1Label = QLabel("y1: ", self.settingsView)
        self.linY1Field = QLineEdit("1", self.settingsView)
        self.settingsView.functionGridLayout.addWidget(self.linY1Label, 1, 2)
        self.settingsView.functionGridLayout.addWidget(self.linY1Field, 1, 3)

        # preview
        self.previewPlot = SimplePlotter(None, width=5, height=2, dpi=60)
        self.settingsView.functionGridLayout.addWidget(self.previewPlot, 3, 0, 1, 4)

        self.settingsView.previewButton.clicked.connect(self.previewFunction)

    def updateSettings(self):
        self.painter.nsPerFrame = float(self.settingsView.nsPerFrameField.text())
        self.painter.threshold = float(self.settingsView.thresholdField.text())
        self.painter.rendered = False
        self.painter.update()
        self.painter.paintEvent(QPaintEvent(QRect(0, 0, self.painter.sizeX, self.painter.sizeY)))

    def updateFilters(self):
        print("filter update")
        self.painter.labelView.clean()
        # total time filter
        totalTimeActive = self.settingsView.activeTotalTimeCheckbox.isChecked()
        scoreActive = self.settingsView.activeScoreCheckbox.isChecked()
        sortingActive = self.settingsView.activeSortingBox.isChecked()
        filterActive = (totalTimeActive or scoreActive or sortingActive)
        weightActive = self.settingsView.functionActiveCheckbox.isChecked()
        # only filter given range
        rangeFilterActive = self.settingsView.filterRangeCheckbox.isChecked()
        if len(self.contacts) > 0:
            lower = int(self.settingsView.lowerRangeField.text()) - 1
            upper = self.settingsView.upperRangeField.text()
            if upper == "end":
                upper = len(self.contacts[0].scoreArray)
            else:
                upper = int(upper)

            if lower < 0:
                lower = 0
            self.painter.range = [lower, upper]
            self.painter.rangeFilterActive = False
            filteredContacts = copy.deepcopy(self.contacts)
            # residue range filter
            resrangeFilter = ResidueRangeFilter("resrange")
            filteredContacts = resrangeFilter.filterResiduesByRange(filteredContacts, self.settingsView.residARangeField.text(), self.settingsView.residBRangeField.text())
            # aminoacids name filter
            aaFilter = NameFilter("name")
            filteredContacts = aaFilter.filterResiduesByName(filteredContacts, self.settingsView.residANameField.text(), self.settingsView.residBNameField.text())
            # range filter
            if rangeFilterActive:
                self.painter.rangeFilterActive = True
                frameRangeFilter = FrameFilter("framer")
                filteredContacts = frameRangeFilter.extractFrameRange(filteredContacts, [lower, upper])
            # weight functions
            if weightActive:
                if self.currentFunctionType == FunctionType.sigmoid:
                    print("sig weight")
                    x0 = float(self.sigX0Field.text())
                    L = float(self.sigLField.text())
                    k = float(self.sigKField.text())
                    y0 = float(self.sigY0Field.text())
                    sig = SigmoidWeightFunction("sig", np.arange(0, len(self.contacts[0].scoreArray), 1), x0, L, k, y0)
                    filteredContacts = sig.weightContactFrames(filteredContacts)
                elif self.currentFunctionType == FunctionType.rect:
                    x0 = float(self.rectX0Field.text())
                    x1 = float(self.rectX1Field.text())
                    h = float(self.rectHField.text())
                    y0 = float(self.rectY0Field.text())
                    rect = RectangularWeightFunction("rect", np.arange(0, len(self.contacts[0].scoreArray), 1), x0, x1, h, y0)
                    filteredContacts = rect.weightContactFrames(filteredContacts)
                elif self.currentFunctionType == FunctionType.linear:
                    y0 = float(self.linY0Field.text())
                    y1 = float(self.linY1Field.text())
                    lin = LinearWeightFunction("rect", np.arange(0, len(self.contacts[0].scoreArray), 1), y0, y1)
                    filteredContacts = lin.weightContactFrames(filteredContacts)
            # other filters
            if filterActive:
                    if totalTimeActive:
                        operator = self.settingsView.compareTotalTimeDropdown.currentText()
                        value = float(self.settingsView.totalTimeField.text())
                        filter = TotalTimeFilter("tottime", operator, value)
                        filteredContacts = filter.filterContacts(filteredContacts)
                    if scoreActive:
                        operator = self.settingsView.compareScoreDropdown.currentText()
                        value = float(self.settingsView.scoreField.text())
                        filter = ScoreFilter("score", operator, value, self.settingsView.meanDropdown.currentText())
                        filteredContacts = filter.filterContacts(filteredContacts)
                    if sortingActive:
                        key = self.settingsView.sortingKeyDropdown.currentText()
                        descending = SortingOrder.mapping[self.settingsView.sortingOrderDropdown.currentText()]
                        sorter = Sorting("sorting", key, descending)
                        sorter.setThresholdAndNsPerFrame(float(self.settingsView.thresholdField.text()), float(self.settingsView.nsPerFrameField.text()))
                        filteredContacts = sorter.sortContacts(filteredContacts)
                    self.painter.contacts = filteredContacts
                    self.painter.rendered = False
                    self.painter.update()
                    self.painter.paintEvent(QPaintEvent(QRect(0, 0, self.painter.sizeX, self.painter.sizeY)))
                    if len(filteredContacts) == 0:
                        self.painter.labelView.clean()
            else:
                #no weight or filters
                self.painter.contacts = filteredContacts
                self.painter.rendered = False
                self.painter.update()
                self.painter.paintEvent(QPaintEvent(QRect(0, 0, self.painter.sizeX, self.painter.sizeY)))

    # switch between weight functions
    def showFunctionSettings(self, radiobutton):
        self.currentFunctionType = radiobutton
        if radiobutton == FunctionType.sigmoid:
            self.showHide(False, True, True)
        elif radiobutton == FunctionType.rect:
            self.showHide(True, False, True)
        elif radiobutton == FunctionType.linear:
            self.showHide(True, True, False)
    #hiding and showing of weight function labels and textfields
    def showHide(self, first, second, third):
        self.sigX0Label.setHidden(first)
        self.sigX0Field.setHidden(first)
        self.sigLLabel.setHidden(first)
        self.sigLField.setHidden(first)
        self.sigKLabel.setHidden(first)
        self.sigKField.setHidden(first)
        self.sigY0Label.setHidden(first)
        self.sigY0Field.setHidden(first)
        self.rectX0Label.setHidden(second)
        self.rectX0Field.setHidden(second)
        self.rectX1Label.setHidden(second)
        self.rectX1Field.setHidden(second)
        self.rectHLabel.setHidden(second)
        self.rectHField.setHidden(second)
        self.rectY0Label.setHidden(second)
        self.rectY0Field.setHidden(second)
        self.linY0Label.setHidden(third)
        self.linY0Field.setHidden(third)
        self.linY1Label.setHidden(third)
        self.linY1Field.setHidden(third)

    #display currenct function in preview window
    def previewFunction(self):
        x = []
        y = []
        if self.currentFunctionType == FunctionType.sigmoid:
            x0 = float(self.sigX0Field.text())
            L = float(self.sigLField.text())
            k = float(self.sigKField.text())
            y0 = float(self.sigY0Field.text())
            if len(self.contacts) > 0:
                sig = SigmoidWeightFunction("sig", np.arange(0, len(self.contacts[0].scoreArray), 1), x0, L, k, y0)
                x = np.arange(0, len(self.contacts[0].scoreArray), 1)
                y = sig.previewFunction()
        elif self.currentFunctionType == FunctionType.rect:
            x0 = float(self.rectX0Field.text())
            x1 = float(self.rectX1Field.text())
            h = float(self.rectHField.text())
            y0 = float(self.rectY0Field.text())
            if len(self.contacts) > 0:
                rect = RectangularWeightFunction("rect", np.arange(0, len(self.contacts[0].scoreArray), 1), x0, x1, h, y0)
                x = np.arange(0, len(self.contacts[0].scoreArray), 1)
                y = rect.previewFunction()
        elif self.currentFunctionType == FunctionType.linear:
            y0 = float(self.linY0Field.text())
            y1 = float(self.linY1Field.text())
            if len(self.contacts) > 0:
                lin = LinearWeightFunction("rect", np.arange(0, len(self.contacts[0].scoreArray), 1), y0, y1)
                x = np.arange(0, len(self.contacts[0].scoreArray), 1)
                y = lin.previewFunction()
        sip.delete(self.previewPlot)
        self.previewPlot = SimplePlotter(None, width=5, height=2, dpi=60)
        self.settingsView.functionGridLayout.addWidget(self.previewPlot, 3, 0, 1, 4)
        self.previewPlot.plot(x, y)
        self.previewPlot.update()

    def openPrefs(self):
        self.settingsView.show()

    def showStatistics(self):
        d = QDialog()
        grid = QGridLayout()
        d.setLayout(grid)

        numberTitleLabel = QLabel("total number of contacts:")
        numberLabel = QLabel(str(len(self.contacts)))

        numberFramesTitleLabel = QLabel("number of frames:")
        numberFramesLabel = QLabel(str(len(self.contacts[0].scoreArray)))

        meanTitleLabel = QLabel("mean contact score:")
        meanLabel = QLabel(str(mean_score_of_contactArray(self.contacts)))

        medianTitleLabel = QLabel("median score:")
        medianLabel = QLabel(str(median_score_of_contactArray(self.contacts)))

        grid.addWidget(numberTitleLabel, 0, 0)
        grid.addWidget(numberLabel, 0, 1)
        grid.addWidget(numberFramesTitleLabel, 1, 0)
        grid.addWidget(numberFramesLabel, 1, 1)
        grid.addWidget(meanTitleLabel, 2, 0)
        grid.addWidget(meanLabel, 2, 1)

        grid.addWidget(medianTitleLabel, 2, 2)
        grid.addWidget(medianLabel, 2, 3)

        allContactPlot = ContactPlotter(None, width=4, height=2, dpi=80)
        allContactPlot.plot_all_contacts_figure(self.contacts)
        grid.addWidget(allContactPlot, 3, 0, 1, 4)
        d.setWindowTitle("Statistics")
        d.resize(600, 450)
        d.setWindowModality(Qt.ApplicationModal)
        d.exec_()

    def pushOpen(self):
        fnames = QFileDialog.getOpenFileNames(self, "Open file")
        for file in fnames[0]:
            self.file = file
            break
        lines = []
        print(self.file)
        with open(self.file, "r") as f:
            for line in f.readlines():
                lines.append(line)
        self.contacts = makeContactFromLines(lines)
        print("new contacts: " + str(len(self.contacts)))
        self.painter.contacts = self.contacts
        self.painter.range = [0, len(self.contacts[0].scoreArray)]
        # self.painter.update()
        # set max slider value to frame number!
        self.mergeSlider.setMaximum(len(self.contacts[0].scoreArray) / 15)
        self.updateSettings()
        self.updateFilters()

    def pushExport(self):
        d = QDialog()
        grid = QGridLayout()
        d.setLayout(grid)

        self.exportLabel = QLabel("Export current view: ")

        self.saveButton = QPushButton("Export")
        self.saveButton.setAutoDefault(False)
        self.saveButton.clicked.connect(self.pushSave)

        self.formatBox = QComboBox()
        self.formatBox.addItem("PNG")
        self.formatBox.addItem("SVG")

        grid.addWidget(self.exportLabel, 0, 0)
        grid.addWidget(self.saveButton, 0, 1)

        grid.addWidget(self.formatBox, 2, 0)

        d.setWindowTitle("Export")
        d.setWindowModality(Qt.ApplicationModal)
        d.exec_()

    def pushSave(self):
        fileName = QFileDialog.getSaveFileName(self, 'Export Path')
        print(self.formatBox.currentText())
        if self.formatBox.currentText() == "PNG":
            if len(fileName[0]) > 0:
                print("Saving current view to ", fileName[0])
                currentView = self.painter.grab()
                currentView.save(fileName[0])
        elif self.formatBox.currentText() == "SVG":
            if len(fileName[0]) > 0:
                print("Saving current view to ", fileName[0])
                generator = QSvgGenerator()
                generator.setFileName(fileName[0])
                generator.setSize(self.painter.size())
                generator.setViewBox(self.painter.rect())
                self.painter.renderContact(generator)
        self.painter.rendered = False
        self.painter.update()
        self.painter.paintEvent(QPaintEvent(QRect(0, 0, self.painter.sizeX, self.painter.sizeY)))

    def pushRunVMDContactSearch(self):
        # test execution
        run_vmd(50, 5, "","")
        ######
        d = QDialog()
        grid = QGridLayout()
        d.setLayout(grid)

        d.setWindowTitle("Run VMD")
        d.resize(650, 700)
        d.setWindowModality(Qt.ApplicationModal)
        d.exec_()

    def mergeValueChanged(self):
        self.painter.merge = self.mergeSlider.value()
        self.painter.rendered = False
        self.painter.update()
        self.painter.paintEvent(QPaintEvent(QRect(0, 0, self.painter.sizeX, self.painter.sizeY)))

    def alphaValueChanged(self):
        self.painter.alphaFactor = self.alphaSlider.value()
        self.painter.rendered = False
        self.painter.update()
        self.painter.paintEvent(QPaintEvent(QRect(0, 0, self.painter.sizeX, self.painter.sizeY)))


class SettingsTabWidget(QTabWidget, Ui_settingsWindowWidget):
    def __init__(self, parent=None):
        super(QtWidgets.QTabWidget, self).__init__(parent)
        self.setupUi(self)