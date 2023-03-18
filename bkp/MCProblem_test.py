import unittest
from MCProblem import MCProblem

class TestMCProblem(unittest.TestCase):

    def test_groupSize(self):
        mc = MCProblem(3)
        self.assertEqual(mc.groupSize, 3)
        self.assertEqual(mc.initialState, {'miss': 3, 'cann': 3, 'boat': 'L'})
        self.assertEqual(mc.goalState, {'miss': 0, 'cann': 0, 'boat': 'R'})

        mc = MCProblem(5, 'R')
        self.assertEqual(mc.groupSize, 5)
        self.assertEqual(mc.initialState, {'miss': 5, 'cann': 5, 'boat': 'R'})
        self.assertEqual(mc.goalState, {'miss': 0, 'cann': 0, 'boat': 'L'})

    def test_groupSize_values(self):
        with self.assertRaises(ValueError):
            mc = MCProblem(0)
            mc = MCProblem(-1)

    def test_actions(self):
        mc = MCProblem(3)

        self.assertEqual(mc.generateActions(mc.initialState), [
            # {'miss': 0, 'cann': 0, 'direction': 'L', 'cost': 1, 'heuristic': 0}, WRONG DIRECTION
            # {'miss': 0, 'cann': 0, 'direction': 'R', 'cost': 1, 'heuristic': 0}, NO CREW MEMBERS
            # {'miss': 0, 'cann': 1, 'direction': 'L', 'cost': 1, 'heuristic': 0}, WRONG DIRECTION
            {'miss': 0, 'cann': 1, 'direction': 'R', 'cost': 1, 'heuristic': 0},
            # {'miss': 0, 'cann': 2, 'direction': 'L', 'cost': 1, 'heuristic': 0}, WRONG DIRECTION
            {'miss': 0, 'cann': 2, 'direction': 'R', 'cost': 1, 'heuristic': 0},
            # {'miss': 1, 'cann': 0, 'direction': 'L', 'cost': 1, 'heuristic': 0}, WRONG DIRECTION
            # {'miss': 1, 'cann': 0, 'direction': 'R', 'cost': 1, 'heuristic': 0}, CANNIBALS OUTNUMBER MISSIONAIRES
            # {'miss': 1, 'cann': 1, 'direction': 'L', 'cost': 1, 'heuristic': 0}, WRONG DIRECTION
            {'miss': 1, 'cann': 1, 'direction': 'R', 'cost': 1, 'heuristic': 0},
            # {'miss': 1, 'cann': 2, 'direction': 'L', 'cost': 1, 'heuristic': 0}, WRONG DIRECTION
            # {'miss': 1, 'cann': 2, 'direction': 'R', 'cost': 1, 'heuristic': 0}, NOT ENOUGH BOAT CAPACITY
            # {'miss': 2, 'cann': 0, 'direction': 'L', 'cost': 1, 'heuristic': 0}, WRONG DIRECTION
            # {'miss': 2, 'cann': 0, 'direction': 'R', 'cost': 1, 'heuristic': 0}, CANNIBALS OUTNUMBER MISSIONAIRES
            # {'miss': 2, 'cann': 1, 'direction': 'L', 'cost': 1, 'heuristic': 0}, WRONG DIRECTION
            # {'miss': 2, 'cann': 1, 'direction': 'R', 'cost': 1, 'heuristic': 0}, NOT ENOUGH BOAT CAPACITY
            # {'miss': 2, 'cann': 2, 'direction': 'L', 'cost': 1, 'heuristic': 0}, WRONG DIRECTION
            # {'miss': 2, 'cann': 2, 'direction': 'R', 'cost': 1, 'heuristic': 0}, NOT ENOUGH BOAT CAPACITY
        ])
