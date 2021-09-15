#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 12:46:13 2018

@author: Campola2211
"""
import numpy as np
import matplotlib.pyplot as plt
import random
#counts the number of houses within the grid generation
def house_count(cube, gen,WIDTH,HEIGHT,HOUSE):
    count = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if cube[x,y,gen] == HOUSE:
                count += 1
    
    return count


# returns the coordinates of the value asked for each point on the grid
def points_for_grid(grid, val,WIDTH,HEIGHT):
    xcoords = []
    ycoords = []
    for i in range(0,WIDTH):
        for j in range(0,HEIGHT):
            if grid[i,j] == val:
                xcoords.append(j)
                ycoords.append(i)
    return [xcoords,ycoords]


#counts down how long a point has left to burn
def burning_time(cube,x,y,gen,timer,BARREN):
    if timer[x,y] != 0:
        timer[x,y] -= 1
        #print("still burning")
        #print(cube[x,y,gen+1]) 
    else:
        cube[x,y,gen+1] = BARREN
        #print(cube[x,y,gen+1])


#chooses a random location that is not within the right side and turns it to a burning space if there is a tree in the space
def lightning_strike(cube, FOREST, BARREN, BURNING_SPACE, gen,timer):


    x_random = random.randint(0,49)
    y_random = random.randint(0,24)
    if cube[x_random,y_random,gen] == FOREST:

        cube[x_random,y_random,gen+1] = BURNING_SPACE
        timer[x_random,y_random] = TIME_TO_BURN


        
#spreads the fire if there is a neighboring non-BARREN spot depending on if the random probabilty that is generated is greater than the immunity
def fire_spread(grid,x,y,gen,WIDTH,HEIGHT,FOREST,BURNING_SPACE,HOUSE, TIME_TO_BURN, timer,PROB_TREE_IMMUNE,PROB_HOUSE_IMMUNE):    
    if x < WIDTH-1 and grid[x+1,y,gen] == FOREST:
        firstTree = random.uniform(0,1)
        if(firstTree > PROB_TREE_IMMUNE):
            grid[x+1,y,gen+1] = BURNING_SPACE
            timer[x+1,y] = TIME_TO_BURN

    if x > 0 and grid[x-1,y,gen] == FOREST:
        secondTree = random.uniform(0,1)
        if(secondTree > PROB_TREE_IMMUNE):
            grid[x-1,y,gen+1] = BURNING_SPACE
            timer[x-1,y] = TIME_TO_BURN

    if y < HEIGHT-1 and grid[x,y+1,gen] == FOREST:
        thirdTree = random.uniform(0,1)
        if(thirdTree > PROB_TREE_IMMUNE):
            grid[x,y+1,gen+1] = BURNING_SPACE
            timer[x,y+1] = TIME_TO_BURN
        
    if y > 0 and grid[x,y-1,gen] == FOREST:                          
        fourthTree = random.uniform(0,1)
        if(fourthTree > PROB_TREE_IMMUNE):
            grid[x,y-1,gen+1] = BURNING_SPACE
            timer[x,y-1] = TIME_TO_BURN
      
        
        
        
        
    if x < WIDTH-1 and grid[x+1,y,gen] == HOUSE:                    
        firstHouse = random.uniform(0,1)
        if(firstHouse > PROB_HOUSE_IMMUNE):
            grid[x+1,y,gen+1] = BURNING_SPACE
        
    if x > 0 and grid[x-1,y,gen] == HOUSE:
        secondHouse = random.uniform(0,1)                          
        if(secondHouse > PROB_HOUSE_IMMUNE):
            grid[x-1,y,gen+1] = BURNING_SPACE
        
    if y < HEIGHT-1 and grid[x,y+1,gen] == HOUSE:                   
        thirdHouse = random.uniform(0,1)
        if(thirdHouse > PROB_HOUSE_IMMUNE):
            grid[x,y+1,gen+1] = BURNING_SPACE
        
    if y > 0 and grid[x,y-1,gen] == HOUSE:                          
        fourthHouse = random.uniform(0,1)
        if(fourthHouse > PROB_HOUSE_IMMUNE):
            grid[x,y-1,gen+1] = BURNING_SPACE
        





#runs the simulation
def runsim(
FOREST_DENSITY = .7,
PROB_LIGHTNING = .1,
PROB_TREE_IMMUNE = .25,
PROB_HOUSE_IMMUNE = .5,
TIME_TO_BURN = 3):
    
    WIDTH = 50
    HEIGHT = 50
    NUM_GEN = 200

    timer = np.zeros(WIDTH * HEIGHT)
    timer.shape = (WIDTH, HEIGHT)

    cube = np.empty((WIDTH, HEIGHT, NUM_GEN))
    cube[:,:,0] = 0


    #creates the forest
    config_woods = np.random.choice([BARREN,FOREST],p=[1-FOREST_DENSITY,FOREST_DENSITY],size=WIDTH * HEIGHT)
    config_woods.shape = (WIDTH,HEIGHT)
    #creates the residential area
    config = np.random.choice([BARREN,HOUSE],p=[.6,.4],size=WIDTH * HEIGHT)
    config.shape = (WIDTH,HEIGHT)


    cube[:,:,0] = config_woods[:,:]

    cube[0:50,49,0] = 0

    cube[0:50,49,0] = config[0:50,49]




    #how many houses exist at the beginning
    first_house_count = house_count(cube, 0,WIDTH,HEIGHT,HOUSE)
    

    for gen in range(1,NUM_GEN):
        cube[:,:,gen] = cube[:,:,gen-1]
        lightning_chance = random.uniform(0,1)
        
        if(lightning_chance <= PROB_LIGHTNING):
            lightning_strike(cube, FOREST, BARREN, BURNING_SPACE,gen-1,timer)
        
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if cube[x,y,gen-1] == BURNING_SPACE:
                
                    fire_spread(cube,x,y,gen-1,WIDTH,HEIGHT,FOREST,BURNING_SPACE,HOUSE, TIME_TO_BURN, timer,PROB_TREE_IMMUNE,PROB_HOUSE_IMMUNE)
                    burning_time(cube,x,y,gen-1,timer,BARREN)
            
            
    
    for gen in range(0,NUM_GEN):
        plt.clf()
        xc, yc = points_for_grid(cube[:,:,gen],0,WIDTH,HEIGHT)
        plt.scatter(xc,yc,marker="s",color="white")
        xc, yc = points_for_grid(cube[:,:,gen],1,WIDTH,HEIGHT)
        plt.scatter(xc,yc,marker="p",color="brown")
        xc, yc = points_for_grid(cube[:,:,gen],3,WIDTH,HEIGHT)
        plt.scatter(xc,yc,marker="^",color="green")
        xc, yc = points_for_grid(cube[:,:,gen],4,WIDTH,HEIGHT)
        plt.scatter(xc,yc,marker="D",color="orange")
        plt.title("Generation #" + str(gen))
        plt.show()
    
    #how many houses are left
    second_house_count = house_count(cube, 199, WIDTH, HEIGHT, HOUSE)
    
    print("The fraction of houses that were burnt down is " + str(1 - (second_house_count/first_house_count)))
    return 1 - (second_house_count/first_house_count)

HOUSE = 1
BARREN = 0
FOREST_DENSITY = .7
FOREST = 3
PROB_LIGHTNING = .1
BURNING_SPACE = 4
PROB_TREE_IMMUNE = .25
PROB_HOUSE_IMMUNE = .5
TIME_TO_BURN = 3




'''
degrees = np.arange(0,1,.1)
#each final generation uniformity within a tested THRESHOLD value
avg_house_fraction = 0
#The average of the acummulated uni_for_tol divided by the amount of simulations ran for the THRESHOLD value
final_fraction = []
for deg in degrees:
    avg_house_fraction = 0
    for i in range(50):
        #print("Degree is " + str(deg))
        avg_house_fraction += runsim(FOREST_DENSITY = .7,
                                     PROB_LIGHTNING = .1,
                                     PROB_TREE_IMMUNE = .25,
                                     PROB_HOUSE_IMMUNE = deg,
                                     TIME_TO_BURN = 3)
        #print(avg_uniformity(cube[:,:],WIDTH,HEIGHT,EMPTY))
        #uni_for_tol += (avg_uniformity(cube[:,:],WIDTH,HEIGHT,EMPTY))
    final_fraction.append(avg_house_fraction/50)


'''
avg_house_fraction = runsim(FOREST_DENSITY = .7,
                            PROB_LIGHTNING = .1,
                            PROB_TREE_IMMUNE = .25,
                            PROB_HOUSE_IMMUNE = .5,
                            TIME_TO_BURN = 3)
'''



plt.clf()
plt.plot(degrees, final_fraction)
plt.title("House Immunity Simulation")
plt.xlabel("Probability of House Immunity")
plt.ylabel("Percent of Houses Burnt Down")
#plt.ylim(0,1)
plt.savefig('House FireProof.png')

'''
