from Task import Task, TaskState, TaskType, TaskStep, StepType
from geometry_msgs.msg import Pose
from enum import Enum
import rospy
from blackboard.msg import TaskMsg
import random
from RosCommunication import Talker
from blackboard.msg import TaskCost
from std_msgs.msg import String
from rosnode import rosnode_ping
from blackboard.msg import bbBackup
from Blackboard import Blackboard
from threading import Lock

class RobotState(Enum):
    busy = 0
    defect = 1
    idle = 2

class Robot:
    def __init__(self, bbAdress, backupAdress, robotId, robotType, repeatability, accuracy, payload, mxVelLinear, mxVelAngular, battery,nodeName,talker):
        self.talker = talker
        self.bb = Blackboard(0,self.talker)
        self.bbAdress = bbAdress
        self.buAdress = backupAdress
        self.robotId = robotId
        self.robotType = robotType
        self.repeatability = repeatability
        self.accuracy = accuracy
        self.payload = payload
        self.mxVelAngular = mxVelAngular
        self.mxVelLinear = mxVelLinear
        self.battery = battery
        self.state = 0
        self.nodeName = nodeName
        self.bbState = True
        
        rospy.Subscriber('taskBC',TaskMsg,self.getTaskCost)
        rospy.Subscriber('taskAssign',TaskMsg,self.addTask)
        self.bbBackupSub = rospy.Subscriber('bbBackup',bbBackup,self.bbBackup)
        self.pingTimer = rospy.Timer(rospy.Duration(1),self.pingBlackboard)
        self.bbBackupTimer = rospy.Timer(rospy.Duration(3),self.bbBackupActivate)
        self.lock = Lock()
  

    def bbBackup(self,data):
        if self.lock.locked() is False:
            self.lock.acquire()
            self.bbAdress = data.bbAdress
            self.buAdress = data.buAdress
            # print('reached')
            self.bbState = True
            self.lock.release()



    
    def registerRobot(robotId, topicMessage):
        # send robot id and computation power to register robot in blackboard
        pass

    def addTask(self,data):  # add the recived task to the current task field
        if data.robotId is self.robotId:
            print('I have been assigned task nr:')
            print(data.taskId)
            
            
    def getTaskCost(self,data):
        y = random.randint(1,10)
        self.updateBlackboard(self.robotId,data.taskId,y)

    def updateBlackboard(self,robotId,taskId,taskCost):
        tskCst = TaskCost()
        tskCst.robotId = robotId
        tskCst.taskId = taskId
        tskCst.taskCost = taskCost
        self.talker.pub_taskCost.publish(tskCst)
        

    def executeTask(task, controller):
        # execute each task step
        pass

    def setState(state):
        self.state = state

    def cancelTask():
        # update blackboard with task canceld
        pass

    def unregister():
        # update blackboard
        pass

    def pingBlackboard(self,event):
        if  self.lock.locked() is False:
            self.lock.acquire()
            self.bbState = rosnode_ping(self.bbAdress,1)
            # print (self.bbState,self.bbAdress,self.buAdress,self.talker.nodeName)
            self.lock.release()
                    

        
        
    def bbBackupActivate(self,event):
        if self.lock.locked() is False:
            self.lock.acquire()
            # print('bbactivation reach')
            if self.bbState is False:
                if self.nodeName == self.buAdress:
                    # print('condition activbation callback')
                    self.pingTimer.shutdown()
                    self.bbState = True
                    self.bbAdress = self.talker.nodeName
                    self.buAdress = 'robot2'
                    bumsg = bbBackup()
                    bumsg.bbAdress = self.bbAdress
                    bumsg.buAdress = self.buAdress
                    self.bb.robotnr = self.bb.robotnr -1
                    self.bb.activateBlackboard(self.talker,'robot2')
                    self.talker.pub_bbBackup.publish(bumsg)
                    self.bbState = True
                    
                    self.pingTimer.shutdown()
                    return
            self.lock.release()


    def analyzeTask():  # split the task into a list of steps
        self.currentTask.stepsList.append(TaskStep(stepType,pose))
