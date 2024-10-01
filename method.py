from typing import List, Dict, Callable


class Method:
    def __init__(self, task_name: str, subtasks: List, condition: Callable[[Dict], bool], ordering: str = "unordered"):
        self.task_name = task_name
        self.subtasks = subtasks
        self.condition = condition
        self.ordering = ordering
