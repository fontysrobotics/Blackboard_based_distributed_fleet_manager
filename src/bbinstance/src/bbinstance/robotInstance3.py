#!/usr/bin/env python
#need to point to classes inorder to import
import rospy
from blackboard.Robot import Robot
from blackboard.RosCommunication import Talker
from rosnode import rosnode_ping
from blackboard.Blackboard import Blackboard


talker = Talker('robot3')
r = Robot('blackboard','robot1',3,3,3,3,5,10,10,3,'robot3',talker)


rospy.spin()
