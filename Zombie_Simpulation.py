import random
import turtle
import math
import time
import numpy
import matplotlib.pyplot as plt


screen=turtle.getscreen()
screen.tracer(0)
turtle.up()
turtle.ht()
turtle.update()


SUSCEPTIBLE=(0,0,1)
INFECTED=(1,0,0)
ZOMBIE=(0,1,0)
RECOVERED=(.5,.5,.5)
MOVE_DISTANCE=1
X=0
Y=1
STATUS=2
DIRECTION=3
n=30

def getPopulation(n):
	
    population=[]
    
    for i in range(n):
		
        x=random.uniform(-200,200)
        y=random.uniform(-200,200)
        direction=random.uniform(0,360)
        status=SUSCEPTIBLE
        population.append([x,y,status,direction])
        
    return population

def infectPopulation(population,n=1):
	
    zombies = []
    
    while n:
		
        person=random.choice(population)
        
        if person[STATUS]==SUSCEPTIBLE:
			
            person[STATUS]=ZOMBIE
            zombies.append(person)
            n-=1

def display(population):
	
    turtle.clear()
    turtle.goto(220,220)
    turtle.down()
    turtle.seth(180)
    
    for i in range(4):
		
        turtle.forward(440)
        turtle.left(90)
        
    turtle.up()
    turtle.shapesize(2,2)
    
    for x,y,status,direction in population:
		
        turtle.goto(x,y)
        turtle.seth(direction)
        turtle.fillcolor(status)
        turtle.stamp()
        
    turtle.update()
    
def step(population,infectionRadius,infectionRate):
	
    perceptionRadius = 20
    zperceptionRadius = 35
    
    for person in population:
		
        x,y,status,direction=person
        
        if (person[STATUS] == ZOMBIE):
			
            smallestd=-1
            bestheading=-1
            
            for other in population:
				
                if other[STATUS] != ZOMBIE:
					
                    if other[STATUS] != RECOVERED:
						
                        i,j,*_=other
                        d=math.hypot(x-i,y-j)
                        heading = (math.degrees(math.atan2(y-j,x-i))-180)
                        
                        if d<zperceptionRadius:
							
                            if d<smallestd or smallestd==-1:
								
                                smallestd=d
                                bestheading=heading
                                
                                if x<-200 or x>200:
                                    x=y=0
                                if y>200 or y<-200:
                                    x=y=0
                                if isinstance(X,list):
                                    print(X)
                                    
                                person[DIRECTION] = bestheading 
                                x+=MOVE_DISTANCE*math.cos(bestheading)
                                y+=MOVE_DISTANCE*math.sin(bestheading)
                                person[X]=x
                                person[Y]=y
                                
            fight(person,population,infectionRadius,infectionRate)
            
        if (person[STATUS] == RECOVERED):
            pass
            
        if (person[STATUS]==SUSCEPTIBLE):
			
            x,y,status,direction=person
            smallestd=-1
            bestheading=-1
            
            for other in population:
				
                if other[STATUS] == ZOMBIE:
					
                    i,j,*_=other
                    d=math.hypot(x-i,y-j)
                    heading = math.degrees(math.atan2(y-j,x-i))
                    x,y,status,direction=person
                    x+=MOVE_DISTANCE*math.cos(direction/180*math.pi)
                    y+=MOVE_DISTANCE*math.sin(direction/180*math.pi)
                    direction+=random.uniform(-5,5)
                    
                    if x<-200 or x>200:
                        direction=180-direction
                    if y>200 or y<-200:
                        direction=-direction
                    if isinstance(X,list):
                        print(X)
                        
                    person[X]=x
                    person[Y]=y
                    person[DIRECTION]=direction
                    
                    if d<perceptionRadius:
						
                        if d<smallestd or smallestd==-1:
							
                            smallestd=d
                            bestheading=heading
                            
                            if x<-200 or x>200:
                                direction=180-direction
                            if y>200 or y<-200:
                                bestheading=-bestheading
                            if isinstance(X,list):
                                print(X)
                                
                            person[DIRECTION] = bestheading 
                            x+=MOVE_DISTANCE*math.cos(bestheading)
                            y+=MOVE_DISTANCE*math.sin(bestheading)
                            person[X]=x
                            person[Y]=y
                            
            expose(person,population,infectionRadius,infectionRate)
            
        if (person[STATUS]==INFECTED):
			
            if random.random()<.02:
				
                person[STATUS]=ZOMBIE
                
            x,y,status,direction=person
            x+=MOVE_DISTANCE*math.cos(direction/180*math.pi)
            y+=MOVE_DISTANCE*math.sin(direction/180*math.pi)
            direction+=random.uniform(-5,5)
            
            if x<-200 or x>200:
                direction=180-direction
            if y>200 or y<-200:
                direction=-direction
            if isinstance(X,list):
                print(X)
                
            person[X]=x
            person[Y]=y
            person[DIRECTION]=direction
            
            
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
	
    x,y,status,direction=person
    
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
    
    for _,_,status,_ in population:
		
        s+=status==SUSCEPTIBLE
        i+=status==INFECTED
        r+=status==RECOVERED
        z+=status==ZOMBIE
        
    return s,i,r,z

def simulation(n=100,InitialInfectionCount=1,infectionRadius=20,infectionRate=.02,show=True):
	
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
            display(population)
            
        if(((S[-1]==0) and (I[-1]==0)) or ((Z[-1]==0) and (I[-1]==0))):
            break
            
    return S,I,R,Z
    


def duration(n=100,samples=10):
	
    m=[]
    
    for i in range(samples):
		
        data=simulation(n=n,show=True)
        m.append(len(data[0]))
        
    m.sort()
    
    return m[samples//2]

'''def duration_and_killcount(n=100,samples=10):
	
    durations=[]
    killcount=[]
    
    for i in range(samples):
		
        data=simulation(n=n,show=False)
        durations.append(len(data[0]))
        killcount.append(max(data[2]))
        
    durations.sort()
    killcount.sort()
    
    return durations[samples//2],
    return killcount[samples//2]

def end_pop(n=100, samples=10):
	
	S = []
	I = []
	R = []
	Z = []
	for i in range(samples):
	
		data = simulation(n=n,show = False)
		S.append(data[0])
		I.append(data[1])
		R.append(data[2])
		Z.append(data[3])
	SUS = numpy.array(S)
	INF = numpy.array(I)
	REC = numpy.array(R)
	ZOM = numpy.array(Z)
	return SUS,INF,REC,ZOM
	
#X_values=[]
#Y_values=[]
#for n in range(10,200,20):
#    X_values.append(n)
#    Y_values.append(end_pop(n=n,samples=10))
#    print(n)


# ~ plt.plot(X_values,Y_values,".")
# ~ plt.xlabel('Population Size')
# ~ plt.ylabel('Duration (au)')
# ~ plt.title('SIR Model Simulating Pandemic Duration')
# ~ plt.show()



# Basic stacked area chart for a population of 75.
# ~ data=simulation(n=75,show=False)
# ~ p=range(len(data[0]))
# ~ plt.stackplot(p,data, labels=['S','I','R','Z'],colors=[SUSCEPTIBLE,INFECTED,RECOVERED,ZOMBIE])
# ~ plt.legend(loc='upper left')
# ~ plt.xlabel('step count')
# ~ plt.ylabel('population')
# ~ plt.title('SIR Simulation (n=100)')
# ~ plt.show()



#Basic stacked area chart for a population of 2045.
# ~ data=simulation(n=350,show=False)
# ~ p=range(len(data[0]))
# ~ plt.stackplot(p,data, labels=['S','I','R','Z'],colors=[SUSCEPTIBLE,INFECTED,RECOVERED,ZOMBIE])
# ~ plt.legend(loc='upper left')
# ~ plt.xlabel('step count')
# ~ plt.ylabel('population')
# ~ plt.title('SIR Simulation (n=100)')
# ~ plt.show()

#a,b,c,d = end_pop()
#plt.plot(X_values, a, 'b--', X_values, b, 'rs', X_values, c, 'k^',X_values,d,'go')
#plt.hist(c, X_values, density=True, histtype='bar', color=[RECOVERED,RECOVERED,RECOVERED,RECOVERED,RECOVERED,RECOVERED,RECOVERED,RECOVERED,RECOVERED,RECOVERED], label=['S','I','R','Z'])
#plt.legend(prop={'size': 10})
#plt.title('bars with legend')
#plt.show()

#plt.stackplot(X_values, Y_values)
'''
duration(100,10)

