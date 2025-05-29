from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import pandas as pd
from app.constants import openai_key

llm = ChatOpenAI(openai_api_key=openai_key, temperature=0.7)

def generate_response(filtered_hotels_df: pd.DataFrame, user_query: str, selected_hotel: str = None):
    if filtered_hotels_df.empty:
        return {
            "content": "Sorry, I couldn't find any hotels matching your request.",
            "type": "no_results"
        }

    hotel_list = []
    for _, row in filtered_hotels_df.head(5).iterrows():
        hotel_list.append({
            "name": row["Hotel Name"],
            "rating": row["Rating"],
            "reviews": row["Reviews"],
            "location": row["Location"],
            "price": row["Final Price"],
            "room_type": row["Room Type"]
        })

    hotel_lines = []
    for i, hotel in enumerate(hotel_list):
        line = (
            f"{i+1}. **{hotel['name']}** - "
            f"**Location:** {hotel['location']} - "
            f"**Rating:** {hotel['rating']} stars - "
            f"**Reviews:** {hotel['reviews']} - "
            f"**Price:** ₹{hotel['price']}"
        )
        hotel_lines.append(line)

    formatted_list = "\n".join(hotel_lines)

    # Summary recommendation section
    if len(hotel_list) >= 2:
        suggestion_text = f"""
Welcome! Thank you for considering our hotel booking service. For your Deluxe room reservation in Mumbai from June 12th to June 15th, 2025, we have some fantastic options for you:

Based on your preferences and travel dates, I would like to recommend the following two top choices for your stay:

1. **{hotel_list[0]['name']}** - Located in {hotel_list[0]['location']}, this hotel is rated {hotel_list[0]['rating']} stars with {hotel_list[0]['reviews']} reviews. The Deluxe room is available for ₹{hotel_list[0]['price']} per night.

2. **{hotel_list[1]['name']}** - Another excellent choice in {hotel_list[1]['location']}, boasting a rating of {hotel_list[1]['rating']} stars and {hotel_list[1]['reviews']} guest reviews. The room is priced at ₹{hotel_list[1]['price']} per night.

Both options ensure comfort, convenience, and quality service. If you need any help with booking or have further preferences, feel free to reach out. Safe travels and we hope you enjoy your stay in Mumbai!
""".strip()
    elif len(hotel_list) == 1:
        suggestion_text = f"""
Welcome! Thank you for considering our hotel booking service. For your Deluxe room reservation in Mumbai from June 12th to June 15th, 2025, we found one excellent option for you:

**{hotel_list[0]['name']}** - Located in {hotel_list[0]['location']}, rated {hotel_list[0]['rating']} stars with {hotel_list[0]['reviews']} reviews. The Deluxe room is available for ₹{hotel_list[0]['price']} per night.

Let us know if you'd like to proceed or explore more options!
""".strip()
    else:
        suggestion_text = "We couldn't find any recommended hotels at this moment. Please refine your search."

    return {
        "hotels": formatted_list,
        "summary": suggestion_text,
        "type": "hotel_list"
    }