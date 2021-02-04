#---------------------------------------------------------------- 
# Blackboard distributed fleet manager - Fontys lectoraat
# Sep 2020 - Feb 2021 internship Eindhoven BIC
# Hussam Ayoub, 356203@student.fontys.nl

#----------------------------Description------------------------- 
# 
# The blackboard class is responsable for handeling new tasks and
# assignning a task to a certain robot.
# A new task is monitored over 'newTask' ROS topic, added to the 
# task list and broadcasted to robots through 'taskBc' topic for 
# reciving task costs on 'taskCost', then a task is assigned to 
# be executed based on the recived costs using 'taskAssign' Topic
#----------------------------------------------------------------


import rospy
from Task import Task,TaskState,TaskStep,TaskType  # task class, and enums
from RosCommunication import Talker                # RosCommunication instance inits Node, publishers
from std_msgs.msg import String                    # Message Type
from blackboard.msg import TaskMsg                 # Custom ROS messages
from blackboard.msg import TaskCost                #
from blackboard.msg import bbBackup                #
from blackboard.msg import bbsynch                 #
from blackboard.msg import TaskStateMsg            #


#Class blackboard Start:
class Blackboard:
    #Class constructor
    def __init__(self, state,talker):                # talker of ROS communication Class type
        
        self.state   = state                         # 0/1 state used to initilize an inactive instance
        self.talker  = talker                        # init talker
        self.robotnr = 4                             # Keeps track of current Nr of active robots "static for test purposes"

        if state is 1:                               # Incase the blackboard instance is active declare variables
            self.taskList = []                       # Local list of Tasks                     
            self.buAdress = 'robot1'                 # Current backup adress "Static for testing purposes -> change to a list based on processing resouces"

            # ROS topic subscribers (ROS Topic Name , Message Type, Callback function)
            rospy.Subscriber('newTask',TaskMsg,self.addTask)
            rospy.Subscriber('taskCost',TaskCost,self.processTaskCost)
            rospy.Subscriber('TaskStateMsg',TaskStateMsg,self.taskStateUpdate)

            # ROS Timers invoked every rospy.Duration in seconds (duration in seconds , callback function)
            self.bbBackuptimer = rospy.Timer(rospy.Duration(1),self.bbBackup)
            self.syncTimer = rospy.Timer(rospy.Duration(2),self.bbsynch)
         
            print('new blackboard object created')    # Logging Message

    # Callback when data is recived over 'TaskStateMsg' used to update task state via robots "started , done"
    def taskStateUpdate(self,data):
        for t in self.taskList:                         # search loop
            if t.taskId == data.taskId:
                if data.taskState ==1:                  # enum not used in ROS custom messages 1 = Started       
                    t.taskState = TaskState.Started     # change task state based on recived data
                if data.taskState ==2:                  # 2 = Done
                    t.taskState = TaskState.Done        # change task state based on recived data


    # Callback in self.syncTimer rospy.Timer used to syncronize current task list with backup blackboard, and taskview
    def bbsynch(self,event):
        syncarray = []                                  # temp array to be sent over synch topic
        sync = bbsynch()                                # declare a custom message instance
        for task in self.taskList:                      # loop over local task list and convert to custom ROS TaskMsg 'bbsynch'
            tmsg = TaskMsg()                            #
            tmsg.taskId = task.taskId                   #
            tmsg.priority = task.priority               #
            tmsg.taskType = task.taskType               #
            tmsg.payload = task.payload                 #
            tmsg.taskState = task.taskState.value       #
            tmsg.pose = task.pose                       #
            tmsg.robotId = task.robotId                 #
            syncarray.append(tmsg)                      # append converted task to temp msg array
        sync.tasks = syncarray                          # store the temp taskMsg array in the message variable
        self.talker.pub_bbSync.publish(sync)            # publish over ROS topic

       

    
    # Callback triggered through 'newTask' ROS subscriber checks for task and broadcasts it.
    # ---------------Future advice - run a task check before accepting---------------------
    def addTask(self,data):
        id = data.taskId            # check for current task existance in local task list
        for t in self.taskList:     # check loop
            if t.taskId is id:
                break
        #if the task doesnt exist create a new task object with the topic data
        tsk = Task(data.taskId,data.priority,data.taskType,data.pose,data.payload)
        self.taskList.append(tsk)   # append the task to the local task list
        self.broadcastTask(tsk)     # broadcast the task


    # broadcast a task over 'taskBC' topic to subscribed robots 
    def broadcastTask(self,task): 
        tmsg = TaskMsg()                        # instance of custom ROS msg
        tmsg.taskId = task.taskId               # initilize custom msg fields
        tmsg.priority = task.priority           #
        tmsg.taskType = task.taskType           #
        tmsg.payload = task.payload             #
        tmsg.taskState = task.taskState.value   #
        tmsg.pose = task.pose                   #
        self.talker.pub_taskBC.publish(tmsg)    # publish the message

        
        
    

    
    # Callback triggered when a task cost is recived over 'taskCost' topic
    def processTaskCost(self,data):
        for t in self.taskList:                     # check if the task exists in the list
            if t.taskId == data.taskId:             # when the task is found
                if t.cost  >= data.taskCost:        # if recived cost is lower that current cost
                    t.robotId = data.robotId        # adjust robot id field in the task
                    t.cost = data.taskCost          # adjust the cost
                    t.energyCost = data.energyCost  # adjust energy cost
                t.recivedCosts = t.recivedCosts+1   # increase the recived costs counter
            if t.recivedCosts == self.robotnr:      # if the blackboard recived costs from all online robots
                self.assignTask(t)                  # assign the task to the robot with lowest cost
        

    # assign task function converts a task object to custom ROS msg and publishes over 'taskAssign' topic
    def assignTask(self,task):
        if task.taskState is TaskState.Waitting:        # check if the task is not assigned
            tmsg = TaskMsg()                            # instance of custom ROS msg
            tmsg.robotId = task.robotId                 # assign the task fields to msg fields
            tmsg.taskId = task.taskId                   #
            tmsg.priority = task.priority               #
            tmsg.taskType = task.taskType               #
            tmsg.payload = task.payload                 #
            tmsg.taskState = task.taskState.value       #
            tmsg.pose = task.pose                       #
            tmsg.cost = task.cost                       #
            tmsg.energyCost = task.energyCost           #
            task.taskState = TaskState.Assigned         # change the task state to assigned
            self.talker.pub_taskAssign.publish(tmsg)    # publish the task over the mentioned topic

        

    # Callback triggered over ROS timer every rospy.duration to broadcast current blackboard and backup adresses 
    def bbBackup(self,event=None):
        bumsg = bbBackup()                          # instance of custom ROS msg
        bumsg.bbAdress = self.talker.nodeName       # blackboard adress
        bumsg.buAdress = self.buAdress              # backup adress 
        self.talker.pub_bbBackup.publish(bumsg)     # publish over the topic
    
        