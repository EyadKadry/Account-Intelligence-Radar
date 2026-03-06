import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

def find_official_website(company_name: str):
    """
    Step 1: Discover the official website of the company
    """
    
    if not SERPAPI_KEY:
        raise ValueError("SERPAPI_API_KEY not found in environment variables")
    
    query = f"{company_name} official website"
    
    params = {
        "q" : query,
        "engine" : "google",
        "api_key" : SERPAPI_KEY,
        "num" : 5
    }
    
    response = requests.get("https://serpapi.com/search", params=params)
    
    if response.status_code !=200:
        raise RuntimeError(f"SerpAPI request failed with status {response.status_code}")
    
    data = response.json()
    
    organic_results = data.get("organic_results", [])

    if not organic_results:
        return None

    top_result = organic_results[0]

    return {
        "title": top_result.get("title"),
        "url": top_result.get("link"),
        "snippet": top_result.get("snippet")
    }