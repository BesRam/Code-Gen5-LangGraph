import os
from dotenv import load_dotenv
from typing import Tuple
from langchain_openai import ChatOpenAI
from prompts.code_optimizer_prompt import optimize_prompt

load_dotenv()

class CodeOptimizerAgent:
    def __init__(self, model_name="gpt-4o", temperature=0.0):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def optimize(self, code: str, evaluation_summary: str) -> str:
        """
        Optimize the code based on its evaluation summary.

        Args:
            code (str): The original code implementation.
            evaluation_summary (str): Combined feedback and score summary.

        Returns:
            str: Optimized code.
        """
        prompt = optimize_prompt.format(
            code=code,
            evaluation_summary=evaluation_summary
        )
        response = self.llm.invoke(prompt)
        return response.content