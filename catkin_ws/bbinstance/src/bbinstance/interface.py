#!/usr/bin/env python
#need to point to classes inorder to import
import rospy
#sys.path.append('../include/blackboard')

from blackboard.msg import TaskMsg
from std_msgs.msg import String
from std_msgs.msg import Float32

from blackboard.Blackboard import Blackboard
from blackboard.RosCommunication import Talker, Listener
from blackboard.Task import Task,TaskType,TaskStep,TaskState
from geometry_msgs.msg import Pose
from blackboard.Robot import RobotState
from blackboard.msg import TaskCost


# pub = rospy.Publisher('task', TaskMsg,queue_size=10)
# rospy.init_node('nnode', anonymous=True)
# rate = rospy.Rate(10) # 10hz

talk = Talker('interface')
tskType = TaskType.GA
pose = Pose()
posearray = []
tskmsg = TaskMsg()
payload = 0



# for x in range(1,10):
#     task =Task(x,10,TaskType.GA,posearray,2)
#     tskmsg.taskId = task.taskId
#     tskmsg.priority = task.priority
#     tskmsg.taskType = task.taskType.value
#     tskmsg.payload = task.payload
#     tskmsg.taskState = task.taskState.value
#     tskmsg.pose = task.pose
#     talk.pub_newTask.publish(tskmsg)





choice = raw_input("press 1 to add a new task\npress 2 to change a robot state")



if choice is '1':
    taskId = input("enter task Id\n")
    priority = input("enter task priority\n")
    taskType = input("enter task type\n1.GA\n2.GAB\n3.GPA\n4.GPAB")
   
    if taskType is 1:
        pose.position.x = input("enter pose.X:")
        pose.position.y = input("enter pose.Y: ")
        pose.position.z = input("enter pose.Z: ")
        pose.orientation.w = input("enter Orientation.w: ")
        posearray.append(pose)
        
        

    if taskType is 2:
        pose.position.x = input("enter pose.X:")
        pose.position.y = input("enter pose.Y: ")
        pose.position.z = input("enter pose.Z: ")
        pose.orientation.w = input("enter Orientation.w: ")
        posearray.append(pose)

        pose.position.x = input("enter pose.X2:")
        pose.position.y = input("enter pose.Y2: ")
        pose.position.z = input("enter pose.Z2: ")
        pose.orientation.w = input("enter Orientation.w2: ")
        posearray.append(pose)
        tskType = TaskType.GAB

    if taskType is 3:
        pose.position.x = input("enter pose.X:")
        pose.position.y = input("enter pose.Y: ")
        pose.position.z = input("enter pose.Z: ")
        pose.orientation.w = input("enter Orientation.w: ")
        posearray.append(pose)

        pose.position.x = input("enter pose.X2:")
        pose.position.y = input("enter pose.Y2: ")
        pose.position.z = input("enter pose.Z2: ")
        pose.orientation.w = input("enter Orientation.w2: ")
        posearray.append(pose)
        tskType = TaskType.GPA

    if taskType is 4:
        pose.position.x = input("enter pose.X:")
        pose.position.y = input("enter pose.Y: ")
        pose.position.z = input("enter pose.Z: ")
        pose.orientation.w = input("enter Orientation.w: ")
        posearray.append(pose)

        pose.position.x = input("enter pose.X2:")
        pose.position.y = input("enter pose.Y2: ")
        pose.position.z = input("enter pose.Z2: ")
        pose.orientation.w = input("enter Orientation.w2: ")
        posearray.append(pose)

        pose.position.x = input("enter pose.X3:")
        pose.position.y = input("enter pose.Y3: ")
        pose.position.z = input("enter pose.Z3: ")
        pose.orientation.w = input("enter Orientation.w3: ")
        posearray.append(pose)
        tskType = TaskType.GPAB

    payload = input("enter Payload: ")

    task = Task(taskId,priority,tskType,posearray,payload)

    tskmsg.taskId = task.taskId
    tskmsg.priority = task.priority
    tskmsg.taskType = task.taskType.value
    tskmsg.payload = task.payload
    tskmsg.taskState = task.taskState.value
    tskmsg.pose = task.pose


    talk.pub_newTask.publish(tskmsg)


if choice is '2':
    rstate = raw_input("Select robot state:\n1.Busy\n2.Defect\n3.Idle ")
    robotID = raw_input("enter robot ID:")
    pu = rstate+','+robotID
    talk.pub2.publish(pu)

