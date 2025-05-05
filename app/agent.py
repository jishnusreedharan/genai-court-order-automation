from langgraph.graph import StateGraph, END
from app.state import AgentState
from app.ocr import extract_text_from_pdf
from app.extractor import extract_fields_with_llm
from app.utils import validate_customer, validate_action
from app.processor import process_action

def build_agent():
    graph = StateGraph(AgentState)

    def extract_fields(s): s.document_text = extract_text_from_pdf(s.file_path); f = extract_fields_with_llm(s.document_text); s.national_id, s.action = f.get("national_id"), f.get("action"); return s
    def check_customer(s): s.customer_id = validate_customer(s.national_id); s.outcome = "Customer not found" if not s.customer_id else ""; return s
    def check_action(s): s.outcome = f"Invalid action: {s.action}" if not validate_action(s.action) else ""; return s
    def execute(s): s.outcome = process_action(s.customer_id, s.action) if s.customer_id and s.action else s.outcome; return s

    graph.add_node("extract_fields", extract_fields)
    graph.add_node("check_customer", check_customer)
    graph.add_node("check_action", check_action)
    graph.add_node("execute", execute)

    graph.set_entry_point("extract_fields")
    graph.add_edge("extract_fields", "check_customer")
    graph.add_conditional_edges("check_customer", lambda s: not s.customer_id, {True: END, False: "check_action"})
    graph.add_conditional_edges("check_action", lambda s: "Invalid action" in (s.outcome or ""), {True: END, False: "execute"})
    graph.add_edge("execute", END)

    return graph.compile()
