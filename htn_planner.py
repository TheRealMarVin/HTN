from method import Method
from action import Action
from typing import List, Dict, Callable
from itertools import permutations
from ordering_type import OrderingType


class HTNPlanner:
    def __init__(self, verbose: bool = False):
        self.methods = []
        self.actions = []
        self.verbose = verbose

    def add_method(self, method: Method):
        self.methods.append(method)

    def add_action(self, action: Action):
        self.actions.append(action)

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

                if method.ordering == OrderingType.ORDERED:
                    for subtask in method.subtasks:
                        plan += self._process_subtask(subtask, state)
                elif method.ordering == OrderingType.UNORDERED:
                    plan = self._decompose_unordered(method.subtasks, state)
                elif method.ordering == OrderingType.PARTIALLY_ORDERED:
                    plan = self._decompose_partially_ordered(method.subtasks, state)

                return plan

        return []

    def _process_subtask(self, subtask, state: Dict[str, int]) -> List[str]:
        if isinstance(subtask, Action):
            if subtask.is_applicable(state):
                subtask.apply(state)
                return [subtask.name]
            return []
        else:
            return self.decompose(subtask, state)

    def _decompose_unordered(self, subtasks: List, state: Dict[str, int]) -> List[str]:
        for perm in permutations(subtasks):
            temp_state = state.copy()
            temp_plan = []
            valid = True
            for subtask in perm:
                result = self._process_subtask(subtask, temp_state)
                if not result:
                    valid = False
                    break
                temp_plan.extend(result)

            if valid:
                return temp_plan

        return []

    def _decompose_partially_ordered(self, subtasks: List, state: Dict[str, int]) -> List[str]:
        pending_tasks = subtasks[:]
        completed_tasks = set()
        temp_state = state.copy()
        temp_plan = []

        while pending_tasks:
            progress = False
            for subtask_info in pending_tasks[:]:
                subtask, dependencies = subtask_info if isinstance(subtask_info, tuple) else (subtask, [])
                if all(dep in completed_tasks for dep in dependencies):
                    result = self._process_subtask(subtask, temp_state)
                    if result:
                        temp_plan.extend(result)
                        completed_tasks.add(subtask)
                        pending_tasks.remove(subtask_info)
                        progress = True

            if not progress:
                return []

        return temp_plan
