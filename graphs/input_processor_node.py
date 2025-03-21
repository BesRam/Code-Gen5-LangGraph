# graphs/input_processor_node.py

"""
Input Processor Node:
Uses InputProcessingAgent to classify input as 'general' or 'code_request'.
"""

from typing import TypedDict, Literal, List
from langchain_core.runnables import Runnable
from agents.input_processing_agent import InputProcessingAgent

class InputProcessorOutput(TypedDict):
    request_type: Literal["general", "code_request"]
    user_input: str
    regulatory_text: str
    assumptions: str
    input_variables: str
    general_answer: str


class InputProcessorNode(Runnable):
    def __init__(self):
        self.input_agent = InputProcessingAgent()

    def invoke(self, input: dict, config: dict = None) -> InputProcessorOutput:
        user_input = input.get("user_input", "")
        result = self.input_agent.process_input(user_input)

        if result["request_type"] == "code_request":
            return {
                "request_type": "code_request",
                "user_input": user_input,
                "regulatory_text": result.get("regulatory_text", ""),
                "assumptions": result.get("assumptions", ""),
                "input_variables": result.get("input_variables", ""),
                "general_answer": ""
            }
        else:
            return {
                "request_type": "general",
                "user_input": user_input,
                "regulatory_text": "",
                "assumptions": "",
                "input_variables": "",
                "general_answer": ""
            }