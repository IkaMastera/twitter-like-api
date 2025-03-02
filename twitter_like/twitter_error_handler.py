import time
import logging
import tweepy

def handle_twitter_error(e, retry_func=None, *args, **kwargs):
    """

    Handles Twitter API Errors and retries when necesarry.

    Args:
        e (Exception): The Tweepy exception raised.
        retry_func (function, optional): The function to retry on recoverable errors.
        "args, **kwargs: Arguments to pass to the retry function.

    Returns:
        The result of the retried function if applicable, otherwise exits on fatal errors.
    
    """

    # Catch Specific Exceptions (Best Practice I found)
    if isinstance(e, tweepy.Unauthorized):
        logging.error("Unauthorized: Invalid API credentials. Check your keys.")
        raise SystemExit(1)

    elif isinstance(e, tweepy.Forbidden):
        logging.error("Forbidden: Action not allowed (tweet may be protected or already liked).")
        raise SystemExit(1)

    elif isinstance(e, tweepy.NotFound):
        logging.error("Not Found: Tweet does not exist or has been deleted.")
        raise SystemExit(1)
    
    elif isinstance(e, tweepy.errors.BadRequest):
        for error in e.api_errors:
            if "id" in error.get("parameters", {}):
                logging.error(f"Invalid Tweet ID: {error['parameters']['id'][0]}. Please provide a valid Tweet ID.")
                raise SystemExit(1)
        
        logging.error("Bad Request: One or more parameters in the request were invalid.")
        raise SystemExit(1)

    # Using a Retry Mechanism for Transient Failures
    elif isinstance(e, tweepy.TooManyRequests):
        headers = e.response.headers
        reset_time = int(headers.get("x-rate-limit-reset", time.time()))
        wait_time = max(reset_time - time.time(), 10)
        logging.warning(f"Rate limit exceeded! Sleeping for {wait_time:.2f} seconds...")
        time.sleep(wait_time + 1)

        if retry_func:
            return retry_func(*args, **kwargs)
        
        logging.error("Max retries reached. Could not complete the request.")
        raise SystemExit(1)

    elif isinstance(e, tweepy.HTTPException):
        if e.response.status_code == 500:
            logging.warning("Twitter Internal Server Error (500). Retrying...")
            time.sleep(10)
            if retry_func:
                return retry_func(*args, **kwargs)
        elif e.response.status_code == 400:
            logging.error("Bad Request: Invalid tweet ID or malformed request.")
        else:
            logging.error(f"HTTP Error {e.response.status_code}: {e}")
        raise SystemExit(1)

    else:
        logging.error(f"Unexpected Twitter API error: {e}")
        raise SystemExit(1)