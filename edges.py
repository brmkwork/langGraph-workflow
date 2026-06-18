from state import WorkflowState
from logger import log

MAX_ATTEMPTS = 3
def should_continue(state: WorkflowState) -> str:
    """
    Conditional edge function.
    Returns the name of the next node — LangGraph routes there.
    """
    score = state["avg_score"]
    attempts = state["attempts"]

    if state['avg_score'] >= 8.0:
        log("CONDITIONAL EDGE", "Score passed threshold → routing to END", {
            "avg_score": score,
            "attempts":  attempts,
            "decision":  "END",
        })
        return "END"
    
    if state["attempts"] >= MAX_ATTEMPTS:
        # print(f"Max attempts reached. Best score: {state['avg_score']}")
        log("CONDITIONAL EDGE", "Max attempts reached → routing to END", {
            "avg_score": score,
            "attempts":  attempts,
            "decision":  "END (max attempts hit)",
        })
        return "END"
    
    log("CONDITIONAL EDGE", "Score below threshold → routing back to generate", {
        "avg_score": score,
        "attempts":  attempts,
        "threshold": "8.0",
        "decision":  "RETRY",
    })
    
    # print(f"Score {state['avg_score']}/10 — retrying (attempt {state['attempts']})")
    return "generate"
