# The falling objects challenge

Your goal is to try to avoid whatever is coming at you. Can you think of the optimal agent 
policy? 

Any overlap of the agent (blue box) with a falling object results in a reward of -1. There is only 
one obstacle on the map at any given moment and they fall with constant speed. The 
obstacles can have different shapes, sizes, rotations, speeds. Your agent has to be prepared for 
any kind of obstacle. 

You have to implement an agent, just like our demo agent from `demo_agent.py`. The agent will be 
tested using the script `test_agent.py` using different config files. We will evaluate the agent using new configs and obstacle shapes, so try to have a agent that is prepared. There must be a better solution than the random agent.

Good luck!

## Getting Started

You can play the game by running the `play_game.py` script. Use the keys `["W", "A", "S", "D"]`
keys to control the agent.

## Submission Format
Your agent must be implemented in python with a class similar to `DemoAgent`. The policy of the 
agent will be implemented in the method `act` and will only have access to the variables returned by the `env.step` method: `observation, reward, done_state` (a numpy array containing the game screen image/ a float number representing the reward / a boolean representing end of episode if True). 

**A python file with your agent class that can be run using our example (details below).**

## Running the tests

```
python test_agent.py -a <module_name>+<class_name>
```
Example:
```
python test_agent.py -a demo_agent+DemoAgent
```
