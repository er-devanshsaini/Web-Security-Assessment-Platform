from backend.app.database.models import Finding, NetworkService
from backend.app.services.http_scanner import HttpObservation, find_missing_security_headers
from backend.app.services.nmap_scanner import parse_nmap_xml
from backend.app.services.risk import calculate_risk_score
from backend.app.services.web_checks import analyze_cookie_security, analyze_http_security


def test_missing_security_headers_are_detected() -> None:
    headers = {"content-security-policy": "default-src 'self'"}

    missing_headers = find_missing_security_headers(headers)

    assert "strict-transport-security" in missing_headers
    assert "x-frame-options" in missing_headers
    assert "content-security-policy" not in missing_headers


def test_http_security_analysis_creates_findings() -> None:
    observation = HttpObservation(
        requested_url="http://example.com",
        final_url="http://example.com",
        status_code=200,
        headers={},
        set_cookie_headers=[],
        uses_https=False,
        redirects_to_https=False,
    )

    findings = analyze_http_security(scan_id=1, observation=observation)

    titles = [finding.title for finding in findings]
    assert "HTTPS is not enforced" in titles
    assert any("Missing content-security-policy" in title for title in titles)


def test_cookie_security_flags_are_checked() -> None:
    findings = analyze_cookie_security(
        scan_id=1,
        cookie_headers=["sessionid=abc123; Path=/"],
        uses_https=True,
    )

    assert len(findings) == 3
    assert {finding.severity for finding in findings} == {"low", "medium"}


def test_risk_score_uses_findings_and_services() -> None:
    findings = [
        Finding(
            scan_id=1,
            title="Missing HSTS",
            category="Transport Security",
            severity="medium",
            description="Missing header",
            evidence="No HSTS",
            recommendation="Add HSTS",
        ),
        Finding(
            scan_id=1,
            title="HTTPS not enforced",
            category="Transport Security",
            severity="high",
            description="HTTP allowed",
            evidence="http://",
            recommendation="Redirect to HTTPS",
        ),
    ]
    services = [NetworkService(scan_id=1, port=443, service_name="https")]

    score, level = calculate_risk_score(findings, services)

    assert score == 33
    assert level == "medium"


def test_nmap_xml_parser_extracts_open_services() -> None:
    xml_output = """
    <nmaprun>
      <host>
        <ports>
          <port protocol="tcp" portid="80">
            <state state="open" />
            <service name="http" product="nginx" version="1.24" />
          </port>
          <port protocol="tcp" portid="22">
            <state state="closed" />
          </port>
        </ports>
      </host>
    </nmaprun>
    """

    services = parse_nmap_xml(scan_id=4, xml_output=xml_output)

    assert len(services) == 1
    assert services[0].port == 80
    assert services[0].service_name == "http"
