import pandas as pd

def find_matching_hotels(parsed_query: dict, df: pd.DataFrame) -> pd.DataFrame:
    # Safely extract and lowercase values, defaulting to empty strings if None
    location = (parsed_query.get("location") or "").lower()
    room_type = (parsed_query.get("room_type") or "").lower()
    hotel_name = (parsed_query.get("hotel_name") or "").lower()
    max_price = parsed_query.get("max_price")

    matches = df.copy()

    # ✅ If hotel name is provided, match directly
    if hotel_name:
        matches = matches[matches["Hotel Name"].str.lower().str.contains(hotel_name, na=False)]
    else:
        # ✅ Filter by location and room type only if no hotel name is given
        if location:
            matches = matches[matches["Location"].str.lower().str.contains(location, na=False)]
        if room_type:
            matches = matches[matches["Room Type"].str.lower().str.contains(room_type, na=False)]

    # ✅ Filter by max price if provided
    if max_price is not None:
        matches = matches[matches["Final Price"] <= max_price]

    # ✅ Sort by price and rating
    sorted_matches = matches.sort_values(by=["Final Price", "Rating"], ascending=[True, False])

    return sorted_matches.head(5)

# Test run
if __name__ == "__main__":
    from data_loader import load_hotels_data
    from query_parser import parse_user_query

    df = load_hotels_data("hotels_with_coordinates.csv")
    parsed = parse_user_query("I want to book a Deluxe room in Mumbai from 2025-06-12 to 2025-06-15")
    top_matches = find_matching_hotels(parsed, df)

    print("Top Hotel Matches:")
    print(top_matches[["Hotel Name", "Rating", "Final Price", "Location", "Room Type"]])