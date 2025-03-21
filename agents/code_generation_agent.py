"""
Code Generation Agent:
Generates Python code to compute risk weights based on Basel III regulatory text and assumptions.
"""

import os
from dotenv import load_dotenv
from typing import List
from langchain_openai import ChatOpenAI
from prompts.code_generation_prompt import code_gen_prompt

load_dotenv()

class CodeGenerationAgent:
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 1.0):
        """
        Initializes the code generation agent with an LLM.
        """
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def generate_code_variants(self, regulatory_text: str, assumptions: str, input_variables: List[str], count: int = 3) -> List[str]:
        """
        Generates multiple code implementations based on the same input.

        Args:
            regulatory_text (str): Basel III regulation section.
            assumptions (str): Domain assumptions.
            input_variables (List[str]): List of variable names in order.
            count (int): Number of code variants to generate.

        Returns:
            List[str]: A list of generated Python function strings.
        """
        generated_codes = []

        for _ in range(count):
            prompt = code_gen_prompt.format(
                regulatory_text=regulatory_text,
                assumptions=assumptions,
                input_variables=", ".join(input_variables)
            )
            response = self.llm.invoke(prompt)
            generated_codes.append(response)

        return generated_codes