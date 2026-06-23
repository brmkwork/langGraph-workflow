from dotenv import load_dotenv
load_dotenv()

from graph import graph
from skills import get_skill_names, get_guardrail_names

print(f"\nAgent ready | skills: {get_skill_names()} | guardrails: {get_guardrail_names()}")
print("Include a file path to trigger file review. Ctrl+C to exit.\n")

topic = input("You: ").strip()

if not topic:
    print("No input provided.")
else:
    result = graph.invoke({
        "topic":            topic,
        "response":         "",
        "attempts":         0,
        "scores":           {},
        "avg_score":        0.0,
        "feedback":         "",
        "history":          [],
        "tool_calls_made":  [],
        "agent_scratchpad": "",
    })

    print(f"\nAgent: {result['response']}")
    print(f"\nscore={result['avg_score']} | attempts={result['attempts']} | tools={', '.join(result.get('tool_calls_made', [])) or 'none'} | metrics={result['scores']}")