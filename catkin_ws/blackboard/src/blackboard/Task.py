#---------------------------------------------------------------- 
# Blackboard distributed fleet manager - Fontys lectoraat
# Sep 2020 - Feb 2021 internship Eindhoven BIC
# Hussam Ayoub, 356203@student.fontys.nl

#----------------------------Description------------------------- 
# The Task class stores task values and runs a task analyze 
# function
#----------------------------------------------------------------


from enum import Enum
from geometry_msgs.msg import Pose
import time

# task types enum
class TaskType(Enum):
    GA = 1                  # go to position a
    GAB = 2                 # go to position a then b
    GPA = 3                 # go to position a and pick object
    GPAB = 4                # go to position a pick then go to pose b


# task state enums
class TaskState(Enum):
    Waitting = 0
    Started = 1
    Done = 2
    Assigned = 3


# start task class
class Task:
    # initilize a task object with the passed parameters
    def __init__(self,taskID,
                 priority,
                 taskType, #type: TaskType
                 pose,  #type: List[Pose]
                 payload):

        self.taskId=taskID
        self.priority = priority
        self.taskType = taskType
        self.pose = pose
        self.payload = payload
        self.taskState = TaskState.Waitting     # when task is created its in waitting state
        self.cost = 1000                        # cost is set to max to be adjusted when calculated later
        self.energyCost = 0                     # amps used to execute task, added to simulate battery usage
        self.robotId = -1                       # task is not assigned " robot id -1 does not exist "
        self.recivedCosts = 0                   # number of recived costs from robots 
        self.stepsList = []                     # a list to hold task steps when a task is analyzed

    # set the task state to one of defined enums
    def updateState(self, taskState #type: TaskState
                    ):  # set the current task state
        self.taskState = taskState

    # analyze the task based on task type and create task steps the append to stepsList
    def analyzeTask(self):
        self.stepsList = []                                 # clear steps list

        if self.taskType is TaskType.GA.value:                    # if type is GA
            tskstp = TaskStep(StepType.go,self.pose[0])     # create a new task step with type go and position 0
            self.stepsList.append(tskstp)                   # append to stepsList
                
        if self.taskType is TaskType.GAB.value:             # if type is GAB
            tskstp = TaskStep(StepType.go,self.pose[0])     # create a new task step with type go and position 0
            self.stepsList.append(tskstp)                   # append to stepsList
            tskstp = TaskStep(StepType.go,self.pose[1])     # create a new task step with type go and position 1
            self.stepsList.append(tskstp)                   # append to stepsList

        if self.taskType is TaskType.GPA.value:             # if type is GPA
            tskstp = TaskStep(StepType.go,self.pose[0])     # create a new task step with type go and position 0
            self.stepsList.append(tskstp)                   # append to stepsList
            tskstp = TaskStep(StepType.pick,self.pose[1])   # create a new task step with type pick and position 1
            self.stepsList.append(tskstp)                   # append to stepsList

        if self.taskType is TaskType.GPAB.value:            # if type is GPAB       
            tskstp = TaskStep(StepType.go,self.pose[0])     # create a new task step with type go and position 0
            self.stepsList.append(tskstp)                   # append to stepsList
            tskstp = TaskStep(StepType.pick,self.pose[1])   # create a new task step with type pick and position 1
            self.stepsList.append(tskstp)                   # append to stepsList
            tskstp = TaskStep(StepType.go,self.pose[2])     # create a new task step with type go and position 2
            self.stepsList.append(tskstp)                   # append to stepsList

        
# task step object has a step type of go , pick and a pose to hold postion and orientation
class TaskStep:
    def __init__(self, stepType, pose):
        self.stepType = stepType        
        self.pose = pose

# step type enum
class StepType(Enum):
    go = 0
    pick = 1
