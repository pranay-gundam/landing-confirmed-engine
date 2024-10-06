import matplotlib.pyplot as plt
from game_objects import *


def test_creation_movement():
    lol1 = MoveableGameObject([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)])

    x, y = lol1.shape.exterior.xy
    plt.plot(x, y)

    plt.show()

if __name__ == "__main__":
    test_creation_movement()