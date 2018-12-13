from random import randint
import random
import math
from parameters import Parameters as PARA
if PARA.Q_Learning and PARA.speed_optimization:
    from decision_maker import Prey
    from decision_maker import Food
    print('c-1')
elif PARA.Q_Learning and not PARA.speed_optimization:
    from decision_maker1 import Prey
    from decision_maker1 import Food
    print('c-2')
elif not PARA.Q_Learning and not PARA.speed_optimization:
    from decision_maker2 import Prey
    from decision_maker2 import Food
    print('c-3')

def distance_diff(reference, target):
        x0 = reference[0]
        y0 = reference[1]
        x1 = target[0]
        y1 = target[1]    
        dist = math.sqrt(math.pow((x0-x1),2) + math.pow((y0-y1),2))
        
        return dist

class World:

    def __init__(self):
        #self.grid = position_grid
        self.preys = []
        self.predators = []
        self.food = []
        self.obstacles = []
        self.width = PARA.initialBoundaryX
        self.height = PARA.initialBoundaryY
        self.foodCount = PARA.enemyCount
        self.preyCount = PARA.fighterCount
        self.obstacleCount = PARA.obstacleNumber
        self.__init_prey(self.preyCount)
        self.__set_food()
        self.__set_obstacle()

    def __set_food(self):
        for i in range(self.foodCount):
            coord = [random.uniform(0, self.height-1), random.uniform(0, self.width-1)]
            velocity = [random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)]
            temp = math.sqrt(velocity[0]**2 + velocity[1]**2)
            velocity[0] = velocity[0] / temp
            velocity[1] = velocity[1] / temp
            #energy = randint(150,220)
            energy = 99999999
            food = Food(coord[0], coord[1], velocity[0], velocity[1], energy, i)
            self.food.append(food)

    def __set_obstacle(self):
            for i in range(self.obstacleCount):
                #coord = [random.uniform(0, self.height-1), random.uniform(0, self.width-1)]
                coord = [randint(1, self.height-1), randint(1, self.width-1)]
                self.obstacles.append(coord)
                
    def __init_prey(self,count):
        for i in range(count):
            coord = [random.uniform(0.0, self.height-1), random.uniform(0.0, self.width-1)]
            velocity = [random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)]
            temp = math.sqrt(velocity[0]**2 + velocity[1]**2)
            velocity[0] = velocity[0] / temp
            velocity[1] = velocity[1] / temp
            energy = randint(0,100)
            prey = Prey(coord[0], coord[1], velocity[0], velocity[1], energy, i)
            self.preys.append(prey)
    
    def move_animat(self, animat, new_coord, new_velocity):
        animat.position = new_coord
        animat.velocity = new_velocity
        animat.energy = animat.energy - 1
    
    def around_point(self, coord, velo, view_range, isPrey = False, isFood = False):
        ranged_animats = []     # Will contain animats in order of ranges.
        if isPrey and not isFood:
            attr = []
            orit = []
            repl = []
            speed = []
            for prey in self.preys:
                distance = distance_diff(coord, prey.position)
                temp1 =[coord[0]+(velo[0]*2), coord[1]+(velo[1]*2)]
                dist1 = distance_diff(temp1, prey.position)
                if dist1 < view_range[3] and dist1!=0:
                    speed.append(prey)
                if distance < view_range[0] and distance > view_range[1] and distance!=0:
                    attr.append(prey)
                elif distance < view_range[1] and distance > view_range[2] and distance!=0:
                    orit.append(prey)
                elif distance < view_range[2] and distance!=0:
                    repl.append(prey)
            ranged_animats = [attr, orit, repl, speed]
        elif not isPrey and not isFood:
            for obstacle in self.obstacles:
                distance = distance_diff(coord, obstacle)
                if distance < view_range and distance!=0:
                    ranged_animats.append(obstacle)
        elif not isPrey and isFood:
            for food in self.food:
                distance = distance_diff(coord,food.position)
                if distance < view_range and distance!=0:
                    ranged_animats.append(food)
        return ranged_animats

    def foodHere(self,position,foods):
        for f in foods:
            if f.energy >= 5:
                #print('hey')
                if distance_diff(position,f.position) < 1:
                    f.energy = f.energy - 5
                    return True
                #self.food.remove(f)
                #---self.food.append([random.uniform(0, self.height-1), random.uniform(0, self.width-1)])
                #return True
            else:
                temp = f.id
                self.food.remove(f)
                coord = [random.uniform(0, self.height-1), random.uniform(0, self.width-1)]
                energy = randint(150,220)
                velocity = [random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)]
                temp = math.sqrt(velocity[0]**2 + velocity[1]**2)
                velocity[0] = velocity[0] / temp
                velocity[1] = velocity[1] / temp
                food = Food(coord[0], coord[1], velocity[0], velocity[1], energy, temp)
                self.food.append(food)
        return False

singleton_world = None  
