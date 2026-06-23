from state import WorkflowState
from logger import log

MAX_ATTEMPTS = 5


def should_continue(state: WorkflowState) -> str:
    """
    Conditional edge after validate.
    If score passes → END.
    If score fails → loop back to agent for a retry.
    If max attempts hit → END regardless.
    """
    score    = state["avg_score"]
    attempts = state["attempts"]

    if score >= 8.0:
        log("CONDITIONAL EDGE", "Score passed threshold → END", {
            "avg_score": score,
            "attempts":  attempts,
            "decision":  "END ✓",
        })
        return "END"

    if attempts >= MAX_ATTEMPTS:
        log("CONDITIONAL EDGE", "Max attempts reached → END", {
            "avg_score": score,
            "attempts":  attempts,
            "decision":  "END (max attempts hit)",
        })
        return "END"

    log("CONDITIONAL EDGE", "Score below threshold → retrying", {
        "avg_score": score,
        "attempts":  attempts,
        "threshold": "8.0",
        "decision":  "agent ↺",
    })
    return "agent"