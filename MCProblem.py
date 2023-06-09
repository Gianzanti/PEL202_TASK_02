from typing import Literal, Tuple, Union

class State():
    ''' Class that represents the state of the problem '''
    def __init__(self, miss:int, cann:int, boat:Literal['L', 'R'], heuristic:float = 0.00) -> None:
        self.miss = miss
        self.cann = cann
        self.boat = boat
        self.heuristic = heuristic
    
    def __repr__(self):
        ''' Returns a string representation of the state, mainly used to hash the state'''
        return f"({self.miss}_{self.cann}_{self.boat})"

    def __eq__(self, other): 
        ''' Returns true if the state is equal to the other state.
            Used to compare states in the frontier and reached sets'''
        
        if not isinstance(other, State):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.miss == other.miss and self.cann == other.cann and self.boat == other.boat

class Action():
    ''' Class that represents the actions of the problem'''
    def __init__(self, miss:int, cann:int, direction:Literal['L', 'R'], cost:float=0.00) -> None:
        self.miss = miss
        self.cann = cann
        self.direction = direction
        self.cost = cost
        # self.heuristic = heuristic

    def __repr__(self):
        ''' Returns a string representation of the state, mainly used to hash the state'''
        return f"({self.miss}_{self.cann}_{self.direction})"

class Node():
    ''' Class that represents the node of the solution problem'''
    def __init__(self, state:State, parent:Union['Node', None]=None, action:Union[Action, None]=None, cost:float=0.00) -> None:
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.priority = 0.00

    def __lt__(self, other: 'Node') -> bool:
        return self.priority < other.priority

class MCProblem():
    ''' Class that represents the problem of the missionaries and cannibals
        All algorithms will use this class to solve the problem
        The problem is defined by the number of missionaries and cannibals (groupSize), 
        the boat's capacity (boatCapacity) and the initial margin of the boat (startMargin)'''

    def __init__(self, groupSize:int = 3, boatCapacity: int = 2, startMargin: Literal['L', 'R'] = 'L' ) -> None:
        # defines the total size of each group (Missionaire or Cannibals)
        if (groupSize < 1):
            raise ValueError("The group size must be greater than 0")
        self.groupSize = groupSize

        # defines the capacity of the boat
        if (boatCapacity < 1):
            raise ValueError("The boat's capacity has to be greater than 0")
        self.boatCapacity = boatCapacity
        
        # set the initial state of the problem
        self.initialState = State(self.groupSize, self.groupSize, startMargin)

        # set the goal state of the problem
        self.goalState = State(0, 0, 'L' if startMargin == 'R' else 'R')

        # set the cache of neighbors
        self.neighborsCache:dict[str, list[Tuple[Action, State]]] = {}

    def reset(self) -> None:
        ''' Resets the problem to the initial state '''
        self.neighborsCache = {}

    # def calculateHeuristic(self, state:State, action:Action) -> int:
    #     ''' Calculates the heuristic of the action based on the current state
    #         The heuristic is the number of people on the initial side of the boat.
    #         Less people on the initial side of the boat, more likely the action is valid
    #         to reach the goal with less steps  '''
      
    #     return state.miss + state.cann - (action.miss + action.cann)

    # This heuristic is considered the best one for this problem
    def calculateHeuristic(self, state:State) -> float:
        ''' The difference heuristic is based on the idea of measuring the difference between 
            the number of missionaries and cannibals on either side of the river.
            
            In this heuristic, the initial state is assigned a heuristic value of zero, 
            and the goal state is assigned a heuristic value of one (since all the missionaries 
            and cannibals must be on the opposite side of the river in the goal state). 
            For all other states, the heuristic value is calculated as the absolute difference 
            between the number of missionaries and cannibals on the original side of the river 
            minus the number of missionaries and cannibals on the opposite side of the river, 
            divided by the total number of people.            '''
      
        initMarginPeople = state.miss + state.cann
        goalMarginPeople = self.groupSize * 2 - initMarginPeople
        heuristic = abs(initMarginPeople - goalMarginPeople) / (self.groupSize * 2)
        return heuristic
        # return 1

    def generateActions(self, state:State) -> list[Tuple[Action, State]]:
        ''' Generates all the possible actions based on the current state.
            The actions are generated by all the possible combinations of people that can be moved.
            The actions are also generated by all the possible directions that the boat can move.
            The actions are also validated to make sure that the action is valid. 
            The cost is set to 1 for all actions.
            The heuristic is calculated for each action. '''
        
        actions:list[Tuple[Action, State]] = []
        
        for miss in range(self.groupSize+1):
            for cann in range(self.groupSize+1):
                directions: list[Literal['L', 'R']] = ['L', 'R']
                for direction in directions:
                    action = Action(miss, cann, direction, 1)
                    if self.validateAction(state, action):
                        newState = self.transitionModel(state, action)
                        newState.heuristic = self.calculateHeuristic(newState)
                        actions.append((action, newState))

        return actions

    def validateAction(self, state:State, action:Action) -> bool:
        ''' Validates the action based on the current state.
            The action is valid if:
                - the boat is moving to the opposite side
                - the boat is not moving more people than the capacity allows
                - the boat is not moving more people than the margin has
                - the margin can't have more cannibals than missionaires '''
        
        # to move the boat it needs at least one person and at max boatCapacity people
        crewmembers = action.miss + action.cann
        if (crewmembers <= 0) or (crewmembers > self.boatCapacity):
            return False
        
        # the boat needs to move to the opposite side
        if action.direction == state.boat:
            return False

        # the boat can't move more people that the margin has
        if action.direction != self.initialState.boat:
            initialMargin = {
                "miss": state.miss - action.miss,
                "cann": state.cann - action.cann
            }
            oppositeMargin = {
                "miss": (self.groupSize - state.miss) + action.miss,
                "cann": (self.groupSize - state.cann) + action.cann
            }

        else:
            initialMargin = {
                "miss": state.miss + action.miss,
                "cann": state.cann + action.cann
            }
            oppositeMargin = {
                "miss": (self.groupSize - state.miss) - action.miss,
                "cann": (self.groupSize - state.cann) - action.cann
            }

        # can't move more people than the margin has
        if initialMargin['miss'] < 0 or initialMargin['cann'] < 0:
            return False

        if oppositeMargin['miss'] < 0 or oppositeMargin['cann'] < 0:
            return False

        # can't have more cannibals than missionaires in any margin
        return (initialMargin['miss'] == 0 or initialMargin['miss'] >= initialMargin['cann']) and (oppositeMargin['miss'] == 0 or oppositeMargin['miss'] >= oppositeMargin['cann'])

    def getValidActions(self, state:State) -> list[Tuple[Action, State]]:
        ''' Returns the valid actions based on the current state.
            The actions are cached to avoid recalculating them. '''
        
        key = repr(state)

        if (key in self.neighborsCache):
            return self.neighborsCache[key]
        
        self.neighborsCache[key] = self.generateActions(state)
        return self.neighborsCache[key]

    def getNeighbors(self, state:State) -> list[Tuple[State, Action]]:
        ''' Returns the neighbors for the current state.
            The neighbors are the valid actions applied to the current state. '''
        
        neighbors:list[Tuple[State, Action]] = []

        for action in self.getValidActions(state):
            neighbors.append((action[1], action[0]))

        return neighbors
    
    def transitionModel(self, state:State, action:Action) -> State:
        ''' Returns the new state based on the current state and the action.
            The new state is the current state with the action applied. '''
        if action.direction != self.initialState.boat:
            return State(state.miss - action.miss, state.cann - action.cann, action.direction)
        
        return State(state.miss + action.miss, state.cann + action.cann, action.direction)

    def showSolution(self, path: list[Tuple[State, Union[Action, None]]]) -> None:
        ''' Prints the solution path in a nice format. '''

        initMargin = self.initialState.boat

        for step in path:
            assert step[1] is not None
            
            s_Init_Margin = f"__{'👼' * step[0].miss:{'⬛'}{'<'}{self.groupSize}}_{'👹' * step[0].cann:{'⬛'}{'>'}{self.groupSize}}__"
            s_Boat = f"{' ' * (6+2*self.boatCapacity)}"
            s_Oppo_Margin = f"__{'👼' * (self.groupSize - step[0].miss):{'⬛'}{'<'}{self.groupSize}}_{'👹' * (self.groupSize - step[0].cann):{'⬛'}{'>'}{self.groupSize}}__"

            if (initMargin == 'L'):
                print(f"{s_Init_Margin} {s_Boat} {s_Oppo_Margin}")
            else:
                print(f"{s_Oppo_Margin} {s_Boat} {s_Init_Margin}")

            if (step[1].direction == initMargin):
                left_arrow = "   " if initMargin == 'R' else "⇇⇇ "
                right_arrow = " ⇉⇉" if initMargin == 'R' else "   "
                boat = f"{left_arrow}{'👼' * step[1].miss}{'👹' * step[1].cann}{'⬛' * (self.boatCapacity - (step[1].miss + step[1].cann))}{right_arrow}"
                print(f"{' ' * (5+(4*self.groupSize))} {boat} {' ' * (5+(4*self.groupSize))}")

            else:
                left_arrow = "   " if initMargin == 'L' else "⇇⇇ "
                right_arrow = " ⇉⇉" if initMargin == 'L' else "   "
                boat = f"{left_arrow}{'👼' * step[1].miss}{'👹' * step[1].cann}{'⬛' * (self.boatCapacity - (step[1].miss + step[1].cann))}{right_arrow}"
                print(f"{' ' * (5+(4*self.groupSize))} {boat} {' ' * (5+(4*self.groupSize))}")


        s_Init_Margin = f"__{'👼' * self.goalState.miss:{'⬛'}{'<'}{self.groupSize}}_{'👹' * self.goalState.cann:{'⬛'}{'>'}{self.groupSize}}__"
        s_Boat = f"{' ' * (6+2*self.boatCapacity)}"
        s_Oppo_Margin = f"__{'👼' * (self.groupSize - self.goalState.miss):{'⬛'}{'<'}{self.groupSize}}_{'👹' * (self.groupSize - self.goalState.cann):{'⬛'}{'>'}{self.groupSize}}__"

        if (initMargin == 'L'):
            print(f"{s_Init_Margin} {s_Boat} {s_Oppo_Margin}")
        else:
            print(f"{s_Oppo_Margin} {s_Boat} {s_Init_Margin}")
