# 🏕️ Welcome to the HTN Planning Experiments! 🏗️

Ah, planning for a relaxing camping trip... or stacking blocks into neat towers? Whether you're pitching tents or balancing cubes, **HTN (Hierarchical Task Network) Planning** is here to help you break down high-level tasks into manageable steps. This repository provides implementations of HTN for various scenarios, including a **Camping Planner** and a **Block-Stacking Problem**.

This code serves as a foundation to experiment with task networks, inspired by the foundational work on HTN, as described in the paper *"Hierarchical Task Network Planning: Formalization, Analysis, and Implementation"* by Ghallab, Nau, and Traverso.

## What is HTN?

**HTN Planning** is a structured approach to problem-solving, where high-level tasks (like "Prepare for a Hike" or "Stack Blocks") are broken down into smaller, manageable subtasks or actions. Unlike other planning approaches, such as GOAP (Goal-Oriented Action Planning), HTN planners rely on predefined task methods and structured decompositions, ensuring that tasks are followed step by step.

## 🏕️ & 🏗️ HTN Examples in This Repository

1. **Camping Planner**:
   - This example focuses on preparing for a camping trip. You'll need to pitch a tent, gather firewood, build a firepit, light the fire, cook food, and, most importantly, serve the food!

2. **Block-Stacking Problem**:
   - In this scenario, the goal is to stack blocks in a specific configuration, such as stacking block A on block B and block B on block C. The planner decomposes the task of stacking into actions like moving and clearing blocks.

Both examples demonstrate the flexibility and power of HTN planning in different problem domains.

## How Does HTN Work?

### 🌳 Decomposition
HTN Planner takes a high-level task (like "Prepare for Camping" or "Stack Blocks") and decomposes it into smaller tasks or actions, ensuring that all steps are followed to achieve the final goal.

### 🚀 Ordered, Unordered, and Partially Ordered Tasks
- **Ordered**: Tasks that need to happen in a specific sequence (e.g., you can’t light a fire without gathering firewood).
- **Unordered**: Tasks can be performed in any order (e.g., packing different items for camping).
- **Partially Ordered**: Some tasks are flexible, but others must follow specific rules (e.g., "gather wood before lighting the fire" or "clear block C before moving block A").

In the code, this is controlled using the `OrderingType` enum, allowing you to define tasks as `ORDERED`, `UNORDERED`, or `PARTIALLY_ORDERED`.

## 🏗️ Block-Stacking Example

### Block Problem Breakdown

1. **Task**: Stack blocks in a specific order (e.g., A on B, B on C).
2. **Subtasks**:
   - **Move block A to block B** (only if B is clear).
   - **Move block B to block C** (only if C is clear).
   - **Clear blocks** (if any blocks are in the way).

### Example Code Snippet for Block Stacking:

```python
move_block = Action("Move Block", {"block_clear": 1}, {"block_stacked": 1}, duration=1)
clear_block = Action("Clear Block", {}, {"block_clear": 1}, duration=1)

block_stacking_method = Method(
    task_name="Stack Blocks",
    subtasks=[move_block, clear_block],
    condition=lambda state: True,  # Stack blocks when blocks are clear
    ordering=OrderingType.PARTIALLY_ORDERED
)
```
In this example, the task is to stack the blocks in a specific configuration, but the method ensures the necessary blocks are cleared before stacking them.

### 🏕️ Camping Example
**Camping Problem Breakdown**
* Task: Prepare for Camping
* Subtasks:
  * Pitch the Tent (because sleeping on the ground isn’t ideal).
  * Gather Firewood (to get that campfire going).
  * Build Firepit (you don’t want a fire hazard).
  * Light the Fire (now we’re talking!).
  * Cook Food (no one likes burnt marshmallows).
  * Serve Food (the final goal: delicious campfire cooking).

Example Code Snippet for Camping:
```python
pitch_tent = Action("Pitch Tent", {}, {"tent_pitched": 1}, duration=2)
gather_firewood = Action("Gather Firewood", {}, {"firewood": 1}, duration=2)
build_firepit = Action("Build Firepit", {"firewood": 1}, {"firepit_built": 1}, duration=2)
light_fire = Action("Light Fire", {"firepit_built": 1}, {"fire_lit": 1}, duration=1)
serve_food = Action("Serve Food", {"cooked_food": 1}, {"served_food": 1}, duration=1)

set_up_campsite_method = Method(
    task_name="Set Up Campsite",
    subtasks=[pitch_tent, gather_firewood, build_firepit, light_fire],
    condition=lambda state: True,  # Can always set up a campsite
    ordering=OrderingType.ORDERED
)
```
#### Installation Instructions
* Clone this repository:

```bash
git clone https://github.com/TheRealMarVin/HTN.git
```

* Set up your environment: Ensure you are using Python 3.x. 

* Run the Camping Planner:
Now that everything is set up, run the planner for the camping scenario:

```bash
python main_camping.py
```

OR

Run the Block-Stacking Planner:

```bash
python main_blocks.py
```

### What to Expect:
#### For the Camping Planner:
When you run the camping planner, the high-level task "Prepare for Camping" will be broken down into subtasks, and you’ll see a plan generated that looks something like this:

```diff
Generated Plan:
- Pitch Tent
- Gather Firewood
- Build Firepit
- Light Fire
- Serve Food
```
#### For the Block-Stacking Planner:
When you run the block-stacking planner, you’ll see a plan generated for stacking the blocks in the desired configuration.

```mathematica
Generated Plan:
- Clear Block C
- Move Block A to Block B
- Move Block B to Block C
```

### Psst... Credit Where It’s Due
Some of this README's code and cleverness came straight from ChatGPT. It might not pitch your tent, but it sure helps polish your code!