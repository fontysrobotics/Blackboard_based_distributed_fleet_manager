#!/usr/bin/env python
#need to point to classes inorder to import
import rospy
#sys.path.append('../include/blackboard')

from blackboard.msg import TaskMsg
from std_msgs.msg import String

from Blackboard import Blackboard
from RosCommunication import Talker, Listener
from Task import Task,TaskType,TaskStep,TaskState
from geometry_msgs.msg import Pose


# pub = rospy.Publisher('task', TaskMsg,queue_size=10)
# rospy.init_node('nnode', anonymous=True)
# rate = rospy.Rate(10) # 10hz

bb = Blackboard(1,1,1)


pose = Pose()
pose.position.x = 1
pose.position.y = 2
pose.position.z = 3

posearray = []
posearray.append(pose)

task = Task(1,TaskType.GA,posearray,10)
tskmsg = TaskMsg()






tskmsg.priority = int(task.priority)
tskmsg.taskType = 1
tskmsg.payload = int(task.payload)
tskmsg.taskState = 1
tskmsg.cost = 10
tskmsg.pose = task.pose

bb.talker.pub2.publish(tskmsg)




