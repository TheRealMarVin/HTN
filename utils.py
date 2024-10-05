from htn_planner import NodeType


def print_executed_actions(plan):
    print("Executed Actions:")
    for node in plan:
        if node['type'] == NodeType.ACTION:
            action = node['action']
            print(f"Action: {action.name}")  # Assuming each action has a 'name' attribute
