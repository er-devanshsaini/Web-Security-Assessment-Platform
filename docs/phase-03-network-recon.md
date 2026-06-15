# Phase 3: Network Reconnaissance With Nmap

## Objective

Integrate Nmap to discover common open TCP ports and identify exposed services.

## What Recruiters Learn

- You know how to call trusted security tools from Python.
- You understand open ports and service exposure.
- You can parse structured XML output instead of scraping terminal text.

## Files And Modules

- `backend/app/services/nmap_scanner.py`: runs Nmap and parses XML results.
- `backend/app/database/models.py`: stores `NetworkService` rows.
- `backend/app/api/routes/scans.py`: lets users enable network scans.

## Code Notes

- `shutil.which("nmap")` checks whether Nmap is installed.
- `-sV` asks Nmap for service identification.
- `--top-ports 20` keeps the default scan small for a portfolio project.
- `-oX -` returns XML to stdout for reliable parsing.

## Interview Questions

1. What is the difference between port discovery and service detection?
2. Why parse XML instead of plain text?
3. What legal permission is needed before running Nmap?
4. Why can an open port be a risk without being a vulnerability?

## Common Mistakes

- Running aggressive scans by default.
- Scanning localhost or internal networks accidentally.
- Assuming every open port means exploitation is possible.

## Security Considerations

- Nmap is optional and must be explicitly enabled.
- Obvious local/private-looking hostnames are skipped by default.
- Timeouts prevent scans from hanging the backend indefinitely.

## Resume Bullet Points

- Integrated Nmap service detection with structured XML parsing.
- Stored open service inventory for later risk scoring and reporting.

## Expected Recruiter Impression

This phase connects networking knowledge with backend engineering discipline.

## GitHub Commit Message

```text
feat: integrate optional nmap reconnaissance
```
