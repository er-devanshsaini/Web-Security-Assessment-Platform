from dataclasses import dataclass
from urllib.parse import urlparse

import httpx

from backend.app.core.config import settings


SECURITY_HEADERS = {
    "content-security-policy": "Content Security Policy reduces XSS impact.",
    "strict-transport-security": "HSTS tells browsers to use HTTPS only.",
    "x-content-type-options": "Prevents MIME sniffing surprises.",
    "x-frame-options": "Helps reduce clickjacking risk.",
    "referrer-policy": "Limits sensitive URL leakage through referrers.",
    "permissions-policy": "Restricts powerful browser features.",
}


@dataclass
class HttpObservation:
    requested_url: str
    final_url: str
    status_code: int
    headers: dict[str, str]
    set_cookie_headers: list[str]
    uses_https: bool
    redirects_to_https: bool


def fetch_website(url: str) -> HttpObservation:
    """Fetch a website and keep the HTTP details we need for analysis."""
    with httpx.Client(
        timeout=settings.request_timeout_seconds,
        follow_redirects=True,
        verify=True,
        headers={"User-Agent": "SecurityAssessmentPlatform/0.1"},
    ) as client:
        response = client.get(url)

    final_url = str(response.url)
    requested_scheme = urlparse(url).scheme
    final_scheme = urlparse(final_url).scheme

    return HttpObservation(
        requested_url=url,
        final_url=final_url,
        status_code=response.status_code,
        headers={key.lower(): value for key, value in response.headers.items()},
        set_cookie_headers=response.headers.get_list("set-cookie"),
        uses_https=final_scheme == "https",
        redirects_to_https=requested_scheme == "http" and final_scheme == "https",
    )


def find_missing_security_headers(headers: dict[str, str]) -> list[str]:
    """Return expected security headers that were not present."""
    return [header for header in SECURITY_HEADERS if header not in headers]
