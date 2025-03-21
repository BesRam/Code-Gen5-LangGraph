"""
Test Generation Node:
Generates 10 valid and 10 invalid test cases in parallel using the TestGenerationAgent.
"""

from typing import List
from langchain_core.runnables import Runnable
from agents.test_generation_agent import TestGenerationAgent

class TestGenerationNode(Runnable):
    def __init__(self):
        self.agent = TestGenerationAgent()
    
    def invoke(self, input: dict, config: dict = None) -> dict:
        regulatory_text = input.get("regulatory_text", "")
        assumptions = input.get("assumptions", "")
        input_variables = input.get("input_variables", "")

        valid_test_cases: List[str] = self.agent.generate_test_cases(
            regulatory_text=regulatory_text,
            assumptions=assumptions,
            input_variables=input_variables,
            test_type="valid",
            num_cases=10
        )

        invalid_test_cases: List[str] = self.agent.generate_test_cases(
            regulatory_text=regulatory_text,
            assumptions=assumptions,
            input_variables=input_variables,
            test_type="invalid",
            num_cases=10
        )

        return {
            "valid_test_cases": valid_test_cases,
            "invalid_test_cases": invalid_test_cases
        }