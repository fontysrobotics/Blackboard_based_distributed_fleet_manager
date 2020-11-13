#!/usr/bin/env python
#need to point to classes inorder to import
import rospy
from blackboard.Robot import Robot
from blackboard.RosCommunication import Talker
from rosnode import rosnode_ping
from blackboard.Blackboard import Blackboard


talker = Talker('robot2')
r = Robot('blackboard','robot1',2,2,2,2,5,10,10,2,'robot2',talker)


rospy.spin()
