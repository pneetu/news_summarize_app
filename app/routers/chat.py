from fastapi import APIRouter
from pydantic import BaseModel
from app.tools.tool_definitions import tools
from app.tools.tool_runner import run_tool
import json
from openai import OpenAI
client = OpenAI()

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
async def chat(request: ChatRequest):

    messages = [ {
        "role": "system",
       "content": "You are an AI assistant for kids activities and family-friendly local events. Use tools when needed to fetch activity data or answer questions about activities."
    },
        {"role": "user", "content": request.question}
    ]

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
        tools=tools
    )

    message = response.choices[0].message

    if message.tool_calls:

        tool_call = message.tool_calls[0]

        result = run_tool(
            tool_call.function.name,
            json.loads(tool_call.function.arguments)
        )

        messages.append(message)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })

        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages
        )

    return {"answer": response.choices[0].message.content}