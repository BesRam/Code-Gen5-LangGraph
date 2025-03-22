"""
Code Optimizer Node:
Takes the best code and evaluation summary to produce an improved version.
"""

from langchain_core.runnables import Runnable
from agents.code_optimizer_agent import CodeOptimizerAgent

class CodeOptimizerNode(Runnable):
    def __init__(self):
        self.agent = CodeOptimizerAgent()

    def invoke(self, state: dict, config: dict = None) -> dict:
        best_code = state.get("best_code", "")
        evaluation_summary = state.get("evaluation_summary", "")

        if not best_code:
            return {"optimized_code": ""}

        optimized = self.agent.optimize(best_code, evaluation_summary)

        return {
            "optimized_code": optimized
        }
