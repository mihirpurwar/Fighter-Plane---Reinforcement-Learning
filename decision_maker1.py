import random
import math
from prey_elements import *
import initialize_grid
from parameters import Parameters as PARA


def distance_calc(reff,target):
    distance = math.sqrt(math.pow((reff[0]-target[0]),2)+math.pow((reff[1]-target[1]),2))
    return distance

class Food:

    def __init__(self, c1, c2, v1, v2, energy, z):
        self.position = [c1, c2]
        self.energy = energy
        self.id = z
        self.velocity=[v1, v2]
        self.turningAngle = 8
        self.speed = 0.5
        self.normalize_value = PARA.normalizeFactor
        

    def move(self):
        if PARA.boundary_check:
            self.boundaryCheck()
        da = [0,0]
        dist = random.randint(15,85)
        #da[0] = da[0] + (random.uniform(10,90) - self.position[0])/dist
        #da[1] = da[1] + (random.uniform(10,90) - self.position[1])/dist
        da[0] = da[0] + (random.randint(10,290) - self.position[0])/dist
        da[1] = da[1] + (random.randint(10,290) - self.position[1])/dist
        self.calcFinalRes(da)

    def calcFinalRes(self,da):
        if da[0] > 0:
            di_angle = math.degrees(math.atan(da[1]/da[0]))
        else:
            di_angle = 180 + math.degrees(math.atan(da[1]/da[0]))
#        di_angle = math.degrees(math.atan(da[1]/da[0]))
            
        if self.velocity[0] > 0:
            vi_angle = math.degrees(math.atan(self.velocity[1]/self.velocity[0]))
        else:
            vi_angle = 180 + math.degrees(math.atan(self.velocity[1]/self.velocity[0]))
        
        velocity = [0,0]
        angle_diff = di_angle - vi_angle
        if abs(angle_diff) < self.turningAngle:
            velocity = da
        else:
            if angle_diff < 0:
                angle = vi_angle - self.turningAngle
            else:
                angle = vi_angle + self.turningAngle
            
            velocity[0] = math.cos(math.radians(angle))
            velocity[1] = math.sin(math.radians(angle))
            
        temp = math.sqrt(velocity[0]**2 + velocity[1]**2)
        
        velocity[0] = velocity[0] / temp
        velocity[1] = velocity[1] / temp
        position = [0,0]
        position[0] = (self.position[0] + velocity[0] * self.speed) % self.normalize_value
        position[1] = (self.position[1] + velocity[1] * self.speed) % self.normalize_value
        initialize_grid.singleton_world.move_animat(self, position, velocity)

    def boundaryCheck(self):
        x = (self.velocity[0]*2)+self.position[0]
        y = (self.velocity[1]*2)+self.position[1]
        if x<=0 or x>=PARA.totalBoundaryX or y<=0 or y>=PARA.totalBoundaryY:
            self.velocity[0] = (-1)*self.velocity[0]
            self.velocity[1] = (-1)*self.velocity[1]
        
class Prey:

    def __init__(self, c1, c2, v1, v2, energy, z):
        self.qlearn = Prey_QLearn()
        self.position = [c1, c2]
        self.velocity = [v1, v2]
        self.energy = energy
        self.maxspeed = 0.4
        self.speed = self.maxspeed
        self.id = z
        self.turningAngle = 6
        self.hunger_threshold = 70
        self.normalize_value = PARA.normalizeFactor
        self.preyRepulsionRange = 3
        self.preyOrientationRange = 18
        self.preyAttractionRange = 35
        self.preyObstacleRange = 10
        self.preyFoodRange = 1500
        self.preySpeedRange = 8

    def get_reward(self,x):
        if x == 1:
            return 1.75
        elif x == 2:
            return 1
        elif x == 3:
            return 0.25
        elif x == 4:
            return -1
            
    def sense_state(self, preys_repulsion,preys_orientation,preys_attraction,obstacles,foods):
            list_state = []
            
            if len(foods)>0:
                list_state.append(PreyState.FoodDetected)
            else:
                list_state.append(PreyState.FoodNotDetected)
            if len(obstacles)>0:
                list_state.append(PreyState.PredatorDetected)
            else:
                list_state.append(PreyState.PredatorNotDetected)
            if len(preys_repulsion)>0:
                list_state.append(PreyState.PreyInRepulsion)
            if len(preys_orientation) >0:
                list_state.append(PreyState.PreyInOrientation)
            if len(preys_attraction)>0:
                list_state.append(PreyState.PreyInAttraction)

            return list_state


    def move(self):
        all_range_preys = initialize_grid.singleton_world.around_point(self.position, self.velocity, [self.preyAttractionRange, self.preyOrientationRange, self.preyRepulsionRange, self.preySpeedRange],isPrey=True)
        preys_repulsion = all_range_preys[2]        
        preys_orientation = all_range_preys[1]        
        preys_attraction = all_range_preys[0]     
        
        obstacles = initialize_grid.singleton_world.around_point(self.position,2, self.preyObstacleRange)

        foods = initialize_grid.singleton_world.around_point(self.position,2, self.preyFoodRange,isFood=True)

        currentState = self.sense_state(preys_repulsion,preys_orientation,preys_attraction,obstacles,foods)

        #if self.id == 0:
            #print("Here: " + str(currentState))
            #print("energy:"+str(self.energy))

        self.qlearn.choose_action(currentState)
        if PARA.record_data:
            self.recordData(currentState)
        if PARA.boundary_check:
            self.boundaryCheck()
        if self.qlearn.chosen_action == PreyAction.MoveTowardsFood:
            #print('hey')
            if len(foods)!=0:
                self.moveTowardsFood(foods)
                if(self.energy < self.hunger_threshold):
                    GotFood = initialize_grid.singleton_world.foodHere(self.position,foods)
                    if GotFood: #
                        self.energy += 5            
                    if currentState[0] == PreyState.FoodDetected and GotFood:
                        self.qlearn.doQLearning(self.get_reward(1), currentState)
                    else:
                        self.qlearn.doQLearning(self.get_reward(2), currentState)
            else:
                self.moveForward()
        elif self.qlearn.chosen_action == PreyAction.MoveAwayFromPredator:
            if len(obstacles) != 0:
                self.moveAwayFromPred(obstacles)
                self.qlearn.doQLearning(self.get_reward(1),currentState)
            else:
                self.moveForward()
                self.qlearn.doQLearning(self.get_reward(4),currentState)
        elif self.qlearn.chosen_action == PreyAction.MoveAwayFromPrey:
            self.moveAwayFromPrey(preys_repulsion,preys_orientation,preys_attraction)
            if preys_repulsion!=0:
                self.qlearn.doQLearning(self.get_reward(1),currentState)
            else:
                self.qlearn.doQLearning(self.get_reward(4),currentState)
        elif self.qlearn.chosen_action == PreyAction.OrientWithPrey:
            self.orientWithPrey(preys_orientation,preys_attraction)
            if len(preys_orientation)>0:
                self.qlearn.doQLearning(self.get_reward(1),currentState)
            else:
                self.qlearn.doQLearning(self.get_reward(4),currentState)
        elif self.qlearn.chosen_action == PreyAction.MoveTowardsPrey:
            self.orientWithPrey(preys_orientation, preys_attraction) 
            if len(preys_attraction) > 0:
                self.qlearn.doQLearning(self.get_reward(1),currentState)
            else:
                self.qlearn.doQLearning(self.get_reward(4),currentState)
        else:
            self.moveForward()
            self.qlearn.doQLearning(self.get_reward(3),currentState)

    def moveForward(self):
        position = [0,0]
        position[0] = (self.position[0] + self.velocity[0]*self.speed) % self.normalize_value
        position[1] = (self.position[1] + self.velocity[1]*self.speed) % self.normalize_value
        initialize_grid.singleton_world.move_animat(self, position, self.velocity)
    
    def moveTowardsFood(self,foods):
        da = [0,0]
        for food in foods:
            dist = distance_calc(food.position,self.position)
            da[0] = da[0] + (food.position[0] - self.position[0])/dist
            da[1] = da[1] + (food.position[1] - self.position[1])/dist
        self.calcFinalRes(da)

    def moveAwayFromPred(self,obstacles):
        dr = [0,0]
        for obstacle in obstacles:
            dist = distance_calc(obstacle,self.position)
            dr[0] = dr[0] + (obstacle[0] - self.position[0])/dist
            dr[1] = dr[1] + (obstacle[0] - self.position[1])/dist
        self.calcFinalRes([-dr[0],-dr[1]])
        
    def moveAwayFromPrey(self,preys_repulsion,preys_orientation,preys_attraction):
        if len(preys_attraction) + len(preys_orientation) + len(preys_repulsion) == 0:
            self.moveForward()
        elif len(preys_repulsion)!=0:
            dr = [0,0]
            for prey in preys_repulsion:
                dist = distance_calc(prey.position,self.position)
                dr[0] += (prey.position[0] - self.position[0])/dist
                dr[1] += (prey.position[1] - self.position[1])/dist
            self.calcFinalRes([-dr[0],-dr[1]])
        else:
            do = [0,0]
            da = [0,0]
            for prey in preys_orientation:
                dist = distance_calc(prey.position,self.position)
                do[0] += (prey.position[0] - self.position[0])/dist
                do[1] += (prey.position[1] - self.position[1])/dist
            for prey in preys_attraction:
                dist = distance_calc(prey.position,self.position)
                da[0] += (prey.position[0] - self.position[0])/dist
                da[1] += (prey.position[1] - self.position[1])/dist
            if len(preys_orientation)==0:
                self.calcFinalRes([-da[0],-da[1]])
            elif len(preys_attraction)==0:
                self.calcFinalRes([-do[0],-do[1]])
            else:
                self.calcFinalRes([-0.5*(do[0]+da[0]), -0.5*(do[1]+da[1])])
                
    def orientWithPrey(self,preys_orientation,preys_attraction):
        if len(preys_orientation)+len(preys_attraction) == 0:
            self.moveForward()
        else:
            do = [0,0]
            da = [0,0]
            for prey in preys_orientation:
                do[0] += (prey.velocity[0])/math.sqrt(prey.velocity[0]**2+prey.velocity[1]**2)
                do[1] += (prey.velocity[1])/math.sqrt(prey.velocity[0]**2+prey.velocity[1]**2)
            for prey in preys_attraction:
                dist = distance_calc(prey.position,self.position)
                da[0] += (prey.position[0] - self.position[0])/dist
                da[1] += (prey.position[1] - self.position[1])/dist
            if len(preys_orientation)==0:
                self.calcFinalRes(da)
            elif len(preys_attraction)==0:
                self.calcFinalRes(do)
            else:
                self.calcFinalRes([0.5*(do[0]+da[0]), 0.5*(do[1]+da[1])])


    def calcFinalRes(self,da):
        if da[0] > 0:
            di_angle = math.degrees(math.atan(da[1]/da[0]))
        else:
            di_angle = 180 + math.degrees(math.atan(da[1]/da[0]))
#        di_angle = math.degrees(math.atan(da[1]/da[0]))
            
        if self.velocity[0] > 0:
            vi_angle = math.degrees(math.atan(self.velocity[1]/self.velocity[0]))
        else:
            vi_angle = 180 + math.degrees(math.atan(self.velocity[1]/self.velocity[0]))
        
        velocity = [0,0]
        angle_diff = di_angle - vi_angle
        if abs(angle_diff) < self.turningAngle:
            velocity = da
        else:
            if angle_diff < 0:
                angle = vi_angle - self.turningAngle
            else:
                angle = vi_angle + self.turningAngle
            
            velocity[0] = math.cos(math.radians(angle))
            velocity[1] = math.sin(math.radians(angle))
            
        temp = math.sqrt(velocity[0]**2 + velocity[1]**2)
        
        velocity[0] = velocity[0] / temp
        velocity[1] = velocity[1] / temp
        position = [0,0]
        position[0] = (self.position[0] + velocity[0] * self.speed) % self.normalize_value
        position[1] = (self.position[1] + velocity[1] * self.speed) % self.normalize_value
        initialize_grid.singleton_world.move_animat(self, position, velocity)


    def boundaryCheck(self):
        x = (self.velocity[0]*2)+self.position[0]
        y = (self.velocity[1]*2)+self.position[1]
        if x<=0 or x>=PARA.totalBoundaryX or y<=0 or y>=PARA.totalBoundaryY:
            self.velocity[0] = (-1)*self.velocity[0]
            self.velocity[1] = (-1)*self.velocity[1]                    


    def recordData(self,C):
        A = self.qlearn.Qtable
        f_destination0 = 'files0/qtable_'+str(self.id)+'.txt'
        file0 = open(f_destination0,'w')
        for i in A:
            temp = '('
            for j in range(len(i)):
                if j != len(i)-1:
                    temp = temp + str(i[j]) + ','
                else:
                    temp = temp + str(i[j]) + ') : ['
            
            for j in range(len(A[i])):
                if j != len(A[i])-1:
                    temp = temp + str(A[i][j]) + ','
                else:
                    temp = temp + str(A[i][j]) + ']\n'

            file0.write(temp)
        file0.close()
        f_destination1 = 'files1/currentState_'+str(self.id)+'.txt'
        file1 = open(f_destination1,'a')
        A = C
        temp = '('
        for j in range(len(A)):
            if j != len(A)-1:
                temp = temp + str(A[j]) + ','
            else:
                temp = temp + str(A[j]) + ') - ['+str(self.qlearn.chosen_action)+']\n'
        file1.write(temp)
        file1.close()
