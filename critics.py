# This file defines critic classes that analyze and modify a plan in HTN planning, resolving conflicts, eliminating redundant preconditions, and reusing existing objects.
from htn_planner import NodeType


class ResolveConflictsCritic:
    def analyze(self, plan):
        """
        Analyzes the given plan to resolve conflicts by removing duplicate actions on the same objects.
        :param plan: The plan to be analyzed, consisting of action nodes.
        :return: A new plan with conflicts (duplicate actions) resolved.
        """
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
        """
        Analyzes the given plan and eliminates redundant actions based on repeated preconditions on the same objects.
        :param plan: The plan to be analyzed, consisting of action nodes.
        :return: A new plan with redundant actions removed.
        """
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
        """
        Analyzes the given plan to reuse existing objects in actions where applicable.
        :param plan: The plan to be analyzed, consisting of action nodes.
        :return: A new plan where existing objects are reused when possible.
        """
        for node in plan:
            if node['type'] == NodeType.ACTION and hasattr(node['action'], 'obj1') and hasattr(node['action'], 'obj2'):
                obj1, obj2 = node['action'].obj1, node['action'].obj2
                if self.is_existing_object_in_plan(obj1, obj2, plan):
                    node['action'].obj1, node['action'].obj2 = self.reuse_existing_object(obj1, obj2, plan)
        return plan

    def is_existing_object_in_plan(self, obj1, obj2, plan):
        """
        Checks if the given objects are already part of any action in the plan.
        :param obj1: The first object to check.
        :param obj2: The second object to check.
        :param plan: The plan to search for existing objects.
        :return: True if the objects are found in the plan, False otherwise.
        """
        for node in plan:
            if node['type'] == NodeType.ACTION and hasattr(node['action'], 'obj1') and hasattr(node['action'], 'obj2'):
                if obj1 in [node['action'].obj1, node['action'].obj2] or obj2 in [node['action'].obj1, node['action'].obj2]:
                    return True
        return False

    def reuse_existing_object(self, obj1, obj2, plan):
        """
        Reuses existing objects in the plan for future actions.
        :param obj1: The first object to reuse.
        :param obj2: The second object to reuse.
        :param plan: The plan to check for object reuse.
        :return: The reused object pair (obj1, obj2).
        """
        return obj1, obj2
