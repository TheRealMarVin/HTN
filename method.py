# This file defines the Method class, which represents a way to decompose a high-level task
# into subtasks. Each method includes a task name, a list of subtasks, a condition for when
# the method is applicable, and an ordering type (ordered, unordered, or partially ordered).
import random

from action import Action
from htn_planner import NodeType
from ordering_type import OrderingType


class Method:
    def __init__(self, task_name, subtasks, condition, ordering, dependencies=None):
        """
        Initializes a method for decomposing a high-level task into subtasks.
        :param task_name: The name of the task this method applies to.
        :param subtasks: A list of subtasks (actions or other methods).
        :param condition: A function that checks whether this method can be applied given the current state.
        :param ordering: Defines the order in which the subtasks should be executed (ordered, unordered, etc.).
        :param dependencies: For partially ordered tasks, defines dependencies (e.g., [('A', 'B')] means A before B).
        """
        self.task_name = task_name
        self.subtasks = subtasks
        self.condition = condition
        self.ordering = ordering
        self.dependencies = dependencies if dependencies is not None else []

    def is_applicable(self, state):
        """
        A generic implementation to check if the method can be applied in the current state.
        It uses the `condition` function provided during initialization.
        :param state: The current state of the world.
        :return: True if the method is applicable, False otherwise.
        """
        return self.condition(state)

    def decompose(self, goal, state):
        """
        Generic implementation for decomposing a task into subtasks.
        :param goal: The goal to achieve with this method.
        :param state: The current state of the world.
        :return: A list of subgoals or actions to achieve the given goal.
        """
        subgoals = []

        if self.ordering == OrderingType.ORDERED:
            ordered_subtasks = self.subtasks
        elif self.ordering == OrderingType.UNORDERED:
            ordered_subtasks = random.sample(self.subtasks, len(self.subtasks))
        elif self.ordering == OrderingType.PARTIALLY_ORDERED:
            ordered_subtasks = self._resolve_partial_order(self.subtasks, self.dependencies)
        else:
            raise ValueError("Unknown ordering type")

        for subtask in ordered_subtasks:
            if isinstance(subtask, Action):
                subgoals.append({'type': NodeType.ACTION, 'action': subtask})
            else:
                subgoals.append({'type': NodeType.GOAL, 'goal': subtask})

        return subgoals

    def _resolve_partial_order(self, subtasks, dependencies):
        """
        Resolves the partial ordering of subtasks based on the provided dependencies.
        :param subtasks: A list of subtasks (actions or other methods).
        :param dependencies: A list of tuples where each tuple represents a dependency (e.g., ('A', 'B') means A must happen before B).
        :return: A list of subtasks in an order that satisfies the partial ordering constraints.
        """
        subtask_names = {subtask.name: subtask for subtask in subtasks}
        dependency_graph = {task_name: [] for task_name in subtask_names.keys()}

        for before, after in dependencies:
            dependency_graph[after].append(before)

        ordered_task_names = self._topological_sort(dependency_graph)
        ordered_subtasks = [subtask_names[task_name] for task_name in ordered_task_names]

        return ordered_subtasks

    @staticmethod
    def _topological_sort(dependency_graph):
        """
        Perform a topological sort to resolve dependencies and return an order of subtasks that respects the partial ordering.
        :param dependency_graph: A dictionary representing the dependency graph (task_name -> list of tasks that must be done before it).
        :return: A valid order of task names that respects the dependencies.
        """
        visited = set()
        temp_mark = set()
        result = []

        def visit(task_name):
            if task_name in temp_mark:
                raise ValueError("Circular dependency detected")
            if task_name not in visited:
                temp_mark.add(task_name)
                for dependency in dependency_graph[task_name]:
                    visit(dependency)
                temp_mark.remove(task_name)
                visited.add(task_name)
                result.append(task_name)

        for task_name in dependency_graph:
            visit(task_name)

        return result
