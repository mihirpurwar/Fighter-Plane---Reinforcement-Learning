import time
import initialize_grid
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt22
import math
from parameters import Parameters as PARA


def distance_diff(reference, target):
        x0 = reference[0]
        y0 = reference[1]
        x1 = target[0]
        y1 = target[1]    
        dist = math.sqrt(math.pow((x0-x1),2) + math.pow((y0-y1),2))
        return dist


iteration = PARA.iterationCount
prey_count = PARA.fighterCount

initialize_grid.singleton_world = initialize_grid.World()


plt.axis([0,PARA.visibleBoundaryX,0,PARA.visibleBoundaryY])
plt.ion()
temp = 0

prey_position = {}
food_position =[]

#while(True):
while(temp < iteration):
    preys = initialize_grid.singleton_world.preys
    food = initialize_grid.singleton_world.food
    obstacles = initialize_grid.singleton_world.obstacles

    plt.xlim([0,PARA.visibleBoundaryX])
    plt.ylim([0,PARA.visibleBoundaryY])

    for obstacle in obstacles:
        plt.scatter(obstacle[0], obstacle[1], color='c')
        
    for f in food:
        #if f.id == 0:
            #print("E:" + str(f.energy))
        f.move()
        food_position.append(f.position)
        #plt.scatter(f.position[0], f.position[1], color='r')
        plt.arrow(f.position[0], f.position[1], f.velocity[0]*2, f.velocity[1]*2, head_width=1, color='r')
        
    for prey in preys:
        '''
        if prey.id == 0:
            A = prey.qlearn.Qtable
            f = open('files0/text.txt','w')
            for i in A:
                temp = '['
                for j in range(len(i)):
                    if j != len(i)-1:
                        temp = temp + str(i[j]) + ','
                    else:
                        temp = temp + str(i[j]) + '] : ['
            
                for j in range(len(A[i])):
                    if j != len(A[i])-1:
                        temp = temp + str(A[i][j]) + ','
                    else:
                        temp = temp + str(A[i][j]) + ']\n'

                f.write(temp)
            f.close()
        '''
        if prey.id in prey_position.keys():
            prey_position[prey.id].append(prey.position)
        else:
            prey_position[prey.id] = [prey.position]
        '''
        if prey.id == 12:
            print('speed: '+ str(prey.speed))
        '''
        prey.move()
        plt.arrow(prey.position[0], prey.position[1], prey.velocity[0]*2, prey.velocity[1]*2, head_width=0.5)

    plt.pause(0.01)
    plt.clf()
    print(temp)
    temp += 1

#print(food_position)
#print(prey_position)

y = range(iteration)
'''
x = {}

for i in range(iteration):
     x[0].append(distance_diff(food_position[i], prey_position[3][i]))
     x[1].append(distance_diff(food_position[i], prey_position[6][i]))
     x[2].append(distance_diff(food_position[i], prey_position[9][i]))
    
plt22.plot(y,x[0])
plt22.plot(y,x[1])
plt22.plot(y,x[2])
'''
'''
x = {}
for i in range(iteration):
    for j in range(prey_count):
        if j in x.keys():
            x[j].append(distance_diff(food_position[i], prey_position[j][i]))
        else:
            x[j] = [distance_diff(food_position[i], prey_position[j][i])]

for i in range(prey_count):
    plt22.plot(y,x[i])


x1=[]
for i in range(iteration):
    t1 = 0
    for j in range(prey_count):
        if j != 25:
            t1 = t1 + (distance_diff(prey_position[15][i], prey_position[j][i]))
    x1.append(t1/29)


x2=[]
for i in range(iteration):
    t2 = 0
    k = prey_count
    for j in range(k):
        for l in range(j+1,k):
            if distance_diff(prey_position[j][i], prey_position[l][i]) < 0.5:
                t2 = t2 + 1
    x2.append(t2)
    
plt22.subplot(2, 1, 1)
plt22.plot(y,x1)
plt22.subplot(2, 1, 2)
plt22.plot(y,x2)

plt22.show()
'''
