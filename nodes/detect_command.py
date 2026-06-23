# # from state import WorkflowState
# # from logger import log

# # def detect_command(state: WorkflowState) -> dict:
# #     topic = state["topic"].strip()

# #     if topic.startswith("/file-review"):
# #         remainder = topic.replace("/file-review", "", 1).strip()

# #         if "|" in remainder:
# #             file_path, file_question = remainder.split("|", 1)
# #             file_path     = file_path.strip()
# #             file_question = file_question.strip()
# #         else:
# #             file_path     = remainder.strip()
# #             file_question = "Summarize the document and highlight the key points"

# #         log("DETECT COMMAND", "File review command detected", {
# #             "file_path":     file_path,
# #             "file_question": file_question,
# #             "route":         "retrieve → generate → validate",
# #         })

# #         return {
# #             "command":       "file-review",
# #             "file_path":     file_path,
# #             "file_question": file_question,
# #         }

# #     log("DETECT COMMAND", "Normal prompt detected", {
# #         "topic": topic,
# #         "route": "generate → validate",
# #     })

# #     return {
# #         "command":       "normal",
# #         "file_path":     "",
# #         "file_question": "",
# #     }

# import os
# import re
# from state import WorkflowState
# from logger import log

# # file extensions to detect automatically
# FILE_EXTENSIONS = [
#     ".pdf", ".txt", ".md", ".docx", ".xlsx", ".xls",
#     ".csv", ".pptx", ".ppt", ".html", ".htm", ".json",
#     ".py", ".js", ".ts", ".java", ".c", ".cpp", ".go",
# ]

# # intent keywords that suggest the user wants file analysis
# INTENT_KEYWORDS = [
#     "review", "summarize", "summary", "read", "analyze", "analyse",
#     "what does this file", "go through", "check this", "look at this",
#     "explain this file", "what is in", "contents of", "tell me about this",
# ]

# # regex to detect file paths 
# FILE_PATH_PATTERN = re.compile(
#     r'([A-Za-z]:\\[\w\\\s\-\.]+|\/[\w\/\-\.]+|[\w\-]+\.\w{2,5})'
# )


# def extract_file_path(topic: str) -> str | None:
#     """Pulls the first file path found in the topic string."""
#     matches = FILE_PATH_PATTERN.findall(topic)
#     for match in matches:
#         ext = os.path.splitext(match)[1].lower()
#         if ext in FILE_EXTENSIONS:
#             return match.strip()
#     return None


# def extract_question(topic: str, file_path: str) -> str:
#     """Removes the file path from the topic to get the actual question."""
#     question = topic.replace(file_path, "").strip(" ,.|")
#     # clean up leftover command prefix
#     question = re.sub(r"^/file-review\s*", "", question).strip()
#     if not question:
#         return "Summarize the document and highlight the key points"
#     return question


# def has_file_intent(topic: str) -> bool:
#     """Checks if the topic contains keywords suggesting file analysis."""
#     topic_lower = topic.lower()
#     return any(keyword in topic_lower for keyword in INTENT_KEYWORDS)


# def detect_command(state: WorkflowState) -> dict:
#     topic = state["topic"].strip()

#     #Explicit command: /file-review
#     if topic.startswith("/file-review"):
#         remainder = topic.replace("/file-review", "", 1).strip()

#         if "|" in remainder:
#             file_path, file_question = remainder.split("|", 1)
#             file_path     = file_path.strip()
#             file_question = file_question.strip()
#         else:
#             file_path     = remainder.strip()
#             file_question = "Summarize the document and highlight the key points"

#         log("DETECT COMMAND", "Explicit /file-review command", {
#             "file_path":     file_path,
#             "file_question": file_question,
#             "route":         "retrieve → generate → validate",
#         })

#         return {
#             "command":       "file-review",
#             "file_path":     file_path,
#             "file_question": file_question,
#         }

#     #Auto detect: file path found in topic 
#     file_path = extract_file_path(topic)

#     if file_path and os.path.exists(file_path):
#         file_question = extract_question(topic, file_path)

#         log("DETECT COMMAND", "Auto-detected file path in prompt", {
#             "file_path":     file_path,
#             "file_question": file_question,
#             "route":         "retrieve → generate → validate",
#         })

#         return {
#             "command":       "file-review",
#             "file_path":     file_path,
#             "file_question": file_question,
#         }

#     #Auto detect: intent keywords found but no valid path
#     if file_path and not os.path.exists(file_path):
#         log("DETECT COMMAND", "File path found but does not exist", {
#             "attempted_path": file_path,
#             "route":          "normal → generate",
#         })

#     if has_file_intent(topic) and not file_path:
#         log("DETECT COMMAND", "File intent detected but no file path found — routing normal", {
#             "topic": topic,
#             "hint":  "include a file path in your prompt",
#         })

#     #Default: normal prompt 
#     log("DETECT COMMAND", "Normal prompt", {
#         "topic":    topic,
#         "route":    "generate → validate",
#     })

#     return {
#         "command":       "normal",
#         "file_path":     "",
#         "file_question": "",
#     }