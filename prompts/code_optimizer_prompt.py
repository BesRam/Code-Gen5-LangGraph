from langchain.prompts import PromptTemplate

# Prompt template
optimize_prompt = PromptTemplate.from_template("""
You are a code optimizer.

Improve the following Python function to maximize its clarity, readability, and correctness
without changing the logic or input/output behavior.

Consider the following evaluation feedback:
### Evaluation:
{evaluation_summary}

Here is the original code:
```python
{code}
```

---

Instructions:
- Improve structure, naming, formatting, and comments.
- Keep the same function signature and behavior.
- Do not return any explanations. Just return the full optimized code in a Python code block.

Your optimized function:
""")