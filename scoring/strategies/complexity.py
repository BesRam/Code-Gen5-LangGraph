"""
Complexity Score Strategy:
Assigns a normalized score based on code structure complexity.
Lower complexity is rewarded.
"""

import re
from typing import List

class ComplexityScoringStrategy:
    def name(self) -> str:
        return "complexity"
    
    def score(self, codes: List[str]) -> List[float]:
        raw_scores = [self._compute_complexity(c) for c in codes]
    
        # Normalize using min-max to 0–1, then reverse (lower = better)
        min_c = min(raw_scores)
        max_c = max(raw_scores)
        if max_c - min_c == 0:
            return [0.5 for _ in raw_scores]
        
        return [1 - ((s - min_c) / (max_c - min_c)) for s in raw_scores]
    
    def _compute_complexity(self, code: str) -> float:
        lines = code.strip().split("\n")
        line_count = len(lines)

        # Count control flow keywords
        num_ifs = len(re.findall(r"\bif\b|\belif\b|\belse\b", code))
        num_loops = len(re.findall(r"\bfor\b|\bwhile\b", code))
        num_tries = len(re.findall(r"\btry\b|\bexcept\b", code))

        # Heuristic: weighted sum of structure elements
        complexity = (
            0.4 * line_count +
            1.5 * num_ifs +
            1.2 * num_loops +
            1.0 * num_tries
        )
        return complexity
    