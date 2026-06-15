# Phase 4: OWASP-Oriented Security Checks

## Objective

Map practical checks to OWASP Top 10 themes: CSP, HSTS, insecure cookies,
authentication exposure, and security misconfiguration.

## What Recruiters Learn

- You can connect findings to OWASP categories.
- You know common browser-side hardening controls.
- You can explain issues in both technical and remediation language.

## Files And Modules

- `backend/app/services/web_checks.py`: contains OWASP-style checks.
- `backend/app/database/models.py`: stores category, severity, evidence, and recommendation.

## Code Notes

- Missing CSP maps to security misconfiguration and XSS impact reduction.
- Missing HSTS maps to transport security weaknesses.
- Missing `HttpOnly`, `Secure`, and `SameSite` flags map to session risk.
- `WWW-Authenticate` is recorded as informational because it may be expected.

## Interview Questions

1. How does CSP reduce XSS impact?
2. What does HSTS protect against?
3. Why should session cookies use HttpOnly?
4. Why is evidence important in a vulnerability report?

## Common Mistakes

- Reporting findings without evidence.
- Giving generic recommendations that developers cannot act on.
- Calling informational observations vulnerabilities.

## Security Considerations

- Findings are framed as configuration risks, not exploitation claims.
- Recommendations avoid destructive or intrusive testing.
- Evidence is stored without collecting response bodies.

## Resume Bullet Points

- Implemented OWASP-aligned checks for headers, TLS behavior, cookies, and authentication signals.
- Produced findings with evidence, severity, category, and remediation guidance.

## Expected Recruiter Impression

This phase shows you can think like a product security reviewer, not just a tool runner.

## GitHub Commit Message

```text
feat: add owasp-based web security checks
```
