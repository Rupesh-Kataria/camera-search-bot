# 🤖 Conversational Camera Recommendation Bot

A smart, interactive assistant that helps users search and filter cameras on Amazon.in through natural conversation.

This project implements a **conversational interface** that:
- **Scrapes camera data** from Amazon.in
- **Interprets user input** using natural language
- **Maintains user preference context**
- **Recommends products** based on user criteria such as brand, features, and price range

---

## 📌 Problem Statement

> **Goal**: Build a conversational product recommendation engine for a given category — **cameras** listed on [amazon.in](https://www.amazon.in/).

The chatbot should:
- Scrape product data from Amazon
- Allow users to explore and filter products conversationally
- Continuously **update user preferences** based on their query history
- Recommend **relevant products** based on preferences and feature-matching logic

---

## 🏗️ Project Architecture

```text
camera-search-bot/
│
├── final_scrapping.ipynb       # Structured web scraping pipeline
├── scrapping.ipynb             # Step-by-step scrapping exploration (draft)
│
├── main3.py                    # Main chatbot interface
├── filter.py                   # Extracts preferences using Gemini
├── filter2.py                  # Filters & ranks products using stored preferences
│
├── amazon_products.csv         # Scraped data (local CSV)
├── requirements.txt            # All dependencies
├── .env                        # User-Agent, Gemini API keys, etc.
└── README.md                   # Detailed documentation


🧾 Getting Started
1️⃣ Clone the repository

git clone https://github.com/your-username/camera-search-bot.git
cd camera-search-bot

2️⃣ Create a virtual environment

python -m venv myenv
myenv/Scripts/activate   
     
3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Add environment variables

USER_AGENT="your_user_agent"
GEMINI_API_KEY="your_gemini_api_key"

🕸️ Web Scraping

jupyter notebook final_scrapping.ipynb

🤖 Running the Chatbot

python main3.py


