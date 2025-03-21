from langchain.prompts import PromptTemplate

test_case_prompt = PromptTemplate.from_template("""
You are given a regulatory text, and I want you to compute the risk weight for the given input values using the regulatory text.
Your task is to generate a {test_type} test case that will be used to evaluate the function `calculate_risk_weight()`.
                                                
The output should be:
- an integer representing the corresponding risk weight (e.g., 20, 100)
- or the string “Invalid input value!” if the test case is invalid
                                                
### Test Type:
{test_type}  # valid or invalid

Here is the regulatory text:
{regulatory_text}

Here are the assumptions for the input values:
{assumptions}

Here are the input values:
{input_variables}

Please generate one test case and output it in the following format:
1. Provide input values (Python-style variable assignments)
2. Use <riskweight></riskweight> tags to wrap the expected result
                                                

Think step-by-step to ensure accurate assignment of the risk weight.
""")