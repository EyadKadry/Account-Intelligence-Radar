import os
import requests
from dotenv import load_dotenv

load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

FIRECRAWL_ENDPOINT = "https://api.firecrawl.dev/v2/scrape"


def extract_company_data(urls):

    if not FIRECRAWL_API_KEY:
        raise ValueError("FIRECRAWL_API_KEY not found")

    schema = {
        "type": "object",
        "properties": {
            "headquarters": {"type": "string"},
            "business_units": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "source_url": {"type": "string"}
                    }
                }
            },
            "leadership": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "title": {"type": "string"},
                        "source_url": {"type": "string"}
                    }
                }
            },
            "strategic_initiatives": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "source_url": {"type": "string"}
                    }
                }
            }
        }
    }

    headers = {
        "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
        "Content-Type": "application/json"
    }

    all_results = []

    for url in urls:

        payload = {
            "url": url,
            "formats": [
                {
                    "type": "json",
                    "schema": schema
                }
            ]
        }

        response = requests.post(
            FIRECRAWL_ENDPOINT,
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            print("Firecrawl error:", response.text)
            continue

        data = response.json()

        all_results.append(data)

    return all_results