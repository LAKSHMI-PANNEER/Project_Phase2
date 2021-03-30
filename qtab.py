import numpy as np
import time
start = time.time()

env_r = 9
env_col = 9

q_values = np.zeros((env_r, env_col, 4))
actions = ['up', 'right', 'down', 'left']
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

for r in rewards:
  print(r)

def is_terminal_state(current_r_index, current_col_index):
  if rewards[current_r_index, current_col_index] == -1:
    return False
  else:
    return True

def get_starting_location():
  current_r_index = np.random.randint(env_r)
  current_col_index = np.random.randint(env_col)
  while is_terminal_state(current_r_index, current_col_index):
    current_r_index = np.random.randint(env_r)
    current_col_index = np.random.randint(env_col)
  return current_r_index, current_col_index

def get_next_action(current_r_index, current_col_index, epsilon):
  if np.random.random() < epsilon:
    return np.argmax(q_values[current_r_index, current_col_index])
  else: 
    return np.random.randint(4)

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

def get_shortest_path(start_r_index, start_col_index):
  if is_terminal_state(start_r_index, start_col_index):
    return []
  else: 
    current_r_index, current_col_index = start_r_index, start_col_index
    shortest_path = []
    shortest_path.append([current_r_index, current_col_index])
    while not is_terminal_state(current_r_index, current_col_index):
      action_index = get_next_action(current_r_index, current_col_index, 1)
      current_r_index, current_col_index = get_next_location(current_r_index, current_col_index, action_index)
      shortest_path.append([current_r_index, current_col_index])
    return shortest_path

epsilon = 0.9 
discount_factor = 0.9
learning_rate = 0.9 

for episode in range(1000):
  r_index, col_index = get_starting_location()
  while not is_terminal_state(r_index, col_index):
    action_index = get_next_action(r_index, col_index, epsilon)

    old_r_index, old_col_index = r_index, col_index 
    r_index, col_index = get_next_location(r_index, col_index, action_index)

    reward = rewards[r_index, col_index]
    old_q_value = q_values[old_r_index, old_col_index, action_index]
    temporal_difference = reward + (discount_factor * np.max(q_values[r_index, col_index])) - old_q_value

    new_q_value = old_q_value + (learning_rate * temporal_difference)
    q_values[old_r_index, old_col_index, action_index] = new_q_value

print('Training complete!')
r,c = input("Enter a starting location for the Agent: ").split()

print("Shortest path to get grass: ",get_shortest_path(int(r),int(c)))
#print("Length of the path: ",len(get_shortest_path(int(r),int(c))))

end = time.time()
print("Execution time => %s seconds" %(end - start))

