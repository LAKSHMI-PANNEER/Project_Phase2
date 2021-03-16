#import libraries
import numpy as np
import time
#start_time = time.clock()
start = time.time()


#define the shape of the environment (states)
env_r = 9
env_col = 9

#Create a 3D numpy array to hold the current Q-values for each state and action pair: Q(s, a)
q_values = np.zeros((env_r, env_col, 4))

#define actions
#numeric action codes: 0 = up, 1 = right, 2 = down, 3 = left
actions = ['up', 'right', 'down', 'left']

#Create a 2D numpy array to hold the rewards for each state.
rewards = np.full((env_r, env_col), -1)

#shelter locations
for r_index in range(2,6):
  for col_index in range(6,9):
    rewards[r_index, col_index] = -100

#TASK : make a bridge = get wood, get iron, and use the factory

#propositions [GOALS]
#rewards[0,0]=100 #factory
#rewards[0,8]=100 #toolshed
#rewards[8,0]=100 #workbench
#rewards[0,2]=100 #iron
#rewards[8,4]=100 #iron
#rewards[6,8]=100 #wood
#rewards[2,3]=100 #wood
rewards[2,1]=100 #grass
#rewards[7,1]=100 #grass

#print rewards matrix
for r in rewards:
  print(r)

#define a function that determines if the specified location is a terminal state
def is_terminal_state(current_r_index, current_col_index):
  #if the reward for this location is -1, then it is not a terminal state
  if rewards[current_r_index, current_col_index] == -1:
    return False
  else:
    return True

#define a function that will choose a random, non-terminal starting location
def get_starting_location():
  #get a random r and col index
  current_r_index = np.random.randint(env_r)
  current_col_index = np.random.randint(env_col)
  #continue choosing random r and col indexes until a non-terminal state is identified
  while is_terminal_state(current_r_index, current_col_index):
    current_r_index = np.random.randint(env_r)
    current_col_index = np.random.randint(env_col)
  return current_r_index, current_col_index

#define an epsilon greedy algorithm that will choose which action to take next (where to move next)
def get_next_action(current_r_index, current_col_index, epsilon):
  #if a randomly chosen value between 0 and 1 is less than epsilon,
  #then choose the most promising value from the Q-table for this state.
  if np.random.random() < epsilon:
    return np.argmax(q_values[current_r_index, current_col_index])
  else: #choose a random action
    return np.random.randint(4)

#define a function that will get the next location based on the chosen action
def get_next_location(current_r_index, current_col_index, action_index):
  new_r_index = current_r_index
  new_col_index = current_col_index
  if actions[action_index] == 'up' and current_r_index > 0:
    new_r_index -= 1
  elif actions[action_index] == 'right' and current_col_index < env_col - 1:
    new_col_index += 1
  elif actions[action_index] == 'down' and current_r_index < env_r - 1:
    new_r_index += 1
  elif actions[action_index] == 'left' and current_col_index > 0:
    new_col_index -= 1
  return new_r_index, new_col_index

#Define a function that will get the shortest path between any location within the mine
#the agent is allowed to travel and reach the goal.
def get_shortest_path(start_r_index, start_col_index):
  #return immediately if this is an invalid starting location
  if is_terminal_state(start_r_index, start_col_index):
    return []
  else: #if this is a 'legal' starting location
    current_r_index, current_col_index = start_r_index, start_col_index
    shortest_path = []
    shortest_path.append([current_r_index, current_col_index])
    #continue moving along the path until we reach the goal
    while not is_terminal_state(current_r_index, current_col_index):
      #get the best action to take
      action_index = get_next_action(current_r_index, current_col_index, 1.)
      #move to the next location on the path, and add the new location to the list
      current_r_index, current_col_index = get_next_location(current_r_index, current_col_index, action_index)
      shortest_path.append([current_r_index, current_col_index])
    return shortest_path

#define training parameters
epsilon = 0.9 #the percentage of time when we should take the best action (instead of a random action)
discount_factor = 0.9 #discount factor for future rewards
learning_rate = 0.9 #the rate at which the AI agent should learn

#run through 1000 training episodes
for episode in range(1000):
  #get the starting location for this episode
  r_index, col_index = get_starting_location()

  #continue taking actions (moving) until we reach a terminal state
  while not is_terminal_state(r_index, col_index):
    #choose which action to take (where to move next)
    action_index = get_next_action(r_index, col_index, epsilon)

    #perform the chosen action, and transition to the next state (move to the next location)
    old_r_index, old_col_index = r_index, col_index #store the old r and col indexes
    r_index, col_index = get_next_location(r_index, col_index, action_index)

    #receive the reward for moving to the new state, and calculate the temporal difference
    reward = rewards[r_index, col_index]
    old_q_value = q_values[old_r_index, old_col_index, action_index]
    temporal_difference = reward + (discount_factor * np.max(q_values[r_index, col_index])) - old_q_value

    #update the Q-value for the previous state and action pair
    new_q_value = old_q_value + (learning_rate * temporal_difference)
    q_values[old_r_index, old_col_index, action_index] = new_q_value

print('Training complete!')

#display shortest paths
print("Shortest path to get grass",get_shortest_path(5,5))
#print("Shortest path to get iron",get_shortest_path(2,1))
#print("Shortest path to use factory",get_shortest_path(0,2))


#execution time
'''
print ("Execution time in seconds",time.process_time())
print(start,end)
print(end - start)
'''

end = time.time()
print("Execution time => %s seconds" % (end - start))

