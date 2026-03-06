import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)


def fuse_company_intelligence(company_name, objective, extracted_data):

    prompt = f"""
You are an expert business analyst.

Your task is to merge multiple extracted data results
into a single structured company intelligence report.

Company:
{company_name}

Objective:
{objective}

Rules:
- Merge duplicate items
- Prefer official sources
- Do not invent information
- If information is missing return null
- Preserve source_url as evidence
- Return JSON only

Extracted data:
{json.dumps(extracted_data, indent=2)}

Output schema:

{{
  "company_identifiers": {{
    "name": "...",
    "headquarters": "..."
  }},
  "business_snapshot": {{
    "business_units": [],
    "products_services": [],
    "target_industries": []
  }},
  "leadership_signals": [
    {{
      "name": "...",
      "title": "...",
      "source_url": "..."
    }}
  ],
  "strategic_initiatives": [
    {{
      "name": "...",
      "description": "...",
      "source_url": "..."
    }}
  ],
  "evidence": [
    "url1",
    "url2"
  ]
}}
"""

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(
        f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        raise RuntimeError(response.text)

    data = response.json()

    text_output = data["candidates"][0]["content"]["parts"][0]["text"]

    cleaned = text_output.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "")
        cleaned = cleaned.replace("```", "")
        cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except Exception as e:
        print("\nLLM raw output:\n")
        print(text_output)
        raise e