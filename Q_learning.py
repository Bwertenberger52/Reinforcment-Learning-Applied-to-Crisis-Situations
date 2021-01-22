import numpy as np
import random

epsilon = 0.2
state_size = 5
action_size = 5

Q = np.zeros((state_size, action_size))

if random.uniform(0, 1) < epsilon:
	pass
	#~Exlore: Select Random
	
else:
	pass
	#~Exploit: Select max value
	
#Q[state, action] = Q[state, action] + lr * (reward + gamma * np.max(Q[new_state, :]) - Q[state, action])

a = [1,1]
b = [1,1]
c = [1,2]
print(a==b)
print(a==c)
