import os
from dotenv import load_dotenv
from typing import List
from langchain_openai import ChatOpenAI
from prompts.test_case_format_prompt import test_case_format_prompt

load_dotenv()

class TestCaseFormatterAgent:
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0.0):
        """
        Initializes the agent for formatting test cases into pytest format.
        """
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    def format_test_cases(self, raw_test_cases: List[str]) -> List[str]:
        """
        Formats a list of test case strings into pytest functions.

        Args:
            raw_test_cases (List[str]): List of test case strings (with <riskweight>).

        Returns:
            List[str]: Formatted pytest-style test functions.
        """
        formatted_tests = []

        for idx, raw_test_case in enumerate(raw_test_cases, start=1):
            prompt = test_case_format_prompt.format(test_case=raw_test_case)
            response = self.llm.invoke(prompt)
            formatted_tests.append(response.content)

        return formatted_tests