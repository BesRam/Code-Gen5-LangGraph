"""
LangGraph Workflow:
This graph handles branching based on whether the input is a general question or a Basel III code request.
"""

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

from graphs.input_processor_node import InputProcessorNode
from graphs.general_answer_node import GeneralAnswerNode

# Define shared state
class WorkflowState(dict):
    user_input: str
    request_type: str
    general_answer: str
    regulatory_text: str
    assumptions: str
    input_variables: str

# Step 1: Initialize nodes
input_processor_node = InputProcessorNode()
general_answer_node = GeneralAnswerNode()

# Step 2: Define graph
workflow = StateGraph(WorkflowState)

workflow.add_node("input_processor", input_processor_node)
workflow.add_node("generate_general_answer", general_answer_node)

def route_request_type(state: dict):
    if state["request_type"] == "general":
        return "general_answer"
    else:
        return "code_generation"  # To be added later
    
# Step 4: Define edges
workflow.set_entry_point("input_processor")
workflow.add_conditional_edges(
    "input_processor",
    route_request_type,
    {
        "general_answer": "generate_general_answer",
        "code_generation": END  # placeholder for now
    }
)

# Step 5: Compile the graph
app = workflow.compile()