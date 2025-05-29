from openai import OpenAI
import json
from app.constants import openai_key

# ✅ Set up the OpenAI client for v1.x
client = OpenAI(api_key=openai_key)

def parse_user_query(query: str) -> dict:
    prompt = f"""
You are an intelligent hotel booking assistant. Extract the following fields from the user's query and return only JSON:

- hotel_name (like "Taj Santacruz" or "The Orchid" — or null if not specified)
- location
- room_type (Standard, Deluxe, Suite, Basic — or null if not specified)
- check_in (YYYY-MM-DD or null)
- check_out (YYYY-MM-DD or null)
- max_price (as integer or null)

### Examples:

User: I want a Deluxe room in Mumbai from 2025-06-12 to 2025-06-15 under INR 10000  
Response:
{{
  "hotel_name": null,
  "location": "Mumbai",
  "room_type": "Deluxe",
  "check_in": "2025-06-12",
  "check_out": "2025-06-15",
  "max_price": 10000
}}

User: Hotels in Delhi for 2 nights under 9500  
Response:
{{
  "hotel_name": null,
  "location": "Delhi",
  "room_type": null,
  "check_in": null,
  "check_out": null,
  "max_price": 9500
}}

User: Need a room in Bangalore from 2025-07-01 to 2025-07-04  
Response:
{{
  "hotel_name": null,
  "location": "Bangalore",
  "room_type": null,
  "check_in": "2025-07-01",
  "check_out": "2025-07-04",
  "max_price": null
}}

User: I want to stay at Taj Santacruz next week  
Response:
{{
  "hotel_name": "Taj Santacruz",
  "location": null,
  "room_type": null,
  "check_in": null,
  "check_out": null,
  "max_price": null
}}

Now extract from:
User: "{query}"
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        content = response.choices[0].message.content
        print("🧠 GPT Output:", content)
        parsed = json.loads(content)

    except Exception as e:
        print("❌ GPT parsing failed, falling back to defaults:", e)
        parsed = {
            "hotel_name": None,
            "location": "Unknown",
            "room_type": "Standard",
            "check_in": None,
            "check_out": None,
            "max_price": None
        }

    return parsed

# ✅ Optional: test run
if __name__ == "__main__":
    q = "Looking for hotels around INR 9000 in Mumbai"
    result = parse_user_query(q)
    print("✅ Parsed:", result)