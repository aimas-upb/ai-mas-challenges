import numpy as np


class DemoAgent:
    def __init__(self, max_action: int):
        self.max_action = max_action

    def act(self, observation: np.ndarray):
        """
        :param observation: numpy array of shape (width, height, 3) *defined in config file
        :return: int between 0 and max_action
        """
        return np.random.randint(self.max_action)
