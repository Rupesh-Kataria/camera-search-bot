import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
# Set your API key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def extract_camera_filters(user_input):
    # prompt = f"""
    # You are an assistant helping to extract camera preference filters from the following user request:

    # Request: "{user_input}"

    # Extract and return the following in a JSON format:
    # - company (string, optional)
    # - min_price (int, optional)
    # - max_price (int, optional)
    # - min_rating (float, optional)
    # - megapixel (int, optional)
    # - color (string, optional)
    # - weight (string or int, optional)
    # - type (string, optional, like DSLR, Mirrorless, Point & Shoot)
    # - use_case (string, optional, like vlogging, travel, wildlife, studio)
    # - resolution (string, optional, like 4K, 1080p)
    # - lens_type (string, optional, like prime, zoom)
    # - screen_size (int, optional)
    # - battery_life (int, optional)
    # - accessories (list of strings, optional, like tripod, lens filter,32GB TF card)

    # Only return a JSON object.

    # Examples:
    # "Looking for a Sony DSLR under ₹60000" →
    #   {{
    #     "company": "Sony",
    #     "type": "DSLR",
    #     "max_price": 60000
    #   }}

    # "Need a lightweight camera with at least 24MP for travel" →
    #   {{
    #     "megapixel": 24,
    #     "weight": "lightweight",
    #     "use_case": "travel"
    #   }}

    # Now return the JSON for the input.
    # """

    prompt = f"""
You are an assistant helping to extract camera preference filters from user conversations. 
The conversation consists of multiple user requests in sequence. Each new request may override or update the previous preferences.

Below is the full conversation so far:

{user_input}

Your task is to extract the user's **latest overall preferences**, taking into account **updates, removals, or overrides** in their most recent request(s).

Return the final updated preference as a JSON object with the following optional keys:
- company (string)
- min_price (int)
- max_price (int)
- min_rating (float)
- megapixel (int)
- color (string)
- weight (string or int)
- type (string)  # e.g., DSLR, Mirrorless, Point & Shoot
- use_case (string)  # e.g., vlogging, travel, wildlife
- resolution (string)  # e.g., 4K, 1080p
- lens_type (string)  # e.g., prime, zoom
- screen_size (int)
- battery_life (int)
- accessories (list of strings)

ONLY return a single valid JSON object containing the updated preferences. Do not include any explanations.

Example:
Conversation:
User: I want a Sony DSLR under ₹60000
User: Actually just show Kodak ones instead

Output:
{{
  "company": "Kodak",
  "type": "DSLR",
  "max_price": 60000
}}
"""


    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    
    return response.text.strip()





def filter(user_input):
    json_output = extract_camera_filters(user_input)
    return json_output