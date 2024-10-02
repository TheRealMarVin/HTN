# This file defines the Action class, which represents an action with preconditions and effects
# in HTN or other planning systems. Actions can be applied to a state if their preconditions
# are met, and they modify the state according to their effects.

from typing import Dict, Optional


class Action:
    def __init__(self, name: str, preconditions: Dict[str, int], effects: Dict[str, int],
                 duration: Optional[int] = None):
        """
        Initializes an action with a name, preconditions, effects, and an optional duration.

        :param name: The name of the action (e.g., "Gather Wood").
        :param preconditions: A dictionary of conditions that must be satisfied for the action to be applicable.
        :param effects: A dictionary of effects that the action has on the state (changes it makes).
        :param duration: Optional; duration of the action (in time units), defaults to None if not specified.
        """
        self.name = name
        self.preconditions = preconditions
        self.effects = effects
        self.duration = duration

    def is_applicable(self, state: Dict[str, int]) -> bool:
        """
        Checks if the action can be applied to the given state by verifying if all the preconditions are met.

        :param state: The current state represented as a dictionary.
        :return: True if all preconditions are satisfied, False otherwise.
        """
        return all(state.get(k, 0) >= v for k, v in self.preconditions.items())

    def apply(self, state: Dict[str, int]):
        """
        Applies the action to the state by updating the state with the action's effects.

        :param state: The current state that will be modified by applying the action's effects.
        """
        for k, v in self.effects.items():
            state[k] = state.get(k, 0) + v
