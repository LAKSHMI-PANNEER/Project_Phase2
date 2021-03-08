import numpy as np

env_rows = 9
env_cols = 9
q_values = np.zeros((env_rows, env_cols, 4))
actions = ['up', 'right', 'down', 'left']

rewards = np.full((env_rows, env_cols), -1)
#propositions
rewards[0,0]=100
rewards[0,8]=100
rewards[8,0]=100
rewards[0,2]=100
rewards[2,3]=100
rewards[2,1]=100
rewards[6,8]=100
rewards[7,1]=100
rewards[8,4]=100
#shelter locations
for r in range(2,6):
  for col in range(6,9):
    rewards[r, col] = 0

for row in rewards:
  print(row)

def is_terminal_state(current_r, current_col):
  if rewards[current_r, current_col] == -1:
    return False
  else:
    return True

def get_starting_location():
  current_r = np.random.randint(env_rows)
  current_col = np.random.randint(env_cols)
  while is_terminal_state(current_r, current_col):
    current_r = np.random.randint(env_rows)
    current_col = np.random.randint(env_cols)
  return current_r, current_col

def get_next_action(current_r, current_col, epsilon):
  if np.random.random() < epsilon:
    return np.argmax(q_values[current_r, current_col])
  else:
    return np.random.randint(4)

def get_next_location(current_r, current_col, action_index):
  new_r = current_r
  new_col = current_col
  if actions[action_index] == 'up' and current_r > 0:
    new_r -= 1
  elif actions[action_index] == 'right' and current_col < env_cols - 1:
    new_col += 1
  elif actions[action_index] == 'down' and current_r < env_rows - 1:
    new_r += 1
  elif actions[action_index] == 'left' and current_col > 0:
    new_col -= 1
  return new_r, new_col

def get_shortest_path(start_r, start_col):
  if is_terminal_state(start_r, start_col):
    return []
  else:
    current_r, current_col = start_r, start_col
    shortest_path = []
    shortest_path.append([current_r, current_col])
    while not is_terminal_state(current_r, current_col):
      action_index = get_next_action(current_r, current_col, 1.)
      current_r, current_col = get_next_location(current_r, current_col, action_index)
      shortest_path.append([current_r, current_col])
    return shortest_path

epsilon = 0.9
discount_factor = 0.9
learning_rate = 0.9

for episode in range(1000):
  r, col = get_starting_location()

  while not is_terminal_state(r, col):
    action_index = get_next_action(r, col, epsilon)
    old_r, old_col = r, col
    r, col = get_next_location(r, col, action_index)
    reward = rewards[r, col]
    old_q_value = q_values[old_r, old_col, action_index]
    temporal_difference = reward + (discount_factor * np.max(q_values[r, col])) - old_q_value
    new_q_value = old_q_value + (learning_rate * temporal_difference)
    q_values[old_r, old_col, action_index] = new_q_value

print('Training complete!')

print(get_shortest_path(0, 5))
