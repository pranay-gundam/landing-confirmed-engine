from enum import Enum
import numpy as np

class MoveAction(Enum): 
    UP = 0 
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    
def get_dir(action):
    match action:
        case MoveAction.UP:
            return 3 * np.pi / 2
        case MoveAction.DOWN:
            return np.pi / 2
        case MoveAction.LEFT:
            return np.pi
        case MoveAction.RIGHT:
            return 0
        case _:
            raise ValueError('Invalid MoveAction')