from langchain.prompts import PromptTemplate

# Prompt for classifying and extracting user input
input_processing_prompt = PromptTemplate.from_template("""
You are a classification and extraction agent.

Your job is to analyze the following user input and determine:
1. If it is a general question → classify as "general".
2. If it is a code generation request → classify as "code_request".

If it is a code_request, extract the following:
- regulatory_text: the Basel III regulation section
- assumptions: the assumptions provided by the user
- input_variables: variables mentioned that should be used as input to a function

### User Input:
{user_input}

### Output Format (in JSON):
  "request_type": "...",            // "general" or "code_request"
  "regulatory_text": "...",         // required if code_request
  "assumptions": "...",             // required if code_request
  "input_variables": "..."        // required if code_request
Only return the JSON, nothing else.
""")