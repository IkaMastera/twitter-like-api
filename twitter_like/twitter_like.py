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
import argparse
import time
from dotenv import load_dotenv
from twitter_like.twitter_error_handler import handle_twitter_error


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
    response = client.like(tweet_id)

    if not response.data:
        logging.warning(f"Tweet ID {tweet_id} does not exist or is unavailable.")

    logging.info(f"Successfully liked tweet ID: {tweet_id}.")

def main():
    setup_logging()
    credentials = load_credentials()
    tweet_id = parse_arguments()
    client = initialize_twitter_client(credentials)
    like_tweet(client, tweet_id)

    try: 
        handle_twitter_error(lambda: like_tweet(client, tweet_id))
    except SystemExit:
        logging.error("Exiting program due to an error.")
        exit(1)


if __name__ == "__main__":
    main()    