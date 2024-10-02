# 🏕️ Hierarchical Task Network (HTN) Planning Explained

This document is an in-depth look at how **Hierarchical Task Network (HTN) Planning** works, with code snippets and explanations. If you're curious about HTN and how it compares to goal-oriented planning approaches like GOAP, you're in the right place!

### What is HTN?

**HTN (Hierarchical Task Network) Planning** is a planning approach where a high-level task (like “Prepare for a Hike”) is broken down into a set of smaller tasks or actions (like “Pack a raincoat” or “Pack a tent”). This decomposition happens in a **top-down** manner, based on predefined methods that describe how to achieve the high-level tasks. HTN doesn't search for the most optimal sequence of actions dynamically. Instead, it relies on **structured decomposition** as described in the task methods.

HTN planning differs from GOAP (Goal-Oriented Action Planning) because it is **more structured and hierarchical**. Instead of dynamically choosing the next best action toward the goal, HTN planners break down tasks into smaller, predefined subtasks, following a set of rules laid out by the designer of the planner.

---

## 📦 How HTN Planning Works

The goal of HTN planning is to **decompose a complex task into smaller, manageable subtasks** that can be executed sequentially. 

### Key Concepts

- **Tasks**: The high-level objectives you want to accomplish, like “Set Up Campsite” or “Prepare for Hike.”
- **Subtasks**: Smaller tasks that need to be completed to achieve the main task.
- **Methods**: A method defines how a task should be decomposed into subtasks, potentially with different strategies for different situations.
- **Actions**: The final steps that change the state of the world, like “Pack Tent” or “Light Fire.”
- **Operators**: The concrete actions that directly modify the state.

---

## 🛠️ HTN Planning Example

Let's consider an example where you want to **set up a campsite**. You need to pitch a tent, gather firewood, build a firepit, and light the fire.

### Ordered Task Example

```python
# Define actions
pitch_tent = Action("Pitch Tent", {}, {"tent_pitched": 1}, duration=2)
gather_firewood = Action("Gather Firewood", {}, {"firewood": 5}, duration=3)
build_firepit = Action("Build Firepit", {"firewood": 5}, {"firepit_built": 1}, duration=1)
light_fire = Action("Light Fire", {"firepit_built": 1}, {"fire_lit": 1}, duration=2)

# Define method for setting up campsite
set_up_campsite_method = Method(
    task_name="Set Up Campsite",
    subtasks=[pitch_tent, gather_firewood, build_firepit, light_fire],
    condition=lambda state: True,  # Can always set up a campsite
    ordering=OrderingType.ORDERED
)
```
In this example, we have a task called "Set Up Campsite" with four subtasks: Pitch Tent, Gather Firewood, Build Firepit, and Light Fire. These subtasks are ordered, meaning they need to be executed in the specified sequence.

---

## 🔄 Why All Subtasks Must Be Visited

In HTN, each method provides a complete set of subtasks required to achieve the main task. The subtasks are not optional, and there is no optimization of which subtasks to pick or which can be skipped. The reasoning behind this design is that HTN operates based on a structured decomposition: each task has a "recipe" that must be followed in order to ensure the task's successful completion.

This is different from approaches like GOAP, where only the actions that directly bring you closer to the goal are chosen. In HTN, all subtasks are part of the solution because they reflect the full process needed to accomplish the task according to domain-specific knowledge.

### Example:
In our camping example, even if you feel that gathering firewood is not immediately necessary (since you already have some), the method might still require it because the task "Set Up Campsite" was designed with the assumption that fresh firewood is needed.

## Why Is There No Dynamic Reordering of Subtasks?

In HTN, the planner does not attempt to dynamically reorder subtasks. If the method specifies an ordered list of subtasks, they are carried out in that exact sequence. The same applies for unordered and partially ordered tasks, where flexibility exists, but it’s still based on pre-designed constraints.

For example, in a partially ordered method:

- Some tasks must be done in a specific order (e.g., "gather wood before lighting the fire").
- Other tasks can happen in any order or simultaneously (e.g., "set up the tent" can happen anytime before nightfall).

HTN methods are designed this way to ensure predictability and domain-specific knowledge consistency.

---

## 🔀 Unordered and Partially Ordered Tasks
HTN also supports tasks that don’t have strict ordering:

Unordered Example:
```python
unordered_method = Method(
    task_name="Set Up Campsite",
    subtasks=[pitch_tent, gather_firewood, build_firepit, light_fire],
    condition=lambda state: True,
    ordering=OrderingType.UNORDERED
)
```

In this case, the subtasks can be performed in any order, and the task will still be considered complete as long as all subtasks are done.

Partially Ordered Example:
```python
partially_ordered_method = Method(
    task_name="Start Campfire",
    subtasks=[
        ("Gather Firewood", []), 
        ("Build Firepit", ["Gather Firewood"]),
        ("Light Fire", ["Build Firepit"])
    ],
    condition=lambda state: True,
    ordering=OrderingType.PARTIALLY_ORDERED
)
```

In this partially ordered method, "Gather Firewood" must be done before "Build Firepit," and "Build Firepit" must be done before "Light Fire." However, "Pitch Tent" or other tasks could still happen in parallel or at any time.

## 🎯 Conclusion
HTN is a powerful planning approach that breaks down complex tasks into smaller steps, following a structured and often domain-specific method. It does not optimize within tasks or dynamically reorder actions based on state (as in GOAP). Instead, it ensures that all subtasks specified in the method are executed to ensure success.

HTN is ideal when you have a predictable environment and a set of predefined procedures that need to be followed. It's like following a step-by-step guide to ensure nothing is missed in achieving your overall goal.