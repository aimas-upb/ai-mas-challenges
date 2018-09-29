from utils import read_cfg
from falling_objects_env import FallingObjects, PLAYER_KEYS
from argparse import ArgumentParser


if __name__ == "__main__":
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        '-c', '--config-file', default='configs/default.yaml', type=str,  dest='config_file',
        help='Default configuration file'
    )

    args = arg_parser.parse_args()
    config_file = args.config_file
    cfg = read_cfg(config_file)

    env = FallingObjects(cfg)

    episode_r = []
    env.reset()
    for _ in range(1000):
        key = env.render()
        if key == "q":
            exit()
        elif key not in PLAYER_KEYS.keys():
            print(f"Unknown key: {key}")
            continue

        obs, r, done, _ = env.step(PLAYER_KEYS[key])  # take a random action
        episode_r.append(r)
        print(f"Reward: {r} (rewards gathered in last 100 steps: {sum(episode_r[-100:])})")
