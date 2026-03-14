from dotenv import load_dotenv
load_dotenv()

import feedparser
from openai import OpenAI

FEEDS = [
    "https://news.google.com/rss/search?q=kids+activities+bay+area&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=family+events+sunnyvale&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=children%27s+museum+events+san+jose&hl=en-US&gl=US&ceid=US:en",
]

MAX_ARTICLES = 10

client = OpenAI()


def fetch_activity_items():
    items = []

    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = getattr(entry, "title", "").strip()
            link = getattr(entry, "link", "").strip()
            published = getattr(entry, "published", "").strip()

            if title and link:
                items.append((title, link, published))

    seen = set()
    unique = []
    for t, l, p in items:
        if l in seen:
            continue
        seen.add(l)
        unique.append((t, l, p))

    return unique[:MAX_ARTICLES]


def summarize_activity_titles(titles):
    prompt = (
        "Summarize these kids activities and family-friendly events. Prefer activities near the user's area if a location is mentioned.\n\n"
        + "\n".join([f"- {t}" for t in titles])
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You summarize kids activities and family-friendly local events clearly. Highlight variety, location, and why the activity may be good for children."
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()


def get_activity_data(limit: int = 10, include_summary: bool = True):
    activities = fetch_activity_items()[:limit]
    titles = [t for (t, _, _) in activities]
    summary = summarize_activity_titles(titles) if include_summary else ""

    articles = []
    for title, link, published in activities:
        articles.append(
            {
                "title": title,
                "url": link,
                "published": published,
            }
        )

    return {"articles": articles, "summary": summary}


def chat_activity_assistant(question: str) -> str:
    if not question.strip():
        return "Please enter a question."

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You help parents and families find kids activities, local events, and family-friendly outings. Give practical, clear suggestions and prefer nearby options when a location is mentioned."
            },
            {"role": "user", "content": question},
        ],
        temperature=0.3,
    )
    return resp.choices[0].message.content.strip()


def main():
    activities = fetch_activity_items()

    if not activities:
        print("No activities found.")
        return

    print("\n==============================")
    print("📰 Latest Activities near your area")
    print("==============================\n")

    for i, (title, link, published) in enumerate(activities, 1):
        when = f" ({published})" if published else ""
        print(f"{i}. {title}{when}")
        print(f"   {link}\n")

    titles = [t for (t, _, _) in activities]

    print("\n==============================")
    print("🤖 Kids Activities Summary")
    print("==============================\n")
    summary = summarize_activity_titles(titles)
    print(summary)


if __name__ == "__main__":
    main()