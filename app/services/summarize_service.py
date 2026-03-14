async def summarize_activity_topic(topic: str, max_articles: int = 5) -> dict:

    return {
        "topic": topic,
        "summary": f"Here are some family-friendly activity ideas related to {topic}.",
        "activities": []
    }