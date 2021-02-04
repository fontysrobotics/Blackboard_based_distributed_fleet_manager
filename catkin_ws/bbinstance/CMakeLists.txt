cmake_minimum_required(VERSION 3.0.2)
project(bbinstance)


find_package(catkin REQUIRED COMPONENTS
  blackboard
  rospy
  

)

find_package(python_qt_binding REQUIRED COMPONENTS
  QtWidgets
  QtCore
  QtGui

)


 catkin_python_setup()


catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES bbinstance
#  CATKIN_DEPENDS blackboard rospy
#  DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

