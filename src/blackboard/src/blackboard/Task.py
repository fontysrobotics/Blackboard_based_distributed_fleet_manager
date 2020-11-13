from enum import Enum
from geometry_msgs.msg import Pose
import time


class TaskType(Enum):
    GA = 1 # go to position a
    GAB = 2  # go to position a then b
    GPA = 3  # go to position a and pick object
    GPAB = 4  # go to position a pick then go to pose b


class TaskState(Enum):
    Waitting = 0
    Started = 1
    Done = 3


class Task:

    stepsList = []  # a list to hold task steps when a task is analyzed

    # initilize a task object with the known parameters
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
        self.taskState = TaskState.Waitting
        self.cost = 10
        self.robotId = -1
        self.recivedCosts = 0

    def updateState(self, taskState #type: TaskState
                    ):  # set the current task state
        self.taskState = taskState



class TaskStep:
    def __init__(self, stepType, pose):  # a straigh forward implementation of a constructor
        self.stepType = stepType
        self.pose = pose


class StepType(Enum):
    go = 0
    pick = 1
