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
from blackboard.msg import bbsynch
from geometry_msgs.msg import Pose , PointStamped
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Pose, Point, Vector3, Quaternion
from std_msgs.msg import ColorRGBA
from threading import Lock
import rviz_tools_py as rviz_tools

class Talker(): #change to multy topic publisher
    def __init__(self,nodeName):
        self.nodeName = nodeName
        self.pubNewTask = rospy.Publisher('BbSync', bbsynch,queue_size=10)
        rospy.init_node(nodeName, anonymous=False)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.lock = Lock()
        self.talker = Talker('taskview')
        rospy.Subscriber('BbSync',bbsynch,self.taskview)   



        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listView = QtWidgets.QListWidget(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(10, 40, 771, 521))
        self.listView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listView.setObjectName("listView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 67, 17))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.tasklist = []
        self.markers = rviz_tools.RvizMarkers('/map','markers')
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Task View"))
        self.label.setText(_translate("MainWindow", "Tasks"))


    def taskview(self,data):
        self.tasklist = []
        for taskmsg in data.tasks:
            task = Task(taskmsg.taskId,taskmsg.priority,taskmsg.taskType,taskmsg.pose,taskmsg.payload)
            task.robotId = taskmsg.robotId
            task.cost = taskmsg.cost
            task.taskState = taskmsg.taskState
            self.tasklist.append(task)
        self.createMarkers()
        self.viewTasks()

    def viewTasks(self):
        self.listView.clear()
        for t in self.tasklist:
            tmpstr = self.taskToString(t)
            self.listView.addItem(tmpstr)

    def taskToString(self,tsk):
        stt = ''
        if tsk.taskState == 0:
            stt = 'Waitting'
        elif tsk.taskState == 1:
            stt = 'Started'
        elif tsk.taskState == 2:
            stt = 'Done'
        elif tsk.taskState == 3:
            stt = 'Assigned'
        strng = 'TaskId: '+ str(tsk.taskId) +'   |   Priority: ' +str(tsk.priority) +'   |   State: '+ stt+'   |   RobotId: '+ str(tsk.robotId)
        return strng

    def createMarkers(self):
        self.markers.deleteAllMarkers()
        stepCounter = 0
        
        for t in self.tasklist:
            if t.taskState is not 2:
                finalStep = 0
                lenght = len(t.pose)
                for po in t.pose:
                    finalStep = finalStep + 1
                    markerpose = po
                    markerpose.orientation.x = 1
                    markerpose.orientation.y = 0
                    markerpose.orientation.z = -1
                    markerpose.orientation.w = 0
                    markerpose.position.z = 0.5
                    scale = 0.5
                    id = t.taskId+stepCounter
                    color = 'gray'
                    if t.robotId == 1:
                        color = 'green'
                    if t.robotId == 2:
                        color = 'red'
                    if t.robotId == 3:
                        color = 'orange'
                    if t.robotId == 4:
                        color = 'yellow'
                    if finalStep == lenght:
                        markerpose.position.z = 1.0
                        scale = 1.0
                    self.markers.publishArrow(markerpose,color,scale,100)
                    stepCounter = stepCounter+1
    



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())
