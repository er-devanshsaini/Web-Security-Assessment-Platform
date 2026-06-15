# Phase 7: React Dashboard

## Objective

Build a dashboard to start scans, view history, inspect findings, visualize risk,
read assistant guidance, and download reports.

## What Recruiters Learn

- You can build a complete user-facing workflow.
- You understand how security tools are used by analysts.
- You can connect a frontend to backend APIs cleanly.

## Files And Modules

- `frontend/src/main.jsx`: dashboard UI and API calls.
- `frontend/src/styles.css`: Tailwind entry and small global styles.
- `frontend/package.json`: React, Vite, lucide icons, and Recharts dependencies.

## Code Notes

- `loadDashboard` fetches scans and stats together.
- `startScan` posts a target URL to the backend.
- `loadScan` fetches findings and assistant output.
- Recharts displays risk distribution.
- Lucide icons make actions easy to scan without heavy text.

## Interview Questions

1. How does the frontend know a scan completed?
2. Why keep API base URL in one constant?
3. What dashboard metrics matter to a security analyst?
4. How would you add authentication to this dashboard?

## Common Mistakes

- Building a landing page instead of the actual tool.
- Showing findings without severity or remediation.
- Forgetting loading and error states.

## Security Considerations

- CORS is limited to local frontend origins.
- The dashboard reminds users to run only authorized Nmap scans.
- Production deployments should add authentication and role-based access.

## Resume Bullet Points

- Built a React security dashboard for scan management, findings review, charts, and PDF downloads.
- Connected FastAPI endpoints to a practical analyst workflow.

## Expected Recruiter Impression

This phase demonstrates full-stack ability and product thinking.

## GitHub Commit Message

```text
feat: build react dashboard for scan results
```
