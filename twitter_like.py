"""
TWITTER LIKE SCRIPT
- Authenticates with twitter API (OAuth 2.0 user context) and likes a tweet by ID.
- Handles rate limits and authentication errors, logging events to a file and console.
Usage:
    1. Set up environment variables in .env (Twitter API keys and tokens).
    2. Run: pyhton twitter_like.py <tweet_id>
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