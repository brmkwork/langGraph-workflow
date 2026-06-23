from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage
from nodes.llm import llm
from skills import get_tools, get_skill_descriptions, get_guardrail_descriptions
from state import WorkflowState
from logger import log


def build_system_prompt() -> str:
    return f"""You are an intelligent, accurate, and thorough assistant.

You have the following SKILLS available — use them when the task requires it:
{get_skill_descriptions()}

You have the following GUARDRAILS available — apply these whenever content warrants it:
{get_guardrail_descriptions()}

RULES:
1. If the user provides a file path or asks about a local file → call retrieve_tool first
2. If you retrieve content from any file → ALWAYS call pii_guardrail_tool on it next
3. Only generate your final response after all necessary tools have been called
4. Think step by step about which tools you need before responding
5. If no tools are needed → answer directly and clearly
"""


# Build the agent using create_agent 
tools = get_tools()

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=build_system_prompt(),
)


# Agent node — called by the graph 
def agent_node(state: WorkflowState) -> dict:
    log("AGENT", f"Starting attempt #{state.get('attempts', 0) + 1}", {
        "topic":           state["topic"],
        "has_feedback":    bool(state.get("feedback")),
        "tools_available": [t.name for t in tools],
    })

    # build input messages
    messages = []

    if state.get("feedback"):
        messages.append(SystemMessage(
            content=f"Previous attempt scored {state['avg_score']:.1f}/10. "
                    f"Improve by addressing: {state['feedback']}"
        ))

    if state.get("history"):
        messages.extend(state["history"])
    else:
        messages.append(HumanMessage(content=state["topic"]))

    # invoke the agent — it handles tool calling loop internally
    result = agent.invoke({"messages": messages})

    # extract final response from last message
    final_message  = result["messages"][-1]
    final_response = final_message.content

    # extract tool names the agent called
    tool_calls_made = [
        m.name
        for m in result["messages"]
        if hasattr(m, "name") and m.name
    ]

    log("AGENT DONE", "Agent finished", {
        "response_preview": final_response[:120] + "...",
        "tools_used":       tool_calls_made,
    })

    return {
        "response":         final_response,
        "attempts":         state.get("attempts", 0) + 1,
        "history":          result["messages"],
        "tool_calls_made":  tool_calls_made,
        "agent_scratchpad": "",
    }