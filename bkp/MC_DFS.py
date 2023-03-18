from typing import Tuple, Union
from MCProblem import MCProblem, State, Action

class DFS():
    def __init__(self, problem: MCProblem):
        self.problem = problem
        self.path: list[Tuple[State, Union[Action, None]]] = []
        self.reached: dict[str, bool] = {}

    def findSolution(self) -> None:
        if self.dfs(self.problem.initialState):
            print("Problema resolvido")
            path = self.path.copy()
            path.reverse()
            self.problem.showSolution(path)
            print("Objetivo alcançado!")
        else:
            print("Falha na resolução do problema")

    def dfs(self, state: State) -> bool:
        keyState = repr(state)

        # checa se o estado atual já foi analisado
        if keyState in self.reached:
            return False
        else:
            self.reached[keyState] = True
    
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
    problem = MCProblem(groupSize=3, boatCapacity=2)
    dfs = DFS(problem)
    dfs.findSolution()


if __name__ == "__main__":
    main()
