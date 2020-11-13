import rospy
from Task import Task,TaskState,TaskStep,TaskType
from RosCommunication import Talker,Listener
from std_msgs.msg import String
from blackboard.msg import TaskMsg
from blackboard.msg import TaskCost
from blackboard.msg import bbBackup


class Blackboard:
    def __init__(self, state,talker): # constructor
        self.state = state
        self.talker = talker
        self.robotnr = 3
        if state is 1:
            self.bbList = []
            self.taskList = []
            self.buAdress = 'robot1'
            rospy.Subscriber('newTask',TaskMsg,self.addTask)
            rospy.Subscriber('taskCost',TaskCost,self.processTaskCost)
            self.bbBackuptimer = rospy.Timer(rospy.Duration(6),self.bbBackup)
            print('new blackboard object created')    
            
        
    def activateBlackboard(self,talker,buAdress):
        print('bb instance activated')
        self.state = 1
        self.bbList = []
        self.taskList = []
        self.bbAdress = talker.nodeName
        self.buAdress = buAdress
        rospy.Subscriber('newTask',TaskMsg,self.addTask)
        rospy.Subscriber('taskCost',TaskCost,self.processTaskCost)
        self.bbBackuptimer = rospy.Timer(rospy.Duration(6),self.bbBackup)
        print('publish timer activated')
        

    

    def addTask(self,data): #add a task to the list
        id = data.taskId
        for t in self.taskList:
            if t.taskId is id:
                break
        tsk = Task(data.taskId,data.priority,data.taskType,data.pose,data.payload)
        self.taskList.append(tsk)
        self.broadcastTask(tsk)

    def broadcastTask(self,task): # broadcast the task to online robots on a ros topic
        tmsg = TaskMsg()
        tmsg.taskId = task.taskId
        tmsg.priority = task.priority
        tmsg.taskType = task.taskType
        tmsg.payload = task.payload
        tmsg.taskState = task.taskState.value
        tmsg.pose = task.pose
        self.talker.pub_taskBC.publish(tmsg)
        
    

    

    def processTaskCost(self,data):
        for t in self.taskList:
            if t.taskId is data.taskId:
                if t.cost > data.taskCost:
                    t.robotId = data.robotId
                t.recivedCosts = t.recivedCosts+1
            if t.recivedCosts == self.robotnr:
                self.assignTask(t)
        

    def assignTask(self,task):
        if task.taskState is TaskState.Waitting:
            tmsg = TaskMsg()
            tmsg.robotId = task.robotId
            tmsg.taskId = task.taskId
            tmsg.priority = task.priority
            tmsg.taskType = task.taskType
            tmsg.payload = task.payload
            tmsg.taskState = task.taskState.value
            tmsg.pose = task.pose
            self.talker.pub_taskAssign.publish(tmsg)
            task.taskState = TaskState.Started

        


    def bbBackup(self,event=None):
        bumsg = bbBackup()
        bumsg.bbAdress = self.talker.nodeName
        bumsg.buAdress = self.buAdress #test
        self.talker.pub_bbBackup.publish(bumsg)


    def syncBlackboard(self, filepath, topicMessage): #update the database file with the current bb data
        #send blackboard updates
        pass

    def processMessage():
        #implement message process
        pass

    def registerRobot():
        #check the backup adress
        pass
        
        