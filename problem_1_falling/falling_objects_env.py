# AI-MAS @ 2018

import cv2
import numpy as np
from argparse import Namespace
import typing
from typing import List, Any, Tuple

Obstacle = typing.NamedTuple("Obstacle", [('shape', np.ndarray),
                                          ('min_scale', float), ('max_scale', float),
                                          ('max_rotation', float)])
DEFAULT_MAP_SIZE = [86, 86]

ACTIONS = dict({
    0: np.array([-1, 0], dtype=int),
    1: np.array([+1, 0], dtype=int),
    2: np.array([0, +1], dtype=int),
    3: np.array([0, -1], dtype=int)
})

PLAYER_KEYS = dict({
    "w": 0,
    "s": 1,
    "d": 2,
    "a": 3,
})

VIEW_SIZE = 512


def rotate_image(img: np.ndarray, angle: float) -> np.ndarray:
    """
    :param img: numpy image
    :param angle: Rotation angle in degrees, Positive values mean counter-clockwise rotation.
    :return: rotated image
    """
    center = tuple(np.array(img.shape[0:2]) / 2)
    rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(img, rot_mat, img.shape[0:2], flags=cv2.INTER_LINEAR)


def load_shape(image_path: str, max_size: int = 0) -> np.ndarray:
    """
    Image will be resized to width size if different tha 0 and empty border cropped
    :param image_path: path to object shape image
    :param width:
    """
    img = cv2.imread(image_path)

    # Trim white spaces
    not_img = img.sum(axis=2)
    rows_fill = not_img.sum(axis=1) == 0
    cols_fill = not_img.sum(axis=0) == 0
    min_r = rows_fill.argmin()
    max_r = rows_fill.shape[0] - rows_fill[::-1].argmin()
    min_c = cols_fill.argmin()
    max_c = cols_fill.shape[0] - cols_fill[::-1].argmin()
    img = img[min_r: max_r, min_c: max_c]

    if max_size != 0:
        max_shape = max(img.shape)
        scale = max_size/ float(max_shape)
        img = cv2.resize(img, (0, 0), fx=scale, fy=scale)
    return img


def image_add_object(img: np.ndarray, obj: np.ndarray, pos_x: int, pos_y: int) -> np.ndarray:
    """
    Overlay object image to background image
    :param img: background image
    :param obj: object image
    :param pos_x
    :param pos_y: pos to add object
    :return: new image
    """
    obj_size = obj.shape
    img_zone = img[pos_x: pos_x + obj_size[0], pos_y: pos_y + obj_size[1]]
    img_zone = cv2.addWeighted(img_zone, 0., obj, 1., 0)
    img[pos_x: pos_x + obj_size[0], pos_y: pos_y + obj_size[1]] = img_zone
    return img


class MapObject:
    def __init__(self, shape: np.ndarray, speed: int,
                 limits_x: Tuple[int, int], limits_y: Tuple[int, int],
                 default_pos: Tuple[int, int] = None):
        self.shape = shape
        self.speed = speed
        self.limits_x = np.array(limits_x, dtype=int)
        self.limits_y = np.array(limits_y, dtype=int)
        self.action_move = dict({
            x: y * speed for x, y in ACTIONS.items()
        })
        if default_pos is None:
            self.default_pos = list([0, 0])
        else:
            self.default_pos = np.array(default_pos, dtype=int)

        shape_size = self.shape.shape
        self.limits_x[1] = self.limits_x[1] - shape_size[0]
        self.limits_y[1] = self.limits_y[1] - shape_size[1]

        self.pos = np.array([0, 0], dtype=int)

    def step(self, action: int) -> np.ndarray:
        action_move = self.action_move
        limits_x = self.limits_x
        limits_y = self.limits_y
        new_pos = self.pos + action_move[action]
        self.pos[0] = np.clip(new_pos[0], limits_x[0], limits_x[1])
        self.pos[1] = np.clip(new_pos[1], limits_y[0], limits_y[1])
        return self.pos

    def reset(self):
        self.pos = self.default_pos.copy()


class FallingObjects:
    metadata = {'render.modes': ['human']}

    def __init__(self, config: Namespace):
        self.map_size = map_size = DEFAULT_MAP_SIZE
        obstacles_config = config.obstacles # type: List[Any]
        self.bckg_color = np.array(config.background, np.uint8)
        self.agent_size = agent_size = config.agent_size # type: int # Size in pixels
        self.agent_color = np.array(config.agent_color, np.uint8)
        self.map_padding = self.map_size
        self.obstacles_speed = config.obstacles_speed

        # Init agent
        agent_shape = self.generate_agent_shape()
        agent_pos = [map_size[1] - agent_size, map_size[0]//2 - agent_size//2]
        self.agent = MapObject(agent_shape, 1, (0, map_size[1]), (0, map_size[0]), agent_pos)

        self.agent_pos = np.array([0, 0])

        # Init map
        self.default_map = self.generate_map()

        # Init object images
        self.obstacles: List[Obstacle] = list([])
        for obstacle_cfg in obstacles_config:
            shape = load_shape(obstacle_cfg[0], max_size=map_size[0])
            obstacle = Obstacle(*([shape] + obstacle_cfg[1:]))
            self.obstacles.append(obstacle)

        self.crt_obstacles: List[MapObject] = list([])

        self.last_obs = np.zeros(map_size + [3], dtype=np.uint8)

    def generate_agent_shape(self) -> np.ndarray:
        agent_size = self.agent_size
        agent_color = self.agent_color

        shape = np.zeros([agent_size, agent_size, 3], dtype=np.uint8)
        shape[:, :] = agent_color
        return shape

    def generate_map(self) -> np.ndarray:
        map_size = self.map_size
        bckg_color = self.bckg_color
        map_padding = self.map_padding
        map_background = np.zeros([map_size[0] + map_padding[0]*2,
                                   map_size[1] + map_padding[1]*2, 3],
                                  dtype=np.uint8)
        map_background[:, :] = bckg_color
        return map_background

    def get_obs(self):
        default_map = self.default_map
        map_p_x, map_p_y = self.map_padding
        a_pos = self.agent.pos
        agent_shape = self.agent.shape
        agent_size_x, agent_size_y = agent_shape.shape[:2]
        obj_map = np.zeros_like(default_map)
        crt_obstacles = self.crt_obstacles

        # Add objects to map
        if len(crt_obstacles) <= 0:
            self.new_object_on_map()

        for crt_obstacle in crt_obstacles:
            obs_shape = crt_obstacle.shape
            obs_x, obs_y = crt_obstacle.pos
            obj_map = image_add_object(obj_map, obs_shape, obs_x+map_p_x, obs_y+map_p_y)

        # Check agent hit
        true_map = obj_map[map_p_x:-map_p_x, map_p_y:-map_p_y]
        hit = true_map[a_pos[0]:a_pos[0]+agent_size_x, a_pos[1]:a_pos[1]+agent_size_y].sum() > 0

        # Add agent to map
        new_map = image_add_object(obj_map, agent_shape, a_pos[0]+map_p_x, a_pos[1]+map_p_y)

        new_map = cv2.addWeighted(default_map, 0., new_map, 1., 0)

        # Crop padding
        true_map = new_map[map_p_x:-map_p_x, map_p_y:-map_p_y]

        self.obstacles_step()
        return true_map, hit

    def obstacles_step(self):
        new_obs = []
        for idx, obj in enumerate(self.crt_obstacles):
            obj.step(1)
            if obj.pos[0] < self.map_size[0]:
                new_obs.append(obj)

        self.crt_obstacles = new_obs

    def new_object_on_map(self):
        obstacles = self.obstacles
        map_size_x, map_size_y = self.map_size
        obstacles_speed = self.obstacles_speed

        obj_idx = np.random.randint(len(obstacles))
        cfg = obstacles[obj_idx]
        obstacle_shape = cfg.shape
        scale = np.random.uniform(low=cfg.min_scale, high=cfg.max_scale, size=(1,))[0]

        obstacle_shape = cv2.resize(obstacle_shape, (0, 0), fx=scale, fy=scale)
        if cfg.max_rotation != 0:
            raise NotImplemented
            # max_r, min_r = cfg.max_rotation, -cfg.max_rotation
            # r_angle = np.random.uniform(low=-min_r, high=max_r, size=(1,))[0]
            # obstacle_shape = rotate_image(obstacle_shape, 0)

        size_x, size_y = obstacle_shape.shape[:2]
        x_pos = -size_x
        y_pos = np.random.randint(0, map_size_y-size_y)

        new_obstacle = MapObject(obstacle_shape, obstacles_speed,
                                 (-size_x, map_size_x+size_x),
                                 (-size_y, map_size_y + size_y), (x_pos, y_pos))
        new_obstacle.reset()
        self.crt_obstacles.append(new_obstacle)

    def step(self, action: int):
        self.agent.step(action)
        obs, hit = self.get_obs()
        self.last_obs = obs
        reward = -int(hit)
        done = False

        return obs, reward, done, dict({})

    def reset(self):
        self.agent.reset()
        obs, hit = self.get_obs()
        return obs

    def render(self, mode='human', close=False, block=True):
        last_obs = self.last_obs
        view_img = last_obs
        view_img = cv2.resize(view_img, (VIEW_SIZE, VIEW_SIZE))
        cv2.imshow("Falling obj", view_img)
        key = None
        if block:
            key = cv2.waitKey(0) % 256
            key = chr(key)
        else:
            cv2.waitKey(1)

        return key


if __name__ == "__main__":
    cfg = Namespace()
    # White borders from object image will be cropped
    # [ [path to obj image, min_scale, max_scale, max_rotation] ...]
    cfg.obstacles = [
        ["objects_examples/obstacle_1.png", 0.2, 0.5, 0]
    ]
    cfg.background = [0, 0, 0]
    cfg.agent_size = 5
    cfg.agent_color = [255, 0, 0]

    env = FallingObjects(cfg)

    env.reset()
    for _ in range(1000):
        key = env.render()
        obs, r, done, _ = env.step(PLAYER_KEYS[key])  # take a random action
        print(f"Reward: {r}")