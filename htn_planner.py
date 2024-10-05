class NodeType:
    SPLIT = "SPLIT"
    JOIN = "JOIN"
    GOAL = "GOAL"
    ACTION = "ACTION"
    PHANTOM = "PHANTOM"


class HTNPlanner:
    def __init__(self, methods, actions, critics, is_goal_satisfied):
        self.methods = methods
        self.actions = actions
        self.critics = critics
        self.is_goal_satisfied = is_goal_satisfied

    def plan(self, goals, state):
        plan = []
        for goal in goals:
            plan.append(self.create_goal_node(goal))

        final_plan = []

        while plan:
            node = plan.pop(0)

            if self.is_goal_satisfied(goals, state):
                break

            if node['type'] == NodeType.GOAL:
                subgoals = self.decompose_goal(node, state)
                if subgoals:
                    plan = subgoals + plan
                else:
                    raise ValueError(f"No method or action found to decompose goal: {node['goal']}")

            elif node['type'] == NodeType.ACTION:
                state = self.execute_action(node, state)
                final_plan.append(node)

            self.apply_critics(plan)

        return final_plan

    def decompose_goal(self, goal_node, state):
        if goal_node['goal'] in self.actions:
            action = self.actions[goal_node['goal']]
            return [{'type': NodeType.ACTION, 'action': action}]

        methods = self.methods.get(goal_node['goal'], [])
        subgoals = []

        for method in methods:
            if method.is_applicable(state):
                subgoals.extend(method.decompose(goal_node['goal'], state))
                break

        return subgoals

    def execute_action(self, action_node, state):
        action = action_node.get('action')
        if action is None:
            raise ValueError("No action found in the node. Cannot execute None.")
        return action.apply(state)

    def handle_split(self, node, state):
        split_goals = node['subgoals']
        return [{'type': NodeType.GOAL, 'goal': subgoal} for subgoal in split_goals]

    def handle_join(self, node, plan):
        return plan

    def apply_critics(self, plan):
        for critic in self.critics:
            plan = critic.analyze(plan)
        return plan

    def create_goal_node(self, goal):
        return {'type': NodeType.GOAL, 'goal': goal}
