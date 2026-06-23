from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


class WorkflowState(TypedDict):
    # core fields 
    topic: str        
    response: str        
    attempts: int       

    # validation fields 
    scores: dict       
    avg_score: float     
    feedback: str        

    # message history 
    history: Annotated[list, add_messages]

    # agent reasoning fields 
    tool_calls_made:  list    
    agent_scratchpad: str    