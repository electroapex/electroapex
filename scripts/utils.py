import sys
import time
import logging
from urllib.error import URLError, HTTPError

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("electroapex")

def retry_api(retries=3, delay=2, backoff=2):
    """
    Decorator to retry operations that might fail due to network hiccups,
    rate limits, or server errors.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            t_retries = retries
            t_delay = delay
            while t_retries > 0:
                try:
                    return func(*args, **kwargs)
                except HTTPError as e:
                    # Check for rate limit or server errors
                    if e.code == 403 or e.code == 429:
                        # Grab reset time if available, else standard delay
                        reset_time = e.headers.get("X-RateLimit-Reset")
                        wait = t_delay
                        if reset_time:
                            try:
                                wait = max(int(reset_time) - int(time.time()), 1)
                            except ValueError:
                                pass
                        logger.warning(f"Rate limited (status {e.code}). Retrying in {wait}s...")
                        time.sleep(wait)
                    elif 500 <= e.code < 600:
                        logger.warning(f"Server error {e.code}. Retrying in {t_delay}s...")
                        time.sleep(t_delay)
                    else:
                        # Fatal error (e.g. 400 Bad Request, 401 Unauthorized)
                        logger.error(f"HTTP Error {e.code}: {e.reason}")
                        raise e
                except (URLError, TimeoutError) as e:
                    logger.warning(f"Network error: {e}. Retrying in {t_delay}s...")
                    time.sleep(t_delay)
                except Exception as e:
                    logger.error(f"Unexpected error: {e}")
                    raise e
                
                t_retries -= 1
                t_delay *= backoff
            
            # One last try
            logger.error("All retries exhausted.")
            return func(*args, **kwargs)
        return wrapper
    return decorator
