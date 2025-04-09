from filter import filter
from filter2 import filter_products

def format_top_products(df):
    formatted_output = ""
    for idx, row in df.head(5).iterrows():
        formatted_output += f"Product {idx + 1}:\n"
        formatted_output += f"Manufacturer: {row.get('manufacturer', 'N/A')}\n"
        formatted_output += f"About Product: {row.get('title', 'N/A')}\n"
        formatted_output += f"Price: ₹{int(row.get('price', 0))}\n"
        formatted_output += f"Rating: {row.get('rating', 'N/A')}\n"
        formatted_output += f"Number of Ratings: {row.get('num_ratings', 'N/A')}\n"
        formatted_output += "\n"
    return formatted_output

def main():
    print("Start typing your camera queries. Type 'exit' to quit.")
    
    conversation_history = ""
    cnt=1
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break

        # Accumulate the user query
        conversation_history += "Query {cnt} " + user_input+"\n"
        cnt=cnt+1
        # Clean up spaces
        full_query = conversation_history.strip()

        # Get updated filter
        extracted_json = filter(full_query)
        
        def process_filters(filters):
          if "color" in filters and isinstance(filters["color"], str):
              # Split by comma and strip whitespace
              filters["color"] = [c.strip().lower() for c in filters["color"].split(",")]
          return filters

        print("\n[DEBUG] Full query sent:", full_query)
        print("[FILTERED JSON]:", extracted_json)
        product_dict=filter_products(extracted_json)
        filt_prod=format_top_products(product_dict)
        print(filt_prod)
        print("-" * 40)

if __name__ == "__main__":
    main()
