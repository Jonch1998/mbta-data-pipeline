import logging
import requests
from requests.adapters import HTTPAdapter
from typing import Any, Final  # Added for strict constant and type safety
from urllib3.util.retry import Retry

# Mark global configuration settings as Final constants
BASE_URL: Final[str] = "https://api-v3.mbta.com"
DEFAULT_TIMEOUT: Final[tuple[float, float]] = (5.0, 10.0)  # (connect, read) seconds

logger = logging.getLogger(__name__)


def _build_session() -> requests.Session:
    """Builds and configures a requests Session with retry logic."""
    retry = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


_session = _build_session()


def get_routes() -> list[dict[str, Any]]:
    """Fetches and returns the route list from the MBTA API."""
    logger.info("Requesting routes from %s", BASE_URL)
    
    response = _session.get(
        f"{BASE_URL}/routes",
        timeout=DEFAULT_TIMEOUT,
    )
    response.raise_for_status()

    try:
        payload: dict[str, Any] = response.json()
    except requests.exceptions.JSONDecodeError as exc:
        raise RuntimeError("MBTA API returned invalid JSON") from exc

    data = payload.get("data")
    
    # Pythonic guard clause: ensures 'data' exists AND is a list
    if data is None or not isinstance(data, list):
        raise RuntimeError("MBTA API response 'data' field is missing or not a list")

    logger.info("Retrieved %d routes", len(data))
    return data


if __name__ == "__main__":
    # Configure logging before running execution blocks
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    
    try:
        routes = get_routes()
        if routes:  # Pythonic check: evaluates to False if the list is empty
            first_route = routes[0]
            print(f"Retrieved {len(routes)} routes")
            print(f"First Route ID: {first_route.get('id')}")
            
            # Using .get() with fallback protects against unexpected missing API keys
            attributes = first_route.get("attributes", {})
            print(f"First Route Name: {attributes.get('long_name', 'Unknown')}")
    except Exception as e:
        logger.error("Failed to fetch MBTA routes: %s", e)
