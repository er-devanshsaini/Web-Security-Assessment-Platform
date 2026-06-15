from datetime import datetime, timezone

import httpx
from sqlmodel import Session

from app.database.models import Finding, NetworkService, Scan
from app.services.http_scanner import fetch_website
from app.services.nmap_scanner import run_nmap_scan
from app.services.reporting import generate_pdf_report
from app.services.risk import calculate_risk_score
from app.services.url_utils import get_hostname, normalize_url
from app.services.web_checks import analyze_http_security


def run_scan(session: Session, scan: Scan, include_network_scan: bool) -> Scan:
    """Run all enabled scan phases and save the results."""
    scan.status = "running"
    session.add(scan)
    session.commit()
    session.refresh(scan)

    findings: list[Finding] = []
    services: list[NetworkService] = []

    try:
        normalized_url = normalize_url(scan.target_url)
        hostname = get_hostname(normalized_url)
        observation = fetch_website(normalized_url)

        scan.normalized_url = observation.final_url
        scan.hostname = hostname
        scan.http_status_code = observation.status_code
        scan.uses_https = observation.uses_https
        scan.redirects_to_https = observation.redirects_to_https

        findings = analyze_http_security(scan.id, observation)

        if include_network_scan:
            services, nmap_error = run_nmap_scan(scan.id, hostname)
            if nmap_error:
                findings.append(
                    Finding(
                        scan_id=scan.id,
                        title="Network scan note",
                        category="Network Reconnaissance",
                        severity="info",
                        description="Nmap did not produce open service results.",
                        evidence=nmap_error,
                        recommendation="Install Nmap and confirm authorization before running network scans.",
                        owasp_reference="Security Testing Process",
                    )
                )

        for finding in findings:
            session.add(finding)
        for service in services:
            session.add(service)

        score, level = calculate_risk_score(findings, services)
        scan.risk_score = score
        scan.risk_level = level
        scan.status = "completed"
        scan.completed_at = datetime.now(timezone.utc)

        report_path = generate_pdf_report(scan, findings, services)
        scan.report_path = report_path

    except httpx.HTTPError as error:
        scan.status = "failed"
        scan.error_message = f"HTTP request failed: {error}"
    except Exception as error:
        scan.status = "failed"
        scan.error_message = f"Unexpected scan error: {error}"

    session.add(scan)
    session.commit()
    session.refresh(scan)
    return scan
