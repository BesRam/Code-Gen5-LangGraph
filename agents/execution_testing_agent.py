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

    def rename_test_functions(self, test_cases: List[str]) -> List[str]:
        """
        Renames all test functions to unique names (e.g. test_case_1, test_case_2, ...)
        to avoid naming collisions during pytest execution.
        """
        renamed_tests = []
        for i, tc in enumerate(test_cases):
            cleaned = self.clean_code_block(tc)
            renamed = re.sub(r"def test_\w+", f"def test_case_{i+1}", cleaned)
            renamed_tests.append(renamed)
        return renamed_tests

    def _extract_test_results(self, raw_output: str) -> List[bool]:
        """
        Parses pytest output to identify which test cases passed/failed.
        Simplified: assumes each line starting with "." = pass, "F" = fail.
        """
        if not raw_output:
            return []

        lines = raw_output.strip().splitlines()
        test_line = next((line for line in lines if set(line.strip()) <= set(".F")), "")
        return [c == "." for c in test_line.strip()] if test_line else []
    
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

        renamed_tests = self.rename_test_functions(test_cases)

        for i, raw_code in enumerate(codes):
            code_str = raw_code.content if hasattr(raw_code, "content") else raw_code
            cleaned_code = self.clean_code_block(code_str)
            full_code = f"{cleaned_code}\n\n" + "\n\n".join(renamed_tests)

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
                completed = None

            code_id = f"code_{i+1}"
            print(f"\n🔎 Testing {code_id}... {'✅ PASSED' if passed else '❌ FAILED'}")

            if completed:
                summary_lines = completed.stdout.strip().split("\n")
                print(f"--- Pytest Output for {code_id} ---")
                print("\n".join(summary_lines))

            results[code_id] = {
                "passed": passed,
                "report": completed.stdout.strip() if completed else "Test execution error",
                "code": cleaned_code,
                "individual_test_results": self._extract_test_results(completed.stdout if completed else "")
            }

            if passed:
                filtered_codes.append(cleaned_code)

            os.remove(test_file_path)

        print(f"\n✅ {len(filtered_codes)} out of {len(codes)} codes passed all tests.")
        return results, filtered_codes
