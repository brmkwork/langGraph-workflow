from state import WorkflowState
from logger import log

def detect_command(state: WorkflowState) -> dict:
    topic = state["topic"].strip()

    if topic.startswith("/file-review"):
        remainder = topic.replace("/file-review", "", 1).strip()

        if "|" in remainder:
            file_path, file_question = remainder.split("|", 1)
            file_path     = file_path.strip()
            file_question = file_question.strip()
        else:
            file_path     = remainder.strip()
            file_question = "Summarize the document and highlight the key points"

        log("DETECT COMMAND", "File review command detected", {
            "file_path":     file_path,
            "file_question": file_question,
            "route":         "retrieve → generate → validate",
        })

        return {
            "command":       "file-review",
            "file_path":     file_path,
            "file_question": file_question,
        }

    log("DETECT COMMAND", "Normal prompt detected", {
        "topic": topic,
        "route": "generate → validate",
    })

    return {
        "command":       "normal",
        "file_path":     "",
        "file_question": "",
    }