# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SendInterface.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(395, 308)
        Dialog.setStyleSheet("")
        self.sendArea = QtWidgets.QPlainTextEdit(Dialog)
        self.sendArea.setGeometry(QtCore.QRect(0, 211, 291, 97))
        self.sendArea.setObjectName("sendArea")
        self.topLabel = QtWidgets.QLabel(Dialog)
        self.topLabel.setGeometry(QtCore.QRect(0, 0, 400, 35))
        self.topLabel.setStyleSheet("color: rgb(63, 63, 63);\n"
"font: 25 20pt \"Calibri Light\";")
        self.topLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.topLabel.setObjectName("topLabel")
        self.send_Btn = QtWidgets.QPushButton(Dialog)
        self.send_Btn.setGeometry(QtCore.QRect(300, 220, 91, 32))
        self.send_Btn.setObjectName("send_Btn")
        self.close_btn = QtWidgets.QPushButton(Dialog)
        self.close_btn.setGeometry(QtCore.QRect(300, 266, 91, 33))
        self.close_btn.setObjectName("close_btn")
        self.displayTable = QtWidgets.QTableWidget(Dialog)
        self.displayTable.setGeometry(QtCore.QRect(0, 30, 391, 182))
        self.displayTable.setStyleSheet("font: 11pt \"幼圆\";\n"
"    \n"
"color: rgb(0, 0, 0);")
        self.displayTable.setObjectName("displayTable")
        self.displayTable.setColumnCount(3)
        self.displayTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.displayTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.displayTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.displayTable.setHorizontalHeaderItem(2, item)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.topLabel.setText(_translate("Dialog", "Sent Imformation Display"))
        self.send_Btn.setText(_translate("Dialog", "Send"))
        self.close_btn.setText(_translate("Dialog", "Close"))
        item = self.displayTable.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Order"))
        item = self.displayTable.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Sent Time"))
        item = self.displayTable.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Imformation"))

