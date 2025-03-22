"""
LangGraph Workflow:
This graph handles branching based on whether the input is a general question or a Basel III code request.
"""

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from graphs.input_processor_node import InputProcessorNode
from graphs.general_answer_node import GeneralAnswerNode
from graphs.code_generation_node import CodeGenerationNode
from graphs.test_generation_node import TestGenerationNode
from graphs.test_formatter_node import TestFormatterNode
from graphs.human_test_selector_node import HumanTestSelectorNode
from graphs.execution_filtering_node import ExecutionFilteringNode

# Define shared state
class WorkflowState(dict):
    user_input: str
    request_type: str
    general_answer: str
    regulatory_text: str
    assumptions: str
    input_variables: str
    generated_codes: list
    valid_test_cases: list
    invalid_test_cases: list
    formatted_valid_tests: list
    formatted_invalid_tests: list
    selected_valid_test: str
    selected_invalid_test: str
    filtered_codes: list
    final_validated_codes: list
    execution_report: dict
    execution_report_final: dict
    regenerate_code: bool
    regeneration_input: dict

# Step 1: Initialize nodes
input_processor_node = InputProcessorNode()
general_answer_node = GeneralAnswerNode()
code_generation_node = CodeGenerationNode()
test_generation_node = TestGenerationNode()
test_formatter_node = TestFormatterNode()
human_test_selector_node = HumanTestSelectorNode()
execution_filtering_node = ExecutionFilteringNode()

# Step 2: Define graph
workflow = StateGraph(WorkflowState)

workflow.add_node("input_processor", input_processor_node)
workflow.add_node("generate_general_answer", general_answer_node)
workflow.add_node("code_generation_node", code_generation_node)
workflow.add_node("test_generation", test_generation_node)
workflow.add_node("test_formatter", test_formatter_node)
workflow.add_node("select_complex_tests", human_test_selector_node)
workflow.add_node("execution_filtering", execution_filtering_node)
workflow.add_node("execution_filtering_all", ExecutionFilteringNode())

def route_request_type(state: dict):
    if state["request_type"] == "general":
        return "general_answer"
    else:
        return "code_generation"
    
# Step 4: Define edges
workflow.set_entry_point("input_processor")
workflow.add_conditional_edges(
    "input_processor",
    route_request_type,
    {
        "general_answer": "generate_general_answer",
        "code_generation": "code_generation_node"
    }
)
workflow.add_edge("generate_general_answer", END)
workflow.add_edge("code_generation_node", "test_generation")
workflow.add_edge("test_generation", "test_formatter")
workflow.add_edge("test_formatter", "select_complex_tests")
workflow.add_edge("select_complex_tests", "execution_filtering")

# Phase 1: Filtering with selected test cases
workflow.add_conditional_edges(
    "execution_filtering",
    lambda state: "regenerate_code" if state.get("regenerate_code") else "continue",
    {
        "regenerate_code": "code_generation_node",
        "continue": "execution_filtering_all"
    }
)

# Phase 2: Filtering with full test suite
workflow.add_conditional_edges(
    "execution_filtering_all",
    lambda state: "regenerate_code" if state.get("regenerate_code") else "end",
    {
        "regenerate_code": "code_generation_node",
        "end": END
    }
)

# Step 5: Compile the graph
app = workflow.compile()

# Step 6: Expose only final formatted test output for display
def run_workflow(user_input: str):
    final_state = app.invoke({"user_input": user_input})

    if final_state.get("final_validated_codes"):
        print("\n✅ Final Validated Codes:")
        for i, code in enumerate(final_state["final_validated_codes"], start=1):
            print(f"\nCode {i} (PASSED ALL TESTS):\n\n{code}\n")
        print(f"\n✅ Total Passed Codes: {len(final_state['final_validated_codes'])}")
    else:
        print("\n❌ No code passed all test cases.")

    return final_state