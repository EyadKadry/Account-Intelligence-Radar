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

MAX_SOURCES = 5


def select_best_sources(official_site, initiative_results, objective):
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables")

    prompt = f"""
You are a senior business consultant.

Objective:
{objective}

Rules:
- Select at most {MAX_SOURCES} URLs
- Prefer official company domains
- One source can support multiple claims
- Do NOT invent information
- Return JSON only
- No explanations outside JSON

Official website:
{json.dumps(official_site, indent=2)}

Candidate sources:
{json.dumps(initiative_results, indent=2)}

Output JSON schema:
{{
  "selected_sources": [
    {{
      "url": "...",
      "reason": "..."
    }}
  ]
}}
"""

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(
        f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Gemini API failed: {response.status_code} - {response.text}"
        )

    data = response.json()

    text_output = data["candidates"][0]["content"]["parts"][0]["text"]

    if not text_output or not text_output.strip():
        raise RuntimeError("LLM returned empty response")

    # تنظيف شائع (إزالة ```json ``` إن وجدت)
    cleaned = text_output.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Failed to parse LLM JSON output.\n"
            f"Raw output was:\n{text_output}"
        ) from e