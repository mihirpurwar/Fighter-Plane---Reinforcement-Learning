from random import uniform

class PreyState:
    # Different states/senarios in which a prey(fish) experience.
    # Assigning numerical value to different states (for simplicity).
    PredatorDetected = 0
    PredatorNotDetected = 1
    FoodDetected = 2
    FoodNotDetected = 3
    PreyInRepulsion = 4
    PreyInAttraction = 5
    PreyInOrientation = 6


class PreyAction:
    # Differnt actions a prey will perform according to their state.
    # Assigning numerical value to actions.
    #EatFood = 0
    MoveTowardsFood = 0
    MoveForward = 1
    MoveAwayFromPrey = 2
    MoveTowardsPrey = 3
    OrientWithPrey = 4
    MoveAwayFromPredator = 5


class Prey_QLearn:

    def __init__(self, alpha=0.2, gamma=0.9):
        self.Qtable = {}
        # Table is a dictionary with a mapping from states to actions, where one state can map to multiple actions.
        self.alpha = alpha
        self.gamma = gamma
        self.prev_state = None
        self.prev_max_index = None
        self.current_action = None
        self.chosen_action = None
        self.setQtable()        # Initialise Q-table.

    def setQtable(self):
        # Key -> different combination of state (type -> list).
        # Value -> list of actions followed by their Q-values.
        self.Qtable[(PreyState.FoodDetected, PreyState.PredatorDetected)] = [PreyAction.MoveTowardsFood, self.rand(), PreyAction.MoveAwayFromPredator, self.rand()]
        self.Qtable[(PreyState.FoodNotDetected, PreyState.PredatorDetected)] = [PreyAction.MoveAwayFromPredator, self.rand()]
        
        self.Qtable[(PreyState.FoodDetected, PreyState.PredatorNotDetected)] = [PreyAction.MoveTowardsFood, self.rand(), PreyAction.MoveForward, self.rand()]
        self.Qtable[(PreyState.FoodNotDetected, PreyState.PredatorNotDetected)] = [PreyAction.MoveForward, self.rand()]
                   
        self.Qtable[(PreyState.FoodDetected, PreyState.PredatorDetected, PreyState.PreyInAttraction)] = [PreyAction.MoveTowardsFood, self.rand(), PreyAction.MoveTowardsPrey, self.rand(), PreyAction.MoveAwayFromPredator, self.rand()]                 
        self.Qtable[(PreyState.FoodDetected, PreyState.PredatorNotDetected, PreyState.PreyInAttraction)] = [PreyAction.MoveTowardsFood, self.rand(), PreyAction.MoveTowardsPrey, self.rand()]                 

        self.Qtable[(PreyState.FoodNotDetected, PreyState.PredatorDetected, PreyState.PreyInAttraction)] = [PreyAction.MoveTowardsPrey, self.rand(), PreyAction.MoveAwayFromPredator, self.rand()]                 
        self.Qtable[(PreyState.FoodNotDetected, PreyState.PredatorNotDetected, PreyState.PreyInAttraction)] = [PreyAction.MoveTowardsPrey, self.rand()]                 

        self.Qtable[(PreyState.FoodDetected, PreyState.PredatorDetected, PreyState.PreyInOrientation)] = [PreyAction.MoveTowardsFood, self.rand(), PreyAction.OrientWithPrey, self.rand(), PreyAction.MoveAwayFromPredator, self.rand()]                 
        self.Qtable[(PreyState.FoodDetected, PreyState.PredatorNotDetected, PreyState.PreyInOrientation)] = [PreyAction.MoveTowardsFood, self.rand(), PreyAction.OrientWithPrey, self.rand()]                 

        self.Qtable[(PreyState.FoodNotDetected, PreyState.PredatorDetected, PreyState.PreyInOrientation)] = [PreyAction.OrientWithPrey, self.rand(), PreyAction.MoveAwayFromPredator, self.rand()]                 
        self.Qtable[(PreyState.FoodNotDetected, PreyState.PredatorNotDetected, PreyState.PreyInOrientation)] = [PreyAction.OrientWithPrey, self.rand()]                 

        self.Qtable[(PreyState.FoodDetected, PreyState.PredatorDetected, PreyState.PreyInRepulsion)] = [PreyAction.MoveTowardsFood, self.rand(), PreyAction.MoveAwayFromPrey, self.rand(), PreyAction.MoveAwayFromPredator, self.rand()]                 
        self.Qtable[(PreyState.FoodDetected, PreyState.PredatorNotDetected, PreyState.PreyInRepulsion)] = [PreyAction.MoveTowardsFood, self.rand(), PreyAction.MoveAwayFromPrey, self.rand()]                 

        self.Qtable[(PreyState.FoodNotDetected, PreyState.PredatorDetected, PreyState.PreyInRepulsion)] = [PreyAction.MoveAwayFromPrey, self.rand(), PreyAction.MoveAwayFromPredator, self.rand()]                 
        self.Qtable[(PreyState.FoodNotDetected, PreyState.PredatorNotDetected, PreyState.PreyInRepulsion)] = [PreyAction.MoveAwayFromPrey, self.rand()]                 

        self.Qtable[(PreyState.FoodDetected, PreyState.PredatorDetected, PreyState.PreyInRepulsion, PreyState.PreyInOrientation, PreyState.PreyInAttraction)] = [PreyAction.MoveTowardsFood, self.rand(), PreyAction.MoveAwayFromPrey, self.rand(), PreyAction.MoveTowardsPrey, self.rand(),PreyAction.OrientWithPrey, self.rand(), PreyAction.MoveAwayFromPredator, self.rand()]                 
        self.Qtable[(PreyState.FoodDetected, PreyState.PredatorNotDetected, PreyState.PreyInRepulsion, PreyState.PreyInOrientation, PreyState.PreyInAttraction)] = [PreyAction.MoveTowardsFood, self.rand(), PreyAction.MoveAwayFromPrey, self.rand(), PreyAction.MoveTowardsPrey, self.rand(),PreyAction.OrientWithPrey, self.rand()]                 

        self.Qtable[(PreyState.FoodNotDetected, PreyState.PredatorDetected, PreyState.PreyInRepulsion, PreyState.PreyInOrientation, PreyState.PreyInAttraction)] = [PreyAction.MoveAwayFromPrey, self.rand(), PreyAction.MoveTowardsPrey, self.rand(),PreyAction.OrientWithPrey, self.rand(), PreyAction.MoveAwayFromPredator, self.rand()]                 
        self.Qtable[(PreyState.FoodNotDetected, PreyState.PredatorNotDetected, PreyState.PreyInRepulsion, PreyState.PreyInOrientation, PreyState.PreyInAttraction)] = [PreyAction.MoveAwayFromPrey, self.rand(), PreyAction.MoveTowardsPrey, self.rand(),PreyAction.OrientWithPrey, self.rand()]                 

        self.Qtable[(PreyState.FoodDetected, PreyState.PredatorDetected, PreyState.PreyInOrientation, PreyState.PreyInAttraction)] = [PreyAction.MoveTowardsFood, self.rand(), PreyAction.MoveTowardsPrey, self.rand(),PreyAction.OrientWithPrey, self.rand(), PreyAction.MoveAwayFromPredator, self.rand()]                 
        self.Qtable[(PreyState.FoodDetected, PreyState.PredatorNotDetected, PreyState.PreyInOrientation, PreyState.PreyInAttraction)] = [PreyAction.MoveTowardsFood, self.rand(), PreyAction.MoveTowardsPrey, self.rand(),PreyAction.OrientWithPrey, self.rand()]                 

        self.Qtable[(PreyState.FoodNotDetected, PreyState.PredatorDetected, PreyState.PreyInOrientation, PreyState.PreyInAttraction)] = [PreyAction.MoveTowardsPrey, self.rand(),PreyAction.OrientWithPrey, self.rand(),PreyAction.MoveAwayFromPredator, self.rand()]                 
        self.Qtable[(PreyState.FoodNotDetected, PreyState.PredatorNotDetected, PreyState.PreyInOrientation, PreyState.PreyInAttraction)] = [PreyAction.MoveTowardsPrey, self.rand(),PreyAction.OrientWithPrey, self.rand()]                 
          
        self.Qtable[(PreyState.FoodDetected, PreyState.PredatorDetected, PreyState.PreyInRepulsion, PreyState.PreyInAttraction)] = [PreyAction.MoveTowardsFood, self.rand(), PreyAction.MoveAwayFromPrey, self.rand(), PreyAction.MoveTowardsPrey, self.rand(), PreyAction.MoveAwayFromPredator, self.rand()]                 
        self.Qtable[(PreyState.FoodDetected, PreyState.PredatorNotDetected, PreyState.PreyInRepulsion,  PreyState.PreyInAttraction)] = [PreyAction.MoveTowardsFood, self.rand(), PreyAction.MoveAwayFromPrey, self.rand(), PreyAction.MoveTowardsPrey, self.rand()]                 

        self.Qtable[(PreyState.FoodNotDetected, PreyState.PredatorDetected, PreyState.PreyInRepulsion, PreyState.PreyInAttraction)] = [PreyAction.MoveAwayFromPrey, self.rand(), PreyAction.MoveTowardsPrey, self.rand(), PreyAction.MoveAwayFromPredator, self.rand()]                 
        self.Qtable[(PreyState.FoodNotDetected, PreyState.PredatorNotDetected, PreyState.PreyInRepulsion,  PreyState.PreyInAttraction)] = [PreyAction.MoveAwayFromPrey, self.rand(), PreyAction.MoveTowardsPrey, self.rand()]                 

        self.Qtable[(PreyState.FoodDetected, PreyState.PredatorDetected, PreyState.PreyInRepulsion, PreyState.PreyInOrientation)] = [PreyAction.MoveTowardsFood, self.rand(), PreyAction.MoveAwayFromPrey, self.rand(),PreyAction.OrientWithPrey, self.rand(), PreyAction.MoveAwayFromPredator, self.rand()]                 
        self.Qtable[(PreyState.FoodDetected, PreyState.PredatorNotDetected, PreyState.PreyInRepulsion,  PreyState.PreyInOrientation)] = [PreyAction.MoveTowardsFood, self.rand(), PreyAction.MoveAwayFromPrey, self.rand(), PreyAction.OrientWithPrey, self.rand()]                 

        self.Qtable[(PreyState.FoodNotDetected, PreyState.PredatorDetected, PreyState.PreyInRepulsion, PreyState.PreyInOrientation)] = [PreyAction.MoveAwayFromPrey, self.rand(),PreyAction.OrientWithPrey, self.rand(), PreyAction.MoveAwayFromPredator, self.rand()]                 
        self.Qtable[(PreyState.FoodNotDetected, PreyState.PredatorNotDetected, PreyState.PreyInRepulsion,  PreyState.PreyInOrientation)] = [PreyAction.MoveAwayFromPrey, self.rand(), PreyAction.OrientWithPrey, self.rand()]                 


    def choose_action(self, current_state):
        if len(current_state) == 1:
            self.current_action = self.Qtable.get((current_state[0]))
        else:
            self.current_action = self.Qtable.get(tuple(current_state))

        if self.current_action is None:
            return None

        # Iterating through current action and finding action with max value
        max_qvalue = -1
        max_index = 0
        index = 0
        while index < len(self.current_action)-1:
            if max_qvalue < self.current_action[index+1]:
                max_index = index
                max_qvalue = self.current_action[index+1]
            index += 2
        self.prev_state = current_state
        self.prev_max_index = max_index
        self.chosen_action = self.current_action[max_index]
        # Return best action and it's q weight
        return self.current_action[max_index], self.current_action[max_index+1]



# --- Perform Q Learning
    def doQLearning(self, reward, state):

        
        if self.prev_state is None:
            return

        prev_state = self.prev_state
        prev_action = self.current_action
        prev_max_index = self.prev_max_index

        oldq = prev_action[prev_max_index+1]

        newqtemp = self.choose_action(state)    
        newq = newqtemp[1]

        oldq += self.alpha*(reward+(self.gamma * newq)-oldq)
        prev_action[prev_max_index+1] = oldq    
        self.Qtable[tuple(prev_state)] = prev_action

       
    def rand(self):
        return uniform(0.0, 1.0)
