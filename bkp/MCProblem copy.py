from typing import Literal, Tuple, TypedDict, Union


class State(TypedDict):
    ''' Class that represents the state of the problem, just for typing purposes'''
    miss: int
    cann: int
    boat: Literal['L', 'R']


class Action(TypedDict):
    ''' Class that represents the actions of the problem, just for typing purposes'''
    miss: int
    cann: int
    direction: Literal['L', 'R']
    cost: int
    heuristic: int


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
        if (boatCapacity < 2):
            raise ValueError("The boat's capacity has to be greater than 1")
        self.boatCapacity = boatCapacity
        
        # define a margem inicial do barco, 0 para esquerda e 1 para direita
        self.initialState: State = {
            "miss": self.groupSize,
            "cann": self.groupSize,
            "boat": startMargin
        }

        # define o estado final do problema
        self.goalState: State = {
            "miss": 0,
            "cann": 0,
            "boat": 'L' if startMargin == 'R' else 'R'
        }

        self.actionsCache:dict[str, list[Action]] = {}


    def getStateKey(self, state:State) -> str:
        return f"{state['miss']}_{state['cann']}_{state['boat']}"


    def calculateHeuristic(self, state:State, action:Action) -> int:
        # 1 - Quanto menor a qtd de pessoas no lado do início, maior prioridade
        if (action['direction'] == self.initialState['boat']):
            return state['miss'] + state['cann'] - (action['miss'] + action['cann'])
        
        return 99


    def generateActions(self, state:State) -> list[Action]:
        actions:list[Action] = []
        
        for miss in range(self.groupSize):
            for cann in range(self.groupSize):
                directions: list[Literal['L', 'R']] = ['L', 'R']
                for direction in directions:
                    action: Action = {
                        "miss": miss,
                        "cann": cann,
                        "direction": direction,
                        "cost": 1,
                        "heuristic": 0 
                    }
                    if self.validateAction(state, action):
                        action['heuristic'] = self.calculateHeuristic(state, action)
                        actions.append(action)

        return actions


    def validateAction(self, state:State, action:Action) -> bool:
        
        # to move the boat it needs at least one person and at max boatCapacity people
        crewmembers = action['miss'] + action['cann']
        if (crewmembers <= 0) or (crewmembers > self.boatCapacity):
            return False
        
        # the boat needs to move to the opposite side
        if action['direction'] == state['boat']:
            return False

        # the boat can't move more people that the margin has
        if action['direction'] != self.initialState['boat']:
            initialMargin = {
                "miss": state['miss'] - action['miss'],
                "cann": state['cann'] - action['cann']
            }
            oppositeMargin = {
                "miss": (self.groupSize - state['miss']) + action['miss'],
                "cann": (self.groupSize - state['cann']) + action['cann']
            }

        else:
            initialMargin = {
                "miss": state['miss'] + action['miss'],
                "cann": state['cann'] + action['cann']
            }
            oppositeMargin = {
                "miss": (self.groupSize - state['miss']) - action['miss'],
                "cann": (self.groupSize - state['cann']) - action['cann']
            }

        # can't move more people than the margin has
        if initialMargin['miss'] < 0 or initialMargin['cann'] < 0:
            return False

        if oppositeMargin['miss'] < 0 or oppositeMargin['cann'] < 0:
            return False

        # can't have more cannibals than missionaires in any margin
        return (initialMargin['miss'] == 0 or initialMargin['miss'] >= initialMargin['cann']) and (oppositeMargin['miss'] == 0 or oppositeMargin['miss'] >= oppositeMargin['cann'])


    def getValidActions(self, state:State) -> list[Action]:
        key = f"{state['miss']}_{state['cann']}_{state['boat']}"

        if (key in self.actionsCache):
            return self.actionsCache[key]
        
        self.actionsCache[key] = self.generateActions(state)
        return self.actionsCache[key]

    
    def transitionModel(self, state:State, action:Action) -> State:
        newState:State = {
            "miss": state['miss'],
            "cann": state['cann'],
            "boat": action['direction']
        }

        if action['direction'] != self.initialState['boat']:
            newState['miss'] -= action['miss']
            newState['cann'] -= action['cann']
        else:
            newState['miss'] += action['miss']
            newState['cann'] += action['cann']

        return newState

    def showSolution(self, path: list[Tuple[State, Union[Action, None], Union[State, None]]]) -> None:
        initMargin = self.initialState['boat']

        for step in path:
            assert step[1] is not None
            assert step[2] is not None
            
            s_Init_Margin = f"__{'👼' * step[0]['miss']:{'⬛'}{'<'}{self.groupSize}}_{'👹' * step[0]['cann']:{'⬛'}{'>'}{self.groupSize}}__"
            s_Boat = f"{' ' * (6+2*self.boatCapacity)}"
            s_Oppo_Margin = f"__{'👼' * (self.groupSize - step[0]['miss']):{'⬛'}{'<'}{self.groupSize}}_{'👹' * (self.groupSize - step[0]['cann']):{'⬛'}{'>'}{self.groupSize}}__"

            if (initMargin == 'L'):
                print(f"{s_Init_Margin} {s_Boat} {s_Oppo_Margin}")
            else:
                print(f"{s_Oppo_Margin} {s_Boat} {s_Init_Margin}")


            if (step[1]['direction'] == initMargin):
                left_arrow = "   " if initMargin == 'R' else "⇇⇇ "
                right_arrow = " ⇉⇉" if initMargin == 'R' else "   "
                boat = f"{left_arrow}{'👼' * step[1]['miss']}{'👹' * step[1]['cann']}{'⬛' * (self.boatCapacity - (step[1]['miss'] + step[1]['cann']))}{right_arrow}"
                print(f"{' ' * (5+(4*self.groupSize))} {boat} {' ' * (5+(4*self.groupSize))}")

            else:
                left_arrow = "   " if initMargin == 'L' else "⇇⇇ "
                right_arrow = " ⇉⇉" if initMargin == 'L' else "   "
                boat = f"{left_arrow}{'👼' * step[1]['miss']}{'👹' * step[1]['cann']}{'⬛' * (self.boatCapacity - (step[1]['miss'] + step[1]['cann']))}{right_arrow}"
                print(f"{' ' * (5+(4*self.groupSize))} {boat} {' ' * (5+(4*self.groupSize))}")