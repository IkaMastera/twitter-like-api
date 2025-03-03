import logging
import prawcore

def reddit_error_handler(func):
    """
    Decorator to handle errors for Reddit API functions.
    If any exception occurs, it logs a friendly error message and exits.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except prawcore.exceptions.NotFound:
            logging.error("Not Found: The requested resource was not found.")
            raise SystemExit(1)
        except prawcore.exceptions.Forbidden:
            logging.error("Forbidden: Access to the requested resource is denied.")
            raise SystemExit(1)
        except prawcore.exceptions.TooManyRequests:
            logging.error("Too Many Requests: Rate limit exceeded. Please wait before making more requests.")
            raise SystemExit(1)
        except prawcore.exceptions.ResponseException as e:
            if e.response and e.response.status_code == 401:
                logging.error(f"Response Exception: {e}")
                raise SystemExit(1)
            else:
                logging.error(f"Response Exception {e}")
                raise SystemExit(1)
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise SystemExit(1)
    return wrapper