from app.database.models import Finding
from app.services.http_scanner import HttpObservation, SECURITY_HEADERS, find_missing_security_headers


def analyze_http_security(scan_id: int, observation: HttpObservation) -> list[Finding]:
    """Convert HTTP observations into application security findings."""
    findings: list[Finding] = []

    for header in find_missing_security_headers(observation.headers):
        severity = "medium" if header in {"content-security-policy", "strict-transport-security"} else "low"
        findings.append(
            Finding(
                scan_id=scan_id,
                title=f"Missing {header} header",
                category="Security Headers",
                severity=severity,
                description=SECURITY_HEADERS[header],
                evidence=f"{header} was not present in the HTTP response headers.",
                recommendation=f"Configure the application or reverse proxy to send {header}.",
                owasp_reference="OWASP Top 10 A05: Security Misconfiguration",
            )
        )

    if not observation.uses_https:
        findings.append(
            Finding(
                scan_id=scan_id,
                title="HTTPS is not enforced",
                category="Transport Security",
                severity="high",
                description="The final URL did not use HTTPS, which can expose traffic to interception.",
                evidence=f"Final URL was {observation.final_url}.",
                recommendation="Redirect HTTP to HTTPS and use a valid TLS certificate.",
                owasp_reference="OWASP Top 10 A02: Cryptographic Failures",
            )
        )

    if observation.uses_https and "strict-transport-security" not in observation.headers:
        findings.append(
            Finding(
                scan_id=scan_id,
                title="HSTS is missing on HTTPS response",
                category="Transport Security",
                severity="medium",
                description="Without HSTS, browsers may still attempt insecure HTTP connections later.",
                evidence="Strict-Transport-Security header was not found.",
                recommendation="Add Strict-Transport-Security with an appropriate max-age value.",
                owasp_reference="OWASP Top 10 A05: Security Misconfiguration",
            )
        )

    if "www-authenticate" in observation.headers:
        findings.append(
            Finding(
                scan_id=scan_id,
                title="Basic authentication challenge detected",
                category="Authentication",
                severity="info",
                description="The site returned an authentication challenge. This may be expected for admin areas.",
                evidence=f"WWW-Authenticate: {observation.headers['www-authenticate']}",
                recommendation="Avoid exposing admin panels publicly and require MFA for sensitive access.",
                owasp_reference="OWASP Top 10 A07: Identification and Authentication Failures",
            )
        )

    findings.extend(analyze_cookie_security(scan_id, observation.set_cookie_headers, observation.uses_https))
    return findings


def analyze_cookie_security(scan_id: int, cookie_headers: list[str], uses_https: bool) -> list[Finding]:
    findings: list[Finding] = []

    for cookie_header in cookie_headers:
        lowered = cookie_header.lower()
        cookie_name = cookie_header.split("=", 1)[0]

        if "httponly" not in lowered:
            findings.append(
                Finding(
                    scan_id=scan_id,
                    title=f"Cookie {cookie_name} is missing HttpOnly",
                    category="Session Management",
                    severity="medium",
                    description="Cookies without HttpOnly can be read by injected JavaScript.",
                    evidence=cookie_header,
                    recommendation="Set the HttpOnly flag on session and authentication cookies.",
                    owasp_reference="OWASP Top 10 A03: Injection",
                )
            )

        if uses_https and "secure" not in lowered:
            findings.append(
                Finding(
                    scan_id=scan_id,
                    title=f"Cookie {cookie_name} is missing Secure",
                    category="Session Management",
                    severity="medium",
                    description="Cookies without Secure may be sent over plain HTTP.",
                    evidence=cookie_header,
                    recommendation="Set the Secure flag for cookies used on HTTPS sites.",
                    owasp_reference="OWASP Top 10 A02: Cryptographic Failures",
                )
            )

        if "samesite" not in lowered:
            findings.append(
                Finding(
                    scan_id=scan_id,
                    title=f"Cookie {cookie_name} is missing SameSite",
                    category="Session Management",
                    severity="low",
                    description="SameSite helps reduce cross-site request forgery risk.",
                    evidence=cookie_header,
                    recommendation="Set SameSite=Lax or SameSite=Strict unless cross-site behavior is required.",
                    owasp_reference="OWASP Top 10 A01: Broken Access Control",
                )
            )

    return findings
