import json
from langchain_core.messages import HumanMessage
from nodes.llm import validation_llm
from nodes.prompts import SCORE_PROMPT
from state import WorkflowState
from logger import log

def validate(state: WorkflowState) -> dict:
    log("VALIDATE", f"Scoring attempt #{state.get('attempts')}", {
        "response_preview": state["response"][:120] + "...",
    })

    prompt = SCORE_PROMPT.format(
        topic=state["topic"],
        response=state["response"],
    )
    result = validation_llm.invoke([HumanMessage(content=prompt)])

    raw = result.content.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        scores = json.loads(raw)
    except json.JSONDecodeError:
        print(f"Bad output: {raw}")
        raise

    feedback = scores.pop("feedback")
    avg      = sum(scores.values()) / len(scores)

    log("VALIDATE DONE", "Scores received", {
        "relevance": scores.get("relevance"),
        "accuracy":  scores.get("accuracy"),
        "clarity":   scores.get("clarity"),
        "depth":     scores.get("depth"),
        "avg_score": round(avg, 2),
        "feedback":  feedback,
    })

    return {
        "scores":    scores,
        "avg_score": round(avg, 2),
        "feedback":  feedback,
    }