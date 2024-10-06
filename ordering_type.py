# This file defines the OrderingType enum, which specifies the type of ordering for subtasks
# in an HTN (Hierarchical Task Network) method. The available options are ordered, unordered,
# and partially ordered.

from enum import Enum


class OrderingType(Enum):
    ORDERED = "ordered"
    UNORDERED = "unordered"
    PARTIALLY_ORDERED = "partially_ordered"
