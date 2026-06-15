from backend.app.database.models import Finding, NetworkService


SEVERITY_POINTS = {
    "critical": 30,
    "high": 20,
    "medium": 10,
    "low": 4,
    "info": 1,
}


def calculate_risk_score(findings: list[Finding], services: list[NetworkService]) -> tuple[int, str]:
    """Calculate a simple risk score from findings and exposed services."""
    score = sum(SEVERITY_POINTS.get(finding.severity, 0) for finding in findings)

    # Open services are not always vulnerabilities, but they increase exposure.
    score += min(len(services) * 3, 15)
    score = min(score, 100)

    if score >= 75:
        return score, "critical"
    if score >= 50:
        return score, "high"
    if score >= 25:
        return score, "medium"
    if score > 0:
        return score, "low"
    return score, "informational"
