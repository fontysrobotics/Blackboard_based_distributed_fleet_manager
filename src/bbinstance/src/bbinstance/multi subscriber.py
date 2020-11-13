#need to point to classes inorder to import
import time
import sys
import rospy
sys.path.append('../include/blackboard')

from std_msgs.msg import String
from RosCommunication import Talker, Listener


lis = Listener('topic1','topic2','topic3','listener')
