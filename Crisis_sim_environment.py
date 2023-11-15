import math
import random
import time
import turtle
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

environment_matrix = np.zeros((20,20,6),dtype = float)

q_matrix = np.zeros((20,20,6),dtype = float)

pos_matrix = np.zeros((20,20),dtype = int)

food_spots = []
gathered = False
ftime = 4
next_state_recc = []
goal = 0
hunger_bonus = 1
for x in range(20):

	environment_matrix[0][x][0]=environment_matrix[19][x][2]=environment_matrix[x][0][3]=environment_matrix[x][19][1] = None

for i in range(15):

	food_x = random.randrange(20)
	food_y = random.randrange(20)
	environment_matrix[food_y][food_x][5] = 200
	food_spots.append([food_x,food_y,gathered,ftime])

screen=turtle.getscreen()
screen.tracer(n=.5,delay=25)
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
n=25
infectionsRaduis = 20
infectionRate = .5
explore = .25
discount = .7
learning_rate = .4
future = 0

def getPopulation(n):
	
	pos_matrix = np.zeros((20,20),dtype = int)
	population=[]
	
	while(n>0):
		
		x=random.randrange(-200,200,20)
		y=random.randrange(-200,200,20)
		y_index =int((y+200)/20)
		x_index =int((x+200)/20)
		
		if pos_matrix[y_index][x_index] == 0:
			
			pos_matrix[y_index][x_index] = 1
			status=SUSCEPTIBLE
			timer = 500
			population.append([x,y,status,timer])
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
 
	
	for x,y,gathered,_ in food_spots:
		
		turtle.shapesize(1,1)
		turtle.shape("square")
		turtle.goto((x*20)-200,(y*20)-200)
		
		if gathered == False:
		
			turtle.fillcolor("yellow")
		
		else:
		
			turtle.fillcolor("grey")
		
		turtle.stamp()	
 	
	for x,y,status,_ in population:
		
		if status == RECOVERED:
		
			pass
		
		else:
		
			turtle.shape("circle")
			turtle.goto(x,y)
			turtle.fillcolor(status)
			turtle.stamp()
		
	turtle.update()
	
def step(population,infectionRadius,infectionRate):
	recover_count = 0
	environment_matrix = np.zeros((20,20,6),dtype = float)
	
	for x in range(20):
	
		environment_matrix[0][x][0]=environment_matrix[19][x][2]=environment_matrix[x][0][3]=environment_matrix[x][19][1] = None
	
	for Y in pos_matrix:
	
		for X in pos_matrix:
	
			if pos_matrix[Y][X].all== 1:
	
				environment_matrix[Y][X-1][3]=environment_matrix[Y][X+1][1]=environment_matrix[Y-1][X][0]=environment_matrix[Y+1][X][2]=None
	
	for person in population:
	
		if person[STATUS] == ZOMBIE:
			global hunger_bonus
			x,y,_,timer = person
			environment_matrix[Y][X-1][4]=environment_matrix[Y][X+1][4]=environment_matrix[Y-1][X][4]=environment_matrix[Y+1][X][4]=100
			if (timer <= 10):
				hunger_bonus = 4
			else:
				hunger_bonus = 1
	for i in food_spots:
	
		food_x,food_y,_,_ = i
		environment_matrix[food_y][food_x][5] = 200*hunger_bonus
		if (food_y>0):
			environment_matrix[food_y-1][food_x][0] = 50
		if (food_y<19):
			environment_matrix[food_y+1][food_x][2] = 50
		if (food_x>0):
			environment_matrix[food_y][food_x-1][3] = 50
		if (food_x<19):
			environment_matrix[food_y][food_x+1][1] = 50
	
	for person in population:

		if person[STATUS] == SUSCEPTIBLE or person[STATUS] == INFECTED:
	
			x,y,status,timer=person
			x_index = int((x+200)/20)
			y_index = int((y+200)/20)
			possible_actions = getAllPossibleNextAction(x_index,y_index)
			possible_actions_values = []

			if (random.random() > explore):
		
				for a in possible_actions:
		
					possible_actions_values.append(a[1])
		
		
				goal = max(possible_actions_values)
		
				for a in possible_actions:
		
					if a[1] != goal:
		
						possible_actions.remove(a)	
		
				action = (random.choice(possible_actions))[0]
			else:
				action = (random.choice(possible_actions))[0]
			next_state, act_type = getNextState(x_index, y_index, action)
	
			if act_type == 1:
	
				fight(person, population, infectionRadius, infectionRate)
	
			if act_type == 2:
				timer = gather(person,food_spots)
	
			q_matrix[y_index][x_index][action] = q_matrix[y_index][x_index][action] + (learning_rate * (environment_matrix[y_index][x_index][action] + (discount * recursive_action_values(x_index,y_index)) - q_matrix[y_index][x_index][action]))
			person[0] = (next_state[0]*20)-200
			person[1] = (next_state[1]*20)-200
			expose(person,population,infectionRadius,infectionRate)
			person[3] -= 1
	
			if person[3] == 0:
	
				person[2] = RECOVERED
				recover_count += 1
	
			if (person[STATUS]==INFECTED):
	
				if random.random()<.02:
	
					person[STATUS]=ZOMBIE 

		if (person[STATUS] == ZOMBIE):

			for other in population:
				
				if other[STATUS] != ZOMBIE:
					
					if other[STATUS] != RECOVERED:
						
						i,j,*_=other
						d=math.hypot(x-i,y-j)
						heading = (math.degrees(math.atan2(y-j,x-i))-180)

						if d<60:
	
							if heading > 0:
	
								if random.random() > 0.5:
	
									x+=20
	
								else:
	
									y+=20
	
							else:
	
								if random.random() > 0.5:
	
									x-=20
	
								else:
	
									y -= 20
	
						if x<-200 or x>200:
	
							x=y=0
	
						if y>200 or y<-200:
	
							x=y=0
	
						if isinstance(X,list):
	
							print(X)
	
						person[0]=x
						person[1]=y
			
def getAllPossibleNextAction(cur_x,cur_y):

	action = []

	if cur_y>0 and type(environment_matrix[cur_y][cur_x][0])!=None:

		action.append((0,q_matrix[cur_y][cur_x][0]))    

	if cur_x<19 and type(environment_matrix[cur_y][cur_x][1])!=None:

		action.append((1,q_matrix[cur_y][cur_x][1]))

	if cur_y<19 and type(environment_matrix[cur_y][cur_x][2])!=None:

		action.append((2,q_matrix[cur_y][cur_x][2]))

	if cur_x>0 and type(environment_matrix[cur_y][cur_x][3])!=None:

		action.append((3,q_matrix[cur_y][cur_x][3]))

	action.append((4,q_matrix[cur_y][cur_x][4]))
	action.append((5,q_matrix[cur_y][cur_x][5]))

	return action
		
def getNextState(cur_x, cur_y, action):

	if (action == 0):

		return [cur_x,cur_y - 1],0

	elif (action == 1):

		return [cur_x + 1,cur_y],0

	elif (action == 2):

		return [cur_x,cur_y + 1],0

	elif (action == 3):

		return [cur_x - 1,cur_y],0

	elif (action == 4): 

		return [cur_x,cur_y],1

	elif (action == 5):

		return [cur_x,cur_y],2
	else:
		return [-1,-1],-1
		
def gather(person,food_spots):

	x,y,_,timer = person

	for i in food_spots:

		if i[2] == False:

			if (((x+200)/20 == i[0]) and ((y+200)/20 == i[1])):

				person[3] += 100
				i[2]=True

		if(i[3]>0):

			i[3] -= 1

		else:

			i[2] = False
			i[3] = 4

		return timer
		
def expose(person,population,infectionRadius,infectionRate):
	
	x,y,status,_=person
	zRate = 1-infectionRate
	
	for other in population:
		
		if other[STATUS]==ZOMBIE:
			
			i,j,*_=other
			d=math.hypot(x-i,y-j)
			
			if d<infectionRadius and random.random()<zRate:
				
				person[STATUS]=INFECTED
				break
				
def fight(person,population, infectionRadius, infectionRate):
	
	x,y,status,_=person
	
	for other in population:
		
		if other[STATUS]==ZOMBIE:
			
			i,j,*_=other
			d=math.hypot(x-i,y-j)
			
			if d<infectionRadius and random.random()<infectionRate:
				
				other[STATUS]=RECOVERED
				break
				
		if other[STATUS]==INFECTED:
			
			i,j,*_=other
			d=math.hypot(x-i,y-j)
			
			if d<infectionRadius and random.random()<infectionRate:
				
				person[STATUS]=RECOVERED
				break
				
def census(population):
	
	s=i=r=z=0
	
	for _,_,status,_ in population:
		
		s+=status==SUSCEPTIBLE
		i+=status==INFECTED
		r+=status==RECOVERED
		z+=status==ZOMBIE
		
	return s,i,r,z

def recursive_action_values(cur_x, cur_y,goal=0):
	a = getAllPossibleNextAction(cur_x, cur_y)
	possible_actions_values =[]
	for i in a:
		possible_actions_values.append(i[1])

	goal = max(possible_actions_values)
	return goal
def simulation(n=25,InitialInfectionCount=1,infectionRadius=20,infectionRate=.25,show=True):

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
		#infectionRate*=(.96+(random.random()/10))
		
		if show:

			display(population,food_spots)

		count += 1
		
		if(((S[-1]==0) and (I[-1]==0)) or ((Z[-1]==0) and (I[-1]==0))):

			break
			
	return S,I,R,Z,count
	
def duration(n=25,samples=1000):
	
	m=[]
	
	for i in range(samples):
		
		data=simulation(n=n,show=False)
		m.append(data)
		print(i)
		
	m.sort()
	
	return m[samples//2],m[samples.max()]

def end_pop(n=25, samples=100):
	
	S = []
	I = []
	R = []
	Z = []
	c = []
	avpop=[]
	countpop = 0

	for i in range(samples):

		if (i%100 == 1):

			t = True
			avpop.append(countpop/100)
			countpop = 0

		else:

			t = False

		data = simulation(n=n,show = t)
		S.append(data[0])
		I.append(data[1])
		R.append(data[2])
		Z.append(data[3])
		c.append(data[4])
		countpop += data[0][-1]
		print(i+1)

	SUS = np.array(S,dtype=object)
	INF = np.array(I,dtype=object)
	REC = np.array(R,dtype=object)
	ZOM = np.array(Z,dtype=object)

	return SUS,INF,REC,ZOM,c,avpop



# Basic stacked area chart for a population without learning.
a,b,c,d,_=simulation(show= False)
p=range(len(a))
plt.stackplot(p,(a,b,c,d), labels=['S','I','R','Z'],colors=[SUSCEPTIBLE,INFECTED,RECOVERED,ZOMBIE])
plt.legend(loc='upper left')
plt.xlabel('step count')
plt.ylabel('population')
plt.title('SIRZ Simulation Sans Learning')
plt.show()

a,b,c,d,e,f = end_pop()
X_values=[]
X2_values=[]
Y1_values=[]
Y2_values=[]
Y3_values=[]

for n in range(100):

    X_values.append(n)
    Y1_values.append(a[n][-1])
    Y2_values.append(e[n])
    if (n%100 == 99):
        Y3_values.append(f[n//100])
        X2_values.append(n)



# Basic stacked area chart for a population with learning
a,b,c,d,_=simulation(show=True)
p=range(len(a))
plt.stackplot(p,(a,b,c,d), labels=['S','I','R','Z'],colors=[SUSCEPTIBLE,INFECTED,RECOVERED,ZOMBIE])
plt.legend(loc='upper left')
plt.xlabel('step count')
plt.ylabel('population')
plt.title('SIRZ Simulation With Learning')
plt.show()

qm = xr.DataArray(q_matrix)
qmdas = qm.to_dataframe("bruh")
qmdas.to_clipboard()

plt.plot(X_values,Y1_values,".")
plt.xlabel('Episode #')
plt.ylabel('Suseptible Population')
plt.title('SIRZ Model Simulating Zombie Epidemic End Populations')
plt.show()

plt.plot(X_values,Y2_values,".")
plt.xlabel('Episode #')
plt.ylabel('End Step Count')
plt.title('SIRZ Model Simulating Zobie Epidemic End Step Count')
plt.show()


plt.plot(X2_values,Y3_values,".")
plt.xlabel('Episod # (Groupings of 100)')
plt.ylabel('Avg Pop')
plt.title('SIRZ Model Simulating Zobie Epidemic Average Population')
plt.show()