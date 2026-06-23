from langgraph.graph import StateGraph, END
from state import WorkflowState
from agent.agent_node import agent_node
from nodes.validate import validate
from edges import should_continue
from logger import log


def build_graph():
    builder = StateGraph(WorkflowState)

    # ── nodes 
    builder.add_node("agent",    agent_node)
    builder.add_node("validate", validate)

    # ── entry point 
    builder.set_entry_point("agent")

    # ── agent always goes to validate 
    builder.add_edge("agent", "validate")

    # ── validate → retry or END 
    
    builder.add_conditional_edges(
        "validate",
        should_continue,
        {
            "agent": "agent",
            "END":    END,
        }
    )

    return builder.compile()


graph = build_graph()