# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'statistics.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Statistics(object):
    def setupUi(self, Statistics):
        Statistics.setObjectName("Statistics")
        Statistics.setWindowModality(QtCore.Qt.WindowModal)
        Statistics.resize(930, 642)
        self.gridLayout = QtWidgets.QGridLayout(Statistics)
        self.gridLayout.setObjectName("gridLayout")
        self.savePlotButton = QtWidgets.QPushButton(Statistics)
        self.savePlotButton.setObjectName("savePlotButton")
        self.gridLayout.addWidget(self.savePlotButton, 6, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(Statistics)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(Statistics)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(Statistics)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.labelNumFrames = QtWidgets.QLabel(Statistics)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelNumFrames.setFont(font)
        self.labelNumFrames.setText("")
        self.labelNumFrames.setObjectName("labelNumFrames")
        self.gridLayout.addWidget(self.labelNumFrames, 0, 1, 1, 1)
        self.labelTotalContacts = QtWidgets.QLabel(Statistics)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelTotalContacts.setFont(font)
        self.labelTotalContacts.setText("")
        self.labelTotalContacts.setObjectName("labelTotalContacts")
        self.gridLayout.addWidget(self.labelTotalContacts, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(Statistics)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)
        self.labelMedianScore = QtWidgets.QLabel(Statistics)
        self.labelMedianScore.setText("")
        self.labelMedianScore.setObjectName("labelMedianScore")
        self.gridLayout.addWidget(self.labelMedianScore, 0, 3, 1, 1)
        self.labelMeanScore = QtWidgets.QLabel(Statistics)
        self.labelMeanScore.setText("")
        self.labelMeanScore.setObjectName("labelMeanScore")
        self.gridLayout.addWidget(self.labelMeanScore, 2, 3, 1, 1)
        self.attributeBox = QtWidgets.QComboBox(Statistics)
        self.attributeBox.setObjectName("attributeBox")
        self.attributeBox.addItem("")
        self.attributeBox.addItem("")
        self.gridLayout.addWidget(self.attributeBox, 6, 0, 1, 1)
        self.line = QtWidgets.QFrame(Statistics)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 4, 0, 1, 4)
        self.plotWidget = QtWidgets.QWidget(Statistics)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotWidget.sizePolicy().hasHeightForWidth())
        self.plotWidget.setSizePolicy(sizePolicy)
        self.plotWidget.setMinimumSize(QtCore.QSize(370, 128))
        self.plotWidget.setObjectName("plotWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.plotWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.plotGridLayout = QtWidgets.QGridLayout()
        self.plotGridLayout.setObjectName("plotGridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.plotGridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.plotGridLayout, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.plotWidget, 5, 0, 1, 4)
        self.plotButton = QtWidgets.QPushButton(Statistics)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotButton.sizePolicy().hasHeightForWidth())
        self.plotButton.setSizePolicy(sizePolicy)
        self.plotButton.setObjectName("plotButton")
        self.gridLayout.addWidget(self.plotButton, 6, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.smoothCheckbox = QtWidgets.QCheckBox(Statistics)
        self.smoothCheckbox.setObjectName("smoothCheckbox")
        self.horizontalLayout.addWidget(self.smoothCheckbox)
        self.smoothStrideField = QtWidgets.QLineEdit(Statistics)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smoothStrideField.sizePolicy().hasHeightForWidth())
        self.smoothStrideField.setSizePolicy(sizePolicy)
        self.smoothStrideField.setMaximumSize(QtCore.QSize(50, 16777215))
        self.smoothStrideField.setObjectName("smoothStrideField")
        self.horizontalLayout.addWidget(self.smoothStrideField)
        self.gridLayout.addLayout(self.horizontalLayout, 6, 2, 1, 1)

        self.retranslateUi(Statistics)
        QtCore.QMetaObject.connectSlotsByName(Statistics)

    def retranslateUi(self, Statistics):
        _translate = QtCore.QCoreApplication.translate
        Statistics.setWindowTitle(_translate("Statistics", "Statistics"))
        self.savePlotButton.setText(_translate("Statistics", "Save"))
        self.label_6.setText(_translate("Statistics", "Mean Contact Score:"))
        self.label_2.setText(_translate("Statistics", "Number of Frames: "))
        self.label.setText(_translate("Statistics", "Total Number of Contacts: "))
        self.label_5.setText(_translate("Statistics", "Median Contact Score: "))
        self.attributeBox.setItemText(0, _translate("Statistics", "Score"))
        self.attributeBox.setItemText(1, _translate("Statistics", "hbond number"))
        self.plotButton.setText(_translate("Statistics", "Plot"))
        self.smoothCheckbox.setText(_translate("Statistics", "Smooth:"))
        self.smoothStrideField.setText(_translate("Statistics", "5"))

