# This file defines the HTNPlanner class which is responsible for decomposing high-level tasks into
# subtasks using methods, and applying actions according to the defined ordering (ordered, unordered,
# or partially ordered). It processes tasks recursively to generate a plan of actions that can be executed.

from method import Method
from action import Action
from typing import List, Dict
from itertools import permutations
from ordering_type import OrderingType


class HTNPlanner:
    def __init__(self, verbose: bool = False):
        """
        Initializes the HTNPlanner with empty lists for methods and actions, and an optional verbosity flag.

        :param verbose: If set to True, the planner will print detailed decomposition steps during planning.
        """
        self.methods = []
        self.actions = []
        self.verbose = verbose

    def add_method(self, method: Method):
        """
        Adds a method to the planner. Methods define how a task should be decomposed into subtasks.

        :param method: The method to be added to the planner.
        """
        self.methods.append(method)

    def add_action(self, action: Action):
        """
        Adds an action to the planner. Actions are the final executable steps that modify the state.

        :param action: The action to be added to the planner.
        """
        self.actions.append(action)

    def decompose(self, task: str, state: Dict[str, int]) -> List[str]:
        """
        Decomposes a task by finding the appropriate method and recursively breaking it down into
        subtasks, which may include both methods and actions.

        :param task: The task name to decompose.
        :param state: The current state of the world as a dictionary.
        :return: A list of action names representing the plan to achieve the task.
        """
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
        """
        Processes a subtask, which can be either an action or a task that needs to be decomposed further.

        :param subtask: The subtask to process (can be an Action or a task name).
        :param state: The current state of the world as a dictionary.
        :return: A list of action names if the subtask is an applicable action, or a plan if it is a decomposable task.
        """
        if isinstance(subtask, Action):
            if subtask.is_applicable(state):
                subtask.apply(state)
                return [subtask.name]
            return []
        else:
            return self.decompose(subtask, state)

    def _decompose_unordered(self, subtasks: List, state: Dict[str, int]) -> List[str]:
        """
        Decomposes a set of unordered subtasks, attempting different permutations of the subtasks
        until a valid plan is found.

        :param subtasks: A list of subtasks to decompose in any order.
        :param state: The current state of the world as a dictionary.
        :return: A list of action names representing a valid plan, or an empty list if no valid plan is found.
        """
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
        """
        Decomposes a set of partially ordered subtasks, ensuring that tasks with dependencies are
        completed in the required order while allowing flexibility for other tasks.

        :param subtasks: A list of tuples where each tuple contains a subtask and its dependencies.
        :param state: The current state of the world as a dictionary.
        :return: A list of action names representing a valid plan, or an empty list if no valid plan is found.
        """
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
