from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from filter import filter
from filter2 import filter_products
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to frontend origin if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conversation_history = ""
cnt = 1



# Global conversation memory


class QueryRequest(BaseModel):
    query: str

def format_top_products(df: pd.DataFrame):
    formatted_output = ""
    for idx, row in df.head(5).iterrows():
        # formatted_output += f"Product {idx + 1}:\n"
        formatted_output += f"Manufacturer: {row.get('manufacturer', 'N/A')}\n"
        formatted_output += f"About Product: {row.get('title', 'N/A')}\n"
        formatted_output += f"Price: ₹{int(row.get('price', 0))}\n"
        formatted_output += f"Rating: {row.get('rating', 'N/A')}\n"
        formatted_output += f"Number of Ratings: {row.get('num_ratings', 'N/A')}\n"
        formatted_output += "\n"
    return formatted_output

@app.post("/assistant/")
def handle_query(request: QueryRequest):
    global conversation_history, cnt

    user_query = request.query
    if user_query=="exit":
        conversation_history = ""
        cnt = 1
        return {"response": "Session ended."}
    # print("[DEBUG] User query:", user_query)

    # Add the new query to the history
    conversation_history += f"Query {cnt} " + user_query + "\n"
    cnt += 1

    full_query = conversation_history.strip()
    # print("[DEBUG] Full query sent:", full_query)

    # Extract filters
    extracted_json = filter(full_query)
    # print("[DEBUG] Filtered JSON:", extracted_json)

    # Get filtered products
    product_dict = filter_products(extracted_json)
    # print("[DEBUG] Filtered products:", product_dict)

    # Format product list
    formatted_products = format_top_products(product_dict)
    # print(formatted_products)

    return {"response": formatted_products,"json_output": extracted_json}
