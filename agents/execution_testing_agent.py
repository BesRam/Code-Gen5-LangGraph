# agents/execution_testing_agent.py

"""
Execution & Testing Agent:
Executes each generated Python function against all formatted test cases (pytest-style).
Filters out code that fails any test.
"""

import os
import tempfile
import subprocess
from typing import List, Dict, Tuple
import re


class ExecutionTestingAgent:
    def __init__(self):
        pass

    def clean_code_block(self, code: str) -> str:
        """
        Removes ```python and ``` markers from code blocks.

        Args:
            code (str): Raw code string from LLM.

        Returns:
            str: Cleaned code string.
        """
        return re.sub(r"```(?:python)?|```", "", code).strip()

    def run_tests(self, codes: List[str], test_cases: List[str]) -> Tuple[Dict[str, bool], List[str]]:
        """
        Runs all test cases against each code snippet individually.

        Args:
            codes (List[str]): List of generated Python functions.
            test_cases (List[str]): List of pytest-style test functions.

        Returns:
            Tuple:
                - results: Dict mapping code IDs to pass/fail.
                - filtered_codes: List of codes that passed all tests.
        """
        results = {}
        filtered_codes = []

        for i, raw_code in enumerate(codes):
            cleaned_code = self.clean_code_block(raw_code)
            full_code = f"{cleaned_code}\n\n" + "\n\n".join([self.clean_code_block(tc) for tc in test_cases])

            with tempfile.NamedTemporaryFile(suffix="_test.py", delete=False, mode="w") as f:
                f.write(full_code)
                test_file_path = f.name

            try:
                completed = subprocess.run(
                    ["pytest", test_file_path, "--tb=short", "-q"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                passed = completed.returncode == 0
            except Exception:
                passed = False

            code_id = f"code_{i+1}"
            passed = completed.returncode == 0
            results[code_id] = {
                "passed": passed,
                "report": completed.stdout.strip(),
                "code": cleaned_code
            }

            if passed:
                filtered_codes.append(cleaned_code)

            os.remove(test_file_path)

        return results, filtered_codes
