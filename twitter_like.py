"""
TWITTER LIKE SCRIPT
- Authenticates with twitter API (OAuth 2.0 user context) and likes a tweet by ID.
- Handles rate limits and authentication errors, logging events to a file and console.
Usage:
    1. Set up environment variables in .env (Twitter API keys and tokens).
    2. Run: python twitter_like.py <tweet_id>
"""

import os
import logging
import tweepy
from dotenv import load_dotenv
import argparse

# Load enviorment variables from .env
load_dotenv()

# Retrieve Twitter API credentials from environment variables
consumer_key = os.getenv("TWITTER_COSUMER_KEY")
consumer_secret = os.getenv("TWITTER_COSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_secret = os.getenv("TWITTER_ACCESS_SECRET")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

# Checking that all required Twitter cerdentials are provided for error handling
if not consumer_key or not consumer_secret or not access_token or not access_secret:
    logging.error("Twitter API credentials not fully set in .env. Exiting")
    exit(1)

# Logs messages to both console and file with timestamps good practice
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("twitter_script.log"), logging.StreamHandler()]
)

# Parse command-line argument for tweet ID to like
argument_parser = argparse.ArgumentParser(description="Like a Tweet by ID using the Twitter API.")
argument_parser.add_argument("tweet_id", help="The unique ID of the tweet to like.")
parsed_args = argument_parser.parsed_args();
target_tweet_id = parsed_args.tweet_id

try: 
    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_secret,
        wait_on_rate_limit=True
    )
    logging.info("Authenticated to Twitter API successfully.")

    # Use the client to like the tweet specified by tweet_id
    response = client.like(tweet_id)
    if hasattr(response, "errors") and response.errors:
        # Log any errors returned by the API
        logging.error(f"Twitter API error: response.errors")
    else:
        logging.info(f"Successfully liked tweet ID {tweet_id}.")

except tweepy.TweepyException as e:
    # Handle exceptions from the Tweepy library
    if hasattr(e, "response") and e.response is not None:
        status_code = e.response.status_code
        if status_code == 429:
            # Rate Limit error handler
            reset_time = e.response.headers.get("x-rate-limit-reset")
            logging.error(f"Rate limit reached. Pause requests until reset time: {reset_time}. Error: {e}")
        elif status_code in (401, 403):
            # Logging Authentication or authorization errors
            logging.error(f"Authentication failed or not authorized (HTTP {status_code}). Error: {e}")
        else:
            logging.error(f"Failed to like tweet (HTTP {status_code}). Error: {e}")
    else:
        logging.error(f"Unexpected error: {e}")       