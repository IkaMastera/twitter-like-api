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
if not consumer_key or not consumer_secret or not access_token or not access_secret
    logging.error("Twitter API credentials not fully set in .env. Exiting")
    exit(1)

# Logs messages to both console and file with timestamps good practice
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("twitter_script.log"), logging.StreamHandler()]
)
