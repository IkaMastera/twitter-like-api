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
from dotenv import load_dotenv
from twitter_like.twitter_error_handler import handle_twitter_error

def setup_logging():
    # Build a path to the "twitter_like" folder within the current working directory.
    log_folder = os.path.join(os.getcwd(), "twitter_like")
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    
    # Define the path for the log file
    log_file_path = os.path.join(log_folder, "twitter_script.log")
    
    # Configure logging to output to the file and the console.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file_path, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def load_credentials():
    load_dotenv()
    credentials = {
        "consumer_key": os.getenv("TWITTER_CONSUMER_KEY"),
        "consumer_secret": os.getenv("TWITTER_CONSUMER_SECRET"),
        "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
        "access_secret": os.getenv("TWITTER_ACCESS_SECRET")
    }

    # Check if all required credentials exist
    if not all(credentials.values()):
        logging.error("Missing OAuth 1.0a credentials in .env file! Exiting.")
        exit(1)

    logging.info("Loaded OAuth 1.0a credentials from .env.")
    return credentials

def parse_arguments():
    parser = argparse.ArgumentParser(description="Like a Tweet by ID using the Twitter API.")
    parser.add_argument("tweet_id", help="The unique ID of the tweet to like.")
    args = parser.parse_args()
    return args.tweet_id

def initialize_twitter_client(credentials):
    """Initialize and return a Tweepy client using OAuth 1.0a (User Authentication)."""
    client = tweepy.Client(
        consumer_key=credentials["consumer_key"],
        consumer_secret=credentials["consumer_secret"],
        access_token=credentials["access_token"],
        access_token_secret=credentials["access_secret"],
        wait_on_rate_limit=False
    )

    logging.info("Authenticated to Twitter API using OAuth 1.0a.")
    return client

@handle_twitter_error
def like_tweet(client, tweet_id):
    """Likes a tweet using the Twitter API."""
    response = client.like(tweet_id)
    
    # Check if the response object includes a 'response' attribute with headers.
    if hasattr(response, 'response') and response.response:
        headers = response.response.headers
        remaining = headers.get('x-rate-limit-remaining', 'Unknown')
        reset = headers.get('x-rate-limit-reset', 'Unknown')
        logging.info(f"Rate Limit Remaining: {remaining}")
        logging.info(f"Rate Limit Reset: {reset}")
    else:
        logging.warning("No rate limit headers found in the response.")
    
    return response

def main():
    setup_logging()
    credentials = load_credentials()
    tweet_id = parse_arguments()
    client = initialize_twitter_client(credentials)

    response = like_tweet(client, tweet_id)
    logging.info(f"Successfully liked tweet ID: {tweet_id}.")

if __name__ == "__main__":
    main()