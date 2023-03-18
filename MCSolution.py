import time
from queue import Queue, PriorityQueue
from typing import Tuple, Union
from MCProblem import MCProblem, State, Action, Node

class MCSolution():
    def __init__(self, problem: MCProblem):
        self.problem = problem
        self.path: list[Tuple[State, Union[Action, None]]] = []
        self.reached: list[str] = []

    def findSolution(self, alghoritm: str, show: bool = False) -> None:
        self.path = []
        self.reached = []
        self.problem.reset()

        if alghoritm == "dfs":
            start = time.time()
            if self.dfs(self.problem.initialState):
                print(f"Problema resolvido com {len(self.path)} passos, usando {alghoritm.upper()} depois {(time.time() - start) * 10**3} ms - depois de {len(self.reached)} estados analisados  ")
                print(self.problem.transitionCount)
                if show:
                    path = self.path.copy()
                    path.reverse()
                    self.problem.showSolution(path)
            else:
                print(f"Não foi possível resolver o problema - usando {alghoritm.upper()}")
        
        elif alghoritm == "bfs":
            start = time.time()
            solution = self.bfs()
            if solution:
                path = self.mountPath(solution, [])
                print(f"Problema resolvido com {len(path)} passos, usando {alghoritm.upper()} depois {(time.time() - start) * 10**3} ms - depois de {len(self.reached)} estados analisados  ")
                print(self.problem.transitionCount)                
                if show:
                    path = self.path.copy()
                    path.reverse()
                    self.problem.showSolution(path)

            else:
                print(f"Não foi possível resolver o problema - usando {alghoritm.upper()}")

        elif alghoritm == "gbfs":
            start = time.time()
            solution = self.gbfs()
            if solution:
                path = self.mountPath(solution, [])
                print(f"Problema resolvido com {len(path)} passos, usando {alghoritm.upper()} depois {(time.time() - start) * 10**3} ms - depois de {len(self.reached)} estados analisados  ")
                print(self.problem.transitionCount)                
                if show:
                    path = self.path.copy()
                    path.reverse()
                    self.problem.showSolution(path)

            else:
                print(f"Não foi possível resolver o problema - usando {alghoritm.upper()}")
            
        elif alghoritm == "astar":
            start = time.time()
            solution = self.aStar()
            if solution:
                path = self.mountPath(solution, [])
                print(f"Problema resolvido com {len(path)} passos, usando {alghoritm.upper()} depois {(time.time() - start) * 10**3} ms - depois de {len(self.reached)} estados analisados  ")
                print(self.problem.transitionCount)                
                if show:
                    path = self.path.copy()
                    path.reverse()
                    self.problem.showSolution(path)

            else:
                print(f"Não foi possível resolver o problema - usando {alghoritm.upper()}")
    
    def mountPath(self, solution: Node, path: list[Tuple[State, Union[Action, None]]]) -> list[Tuple[State, Union[Action, None]]]:
        if (solution.parent is not None):
            path.append((solution.parent.state, solution.action))
            return self.mountPath(solution.parent, path)
            
        return path

    def aStar(self) -> Node | None:
        node = Node(state=self.problem.initialState)
        if node.state == self.problem.goalState:
            return node

        frontier: PriorityQueue[Node] = PriorityQueue()
        frontier.put(node)
        self.reached.append(repr(node.state))

        while not frontier.empty():
            node = frontier.get()
            actions = self.problem.getValidActions(node.state)
            
            for action in actions:
                childState = self.problem.transitionModel(node.state, action)
                childNode = Node(parent=node, action=action, state=childState, cost=node.cost + action.cost + action.heuristic)

                if childState == self.problem.goalState:
                    return childNode
                
                childKeyState = repr(childNode.state)
                if childKeyState not in self.reached:
                    self.reached.append(childKeyState)
                    childNode.setPriority(childNode.cost)
                    frontier.put(childNode)

        return None
    
    def gbfs(self) -> Node | None:
        node = Node(state=self.problem.initialState)
        if node.state == self.problem.goalState:
            return node
        
        frontier: PriorityQueue[Node] = PriorityQueue()
        frontier.put(node)
        self.reached.append(repr(node.state))

        while not frontier.empty():
            node = frontier.get()
            actions = self.problem.getValidActions(node.state)
            
            for action in actions:
                childState = self.problem.transitionModel(node.state, action)
                childNode = Node(parent=node, action=action, state=childState)
                if childState == self.problem.goalState:
                    return childNode
                
                childKeyState = repr(childNode.state)
                if childKeyState not in self.reached:
                    self.reached.append(childKeyState)
                    childNode.setPriority(action.heuristic)
                    frontier.put(childNode)

        return None

    def bfs(self) -> Node | None:
        node = Node(state=self.problem.initialState)
        if node.state == self.problem.goalState:
            return node
        
        frontier: Queue[Node] = Queue()
        frontier.put(node)
        self.reached.append(repr(node.state))

        while not frontier.empty():
            node = frontier.get()
            actions = self.problem.getValidActions(node.state)
            
            for action in actions:
                childState = self.problem.transitionModel(node.state, action)
                childNode = Node(parent=node, action=action, state=childState)
                if childState == self.problem.goalState:
                    return childNode
                
                childKeyState = repr(childNode.state)
                if childKeyState not in self.reached:
                    self.reached.append(childKeyState)
                    frontier.put(childNode)

        return None

    def dfs(self, state: State) -> bool:
        keyState = repr(state)

        # checa se o estado atual já foi analisado
        if keyState in self.reached:
            return False
        else:
            self.reached.append(keyState)
    
        if state == self.problem.goalState:
            return True
        
        actions = self.problem.getValidActions(state)

        for action in actions:
            childState = self.problem.transitionModel(state, action)
            if self.dfs(childState):
                self.path.append((state, action))
                return True
        
        return False


def main():
    # problem = MCProblem()
    problem = MCProblem(groupSize=100, boatCapacity=10)
    solution = MCSolution(problem)
    solution.findSolution("astar")
    solution.findSolution("gbfs")
    solution.findSolution("bfs")
    solution.findSolution("dfs")


if __name__ == "__main__":
    main()
