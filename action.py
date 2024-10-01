from typing import Dict, Optional


class Action:
    def __init__(self, name: str, preconditions: Dict[str, int], effects: Dict[str, int], duration: Optional[int] = None):
        self.name = name
        self.preconditions = preconditions
        self.effects = effects
        self.duration = duration

    def is_applicable(self, state: Dict[str, int]) -> bool:
        return all(state.get(k, 0) >= v for k, v in self.preconditions.items())

    def apply(self, state: Dict[str, int]):
        for k, v in self.effects.items():
            state[k] = state.get(k, 0) + v
