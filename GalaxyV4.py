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

global bigI     #The Universal time step (heartbeat) of the program see Main
global starforming_chance   #Single tunable value. Indvidual probabilites are associated with
                            #triggering neighboring pixels regions for geometric reasons see the SPSF function
global Total_Galactic_Cells #The total number of clouds in the galaxy. 
global previous_count       #A record keeping of total active cells at the last iteration
global active_list          #Records the total number of active cells at each iteration for a graph
bigI = 0
starforming_flag = False
Total_Galactic_Cells = 0
previous_count = 0
active_list = []



#Decided to make most things Global
Rings = 80                     #the size of the Galaxy
Iterations = 4000              #number of times to go through loop in main
Galaxy =[]                      #global stucture that holds the Galaxy
Ring_Velocity = [] #This is a set of ring lists for the velocity/increment angle for rotation
Cloud_num = [] #This is a single list that enumerates how many cells are in each ring
starforming_chance = 1.5 #The global starforming probability- it is modified in SPSF function
initial_SN_coefficient = .001 #adjust to control initial number of SN


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
        #(2*math.pi/(2.5*x+1)) 
        
    return  (2*math.pi/(2.5*x+1))


#Makes the Galaxy construct. There may be a better Pythonic way... 
def Make_Galaxy(Rings):
    
    Clouds = [] #this is just temporary to create a cloud attribute list
    global Total_Galactic_Cells

    
    #This loop generates the number of clouds per Ring. The values are
    #stored in a list and referred to in the loop that makes the Galaxy
    #Many functions act weird near zero and 1... so I gave up and said
    #Clouds will start in a ring of at least Fx(2)
    for i in range(2,Rings+2,1):
        Cloud_num.append(round(Cloud_Maker(i)))
    for i in range(len(Cloud_num)):
        Ring_Velocity.append(Ring_Velocity_Maker(i))
    
    #Creates Rings and Clouds for the Galaxy 
    # The attributes of a cloud are theta (Cloud_PA), age, and color. This is a small nested
    #list for each cloud.
    for i in range(Rings):
        for j in range(Cloud_num[i]):
            cloud_PA = 2*math.pi/Cloud_num[i]*j #the (initial/current) position angle of the cloud
            Clouds.append([cloud_PA,0,'black']) # this appends a small list of attibutes to each cloud in the cloud list (a Ring) 
            Total_Galactic_Cells += 1
            
        Galaxy.append(Clouds)  #appends a newly made Ring
        Clouds = []           #This cloud list is temporary so it is reset

        
    #prints the number of clouds in each ring to the console
    #it is helpful to see this          
    print(Cloud_num)    

    return()


#Seeds the galaxy with SNe, adjustment of the probabilty
# is necessary depending on number of cells in the Galaxy 
def Initialize_Galaxy():
    

    for i in range(len(Galaxy)):
        for j in range(len(Galaxy[i])):
            rng.seed()
            if rng.random() < initial_SN_coefficient: #adjust this number
                Galaxy[i][j][age] = 1  #SNe are the lowest numbered active cells
                Galaxy[i][j][color_] = 'white'
                       
    return ()

def Display_Rotation_Curve():
    
    rotation_rate = []
    
    fig, (ax1) = plt.subplots(1,constrained_layout=True,figsize=(12,12),sharex=False, sharey=False)
    fig.suptitle('Galaxy Rotation Curve')
    plt.sca(ax1)
    ax1.set_facecolor('#000000')
    ax1.set_xlabel('Ring')
    ax1.set_ylabel('Cloud Velocity')
                      
    rings = range(0,len(Galaxy),1)

    for i in range(len(Galaxy)):
        rotation_rate.append(Ring_Velocity[i]*Cloud_num[i]) 
                     
    ax1.plot(rings,rotation_rate,color='red')
      
    plt.savefig('galaxy_rotation_curve.png')                      
                       
                
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
                black_x_coords.append((i)*math.cos(Galaxy[i][j][theta]-Ring_Velocity[i]*bigI))
                black_y_coords.append((i)*math.sin(Galaxy[i][j][theta]-Ring_Velocity[i]*bigI))
            else:
                active_x_coords.append((i)*math.cos(Galaxy[i][j][theta]-Ring_Velocity[i]*bigI))
                active_y_coords.append((i)*math.sin(Galaxy[i][j][theta]-Ring_Velocity[i]*bigI))
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
    
    fig, (ax1) = plt.subplots(1,constrained_layout=True,figsize=(36,36),sharex=False, sharey=False)
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
        ax1.scatter(x_coords_,y_coords_,marker='o',color=colors_,s=4)  
    else:
        ax1.scatter(active_x_coords,active_y_coords,marker='o',color=colors,s=4,alpha=1)
        ax1.scatter(black_x_coords,black_y_coords,marker='o',color='black',s=4,alpha=1)
      
    plt.savefig('galaxy_'+str(index)+'.png')          
    plt.close(fig)
            
    return  

#Updates the Galaxy in the following way.. for each cell
    
#1.  Cells that have a value of "1" and within the Ring bounds  
#       are sent to SPSF which returns a list of neighboring cells that are
#       made active. This is a list of index pairs.
    
#2.  All Cells are aged if they are active ("0" cells just stay 0)

#3   Finally "triggered" cells are written to the Galaxy for the next loop  
#       This does mean some cells are aged that may be subsequently trigged 
#       and reset to age 1..but this is correct. Update of triggered cells
#       occurs after aging them, see below that Triggered_cells is investigated
#       after the aging process.

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
    
    #kickstart the nucleus. See  the SPSF function         
    if rng.random() < .5 and Galaxy[1][1][age] != 1 and bigI < 10:
        Galaxy[1][1][age]= 1
        Galaxy[1][1][color_] = 'white'
    
    for i in range(len(Galaxy)):
        for j in range(len(Galaxy[i])):
            if Galaxy[i][j][age] == 1 and i > 0 and i < len(Galaxy)-1:
                triggered_cells.append(SPSF(i,j))
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
                       triggered_cells.append(SPSF(i,j))
                    else:
                        Galaxy[i][j][color_] = '#C21515'  #basically red  
                        Galaxy[i][j][age] += 1
                count += 1 #Totals the number of active cells in each iteration
    active_list.append(count) #Update returns this list to graph active cells versus time
    
    #Although cells are unchanged for detemining neighbors and aged above, triggered_cells
    #stores the list of small lists that SPSF returns. The number of pairs of indices (Ring,cell)
    #is unknown until after SPSF returns the results of which neighbors were activated. This is
    #why the inner loop is the len(triggered_cells[k]) for each return of SPSF (l). The "0" 
    #index is for the Ring and "1" is the cell index. 
    if triggered_cells:                
        for k in range(len(triggered_cells)):
            for l in range(len(triggered_cells[k])):
                count += 1
                ring = triggered_cells[k][l][0]
                cell = triggered_cells[k][l][1]
                Galaxy[ring][cell][age] = 1
                Galaxy[ring][cell][color_] = 'white'
    
    #This ratio is monitored if it is desired to regulate the starformation based
    #on the number of active cells            
    starburst_ratio = count/Total_Galactic_Cells
    print('Iterations %d      Active Cells %d (Previous %d)  Starburst Ratio  %.2f' % (bigI,count,previous_count,starburst_ratio))
    #The starforming_flag is tripped to being true only after the constraints for a high ratio
    #are met. This prevents the second if statement from adjusting the rate during the intial 
    #ramp up to what is hopefully a pseudo-stable system. 
    if starburst_ratio >.3 and count > previous_count and starforming_chance > 1.55:
        previous_count = count
        starforming_chance -= .025 
        starforming_flag = True
        print('StarFormation Rate Adjusted down to %.2f ' % starforming_chance)
    if starburst_ratio <.29 and  starforming_chance < 1.63:
        previous_count = count
        starforming_chance += .025
        print('StarFormation Rate Adjusted up to %.2f ' % starforming_chance)
        
    return(active_list)



#This routine ("Self Propogating Star Formation) applies the rules of triggering
    #neighboring cells if they win each roll of the dice. The indices are saved
    #to a small list which is returned. Thus, the "triggered" list in Update_Galaxy
    #is actually a list of lists. The number of elements is variable since the
    #it is not known in advance how many neighbors will become active
    #The index of an inner or outecring cell compared to the current cell in the
    #current ring  is found by the formula index2 = theta*Cloud_num[i -/+ 1 ]/2*PI
    #Where each ring's cell is of the form index = Galaxy[i][j][theta]*2*PI/Cloud_num[i]
    #Since the thetas in each ring are the same- this equation with index1, i, is equal to
    #index2 (what we need to know) and i -/+ 1. 
    #!Most important! Note that the rotation of the entire ring must also be compensated for 
    #in the calculation so that the relative angles between rings
    #work out. This is accomplished with -Ring_Velocity[current_ring-1]*bigI
    
def SPSF(current_ring, current_cell):

    total_cells = Cloud_num[current_ring]
    total_cells_outer_ring = Cloud_num[current_ring+1]
    total_cells_inner_ring = Cloud_num[current_ring-1]
    change_list = []
    enhance = 1 #see below
    age_throttle = [1] # for less starformation, triggered cells will not be of values in this list
                        #e.g. [1,2] will prevent starformation occurring in cells of age 1 or 2                    
    global bigI
    
    #Some runs have starformation die in the nucleus. That isn't fair. 
    #This enhancment for inner rings should help. This is a multiplier for starforming_chance
    if current_ring < 3:
        enhance = 2
    
    
    if current_ring > 0 and current_ring < len(Galaxy): #extra protection... not needed I think..but..
            
        #Current ring. Neighbors +/-1 in cell index
        rng.seed()
        if rng.random() < .2 *starforming_chance*enhance:
            if Galaxy[current_ring][(current_cell+1) % total_cells][age] not in age_throttle:
                change_list.append([current_ring,(current_cell+1) % total_cells])
            

                
        rng.seed()
        if rng.random() < .2 *starforming_chance*enhance:
            if Galaxy[current_ring][(current_cell-1) % total_cells][age] not in age_throttle:
                change_list.append([current_ring,(current_cell-1)])

                

        #Inner ring. Neighbors are matching angle in inner ring and that cell index -1
        rng.seed()
        if rng.random() < .15*starforming_chance*enhance: 
            j_inner_index = round((Galaxy[current_ring][current_cell][theta]-Ring_Velocity[current_ring-1]*bigI)*Cloud_num[current_ring-1]/(2*math.pi)) % total_cells_inner_ring
            if Galaxy[current_ring-1][j_inner_index][age] not in age_throttle :
                change_list.append([current_ring-1,(j_inner_index)])

        #The below is now vestigial. It would consider another inner ring neighbor pixel
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
        if rng.random() < .04*starforming_chance*enhance:
            j_outer_index = round((Galaxy[current_ring][current_cell][theta]-Ring_Velocity[current_ring+1]*bigI)*Cloud_num[current_ring+1]/(2*math.pi)) % total_cells_outer_ring 
            if Galaxy[current_ring+1][j_outer_index][age] not in age_throttle:
                change_list.append([current_ring+1,j_outer_index])
      
        rng.seed()    
        if rng.random() < .04*starforming_chance*enhance:
            j_outer_index = round((Galaxy[current_ring][current_cell][theta]-Ring_Velocity[current_ring+1]*bigI)*Cloud_num[current_ring+1]/(2*math.pi)) % total_cells_outer_ring
            if Galaxy[current_ring+1][(j_outer_index+1) % total_cells_outer_ring][age] not in age_throttle:
                change_list.append([current_ring+1,(j_outer_index+1) % total_cells_outer_ring])  
                
        rng.seed()    
        if rng.random() < .04*starforming_chance*enhance:
            j_outer_index = j_outer_index = round((Galaxy[current_ring][current_cell][theta]-Ring_Velocity[current_ring+1]*bigI)*Cloud_num[current_ring+1]/(2*math.pi)) % total_cells_outer_ring
            if Galaxy[current_ring+1][(j_outer_index-1) % total_cells_outer_ring][age] not in age_throttle:
                change_list.append([current_ring+1,(j_outer_index-1) % total_cells_outer_ring])     

    return(change_list)
    
def Finalize_Galaxy(active_list): #plots active cells versus time
          
    fig, (ax1) = plt.subplots(1,constrained_layout=True,figsize=(12,12),sharex=False, sharey=False)
    fig.suptitle('Active Galaxy Regions')
    plt.sca(ax1)
    ax1.set_facecolor('#000000')
                      
    timesteps = range(0,bigI,1)                  
                      
    ax1.plot(timesteps,active_list,color='green')
      
    plt.savefig('galaxy_active_cells.png')                      
                       
                
    return ()
    

#I love simple lists of functions in main
#I use the loop in Rotate to create lists of rectangular coordinates to be rendered
#Unfortunately it was necessary to break up the list in to background-colored and
#normally colored pixels- becuase the argument for a subplot marker alpha value
# DOES NOT take a list...unlike all other arguments.
def main():
    
    global bigI
    active_list = []

    black_x_coords,active_x_coords,black_y_coords,active_y_coords, colors = [],[],[],[],[]
    
    Make_Galaxy(Rings)
    Display_Rotation_Curve()
    Initialize_Galaxy()
    Render_Galaxy(0,black_x_coords,active_x_coords,black_y_coords,active_y_coords,colors)
    for i in range(1,Iterations):
        active_list = Update_Galaxy(i)
        black_x_coords,active_x_coords,black_y_coords,active_y_coords,colors = Rotate_Galaxy()
        Render_Galaxy(i,black_x_coords,active_x_coords,black_y_coords,active_y_coords,colors)
        bigI += 1

    Finalize_Galaxy(active_list)
    
    return()

#This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
    



        