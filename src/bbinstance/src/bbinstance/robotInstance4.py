#!/usr/bin/env python
#need to point to classes inorder to import
import rospy
from blackboard.Robot import Robot
from blackboard.RosCommunication import Talker
from rosnode import rosnode_ping
from blackboard.Blackboard import Blackboard
from blackboard.Battery import Battery

bat = Battery(100,500,100)

talker = Talker('robot4')
r = Robot('blackboard','robot1',4,4,4,4,5,10,10,bat,'robot4',talker)


rospy.spin()
