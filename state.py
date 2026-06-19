from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class WorkflowState(TypedDict):
    topic: str
    response: str
    scores: dict[str, float]
    avg_score: float
    attempts: int
    feedback: str
    history: Annotated[list, add_messages]

    command: str
    file_path: str
    file_question: str        
    retrieved_chunks: str
    retrieval_scores: list   
    file_already_embedded: bool

    pii_found: list
    pii_redaction_count: int