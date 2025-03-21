# Import the necessary module for creating structured prompts
from langchain.prompts import PromptTemplate

# Create a structured prompt template for generating Python code using LangChain
code_gen_prompt = PromptTemplate.from_template("""
Write a Python function which computes the risk weight for exposures according to the given regulatory text.
Users of this function will provide the input values required for determining the risk weight of the exposure.
                                               
Use the following instructions for writing the python function:
- Instruction 1: Always comment the code of the python function (including input variables and values), so that it is clear to the user what the code does.
- Instruction 2: The output should be an integer representing the risk weight (e.g., 20, 100) or a string "Invalid input value!" if the python function fails to assign a risk weight for the given input.

For creating the python function, use only these variables as input variables with this precise order:
### Input Variables: 
{input_variables}

Furthermore, for creating the python function make the following assumptions:
### Assumptions:
{assumptions}

Here is the regulatory text:
### Regulatory Text: 
{regulatory_text}

Start the python function with:
### Function Declaration:
```python
def calculate_risk_weight(...):

Provide only the Code without any explanation or text.
""")