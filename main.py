# from graph import graph

# print("─" * 50)
# print("  LangGraph Workflow")
# print("─" * 50)
# print("  Normal prompt  : just type your question")
# print("  File review    : /file-review <path> | <question>")
# print("  Example        : /file-review C:\\docs\\report.pdf | what are the key findings?")
# print("─" * 50)

# topic = input("\nEnter your prompt: ").strip()

# result = graph.invoke({
#     "topic":                topic,
#     "attempts":             0,
#     "history":              [],
#     "command":              "",
#     "file_path":            "",
#     "file_question":        "",
#     "retrieved_chunks":     "",
#     "retrieval_scores":     [],
#     "file_already_embedded": False,
# })

# print("\n" + "─" * 50)
# print(f"  Final response (score: {result['avg_score']}/10)")
# print("─" * 50)
# print(result["response"])
# print(f"\n  Metrics  : {result['scores']}")
# print(f"  Attempts : {result['attempts']}")

# if result.get("retrieval_scores"):
#     print(f"  Chunk relevance scores : {result['retrieval_scores']}")

from graph import graph

print("  LangGraph Workflow")
print("─" * 30)
print("  Just type any question or topic")
print("  Include a file path to auto-trigger file review")
print("  Or use: /file-review <path> | <question>")
print("─" * 30)
print("  Examples:")
print("  > explain gradient descent")
print("  > summarize C:\\docs\\report.pdf")
print("  > what does main.py do?")
print("  > /file-review C:\\docs\\notes.txt | key points?")
print("─" * 30)

topic = input("\nEnter your prompt: ").strip()

result = graph.invoke({
    "topic":                 topic,
    "attempts":              0,
    "history":               [],
    "command":               "",
    "file_path":             "",
    "file_question":         "",
    "retrieved_chunks":      "",
    "retrieval_scores":      [],
    "file_already_embedded": False,
})

print("\n" + "─" * 30)
print(f"  Final response (score: {result['avg_score']}/10)")
print(f"  Mode     : {result['command']}")
print(f"  Attempts : {result['attempts']}")
print("─" * 30)
print(result["response"])
print(f"\n  Metrics : {result['scores']}")

if result.get("retrieval_scores"):
    print(f"  Chunk relevance scores : {result['retrieval_scores']}")