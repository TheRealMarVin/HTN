import argparse

from htn_planner import HTNPlanner, NodeType
from critics import ResolveConflictsCritic, EliminateRedundantPreconditionsCritic, UseExistingObjectsCritic
from method import Method
from action import Action
from ordering_type import OrderingType


# Example methods
from ordering_type import OrderingType
from utils import print_executed_actions


class PutOnMethod(Method):
    def __init__(self, obj1, obj2):
        task_name = f'ON({obj1}, {obj2})'
        self.obj1 = obj1
        self.obj2 = obj2

        # Condition to check if the method is applicable
        condition = lambda state: self.is_applicable(state)

        # Initialize the method without subtasks, they will be defined in decompose
        super().__init__(task_name, [], condition, ordering=OrderingType.ORDERED)

    def is_applicable(self, state):
        # Check if obj2 is clear in the current state
        return self.obj2 in state['CLEAR']

    def decompose(self, goal, state):
        subtasks = []
        # If obj1 is not clear, add a clear subtask first
        if self.obj1 not in state['CLEAR']:
            subtasks.append({'type': NodeType.ACTION, 'action': ClearAction(self.obj1, state['ON'][self.obj1])})

        # Then add the put-on subtask
        subtasks.append({'type': NodeType.ACTION, 'action': PutOnAction(self.obj1, self.obj2)})

        # Return the ordered subtasks
        return subtasks


class ClearMethod(Method):
    def __init__(self, obj, obj_under):
        task_name = f'CLEAR({obj})'
        self.obj = obj
        self.obj_under = obj_under

        # Condition to check if the method is applicable
        condition = lambda state: self.is_applicable(state)

        # Initialize the method with ordered subtasks
        subtasks = [{'type': NodeType.ACTION, 'action': ClearAction(self.obj, self.obj_under)}]
        super().__init__(task_name, subtasks, condition, ordering=OrderingType.ORDERED)

    def is_applicable(self, state):
        # Check if obj is on top of obj_under
        return state['ON'].get(self.obj) == self.obj_under


class PutOnAction(Action):
    def __init__(self, obj1, obj2):
        # Define the action's name, preconditions, and effects
        name = f'PUTON({obj1}, {obj2})'
        preconditions = self.define_preconditions(obj1, obj2)
        effects = self.define_effects(obj1, obj2)

        # Initialize the base Action class with name, preconditions, and effects
        super().__init__(name, preconditions, effects)

    def define_preconditions(self, obj1, obj2):
        # Preconditions: obj1 and obj2 must both be clear
        return [
            lambda state: obj1 in state['CLEAR'],  # obj1 is clear
            lambda state: obj2 in state['CLEAR']  # obj2 is clear
        ]

    def define_effects(self, obj1, obj2):
        # Effects: obj1 is placed on obj2, obj1 is no longer clear
        return [
            lambda state: state['ON'].update({obj1: obj2}),  # obj1 is on obj2
            lambda state: state['CLEAR'].remove(obj1)  # obj1 is no longer clear
        ]

    def apply(self, state):
        # Apply the action if preconditions are met
        for precondition in self.preconditions:
            if not precondition(state):
                raise ValueError(f"Cannot put {self.obj1} on {self.obj2}: preconditions not met.")

        # Apply the effects of the action
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
        # Preconditions: obj must be on top of obj_under
        return [
            lambda state: state['ON'].get(self.obj) == self.obj_under  # obj is on top of obj_under
        ]

    def define_effects(self):
        # Effects: obj becomes clear, and it's removed from being on top of obj_under
        return [
            lambda state: state['CLEAR'].append(self.obj),  # obj becomes clear
            lambda state: state['ON'].pop(self.obj)         # obj is no longer on obj_under
        ]

    def apply(self, state):
        # Check if preconditions are met before applying the action
        for precondition in self.preconditions:
            if not precondition(state):
                raise ValueError(f"Cannot clear {self.obj} from {self.obj_under}: preconditions not met.")

        # Apply effects
        for effect in self.effects:
            effect(state)

        return state


def block_stacking_is_goal_satisfied(goals, state):
    for goal in goals:
        # Handle relational goals like 'ON(A, B)'
        if goal.startswith('ON('):
            obj1, obj2 = goal[3:-1].split(', ')
            if state['ON'].get(obj1) != obj2:
                return False  # If any goal is not satisfied, return False

    # If all goals are satisfied, return True
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
