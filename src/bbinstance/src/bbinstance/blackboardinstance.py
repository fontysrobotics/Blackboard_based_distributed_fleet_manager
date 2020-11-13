#!/usr/bin/env python
#need to point to classes inorder to import
import rospy


from blackboard.msg import TaskMsg
from std_msgs.msg import String
from blackboard.RosCommunication import Talker

from blackboard.Blackboard import Blackboard

talker = Talker('blackboard')

bb = Blackboard(1,talker)




rospy.spin()