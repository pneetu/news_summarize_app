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
    messages = [
        {
            "role": "system",
           "content": (
    "You are an AI assistant for kids activities and family-friendly local events. "
    "Give short, specific, practical answers. "
    "Prioritize nearby options, age-appropriate suggestions, and clear recommendations. "
    "Do not give broad generic advice. "
    "When possible, organize the answer as:\n"
    "1. Best options\n"
    "2. Why they fit\n"
    "3. Helpful next step\n"
    "If the user asks about a type of activity, answer directly with concrete examples."
),
        },
        {"role": "user", "content": request.question},
    ]

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
        tools=tools,
        temperature=0.3, 
    )

    message = response.choices[0].message

    if message.tool_calls:
        messages.append(message)

        for tool_call in message.tool_calls:
            try:
                tool_args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                tool_args = {}

            result = run_tool(
                tool_call.function.name,
                tool_args,
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )

        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
            temperature=0.3,
        )

    answer = response.choices[0].message.content or "Sorry, I couldn't generate a response."
    return {"answer": answer}