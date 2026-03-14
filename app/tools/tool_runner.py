from activities import get_activity_data
from rag.rag_news import rag_answer

def run_tool(name, args):
    if name == "get_activity_data":
        return get_activity_data(**args)

    if name == "rag_answer":
        return rag_answer(**args)

    raise ValueError("Unknown tool")