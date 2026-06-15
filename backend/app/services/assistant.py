from collections import Counter

from backend.app.database.models import Finding, NetworkService, Scan


def explain_scan(scan: Scan, findings: list[Finding], services: list[NetworkService]) -> tuple[str, list[str]]:
    """Create deterministic assistant-style guidance without requiring an API key."""
    severity_counts = Counter(finding.severity for finding in findings)
    top_categories = Counter(finding.category for finding in findings).most_common(3)

    category_text = ", ".join(category for category, _ in top_categories) or "no major categories"
    summary = (
        f"Scan {scan.id} for {scan.hostname or scan.target_url} is rated {scan.risk_level} "
        f"with a score of {scan.risk_score}/100. Findings are concentrated around "
        f"{category_text}. Severity mix: {dict(severity_counts)}. "
        f"{len(services)} network services were recorded."
    )

    remediation_plan: list[str] = []

    for finding in sorted(findings, key=lambda item: severity_rank(item.severity), reverse=True)[:5]:
        remediation_plan.append(f"{finding.title}: {finding.recommendation}")

    if services:
        remediation_plan.append("Review each open service and close anything not required for business use.")

    if not remediation_plan:
        remediation_plan.append("Keep monitoring headers, TLS settings, dependencies, and exposed services.")

    return summary, remediation_plan


def severity_rank(severity: str) -> int:
    return {"critical": 5, "high": 4, "medium": 3, "low": 2, "info": 1}.get(severity, 0)
