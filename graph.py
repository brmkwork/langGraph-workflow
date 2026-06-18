from langgraph.graph import StateGraph, END
from state import WorkflowState
from nodes import detect_command, retrieve, generate, validate
from edges import should_continue
from logger import log
from nodes import detect_command, retrieve, generate, validate

#Conditional edge: after detect_command 
def route_command(state: WorkflowState) -> str:
    if state["command"] == "file-review":
        log("CONDITIONAL EDGE", "File review detected → routing to retrieve", {
            "file_path":     state["file_path"],
            "file_question": state["file_question"],
            "decision":      "retrieve ↓",
        })
        return "retrieve"

    log("CONDITIONAL EDGE", "Normal prompt → routing to generate", {
        "topic":    state["topic"],
        "decision": "generate ↓",
    })
    return "generate"


def build_graph():
    builder = StateGraph(WorkflowState)

    #Register all nodes 
    builder.add_node("detect_command", detect_command)
    builder.add_node("retrieve",       retrieve)
    builder.add_node("generate",       generate)
    builder.add_node("validate",       validate)

    #Entry point 
    builder.set_entry_point("detect_command")

    #Conditional edge: detect_command → retrieve OR generate 
    builder.add_conditional_edges(
        "detect_command",
        route_command,
        {
            "retrieve": "retrieve",
            "generate": "generate",
        }
    )

    #retrieve always goes to generate 
    builder.add_edge("retrieve", "generate")

    #generate always goes to validate 
    builder.add_edge("generate", "validate")

    #Conditional edge: validate → generate OR END
    builder.add_conditional_edges(
        "validate",
        should_continue,
        {
            "generate": "generate",
            "END":       END,
        }
    )

    return builder.compile()

graph = build_graph()