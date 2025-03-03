#!/usr/bin/env python
"""
Reddit Fetch Script
- Authenticates with Reddit using PRAW and OAuth.
- Retrieves the 5 latest posts from a specific subreddit.
- Prints each post's title, author, and upvote count.
Usage:
    python -m reddit_fetch.reddit_fetch <subreddit>
Example:
    python -m reddit_fetch.reddit_fetch python
"""

import os
import logging
import argparse
import praw
from dotenv import load_dotenv
from reddit_fetch.reddit_error_handler import reddit_error_handler

def setup_logging():
    log_folder = os.path.join(os.getcwd(), "reddit_fetch")
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_file_path = os.path.join(log_folder, "reddit_script.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s %(message)s]",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_file_path, encoding='utf-8')]
    )

def load_reddit_credentials():
    #Load environment variables from .env
    load_dotenv()
    creds = {
        "client_id": os.getenv("REDDIT_CLIENT_ID"),
        "client_secret": os.getenv("REDDIT_CLIENT_SECRET"),
        "user_agent": os.getenv("REDDIT_USER_AGENT")
    }
    # Check that the required credentials are provided
    if not creds["client_id"] or not creds["client_secret"] or not creds["user_agent"]:
        logging.error("Missing required Reddit credentials in .env. Exiting.")
        exit(1)
    return creds

@reddit_error_handler
def fetch_latest_posts(subreddit_name, limit=5):
    creds = load_reddit_credentials()
    reddit = praw.Reddit(
        client_id=creds["client_id"],
        client_secret=creds["client_secret"],
        user_agent=creds["user_agent"]
    )

    subreddit = reddit.subreddit(subreddit_name)
    posts = list(subreddit.new(limit=limit))
    return posts

def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Fetch the 5 latest posts from a subreddit.")
    parser.add_argument("subreddit", help="Name of the subreddit (e.g., python)")
    args = parser.parse_args()

    posts = fetch_latest_posts(args.subreddit)
    logging.info(f"Latest 5 posts from r/{args.subreddit}:")
    for post in posts:
        logging.info(f"Title: {post.title}")
        logging.info(f"Author: {post.author}")
        logging.info(f"Upvotes: {post.score}")
        logging.info("-" * 40)

if __name__ == "__main__":
    main()     

