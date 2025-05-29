import pandas as pd

def load_hotels_data(filepath="hotels_with_coordinates.csv"):
    df = pd.read_csv(filepath)
    return df

# 👇 Add this block so something prints when you run the script directly
if __name__ == "__main__":
    df = load_hotels_data()
    print(df.head())  # ✅ This will print the first 5 rows to confirm it's working