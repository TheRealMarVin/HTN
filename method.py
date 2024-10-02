# This file defines the Method class, which represents a way to decompose a high-level task
# into subtasks. Each method includes a task name, a list of subtasks, a condition for when
# the method is applicable, and an ordering type (ordered, unordered, or partially ordered).

from typing import List, Dict, Callable

from ordering_type import OrderingType


class Method:
    def __init__(self, task_name: str, subtasks: List, condition: Callable[[Dict], bool],
                 ordering: OrderingType = OrderingType.UNORDERED):
        """
        Initializes a method for decomposing a task into subtasks.

        :param task_name: The name of the high-level task (e.g., "Prepare for Camping").
        :param subtasks: A list of subtasks (can be actions or other tasks).
        :param condition: A function that takes the current state and returns True if the method is applicable.
        :param ordering: Specifies whether the subtasks must be ordered, unordered, or partially ordered.
        """
        self.task_name = task_name
        self.subtasks = subtasks
        self.condition = condition
        self.ordering = ordering
