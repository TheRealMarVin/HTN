import argparse

from htn_planner import HTNPlanner, NodeType
from critics import ResolveConflictsCritic, EliminateRedundantPreconditionsCritic, UseExistingObjectsCritic
from method import Method
from action import Action
from ordering_type import OrderingType
from utils import print_executed_actions


class PutOnMethod(Method):
    def __init__(self, obj1, obj2):
        task_name = f'ON({obj1}, {obj2})'
        self.obj1 = obj1
        self.obj2 = obj2

        condition = lambda state: self.is_applicable(state)

        super().__init__(task_name, [], condition, ordering=OrderingType.ORDERED)

    def is_applicable(self, state):
        return self.obj2 in state['CLEAR']

    def decompose(self, goal, state):
        subtasks = []
        if self.obj1 not in state['CLEAR']:
            subtasks.append({'type': NodeType.ACTION, 'action': ClearAction(self.obj1, state['ON'][self.obj1])})

        subtasks.append({'type': NodeType.ACTION, 'action': PutOnAction(self.obj1, self.obj2)})

        return subtasks


class ClearMethod(Method):
    def __init__(self, obj, obj_under):
        task_name = f'CLEAR({obj})'
        self.obj = obj
        self.obj_under = obj_under

        condition = lambda state: self.is_applicable(state)

        subtasks = [{'type': NodeType.ACTION, 'action': ClearAction(self.obj, self.obj_under)}]
        super().__init__(task_name, subtasks, condition, ordering=OrderingType.ORDERED)

    def is_applicable(self, state):
        return state['ON'].get(self.obj) == self.obj_under


class PutOnAction(Action):
    def __init__(self, obj1, obj2):
        name = f'PUTON({obj1}, {obj2})'
        preconditions = self.define_preconditions(obj1, obj2)
        effects = self.define_effects(obj1, obj2)

        super().__init__(name, preconditions, effects)

    def define_preconditions(self, obj1, obj2):
        return [
            lambda state: obj1 in state['CLEAR'],
            lambda state: obj2 in state['CLEAR']
        ]

    def define_effects(self, obj1, obj2):
        return [
            lambda state: state['ON'].update({obj1: obj2}),
            lambda state: state['CLEAR'].remove(obj1)
        ]

    def apply(self, state):
        for precondition in self.preconditions:
            if not precondition(state):
                raise ValueError(f"Cannot put {self.obj1} on {self.obj2}: preconditions not met.")

        for effect in self.effects:
            effect(state)

        return state


class ClearAction(Action):
    def __init__(self, obj, obj_under):
        name = f'CLEAR({obj})'
        self.obj = obj
        self.obj_under = obj_under
        preconditions = self.define_preconditions()
        effects = self.define_effects()
        super().__init__(name, preconditions, effects)

    def define_preconditions(self):
        return [
            lambda state: state['ON'].get(self.obj) == self.obj_under
        ]

    def define_effects(self):
        return [
            lambda state: state['CLEAR'].append(self.obj),
            lambda state: state['ON'].pop(self.obj)
        ]

    def apply(self, state):
        for precondition in self.preconditions:
            if not precondition(state):
                raise ValueError(f"Cannot clear {self.obj} from {self.obj_under}: preconditions not met.")

        for effect in self.effects:
            effect(state)

        return state


def block_stacking_is_goal_satisfied(goals, state):
    for goal in goals:
        if goal.startswith('ON('):
            obj1, obj2 = goal[3:-1].split(', ')
            if state['ON'].get(obj1) != obj2:
                return False

    return True




def main():
    methods = {
        'ON(A, B)': [PutOnMethod('A', 'B')],
        'ON(B, C)': [PutOnMethod('B', 'C')],
        'CLEAR(A)': [ClearAction('A', 'C')],  # Clear A from C
        'CLEAR(B)': [ClearAction('B', 'A')],  # Example clear actions for pairs
        'CLEAR(C)': [ClearAction('C', 'A')]
    }

    actions = {}
    critics = [ResolveConflictsCritic(), EliminateRedundantPreconditionsCritic(), UseExistingObjectsCritic()]
    planner = HTNPlanner(methods, actions, critics, block_stacking_is_goal_satisfied)

    # Correct initial state
    initial_state = {
        'CLEAR': ['B', 'C'],  # B is clear and C is clear (on A)
        'ON': {'A': 'C'}  # C is on A
    }
    goals = ['ON(A, B)', 'ON(B, C)']

    # Execute the plan
    plan = planner.plan(goals, initial_state)
    print_executed_actions(plan)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Blocks Experiment")
    args = parser.parse_args()

    main()
