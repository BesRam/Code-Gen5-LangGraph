"""
Test Formatter Node:
Converts all valid and invalid test cases into Python unit test functions using pytest style.
"""

from typing import List
from langchain_core.runnables import Runnable
from agents.test_case_formatter_agent import TestCaseFormatterAgent

class TestFormatterNode(Runnable):
    def __init__(self):
        self.agent = TestCaseFormatterAgent()

    def invoke(self, input: dict, config: dict = None) -> dict:
        valid_test_cases = input.get("valid_test_cases", [])
        invalid_test_cases = input.get("invalid_test_cases", [])
    
        formatted_valid = self.agent.format_test_cases(valid_test_cases)
        formatted_invalid = self.agent.format_test_cases(invalid_test_cases)


        return {
            "formatted_valid_tests": formatted_valid,
            "formatted_invalid_tests": formatted_invalid
        }
