from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from backend.app.core.config import settings
from backend.app.database.models import Finding, NetworkService, Scan


def generate_pdf_report(scan: Scan, findings: list[Finding], services: list[NetworkService]) -> str:
    """Generate a practical PDF report for recruiters and technical reviewers."""
    report_dir = Path(settings.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / f"scan-{scan.id}-report.pdf"
    styles = getSampleStyleSheet()
    document = SimpleDocTemplate(str(report_path), pagesize=letter)

    story = [
        Paragraph("Security Assessment Report", styles["Title"]),
        Paragraph(f"Target: {scan.target_url}", styles["Normal"]),
        Paragraph(f"Risk: {scan.risk_level.upper()} ({scan.risk_score}/100)", styles["Normal"]),
        Spacer(1, 12),
        Paragraph("Executive Summary", styles["Heading2"]),
        Paragraph(build_executive_summary(scan, findings, services), styles["BodyText"]),
        Spacer(1, 12),
        Paragraph("Technical Findings", styles["Heading2"]),
    ]

    if not findings:
        story.append(Paragraph("No web security findings were recorded.", styles["BodyText"]))

    for finding in findings:
        story.extend(
            [
                Paragraph(f"{finding.severity.upper()}: {finding.title}", styles["Heading3"]),
                Paragraph(f"Category: {finding.category}", styles["BodyText"]),
                Paragraph(f"Evidence: {finding.evidence}", styles["BodyText"]),
                Paragraph(f"Recommendation: {finding.recommendation}", styles["BodyText"]),
                Spacer(1, 8),
            ]
        )

    story.append(Paragraph("Network Services", styles["Heading2"]))
    if not services:
        story.append(Paragraph("No open services were recorded or Nmap was skipped.", styles["BodyText"]))

    for service in services:
        label = f"{service.port}/{service.protocol} {service.service_name}"
        if service.product:
            label = f"{label} - {service.product} {service.version or ''}"
        story.append(Paragraph(label, styles["BodyText"]))

    document.build(story)
    return str(report_path)


def build_executive_summary(scan: Scan, findings: list[Finding], services: list[NetworkService]) -> str:
    return (
        f"The assessment identified {len(findings)} web security findings and "
        f"{len(services)} open network services. The calculated risk level is "
        f"{scan.risk_level}. Prioritize high and medium severity issues first, "
        "especially transport security, missing browser protections, and exposed services."
    )
