"""
Human-in-the-Loop Test Selector Node:
Displays all formatted valid and invalid test cases and allows a human to select the most complex ones.
"""

from langchain_core.runnables import Runnable

class HumanTestSelectorNode(Runnable):
    def invoke(self, state: dict, config: dict = None) -> dict:
        valid_tests = state.get("formatted_valid_tests", [])
        invalid_tests = state.get("formatted_invalid_tests", [])

        print("\n✅ Select the most complex VALID test case:")
        for idx, test in enumerate(valid_tests):
            print(f"\n[{idx}]\n{test}\n")

        selected_valid_idx = int(input("Enter the index of the most complex VALID test case: "))

        print("\n🚫 Select the most complex INVALID test case:")
        for idx, test in enumerate(invalid_tests):
            print(f"\n[{idx}]\n{test}\n")

        selected_invalid_idx = int(input("Enter the index of the most complex INVALID test case: "))

        return {
            "selected_valid_test": valid_tests[selected_valid_idx],
            "selected_invalid_test": invalid_tests[selected_invalid_idx]
        }