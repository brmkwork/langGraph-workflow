SCORE_PROMPT = """
You are a strict quality evaluator. Score the response on each metric from 0 to 10.
Return ONLY a JSON object with this exact shape:
{{
  "relevance": <0-10>,
  "accuracy":  <0-10>,
  "clarity":   <0-10>,
  "depth":     <0-10>,
  "feedback":  "<one sentence on the biggest weakness>"
}}

Topic: {topic}
Response: {response}
"""