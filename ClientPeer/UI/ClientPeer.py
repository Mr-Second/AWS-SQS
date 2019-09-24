# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ClientPeer.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from resources import images_rc

class Ui_ConfigDialog(object):
    def setupUi(self, ConfigDialog):
        ConfigDialog.setObjectName("ConfigDialog")
        ConfigDialog.resize(410, 289)
        ConfigDialog.setStyleSheet("")
        self.MyWidget = QtWidgets.QWidget(ConfigDialog)
        self.MyWidget.setGeometry(QtCore.QRect(-1, -1, 411, 291))
        self.MyWidget.setStyleSheet("")
        self.MyWidget.setObjectName("MyWidget")
        self.connectBtn = QtWidgets.QPushButton(self.MyWidget)
        self.connectBtn.setEnabled(False)
        self.connectBtn.setGeometry(QtCore.QRect(120, 220, 261, 35))
        self.connectBtn.setObjectName("connectBtn")
        self.regionLabel = QtWidgets.QLabel(self.MyWidget)
        self.regionLabel.setGeometry(QtCore.QRect(10, 92, 101, 31))
        self.regionLabel.setStyleSheet("")
        self.regionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.regionLabel.setObjectName("regionLabel")
        self.queueUrlLabel = QtWidgets.QLabel(self.MyWidget)
        self.queueUrlLabel.setGeometry(QtCore.QRect(20, 150, 91, 31))
        self.queueUrlLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.queueUrlLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.queueUrlLabel.setObjectName("queueUrlLabel")
        self.layoutWidget = QtWidgets.QWidget(self.MyWidget)
        self.layoutWidget.setGeometry(QtCore.QRect(120, 70, 261, 121))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.region_Input = QtWidgets.QLineEdit(self.layoutWidget)
        self.region_Input.setMinimumSize(QtCore.QSize(0, 40))
        self.region_Input.setStyleSheet("")
        self.region_Input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.region_Input.setObjectName("region_Input")
        self.verticalLayout.addWidget(self.region_Input)
        self.queueUrl_Input = QtWidgets.QLineEdit(self.layoutWidget)
        self.queueUrl_Input.setMinimumSize(QtCore.QSize(0, 40))
        self.queueUrl_Input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.queueUrl_Input.setObjectName("queueUrl_Input")
        self.verticalLayout.addWidget(self.queueUrl_Input)
        self.close_Btn = QtWidgets.QPushButton(self.MyWidget)
        self.close_Btn.setGeometry(QtCore.QRect(372, -1, 41, 31))
        self.close_Btn.setText("×")
        self.close_Btn.setObjectName("close_Btn")
        self.checkBox = QtWidgets.QCheckBox(self.MyWidget)
        self.checkBox.setGeometry(QtCore.QRect(120, 190, 111, 31))
        self.checkBox.setStyleSheet("")
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi(ConfigDialog)
        self.region_Input.textChanged['QString'].connect(ConfigDialog.setConnectBtnEnable)
        self.queueUrl_Input.textChanged['QString'].connect(ConfigDialog.setConnectBtnEnable)
        self.checkBox.clicked.connect(ConfigDialog.setRemember)
        QtCore.QMetaObject.connectSlotsByName(ConfigDialog)

    def retranslateUi(self, ConfigDialog):
        _translate = QtCore.QCoreApplication.translate
        ConfigDialog.setWindowTitle(_translate("ConfigDialog", "Dialog"))
        self.connectBtn.setText(_translate("ConfigDialog", "Connect"))
        self.regionLabel.setText(_translate("ConfigDialog", "region_name"))
        self.queueUrlLabel.setText(_translate("ConfigDialog", "queue_url"))
        self.checkBox.setText(_translate("ConfigDialog", "remember"))


