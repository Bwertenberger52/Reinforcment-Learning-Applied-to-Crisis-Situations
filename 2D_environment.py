import numpy as np
import random
count =0
environment_matrix = np.array([[[None,0,-100,None],
								[None,0,0,0],
								[None,None,-100,0]],
								
								[[0,0,0,None],
								[0,-100,0,-100],
								[0,None,100,0]],
								
								[[-100,None,None,0],
								[0,100,None,0],
								[-100,0,None,None]]])
q_matrix = np.array([[[0,0,0,0],
					[0,0,0,0],
					[0,0,0,0]],
					
					[[0,0,0,0],
					[0,0,0,0],
					[0,0,0,0]],
					
					[[0,0,0,0],
					[0,0,0,0],[
					0,0,0,0]]])

win_loss_states = [[2,2],[0,1],[2,1]]

def getAllPossibleNextAction(cur_x,cur_y):
	action = []
	step_matrix = [x != None for x in environment_matrix[cur_pos]]
	if cur_y>0 and environment_matrix[cur_y,cur_x].ravel:
		action.append(0)    
	if cur_x<2 and environment_matrix[cur_y,cur_x].ravel:
		action.append(1)
	if cur_y<2 and environment_matrix[cur_y,cur_x].ravel:
		action.append(2)
	if cur_x>0 and environment_matrix[cur_y,cur_x].ravel:
		action.append(3)
	#else:
		#again([cur_x,cur_y],action)
		
	return(action)

def isGoalStateReached(cur_pos):
	return ([cur_x,cur_y] == [2,2])

def getNextState(cur_x, cur_y, action):
	if (action == 0):
		return [cur_x,cur_y - 1]
	elif (action == 1):
		return [cur_x + 1,cur_y]
	elif (action == 2):
		return [cur_x,cur_y + 1]
	elif (action == 3):
		return [cur_x - 1,cur_y]
		
def isGameOver(cur_x, cur_y):
	return [cur_x, cur_y] in win_loss_states
	
#def again(cur_pos, action):
	#getNextState(cur_pos[0], cur_pos[1], action)
	
discount = 0.9
learning_rate = 0.5
for _ in range(1000):
	# get starting place
	cur_pos = random.randrange(3),random.randrange(3)
	# while goal state is not reached
	while(not isGameOver(cur_pos[0],cur_pos[1])):
		# get all possible next states from cur_step
		possible_actions = getAllPossibleNextAction(cur_pos[0],cur_pos[1])
		# select any one action randomly
		action = random.choice(possible_actions)
		# find the next state corresponding to the action selected
		next_state = getNextState(cur_pos[0], cur_pos[1], action)
		# update the q_matrix
		if(environment_matrix[cur_pos[0],cur_pos[1]][action]):
			q_matrix[cur_pos[0],cur_pos[1]][action] = x=q_matrix[cur_pos[0],cur_pos[1]][action] + learning_rate * (environment_matrix[cur_pos[0],cur_pos[1]][action] + discount * max(q_matrix[next_state].ravel()) - q_matrix[cur_pos[0], cur_pos[1]][action])
			count+=1
		# go to next state
		cur_pos = next_state
		
	# print status
	print("Episode ", _ , " done")
print(q_matrix)
print("Training done...")
print(count)



	
