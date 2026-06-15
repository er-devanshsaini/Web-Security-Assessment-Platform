from urllib.parse import urlparse


def normalize_url(raw_url: str) -> str:
    """Return a URL with a scheme so HTTP clients behave predictably."""
    if raw_url.startswith(("http://", "https://")):
        return raw_url
    return f"https://{raw_url}"


def get_hostname(url: str) -> str:
    """Extract a hostname from a URL."""
    parsed_url = urlparse(url)
    return parsed_url.hostname or ""


def is_private_or_local_hostname(hostname: str) -> bool:
    """Block obvious local targets from accidental network scans.

    Developer note:
    This is not a full SSRF defense, but it is a useful first guardrail for a
    student project. Production scanners need stricter DNS and IP validation.
    """
    lowered = hostname.lower()
    return lowered in {"localhost", "127.0.0.1", "::1"} or lowered.endswith(".local")
