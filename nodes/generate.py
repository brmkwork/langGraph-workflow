# from langchain_core.messages import HumanMessage, SystemMessage
# from nodes.llm import llm
# from state import WorkflowState
# from logger import log

# def generate(state: WorkflowState) -> dict:
#     log("GENERATE", f"Starting attempt #{state.get('attempts', 0) + 1}", {
#         "topic":           state["topic"],
#         "has_feedback":    bool(state.get("feedback")),
#         "feedback":        state.get("feedback", "none"),
#         "has_rag_context": bool(state.get("retrieved_chunks")),
#     })

#     messages = [
#         SystemMessage(content="You are a helpful, accurate, and clear assistant."),
#     ]

#     if state.get("feedback"):
#         messages.append(SystemMessage(
#             content=f"Previous attempt scored {state['avg_score']:.1f}/10. "
#                     f"Improve by addressing: {state['feedback']}"
#         ))

#     if state.get("retrieved_chunks"):
#         messages.append(SystemMessage(
#             content=f"Use the following extracted content from the file to answer the user's question. "
#                     f"Only use information present in the content below:\n\n"
#                     f"{state['retrieved_chunks']}"
#         ))
#         messages.append(HumanMessage(content=state["file_question"]))
#     else:
#         messages.append(HumanMessage(content=state["topic"]))

#     response = llm.invoke(messages)

#     log("GENERATE DONE", "LLM responded", {
#         "response_preview": response.content[:120] + "...",
#     })

#     return {
#         "response": response.content,
#         "attempts": state.get("attempts", 0) + 1,
#         "history":  messages + [response],
#     }