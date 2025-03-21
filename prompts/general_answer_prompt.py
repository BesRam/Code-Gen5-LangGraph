from langchain.prompts import PromptTemplate

# Prompt for answering general questions
general_answer_prompt = PromptTemplate.from_template("""
You are a helpful assistant. Answer the following general question in a clear and concise way.

### Question:
{user_input}
""")