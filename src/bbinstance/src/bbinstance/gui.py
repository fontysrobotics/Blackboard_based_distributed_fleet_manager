#!/usr/bin/env python

###############################################################################################
from python_qt_binding import QtWidgets
from python_qt_binding import QtCore
from python_qt_binding import QtGui
# from PyQt5 import QtCore, QtGui, QtWidgets

import rospy
from blackboard.msg import TaskMsg
from blackboard.Task import Task,TaskType,TaskStep,TaskState
from std_msgs.msg import String
from std_msgs.msg import Float32
from blackboard.msg import bbBackup
from geometry_msgs.msg import Pose , PointStamped

from threading import Lock


class Talker(): #change to multy topic publisher
    def __init__(self,nodeName):
        self.nodeName = nodeName
        self.pubNewTask = rospy.Publisher('newTask', TaskMsg,queue_size=10)
        self.pubRobotState = rospy.Publisher('robotState', String,queue_size=10)
        
        rospy.init_node(nodeName, anonymous=False)



###############################################################################################
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
###############################################################################################
        self.lock = Lock()
        self.talker = Talker('gui')
        rospy.Subscriber('bbBackup',bbBackup,self.backupFunction)   
        rospy.Subscriber('clicked_point',PointStamped,self.clickedPintRviz)
###############################################################################################


        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(560, 440)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gBnewTask = QtWidgets.QGroupBox(self.centralwidget)
        self.gBnewTask.setGeometry(QtCore.QRect(10, 60, 541, 291))
        self.gBnewTask.setObjectName("gBnewTask")
        self.gBc = QtWidgets.QGroupBox(self.gBnewTask)
        self.gBc.setEnabled(False)
        self.gBc.setGeometry(QtCore.QRect(420, 80, 111, 151))
        self.gBc.setObjectName("gBc")
        self.label_29 = QtWidgets.QLabel(self.gBc)
        self.label_29.setGeometry(QtCore.QRect(10, 30, 16, 21))
        self.label_29.setObjectName("label_29")
        self.label_30 = QtWidgets.QLabel(self.gBc)
        self.label_30.setGeometry(QtCore.QRect(10, 90, 21, 21))
        self.label_30.setObjectName("label_30")
        self.label_31 = QtWidgets.QLabel(self.gBc)
        self.label_31.setGeometry(QtCore.QRect(10, 60, 16, 21))
        self.label_31.setObjectName("label_31")
        self.cx = QtWidgets.QDoubleSpinBox(self.gBc)
        self.cx.setGeometry(QtCore.QRect(30, 30, 69, 26))
        self.cx.setObjectName("cx")
        self.cx.setRange(-100.0,100.0)
        self.cy = QtWidgets.QDoubleSpinBox(self.gBc)
        self.cy.setGeometry(QtCore.QRect(30, 60, 69, 26))
        self.cy.setObjectName("cy")
        self.cy.setRange(-100.0,100.0)
        self.cz = QtWidgets.QDoubleSpinBox(self.gBc)
        self.cz.setGeometry(QtCore.QRect(30, 90, 69, 26))
        self.cz.setObjectName("cz")
        self.cz.setRange(-100.0,100.0)
        self.cw = QtWidgets.QDoubleSpinBox(self.gBc)
        self.cw.setGeometry(QtCore.QRect(30, 120, 69, 26))
        self.cw.setObjectName("cw")
        self.cw.setRange(-100.0,100.0)
        self.label_39 = QtWidgets.QLabel(self.gBc)
        self.label_39.setGeometry(QtCore.QRect(10, 120, 21, 21))
        self.label_39.setObjectName("label_39")
        self.gBb = QtWidgets.QGroupBox(self.gBnewTask)
        self.gBb.setEnabled(False)
        self.gBb.setGeometry(QtCore.QRect(300, 80, 111, 151))
        self.gBb.setObjectName("gBb")
        self.label_40 = QtWidgets.QLabel(self.gBb)
        self.label_40.setGeometry(QtCore.QRect(10, 30, 16, 21))
        self.label_40.setObjectName("label_40")
        self.label_41 = QtWidgets.QLabel(self.gBb)
        self.label_41.setGeometry(QtCore.QRect(10, 90, 21, 21))
        self.label_41.setObjectName("label_41")
        self.label_42 = QtWidgets.QLabel(self.gBb)
        self.label_42.setGeometry(QtCore.QRect(10, 60, 16, 21))
        self.label_42.setObjectName("label_42")
        self.bx = QtWidgets.QDoubleSpinBox(self.gBb)
        self.bx.setGeometry(QtCore.QRect(30, 30, 69, 26))
        self.bx.setObjectName("bx")
        self.bx.setRange(-100.0,100.0)
        self.by = QtWidgets.QDoubleSpinBox(self.gBb)
        self.by.setGeometry(QtCore.QRect(30, 60, 69, 26))
        self.by.setObjectName("by")
        self.by.setRange(-100.0,100.0)
        self.bz = QtWidgets.QDoubleSpinBox(self.gBb)
        self.bz.setGeometry(QtCore.QRect(30, 90, 69, 26))
        self.bz.setObjectName("bz")
        self.bz.setRange(-100.0,100.0)
        self.bw = QtWidgets.QDoubleSpinBox(self.gBb)
        self.bw.setGeometry(QtCore.QRect(30, 120, 69, 26))
        self.bw.setObjectName("bw")
        self.bw.setRange(-100.0,100.0)
        self.label_43 = QtWidgets.QLabel(self.gBb)
        self.label_43.setGeometry(QtCore.QRect(10, 120, 21, 21))
        self.label_43.setObjectName("label_43")
        self.gBtaskType = QtWidgets.QGroupBox(self.gBnewTask)
        self.gBtaskType.setGeometry(QtCore.QRect(10, 80, 161, 151))
        self.gBtaskType.setObjectName("gBtaskType")
        self.radioButton = QtWidgets.QRadioButton(self.gBtaskType)
        self.radioButton.setEnabled(True)
        self.radioButton.setGeometry(QtCore.QRect(10, 30, 131, 23))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.gBtaskType)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 60, 101, 23))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.gBtaskType)
        self.radioButton_3.setGeometry(QtCore.QRect(10, 90, 131, 23))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self.gBtaskType)
        self.radioButton_4.setGeometry(QtCore.QRect(10, 120, 141, 23))
        self.radioButton_4.setObjectName("radioButton_4")
        self.gBa = QtWidgets.QGroupBox(self.gBnewTask)
        self.gBa.setEnabled(True)
        self.gBa.setGeometry(QtCore.QRect(180, 80, 111, 151))
        self.gBa.setObjectName("gBa")
        self.label_25 = QtWidgets.QLabel(self.gBa)
        self.label_25.setGeometry(QtCore.QRect(10, 30, 16, 21))
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(self.gBa)
        self.label_26.setGeometry(QtCore.QRect(10, 90, 21, 21))
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(self.gBa)
        self.label_27.setGeometry(QtCore.QRect(10, 60, 16, 21))
        self.label_27.setObjectName("label_27")
        self.ax = QtWidgets.QDoubleSpinBox(self.gBa)
        self.ax.setGeometry(QtCore.QRect(30, 30, 69, 26))
        self.ax.setObjectName("ax")
        self.ax.setRange(-100.0,100.0)
        self.ay = QtWidgets.QDoubleSpinBox(self.gBa)
        self.ay.setGeometry(QtCore.QRect(30, 60, 69, 26))
        self.ay.setObjectName("ay")
        self.ay.setRange(-100.0,100.0)
        self.az = QtWidgets.QDoubleSpinBox(self.gBa)
        self.az.setGeometry(QtCore.QRect(30, 90, 69, 26))
        self.az.setObjectName("az")
        self.az.setRange(-100.0,100.0)
        self.aw = QtWidgets.QDoubleSpinBox(self.gBa)
        self.aw.setGeometry(QtCore.QRect(30, 120, 69, 26))
        self.aw.setObjectName("aw")
        self.aw.setRange(-100.0,100.0)
        self.label_28 = QtWidgets.QLabel(self.gBa)
        self.label_28.setGeometry(QtCore.QRect(10, 120, 21, 21))
        self.label_28.setObjectName("label_28")
        self.btnAddTask = QtWidgets.QPushButton(self.gBnewTask)
        self.btnAddTask.setEnabled(True)
        self.btnAddTask.setGeometry(QtCore.QRect(10, 240, 521, 31))
        self.btnAddTask.setObjectName("btnAddTask")
        self.widget = QtWidgets.QWidget(self.gBnewTask)
        self.widget.setGeometry(QtCore.QRect(10, 30, 521, 28))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.sBtaskid = QtWidgets.QSpinBox(self.widget)
        self.sBtaskid.setObjectName("sBtaskid")
        self.horizontalLayout.addWidget(self.sBtaskid)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.sbtaskPriority = QtWidgets.QSpinBox(self.widget)
        self.sbtaskPriority.setObjectName("sbtaskPriority")
        self.horizontalLayout.addWidget(self.sbtaskPriority)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.sbtaskPayload = QtWidgets.QSpinBox(self.widget)
        self.sbtaskPayload.setObjectName("sbtaskPayload")
        self.horizontalLayout.addWidget(self.sbtaskPayload)
        self.gBrobotState = QtWidgets.QGroupBox(self.centralwidget)
        self.gBrobotState.setGeometry(QtCore.QRect(10, 360, 541, 71))
        self.gBrobotState.setObjectName("gBrobotState")
        self.sBrobotId = QtWidgets.QSpinBox(self.gBrobotState)
        self.sBrobotId.setGeometry(QtCore.QRect(80, 30, 48, 31))
        self.sBrobotId.setObjectName("sBrobotId")
        self.radioButton_5 = QtWidgets.QRadioButton(self.gBrobotState)
        self.radioButton_5.setGeometry(QtCore.QRect(140, 32, 61, 31))
        self.radioButton_5.setChecked(True)
        self.radioButton_5.setObjectName("radioButton_5")
        self.radioButton_6 = QtWidgets.QRadioButton(self.gBrobotState)
        self.radioButton_6.setGeometry(QtCore.QRect(280, 32, 71, 31))
        self.radioButton_6.setObjectName("radioButton_6")
        self.radioButton_7 = QtWidgets.QRadioButton(self.gBrobotState)
        self.radioButton_7.setGeometry(QtCore.QRect(210, 32, 51, 31))
        self.radioButton_7.setObjectName("radioButton_7")
        self.btnsetRobotState = QtWidgets.QPushButton(self.gBrobotState)
        self.btnsetRobotState.setEnabled(True)
        self.btnsetRobotState.setGeometry(QtCore.QRect(380, 30, 151, 31))
        self.btnsetRobotState.setObjectName("btnsetRobotState")
        self.label_32 = QtWidgets.QLabel(self.gBrobotState)
        self.label_32.setGeometry(QtCore.QRect(10, 30, 81, 31))
        self.label_32.setObjectName("label_32")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 81, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(300, 20, 141, 17))
        self.label_2.setObjectName("label_2")
        self.lblblackBoard = QtWidgets.QLabel(self.centralwidget)
        self.lblblackBoard.setGeometry(QtCore.QRect(100, 20, 141, 17))
        font = QtGui.QFont()
        font.setItalic(True)
        self.lblblackBoard.setFont(font)
        self.lblblackBoard.setObjectName("lblblackBoard")
        self.lblbackupBlackboard = QtWidgets.QLabel(self.centralwidget)
        self.lblbackupBlackboard.setGeometry(QtCore.QRect(450, 20, 91, 17))
        font = QtGui.QFont()
        font.setItalic(True)
        self.lblbackupBlackboard.setFont(font)
        self.lblbackupBlackboard.setObjectName("lblbackupBlackboard")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.currentpint = 1


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BlackBoard"))
        self.gBnewTask.setTitle(_translate("MainWindow", "New Task"))
        self.gBc.setTitle(_translate("MainWindow", "C"))
        self.label_29.setText(_translate("MainWindow", "X"))
        self.label_30.setText(_translate("MainWindow", "Z"))
        self.label_31.setText(_translate("MainWindow", "Y"))
        self.label_39.setText(_translate("MainWindow", "w"))
        self.gBb.setTitle(_translate("MainWindow", "B"))
        self.label_40.setText(_translate("MainWindow", "X"))
        self.label_41.setText(_translate("MainWindow", "Z"))
        self.label_42.setText(_translate("MainWindow", "Y"))
        self.label_43.setText(_translate("MainWindow", "w"))
        self.gBtaskType.setTitle(_translate("MainWindow", "Task Type"))
        self.radioButton.setText(_translate("MainWindow", "Go A"))
        self.radioButton_2.setText(_translate("MainWindow", "Go A Go B"))
        self.radioButton_3.setText(_translate("MainWindow", "Go A Pick B"))
        self.radioButton_4.setText(_translate("MainWindow", "Go A Pick B Go C"))
        self.gBa.setTitle(_translate("MainWindow", "A"))
        self.label_25.setText(_translate("MainWindow", "X"))
        self.label_26.setText(_translate("MainWindow", "Z"))
        self.label_27.setText(_translate("MainWindow", "Y"))
        self.label_28.setText(_translate("MainWindow", "w"))
        self.btnAddTask.setText(_translate("MainWindow", "Add Task"))
        self.label_3.setText(_translate("MainWindow", "Task ID"))
        self.label_4.setText(_translate("MainWindow", "Task Priority"))
        self.label_5.setText(_translate("MainWindow", "Task Payload"))
        self.gBrobotState.setTitle(_translate("MainWindow", "Set Robot State"))
        self.radioButton_5.setText(_translate("MainWindow", "Busy"))
        self.radioButton_6.setText(_translate("MainWindow", "Defect"))
        self.radioButton_7.setText(_translate("MainWindow", "Idle"))
        self.btnsetRobotState.setText(_translate("MainWindow", "Set State"))
        self.label_32.setText(_translate("MainWindow", "Robot ID"))
        self.label.setText(_translate("MainWindow", "BlackBoard:"))
        self.label_2.setText(_translate("MainWindow", "Backup BlackBoard:"))
        self.lblblackBoard.setText(_translate("MainWindow", "None"))
        self.lblbackupBlackboard.setText(_translate("MainWindow", "None"))



###############################################################################################
        self.radioButton.clicked.connect(self.aActivate)
        self.radioButton_2.clicked.connect(self.abActivate)
        self.radioButton_3.clicked.connect(self.abActivate)
        self.radioButton_4.clicked.connect(self.abcActivate)
        self.btnAddTask.clicked.connect(self.addTaskFunction)



    def clickedPintRviz(self,data):
        if self.currentpint == 1:
            self.ax.setValue(data.point.x)
            self.ay.setValue(data.point.y)
            self.currentpint = 2
            return
        if self.currentpint == 2:
            self.bx.setValue(data.point.x)
            self.by.setValue(data.point.y)
            self.currentpint = 3
            return
        if self.currentpint == 3:
            self.cx.setValue(data.point.x)
            self.cy.setValue(data.point.y)
            self.currentpint = 1
            return


    def resetInterface(self):
        self.sbtaskPriority.setValue(0)
        self.sbtaskPayload.setValue(0)
        self.ax.setValue(0)
        self.ay.setValue(0)
        self.az.setValue(0)
        self.aw.setValue(0)

        self.bx.setValue(0)
        self.by.setValue(0)
        self.bz.setValue(0)
        self.bw.setValue(0)

        self.cx.setValue(0)
        self.cy.setValue(0)
        self.cz.setValue(0)
        self.cw.setValue(0)
        self.currentpint = 1


    def aActivate(self,event):
        self.gBa.setEnabled(True)
        self.gBb.setEnabled(False)
        self.gBc.setEnabled(False)
        self.currentpint = 1

    def abActivate(self,event):
        self.gBa.setEnabled(True)
        self.gBb.setEnabled(True)
        self.gBc.setEnabled(False)
        self.currentpint = 1
  
    def abcActivate(self,event):
        self.gBa.setEnabled(True)
        self.gBb.setEnabled(True)
        self.gBc.setEnabled(True)
        self.currentpint = 1


    def backupFunction(self,data):
        if self.lock.locked() is False:
            self.lock.acquire()
            self.lblblackBoard.setText(data.bbAdress)
            self.lblbackupBlackboard.setText(data.buAdress)
            self.lock.release()

    def addTaskFunction(self,event):
        posearray = []
        posea = Pose()
        poseb = Pose()
        posec = Pose()
        tskmsg = TaskMsg()

        
        
        if self.radioButton.isChecked():
            posearray = []
            posea.position.x = self.ax.value()
            posea.position.y = self.ay.value()
            posea.position.z = self.az.value()
            posea.orientation.w = self.aw.value()
            posearray.append(posea)
            tskmsg.taskType = 1

        if self.radioButton_2.isChecked():
            posearray = []
            posea.position.x = self.ax.value()
            posea.position.y = self.ay.value()
            posea.position.z = self.az.value()
            posea.orientation.w = self.aw.value()
            poseb.position.x = self.bx.value()
            poseb.position.y = self.by.value()
            poseb.position.z = self.bz.value()
            poseb.orientation.w = self.bw.value()
            posearray.append(posea)
            posearray.append(poseb)
            tskmsg.taskType = 2

        if self.radioButton_3.isChecked():
            posearray = []
            posea.position.x = self.ax.value()
            posea.position.y = self.ay.value()
            posea.position.z = self.az.value()
            posea.orientation.w = self.aw.value()
            poseb.position.x = self.bx.value()
            poseb.position.y = self.by.value()
            poseb.position.z = self.bz.value()
            poseb.orientation.w = self.bw.value()
            posearray.append(posea)
            posearray.append(poseb)
            tskmsg.taskType = 3

        if self.radioButton_4.isChecked():
            posearray = []
            posea.position.x = self.ax.value()
            posea.position.y = self.ay.value()
            posea.position.z = self.az.value()
            posea.orientation.w = self.aw.value()
            poseb.position.x = self.bx.value()
            poseb.position.y = self.by.value()
            poseb.position.z = self.bz.value()
            poseb.orientation.w = self.bw.value()
            posec.position.x = self.cx.value()
            posec.position.y = self.cy.value()
            posec.position.z = self.cz.value()
            posec.orientation.w = self.cw.value()
            posearray.append(posea)
            posearray.append(poseb)
            posearray.append(posec)
            tskmsg.taskType = 4

           
        
        
        tskmsg.taskId = self.sBtaskid.value()
        tskmsg.priority = self.sbtaskPriority.value()
        tskmsg.payload = self.sbtaskPayload.value()
        tskmsg.taskState = 1
        tskmsg.pose = posearray
        self.sBtaskid.setValue(self.sBtaskid.value()+1)
        self.resetInterface()
        self.talker.pubNewTask.publish(tskmsg)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())
