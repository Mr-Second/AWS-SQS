from ClientPeer.UI.ServerPeer import Ui_Dialog
from PyQt5.QtWidgets import QDialog,QApplication
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem,QMessageBox
import sys
import os
import time
import boto3
import threading
import queue
import json
from botocore.exceptions import ClientError

# 全局队列存储获得的消息
myQueue = queue.Queue()
# 线程锁
lock = threading.Lock()

# 控制子线程关闭的标志
flag = True


class ServerPeer(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(ServerPeer, self).__init__(parent)
        self.setupUi(self)

        # 控制无边窗口移动
        self.m_flag = None
        self.m_Position = None

        self.path = os.path.abspath(os.path.dirname(os.getcwd()))+'\\Config\\config_2.ini'
        # 计时器，每隔一段时间刷新界面
        self.timer = QtCore.QTimer(self)
        self.init()

    def init(self):
        self.StartBtn.setEnabled(False)
        # 设置窗体无边框
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # 设置样式
        self.loadStytleSheet(os.path.dirname(os.getcwd())+'/Config/styleSheet_3.qss')

        # 将定时器连接槽函数，并设置定时时间
        self.timer.timeout.connect(self.changeTable)
        # 导入配置文件
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                wait_time = f.readline().strip()
                nums_msg = f.readline().strip()
                queueUrl = f.readline().strip()
                region = f.readline().strip()
                visibility_time = f.readline().strip()
                self.waitTime_Input.setText(wait_time)
                self.msgNums_Input.setText(nums_msg)
                self.QueueUrl_Input.setText(queueUrl)
                self.region_Input.setText(region)
                self.visibilityTime_Input.setText(visibility_time)

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

    # 导入样式文件
    def loadStytleSheet(self, filepath):
        if not os.path.exists(filepath):
            print("file not exists!")
        else:
            with open(filepath, "r") as f:
                s = f.read()
                self.setStyleSheet(s)

    # 关闭窗口槽函数
    def close_Event(self):
        opa = 1.0
        while opa >= 0:
            self.setWindowOpacity(opa)
            opa -= 0.1
            time.sleep(0.05)
        global flag
        flag = False
        time.sleep(0.1)
        exit(0)

    # 开始按钮槽函数,开启子线程
    def startEvent(self):
        self.StartBtn.setEnabled(False)
        self.timer.start(5.0)
        queueUrl = self.QueueUrl_Input.text()
        region_name = self.region_Input.text()
        num_msgs = int(self.msgNums_Input.text())
        wait_time = int(self.waitTime_Input.text())
        visibility_time = int(self.visibilityTime_Input.text())
        subthread = threading.Thread(target=self.subthread, args=(queueUrl,
                                                                  region_name, num_msgs, wait_time, visibility_time,))
        subthread.start()

    # 子线程
    def subthread(self,sqs_queue_url, region_name, num_msgs=1, wait_time=0, visibility_time=5):
        global flag
        while flag:
            ReceiptHandle = self.retrieve_sqs_messages(sqs_queue_url, region_name, num_msgs, wait_time, visibility_time)
            if ReceiptHandle:
                self.delete_sqs_message(sqs_queue_url, region_name, ReceiptHandle)
            time.sleep(0.1)
        print('子线程结束')

    # 设置开始按钮是否可按
    def setSendBtnEnble(self):
        wait_time = self.waitTime_Input.text()
        nums_msg = self.msgNums_Input.text()
        queueUrl = self.QueueUrl_Input.text()
        region = self.region_Input.text()
        visibility_time = self.visibilityTime_Input.text()
        if wait_time and nums_msg and queueUrl and region and visibility_time:
            if len(wait_time) != 0 and len(nums_msg) != 0 and \
                    len(queueUrl) != 0 and len(region) != 0 and len(visibility_time) != 0:
                self.StartBtn.setEnabled(True)

    # 将数据写入文件
    def setRemember(self):
        wait_time = self.waitTime_Input.text()
        nums_msg = self.msgNums_Input.text()
        queueUrl = self.QueueUrl_Input.text()
        region = self.region_Input.text()
        visibility_time = self.visibilityTime_Input.text()
        if self.checkBox.isChecked() and wait_time and nums_msg and queueUrl and region and visibility_time:
            if len(wait_time) != 0 and len(nums_msg) != 0 and \
                    len(queueUrl) != 0 and len(region) != 0 and len(visibility_time) != 0:
                with open(self.path, 'w') as f:
                    f.write(wait_time+'\n')
                    f.write(nums_msg+'\n')
                    f.write(queueUrl+'\n')
                    f.write(region+'\n')
                    f.write(visibility_time)
            else:
                self.checkBox.setChecked(False)

    # 静态方法，接收消息，将其放在子线程中
    @staticmethod
    def retrieve_sqs_messages(sqs_queue_url, region_name, num_msgs=1, wait_time=0, visibility_time=5):
        # Validate number of messages to retrieve
        global myQueue
        if num_msgs < 1:
            num_msgs = 1
        elif num_msgs > 10:
            num_msgs = 10

        # Retrieve messages from an SQS queue
        sqs_client = boto3.client('sqs', region_name=region_name)
        try:
            msgs = sqs_client.receive_message(QueueUrl=sqs_queue_url,
                                              AttributeNames=['All'],
                                              MaxNumberOfMessages=num_msgs,
                                              WaitTimeSeconds=wait_time,
                                              VisibilityTimeout=visibility_time)
        except ClientError as e:
            print(e)
            print("身份信息已过期，请及时更新./aws/credentials文件的内容！")
            return
        print(msgs)
        print(type(msgs))
        # 加锁
        lock.acquire()
        myQueue.put(json.dumps(msgs))
        # 释放锁
        lock.release()

        if 'Messages' in msgs:
            msgs = json.loads(json.dumps(msgs))
            return dict(msgs['Messages'][0])['ReceiptHandle']

    def changeTable(self):
        global myQueue
        while not myQueue.empty():
            # 加锁
            lock.acquire()
            msg = myQueue.get()
            # 释放锁
            lock.release()

            msg = json.loads(msg)
            rowcount = self.tableWidget.rowCount()
            if 'Messages' in msg:
                self.tableWidget.insertRow(rowcount)
                data = dict(msg['Messages'][0])['Body']
                templist = str(msg['ResponseMetadata']['HTTPHeaders']['date']).split(' ')
                date = templist[3] + ' ' + templist[4]
                senderId = str(dict(msg['Messages'][0])['Attributes']['SenderId']).split('=')[1]
                item_1 = QTableWidgetItem(str(rowcount))
                item_2 = QTableWidgetItem(str(date))
                item_3 = QTableWidgetItem(str(senderId))
                item_4 = QTableWidgetItem(str(data))
                self.tableWidget.setItem(rowcount, 0, item_1)
                self.tableWidget.setItem(rowcount, 1, item_2)
                self.tableWidget.setItem(rowcount, 2, item_3)
                self.tableWidget.setItem(rowcount, 3, item_4)
                self.tableWidget.viewport().update()
            else:
                print('No message')

    @staticmethod
    def delete_sqs_message(sqs_queue_url, region_name, msg_receipt_handle):
        # Delete the message from the SQS queue
        sqs_client = boto3.client('sqs', region_name=region_name)
        sqs_client.delete_message(QueueUrl=sqs_queue_url,ReceiptHandle=msg_receipt_handle)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = ServerPeer()
    myWin.exec()
    sys.exit(app.exec_())
