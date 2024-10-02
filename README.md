# 🏕️ Welcome to the HTN Camping Planner! 🏕️

Ah, planning for a relaxing camping trip... but wait, the campfire won’t light itself, and those marshmallows won’t roast without a little help! Fear not, intrepid adventurer, for we are here to introduce you to **HTN (Hierarchical Task Network) Planning**, an exploration of HTN concepts where camping dreams come true—one structured decomposition at a time! This is not the most complete HTN implementation but serves as a foundation to experiment with task networks. This code is inspired by the foundational work on HTN, as described in the paper *"Hierarchical Task Network Planning: Formalization, Analysis, and Implementation"* by Ghallab, Nau, and Traverso.


## What is this sorcery called HTN?

**HTN Planning** is like following a recipe book for your camping trip. It breaks down your lofty ambitions (like not sleeping on bare rocks) into smaller, manageable subtasks that you can tackle. Unlike goal-oriented planning (*ahem* GOAP), where you're always looking for the "best" path, HTN is more like your friendly scoutmaster telling you, "First pitch the tent, THEN gather firewood. No skipping steps!"

## 🏕️ Camping Planner Breakdown

Imagine you're prepping for the ultimate camping experience. Here’s what HTN has in store for you:

1. **Task**: Prepare for Camping
   - Like a general in charge of making sure everything gets done before nightfall. (Or the rain comes.)

2. **Subtasks**:
   - **Pitch the Tent** (no, it’s not a suggestion).
   - **Gather Firewood** (if you don’t, good luck roasting marshmallows).
   - **Build Firepit** (because random fires in the woods are frowned upon).
   - **Light the Fire** (cue dramatic flint-striking montage).
   - **Cook Food** (don’t even think about skipping this step).

## How Does it Work?

### 🌳 Decomposition
HTN Planner will take your high-level task ("Prepare for Camping") and decompose it into smaller tasks, like a pro project manager, ensuring every little detail is covered (because you *really* need that firepit).

### 🚀 Ordered, Unordered, and Partially Ordered Tasks
- **Ordered**: Tasks that need to happen in a specific sequence. No fire without firewood, right?
- **Unordered**: Go wild! Do tasks in any order, but make sure they all get done.
- **Partially Ordered**: Some tasks can happen in any order, but others—like "gather wood before lighting fire"—are non-negotiable.

## Installation Instructions

1. **Clone this repository**:  
   `git clone https://github.com/your-repo/HTN-planner.git`
2. **Install the requirements** (we like things simple—just Python):  
   `pip install -r requirements.txt`
3. **Run the demo**:
   - Want to see the plan? Run the HTN planner in plan mode!  
     `python main_htn.py --mode plan`
   - Ready for the action? Execute the plan and see the HTN planner in action!  
     `python main_htn.py --mode execute`

## Psst... Credit Where It’s Due
Some of this README's code and cleverness came straight from ChatGPT. It might not pitch your tent, but it sure helps polish your code!
