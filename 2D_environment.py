import numpy as np
import random
count =0
environment_matrix = np.array([[[None,0,0,None],
								[None,-100,0,0],
								[None,None,0,0]],
								
								[[0,-100,0,None],
								[0,0,0,0],
								[0,None,100,-100]],
								
								[[0,0,None,None],
								[-100,100,None,0],
								[0,None,None,0]]])
q_matrix = np.array([[[0,0,0,0],
					[0,0,0,0],
					[0,0,0,0]],
					
					[[0,0,0,0],
					[0,0,0,0],
					[0,0,0,0]],
					
					[[0,0,0,0],
					[0,0,0,0],[
					0,0,0,0]]])

win_loss_states = [[2,2]]

def getAllPossibleNextAction(cur_x,cur_y):
	action = []
	if cur_y>0 and type(environment_matrix[cur_y][cur_x][0])==type(1):
		action.append(0)    
	if cur_x<2 and type(environment_matrix[cur_y][cur_x][1])==type(1):
		action.append(1)
	if cur_y<2 and type(environment_matrix[cur_y][cur_x][2])==type(1):
		action.append(2)
	if cur_x>0 and type(environment_matrix[cur_y][cur_x][3])==type(1):
		action.append(3)
	#else:
		#again([cur_x,cur_y],action)
		
	return action

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
	#return [cur_x, cur_y] in win_loss_states
	for x in win_loss_states:
		if [cur_x, cur_y] == x:
			return True
	
#def again(cur_pos, action):
	#getNextState(cur_pos[0], cur_pos[1], action)
	
discount = .5
learning_rate = .5
for _ in range(1000):
	# get starting place
	cur_pos = [0,0]
	# while goal state is not reached
	while(not isGameOver(cur_pos[0],cur_pos[1])):
		# get all possible next states from cur_step
		possible_actions = getAllPossibleNextAction(cur_pos[0],cur_pos[1])
		# select any one action randomly
		action = random.choice(possible_actions)
		# find the next state corresponding to the action selected
		next_state = getNextState(cur_pos[0], cur_pos[1], action)
		# update the q_matrix
		q_matrix[cur_pos[1]][cur_pos[0]][action] = q_matrix[cur_pos[1]][cur_pos[0]][action] + learning_rate * (environment_matrix[cur_pos[1]][cur_pos[0]][action] + discount * max(q_matrix[next_state].ravel()) - q_matrix[cur_pos[1]][ cur_pos[0]][action])
		# go to next state
		cur_pos = next_state
		
		
	# print status
	print("Episode ", _ , " done")
print(q_matrix)
print("Training done...")


	
