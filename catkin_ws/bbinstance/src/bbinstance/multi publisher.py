#need to point to classes inorder to import
import time
import sys
import rospy
sys.path.append('../include/blackboard')

from std_msgs.msg import String

from Blackboard import Blackboard
from RosCommunication import Talker, Listener

bb = Blackboard(0,1,0)

bb.addTask(1)
bb.addTask(2)
bb.addTask(3)

for i in bb.taskList:
    print(i)




tlk = Talker('nodename','topic1','topic2','topic3')

tlk.pub1.publish('messsage 111111111111111111111')

tlk.pub2.publish('messsage 222222222222222222222')

tlk.pub3.publish('messsage 33332233333333333333')
