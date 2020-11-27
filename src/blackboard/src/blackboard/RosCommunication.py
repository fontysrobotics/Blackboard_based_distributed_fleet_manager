#---------------------------------------------------------------- 
# Blackboard distributed fleet manager - Fontys lectoraat
# Sep 2020 - Feb 2021 internship Eindhoven BIC
# Hussam Ayoub, 356203@student.fontys.nl

#----------------------------Description------------------------- 
# 
# The Talker class is responsable for initilizing a ROS
# Node and its publishers on specified topics.
#----------------------------------------------------------------


import rospy
from std_msgs.msg import String             # Custom built ROS messages
from blackboard.msg import TaskMsg          #
from blackboard.msg import bbBackup         #
from blackboard.msg import TaskCost         #
from blackboard.msg import bbsynch          #
from blackboard.msg import TaskStateMsg     #



class Talker():
    # class constructor with node name variable
    def __init__(self,nodeName):
        # assign passed node name
        self.nodeName = nodeName
        # init publishers:
        self.pub_newTask = rospy.Publisher('newTask', TaskMsg,queue_size=1)                 # new task publisher
        self.pub_robotState = rospy.Publisher('robotState', String,queue_size=1)            # robot state to simulate defect
        self.pub_bbSync = rospy.Publisher('BbSync', bbsynch,queue_size=1)                   # syncronize blackboard task list
        self.pub_taskBC = rospy.Publisher('taskBC', TaskMsg,queue_size=1)                   # broadcast a task over topic
        self.pub_bbBackup = rospy.Publisher('bbBackup', bbBackup,queue_size=1)              # blackboard and backup adresses
        self.pub_taskAssign = rospy.Publisher('taskAssign', TaskMsg,queue_size=1)           # assign a task to robot
        self.pub_taskCost = rospy.Publisher('taskCost', TaskCost,queue_size=1)              # send task cost from robots
        self.pub_taskState = rospy.Publisher('TaskStateMsg', TaskStateMsg,queue_size=1)     # update task state in blackboare
        rospy.init_node(nodeName, anonymous=False)                                          # initilize ROS node

        

