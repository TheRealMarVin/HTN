from method import Method
from action import Action
from typing import List, Dict, Callable

from ordering_type import OrderingType


class HTNPlanner:
    def __init__(self, verbose: bool = False):
        self.methods = []
        self.operators = []
        self.verbose = verbose

    def add_method(self, method: Method):
        self.methods.append(method)

    def add_operator(self, operator: Action):
        self.operators.append(operator)

    def decompose(self, task: str, state: Dict[str, int]) -> List[str]:
        for method in self.methods:
            if method.task_name == task and method.condition(state):
                if self.verbose:
                    if method.ordering == OrderingType.ORDERED:
                        print(f"Decomposing task '{task}' in ordered manner using method {method.subtasks}")
                    elif method.ordering == OrderingType.UNORDERED:
                        print(f"Decomposing task '{task}' in unordered manner using method {method.subtasks}")
                    elif method.ordering == OrderingType.PARTIALLY_ORDERED:
                        print(f"Decomposing task '{task}' in partially ordered manner using method {method.subtasks}")

                plan = []
                for subtask in method.subtasks:
                    if isinstance(subtask, Action):
                        if subtask.is_applicable(state):
                            plan.append(subtask.name)
                            subtask.apply(state)
                        else:
                            return []
                    else:
                        plan += self.decompose(subtask, state)
                return plan
        return []

