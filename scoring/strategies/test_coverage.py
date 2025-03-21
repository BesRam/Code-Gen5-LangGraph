"""
Test Coverage Scoring Strategy:
Scores each code based on how many test cases it passed.
"""

from typing import List, Dict

class TestCoverageScoringStrategy:
    def __init__(self, test_results: Dict[str, List[bool]]):
        """
        Args:
            test_results: A dictionary like:
              {
                  "code_1": [True, True, False],
                  "code_2": [True, True, True],
                  ...
              }
        """
        self.test_results = test_results
    
    def name(self) -> str:
        return "test_coverage"
    
    def score(self, codes: List[str]) -> List[float]:
        """
        Scores codes by their test pass ratio (0.0 - 1.0)

        Args:
            codes (List[str]): The actual code list, used to determine order.

        Returns:
            List[float]: Test coverage score per code.
        """
        scores = []

        for idx in range(len(codes)):
            code_id = f"code_{idx+1}"
            results = self.test_results.get(code_id, [])
            if not results:
                scores.append(0.0)
            else:
                ratio = sum(results) / len(results)
                scores.append(round(ratio, 4))

        return scores
    