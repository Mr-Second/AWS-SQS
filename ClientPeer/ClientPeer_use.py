from ClientPeer.UI.ClientPeer import Ui_ConfigDialog
from PyQt5.QtWidgets import QDialog,QApplication
from PyQt5 import QtCore,QtGui
import sys
import os
import time
import logging
import boto3
from botocore.exceptions import ClientError
from ClientPeer.SendInterface_use import SendInterface



class ClientPeer(QDialog, Ui_ConfigDialog):
    def __init__(self, parent=None):
        super(ClientPeer, self).__init__(parent)
        self.setupUi(self)
        self.queueUrl = None
        self.region = None
        self.client = None
        self.sendInterface = None

        # 控制无边窗口移动
        self.m_flag = None
        self.m_Position = None

        self.init()


    def init(self):
        self.setFixedHeight(289)
        self.setFixedWidth(410)

        # 设置窗体无边框
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # 设置背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # 设置样式
        self.loadStytleSheet("../Config/styleSheet.qss")
        # 连接信号与槽
        self.close_Btn.clicked.connect(self.close_event)
        self.connectBtn.clicked.connect(self.connectEvent)

        path = os.path.abspath(os.path.dirname(os.getcwd()))+'\\Config\\config.ini'
        if os.path.exists(path):
            with open(path,'r') as f:
                line_1= f.readline().strip('\n')
                line_2 = f.readline().strip('\n')
                self.region = line_1
                self.queueUrl = line_2
                self.region_Input.setText(line_1)
                self.queueUrl_Input.setText(line_2)




    # 以下三个函数用于控制无边框的窗口移动
    # --------------------------------------------------------------------------------
    # 重载鼠标按压事件
    def mousePressEvent(self, *args, **kwargs):
        event = args[0]
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

        # 重载鼠标移动事件

    def mouseMoveEvent(self, *args, **kwargs):
        QMouseEvent = args[0]
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

        # 重载鼠标释放事件

    def mouseReleaseEvent(self, *args, **kwargs):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    # --------------------------------------------------------------------------------

    def loadStytleSheet(self,filepath):
        if not os.path.exists(filepath):
            print("file not exists!")
        else:
            with open(filepath,"r") as f:
                s = f.read()
                self.setStyleSheet(s)

    def close_event(self):
        opa = 1.0
        while opa >= 0:
            self.setWindowOpacity(opa)
            opa -= 0.1
            time.sleep(0.05)
        exit(0)

    def setConnectBtnEnable(self):
        self.queueUrl = self.queueUrl_Input.text()
        self.region = self.region_Input.text()
        if len(self.queueUrl) != 0 and len(self.region) != 0:
            self.connectBtn.setEnabled(True)
        else:
            self.connectBtn.setEnabled(False)

    def connectEvent(self):
        self.client = boto3.client('sqs', region_name= self.region)
        self.sendInterface = SendInterface(None,self.client,self.queueUrl,self.region)
        self.close()
        self.sendInterface.exec_()

    def setRemember(self):
        if self.region is None or self.queueUrl is None:
            return
        if self.checkBox.isChecked() and  len(self.region) != 0 and len(self.queueUrl) != 0:
            path = os.path.abspath(os.path.dirname(os.getcwd()))+'\\Config\\config.ini'
            with open(path,'w') as f:
                f.write(self.region+'\n')
                f.write(self.queueUrl)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = ClientPeer()
    myWin.exec()
    sys.exit(app.exec_())
