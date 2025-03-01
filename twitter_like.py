"""
TWITTER LIKE SCRIPT
- Authenticates with twitter API (OAuth 2.0 user context) and likes a tweet by ID.
- Handles rate limits and authentication errors, logging events to a file and console.
Usage:
    1. Set up environment variables in .env (Twitter API keys and tokens).
    2. Run: python twitter_like.py <tweet_id>
    3. You can get your twitter ID by going in the tweet you want to like, https://x.com/lexfridman/status/1895770434580464107 in this example your tweet_id is 1895770434580464107.
"""

import os
import logging
import tweepy
from dotenv import load_dotenv
import argparse

# Logs messages to both console and file with timestamps good practice
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.FileHandler("twitter_script.log"), logging.StreamHandler()]
    )

def load_credentials():
    # Load enviorment variables from .env
    load_dotenv()

    # Retrieve Twitter API credentials from environment variables
    credentials = {
        "consumer_key": os.getenv("TWITTER_CONSUMER_KEY"),
        "consumer_secret": os.getenv("TWITTER_CONSUMER_SECRET"),
        "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
        "access_secret": os.getenv("TWITTER_ACCESS_SECRET"),
        "bearer_token": os.getenv("TWITTER_BEARER_TOKEN"),
    }

    # Checking that all required Twitter cerdentials are provided for error handling
    if not all([credentials["consumer_key"], credentials["consumer_secret"],
                credentials["access_token"], credentials["access_secret"]]):
        logging.error("Twitter API credentials not fully set in .env. Exiting.")
        exit(1)
    return credentials


def parse_arguments():
    # Parse command-line argument for tweet ID to like
    argument_parser = argparse.ArgumentParser(description="Like a Tweet by ID using the Twitter API.")
    argument_parser.add_argument("tweet_id", help="The unique ID of the tweet to like.")
    parsed_args = argument_parser.parse_args();
    tweet_id = parsed_args.tweet_id
    return tweet_id

def initialize_twitter_client(credentials):
    "Initialize and return a Tweepy client using the provided credentials"
    client = tweepy.Client(
        bearer_token=credentials["bearer_token"],
        consumer_key=credentials["consumer_key"],
        consumer_secret=credentials["consumer_secret"],
        access_token=credentials["access_token"],
        access_token_secret=credentials["access_secret"],
        wait_on_rate_limit=True
    )
    logging.info("Authenticated to Twitter API successfully.")
    return client

def like_tweet(client, tweet_id):
    try:
        # Use the client to like the tweet specified by tweet_id
        response = client.like(tweet_id)
        if hasattr(response, "errors") and response.errors:
            # Log any errors returned by the API
            logging.error(f"Twitter API error: response.errors")
        else:
            logging.info(f"Successfully liked tweet ID {tweet_id}.")
            exit(0)

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

def main():
    setup_logging()
    credentials = load_credentials()
    tweet_id = parse_arguments()
    client = initialize_twitter_client(credentials)
    like_tweet(client, tweet_id)

if __name__ == "__main__":
    main()    