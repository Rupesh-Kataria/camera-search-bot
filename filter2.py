import pandas as pd
import numpy as np
import json
import re

def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df

def filter_products(filters):
    df=read_csv("amazon_products.csv")
    df = df.copy()
    df["feature_match"] = 0
    # try:
    #     filters = re.sub(r'[`~\\]', '', filters)  # Remove backticks and tildes
    #     filters = re.sub(r'}\s*\.?$', '}', filters)  # Fix trailing dots
    #     filters = filters.strip()
    #     filters = re.sub(r'^json\s*', '', filters, flags=re.IGNORECASE)  # Remove "json" prefix
    #     filters = filters.strip()
    #     print(filters)
    #     # Parse JSON if it's a string
    #     if isinstance(filters, str):
    #         filters_dict = json.loads(filters) 
    #         filters=filters_dict
        
    # except json.JSONDecodeError as e:
    #     print(f"Invalid JSON: {e}")
    #     print(f"Received input: {filters}")
    #     return []

    if isinstance(filters, str):
        try:
            filters = re.sub(r'[`~\\]', '', filters)
            filters = re.sub(r'}\s*\.?$', '}', filters)
            filters = filters.strip()
            filters = re.sub(r'^json\s*', '', filters, flags=re.IGNORECASE)
            filters = filters.strip()
            # print("[CLEANED FILTER STRING]", filters)

            filters = json.loads(filters)  # Convert to dictionary
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}")
            print(f"Received input: {filters}")
            return []

    # print("[FINAL FILTER DICT]", filters)

    # print("Looping over filters now...")
    # print("Total keys:", len(filters))
    
    # print("filters type:", type(filters))
    # print("filters keys:", filters.keys())

    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['price'].fillna(0, inplace=True)

 
    for key, value in filters.items():
        key = key.lower()
        # print(" key1 ",key)
        # print("value1 ",value)
        # --- Special case: company -> match against 'manufacturer' column ---
        if key == "company":
            # print(" key2 ",key)
            # print("value2 ",value)
            # print(" df[manufacturer] ",df["manufacturer"][0])
            if isinstance(value, list):
                match_mask = df["manufacturer"].fillna('').str.lower().apply(lambda c: any(v.lower() in c for v in value))
            else:
                match_mask = df["manufacturer"].fillna('').str.lower().str.contains(str(value).lower())
            df = df[match_mask]
            continue

        if key=="min_price":
            match_mask = (df["price"] >= value)
            df = df[match_mask]
            continue
        if key=="max_price":
            match_mask = (df["price"] <= value)
            df = df[match_mask]
            continue
        
        
        if key == "color":
            if isinstance(value, list):
                match_mask = df["title"].str.lower().apply(lambda c: any(v in c for v in value))
            else:
                match_mask = df["title"].str.lower().str.contains(str(value).lower())

        elif key == "min_rating":
            match_mask = df["rating"] >= value
        
        elif key in ["resolution", "lens_type", "type", "use_case", "weight","megapixel"]:
            match_mask = df["title"].str.lower().apply(lambda x: any(
                word in x for word in str(value).lower().replace(",", " ").split()
            ))

        elif key == "accessories":
            if isinstance(value, list):
                match_mask = df["title"].str.lower().apply(
                    lambda acc: any(
                        any(word in acc for word in item.lower().replace(",", " ").split())
                        for item in value
                    )
                )
            else:
                match_mask = df["title"].str.lower().apply(
                    lambda acc: any(
                        word in acc for word in value.lower().replace(",", " ").split()
                    )
                )
        elif key == "screen_size":
            df.loc[df["title"] == value, "feature_match"] += 1
            continue

        elif key == "battery_life":
            df.loc[df["title"] >= value, "feature_match"] += 1
            continue
   
        else:
           match_mask = df["title"].str.lower().apply(lambda x: any(
                word in x for word in str(value).lower().replace(",", " ").split()
            ))
        df.loc[match_mask, "feature_match"] += 1

        
    if "num_ratings" in df.columns:
        df["num_ratings"] = (
            df["num_ratings"]
            .astype(str)
            .str.replace(",", "")  # remove commas
            .str.extract("(\d+)", expand=False)  # extract digits only
            .astype(float)  # or int, based on your use
            .fillna(0)
        )

    # Normalize rating and review_count (scale to max 5)
    if "rating" in df.columns and df["rating"].max() > 0:
        df["norm_rating"] = (df["rating"] / df["rating"].max())
    else:
        df["norm_rating"] = 0

    if "num_ratings" in df.columns and df["num_ratings"].max() > 0:
        df["norm_reviews"] = (df["num_ratings"] / df["num_ratings"].max())
    else:
        df["norm_reviews"] = 0

    # Compute score based on feature match + normalized factors
    df["final_score"] = (df["norm_rating"]*df["norm_reviews"])

    # Sort by feature match and then score
    df = df.sort_values(by=["feature_match", "final_score"], ascending=False)
    df.head(5).to_csv("result.csv", index=False)

    return df.head(5)
