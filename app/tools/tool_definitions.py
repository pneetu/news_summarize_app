tools = [
    {
        "type": "function",
        "function": {
           "name": "get_activity_data", 
            "description": "Get recent kids activities and family-friendly local events",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {"type": "integer"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "rag_answer",
            "description": "Answer questions about kids activities and local family events using retrieved context",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"}
                },
                "required": ["question"]
            }
        }
    }
]