# Social Media Automation Project

This project contains Python scripts to automate social media tasks. It includes:

- **Twitter Like Automation Script:** Automatically likes a tweet using the Twitter API.
- **Reddit Fetch Script:** Retrieves the 5 latest posts from a specified subreddit using Reddit's API.

---

## Overview

This project demonstrates how to interact with social media APIs using Python:

- **Twitter Like Automation Script:**  
  Authenticates with Twitter via OAuth 1.0a (using Consumer Keys & Access Tokens) to like a tweet specified by its tweet ID. It automatically handles rate limits and logs events.

- **Reddit Fetch Script:**  
  Authenticates with Reddit using PRAW and OAuth, then fetches and displays the 5 latest posts from a given subreddit (showing the title, author, and upvote count).

---

## Prerequisites

- Python 3.6+
- Virtual Environment (recommended)

---

## Features

- **Twitter Script:**

  - OAuth 1.0a Authentication (Consumer Key/Secret & Access Token/Secret).
  - Command-line argument to specify the tweet ID.
  - Automatic rate limit handling.
  - Logging of events to both the console and a log file.

- **Reddit Script:**
  - OAuth Authentication using PRAW.
  - Fetches the 5 most recent posts from a subreddit.
  - Displays post title, author, and upvote count.
  - Error handling and logging.

---

## Setup

### Virtual Environment

1. **Clone the Repository** and navigate into the project folder.

2. **Create a virtual environment:**

   - **Windows:**
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

### Dependencies

Install the required packages with:
pip install tweepy python-dotenv praw

### Environment Variables

Create a file named `.env` in the project root and add your API credentials:

Twitter API Credentials:

- Obtain these by creating a Twitter Developer account and setting up an app with Read & Write permissions. [Learn more](https://developer.twitter.com/en/docs/authentication/oauth-1-0a).

TWITTER_CONSUMER_KEY="your_twitter_api_key_here"

TWITTER_CONSUMER_SECRET="your_twitter_api_key_secret_here"

TWITTER_ACCESS_TOKEN="your_twitter_access_token_here" TWITTER_ACCESS_SECRET="your_twitter_access_token_secret_here"

TWITTER_BEARER_TOKEN="your_twitter_bearer_token_here" # Optional

Reddit API Credentials:

- For detailed instructions on acquiring Reddit API credentials, please refer to [this guide](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example).

REDDIT_CLIENT_ID="your_reddit_client_id_here"

REDDIT_CLIENT_SECRET="your_reddit_client_secret_here"

REDDIT_USER_AGENT="script:reddit_fetch:v1.0 (by /u/your_reddit_username)"

> **Important:**
>
> - Make sure your Twitter app is configured with Read & Write permissions.
> - Do not commit your `.env` file to version control. Consider adding it to your `.gitignore`.

---

## Usage

### Twitter Like Script

This script authenticates with the Twitter API using OAuth 1.0a and likes a tweet by its ID. It handles rate limits and logs errors or success messages.

### How to Run:

From the project root:

python -m twitter_like.twitter_like <tweet_id>

Replace <tweet_id> with the tweet’s numeric ID. Example:

python -m twitter_like.twitter_like 1895770434580464107

_(The tweet ID is the numeric part from the tweet URL.)_

### Reddit Fetch Script

Fetches the 5 latest posts from a subreddit using PRAW. It prints and logs each post’s title, author, and upvotes.

How to Run:
From the project root:

python -m reddit_fetch.reddit_fetch subreddit_name

Replace subreddit_name with the subreddit name. Example:

python -m reddit_fetch.reddit_fetch python

**What It Does:**

- **Loads credentials from .env**: Retrieves Reddit API credentials from the .env file.
- **Authenticates with Reddit**: Uses the loaded credentials to authenticate with the Reddit API.
- **Grabs the 5 latest posts**: Fetches the five most recent posts from the specified subreddit.
- **Logs and prints titles, authors, and upvotes**: Records and displays the title, author, and upvote count for each post.
- **Handles errors cleanly**: Manages any errors that occur during execution, ensuring the script doesn't crash unexpectedly.

---
