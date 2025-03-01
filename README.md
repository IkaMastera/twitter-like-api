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

TWITTER_CONSUMER_KEY="your_twitter_api_key_here"
TWITTER_CONSUMER_SECRET="your_twitter_api_key_secret_here"
TWITTER_ACCESS_TOKEN="your_twitter_access_token_here" TWITTER_ACCESS_SECRET="your_twitter_access_token_secret_here"
TWITTER_BEARER_TOKEN="your_twitter_bearer_token_here" # Optional

Reddit API Credentials:

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

Run the Twitter script by providing the tweet ID as an argument:

python twitter_like.py <tweet_id>

Example:

python twitter_like.py 1895770434580464107

_(The tweet ID is the numeric part from the tweet URL.)_

### Reddit Fetch Script

Run the Reddit script by providing the subreddit name as an argument:

python reddit_fetch.py <subreddit>

Example:

python reddit_fetch.py python

This will fetch and display the 5 latest posts from the `r/python` subreddit.

---
