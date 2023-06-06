# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 09:38:37 2020

@author: ngc1535
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 07:21:08 2020

@author: ngc1535
"""
import random as rng
import matplotlib.pyplot as plt
import math


#Nice index names to be used to clarify what is in [] brackets of nested
#lists
theta = 0
age =   1
color_ = 2  #the underscore was because I feared color might be in use

global bigI     #This is the Universal time step (heartbeat) of the program see Main
global starforming_chance   #Single tunable value. Indvidual probabilites are associated 
                            #triggering neighboring pixels regions for geometric reasons
global Total_Galactic_Cells #The total number of clouds in the galaxy. 
global previous_count       #A record keeping of total active cells
global active_list
bigI = 0
starforming_flag = False
Total_Galactic_Cells = 0
previous_count = 0
active_list = []



#Decided to make most things Global
Rings = 80 #the size of the Galaxy
Iterations = 1000
 #number of times to go through loop in main
Galaxy =[] #global stucture that holds the Galaxy
Cloud_angle_template= []  #A set of lists for each ring that contains the angles (for each index)
Ring_Velocity = [] #This is a set of ring lists for the velocity/increment angle for rotation
Cloud_num = [] #This is a single list that enumerates how many cells are in each ring
starforming_chance = 1.4 #The global starforming probability- it is modified in SPSF function
initial_SN_coefficient = .001 #adjust to control initial number of SN
Render_Scale = []

#adjust this function to change the number of clouds per ring
def Cloud_Maker(x):
       #
    return (pow(x,2)+50)# 

#adjust this function to change the increment angle per ring (for rotation rate)
def Ring_Velocity_Maker(x):
        #(2*math.pi/(1+1000-1000/pow(x,1)))
        #(2*math.pi/(x*math.log(x)+1))/150 
        #(x/math.log(180*x+2))/150
        #(2*math.pi/(Cloud_num[x]))
        
    return  (2*math.pi/(2.5*x+1))  #the last coefficient affects the "speed"


#Makes the Galaxy construct. There may be a better Pythonic way... 
def Make_Galaxy(Rings):
    
    Clouds,angles = [],[] #these are just temporary, used to create lists
    global Total_Galactic_Cells

    
    #This loop generates the number of clouds per Ring. The values are
    #stored in a list and referred to in the loop that makes the Galaxy
    #Many functions act weird near zero and 1... so I gave up and said
    #Clouds will start in a ring of at least Fx(2)
    for i in range(2,Rings+2,1):
        Cloud_num.append(round(Cloud_Maker(i)))
    for i in range(len(Cloud_num)):
        Ring_Velocity.append(Ring_Velocity_Maker(i))
    
    #Creates Rings, Clouds, and an "Cloud_angle_template" that I search to get indexes for a particular cloud
    #if necessary. The attributes of a cloud are theta (Cloud_PA), age, and color. This is a small nested
    #list for each cloud.
    for i in range(Rings):
        for j in range(Cloud_num[i]):
            cloud_PA = 2*math.pi/Cloud_num[i]*j #the (initial/current) position angle of the cloud
            Clouds.append([cloud_PA,0,'black']) # loop creates a cloud list (a Ring) with a smaller list of attributes
            angles.append(cloud_PA)
            Total_Galactic_Cells += 1
            
        Galaxy.append(Clouds)  #appends a newly made Ring
        Cloud_angle_template.append(angles) #a lists of angles for each cell of the ring
        Clouds = []           #This cloud list is temporary so it is reset
        angles = []             #also temporary in this function
        
             
    print(Cloud_num)    

 
        
    return()


#Seeds the galaxy with SNe, adjustment of the probabilty
# is necessary depending on number of cells in the Galaxy 
def Initialize_Galaxy():
    
    #for i in range(len(Galaxy)):
       # find_angle = getIndex.bisect_right(Cloud_angle_template[i],math.pi/5)
        #for j in range(len(Galaxy[i])):
            #if i == len(Galaxy)-12 and j==find_angle:
               # Galaxy[i][find_angle][age] = 1
                #Galaxy[i][j][color_]=='white'
            #if i == len(Galaxy)-2 and j==0:
                #Galaxy[i][j][age] = 1
                #Galaxy[i][j][color_]=='white'    
           
           
    for i in range(len(Galaxy)):
        for j in range(len(Galaxy[i])):
            rng.seed()
            if rng.random() < initial_SN_coefficient: #adjust this number
                Galaxy[i][j][age] = 1  #SNe are the lowest numbered active cells
                Galaxy[i][j][color_] = 'white'
                       
          
    return ()

#For each cell add the small angle increment that rotates a Ring
#The angles are stored in the list Ring_Velocity which was created in Make_Galaxy()
    #Used the loop here to create lists of cells to be passed to Render_Galaxy
    #This is one less loop through all the points!
    #Two four lists (two coordinates per color) are required to differentiate between
    #Active pixels with color and Transparent pixels for background-colors (black) cells (see Render_Galaxy)
    #This solved the display issue!!
def Rotate_Galaxy():
    
    black_x_coords,active_x_coords,black_y_coords,active_y_coords,colors = [],[],[],[],[]
    
    #for i in range(len(Galaxy)):
        #for j in range(len(Galaxy[i])):
            #if Galaxy[i][j][theta] + Ring_Velocity[i] > 2*math.pi:  #keeping theta between 0-2PI
                #Galaxy[i][j][theta] = Galaxy[i][j][theta] + Ring_Velocity[i] - 2*math.pi
            #else:    
                #Galaxy[i][j][theta] += Ring_Velocity[i] 
                
    for i in range(len(Galaxy)):
        #Galaxy[i].append(Galaxy[i].pop(0))
        for j in range(len(Galaxy[i])):
            if Galaxy[i][j][theta] + Ring_Velocity[i] > 2*math.pi:  #keeping theta between 0-2PI
                Galaxy[i][j][theta] = Galaxy[i][j][theta] + Ring_Velocity[i] - 2*math.pi
            else:    
                Galaxy[i][j][theta] = Galaxy[i][j][theta] + Ring_Velocity[i] 

            if Galaxy[i][j][age] == 0:#black cells
                black_x_coords.append((i)*math.cos(Galaxy[i][j][theta]))
                black_y_coords.append((i)*math.sin(Galaxy[i][j][theta]))
            else:
                active_x_coords.append((i)*math.cos(Galaxy[i][j][theta]))
                active_y_coords.append((i)*math.sin(Galaxy[i][j][theta]))
                colors.append(Galaxy[i][j][color_])    
           # print(Galaxy[i][j][theta],j*2*math.pi/Cloud_num[i])    
                
    return (black_x_coords,active_x_coords,black_y_coords,active_y_coords,colors)



#plots the Galaxy 
#This function now only loops through the Galaxy once initially. 
#Otherwise, it receives coordinates from Rotate_Galaxy in two coordinate pair lists
#(four lists total) The active cells come in with a color list as well. The background-
#colored cells all have the same color. The background [age]=0 cells are transparent
#pixels which when overlayed with the previous cell state will permit underlying 
#pixel colors to show. No more clobbering of cells of any size!
    #
def Render_Galaxy(index,black_x_coords,active_x_coords,black_y_coords,active_y_coords,colors):
    
    fig, (ax1) = plt.subplots(1,constrained_layout=True,figsize=(12,12),sharex=False, sharey=False)
    plt.sca(ax1)
    ax1.set_facecolor('#000000')
    x_coords_,y_coords_,colors_ = [],[],[]
    
    
    if index == 0:    #first time render
        for i in range(len(Galaxy)):
            for j in range(len(Galaxy[i])):
                cloud_PA = Galaxy[i][j][theta]
                x_coords_.append((i)*math.cos(cloud_PA))
                y_coords_.append((i)*math.sin(cloud_PA))
                colors_.append(Galaxy[i][j][color_])      
        ax1.scatter(x_coords_,y_coords_,marker='o',color=colors_,s=(72./fig.dpi)**2)  
    else:
        ax1.scatter(active_x_coords,active_y_coords,marker='o',color=colors,s=(72./fig.dpi)**2,alpha=1)
        ax1.scatter(black_x_coords,black_y_coords,marker='o',color='black',s=(72./fig.dpi)**2,alpha=1)
      
    plt.savefig('galaxy_'+str(index)+'.png')          
    plt.close(fig)
            
    return  

#Updates the Galaxy in the following way.. for each cell
    
#1.  Cells that have a value of "1" and within the Ring bounds  
#       are sent to SPFS which returns a list of neighboring cells that are
#       made active. This is a list of index pairs.
    
#2.  All Cells are aged if they are active ("0" cells just stay 0)

#3   Finally "triggered" cells are written to the Galaxy for the next loop  

#Note that the reset of age 15 to zero does not allow for Galaxy[i][j][age] =1
#to be an exposed statement to the first major else... otherwise you age it!
#I guess the other Galaxy[i][j][age] =1 could be reduced... but for 
#concrete clarity..there they are.    
def Update_Galaxy(index):
    
    triggered_cells = []
    count = 0
    global starforming_chance
    global starforming_flag
    global previous_count
    global active_list
    
    rng.seed()
    
    
    for i in range(len(Galaxy)):
        for j in range(len(Galaxy[i])):
            if Galaxy[i][j][age] == 1 and i > 0 and i < len(Galaxy)-1:
                triggered_cells.append(SPFS(i,j))
            if Galaxy[i][j][age] == 0:
                pass
            else:
                if Galaxy[i][j][age] > 48:
                    Galaxy[i][j][age] = 0
                    Galaxy[i][j][color_] ='black'
                elif Galaxy[i][j][age] == 1:
                     Galaxy[i][j][age] += 1   
                     Galaxy[i][j][color_] ='White'
                elif Galaxy[i][j][age] > 1 and Galaxy[i][j][age] < 8:
                    Galaxy[i][j][color_] = '#db76f5' #bright purple
                    Galaxy[i][j][age] += 1   
                elif Galaxy[i][j][age] > 7 and Galaxy[i][j][age] < 14:
                    Galaxy[i][j][color_] = '#fac31e' #light orange
                    Galaxy[i][j][age] += 1    
                elif Galaxy[i][j][age] > 13 and Galaxy[i][j][age] < 50:
                    if rng.random() < .01 and Galaxy[i][j][age] > 40 and i > 0 and i < len(Galaxy)-1:
                       triggered_cells.append(SPFS(i,j))
                    else:
                        Galaxy[i][j][color_] = '#C21515'   
                        Galaxy[i][j][age] += 1
                count += 1
    active_list.append(count)
    
    if triggered_cells:                
        for k in range(len(triggered_cells)):
            for l in range(len(triggered_cells[k])):
                count += 1
                ring = triggered_cells[k][l][0]
                cell = triggered_cells[k][l][1]
                Galaxy[ring][cell][age] = 1
                Galaxy[ring][cell][color_] = 'white'
                
    starburst_ratio = count/Total_Galactic_Cells
    print('Iterations %d      Active Cells %d (Previous %d)  Starburst Ratio  %.2f' % (bigI,count,previous_count,starburst_ratio))
    if starburst_ratio >.3 and count > previous_count and starforming_chance > 1.48:
        previous_count = count
        starforming_chance -= .1   
        starforming_flag = True
        print('StarFormation Rate Adjusted down to %.2f ' % starforming_chance)
    if starburst_ratio <.28 and  starforming_chance < 1.6:
        previous_count = count
        starforming_chance += .1
        print('StarFormation Rate Adjusted up to %.2f ' % starforming_chance)
    return(active_list)



#This routine ("Self Propogating Star Formation) applies the rules of triggering
    #neighboring cells if they win each roll of the dice. The indices are saved
    #to a small list which is returned. Thus, the "triggered" list in Update_Galaxy
    #is actually a list of lists. The number of elements is variable since the
    #it is not known in advance how many neighbors will become active
    #To compute the index of a cell in an inner or outer ring (compared with
    #the current cell) a binary search of Cloud_angle_temple- which holds the 
    #theta value for each cell occurs. The index returned by bisect is the 
    #INSERTION position...which is +1 of the index I want... so I need to decrement the result.
    #If Bisect returns 0... then the index I want is actually -1... or the wrap around cell value.
    #Probabilities generally favor inner direction slightly due to geometry, cell numbers, and 
    #propogation effects
def SPFS(current_ring, current_cell):

    total_cells = Cloud_num[current_ring]
    total_cells_outer_ring = Cloud_num[current_ring+1]
    total_cells_inner_ring = Cloud_num[current_ring-1]
    change_list = []
    age_throttle = [1] # for less starformation, triggered cells will not be of values in this list
                        #e.g. [1,2] will prevent starformation occurring in cells of age 1 or 2                    
    global bigI
    
    
    if current_ring > 0 and current_ring < len(Galaxy): #extra protection... not needed I think..but..
            
        #Current ring. Neighbors +/-1 in cell index
        rng.seed()
        if rng.random() < .2 *starforming_chance:
            if Galaxy[current_ring][(current_cell+1) % total_cells][age] not in age_throttle:
                change_list.append([current_ring,(current_cell+1) % total_cells])
            

                
        rng.seed()
        if rng.random() < .2 *starforming_chance:
            if Galaxy[current_ring][(current_cell-1) % total_cells][age] not in age_throttle:
                change_list.append([current_ring,(current_cell-1)])

                

        #Inner ring. Neighbors are matching angle in inner ring and that cell index -1
        rng.seed()
        if rng.random() < .15*starforming_chance: 
            j_inner_index = round((Galaxy[current_ring][current_cell][theta]-Ring_Velocity[current_ring-1]*bigI)*Cloud_num[current_ring-1]/(2*math.pi)) % total_cells_inner_ring
            #print(math.degrees(Galaxy[current_ring][current_cell][theta]),math.degrees(Galaxy[current_ring-1][j_inner_index][theta]))
            if Galaxy[current_ring-1][j_inner_index][age] not in age_throttle :
                change_list.append([current_ring-1,(j_inner_index)])

        #rng.seed()
        #if rng.random() < .2*starforming_chance:
            #j_inner_index = int(Galaxy[current_ring][current_cell][theta]*Cloud_num[current_ring-1]/(2*math.pi)) % total_cells_inner_ring 
            #print(Galaxy[current_ring-1][(j_inner_index+1) % total_cells_inner_ring][age] < 1000 and abs(Galaxy[current_ring][current_cell][theta]-Galaxy[current_ring-1][(j_inner_index-1) % total_cells_inner_ring ][theta]),2*math.pi/Cloud_num[current_ring-1]*1.4)
            #if Galaxy[current_ring-1][(j_inner_index+1) % total_cells_inner_ring][age] < 1000 and abs(Galaxy[current_ring][current_cell][theta]-Galaxy[current_ring-1][(j_inner_index-1) % total_cells_inner_ring ][theta]) < 2*math.pi/Cloud_num[current_ring]:
               # print(Galaxy[current_ring-1][(j_inner_index+1) % total_cells_inner_ring][age] < 1000 and abs(Galaxy[current_ring][current_cell][theta]-Galaxy[current_ring-1][(j_inner_index-1) % total_cells_inner_ring ][theta]),2*math.pi/Cloud_num[current_ring-1]*1.4)
               # print('true')
               # change_list.append([current_ring-1,(j_inner_index+1) % total_cells_inner_ring])       


        
        #Outer ring. Neighbors are matching angle in outer ring, and +/- 1 cell index
        rng.seed()
        if rng.random() < .04*starforming_chance:
            j_outer_index = round((Galaxy[current_ring][current_cell][theta]-Ring_Velocity[current_ring+1]*bigI)*Cloud_num[current_ring+1]/(2*math.pi)) % total_cells_outer_ring 
            if Galaxy[current_ring+1][j_outer_index][age] not in age_throttle:
                change_list.append([current_ring+1,j_outer_index])
      
        rng.seed()    
        if rng.random() < .04*starforming_chance:
            j_outer_index = round((Galaxy[current_ring][current_cell][theta]-Ring_Velocity[current_ring+1]*bigI)*Cloud_num[current_ring+1]/(2*math.pi)) % total_cells_outer_ring
            if Galaxy[current_ring+1][(j_outer_index+1) % total_cells_outer_ring][age] not in age_throttle:
                change_list.append([current_ring+1,(j_outer_index+1) % total_cells_outer_ring])  
                
        rng.seed()    
        if rng.random() < .04*starforming_chance:
            j_outer_index = j_outer_index = round((Galaxy[current_ring][current_cell][theta]-Ring_Velocity[current_ring+1]*bigI)*Cloud_num[current_ring+1]/(2*math.pi)) % total_cells_outer_ring
            if Galaxy[current_ring+1][(j_outer_index-1) % total_cells_outer_ring][age] not in age_throttle:
                change_list.append([current_ring+1,(j_outer_index-1) % total_cells_outer_ring])     

    return(change_list)
    
def Finalize_Galaxy(active_list):
    
    #for i in range(len(Galaxy)):
        #find_angle = getIndex.bisect_right(Cloud_angle_template[i],math.pi/2)
        #for j in range(len(Galaxy[i])):
            #if i == len(Galaxy)-2 and j==find_angle:
                #Galaxy[i][find_angle][age] = 1
                #Galaxy[i][j][color_]=='white'
           # if i == len(Galaxy)-2 and j==0:
                #Galaxy[i][j][age] = 1
                #Galaxy[i][j][color_]=='white'    
           
    fig, (ax1) = plt.subplots(1,constrained_layout=True,figsize=(12,12),sharex=False, sharey=False)
    fig.suptitle('Active Galaxy Regions')
    plt.sca(ax1)
    ax1.set_facecolor('#000000')
                      
    timesteps = range(0,bigI,1)                  
                      
    ax1.plot(timesteps,active_list,color='green')
      
    plt.savefig('galaxy_active_cells.png')                      
                       
                
    return ()
    

#I love simple lists of functions in main
def main():
    
    global bigI
    active_list = []

    black_x_coords,active_x_coords,black_y_coords,active_y_coords, colors = [],[],[],[],[]
    
    Make_Galaxy(Rings)
    Initialize_Galaxy()
    Render_Galaxy(0,black_x_coords,active_x_coords,black_y_coords,active_y_coords,colors)
    for i in range(1,Iterations):
        active_list = Update_Galaxy(i)
        black_x_coords,active_x_coords,black_y_coords,active_y_coords,colors = Rotate_Galaxy()
        #if index % 10 == 0: #this is for purposes of outputting each nth iteration
        Render_Galaxy(i,black_x_coords,active_x_coords,black_y_coords,active_y_coords,colors)
        bigI += 1

    Finalize_Galaxy(active_list)
    return()

#This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
    



        