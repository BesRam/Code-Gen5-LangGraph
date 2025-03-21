# scoring/scoring_agent.py

"""
Scoring & Ranking Agent (Final Combined Version):
Evaluates and ranks a list of Python code implementations based on multiple scoring strategies.
"""

from typing import List, Dict
from sentence_transformers import SentenceTransformer, util
from sklearn.preprocessing import MinMaxScaler

from scoring.strategies.complexity import ComplexityScoringStrategy
from scoring.strategies.llm_feedback import LLMFeedbackScoringStrategy
from scoring.strategies.test_coverage import TestCoverageScoringStrategy
from agents.elo_rating_agent import EloRatingAgent


class ScoringAndRankingAgent:
    def __init__(self, test_results: Dict[str, List[bool]] = None):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.elo_agent = EloRatingAgent()
        self.complexity_strategy = ComplexityScoringStrategy()
        self.llm_strategy = LLMFeedbackScoringStrategy()
        self.test_coverage_strategy = TestCoverageScoringStrategy(test_results or {})

    def score_codes(self, codes: List[str]) -> List[Dict]:
        # Initialize score containers
        scored_entries = []

        # === Core raw scores ===
        embeddings = self.embedding_model.encode(codes, convert_to_tensor=True)
        similarity_matrix = util.cos_sim(embeddings, embeddings)

        for i, code in enumerate(codes):
            scored_entries.append({
                "code_id": f"code_{i+1}",
                "code": code,
                "quality": self._score_quality(code),
                "similarity": float(similarity_matrix[i].mean())
            })

        # === Add scores from other strategies ===
        # Elo rating
        elo_scores = self.elo_agent.compute_elo_scores(codes)
        for i, entry in enumerate(scored_entries):
            entry["elo"] = elo_scores[i]

        # Complexity
        complexity_scores = self.complexity_strategy.score(codes)
        for i, entry in enumerate(scored_entries):
            entry["complexity"] = complexity_scores[i]

        # LLM Feedback
        llm_scores = self.llm_strategy.score(codes)
        for i, entry in enumerate(scored_entries):
            entry["llm_feedback"] = llm_scores[i]

        # Test Coverage
        coverage_scores = self.test_coverage_strategy.score(codes)
        for i, entry in enumerate(scored_entries):
            entry["test_coverage"] = coverage_scores[i]

        # === Normalize and compute total score ===
        scored_entries = self._normalize_and_rank(scored_entries)

        return sorted(scored_entries, key=lambda x: x["total_score"], reverse=True)

    def _score_quality(self, code: str) -> float:
        import re
        lines = code.strip().split("\n")
        comment_lines = len([line for line in lines if line.strip().startswith("#")])
        total_lines = len(lines)
        comment_ratio = comment_lines / total_lines if total_lines else 0
        has_docstring = bool(re.search(r'"""[\s\S]+?"""', code)) or bool(re.search(r"'''[\s\S]+?'''", code))
        return min(1.0, comment_ratio + (0.2 if has_docstring else 0))

    def _normalize_and_rank(self, scores: List[Dict]) -> List[Dict]:
        keys_to_normalize = ["quality", "similarity", "elo", "complexity", "llm_feedback", "test_coverage"]
        scalers = {key: MinMaxScaler() for key in keys_to_normalize}

        for key in keys_to_normalize:
            values = [[s[key]] for s in scores]
            try:
                normalized = scalers[key].fit_transform(values)
            except ValueError:
                normalized = [[0.5] for _ in values]
            for i, s in enumerate(scores):
                s[f"normalized_{key}"] = float(normalized[i])

        # Weighting: adjust as needed
        for s in scores:
            s["total_score"] = round((
                0.15 * s["normalized_quality"] +
                0.10 * s["normalized_similarity"] +
                0.20 * s["normalized_elo"] +
                0.15 * s["normalized_complexity"] +
                0.20 * s["normalized_llm_feedback"] +
                0.20 * s["normalized_test_coverage"]
            ), 4)

        return scores