import logging
import time
import tweepy

def handle_twitter_error(func):
    """
    A decorator that wraps a function and handles Tweepy API errors.
    If an error occurs, it logs the error and (optionally) retries.
    """
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            # Check if the response has errors (if the response structure includes an errors attribute)
            if hasattr(response, "errors") and response.errors:
                logging.error(f"API returned errors: {response.errors}")
                raise tweepy.TweepyException("API returned errors.")
            return response

        except tweepy.errors.Unauthorized:
            logging.error("Unauthorized: Invalid API credentials. Check your keys.")
            raise SystemExit(1)

        except tweepy.errors.Forbidden:
            logging.error("Forbidden: Action not allowed (tweet may be protected or already liked).")
            raise SystemExit(1)

        except tweepy.errors.BadRequest as e:
            for error in e.api_errors:
                if "id" in error.get("parameters", {}):
                    logging.error(f"Invalid Tweet ID: {error['parameters']['id'][0]}.")
                    raise SystemExit(1)
            logging.error("Bad Request: One or more parameters in the request were invalid.")
            raise SystemExit(1)
        
        except tweepy.errors.TooManyRequests as e:
            headers = e.response.headers
            reset_time = int(headers.get("x-rate-limit-reset", time.time() + 60))
            wait_time = max(reset_time - time.time(), 10)
            logging.warning(f"Rate limit exceeded! Sleeping for {wait_time:.2f} seconds...")
            time.sleep(wait_time + 1)
            try:
                return func(*args, **kwargs)
            except tweepy.TweepyException:
                logging.error("Still rate-limited after retry. Exiting.")
                raise SystemExit(1)
        
        except tweepy.errors.TwitterServerError as e:
            logging.warning("Twitter Internal Server Error. Retrying once...")
            time.sleep(10)
            try:
                return func(*args, **kwargs)
            except tweepy.TweepyException:
                logging.error("Still failing after server error retry. Exiting.")
                raise SystemExit(1)
        
        except tweepy.errors.TweepyException as e:
            logging.error(f"Unexpected Twitter API error: {e}")
            raise SystemExit(1)
        
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise SystemExit(1)
    return wrapper