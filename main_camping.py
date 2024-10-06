# This file defines a camping example using HTN (Hierarchical Task Network) planning.
# The example involves tasks like packing, setting up a campsite, starting a campfire,
# and cooking food. Each task is decomposed into subtasks, which can be ordered, unordered,
# or partially ordered, depending on the nature of the task.

import argparse

from action import Action
from htn_planner import HTNPlanner
from method import Method
from ordering_type import OrderingType

pack_tent = Action("Pack Tent", {}, {"packed_tent": 1}, duration=1)
pack_sleeping_bag = Action("Pack Sleeping Bag", {}, {"packed_sleeping_bag": 1}, duration=1)
pack_food = Action("Pack Food", {}, {"packed_food": 1}, duration=1)
pitch_tent = Action("Pitch Tent", {"packed_tent": 1}, {"pitched_tent": 1}, duration=2)
inflate_sleeping_bag = Action("Inflate Sleeping Bag", {"packed_sleeping_bag": 1}, {"inflated_sleeping_bag": 1}, duration=1)
lay_out_ground_mat = Action("Lay Out Ground Mat", {}, {"ground_mat": 1}, duration=1)
gather_firewood = Action("Gather Firewood", {}, {"firewood": 1}, duration=2)
build_firepit = Action("Build Firepit", {}, {"firepit": 1}, duration=2)
light_fire = Action("Light Fire", {"firepit": 1}, {"fire": 1}, duration=1)
prepare_ingredients = Action("Prepare Ingredients", {}, {"prepared_ingredients": 1}, duration=1)
cook_on_fire = Action("Cook on Fire", {"fire": 1, "prepared_ingredients": 1}, {"cooked_food": 1}, duration=2)
serve_food = Action("Serve Food", {"cooked_food": 1}, {"served_food": 1}, duration=1)

packing_items_method = Method(
    task_name="Pack Items",
    subtasks=[pack_tent, pack_sleeping_bag, pack_food],
    condition=lambda state: state.get("packed_tent", 0) == 0,
    ordering=OrderingType.ORDERED
)

setting_up_campsite_method = Method(
    task_name="Set Up Campsite",
    subtasks=[pitch_tent, inflate_sleeping_bag, lay_out_ground_mat],
    condition=lambda state: state.get("pitched_tent", 0) == 0,
    ordering=OrderingType.UNORDERED
)

starting_campfire_method = Method(
    task_name="Start Campfire",
    subtasks=[gather_firewood, build_firepit, light_fire],  # Subtasks as individual tasks or actions
    condition=lambda state: state.get("fire", 0) == 0,
    ordering=OrderingType.PARTIALLY_ORDERED,  # Specify that the tasks are partially ordered
    dependencies=[('Gather Firewood', 'Build Firepit'), ('Build Firepit', 'Light Fire')]  # Define dependencies
)

cooking_food_method = Method(
    task_name="Cook Food",
    subtasks=[prepare_ingredients, cook_on_fire, serve_food],
    condition=lambda state: state.get("served_food", 0) == 0,
    ordering=OrderingType.ORDERED
)

prepare_for_camping_method = Method(
    task_name="Prepare for Camping",
    subtasks=["Pack Items", "Set Up Campsite", "Start Campfire", "Cook Food"],
    condition=lambda state: state.get("served_food", 0) == 0,
    ordering=OrderingType.ORDERED
)


def camping_is_goal_satisfied(goal, state):
    """
    Simple goal-checking function for camping.
    Checks if the goal is satisfied based on the state.
    """
    for goal_name in goal:
        if goal_name == "Serve Food" and state.get("served_food", 0) > 0:
            return True

    return False


def main():
    """
    Main function to run the camping HTN planning example.
    Initializes the HTN planner, adds actions and methods, and generates a plan to achieve the state of 'served_food': 1.
    """
    actions = {
        "Pack Tent": pack_tent,
        "Pack Sleeping Bag": pack_sleeping_bag,
        "Pack Food": pack_food,
        "Pitch Tent": pitch_tent,
        "Inflate Sleeping Bag": inflate_sleeping_bag,
        "Lay Out Ground Mat": lay_out_ground_mat,
        "Gather Firewood": gather_firewood,
        "Build Firepit": build_firepit,
        "Light Fire": light_fire,
        "Prepare Ingredients": prepare_ingredients,
        "Cook on Fire": cook_on_fire,
        "Serve Food": serve_food
    }

    methods = {
        "Pack Items": [packing_items_method],
        "Set Up Campsite": [setting_up_campsite_method],
        "Start Campfire": [starting_campfire_method],
        "Cook Food": [cooking_food_method],
        "Prepare for Camping": [prepare_for_camping_method]
    }

    htn_planner = HTNPlanner(
        methods=methods,
        actions=actions,
        critics=[],
        is_goal_satisfied=camping_is_goal_satisfied
    )

    initial_state = {
        "packed_tent": 0,
        "packed_sleeping_bag": 0,
        "packed_food": 0,
        "pitched_tent": 0,
        "inflated_sleeping_bag": 0,
        "ground_mat": 0,
        "firewood": 0,
        "firepit": 0,
        "fire": 0,
        "prepared_ingredients": 0,
        "cooked_food": 0,
        "served_food": 0,
    }

    goals = ["Prepare for Camping"]

    plan = htn_planner.plan(goals, initial_state)

    print("Generated Plan:")
    for step in plan:
        print(step['action'].name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Camping Experiment")
    args = parser.parse_args()

    main()
