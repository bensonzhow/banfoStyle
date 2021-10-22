# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import os
import sys
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from system_hotkey import SystemHotkey

from generation import getPredictText
from utils import getTips


class getTipsThread(QThread):
    """
    获取提示线程类
    """
    signal = pyqtSignal(str)

    def __init__(self, mText: str) -> None:
        """
        初始化获取提示线程类
        :param mText: 关键词句
        """
        super().__init__()
        self.text = mText

    def __del__(self):
        self.wait()

    def run(self):
        """
        文本生成
        :return: None
        """

        '''
        # 使用deepai的文本生成服务
        text = getTips(self.text)
        self.signal.emit(text)
        '''

        text = getPredictText(self.text.replace('\n', ''), length=50)
        self.signal.emit(text)



class Ui_MainWindow(QObject):

    hotkeySign = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.subThread = None
        self.fileName = None

    def setupUi(self, MainWindow):
        MainWindow.resize(862, 579)
        self.mainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        # 文案输入&编辑框
        self.writingEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.writingEdit.setGeometry(QtCore.QRect(10, 10, 431, 501))

        # 给文案提示加个框框
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(450, 10, 401, 501))
        self.groupBox.setCheckable(False)
        self.groupBox.setTitle('提示')

        # 文案提示框框
        self.tipsEdit = QtWidgets.QPlainTextEdit(self.groupBox)
        self.tipsEdit.setGeometry(QtCore.QRect(10, 20, 381, 471))

        # 文件名
        self.FileNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.FileNameLabel.setGeometry(QtCore.QRect(10, 520, 101, 31))
        self.FileNameLabel.setText('文件路径:')
        self.fileNameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.fileNameEdit.setGeometry(QtCore.QRect(90, 520, 351, 31))

        # 三个按钮水平分布
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(450, 514, 401, 41))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName('horizontalLayout')

        # 打开
        self.openButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.openButton.setText('打开')
        self.openButton.clicked.connect(self.openFile)
        self.horizontalLayout.addWidget(self.openButton)

        # 保存
        self.saveButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.saveButton.setText('保存')
        self.saveButton.clicked.connect(self.saveFile)
        self.horizontalLayout.addWidget(self.saveButton)

        # 提示
        self.tipsButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.tipsButton.setText('提示')
        self.tipsButton.clicked.connect(self.tips)
        self.horizontalLayout.addWidget(self.tipsButton)

        # 热键
        self.hotkeySign.connect(self.tips)
        self.F1Hotkey = SystemHotkey()
        self.F1Hotkey.register(['f1'], callback=lambda x: self.hotkeyEvent())

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def hotkeyEvent(self):
        self.hotkeySign.emit()

    def msgBox(self, msg: str, hasQuery: bool = False) -> bool:
        """
        :param msg: 消息
        :param hasQuery: 是否带询问
        :return: 如果hasQuery为True,返回值为用户是否点击了确定
        """
        if not hasQuery:
            QtWidgets.QMessageBox.information(self.mainWindow, '提示', msg, QtWidgets.QMessageBox.Ok,
                                              QtWidgets.QMessageBox.Ok)
            return True
        reply = QtWidgets.QMessageBox.question(self.mainWindow, '提示', msg,
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                                               QtWidgets.QMessageBox.Cancel)
        return reply == QtWidgets.QMessageBox.Yes

    def openFile(self) -> None:
        """
        打开一个文件
        :return: None
        """
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.mainWindow, '选择文案', os.path.join(os.getcwd(), 'writing'), 'Text Files (*.txt)')
        if not os.path.exists(fileName):
            self.msgBox('未选择文件!')
            return
        with open(fileName, 'r+', encoding='UTF-8') as f:
            data = f.read()
        self.writingEdit.appendPlainText(data)
        self.fileName = fileName
        self.fileNameEdit.setText(fileName)

    def saveFile(self) -> None:
        """
        保存文件
        :return: None
        """
        fileName = self.fileNameEdit.text()
        if os.path.sep not in fileName:
            if fileName == '':
                self.msgBox('请先设置文件名!')
                return
            if len(fileName) <= 4:
                self.msgBox('文件名非法!')
                return
            fileName = os.path.join('writing', fileName)
            if not os.path.exists('writing'):
                os.mkdir('writing')
        self.fileName = fileName
        with open(fileName, 'w+', encoding='UTF-8') as f:
            f.write(self.writingEdit.toPlainText())
        self.msgBox('文件已保存在{}'.format(fileName))

    def tips(self) -> None:
        text = self.writingEdit.toPlainText()
        if text == '':
            return
        self.tipsEdit.setPlainText('')
        if self.subThread is not None:
            self.subThread.terminate()
            while self.subThread.isRunning() and not self.subThread.isFinished():
                time.sleep(0.1)
        self.subThread = getTipsThread(self.writingEdit.toPlainText())
        self.subThread.signal.connect(self.setTips)
        self.subThread.start()

    def setTips(self, text: str) -> None:
        """
        设置提示
        :param text: 提示文本
        :return: None
        """
        self.tipsEdit.setPlainText(text)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
