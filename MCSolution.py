import time
from queue import Queue, PriorityQueue
from typing import Literal, Tuple, Union
from MCProblem import MCProblem, State, Action, Node

class MCSolution():
    def __init__(self, groupSize:int = 3, boatCapacity: int = 2, startMargin: Literal['L', 'R'] = 'L'):
        self.problem = MCProblem(groupSize, boatCapacity, startMargin)
        self.path: list[Tuple[State, Union[Action, None]]] = []
        self.reached: list[str] = []

    def findSolution(self, alghoritm: str, show: bool = False) -> None:
        self.path = []
        self.reached = []
        self.problem.reset()

        match alghoritm.lower():
            case "dfs":
                start = time.time()
                if self.dfs(self.problem.initialState):
                    print(f"\n\n{alghoritm.upper()} - {len(self.path)} passos - {(time.time() - start) * 10**3} ms - {len(self.reached)} estados analisados")
                    if show:
                        path = self.path.copy()
                        path.reverse()
                        self.problem.showSolution(path)
                else:
                    print(f"\n\nNão foi possível resolver o problema - usando {alghoritm.upper()}")
        
            case "bfs":
                start = time.time()
                solution = self.bfs()
                if solution:
                    path = self.mountPath(solution, [])
                    print(f"\n\n{alghoritm.upper()} - {len(path)} passos - {(time.time() - start) * 10**3} ms - {len(self.reached)} estados analisados")
                    if show:
                        path.reverse()
                        self.problem.showSolution(path)

                else:
                    print(f"\n\nNão foi possível resolver o problema - usando {alghoritm.upper()}")

            case "gbfs":
                start = time.time()
                solution = self.gbfs()
                if solution:
                    path = self.mountPath(solution, [])
                    print(f"\n\n{alghoritm.upper()} - {len(path)} passos - {(time.time() - start) * 10**3} ms - {len(self.reached)} estados analisados")
                    if show:
                        path.reverse()
                        self.problem.showSolution(path)

                else:
                    print(f"\n\nNão foi possível resolver o problema - usando {alghoritm.upper()}")
                
            case "a*":
                start = time.time()
                solution = self.aStar()
                if solution:
                    path = self.mountPath(solution, [])
                    print(f"\n\n{alghoritm.upper()} - {len(path)} passos - {(time.time() - start) * 10**3} ms - {len(self.reached)} estados analisados")
                    if show:
                        path.reverse()
                        self.problem.showSolution(path)

                else:
                    print(f"\n\nNão foi possível resolver o problema - usando {alghoritm.upper()}")
    
    def mountPath(self, solution: Node, path: list[Tuple[State, Union[Action, None]]]) -> list[Tuple[State, Union[Action, None]]]:
        if (solution.parent is not None):
            path.append((solution.parent.state, solution.action))
            return self.mountPath(solution.parent, path)
            
        return path

    def aStar(self) -> Node | None:
        ''' A* (A Star) algorithm'''

        # Create the root node
        node = Node(state=self.problem.initialState)
        # Check if the root node is the goal
        if node.state == self.problem.goalState: return node

        # Create the frontier queue and add the root node
        frontier: PriorityQueue[Node] = PriorityQueue()
        frontier.put(node)

        # Add the root node to the reached list
        self.reached.append(repr(node.state))

        # While the frontier is not empty
        while not frontier.empty():
            # Get the first node from the frontier
            node = frontier.get()
            # Get the neighbors of the node
            neighbors = self.problem.getNeighbors(node.state)
            
            # For each neighbor
            for neighbor in neighbors:
                neighborAction = neighbor[1]
                neighborState = neighbor[0]
                # Calculate the neighbor cost
                neighborCost = node.cost + neighborAction.cost + neighborState.heuristic
                # Create a child node
                neighborNode = Node(parent=node, action=neighborAction, state=neighborState, cost=neighborCost)                
                # Check if the child node is the goal
                if neighborState == self.problem.goalState: return neighborNode
                
                # Check if the child node was already reached
                neighborKeyState = repr(neighborState)
                if neighborKeyState not in self.reached:
                    # Add the child node to the frontier
                    self.reached.append(neighborKeyState)
                    # Set the neighbor node priority
                    neighborNode.priority = neighborCost
                    # Add the child node to the frontier
                    frontier.put(neighborNode)

        return None
    
    def gbfs(self) -> Node | None:
        ''' GBFS (Greedy Best First Search - Busca Gulosa) algorithm'''
        # Create the root node
        node = Node(state=self.problem.initialState)
        # Check if the root node is the goal
        if node.state == self.problem.goalState: return node
        
        # Create the frontier queue and add the root node
        frontier: PriorityQueue[Node] = PriorityQueue()
        frontier.put(node)

        # Add the root node to the reached list
        self.reached.append(repr(node.state))

        # While the frontier is not empty
        while not frontier.empty():
            # Get the first node from the frontier
            node = frontier.get()
            # Get the neighbors of the node
            neighbors = self.problem.getNeighbors(node.state)
            
            # For each neighbor
            for neighbor in neighbors:
                neighborAction = neighbor[1]
                neighborState = neighbor[0]
                # Create a child node
                childNode = Node(parent=node, action=neighborAction, state=neighborState)
                # Check if the child node is the goal
                if neighborState == self.problem.goalState: return childNode
                
                # Check if the child node was already reached
                childKeyState = repr(childNode.state)
                if childKeyState not in self.reached:
                    # Add the child node to the reached list
                    self.reached.append(childKeyState)
                    # Set the child node priority, which is the heuristic value
                    childNode.priority = neighborState.heuristic
                    # Add the child node to the frontier
                    frontier.put(childNode)

        return None

    def bfs(self) -> Node | None:
        ''' BFS (Breadth First Search - Busca em Largura) algorithm'''
        # Create the root node
        node = Node(state=self.problem.initialState)
        # Check if the root node is the goal
        if node.state == self.problem.goalState: return node
        
        # Create the frontier queue and add the root node
        frontier: Queue[Node] = Queue()
        frontier.put(node)

        # Add the root node to the reached list
        self.reached.append(repr(node.state))

        # While the frontier is not empty
        while not frontier.empty():
            # Get the first node of the frontier
            node = frontier.get()
            # Get the neighbors of the node
            neighbors = self.problem.getNeighbors(node.state)
            
            # For each neighbor
            for neighbor in neighbors:
                # Create a child node
                childNode = Node(parent=node, action=neighbor[1], state=neighbor[0])
                # Check if the child node is the goal
                if neighbor[0] == self.problem.goalState: return childNode
                
                # Check if the child node was already reached
                childKeyState = repr(childNode.state)
                if childKeyState not in self.reached:
                    # Add the child node to the reached list
                    self.reached.append(childKeyState)
                    # Add the child node to the frontier
                    frontier.put(childNode)

        return None

    def dfs(self, state: State) -> bool:
        ''' DFS (Depth First Search - Busca em Profundidade) algorithm '''

        # Check if the state is the goal
        if state == self.problem.goalState: return True

        # Check if the state was already reached
        keyState = repr(state)
        if keyState in self.reached: return False
        self.reached.append(keyState)
        
        # Get the neighbors of the state
        neighbors = self.problem.getNeighbors(state)
        for neighbor in neighbors:
            neighborAction = neighbor[1]
            neighborState = neighbor[0]
            # Recursive checks all the neighbors
            if self.dfs(neighborState):
                # If the neighbor is the goal, add the parent state and the action to the path
                self.path.append((state, neighborAction))
                return True
        
        return False


def main():
    groupSize = 3
    boatCapacity = 2
    algorithms = ["A*", "GBFS", "BFS", "DFS"]
    showGraph = True
    solution = MCSolution(groupSize=groupSize, boatCapacity=boatCapacity)
    for i in algorithms:
        solution.findSolution(i, show=showGraph)

if __name__ == "__main__":
    main()
