"""
General Answer Node:
This node is triggered when the input is classified as a general question.
It uses an LLM to generate a helpful answer.
"""

from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable
from prompts.general_answer_prompt import general_answer_prompt
import os
from dotenv import load_dotenv

load_dotenv()

class GeneralAnswerNode(Runnable):
    def __init__(self, model_name="gpt-4o", temperature=0.0):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def invoke(self, input: dict, config: dict = None) -> dict:
        user_input = input.get("user_input", "")
        answer = self.llm.invoke(general_answer_prompt.format(user_input=user_input))

        return {
            "general_answer": answer.content.strip()
        }