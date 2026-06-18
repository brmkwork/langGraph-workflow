from graph import graph

topic = input("Enter your prompt: ").strip()
result = graph.invoke({
    "topic": topic,
    "attempts": 0,
    "history": [],
})

print(f"\nFinal response (score: {result['avg_score']}/10):")
print(result["response"])
print(f"\nMetrics: {result['scores']}")
print(f"Attempts taken: {result['attempts']}")