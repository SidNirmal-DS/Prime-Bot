import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, render_template
import sys
from pathlib import Path

# Setup import path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.constants import openai_key
from app.data_loader import load_hotels_data
from app.query_parser import parse_user_query
from app.hotel_selector import find_matching_hotels
from app.response_generator import generate_response

app = Flask(__name__, template_folder="templates", static_folder="static")

df = load_hotels_data("hotels_with_coordinates.csv")
chat_history = []

@app.route("/", methods=["GET", "POST"])
def index():
    global chat_history
    user_query = request.form.get("query", "").strip()
    selected_hotel = request.form.get("selected_hotel")

    # 🔍 1. If user clicked on a specific hotel
    if selected_hotel:
        selected_df = df[df["Hotel Name"].str.contains(selected_hotel.strip(), case=False, na=False, regex=False)]
        if not selected_df.empty:
            hotel = selected_df.iloc[0]
            return render_template("map.html",
                                   hotel_name=hotel["Hotel Name"],
                                   latitude=hotel["Latitude"],
                                   longitude=hotel["Longitude"])

    # 🧠 2. If user entered a query
    if user_query:
        chat_history.append({"sender": "user", "text": user_query})
        parsed = parse_user_query(user_query)
        matches = find_matching_hotels(parsed, df)
        response = generate_response(matches, user_query, selected_hotel)

        chat_history.append({
            "sender": "bot",
            "text": response["hotels"],
            "type": "hotel_list"
        })
        chat_history.append({
            "sender": "bot",
            "text": response["summary"],
            "type": "general"
        })

    # 💬 3. Render Chat
    safe_history = [
        {"sender": str(msg.get("sender", "bot")), "text": str(msg.get("text", "")), "type": msg.get("type", "general")}
        for msg in chat_history
    ]
    return render_template("index.html", chat_history=safe_history)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5055, debug=True)