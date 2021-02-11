import math
import random
import time
import turtle

import matplotlib.pyplot as plt
import numpy as np

environment_matrix = np.zeros((20,20,6),dtype = float)

q_matrix = np.zeros((20,20,6),dtype = float)

pos_matrix = np.zeros((20,20),dtype = int)

food_spots = []
gathered = False
for x in range(20):
	environment_matrix[0][x][0]=environment_matrix[19][x][2]=environment_matrix[x][0][1]=environment_matrix[x][19][3] = None
for i in range(8):
	food_x = random.randrange(20)
	food_y = random.randrange(20)
	environment_matrix[food_y][food_x][5] = 50
	food_spots.append([food_x,food_y,gathered])
screen=turtle.getscreen()
screen.tracer(0)
turtle.up()
turtle.ht()
turtle.update()
SUSCEPTIBLE=(0,0,1)
INFECTED=(1,0,0)
ZOMBIE=(0,1,0)
RECOVERED=(.5,.5,.5)
X=0
Y=1
STATUS=2
n=30

def getPopulation(n):
	
	population=[]
	
	while(n>0):
		
		x=random.randrange(-200,200,20)
		y=random.randrange(-200,200,20)
		y_index =int((y+200)/20)
		x_index =int((x+200)/20)
		if pos_matrix[y_index][x_index] == 0:
			pos_matrix[y_index][x_index] = 1
			status=SUSCEPTIBLE
			population.append([x,y,status])
			n-=1
		
	return population

def infectPopulation(population,n=1):
	
	zombies = []
	
	while n:
		
		person=random.choice(population)
		
		if person[STATUS]==SUSCEPTIBLE:
			
			person[STATUS]=ZOMBIE
			zombies.append(person)
			n-=1

def display(population,food_spots):
	
	turtle.clear()
	turtle.goto(220,220)
	turtle.down()
	turtle.seth(180)
	
	for i in range(4):
		
		turtle.forward(440)
		turtle.left(90)
		
	turtle.up()
 
	
	for x,y,gathered in food_spots:
		turtle.shapesize(1,1)
		turtle.shape("square")
		turtle.goto((x*20)-200,(y*20)-200)
		turtle.fillcolor("yellow")
		turtle.stamp()	
 	
	for x,y,status in population:
		turtle.shape("circle")
		turtle.goto(x,y)
		turtle.fillcolor(status)
		turtle.stamp()
		
	turtle.update()
	
def step(population,infectionRadius,infectionRate):
	for y in pos_matrix:
		for x in pos_matrix:
			if pos_matrix[y][x].all== 1:
				environment_matrix[y][x-1][1]=environment_matrix[y][x+1][3]=environment_matrix[y-1][x][2]=environment_matrix[y+1][x][0]=None
	for person in population:
		
		x,y,status=person
		x_index = int((x+200)/20)
		y_index = int((y+200)/20)
		discount = 0.2
		learning_rate = .5
		possible_actions = getAllPossibleNextAction(x_index,y_index)
		action = random.choice(possible_actions)
		next_state = getNextState(x_index, y_index, action)
		q_matrix[y_index][x_index][action] = q_matrix[y_index][x_index][action] + learning_rate * (environment_matrix[y_index][x_index][action] + discount * max(q_matrix[next_state].ravel()) - q_matrix[y_index][x_index][action])
		
		person[X] = (next_state[0]*20)-200
		person[Y] = (next_state[1]*20)-200


def getAllPossibleNextAction(cur_x,cur_y):
	action = []
	if cur_y>0 and type(environment_matrix[cur_y][cur_x][0])!=None:
		action.append(0)    
	if cur_x<19 and type(environment_matrix[cur_y][cur_x][1])!=None:
		action.append(1)
	if cur_y<19 and type(environment_matrix[cur_y][cur_x][2])!=None:
		action.append(2)
	if cur_x>0 and type(environment_matrix[cur_y][cur_x][3])!=None:
		action.append(3)
	action.append(4)
	action.append(5)
	return action
		
		
def getNextState(cur_x, cur_y, action):
	if (action == 0):
		return [cur_x,cur_y - 1]
	elif (action == 1):
		return [cur_x + 1,cur_y]
	elif (action == 2):
		return [cur_x,cur_y + 1]
	elif (action == 3):
		return [cur_x - 1,cur_y]
	elif (action == 4): 
		#fight()
		return [cur_x,cur_y] 
	elif (action == 5): 
		gather() 
		return [cur_x,cur_y] 
		
def gather():
	pass
		
def expose(person,population,infectionRadius,infectionRate):
	
	x,y,status,direction=person
	zRate = 1-infectionRate
	
	for other in population:
		
		if other[STATUS]==ZOMBIE:
			
			i,j,*_=other
			d=math.hypot(x-i,y-j)
			
			if d<infectionRadius and random.random()<zRate:
				
				person[STATUS]=INFECTED
				break
				
	
	
	
def fight(person,population, infectionRadius, infectionRate):
	
	x,y,status=person
	
	for other in population:
		
		if other[STATUS]==SUSCEPTIBLE:
			
			i,j,*_=other
			d=math.hypot(x-i,y-j)
			
			if d<infectionRadius and random.random()<infectionRate:
				
				person[STATUS]=RECOVERED
				break
				
		if other[STATUS]==INFECTED:
			
			i,j,*_=other
			d=math.hypot(x-i,y-j)
			
			if d<infectionRadius and random.random()<infectionRate:
				
				person[STATUS]=RECOVERED
				break
				
def census(population):
	
	s=i=r=z=0
	
	for _,_,status in population:
		
		s+=status==SUSCEPTIBLE
		i+=status==INFECTED
		r+=status==RECOVERED
		z+=status==ZOMBIE
		
	return s,i,r,z

def simulation(n=100,InitialInfectionCount=1,infectionRadius=20,infectionRate=.02,show=True):
	count = 0 
	population=getPopulation(n)
	infectPopulation(population,n=InitialInfectionCount)
	s,i,r,z=census(population)
	S=[s]
	I=[i]
	R=[r]
	Z=[z]
	while (True):
		
		step(population,infectionRadius,infectionRate)
		s,i,r,z=census(population)
		S.append(s)
		I.append(i)
		R.append(r)
		Z.append(z)
		infectionRate*=(.55+random.random())
		
		if show:
			display(population,food_spots)
		count += 1
		#if(((S[-1]==0) and (I[-1]==0)) or ((Z[-1]==0) and (I[-1]==0))):
		if count == 1000:
			print('Done')
			print(q_matrix.tolist())
			break
			
	return S,I,R,Z
	


def duration(n=100,samples=10):
	
	m=[]
	
	for i in range(samples):
		
		data=simulation(n=n,show=True)
		m.append(len(data[0]))
		
	m.sort()
	
	return m[samples//2]

simulation()
