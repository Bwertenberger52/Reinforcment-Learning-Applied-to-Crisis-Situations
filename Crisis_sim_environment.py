import random
import turtle
import math
import time
import numpy as np
import matplotlib.pyplot as plt

environment_matrix = []

q_matrix = np.zeros((20,20,6))
print(q_matrix)
screen=turtle.getscreen()
screen.tracer(0)
turtle.up()
turtle.ht()
turtle.update()


SUSCEPTIBLE=(0,0,1)
INFECTED=(1,0,0)
ZOMBIE=(0,1,0)
RECOVERED=(.5,.5,.5)
MOVE_DISTANCE=20
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
            
        x,y,status,direction=person
            
        for other in population:
                
            if other[STATUS] == ZOMBIE:
                    
                    
                if d<perceptionRadius:
                    pass
            
        if (person[STATUS]==INFECTED):
            
            if random.random()<.02:
                
                person[STATUS]=ZOMBIE
                
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

