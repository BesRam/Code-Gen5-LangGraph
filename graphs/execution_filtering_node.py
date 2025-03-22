"""
Execution & Filtering Node:
Reusable node to run any list of codes against any set of test cases.
Filters out failing codes and returns execution report.
"""

from langchain_core.runnables import Runnable
from agents.execution_testing_agent import ExecutionTestingAgent

class ExecutionFilteringNode(Runnable):
    def __init__(self):
        self.agent = ExecutionTestingAgent()

    def invoke(self, state: dict, config: dict = None) -> dict:
        # Detect if this is second filtering phase (full test suite)
        is_second_pass = "filtered_codes" in state

        if is_second_pass:
            print("\n🔁 Phase 2: Running full test suite on previously filtered codes...")
            # ✅ Second phase: validate passed codes against ALL tests
            codes = state["filtered_codes"]
            test_suite = state.get("formatted_valid_tests", []) + state.get("formatted_invalid_tests", [])

            results, final_codes = self.agent.run_tests(codes, test_suite)

            # Determine if all failed again
            regenerate = len(final_codes) == 0

            return {
                "execution_report_final": results,
                "final_validated_codes": final_codes,
                "regenerate_code": regenerate,
                "regeneration_input": {
                    "failed_codes": codes,
                    "failure_reports": results
                }
            }

        else:
            print("\n🚦 Phase 1: Running initial filtering with selected complex test cases...")
            # ✅ First phase: test all generated codes against 2 selected tests
            codes = state["generated_codes"]
            valid_test = state.get("selected_valid_test", "")
            invalid_test = state.get("selected_invalid_test", "")
            test_suite = [valid_test, invalid_test]

            results, filtered = self.agent.run_tests(codes, test_suite)

            regenerate = len(filtered) == 0

            return {
                "execution_report": results,
                "filtered_codes": filtered,
                "regenerate_code": regenerate,
                "regeneration_input": {
                    "failed_codes": codes,
                    "failure_reports": results
                }
            }