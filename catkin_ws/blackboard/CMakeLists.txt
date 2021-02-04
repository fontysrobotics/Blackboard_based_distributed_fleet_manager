cmake_minimum_required(VERSION 3.0.2)
project(blackboard)


find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  geometry_msgs
  message_generation
)


 catkin_python_setup()



## Generate messages in the 'msg' folder
 add_message_files(
   FILES
   TaskMsg.msg
   TaskCost.msg
   bbBackup.msg
   bbsynch.msg
   TaskStateMsg.msg

 )


## Generate added messages and services with any dependencies listed here
 generate_messages(
   DEPENDENCIES
   std_msgs
   geometry_msgs
 )




catkin_package(

#  LIBRARIES blackboard
  CATKIN_DEPENDS roscpp rospy std_msgs message_runtime
#  DEPENDS system_lib
)


include_directories(
 include
  ${catkin_INCLUDE_DIRS}
)


