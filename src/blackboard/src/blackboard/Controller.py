#!/usr/bin/env python

#---------------------------------------------------------------- 
# Blackboard distributed fleet manager - Fontys lectoraat
# Sep 2020 - Feb 2021 internship Eindhoven BIC
# Hussam Ayoub, 356203@student.fontys.nl

#----------------------------Description------------------------- 
# The controller is responsable for executing tasks for robots
# it contains an instance of ROS movebaseaction and goal to
# execute navigation tasks, for future development this class
# should contain an instance of ROS moveit to execute manipulator
# tasks, which are dropped for the current project for simulation
# limitations
#----------------------------------------------------------------


from blackboard.RosCommunication import Talker
import rospy
import actionlib
from blackboard.Task import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from threading import Thread

# movebase command class start
class MoveBaseCommand:
    def __init__(self, robotid):                                # pass robot id to use in movebase topic name
        self.robotid = robotid
        moveBaseTopic = robotid+"/move_base"     # set movebase topic "RULE: /Robotx/move_base" x is robot id
        self.client = actionlib.SimpleActionClient(
            moveBaseTopic, MoveBaseAction)                      # movebase action clinet
        self.client.wait_for_server()                           # connect to movebase server
        self.state = 0                                          # holds movebase object state

        
    # send a goal to movebase action server
    def sendGoal(self, goal):
        movebasegoal = MoveBaseGoal()                                  # instance of movebase goal
        movebasegoal.target_pose.header.frame_id = "map"               # with respect to global frame " map "
        movebasegoal.target_pose.header.stamp = rospy.Time.now()       # time stamp, moment of sending the goal
        movebasegoal.target_pose.pose.position.x = goal.position.x     # goal position x, passed goal
        movebasegoal.target_pose.pose.position.y = goal.position.y     # goal position y, passed goal
        movebasegoal.target_pose.pose.orientation.w = 1.0              
        self.client.send_goal(movebasegoal)                            # send the goal instance

# class controller start
class Controller:
    def __init__(self, robotid):
        self.stepcounter = 0                                # holds the number of steps to execute
        self.robotid = robotid                              # used to be passed to movebase command object
        self.mb = MoveBaseCommand(robotid)                  # init movebase command object
        self.state = 0                                      # controller state idle


    # starts a new thread to execute a task "movebase has blocking functions"
    def startExecute(self, task):
        a = Thread(target=self.executeTask, args=(task,))   # create the new thread and starts it
        a.start()

    # called through startExecute function as a thread
    def executeTask(self, task):
        self.state = -1                                     # set state to busy
        self.stepcounter = 0                                # reset step counter
        task.analyzeTask()                                  # analyze the task
        
        for step in task.stepsList:                         # send each stgep in task.stepsList as a goal
            self.mb.sendGoal(step.pose)
            wait = self.mb.client.wait_for_result()         # wait for result
            if wait:
                self.stepcounter = self.stepcounter + 1     # if done start next increase executed steps counter

        if self.stepcounter == len(task.stepsList):         # if executed steps = number of steps to be executed     
            task.taskState = TaskState.Done                 # set task state to done
            self.state = 1                                  # set controller state to done
      
