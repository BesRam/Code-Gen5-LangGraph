from langchain_core.runnables import Runnable
from agents.scoring_agent import ScoringAndRankingAgent

class ScoringNode(Runnable):
    def __init__(self):
        self.agent = ScoringAndRankingAgent()
    
    def invoke(self, state: dict, config: dict = None) -> dict:
        codes = state.get("final_validated_codes", [])

        if not codes:
            return {"scoring_results": [], "best_code": None}
        
        # Score and rank all codes
        ranked = self.agent.score_codes(codes)

        best_code_entry = ranked[0] if ranked else None

        return {
            "scoring_results": ranked,
            "best_code": best_code_entry["code"] if best_code_entry else None
        }