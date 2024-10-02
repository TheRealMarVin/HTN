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
    subtasks=[
        ("Gather Firewood", []),
        ("Build Firepit", ["Gather Firewood"]),
        ("Light Fire", ["Build Firepit"])],
    condition=lambda state: state.get("fire", 0) == 0,
    ordering=OrderingType.PARTIALLY_ORDERED
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


def main():
    htn_planner = HTNPlanner(verbose=True)

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

    htn_planner.add_method(packing_items_method)
    htn_planner.add_method(setting_up_campsite_method)
    htn_planner.add_method(starting_campfire_method)
    htn_planner.add_method(cooking_food_method)
    htn_planner.add_method(prepare_for_camping_method)

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

    plan = htn_planner.decompose("Prepare for Camping", initial_state)

    print("Generated Plan:", plan)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Camping Experiment")
    args = parser.parse_args()

    main()