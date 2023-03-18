from typing import Tuple, Union
from queue import PriorityQueue
from MCProblem import MCProblem, State, Action, Node

class GBFS():
    def __init__(self, problem: MCProblem):
        self.problem = problem
        self.reached: dict[str, bool] = {}
        self.frontier: PriorityQueue[Node] = PriorityQueue()

    def findSolution(self) -> None:
        solution = self.gbfs()
        if solution:
            print("Problema resolvido")
            self.mountPath(solution, [])
            print("Objetivo alcançado!")
        else:
            print("Falha na resolução do problema")


    def gbfs(self) -> Node | None:
        node = Node(state=self.problem.initialState)
        if node.state == self.problem.goalState:
            return node

        self.frontier.put(node)
        keyState = repr(node.state)
        self.reached[keyState] = True

        while not self.frontier.empty():
            node = self.frontier.get()
            actions = self.problem.getValidActions(node.state)
            
            for action in actions:
                childState = self.problem.transitionModel(node.state, action)
                childNode = Node(parent=node, action=action, state=childState)
                if childState == self.problem.goalState:
                    return childNode
                
                childKeyState = repr(childNode.state)
                if childKeyState not in self.reached:
                    self.reached[childKeyState] = True
                    # assert action.heuristic is not None
                    childNode.setPriority(action.heuristic)
                    self.frontier.put(childNode)

        return None

    def mountPath(self, solution: Node, path: list[Tuple[State, Union[Action, None]]]) -> None:
        if (solution.parent is not None):
            path.append((solution.parent.state, solution.action))
            self.mountPath(solution.parent, path)
            
        else:
            path.reverse()
            self.problem.showSolution(path)
            return


def main():
    problem = MCProblem(groupSize=5, boatCapacity=4)
    gfs = GBFS(problem)
    gfs.findSolution()


if __name__ == "__main__":
    main()
