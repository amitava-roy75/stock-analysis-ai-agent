from langgraph.graph import END, StateGraph

from graph.state import StockState

from nodes.planner_node import PlannerNode
from nodes.router_node import RouterNode
from nodes.reflection_node import ReflectionNode


builder = StateGraph(StockState)

#
# Nodes
#

builder.add_node(
    "planner",
    PlannerNode()
)

builder.add_node(
    "router",
    RouterNode()
)

builder.add_node(
    "reflection",
    ReflectionNode()
)

#
# Flow
#

builder.set_entry_point("planner")

builder.add_edge(
    "planner",
    "router"
)

builder.add_edge(
    "router",
    "reflection"
)

builder.add_edge(
    "reflection",
    END
)

graph = builder.compile()