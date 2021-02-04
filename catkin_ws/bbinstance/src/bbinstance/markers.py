#!/usr/bin/env python

# Copyright (c) 2015, Carnegie Mellon University
# All rights reserved.
# Authors: David Butterworth <dbworth@cmu.edu>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# - Neither the name of Carnegie Mellon University nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""
This is a demo of Rviz Tools for python which tests all of the
available functions by publishing lots of Markers in Rviz.
"""

# Python includes
import numpy
import random

# ROS includes
import roslib
import rospy
from geometry_msgs.msg import Pose, Point, Quaternion, Vector3, Polygon
from tf import transformations # rotation_matrix(), concatenate_matrices()

import rviz_tools_py as rviz_tools


# Initialize the ROS Node
rospy.init_node('test', anonymous=False, log_level=rospy.INFO, disable_signals=False)

# Define exit handler
def cleanup_node():
    print "Shutting down node"
    markers.deleteAllMarkers()

rospy.on_shutdown(cleanup_node)


markers = rviz_tools.RvizMarkers('/map', 'visualization_marker')


while not rospy.is_shutdown():

    # Axis:


    T = transformations.translation_matrix((1,-2,0))
    scale = Vector3(1.0,0.2,0.2) # x=length, y=height, z=height
    markers.publishArrow(T, 'blue', scale, 5.0) # pose, color, scale, lifetime


    P = Pose(Point(0,0,1),Quaternion(1,0,-1,0))
    arrow_length = 2.0 # single value for length (height is relative)
    markers.publishArrow(P, 'pink', arrow_length, 5.0) # pose, color, arrow_length, lifetime


    rospy.Rate(1).sleep() #1 Hz