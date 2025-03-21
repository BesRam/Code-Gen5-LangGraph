"""
Elo Rating Agent using Cross-Encoder similarity for pairwise ranking of code snippets.
"""

from typing import List, Tuple
from sentence_transformers import CrossEncoder
import numpy as np
import itertools

class EloRatingAgent:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2", k: int = 32):
        self.model = CrossEncoder(model_name)
        self.k = k  # Elo update factor

    def initialize_ratings(self, codes: List[str]) -> List[float]:
        return [1000.0 for _ in codes]
    
    def _expected_score(self, r1, r2):
        return 1 / (1 + 10 ** ((r2 - r1) / 400))
    
    def _update_rating(self, r1, r2, outcome):
        expected_r1 = self._expected_score(r1, r2)
        new_r1 = r1 + self.k * (outcome - expected_r1)
        return new_r1
    
    def compute_elo_scores(self, codes: List[str]) -> List[float]:
        n = len(codes)
        ratings = self.initialize_ratings(codes)

        # Create all pairwise combinations
        pairs = list(itertools.combinations(range(n), 2))

        for i, j in pairs:
            c1, c2 = codes[i], codes[j]
            score = self.model.predict([(c1, c2)])[0]

            # Interpret score: > 0.5 → c1 wins, < 0.5 → c2 wins, == 0.5 → draw
            if score > 0.5:
                outcome_i, outcome_j = 1, 0
            elif score < 0.5:
                outcome_i, outcome_j = 0, 1
            else:
                outcome_i = outcome_j = 0.5

            new_i = self._update_rating(ratings[i], ratings[j], outcome_i)
            new_j = self._update_rating(ratings[j], ratings[i], outcome_j)

            ratings[i] = new_i
            ratings[j] = new_j

        return ratings