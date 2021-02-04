#---------------------------------------------------------------- 
# Blackboard distributed fleet manager - Fontys lectoraat
# Sep 2020 - Feb 2021 internship Eindhoven BIC
# Hussam Ayoub, 356203@student.fontys.nl

#----------------------------Description------------------------- 
# 
# The Robot class is intended to run as an independent ros node on
# different robots from different vendors. it processes new tasks 
# calculate the cost of executing a certain task based on the robot
# charactaristis and it is responsable for executing a task through
# the "Controller" object which is initilized in the robot class.
#----------------------------------------------------------------



import random                                                  # for testing purboses
from enum import Enum         

import rospy   

from geometry_msgs.msg import Pose                             # ros pose msg
from geometry_msgs.msg import PoseWithCovarianceStamped
from rosnode import rosnode_ping                               # ROS node ping                  
from blackboard.msg import TaskMsg                             # ROS custom msgs
from blackboard.msg import TaskCost                            #
from blackboard.msg import bbBackup                            #
from std_msgs.msg import String                                #
from blackboard.msg import TaskStateMsg                        #

from RosCommunication import Talker                            # blackboard package classes
from Blackboard import Blackboard                              #                        
from blackboard.Controller import Controller                   #
from Task import Task, TaskState, TaskType, TaskStep, StepType #
from blackboard.Battery import Battery

from threading import Lock,Thread                              # Python threading
import math


# Robot state enums
class RobotState(Enum):
    busy = 0
    defect = 1
    idle = 2

# Start Robot class
class Robot:
    def __init__(self, bbAdress, backupAdress, robotId, robotType, repeatability, accuracy, payload, mxVelLinear, mxVelAngular, battery,nodeName,talker):
        self.talker = talker                    # ROS publishers ande node init
        self.bb = Blackboard(0,self.talker)     # inactive instance of blackboared
        self.bbAdress = bbAdress                # blackboard adress
        self.buAdress = backupAdress            # backup adress
        self.robotId = robotId                  # robot Id
        self.robotType = robotType              # robot type , "agv , heterogenous"
        
        self.repeatability = repeatability      # robot charactaristics
        self.accuracy = accuracy                #
        self.payload = payload                  #
        self.mxVelAngular = mxVelAngular        #
        self.mxVelLinear = mxVelLinear          #

        self.battery = battery                  # battery class instance
        self.state = RobotState.idle            # current robot state 
        self.nodeName = nodeName                # ROS node name "naming rule: Robot + robotId"
        self.bbState = True                     # current blackboard state "online , offline"
        self.currentTaskList = []               # assigned tasks list
        self.currentTaskid = 0                  # points to the current task index in currentTaskList
        self.taskCounter = -1                   # number of recived tasks
        self.currentTask = None
        self.amclx = 0                          # holds amcl topic pose
        self.amcly = 0                          #


        self.controller = Controller(nodeName)                                 # instance of controller class
        rospy.Subscriber('taskBC',TaskMsg,self.getTaskCost)                         # Ros subscribers
        rospy.Subscriber('taskAssign',TaskMsg,self.addTask)                         #
        amclPose = '/'+self.nodeName+'/amcl_pose'                                    # topic name based on robot id
        rospy.Subscriber(amclPose,PoseWithCovarianceStamped,self.initialPose)       # 
        self.bbBackupSub = rospy.Subscriber('bbBackup',bbBackup,self.bbBackup)      #

        self.pingTimer = rospy.Timer(rospy.Duration(5),self.pingBlackboard)         # ros timers for function callback over duration
        self.bbBackupTimer = rospy.Timer(rospy.Duration(3),self.bbBackupActivate)   #
        self.exeTimer = rospy.Timer(rospy.Duration(1),self.executeTask)             #


        self.lock = Lock()              # Lock used to lock callback functions  
        self.execLock = Lock()          # task execution lock
        self.addtaskLock = Lock()       # adding a task lock
        self.taskCostLock = Lock()      #
        self.updateLock = Lock()        #
        self.pingLock = Lock()          #
        self.bbactiveLock = Lock()      #


    # Callback triggered on '/robotx/amcl_pose' topic updates robot amclx and amcly
    def initialPose(self,data):
        if self.taskCostLock.locked() is False:
            self.amclx = data.pose.pose.position.x            
            self.amcly = data.pose.pose.position.y
        
  
    # Callback triggered on 'bbBackup' topic updates the current blackboard and backup adress
    def bbBackup(self,data):
        if self.lock.locked() is False:         # check lock
            self.lock.acquire()         
            self.bbAdress = data.bbAdress       # update adress
            self.buAdress = data.buAdress       # update backup adress
            self.bbState = True                 # blackboard is online
            self.lock.release()                 

    
    # callback triggered on 'taskAssign' topic
    def addTask(self,data):
        if self.addtaskLock.locked() is False:      #check lock
            self.addtaskLock.acquire()              
            if data.robotId is self.robotId:        # if msg is intended to this robot
                # create a new task with the topic data values
                self.newtask = Task(data.taskId,data.priority,data.taskType,data.pose,data.payload)
                self.newtask.cost = data.cost
                self.newtask.energyCost = data.energyCost
                self.newtask.taskState = TaskState.Assigned
                # add task to the list check the list for task priority insert in right order or at the end
                counter = 0                                                     # stores the index of the current list item
                for t in self.currentTaskList:                                  # loop over the current task list
                    if t.priority < self.newtask.priority:                      # compare task priority
                        if t.taskState is TaskState.Assigned:                   # check if the task is not in execution yet
                            self.currentTaskList.insert(counter,self.newtask)   # insert the new task at the index
                            return                                              # if conditions met break the function
                    counter = counter + 1                                       # increase the counter 
                self.currentTaskList.append(self.newtask)                       # if condition are not met append at the end of list             
                self.taskCounter = self.taskCounter + 1                         # increase assigned task counter                       
            self.addtaskLock.release()                                          # release thread lock
            
    
    
    # callback triggered over 'taskCost' topic calculates the cost of executing a task 
    # current task  
    def getTaskCost(self,data):
        if self.taskCostLock.locked() is False:
            self.taskCostLock.acquire()
            cost = 1000
            cr = 10
            energyTolerance = 10
            energyAtTask = 0
            preTasks = 1

            

            if data.payload > self.payload:
                self.updateBlackboard(self.robotId,data.taskId,cost,0)
                print('first execption')
                self.taskCostLock.release()
                return

            x = self.amclx
            y = self.amcly
            distance = -1

            for pos in data.pose:
                distance = distance + (math.sqrt((pos.position.x - x)**2) + math.sqrt((pos.position.y - y)**2))
                x = pos.position.x
                y = pos.position.x


            fr = cr * (data.payload + self.payload)
            en = fr * distance

            
            energyCost = en / self.battery.getVolt()
            print(self.nodeName,'    distance:',distance,'     Energy:',energyCost)

            if energyCost >= self.battery.getAmps()/energyTolerance:
                cost = 1000
                self.updateBlackboard(self.robotId,data.taskId,cost,0)
                print('second exception')
                self.taskCostLock.release()
                return


            for t in self.currentTaskList:
                if t.priority >= data.priority:
                    energyAtTask = energyAtTask + t.energyCost
                    preTasks = preTasks + 1
            energyAtTask = self.battery.getAmps() - energyAtTask
            
            if energyAtTask <= energyTolerance:
                cost = 1000
                self.updateBlackboard(self.robotId,data.taskId,cost,0)
                print('third exception')
                self.taskCostLock.release()
                return
            if energyAtTask is not 0:
                cost = energyCost * preTasks / energyAtTask
            self.updateBlackboard(self.robotId,data.taskId,cost,energyCost)

            self.taskCostLock.release()

    # Sends the calculated cost to blackboard
    def updateBlackboard(self,robotId,taskId,taskCost,energyCost):
        if self.updateLock.locked() is False:           # check lock
            self.updateLock.acquire()
            tskCst = TaskCost()                         # instance of custom ROS msg
            tskCst.robotId = robotId            
            tskCst.taskId = taskId
            tskCst.taskCost = taskCost
            tskCst.energyCost = energyCost
            self.talker.pub_taskCost.publish(tskCst)    # publish over topic
            self.updateLock.release()
        


    # Callback to execute tasks in task list called over ROS timer
    def executeTask(self,event):
        if self.taskCounter >= 0:                                   # check if tasks are assigned
            statemsg = TaskStateMsg()                               # instance of custom task state msg
            if self.execLock.locked() is False:                     # check lock
                self.execLock.acquire()                             # if not locked the lock

                if self.state is RobotState.idle:
                    for tasks in self.currentTaskList:                  # loop to assign current task
                        if tasks.taskState is TaskState.Assigned:       # changed after ordering the list by prioritys
                            self.currentTask = tasks
                            break

                
                if self.state is RobotState.idle:                   # if the robot is idle
                    if self.currentTask.taskState is not TaskState.Done:           # if the task is not done
                        self.state = RobotState.busy                # set robot state to busy
                        statemsg.taskId = self.currentTask.taskId                  # initilize the state message with current task id 
                        statemsg.taskState = 1                      # set task state to started 
                        self.currentTask.taskState = TaskState.Started
                        self.talker.pub_taskState.publish(statemsg) # update blackboard with new task state
                        self.controller.startExecute(self.currentTask)             # call task execution on controller class

                if self.controller.state == 1:                      # if controller class is done
                    if self.state is RobotState.busy:                   # if the robot is idle
                        statemsg.taskId = self.currentTask.taskId                      # initilize state message with current task id
                        statemsg.taskState = 2                          # set task state to done
                        self.currentTask.taskState = TaskState.Done
                        self.talker.pub_taskState.publish(statemsg)     # update blackboard with new task state
                        self.battery.updateLevel(self.currentTask.energyCost)          # update robot battery level
                        self.state = RobotState.idle                    # set robot state to idle
                              
                self.execLock.release()                             # release the lock
    
    
    # Set current robot state 
    def setState(self,state):
        self.state = state

    # Callback triggered on ROS timer checks if the blackboard is online
    def pingBlackboard(self,event):
        if  self.pingLock.locked() is False:                            # check lock
            self.pingLock.acquire()
            self.bbState = rosnode_ping(self.bbAdress,1)                # ping  blackboard node, assign result to bbstate
            if self.bbState is False:                                   # if node is offline 
                self.bbthread = Thread(target=self.bbBackupActivate)    # start backup function on a new thread
            self.pingLock.release()
                    
        
    # backup function invoked incase blackboard is offline     
    def bbBackupActivate(self,event):
        if self.bbactiveLock.locked() is False:                     # check lock
            self.bbactiveLock.acquire()
            if self.bbState is False:                               # check if blackboard is offline
                if self.nodeName == self.buAdress:                  # if Robot is the bakcup blackboard
                    self.bbState = True                             # blackboard state is online
                    self.pingTimer.shutdown()                       # shutdown ping timer
                    self.oldbbadress = self.bbAdress                # store the last known blackboard adress
                    self.bb = Blackboard(1,self.talker)             # initilize a new instance of blackboard
                    
                    if self.nodeName == 'robot1':                    # hard coded for testing will be replaced with a list
                        self.bb.robotnr = 4
                        self.bb.buAdress = 'robot2'                     
                    
                    if self.nodeName == 'robot2':
                        self.bb.robotnr = 3
                        self.bb.buAdress = 'robot3'

                    if self.nodeName == 'robot3':
                        self.bb.robotnr = 2
                        self.bb.buAdress = 'robot4'


                    if self.nodeName == 'robot4':
                        self.bb.robotnr = 1
                        self.bb.buAdress = 'robot4'
                        
            self.bbactiveLock.release()




