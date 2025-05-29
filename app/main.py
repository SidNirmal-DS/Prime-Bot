from app.query_parser import parse_user_query
from app.data_loader import load_hotels_data
from app.hotel_selector import find_matching_hotels
from app.response_generator import generate_response

def main():
    # 1. Get user input (hardcoded for now)
    user_query = "I want to book a Deluxe room in Mumbai from 2025-06-12 to 2025-06-15"

    # 2. Parse the query
    parsed_query = parse_user_query(user_query)

    # 3. Load hotel data
    df = load_hotels_data("hotels_with_coordinates.csv")

    # 4. Get matching hotels
    top_matches = find_matching_hotels(parsed_query, df)

    # 5. Generate LLM response
    final_response = generate_response(top_matches, user_query)

    # 6. Show the output
    print("\n🤖 GPT Recommendation:\n")
    print(final_response)

if __name__ == "__main__":
    main()