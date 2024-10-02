# This file defines a camping example using HTN (Hierarchical Task Network) planning. 
# The example involves tasks like packing, setting up a campsite, starting a campfire, 
# and cooking food. Each task is decomposed into subtasks, which can be ordered, unordered, 
# or partially ordered, depending on the nature of the task.

import argparse

from action import Action
from htn_planner import HTNPlanner
from method import Method
from ordering_type import OrderingType

# Define individual actions for the camping process.
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

# Define methods for packing items, setting up a campsite, starting a campfire, and cooking food.

# Method to pack items (executed in a specific order)
packing_items_method = Method(
    task_name="Pack Items",
    subtasks=[pack_tent, pack_sleeping_bag, pack_food],
    condition=lambda state: state.get("packed_tent", 0) == 0,
    ordering=OrderingType.ORDERED
)

# Method to set up the campsite (unordered subtasks, they can happen in any order)
setting_up_campsite_method = Method(
    task_name="Set Up Campsite",
    subtasks=[pitch_tent, inflate_sleeping_bag, lay_out_ground_mat],
    condition=lambda state: state.get("pitched_tent", 0) == 0,
    ordering=OrderingType.UNORDERED
)

# Method to start a campfire (partially ordered with dependencies between subtasks)
starting_campfire_method = Method(
    task_name="Start Campfire",
    subtasks=[
        ("Gather Firewood", []),
        ("Build Firepit", ["Gather Firewood"]),
        ("Light Fire", ["Build Firepit"])],
    condition=lambda state: state.get("fire", 0) == 0,
    ordering=OrderingType.PARTIALLY_ORDERED
)

# Method to cook food (ordered subtasks: prepare ingredients, cook, then serve)
cooking_food_method = Method(
    task_name="Cook Food",
    subtasks=[prepare_ingredients, cook_on_fire, serve_food],
    condition=lambda state: state.get("served_food", 0) == 0,
    ordering=OrderingType.ORDERED
)

# High-level method to prepare for camping, consisting of packing, setting up the campsite, starting the fire, and cooking
prepare_for_camping_method = Method(
    task_name="Prepare for Camping",
    subtasks=["Pack Items", "Set Up Campsite", "Start Campfire", "Cook Food"],
    condition=lambda state: state.get("served_food", 0) == 0,
    ordering=OrderingType.ORDERED
)

def main():
    """
    Main function to run the camping HTN planning example. 
    Initializes the HTN planner, adds actions and methods, and generates a plan for 'Prepare for Camping'.
    """
    htn_planner = HTNPlanner(verbose=True)

    # Add actions to the planner.
    htn_planner.add_action(pack_tent)
    htn_planner.add_action(pack_sleeping_bag)
    htn_planner.add_action(pack_food)
    htn_planner.add_action(pitch_tent)
    htn_planner.add_action(inflate_sleeping_bag)
    htn_planner.add_action(lay_out_ground_mat)
    htn_planner.add_action(gather_firewood)
    htn_planner.add_action(build_firepit)
    htn_planner.add_action(light_fire)
    htn_planner.add_action(prepare_ingredients)
    htn_planner.add_action(cook_on_fire)
    htn_planner.add_action(serve_food)

    # Add methods to the planner.
    htn_planner.add_method(packing_items_method)
    htn_planner.add_method(setting_up_campsite_method)
    htn_planner.add_method(starting_campfire_method)
    htn_planner.add_method(cooking_food_method)
    htn_planner.add_method(prepare_for_camping_method)

    # Define the initial state for the planning process.
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

    # Decompose the high-level task "Prepare for Camping" into a plan of actions.
    plan = htn_planner.decompose("Prepare for Camping", initial_state)

    print("Generated Plan:", plan)


if __name__ == "__main__":
    # Argument parser for selecting the mode of operation.
    parser = argparse.ArgumentParser(description="Camping Experiment")
    args = parser.parse_args()

    main()
