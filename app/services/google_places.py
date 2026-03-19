import os
import requests

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

TEXT_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"


def search_places(query: str, max_results: int = 5):
    if not GOOGLE_MAPS_API_KEY:
        return []

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
        "X-Goog-FieldMask": (
            "places.displayName,"
            "places.formattedAddress,"
            "places.websiteUri,"
            "places.googleMapsUri"
        ),
    }

    body = {
        "textQuery": query,
        "maxResultCount": max_results,
    }

    try:
        response = requests.post(
            TEXT_SEARCH_URL,
            headers=headers,
            json=body,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        results = []
        for place in data.get("places", []):

            name = place.get("displayName", {}).get("text", "")
            website = place.get("websiteUri", "")
            maps_url = place.get("googleMapsUri", "")

            # FIX: fallback logic
            final_url = website if website else maps_url

            # Extra safety: avoid bad domains
            if final_url and "godaddy" in final_url.lower():
                final_url = maps_url

            results.append(
                {
                    "name": name,
                    "website": final_url,
                    "reason": f"Located at {place.get('formattedAddress', 'a nearby location')}",
                    "maps_url": maps_url,
                }
            )

        return results

    except Exception as e:
        print("Google Places error:", e)
        return []