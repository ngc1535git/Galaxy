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
import bisect as getIndex



#Nice index names
theta = 0
age =   1
color_ = 2
cloud_angle = 3 #This is 2*PI/number of clouds in a Ring


Rings = 80 #the size of the Galaxy
Iterations = 1000  #number of times to go through loop in main
Galaxy =[] #global stucture
Cloud_angle_template= []
Ring_Velocity = []
Cloud_num = []
starforming_chance = .35

#adjust this function to change the number of clouds per ring
def Cloud_Maker(x):
       
    return (4*pow(x,2)) 

#adjust this function to change the number of clouds per ring
def Ring_Velocity_Maker(x):
        #(2*math.pi/(1+1000-1000/pow(x,1)))
        #(2*math.pi/(x*math.log(x)+1))/150 
        
    return (2*math.pi/(x*math.log(x)+1))/100 


#Makes the Galaxy construct. There may be a better Pythonic way... 
def Make_Galaxy(Rings):
    
    Clouds,angles = [],[]
    
    #This loop generates the number of clouds per Ring. The values are
    #stored in a list and referred to in the loop that makes the Galaxy
    for i in range(2,Rings+2,1):
        Cloud_num.append(round(Cloud_Maker(i)))
    for i in range(len(Cloud_num)):
        if i == 0:
            Ring_Velocity.append(Ring_Velocity_Maker(1))
        else:
            Ring_Velocity.append(Ring_Velocity_Maker(i))
    


    for i in range(Rings):
        for j in range(Cloud_num[i]):
            cloud_size = 2*math.pi/Cloud_num[i]
            cloud_PA = 2*math.pi/Cloud_num[i]*j #the (initial/current) position angle of the cloud
            Clouds.append([cloud_PA,0,'black',cloud_size]) # loop creates a cloud list (a Ring) with a smaller list of attributes
            angles.append(cloud_PA)
            
        Galaxy.append(Clouds)  #appends a newly made Ring
        Cloud_angle_template.append(angles) #a lists of angles for each cell of the ring
        Clouds = []           #This cloud list is temporary so it is reset
        angles = []

        
    return()

#plots the Galaxy 
def Render_Galaxy(index):
    
    fig, (ax1) = plt.subplots(1,constrained_layout=True,figsize=(10,10),sharex=False, sharey=False)
    fig.suptitle('Galaxy Prototype')
    plt.sca(ax1)
    ax1.set_facecolor('#000000')

    x_coords,y_coords,colors = [],[],[]
            
    for i in range(len(Galaxy)):
        for j in range(len(Galaxy[i])):
            cloud_PA = Galaxy[i][j][theta]
            x_coords.append((i+1)*math.cos(cloud_PA))
            y_coords.append((i+1)*math.sin(cloud_PA))
            colors.append(Galaxy[i][j][color_])
            
    ax1.scatter(x_coords,y_coords,marker='o',color=colors,s=1)  
    plt.savefig('galaxy_'+str(index)+'.png')          
    plt.close(fig)
            
    return  



def Initialize_Galaxy():
    
    #for i in range(len(Galaxy)):
        #find_angle = getIndex.bisect_right(Cloud_angle_template[i],math.pi/2)
        #Galaxy[i][find_angle][color_] = 'white'
        #for j in range(len(Galaxy[i])):
           # Galaxy[i][find_angle][age] = 1
    for i in range(len(Galaxy)):
        for j in range(len(Galaxy[i])):
            rng.seed()
            if rng.random() < .001:
                Galaxy[i][j][age] = 1
                Galaxy[i][j][color_] = 'white'
                        
                
    return ()


def Rotate_Galaxy():
    
    for i in range(len(Galaxy)):
        for j in range(len(Galaxy[i])):
            if Galaxy[i][j][theta] + Ring_Velocity[i] > 2*math.pi:
                Galaxy[i][j][theta] = Galaxy[i][j][theta] + Ring_Velocity[i] - 2*math.pi
            else:    
                Galaxy[i][j][theta] += Ring_Velocity[i]  
            #print(i,j,Ring_Velocity[i],2*math.pi/Cloud_num[i])
    return
    
def Update_Galaxy():
    
    triggered_cells = []
    
    for i in range(len(Galaxy)):
        for j in range(len(Galaxy[i])):
            if Galaxy[i][j][age] == 1 and i > 0 and i < len(Galaxy)-1:
                triggered_cells.append(SPFS(i,j))
            if Galaxy[i][j][age] == 0:
                pass
            else:
                if Galaxy[i][j][age] > 15:
                    Galaxy[i][j][age] = 0
                    Galaxy[i][j][color_] ='black'
                elif Galaxy[i][j][age] == 1:
                     Galaxy[i][j][age] += 1   
                     Galaxy[i][j][color_] ='White'
                elif Galaxy[i][j][age] > 1 and Galaxy[i][j][age] < 4:
                    Galaxy[i][j][color_] = 'purple' 
                    Galaxy[i][j][age] += 1    
                elif Galaxy[i][j][age] >3 and Galaxy[i][j][age] < 11:
                    Galaxy[i][j][color_] = 'orange' 
                    Galaxy[i][j][age] += 1    
                elif Galaxy[i][j][age] > 10 and Galaxy[i][j][age] < 16:
                    Galaxy[i][j][color_] = 'red'   
                    Galaxy[i][j][age] += 1 
    
    if triggered_cells:                
        for k in range(len(triggered_cells)):
            for l in range(len(triggered_cells[k])):
                ring = triggered_cells[k][l][0]
                cell = triggered_cells[k][l][1]
                Galaxy[ring][cell][age] = 1
                Galaxy[ring][cell][color_] = 'white'

    
    return()


def SPFS(current_ring, current_cell):

    total_cells = Cloud_num[current_ring]
    total_cells_outer_ring = Cloud_num[current_ring+1]
    total_cells_inner_ring = Cloud_num[current_ring-1]
    change_list = []
    age_throttle = [1]

    
    if current_ring > 0 and current_ring < len(Galaxy):
        
        rng.seed()
        if rng.random() < .4*starforming_chance:
            if Galaxy[current_ring][(current_cell+1) % total_cells][age] not in age_throttle:
                change_list.append([current_ring,(current_cell+1) % total_cells])
        rng.seed()
        if rng.random() < .4*starforming_chance:
            if Galaxy[current_ring][(current_cell-1) % total_cells][age] not in age_throttle:
                change_list.append([current_ring,(current_cell-1)]) 
                
        
        
        rng.seed()
        if rng.random() < .8*starforming_chance:
            j_inner_index = getIndex.bisect_left(Cloud_angle_template[current_ring-1],Galaxy[current_ring][current_cell][theta])
            if j_inner_index > Cloud_num[current_ring-1]-1:
                j_inner_index =  -1 #need to think about this!
            if Galaxy[current_ring-1][j_inner_index][age] not in age_throttle:
                change_list.append([current_ring-1,(j_inner_index)])
            
        rng.seed()
        if rng.random() < .8*starforming_chance:
            j_inner_index = getIndex.bisect_left(Cloud_angle_template[current_ring-1],Galaxy[current_ring][current_cell][theta])
            if j_inner_index > Cloud_num[current_ring-1]-1:
                j_inner_index =  -1 #need to think about this!
            if Galaxy[current_ring-1][(j_inner_index-1) % total_cells_inner_ring][age] not in age_throttle:
                change_list.append([current_ring-1,(j_inner_index)])
        
        
        
        
        rng.seed()
        if rng.random() < .3*starforming_chance:
            j_outer_index = getIndex.bisect_left(Cloud_angle_template[current_ring+1],Galaxy[current_ring][current_cell][theta]) 
            if j_outer_index > Cloud_num[current_ring+1]-1:
                j_outer_index =  -1 #need to think about this!
            if Galaxy[current_ring+1][j_outer_index][age] not in age_throttle:
                change_list.append([current_ring+1,j_outer_index])
      
        rng.seed()    
        if rng.random() < .3*starforming_chance:
            j_outer_index = getIndex.bisect_left(Cloud_angle_template[current_ring+1],Galaxy[current_ring][current_cell][theta]) 
            if j_outer_index > Cloud_num[current_ring+1]-1:
                j_outer_index =  -1 #need to think about this!
            if Galaxy[current_ring+1][(j_outer_index+1) % total_cells_outer_ring][age] not in age_throttle:
                change_list.append([current_ring+1,(j_outer_index+1) % total_cells_outer_ring])  
                
        rng.seed()    
        if rng.random() < .3*starforming_chance:
            j_outer_index = getIndex.bisect_left(Cloud_angle_template[current_ring+1],Galaxy[current_ring][current_cell][theta]) 
            if j_outer_index > Cloud_num[current_ring+1]-1:
                j_outer_index =  -1 #need to think about this!
            if Galaxy[current_ring+1][(j_outer_index-1) % total_cells_outer_ring][age] not in age_throttle:
                change_list.append([current_ring+1,(j_outer_index-1) % total_cells_outer_ring])     
            

    return(change_list)

def main():

    Make_Galaxy(Rings)
    Initialize_Galaxy()
    Render_Galaxy(0)
    for i in range(1,Iterations):
        Update_Galaxy()
        Rotate_Galaxy()
        if i % 10 == 0:
            Render_Galaxy(i)

    return()

#This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
    



        