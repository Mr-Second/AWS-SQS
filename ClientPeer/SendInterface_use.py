from ClientPeer.UI.SendInterface import Ui_Dialog
from PyQt5.QtWidgets import QDialog,QApplication,QMessageBox
from PyQt5 import QtCore,QtGui
from PyQt5.QtWidgets import QHeaderView,QTableWidgetItem
import boto3
from botocore.exceptions import ClientError
import sys
import os
import time


class SendInterface(QDialog, Ui_Dialog):
    def __init__(self, parent=None, *args):
        super(SendInterface, self).__init__(parent)
        self.setupUi(self)
        self.init()
        # 构造函数传入的参数
        self.client = args[0]
        self.queueUrl = args[1]
        self.region = args[2]
        # 用于控制无边框窗口移动
        self.m_flag = None
        self.m_Position = None

    def init(self):
        self.setFixedHeight(308)
        self.setFixedWidth(395)
        # 设置窗体无边框
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #   设置tableWidget每列和每行长度自由伸展
        self.displayTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.displayTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 设置样式
        self.loadStytleSheet("../Config/styleSheet_2.qss")
        # 连接信号与槽
        self.close_btn.clicked.connect(self.close_event)
        self.send_Btn.clicked.connect(self.send_event)

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

    def loadStytleSheet(self, filepath):
        if not os.path.exists(filepath):
            print("file not exists!")
        else:
            with open(filepath, "r") as f:
                s = f.read()
                self.setStyleSheet(s)

    def close_event(self):
        opa = 1.0
        while opa >= 0:
            self.setWindowOpacity(opa)
            opa -= 0.1
            time.sleep(0.05)
        exit(0)

    def send_event(self):
        msg_body = self.sendArea.toPlainText()
        msg = self.send_sqs_message(self.client, sqs_queue_url=self.queueUrl, msg_body=msg_body)
        if msg is None:
            QMessageBox.warning(self, "WARNING", "身份信息已过期，请及时更新./aws/credentials文件的内容！",
                                QMessageBox.Ok)
            return
        date = str(msg['ResponseMetadata']['HTTPHeaders']['date'])
        stringlist = date.split(' ')
        date = stringlist[3]+' '+stringlist[4]
        rowcount = self.displayTable.rowCount()
        self.displayTable.insertRow(rowcount)
        if date:
            item_1 = QTableWidgetItem(str(rowcount))
            item_2 = QTableWidgetItem(str(date))
            item_3 = QTableWidgetItem(str(msg_body))
            self.displayTable.setItem(rowcount, 0, item_1)
            self.displayTable.setItem(rowcount, 1, item_2)
            self.displayTable.setItem(rowcount, 2, item_3)
            self.displayTable.viewport().update()
            self.sendArea.clear()

    @staticmethod
    def send_sqs_message(client, sqs_queue_url, msg_body):
        try:
            msg = client.send_message(QueueUrl=sqs_queue_url, MessageBody=msg_body)
        except ClientError as e:
            print(e)
            return None
        return msg


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     myWin = SendInterface(None,'a','a','a')
#     myWin.exec()
#     sys.exit(app.exec_())
