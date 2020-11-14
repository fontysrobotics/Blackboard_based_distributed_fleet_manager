#!/usr/bin/env python

from python_qt_binding import QtWidgets
from python_qt_binding import QtCore
from python_qt_binding import QtGui
# from PyQt5 import QtCore, QtGui, QtWidgets

import rospy
from std_msgs.msg import String
from blackboard.msg import TaskMsg
from blackboard.msg import bbBackup
from blackboard.msg import TaskCost
from threading import Lock

class Talker(): #change to multy topic publisher
    def __init__(self,nodeName):
        self.nodeName = nodeName
        self.pub = rospy.Publisher('top', String,queue_size=10)
        
        rospy.init_node(nodeName, anonymous=False)

class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        self.lock = Lock()
        self.talker = Talker('interface')
        rospy.Subscriber('bbBackup',bbBackup,self.bbBackup)        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(120, 120, 89, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(230, 120, 89, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(140, 200, 112, 23))
        self.radioButton.setObjectName("radioButton")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(130, 250, 92, 23))
        self.checkBox.setObjectName("checkBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.clickevent)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.radioButton.setText(_translate("MainWindow", "RadioButton"))
        self.checkBox.setText(_translate("MainWindow", "CheckBox"))


    def clickevent(self,event):
        self.talker.pub.publish('message')

    def bbBackup(self,data):
        if self.lock.locked() is False:
            self.lock.acquire()
            self.pushButton_2.setText(data.bbAdress)
            self.pushButton.setText(data.buAdress)
            self.lock.release()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())