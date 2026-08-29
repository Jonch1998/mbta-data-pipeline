import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://api-v3.mbta.com"

DEFAULT_TIMEOUT = (5, 10)  # (connect, read) seconds

logger = logging.getLogger(__name__)


def _build_session() -> requests.Session:
    retry = Retry(
        total=3,
        backoff_factor=0.5,  # 0.5s, 1s, 2s between retries
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


_session = _build_session()


def get_routes() -> list[dict]:
    logger.info("Requesting routes from %s", BASE_URL)
    response = _session.get(
        f"{BASE_URL}/routes",
        timeout=DEFAULT_TIMEOUT,
    )
    response.raise_for_status()

    try:
        payload = response.json()
    except requests.exceptions.JSONDecodeError as exc:
        raise RuntimeError("MBTA API returned invalid JSON") from exc

    data = payload.get("data")

    if not isinstance(data, list):
        raise RuntimeError("MBTA API response 'data' field is not a list")

    logger.info("Retrieved %d routes", len(data))
    return data


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    routes = get_routes()
    print(f"Retrieved {len(routes)} routes")
    print(routes[0]["id"])
    print(routes[0]["attributes"]["long_name"])