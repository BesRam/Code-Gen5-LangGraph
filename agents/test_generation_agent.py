"""
Test Generation Agent:
Generates either valid or invalid test cases based on the Basel III regulatory text and assumptions.
Uses a structured prompt and LLM to generate 10 test case examples as text with <riskweight> tags.
"""

import os
from dotenv import load_dotenv
from typing import List
from langchain_openai import ChatOpenAI
from prompts.test_case_prompt import test_case_prompt

load_dotenv()

class TestGenerationAgent:
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 1.0):
        """
        Initializes the agent with an OpenAI model.
        """
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    def generate_test_cases(
        self,
        regulatory_text: str,
        assumptions: str,
        input_variables: str,
        test_type: str = "valid",  # or "invalid"
        count: int = 10
    ) -> List[str]:
        
        """
        Generates test cases (valid or invalid) as text examples.

        Args:
            regulatory_text (str): Basel III regulation section.
            assumptions (str): Context assumptions.
            input_variables (List[str]): Input variable names.
            test_type (str): "valid" or "invalid".
            count (int): Number of test cases to generate.

        Returns:
            List[str]: A list of generated test case strings with <riskweight> tag.
        """

        test_cases = []

        for _ in range(count):
            prompt = test_case_prompt.format(
                regulatory_text=regulatory_text,
                assumptions=assumptions,
                test_type=test_type,
                input_variables=input_variables
            )
            response = self.llm.invoke(prompt)
            test_cases.append(response)

        return test_cases