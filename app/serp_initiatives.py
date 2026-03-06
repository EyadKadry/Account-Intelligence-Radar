import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

MAX_RESULTS_PER_QUERY = 5


def discover_initiatives(company_name: str):
    """
    Discover press releases, partnerships, and strategic initiatives
    related to the company.
    """
    if not SERPAPI_KEY:
        raise ValueError("SERPAPI_API_KEY not found")

    queries = [
        f"{company_name} press release",
        f"{company_name} partnership",
        f"{company_name} AI transformation",
        f"{company_name} ERP implementation"
    ]

    collected_results = []

    for query in queries:
        params = {
            "q": query,
            "engine": "google",
            "api_key": SERPAPI_KEY,
            "num": MAX_RESULTS_PER_QUERY
        }

        response = requests.get("https://serpapi.com/search", params=params)

        if response.status_code != 200:
            continue  # لا نوقف النظام، الفشل وارد

        data = response.json()
        organic_results = data.get("organic_results", [])

        for result in organic_results:
            collected_results.append({
                "query": query,
                "title": result.get("title"),
                "url": result.get("link"),
                "snippet": result.get("snippet")
            })

    return collected_results