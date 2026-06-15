# Phase 2: Website Scanning And HTTP Analysis

## Objective

Add a scanning module that fetches a target website, records HTTP status,
captures response headers, detects missing browser security headers, and checks
whether the final response uses HTTPS.

## What Recruiters Learn

- You understand HTTP request and response flow.
- You can safely use an HTTP client with timeouts and TLS verification.
- You can translate raw HTTP observations into security findings.

## Files And Modules

- `backend/app/services/http_scanner.py`: performs the HTTP request and stores observations.
- `backend/app/services/web_checks.py`: turns headers, HTTPS state, and cookies into findings.
- `backend/app/services/url_utils.py`: normalizes URLs and extracts hostnames.
- `backend/app/api/routes/scans.py`: exposes scan creation and result endpoints.

## Code Notes

- `httpx.Client(..., follow_redirects=True)` follows redirects like a browser.
- `verify=True` keeps TLS certificate validation enabled.
- Header names are lowercased because HTTP header casing is not meaningful.
- `find_missing_security_headers` compares the response to an expected baseline.

## Interview Questions

1. Why do scanners need request timeouts?
2. Why are HTTP header names normalized to lowercase?
3. What is the difference between requested URL and final URL?
4. Why is HTTPS enforcement important?

## Common Mistakes

- Disabling TLS verification to avoid certificate errors.
- Treating every missing header as the same severity.
- Forgetting that redirects can change the final security posture.

## Security Considerations

- The scanner uses a clear User-Agent.
- It performs a simple GET request, not intrusive payload testing.
- Users should only scan authorized systems.

## Resume Bullet Points

- Built HTTP scanning logic to collect response metadata and detect missing security headers.
- Implemented HTTPS enforcement checks using final redirect destination analysis.

## Expected Recruiter Impression

This phase shows practical web security fundamentals and responsible scanner behavior.

## GitHub Commit Message

```text
feat: add website scanning and security header checks
```
