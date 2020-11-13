import rospy
from std_msgs.msg import String
from blackboard.msg import TaskMsg
from blackboard.msg import bbBackup
from blackboard.msg import TaskCost

class Talker(): #change to multy topic publisher
    def __init__(self,nodeName):
        self.nodeName = nodeName
        self.pub_newTask = rospy.Publisher('newTask', TaskMsg,queue_size=10)
        self.pub_robotState = rospy.Publisher('robotState', String,queue_size=10)
        self.pub_bbSync = rospy.Publisher('BbSync', String,queue_size=10)
        self.pub_taskBC = rospy.Publisher('taskBC', TaskMsg,queue_size=10)
        self.pub_bbBackup = rospy.Publisher('bbBackup', bbBackup,queue_size=10)
        self.pub_taskAssign = rospy.Publisher('taskAssign', TaskMsg,queue_size=10)
        self.pub_taskCost = rospy.Publisher('taskCost', TaskCost,queue_size=10)
        self.pub_taskAssign = rospy.Publisher('taskAssign', TaskMsg,queue_size=10)
        rospy.init_node(nodeName, anonymous=False)

        

class Listener: # change to multitopick listerner somehow
    def callback1(self,data):
        print(data)
        print(" recived111")

    def callback2(self,data):
        print(data)
        print(" recived222")


    def callback3(self,data):
        print(data)
        print(" recived333")

    def callback4(self,data):
        print(data)
        print(" recived444")

    def __init__(self,topic1,topic2,topic3,topic4,type1,type2,type3,type4):
        rospy.Subscriber(topic1,type1,self.callback1)
        rospy.Subscriber(topic2,type2,self.callback2)
        rospy.Subscriber(topic3,type3,self.callback3)
        rospy.Subscriber(topic4,type4,self.callback3)
#add rospyspin