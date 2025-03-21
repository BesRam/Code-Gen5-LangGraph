from langchain.prompts import PromptTemplate

test_case_format_prompt = PromptTemplate.from_template("""
You are given a test case for the function `calculate_risk_weight()`.
                                                       
Your task is to generate a **pytest-style** test function based on this test case.

### Test Case:
{test_case}

### Instructions:
- Use Pythons `pytest` framework (no classes, just plain test functions).
- Name the test function starting with `test_case_` followed by a number.
- Extract **only the numeric value** inside `<riskweight></riskweight>` and assign it to `expected_output`.
- Convert `expected_output` to an **integer** if valid and otherwise as **string" when 'Invalid input value!'.
- Call `calculate_risk_weight()` using the provided input variables and values.
- Use a simple `assert` statement to compare the result with the expected output.
- Do **not** return any extra explanation or text — only the raw Python test function.

### Example Output:
```python
def test_case_1():
    input_variables
    expected_output = 50 or 'Invalid input value!' # The value between the tags <riskweight></riskweight>
    result = calculate_risk_weight(input_variables)
    assert result == expected_output
                                                       
""")