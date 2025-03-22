from langchain_core.runnables import Runnable
from agents.scoring_agent import ScoringAndRankingAgent

class ScoringNode(Runnable):
    def __init__(self):
        self.agent = None  # Delay init

    def invoke(self, state: dict, config: dict = None) -> dict:
        codes = state.get("final_validated_codes", [])
        test_report = state.get("execution_report_final", {})

        if not codes:
            return {
                "scoring_results": [],
                "best_code": None,
                "evaluation_summary": ""
            }

        # Extrahiere Teststatus aus Report (code_1 → True/False pro Test)
        test_results = {}
        for code_id, data in test_report.items():
            test_results[code_id] = data.get("individual_test_results", [])

        # Übergib test_results an den Agenten
        self.agent = ScoringAndRankingAgent(test_results)

        # Score und ranke
        ranked = self.agent.score_codes(codes)

        best_code_entry = ranked[0] if ranked else None

        summary_lines = []
        for entry in ranked:
            summary_lines.append(f"Code ID: {entry['code_id']}")
            summary_lines.append(f"- Total Score: {entry['total_score']}")
            summary_lines.append(f"- Quality: {entry['quality']:.2f}, Elo: {entry['elo']}, LLM Feedback: {entry['llm_feedback']}")
            summary_lines.append(f"- Test Coverage: {entry['test_coverage']}, Complexity: {entry['complexity']}, Similarity: {entry['similarity']:.2f}")
            summary_lines.append("")

        evaluation_summary = "\n".join(summary_lines)

        return {
            "scoring_results": ranked,
            "best_code": best_code_entry["code"] if best_code_entry else None,
            "evaluation_summary": evaluation_summary
        }