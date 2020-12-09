#!/usr/bin/env python
#need to point to classes inorder to import
import rospy
from blackboard.Robot import Robot
from blackboard.RosCommunication import Talker
from rosnode import rosnode_ping
from blackboard.Blackboard import Blackboard
from blackboard.Battery import Battery

bat = Battery(100,1000,100)
talker = Talker('robot1')
r = Robot('blackboard','robot1',1,1,1,1,5,10,10,bat,'robot1',talker)


    
rospy.spin()