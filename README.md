# Twitter Like Automation Script

This project automates the process of liking a tweet using Python and the Twitter API. It authenticates using OAuth 1.0a (Consumer Keys & Access Tokens), handles rate limits, and logs events.

## Overview

- **Authentication:** Uses Twitter API credentials (Consumer Key/Secret and Access Token/Secret).
- **Action:** Likes a tweet specified by its tweet ID from the command line.
- **Rate Limits:** Automatically waits when limits are reached.
- **Logging:** Outputs information and errors to the console and a log file.

## Setup

1. **Clone the repository** and navigate into the folder.

2. **Create a virtual environment:**

   - Windows:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   pip install tweepy python-dotenv
4. **Configure credentials:**  
   Create a file named `.env` in the project root with:

   TWITTER_CONSUMER_KEY="your_api_key_here"
   TWITTER_CONSUMER_SECRET="your_api_key_secret_here"
   TWITTER_ACCESS_TOKEN="your_access_token_here"
   TWITTER_ACCESS_SECRET="your_access_token_secret_here"
   TWITTER_BEARER_TOKEN="your_bearer_token_here" # Optional

_Make sure your Twitter app has Read & Write permissions._

## Usage

Run the script with the tweet ID as an argument:
python twitter_like.py <tweet_id>

Example: python twitter_like.py 1895770434580464107

_(The tweet ID is the numeric part from the tweet URL.)_
