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

# Step 1: Initialize nodes
input_processor_node = InputProcessorNode()
general_answer_node = GeneralAnswerNode()
code_generation_node = CodeGenerationNode()
test_generation_node = TestGenerationNode()

# Step 2: Define graph
workflow = StateGraph(WorkflowState)

workflow.add_node("input_processor", input_processor_node)
workflow.add_node("generate_general_answer", general_answer_node)
workflow.add_node("code_generation_node", code_generation_node)
workflow.add_node("test_generation", test_generation_node)

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
workflow.add_edge("test_generation", END)

# Step 5: Compile the graph
app = workflow.compile()