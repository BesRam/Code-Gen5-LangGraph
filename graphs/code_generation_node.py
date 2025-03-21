from typing import List
from langchain_core.runnables import Runnable
from agents.code_generation_agent import CodeGenerationAgent

class CodeGenerationNode(Runnable):
    def __init__(self):
        self.agent = CodeGenerationAgent()
    
    def invoke(self, input: dict, config: dict = None) -> dict:
        regulatory_text = input.get("regulatory_text", "")
        assumptions = input.get("assumptions", "")
        input_variables = input.get("input_variables", "")

        codes: List[str] = self.agent.generate_code_variants(
            regulatory_text=regulatory_text,
            assumptions=assumptions,
            input_variables=input_variables,
            num_variants=10
        )

        return {"generated_codes": codes}