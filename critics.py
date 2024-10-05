from htn_planner import NodeType


class ResolveConflictsCritic:
    def analyze(self, plan):
        seen_actions = set()
        new_plan = []

        for node in plan:
            if node['type'] == NodeType.ACTION and hasattr(node['action'], 'obj1') and hasattr(node['action'], 'obj2'):
                obj1, obj2 = node['action'].obj1, node['action'].obj2
                if (obj1, obj2) not in seen_actions:
                    seen_actions.add((obj1, obj2))
                    new_plan.append(node)
            else:
                new_plan.append(node)

        return new_plan


class EliminateRedundantPreconditionsCritic:
    def analyze(self, plan):
        seen_actions = set()
        new_plan = []

        for node in plan:
            if node['type'] == NodeType.ACTION and hasattr(node['action'], 'obj1') and hasattr(node['action'], 'obj2'):
                obj1, obj2 = node['action'].obj1, node['action'].obj2
                if (obj1, obj2) not in seen_actions:
                    seen_actions.add((obj1, obj2))
                    new_plan.append(node)
            else:
                new_plan.append(node)

        return new_plan


class UseExistingObjectsCritic:
    def analyze(self, plan):
        for node in plan:
            if node['type'] == NodeType.ACTION and hasattr(node['action'], 'obj1') and hasattr(node['action'], 'obj2'):
                obj1, obj2 = node['action'].obj1, node['action'].obj2
                if self.is_existing_object_in_plan(obj1, obj2, plan):
                    node['action'].obj1, node['action'].obj2 = self.reuse_existing_object(obj1, obj2, plan)
        return plan

    def is_existing_object_in_plan(self, obj1, obj2, plan):
        for node in plan:
            if node['type'] == NodeType.ACTION and hasattr(node['action'], 'obj1') and hasattr(node['action'], 'obj2'):
                if obj1 in [node['action'].obj1, node['action'].obj2] or obj2 in [node['action'].obj1, node['action'].obj2]:
                    return True
        return False

    def reuse_existing_object(self, obj1, obj2, plan):
        return obj1, obj2

